# Troubleshooting: Device Will Not Power On or Will Not Boot to OS

**Document ID:** TS-LT-BOOT-002
**Applies to:** NovaBook XPS 15, NovaBook Air 13, NovaBook Pro 14, WorkStation Pro T7
**Severity:** High
**Estimated time:** 15-30 minutes
**Last Updated:** 2025-09-15

## Symptom Categories
- **A. No signs of life:** No LEDs, no fans, no sound.
- **B. Powers on but no display:** Fans spin, but black screen / no POST.
- **C. POSTs but does not reach OS:** TechNova splash appears, then errors or reboot loop.
- **D. Beep codes / diagnostic LEDs flash a pattern.**

## Required Information Before Troubleshooting
1. Model and Service Tag.
2. Exact symptom (which category above).
3. Any error message, beep code, or LED pattern.
4. Recent changes: new hardware installed, OS update, BIOS update, dropped/spilled-on?
5. Last known working configuration.

## Diagnostic Workflow - Category A (No signs of life)

### A.1 Verify power source
- Try a different outlet.
- For desktops: try a different IEC C13 power cable.
- For laptops: confirm adapter LED is on. If not, the brick or cable is faulty.

### A.2 Hard reset
- Laptop: disconnect adapter, hold **Power button for 30 seconds**, then reconnect adapter and power on.
- Desktop: unplug power, press and hold the **Power button for 15 seconds** to drain residual, then reconnect.

### A.3 Memory and storage reseat (T7 only)
- Power off and unplug.
- Open the side panel.
- Reseat each DIMM and each NVMe / SATA drive.
- Power on with **only one DIMM in slot A1** and no add-in cards.

If still no LEDs, fans, or beeps -> motherboard / PSU fault. Escalate to depot.

## Diagnostic Workflow - Category B (Powers on, no display)

### B.1 External display
- Connect an external monitor (HDMI for NovaBook, DisplayPort for T7).
- If external displays an image, the internal panel or display cable is faulty.

### B.2 Force POST diagnostics
- Power off.
- Hold **D key** while pressing the power button. Release **D** after 5 seconds. This forces the LCD self-test (color bars). If you see color bars, the panel is good.

### B.3 Reseat memory (desktops and serviceable laptops)
- Power off, unplug, and reseat memory modules.

### B.4 Clear CMOS
- For T7: press the **CMOS reset button** on the rear I/O for 5 seconds while AC is disconnected.
- For NovaBook: clearing CMOS requires depot service.

## Diagnostic Workflow - Category C (POSTs, no OS)

### C.1 Boot menu / Recovery
- Tap **F12** at the TechNova splash for the One-Time Boot Menu.
- Select **Diagnostics** > Run full hardware test.
- If hardware passes, boot **Windows Recovery**: F12 > **UEFI HTTP Boot** or use a Windows recovery USB.

### C.2 Common errors and resolutions

| Error / Message | Likely cause | Action |
|---|---|---|
| "No bootable device found" | Boot order wrong, or SSD not detected | F2 > Boot Sequence: confirm Windows Boot Manager is present and first. If SSD is missing in BIOS, reseat or replace. |
| "Operating system not found" | EFI partition corrupt | Boot WinRE > Startup Repair. If unsuccessful, run `bootrec /rebuildbcd`. |
| INACCESSIBLE_BOOT_DEVICE (BSOD) | Storage driver issue after Windows update | Boot WinRE > Uninstall latest update. |
| Reboot loop at splash | Failed firmware update | Power off; hold **Esc + Power** for 10 seconds to invoke BIOS Recovery from USB. |
| "BitLocker recovery key required" | TPM/PCR change after BIOS update | Provide the 48-digit BitLocker recovery key (Microsoft account or AD/Intune). |

## Diagnostic Workflow - Category D (Beep codes / LED patterns)

| Pattern (NovaBook) | Meaning | Action |
|---|---|---|
| 2 blinks amber | CPU failure | Escalate - motherboard service |
| 3 blinks amber | Memory failure | Reseat / replace RAM, run diagnostics |
| 4 blinks amber | Storage / SSD failure | Run diagnostics; reseat or replace SSD |
| 5 blinks amber | Coin-cell battery / RTC failure | Replace coin-cell battery |
| 6 blinks amber | Video / GPU failure | Test external display; escalate if needed |
| 7 blinks amber | Motherboard general failure | Escalate to depot |

## Escalation Criteria
Escalate to depot service if:
- No display after external monitor and panel self-test both fail.
- Diagnostic indicates CPU, motherboard, or video failure.
- BIOS recovery procedure (Esc + Power) does not bring the device back to a POST screen.
- Device was exposed to liquid or physical damage is visible.
