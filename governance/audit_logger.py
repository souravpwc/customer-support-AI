"""Append-only JSONL audit logger for every support interaction."""
from __future__ import annotations
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from config import AUDIT_LOG_FILE


class AuditLogger:
    """Writes one JSON line per event to the audit log file."""

    EVENT_TYPES = {
        "session_start", "session_end",
        "message_received", "intent_classified",
        "docs_retrieved", "api_called",
        "response_generated", "escalation_triggered",
        "ticket_created", "guardrail_triggered",
        "human_review_requested", "confidence_low",
    }

    def log(
        self,
        event_type: str,
        session_id: str,
        data: Dict[str, Any],
        customer_id: Optional[str] = None,
        intent: Optional[str] = None,
        confidence: Optional[float] = None,
    ) -> str:
        event_id = uuid.uuid4().hex
        entry = {
            "event_id": event_id,
            "event_type": event_type,
            "session_id": session_id,
            "customer_id": customer_id,
            "intent": intent,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return event_id

    def read_logs(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 200,
    ) -> List[dict]:
        if not AUDIT_LOG_FILE.exists():
            return []
        logs = []
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if session_id and entry.get("session_id") != session_id:
                    continue
                if event_type and entry.get("event_type") != event_type:
                    continue
                logs.append(entry)
        return logs[-limit:]

    def get_stats(self) -> dict:
        logs = self.read_logs(limit=10000)
        if not logs:
            return {}
        intents: Dict[str, int] = {}
        events: Dict[str, int] = {}
        escalations = 0
        guardrail_hits = 0
        for entry in logs:
            ev = entry.get("event_type", "unknown")
            events[ev] = events.get(ev, 0) + 1
            if intent := entry.get("intent"):
                intents[intent] = intents.get(intent, 0) + 1
            if ev == "escalation_triggered":
                escalations += 1
            if ev == "guardrail_triggered":
                guardrail_hits += 1
        return {
            "total_events": len(logs),
            "intent_distribution": intents,
            "event_distribution": events,
            "total_escalations": escalations,
            "guardrail_hits": guardrail_hits,
        }


# Singleton
_AUDIT: AuditLogger | None = None


def get_audit_logger() -> AuditLogger:
    global _AUDIT
    if _AUDIT is None:
        _AUDIT = AuditLogger()
    return _AUDIT
