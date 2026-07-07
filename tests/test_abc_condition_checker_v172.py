"""tests/test_abc_condition_checker_v172.py — Condition checker tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
    check_a_conditions, check_b_conditions, check_c_conditions,
    check_conditions, get_condition_names,
)
from paper_trading.small_capital_strategy.abc_signal_normalizer_v172 import normalize_signal
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCConditionStatus, ABCExecutionBlockReason,
)


def _make_good_a_signal(tier="MAIN_THEME", regime="BULL"):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        close=100.0, ma5=99.0, ma10=98.0, ma20=95.0, ma60=85.0,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5,
        theme_strength="STRONG", consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier=tier, market_regime=regime,
    )


def _make_good_b_signal(tier="MAIN_THEME", regime="BULL"):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        close=105.0, ma5=103.0, ma10=100.0, ma20=95.0, ma60=85.0,
        volume=2_000_000, avg_volume_20d=1_000_000, volume_ratio=2.0, atr_pct=0.05,
        kd_k=65.0, kd_d=55.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5,
        theme_strength="STRONG", consolidation_weeks=3, prior_platform_high=102.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=False, kd_golden_cross=True,
        institutional_reaccumulation=True, tier=tier, market_regime=regime,
    )


def _make_good_c_signal(tier="SECOND_WAVE", regime="BULL"):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        close=100.0, ma5=99.0, ma10=98.0, ma20=98.0, ma60=85.0,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5,
        theme_strength="STRONG", consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier=tier, market_regime=regime,
    )


def test_a_conditions_all_met_no_blocks():
    sig = _make_good_a_signal()
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, sig.tier, sig.market_regime)
    assert len(checks) > 0
    # All conditions should be met or non-blocking
    assert len([c for c in checks if c.is_blocking]) == 0


def test_a_conditions_ma20_block():
    import dataclasses
    sig = _make_good_a_signal()
    sig2 = dataclasses.replace(sig, close=90.0, ma20=95.0)
    norm = normalize_signal(sig2)
    checks, blocks = check_conditions(norm, sig2.tier, sig2.market_regime)
    assert ABCExecutionBlockReason.BELOW_20MA in blocks


def test_a_conditions_excluded_blocked():
    sig = _make_good_a_signal(tier="EXCLUDED")
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, "EXCLUDED", sig.market_regime)
    assert ABCExecutionBlockReason.WATCHLIST_EXCLUDED in blocks


def test_a_conditions_bear_non_core_blocked():
    sig = _make_good_a_signal(tier="MAIN_THEME", regime="BEAR")
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, "MAIN_THEME", "BEAR")
    assert ABCExecutionBlockReason.BEAR_REGIME_NON_CORE in blocks


def test_a_conditions_bear_core_allowed():
    sig = _make_good_a_signal(tier="CORE", regime="BEAR")
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, "CORE", "BEAR")
    assert ABCExecutionBlockReason.BEAR_REGIME_NON_CORE not in blocks


def test_b_conditions_volume_not_confirmed_block():
    import dataclasses
    sig = _make_good_b_signal()
    sig2 = dataclasses.replace(sig, volume_ratio=0.8, volume=800_000)
    norm = normalize_signal(sig2)
    checks, blocks = check_conditions(norm, sig2.tier, sig2.market_regime)
    assert ABCExecutionBlockReason.VOLUME_NOT_CONFIRMED in blocks


def test_b_conditions_bear_regime_blocked():
    sig = _make_good_b_signal(regime="BEAR")
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, sig.tier, "BEAR")
    assert ABCExecutionBlockReason.MARKET_REGIME_BLOCKED in blocks


def test_b_conditions_excluded_blocked():
    sig = _make_good_b_signal(tier="EXCLUDED")
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, "EXCLUDED", sig.market_regime)
    assert ABCExecutionBlockReason.WATCHLIST_EXCLUDED in blocks


def test_c_conditions_no_first_wave_blocked():
    import dataclasses
    sig = _make_good_c_signal()
    sig2 = dataclasses.replace(sig, had_first_wave=False)
    norm = normalize_signal(sig2)
    checks, blocks = check_conditions(norm, sig2.tier, sig2.market_regime)
    assert ABCExecutionBlockReason.NO_FIRST_WAVE in blocks


def test_c_conditions_risk_off_blocked():
    sig = _make_good_c_signal(regime="RISK_OFF")
    norm = normalize_signal(sig)
    checks, blocks = check_conditions(norm, sig.tier, "RISK_OFF")
    assert ABCExecutionBlockReason.RISK_OFF_REGIME in blocks


def test_c_conditions_below_ma20_blocked():
    import dataclasses
    sig = _make_good_c_signal()
    sig2 = dataclasses.replace(sig, close=94.0, ma20=98.0)
    norm = normalize_signal(sig2)
    checks, blocks = check_conditions(norm, sig2.tier, sig2.market_regime)
    assert ABCExecutionBlockReason.BELOW_20MA in blocks


def test_get_condition_names_a_nonempty():
    names = get_condition_names(ABCBuyPointType.A_10MA_PULLBACK)
    assert len(names) >= 8


def test_get_condition_names_b_nonempty():
    names = get_condition_names(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert len(names) >= 4


def test_get_condition_names_c_nonempty():
    names = get_condition_names(ABCBuyPointType.C_20MA_RECLAIM)
    assert len(names) >= 6


def test_get_condition_names_unsupported_empty():
    names = get_condition_names(ABCBuyPointType.UNSUPPORTED)
    assert names == []


def test_check_conditions_unsupported_returns_block():
    import dataclasses
    sig = _make_good_a_signal()
    sig2 = dataclasses.replace(sig, buy_point_type=ABCBuyPointType.UNSUPPORTED)
    norm = normalize_signal(sig2)
    checks, blocks = check_conditions(norm, sig2.tier, sig2.market_regime)
    assert ABCExecutionBlockReason.UNSUPPORTED_BUY_POINT in blocks
