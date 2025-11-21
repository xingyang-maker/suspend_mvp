#!/usr/bin/env python3
"""
Utility Functions for Android Suspend Diagnosis

This module provides helper functions for executing shell commands and ADB commands.
"""
import subprocess


def run(cmd: str, timeout: int = 60) -> str:
    """
    Execute a shell command and return stdout (decoded as UTF-8).
    
    Returns an error message like "<ERROR: ...>" on failure without raising exceptions,
    maintaining the error-tolerant style of the original script.
    
    Args:
        cmd: Shell command to execute
        timeout: Command timeout in seconds (default: 60)
        
    Returns:
        str: Command output or error message
    """
    try:
        out = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, timeout=timeout
        )
        return out.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"<ERROR: {e}>"


def adb_shell(adb: str, device: str, command: str, timeout: int = 60) -> str:
    """
    Execute an ADB shell command on the specified device.
    
    If device is empty, the default device will be used.
    
    Args:
        adb: Path to ADB executable
        device: Target device serial number (empty for default device)
        command: ADB shell command to execute
        timeout: Command timeout in seconds (default: 60)
        
    Returns:
        str: Command output or error message
    """
    dev = f"-s {device}" if device else ""
    return run(f"{adb} {dev} shell {command}", timeout=timeout)
