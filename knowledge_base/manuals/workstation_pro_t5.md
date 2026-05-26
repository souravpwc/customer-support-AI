# TechNova WorkStation Pro T5 - Product Manual

**Document ID:** MAN-DT-WSPRO-T5-2025
**Product Category:** Desktops - Entry Workstation
**Audience:** SMB, Engineering, Education
**Last Updated:** 2025-08-15

## 1. Product Overview
The TechNova WorkStation Pro T5 is a single-socket entry tower workstation positioned below the T7. It targets CAD drafting, light 3D, photo and video editing, software development, and ISV-certified workloads where a workstation-class platform is required but dual-socket and multi-GPU capacity are not.

## 2. Form Factor and Box Contents
- Compact mid-tower chassis, 23 kg fully loaded
- USB keyboard (TechNova KB-220) and optical mouse (TechNova MS-110)
- 1.8 m C13 power cable
- DisplayPort 1.4 cable (1 included)
- Quick Start Guide and warranty leaflet

## 3. Hardware Specifications
| Component | Specification |
|---|---|
| CPU | 1x Intel Xeon W3-2400 series (up to 16 cores) or Intel Core i9-14900K (CTO option) |
| Memory | Up to 256 GB ECC DDR5 4400 (4 DIMM slots) |
| Storage | Up to 3x M.2 NVMe Gen4 + 2x 3.5" SATA bays |
| GPU | 1x NVIDIA RTX A2000 / A4000 / RTX 4070 (single-wide or dual-wide) |
| Power Supply | 750 W 80 Plus Platinum (non-redundant) |
| Network | 1x 2.5 GbE RJ-45 |
| PCIe | 1x PCIe Gen5 x16, 1x Gen4 x8, 1x Gen3 x4 |
| Form Factor | Mid tower, fits standard desk-side or under-desk |

## 4. Site Preparation
- Operating temperature: 10°C to 35°C; humidity 8% to 90% non-condensing.
- Required clearance: 10 cm front, 10 cm rear, 5 cm sides for airflow.
- Dedicated 15 A circuit at 115 V is recommended (10 A at 230 V).

## 5. First-Time Setup
1. Place the workstation on a stable, ventilated surface.
2. Connect power, monitor (DisplayPort recommended), keyboard, mouse, network.
3. Press the front power button. Initial POST takes up to 60 seconds.
4. Complete Windows 11 Pro for Workstations or Ubuntu 22.04 LTS first-boot.
5. Open **TechNova Workstation Console** to register the device, check for firmware updates, and configure storage.

## 6. Storage Configuration
- The T5 supports software RAID via Windows Storage Spaces or Linux mdadm.
- Hardware RAID requires the optional MegaRAID 9560-8i controller (single-slot PCIe Gen4 x8).
- Supported levels via TechNova Workstation Console: RAID 0, 1, 5, 10.

## 7. GPU Installation Notes
- The T5 supports up to one double-wide GPU in PCIe Gen5 x16 slot 1.
- Connect the included 12VHPWR cable when installing an RTX 4070 / RTX A4000.
- After GPU installation, run **Workstation Console > Diagnostics > GPU Stress Test** for 10 minutes to verify stability.

## 8. Indicator Lights and Audio Codes
| Indicator | Pattern | Meaning |
|---|---|---|
| Front power LED | Solid white | System on |
| Front power LED | Pulsing white | Sleep |
| Front power LED | Blinking amber | Power or thermal fault - check Workstation Console |
| Front diagnostic LEDs | "1-3-2" beep code | Memory failure |
| Front diagnostic LEDs | "5-1-1" beep code | CPU thermal trip |

## 9. Drivers and Firmware
- Use **TechNova Workstation Console** to apply BIOS, NIC, RAID, and GPU driver updates as a coordinated bundle.
- Offline update bundle: `support.technova.com/workstation/firmware/T5`.

## 10. Service Access
- Tool-less side panel: press the green latch at the top-rear and slide the panel back.
- Service Tag is on a pull-out card at the front-top of the chassis.

## 11. Differences vs. T7 and T9
| Capability | T5 | T7 | T9 |
|---|---|---|---|
| Sockets | 1 | Up to 2 | 2 |
| Max memory | 256 GB ECC | 512 GB ECC | 2 TB ECC |
| Max GPUs | 1 (double-wide) | 2 (double-wide) | 4 (double-wide) |
| Max PSU | 750 W single | 1400 W redundant (optional 1+1) | 2x 2000 W redundant |
| Form factor | Mid-tower | Full-tower (rack-convertible 5U) | Full-tower (rack-convertible 5U) |

## 12. Warranty
- Standard: 3 years ProSupport, 9x5 next-business-day on-site (see WARRANTY-POL-001).
- ProSupport Plus (optional): adds ADS, 24x7 priority support, Keep Your Hard Drive, predictive failure analysis.
