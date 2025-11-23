#!/usr/bin/env python3
"""
Wakeup Diagnosis CLI Module

Command-line interface for the Android wakeup diagnosis tool.
"""
import argparse


def parse_args():
    """
    Parse command-line arguments for wakeup diagnosis.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Android Wakeup Diagnosis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect logs from default device and analyze wakeup patterns
  python bin/wakeup_diagnosis

  # Analyze existing logs
  python bin/wakeup_diagnosis --case-dir ./cases/wakeup/case1

  # Collect from specific device
  python bin/wakeup_diagnosis --device DEVICE_SERIAL

  # Specify output directory
  python bin/wakeup_diagnosis --out ./my_wakeup_reports
        """
    )
    
    parser.add_argument(
        "--adb",
        default="adb",
        help="Path to ADB executable (default: 'adb')"
    )
    
    parser.add_argument(
        "--device",
        help="Target device serial number (empty for default device)"
    )
    
    parser.add_argument(
        "--out",
        default="./reports/wakeup",
        help="Output directory for reports (default: './reports/wakeup')"
    )
    
    parser.add_argument(
        "--case-dir",
        help="""Path to a directory containing pre-collected log files for wakeup analysis.
        Expected files: dmesg.txt, wakeup_sources.txt, dumpsys_power.txt, logcat.txt.
        Files can be partial - the tool will analyze whatever logs are available."""
    )
    
    parser.add_argument(
        "--enable-ai",
        action="store_true",
        help="Enable AI-powered analysis (requires QGenie configuration)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(f"Parsed arguments: {args}")
