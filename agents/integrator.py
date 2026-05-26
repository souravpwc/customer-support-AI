"""Integration agent — calls mock APIs based on intent and entities."""
from __future__ import annotations
from agents.state import SupportState
from integrations.order_api import OrderAPI
from integrations.warranty_api import WarrantyAPI
from integrations.crm_api import CRMAPI

_order_api = OrderAPI()
_warranty_api = WarrantyAPI()
_crm_api = CRMAPI()


def integrate_node(state: SupportState) -> SupportState:
    """LangGraph node: call relevant mock APIs."""
    intent = state.get("intent", "")
    entities = state.get("entities", {})
    customer_id = state.get("customer_id", "")

    updates: dict = {}
    api_success = None

    # ── Order lookup ──────────────────────────────────────────────────────────
    if intent == "order_status" or entities.get("order_id"):
        order_id = entities.get("order_id")
        if order_id:
            result = _order_api.get_order(order_id)
        elif customer_id:
            result = _order_api.get_orders_by_customer(customer_id)
        else:
            result = {"success": False, "error": "Please provide your order number (e.g. TN-100001)."}
        updates["order_result"] = result
        api_success = result.get("success", False)

    # ── Warranty lookup ───────────────────────────────────────────────────────
    if intent == "warranty_check" or entities.get("service_tag"):
        service_tag = entities.get("service_tag")
        if service_tag:
            result = _warranty_api.check_warranty(service_tag)
            updates["warranty_result"] = result
            api_success = result.get("success", False)
        else:
            updates["warranty_result"] = {
                "success": False,
                "error": "Please provide your Service Tag (found on the bottom of your device or in BIOS > System Info).",
            }
            api_success = False

    # ── CRM lookup ────────────────────────────────────────────────────────────
    if customer_id:
        crm = _crm_api.get_customer(customer_id)
        updates["crm_result"] = crm
        if crm.get("success"):
            customer = crm["customer"]
            updates["customer_name"] = customer.get("name", state.get("customer_name", "Customer"))
            updates["customer_tier"] = customer.get("tier", "Standard")

    return {**state, **updates, "api_success": api_success}
