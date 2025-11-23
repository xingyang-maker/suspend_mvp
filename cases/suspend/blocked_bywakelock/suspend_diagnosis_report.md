# Suspend Diagnosis Report

**Collection Directory**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\suspend\blocked_bywakelock`  
**Time**: 2025-11-23T18:08:05.099498

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
**Result:** Suspend has never been attempted.  

- `success: 0`  
- `fail: 0`  
- `suspend attempts: 0`  

The kernel reports **zero suspend attempts** and **zero successful suspends**, which means the system never entered a low‑power state.

---

## Wakelock Analysis  
**Active wakelocks that block suspend**

| Name (type)                         | PID | Status | Active time |
|-------------------------------------|-----|--------|-------------|
| **PowerManager.Service.Display**    | 1922| **Active** | ≈ 941 s (≈ 15 min) |
| **PowerManager.SuspendLockout**      | 1922| **Active** | ≈ 941 s (≈ 15 min) |

Both of the above are **native** wakelocks held by the system process (`pid 1922`).  

- `PowerManager.Service.Display` is the classic “screen‑on” wakelock – the display is on, so the device is not allowed to suspend.  
- `PowerManager.SuspendLockout` is a special lock that deliberately prevents suspend (e.g., “Stay awake while charging”, developer‑option “Stay awake”, or a bugged system component).  

All other wakelocks are **inactive**; no third‑party app is holding a lock.

**Conclusion:** The active **Display** and **SuspendLockout** wakelocks are the direct reason why the kernel never attempts to suspend.

---

## Root Cause (if applicable)  
*Not applicable* – suspend failure is fully explained by the active wakelocks. No kernel‑level errors are present in `dmesg` (the log is empty), and `/d/suspend_stats` shows no failure counters.

---

## Recommendations  

1. **Turn off the display / let the screen sleep**  
   - Manually press the power button or set a shorter screen‑timeout (`Settings → Display → Sleep`).  
   - Verify that the `PowerManager.Service.Display` wakelock disappears (`adb shell dumpsys power | grep "Display"`).

2. **Clear the SuspendLockout wakelock**  
   - Check for the “Stay awake while charging” developer option:  
     ```bash
     adb shell settings get global stay_on_while_plugged_in
     ```  
     If the value is non‑zero, clear it:  
     ```bash
     adb shell settings put global stay_on_while_plugged_in 0
     ```
   - Look for other system settings that may request a suspend lockout (e.g., “Never sleep” in battery‑optimization UI).  

3. **Confirm suspend can now be entered**  
   - Run a manual suspend test:  
     ```bash
     adb shell dumpsys suspend_control_internal
     ```
   - Or trigger a suspend via:  
     ```bash
     adb shell echo mem > /sys/power/state
     ```
   - After the screen is off and the lockout cleared, you should see `suspend attempts` increase and `success` counters in `/d/suspend_stats`.

4. **If the lockout persists after the above steps**  
   - Identify the component that is programmatically acquiring `PowerManager.SuspendLockout` (e.g., a custom ROM feature, background service, or a buggy driver).  
   - Use `adb shell dumpsys power | grep "SuspendLockout"` to see the stack trace or caller.  
   - Update/disable the offending component, or file a bug report with the OEM.

5. **General power‑optimisation checklist**  
   - Disable “Always‑On Display” or “Ambient Display”.  
   - Ensure no app is holding a *partial* wake lock (`adb shell dumpsys power | grep "WakeLock"`).  
   - Verify battery‑optimisation is enabled for all third‑party apps (`Settings → Battery → Battery optimisation`).  

Once the display is off and the suspend lockout cleared, the kernel will be able to enter suspend, and the counters in `/d/suspend_stats` will start reflecting successful suspend cycles.

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
