# Troubleshooting: Enterprise Server Outage (NovaEdge R760)

**Document ID:** TS-SRV-008
**Applies to:** NovaEdge R760, NovaEdge R660, NovaEdge MX-Series
**Severity:** Critical (P1)
**Estimated time:** Immediate escalation; engagement < 15 minutes
**Last Updated:** 2025-09-12

## Policy: Auto-Escalation
A reported enterprise server outage **must be auto-escalated** to the Critical Incident Response Team (CIRT). Front-line agents do **not** attempt independent troubleshooting beyond data collection.

## Required Information (collect in parallel with escalation)
1. Service Tag of affected server(s).
2. Customer account ID and support contract level (ProSupport Plus / Mission Critical).
3. Number of users / business processes impacted.
4. iNova event log export (BMC).
5. SEL (System Event Log) summary, if available.
6. Workload running on the server (vSphere, K8s, SQL, file services).
7. Any recent change: firmware, OS patch, cabling, environmental (HVAC, power).
8. Did automatic failover occur?

## Initial Triage Workflow (concurrent with CIRT engagement)

### Step 1: Reach the iNova / BMC
- Browse to `https://<inova-ip>` from the customer's management network.
- If iNova is reachable, capture **System Health**, **Hardware Inventory**, and **Lifecycle Log** under Maintenance > Lifecycle Log > Export.
- If iNova is unreachable, instruct the on-site contact to check the rear iNova LED and the dedicated management switch.

### Step 2: Power and PSU status
- Both PSU LEDs should be solid green. Amber on either indicates input loss or PSU fault.
- If one PSU is amber and the system is still up, redundancy is intact but the failed PSU must be replaced ASAP.
- If both PSUs are amber, system is on a single feed - high risk of total outage.

### Step 3: Check for thermal or environmental triggers
- Data center temperature readings from facility BMS.
- Recent HVAC alarms.
- iNova > Thermal > confirm inlet temperature < 35°C.

### Step 4: Storage and RAID
- iNova > Storage > controller and physical disk health.
- A degraded RAID 5/6 is **operational but at risk**. A failed second drive in RAID 5 = data loss.
- A failed cache battery on the PERC controller forces write-through mode and severely impacts performance.

## Severity Mapping

| Symptom | Severity | Response SLA (ProSupport Plus) |
|---|---|---|
| Server down, no production impact (lab) | P3 | Next business day |
| Single server down, partial production impact | P2 | 4 hours |
| Mission-critical production down OR data loss risk | P1 | < 1 hour, on-site parts dispatch |
| Multi-server outage affecting site | P1+ / CIRT | < 15 min engagement, war room |

## Communication Cadence (P1)
- Initial customer status: within 30 minutes of case creation.
- Subsequent updates: every 60 minutes until resolved.
- Post-incident report: within 5 business days after resolution.

## Escalation Targets
| Role | Engage When |
|---|---|
| L2 Hardware Engineer | Any P2 within 1 hour |
| CIRT (Critical Incident Response) | P1 immediately |
| Field Service Dispatch | Parts identified, on-site needed |
| Account Executive | P1 in production, customer-facing comms |

## Do NOT
- Do not advise the customer to power-cycle a production server until L2/CIRT approves.
- Do not push firmware updates during an active incident.
- Do not clear iNova logs - they are needed for root cause analysis.
