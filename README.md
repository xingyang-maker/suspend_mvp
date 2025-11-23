# Android Power Management Diagnosis Platform

A comprehensive platform for diagnosing various Android device power management issues.

## Overview

This platform provides specialized tools for diagnosing different types of Android power management problems:

1. **Suspend Issues** - Problems with device entering deep sleep mode
2. **Wakeup Issues** - Problems with excessive or inappropriate device wakeups
3. **Extensible Architecture** - Easy to add new diagnosis modules

## 🔧 Available Tools

### 1. Suspend Diagnosis (`bin/suspend_diagnosis`)
Diagnoses Android device suspend failures using a systematic 3-step analysis:
- **Step 1**: Check suspend statistics (`/d/suspend_stats`)
- **Step 2**: Analyze wakelocks (`dumpsys suspend_control_internal`)
- **Step 3**: Examine kernel messages (`dmesg`)

### 2. Wakeup Diagnosis (`bin/wakeup_diagnosis`)
Analyzes Android device wakeup patterns to identify issues:
- **Wakeup Sources**: Analyze `/sys/kernel/debug/wakeup_sources`
- **Wakeup Events**: Examine kernel wakeup messages in dmesg
- **Power Management**: Check dumpsys power for wake locks
- **App Wakeups**: Analyze logcat for application-related wakeups

## 🚀 Quick Start

### Suspend Issues
```bash
# Collect and analyze suspend logs
python bin/suspend_diagnosis

# Analyze existing logs
python bin/suspend_diagnosis --case-dir ./cases/suspend/case1

# Quick log collection
scripts/suspend/collect_suspend_logs.bat  # Windows
scripts/suspend/collect_suspend_logs.sh   # Linux/macOS
```

### Wakeup Issues
```bash
# Collect and analyze wakeup logs
python bin/wakeup_diagnosis

# Analyze existing logs
python bin/wakeup_diagnosis --case-dir ./cases/wakeup/case1

# Quick log collection
scripts/wakeup/collect_wakeup_logs.bat    # Windows
scripts/wakeup/collect_wakeup_logs.sh     # Linux/macOS
```

## 📁 Project Structure

```
android_power_diagnosis/
├── bin/                           # Executable tools
│   ├── suspend_diagnosis          # Suspend failure diagnosis
│   └── wakeup_diagnosis          # Wakeup issue diagnosis
├── src/                          # Source code
│   ├── common/                   # Shared utilities
│   │   ├── collector.py          # Log collection
│   │   ├── ai.py                # AI analysis
│   │   ├── types.py             # Data models
│   │   └── report/              # Report generation
│   │       ├── markdown_builder.py
│   │       └── html_renderer.py
│   ├── suspend_diagnosis/        # Suspend-specific modules
│   │   ├── suspend_main.py
│   │   ├── suspend_cli.py
│   │   └── suspend_analyzer.py
│   └── wakeup_diagnosis/         # Wakeup-specific modules
│       ├── wakeup_main.py
│       ├── wakeup_cli.py
│       └── wakeup_analyzer.py
├── cases/                        # Test cases and examples
│   ├── suspend/                  # Suspend failure cases
│   │   ├── test_case1/
│   │   ├── test_case2/
│   │   └── blocked_bywakelock/
│   └── wakeup/                   # Wakeup issue cases
├── scripts/                      # Collection scripts
│   ├── suspend/                  # Suspend log collection
│   │   ├── collect_suspend_logs.bat
│   │   └── collect_suspend_logs.sh
│   └── wakeup/                   # Wakeup log collection
│       ├── collect_wakeup_logs.bat
│       └── collect_wakeup_logs.sh
├── docs/                         # Documentation
│   ├── suspend_collection_guide.md
│   └── wakeup_collection_guide.md
└── reports/                      # Generated reports
    ├── suspend/
    └── wakeup/
```

## 📋 Documentation

- **[Suspend Collection Guide](docs/suspend_collection_guide.md)** - How to collect logs for suspend analysis
- **[Wakeup Collection Guide](docs/wakeup_collection_guide.md)** - How to collect logs for wakeup analysis

## 🔍 Features

### Common Features
- **Multiple input methods**: Analyze existing logs or collect fresh ones
- **Cross-platform**: Works on Windows, Linux, and macOS
- **AI-powered analysis**: Optional AI insights using QGenie
- **Multiple output formats**: Markdown and HTML reports
- **Flexible log handling**: Works with partial log sets

### Suspend Diagnosis Features
- **3-step systematic analysis**: Follows Android power debugging best practices
- **Wakelock detection**: Identifies blocking wakelocks
- **Kernel failure analysis**: Examines suspend entry failures
- **Success/failure statistics**: Tracks suspend performance over time

### Wakeup Diagnosis Features
- **Wakeup source analysis**: Identifies excessive wakeup sources
- **Timing pattern analysis**: Detects frequent or irregular wakeups
- **App wakeup tracking**: Monitors application-caused wakeups
- **Power correlation**: Links wakeups to power consumption

## 🛠️ Requirements

- Python 3.9+
- Android Debug Bridge (ADB)
- Connected Android device with USB debugging enabled
- Python packages:
  - matplotlib
  - markdown
  - qgenie (optional, for AI analysis)

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/xingyang-maker/suspend_mvp.git
   cd suspend_mvp
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python bin/suspend_diagnosis --help
   python bin/wakeup_diagnosis --help
   ```

## 🎯 Usage Examples

### Suspend Analysis Workflow
```bash
# 1. Collect logs
scripts/suspend/collect_suspend_logs.bat my_suspend_case

# 2. Analyze
python bin/suspend_diagnosis --case-dir my_suspend_case

# 3. View reports
# - my_suspend_case/suspend_diagnosis_report.md
# - my_suspend_case/suspend_diagnosis_report.html
```

### Wakeup Analysis Workflow
```bash
# 1. Collect logs
scripts/wakeup/collect_wakeup_logs.bat my_wakeup_case

# 2. Analyze
python bin/wakeup_diagnosis --case-dir my_wakeup_case

# 3. View reports
# - my_wakeup_case/wakeup_diagnosis_report.md
# - my_wakeup_case/wakeup_diagnosis_report.html
```

## 🔧 Adding New Diagnosis Modules

The platform is designed to be extensible. To add a new diagnosis type:

1. **Create module directory**: `src/new_diagnosis/`
2. **Implement core files**:
   - `new_main.py` - Main logic
   - `new_cli.py` - Command line interface
   - `new_analyzer.py` - Analysis logic
3. **Create bin file**: `bin/new_diagnosis`
4. **Add collection scripts**: `scripts/new/`
5. **Create documentation**: `docs/new_collection_guide.md`
6. **Add test cases**: `cases/new/`

## 📊 Report Structure

All tools generate comprehensive reports including:

1. **Executive Summary** - High-level findings and conclusions
2. **Detailed Analysis** - Step-by-step analysis results
3. **Evidence Files** - List of analyzed log files
4. **AI Insights** - AI-powered analysis and recommendations (optional)
5. **Verification Checklist** - Steps to verify fixes
6. **Raw Log Excerpts** - Relevant portions of original logs

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- New diagnosis modules (battery drain, thermal issues, etc.)
- Enhanced analysis algorithms
- Better visualization and reporting
- Cross-platform improvements
- Documentation and examples

## 📄 License

[MIT License](LICENSE)

## 🆘 Support

For issues and questions:
1. Check the relevant collection guide in `docs/`
2. Review existing test cases in `cases/`
3. Submit issues with log samples and device information
