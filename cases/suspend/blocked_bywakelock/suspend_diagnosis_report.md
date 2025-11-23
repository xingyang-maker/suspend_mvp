# Suspend Diagnosis Report

**Collection Directory**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\suspend\blocked_bywakelock`  
**Time**: 2025-11-23T17:48:26.691555

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

**## Suspend Status**  
- `/d/suspend_stats` is empty, so no kernel‑level statistics are available.  
- The `dumpsys suspend_control_internal` section shows **no suspend attempts** have been recorded (`suspend attempts: 0`).  
- All counters for successes/failures are **0** (`success: 0`, `fail: 0`).  
- **Conclusion:** The device is **not entering suspend at all**.

---

**## Wakelock Analysis**  
The wakelock table from `dumpsys suspend_control_internal` reveals several **active** locks that are currently preventing suspend:

| Name                               | Type   | Status   | Active Count | Total Time |
|------------------------------------|--------|----------|--------------|------------|
| **PowerManager.Service.Display**   | Native | **Active** | 1            | 941 874 ms |
| **PowerManager.SuspendLockout**    | Native | **Active** | 1            | 941 839 ms |
| **a600000.hsusb** (USB)            | Kernel | **Active** | 1            | 1 018 798 ms |

- **Display wakelock** – the screen is on (or a “stay‑awake while charging” setting is enabled).  
- **SuspendLockout** – a system‑level lock that deliberately blocks suspend (often set by a developer option, a debugging tool, or a misbehaving app).  
- **USB (hsusb) wakelock** – a USB‑related wake lock, typically held while a USB cable is attached, USB debugging is active, or a peripheral driver is busy.

No other wakelocks are active; the rest are **Inactive**.

Because active wakelocks are present, the system cannot proceed to suspend, which explains the zero suspend attempts.

---

**## Root Cause (not applicable)**  
A root‑cause analysis of `dmesg` is **not required** here because suspend failures are directly attributable to active wakelocks.

---

**## Recommendations**

1. **Turn off the display / disable “Stay awake”**
   - Settings → Developer options → **Stay awake (Screen will never sleep while charging)** – make sure this is **unchecked**.
   - Manually turn off the screen or let it time‑out.

2. **Identify and clear the `PowerManager.SuspendLockout`**
   - This lock is usually set by:
     - **Developer options** – “Enable wake‑lock debugging” or “Force keep‑awake”.
     - **Battery‑optimisation** tools or third‑party apps that request a suspend lock.
   - Steps:
     1. Re‑boot the device into **Safe Mode** (press power button, then long‑press “Power off” → “Reboot to safe mode”).  
        - If the lock disappears, a third‑party app is responsible; uninstall or update the offending app.  
     2. If it persists, clear it via **adb** (requires root or appropriate permissions):
        ```bash
        adb shell dumpsys power | grep SuspendLockout
        # To release (if you have permission):
        adb shell su -c "echo 0 > /sys/power/wakeup_count"
        ```
     3. Check for any **system services** that may have called `PowerManager.acquireSuspendLock()` (e.g., certain OEM power‑saving or performance‑tuning apps). Disable or update them.

3. **Clear the USB wake lock**
   - Disconnect any USB cable or peripheral.
   - Disable **USB debugging** (Settings → Developer options → USB debugging) if not needed.
   - If the lock remains while the cable is unplugged, a driver may be stuck; a quick reboot usually clears it.

4. **Verify with `dumpsys` after changes**
   - Run:
     ```bash
     adb shell dumpsys suspend_control_internal
     ```
   - Ensure **no active wakelocks** remain (all entries should show `Inactive`).

5. **Test suspend functionality**
   - Force a suspend manually:
     ```bash
     adb shell echo mem > /sys/power/state
     ```
   - If the device enters suspend (screen turns off, no wake‑up for a few seconds), the issue is resolved.

6. **Monitor for recurrence**
   - Keep an eye on `/d/suspend_stats` (or `cat /sys/kernel/debug/power/suspend_stats` on newer kernels) to confirm that suspend attempts and successes start occurring after the fixes.

By clearing the active display, suspend‑lockout, and USB wake locks, the system should be able to enter suspend normally, and the suspend statistics will begin to show successful suspend cycles.

---

## 📁 Evidence Files

- **dumpsys_suspend.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\suspend\blocked_bywakelock\dumpsys_suspend.txt`

---

## ✅ Verification Checklist

After fixing the identified issue:

1. **Re-run diagnosis**: Collect new evidence and verify the issue is resolved
2. **Check suspend_stats**: Verify success count increases and fail count remains 0
3. **Check wakelocks**: Ensure no active wakelocks in dumpsys output
4. **Measure power**: Compare power consumption before/after fix (expect ≥3% reduction)
