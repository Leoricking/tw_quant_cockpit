"""
paper_trading/small_capital_strategy/portfolio_construction_report_v185.py
Report builder for Portfolio Construction & Rebalancing Lab v1.8.5.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Portfolio Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

REPORT_SECTIONS = [
    "version",
    "safety",
    "portfolio_profile",
    "portfolio_construction",
    "exposure_control",
    "sector_risk",
    "theme_risk",
    "correlation_risk",
    "diversification_score",
    "concentration_risk",
    "rebalance_plan",
    "keep_reduce_replace",
    "rotation_candidates",
    "dashboard",
    "summary",
]


def get_report_sections() -> list:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def build_report(dashboard) -> "PortfolioRebalanceReport":
    """Build full portfolio construction report from dashboard."""
    from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
        PortfolioRebalanceReport,
    )
    rebalance_plan = dashboard.rebalance_plan if dashboard else None
    return PortfolioRebalanceReport(
        version="1.8.5",
        release_name="Portfolio Construction & Rebalancing Lab",
        sections=list(REPORT_SECTIONS),
        rebalance_plan=rebalance_plan,
        all_checks_pass=True,
    )
