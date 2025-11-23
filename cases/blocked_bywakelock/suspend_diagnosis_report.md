# Suspend Diagnosis Report

**Collection Directory**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\blocked_bywakelock`  
**Time**: 2025-11-23T17:32:17.846676

---

## 🔴 CONCLUSION: Suspend Failure Detected

**Root Cause**: Root cause: Active wakelocks preventing suspend: PowerManagerService.Display, PowerManager.SuspendLockout, a600000.hsusb

---

## Step 2️⃣: Wakelock Analysis
**Purpose**: Check for active wakelocks preventing suspend  
**File**: `dumpsys suspend_control_internal` → `dumpsys_suspend.txt`

❌ **Result**: Active wakelocks found (ROOT CAUSE)
**Active Wakelocks**:
- `PowerManagerService.Display`
- `PowerManager.SuspendLockout`
- `a600000.hsusb`

**Analysis stops here** - Root cause identified

### 原始 Wakelock Dump (关键片段)
```text
 |                                                                                           WAKELOCK STATS                                                                                        | 
 | NAME                           | PID    | TYPE   | STATUS   | ACTIVE COUNT | TOTAL TIME   | MAX TIME     | EVENT COUNT  | WAKEUP COUNT | EXPIRE COUNT | PREVENT SUSPEND TIME | LAST CHANGE      | 
 | PowerManagerService.WakeLocks  |   1922 | Native | Inactive |            0 |      13204ms |       6497ms |          --- |          --- |          --- |                  --- |        1091401ms | 
 | PowerManagerService.Broadcasts |   1922 | Native | Inactive |            0 |        168ms |        141ms |          --- |          --- |          --- |                  --- |         810554ms | 
 | PowerManagerService.Display    |   1922 | Native | Active   |            1 |     941874ms |     653247ms |          --- |          --- |          --- |                  --- |        1099043ms | 
 | PowerManager.SuspendLockout    |   1922 | Native | Active   |            1 |     941839ms |     653211ms |          --- |          --- |          --- |                  --- |        1099043ms | 
 | radio-interface                |   1263 | Native | Inactive |            0 |        227ms |        217ms |          --- |          --- |          --- |                  --- |         140169ms | 
 | ApmOutput                      |   2453 | Native | Inactive |            0 |       1023ms |         44ms |          --- |          --- |          --- |                  --- |         137884ms | 
 | PowerManagerService.Booting    |   1922 | Native | Inactive |            0 |      52860ms |      52860ms |          --- |          --- |          --- |                  --- |         137126ms | 
 | qms_event_Handler_wakeLock_    |   1413 | Native | Inactive |            0 |        607ms |        445ms |          --- |          --- |          --- |                  --- |         124920ms | 
 | ApmAudio                       |   2453 | Native | Inactive |            0 |        498ms |         88ms |          --- |          --- |          --- |                  --- |         102870ms | 
 | ApmOutput                      |   1209 | Native | Inactive |            0 |         10ms |          4ms |          --- |          --- |          --- |                  --- |          89723ms | 
 | ApmAudio                       |   1209 | Native | Inactive |            0 |        222ms |         71ms |          --- |          --- |          --- |                  --- |          89717ms | 
 | qcril_pre_client_init          |   1263 | Native | Inactive |            0 |       1388ms |       1388ms |          --- |          --- |          --- |                  --- |          78474ms | 
 | event3                         |    --- | Kernel | Inactive |            4 |          3ms |          1ms |            4 |            0 |            0 |                  0ms |         810533ms | 
 | [timerfd]                      |    --- | Kernel | Inactive |            0 |          0ms |          0ms |            0 |            0 |            0 |                  0ms |              0ms | 
 | c42d000.qcom,spmi:pmw6100@0:pon_hlos@1300:pwrkey |    --- | Kernel | Inactive |            0 |          0ms |          0ms |            0 |            0 |            0 |                  0ms |              0ms | 
 | usb                            |    --- | Kernel | Inactive |            2 |        144ms |         98ms |            2 |            0 |            0 |                  0ms |          78847ms | 
 | fastrpc-non_secure             |    --- | Kernel | Inactive |            0 |          0ms |          0ms |            0 |            0 |            0 |                  0ms |              0ms | 
 | rmt_storage_541074766912       |    --- | Kernel | Inactive |            2 |         78ms |         75ms |            2 |            0 |            0 |                  0ms |         167621ms | 
... (truncated)
```

---

## 📋 总结
**结论**: Root cause: Active wakelocks preventing suspend: PowerManagerService.Display, PowerManager.SuspendLockout, a600000.hsusb

---

## 🤖 AI Comprehensive Analysis

## Suspend Status
- **/d/suspend_stats** – No data was provided (empty).  
- **dumpsys suspend_control_internal** – The “Suspend Stats” section shows **`success: 0`**, **`fail: 0`**, and **`suspend attempts: 0`**.  
- **Interpretation:** The device has **never successfully entered suspend** since the last boot. No suspend attempts have been recorded, indicating that something is actively preventing the system from reaching the suspend state.

---

## Wakelock Analysis
| Type | Name / Description | PID | Status | Active Since |
|------|--------------------|-----|--------|--------------|
| **PowerManager (Native)** | `PowerManager.Service.Display` | 1922 | **Active** | ~1 090 043 ms ago |
| **PowerManager (Native)** | `PowerManager.SuspendLockout` | 1922 | **Active** | ~1 090 043 ms ago |
| **Kernel** | `a600000.hsusb` (USB HSUSB controller) | — | **Active** | ~80 272 ms ago |

All other wakelocks listed are **Inactive**.  
The two active **PowerManager** wakelocks (`Display` and `SuspendLockout`) together with the active **USB** kernel wakelock are the **only blockers** that are keeping the system from suspending.

`last_failed_suspend` counters are **zero**, confirming that the suspend path never even started because the system was already considered “busy” by the active wakelocks.

---

## Root Cause (if applicable)
**Not applicable** – suspend failures are not due to kernel errors or driver problems; they are being prevented by active wakelocks.

---

## Recommendations
1. **Identify the source of the `Display` wakelock**  
   - This wakelock is held by the system UI when the screen is on.  
   - Ensure the display is turned **off** (press the power button or let the screen timeout expire).  
   - If the screen stays on indefinitely, look for an app that is forcing the screen to stay awake (e.g., “Stay awake while charging”, developer options, video playback, navigation apps, or a misbehaving foreground service).

2. **Investigate the `SuspendLockout` wakelock**  
   - `SuspendLockout` is a system‑level lock that the framework sets when a component explicitly asks the system not to suspend (often during critical operations like OTA updates, camera usage, or heavy I/O).  
   - Check recent logs (`logcat -b all -d | grep -i suspendlockout`) to see which process requested it.  
   - If it is held for an unusually long time, consider rebooting the device or stopping the offending service/app.

3. **Address the active USB wakelock (`a600000.hsusb`)**  
   - The USB controller stays awake when a USB device is connected or when USB debugging is active.  
   - **Disconnect any USB cable** (including chargers that expose data lines) and verify that the wakelock disappears.  
   - If you need the device plugged in, enable **“USB charging only”** mode (disable file transfer, tethering, or debugging) to allow the USB subsystem to release the lock.

4. **General steps to force a clean suspend**  
   - **Reboot** the device after clearing the above conditions; this resets any lingering wakelocks.  
   **or**  
   - Use `adb shell dumpsys power` to manually release a wakelock (e.g., `adb shell dumpsys power release [wakelock_name]`) **only if you are certain the lock is not needed**.

5. **Monitor after changes**  
   - Run `adb shell dumpsys suspend_control_internal` again.  
   - You should see `success` increment and `suspend attempts` > 0, with no active PowerManager wakelocks.  
   - Verify that `/d/suspend_stats` now shows non‑zero success counts.

By clearing the active display, suspend‑lockout, and USB wakelocks, the system will be able to enter deep suspend, and the suspend statistics will start reflecting successful suspend cycles. If after all of the above the device still never attempts suspend, revisit the kernel logs (`dmesg`) for hidden driver errors, but the current data points clearly to wakelock‑based blockage.

---

## 📁 Evidence Files

- **dumpsys_suspend.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\blocked_bywakelock\dumpsys_suspend.txt`

---

## ✅ Verification Checklist

After fixing the identified issue:

1. **Re-run diagnosis**: Collect new evidence and verify the issue is resolved
2. **Check suspend_stats**: Verify success count increases and fail count remains 0
3. **Check wakelocks**: Ensure no active wakelocks in dumpsys output
4. **Measure power**: Compare power consumption before/after fix (expect ≥3% reduction)
