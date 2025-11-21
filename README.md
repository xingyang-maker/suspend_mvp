# Android Suspend Diagnosis Tool

A command-line tool for diagnosing Android device suspend issues by collecting and analyzing logs.

## Overview

This tool helps diagnose Android suspend-related issues by:

1. Collecting relevant logs from an Android device using ADB
2. Analyzing logs to detect suspend failures
3. Identifying top wakeup sources that may be preventing suspend
4. Generating comprehensive reports in both Markdown and HTML formats
5. Providing AI-powered analysis of the collected logs (optional)

## Features

- Collects multiple log files (logcat, dmesg, dumpsys, wakeup sources)
- Detects suspend failures based on known patterns
- Identifies and ranks top wakeup sources
- Generates visual charts of wakeup source activity
- Provides AI-powered analysis and recommendations (requires QGenie)
- Outputs both Markdown and HTML reports

## Requirements

- Python 3.9+
- Android Debug Bridge (ADB)
- Connected Android device with USB debugging enabled
- Python packages:
  - matplotlib
  - markdown
  - qgenie (optional, for AI analysis)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/android-suspend-diagnosis.git
   cd android-suspend-diagnosis
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage:

```bash
python main.py
```

This will collect logs from the default connected device and generate a report in the `./reports` directory.

### Command-line Options

```
usage: main.py [-h] [--adb ADB] [--device DEVICE] [--out OUT] [--ai-endpoint AI_ENDPOINT] [--collect-ftrace]

Android Suspend Diagnosis Tool

options:
  -h, --help            show this help message and exit
  --adb ADB             Path to ADB executable (default: 'adb')
  --device DEVICE       Target device serial number (empty for default device)
  --out OUT             Output directory for reports (default: './reports')
  --ai-endpoint AI_ENDPOINT
                        QGenie LLM endpoint URL (empty to use default configuration)
  --collect-ftrace      Collect ftrace data from /sys/kernel/tracing/trace
```

### Examples

Collect logs from a specific device:
```bash
python main.py --device DEVICE_SERIAL_NUMBER
```

Specify a custom output directory:
```bash
python main.py --out /path/to/output/directory
```

Collect additional ftrace data:
```bash
python main.py --collect-ftrace
```

## Report Structure

The generated reports include:

1. **Conclusion** - Whether a suspend failure was detected
2. **Rule-based Criteria** - Specific reasons for the failure determination
3. **Potential Blocking Wakeup Sources** - Top wakeup sources that may be preventing suspend
4. **Evidence Files** - List of collected log files
5. **AI Analysis** (if available) - AI-powered analysis and recommendations
6. **Verification Checklist** - Steps to verify that the issue has been resolved

## Project Structure

```
.
├── main.py                 # Main entry point
├── cli.py                  # Command-line interface definition
├── core/                   # Core functionality
│   ├── collector.py        # Log collection from Android devices
│   ├── analyzer.py         # Log analysis and suspend failure detection
│   ├── ai.py               # AI-powered analysis using QGenie
│   ├── utils.py            # Utility functions
│   └── report/             # Report generation
│       ├── markdown_builder.py  # Markdown report generation
│       └── html_renderer.py     # HTML report generation with charts
├── models/                 # Data models
│   └── types.py            # Type definitions
└── reports/                # Generated reports (default location)
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
