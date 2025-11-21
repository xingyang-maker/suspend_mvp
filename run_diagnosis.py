#!/usr/bin/env python3
"""
Convenience script to run the Android Suspend Diagnosis Tool with common options.

This script provides a simple way to run the tool with the most commonly used options.
"""
import argparse
import subprocess
import sys
from pathlib import Path


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Android Suspend Diagnosis Tool with common options"
    )
    parser.add_argument(
        "--device", "-d",
        help="Target device serial number (empty for default device)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./reports",
        help="Output directory for reports (default: './reports')"
    )
    parser.add_argument(
        "--ftrace", "-f",
        action="store_true",
        help="Collect ftrace data"
    )
    parser.add_argument(
        "--ai", "-a",
        action="store_true",
        help="Enable AI analysis"
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    # Build command
    cmd = [sys.executable, "main.py"]
    
    if args.device:
        cmd.extend(["--device", args.device])
    
    if args.output:
        cmd.extend(["--out", args.output])
    
    if args.ftrace:
        cmd.append("--collect-ftrace")
    
    # Run the command
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)
    
    # Find the most recent report
    output_dir = Path(args.output)
    if output_dir.exists():
        report_dirs = sorted(
            [d for d in output_dir.iterdir() if d.is_dir() and d.name.startswith("suspend_diag_")],
            key=lambda d: d.stat().st_mtime,
            reverse=True
        )
        
        if report_dirs:
            latest_report = report_dirs[0]
            html_report = latest_report / "suspend_diagnosis_report.html"
            
            if html_report.exists():
                print(f"\nLatest report: {html_report}")
                print("You can open this HTML file in your browser to view the report.")


if __name__ == "__main__":
    main()
