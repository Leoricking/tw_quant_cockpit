"""
paper_trading/small_capital_strategy/watchlist_safety_v171.py
Safety flags for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

# Watchlist-specific safety flags
WATCHLIST_STRATEGY_AVAILABLE            = True
WATCHLIST_STRATEGY_RESEARCH_ONLY        = True
WATCHLIST_STRATEGY_PAPER_ONLY           = True
WATCHLIST_STRATEGY_READ_ONLY            = True
WATCHLIST_STRATEGY_DETERMINISTIC        = True
WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE = True

WATCHLIST_REAL_TRADING_ENABLED          = False
WATCHLIST_REAL_ACCOUNT_ENABLED          = False
WATCHLIST_REAL_ORDER_ENABLED            = False
WATCHLIST_BROKER_EXECUTION_ENABLED      = False
WATCHLIST_PRODUCTION_TRADING_ENABLED    = False
WATCHLIST_LIVE_EXECUTION_ENABLED        = False
WATCHLIST_AUTO_ORDER_ENABLED            = False
WATCHLIST_MARGIN_ENABLED                = False

# Canonical safety aliases
NO_REAL_ORDERS              = True
BROKER_EXECUTION_ENABLED    = False
PRODUCTION_TRADING_BLOCKED  = True


def get_watchlist_safety_flags() -> Dict[str, Any]:
    """Return all watchlist safety flags as a dict."""
    return {
        "WATCHLIST_STRATEGY_AVAILABLE": WATCHLIST_STRATEGY_AVAILABLE,
        "WATCHLIST_STRATEGY_RESEARCH_ONLY": WATCHLIST_STRATEGY_RESEARCH_ONLY,
        "WATCHLIST_STRATEGY_PAPER_ONLY": WATCHLIST_STRATEGY_PAPER_ONLY,
        "WATCHLIST_STRATEGY_READ_ONLY": WATCHLIST_STRATEGY_READ_ONLY,
        "WATCHLIST_STRATEGY_DETERMINISTIC": WATCHLIST_STRATEGY_DETERMINISTIC,
        "WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE": WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE,
        "WATCHLIST_REAL_TRADING_ENABLED": WATCHLIST_REAL_TRADING_ENABLED,
        "WATCHLIST_REAL_ACCOUNT_ENABLED": WATCHLIST_REAL_ACCOUNT_ENABLED,
        "WATCHLIST_REAL_ORDER_ENABLED": WATCHLIST_REAL_ORDER_ENABLED,
        "WATCHLIST_BROKER_EXECUTION_ENABLED": WATCHLIST_BROKER_EXECUTION_ENABLED,
        "WATCHLIST_PRODUCTION_TRADING_ENABLED": WATCHLIST_PRODUCTION_TRADING_ENABLED,
        "WATCHLIST_LIVE_EXECUTION_ENABLED": WATCHLIST_LIVE_EXECUTION_ENABLED,
        "WATCHLIST_AUTO_ORDER_ENABLED": WATCHLIST_AUTO_ORDER_ENABLED,
        "WATCHLIST_MARGIN_ENABLED": WATCHLIST_MARGIN_ENABLED,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def audit_watchlist_safety() -> Dict[str, Any]:
    """Run safety audit. Returns {all_safe, safety_capabilities, issues}."""
    flags = get_watchlist_safety_flags()
    issues = []

    must_be_false = [
        "WATCHLIST_REAL_TRADING_ENABLED",
        "WATCHLIST_REAL_ACCOUNT_ENABLED",
        "WATCHLIST_REAL_ORDER_ENABLED",
        "WATCHLIST_BROKER_EXECUTION_ENABLED",
        "WATCHLIST_PRODUCTION_TRADING_ENABLED",
        "WATCHLIST_LIVE_EXECUTION_ENABLED",
        "WATCHLIST_AUTO_ORDER_ENABLED",
        "WATCHLIST_MARGIN_ENABLED",
        "BROKER_EXECUTION_ENABLED",
    ]
    for key in must_be_false:
        if flags.get(key) is not False:
            issues.append(f"{key} must be False, got {flags.get(key)!r}")

    must_be_true = [
        "WATCHLIST_STRATEGY_AVAILABLE",
        "WATCHLIST_STRATEGY_RESEARCH_ONLY",
        "WATCHLIST_STRATEGY_PAPER_ONLY",
        "WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE",
        "NO_REAL_ORDERS",
        "PRODUCTION_TRADING_BLOCKED",
    ]
    for key in must_be_true:
        if flags.get(key) is not True:
            issues.append(f"{key} must be True, got {flags.get(key)!r}")

    dangerous_enabled = [k for k in must_be_false if flags.get(k) is not False]
    safety_capabilities = len(dangerous_enabled)

    return {
        "all_safe": len(issues) == 0,
        "safety_capabilities": safety_capabilities,
        "issues": issues,
        "flags": flags,
    }


def assert_watchlist_safe() -> None:
    """Assert all watchlist safety invariants. Raises AssertionError on violation."""
    result = audit_watchlist_safety()
    if not result["all_safe"]:
        raise AssertionError(f"Watchlist safety violation: {result['issues']}")
