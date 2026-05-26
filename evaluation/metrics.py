"""Evaluation metrics for measuring support quality and efficiency."""
from __future__ import annotations
import json
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from config import CONVERSATIONS_FILE, TICKETS_FILE
from governance.audit_logger import get_audit_logger


class EvaluationMetrics:
    """Computes and reports quality and efficiency metrics."""

    def __init__(self):
        self._audit = get_audit_logger()

    # ── Data Loaders ──────────────────────────────────────────────────────────

    def _load_conversations(self) -> List[dict]:
        if not CONVERSATIONS_FILE.exists():
            return []
        try:
            data = json.loads(CONVERSATIONS_FILE.read_text())
            return list(data.values())
        except Exception:
            return []

    def _load_tickets(self) -> List[dict]:
        if not TICKETS_FILE.exists():
            return []
        try:
            data = json.loads(TICKETS_FILE.read_text())
            return list(data.values())
        except Exception:
            return []

    # ── Core Metrics ──────────────────────────────────────────────────────────

    def get_response_quality_metrics(self) -> Dict:
        """Aggregate confidence scores and quality signals."""
        convos = self._load_conversations()
        if not convos:
            return {"error": "No conversation data yet."}

        scores = [c.get("confidence_score", 0) for c in convos]
        labels = defaultdict(int)
        for c in convos:
            labels[c.get("confidence_label", "unknown")] += 1

        avg_score = sum(scores) / len(scores) if scores else 0
        high_conf = sum(1 for s in scores if s >= 0.80)
        low_conf = sum(1 for s in scores if s < 0.40)

        return {
            "total_conversations": len(convos),
            "avg_confidence_score": round(avg_score, 3),
            "confidence_distribution": dict(labels),
            "high_confidence_rate": round(high_conf / len(convos), 3) if convos else 0,
            "low_confidence_rate": round(low_conf / len(convos), 3) if convos else 0,
        }

    def get_resolution_metrics(self) -> Dict:
        """Compute first-contact resolution and escalation rates."""
        convos = self._load_conversations()
        tickets = self._load_tickets()
        if not convos:
            return {"error": "No conversation data yet."}

        total = len(convos)
        escalated = sum(1 for c in convos if c.get("escalated"))
        resolved_tickets = sum(
            1 for t in tickets if t.get("status") in ("Resolved", "Closed")
        )

        # FCR: conversations that did NOT require escalation
        fcr = (total - escalated) / total if total > 0 else 0

        return {
            "total_conversations": total,
            "escalation_count": escalated,
            "escalation_rate": round(escalated / total, 3) if total > 0 else 0,
            "first_contact_resolution_rate": round(fcr, 3),
            "total_tickets": len(tickets),
            "resolved_tickets": resolved_tickets,
            "ticket_resolution_rate": round(resolved_tickets / len(tickets), 3) if tickets else 0,
        }

    def get_intent_distribution(self) -> Dict:
        """Distribution of classified intents."""
        convos = self._load_conversations()
        dist = defaultdict(int)
        for c in convos:
            dist[c.get("intent", "unknown")] += 1
        total = sum(dist.values())
        return {
            intent: {"count": count, "percentage": round(count / total * 100, 1) if total else 0}
            for intent, count in sorted(dist.items(), key=lambda x: -x[1])
        }

    def get_audit_summary(self) -> Dict:
        """High-level audit log summary."""
        return self._audit.get_stats()

    def get_guardrail_metrics(self) -> Dict:
        """Count and categorize guardrail triggers."""
        logs = self._audit.read_logs(event_type="guardrail_triggered", limit=1000)
        violations: Dict[str, int] = defaultdict(int)
        for log in logs:
            for v in log.get("data", {}).get("violations", []):
                vtype = v.split(":")[0]
                violations[vtype] += 1
        return {
            "total_guardrail_triggers": len(logs),
            "violation_types": dict(violations),
        }

    def get_retrieval_quality(self) -> Dict:
        """Average retrieval scores from audit logs."""
        logs = self._audit.read_logs(event_type="docs_retrieved", limit=500)
        if not logs:
            return {"error": "No retrieval data yet."}
        scores = [
            log["data"].get("top_score", 0)
            for log in logs
            if "data" in log and log["data"].get("top_score") is not None
        ]
        counts = [
            log["data"].get("count", 0)
            for log in logs
            if "data" in log
        ]
        return {
            "total_retrievals": len(logs),
            "avg_top_score": round(sum(scores) / len(scores), 4) if scores else 0,
            "avg_docs_retrieved": round(sum(counts) / len(counts), 1) if counts else 0,
        }

    def get_full_report(self) -> Dict:
        """Return all metrics as a single dictionary."""
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "response_quality": self.get_response_quality_metrics(),
            "resolution": self.get_resolution_metrics(),
            "intent_distribution": self.get_intent_distribution(),
            "retrieval_quality": self.get_retrieval_quality(),
            "guardrails": self.get_guardrail_metrics(),
            "audit_summary": self.get_audit_summary(),
        }


_METRICS: EvaluationMetrics | None = None


def get_metrics() -> EvaluationMetrics:
    global _METRICS
    if _METRICS is None:
        _METRICS = EvaluationMetrics()
    return _METRICS
