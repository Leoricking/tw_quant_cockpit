"""
paper_trading/small_capital_strategy/theme_rotation_dashboard_v177.py
Dashboard builder for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"

_DASHBOARD_SECTIONS = [
    "theme_ranking",
    "leader_themes",
    "strong_themes",
    "market_overview",
]


def build_dashboard(
    ranks: List[object],
    date: str,
    market_regime: str = "BULL",
) -> object:
    """Build a ThemeRotationDashboard from ranked themes."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationDashboard
    from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import get_top_n_themes

    top_themes  = get_top_n_themes(ranks, 5)
    leader_count = len([r for r in ranks if getattr(r, "grade", None) == ThemeGrade.LEADER])
    strong_count = len([r for r in ranks if getattr(r, "grade", None) == ThemeGrade.STRONG])

    return ThemeRotationDashboard(
        date=date,
        top_themes=top_themes,
        market_regime=market_regime,
        total_themes=len(ranks),
        leader_count=leader_count,
        strong_count=strong_count,
        sections=list(_DASHBOARD_SECTIONS),
    )
