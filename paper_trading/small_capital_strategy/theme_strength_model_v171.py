"""
paper_trading/small_capital_strategy/theme_strength_model_v171.py
Theme strength model for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    ThemeStrength, ThemeCategory,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import ThemeStrengthResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"


def assess_theme_strength(
    theme: str,
    leader_count: int,
    breadth_pct: float,   # fraction of stocks above 20MA, 0.0-1.0
    momentum_score: float  # 0-100
) -> ThemeStrength:
    """Assess theme strength from leader count, breadth, and momentum."""
    if leader_count >= 5 and breadth_pct >= 0.70 and momentum_score >= 80:
        return ThemeStrength.LEADING
    if leader_count >= 3 and breadth_pct >= 0.50 and momentum_score >= 60:
        return ThemeStrength.STRONG
    if leader_count >= 1 and breadth_pct >= 0.30 and momentum_score >= 40:
        return ThemeStrength.MODERATE
    if leader_count == 0 or breadth_pct < 0.20 or momentum_score < 20:
        return ThemeStrength.WEAK
    return ThemeStrength.UNKNOWN


def score_theme_for_strength(strength: ThemeStrength) -> float:
    """Return 0-100 score from theme strength."""
    mapping = {
        ThemeStrength.LEADING:  100.0,
        ThemeStrength.STRONG:    85.0,
        ThemeStrength.MODERATE:  60.0,
        ThemeStrength.WEAK:       0.0,
        ThemeStrength.UNKNOWN:   35.0,
    }
    return mapping[strength]


def apply_theme_strength_filter(
    symbol: str,
    theme: str,
    theme_strength: ThemeStrength,
) -> ThemeStrengthResult:
    """Apply theme strength filter. Weak theme = not passed."""
    score = score_theme_for_strength(theme_strength)
    passed = theme_strength != ThemeStrength.WEAK
    reason = "" if passed else f"weak theme '{theme}' — excluded"
    return ThemeStrengthResult(
        symbol=symbol,
        theme=theme,
        theme_strength=theme_strength,
        score=score,
        passed=passed,
        reason=reason,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_theme_strength_scores() -> Dict[str, Any]:
    """Return theme strength score mapping. Deterministic."""
    return {s.value: score_theme_for_strength(s) for s in ThemeStrength}
