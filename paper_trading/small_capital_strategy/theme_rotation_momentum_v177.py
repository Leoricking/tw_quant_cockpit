"""
paper_trading/small_capital_strategy/theme_rotation_momentum_v177.py
Momentum score calculator for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def calculate_momentum_score(
    theme: object,
    week_change_pct: float,
    month_change_pct: float,
    relative_strength: float,
) -> object:
    """Calculate ThemeMomentumScore."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeMomentumScore

    score = week_change_pct * 0.4 + month_change_pct * 0.3 + relative_strength * 0.3
    score = min(100.0, max(0.0, score))

    return ThemeMomentumScore(
        theme=theme,
        score=score,
        week_change_pct=week_change_pct,
        month_change_pct=month_change_pct,
        relative_strength=relative_strength,
    )
