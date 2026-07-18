"""
paper_trading/small_capital_strategy/strategy_review_version_v195.py
Version metadata for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.5"
RELEASE_NAME = "Paper Strategy Review Alert & Human Approval Lab"
BASE_RELEASE = "v1.9.4-paper-strategy-monitoring-drift-detection-lab"
SCHEMA_VERSION = "195"
POLICY_VERSION = "1.9.5-small-capital-strategy-paper-strategy-review-alert-human-approval-lab"

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
]

REVIEW_ALERT_CATEGORIES = [
    "WIN_RATE_DRIFT_REVIEW",
    "EXPECTANCY_DRIFT_REVIEW",
    "PROFIT_FACTOR_DRIFT_REVIEW",
    "DRAWDOWN_REVIEW",
    "SIGNAL_COLLAPSE_REVIEW",
    "GUARDRAIL_FALSE_POSITIVE_REVIEW",
    "OPPORTUNITY_LOSS_REVIEW",
    "EVIDENCE_MISSING_REVIEW",
    "MARKET_REGIME_MISMATCH_REVIEW",
    "ROLLBACK_TRIGGER_REVIEW",
    "SAFETY_FLAG_REVIEW",
    "MANUAL_APPROVAL_REQUIRED",
    "PACKAGE_SUSPENSION_REVIEW",
    "CONTINUE_MONITORING_REVIEW",
]

REVIEW_SEVERITIES = [
    "INFO",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

REVIEW_DECISION_STATES = [
    "DRAFT",
    "PENDING_REVIEW",
    "APPROVED_FOR_PAPER_ONLY",
    "KEEP_MONITORING",
    "KEEP_SHADOW_ONLY",
    "REJECTED",
    "ROLLBACK_REVIEW_REQUIRED",
    "SUSPENDED_FOR_PAPER",
    "NEED_MORE_EVIDENCE",
    "INVALID",
]

REVIEW_RECOMMENDATIONS = [
    "APPROVE_FOR_PAPER_ONLY",
    "KEEP_MONITORING",
    "KEEP_SHADOW_ONLY",
    "REJECT_CANDIDATE",
    "OPEN_ROLLBACK_REVIEW",
    "SUSPEND_CANDIDATE_RULE",
    "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_LONGER_MONITORING",
    "ESCALATE_TO_MANUAL_REVIEW",
    "NO_CHANGE",
]

FORBIDDEN_REVIEW_ACTIONS = [
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

ALLOWED_REVIEW_ACTIONS = [
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
    "HUMAN_APPROVAL",
    "REVIEW_DECISION",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_requested",
    "leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_monitoring_alert_source",
    "missing_drift_detection_source",
    "missing_review_evidence",
    "missing_human_approval_checklist",
    "missing_decision_rationale",
    "malformed_review_input",
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
        "monitoring_review_only": True,
        "human_approval_only": True,
        "rollback_review_only": True,
        "review_only": True,
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
        "review_alert_categories": REVIEW_ALERT_CATEGORIES,
        "review_severities": REVIEW_SEVERITIES,
        "review_decision_states": REVIEW_DECISION_STATES,
        "review_recommendations": REVIEW_RECOMMENDATIONS,
        "forbidden_review_actions": FORBIDDEN_REVIEW_ACTIONS,
        "allowed_review_actions": ALLOWED_REVIEW_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.5'."""
    return VERSION == "1.9.5"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_review_alert_categories() -> list:
    return list(REVIEW_ALERT_CATEGORIES)


def get_review_severities() -> list:
    return list(REVIEW_SEVERITIES)


def get_review_decision_states() -> list:
    return list(REVIEW_DECISION_STATES)


def get_review_recommendations() -> list:
    return list(REVIEW_RECOMMENDATIONS)


def get_forbidden_review_actions() -> list:
    return list(FORBIDDEN_REVIEW_ACTIONS)


def get_allowed_review_actions() -> list:
    return list(ALLOWED_REVIEW_ACTIONS)


def get_hard_block_conditions() -> list:
    return list(HARD_BLOCK_CONDITIONS)
