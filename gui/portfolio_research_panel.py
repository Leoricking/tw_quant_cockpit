"""
gui/portfolio_research_panel.py — Portfolio Research Foundation GUI panel v1.5.0.

Read-only research panel. No broker connection. No order submission.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PANEL_VERSION = "1.5.0"
PANEL_NAME = "Portfolio Research Foundation"
BROKER_LINKED = False
REAL_ORDER_ENABLED = False
_DISCLAIMER = (
    "RESEARCH ONLY — No Real Orders — No Broker Connection — Not Investment Advice"
)


class PortfolioResearchPanel:
    """
    Read-only GUI panel for Portfolio Research Foundation.
    Displays portfolio valuation, PnL, exposure, concentration, returns.
    No order submission. No broker connection.
    """

    RESEARCH_ONLY = True
    BROKER_LINKED = False
    REAL_ORDER_ENABLED = False

    def __init__(self):
        self._current_portfolio_id: Optional[str] = None
        self._current_as_of: Optional[str] = None
        self._last_report: Optional[Dict] = None

    def set_portfolio(self, portfolio_id: str, as_of: str) -> None:
        """Select which portfolio and as-of date to display."""
        self._current_portfolio_id = portfolio_id
        self._current_as_of = as_of

    def load_report(self, report: Dict[str, Any]) -> None:
        """Load a pre-generated portfolio research report into the panel."""
        self._last_report = report

    def render(self) -> Dict[str, Any]:
        """
        Return panel render state (dict).
        In a real GUI this would draw widgets; here it returns a structured dict
        suitable for JSON serialization or terminal display.
        """
        if not self._last_report:
            return {
                "panel": PANEL_NAME,
                "status": "NO_DATA",
                "disclaimer": _DISCLAIMER,
                "research_only": True,
            }

        report = self._last_report
        sections = report.get("sections", {})
        summary = report.get("summary", {})

        return {
            "panel": PANEL_NAME,
            "version": PANEL_VERSION,
            "portfolio_id": report.get("portfolio_id"),
            "as_of": report.get("as_of"),
            "generated_at": report.get("generated_at"),
            "disclaimer": _DISCLAIMER,
            "research_only": True,
            "broker_linked": False,
            "real_order_enabled": False,
            "summary": summary,
            "valuation_status": sections.get("valuation", {}).get("valuation_status"),
            "eligibility_status": sections.get("eligibility", {}).get("status"),
            "concentration_level": summary.get("concentration_level"),
            "total_value_twd": summary.get("total_portfolio_value_twd"),
        }

    def get_disclaimer(self) -> str:
        return _DISCLAIMER
