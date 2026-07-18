"""
paper_trading/small_capital_strategy/strategy_promotion_version_v193.py
Version metadata for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.3"
RELEASE_NAME = "Paper Strategy Promotion Package & Rollback Plan Lab"
BASE_RELEASE = "v1.9.2-paper-strategy-rule-sandbox-shadow-validation-lab"
SCHEMA_VERSION = "193"
POLICY_VERSION = "1.9.3-small-capital-strategy-paper-strategy-promotion-package-rollback-plan-lab"

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
]

PROMOTION_APPROVAL_STATES = [
    "DRAFT",
    "SHADOW_ONLY",
    "PAPER_PROMOTION_READY",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "REGRESSION_DETECTED",
    "ROLLBACK_REQUIRED",
    "INVALID",
]

PROMOTION_RECOMMENDATIONS = [
    "KEEP_BASELINE",
    "PROMOTE_TO_PAPER_PACKAGE",
    "KEEP_SHADOW_ONLY",
    "REQUIRE_MORE_DATA",
    "REQUIRE_MANUAL_REVIEW",
    "BLOCK_CANDIDATE",
    "ROLLBACK_TO_BASELINE",
    "SPLIT_PACKAGE",
    "TIGHTEN_ROLLBACK_TRIGGER",
    "ADD_MONITORING_RULE",
    "NO_CHANGE",
]

ROLLBACK_TRIGGERS = [
    "WIN_RATE_DETERIORATION",
    "EXPECTANCY_DETERIORATION",
    "DRAWDOWN_INCREASED",
    "PROFIT_FACTOR_DETERIORATION",
    "MISTAKE_RATE_INCREASED",
    "SIGNAL_COUNT_COLLAPSE",
    "OPPORTUNITY_LOSS_TOO_HIGH",
    "GUARDRAIL_FALSE_POSITIVE_TOO_HIGH",
    "BLOCKED_CONDITION_BREACH",
    "EVIDENCE_MISSING",
    "MANUAL_REVIEW_FAILED",
    "SAFETY_FLAG_MISSING",
]

FORBIDDEN_PROMOTION_ACTIONS = [
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

ALLOWED_PROMOTION_ACTIONS = [
    "REVIEW",
    "PROMOTION_BUILD",
    "PROMOTION_REVIEW",
    "ROLLBACK_PLAN",
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
    "missing_sandbox_validation_source",
    "missing_shadow_comparison_source",
    "missing_rollback_plan",
    "missing_evidence",
    "malformed_promotion_input",
    "promotion_package_without_approval_checklist",
    "candidate_rule_without_validation_evidence",
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
        "promotion_package_only": True,
        "rollback_plan_only": True,
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
        "promotion_approval_states": PROMOTION_APPROVAL_STATES,
        "promotion_recommendations": PROMOTION_RECOMMENDATIONS,
        "rollback_triggers": ROLLBACK_TRIGGERS,
        "forbidden_promotion_actions": FORBIDDEN_PROMOTION_ACTIONS,
        "allowed_promotion_actions": ALLOWED_PROMOTION_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.3'."""
    return VERSION == "1.9.3"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_promotion_approval_states() -> list:
    """Return list of promotion approval states."""
    return list(PROMOTION_APPROVAL_STATES)


def get_promotion_recommendations() -> list:
    """Return list of promotion recommendations."""
    return list(PROMOTION_RECOMMENDATIONS)


def get_rollback_triggers() -> list:
    """Return list of rollback triggers."""
    return list(ROLLBACK_TRIGGERS)


def get_forbidden_promotion_actions() -> list:
    """Return list of forbidden promotion actions."""
    return list(FORBIDDEN_PROMOTION_ACTIONS)


def get_allowed_promotion_actions() -> list:
    """Return list of allowed promotion actions."""
    return list(ALLOWED_PROMOTION_ACTIONS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
