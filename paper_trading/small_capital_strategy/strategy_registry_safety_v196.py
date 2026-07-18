"""
paper_trading/small_capital_strategy/strategy_registry_safety_v196.py
Safety flags and audit for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, FrozenSet, List

SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "governance_only": True,
    "registry_only": True,
    "decision_record_only": True,
    "review_only": True,
    "report_only": True,
    "audit_only": True,
    "real_order": False,
    "broker_execution": False,
    "real_trading": False,
    "real_account": False,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_writes": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "auto_approval": False,
    "auto_decision": False,
    "auto_registry_mutation": False,
    "immutable_decision_record": True,
    "deterministic_registry": True,
}

FORBIDDEN_REGISTRY_ACTIONS: FrozenSet[str] = frozenset([
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
])

ALLOWED_REGISTRY_ACTIONS: FrozenSet[str] = frozenset([
    "REGISTRY_VERSION",
    "REGISTRY_RUN",
    "REGISTRY_RECORD",
    "REGISTRY_LIST",
    "REGISTRY_LINEAGE",
    "GOVERNANCE_CHECK",
    "REGISTRY_QUEUE",
    "REGISTRY_VALIDATE",
    "REGISTRY_REPORT",
    "REGISTRY_DASHBOARD",
    "REGISTRY_EXPORT",
    "EVIDENCE_PACK",
    "AUDIT_TRAIL",
    "HEALTH_CHECK",
    "RELEASE_GATE",
    "REGISTRY_SCENARIOS",
    "REGISTRY_FIXTURES",
    "SAFETY_AUDIT",
])

HARD_BLOCK_CONDITIONS: List[str] = [
    "real_order_requested",
    "broker_requested",
    "margin_or_leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_decision_id",
    "missing_decision_source",
    "missing_decision_lineage",
    "missing_decision_evidence",
    "missing_decision_rationale",
    "missing_governance_checklist",
    "duplicate_decision_id",
    "malformed_registry_input",
    "unsafe_export_path",
    "forbidden_action_words",
]

_FORBIDDEN_WORDS = frozenset(["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                               "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"])

_SAFE_PATH_PREFIXES = ("/tmp/", "C:/tmp/", "C:/Users/", "/home/", "./", "../",
                        "output/", "reports/", "exports/", "paper_")


def is_safe_output_path(path: str) -> bool:
    """Return True if the export path is safe (no production DB paths)."""
    if not path:
        return False
    danger = ("production", "prod_db", "live_db", "broker_", "/etc/", "C:/Windows/",
               "C:/Program Files/", "real_trade", "real_order")
    lower = path.lower()
    return not any(d in lower for d in danger)


def is_forbidden_action(action: str) -> bool:
    """Return True if action is in FORBIDDEN_REGISTRY_ACTIONS."""
    return action.upper() in FORBIDDEN_REGISTRY_ACTIONS


def is_allowed_action(action: str) -> bool:
    """Return True if action is in ALLOWED_REGISTRY_ACTIONS."""
    return action.upper() in ALLOWED_REGISTRY_ACTIONS


def validate_registry_action(action: str) -> Dict[str, Any]:
    """Validate a registry action. Returns dict with valid/blocked."""
    if is_forbidden_action(action):
        return {"valid": False, "blocked": True,
                "block_reason": f"forbidden_action: {action}",
                "paper_only": True, "no_real_orders": True}
    if is_allowed_action(action):
        return {"valid": True, "blocked": False, "action": action,
                "paper_only": True, "governance_only": True, "no_real_orders": True}
    return {"valid": False, "blocked": False,
            "block_reason": f"unknown_action: {action}",
            "paper_only": True, "no_real_orders": True}


def run_safety_audit() -> Dict[str, Any]:
    """Run a full safety audit. Returns dict with all_safe and details."""
    violations: List[str] = []

    if SAFETY_FLAGS.get("real_order") is not False:
        violations.append("real_order_flag_not_false")
    if SAFETY_FLAGS.get("broker_execution") is not False:
        violations.append("broker_execution_flag_not_false")
    if SAFETY_FLAGS.get("paper_only") is not True:
        violations.append("paper_only_flag_not_true")
    if SAFETY_FLAGS.get("no_real_orders") is not True:
        violations.append("no_real_orders_flag_not_true")
    if SAFETY_FLAGS.get("no_broker") is not True:
        violations.append("no_broker_flag_not_true")
    if SAFETY_FLAGS.get("not_investment_advice") is not True:
        violations.append("not_investment_advice_flag_not_true")
    if SAFETY_FLAGS.get("governance_only") is not True:
        violations.append("governance_only_flag_not_true")
    if SAFETY_FLAGS.get("registry_only") is not True:
        violations.append("registry_only_flag_not_true")
    if SAFETY_FLAGS.get("no_production_strategy_mutation") is not True:
        violations.append("no_production_strategy_mutation_not_true")
    if SAFETY_FLAGS.get("no_automatic_rollback") is not True:
        violations.append("no_automatic_rollback_not_true")
    if SAFETY_FLAGS.get("no_live_strategy_activation") is not True:
        violations.append("no_live_strategy_activation_not_true")
    if SAFETY_FLAGS.get("immutable_decision_record") is not True:
        violations.append("immutable_decision_record_not_true")
    if len(FORBIDDEN_REGISTRY_ACTIONS) < 9:
        violations.append("forbidden_actions_count_too_low")
    if len(ALLOWED_REGISTRY_ACTIONS) < 18:
        violations.append("allowed_actions_count_too_low")
    if len(HARD_BLOCK_CONDITIONS) < 20:
        violations.append("hard_block_conditions_count_too_low")

    return {
        "all_safe": len(violations) == 0,
        "violations": violations,
        "violation_count": len(violations),
        "paper_only": True,
        "governance_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "schema_version": "196",
    }


def assert_safe() -> None:
    """Raise AssertionError if any safety flag is violated."""
    result = run_safety_audit()
    assert result["all_safe"], f"Safety violations: {result['violations']}"
