# TechNova WorkStation Pro T7 - Product Manual

**Document ID:** MAN-DT-WSPRO-T7-2025
**Product Category:** Desktops - Workstation
**Audience:** Creative Professionals, Engineering, Enterprise
**Last Updated:** 2025-08-04

## 1. Product Overview
The TechNova WorkStation Pro T7 is a tower workstation built for engineering simulation, 3D rendering, AI/ML development, and media production. It supports up to dual Xeon W7 processors, 512 GB ECC DDR5 memory, and dual NVIDIA RTX 6000 Ada Generation GPUs.

## 2. Box Contents
- TechNova WorkStation Pro T7 chassis
- USB keyboard (TechNova KB-220) and optical mouse (TechNova MS-110)
- 1.8 m C13 power cable
- DisplayPort 1.4 cable (1 included; additional cables sold separately)
- Quick Start Guide and warranty leaflet

## 3. Hardware Specifications
| Component | Specification |
|---|---|
| CPU | Up to 2x Intel Xeon W7-3475X (36 cores each) |
| Memory | Up to 512 GB ECC DDR5 4800 (8 DIMM slots per socket) |
| Storage | Up to 4x M.2 NVMe SSDs and 4x 3.5" SATA bays (hot-swap) |
| GPU | Up to 2x NVIDIA RTX 6000 Ada (48 GB each) |
| Power Supply | 1400 W 80 Plus Platinum redundant (1+1 optional) |
| Network | 2x 10 GbE RJ-45, 1x dedicated BMC (IPMI) |
| Form Factor | Full tower, rack convertible (5U with optional rails) |

## 4. Site Preparation
- Operating temperature: 10°C to 35°C; relative humidity 8% to 90% non-condensing.
- Required clearance: 15 cm front, 15 cm rear, 10 cm sides for airflow.
- Dedicated 15 A circuit recommended at 115 V; 10 A at 230 V.
- The chassis weighs up to 28 kg fully loaded; use the included caster wheels or a workstation cart for relocation.

## 5. First-Time Setup
1. Place the workstation on a stable, ventilated surface or a workstation cart.
2. Connect the power cable, monitor (DisplayPort recommended), keyboard, mouse, and network cable.
3. Press the front power button. Initial POST may take up to 90 seconds while memory is trained.
4. Complete Windows 11 Pro for Workstations or Ubuntu 22.04 LTS first-boot setup.
5. Open **TechNova Workstation Console** to register the device and configure RAID, BMC, and monitoring.

## 6. Storage Configuration
- The T7 ships with software RAID by default. For hardware RAID, install the optional TechNova MegaRAID 9560-8i controller.
- Supported levels via TechNova Workstation Console: RAID 0, 1, 5, 6, 10.
- M.2 NVMe slots support PCIe Gen4 x4 each. Mixing Gen3 and Gen4 in the same array is supported but limits throughput to the slowest device.

## 7. Remote Management (BMC / IPMI)
- The dedicated BMC port provides IPMI 2.0 and Redfish.
- Default credentials: username `admin`, password printed on the chassis side label.
- Change the default password during first login. Enable HTTPS-only and disable IPMI over LAN if not required.

## 8. GPU Installation Notes
- The T7 supports up to two double-wide GPUs in PCIe Gen5 x16 slots 1 and 3.
- Connect both 12VHPWR cables when installing the RTX 6000 Ada; partial connection will trigger a fan ramp-up and a BMC alert.
- After installing a new GPU, run **TechNova Workstation Console > Diagnostics > GPU Stress Test** for 10 minutes to verify stability.

## 9. Indicator Lights and Audio Codes
| Indicator | Pattern | Meaning |
|---|---|---|
| Front power LED | Solid white | System on |
| Front power LED | Blinking amber | Power supply fault - check redundant PSU |
| Front diagnostic LEDs | "1-3-2" beep code | Memory failure |
| Front diagnostic LEDs | "5-1-1" beep code | CPU thermal trip |
| Rear BMC LED | Solid green | BMC healthy |
| Rear BMC LED | Blinking amber | BMC alert - check IPMI event log |

## 10. Drivers and Firmware
- Use **TechNova Workstation Console** to apply BIOS, BMC, NIC, RAID, and GPU driver updates as a coordinated bundle.
- For air-gapped environments, download the offline update bundle from `support.technova.com/workstation/firmware`.

## 11. Service Access
- Tool-less side panel: press the green latch at the top-rear and slide the panel back.
- All hot-swap bays (PSU, fans, drives) are color-coded green.
- Service Tag is on a pull-out card at the front-top of the chassis.
