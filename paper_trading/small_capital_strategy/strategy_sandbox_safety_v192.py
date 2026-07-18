"""
paper_trading/small_capital_strategy/strategy_sandbox_safety_v192.py
Safety flags and audit for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List


SAFETY_FLAGS: Dict[str, bool] = {
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
    "broker_execution": False,
    "real_order": False,
    "live_trade": False,
    "margin_enabled": False,
    "leverage_enabled": False,
    "production_db_write": False,
    "production_strategy_mutation": False,
    "live_strategy_activation": False,
}

FORBIDDEN_SANDBOX_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_SANDBOX_ACTIONS = frozenset({
    "REVIEW", "SANDBOX_RUN", "SHADOW_COMPARE", "ANALYZE", "REPORT",
    "EXPORT", "AUDIT", "VALIDATE", "SIMULATE", "RESEARCH", "RECOMMEND",
    "GUARDRAIL_CHECK", "EVIDENCE_PACK", "DASHBOARD", "HEALTH_CHECK",
    "SAFETY_AUDIT",
})

HARD_BLOCK_CONDITIONS: List[str] = [
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

_UNSAFE_PATH_TOKENS = [
    "production_db", "prod_db", "live_db", "real_db",
    "broker", "live_orders", "real_orders", "execution",
    "margin_account", "leverage_account", "production_strategy",
    "live_strategy",
]

_FORBIDDEN_WORDS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]


def run_safety_audit() -> Dict[str, object]:
    """Run safety audit and return result dict."""
    issues = []
    positive_flags = [
        "paper_only", "research_only", "simulate_only", "validation_only",
        "sandbox_only", "shadow_only", "review_only", "report_only", "audit_only",
        "no_real_orders", "no_broker", "no_margin", "no_leverage",
        "no_production_strategy_mutation", "no_live_strategy_activation",
        "not_investment_advice", "demo_only", "not_for_production",
        "production_trading_blocked",
    ]
    for flag in positive_flags:
        if not SAFETY_FLAGS.get(flag, False):
            issues.append(f"safety_flag_{flag}_not_set")
    negative_flags = [
        "broker_execution", "real_order", "live_trade",
        "margin_enabled", "leverage_enabled", "production_db_write",
        "production_strategy_mutation", "live_strategy_activation",
    ]
    for flag in negative_flags:
        if SAFETY_FLAGS.get(flag, True) is not False:
            issues.append(f"negative_flag_{flag}_should_be_false")
    return {
        "all_safe": len(issues) == 0,
        "issues": issues,
        "paper_only": True,
        "research_only": True,
        "sandbox_only": True,
        "shadow_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_production_strategy_mutation": True,
        "no_live_strategy_activation": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "192",
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
    return action.upper() in FORBIDDEN_SANDBOX_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if the action is in the allowed set."""
    return action.upper() in ALLOWED_SANDBOX_ACTIONS


def validate_sandbox_action(action: str) -> Dict[str, object]:
    """Validate a sandbox action and return result."""
    upper = action.upper()
    if upper in FORBIDDEN_SANDBOX_ACTIONS:
        return {"valid": False, "blocked": True, "reason": f"forbidden_action:{upper}",
                "paper_only": True, "no_real_orders": True}
    if upper in ALLOWED_SANDBOX_ACTIONS:
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


def validate_sandbox_input_safe(
    sandbox_id: str,
    baseline_snapshot_id: str,
    candidate_snapshot_id: str,
) -> Dict[str, object]:
    """Validate a sandbox input for safety compliance."""
    errors = []
    if not sandbox_id:
        errors.append("missing_sandbox_id")
    if not baseline_snapshot_id:
        errors.append("missing_baseline_strategy_snapshot")
    if not candidate_snapshot_id:
        errors.append("missing_candidate_strategy_snapshot")
    if has_forbidden_words(sandbox_id):
        errors.append("forbidden_action_words")
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "paper_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "sandbox_only": True,
        "shadow_only": True,
        "no_production_strategy_mutation": True,
        "no_live_strategy_activation": True,
        "production_trading_blocked": True,
    }


def get_safety_flags() -> Dict[str, bool]:
    """Return copy of SAFETY_FLAGS."""
    return dict(SAFETY_FLAGS)


def get_hard_block_conditions() -> List[str]:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)


def get_forbidden_sandbox_actions() -> List[str]:
    """Return list of forbidden sandbox actions."""
    return list(FORBIDDEN_SANDBOX_ACTIONS)


def get_allowed_sandbox_actions() -> List[str]:
    """Return list of allowed sandbox actions."""
    return list(ALLOWED_SANDBOX_ACTIONS)
