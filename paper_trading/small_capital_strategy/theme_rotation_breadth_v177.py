"""
paper_trading/small_capital_strategy/theme_rotation_breadth_v177.py
Breadth score calculator for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def calculate_breadth_score(advancing: int, declining: int, total: int, theme: object) -> object:
    """Calculate ThemeBreadthScore from advancing/declining/total counts."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeBreadthScore

    score = (advancing / total * 100) if total > 0 else 0.0
    score = min(100.0, max(0.0, score))
    advance_decline_ratio = advancing / max(declining, 1)

    return ThemeBreadthScore(
        theme=theme,
        score=score,
        advancing=advancing,
        declining=declining,
        total=total,
        advance_decline_ratio=advance_decline_ratio,
    )
