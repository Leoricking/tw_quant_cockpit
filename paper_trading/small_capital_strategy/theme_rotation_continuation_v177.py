"""
paper_trading/small_capital_strategy/theme_rotation_continuation_v177.py
Continuation score calculator for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def calculate_continuation_score(
    theme: object,
    consecutive_up_days: int,
    pullback_shallow: bool,
    holding_gain: bool,
) -> object:
    """Calculate ThemeContinuationScore."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeContinuationScore

    score = consecutive_up_days * 10
    score += 20 if pullback_shallow else 0
    score += 20 if holding_gain else 0
    score = min(100.0, max(0.0, float(score)))

    return ThemeContinuationScore(
        theme=theme,
        score=score,
        consecutive_up_days=consecutive_up_days,
        pullback_shallow=pullback_shallow,
        holding_gain=holding_gain,
    )
