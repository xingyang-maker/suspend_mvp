#!/usr/bin/env python3
"""
HTML Report Generator for Android Suspend Diagnosis

This module converts Markdown reports to HTML and adds interactive charts.
"""
import base64
import io
from pathlib import Path
from typing import List

import markdown
import matplotlib.pyplot as plt

from models.types import WakeupSource


class HtmlRenderer:
    """
    Converts Markdown files to HTML and embeds a bar chart of Top-5 Wakeup Sources.
    Returns the path to the generated HTML file.
    """

    def render(self, md_path: str, top_ws: List[WakeupSource]) -> str:
        """
        Convert a Markdown report to HTML and add visualizations.
        
        Args:
            md_path: Path to the Markdown file
            top_ws: List of top wakeup sources (name, active_count, total_time)
            
        Returns:
            str: Path to the generated HTML file
        """
        # Read the Markdown file
        with open(md_path, encoding="utf-8") as f:
            md_text = f.read()
        
        # Convert Markdown to HTML
        html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

        # Generate chart for wakeup sources
        img_tag = ""
        if top_ws:
            # Extract data for the chart
            names = [n for n, _, _ in top_ws]
            actives = [a for _, a, _ in top_ws]
            totals = [t for _, _, t in top_ws]

            # Create a figure with two Y axes
            fig, ax1 = plt.subplots(figsize=(8, 4))
            
            # Bar chart for active_count
            ax1.bar(names, actives, color="#1f77b4", label="active_count")
            ax1.set_ylabel("active_count", color="#1f77b4")
            ax1.tick_params(axis="x", rotation=45)

            # Line chart for total_time on secondary Y axis
            ax2 = ax1.twinx()
            ax2.plot(names, totals, color="#ff7f0e", marker="o", label="total_time")
            ax2.set_ylabel("total_time", color="#ff7f0e")
            
            plt.title("Top Wakeup Sources")
            plt.tight_layout()

            # Convert the plot to a base64-encoded image
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            plt.close(fig)
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode()
            
            # Create an HTML img tag with the embedded image
            img_tag = f'<h2>Top Wakeup Sources Chart</h2><img src="data:image/png;base64,{b64}" alt="wakeup sources"/>'

        # Assemble the complete HTML document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Suspend Diagnosis Report</title>
    <style>
        body {{font-family: Arial, Helvetica, sans-serif; margin: 2rem; line-height: 1.6;}}
        h1, h2, h3 {{color: #2c3e50;}}
        pre {{background:#f8f8f8; padding:1rem; overflow:auto;}}
        table {{border-collapse: collapse; width: 100%;}}
        th, td {{border: 1px solid #ddd; padding: 8px; text-align: left;}}
        th {{background:#f2f2f2;}}
    </style>
</head>
<body>
{html_body}
{img_tag}
</body>
</html>"""

        # Write the HTML to a file
        html_path = Path(md_path).with_suffix(".html")
        Path(html_path).write_text(html, encoding="utf-8")
        
        print(f"[REPORT] Markdown: {md_path}")
        print(f"[REPORT] HTML    : {html_path}")
        
        return str(html_path)
