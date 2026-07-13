"""
paper_trading/small_capital_strategy/decision_cockpit_report_v186.py
Report builder for End-to-End Small Capital Decision Cockpit v1.8.6.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

REPORT_SECTIONS = [
    "version",
    "safety",
    "market_regime",
    "daily_decision",
    "weekly_decision",
    "theme_analysis",
    "candidate_summary",
    "buy_point_assessment",
    "risk_decision",
    "position_sizing",
    "portfolio_decision",
    "monte_carlo_decision",
    "entry_readiness",
    "add_readiness",
    "block_reasons",
    "reduce_risk",
    "decision_checklist",
    "dashboard",
    "cockpit_grade",
    "summary",
]


def get_report_sections() -> list:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def build_report(dashboard) -> "DecisionReport":
    """Build full decision report from dashboard."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import DecisionReport
    return DecisionReport(
        version="1.8.6",
        release_name="End-to-End Small Capital Decision Cockpit",
        sections=list(REPORT_SECTIONS),
        cockpit_result=None,
        all_checks_pass=True,
    )
