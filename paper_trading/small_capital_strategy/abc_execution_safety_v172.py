"""
paper_trading/small_capital_strategy/abc_execution_safety_v172.py
Safety flags for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

# Positive safety flags (capabilities = True)
ABC_EXECUTION_PLAN_AVAILABLE          = True
ABC_EXECUTION_PLAN_RESEARCH_ONLY      = True
ABC_EXECUTION_PLAN_PAPER_ONLY         = True
ABC_EXECUTION_PLAN_READ_ONLY          = True
ABC_EXECUTION_PLAN_DETERMINISTIC      = True
ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE = True

# Negative safety flags (dangerous capabilities = False)
ABC_REAL_TRADING_ENABLED              = False
ABC_REAL_ACCOUNT_ENABLED              = False
ABC_REAL_ORDER_ENABLED                = False
ABC_BROKER_EXECUTION_ENABLED          = False
ABC_PRODUCTION_TRADING_ENABLED        = False
ABC_LIVE_EXECUTION_ENABLED            = False
ABC_AUTO_ORDER_ENABLED                = False
ABC_AUTO_STOP_LOSS_ENABLED            = False
ABC_AUTO_TAKE_PROFIT_ENABLED          = False
ABC_MARGIN_ENABLED                    = False
ABC_DAY_TRADING_PRIMARY_ENABLED       = False

# Canonical safety aliases
NO_REAL_ORDERS              = True
BROKER_EXECUTION_ENABLED    = False
PRODUCTION_TRADING_BLOCKED  = True

_MUST_BE_FALSE = [
    "ABC_REAL_TRADING_ENABLED",
    "ABC_REAL_ACCOUNT_ENABLED",
    "ABC_REAL_ORDER_ENABLED",
    "ABC_BROKER_EXECUTION_ENABLED",
    "ABC_PRODUCTION_TRADING_ENABLED",
    "ABC_LIVE_EXECUTION_ENABLED",
    "ABC_AUTO_ORDER_ENABLED",
    "ABC_AUTO_STOP_LOSS_ENABLED",
    "ABC_AUTO_TAKE_PROFIT_ENABLED",
    "ABC_MARGIN_ENABLED",
    "ABC_DAY_TRADING_PRIMARY_ENABLED",
    "BROKER_EXECUTION_ENABLED",
]

_MUST_BE_TRUE = [
    "ABC_EXECUTION_PLAN_AVAILABLE",
    "ABC_EXECUTION_PLAN_RESEARCH_ONLY",
    "ABC_EXECUTION_PLAN_PAPER_ONLY",
    "ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE",
    "NO_REAL_ORDERS",
    "PRODUCTION_TRADING_BLOCKED",
]


def get_abc_safety_flags() -> Dict[str, Any]:
    """Return all ABC safety flags as a dict."""
    return {
        "ABC_EXECUTION_PLAN_AVAILABLE": ABC_EXECUTION_PLAN_AVAILABLE,
        "ABC_EXECUTION_PLAN_RESEARCH_ONLY": ABC_EXECUTION_PLAN_RESEARCH_ONLY,
        "ABC_EXECUTION_PLAN_PAPER_ONLY": ABC_EXECUTION_PLAN_PAPER_ONLY,
        "ABC_EXECUTION_PLAN_READ_ONLY": ABC_EXECUTION_PLAN_READ_ONLY,
        "ABC_EXECUTION_PLAN_DETERMINISTIC": ABC_EXECUTION_PLAN_DETERMINISTIC,
        "ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE": ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE,
        "ABC_REAL_TRADING_ENABLED": ABC_REAL_TRADING_ENABLED,
        "ABC_REAL_ACCOUNT_ENABLED": ABC_REAL_ACCOUNT_ENABLED,
        "ABC_REAL_ORDER_ENABLED": ABC_REAL_ORDER_ENABLED,
        "ABC_BROKER_EXECUTION_ENABLED": ABC_BROKER_EXECUTION_ENABLED,
        "ABC_PRODUCTION_TRADING_ENABLED": ABC_PRODUCTION_TRADING_ENABLED,
        "ABC_LIVE_EXECUTION_ENABLED": ABC_LIVE_EXECUTION_ENABLED,
        "ABC_AUTO_ORDER_ENABLED": ABC_AUTO_ORDER_ENABLED,
        "ABC_AUTO_STOP_LOSS_ENABLED": ABC_AUTO_STOP_LOSS_ENABLED,
        "ABC_AUTO_TAKE_PROFIT_ENABLED": ABC_AUTO_TAKE_PROFIT_ENABLED,
        "ABC_MARGIN_ENABLED": ABC_MARGIN_ENABLED,
        "ABC_DAY_TRADING_PRIMARY_ENABLED": ABC_DAY_TRADING_PRIMARY_ENABLED,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def audit_abc_safety() -> Dict[str, Any]:
    """Run ABC safety audit. Returns {all_safe, safety_capabilities, issues}."""
    flags = get_abc_safety_flags()
    issues = []

    for key in _MUST_BE_FALSE:
        if flags.get(key) is not False:
            issues.append(f"{key} must be False, got {flags.get(key)!r}")

    for key in _MUST_BE_TRUE:
        if flags.get(key) is not True:
            issues.append(f"{key} must be True, got {flags.get(key)!r}")

    dangerous_enabled = [k for k in _MUST_BE_FALSE if flags.get(k) is not False]
    safety_capabilities = len(dangerous_enabled)

    return {
        "all_safe": len(issues) == 0,
        "safety_capabilities": safety_capabilities,
        "issues": issues,
        "flags": flags,
    }


def assert_abc_safe() -> None:
    """Assert all ABC safety invariants. Raises AssertionError on violation."""
    result = audit_abc_safety()
    if not result["all_safe"]:
        raise AssertionError(f"ABC safety violation: {result['issues']}")
