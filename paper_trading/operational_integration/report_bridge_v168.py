"""
paper_trading/operational_integration/report_bridge_v168.py
Report Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_LIMITATIONS = [
    "Simulation only - not a real performance record",
    "Paper trading only - no real orders executed",
    "Research only - not investment advice",
    "Not for production use",
    "Historical replay only - no real-time predictions",
]

_SAFETY_DISCLAIMERS = [
    "NO_REAL_ORDERS: All orders are simulated",
    "NO_BROKER: No broker connection used",
    "NO_REAL_ACCOUNT: No real account access",
    "PAPER_ONLY: Paper trading simulation only",
    "NOT_FOR_PRODUCTION: Research and backtesting only",
]


class ReportBridge:
    """Validates and enriches integration reports. Research only."""

    def check_report_lineage(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Check report has valid lineage linking to run."""
        has_run_id = bool(report.get("run_id"))
        has_report_id = bool(report.get("report_id"))
        has_lineage = bool(report.get("source_lineage") or report.get("lineage_id"))
        return {
            "has_run_id": has_run_id,
            "has_report_id": has_report_id,
            "has_lineage": has_lineage,
            "valid": has_run_id and has_report_id,
            "paper_only": True,
        }

    def check_summary_reconciliation(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Check that report summary reconciles with detail sections."""
        summary = report.get("summary", {})
        sections = report.get("sections", {})
        has_summary = bool(summary)
        has_sections = bool(sections)
        section_count = len(sections) if isinstance(sections, dict) else 0
        return {
            "has_summary": has_summary,
            "has_sections": has_sections,
            "section_count": section_count,
            "reconciled": has_summary and has_sections,
            "paper_only": True,
        }

    def add_limitations(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Add standard limitations section to report."""
        report_copy = dict(report)
        existing = report_copy.get("limitations", [])
        combined = list(existing) + [l for l in _LIMITATIONS if l not in existing]
        report_copy["limitations"] = combined
        report_copy["paper_only"] = True
        return report_copy

    def add_safety_status(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Add safety status section to report."""
        report_copy = dict(report)
        report_copy["safety_status"] = {
            "disclaimers": _SAFETY_DISCLAIMERS,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
            "broker_enabled": False,
            "production_trading_blocked": True,
        }
        return report_copy

    def summarize(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Return summary of report."""
        return {
            "report_id": report.get("report_id", ""),
            "run_id": report.get("run_id", ""),
            "has_summary": bool(report.get("summary")),
            "has_sections": bool(report.get("sections")),
            "has_limitations": bool(report.get("limitations")),
            "has_safety_status": bool(report.get("safety_status")),
            "paper_only": True,
        }
