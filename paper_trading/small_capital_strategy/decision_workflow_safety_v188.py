"""
paper_trading/small_capital_strategy/decision_workflow_safety_v188.py
Safety flags and audit for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List


SAFETY_FLAGS: Dict[str, bool] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "decision_only": True,
    "workflow_only": True,
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
    "broker_execution": False,
    "real_order": False,
    "live_trade": False,
    "margin_enabled": False,
    "leverage_enabled": False,
    "production_db_write": False,
}

FORBIDDEN_WORKFLOW_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_WORKFLOW_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "ALLOCATION_ONLY", "PORTFOLIO_ONLY", "DECISION_ONLY", "REPORT_ONLY",
    "AUDIT_ONLY", "WORKFLOW_ONLY",
})

HARD_BLOCK_CONDITIONS: List[str] = [
    "real_order_requested",
    "broker_requested",
    "margin_requested",
    "leverage_requested",
    "production_db_write_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_workflow_audit_trail",
    "missing_evidence_pack",
    "missing_decision_report",
    "malformed_workflow_input",
    "inconsistent_candidate_count",
    "blocked_candidate_without_reason",
    "paper_entry_candidate_without_evidence",
    "reduce_risk_candidate_without_risk_evidence",
    "unsafe_export_path",
    "non_deterministic_timestamp_without_policy",
    "workflow_step_failed_without_block_reason",
    "report_outputs_forbidden_words",
]

_UNSAFE_PATH_TOKENS = [
    "production_db", "prod_db", "live_db", "real_db",
    "broker", "live_orders", "real_orders", "execution",
    "margin_account", "leverage_account",
]


def run_safety_audit() -> Dict[str, object]:
    """Run full safety audit. Returns dict with all_safe=True if clean."""
    errors: List[str] = []
    for key, expected in SAFETY_FLAGS.items():
        val = SAFETY_FLAGS.get(key)
        if val != expected:
            errors.append(f"safety_flag_mismatch: {key}={val} expected={expected}")
    return {
        "all_safe": len(errors) == 0,
        "errors": errors,
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


def is_safe_output_path(path: str) -> bool:
    """Return True if export path is safe (not production DB or broker path)."""
    p = path.lower()
    for token in _UNSAFE_PATH_TOKENS:
        if token in p:
            return False
    return True


def is_forbidden_action(action: str) -> bool:
    """Return True if action is in FORBIDDEN_WORKFLOW_ACTIONS."""
    return action in FORBIDDEN_WORKFLOW_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if action is in ALLOWED_WORKFLOW_ACTIONS."""
    return action in ALLOWED_WORKFLOW_ACTIONS


def validate_workflow_action(action: str) -> bool:
    """Return True if action is allowed and not forbidden."""
    return is_allowed_action(action) and not is_forbidden_action(action)


def get_safety_flags() -> Dict[str, bool]:
    """Return copy of safety flags."""
    return dict(SAFETY_FLAGS)


def get_hard_block_conditions() -> List[str]:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)
