# Troubleshooting: Battery Drains Quickly or Will Not Charge

**Document ID:** TS-LT-BAT-001
**Applies to:** NovaBook XPS 15, NovaBook Air 13, NovaBook Pro 14
**Severity:** Medium
**Estimated time:** 10-20 minutes
**Last Updated:** 2025-10-01

## Symptoms
- Battery percentage drops faster than expected (more than 15% per hour at idle on battery).
- Laptop does not charge when plugged in, or charges very slowly.
- "Plugged in, not charging" message in Windows.
- Charging LED is off or amber when adapter is connected.

## Required Information Before Troubleshooting
1. Device model and Service Tag.
2. Wattage of the power adapter in use (printed on the brick - look for "Output: 20.0 V / 6.5 A = 130 W").
3. Operating system and version (Windows 11 23H2, etc.).
4. Approximate age of the battery (in months).
5. Whether a recent BIOS, Windows, or driver update was installed.

## Diagnostic Workflow

### Step 1: Verify the power adapter
- Inspect the cable for cuts, kinks, or scorch marks.
- Confirm the adapter is **TechNova certified** and rated **>= 100 W USB-C PD** for the NovaBook XPS 15.
- If a "slow charger" notification appears, the adapter cannot supply enough wattage. Swap to a known-good 130 W adapter.

### Step 2: Try a different wall outlet
- Plug into a different grounded outlet, ideally not on a surge-protected power strip.
- If a power strip is required, verify it is rated for the adapter wattage.

### Step 3: Hard reset (drain residual power)
1. Disconnect the adapter and all peripherals.
2. Hold the **power button for 30 seconds**.
3. Reconnect only the adapter and power on.

### Step 4: Run the built-in battery diagnostic
- Reboot. At the TechNova splash screen, press **F12** to enter the One-Time Boot Menu.
- Select **Diagnostics** > **Battery**. The test takes 2-4 minutes.
- Note any error code that appears (format `2000-0xxx` or `BAT-xxx`).

### Step 5: Generate a Windows battery report
1. Open Command Prompt **as Administrator**.
2. Run: `powercfg /batteryreport /output "%USERPROFILE%\battery-report.html"`
3. Open the report and check **Battery capacity history**.
4. If **Full Charge Capacity** is less than 60% of **Design Capacity**, the battery is degraded and should be replaced.

### Step 6: Update BIOS and chipset drivers
- Open **TechNova Companion** > Check for Updates.
- Apply BIOS and chipset/EC firmware updates if available.
- Reboot and retest.

### Step 7: Reset the Embedded Controller (EC)
- Power off.
- Hold **Fn + Power** for 15 seconds.
- Release and power on normally. This resets the EC and battery gas-gauge calibration.

## Decision Tree / Resolution

| Diagnostic Result | Action |
|---|---|
| Battery test passes, charging now works | No further action. Recommend Battery Care mode at 80% cap. |
| Battery test fails with error 2000-0131 | Battery is at end of life. Verify warranty status and create a battery replacement service request. |
| Battery test passes, but adapter charges slowly | Adapter is under-rated or faulty. Replace with certified 130 W TechNova adapter. |
| Battery test passes, OS shows "Plugged in, not charging" | Toggle Battery Care off temporarily; verify Windows Updates; reset EC (Step 7). |
| Charging LED never lights up regardless of adapter | Likely DC-in / motherboard fault. Escalate to depot service. |

## Escalation Criteria
Escalate to L2 / depot if:
- Two different known-good adapters both fail to charge.
- Diagnostic returns motherboard fault codes (2000-0511, 2000-0512).
- Battery has visibly swollen or deformed the chassis. **Stop using the device immediately** and instruct the customer to disconnect power.

## Safety Notice (Swollen Battery)
A swollen battery is a fire and injury hazard. The customer should:
1. Power off the device.
2. Disconnect the adapter.
3. Place the device on a non-flammable surface away from people.
4. Not attempt to remove the battery themselves.
5. Wait for TechNova-authorized service.
