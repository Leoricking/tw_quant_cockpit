"""
paper_trading/small_capital_strategy/strategy_review_safety_v195.py
Safety flags and audit for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List


SAFETY_FLAGS: Dict[str, bool] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "monitoring_review_only": True,
    "human_approval_only": True,
    "rollback_review_only": True,
    "review_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "requires_manual_review": True,
    "no_auto_approval": True,
    # negative flags
    "broker_execution": False,
    "real_order": False,
    "live_trade": False,
    "margin_enabled": False,
    "leverage_enabled": False,
    "production_db_write": False,
    "production_strategy_mutation": False,
    "live_strategy_activation": False,
    "auto_rollback": False,
    "auto_approval": False,
    "production_trading": False,
    "margin_trading": False,
    "leverage_trading": False,
    "live_broker_connection": False,
}

FORBIDDEN_REVIEW_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_REVIEW_ACTIONS = frozenset({
    "REVIEW", "MONITOR", "DRIFT_CHECK", "ROLLBACK_ALERT",
    "ANALYZE", "REPORT", "EXPORT", "AUDIT", "VALIDATE", "SIMULATE",
    "RESEARCH", "RECOMMEND", "EVIDENCE_PACK", "DASHBOARD",
    "HEALTH_CHECK", "SAFETY_AUDIT", "HUMAN_APPROVAL", "REVIEW_DECISION",
})

HARD_BLOCK_CONDITIONS: List[str] = [
    "real_order_requested",
    "broker_requested",
    "margin_requested",
    "leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_monitoring_alert_source",
    "missing_drift_detection_source",
    "missing_review_evidence",
    "missing_human_approval_checklist",
    "missing_decision_rationale",
    "malformed_review_input",
    "unsafe_export_path",
    "forbidden_action_words",
]

_UNSAFE_PATH_TOKENS = [
    "production_db", "prod_db", "live_db", "real_db",
    "broker", "live_orders", "real_orders", "execution",
    "margin_account", "leverage_account", "production_strategy",
    "live_strategy", "live_trading",
]

_FORBIDDEN_WORDS = list(FORBIDDEN_REVIEW_ACTIONS)


def run_safety_audit() -> Dict[str, object]:
    """Run full safety audit and return dict with all_safe flag."""
    violations = []
    if not SAFETY_FLAGS.get("paper_only"):
        violations.append("paper_only_false")
    if not SAFETY_FLAGS.get("no_real_orders"):
        violations.append("no_real_orders_false")
    if not SAFETY_FLAGS.get("no_broker"):
        violations.append("no_broker_false")
    if not SAFETY_FLAGS.get("not_investment_advice"):
        violations.append("not_investment_advice_false")
    if not SAFETY_FLAGS.get("review_only"):
        violations.append("review_only_false")
    if not SAFETY_FLAGS.get("human_approval_only"):
        violations.append("human_approval_only_false")
    if SAFETY_FLAGS.get("broker_execution"):
        violations.append("broker_execution_true")
    if SAFETY_FLAGS.get("real_order"):
        violations.append("real_order_true")
    if SAFETY_FLAGS.get("live_trade"):
        violations.append("live_trade_true")
    if SAFETY_FLAGS.get("production_db_write"):
        violations.append("production_db_write_true")
    if SAFETY_FLAGS.get("production_strategy_mutation"):
        violations.append("production_strategy_mutation_true")
    if SAFETY_FLAGS.get("live_strategy_activation"):
        violations.append("live_strategy_activation_true")
    if SAFETY_FLAGS.get("auto_approval"):
        violations.append("auto_approval_true")
    return {
        "all_safe": len(violations) == 0,
        "violations": violations,
        "paper_only": True,
        "research_only": True,
        "review_only": True,
        "human_approval_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "schema_version": "195",
    }


def is_safe_output_path(path: str) -> bool:
    """Return True if path does not contain unsafe tokens."""
    lower = path.lower()
    return not any(tok in lower for tok in _UNSAFE_PATH_TOKENS)


def is_forbidden_action(action: str) -> bool:
    """Return True if action is in FORBIDDEN_REVIEW_ACTIONS."""
    return action.upper() in FORBIDDEN_REVIEW_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if action is in ALLOWED_REVIEW_ACTIONS."""
    return action.upper() in ALLOWED_REVIEW_ACTIONS


def validate_review_action(action: str) -> Dict[str, object]:
    """Validate a review action string."""
    if is_forbidden_action(action):
        return {
            "valid": False,
            "blocked": True,
            "reason": f"forbidden:{action.upper()}",
            "paper_only": True,
            "no_real_orders": True,
            "schema_version": "195",
        }
    if is_allowed_action(action):
        return {
            "valid": True,
            "blocked": False,
            "reason": "allowed",
            "paper_only": True,
            "no_real_orders": True,
            "schema_version": "195",
        }
    return {
        "valid": False,
        "blocked": False,
        "reason": f"unknown:{action.upper()}",
        "paper_only": True,
        "no_real_orders": True,
        "schema_version": "195",
    }


def has_forbidden_words(text: str) -> bool:
    """Return True if text contains any forbidden action words."""
    upper = text.upper()
    return any(word in upper for word in _FORBIDDEN_WORDS)


def validate_review_input_safe(inp: Dict[str, object]) -> Dict[str, object]:
    """Validate that a review input dict has required safety flags."""
    required = [
        "paper_only", "no_real_orders", "no_broker",
        "not_investment_advice", "review_only",
    ]
    missing = [k for k in required if not inp.get(k)]
    blocked = len(missing) > 0
    return {
        "valid": not blocked,
        "blocked": blocked,
        "block_reasons": [f"missing_{m}" for m in missing],
        "paper_only": True,
        "review_only": True,
        "no_real_orders": True,
        "schema_version": "195",
    }
