"""
paper_trading/small_capital_strategy/theme_rotation_score_v177.py
Strength score calculator for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def score_to_grade(score: float) -> object:
    """Convert numeric score to ThemeGrade."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade
    if score >= 80:
        return ThemeGrade.LEADER
    elif score >= 65:
        return ThemeGrade.STRONG
    elif score >= 50:
        return ThemeGrade.WATCH
    elif score >= 35:
        return ThemeGrade.WEAK
    else:
        return ThemeGrade.EXCLUDED


def apply_market_regime_cap(grade: object, regime: str) -> object:
    """Cap grade based on market regime. RISK_OFF caps at WATCH."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade
    if regime == "RISK_OFF":
        # Maximum grade in RISK_OFF is WATCH
        if grade in (ThemeGrade.LEADER, ThemeGrade.STRONG):
            return ThemeGrade.WATCH
    return grade


def _downgrade(grade: object) -> object:
    """Downgrade a ThemeGrade by one level."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade
    order = [ThemeGrade.LEADER, ThemeGrade.STRONG, ThemeGrade.WATCH, ThemeGrade.WEAK, ThemeGrade.EXCLUDED]
    idx = order.index(grade) if grade in order else len(order) - 1
    return order[min(idx + 1, len(order) - 1)]


def calculate_strength_score(signals: List[object], theme: object) -> object:
    """Calculate ThemeStrengthScore from signals for a given theme."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeSignalType, ThemeGrade
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore

    # Extract signal values by type
    sig_map = {}
    for s in signals:
        st = getattr(s, "signal_type", None)
        if st is not None:
            sig_map[st] = getattr(s, "value", 0.0)

    strong_ratio             = sig_map.get(ThemeSignalType.BREADTH, 0.0)
    new_high_ratio           = sig_map.get(ThemeSignalType.MOMENTUM, 0.0)
    above_ma5_ratio          = sig_map.get(ThemeSignalType.CONTINUATION, 0.0)
    above_ma10_ratio         = sig_map.get(ThemeSignalType.VOLUME, 0.0)
    above_ma20_ratio         = sig_map.get(ThemeSignalType.INSTITUTIONAL, 0.0)
    above_ma60_ratio         = sig_map.get(ThemeSignalType.MARGIN, 0.0)
    volume_expand_ratio      = sig_map.get(ThemeSignalType.VOLUME, 0.0)
    institutional_buy_ratio  = sig_map.get(ThemeSignalType.INSTITUTIONAL, 0.0)
    investment_trust_buy_ratio = sig_map.get(ThemeSignalType.INSTITUTIONAL, 0.0) * 0.5
    margin_risk              = sig_map.get(ThemeSignalType.MARGIN, 0.0) > 0.7
    overheated               = sig_map.get(ThemeSignalType.RISK, 0.0) > 0.8
    resonance_count          = int(strong_ratio * 10)
    single_stock_only        = resonance_count <= 1

    # Weighted score 0~100
    score = (
        strong_ratio * 25
        + new_high_ratio * 20
        + above_ma5_ratio * 10
        + above_ma10_ratio * 10
        + above_ma20_ratio * 10
        + volume_expand_ratio * 10
        + institutional_buy_ratio * 15
    ) * 100
    score = min(100.0, max(0.0, score))

    grade = score_to_grade(score)

    # Downgrade rules
    if single_stock_only and grade == ThemeGrade.LEADER:
        grade = ThemeGrade.STRONG
    if margin_risk and not institutional_buy_ratio > 0.5:
        grade = _downgrade(grade)
    if overheated:
        grade = _downgrade(grade)

    return ThemeStrengthScore(
        theme=theme,
        score=score,
        grade=grade,
        strong_ratio=strong_ratio,
        new_high_ratio=new_high_ratio,
        above_ma5_ratio=above_ma5_ratio,
        above_ma10_ratio=above_ma10_ratio,
        above_ma20_ratio=above_ma20_ratio,
        above_ma60_ratio=above_ma60_ratio,
        volume_expand_ratio=volume_expand_ratio,
        institutional_buy_ratio=institutional_buy_ratio,
        investment_trust_buy_ratio=investment_trust_buy_ratio,
        margin_risk=margin_risk,
        overheated=overheated,
        resonance_count=resonance_count,
        single_stock_only=single_stock_only,
    )
