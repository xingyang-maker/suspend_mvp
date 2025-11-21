#!/usr/bin/env python3
"""
Android Suspend Diagnosis Tool

This tool collects and analyzes Android device logs to diagnose suspend-related issues.
It generates both Markdown and HTML reports with analysis results.
"""

import argparse
from pathlib import Path

from core.collector import AdbEvidenceCollector
from core.analyzer import SimpleAnalyzer
from core.ai import QGenieReporter
from core.report.markdown_builder import MarkdownBuilder
from core.report.html_renderer import HtmlRenderer
from cli import build_parser
from models.types import LogMap

def main(args):
    """
    Main function that orchestrates the suspend diagnosis process.
    
    Args:
        args: Command line arguments parsed by argparse
    """
    # Step 1: Collect evidence from the device
    collector = AdbEvidenceCollector(
        adb=args.adb,
        device=args.device,
        out_dir=args.out,
        collect_ftrace=args.collect_ftrace,
    )
    case_dir, artifacts = collector.collect()
    
    # Step 2: Read collected files
    txts = {k: Path(v).read_text(encoding='utf-8', errors='ignore') 
            for k, v in artifacts.items()}
    
    # Step 3: Analyze logs for suspend failures
    analyzer = SimpleAnalyzer()
    failed, reasons = analyzer.parse_suspend_failed(
        txts.get("dmesg.txt", ""), 
        txts.get("dumpsys_suspend.txt", "")
    )
    
    # Step 4: Extract top wakeup sources
    top_ws = analyzer.extract_wakeup_top(txts.get("wakeup_sources.txt", ""))
    
    # Step 5: AI analysis using QGenieReporter
    reporter = QGenieReporter(endpoint=args.ai_endpoint)
    logs: LogMap = {
        "dmesg": txts.get("dmesg.txt", "")[:4000],
        "logcat": txts.get("logcat.txt", "")[:4000],
        "dumpsys_suspend": txts.get("dumpsys_suspend.txt", "")[:4000],
        "wakeup_sources": txts.get("wakeup_sources.txt", "")[:4000],
    }
    ai_md = reporter.generate(logs)
    
    if ai_md:
        print("\n[AI RESPONSE]")
        print(ai_md)
    
    # Step 6: Generate Markdown report
    md_builder = MarkdownBuilder()
    md_path = md_builder.build(case_dir, failed, reasons, top_ws, ai_md, artifacts)
    
    # Step 7: Generate HTML report with charts
    html_renderer = HtmlRenderer()
    html_path = html_renderer.render(md_path, top_ws)
    
    print(f"\n[REPORT] Generated: {html_path}")

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    main(args)
