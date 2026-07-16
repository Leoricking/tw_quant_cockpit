"""
paper_trading/small_capital_strategy/decision_journal_safety_v189.py
Safety flags and audit for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List


SAFETY_FLAGS: Dict[str, bool] = {
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
    "broker_execution": False,
    "real_order": False,
    "live_trade": False,
    "margin_enabled": False,
    "leverage_enabled": False,
    "production_db_write": False,
}

FORBIDDEN_JOURNAL_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_JOURNAL_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "SIMULATE_ONLY", "VALIDATION_ONLY", "DECISION_ONLY", "REPORT_ONLY",
    "WORKFLOW_ONLY", "AUDIT_ONLY",
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

_UNSAFE_PATH_TOKENS = [
    "production_db", "prod_db", "live_db", "real_db",
    "broker", "live_orders", "real_orders", "execution",
    "margin_account", "leverage_account",
]

_FORBIDDEN_WORDS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
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
        "journal_only": True,
        "review_only": True,
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
    """Return True if action is in FORBIDDEN_JOURNAL_ACTIONS."""
    return action in FORBIDDEN_JOURNAL_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if action is in ALLOWED_JOURNAL_ACTIONS."""
    return action in ALLOWED_JOURNAL_ACTIONS


def validate_journal_action(action: str) -> bool:
    """Return True if action is allowed and not forbidden."""
    return is_allowed_action(action) and not is_forbidden_action(action)


def has_forbidden_words(text: str) -> bool:
    """Return True if text contains any forbidden action words."""
    for word in _FORBIDDEN_WORDS:
        if word in text.upper():
            return True
    return False


def validate_journal_entry_safe(entry_dict: Dict[str, object]) -> bool:
    """Return True if journal entry dict has required safety flags set correctly."""
    required_true = [
        "paper_only", "no_real_orders", "no_broker", "not_investment_advice",
        "production_trading_blocked", "journal_only",
    ]
    for key in required_true:
        if not entry_dict.get(key, False):
            return False
    forbidden_keys = ["broker_execution", "real_order", "live_trade", "production_db_write"]
    for key in forbidden_keys:
        if entry_dict.get(key, False):
            return False
    return True


def get_safety_flags() -> Dict[str, bool]:
    """Return copy of safety flags."""
    return dict(SAFETY_FLAGS)


def get_hard_block_conditions() -> List[str]:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)


def get_forbidden_journal_actions() -> List[str]:
    """Return list of forbidden journal actions."""
    return sorted(FORBIDDEN_JOURNAL_ACTIONS)


def get_allowed_journal_actions() -> List[str]:
    """Return list of allowed journal actions."""
    return sorted(ALLOWED_JOURNAL_ACTIONS)
