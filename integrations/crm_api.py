"""Mock CRM API — customer profile and interaction history."""
from __future__ import annotations
import json
from typing import Optional
from config import DATA_DIR

_CUSTOMERS_FILE = DATA_DIR / "mock_customers.json"


def _load() -> dict:
    if _CUSTOMERS_FILE.exists():
        return json.loads(_CUSTOMERS_FILE.read_text())
    return {}


class CRMAPI:
    """Simulates a customer relationship management system."""

    def get_customer(self, customer_id: str) -> dict:
        customers = _load()
        customer = customers.get(customer_id.upper())
        if customer:
            return {"success": True, "customer": customer}
        return {
            "success": False,
            "error": f"Customer {customer_id} not found in CRM.",
        }

    def find_by_email(self, email: str) -> dict:
        customers = _load()
        for cust in customers.values():
            if cust.get("email", "").lower() == email.lower():
                return {"success": True, "customer": cust}
        return {"success": False, "error": "No customer found with that email."}

    def get_tier_benefits(self, tier: str) -> dict:
        benefits = {
            "Standard": {
                "support_hours": "9x5",
                "response_sla": "4 business hours",
                "channels": ["Web chat", "Email"],
            },
            "Premium": {
                "support_hours": "24x7",
                "response_sla": "2 hours",
                "channels": ["Web chat", "Email", "Phone"],
            },
            "Business": {
                "support_hours": "24x7",
                "response_sla": "1 hour",
                "channels": ["Web chat", "Email", "Phone", "Dedicated rep"],
            },
            "Enterprise": {
                "support_hours": "24x7 mission-critical",
                "response_sla": "15 minutes",
                "channels": ["Web chat", "Email", "Phone", "Dedicated account team"],
            },
        }
        return benefits.get(tier, benefits["Standard"])

    def format_customer_context(self, customer: dict) -> str:
        tier_info = self.get_tier_benefits(customer.get("tier", "Standard"))
        return (
            f"Customer: {customer['name']} | Tier: {customer['tier']}\n"
            f"Support: {tier_info['support_hours']} | SLA: {tier_info['response_sla']}\n"
            f"Open tickets: {customer.get('open_tickets', 0)} | "
            f"Total orders: {customer.get('total_orders', 0)}"
        )
