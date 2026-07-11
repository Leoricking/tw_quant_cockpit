"""
paper_trading/small_capital_strategy/simulation_matrix_safety_v181.py
Safety flags for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "stress_test_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "production_trading_blocked": True,
    "real_trading": False,
    "real_account": False,
    "real_order": False,
    "broker_execution": False,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_writes": True,
    "deterministic": True,
    "demo_only": True,
    "not_for_production": True,
}

_MUST_BE_TRUE: List[str] = [
    "paper_only", "research_only", "simulate_only", "stress_test_only",
    "no_real_orders", "no_broker", "not_investment_advice",
    "production_trading_blocked", "no_margin", "no_leverage",
    "no_production_db_writes", "deterministic", "demo_only", "not_for_production",
]

_MUST_BE_FALSE: List[str] = [
    "real_trading", "real_account", "real_order", "broker_execution",
]


def get_safety_flags() -> Dict[str, Any]:
    """Return a copy of SAFETY_FLAGS."""
    return dict(SAFETY_FLAGS)


def run_safety_audit() -> Dict[str, Any]:
    """Run safety audit; return dict with all_safe bool and issues list."""
    issues: List[str] = []
    for key in _MUST_BE_TRUE:
        if not SAFETY_FLAGS.get(key):
            issues.append(f"{key} must be True but is {SAFETY_FLAGS.get(key)!r}")
    for key in _MUST_BE_FALSE:
        if SAFETY_FLAGS.get(key) is not False:
            issues.append(f"{key} must be False but is {SAFETY_FLAGS.get(key)!r}")
    return {
        "all_safe": len(issues) == 0,
        "issues": issues,
        "checked_true": list(_MUST_BE_TRUE),
        "checked_false": list(_MUST_BE_FALSE),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def assert_safe() -> None:
    """Raise RuntimeError if any safety flag is misconfigured."""
    result = run_safety_audit()
    if not result["all_safe"]:
        raise RuntimeError(f"Safety audit failed: {result['issues']}")
