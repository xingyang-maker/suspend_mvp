#!/usr/bin/env python3
"""
AI Analysis Module for Android Suspend Diagnosis

This module provides AI-powered analysis of Android logs using the QGenie LLM service.
"""
import json
from typing import Optional

from qgenie import ChatMessage, QGenieClient
from suspend_diagnosis.models.types import LogMap


class QGenieReporter:
    """
    Calls the QGenie LLM service and returns text analysis results.
    
    The `endpoint` parameter is kept for compatibility but doesn't affect the actual call.
    If empty, the default QGenie configuration will be used.
    """

    def __init__(self, endpoint: Optional[str] = None):
        """
        Initialize the QGenie reporter.
        
        Args:
            endpoint: Optional QGenie endpoint URL (not used in current implementation)
        """
        self.endpoint = endpoint
        self.client = QGenieClient(max_retries=1, debug=True)

    def generate(self, logs: LogMap) -> Optional[str]:
        """
        Send logs to the model and return the generated text analysis.
        
        Args:
            logs: Dictionary mapping log types to their content
            
        Returns:
            Optional[str]: AI-generated analysis text, or None if an error occurred
        """
        # Construct prompt with length limit
        prompt = (
            "You are a power consumption and Android kernel expert. Based on the following logs, "
            "determine if there are any suspend failures and provide actionable remediation suggestions. "
            "Format your response as: Conclusion/Evidence Summary/Causes/Recommendations.\n\n"
            + json.dumps(logs, ensure_ascii=False)[:12000]
        )

        try:
            response = self.client.chat(
                messages=[ChatMessage(role="user", content=prompt)]
            )
            return response.choices[0].message.content
        except Exception as e:
            print("[AI ERROR]", e)
            return None
