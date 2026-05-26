# Service Request: Damaged Screen Repair

**Document ID:** TS-SVC-007
**Applies to:** All NovaBook laptops
**Severity:** Hardware Damage
**Estimated repair time:** 5-7 business days (depot), 1-2 days (on-site for Premium Support)
**Last Updated:** 2025-09-08

## Coverage Overview
Physical screen damage is **NOT** covered by the standard 1-year limited warranty (see WARRANTY-POL-001 section "What Is Not Covered"). Coverage requires:
- **TechNova Accidental Damage Service (ADS)** subscription, OR
- **Premium Support Plus**, which includes ADS.

If neither is active, the repair is **billable** and a quote will be provided before service is scheduled.

## Required Information
1. Service Tag.
2. Photo of the damage (front and side angles).
3. Brief description of how the damage occurred (for ADS claim).
4. Confirmation that the device can still power on (affects whether data backup is needed before shipping).
5. Customer address and preferred service mode (depot mail-in or on-site).

## Decision Tree

| Coverage Status | Service Mode | Action |
|---|---|---|
| ADS or Premium Support Plus active | On-site (Premium Support Plus) | Schedule on-site within 1-2 business days; technician brings replacement panel. |
| ADS or Premium Support Plus active | Depot mail-in | Generate prepaid shipping label; depot repair in 3-5 business days after receipt. |
| Standard warranty only | Billable depot | Provide quote (panel + labor: typically $260-$490 USD depending on model). Customer approves before work. |
| Out of warranty, no ADS | Billable depot | Same as above; service is at customer expense. |

## Repair Workflow
1. Create a Service Request in the case management system; attach photos.
2. For ADS claims, set claim type = `ADS_PHYSICAL_DAMAGE`.
3. Quote and authorization (billable only).
4. Send prepaid shipping label (mail-in) or assign technician (on-site).
5. Customer **backs up data** before shipping. Display repair does not normally affect storage, but customers should be advised.
6. Customer **removes** any third-party stickers, security cables, and SIM trays.
7. Repair, QA test, return shipment.
8. Close case and request CSAT survey.

## Data Backup Reminder Script
> "Before you ship the device, please back up your data to OneDrive or an external drive. While a screen repair does not normally affect your storage, we strongly recommend backups for any depot service."

## Escalation / Special Cases
- **Cracked screen with battery damage** (chassis flexed): treat as a safety case - escalate to Senior Hardware. Do not ship via standard carrier; use TechNova-arranged damaged-battery logistics.
- **Enterprise fleet damage** (>= 10 units): route to **Enterprise Service Desk** for batch repair quote and on-site dispatch.
- **Damage on a device still under DOA (Dead-on-Arrival) replacement window**: 30-day DOA covers manufacturing defects only, NOT physical damage; route to ADS or billable.
