"""
paper_trading/small_capital_strategy/decision_performance_safety_v190.py
Safety flags and audit for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List


SAFETY_FLAGS: Dict[str, bool] = {
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
    "broker_execution": False,
    "real_order": False,
    "live_trade": False,
    "margin_enabled": False,
    "leverage_enabled": False,
    "production_db_write": False,
}

FORBIDDEN_PERFORMANCE_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_PERFORMANCE_ACTIONS = frozenset({
    "REVIEW", "SUMMARIZE", "ANALYZE", "REPORT", "EXPORT", "AUDIT",
    "IMPROVE", "VALIDATE", "SIMULATE", "RESEARCH", "PERFORMANCE_REVIEW",
    "STRATEGY_IMPROVEMENT", "SETUP_ANALYSIS", "EVIDENCE_PACK",
    "DASHBOARD", "HEALTH_CHECK",
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
    "missing_journal_source",
    "missing_review_evidence",
    "malformed_performance_input",
    "performance_review_without_journal_entries",
    "improvement_suggestion_without_evidence",
    "unsafe_export_path",
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
    """Run safety audit and return result dict."""
    issues = []
    for flag, expected in SAFETY_FLAGS.items():
        if expected is True and not SAFETY_FLAGS.get(flag, False):
            issues.append(f"safety_flag_{flag}_not_set")
    negative_flags = ["broker_execution", "real_order", "live_trade", "margin_enabled",
                      "leverage_enabled", "production_db_write"]
    for flag in negative_flags:
        if SAFETY_FLAGS.get(flag, True) is not False:
            issues.append(f"negative_flag_{flag}_should_be_false")
    return {
        "all_safe": len(issues) == 0,
        "issues": issues,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "performance_review_only": True,
        "strategy_improvement_only": True,
        "production_trading_blocked": True,
        "schema_version": "190",
    }


def is_safe_output_path(path: str) -> bool:
    """Return True if the output path is safe for paper-only exports."""
    if not path:
        return False
    lower = path.lower()
    for token in _UNSAFE_PATH_TOKENS:
        if token in lower:
            return False
    return True


def is_forbidden_action(action: str) -> bool:
    """Return True if the action is in the forbidden set."""
    return action.upper() in FORBIDDEN_PERFORMANCE_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if the action is in the allowed set."""
    return action.upper() in ALLOWED_PERFORMANCE_ACTIONS


def validate_performance_action(action: str) -> Dict[str, object]:
    """Validate a performance action and return result."""
    upper = action.upper()
    if upper in FORBIDDEN_PERFORMANCE_ACTIONS:
        return {"valid": False, "blocked": True, "reason": f"forbidden_action:{upper}",
                "paper_only": True, "no_real_orders": True}
    if upper in ALLOWED_PERFORMANCE_ACTIONS:
        return {"valid": True, "blocked": False, "reason": "allowed",
                "paper_only": True, "no_real_orders": True}
    return {"valid": False, "blocked": False, "reason": f"unknown_action:{upper}",
            "paper_only": True, "no_real_orders": True}


def has_forbidden_words(text: str) -> bool:
    """Return True if text contains any forbidden action words."""
    upper = text.upper()
    for word in _FORBIDDEN_WORDS:
        if word in upper:
            return True
    return False


def validate_performance_input_safe(review_id: str, journal_entry_ids: list) -> Dict[str, object]:
    """Validate a performance review input for safety compliance."""
    errors = []
    if not review_id:
        errors.append("missing_review_id")
    if not journal_entry_ids:
        errors.append("performance_review_without_journal_entries")
    if has_forbidden_words(review_id):
        errors.append("forbidden_action_words")
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "paper_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "performance_review_only": True,
        "production_trading_blocked": True,
    }


def get_safety_flags() -> Dict[str, bool]:
    """Return copy of SAFETY_FLAGS."""
    return dict(SAFETY_FLAGS)


def get_hard_block_conditions() -> List[str]:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)


def get_forbidden_performance_actions() -> List[str]:
    """Return list of forbidden performance actions."""
    return list(FORBIDDEN_PERFORMANCE_ACTIONS)


def get_allowed_performance_actions() -> List[str]:
    """Return list of allowed performance actions."""
    return list(ALLOWED_PERFORMANCE_ACTIONS)
