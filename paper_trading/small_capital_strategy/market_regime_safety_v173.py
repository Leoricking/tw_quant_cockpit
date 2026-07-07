"""
paper_trading/small_capital_strategy/market_regime_safety_v173.py
Safety flags for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

# Positive safety flags (capabilities = True)
MARKET_REGIME_CONTROL_AVAILABLE          = True
MARKET_REGIME_CONTROL_RESEARCH_ONLY      = True
MARKET_REGIME_CONTROL_PAPER_ONLY         = True
MARKET_REGIME_CONTROL_READ_ONLY          = True
MARKET_REGIME_CONTROL_DETERMINISTIC      = True
MARKET_REGIME_CONTROL_NOT_INVESTMENT_ADVICE = True

# Negative safety flags (dangerous capabilities = False)
MARKET_REGIME_REAL_TRADING_ENABLED       = False
MARKET_REGIME_REAL_ACCOUNT_ENABLED       = False
MARKET_REGIME_REAL_ORDER_ENABLED         = False
MARKET_REGIME_BROKER_EXECUTION_ENABLED   = False
MARKET_REGIME_PRODUCTION_TRADING_ENABLED = False
MARKET_REGIME_LIVE_EXECUTION_ENABLED     = False
MARKET_REGIME_AUTO_ORDER_ENABLED         = False
MARKET_REGIME_AUTO_STOP_LOSS_ENABLED     = False
MARKET_REGIME_AUTO_TAKE_PROFIT_ENABLED   = False
MARKET_REGIME_MARGIN_ENABLED             = False

# Canonical safety aliases
NO_REAL_ORDERS             = True
BROKER_EXECUTION_ENABLED   = False
PRODUCTION_TRADING_BLOCKED = True

_MUST_BE_FALSE = [
    "MARKET_REGIME_REAL_TRADING_ENABLED",
    "MARKET_REGIME_REAL_ACCOUNT_ENABLED",
    "MARKET_REGIME_REAL_ORDER_ENABLED",
    "MARKET_REGIME_BROKER_EXECUTION_ENABLED",
    "MARKET_REGIME_PRODUCTION_TRADING_ENABLED",
    "MARKET_REGIME_LIVE_EXECUTION_ENABLED",
    "MARKET_REGIME_AUTO_ORDER_ENABLED",
    "MARKET_REGIME_AUTO_STOP_LOSS_ENABLED",
    "MARKET_REGIME_AUTO_TAKE_PROFIT_ENABLED",
    "MARKET_REGIME_MARGIN_ENABLED",
    "BROKER_EXECUTION_ENABLED",
]

_MUST_BE_TRUE = [
    "MARKET_REGIME_CONTROL_AVAILABLE",
    "MARKET_REGIME_CONTROL_RESEARCH_ONLY",
    "MARKET_REGIME_CONTROL_PAPER_ONLY",
    "MARKET_REGIME_CONTROL_NOT_INVESTMENT_ADVICE",
    "NO_REAL_ORDERS",
    "PRODUCTION_TRADING_BLOCKED",
]


def get_market_regime_safety_flags() -> Dict[str, Any]:
    """Return all market regime safety flags as a dict."""
    return {
        "MARKET_REGIME_CONTROL_AVAILABLE": MARKET_REGIME_CONTROL_AVAILABLE,
        "MARKET_REGIME_CONTROL_RESEARCH_ONLY": MARKET_REGIME_CONTROL_RESEARCH_ONLY,
        "MARKET_REGIME_CONTROL_PAPER_ONLY": MARKET_REGIME_CONTROL_PAPER_ONLY,
        "MARKET_REGIME_CONTROL_READ_ONLY": MARKET_REGIME_CONTROL_READ_ONLY,
        "MARKET_REGIME_CONTROL_DETERMINISTIC": MARKET_REGIME_CONTROL_DETERMINISTIC,
        "MARKET_REGIME_CONTROL_NOT_INVESTMENT_ADVICE": MARKET_REGIME_CONTROL_NOT_INVESTMENT_ADVICE,
        "MARKET_REGIME_REAL_TRADING_ENABLED": MARKET_REGIME_REAL_TRADING_ENABLED,
        "MARKET_REGIME_REAL_ACCOUNT_ENABLED": MARKET_REGIME_REAL_ACCOUNT_ENABLED,
        "MARKET_REGIME_REAL_ORDER_ENABLED": MARKET_REGIME_REAL_ORDER_ENABLED,
        "MARKET_REGIME_BROKER_EXECUTION_ENABLED": MARKET_REGIME_BROKER_EXECUTION_ENABLED,
        "MARKET_REGIME_PRODUCTION_TRADING_ENABLED": MARKET_REGIME_PRODUCTION_TRADING_ENABLED,
        "MARKET_REGIME_LIVE_EXECUTION_ENABLED": MARKET_REGIME_LIVE_EXECUTION_ENABLED,
        "MARKET_REGIME_AUTO_ORDER_ENABLED": MARKET_REGIME_AUTO_ORDER_ENABLED,
        "MARKET_REGIME_AUTO_STOP_LOSS_ENABLED": MARKET_REGIME_AUTO_STOP_LOSS_ENABLED,
        "MARKET_REGIME_AUTO_TAKE_PROFIT_ENABLED": MARKET_REGIME_AUTO_TAKE_PROFIT_ENABLED,
        "MARKET_REGIME_MARGIN_ENABLED": MARKET_REGIME_MARGIN_ENABLED,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def audit_market_regime_safety() -> Dict[str, Any]:
    """Run market regime safety audit. Returns {all_safe, safety_capabilities, issues}."""
    flags = get_market_regime_safety_flags()
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


def assert_market_regime_safe() -> None:
    """Assert all market regime safety invariants. Raises AssertionError on violation."""
    result = audit_market_regime_safety()
    if not result["all_safe"]:
        raise AssertionError(f"Market regime safety violation: {result['issues']}")
