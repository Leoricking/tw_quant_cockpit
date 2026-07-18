"""
paper_trading/small_capital_strategy/strategy_monitoring_safety_v194.py
Safety flags and audit for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List


SAFETY_FLAGS: Dict[str, bool] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "monitoring_only": True,
    "drift_detection_only": True,
    "rollback_trigger_only": True,
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
    "requires_manual_review": True,
    "no_auto_rollback": True,
    "broker_execution": False,
    "real_order": False,
    "live_trade": False,
    "margin_enabled": False,
    "leverage_enabled": False,
    "production_db_write": False,
    "production_strategy_mutation": False,
    "live_strategy_activation": False,
    "auto_rollback": False,
    "production_trading": False,
    "margin_trading": False,
    "leverage_trading": False,
    "live_broker_connection": False,
}

FORBIDDEN_MONITORING_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

ALLOWED_MONITORING_ACTIONS = frozenset({
    "REVIEW", "MONITOR", "DRIFT_CHECK", "ROLLBACK_ALERT",
    "ANALYZE", "REPORT", "EXPORT", "AUDIT", "VALIDATE", "SIMULATE",
    "RESEARCH", "RECOMMEND", "EVIDENCE_PACK", "DASHBOARD",
    "HEALTH_CHECK", "SAFETY_AUDIT",
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
    "missing_promotion_package_source",
    "missing_rollback_plan_source",
    "missing_baseline_monitoring_snapshot",
    "missing_current_monitoring_snapshot",
    "missing_monitoring_window",
    "missing_evidence",
    "malformed_monitoring_input",
    "unsafe_export_path",
    "forbidden_action_words",
    "auto_rollback_attempted",
]

_UNSAFE_PATH_TOKENS = [
    "production_db", "prod_db", "live_db", "real_db",
    "broker", "live_orders", "real_orders", "execution",
    "margin_account", "leverage_account", "production_strategy",
    "live_strategy", "live_trading",
]

_FORBIDDEN_WORDS = list(FORBIDDEN_MONITORING_ACTIONS)


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
    if not SAFETY_FLAGS.get("monitoring_only"):
        violations.append("monitoring_only_false")
    if not SAFETY_FLAGS.get("drift_detection_only"):
        violations.append("drift_detection_only_false")
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
    return {
        "all_safe": len(violations) == 0,
        "violations": violations,
        "paper_only": True,
        "research_only": True,
        "monitoring_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "schema_version": "194",
    }


def is_safe_output_path(path: str) -> bool:
    """Return True if path does not contain unsafe tokens."""
    lower = path.lower()
    return not any(tok in lower for tok in _UNSAFE_PATH_TOKENS)


def is_forbidden_action(action: str) -> bool:
    """Return True if action is in FORBIDDEN_MONITORING_ACTIONS."""
    return action.upper() in FORBIDDEN_MONITORING_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if action is in ALLOWED_MONITORING_ACTIONS."""
    return action.upper() in ALLOWED_MONITORING_ACTIONS


def validate_monitoring_action(action: str) -> Dict[str, object]:
    """Validate a monitoring action string."""
    if is_forbidden_action(action):
        return {
            "valid": False,
            "blocked": True,
            "reason": f"forbidden:{action.upper()}",
            "paper_only": True,
            "no_real_orders": True,
            "schema_version": "194",
        }
    if is_allowed_action(action):
        return {
            "valid": True,
            "blocked": False,
            "reason": "allowed",
            "paper_only": True,
            "no_real_orders": True,
            "schema_version": "194",
        }
    return {
        "valid": False,
        "blocked": False,
        "reason": f"unknown:{action.upper()}",
        "paper_only": True,
        "no_real_orders": True,
        "schema_version": "194",
    }


def has_forbidden_words(text: str) -> bool:
    """Return True if text contains any forbidden action words."""
    upper = text.upper()
    return any(word in upper for word in _FORBIDDEN_WORDS)


def validate_monitoring_input_safe(inp: Dict[str, object]) -> Dict[str, object]:
    """Validate that a monitoring input dict has required safety flags."""
    required = [
        "paper_only", "no_real_orders", "no_broker",
        "not_investment_advice", "monitoring_only",
    ]
    missing = [k for k in required if not inp.get(k)]
    blocked = len(missing) > 0
    return {
        "valid": not blocked,
        "blocked": blocked,
        "block_reasons": [f"missing_{m}" for m in missing],
        "paper_only": True,
        "monitoring_only": True,
        "no_real_orders": True,
        "schema_version": "194",
    }
