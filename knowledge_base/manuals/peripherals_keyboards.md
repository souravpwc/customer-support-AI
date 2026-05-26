# TechNova Keyboard Catalog - Product Manual

**Document ID:** MAN-ACC-KB-CAT-2025
**Product Category:** Accessories - Keyboards
**Audience:** Consumer, SMB, Enterprise, Developers, Creative Professionals
**Last Updated:** 2025-09-30

## 1. Catalog Overview
The TechNova keyboard lineup spans bundled USB workhorses, hot-swappable mechanical keyboards, ergonomic split designs, and slim multi-device Bluetooth boards. All wireless TechNova keyboards support TechNova Easy-Switch (pair up to 3 devices, switch with a function key) and are managed by **TechNova Peripheral Manager (TPM)** for key remapping, macros, and firmware updates.

## 2. TechNova Wired Keyboard KB-220

| Spec | Value |
|---|---|
| Connectivity | USB-A wired (1.8 m) |
| Layout | Full-size 104-key (US ANSI); 105-key UK / EU layouts on request |
| Switch type | Membrane, ~1.8 mm travel |
| Backlighting | None |
| Multimedia keys | Volume, mute, play/pause via Fn |
| Weight | 580 g |

### Use Cases
- Bundled with WorkStation Pro T5, T7, and T9 tower sales.
- IT spares stock; call-center and shared-desk environments.

## 3. TechNova Mechanical Keyboard KB-450

| Spec | Value |
|---|---|
| Connectivity | USB-C wired (detachable cable, 1.8 m) |
| Layout | Tenkeyless (TKL, 87-key) and Full-size (104-key) variants |
| Switch type | Hot-swappable 5-pin MX-style. Default: TechNova Tactile (Brown-equivalent). Linear (Red) and Clicky (Blue) variants stocked. |
| Keycaps | Double-shot PBT, Cherry profile |
| Backlighting | Per-key RGB |
| N-Key rollover | Full NKRO over USB |
| Weight | 880 g (TKL) / 1100 g (Full-size) |

### Key Features
- Hot-swap sockets allow switch replacement without soldering. Spare switch packs sold separately.
- Onboard memory stores up to 3 lighting profiles and 1 macro layer; portable to any computer.
- TPM exposes per-key lighting, macros, and meta-key swapping (Caps <-> Ctrl, etc.).

### Setup (KB-450)
1. Plug into any USB-A or USB-C port on the host.
2. The keyboard appears as `TechNova KB-450 Mechanical`.
3. Install **TPM** for full per-key lighting and macro control.

## 4. TechNova Ergonomic Split Keyboard KB-670

| Spec | Value |
|---|---|
| Connectivity | Bluetooth 5.3, 2.4 GHz USB-A dongle, USB-C wired |
| Layout | Split 88-key with tenting hinge (0° / 5° / 10° tilt) |
| Switch type | Low-profile tactile, ~2.5 mm travel |
| Palm rest | Detachable padded leatherette |
| Backlighting | White, 5 brightness levels |
| Battery | Built-in 2000 mAh Li-ion, up to 2 months per charge |
| Easy-Switch | Yes (Fn + 1 / 2 / 3) |
| Weight | 980 g (with palm rest) |

### Use Cases
- Customers with RSI, shoulder tension, or those transitioning from a non-split layout.
- Workers spending 6+ hours/day on the keyboard.

### Setup (KB-670)
1. Charge for 30 minutes via USB-C before first use.
2. Slide power switch to **On**.
3. Hold Fn + the Bluetooth key (1, 2, or 3) for 3 seconds to enter pairing for that slot; complete pairing on the host as `TechNova KB-670`.
4. Switch hosts later with Fn + 1 / 2 / 3.

## 5. TechNova Slim Multi-Device Keyboard KB-880

| Spec | Value |
|---|---|
| Connectivity | Bluetooth 5.3, USB-C wired |
| Layout | 78-key compact (no numpad) |
| Switch type | Low-profile scissor, ~1.5 mm travel |
| Backlighting | White, ambient-light auto-dimming, 5 brightness levels |
| Battery | Built-in 1500 mAh Li-ion, up to 10 days backlit on / 5 months backlit off |
| Easy-Switch | Yes (Fn + 1 / 2 / 3) |
| OS shortcuts | Pre-mapped F1-F12 for Windows, macOS, iPadOS (auto-detected) |
| Weight | 480 g |

### Use Cases
- Travel and hot-desk; pairs naturally with a NovaBook Air 13, a tablet, and a phone.
- Hybrid Windows + macOS + iPad workflows.

### OS Auto-Detection
- On first pairing, the keyboard fingerprints the host OS and switches its F-row to match (e.g., macOS shows Mission Control / Launchpad icons; Windows shows Task View / Notification Center).
- To override, hold Fn + Esc + W (Windows), M (macOS), or I (iPadOS).

## 6. Lineup Summary

| Model | Type | Layout | Connectivity | Battery | Best for |
|---|---|---|---|---|---|
| KB-220 | Wired membrane | Full-size 104 | USB-A | N/A | Bundled, kiosk, call center |
| KB-450 | Mechanical hot-swap | TKL or Full-size | USB-C | N/A | Developers, gamers, enthusiasts |
| KB-670 | Ergonomic split | 88-key split | BT / dongle / USB-C | 2 months | RSI prevention, comfort focus |
| KB-880 | Slim scissor | 78-key compact | BT / USB-C | 10 days (backlit) | Travel, multi-device, Mac/Win/iPad |

## 7. Driver and Firmware Updates
- Open **TechNova Peripheral Manager (TPM)** on Windows or macOS.
- Connect the keyboard via USB-C cable for firmware updates. Firmware updates over Bluetooth are **not** supported.

## 8. Common Issues and Resolutions
| Symptom | Likely cause | Action |
|---|---|---|
| Bluetooth keyboard not appearing in pair list | Slot in pairing mode for too short a time | Hold Fn + slot number for the full 3 seconds; LED should remain solid blue during pair window. |
| Function keys do media instead of F1-F12 (Windows) | Fn-Lock off | Press Fn + Esc to toggle Fn-Lock; permanent setting in TPM > Keyboard > "Default F-row". |
| Caps Lock LED not lighting on KB-450 | Per-key RGB profile overrides Caps Lock indicator | TPM > Lighting > enable "Reserve Caps Lock indicator". |
| Slow / lagging keystrokes on KB-880 over BT | Bluetooth coexistence with 2.4 GHz Wi-Fi | Move Wi-Fi to 5 GHz / 6 GHz, or switch keyboard to USB-C wired. |

## 9. Warranty
All TechNova keyboards carry a **1-year limited warranty** (3-year optional via TechNova Accessory Care). Keycaps, palm rests, and switch packs are classed as consumables and are not covered after 90 days from purchase. Mechanical switches that fail within warranty (KB-450) are replaced one-for-one with TechNova-stocked switch packs.
