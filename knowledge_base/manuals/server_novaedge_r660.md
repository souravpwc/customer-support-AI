# TechNova NovaEdge R660 Rack Server - Product Manual

**Document ID:** MAN-SRV-NE-R660-2025
**Product Category:** Enterprise Servers - Rack
**Audience:** Enterprise IT, Data Center Operations
**Last Updated:** 2025-07-12

## 1. Product Overview
The TechNova NovaEdge R660 is a 1U dual-socket rack server based on 4th and 5th Gen Intel Xeon Scalable processors. It targets dense general-purpose virtualization, web tier, edge compute, and high-density caching deployments where rack-unit density matters more than maximum storage or GPU capacity. The R660 is the 1U sibling of the 2U NovaEdge R760 (MAN-SRV-NE-R760-2025).

## 2. Form Factor
- Chassis: 1U rack, 800 mm depth
- Drive bays: Up to 10x 2.5" SAS/SATA/NVMe (front), or 8x 2.5" + 2x rear
- PCIe: Up to 3x PCIe Gen5 slots via low-profile risers (configuration dependent)
- Power: Up to 2x 1100 W Platinum / Titanium PSUs (1+1 redundant)
- Cooling: Hot-swap, redundant N+1 fans (8 fans total, slim form factor)

## 3. Out-of-Band Management (iNova Controller)
The iNova Controller (TechNova's BMC) provides Redfish, IPMI 2.0, and an HTML5 console.

**Default credentials**
- Username: `root`
- Password: shipped on the pull-tag at the front of the chassis, OR `calvin` if no tag is present (legacy default).

**First-time iNova configuration**
1. Connect the dedicated iNova RJ-45 port on the rear to your management network.
2. iNova obtains a DHCP address by default. Lookup via your DHCP server, or press F2 at POST > **iNova Settings** to set a static IP.
3. Browse to `https://<inova-ip>` and log in.
4. Force the default password to be changed at first login.
5. Update the iNova firmware to the latest 7.x build before deploying workloads.

## 4. RAID and Storage
- The PERC H965i controller supports RAID 0, 1, 5, 6, 10, 50, 60.
- NVMe drives behind the controller support hardware RAID 0/1/5/10 (PERC NVMe mode).
- Use the **iNova Storage Wizard** for RAID creation.
- Note: the R660's 1U form factor limits internal storage compared with the R760. For high-capacity storage tiers, choose the R760 or the MX-Series modular chassis.

## 5. Cabling and Rack Installation
- Use the included ReadyRails II tool-less rails for 4-post racks 24"–36" deep.
- Cable management arm (CMA) installs on the left when viewed from the rear.
- Power cables: route through the CMA from the left PSU and right PSU. Do not cross-bundle power and data cables in the same channel.

## 6. Power-On Sequence
1. Verify both PSUs are seated and connected. Both PSU LEDs should be solid green within 5 seconds.
2. Press the front-panel power button. The system status LED turns solid blue when healthy.
3. POST may take 60-150 seconds depending on memory configuration.

## 7. Indicator LEDs (front)
| LED | Pattern | Meaning |
|---|---|---|
| System Status | Solid blue | Healthy, powered on |
| System Status | Blinking blue | System identification on (locate function) |
| System Status | Solid amber | Critical fault - check iNova event log |
| System Status | Blinking amber | Warning - check iNova event log |
| PSU LED | Solid green | Healthy |
| PSU LED | Blinking amber (1 Hz) | PSU input lost (other PSU still powering system) |
| PSU LED | Solid amber | PSU fault - replace |

## 8. Firmware Updates
- Use **TechNova Update Manager (TUM)** for cluster-aware firmware updates.
- For standalone updates, log into iNova and use **System > Firmware Update**.
- Critical CVEs are pushed via the **TechNova Security Advisory** feed.

## 9. Supported Operating Systems
- VMware ESXi 8.0 U2 and later
- Red Hat Enterprise Linux 8.8, 9.2 and later
- SUSE Linux Enterprise Server 15 SP5 and later
- Ubuntu Server 22.04 LTS and 24.04 LTS
- Windows Server 2019, 2022, 2025

## 10. Differences vs. R760 and MX-Series
| Capability | R660 (1U) | R760 (2U) | MX-Series (7U modular) |
|---|---|---|---|
| Sockets per node | Up to 2 | Up to 2 | Up to 2 per blade, up to 8 blades per chassis |
| Max drives (2.5") | 10 | 24 | Per-blade: 6; per-chassis: 48 |
| Max PCIe slots | 3 (low-profile) | 8 (full-height capable) | 2 per blade + 6 fabric slots per chassis |
| Max PSU | 2x 1100 W | 2x 1800 W | 6x 3200 W (3+3 redundant) |
| Form factor | 1U rack | 2U rack | 7U modular chassis (blade) |

## 11. Support
- Enterprise customers have access to ProSupport Plus 24x7x4 with mission-critical response.
- Service tag is on the pull-out information tag at the front-left of the chassis. Have the service tag and iNova **lifecycle log export** ready when contacting support.
- Outage handling and CIRT engagement: see TS-SRV-008 (Enterprise Server Outage runbook).
