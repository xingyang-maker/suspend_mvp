# Android Wakeup 日志收集规范

本文档详细说明如何正确收集Android设备wakeup诊断所需的日志文件。

## 概述

Wakeup诊断工具需要四个关键的日志文件来进行全面的wakeup分析：

1. **wakeup_sources.txt** - Wakeup源统计信息 (来自 `/sys/kernel/debug/wakeup_sources`)
2. **dumpsys_power.txt** - 电源管理状态 (来自 `dumpsys power`)
3. **dmesg.txt** - 内核消息日志 (来自 `dmesg`)
4. **logcat.txt** - 应用层日志 (来自 `logcat`)

## 前置条件

### 设备要求
- Android设备已开启USB调试
- 设备已通过USB连接到电脑
- ADB工具已安装并可用

### 权限要求
- Root权限 (用于访问 `/sys/kernel/debug/wakeup_sources`)
- 或者具有系统级权限的shell访问

### 验证连接
```bash
# 检查设备连接
adb devices

# 检查shell权限
adb shell whoami
```

## 日志收集步骤

### 方法一：使用快速收集脚本 (推荐)

**Windows:**
```cmd
# 使用默认目录 (collected_wakeup_logs)
scripts\wakeup\collect_wakeup_logs.bat

# 指定输出目录
scripts\wakeup\collect_wakeup_logs.bat my_wakeup_logs
```

**Linux/macOS:**
```bash
# 使用默认目录 (collected_wakeup_logs)
./scripts/wakeup/collect_wakeup_logs.sh

# 指定输出目录
./scripts/wakeup/collect_wakeup_logs.sh my_wakeup_logs
```

这些脚本会：
- 自动检查设备连接和ADB可用性
- 收集所有必需的wakeup相关日志文件
- 提供详细的收集状态反馈
- 验证收集的文件质量
- 收集额外的有用信息

### 方法二：使用诊断工具自动收集

```bash
# 自动收集所有必需的日志
python bin/wakeup_diagnosis

# 或指定特定设备
python bin/wakeup_diagnosis --device DEVICE_SERIAL
```

### 方法三：手动收集日志

如果需要手动收集日志，请按以下步骤操作：

#### 1. 收集 Wakeup Sources 信息

```bash
# 方法1: 直接读取 (需要root权限)
adb shell "su -c 'cat /sys/kernel/debug/wakeup_sources'" > wakeup_sources.txt

# 方法2: 如果没有root权限，尝试以下命令
adb shell cat /sys/kernel/debug/wakeup_sources > wakeup_sources.txt

# 方法3: 如果上述都不行，尝试
adb shell "cat /d/wakeup_sources" > wakeup_sources.txt
```

**预期内容示例：**
```
name            active_count    event_count     wakeup_count    active_since    total_time      max_time        last_change     prevent_suspend_time
alarmtimer      0               0               0               0               0               0               12345           0
rtc0            0               15              15              0               0               0               67890           0
gpio-keys       0               25              25              0               0               0               11111           0
```

#### 2. 收集电源管理信息

```bash
# 收集dumpsys power信息
adb shell dumpsys power > dumpsys_power.txt
```

**预期内容示例：**
```
POWER MANAGER (dumpsys power)

Power Manager State:
  mDirty=0x0
  mWakefulness=Awake
  mWakefulnessChanging=false
  mIsPowered=false
  mPlugType=0
  mBatteryLevel=85
  mBatteryLevelWhenDreamStarted=0

Wake Locks: size=2
  PARTIAL_WAKE_LOCK              'AudioOut' ON_AFTER_RELEASE (uid=1041, pid=1234, ws=WorkSource{1041})
  PARTIAL_WAKE_LOCK              'WifiLock' (uid=1000, pid=5678, ws=WorkSource{1000})
```

#### 3. 收集内核日志

```bash
# 方法1: 收集带时间戳的dmesg (推荐)
adb shell "dmesg -T" > dmesg.txt

# 方法2: 如果不支持-T参数
adb shell dmesg > dmesg.txt

# 方法3: 收集最近的内核日志
adb shell "dmesg | tail -n 1000" > dmesg.txt
```

**预期内容示例：**
```
[2023-11-23 17:30:15] PM: suspend exit
[2023-11-23 17:30:15] PM: resume of devices complete after 123.456 msecs
[2023-11-23 17:30:16] input: gpio-keys as /devices/soc/gpio-keys/input/input0
[2023-11-23 17:30:16] IRQ 123: wakeup source
```

#### 4. 收集应用层日志

```bash
# 方法1: 收集最近的logcat日志
adb logcat -d -v time > logcat.txt

# 方法2: 收集特定时间段的日志
adb logcat -d -v time -t '11-23 17:00:00.000' > logcat.txt

# 方法3: 实时收集一段时间的日志
adb logcat -v time > logcat.txt &
# 等待一段时间后停止
```

**预期内容示例：**
```
11-23 17:30:15.123  1234  5678 I AlarmManager: Wakeup alarm triggered for com.example.app
11-23 17:30:15.456  1000  2000 D PowerManager: acquireWakeLock: AudioOut
11-23 17:30:16.789  1041  3000 I JobScheduler: Wakeup job scheduled for uid 1041
```

## 日志质量检查

### 检查文件完整性

收集完成后，请验证每个文件的内容：

```bash
# 检查文件大小 (不应为空)
ls -la wakeup_sources.txt dumpsys_power.txt dmesg.txt logcat.txt

# 检查文件内容
head -10 wakeup_sources.txt
head -10 dumpsys_power.txt  
head -10 dmesg.txt
head -10 logcat.txt
```

### 关键内容验证

#### wakeup_sources.txt 应包含：
- 表头行 (`name active_count event_count wakeup_count...`)
- 各种wakeup源的统计数据
- 如果有活跃的wakeup源，`active_count` 应该大于0

#### dumpsys_power.txt 应包含：
- "POWER MANAGER" 标题
- "Wake Locks:" 部分
- 电源状态信息 (`mWakefulness`, `mBatteryLevel` 等)

#### dmesg.txt 应包含：
- 内核时间戳或序号
- 如果设备有wakeup事件，应包含 "PM: suspend exit", "wakeup", "IRQ" 等相关消息

#### logcat.txt 应包含：
- 时间戳格式的日志条目
- 应用相关的wakeup事件 (`AlarmManager`, `JobScheduler`, `PowerManager` 等)

## 常见问题和解决方案

### 问题1: 权限不足无法访问 wakeup_sources

**症状：** `Permission denied` 错误

**解决方案：**
```bash
# 尝试获取root权限
adb root
adb shell cat /sys/kernel/debug/wakeup_sources > wakeup_sources.txt

# 或者尝试替代路径
adb shell cat /d/wakeup_sources > wakeup_sources.txt
```

### 问题2: dumpsys power 输出为空或不完整

**症状：** 空文件或缺少关键部分

**解决方案：**
```bash
# 检查dumpsys服务是否可用
adb shell dumpsys -l | grep power

# 尝试其他相关的dumpsys服务
adb shell dumpsys battery > battery_info.txt
adb shell dumpsys alarm > alarm_info.txt
```

### 问题3: logcat 权限限制

**症状：** `Permission denied` 或只能看到自己应用的日志

**解决方案：**
```bash
# 尝试获取更高权限
adb root
adb logcat -d -v time > logcat.txt

# 或者收集特定标签的日志
adb logcat -d -v time AlarmManager:* PowerManager:* JobScheduler:* > logcat_filtered.txt
```

### 问题4: wakeup事件太少或没有

**可能原因：**
- 设备处于活跃状态，没有进入suspend
- 收集时间窗口太短
- 设备suspend功能异常

**解决方案：**
1. 手动触发suspend/wakeup循环：
   ```bash
   # 让设备进入suspend
   adb shell input keyevent KEYCODE_POWER
   
   # 等待10-30秒
   sleep 30
   
   # 唤醒设备
   adb shell input keyevent KEYCODE_POWER
   
   # 立即收集日志
   ```

2. 延长收集时间：
   ```bash
   # 实时监控wakeup事件
   adb shell "while true; do echo '=== $(date) ==='; cat /sys/kernel/debug/wakeup_sources | head -5; sleep 10; done" > wakeup_monitor.txt &
   ```

## 最佳实践

### 收集时机
1. **问题复现期间收集** - 在wakeup问题发生时实时收集
2. **对比收集** - 收集正常和异常情况下的日志进行对比
3. **长期监控** - 收集较长时间段的数据以识别模式

### 文件组织
```
wakeup_case_directory/
├── wakeup_sources.txt     # Wakeup源统计
├── dumpsys_power.txt      # 电源管理状态
├── dmesg.txt              # 内核日志
├── logcat.txt             # 应用层日志
├── collection_info.txt    # 收集时间和环境信息
├── interrupts.txt         # 中断统计 (额外)
├── dumpsys_alarm.txt      # 闹钟信息 (额外)
└── wakeup_count.txt       # 唤醒计数 (额外)
```

### 环境信息记录
创建 `collection_info.txt` 记录收集环境：
```bash
echo "Collection Time: $(date)" > collection_info.txt
echo "Collection Type: Wakeup Analysis" >> collection_info.txt
echo "Device Model: $(adb shell getprop ro.product.model)" >> collection_info.txt
echo "Android Version: $(adb shell getprop ro.build.version.release)" >> collection_info.txt
echo "Kernel Version: $(adb shell uname -r)" >> collection_info.txt
echo "Battery Level: $(adb shell dumpsys battery | grep level)" >> collection_info.txt
```

## 使用收集的日志

收集完成后，使用以下命令进行分析：

```bash
# 分析收集的wakeup日志
python bin/wakeup_diagnosis --case-dir /path/to/collected/logs

# 示例
python bin/wakeup_diagnosis --case-dir ./my_wakeup_case_logs
```

## 故障排除检查清单

在提交日志进行分析前，请确认：

- [ ] 所有四个核心文件都已收集 (wakeup_sources.txt, dumpsys_power.txt, dmesg.txt, logcat.txt)
- [ ] 文件不为空且包含预期的内容格式
- [ ] 日志收集时间覆盖了wakeup问题发生的时间窗口
- [ ] 设备信息和收集环境已记录
- [ ] 如果可能，已收集问题复现前后的对比日志
- [ ] wakeup_sources.txt 包含有意义的统计数据
- [ ] dumpsys_power.txt 包含wake lock信息

遵循此规范可以确保收集到高质量的wakeup相关日志，提高wakeup问题诊断的准确性和效率。

## 高级收集技巧

### 实时监控wakeup事件
```bash
# 监控wakeup源变化
adb shell "watch -n 5 'cat /sys/kernel/debug/wakeup_sources | head -10'"

# 监控电源状态变化
adb shell "watch -n 2 'dumpsys power | grep -A 5 \"Power Manager State\"'"
```

### 过滤关键日志
```bash
# 只收集wakeup相关的dmesg
adb shell "dmesg | grep -i 'wakeup\|suspend\|resume\|irq'" > dmesg_wakeup.txt

# 只收集电源相关的logcat
adb logcat -d -v time | grep -i 'power\|wakeup\|alarm\|job' > logcat_power.txt
```

### 自动化收集脚本
可以创建自定义脚本来定期收集wakeup数据，用于长期监控和趋势分析。
