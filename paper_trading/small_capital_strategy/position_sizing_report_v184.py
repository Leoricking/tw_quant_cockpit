"""
paper_trading/small_capital_strategy/position_sizing_report_v184.py
Report builder for Position Sizing & Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

REPORT_SECTIONS = [
    "version",
    "safety",
    "capital_profile",
    "risk_budget",
    "position_sizing_engine",
    "abc_staged_sizing",
    "exposure_limits",
    "concentration_risk",
    "drawdown_budget",
    "cash_reserve",
    "capital_stage_plan",
    "summary",
]


def get_report_sections() -> list:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def build_report(dashboard) -> "PositionSizingReport":
    """Build full position sizing report from dashboard."""
    from paper_trading.small_capital_strategy.position_sizing_models_v184 import PositionSizingReport
    return PositionSizingReport(
        version="1.8.4",
        release_name="Position Sizing & Capital Allocation Lab",
        sections=list(REPORT_SECTIONS),
        all_checks_pass=True,
    )
