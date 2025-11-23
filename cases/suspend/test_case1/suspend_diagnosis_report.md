# Suspend Diagnosis Report

**Collection Directory**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case1`  
**Time**: 2025-11-23T16:58:11.504769

---

## 🔴 CONCLUSION: Suspend Failure Detected

**Root Cause**: Root cause: Active wakelocks preventing suspend: PowerManagerService.Display, PowerManager.SuspendLockout, a600000.hsusb

---

## Step 1️⃣: Suspend Statistics Check
**Purpose**: Check if suspend succeeded or failed  
**File**: `/d/suspend_stats` → `suspend_stats.txt`

❌ **Result**: Suspend has failures
- Suspend has failures (success: 0, fail: 0)
- **Continue to Step 2** - Check for wakelocks

### 原始 Suspend Stats (关键片段)
```text
fail: 0
failed_freeze: 0
failed_prepare: 0
failed_suspend: 0
failed_suspend_late: 0
failed_suspend_noirq: 0
failed_resume_noirq: 0
failed_resume_early: 0
failed_resume: 0
failures:
  last_failed_dev:	
  last_failed_errno:	0
  last_failed_step:	
... (truncated)
```

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

## Step 3️⃣: Kernel Log Analysis
**Purpose**: Check for suspend entry and failure details  
**File**: `dmesg -T` → `dmesg.txt`

❌ **Result**: No suspend entry found
- System did not attempt to enter suspend
- Check if suspend is triggered properly

### 原始 dmesg 日志 (关键片段)
```text
[Sat Nov 15 08:23:01 2025] modprobe: Failed to insmod '/system/lib/modules/ptp_kvm.ko' with args '': Operation not supported on transport endpoint
[Sat Nov 15 08:23:01 2025] modprobe: Failed to insmod '/system/lib/modules/ptp_kvm.ko' with args '': Operation not supported on transport endpoint
[Sat Nov 15 08:23:01 2025] modprobe: Failed to load module /system_dlkm/lib/modules/ptp_kvm.ko: Operation not supported on transport endpoint
[Sat Nov 15 08:23:01 2025] modprobe: Failed to load module /system_dlkm/lib/modules/ptp_kvm.ko: Operation not supported on transport endpoint
[Sat Nov 15 08:23:01 2025] Bluetooth: Bind failed -13
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
[Sat Nov 15 08:23:03 2025] rdbg_probe: register_smp2p_out failed for rdbg_adsp
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
[Sat Nov 15 08:23:03 2025] rdbg_probe: register_smp2p_out failed for rdbg_cdsp
[Sat Nov 15 08:23:03 2025] sdhci_msm 8844000.sdhci: nvmem cell get failed
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
[Sat Nov 15 08:23:03 2025] rdbg_probe: register_smp2p_out failed for rdbg_adsp
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
[Sat Nov 15 08:23:03 2025] rdbg_probe: register_smp2p_out failed for rdbg_cdsp
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
[Sat Nov 15 08:23:03 2025] rdbg_probe: register_smp2p_out failed for rdbg_adsp
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
[Sat Nov 15 08:23:03 2025] rdbg_probe: register_smp2p_out failed for rdbg_cdsp
[Sat Nov 15 08:23:03 2025] sdhci_msm 8844000.sdhci: nvmem cell get failed
[Sat Nov 15 08:23:03 2025] rdbg: failed get smem state
... (truncated)
```

---

## 📋 总结
**结论**: Root cause: Active wakelocks preventing suspend: PowerManagerService.Display, PowerManager.SuspendLockout, a600000.hsusb

---

## 🤖 AI Comprehensive Analysis

**## Suspend Status**  
- **/d/suspend_stats** shows `success: 0` and `fail: 0`.  
- The suspend statistics report **no successful suspend cycles** since boot.  
- The “last_failed_*” fields are empty, indicating the kernel never reached a point where it could record a failure – it simply never entered suspend.  

**Conclusion:** The device is **not entering suspend** at all.

---

**## Wakelock Analysis** (from `dumpsys suspend_control_internal`)

| Wake‑lock name                     | PID  | Type   | Status   | Active count | Total time |
|-----------------------------------|------|--------|----------|--------------|------------|
| **PowerManagerService.Display**   | 1922 | Native | **Active** | 1 | ~941 s |
| **PowerManager.SuspendLockout**   | 1922 | Native | **Active** | 1 | ~941 s |
| PowerManagerService.Booting      | 1922 | Native | Inactive | 0 | 52 s |
| radio‑interface                  | 1263 | Native | Inactive | 0 | 0.2 s |
| … *(all other native wake‑locks are inactive)* | | | | | |

**Kernel‑side wake‑locks (excerpt)**  
- `eventpoll` (many instances) – all inactive.  
- `usb`, `wifi`, `wlan`, `st21nfc` – inactive at the moment of the dump.  
- No kernel “active” wake‑locks besides the generic `eventpoll` counters.

**Key observation:** The **only active wake‑locks are the high‑level PowerManager ones** – the display and the suspend‑lockout. No other user‑space or kernel wakelocks are holding the device awake.

---

**## Root Cause (why suspend never succeeds)**  

1. **Display wake‑lock still held**  
   - `PowerManagerService.Display` is active for almost the entire uptime (≈ 941 s).  
   - This indicates the system believes the screen is on (or a display‑related WAKE‑LOCK has never been released). As long as the display wake‑lock is held, the kernel will not attempt suspend.

2. **Suspend‑Lockout active**  
   - `PowerManager.SuspendLockout` is also active for the same duration.  
   - The lockout is typically set by the framework when a subsystem reports it cannot safely suspend (e.g., pending I/O, driver not ready, or a “no‑sleep” flag).

3. **Driver / firmware initialization problems that trigger the lockout**  
   - **SDIO / Wi‑Fi driver**: Repeated log lines like  
     ```
     sdhci_msm 8844000.sdhci: nvmem cell get failed
     sdhci_msm 8844000.sdhci: SDIO dependent driver probe not complete
     ```  
     show the SDIO‑based Wi‑Fi (and possibly other peripherals) never finish probing.  
     An unfinished SDIO driver registers a **suspend lockout** to prevent the system from sleeping while the hardware is not ready.

   - **Missing firmware**:  
     - `regulatory.db` cannot be loaded (`Failed to load regulatory.db`).  
     - Numerous ADSP/CDSP/modem firmware files (`adsp.mdt`, `cdsp.mdt`, `modem.mdt`, etc.) fall back to “sysfs fallback” and ultimately fail.  
     - The modem and DSP subsystems stay in a “not‑ready” state, which also contributes to the suspend lockout.

   - **USB gadget / UDC errors**: “couldn't find an available UDC or it's busy” repeatedly appears, indicating the USB peripheral controller never fully initializes, another condition that can block suspend.

   - **Repeated “Failed to get ddr_device_type”** and other sensor‑related errors suggest additional hardware components are stuck in an error state.

4. **Resulting behaviour**  
   - Because the display wake‑lock never clears and the framework‑level suspend‑lockout stays asserted (driven by the unfinished SDIO/Wi‑Fi and modem/DSP subsystems), the kernel never reaches the suspend path, so `suspend_stats` never records a successful or failed suspend attempt.

---

**## Recommendations (what to fix to enable suspend)**  

| Area | Action |
|------|--------|
| **Display wake‑lock** | Verify the UI actually turns the screen off. Check for any app‑level wake‑lock (`android.os.PowerManager.WakeLock`) that might be held indefinitely (e.g., a debug‑screen‑on flag, a stuck `android.hardware.display` service). Use `adb shell dumpsys power` to list active display wake‑locks and release them. |
| **Suspend‑Lockout source** | Identify the component that called `PowerManagerService.acquireSuspendLock`. The log shows the lockout is likely set by the SDIO/Wi‑Fi driver (`sdhci_msm` errors). Fix the driver initialization so it can complete and release the lock. |
| **SDIO / Wi‑Fi driver** | - Ensure the required NVMEM cells are present in the device tree (the “nvmem cell get failed” messages indicate missing entries). <br> - Load the correct Wi‑Fi firmware (`regulatory.db`, `modem.mdt`, etc.) into `/vendor/firmware` or the appropriate partition. <br> - Verify the SDIO device tree node (`sdhci_msm`) has a valid `vdd` regulator and `reset` line. |
| **Modem / DSP firmware** | Provide the missing firmware files (`adsp.mdt`, `cdsp.mdt`, `modem.mdt`, `ipa_fws.mdt`, etc.) in the expected locations (`/vendor/firmware_mnt/image/`). Re‑flash the device with a complete firmware package or update the OTA that includes these blobs. |
| **USB gadget / UDC** | The kernel logs “couldn't find an available UDC or it's busy”. Ensure the USB controller driver (`dwc3`) is correctly bound and that a UDC (e.g., `gadgetfs` or `configfs` gadget) is available, or disable the gadget if not needed. |
| **Kernel configuration** | If the device tree is missing entries for the regulators or clocks (`vdd`, `core_reset`, `tcxo`), add them. The logs also show “TCXO clk not present (-2)”. Supplying the correct clock definitions can allow the SDHCI controller to initialize. |
| **System updates** | Apply any vendor‑provided OTA that fixes the missing NVMEM cells and includes the proper firmware packages. Often these issues are resolved by an updated `system.img`/`vendor.img`. |
| **Testing after fixes** | After applying the above changes, reboot and run: <br> `adb shell dumpsys power` → confirm `Display` and `SuspendLockout` are **inactive**. <br> `adb shell dumpsys suspend_control_internal` → verify no active wake‑locks. <br> `adb shell cat /d/suspend_stats` → should now show `success: N` with a non‑zero count. |

By addressing the **display wake‑lock**, ensuring **SDIO/Wi‑Fi and modem/DSP firmware** are correctly loaded, and fixing the **device‑tree NVMEM/clock/regulator definitions**, the system will be able to clear the suspend‑lockout and allow the kernel to enter suspend normally.

---

## 📁 Evidence Files

- **suspend_stats.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case1\suspend_stats.txt`
- **dumpsys_suspend.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case1\dumpsys_suspend.txt`
- **dmesg.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case1\dmesg.txt`

---

## ✅ Verification Checklist

After fixing the identified issue:

1. **Re-run diagnosis**: Collect new evidence and verify the issue is resolved
2. **Check suspend_stats**: Verify success count increases and fail count remains 0
3. **Check wakelocks**: Ensure no active wakelocks in dumpsys output
4. **Measure power**: Compare power consumption before/after fix (expect ≥3% reduction)
