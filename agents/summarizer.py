"""Summarization agent — creates a concise summary of the support interaction."""
from __future__ import annotations
import json
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import OPENAI_API_KEY, LLM_MODEL, CONVERSATIONS_FILE
from agents.state import SupportState

_llm = ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0)

_SYSTEM_PROMPT = """You are a support case summarizer.
Given a conversation between a customer and a support AI, write a concise case summary.

The summary must include:
1. **Issue**: What was the customer's problem?
2. **Actions Taken**: What did the support assistant do? (lookups, troubleshooting steps provided, etc.)
3. **Resolution**: Was the issue resolved? What was the outcome?
4. **Follow-up Needed**: Any open items or next steps for human agents?

Keep the summary under 200 words. Be factual and specific."""


def summarize_node(state: SupportState) -> SupportState:
    """LangGraph node: summarize the conversation and persist it."""
    history = state.get("conversation_history", [])
    intent = state.get("intent", "general")
    final_response = state.get("final_response", "")
    ticket_id = state.get("ticket_id", "")
    confidence = state.get("confidence_score", 0.0)

    if not history and not final_response:
        return {**state, "conversation_summary": "No conversation to summarize."}

    # Build conversation text
    conv_text = ""
    for turn in history:
        role = "Customer" if turn.get("role") == "user" else "Support AI"
        conv_text += f"\n{role}: {turn['content']}"
    if final_response:
        conv_text += f"\nSupport AI: {final_response}"

    try:
        resp = _llm.invoke([
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=f"Conversation:\n{conv_text}"),
        ])
        summary = resp.content
    except Exception:
        summary = (
            f"Session {state.get('session_id', 'unknown')} | "
            f"Intent: {intent} | "
            f"Confidence: {confidence:.0%} | "
            f"Ticket: {ticket_id or 'None'}"
        )

    # Persist conversation record
    _persist_conversation(state, summary)

    return {**state, "conversation_summary": summary}


def _persist_conversation(state: SupportState, summary: str):
    """Save conversation summary to the conversations JSON file."""
    try:
        existing = {}
        if CONVERSATIONS_FILE.exists():
            existing = json.loads(CONVERSATIONS_FILE.read_text())

        session_id = state.get("session_id", "unknown")
        existing[session_id] = {
            "session_id": session_id,
            "customer_id": state.get("customer_id", ""),
            "customer_name": state.get("customer_name", ""),
            "intent": state.get("intent", ""),
            "confidence_score": state.get("confidence_score", 0.0),
            "confidence_label": state.get("confidence_label", ""),
            "escalated": state.get("should_escalate", False),
            "ticket_id": state.get("ticket_id"),
            "summary": summary,
            "turn_count": len(state.get("conversation_history", [])),
            "timestamp": datetime.utcnow().isoformat(),
        }
        CONVERSATIONS_FILE.write_text(json.dumps(existing, indent=2))
    except Exception:
        pass  # Non-critical; don't break the flow
