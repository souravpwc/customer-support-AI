"""Classification agent — determines intent and extracts entities."""
from __future__ import annotations
import json
import re
from typing import Any, Dict, Tuple

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import OPENAI_API_KEY, LLM_MODEL, INTENTS, INTENT_DESCRIPTIONS
from agents.state import SupportState

_llm = ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0)

_SYSTEM_PROMPT = f"""You are an intent classifier for TechNova customer support.

Classify the user message into EXACTLY one of these intents:
{json.dumps(INTENT_DESCRIPTIONS, indent=2)}

Also extract any entities mentioned:
- order_id: TechNova order numbers (format: TN-XXXXXX or plain 6-digit numbers)
- service_tag: Device service tags (format: SVC-TAG-XXX or any code that looks like a device serial/tag)
- product_name: Device model names (e.g. NovaBook XPS 15, WorkStation Pro T9)
- issue_type: The type of technical issue if troubleshooting
- customer_email: Email addresses

Respond with ONLY valid JSON in this exact format:
{{
  "intent": "<intent_label>",
  "confidence": <0.0-1.0>,
  "entities": {{
    "order_id": null,
    "service_tag": null,
    "product_name": null,
    "issue_type": null,
    "customer_email": null
  }},
  "reasoning": "<brief explanation>"
}}"""


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM output that may have extra text."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {}


def classify_node(state: SupportState) -> SupportState:
    """LangGraph node: classify user intent and extract entities."""
    user_message = state.get("user_message", "")
    history = state.get("conversation_history", [])

    # Build context from recent history
    context_msgs = []
    for turn in history[-4:]:
        role = turn.get("role", "user")
        context_msgs.append(f"{role.upper()}: {turn['content']}")
    context = "\n".join(context_msgs) if context_msgs else "No prior context."

    prompt = f"""Conversation so far:
{context}

Current user message:
{user_message}

Classify the CURRENT user message."""

    try:
        resp = _llm.invoke([
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ])
        result = _extract_json(resp.content)
    except Exception as e:
        result = {}

    intent = result.get("intent", "general_faq")
    if intent not in INTENTS:
        intent = "general_faq"
    confidence = float(result.get("confidence", 0.5))
    entities = result.get("entities", {}) or {}

    # Regex fallback for entities not caught by LLM
    if not entities.get("order_id"):
        m = re.search(r"\bTN-\d{6}\b|\b\d{6}\b", user_message, re.IGNORECASE)
        if m:
            num = m.group()
            entities["order_id"] = num if num.upper().startswith("TN-") else f"TN-{num}"

    if not entities.get("service_tag"):
        m = re.search(r"\bSVC-TAG-\d{3}\b", user_message, re.IGNORECASE)
        if m:
            entities["service_tag"] = m.group().upper()

    # Keyword fallback / reinforcement for explicit escalation requests.
    # The LLM sometimes mis-routes clear "talk to a human" messages, so we
    # double-check with a regex and upgrade the intent if needed.
    _ESCALATION_PATTERNS = (
        r"\b(human|live|real)\s+(agent|person|support|rep(resentative)?)\b",
        r"\bspeak\s+(to|with)\s+(a|an)?\s*(human|person|agent|manager)\b",
        r"\btalk\s+(to|with)\s+(a|an)?\s*(human|person|agent|manager)\b",
        r"\bescalat(e|ion|ed)\b",
        r"\btransfer\s+me\b",
        r"\bconnect\s+me\s+(to|with)\b",
    )
    if any(re.search(p, user_message, re.IGNORECASE) for p in _ESCALATION_PATTERNS):
        intent = "escalation_request"
        confidence = max(confidence, 0.9)

    updates: dict = {
        "intent": intent,
        "intent_confidence": confidence,
        "entities": {k: v for k, v in entities.items() if v},
    }

    # CRITICAL: when the customer explicitly asks for a human, force the
    # escalation branch so a ticket is created and the admin dashboard
    # picks it up. Without this, escalation only fires when the response
    # confidence falls below ESCALATION_THRESHOLD, which rarely happens
    # for a polite "please escalate" reply.
    if intent == "escalation_request":
        updates["should_escalate"] = True
        updates["escalation_reason"] = (
            state.get("escalation_reason")
            or "Customer explicitly requested a human agent"
        )

    return {**state, **updates}
