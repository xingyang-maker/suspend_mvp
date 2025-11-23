@echo off
setlocal enabledelayedexpansion

REM Android Wakeup 日志收集脚本 (Windows版本)
REM 使用方法: collect_wakeup_logs.bat [输出目录]

echo 🔍 Android Wakeup 日志收集工具
echo.

REM 设置默认输出目录
if "%1"=="" (
    set "OUTPUT_DIR=collected_wakeup_logs"
) else (
    set "OUTPUT_DIR=%1"
)

echo 输出目录: %OUTPUT_DIR%
echo.

REM 创建输出目录
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM 检查ADB是否可用
echo 📱 检查ADB和设备连接...
adb version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: ADB未找到或未安装
    echo 请确保ADB已安装并添加到PATH环境变量中
    pause
    exit /b 1
)

REM 检查设备连接
adb devices | findstr "device" >nul
if errorlevel 1 (
    echo ❌ 错误: 未找到连接的Android设备
    echo 请确保:
    echo   1. 设备已通过USB连接
    echo   2. 已开启USB调试
    echo   3. 已授权调试连接
    echo.
    adb devices
    pause
    exit /b 1
)

REM 获取设备信息
for /f "tokens=*" %%i in ('adb shell getprop ro.product.model 2^>nul') do set "DEVICE_MODEL=%%i"
if "!DEVICE_MODEL!"=="" set "DEVICE_MODEL=Unknown"
echo ✅ 设备已连接: !DEVICE_MODEL!
echo.

REM 收集设备信息
echo 📋 收集设备信息...
(
    echo Collection Time: %date% %time%
    echo Collection Type: Wakeup Analysis
    for /f "tokens=*" %%i in ('adb shell getprop ro.product.model 2^>nul') do echo Device Model: %%i
    for /f "tokens=*" %%i in ('adb shell getprop ro.build.version.release 2^>nul') do echo Android Version: %%i
    for /f "tokens=*" %%i in ('adb shell uname -r 2^>nul') do echo Kernel Version: %%i
    for /f "tokens=*" %%i in ('adb shell dumpsys battery 2^>nul ^| findstr level') do echo Battery Level: %%i
    for /f "tokens=*" %%i in ('adb shell whoami 2^>nul') do echo ADB User: %%i
) > "%OUTPUT_DIR%\collection_info.txt"

REM 1. 收集 wakeup_sources
echo 🌟 收集 wakeup sources 信息...
adb shell "cat /sys/kernel/debug/wakeup_sources" > "%OUTPUT_DIR%\wakeup_sources.txt" 2>nul
if errorlevel 1 (
    echo ⚠️  无法读取 /sys/kernel/debug/wakeup_sources，尝试替代路径...
    adb shell "cat /d/wakeup_sources" > "%OUTPUT_DIR%\wakeup_sources.txt" 2>nul
    if errorlevel 1 (
        echo ❌ 无法访问 wakeup_sources，可能需要root权限
        type nul > "%OUTPUT_DIR%\wakeup_sources.txt"
    )
)

REM 检查文件内容
for %%F in ("%OUTPUT_DIR%\wakeup_sources.txt") do (
    if %%~zF gtr 0 (
        for /f %%A in ('type "%OUTPUT_DIR%\wakeup_sources.txt" ^| find /c /v ""') do echo ✅ wakeup_sources.txt 收集成功 ^(%%A 行^)
    ) else (
        echo ⚠️  wakeup_sources.txt 为空
    )
)

REM 2. 收集 dumpsys power
echo 🔋 收集电源管理信息...
adb shell dumpsys power > "%OUTPUT_DIR%\dumpsys_power.txt" 2>nul
if not errorlevel 1 (
    for %%F in ("%OUTPUT_DIR%\dumpsys_power.txt") do (
        if %%~zF gtr 0 (
            for /f %%A in ('type "%OUTPUT_DIR%\dumpsys_power.txt" ^| find /c /v ""') do echo ✅ dumpsys_power.txt 收集成功 ^(%%A 行^)
        ) else (
            echo ⚠️  dumpsys_power.txt 为空
        )
    )
) else (
    echo ❌ 无法执行 dumpsys power
    type nul > "%OUTPUT_DIR%\dumpsys_power.txt"
)

REM 3. 收集 dmesg (重点关注wakeup相关)
echo 🖥️  收集内核日志...
adb shell "dmesg -T" > "%OUTPUT_DIR%\dmesg.txt" 2>nul
if not errorlevel 1 (
    for %%F in ("%OUTPUT_DIR%\dmesg.txt") do (
        if %%~zF gtr 0 (
            for /f %%A in ('type "%OUTPUT_DIR%\dmesg.txt" ^| find /c /v ""') do echo ✅ dmesg.txt 收集成功 ^(%%A 行^)
        ) else (
            echo ⚠️  dmesg -T 输出为空，尝试不带时间戳...
            adb shell dmesg > "%OUTPUT_DIR%\dmesg.txt" 2>nul
        )
    )
) else (
    echo ⚠️  dmesg -T 失败，尝试标准dmesg...
    adb shell dmesg > "%OUTPUT_DIR%\dmesg.txt" 2>nul
    if errorlevel 1 (
        echo ❌ 无法获取dmesg
        type nul > "%OUTPUT_DIR%\dmesg.txt"
    )
)

REM 4. 收集 logcat (应用层wakeup事件)
echo 📱 收集应用层日志...
echo 正在收集最近的logcat日志 (10秒)...
timeout /t 1 >nul
adb logcat -d -v time > "%OUTPUT_DIR%\logcat.txt" 2>nul
if not errorlevel 1 (
    for %%F in ("%OUTPUT_DIR%\logcat.txt") do (
        if %%~zF gtr 0 (
            for /f %%A in ('type "%OUTPUT_DIR%\logcat.txt" ^| find /c /v ""') do echo ✅ logcat.txt 收集成功 ^(%%A 行^)
        ) else (
            echo ⚠️  logcat.txt 为空
        )
    )
) else (
    echo ❌ 无法获取logcat
    type nul > "%OUTPUT_DIR%\logcat.txt"
)

REM 收集额外的有用信息
echo 📊 收集额外wakeup相关信息...

REM 电源状态
adb shell "cat /sys/power/state" > "%OUTPUT_DIR%\power_state.txt" 2>nul || type nul > "%OUTPUT_DIR%\power_state.txt"

REM 唤醒统计
adb shell "cat /sys/power/wakeup_count" > "%OUTPUT_DIR%\wakeup_count.txt" 2>nul || type nul > "%OUTPUT_DIR%\wakeup_count.txt"

REM 中断统计
adb shell "cat /proc/interrupts" > "%OUTPUT_DIR%\interrupts.txt" 2>nul || type nul > "%OUTPUT_DIR%\interrupts.txt"

REM AlarmManager信息
adb shell dumpsys alarm > "%OUTPUT_DIR%\dumpsys_alarm.txt" 2>nul || type nul > "%OUTPUT_DIR%\dumpsys_alarm.txt"

echo.
echo 📁 收集完成! 文件保存在: %OUTPUT_DIR%
echo.
echo 📋 收集的文件:
dir /b "%OUTPUT_DIR%"

echo.
echo 🔍 文件内容检查:
for %%f in (wakeup_sources.txt dumpsys_power.txt dmesg.txt logcat.txt) do (
    for %%F in ("%OUTPUT_DIR%\%%f") do (
        if %%~zF gtr 0 (
            for /f %%A in ('type "%OUTPUT_DIR%\%%f" ^| find /c /v ""') do echo   ✅ %%f: %%A 行
        ) else (
            echo   ❌ %%f: 空文件
        )
    )
)

echo.
echo 🚀 使用收集的日志进行wakeup分析:
echo   python bin/wakeup_diagnosis --case-dir %OUTPUT_DIR%
echo.
echo 📖 详细的wakeup日志收集指南请参考相关文档
echo.
pause
