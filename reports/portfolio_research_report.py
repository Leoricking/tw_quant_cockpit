"""
reports/portfolio_research_report.py — Portfolio Research Foundation report v1.5.0.

Generates a structured portfolio research report including valuation,
PnL, exposure, concentration, returns, and eligibility status.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
REPORT_VERSION = "1.5.0"
REPORT_NAME = "Portfolio Research Foundation"
_DISCLAIMER = (
    "[!] Research Only. No Real Orders. Not Investment Advice. "
    "All values are for research purposes only."
)


class PortfolioResearchReport:
    RESEARCH_ONLY = True

    def generate(
        self,
        portfolio_id: str,
        as_of: str,
        valuation: Optional[Dict] = None,
        pnl_summary: Optional[Dict] = None,
        exposure: Optional[Dict] = None,
        concentration: Optional[Dict] = None,
        returns: Optional[Dict] = None,
        eligibility: Optional[Dict] = None,
        benchmark: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Generate a structured portfolio research report.
        """
        generated_at = datetime.now(timezone.utc).isoformat()

        report = {
            "report_version": REPORT_VERSION,
            "report_name": REPORT_NAME,
            "portfolio_id": portfolio_id,
            "as_of": as_of,
            "generated_at": generated_at,
            "disclaimer": _DISCLAIMER,
            "research_only": True,
            "sections": {
                "valuation": valuation or {},
                "pnl_summary": pnl_summary or {},
                "exposure": exposure or {},
                "concentration": concentration or {},
                "returns": returns or {},
                "eligibility": eligibility or {},
                "benchmark": benchmark or {},
            },
            "metadata": metadata or {},
            "summary": self._build_summary(valuation, pnl_summary, concentration, eligibility),
        }
        return report

    def _build_summary(
        self,
        valuation: Optional[Dict],
        pnl_summary: Optional[Dict],
        concentration: Optional[Dict],
        eligibility: Optional[Dict],
    ) -> Dict[str, Any]:
        total_value = None
        if valuation:
            total_value = valuation.get("total_value_twd") or valuation.get("total_value")

        unrealized_pnl = None
        if pnl_summary:
            unrealized_pnl = pnl_summary.get("total_unrealized_pnl")

        concentration_level = None
        if concentration:
            level = concentration.get("concentration_level")
            concentration_level = level.value if hasattr(level, "value") else str(level) if level else None

        eligibility_status = None
        if eligibility:
            eligibility_status = eligibility.get("status")

        return {
            "total_portfolio_value_twd": str(total_value) if total_value is not None else None,
            "total_unrealized_pnl_twd": str(unrealized_pnl) if unrealized_pnl is not None else None,
            "concentration_level": concentration_level,
            "eligibility_status": eligibility_status,
            "research_only": True,
        }


def generate_portfolio_report(
    portfolio_id: str,
    as_of: str,
    **sections,
) -> Dict[str, Any]:
    """Convenience function."""
    return PortfolioResearchReport().generate(portfolio_id, as_of, **sections)
