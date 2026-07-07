"""tests/test_abc_entry_engine_v172.py — Entry price engine tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_entry_price_engine_v172 import (
    build_entry_plan, build_a_entry_plan, build_b_entry_plan, build_c_entry_plan,
)
from paper_trading.small_capital_strategy.abc_signal_normalizer_v172 import normalize_signal
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCEntryMode, ABCExecutionBlockReason,
)


def _sig_a(close=100.0, ma10=98.0, ma20=95.0, ma60=85.0, vol_ratio=0.7):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        close=close, ma5=close*0.99, ma10=ma10, ma20=ma20, ma60=ma60,
        volume=vol_ratio*1_000_000, avg_volume_20d=1_000_000, volume_ratio=vol_ratio,
        atr_pct=0.05, kd_k=60.0, kd_d=50.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5,
        theme_strength="STRONG", consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=True, pullback_completed=True, volume_dry_up_before_reclaim=True,
        kd_golden_cross=True, institutional_reaccumulation=True,
        tier="MAIN_THEME", market_regime="BULL",
    )


def _sig_b(close=105.0, prior_high=102.0, vol_ratio=2.0):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        close=close, ma5=close*0.99, ma10=close*0.97, ma20=close*0.95, ma60=close*0.85,
        volume=vol_ratio*1_000_000, avg_volume_20d=1_000_000, volume_ratio=vol_ratio,
        atr_pct=0.05, kd_k=65.0, kd_d=55.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5,
        theme_strength="STRONG", consolidation_weeks=3, prior_platform_high=prior_high,
        had_first_wave=True, pullback_completed=True, volume_dry_up_before_reclaim=False,
        kd_golden_cross=True, institutional_reaccumulation=True,
        tier="MAIN_THEME", market_regime="BULL",
    )


def _sig_c(close=100.0, ma20=98.0, had_first_wave=True, pullback_completed=True):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        close=close, ma5=close*0.99, ma10=close*0.98, ma20=ma20, ma60=close*0.85,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7,
        atr_pct=0.05, kd_k=60.0, kd_d=50.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5,
        theme_strength="STRONG", consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=had_first_wave, pullback_completed=pullback_completed,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier="SECOND_WAVE", market_regime="BULL",
    )


def test_build_a_entry_plan_ready():
    sig = _sig_a()
    norm = normalize_signal(sig)
    plan = build_a_entry_plan(sig, norm, [])
    assert plan.entry_mode == ABCEntryMode.MA10_RECLAIM
    assert plan.entry_price > 0


def test_build_a_entry_plan_blocked():
    sig = _sig_a()
    norm = normalize_signal(sig)
    plan = build_a_entry_plan(sig, norm, [ABCExecutionBlockReason.BELOW_20MA])
    assert plan.status == ABCExecutionStatus.BLOCKED
    assert plan.entry_price == 0.0


def test_build_b_entry_plan_ready():
    sig = _sig_b()
    norm = normalize_signal(sig)
    plan = build_b_entry_plan(sig, norm, [])
    assert plan.entry_mode == ABCEntryMode.BREAKOUT_CONFIRMATION
    assert plan.entry_price > 0


def test_build_b_entry_plan_blocked():
    sig = _sig_b()
    norm = normalize_signal(sig)
    plan = build_b_entry_plan(sig, norm, [ABCExecutionBlockReason.VOLUME_NOT_CONFIRMED])
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_build_c_entry_plan_ready():
    sig = _sig_c()
    norm = normalize_signal(sig)
    plan = build_c_entry_plan(sig, norm, [])
    assert plan.entry_mode == ABCEntryMode.MA20_RECLAIM
    assert plan.entry_price > 0


def test_build_c_entry_plan_blocked():
    sig = _sig_c()
    norm = normalize_signal(sig)
    plan = build_c_entry_plan(sig, norm, [ABCExecutionBlockReason.NO_FIRST_WAVE])
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_build_entry_plan_dispatches_a():
    sig = _sig_a()
    norm = normalize_signal(sig)
    plan = build_entry_plan(sig, norm, [])
    assert plan.buy_point_type == ABCBuyPointType.A_10MA_PULLBACK


def test_build_entry_plan_dispatches_b():
    sig = _sig_b()
    norm = normalize_signal(sig)
    plan = build_entry_plan(sig, norm, [])
    assert plan.buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT


def test_build_entry_plan_dispatches_c():
    sig = _sig_c()
    norm = normalize_signal(sig)
    plan = build_entry_plan(sig, norm, [])
    assert plan.buy_point_type == ABCBuyPointType.C_20MA_RECLAIM


def test_build_entry_plan_unsupported_blocked():
    import dataclasses
    sig = _sig_a()
    sig2 = dataclasses.replace(sig, buy_point_type=ABCBuyPointType.UNSUPPORTED)
    norm = normalize_signal(sig2)
    plan = build_entry_plan(sig2, norm, [])
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_entry_plan_paper_only():
    sig = _sig_a()
    norm = normalize_signal(sig)
    plan = build_entry_plan(sig, norm, [])
    assert plan.paper_only is True


def test_entry_plan_not_investment_advice():
    sig = _sig_a()
    norm = normalize_signal(sig)
    plan = build_entry_plan(sig, norm, [])
    assert plan.not_investment_advice is True
