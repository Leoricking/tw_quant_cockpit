"""
paper_trading/small_capital_strategy/abc_signal_normalizer_v172.py
Signal normalizer for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Optional

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCNormalizedSignal,
)

# Thresholds
_FINANCING_SAFE_THRESHOLD    = 0.30   # <= 30% is safe
_INST_NOT_SELLING_THRESHOLD  = 0      # >= 0 net buy days = not selling
_VOLUME_CONTRACTING_RATIO    = 0.8    # volume < 80% of avg = contracting
_VOLUME_CONFIRMED_RATIO      = 1.5    # volume >= 1.5x avg = confirmed
_CONSOLIDATION_MIN_WEEKS     = 2
_CONSOLIDATION_MAX_WEEKS     = 6
_MA10_TOUCH_TOLERANCE        = 0.005  # 0.5% tolerance for low touching MA10


def normalize_signal(signal: ABCSignalInput) -> ABCNormalizedSignal:
    """Normalize raw signal into boolean condition flags."""
    above_ma10 = signal.close >= signal.ma10
    above_ma20 = signal.close > signal.ma20
    above_ma60 = signal.close > signal.ma60

    # low touched MA10: close >= MA10 but low <= MA10 * (1 + tolerance)
    low_estimate = signal.close * (1 - signal.atr_pct * 0.5)
    low_touched_ma10 = (
        signal.close >= signal.ma10
        and low_estimate <= signal.ma10 * (1 + _MA10_TOUCH_TOLERANCE)
    )

    avg_vol = signal.avg_volume_20d if signal.avg_volume_20d > 0 else 1.0
    vol_ratio = signal.volume / avg_vol
    volume_contracting = vol_ratio < _VOLUME_CONTRACTING_RATIO
    volume_confirmed   = signal.volume_ratio >= _VOLUME_CONFIRMED_RATIO

    financing_safe = signal.financing_ratio <= _FINANCING_SAFE_THRESHOLD
    institutional_not_selling = signal.institutional_net_buy_days >= _INST_NOT_SELLING_THRESHOLD

    consolidation_valid = (
        _CONSOLIDATION_MIN_WEEKS
        <= signal.consolidation_weeks
        <= _CONSOLIDATION_MAX_WEEKS
    )

    first_wave_present   = signal.had_first_wave
    pullback_complete    = signal.pullback_completed
    ma20_reclaim_valid   = signal.close >= signal.ma20
    kd_not_dead_cross    = not signal.kd_dead_cross
    kd_improving         = signal.kd_golden_cross or (signal.kd_k > signal.kd_d)

    return ABCNormalizedSignal(
        symbol=signal.symbol,
        buy_point_type=signal.buy_point_type,
        above_ma10=above_ma10,
        above_ma20=above_ma20,
        above_ma60=above_ma60,
        low_touched_ma10=low_touched_ma10,
        volume_contracting=volume_contracting,
        volume_confirmed=volume_confirmed,
        financing_safe=financing_safe,
        institutional_not_selling=institutional_not_selling,
        consolidation_valid=consolidation_valid,
        first_wave_present=first_wave_present,
        pullback_complete=pullback_complete,
        ma20_reclaim_valid=ma20_reclaim_valid,
        kd_not_dead_cross=kd_not_dead_cross,
        kd_improving=kd_improving,
        raw=signal,
    )


def get_normalization_thresholds() -> dict:
    """Return normalization threshold constants."""
    return {
        "financing_safe_threshold": _FINANCING_SAFE_THRESHOLD,
        "inst_not_selling_threshold": _INST_NOT_SELLING_THRESHOLD,
        "volume_contracting_ratio": _VOLUME_CONTRACTING_RATIO,
        "volume_confirmed_ratio": _VOLUME_CONFIRMED_RATIO,
        "consolidation_min_weeks": _CONSOLIDATION_MIN_WEEKS,
        "consolidation_max_weeks": _CONSOLIDATION_MAX_WEEKS,
        "ma10_touch_tolerance": _MA10_TOUCH_TOLERANCE,
    }


def describe_buy_point_type(bpt: ABCBuyPointType) -> str:
    """Return human-readable description of a buy point type."""
    descriptions = {
        ABCBuyPointType.A_10MA_PULLBACK:     "A: 10MA Pullback (回測不破)",
        ABCBuyPointType.B_PLATFORM_BREAKOUT: "B: Platform Breakout (平台突破)",
        ABCBuyPointType.C_20MA_RECLAIM:      "C: 20MA Reclaim Second Wave (20MA站回第二波)",
        ABCBuyPointType.UNSUPPORTED:         "Unsupported Buy Point Type",
    }
    return descriptions.get(bpt, "Unknown")
