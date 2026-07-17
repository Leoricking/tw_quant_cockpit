"""
paper_trading/small_capital_strategy/strategy_tuning_version_v191.py
Version metadata for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.1"
RELEASE_NAME = "Paper Strategy Rule Tuning & Guardrail Lab"
BASE_RELEASE = "v1.9.0-paper-trading-performance-review-strategy-improvement-lab"
SCHEMA_VERSION = "191"
POLICY_VERSION = "1.9.1-small-capital-strategy-paper-strategy-rule-tuning-guardrail-lab"

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
]

RULE_CATEGORIES = [
    "ABC_BUY_POINT",
    "SECOND_WAVE_ENTRY",
    "MARKET_REGIME_FILTER",
    "VOLUME_CONFIRMATION",
    "MOVING_AVERAGE_FILTER",
    "POSITION_SIZING",
    "CASH_RESERVE",
    "CONCENTRATION_LIMIT",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "REDUCE_RISK",
    "BLOCKED_CONDITION",
    "EVIDENCE_REQUIREMENT",
    "MANUAL_REVIEW",
]

GUARDRAIL_TRIGGERS = [
    "EXPECTANCY_NEGATIVE",
    "WIN_RATE_TOO_LOW",
    "AVERAGE_LOSS_TOO_HIGH",
    "DRAWDOWN_BUDGET_EXCEEDED",
    "MISTAKE_RATE_TOO_HIGH",
    "CHASE_HIGH_REPEATED",
    "EARLY_ENTRY_REPEATED",
    "OVER_CONCENTRATION_REPEATED",
    "LOW_CASH_RESERVE_REPEATED",
    "BLOCK_REASON_IGNORED",
    "EVIDENCE_MISSING_REPEATED",
    "MARKET_REGIME_MISMATCH",
    "VOLUME_CONFIRMATION_MISSING",
    "MA_BREAK_IGNORED",
    "NO_CLEAR_STOP",
    "NO_CLEAR_TAKE_PROFIT",
]

TUNING_RECOMMENDATIONS = [
    "KEEP_RULE",
    "TIGHTEN_RULE",
    "LOOSEN_RULE",
    "DISABLE_SETUP",
    "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE",
    "LOWER_CONCENTRATION_LIMIT",
    "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_MARKET_REGIME_CONFIRMATION",
    "REQUIRE_VOLUME_CONFIRMATION",
    "REQUIRE_MA_CONFIRMATION",
    "REQUIRE_MANUAL_REVIEW",
    "ADD_GUARDRAIL",
    "ESCALATE_TO_REVIEW",
    "NO_CHANGE",
]

APPROVAL_STATES = [
    "PROPOSED",
    "REVIEW_REQUIRED",
    "PAPER_APPROVED",
    "PAPER_REJECTED",
    "BLOCKED",
    "INVALID",
]

GUARDRAIL_SEVERITIES = [
    "INFO",
    "WARNING",
    "CRITICAL",
    "HARD_BLOCK",
]

GUARDRAIL_ACTIONS = [
    "LOG_ONLY",
    "REQUIRE_REVIEW",
    "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE",
    "DISABLE_SETUP",
    "HARD_BLOCK",
]

FORBIDDEN_TUNING_ACTIONS = [
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

ALLOWED_TUNING_ACTIONS = [
    "REVIEW",
    "TUNE",
    "ANALYZE",
    "REPORT",
    "EXPORT",
    "AUDIT",
    "VALIDATE",
    "SIMULATE",
    "RESEARCH",
    "RECOMMEND",
    "GUARDRAIL_CHECK",
    "EVIDENCE_PACK",
    "DASHBOARD",
    "HEALTH_CHECK",
    "RULE_TUNING",
    "GUARDRAIL_REVIEW",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_requested",
    "leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_performance_source",
    "missing_journal_source",
    "missing_evidence",
    "malformed_tuning_input",
    "rule_adjustment_without_evidence",
    "guardrail_without_trigger",
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
        "tuning_only": True,
        "guardrail_only": True,
        "review_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "no_production_strategy_mutation": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "rule_categories": RULE_CATEGORIES,
        "guardrail_triggers": GUARDRAIL_TRIGGERS,
        "tuning_recommendations": TUNING_RECOMMENDATIONS,
        "approval_states": APPROVAL_STATES,
        "forbidden_tuning_actions": FORBIDDEN_TUNING_ACTIONS,
        "allowed_tuning_actions": ALLOWED_TUNING_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.1'."""
    return VERSION == "1.9.1"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_rule_categories() -> list:
    """Return list of rule categories."""
    return list(RULE_CATEGORIES)


def get_guardrail_triggers() -> list:
    """Return list of guardrail triggers."""
    return list(GUARDRAIL_TRIGGERS)


def get_tuning_recommendations() -> list:
    """Return list of tuning recommendations."""
    return list(TUNING_RECOMMENDATIONS)


def get_approval_states() -> list:
    """Return list of approval states."""
    return list(APPROVAL_STATES)


def get_guardrail_severities() -> list:
    """Return list of guardrail severities."""
    return list(GUARDRAIL_SEVERITIES)


def get_guardrail_actions() -> list:
    """Return list of guardrail actions."""
    return list(GUARDRAIL_ACTIONS)


def get_forbidden_tuning_actions() -> list:
    """Return list of forbidden tuning actions."""
    return list(FORBIDDEN_TUNING_ACTIONS)


def get_allowed_tuning_actions() -> list:
    """Return list of allowed tuning actions."""
    return list(ALLOWED_TUNING_ACTIONS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
