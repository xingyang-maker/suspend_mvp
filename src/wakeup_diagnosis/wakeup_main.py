#!/usr/bin/env python3
"""
Wakeup Diagnosis Main Module

This module provides the main functionality for diagnosing Android device wakeup issues.
"""
import sys
from pathlib import Path

# Add common modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from wakeup_analyzer import WakeupAnalyzer
from wakeup_cli import parse_args
from collector import LogCollector
from ai import AIAnalyzer
from report.markdown_builder import MarkdownBuilder
from report.html_renderer import HTMLRenderer


def main(args):
    """
    Main function for wakeup diagnosis.
    
    Args:
        args: Parsed command line arguments
    """
    print("🔍 Android Wakeup Diagnosis Tool")
    print("=" * 50)
    
    # Initialize components
    collector = LogCollector(args.adb, args.device)
    analyzer = WakeupAnalyzer()
    ai_analyzer = AIAnalyzer() if hasattr(args, 'enable_ai') and args.enable_ai else None
    
    # Collect or use existing logs
    if args.case_dir:
        print(f"📁 Using existing logs from: {args.case_dir}")
        case_dir = args.case_dir
        artifacts = collector.discover_logs(case_dir)
    else:
        print("📱 Collecting fresh logs from device...")
        case_dir, artifacts = collector.collect_wakeup_logs(args.out)
    
    print(f"📊 Analyzing wakeup patterns...")
    
    # Analyze logs
    failed, reasons, detailed_analysis = analyzer.analyze(artifacts)
    
    # AI analysis (if enabled)
    ai_md = None
    if ai_analyzer and artifacts:
        print("🤖 Running AI analysis...")
        try:
            ai_md = ai_analyzer.analyze_wakeup_logs(artifacts)
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
    
    # Generate reports
    print("📝 Generating reports...")
    
    # Markdown report
    md_builder = MarkdownBuilder()
    md_path = md_builder.build_wakeup_report(
        case_dir, failed, reasons, ai_md, artifacts, detailed_analysis
    )
    
    # HTML report
    html_renderer = HTMLRenderer()
    html_path = html_renderer.render_wakeup_report(md_path, artifacts)
    
    # Summary
    print("\n" + "=" * 50)
    if failed:
        print("🔴 CONCLUSION: Wakeup Issues Detected")
        for reason in reasons:
            print(f"  • {reason}")
    else:
        print("🟢 CONCLUSION: Wakeup Behavior Normal")
    
    print(f"\n📄 Reports generated:")
    print(f"  • Markdown: {md_path}")
    print(f"  • HTML: {html_path}")
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    args = parse_args()
    main(args)
