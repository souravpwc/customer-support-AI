"""
LangGraph orchestrator — wires all agents into a stateful workflow.

Flow:
  classify → retrieve → integrate → (troubleshoot if needed) → generate → (escalate if needed) → summarize
"""
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal

from langgraph.graph import StateGraph, END

from agents.state import SupportState
from agents.classifier import classify_node
from agents.retriever import retrieve_node
from agents.integrator import integrate_node
from agents.troubleshooter import troubleshoot_node
from agents.response_generator import generate_response_node
from agents.summarizer import summarize_node
from agents.escalation import escalate_node
from governance.audit_logger import get_audit_logger
from governance.data_masker import get_masker

_audit = get_audit_logger()
_masker = get_masker()


# ── Routing functions ──────────────────────────────────────────────────────────

def _route_after_classify(state: SupportState) -> Literal["retrieve", "integrate", "generate"]:
    """After classification: some intents skip retrieval and go straight to integration."""
    intent = state.get("intent", "general_faq")
    entities = state.get("entities", {})

    # Order status with an order ID → integrate directly (no KB needed)
    if intent == "order_status" and entities.get("order_id"):
        return "integrate"

    # All others benefit from retrieval first
    return "retrieve"


def _route_after_retrieve(state: SupportState) -> Literal["integrate", "troubleshoot"]:
    """After retrieval: troubleshooting goes to troubleshooter, others go to integrate/generate."""
    intent = state.get("intent", "general_faq")
    if intent == "troubleshooting":
        return "troubleshoot"
    return "integrate"


def _route_after_generate(state: SupportState) -> Literal["escalate", "summarize"]:
    """After response generation: escalate if needed, else summarize."""
    if state.get("should_escalate"):
        return "escalate"
    return "summarize"


# ── Audit wrapper nodes ───────────────────────────────────────────────────────

def _audit_classify(state: SupportState) -> SupportState:
    result = classify_node(state)
    masked_msg, _ = _masker.mask(state.get("user_message", ""))
    _audit.log(
        "intent_classified",
        session_id=state.get("session_id", ""),
        data={"intent": result.get("intent"), "entities": result.get("entities", {}),
              "message_preview": masked_msg[:100]},
        customer_id=state.get("customer_id"),
        intent=result.get("intent"),
        confidence=result.get("intent_confidence"),
    )
    return result


def _audit_retrieve(state: SupportState) -> SupportState:
    result = retrieve_node(state)
    _audit.log(
        "docs_retrieved",
        session_id=state.get("session_id", ""),
        data={"count": len(result.get("retrieved_docs", [])),
              "top_score": max(result.get("retrieval_scores", [0]), default=0)},
        customer_id=state.get("customer_id"),
        intent=state.get("intent"),
    )
    return result


def _audit_integrate(state: SupportState) -> SupportState:
    result = integrate_node(state)
    _audit.log(
        "api_called",
        session_id=state.get("session_id", ""),
        data={"intent": state.get("intent"), "api_success": result.get("api_success")},
        customer_id=state.get("customer_id"),
        intent=state.get("intent"),
    )
    return result


def _audit_generate(state: SupportState) -> SupportState:
    result = generate_response_node(state)
    masked_resp, _ = _masker.mask(result.get("final_response", ""))
    _audit.log(
        "response_generated",
        session_id=state.get("session_id", ""),
        data={
            "confidence_score": result.get("confidence_score"),
            "confidence_label": result.get("confidence_label"),
            "guardrail_violations": result.get("guardrail_violations", []),
            "response_length": len(result.get("final_response", "")),
            "needs_review": result.get("needs_review"),
        },
        customer_id=state.get("customer_id"),
        intent=state.get("intent"),
        confidence=result.get("confidence_score"),
    )
    if result.get("guardrail_violations"):
        _audit.log(
            "guardrail_triggered",
            session_id=state.get("session_id", ""),
            data={"violations": result.get("guardrail_violations", [])},
            customer_id=state.get("customer_id"),
        )
    return result


# ── Build the LangGraph ───────────────────────────────────────────────────────

def _build_graph() -> Any:
    graph = StateGraph(SupportState)

    graph.add_node("classify", _audit_classify)
    graph.add_node("retrieve", _audit_retrieve)
    graph.add_node("integrate", _audit_integrate)
    graph.add_node("troubleshoot", troubleshoot_node)
    graph.add_node("generate", _audit_generate)
    graph.add_node("escalate", escalate_node)
    graph.add_node("summarize", summarize_node)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        _route_after_classify,
        {"retrieve": "retrieve", "integrate": "integrate", "generate": "generate"},
    )
    graph.add_conditional_edges(
        "retrieve",
        _route_after_retrieve,
        {"troubleshoot": "troubleshoot", "integrate": "integrate"},
    )
    graph.add_edge("troubleshoot", "integrate")
    graph.add_edge("integrate", "generate")
    graph.add_conditional_edges(
        "generate",
        _route_after_generate,
        {"escalate": "escalate", "summarize": "summarize"},
    )
    graph.add_edge("escalate", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


_COMPILED_GRAPH = None


def _get_graph():
    global _COMPILED_GRAPH
    if _COMPILED_GRAPH is None:
        _COMPILED_GRAPH = _build_graph()
    return _COMPILED_GRAPH


# ── Public API ────────────────────────────────────────────────────────────────

class SupportOrchestrator:
    """Entry point for the TechNova support agent system."""

    def process_message(
        self,
        user_message: str,
        session_id: str | None = None,
        customer_id: str = "",
        customer_name: str = "",
        conversation_history: List[Dict[str, str]] | None = None,
        force_escalate: bool = False,
    ) -> SupportState:
        """Process a single customer message through the full agent pipeline."""
        if not session_id:
            session_id = uuid.uuid4().hex

        _audit.log(
            "message_received",
            session_id=session_id,
            data={"message_length": len(user_message)},
            customer_id=customer_id or None,
        )

        initial_state: SupportState = {
            "session_id": session_id,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "customer_tier": "Standard",
            "user_message": user_message,
            "conversation_history": conversation_history or [],
            "intent": "",
            "intent_confidence": 0.0,
            "entities": {},
            "retrieved_docs": [],
            "retrieval_scores": [],
            "order_result": None,
            "warranty_result": None,
            "crm_result": None,
            "api_success": None,
            "troubleshooting_steps": [],
            "troubleshooting_summary": "",
            "draft_response": "",
            "final_response": "",
            "guardrail_violations": [],
            "confidence_score": 0.0,
            "confidence_label": "medium",
            "needs_review": False,
            "should_escalate": force_escalate,
            "escalation_reason": "Customer requested human agent" if force_escalate else "",
            "ticket_id": None,
            "ticket_priority": "Medium",
            "conversation_summary": "",
            "audit_events": [],
            "error": None,
        }

        graph = _get_graph()
        final_state = graph.invoke(initial_state)
        return final_state

    def start_session(self, customer_id: str = "", customer_name: str = "") -> str:
        """Create a new session ID and log session start."""
        session_id = uuid.uuid4().hex
        _audit.log(
            "session_start",
            session_id=session_id,
            data={"timestamp": datetime.utcnow().isoformat()},
            customer_id=customer_id or None,
        )
        return session_id
