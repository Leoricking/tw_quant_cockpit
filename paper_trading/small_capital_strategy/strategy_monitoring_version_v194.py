"""
paper_trading/small_capital_strategy/strategy_monitoring_version_v194.py
Version metadata for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.4"
RELEASE_NAME = "Paper Strategy Monitoring & Drift Detection Lab"
BASE_RELEASE = "v1.9.3-paper-strategy-promotion-package-rollback-plan-lab"
SCHEMA_VERSION = "194"
POLICY_VERSION = "1.9.4-small-capital-strategy-paper-strategy-monitoring-drift-detection-lab"

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
]

DRIFT_CATEGORIES = [
    "WIN_RATE_DRIFT",
    "EXPECTANCY_DRIFT",
    "PROFIT_FACTOR_DRIFT",
    "DRAWDOWN_DRIFT",
    "AVERAGE_LOSS_DRIFT",
    "SIGNAL_COUNT_DRIFT",
    "SIGNAL_QUALITY_DRIFT",
    "MISTAKE_RATE_DRIFT",
    "CHASE_HIGH_DRIFT",
    "EARLY_ENTRY_DRIFT",
    "OVER_CONCENTRATION_DRIFT",
    "CASH_RESERVE_DRIFT",
    "GUARDRAIL_FALSE_POSITIVE_DRIFT",
    "GUARDRAIL_FALSE_NEGATIVE_DRIFT",
    "OPPORTUNITY_LOSS_DRIFT",
    "EVIDENCE_COMPLETENESS_DRIFT",
    "MARKET_REGIME_MISMATCH_DRIFT",
]

DRIFT_SEVERITIES = [
    "NONE",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

MONITORING_STATUSES = [
    "HEALTHY",
    "WATCH",
    "REVIEW_REQUIRED",
    "ROLLBACK_REQUIRED",
    "BLOCKED",
    "INVALID",
]

MONITORING_RECOMMENDATIONS = [
    "CONTINUE_MONITORING",
    "KEEP_SHADOW_ONLY",
    "REQUIRE_MANUAL_REVIEW",
    "TRIGGER_ROLLBACK_REVIEW",
    "ROLLBACK_TO_BASELINE",
    "EXTEND_MONITORING_WINDOW",
    "REQUIRE_MORE_DATA",
    "TIGHTEN_GUARDRAIL",
    "LOOSEN_GUARDRAIL",
    "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE",
    "SUSPEND_CANDIDATE_RULE",
    "NO_CHANGE",
]

FORBIDDEN_MONITORING_ACTIONS = [
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

ALLOWED_MONITORING_ACTIONS = [
    "REVIEW",
    "MONITOR",
    "DRIFT_CHECK",
    "ROLLBACK_ALERT",
    "ANALYZE",
    "REPORT",
    "EXPORT",
    "AUDIT",
    "VALIDATE",
    "SIMULATE",
    "RESEARCH",
    "RECOMMEND",
    "EVIDENCE_PACK",
    "DASHBOARD",
    "HEALTH_CHECK",
    "SAFETY_AUDIT",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_requested",
    "leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_promotion_package_source",
    "missing_rollback_plan_source",
    "missing_baseline_monitoring_snapshot",
    "missing_current_monitoring_snapshot",
    "missing_monitoring_window",
    "missing_evidence",
    "malformed_monitoring_input",
    "unsafe_export_path",
    "forbidden_action_words",
]

MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 18
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
        "monitoring_only": True,
        "drift_detection_only": True,
        "rollback_trigger_only": True,
        "review_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "no_production_strategy_mutation": True,
        "no_live_strategy_activation": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "drift_categories": DRIFT_CATEGORIES,
        "drift_severities": DRIFT_SEVERITIES,
        "monitoring_statuses": MONITORING_STATUSES,
        "monitoring_recommendations": MONITORING_RECOMMENDATIONS,
        "forbidden_monitoring_actions": FORBIDDEN_MONITORING_ACTIONS,
        "allowed_monitoring_actions": ALLOWED_MONITORING_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.4'."""
    return VERSION == "1.9.4"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_drift_categories() -> list:
    """Return list of drift categories."""
    return list(DRIFT_CATEGORIES)


def get_drift_severities() -> list:
    """Return list of drift severities."""
    return list(DRIFT_SEVERITIES)


def get_monitoring_statuses() -> list:
    """Return list of monitoring statuses."""
    return list(MONITORING_STATUSES)


def get_monitoring_recommendations() -> list:
    """Return list of monitoring recommendations."""
    return list(MONITORING_RECOMMENDATIONS)


def get_forbidden_monitoring_actions() -> list:
    """Return list of forbidden monitoring actions."""
    return list(FORBIDDEN_MONITORING_ACTIONS)


def get_allowed_monitoring_actions() -> list:
    """Return list of allowed monitoring actions."""
    return list(ALLOWED_MONITORING_ACTIONS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
