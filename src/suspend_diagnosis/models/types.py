#!/usr/bin/env python3
"""
Type Definitions for Android Suspend Diagnosis

This module defines common types used throughout the project.
"""
from typing import Dict, List, Tuple, Optional, Mapping, Any, Union

# Check if TypeAlias is available (Python 3.10+)
try:
    from typing import TypeAlias
    HAS_TYPE_ALIAS = True
except ImportError:
    HAS_TYPE_ALIAS = False

# Type for a collection of evidence files
if HAS_TYPE_ALIAS:
    ArtifactMap: TypeAlias = Dict[str, str]  # {filename: absolute_path}
    # Type for a wakeup source entry
    WakeupSource: TypeAlias = Tuple[str, int, float]  # (name, active_count, total_time)
    # Type for a collection of log contents
    LogMap: TypeAlias = Mapping[str, str]  # {log_type: content}
    # Type for suspend failure analysis result
    SuspendAnalysisResult: TypeAlias = Tuple[bool, List[str]]  # (failed, reasons)
else:
    # For Python < 3.10, use type comments instead
    ArtifactMap = Dict[str, str]  # {filename: absolute_path}
    WakeupSource = Tuple[str, int, float]  # (name, active_count, total_time)
    LogMap = Mapping[str, str]  # {log_type: content}
    SuspendAnalysisResult = Tuple[bool, List[str]]  # (failed, reasons)
