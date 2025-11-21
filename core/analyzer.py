#!/usr/bin/env python3
"""
Log Analysis Module for Android Suspend Diagnosis

This module provides functionality to analyze Android logs for suspend failures
and extract information about wakeup sources.
"""
import re
from typing import List, Tuple

from models.types import WakeupSource, SuspendAnalysisResult


class SimpleAnalyzer:
    """
    Business logic layer: Parses logs to determine if suspend failed and extracts wakeup source rankings.
    """

    @staticmethod
    def parse_suspend_failed(dmesg_txt: str, dumpsys_suspend_txt: str) -> SuspendAnalysisResult:
        """
        Analyze logs to determine if suspend failed and identify reasons.
        
        Args:
            dmesg_txt: Content of dmesg log
            dumpsys_suspend_txt: Content of dumpsys suspend_control_internal output
            
        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - failed: Boolean indicating if suspend failed
                - reasons: List of reasons for failure
        """
        failed, reasons = False, []
        
        # Check dumpsys output for last_failed_suspend counter
        if "last_failed_suspend" in dumpsys_suspend_txt:
            for line in dumpsys_suspend_txt.splitlines():
                if "last_failed_suspend" in line:
                    try:
                        # Extract numeric value from the line
                        val = int("".join([c for c in line if c.isdigit()]))
                        if val > 0:
                            failed = True
                            reasons.append(f"dumpsys: last_failed_suspend={val}")
                    except Exception:
                        # Skip if we can't parse the value
                        pass
        
        # Check dmesg for suspend failure messages
        if ("PM: suspend entry failed" in dmesg_txt) or ("suspend entry failed" in dmesg_txt):
            failed = True
            reasons.append("dmesg: suspend entry failed")
            
        return failed, reasons

    @staticmethod
    def extract_wakeup_top(ws_txt: str, topn: int = 5) -> List[WakeupSource]:
        """
        Parse /sys/kernel/debug/wakeup_sources content and return top wakeup sources.
        
        Performs error-tolerant parsing of numeric fields to handle different kernel versions.
        
        Args:
            ws_txt: Content of wakeup_sources file
            topn: Number of top wakeup sources to return (default: 5)
            
        Returns:
            List[Tuple[str, int, float]]: List of tuples containing:
                - name: Wakeup source name
                - active_count: Number of active wakeups
                - total_time: Total wakeup time
        """
        # Filter out empty lines
        lines = [l for l in ws_txt.splitlines() if l.strip()]
        if not lines:
            return []

        # Parse header row to identify column positions
        header = lines[0].split()
        tbl: List[WakeupSource] = []

        # Process each data row
        for l in lines[1:]:
            cols = l.split()
            if len(cols) < len(header):
                continue
                
            # Create a dictionary mapping column names to values
            row = dict(zip(header, cols))

            # Extract name (handle different kernel versions)
            name = row.get("name") or row.get("wakeup_source") or cols[0]

            # Extract active_count with error handling
            raw_active = row.get("active_count", "0")
            m = re.search(r"\d+", raw_active)
            active = int(m.group()) if m else 0

            # Extract total_time with error handling
            raw_total = row.get("total_time", "0")
            # Clean up the value (handle different formats)
            cleaned = re.sub(r"[^0-9.]", "", raw_total.replace(",", "."))
            try:
                total = float(cleaned) if cleaned else 0.0
            except ValueError:
                total = 0.0

            tbl.append((name, active, total))

        # Sort by active_count (primary) and total_time (secondary)
        tbl.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return tbl[:topn]
