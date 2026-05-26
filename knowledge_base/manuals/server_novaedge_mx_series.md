# TechNova NovaEdge MX-Series Modular Server Platform - Product Manual

**Document ID:** MAN-SRV-NE-MX-2025
**Product Category:** Enterprise Servers - Modular / Blade
**Audience:** Enterprise IT, Data Center Operations, Service Providers
**Last Updated:** 2025-07-30

## 1. Platform Overview
The TechNova NovaEdge MX-Series is a 7U modular chassis platform that consolidates compute, storage, networking, and fabric into a single converged enclosure. It is the highest-density NovaEdge offering and is intended for private cloud, VDI, software-defined storage, and large virtualization estates where lifecycle management and TCO matter more than per-node price.

The MX-Series complements the rack NovaEdge family:
- **NovaEdge R660** (1U rack) - density, edge, web tier
- **NovaEdge R760** (2U rack) - general purpose virtualization, mid-range storage
- **NovaEdge MX-Series** (7U modular) - converged, high-scale, fabric-based

## 2. Chassis: MX7000

| Spec | Value |
|---|---|
| Form factor | 7U modular, fits standard 19" 4-post rack |
| Compute slots | 8x single-width MX740c blades or 4x double-width MX840c blades |
| Storage sled slots | Up to 12x MX5016s SAS sleds (16x 2.5" drives each = 192 drives per chassis) |
| Fabric slots | 6x I/O Module slots (2 per side, configurable as Ethernet, FC, or SAS fabric) |
| Power | Up to 6x 3200 W Platinum / Titanium PSUs (3+3 redundant) |
| Cooling | 9 hot-swap fans, N+1 redundant |
| Management | 2x redundant Management Modules (MM); active/passive failover |
| Weight (empty chassis) | 79 kg |
| Weight (fully loaded) | 318 kg |

## 3. Compute Sleds

### MX740c (single-width blade)
| Spec | Value |
|---|---|
| Sockets | 2x Intel Xeon Scalable (4th / 5th Gen) |
| Memory | Up to 8 TB DDR5 (32 DIMM slots) |
| Storage | 6x 2.5" SAS/SATA/NVMe drive bays per sled |
| Local M.2 | 2x M.2 NVMe boot slots |
| Mezzanine | 2x mezzanine slots for fabric I/O (Ethernet 25/100 GbE, FC 32G) |

### MX840c (double-width blade)
| Spec | Value |
|---|---|
| Sockets | 4x Intel Xeon Scalable |
| Memory | Up to 16 TB DDR5 (64 DIMM slots) |
| Storage | 8x 2.5" SAS/SATA/NVMe drive bays per sled |
| Local M.2 | 2x M.2 NVMe boot slots |
| Mezzanine | 4x mezzanine slots for fabric I/O |

## 4. Storage Sled

### MX5016s
- 16x 2.5" SAS HDD or SSD bays per sled
- Drives mapped to compute sleds via the chassis SAS fabric
- Supports SAS RAID via the chassis-level Storage Controller (managed by the MM)

## 5. Out-of-Band Management (Chassis MM + iNova per blade)
- The **Management Module (MM)** provides chassis-level Redfish, web UI, and CLI.
- Each compute blade contains its own **iNova Controller** that is reachable through the MM or directly via the per-blade out-of-band IP.

**Default credentials (MM)**
- Username: `root`
- Password: shipped on the pull-tag at the front of the chassis, OR `calvin` if no tag is present (legacy default).

**First-time MM configuration**
1. Connect the dedicated MM RJ-45 ports (2x for redundancy) on the rear to your management network.
2. The active MM obtains a DHCP address by default. Lookup via your DHCP server, or use the chassis front-panel KVM ("Configure MM" wizard) to set a static IP.
3. Browse to `https://<mm-ip>` and log in.
4. Force the default password to be changed at first login.
5. Update the MM firmware to the latest `5.x` build before deploying blades or storage sleds.

## 6. Cabling and Site Preparation
- Floor loading: confirm building floor rating is at least 1200 kg/m² for a fully loaded chassis.
- Required clearance: 100 cm front, 100 cm rear, 8 cm sides.
- Recommended power: 3-phase 200-240 V; chassis can be wired to single-phase but loses some redundancy modes.
- Always connect PSUs across **two independent power feeds** (PDU A and PDU B) for true power redundancy.

## 7. Indicator LEDs
| LED | Pattern | Meaning |
|---|---|---|
| Chassis System Status | Solid blue | Healthy, powered on |
| Chassis System Status | Blinking blue | Chassis identification on |
| Chassis System Status | Solid amber | Critical fault - check MM event log |
| MM Active LED | Solid green | Active MM healthy |
| MM Passive LED | Solid green | Passive MM healthy, ready to take over |
| Blade System Status | Solid blue | Blade healthy |
| Blade System Status | Solid amber | Blade fault - check iNova for that blade |
| PSU LED | Solid green | Healthy |
| PSU LED | Blinking amber | PSU input lost (other PSUs still carrying load) |
| PSU LED | Solid amber | PSU fault - replace |

## 8. Firmware Updates
- Use the **TechNova Update Manager (TUM)** for coordinated chassis + blade firmware updates (MM, iNova, BIOS, NICs, RAID, GPUs).
- For air-gapped environments, download the offline bundle from `support.technova.com/mx/firmware`.
- Firmware updates are applied in this safe order: MM → fabric I/O modules → storage controller → per-blade BIOS/iNova → operating-system drivers.
- Critical CVEs are pushed via the **TechNova Security Advisory** feed.

## 9. Supported Operating Systems
- VMware ESXi 8.0 U2 and later
- Red Hat Enterprise Linux 8.8, 9.2 and later
- SUSE Linux Enterprise Server 15 SP5 and later
- Ubuntu Server 22.04 LTS and 24.04 LTS
- Windows Server 2019, 2022, 2025

## 10. Differences vs. R660 and R760
| Capability | R660 (1U) | R760 (2U) | MX-Series (7U modular) |
|---|---|---|---|
| Sockets per node | Up to 2 | Up to 2 | Up to 2 per MX740c, up to 4 per MX840c |
| Max drives per node | 10 | 24 | 6 (MX740c) or 8 (MX840c) per node + 192 shared SAS via MX5016s |
| Max memory per node | 4 TB | 8 TB | 8 TB (MX740c) / 16 TB (MX840c) |
| Max PSU | 2x 1100 W | 2x 1800 W | 6x 3200 W (3+3 redundant) |
| Fabric | Per-server NICs | Per-server NICs | Chassis-level fabric I/O modules (shared across blades) |
| Best for | Edge, web tier | General virtualization | Private cloud, VDI, large virtualization, SDS |

## 11. Support and Service Tag
- The chassis Service Tag is on the pull-out information tag at the front-left.
- Each blade and each storage sled has its own Service Tag on a front pull-tab.
- For any outage that affects the chassis or multiple blades, follow the Enterprise Server Outage runbook (TS-SRV-008) - this is treated as a P1 / CIRT engagement.
- Enterprise customers have access to ProSupport Plus 24x7x4 with mission-critical response; MX-class deployments commonly add the Mission-Critical 4-hour parts and labor SLA.
