"""
paper_trading/small_capital_strategy/theme_rotation_risk_v177.py
Risk score calculator for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def calculate_risk_score(
    theme: object,
    margin_expansion_rate: float,
    institutional_selling: bool,
    volume_spike: bool,
    overheated: bool,
) -> object:
    """Calculate ThemeRiskScore (higher = more dangerous)."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRiskScore

    score = margin_expansion_rate * 40
    score += 30 if institutional_selling else 0
    score += 15 if volume_spike else 0
    score += 15 if overheated else 0
    score = min(100.0, max(0.0, score))

    return ThemeRiskScore(
        theme=theme,
        score=score,
        margin_expansion_rate=margin_expansion_rate,
        institutional_selling=institutional_selling,
        volume_spike=volume_spike,
        overheated=overheated,
    )
