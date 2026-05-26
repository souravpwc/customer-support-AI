"""LangGraph state definition for the TechNova support workflow."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypedDict


class SupportState(TypedDict, total=False):
    # ── Session metadata ──────────────────────────────────────────────────────
    session_id: str
    customer_id: str
    customer_name: str
    customer_tier: str

    # ── Conversation ──────────────────────────────────────────────────────────
    user_message: str
    conversation_history: List[Dict[str, str]]  # [{role, content}]

    # ── Classification ────────────────────────────────────────────────────────
    intent: str
    intent_confidence: float
    entities: Dict[str, Any]  # e.g. {"order_id": "TN-100001", "service_tag": "SVC-001"}

    # ── Retrieval ─────────────────────────────────────────────────────────────
    retrieved_docs: List[Dict[str, Any]]        # serialized RetrievedChunk
    retrieval_scores: List[float]

    # ── Integration results ───────────────────────────────────────────────────
    order_result: Optional[Dict[str, Any]]
    warranty_result: Optional[Dict[str, Any]]
    crm_result: Optional[Dict[str, Any]]
    api_success: Optional[bool]

    # ── Troubleshooting ───────────────────────────────────────────────────────
    troubleshooting_steps: List[str]
    troubleshooting_summary: str

    # ── Response ──────────────────────────────────────────────────────────────
    draft_response: str
    final_response: str
    guardrail_violations: List[str]

    # ── Confidence & Governance ───────────────────────────────────────────────
    confidence_score: float
    confidence_label: str
    needs_review: bool

    # ── Escalation ────────────────────────────────────────────────────────────
    should_escalate: bool
    escalation_reason: str
    ticket_id: Optional[str]
    ticket_priority: str

    # ── Summarization ─────────────────────────────────────────────────────────
    conversation_summary: str

    # ── Audit ─────────────────────────────────────────────────────────────────
    audit_events: List[str]
    error: Optional[str]
