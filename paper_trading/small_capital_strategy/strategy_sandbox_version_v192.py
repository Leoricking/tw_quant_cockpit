"""
paper_trading/small_capital_strategy/strategy_sandbox_version_v192.py
Version metadata for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.2"
RELEASE_NAME = "Paper Strategy Rule Sandbox & Shadow Validation Lab"
BASE_RELEASE = "v1.9.1-paper-strategy-rule-tuning-guardrail-lab"
SCHEMA_VERSION = "192"
POLICY_VERSION = "1.9.2-small-capital-strategy-paper-strategy-rule-sandbox-shadow-validation-lab"

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
]

SANDBOX_MODES = [
    "BASELINE_ONLY",
    "CANDIDATE_ONLY",
    "SHADOW_COMPARE",
    "A_B_RULE_COMPARE",
    "GUARDRAIL_COMPARE",
    "POSITION_SIZING_COMPARE",
    "CASH_RESERVE_COMPARE",
    "CONCENTRATION_LIMIT_COMPARE",
    "FULL_RULESET_COMPARE",
    "REGRESSION_ONLY",
    "SAFETY_ONLY",
]

VALIDATION_DIMENSIONS = [
    "signal_count_delta",
    "blocked_signal_delta",
    "win_rate_delta",
    "expectancy_delta_r",
    "average_gain_delta_r",
    "average_loss_delta_r",
    "profit_factor_delta",
    "max_drawdown_delta_r",
    "drawdown_budget_usage_delta_pct",
    "mistake_rate_delta",
    "chase_high_delta",
    "early_entry_delta",
    "over_concentration_delta",
    "low_cash_reserve_delta",
    "evidence_completeness_delta",
    "blocked_condition_respect_delta",
    "opportunity_loss_score",
    "risk_reduction_score",
    "rule_stability_score",
    "shadow_validation_score",
]

SANDBOX_APPROVAL_STATES = [
    "SHADOW_ONLY",
    "PAPER_APPROVED",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "REGRESSION_DETECTED",
    "INVALID",
]

SANDBOX_RECOMMENDATIONS = [
    "KEEP_BASELINE",
    "ACCEPT_CANDIDATE_FOR_PAPER",
    "KEEP_SHADOW_TESTING",
    "REJECT_CANDIDATE",
    "TIGHTEN_MORE",
    "LOOSEN_MORE",
    "REQUIRE_MORE_DATA",
    "REQUIRE_MANUAL_REVIEW",
    "ADD_GUARDRAIL",
    "REMOVE_CANDIDATE_GUARDRAIL",
    "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE",
    "NO_CHANGE",
]

FORBIDDEN_SANDBOX_ACTIONS = [
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

ALLOWED_SANDBOX_ACTIONS = [
    "REVIEW",
    "SANDBOX_RUN",
    "SHADOW_COMPARE",
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
    "missing_baseline_strategy_snapshot",
    "missing_candidate_strategy_snapshot",
    "missing_evidence",
    "malformed_sandbox_input",
    "candidate_rule_without_evidence",
    "unsafe_export_path",
    "forbidden_action_words",
]

MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 20
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
        "sandbox_only": True,
        "shadow_only": True,
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
        "sandbox_modes": SANDBOX_MODES,
        "validation_dimensions": VALIDATION_DIMENSIONS,
        "sandbox_approval_states": SANDBOX_APPROVAL_STATES,
        "sandbox_recommendations": SANDBOX_RECOMMENDATIONS,
        "forbidden_sandbox_actions": FORBIDDEN_SANDBOX_ACTIONS,
        "allowed_sandbox_actions": ALLOWED_SANDBOX_ACTIONS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.2'."""
    return VERSION == "1.9.2"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_sandbox_modes() -> list:
    """Return list of sandbox modes."""
    return list(SANDBOX_MODES)


def get_validation_dimensions() -> list:
    """Return list of validation dimensions."""
    return list(VALIDATION_DIMENSIONS)


def get_sandbox_approval_states() -> list:
    """Return list of sandbox approval states."""
    return list(SANDBOX_APPROVAL_STATES)


def get_sandbox_recommendations() -> list:
    """Return list of sandbox recommendations."""
    return list(SANDBOX_RECOMMENDATIONS)


def get_forbidden_sandbox_actions() -> list:
    """Return list of forbidden sandbox actions."""
    return list(FORBIDDEN_SANDBOX_ACTIONS)


def get_allowed_sandbox_actions() -> list:
    """Return list of allowed sandbox actions."""
    return list(ALLOWED_SANDBOX_ACTIONS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
