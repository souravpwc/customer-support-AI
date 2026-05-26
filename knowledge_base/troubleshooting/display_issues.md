# Troubleshooting: Display Issues (Flickering, No Signal, Resolution, External Monitor)

**Document ID:** TS-DISP-003
**Applies to:** NovaBook laptops, WorkStation Pro T7, UltraView U2724Q
**Severity:** Medium
**Estimated time:** 10-20 minutes
**Last Updated:** 2025-09-25

## Symptoms
- Flickering, flashing, or tearing on the screen.
- External monitor not detected.
- Wrong resolution or refresh rate.
- Color cast (pink, green, yellow tint) or color banding.
- Black screen after wake from sleep.

## Required Information
1. Internal panel or external monitor? Both?
2. Cable type (HDMI / DisplayPort / USB-C / Thunderbolt) and length.
3. Through a dock / hub or direct?
4. Was the issue triggered by a recent driver, OS, or BIOS update?
5. Does the issue persist in Safe Mode?

## Diagnostic Workflow

### Step 1: Panel self-test (laptops)
- Power off.
- Hold **D** while pressing Power. Release **D** after 5 seconds.
- Color bars should cycle through red, green, blue, white, black. If they display correctly, the LCD and panel cable are good.

### Step 2: External monitor swap-out
- Connect the laptop or workstation to a second known-good monitor.
- Swap the cable for a known-good cable.
- If the second monitor works, the original monitor or cable is the fault.

### Step 3: USB-C / Thunderbolt direct vs. dock
- Disconnect from any dock or hub. Connect monitor directly to the laptop / workstation.
- If display works direct, the dock firmware may be out of date - run **TechNova Dock Firmware Updater**.

### Step 4: Refresh rate and resolution
- Right-click desktop > **Display Settings**.
- Set **Display resolution** to the panel's native (e.g., 3456 x 2160 for XPS 15, 3840 x 2160 for U2724Q).
- Click **Advanced display** > set refresh rate to the highest supported (120 Hz for XPS 15 panel, 120 Hz for U2724Q via DP/USB-C).

### Step 5: Graphics driver clean install
- Open **TechNova Companion** and apply available GPU driver updates.
- Alternatively, download the latest driver from the GPU vendor (NVIDIA / Intel / AMD) and run a **clean install**.
- Reboot.

### Step 6: Test in Safe Mode
- Hold Shift while clicking Restart > Troubleshoot > Advanced options > Startup Settings > Restart > **4 (Safe Mode)**.
- If flickering stops in Safe Mode, a third-party app or driver is the cause. Most common: third-party display utilities, GPU overclocking tools, or out-of-date dock drivers.

## Decision Tree / Resolution

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Flicker on internal panel, external works fine | Panel cable or panel itself | Run panel self-test; if pass, escalate for panel cable inspection. |
| External monitor not detected via dock | Dock firmware / TB driver | Update dock firmware; reseat TB cable; try another TB port on host. |
| 60 Hz max even on 120 Hz panel | Wrong cable (HDMI for high refresh) | Use DisplayPort or USB-C; HDMI 2.0 cannot do 4K@120 Hz. |
| Color cast / banding | Color profile mismatch | Reset color profile under Settings > System > Display > Color management. |
| Black screen after sleep | GPU driver / Modern Standby quirk | Update GPU driver and BIOS; disable Fast Startup; if persists, set sleep to Hibernate. |
| Tearing during gaming | V-Sync / G-Sync off | Enable G-Sync in NVIDIA Control Panel; enable VRR in Windows Display settings. |

## Escalation Criteria
Escalate to L2 / depot if:
- Panel self-test shows missing colors, lines, or dead pixel clusters.
- Multiple external monitors and cables fail to display from the same host port (likely GPU output fault).
- Issue persists in clean Windows install with default drivers.
