"""
paper_trading/small_capital_strategy/theme_rotation_watchlist_v177.py
Watchlist candidate functions for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def build_watchlist_candidate(
    symbol: str,
    theme: object,
    grade: object,
    reason: str,
) -> object:
    """Build a ThemeWatchlistCandidate. eligible if grade in (LEADER, STRONG)."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeWatchlistCandidate

    eligible = grade in (ThemeGrade.LEADER, ThemeGrade.STRONG)

    return ThemeWatchlistCandidate(
        symbol=symbol,
        theme=theme,
        grade=grade,
        reason=reason,
        eligible=eligible,
    )


def filter_eligible_candidates(candidates: List[object]) -> List[object]:
    """Return only candidates with eligible=True."""
    return [c for c in candidates if getattr(c, "eligible", False)]


def get_watchlist_by_theme(candidates: List[object], theme: object) -> List[object]:
    """Return candidates filtered by specific theme."""
    return [c for c in candidates if getattr(c, "theme", None) == theme]
