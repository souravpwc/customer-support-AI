"""Escalation agent — creates tickets and notifies human support queue."""
from __future__ import annotations
from agents.state import SupportState
from integrations.ticket_api import TicketAPI
from governance.audit_logger import get_audit_logger

_ticket_api = TicketAPI()
_audit = get_audit_logger()

_PRIORITY_MAP = {
    "Enterprise": "Critical",
    "Business": "High",
    "Premium": "High",
    "Standard": "Medium",
}

_INTENT_CATEGORY_MAP = {
    "order_status": "Order Management",
    "warranty_check": "Warranty & Service",
    "troubleshooting": "Technical Support",
    "return_refund": "Returns & Refunds",
    "product_info": "Product Information",
    "escalation_request": "Customer Escalation",
    "general_faq": "General Inquiry",
}


def escalate_node(state: SupportState) -> SupportState:
    """LangGraph node: create a support ticket and prepare escalation response."""
    customer_id = state.get("customer_id", "GUEST")
    customer_name = state.get("customer_name", "Customer")
    customer_tier = state.get("customer_tier", "Standard")
    intent = state.get("intent", "general_faq")
    session_id = state.get("session_id", "")
    escalation_reason = state.get("escalation_reason", "Customer requested escalation")
    history = state.get("conversation_history", [])
    final_response = state.get("final_response", "")

    # Determine priority
    priority = _PRIORITY_MAP.get(customer_tier, "Medium")
    if intent == "troubleshooting" and state.get("confidence_score", 1.0) < 0.4:
        priority = "High"

    # Build ticket description
    last_messages = history[-4:] if history else []
    conv_excerpt = "\n".join(
        f"{t['role'].upper()}: {t['content']}" for t in last_messages
    )
    description = (
        f"Session: {session_id}\n"
        f"Intent: {intent}\n"
        f"Escalation reason: {escalation_reason}\n"
        f"Confidence score: {state.get('confidence_score', 0):.0%}\n\n"
        f"Conversation excerpt:\n{conv_excerpt}\n\n"
        f"AI's last response:\n{final_response}"
    )

    # Subject from last user message
    last_user = next(
        (t["content"] for t in reversed(history) if t.get("role") == "user"),
        state.get("user_message", "Support needed"),
    )
    subject = f"{_INTENT_CATEGORY_MAP.get(intent, 'Support')}: {last_user[:80]}"

    result = _ticket_api.create_ticket(
        customer_id=customer_id,
        customer_name=customer_name,
        subject=subject,
        description=description,
        priority=priority,
        category=_INTENT_CATEGORY_MAP.get(intent, "General"),
        session_id=session_id,
        escalated=True,
    )

    ticket_id = None
    escalation_response_suffix = ""

    if result.get("success"):
        ticket = result["ticket"]
        ticket_id = ticket["ticket_id"]
        _audit.log(
            "escalation_triggered",
            session_id=session_id,
            data={"ticket_id": ticket_id, "reason": escalation_reason, "priority": priority},
            customer_id=customer_id,
            intent=intent,
        )
        escalation_response_suffix = (
            f"\n\n---\n🎫 **Ticket Created:** `{ticket_id}`\n"
            f"A human support agent will contact you within your SLA window. "
            f"Please reference this ticket number in future communications."
        )
    else:
        escalation_response_suffix = (
            "\n\nI've flagged this conversation for human review. "
            f"Please contact us at our support line for immediate assistance."
        )

    updated_response = state.get("final_response", "") + escalation_response_suffix

    return {
        **state,
        "ticket_id": ticket_id,
        "ticket_priority": priority,
        "final_response": updated_response,
    }
