# Troubleshooting: Overheating, Loud Fans, and Slow Performance

**Document ID:** TS-PERF-005
**Applies to:** NovaBook XPS 15, NovaBook Pro 14, WorkStation Pro T7
**Severity:** Medium
**Estimated time:** 15-30 minutes
**Last Updated:** 2025-10-05

## Symptoms
- Device chassis is uncomfortably hot to the touch.
- Fans constantly running at high RPM, even at idle.
- System slows down or stutters; CPU is thermally throttling.
- Sudden shutdowns under load.

## Required Information
1. Workload during the issue (browsing, gaming, rendering, virtualization).
2. Ambient room temperature.
3. Surface placement (desk, bed, lap, hard vs. soft).
4. Last cleaning / age of device.
5. Active thermal profile in TechNova Companion (Quiet, Optimized, Performance, Ultra Performance).

## Diagnostic Workflow

### Step 1: Verify ventilation
- Move to a hard, flat surface. Soft surfaces (bed, cushion) block intake vents on the bottom.
- Confirm at least 10 cm clearance behind the device.
- Check for visible dust on intake and exhaust vents - clean with compressed air (short bursts; do not spin fans freely).

### Step 2: Set the correct thermal profile
- Open **TechNova Companion** > Thermal.
- For long sustained workloads (video render, 3D), select **Performance** or **Ultra Performance**.
- For meetings and light use, **Optimized** balances acoustics and temperature.

### Step 3: Identify the heavy process
- Open **Task Manager** (Ctrl+Shift+Esc) > **Processes** tab > sort by CPU.
- If a non-obvious process (e.g., `MoUsoCoreWorker`, antivirus scan, OneDrive sync) is at the top, give it 10-15 minutes to finish, or schedule it off-peak.

### Step 4: Driver and BIOS updates
- TechNova Companion > Drivers and BIOS > install all updates and reboot.
- Many CPU/EC thermal tuning fixes are shipped via BIOS.

### Step 5: Run the thermal diagnostic
- Reboot, press **F12** at the splash > Diagnostics > **Thermal**. The test runs CPU and GPU at sustained load while monitoring temperatures.
- A pass means the cooling system is functioning to spec. Persistent throttling outside diagnostics is usually a software/workload tuning issue.

### Step 6: Reapply / inspect thermal paste (depot only)
- If diagnostics show thermal trips and the device is more than 3 years old, schedule depot service for thermal paste reapplication.

### Step 7: Check Windows power plan
- Settings > System > Power & battery > **Power mode** > set to **Balanced** for daily use.
- Avoid **Best performance** on battery.

### Step 8: Malware scan
- Run a full scan with Windows Defender. Cryptominers and adware are a common cause of "always loud" fans on consumer laptops.

## Decision Tree / Resolution

| Observation | Likely Cause | Resolution |
|---|---|---|
| Fans loud at idle, low CPU usage | Background process or stale fan curve | Update BIOS; check Task Manager; reset thermal profile to Optimized. |
| CPU throttles below 1 GHz under load | Thermal limit reached | Improve ventilation; performance profile; depot service for paste if persistent. |
| Sudden shutdowns under load | Thermal trip or PSU under-spec | Verify adapter wattage (>=130 W for XPS 15); check vents; run thermal diagnostic. |
| Hot chassis, fans NOT running | Fan failure | Run F12 > Diagnostics > Fan. Replace fan via depot if it fails. |
| GPU temps high, CPU normal (T7) | GPU fan curve or seating | TechNova Workstation Console > GPU > set custom fan curve; verify both 12VHPWR cables seated. |

## Escalation Criteria
- Thermal diagnostic fails with error code 2000-0123 (overtemp) or 2000-0124 (fan).
- Repeated shutdowns under moderate workloads after BIOS/driver updates.
- Visible damage (melted plastic, discoloration around vents) -> stop use, escalate immediately for safety inspection.
