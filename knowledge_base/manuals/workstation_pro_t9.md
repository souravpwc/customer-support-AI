# TechNova WorkStation Pro T9 - Product Manual

**Document ID:** MAN-DT-WSPRO-T9-2025
**Product Category:** Desktops - High-End Workstation
**Audience:** AI/ML Research, VFX, Simulation, Enterprise Engineering
**Last Updated:** 2025-08-15

## 1. Product Overview
The TechNova WorkStation Pro T9 is the flagship dual-socket tower workstation built for AI/ML training, large-scale simulation, multi-GPU rendering, and broadcast/post-production. It supports up to 4x double-wide GPUs, 2 TB ECC memory, and redundant 2000 W power supplies.

## 2. Form Factor and Box Contents
- Full-tower chassis with caster wheels (35 kg empty, up to 55 kg fully loaded)
- USB keyboard (TechNova KB-220) and optical mouse (TechNova MS-110)
- 2x 1.8 m C19 power cables (for 2000 W PSUs)
- DisplayPort 1.4 cable (1 included)
- Quick Start Guide and warranty leaflet
- Rack conversion kit (optional, 5U rails sold separately)

## 3. Hardware Specifications
| Component | Specification |
|---|---|
| CPU | Up to 2x Intel Xeon W9-3495X (56 cores each) |
| Memory | Up to 2 TB ECC DDR5 4800 (16 DIMM slots) |
| Storage | Up to 8x M.2 NVMe Gen4 SSDs and 8x 3.5" SAS/SATA bays (hot-swap) |
| GPU | Up to 4x NVIDIA RTX 6000 Ada (48 GB each) or 2x H100 NVL (94 GB) |
| Power Supply | 2x 2000 W 80 Plus Titanium redundant (1+1) |
| Cooling | Liquid CPU cooling + 8 high-static-pressure fans (hot-swap) |
| Network | 2x 10 GbE RJ-45 + 1x dedicated BMC management port |
| PCIe | 4x PCIe Gen5 x16, 2x Gen5 x8, 1x Gen4 x4 (BMC) |
| Form Factor | Full tower, rack-convertible (5U with optional rails) |

## 4. Site Preparation
- Operating temperature: 10°C to 35°C; humidity 8% to 90% non-condensing.
- Required clearance: 20 cm front, 20 cm rear, 10 cm sides for airflow.
- Power: dedicated 20 A circuit at 115 V, or 15 A at 230 V (preferred for redundancy).
- Floor loading: confirm building floor rating is at least 60 kg per workstation when fully loaded.

## 5. First-Time Setup
1. Position the workstation on a stable surface or use the caster wheels for relocation.
2. Connect both PSUs to separate UPS-protected circuits for true redundancy.
3. Connect monitor (DisplayPort recommended), keyboard, mouse, network cables (both 10 GbE for SMB Multichannel), and BMC management cable.
4. Press the front power button. POST may take 90-180 seconds while DDR5 memory is trained.
5. Complete Windows 11 Pro for Workstations or Ubuntu 22.04 / 24.04 LTS first-boot.
6. Open **TechNova Workstation Console** to register the device and configure RAID, BMC, and monitoring.

## 6. Storage Configuration
- Default: software RAID via Windows Storage Spaces, Linux mdadm, or ZFS.
- Hardware RAID via TechNova MegaRAID 9670W-16i (Tri-Mode NVMe/SAS/SATA, included on top-tier SKUs).
- Supported levels: RAID 0, 1, 5, 6, 10, 50, 60.
- Mixing Gen4 and Gen5 NVMe in the same array is supported but limits throughput to the slowest device.

## 7. Remote Management (BMC / IPMI)
- Dedicated BMC port provides IPMI 2.0 and Redfish.
- Default credentials: username `admin`, password printed on the chassis side label.
- Change the default password during first login. Enable HTTPS-only and disable IPMI over LAN if not required.
- The T9 ships with **TechNova iNova Controller 8.x** for enterprise-grade lifecycle management.

## 8. GPU Installation Notes
- Supports up to 4x double-wide GPUs in PCIe Gen5 x16 slots 1, 3, 5, 7.
- For H100 NVL pairs, install in slots 1 + 3 (NVLink bridge included with H100 NVL kit).
- All 12VHPWR cables must be fully seated; partial connection triggers a fan ramp-up and BMC alert.
- After GPU installation, run **Workstation Console > Diagnostics > GPU Stress Test** for 30 minutes; for multi-GPU configs, run **Multi-GPU Bandwidth Test** to verify NVLink and PCIe topology.

## 9. Indicator Lights and Audio Codes
| Indicator | Pattern | Meaning |
|---|---|---|
| Front power LED | Solid white | System on |
| Front power LED | Blinking amber | Power or thermal fault - check BMC |
| Front diagnostic LEDs | "1-3-2" beep code | Memory failure |
| Front diagnostic LEDs | "5-1-1" beep code | CPU thermal trip |
| Rear BMC LED | Solid green | BMC healthy |
| Rear BMC LED | Blinking amber | BMC alert - check event log |
| Liquid cooler LED | Solid blue | Healthy |
| Liquid cooler LED | Solid red | Pump fault - power off and contact support |

## 10. Drivers and Firmware
- Use **TechNova Workstation Console** for coordinated BIOS, BMC, NIC, RAID, GPU, and liquid-cooler firmware updates.
- Critical CVEs are pushed via the **TechNova Security Advisory** feed.
- Offline update bundle: `support.technova.com/workstation/firmware/T9`.

## 11. Service Access
- Tool-less side panel: press the green latch at the top-rear and slide the panel back.
- All hot-swap bays (PSU, fans, drives) are color-coded green.
- Liquid cooling reservoir has a visible coolant level window; report any visible drop to TechNova support immediately.
- Service Tag is on a pull-out card at the front-top of the chassis.

## 12. Differences vs. T5 and T7
| Capability | T5 | T7 | T9 |
|---|---|---|---|
| Sockets | 1 | Up to 2 | 2 |
| Max memory | 256 GB ECC | 512 GB ECC | 2 TB ECC |
| Max GPUs | 1 (double-wide) | 2 (double-wide) | 4 (double-wide) |
| Max PSU | 750 W single | 1400 W redundant (1+1) | 2x 2000 W redundant |
| Cooling | Air | Air | Liquid (CPU) + air (GPU) |
| Form factor | Mid-tower | Full-tower (rack-convertible 5U) | Full-tower (rack-convertible 5U) |

## 13. Warranty
- Standard: 3 years ProSupport, 9x5 next-business-day on-site (see WARRANTY-POL-001).
- ProSupport Plus (recommended for production workloads): adds 24x7 priority response, ADS, Keep Your Hard Drive, predictive failure analysis.
- Mission-Critical 4-hour parts and labor SLA is available for an extra fee for T9-class deployments.
