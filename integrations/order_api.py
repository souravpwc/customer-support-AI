"""Mock Order Management API."""
from __future__ import annotations
import json
from typing import Optional
from config import DATA_DIR

_ORDERS_FILE = DATA_DIR / "mock_orders.json"


def _load() -> dict:
    if _ORDERS_FILE.exists():
        return json.loads(_ORDERS_FILE.read_text())
    return {}


class OrderAPI:
    """Simulates an order management system REST API."""

    def get_order(self, order_id: str) -> dict:
        """Look up an order by ID."""
        orders = _load()
        order_id = order_id.upper().strip()
        if order_id in orders:
            order = orders[order_id]
            return {"success": True, "order": order}
        # Fuzzy match: try without prefix
        for oid, data in orders.items():
            if order_id in oid or oid.endswith(order_id):
                return {"success": True, "order": data}
        return {
            "success": False,
            "error": f"Order {order_id} not found. Please verify the order number.",
        }

    def get_orders_by_customer(self, customer_id: str) -> dict:
        """Get all orders for a customer."""
        orders = _load()
        customer_orders = [
            o for o in orders.values() if o.get("customer_id") == customer_id
        ]
        if customer_orders:
            return {"success": True, "orders": customer_orders, "count": len(customer_orders)}
        return {"success": False, "error": "No orders found for this customer."}

    def format_order_summary(self, order: dict) -> str:
        """Return a human-readable order summary string."""
        items_str = ", ".join(
            f"{i['name']} x{i['qty']}" for i in order.get("items", [])
        )
        tracking = (
            f"Tracking: {order['carrier']} #{order['tracking_number']}"
            if order.get("tracking_number")
            else "Tracking not yet available"
        )
        delivery = (
            f"Estimated delivery: {order['estimated_delivery']}"
            if order.get("estimated_delivery")
            else ""
        )
        return (
            f"Order **{order['order_id']}** — Status: **{order['status']}**\n"
            f"Items: {items_str}\n"
            f"Total: ${order['total']:.2f} | Ordered: {order['order_date']}\n"
            f"{tracking}\n"
            f"{delivery}"
        ).strip()
