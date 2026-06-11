"""
Empty state helpers for GUI panels.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from typing import Optional

EMPTY_NO_DATA = ("No Data Yet", "No data available.", "Run the command first to load data.")
EMPTY_INSUFFICIENT = ("Insufficient Evidence", "Not enough data to display results.", "Collect more backtest results and retry.")
EMPTY_RUN_SCAN_FIRST = ("No Scan Results", "No scan results found.", "Run the scan command first, then refresh.")
EMPTY_RUN_REPORT_FIRST = ("No Report Found", "No latest report output found.", "Generate the report first, then refresh.")


def build_empty_state(
    title: str,
    description: str,
    next_step: str,
    research_note: Optional[str] = None,
) -> dict:
    """
    Build a friendly empty state descriptor dict.
    All fields are research-only safe.
    """
    note = research_note or "Research Only — No Real Orders"
    return {
        "title": title,
        "description": description,
        "next_step": next_step,
        "research_note": note,
    }
