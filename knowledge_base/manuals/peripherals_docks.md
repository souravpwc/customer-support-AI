# TechNova Dock Catalog - Product Manual

**Document ID:** MAN-ACC-DK-CAT-2025
**Product Category:** Accessories - Docks and Hubs
**Audience:** Hybrid workers, Enterprise IT, Engineering
**Last Updated:** 2025-09-30

## 1. Catalog Overview
The TechNova dock lineup ranges from portable USB-C travel hubs to enterprise dual-Thunderbolt-4 docks with managed firmware. All TechNova docks include:
- TechNova Dock Firmware Updater support (Windows and macOS).
- TechNova Dock Manager for Intune (managed firmware deployment).
- USB-IF and Thunderbolt 4 certification where applicable.
- 1-year standard warranty (3-year optional via Accessory Care).

The detailed manual for the **Thunderbolt 4 Dock TD-340** is published in MAN-ACC-CAT-2025 (accessories.md). This document covers the rest of the lineup.

## 2. TechNova USB-C Travel Hub TD-220

| Spec | Value |
|---|---|
| Host connection | USB-C 3.2 Gen 2 (10 Gbps) |
| Power delivery | 100 W passthrough to host |
| Displays | 1x 4K @ 60 Hz (HDMI) or 1x QHD @ 144 Hz (DP via USB-C alt mode) |
| Ports | 1x HDMI 2.0, 1x USB-C 3.2 Gen 2 (data + 100 W PD in), 2x USB-A 3.2 Gen 1, 1x microSD/SD reader, 1x 3.5 mm combo audio, 1x RJ-45 1 GbE |
| OS support | Windows 11, macOS 13+, Linux (kernel 5.15+), iPad Pro/Air (USB-C) |
| Weight | 110 g |
| Dimensions | 124 x 53 x 16 mm |

### Use Cases
- Daily travel kit alongside a NovaBook Air 13 / Pro 14.
- Customer demos, conference rooms, and hot-desk environments.

### Setup
1. Plug the captive USB-C cable into the host.
2. Connect display, network, peripherals, and optionally a USB-C PD adapter (>= 30 W recommended) for host charging.
3. No driver installation is required on Windows 11 or macOS 13+.

## 3. TechNova Thunderbolt 4 Dock TD-340 (cross-reference)
See MAN-ACC-CAT-2025 section 2 for the full TD-340 manual. Summary:
- Thunderbolt 4 host link.
- 130 W host PD.
- Up to 3x 4K @ 60 Hz or 1x 8K @ 60 Hz.
- 4x USB-A, 1x USB-C downstream, 1x 2.5 GbE, audio combo.

## 4. TechNova Enterprise Thunderbolt 4 Dock TD-410

| Spec | Value |
|---|---|
| Host connection | Thunderbolt 4 (40 Gbps) |
| Power delivery | 180 W to host (works fully with NovaBook XPS 15 and WorkStation laptops) |
| Displays | Up to 4x 4K @ 60 Hz, or 2x 8K @ 60 Hz, or 1x 8K + 2x 4K |
| Ports | 1x TB4 upstream, 3x TB4 downstream, 6x USB-A 3.2 Gen 2, 2x USB-C 3.2 Gen 2, 2x DisplayPort 1.4, 1x HDMI 2.1, 1x 10 GbE RJ-45, 1x 3.5 mm headset, 1x line-out, Kensington lock slot |
| Management | TechNova Dock Manager for Intune, supports remote firmware push, asset tagging, MAC pass-through |
| OS support | Windows 11, macOS 13+, Linux (kernel 6.1+) |
| Power brick | 230 W bundled |
| Weight | 1.15 kg |

### Use Cases
- Enterprise hot-desk and shared-workstation deployments where IT must manage firmware centrally.
- High-end creative workstations driving multiple 4K/8K monitors.

### MAC Address Pass-Through
- The TD-410 supports MAC address pass-through (MAPT) for PXE boot and 802.1X authentication tied to a laptop's identity.
- Enable in BIOS Setup (F2) > Network > MAC Address Pass-Through > **On**.
- Confirm in Dock Manager > Device > "MAPT active = Yes".

## 5. Lineup Summary

| Model | Host link | Max PD | Max displays | Manageable | Target use |
|---|---|---|---|---|---|
| TD-220 | USB-C 3.2 Gen 2 | 100 W | 1x 4K @ 60 Hz | No | Travel, conference rooms |
| TD-340 | Thunderbolt 4 | 130 W | 3x 4K @ 60 Hz / 1x 8K | Yes (TPM only) | Premium home office |
| TD-410 | Thunderbolt 4 | 180 W | 4x 4K @ 60 Hz / 2x 8K | Yes (Intune + MAPT) | Enterprise hot-desk |

## 6. Driver and Firmware Updates
- Open **TechNova Dock Firmware Updater** (Windows / macOS) or **TechNova Dock Manager** (managed fleets).
- For full host PD on TD-340 and TD-410, use the included power brick. Third-party bricks may downgrade PD by 30 W or more.
- Multi-monitor wake-from-sleep on Windows requires firmware >= `1.4.7` (TD-340) or `2.1.3` (TD-410).

## 7. Common Issues and Resolutions
| Symptom | Likely cause | Action |
|---|---|---|
| Monitor not detected after wake | Old dock firmware | Update via Dock Firmware Updater. |
| Slow charge / "Slow charger" message | Using a non-TechNova power brick | Re-install the included brick; if missing, order replacement part. |
| 2.5 GbE / 10 GbE link drops | Driver mismatch | Reinstall network driver from TechNova Companion. |
| KVM-like behavior not working | TD-220 does not support KVM | Use TD-340 or TD-410, or pair with an UltraView monitor that has built-in KVM. |

## 8. Warranty
All TechNova docks carry a **1-year limited warranty** (3-year optional via TechNova Accessory Care). The included power brick is covered for the same period; replacement bricks are sold separately at MSRP if out of warranty.
