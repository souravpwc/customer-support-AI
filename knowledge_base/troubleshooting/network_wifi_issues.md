# Troubleshooting: Wi-Fi and Network Connectivity

**Document ID:** TS-NET-004
**Applies to:** NovaBook XPS 15, NovaBook Air 13, NovaBook Pro 14
**Severity:** Medium
**Estimated time:** 10-15 minutes
**Last Updated:** 2025-09-18

## Symptoms
- Wi-Fi not listed in available networks.
- Connects to Wi-Fi but no internet ("No internet, secured").
- Slow Wi-Fi or frequent disconnects.
- Bluetooth devices disconnect when Wi-Fi is active (2.4 GHz interference).

## Required Information
1. Wi-Fi network band (2.4 GHz, 5 GHz, 6 GHz) and security (WPA2, WPA3).
2. Other devices on the same network working normally?
3. Router make/model.
4. Adapter shown in Device Manager (Intel AX211, Killer AX1675, etc.).
5. VPN active?

## Diagnostic Workflow

### Step 1: Toggle airplane mode and Wi-Fi
- Press **Fn + F2** (or the airplane key) to toggle airplane mode on, wait 5 seconds, toggle off.
- Click the Wi-Fi icon and disable/re-enable Wi-Fi.

### Step 2: Forget and re-add the network
- Settings > Network & Internet > Wi-Fi > Manage known networks > select the SSID > **Forget**.
- Reconnect, entering the password again.

### Step 3: Verify adapter in Device Manager
- Open **Device Manager** > Network adapters.
- The Wi-Fi adapter should appear with no yellow exclamation. If missing, the driver is uninstalled or hardware failure.

### Step 4: Update / reinstall the Wi-Fi driver
- Open **TechNova Companion** > Drivers > install the latest Wi-Fi driver.
- If problems persist: Device Manager > right-click adapter > **Uninstall device** (check "Delete the driver software") > Reboot. Windows will reinstall a clean driver from TechNova Companion.

### Step 5: Reset TCP/IP stack
Open Command Prompt as Administrator and run, one at a time:
```
netsh winsock reset
netsh int ip reset
ipconfig /flushdns
ipconfig /release
ipconfig /renew
```
Reboot after.

### Step 6: Disable Wi-Fi power management
- Device Manager > Wi-Fi adapter > Properties > **Power Management** > uncheck "Allow the computer to turn off this device to save power".

### Step 7: Check band steering / router compatibility
- If the SSID broadcasts 2.4, 5, and 6 GHz under the same name and only 6 GHz fails, the issue is **WPA3-only requirement on Wi-Fi 6E**. Either set the network to WPA2/WPA3 mixed, or update the Intel Wi-Fi driver.

### Step 8: Roll back BIOS (last resort)
- If the issue began after a BIOS update, TechNova Companion > **Recovery** > **Restore previous BIOS**.

## Decision Tree / Resolution

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Wi-Fi adapter missing in Device Manager | Driver not installed, hardware fault | Run Companion driver install; if still missing, run hardware diagnostics (F12 > Diagnostics). |
| "No internet, secured" after connect | DHCP / IPv6 issue, captive portal | Reset TCP/IP stack; open browser to trigger captive portal; disable IPv6 temporarily. |
| Slow throughput on 5 GHz | Driver power saving, channel congestion | Disable Wi-Fi power saving; in router, set 5 GHz to channel 36 or 149. |
| Drops when Bluetooth in use | 2.4 GHz coexistence | Use 5 GHz/6 GHz Wi-Fi or update Wi-Fi + BT drivers together. |
| Can connect at home, not at office | 802.1X / cert / VPN config | Confirm corporate Wi-Fi profile pushed via Intune/MDM; verify VPN posture compliance. |

## Escalation Criteria
- Adapter not detected even after driver reinstall and BIOS recovery.
- Hardware diagnostics (F12 > Diagnostics > Wireless) returns an error code in the 2000-04xx range.
- Issue isolated to a specific frequency band that other devices use successfully on the same network.
