"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_version_v197.py
Version metadata for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.7"
RELEASE_NAME = "Paper Strategy Governance Dashboard & Decision Quality Analytics Lab"
BASE_RELEASE = "v1.9.6-paper-strategy-decision-registry-governance-lab"
SCHEMA_VERSION = "197"
POLICY_VERSION = "1.9.7-small-capital-strategy-paper-strategy-governance-dashboard-decision-quality-analytics-lab"

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
    "Paper Decision Workflow Runner v1.8.8",
    "Paper Decision Journal & Review Loop v1.8.9",
    "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0",
    "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1",
    "Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2",
    "Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3",
    "Paper Strategy Monitoring & Drift Detection Lab v1.9.4",
    "Paper Strategy Review Alert & Human Approval Lab v1.9.5",
    "Paper Strategy Decision Registry & Governance Lab v1.9.6",
    "Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7",
]

DECISION_QUALITY_METRICS = [
    "evidence_coverage_score",
    "rationale_completeness_score",
    "checklist_completeness_score",
    "lineage_completeness_score",
    "audit_trail_completeness_score",
    "outcome_consistency_score",
    "rollback_review_frequency_score",
    "governance_violation_score",
    "paper_only_safety_score",
    "decision_latency_score",
    "review_quality_score",
    "registry_integrity_score",
]

DECISION_QUALITY_GRADES = [
    "EXCELLENT",
    "GOOD",
    "WATCH",
    "WEAK",
    "INVALID",
]

ANALYTICS_WINDOWS = [
    "DAILY",
    "WEEKLY",
    "MONTHLY",
    "QUARTERLY",
    "FULL_HISTORY",
]

DASHBOARD_PANELS = [
    "quality_overview",
    "evidence_coverage",
    "decision_outcome",
    "approval_quality",
    "rejection_quality",
    "keep_monitoring_quality",
    "rollback_review_frequency",
    "governance_violations",
    "decision_lineage_health",
    "audit_trail_health",
    "safety_summary",
    "export_manifest",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_or_leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_registry_source",
    "missing_decision_records",
    "malformed_analytics_input",
    "unsafe_export_path",
    "forbidden_action_words",
    "analytics_tries_to_execute_decision",
    "dashboard_tries_to_mutate_strategy",
]

FORBIDDEN_DASHBOARD_ACTIONS = [
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
]

ALLOWED_DASHBOARD_ACTIONS = [
    "GOVERNANCE_DASHBOARD_VERSION",
    "GOVERNANCE_DASHBOARD_RUN",
    "GOVERNANCE_DASHBOARD_QUALITY",
    "GOVERNANCE_DASHBOARD_SCORECARD",
    "GOVERNANCE_DASHBOARD_EVIDENCE",
    "GOVERNANCE_DASHBOARD_OUTCOMES",
    "GOVERNANCE_DASHBOARD_VIOLATIONS",
    "GOVERNANCE_DASHBOARD_ROLLBACK_FREQUENCY",
    "GOVERNANCE_DASHBOARD_LINEAGE_HEALTH",
    "GOVERNANCE_DASHBOARD_AUDIT_HEALTH",
    "GOVERNANCE_DASHBOARD_REPORT",
    "GOVERNANCE_DASHBOARD_EXPORT",
    "GOVERNANCE_DASHBOARD_HEALTH",
    "GOVERNANCE_DASHBOARD_GATE",
    "GOVERNANCE_DASHBOARD_SCENARIOS",
    "GOVERNANCE_DASHBOARD_FIXTURES",
    "GOVERNANCE_DASHBOARD_SAFETY_AUDIT",
    "QUALITY_ANALYTICS",
]

MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 16
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
        "governance_analytics_only": True,
        "dashboard_only": True,
        "quality_analytics_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "no_production_strategy_mutation": True,
        "no_automatic_rollback": True,
        "no_live_strategy_activation": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "decision_quality_metrics": DECISION_QUALITY_METRICS,
        "decision_quality_grades": DECISION_QUALITY_GRADES,
        "analytics_windows": ANALYTICS_WINDOWS,
        "dashboard_panels": DASHBOARD_PANELS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
        "forbidden_dashboard_actions": FORBIDDEN_DASHBOARD_ACTIONS,
        "allowed_dashboard_actions": ALLOWED_DASHBOARD_ACTIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.7'."""
    return VERSION == "1.9.7"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_decision_quality_metrics() -> list:
    """Return list of decision quality metric names."""
    return list(DECISION_QUALITY_METRICS)


def get_decision_quality_grades() -> list:
    """Return list of decision quality grade names."""
    return list(DECISION_QUALITY_GRADES)


def get_analytics_windows() -> list:
    """Return list of analytics window names."""
    return list(ANALYTICS_WINDOWS)


def get_dashboard_panels() -> list:
    """Return list of dashboard panel names."""
    return list(DASHBOARD_PANELS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)


def get_forbidden_dashboard_actions() -> list:
    """Return list of forbidden dashboard actions."""
    return list(FORBIDDEN_DASHBOARD_ACTIONS)


def get_allowed_dashboard_actions() -> list:
    """Return list of allowed dashboard actions."""
    return list(ALLOWED_DASHBOARD_ACTIONS)
