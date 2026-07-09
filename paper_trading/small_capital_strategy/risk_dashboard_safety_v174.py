"""
paper_trading/small_capital_strategy/risk_dashboard_safety_v174.py
Safety flags for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

# Positive safety flags (capabilities = True)
SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE          = True
SMALL_ACCOUNT_RISK_DASHBOARD_RESEARCH_ONLY      = True
SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY         = True
SMALL_ACCOUNT_RISK_DASHBOARD_READ_ONLY          = True
SMALL_ACCOUNT_RISK_DASHBOARD_DETERMINISTIC      = True
SMALL_ACCOUNT_RISK_DASHBOARD_NOT_INVESTMENT_ADVICE = True

# Negative safety flags (dangerous capabilities = False)
SMALL_ACCOUNT_RISK_REAL_TRADING_ENABLED         = False
SMALL_ACCOUNT_RISK_REAL_ACCOUNT_ENABLED         = False
SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED           = False
SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED     = False
SMALL_ACCOUNT_RISK_PRODUCTION_TRADING_ENABLED   = False
SMALL_ACCOUNT_RISK_LIVE_EXECUTION_ENABLED       = False
SMALL_ACCOUNT_RISK_AUTO_ORDER_ENABLED           = False
SMALL_ACCOUNT_RISK_AUTO_STOP_LOSS_ENABLED       = False
SMALL_ACCOUNT_RISK_AUTO_TAKE_PROFIT_ENABLED     = False
SMALL_ACCOUNT_RISK_MARGIN_ENABLED               = False

# Canonical safety aliases
NO_REAL_ORDERS             = True
BROKER_EXECUTION_ENABLED   = False
PRODUCTION_TRADING_BLOCKED = True

_MUST_BE_FALSE = [
    "SMALL_ACCOUNT_RISK_REAL_TRADING_ENABLED",
    "SMALL_ACCOUNT_RISK_REAL_ACCOUNT_ENABLED",
    "SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED",
    "SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED",
    "SMALL_ACCOUNT_RISK_PRODUCTION_TRADING_ENABLED",
    "SMALL_ACCOUNT_RISK_LIVE_EXECUTION_ENABLED",
    "SMALL_ACCOUNT_RISK_AUTO_ORDER_ENABLED",
    "SMALL_ACCOUNT_RISK_AUTO_STOP_LOSS_ENABLED",
    "SMALL_ACCOUNT_RISK_AUTO_TAKE_PROFIT_ENABLED",
    "SMALL_ACCOUNT_RISK_MARGIN_ENABLED",
    "BROKER_EXECUTION_ENABLED",
]

_MUST_BE_TRUE = [
    "SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE",
    "SMALL_ACCOUNT_RISK_DASHBOARD_RESEARCH_ONLY",
    "SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY",
    "SMALL_ACCOUNT_RISK_DASHBOARD_NOT_INVESTMENT_ADVICE",
    "NO_REAL_ORDERS",
    "PRODUCTION_TRADING_BLOCKED",
]


def get_risk_dashboard_safety_flags() -> Dict[str, Any]:
    """Return all risk dashboard safety flags as a dict."""
    return {
        "SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE": SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE,
        "SMALL_ACCOUNT_RISK_DASHBOARD_RESEARCH_ONLY": SMALL_ACCOUNT_RISK_DASHBOARD_RESEARCH_ONLY,
        "SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY": SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY,
        "SMALL_ACCOUNT_RISK_DASHBOARD_READ_ONLY": SMALL_ACCOUNT_RISK_DASHBOARD_READ_ONLY,
        "SMALL_ACCOUNT_RISK_DASHBOARD_DETERMINISTIC": SMALL_ACCOUNT_RISK_DASHBOARD_DETERMINISTIC,
        "SMALL_ACCOUNT_RISK_DASHBOARD_NOT_INVESTMENT_ADVICE": SMALL_ACCOUNT_RISK_DASHBOARD_NOT_INVESTMENT_ADVICE,
        "SMALL_ACCOUNT_RISK_REAL_TRADING_ENABLED": SMALL_ACCOUNT_RISK_REAL_TRADING_ENABLED,
        "SMALL_ACCOUNT_RISK_REAL_ACCOUNT_ENABLED": SMALL_ACCOUNT_RISK_REAL_ACCOUNT_ENABLED,
        "SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED": SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED,
        "SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED": SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED,
        "SMALL_ACCOUNT_RISK_PRODUCTION_TRADING_ENABLED": SMALL_ACCOUNT_RISK_PRODUCTION_TRADING_ENABLED,
        "SMALL_ACCOUNT_RISK_LIVE_EXECUTION_ENABLED": SMALL_ACCOUNT_RISK_LIVE_EXECUTION_ENABLED,
        "SMALL_ACCOUNT_RISK_AUTO_ORDER_ENABLED": SMALL_ACCOUNT_RISK_AUTO_ORDER_ENABLED,
        "SMALL_ACCOUNT_RISK_AUTO_STOP_LOSS_ENABLED": SMALL_ACCOUNT_RISK_AUTO_STOP_LOSS_ENABLED,
        "SMALL_ACCOUNT_RISK_AUTO_TAKE_PROFIT_ENABLED": SMALL_ACCOUNT_RISK_AUTO_TAKE_PROFIT_ENABLED,
        "SMALL_ACCOUNT_RISK_MARGIN_ENABLED": SMALL_ACCOUNT_RISK_MARGIN_ENABLED,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def audit_risk_dashboard_safety() -> Dict[str, Any]:
    """Run risk dashboard safety audit. Returns {all_safe, safety_capabilities, issues}."""
    flags = get_risk_dashboard_safety_flags()
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


def assert_risk_dashboard_safe() -> None:
    """Assert all risk dashboard safety invariants. Raises AssertionError on violation."""
    result = audit_risk_dashboard_safety()
    if not result["all_safe"]:
        raise AssertionError(f"Risk dashboard safety violation: {result['issues']}")
