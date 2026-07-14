"""
paper_trading/small_capital_strategy/decision_report_safety_v187.py
Safety flags for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

SAFETY_FLAGS = {
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
    "no_auto_trade": True,
    "no_live_session": True,
    "no_production_db_writes": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "broker_execution": False,
    "real_order": False,
    "real_trading": False,
    "real_account": False,
}

_MUST_BE_TRUE = [
    "paper_only", "research_only", "simulate_only", "validation_only",
    "decision_only", "report_only", "audit_only",
    "no_real_orders", "no_broker", "no_margin",
    "no_leverage", "no_auto_trade", "no_live_session", "no_production_db_writes",
    "not_investment_advice", "demo_only", "not_for_production",
    "production_trading_blocked",
]
_MUST_BE_FALSE = ["broker_execution", "real_order", "real_trading", "real_account"]

FORBIDDEN_REPORT_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_REPORT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "ALLOCATION_ONLY", "PORTFOLIO_ONLY", "DECISION_ONLY", "REPORT_ONLY", "AUDIT_ONLY",
})

UNSAFE_OUTPUT_PATHS = frozenset({
    "runtime_db", "production_db", "credentials", "tokens", "cache",
    "live_session", "broker_session", "real_account",
})

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_leverage_requested",
    "production_db_write_attempted",
    "report_outputs_buy_sell_order_execute",
    "missing_audit_trail",
    "missing_evidence_pack",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "non_deterministic_timestamp_without_policy",
    "unsafe_file_output_path",
    "malformed_decision_cockpit_input",
    "inconsistent_candidate_counts",
    "blocked_candidate_without_block_reason",
    "paper_entry_candidate_without_evidence",
    "reduce_risk_candidate_without_risk_evidence",
]


def get_safety_flags() -> dict:
    """Return copy of safety flags."""
    return dict(SAFETY_FLAGS)


def run_safety_audit() -> dict:
    """Run safety audit. Returns dict with all_safe, violations, etc."""
    violations = []
    for key in _MUST_BE_TRUE:
        if not SAFETY_FLAGS.get(key, False):
            violations.append(f"{key} must be True")
    for key in _MUST_BE_FALSE:
        if SAFETY_FLAGS.get(key, True):
            violations.append(f"{key} must be False")
    return {
        "all_safe": len(violations) == 0,
        "violations": violations,
        "issues": violations,
        "total_flags": len(SAFETY_FLAGS),
        "must_be_true_count": len(_MUST_BE_TRUE),
        "must_be_false_count": len(_MUST_BE_FALSE),
        "forbidden_actions_count": len(FORBIDDEN_REPORT_ACTIONS),
        "allowed_actions_count": len(ALLOWED_REPORT_ACTIONS),
        "hard_block_conditions_count": len(HARD_BLOCK_CONDITIONS),
        "paper_only": True,
        "report_only": True,
        "audit_only": True,
        "schema_version": "187",
    }


def assert_safe() -> None:
    """Raise RuntimeError if any safety check fails."""
    audit = run_safety_audit()
    if not audit["all_safe"]:
        raise RuntimeError(f"Safety audit FAILED: {audit['violations']}")


def is_safe_output_path(path: str) -> bool:
    """Return True if path is NOT in UNSAFE_OUTPUT_PATHS."""
    path_lower = path.lower()
    return not any(unsafe in path_lower for unsafe in UNSAFE_OUTPUT_PATHS)


def is_forbidden_action(action: str) -> bool:
    """Return True if action is in FORBIDDEN_REPORT_ACTIONS."""
    return action in FORBIDDEN_REPORT_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if action is in ALLOWED_REPORT_ACTIONS."""
    return action in ALLOWED_REPORT_ACTIONS


def validate_report_action(action: str) -> bool:
    """Return True if action is allowed and not forbidden."""
    return is_allowed_action(action) and not is_forbidden_action(action)
