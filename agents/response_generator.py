"""Response generation agent — produces the final customer-facing reply."""
from __future__ import annotations
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import OPENAI_API_KEY, LLM_MODEL, COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE
from agents.state import SupportState
from governance.guardrails import get_guardrails
from governance.confidence_scorer import get_scorer, has_fallback
from integrations.order_api import OrderAPI
from integrations.warranty_api import WarrantyAPI

_llm = ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0.3)
_guardrails = get_guardrails()
_scorer = get_scorer()
_order_api = OrderAPI()
_warranty_api = WarrantyAPI()

_SYSTEM_PROMPT = f"""You are the {COMPANY_NAME} AI Support Assistant — expert, friendly, and concise.

Persona guidelines:
- Address the customer by name if known, otherwise use a friendly greeting.
- Be warm but professional. Never be dismissive.
- Use markdown formatting: **bold** for key info, numbered lists for steps.
- Always acknowledge the customer's issue before diving into the solution.
- Cite knowledge base sources naturally (e.g. "According to our warranty policy...").
- If an API result is provided, use it to give specific, personalized information.
- If you cannot fully resolve the issue, clearly explain next steps and offer to escalate.
- End with a follow-up question or offer of additional help.
- Do NOT make up product specs, prices, or policies not in the provided context.
- Company support: {SUPPORT_EMAIL} | {SUPPORT_PHONE}"""


def _build_context(state: SupportState) -> str:
    """Build a rich context string for the response generator."""
    parts: List[str] = []

    customer_name = state.get("customer_name", "")
    if customer_name:
        parts.append(f"Customer: {customer_name} ({state.get('customer_tier', 'Standard')} tier)")

    intent = state.get("intent", "")
    parts.append(f"Intent: {intent}")

    # Order result
    if order_result := state.get("order_result"):
        if order_result.get("success"):
            order = order_result.get("order") or order_result.get("orders", [{}])[0]
            parts.append(f"\n**Order Information:**\n{_order_api.format_order_summary(order)}")
        else:
            parts.append(f"\n**Order Lookup:** {order_result.get('error', 'Not found')}")

    # Warranty result
    if warranty_result := state.get("warranty_result"):
        if warranty_result.get("success"):
            warranty = warranty_result["warranty"]
            parts.append(f"\n**Warranty Information:**\n{_warranty_api.format_warranty_summary(warranty)}")
        else:
            parts.append(f"\n**Warranty Lookup:** {warranty_result.get('error', 'Not found')}")

    # Troubleshooting steps
    if steps := state.get("troubleshooting_steps"):
        formatted = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        parts.append(f"\n**Troubleshooting Steps:**\n{formatted}")

    # KB content
    docs = state.get("retrieved_docs", [])[:3]
    if docs:
        kb_parts = []
        for doc in docs:
            kb_parts.append(f"[{doc['category'].upper()}] {doc['title']}:\n{doc['content'][:600]}")
        parts.append(f"\n**Knowledge Base Context:**\n{'---'.join(kb_parts)}")

    return "\n".join(parts)


def generate_response_node(state: SupportState) -> SupportState:
    """LangGraph node: generate the final customer response."""
    user_message = state.get("user_message", "")
    history = state.get("conversation_history", [])
    intent = state.get("intent", "general_faq")

    context = _build_context(state)

    # Build conversation messages for LLM
    messages = [SystemMessage(content=_SYSTEM_PROMPT)]

    # Add recent history (up to 6 turns)
    for turn in history[-6:]:
        role = turn.get("role", "user")
        if role == "user":
            messages.append(HumanMessage(content=turn["content"]))
        else:
            from langchain_core.messages import AIMessage
            messages.append(AIMessage(content=turn["content"]))

    # Final user message with context
    full_prompt = f"""Context for your response:
{context}

Customer's message: {user_message}

Generate a helpful, complete response."""

    messages.append(HumanMessage(content=full_prompt))

    try:
        resp = _llm.invoke(messages)
        draft = resp.content
    except Exception as e:
        draft = (
            f"I apologize, I'm experiencing a temporary issue. "
            f"Please contact us at {SUPPORT_EMAIL} or {SUPPORT_PHONE} for immediate assistance."
        )

    # Run guardrails
    gr = _guardrails.check(draft, intent=intent)
    final_response = gr.sanitized_response

    # Score confidence
    retrieval_scores = state.get("retrieval_scores", [])
    api_success = state.get("api_success")
    intent_conf = state.get("intent_confidence", 0.5)

    conf_result = _scorer.score(
        intent=intent,
        retrieval_scores=retrieval_scores,
        api_success=api_success,
        intent_confidence=intent_conf,
        response_length=len(final_response),
        has_fallback_phrases=has_fallback(final_response),
    )

    return {
        **state,
        "draft_response": draft,
        "final_response": final_response,
        "guardrail_violations": gr.violations,
        "confidence_score": conf_result.score,
        "confidence_label": conf_result.label,
        "needs_review": conf_result.needs_review,
        "should_escalate": state.get("should_escalate", False) or conf_result.needs_escalation,
        "escalation_reason": (
            state.get("escalation_reason", "")
            or (f"Low confidence ({conf_result.score:.0%})" if conf_result.needs_escalation else "")
        ),
    }
