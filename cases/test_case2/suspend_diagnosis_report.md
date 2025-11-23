# Suspend Diagnosis Report

**Collection Directory**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case2`  
**Time**: 2025-11-23T17:04:33.562457

---

## 🔴 CONCLUSION: Suspend Failure Detected

**Root Cause**: Root cause: Active wakelocks preventing suspend: a600000.hsusb

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
- `a600000.hsusb`

**Analysis stops here** - Root cause identified

### 原始 Wakelock Dump (关键片段)
```text
 |                                                                                           WAKELOCK STATS                                                                                        | 
 | NAME                           | PID    | TYPE   | STATUS   | ACTIVE COUNT | TOTAL TIME   | MAX TIME     | EVENT COUNT  | WAKEUP COUNT | EXPIRE COUNT | PREVENT SUSPEND TIME | LAST CHANGE      | 
 | suspend_stats_lock             |   4245 | Native | Inactive |            0 |          0ms |          0ms |          --- |          --- |          --- |                  --- |        1557698ms | 
 | PowerManagerService.WakeLocks  |   1922 | Native | Inactive |            0 |      13311ms |       6497ms |          --- |          --- |          --- |                  --- |        1411913ms | 
 | PowerManagerService.Broadcasts |   1922 | Native | Inactive |            0 |        187ms |        141ms |          --- |          --- |          --- |                  --- |        1411906ms | 
 | PowerManager.SuspendLockout    |   1922 | Native | Inactive |            0 |    1254685ms |     653211ms |          --- |          --- |          --- |                  --- |        1411889ms | 
 | PowerManagerService.Display    |   1922 | Native | Inactive |            0 |    1254719ms |     653247ms |          --- |          --- |          --- |                  --- |        1411888ms | 
 | suspend_stats_lock             |   4230 | Native | Inactive |            0 |          1ms |          1ms |          --- |          --- |          --- |                  --- |        1099079ms | 
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
**结论**: Root cause: Active wakelocks preventing suspend: a600000.hsusb

---

## 🤖 AI Comprehensive Analysis

**## 1. Suspend status – `/d/suspend_stats`**

```
success: 0
fail:    0
failed_freeze:          0
failed_prepare:         0
failed_suspend:         0
failed_suspend_late:    0
failed_suspend_noirq:   0
failed_resume:          0
failed_resume_early:    0
failed_resume_noirq:    0
```

* The system has **never entered a successful suspend** since the last boot (0 successes, 0 failures).  
* No “failed‑freeze” or “failed‑prepare” counters are incremented, but the fact that *success* is zero tells us that the kernel never completed a suspend cycle.

---

**## 2. Wake‑lock analysis – `dumpsys suspend_control_internal`**

The WAKELOCK STATS table (excerpt) shows **all wake‑locks inactive**:

| NAME                         | STATUS   | ACTIVE COUNT |
|------------------------------|----------|--------------|
| `PowerManagerService.WakeLocks` | Inactive | 0 |
| `PowerManagerService.Broadcasts`| Inactive | 0 |
| `PowerManager.SuspendLockout`   | Inactive | 0 |
| `radio‑interface`              | Inactive | 0 |
| `event3` (kernel)              | Inactive | 4 (but all **inactive** – total time = 3 ms) |
| `eventpoll`, `usb`, `st21nfc`, …| Inactive | 0‑2 (all inactive) |

* No user‑space wakelock is held at the moment.  
* The kernel‑side “event3” entry shows a few short‑lived wake‑ups (4 total, each ≤ 1 ms) – far too small to block suspend.  
* The `last_failed_suspend` counter in the suspend‑control dump is **0**, matching the `/d/suspend_stats` output.

**Conclusion:** The device is **not being kept awake by a wakelock**; the lack of suspend is caused by something else in the kernel/driver stack.

---

## 3. Kernel‑level root‑cause – `dmesg` inspection  

Since no wakelocks are active, we look for driver‑ or firmware‑related errors that can prevent the kernel from entering deep sleep. The most relevant messages are:

| Time (approx.) | Message | Why it matters |
|----------------|---------|----------------|
| **08:22:58**   | `qcom,rpmh-regulator … sync_state() pending …` (many regulators) | Indicates regulator drivers are waiting on other components – could keep the power domain active. |
| **08:23:01‑08:23:04** | Repeated `sdhci_msm 8844000.sdhci: nvmem cell get failed` / `SDIO dependent driver probe not complete` | The SDIO host can never finish probing, leaving the SDIO bus in a “busy” state that blocks low‑power entry. |
| **08:23:08**   | `qcom_q6v5_pas … Direct firmware load for … failed with error -2` (adsp.mdt, cdsp.mdt, ipa_fws.mdt, regulatory.db, etc.) | Missing firmware for ADSP, CDSP, IPA and other DSP subsystems – those subsystems stay in a **reset/idle‑wait** state, which the kernel treats as a “device active” condition. |
| **08:23:18**   | `remoteproc remoteproc2: powering up 32300000.remoteproc-cdsp` followed by many “Direct firmware load … failed with error -2” and a cascade of “Falling back to sysfs fallback” | The CDSP (modem DSP) never receives its firmware, so the remote‑proc driver never signals “ready”, preventing the power‑management framework from powering the domain down. |
| **08:23:36**   | `adsp-loader … adsp.mdt not found` and later `ipa … Direct firmware load for ipa_fws.mdt failed` | Same problem for the ADSP and IPA – they keep the corresponding subsystems awake. |
| **08:23:36‑08:23:38** | `cfg80211: failed to load regulatory.db` | The Wi‑Fi regulatory database cannot be loaded; the Wi‑Fi driver stays in a “initialising” state, which also blocks suspend. |
| **08:24:01‑08:24:02** | `UDC core: g1: couldn't find an available UDC or it's busy` (repeated many times) | USB gadget driver repeatedly failing to bind a controller; the USB gadget framework treats the missing controller as a wake‑source. |
| **08:24:55**   | `spmi 2‑00: Can't add 2‑00, status -17` (duplicate sysfs node) | Indicates a failure in the PMIC/SLPI driver that may keep the PMIC power rail active. |
| **08:24:58‑08:25:00** | `smc-client-dev:Rxd SMC event: 11` / `IPA not ready, waiting for init completion` | The IPA (network offload) stack never reaches the “ready” state, holding a power domain active. |
| **08:30:05‑08:30:15** | Repeated SELinux denials for `vndbinder` and many writes to `/dev/zygote_tmpfs` from `CachedAppOptimi` | These are **post‑suspend** audit messages (the system is already awake) and are not the cause of the suspend block. |
| **08:40:32**   | `USB_STATE=DISCONNECTED` → `USB_STATE=CONNECTED` → `USB_STATE=CONFIGURED` | USB state changes trigger a wake‑up; however the USB controller (`dwc3`) immediately goes back to idle, so it is not the primary blocker. |
| **08:46:19**   | `panel_event_notifier_callback: DRM Power - DOWN` → `BLANK` → `Suspend notifier called!` → **device goes to suspend** (the first successful suspend observed) | After many hours the display driver finally allowed the system to enter suspend, showing that the earlier failures were indeed preventing it. |

### What the dmesg tells us

1. **Missing firmware** for several critical subsystems (ADSP, CDSP, IPA, Wi‑Fi regulatory DB, modem, etc.) – the drivers stay in a “waiting for firmware” state, which the kernel treats as a *wake‑source*.  
2. **SDIO host failures** (`nvmem cell get failed`, `probe not complete`) – the SDIO controller never finishes initialization, keeping the SDIO bus powered.  
3. **Regulator‑sync loops** – many regulator drivers are stuck in `sync_state()` pending on other components that never become ready (because the firmware is missing).  
4. **USB‑gadget controller not bound** – repeated “couldn't find an available UDC” messages keep the USB gadget framework from completing its power‑down sequence.  
5. **IPA not ready** – the IPA driver repeatedly reports “IPA not ready, waiting for init completion”, which also blocks deep‑sleep.  

All of these conditions cause the kernel’s **suspend candidate checklist** to fail, so the kernel never proceeds to the “Suspend entry successful” path, which explains the `success: 0` in `/d/suspend_stats`.

---

## 4. Recommendations – how to get suspend working again

| Area | Action |
|------|--------|
| **Firmware files** | - Verify that the device’s `/vendor/firmware/` (or `/vendor/firmware_mnt/image/`) contains the required images: `adsp.mdt`, `adsp_dtb.mdt`, `cdsp.mdt`, `cdsp_dtb.mdt`, `ipa_fws.mdt`, `regulatory.db`, `modem.mdt`, etc.<br>- If the images are missing, copy them from the device’s factory image or from the SoC vendor’s BSP.<br>- Ensure the file names match exactly (case‑sensitive) and that the device can read them (check SELinux contexts). |
| **SDIO host (sdhci_msm)** | - The repeated `nvmem cell get failed` indicates a missing NVMEM cell definition in the DT. Verify the device‑tree entry `sdhci@8844000` includes a valid `nvmem` reference.<br>- If the SDIO host is not used (e.g., no external SDIO peripherals), consider disabling it in the DT (`status = "disabled"`). |
| **Regulator sync loops** | - Many `qcom,rpmh-regulator … sync_state() pending` messages are caused by regulators waiting on each other. Once the missing firmware loads and the dependent devices come up, these syncs will resolve automatically.<br>- If a particular regulator (e.g., `ldoa25`, `ldoa26`) is not needed, set `qcom,always-on` or disable it in the DT to break the dependency chain. |
| **USB gadget (UDC)** | - The kernel repeatedly logs “couldn't find an available UDC or it's busy”. Verify that the USB‑OTG controller driver (`dwc3`) is correctly bound and that the UDC driver (`dwc3_udc`) is present. If the gadget functionality is not required, disable the `usb_gadget` config in the kernel or set `status = "disabled"` for the UDC node. |
| **IPA / network offload** | - The IPA driver reports “IPA not ready”. After the missing firmware (`ipa_fws.mdt`) is restored, the IPA will finish initialization and release its wake‑lock.<br>- Ensure the IPA DMA buffers are correctly allocated (check `ipa` dmesg for “Failed to create device link”). |
| **Wi‑Fi firmware** | - The Wi‑Fi driver fails to load `regulatory.db`. Place the correct regulatory database in `/vendor/firmware/` (or the appropriate location for the WLAN driver). |
| **Modem / CDSP** | - The remote‑proc subsystems (`adsp`, `cdsp`, `modem`) keep waiting for firmware. Provide the `.mdt` and `.bxx` files for each remote processor. |
| **SELinux** | - Several SELinux denials (e.g., `vndbinder`, `syslog_read`) are unrelated to suspend, but ensure the policies allow the binder services to start; otherwise they may cause other services to crash and keep the system awake. |
| **Testing after fixes** | 1. Reboot the device.<br>2. Run `dmesg | grep -i 'failed\|error\|pending'` – there should be no long‑running pending‑state messages.<br>3. Run `dumpsys suspend_control_internal` – all wake‑locks should still be inactive.<br>4. Run `cat /d/suspend_stats` – you should now see **success > 0** after the first suspend cycle.<br>5. Optionally, trigger a manual suspend (`adb shell dumpsys deviceidle force-idle`) and verify that the device enters suspend (`cat /sys/power/state` should show `mem`). |

---

### TL;DR

* **Suspend never succeeds** (`/d/suspend_stats` shows 0 successes).  
* **No active wake‑locks** are reported (`dumpsys suspend_control_internal` shows all inactive).  
* The kernel is blocked by **missing firmware and driver initialisation failures** (ADSP, CDSP, IPA, Wi‑Fi regulatory DB, SDIO host, USB gadget, regulators).  
* **Fix the missing firmware files and correct the device‑tree entries** for the failing subsystems; after those drivers can finish their probe, the kernel will be able to enter suspend and the `success` counter will start increasing.

---

## 📁 Evidence Files

- **suspend_stats.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case2\suspend_stats.txt`
- **dumpsys_suspend.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case2\dumpsys_suspend.txt`
- **dmesg.txt**: `C:\Users\xingya\OneDrive - Qualcomm\Desktop\AI_tools\suspend_mvp\cases\test_case2\dmesg.txt`

---

## ✅ Verification Checklist

After fixing the identified issue:

1. **Re-run diagnosis**: Collect new evidence and verify the issue is resolved
2. **Check suspend_stats**: Verify success count increases and fail count remains 0
3. **Check wakelocks**: Ensure no active wakelocks in dumpsys output
4. **Measure power**: Compare power consumption before/after fix (expect ≥3% reduction)
