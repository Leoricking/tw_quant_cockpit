"""
paper_trading/small_capital_strategy/safety_v170.py
Safety assertions for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

# Safety invariants — never change these
LIVE_FALLBACK_ENABLED = False
REAL_TRADING_ENABLED = False
BROKER_ENABLED = False
REAL_ACCOUNT_ENABLED = False
REAL_ORDER_ENABLED = False
PRODUCTION_TRADING_ENABLED = False
AUTO_ORDER_ENABLED = False
AUTO_STOP_LOSS_ENABLED = False
AUTO_TAKE_PROFIT_ENABLED = False
MARGIN_ENABLED = False
DAY_TRADING_PRIMARY_ENABLED = False
SHIOAJI_ENABLED = False
EXTERNAL_HTTP_ENABLED = False
PRODUCTION_WRITE_ENABLED = False
REAL_CAPITAL_MUTATION_ENABLED = False

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NOT_INVESTMENT_ADVICE = True
DETERMINISTIC = True
READ_ONLY = True


def get_safety_flags() -> Dict[str, Any]:
    """Return all safety flags as a dict."""
    return {
        "LIVE_FALLBACK_ENABLED": LIVE_FALLBACK_ENABLED,
        "REAL_TRADING_ENABLED": REAL_TRADING_ENABLED,
        "BROKER_ENABLED": BROKER_ENABLED,
        "REAL_ACCOUNT_ENABLED": REAL_ACCOUNT_ENABLED,
        "REAL_ORDER_ENABLED": REAL_ORDER_ENABLED,
        "PRODUCTION_TRADING_ENABLED": PRODUCTION_TRADING_ENABLED,
        "AUTO_ORDER_ENABLED": AUTO_ORDER_ENABLED,
        "AUTO_STOP_LOSS_ENABLED": AUTO_STOP_LOSS_ENABLED,
        "AUTO_TAKE_PROFIT_ENABLED": AUTO_TAKE_PROFIT_ENABLED,
        "MARGIN_ENABLED": MARGIN_ENABLED,
        "DAY_TRADING_PRIMARY_ENABLED": DAY_TRADING_PRIMARY_ENABLED,
        "SHIOAJI_ENABLED": SHIOAJI_ENABLED,
        "EXTERNAL_HTTP_ENABLED": EXTERNAL_HTTP_ENABLED,
        "PRODUCTION_WRITE_ENABLED": PRODUCTION_WRITE_ENABLED,
        "REAL_CAPITAL_MUTATION_ENABLED": REAL_CAPITAL_MUTATION_ENABLED,
        "RESEARCH_ONLY": RESEARCH_ONLY,
        "PAPER_ONLY": PAPER_ONLY,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "NOT_INVESTMENT_ADVICE": NOT_INVESTMENT_ADVICE,
        "DETERMINISTIC": DETERMINISTIC,
        "READ_ONLY": READ_ONLY,
    }


def audit_safety() -> Dict[str, Any]:
    """Run safety audit. Returns {all_safe, safety_capabilities, issues}."""
    flags = get_safety_flags()
    issues = []

    # Flags that must be False
    must_be_false = [
        "LIVE_FALLBACK_ENABLED", "REAL_TRADING_ENABLED", "BROKER_ENABLED",
        "REAL_ACCOUNT_ENABLED", "REAL_ORDER_ENABLED", "PRODUCTION_TRADING_ENABLED",
        "AUTO_ORDER_ENABLED", "AUTO_STOP_LOSS_ENABLED", "AUTO_TAKE_PROFIT_ENABLED",
        "MARGIN_ENABLED", "DAY_TRADING_PRIMARY_ENABLED", "SHIOAJI_ENABLED",
        "EXTERNAL_HTTP_ENABLED", "PRODUCTION_WRITE_ENABLED", "REAL_CAPITAL_MUTATION_ENABLED",
    ]
    for key in must_be_false:
        if flags.get(key) is not False:
            issues.append(f"{key} must be False, got {flags.get(key)!r}")

    # Flags that must be True
    must_be_true = [
        "RESEARCH_ONLY", "PAPER_ONLY", "NO_REAL_ORDERS",
        "NOT_INVESTMENT_ADVICE", "DETERMINISTIC", "READ_ONLY",
    ]
    for key in must_be_true:
        if flags.get(key) is not True:
            issues.append(f"{key} must be True, got {flags.get(key)!r}")

    # safety_capabilities = count of False-when-safe violations
    dangerous_enabled = [k for k in must_be_false if flags.get(k) is not False]
    safety_capabilities = len(dangerous_enabled)

    return {
        "all_safe": len(issues) == 0,
        "safety_capabilities": safety_capabilities,
        "issues": issues,
        "flags": flags,
    }


def assert_safe() -> None:
    """Assert all safety invariants. Raises AssertionError on violation."""
    result = audit_safety()
    if not result["all_safe"]:
        raise AssertionError(f"Safety violation: {result['issues']}")
