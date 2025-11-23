#!/usr/bin/env python3
"""
Wakeup Analyzer Module

This module analyzes Android device wakeup patterns and identifies potential issues.
"""
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime, timedelta


class WakeupAnalyzer:
    """
    Analyzes Android device wakeup patterns to identify issues.
    
    This analyzer focuses on:
    1. Frequent wakeups (too many wakeup events)
    2. Wakeup source analysis (which components are causing wakeups)
    3. Wakeup timing patterns (irregular or excessive wakeup intervals)
    4. Power consumption correlation with wakeup events
    """
    
    def __init__(self):
        self.wakeup_threshold = 10  # wakeups per minute threshold
        self.analysis_window = 3600  # 1 hour analysis window in seconds
    
    def analyze(self, artifacts: Dict[str, str]) -> Tuple[bool, List[str], Optional[Dict]]:
        """
        Analyze wakeup patterns from collected logs.
        
        Args:
            artifacts: Dictionary mapping log file names to their paths
            
        Returns:
            Tuple of (has_issues, reasons, detailed_analysis)
        """
        reasons = []
        detailed_analysis = {}
        
        # Step 1: Analyze wakeup sources
        wakeup_sources_analysis = self._analyze_wakeup_sources(artifacts)
        detailed_analysis["wakeup_sources"] = wakeup_sources_analysis
        
        if wakeup_sources_analysis.get("excessive_wakeups"):
            reasons.extend(wakeup_sources_analysis["issues"])
        
        # Step 2: Analyze dmesg for wakeup events
        dmesg_analysis = self._analyze_dmesg_wakeups(artifacts)
        detailed_analysis["dmesg_wakeups"] = dmesg_analysis
        
        if dmesg_analysis.get("frequent_wakeups"):
            reasons.extend(dmesg_analysis["issues"])
        
        # Step 3: Analyze power management logs
        power_analysis = self._analyze_power_logs(artifacts)
        detailed_analysis["power_management"] = power_analysis
        
        if power_analysis.get("power_issues"):
            reasons.extend(power_analysis["issues"])
        
        # Step 4: Analyze logcat for app-related wakeups
        logcat_analysis = self._analyze_logcat_wakeups(artifacts)
        detailed_analysis["logcat_wakeups"] = logcat_analysis
        
        if logcat_analysis.get("app_wakeup_issues"):
            reasons.extend(logcat_analysis["issues"])
        
        # Overall conclusion
        has_issues = len(reasons) > 0
        if has_issues:
            detailed_analysis["conclusion"] = f"Detected {len(reasons)} wakeup-related issues"
        else:
            detailed_analysis["conclusion"] = "No significant wakeup issues detected"
        
        return has_issues, reasons, detailed_analysis
    
    def _analyze_wakeup_sources(self, artifacts: Dict[str, str]) -> Dict:
        """Analyze /sys/kernel/debug/wakeup_sources for excessive wakeup activity."""
        analysis = {
            "excessive_wakeups": False,
            "active_sources": [],
            "top_wakeup_sources": [],
            "issues": []
        }
        
        wakeup_sources_file = artifacts.get("wakeup_sources.txt")
        if not wakeup_sources_file or not Path(wakeup_sources_file).exists():
            analysis["issues"].append("wakeup_sources.txt not available for analysis")
            return analysis
        
        try:
            content = Path(wakeup_sources_file).read_text(encoding="utf-8", errors="ignore")
            lines = content.strip().split('\n')
            
            # Parse wakeup sources (format: name active_count event_count wakeup_count active_since total_time max_time last_change prevent_suspend_time)
            wakeup_data = []
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        name = parts[0]
                        active_count = int(parts[1]) if parts[1].isdigit() else 0
                        event_count = int(parts[2]) if parts[2].isdigit() else 0
                        wakeup_count = int(parts[3]) if parts[3].isdigit() else 0
                        
                        wakeup_data.append({
                            "name": name,
                            "active_count": active_count,
                            "event_count": event_count,
                            "wakeup_count": wakeup_count
                        })
            
            # Sort by wakeup count
            wakeup_data.sort(key=lambda x: x["wakeup_count"], reverse=True)
            analysis["top_wakeup_sources"] = wakeup_data[:10]
            
            # Check for excessive wakeups
            total_wakeups = sum(item["wakeup_count"] for item in wakeup_data)
            if total_wakeups > 1000:  # Threshold for excessive wakeups
                analysis["excessive_wakeups"] = True
                analysis["issues"].append(f"Excessive total wakeups detected: {total_wakeups}")
            
            # Check for individual sources with high wakeup counts
            for item in wakeup_data[:5]:  # Check top 5
                if item["wakeup_count"] > 100:
                    analysis["issues"].append(f"High wakeup count from '{item['name']}': {item['wakeup_count']} wakeups")
            
            # Check for active wakeup sources
            active_sources = [item for item in wakeup_data if item["active_count"] > 0]
            analysis["active_sources"] = active_sources
            
            if len(active_sources) > 5:
                analysis["issues"].append(f"Multiple active wakeup sources detected: {len(active_sources)}")
        
        except Exception as e:
            analysis["issues"].append(f"Failed to parse wakeup_sources.txt: {str(e)}")
        
        return analysis
    
    def _analyze_dmesg_wakeups(self, artifacts: Dict[str, str]) -> Dict:
        """Analyze dmesg for wakeup-related kernel messages."""
        analysis = {
            "frequent_wakeups": False,
            "wakeup_events": [],
            "wakeup_intervals": [],
            "issues": []
        }
        
        dmesg_file = artifacts.get("dmesg.txt")
        if not dmesg_file or not Path(dmesg_file).exists():
            analysis["issues"].append("dmesg.txt not available for wakeup analysis")
            return analysis
        
        try:
            content = Path(dmesg_file).read_text(encoding="utf-8", errors="ignore")
            lines = content.strip().split('\n')
            
            # Look for wakeup-related messages
            wakeup_patterns = [
                r"PM: suspend exit",
                r"PM: resume",
                r"wakeup.*interrupt",
                r"IRQ.*wakeup",
                r"Wakeup.*source"
            ]
            
            wakeup_events = []
            for line in lines:
                for pattern in wakeup_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Try to extract timestamp
                        timestamp_match = re.search(r'\[(\d+\.\d+)\]', line)
                        if timestamp_match:
                            timestamp = float(timestamp_match.group(1))
                            wakeup_events.append({
                                "timestamp": timestamp,
                                "message": line.strip()
                            })
                        break
            
            analysis["wakeup_events"] = wakeup_events[-20:]  # Keep last 20 events
            
            # Calculate wakeup intervals
            if len(wakeup_events) > 1:
                intervals = []
                for i in range(1, len(wakeup_events)):
                    interval = wakeup_events[i]["timestamp"] - wakeup_events[i-1]["timestamp"]
                    intervals.append(interval)
                
                analysis["wakeup_intervals"] = intervals
                
                # Check for frequent wakeups (less than 30 seconds apart)
                frequent_intervals = [i for i in intervals if i < 30]
                if len(frequent_intervals) > len(intervals) * 0.5:  # More than 50% are frequent
                    analysis["frequent_wakeups"] = True
                    analysis["issues"].append(f"Frequent wakeups detected: {len(frequent_intervals)} intervals < 30s")
                
                # Check average interval
                avg_interval = sum(intervals) / len(intervals)
                if avg_interval < 60:  # Less than 1 minute average
                    analysis["issues"].append(f"Short average wakeup interval: {avg_interval:.1f} seconds")
        
        except Exception as e:
            analysis["issues"].append(f"Failed to analyze dmesg wakeups: {str(e)}")
        
        return analysis
    
    def _analyze_power_logs(self, artifacts: Dict[str, str]) -> Dict:
        """Analyze power management related logs."""
        analysis = {
            "power_issues": False,
            "power_events": [],
            "issues": []
        }
        
        dumpsys_power_file = artifacts.get("dumpsys_power.txt")
        if not dumpsys_power_file or not Path(dumpsys_power_file).exists():
            analysis["issues"].append("dumpsys_power.txt not available for power analysis")
            return analysis
        
        try:
            content = Path(dumpsys_power_file).read_text(encoding="utf-8", errors="ignore")
            
            # Look for power-related issues
            if "Wake Locks:" in content:
                # Extract wake lock information
                wake_lock_section = content.split("Wake Locks:")[1].split("\n\n")[0]
                active_locks = []
                for line in wake_lock_section.split('\n'):
                    if 'PARTIAL_WAKE_LOCK' in line and 'held' in line:
                        active_locks.append(line.strip())
                
                if active_locks:
                    analysis["power_issues"] = True
                    analysis["issues"].append(f"Active wake locks detected: {len(active_locks)}")
                    analysis["power_events"].extend(active_locks[:5])  # Top 5
            
            # Check for screen wake events
            if "Screen wake locks:" in content:
                screen_wake_section = content.split("Screen wake locks:")[1].split("\n\n")[0]
                screen_wakes = len([line for line in screen_wake_section.split('\n') if line.strip()])
                if screen_wakes > 10:
                    analysis["issues"].append(f"Excessive screen wake events: {screen_wakes}")
        
        except Exception as e:
            analysis["issues"].append(f"Failed to analyze power logs: {str(e)}")
        
        return analysis
    
    def _analyze_logcat_wakeups(self, artifacts: Dict[str, str]) -> Dict:
        """Analyze logcat for application-related wakeup events."""
        analysis = {
            "app_wakeup_issues": False,
            "app_wakeups": [],
            "issues": []
        }
        
        logcat_file = artifacts.get("logcat.txt")
        if not logcat_file or not Path(logcat_file).exists():
            analysis["issues"].append("logcat.txt not available for app wakeup analysis")
            return analysis
        
        try:
            content = Path(logcat_file).read_text(encoding="utf-8", errors="ignore")
            lines = content.strip().split('\n')
            
            # Look for app wakeup patterns
            app_wakeup_patterns = [
                r"AlarmManager.*wakeup",
                r"JobScheduler.*wakeup",
                r"WakeLock.*acquired",
                r"PowerManager.*wakeUp"
            ]
            
            app_wakeups = []
            for line in lines:
                for pattern in app_wakeup_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        app_wakeups.append(line.strip())
                        break
            
            analysis["app_wakeups"] = app_wakeups[-10:]  # Keep last 10
            
            # Check for excessive app wakeups
            if len(app_wakeups) > 50:
                analysis["app_wakeup_issues"] = True
                analysis["issues"].append(f"Excessive app wakeup events detected: {len(app_wakeups)}")
            
            # Check for specific problematic apps
            app_counts = {}
            for wakeup in app_wakeups:
                # Try to extract app name
                app_match = re.search(r'([a-z]+\.[a-z]+\.[a-z]+)', wakeup)
                if app_match:
                    app_name = app_match.group(1)
                    app_counts[app_name] = app_counts.get(app_name, 0) + 1
            
            # Report apps with high wakeup counts
            for app, count in sorted(app_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                if count > 5:
                    analysis["issues"].append(f"App '{app}' has high wakeup activity: {count} events")
        
        except Exception as e:
            analysis["issues"].append(f"Failed to analyze logcat wakeups: {str(e)}")
        
        return analysis


if __name__ == "__main__":
    # Test the analyzer
    analyzer = WakeupAnalyzer()
    test_artifacts = {
        "wakeup_sources.txt": "test_wakeup_sources.txt",
        "dmesg.txt": "test_dmesg.txt"
    }
    
    failed, reasons, analysis = analyzer.analyze(test_artifacts)
    print(f"Analysis result: failed={failed}")
    print(f"Reasons: {reasons}")
    print(f"Detailed analysis: {analysis}")
