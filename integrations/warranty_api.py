"""Mock Warranty Lookup API."""
from __future__ import annotations
import json
from datetime import date
from config import DATA_DIR

_WARRANTY_FILE = DATA_DIR / "mock_warranties.json"


def _load() -> dict:
    if _WARRANTY_FILE.exists():
        return json.loads(_WARRANTY_FILE.read_text())
    return {}


class WarrantyAPI:
    """Simulates a warranty verification service."""

    def check_warranty(self, service_tag: str) -> dict:
        """Look up warranty status by Service Tag."""
        warranties = _load()
        tag = service_tag.upper().strip()
        record = warranties.get(tag)
        if not record:
            # Flexible match
            for k, v in warranties.items():
                if tag in k:
                    record = v
                    break
        if not record:
            return {
                "success": False,
                "error": (
                    f"Service Tag '{service_tag}' not found. "
                    "Please check the tag on the bottom of your device or in BIOS (F2 > System Info)."
                ),
            }

        # Compute live status
        today = date.today()
        warranty_end = date.fromisoformat(record["warranty_end_date"])
        days_remaining = (warranty_end - today).days
        is_active = days_remaining > 0

        battery_status = None
        if record.get("battery_warranty_end"):
            bat_end = date.fromisoformat(record["battery_warranty_end"])
            bat_days = (bat_end - today).days
            battery_status = {
                "end_date": record["battery_warranty_end"],
                "active": bat_days > 0,
                "days_remaining": bat_days,
            }

        return {
            "success": True,
            "warranty": {
                **record,
                "is_active": is_active,
                "days_remaining": days_remaining,
                "battery_warranty": battery_status,
            },
        }

    def format_warranty_summary(self, warranty: dict) -> str:
        """Return a human-readable warranty summary."""
        status_icon = "✅ Active" if warranty["is_active"] else "❌ Expired"
        addons = ", ".join(warranty.get("addons", [])) or "None"
        lines = [
            f"**{warranty['product_name']}** (Tag: `{warranty['service_tag']}`)",
            f"Warranty: {status_icon} — expires {warranty['warranty_end_date']} "
            f"({warranty['days_remaining']} days remaining)",
            f"Type: {warranty['warranty_type']}",
            f"Service Level: {warranty['service_level']}",
            f"Add-ons: {addons}",
        ]
        if bw := warranty.get("battery_warranty"):
            bat_icon = "✅" if bw["active"] else "❌"
            lines.append(
                f"Battery warranty: {bat_icon} expires {bw['end_date']}"
            )
        return "\n".join(lines)
