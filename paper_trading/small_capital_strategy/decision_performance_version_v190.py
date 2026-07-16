"""
paper_trading/small_capital_strategy/decision_performance_version_v190.py
Version metadata for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.0"
RELEASE_NAME = "Paper Trading Performance Review & Strategy Improvement Lab"
BASE_RELEASE = "v1.8.9-paper-decision-journal-review-loop"
SCHEMA_VERSION = "190"
POLICY_VERSION = "1.9.0-small-capital-strategy-paper-trading-performance-review"

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
]

SETUP_TYPES = [
    "A_10MA_PULLBACK",
    "B_BASE_BREAKOUT",
    "C_20MA_RECLAIM",
    "SECOND_WAVE",
    "WATCHLIST_ONLY",
    "REDUCE_RISK",
    "BLOCKED_MARKET",
    "BLOCKED_RISK",
    "BLOCKED_EVIDENCE",
    "NO_TRADE_DAY",
    "UNKNOWN_SETUP",
]

IMPROVEMENT_SUGGESTIONS = [
    "KEEP_RULE",
    "TIGHTEN_RULE",
    "LOOSEN_RULE",
    "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE",
    "BLOCK_SETUP",
    "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_MARKET_REGIME_CONFIRMATION",
    "REQUIRE_VOLUME_CONFIRMATION",
    "REQUIRE_MA_CONFIRMATION",
    "REQUIRE_RISK_REVIEW",
    "REVIEW_MANUALLY",
    "NO_CHANGE",
]

QUALITY_GRADES = [
    "EXCELLENT",
    "GOOD",
    "ACCEPTABLE",
    "REVIEW_REQUIRED",
    "POOR",
    "INVALID",
]

PERFORMANCE_DIMENSIONS = [
    "total_paper_decisions",
    "reviewed_decision_count",
    "paper_plan_ready_count",
    "paper_entry_allowed_count",
    "reduce_risk_count",
    "blocked_count",
    "no_trade_count",
    "win_rate",
    "loss_rate",
    "average_gain_r",
    "average_loss_r",
    "expectancy_r",
    "profit_factor",
    "max_drawdown_r",
    "drawdown_budget_usage_pct",
    "average_holding_days",
    "setup_quality_score",
    "mistake_rate",
    "rule_violation_rate",
    "evidence_completeness_rate",
    "blocked_condition_respect_rate",
    "overtrade_score",
    "chase_high_score",
    "early_entry_score",
    "risk_control_score",
    "strategy_improvement_score",
]

FORBIDDEN_PERFORMANCE_ACTIONS = [
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

ALLOWED_PERFORMANCE_ACTIONS = [
    "REVIEW",
    "SUMMARIZE",
    "ANALYZE",
    "REPORT",
    "EXPORT",
    "AUDIT",
    "IMPROVE",
    "VALIDATE",
    "SIMULATE",
    "RESEARCH",
    "PERFORMANCE_REVIEW",
    "STRATEGY_IMPROVEMENT",
    "SETUP_ANALYSIS",
    "EVIDENCE_PACK",
    "DASHBOARD",
    "HEALTH_CHECK",
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
    "missing_journal_source",
    "missing_review_evidence",
    "malformed_performance_input",
    "performance_review_without_journal_entries",
    "improvement_suggestion_without_evidence",
    "unsafe_export_path",
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
        "review_only": True,
        "performance_review_only": True,
        "strategy_improvement_only": True,
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
        "setup_types": SETUP_TYPES,
        "improvement_suggestions": IMPROVEMENT_SUGGESTIONS,
        "quality_grades": QUALITY_GRADES,
        "performance_dimensions": PERFORMANCE_DIMENSIONS,
        "forbidden_performance_actions": FORBIDDEN_PERFORMANCE_ACTIONS,
        "allowed_performance_actions": ALLOWED_PERFORMANCE_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.0'."""
    return VERSION == "1.9.0"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_setup_types() -> list:
    """Return list of supported setup types."""
    return list(SETUP_TYPES)


def get_improvement_suggestions() -> list:
    """Return list of improvement suggestion types."""
    return list(IMPROVEMENT_SUGGESTIONS)


def get_quality_grades() -> list:
    """Return list of quality grades."""
    return list(QUALITY_GRADES)


def get_performance_dimensions() -> list:
    """Return list of performance dimensions."""
    return list(PERFORMANCE_DIMENSIONS)


def get_forbidden_performance_actions() -> list:
    """Return list of forbidden performance actions."""
    return list(FORBIDDEN_PERFORMANCE_ACTIONS)


def get_allowed_performance_actions() -> list:
    """Return list of allowed performance actions."""
    return list(ALLOWED_PERFORMANCE_ACTIONS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
