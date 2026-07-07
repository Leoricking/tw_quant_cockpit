"""tests/test_abc_signal_normalizer_v172.py — Signal normalizer tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_signal_normalizer_v172 import (
    normalize_signal, get_normalization_thresholds, describe_buy_point_type,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType


def _make_signal(symbol="2330", bpt=ABCBuyPointType.A_10MA_PULLBACK,
                 close=100.0, ma5=99.0, ma10=98.0, ma20=95.0, ma60=85.0,
                 volume=700_000, avg_vol=1_000_000, vol_ratio=0.7,
                 atr_pct=0.05, kd_k=60.0, kd_d=50.0, kd_dead_cross=False,
                 financing_ratio=0.10, inst_days=5, theme="STRONG",
                 consolidation_weeks=3, prior_high=95.0,
                 had_first_wave=True, pullback_completed=True,
                 vol_dry_up=True, kd_golden=True, inst_reaccum=True,
                 tier="MAIN_THEME", regime="BULL"):
    return ABCSignalInput(
        symbol=symbol, buy_point_type=bpt, close=close,
        ma5=ma5, ma10=ma10, ma20=ma20, ma60=ma60,
        volume=volume, avg_volume_20d=avg_vol,
        volume_ratio=vol_ratio, atr_pct=atr_pct,
        kd_k=kd_k, kd_d=kd_d, kd_dead_cross=kd_dead_cross,
        financing_ratio=financing_ratio,
        institutional_net_buy_days=inst_days,
        theme_strength=theme, consolidation_weeks=consolidation_weeks,
        prior_platform_high=prior_high,
        had_first_wave=had_first_wave, pullback_completed=pullback_completed,
        volume_dry_up_before_reclaim=vol_dry_up,
        kd_golden_cross=kd_golden,
        institutional_reaccumulation=inst_reaccum,
        tier=tier, market_regime=regime,
    )


def test_normalize_signal_returns_normalized():
    sig = _make_signal()
    norm = normalize_signal(sig)
    assert norm is not None


def test_above_ma10_when_close_above():
    sig = _make_signal(close=100.0, ma10=98.0)
    norm = normalize_signal(sig)
    assert norm.above_ma10 is True


def test_above_ma20_when_close_above():
    sig = _make_signal(close=100.0, ma20=95.0)
    norm = normalize_signal(sig)
    assert norm.above_ma20 is True


def test_above_ma20_false_when_below():
    sig = _make_signal(close=90.0, ma20=95.0)
    norm = normalize_signal(sig)
    assert norm.above_ma20 is False


def test_above_ma60_when_close_above():
    sig = _make_signal(close=100.0, ma60=85.0)
    norm = normalize_signal(sig)
    assert norm.above_ma60 is True


def test_financing_safe_when_low():
    sig = _make_signal(financing_ratio=0.10)
    norm = normalize_signal(sig)
    assert norm.financing_safe is True


def test_financing_unsafe_when_high():
    sig = _make_signal(financing_ratio=0.35)
    norm = normalize_signal(sig)
    assert norm.financing_safe is False


def test_institutional_not_selling_when_positive():
    sig = _make_signal(inst_days=5)
    norm = normalize_signal(sig)
    assert norm.institutional_not_selling is True


def test_institutional_selling_when_negative():
    sig = _make_signal(inst_days=-3)
    norm = normalize_signal(sig)
    assert norm.institutional_not_selling is False


def test_volume_contracting_when_low():
    sig = _make_signal(volume=700_000, avg_vol=1_000_000)
    norm = normalize_signal(sig)
    assert norm.volume_contracting is True


def test_volume_confirmed_when_high():
    sig = _make_signal(vol_ratio=2.0)
    norm = normalize_signal(sig)
    assert norm.volume_confirmed is True


def test_kd_not_dead_cross():
    sig = _make_signal(kd_dead_cross=False)
    norm = normalize_signal(sig)
    assert norm.kd_not_dead_cross is True


def test_kd_dead_cross_detected():
    sig = _make_signal(kd_dead_cross=True)
    norm = normalize_signal(sig)
    assert norm.kd_not_dead_cross is False


def test_consolidation_valid():
    sig = _make_signal(consolidation_weeks=3)
    norm = normalize_signal(sig)
    assert norm.consolidation_valid is True


def test_first_wave_present():
    sig = _make_signal(had_first_wave=True)
    norm = normalize_signal(sig)
    assert norm.first_wave_present is True


def test_first_wave_absent():
    sig = _make_signal(had_first_wave=False)
    norm = normalize_signal(sig)
    assert norm.first_wave_present is False


def test_pullback_complete():
    sig = _make_signal(pullback_completed=True)
    norm = normalize_signal(sig)
    assert norm.pullback_complete is True


def test_ma20_reclaim_valid():
    sig = _make_signal(close=100.0, ma20=98.0)
    norm = normalize_signal(sig)
    assert norm.ma20_reclaim_valid is True


def test_raw_signal_preserved():
    sig = _make_signal()
    norm = normalize_signal(sig)
    assert norm.raw is sig


def test_get_normalization_thresholds_returns_dict():
    thresholds = get_normalization_thresholds()
    assert isinstance(thresholds, dict)


def test_financing_threshold_set():
    thresholds = get_normalization_thresholds()
    assert thresholds["financing_safe_threshold"] == 0.30


def test_volume_confirmed_ratio_set():
    thresholds = get_normalization_thresholds()
    assert thresholds["volume_confirmed_ratio"] == 1.5


def test_describe_buy_point_type_a():
    desc = describe_buy_point_type(ABCBuyPointType.A_10MA_PULLBACK)
    assert "10MA" in desc or "A:" in desc
