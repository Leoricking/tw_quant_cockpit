"""
paper_trading/small_capital_strategy/integrated_strategy_safety_v178.py
Safety flags for Small Capital Strategy Integration v1.7.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"

INTEGRATED_STRATEGY_AVAILABLE           = True
INTEGRATED_STRATEGY_RESEARCH_ONLY       = True
INTEGRATED_STRATEGY_PAPER_ONLY          = True
INTEGRATED_STRATEGY_READ_ONLY           = True
INTEGRATED_STRATEGY_DETERMINISTIC       = True
INTEGRATED_STRATEGY_NOT_INVESTMENT_ADVICE = True

real_trading            = False
real_account            = False
real_order              = False
broker_execution        = False
production_trading_blocked = True

SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only":                  True,
    "research_only":               True,
    "no_real_orders":              True,
    "no_broker":                   True,
    "not_investment_advice":       True,
    "production_trading_blocked":  True,
    "real_trading":                False,
    "real_account":                False,
    "real_order":                  False,
    "broker_execution":            False,
    "no_margin":                   True,
    "no_leverage":                 True,
    "no_production_db_writes":     True,
    "deterministic":               True,
    "demo_only":                   True,
    "not_for_production":          True,
}


def get_safety_flags() -> Dict[str, Any]:
    """Return copy of safety flags."""
    return dict(SAFETY_FLAGS)


def run_safety_audit() -> Dict[str, Any]:
    """Run safety audit. Returns {all_safe, issues, flags}."""
    issues: List[str] = []
    if SAFETY_FLAGS["real_trading"]:
        issues.append("real_trading must be False")
    if SAFETY_FLAGS["real_account"]:
        issues.append("real_account must be False")
    if SAFETY_FLAGS["real_order"]:
        issues.append("real_order must be False")
    if SAFETY_FLAGS["broker_execution"]:
        issues.append("broker_execution must be False")
    if not SAFETY_FLAGS["paper_only"]:
        issues.append("paper_only must be True")
    if not SAFETY_FLAGS["research_only"]:
        issues.append("research_only must be True")
    if not SAFETY_FLAGS["no_real_orders"]:
        issues.append("no_real_orders must be True")
    if not SAFETY_FLAGS["production_trading_blocked"]:
        issues.append("production_trading_blocked must be True")
    if not SAFETY_FLAGS["no_margin"]:
        issues.append("no_margin must be True")
    if not SAFETY_FLAGS["no_production_db_writes"]:
        issues.append("no_production_db_writes must be True")
    return {
        "all_safe": len(issues) == 0,
        "issues": issues,
        "flags": dict(SAFETY_FLAGS),
    }


def assert_safe() -> None:
    """Assert all safety invariants. Raises AssertionError on violation."""
    audit = run_safety_audit()
    assert audit["all_safe"], f"Safety violation: {audit['issues']}"
