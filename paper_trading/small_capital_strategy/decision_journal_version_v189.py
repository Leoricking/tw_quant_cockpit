"""
paper_trading/small_capital_strategy/decision_journal_version_v189.py
Version metadata for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.8.9"
RELEASE_NAME = "Paper Decision Journal & Review Loop"
BASE_RELEASE = "v1.8.8-paper-decision-workflow-runner"
SCHEMA_VERSION = "189"
POLICY_VERSION = "1.8.9-small-capital-strategy-paper-decision-journal-review-loop"

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
]

JOURNAL_ENTRY_STATES = [
    "OBSERVE",
    "WAIT",
    "PAPER_PLAN_READY",
    "PAPER_ENTRY_ALLOWED",
    "PAPER_ADD_ALLOWED",
    "REDUCE_RISK",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "NO_TRADE",
    "RESEARCH_ONLY",
    "SIMULATE_ONLY",
    "VALIDATION_ONLY",
    "DECISION_ONLY",
    "REPORT_ONLY",
    "WORKFLOW_ONLY",
    "AUDIT_ONLY",
]

REVIEW_DIMENSIONS = [
    "market_regime_alignment",
    "theme_alignment",
    "abc_buy_point_quality",
    "position_sizing_quality",
    "stop_loss_quality",
    "take_profit_quality",
    "evidence_completeness",
    "risk_budget_usage",
    "concentration_risk",
    "cash_reserve_quality",
    "blocked_condition_respect",
    "execution_discipline",
    "overtrade_risk",
    "chase_high_risk",
    "premature_entry_risk",
    "missed_risk_warning",
    "decision_consistency",
    "workflow_completeness",
    "journal_completeness",
    "audit_traceability",
]

MISTAKE_TAGS = [
    "CHASE_HIGH",
    "ENTER_TOO_EARLY",
    "IGNORE_MARKET_REGIME",
    "IGNORE_VOLUME_RISK",
    "IGNORE_MA_BREAK",
    "OVERSIZE_POSITION",
    "OVER_CONCENTRATION",
    "LOW_CASH_RESERVE",
    "IGNORE_BLOCK_REASON",
    "MISSING_EVIDENCE",
    "WEAK_THEME",
    "WEAK_RELATIVE_STRENGTH",
    "LATE_SECOND_WAVE",
    "NO_CLEAR_STOP",
    "NO_CLEAR_TAKE_PROFIT",
    "PLAN_NOT_FOLLOWED",
    "REVIEW_REQUIRED",
    "NO_MISTAKE_FOUND",
]

QUALITY_GRADES = [
    "EXCELLENT",
    "GOOD",
    "ACCEPTABLE",
    "REVIEW_REQUIRED",
    "POOR",
    "INVALID",
]

FORBIDDEN_JOURNAL_ACTIONS = [
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

ALLOWED_JOURNAL_ACTIONS = [
    "OBSERVE",
    "WAIT",
    "PAPER_PLAN_READY",
    "PAPER_ENTRY_ALLOWED",
    "PAPER_ADD_ALLOWED",
    "REDUCE_RISK",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "NO_TRADE",
    "RESEARCH_ONLY",
    "SIMULATE_ONLY",
    "VALIDATION_ONLY",
    "DECISION_ONLY",
    "REPORT_ONLY",
    "WORKFLOW_ONLY",
    "AUDIT_ONLY",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_requested",
    "leverage_requested",
    "production_db_write_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_journal_audit_trail",
    "missing_workflow_evidence_link",
    "missing_decision_timestamp_policy",
    "malformed_journal_entry",
    "paper_decision_without_evidence",
    "review_without_source_workflow_id",
    "outcome_snapshot_without_risk_context",
    "weekly_review_without_daily_entries",
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
        "decision_only": True,
        "journal_only": True,
        "review_only": True,
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
        "journal_entry_states": JOURNAL_ENTRY_STATES,
        "review_dimensions": REVIEW_DIMENSIONS,
        "mistake_tags": MISTAKE_TAGS,
        "quality_grades": QUALITY_GRADES,
        "allowed_journal_actions": ALLOWED_JOURNAL_ACTIONS,
        "forbidden_journal_actions": FORBIDDEN_JOURNAL_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.8.9'."""
    return VERSION == "1.8.9"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_journal_entry_states() -> list:
    """Return list of supported journal entry states."""
    return list(JOURNAL_ENTRY_STATES)


def get_review_dimensions() -> list:
    """Return list of review dimensions."""
    return list(REVIEW_DIMENSIONS)


def get_mistake_tags() -> list:
    """Return list of mistake tags."""
    return list(MISTAKE_TAGS)


def get_quality_grades() -> list:
    """Return list of quality grades."""
    return list(QUALITY_GRADES)


def get_allowed_journal_actions() -> list:
    """Return list of allowed journal actions."""
    return list(ALLOWED_JOURNAL_ACTIONS)


def get_forbidden_journal_actions() -> list:
    """Return list of forbidden journal actions."""
    return list(FORBIDDEN_JOURNAL_ACTIONS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
