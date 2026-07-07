"""
paper_trading/small_capital_strategy/theme_filter_v170.py
Theme filter for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.enums_v170 import ThemeStrength
from paper_trading.small_capital_strategy.models_v170 import ThemeFilterResult

MINIMUM_THEME_STRENGTH = ThemeStrength.MODERATE


def filter_by_theme(symbol: str, theme: str, theme_strength: str) -> ThemeFilterResult:
    """
    Filter a symbol by theme strength.
    Requires theme_strength >= MODERATE.
    """
    strength_order = {
        ThemeStrength.NONE.value: 0,
        ThemeStrength.WEAK.value: 1,
        ThemeStrength.MODERATE.value: 2,
        ThemeStrength.STRONG.value: 3,
    }

    min_order = strength_order.get(MINIMUM_THEME_STRENGTH.value, 2)
    actual_order = strength_order.get(theme_strength, 0)
    passed = actual_order >= min_order

    ts = ThemeStrength(theme_strength) if theme_strength in ThemeStrength._value2member_map_ else ThemeStrength.NONE

    return ThemeFilterResult(
        symbol=symbol,
        theme=theme,
        theme_strength=ts,
        passed=passed,
        reason="" if passed else f"theme_strength {theme_strength!r} < required MODERATE",
    )


def batch_filter(candidates: List[Dict[str, Any]]) -> List[ThemeFilterResult]:
    """Apply theme filter to a list of candidates."""
    results = []
    for c in candidates:
        result = filter_by_theme(
            symbol=c.get("symbol", ""),
            theme=c.get("theme", ""),
            theme_strength=c.get("theme_strength", "NONE"),
        )
        results.append(result)
    return results


def get_passing_symbols(results: List[ThemeFilterResult]) -> List[str]:
    """Return symbols that passed theme filter."""
    return [r.symbol for r in results if r.passed]


def validate_theme_filter_result(result: ThemeFilterResult) -> Dict[str, Any]:
    """Validate a ThemeFilterResult."""
    issues = []
    if not result.symbol:
        issues.append("symbol must be non-empty")
    if not result.paper_only:
        issues.append("paper_only must be True")
    return {"valid": len(issues) == 0, "issues": issues}
