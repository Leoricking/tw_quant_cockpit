"""
paper_trading/small_capital_strategy/trade_journal_safety_v175.py
Safety flags for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

# Positive safety flags
TRADE_JOURNAL_AVAILABLE          = True
TRADE_JOURNAL_RESEARCH_ONLY      = True
TRADE_JOURNAL_PAPER_ONLY         = True
TRADE_JOURNAL_READ_ONLY          = True
TRADE_JOURNAL_DETERMINISTIC      = True
TRADE_JOURNAL_NOT_INVESTMENT_ADVICE = True

# Negative safety flags (dangerous capabilities = False)
real_trading         = False
real_account         = False
real_order           = False
broker_execution     = False
production_trading_blocked = True

# SAFETY_FLAGS canonical dict
SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only":               True,
    "research_only":            True,
    "no_real_orders":           True,
    "no_broker":                True,
    "not_investment_advice":    True,
    "production_trading_blocked": True,
    "real_trading":             False,
    "real_account":             False,
    "real_order":               False,
    "broker_execution":         False,
}

_MUST_BE_TRUE = [
    "paper_only",
    "research_only",
    "no_real_orders",
    "no_broker",
    "not_investment_advice",
    "production_trading_blocked",
]

_MUST_BE_FALSE = [
    "real_trading",
    "real_account",
    "real_order",
    "broker_execution",
]


def get_safety_flags() -> Dict[str, Any]:
    """Return all trade journal safety flags as a dict."""
    return dict(SAFETY_FLAGS)


def run_safety_audit() -> Dict[str, Any]:
    """Run trade journal safety audit. Returns {all_safe, issues, flags}."""
    flags = get_safety_flags()
    issues = []

    for key in _MUST_BE_TRUE:
        if flags.get(key) is not True:
            issues.append(f"{key} must be True, got {flags.get(key)!r}")

    for key in _MUST_BE_FALSE:
        if flags.get(key) is not False:
            issues.append(f"{key} must be False, got {flags.get(key)!r}")

    return {
        "all_safe": len(issues) == 0,
        "issues":   issues,
        "flags":    flags,
    }


def assert_safe() -> None:
    """Assert all safety invariants. Raises AssertionError on violation."""
    result = run_safety_audit()
    if not result["all_safe"]:
        raise AssertionError(f"Trade journal safety violation: {result['issues']}")
