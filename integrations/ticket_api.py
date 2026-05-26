"""Mock Ticketing / CRM API — creates and manages support tickets."""
from __future__ import annotations
import json
import uuid
from datetime import datetime
from typing import Optional, List
from config import TICKETS_FILE


def _load() -> dict:
    if TICKETS_FILE.exists():
        return json.loads(TICKETS_FILE.read_text())
    return {}


def _save(tickets: dict):
    TICKETS_FILE.write_text(json.dumps(tickets, indent=2, default=str))


class TicketAPI:
    """Simulates a help-desk ticketing system."""

    PRIORITIES = ["Low", "Medium", "High", "Critical"]
    STATUSES = ["Open", "In Progress", "Pending Customer", "Resolved", "Closed"]

    def create_ticket(
        self,
        customer_id: str,
        customer_name: str,
        subject: str,
        description: str,
        priority: str = "Medium",
        category: str = "General",
        session_id: str = "",
        escalated: bool = False,
    ) -> dict:
        tickets = _load()
        ticket_id = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.utcnow().isoformat()
        ticket = {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "subject": subject,
            "description": description,
            "priority": priority,
            "category": category,
            "status": "Open",
            "escalated": escalated,
            "session_id": session_id,
            "created_at": now,
            "updated_at": now,
            "resolution": None,
            "notes": [],
        }
        tickets[ticket_id] = ticket
        _save(tickets)
        return {"success": True, "ticket": ticket}

    def get_ticket(self, ticket_id: str) -> dict:
        tickets = _load()
        ticket = tickets.get(ticket_id.upper())
        if ticket:
            return {"success": True, "ticket": ticket}
        return {"success": False, "error": f"Ticket {ticket_id} not found."}

    def list_tickets(
        self,
        status: Optional[str] = None,
        escalated_only: bool = False,
        limit: int = 50,
    ) -> List[dict]:
        tickets = _load()
        results = list(tickets.values())
        if status:
            results = [t for t in results if t["status"] == status]
        if escalated_only:
            results = [t for t in results if t.get("escalated")]
        results.sort(key=lambda t: t["created_at"], reverse=True)
        return results[:limit]

    def update_ticket(
        self,
        ticket_id: str,
        status: Optional[str] = None,
        resolution: Optional[str] = None,
        note: Optional[str] = None,
    ) -> dict:
        tickets = _load()
        ticket = tickets.get(ticket_id.upper())
        if not ticket:
            return {"success": False, "error": f"Ticket {ticket_id} not found."}
        if status:
            ticket["status"] = status
        if resolution:
            ticket["resolution"] = resolution
        if note:
            ticket["notes"].append(
                {"text": note, "timestamp": datetime.utcnow().isoformat()}
            )
        ticket["updated_at"] = datetime.utcnow().isoformat()
        tickets[ticket_id.upper()] = ticket
        _save(tickets)
        return {"success": True, "ticket": ticket}

    def get_stats(self) -> dict:
        tickets = _load()
        all_t = list(tickets.values())
        return {
            "total": len(all_t),
            "open": sum(1 for t in all_t if t["status"] == "Open"),
            "in_progress": sum(1 for t in all_t if t["status"] == "In Progress"),
            "resolved": sum(1 for t in all_t if t["status"] in ("Resolved", "Closed")),
            "escalated": sum(1 for t in all_t if t.get("escalated")),
        }
