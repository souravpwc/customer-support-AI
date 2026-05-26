# Troubleshooting: Driver Installation After OS Reinstall

**Document ID:** TS-DRV-006
**Applies to:** NovaBook XPS 15, NovaBook Air 13, NovaBook Pro 14, WorkStation Pro T7
**Severity:** Low-Medium
**Estimated time:** 30-60 minutes
**Last Updated:** 2025-08-20

## Symptoms
- Just reinstalled Windows; several devices show "Unknown device" in Device Manager.
- No Wi-Fi or no audio after a clean Windows install.
- Touchpad gestures missing, function keys not working.

## Required Information
1. Model and Service Tag.
2. Edition of Windows installed (Home / Pro / Workstations / Enterprise) and version.
3. Was the install from TechNova recovery media or generic Microsoft media?
4. Internet access available (Ethernet / phone tether)?

## Recommended Install Order
Drivers should be installed in this sequence to avoid conflicts:

1. **Chipset / Intel Management Engine**
2. **Storage / Intel RST or AMD RAID**
3. **Graphics (Intel + NVIDIA, in that order)**
4. **Network: Ethernet, then Wi-Fi, then Bluetooth**
5. **Audio (Realtek or Cirrus)**
6. **Touchpad / HID**
7. **Card readers, fingerprint, IR camera**
8. **BIOS / Firmware updates**
9. **TechNova Companion (last)**

## Diagnostic Workflow

### Step 1: Get on the network
- If Wi-Fi driver is missing, plug in a USB-C or Thunderbolt **Ethernet adapter** (TechNova TD-340 dock or USB-A 3.0 RJ-45 dongle work without drivers on Windows 11).
- Alternatively, USB-tether to a phone.

### Step 2: Install TechNova Companion
- Browse to `support.technova.com/companion` and download the latest installer.
- Run as administrator. The first launch will detect missing drivers automatically using the Service Tag.

### Step 3: Use Service-Tag-based driver bundle (offline)
- If the device has no network at all, on a working PC visit `support.technova.com/drivers`, enter the Service Tag, and download the **OS deployment driver pack** (single ZIP).
- Extract the ZIP onto a USB drive, then on the affected device run `DriverPackInstall.exe`.

### Step 4: Verify all devices
- Open **Device Manager**. There should be zero yellow exclamation marks. If any remain:
  - Right-click > **Properties** > Details tab > Property = `Hardware Ids`. Copy the `VEN_xxxx&DEV_xxxx` value.
  - Search `support.technova.com/drivers` for that hardware ID.

### Step 5: Function keys not working
- Install **TechNova Function Key Service** via Companion. Without it, F1-F12 default to multimedia roles and toggling requires Fn-Lock.

## Decision Tree / Resolution

| Problem | Resolution |
|---|---|
| All drivers refuse to install | Confirm Windows version matches a TechNova-supported edition (Win 11 Home/Pro x64 23H2+); generic Windows media may install ARM or N edition that lacks codecs. |
| Wi-Fi driver installs but no networks listed | Reboot; if still empty, install Intel Wi-Fi driver + Intel PROSet, then reboot. |
| Touchpad cursor jumpy after install | Install TechNova Touchpad driver, NOT just the Microsoft Precision Touchpad generic driver. |
| Fingerprint reader unrecognized | Install in order: Chipset > Trusted Platform Module > **TechNova Goodix Fingerprint** > set up Windows Hello again. |
| BIOS update refuses to install on battery | Plug in the AC adapter; BIOS updates require AC + battery > 10%. |

## Reference: Recovery Media
- TechNova Cloud Recovery: `cloud.technova.com/recovery` lets you build a bootable USB with the original factory image including OEM drivers.
- A bootable USB takes ~15 minutes to build and a 16 GB drive is required.
