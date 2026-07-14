"""
paper_trading/small_capital_strategy/decision_report_version_v187.py
Version metadata for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only.
[!] Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.8.7"
RELEASE_NAME = "Decision Report Export & Evidence Pack"
BASE_RELEASE = "v1.8.6-end-to-end-small-capital-decision-cockpit"
SCHEMA_VERSION = "187"
POLICY_VERSION = "1.8.7-small-capital-strategy-decision-report-export-evidence-pack"
INCLUDED_RELEASES = [
    "Small Capital Strategy v1.7.0",
    "Watchlist Strategy Layer v1.7.1",
    "A/B/C Buy Point Execution Plan v1.7.2",
    "Market Regime Position Control v1.7.3",
    "Small Account Trade Journal v1.7.5",
    "Mistake Taxonomy Review Dashboard v1.7.6",
    "Theme Rotation Scanner v1.7.7",
    "Small Capital Strategy Integration v1.7.8",
    "Small Capital Strategy Stable Rollup v1.7.9",
    "Paper Simulation & Performance Lab v1.8.0",
    "Simulation Scenario Matrix & Stress Test Lab v1.8.1",
    "Parameter Optimization & Walk-Forward Validation Lab v1.8.2",
    "Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3",
    "Position Sizing & Capital Allocation Lab v1.8.4",
    "Portfolio Construction & Rebalancing Lab v1.8.5",
    "End-to-End Small Capital Decision Cockpit v1.8.6",
    "Decision Report Export & Evidence Pack v1.8.7",
]

REPORT_TYPES = [
    "daily_decision_report",
    "weekly_decision_report",
    "watchlist_report",
    "blocked_candidates_report",
    "reduce_risk_report",
    "paper_plan_ready_report",
    "portfolio_exposure_report",
    "monte_carlo_risk_report",
    "abc_buy_point_report",
    "evidence_pack",
    "audit_trail",
    "export_manifest",
]

EXPORT_FORMATS = [
    "json",
    "markdown",
    "csv_rows",
    "console_summary",
    "dashboard_payload",
]

FINAL_REPORT_GRADES = [
    "COMPLETE",
    "REVIEW_REQUIRED",
    "PARTIAL",
    "BLOCKED",
    "INVALID",
]

MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 23
MIN_HEALTH_CHECKS = 60
KNOWN_RELEASE_NAMES = list(INCLUDED_RELEASES)


def get_version_info() -> dict:
    """Return version metadata dict."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "decision_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "report_types": REPORT_TYPES,
        "export_formats": EXPORT_FORMATS,
        "final_report_grades": FINAL_REPORT_GRADES,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.8.7'."""
    return VERSION == "1.8.7"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_report_types() -> list:
    """Return list of supported report types."""
    return list(REPORT_TYPES)


def get_export_formats() -> list:
    """Return list of supported export formats."""
    return list(EXPORT_FORMATS)


def get_final_report_grades() -> list:
    """Return list of final report grades."""
    return list(FINAL_REPORT_GRADES)
