"""Mock Repair Scheduling API."""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, date
from typing import Optional


_APPOINTMENTS: dict = {}

AVAILABLE_SLOTS = [
    "09:00 AM", "10:00 AM", "11:00 AM",
    "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM",
]

REPAIR_CENTERS = [
    {"id": "RC-001", "name": "TechNova Austin Service Center", "city": "Austin, TX"},
    {"id": "RC-002", "name": "TechNova Seattle Service Center", "city": "Seattle, WA"},
    {"id": "RC-003", "name": "TechNova Chicago Service Center", "city": "Chicago, IL"},
    {"id": "RC-004", "name": "TechNova New York Service Center", "city": "New York, NY"},
    {"id": "RC-005", "name": "TechNova Miami Service Center", "city": "Miami, FL"},
]


def _next_business_days(n: int = 5) -> list[str]:
    """Return the next n business days as ISO strings."""
    days = []
    current = date.today() + timedelta(days=1)
    while len(days) < n:
        if current.weekday() < 5:  # Mon-Fri
            days.append(current.isoformat())
        current += timedelta(days=1)
    return days


class RepairAPI:
    """Simulates a device repair scheduling system."""

    def get_available_slots(self, city: Optional[str] = None) -> dict:
        centers = REPAIR_CENTERS
        if city:
            centers = [c for c in REPAIR_CENTERS if city.lower() in c["city"].lower()]
            if not centers:
                centers = REPAIR_CENTERS[:1]

        return {
            "success": True,
            "centers": centers,
            "available_dates": _next_business_days(5),
            "available_times": AVAILABLE_SLOTS,
        }

    def schedule_appointment(
        self,
        customer_id: str,
        customer_name: str,
        service_tag: str,
        issue_description: str,
        center_id: str,
        date_str: str,
        time_slot: str,
    ) -> dict:
        appt_id = f"APT-{uuid.uuid4().hex[:6].upper()}"
        center = next((c for c in REPAIR_CENTERS if c["id"] == center_id), REPAIR_CENTERS[0])
        appointment = {
            "appointment_id": appt_id,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "service_tag": service_tag,
            "issue_description": issue_description,
            "center": center,
            "date": date_str,
            "time": time_slot,
            "status": "Confirmed",
            "created_at": datetime.utcnow().isoformat(),
        }
        _APPOINTMENTS[appt_id] = appointment
        return {"success": True, "appointment": appointment}

    def get_appointment(self, appointment_id: str) -> dict:
        appt = _APPOINTMENTS.get(appointment_id.upper())
        if appt:
            return {"success": True, "appointment": appt}
        return {"success": False, "error": f"Appointment {appointment_id} not found."}
