"""
paper_trading/small_capital_strategy/position_sizing_safety_v184.py
Safety flags for Position Sizing & Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

SAFETY_FLAGS = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "allocation_only": True,
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
    "allocation_only", "no_real_orders", "no_broker", "no_margin",
    "no_leverage", "no_auto_trade", "no_live_session", "no_production_db_writes",
    "not_investment_advice", "demo_only", "not_for_production",
    "production_trading_blocked",
]
_MUST_BE_FALSE = ["broker_execution", "real_order", "real_trading", "real_account"]


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
        "paper_only": True,
        "allocation_only": True,
        "schema_version": "184",
    }


def assert_safe() -> None:
    """Raise RuntimeError if any safety check fails."""
    audit = run_safety_audit()
    if not audit["all_safe"]:
        raise RuntimeError(f"Safety audit FAILED: {audit['violations']}")
