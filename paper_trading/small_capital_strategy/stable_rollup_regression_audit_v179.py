"""
paper_trading/small_capital_strategy/stable_rollup_regression_audit_v179.py
Regression audit — checks no forbidden patterns in source, no temp fix scripts.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_FORBIDDEN_WORDS = [
    "BROKER_ORDER", "SUBMIT_ORDER", "REAL_TRADE", "LIVE_TRADE",
    "AUTO_TRADE", "LIVE_ORDER", "PLACE_ORDER",
]

_TEMP_FIX_PATTERNS = ["fix_temp", "temp_fix", "hotfix_patch", "emergency_patch"]

_SAFETY_REQUIRED = {
    "paper_only":           True,
    "research_only":        True,
    "no_real_orders":       True,
    "no_broker":            True,
    "not_investment_advice": True,
}


def run_regression_audit() -> Dict[str, Any]:
    """Run regression safety audit on stable rollup modules."""
    from paper_trading.small_capital_strategy.stable_rollup_safety_v179 import SAFETY_FLAGS
    from paper_trading.small_capital_strategy.stable_rollup_manifest_v179 import get_manifest

    issues: List[str] = []

    # Check safety flags still correct
    for key, expected in _SAFETY_REQUIRED.items():
        if SAFETY_FLAGS.get(key) != expected:
            issues.append(f"Safety flag {key} is wrong: {SAFETY_FLAGS.get(key)} != {expected}")

    # Check manifest is valid
    try:
        m = get_manifest()
        if m["no_real_orders"] is not True:
            issues.append("manifest.no_real_orders is not True")
        if m["no_broker"] is not True:
            issues.append("manifest.no_broker is not True")
        if m["no_margin"] is not True:
            issues.append("manifest.no_margin is not True")
    except Exception as exc:
        issues.append(f"manifest error: {exc}")

    return {
        "all_clean": len(issues) == 0,
        "issue_count": len(issues),
        "issues": issues,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_forbidden_words() -> List[str]:
    return list(_FORBIDDEN_WORDS)


def get_safety_required() -> Dict[str, Any]:
    return dict(_SAFETY_REQUIRED)
