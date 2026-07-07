"""tests/test_abc_stop_loss_engine_v172.py — Stop loss engine tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_stop_loss_engine_v172 import (
    build_stop_loss_plan, validate_stop_loss, get_stop_loss_constants,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCStopLossMode, ABCExecutionBlockReason,
)


def _make_sig(bpt, close=100.0, ma10=98.0, ma20=95.0, ma60=85.0, prior_high=95.0):
    return ABCSignalInput(
        symbol="2330", buy_point_type=bpt, close=close, ma5=close*0.99,
        ma10=ma10, ma20=ma20, ma60=ma60, volume=700_000, avg_volume_20d=1_000_000,
        volume_ratio=0.7, atr_pct=0.05, kd_k=60.0, kd_d=50.0, kd_dead_cross=False,
        financing_ratio=0.10, institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=prior_high,
        had_first_wave=True, pullback_completed=True, volume_dry_up_before_reclaim=True,
        kd_golden_cross=True, institutional_reaccumulation=True,
        tier="MAIN_THEME", market_regime="BULL",
    )


def test_build_a_stop_loss_plan_ma10_mode():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_stop_loss_plan(sig, [])
    assert plan.stop_loss_mode == ABCStopLossMode.MA10_BREAK_REF
    assert plan.stop_loss_price > 0


def test_build_a_stop_loss_below_entry():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_stop_loss_plan(sig, [])
    assert plan.stop_loss_price < sig.close


def test_build_a_stop_loss_blocked():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_stop_loss_plan(sig, [ABCExecutionBlockReason.BELOW_20MA])
    assert plan.status == ABCExecutionStatus.BLOCKED
    assert plan.stop_loss_price == 0.0


def test_build_b_stop_loss_platform_mode():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT, close=105.0, prior_high=102.0)
    plan = build_stop_loss_plan(sig, [])
    assert plan.stop_loss_mode == ABCStopLossMode.PLATFORM_LOWER


def test_build_c_stop_loss_below_ma20_mode():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, close=100.0, ma20=98.0)
    plan = build_stop_loss_plan(sig, [])
    assert plan.stop_loss_mode == ABCStopLossMode.BELOW_MA20


def test_build_c_stop_loss_below_entry():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, close=100.0, ma20=98.0)
    plan = build_stop_loss_plan(sig, [])
    assert plan.stop_loss_price < sig.close


def test_stop_loss_pct_from_entry_positive():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_stop_loss_plan(sig, [])
    assert plan.stop_loss_pct_from_entry >= 0


def test_validate_stop_loss_valid():
    assert validate_stop_loss(90.0, 100.0) is True


def test_validate_stop_loss_above_entry_invalid():
    assert validate_stop_loss(110.0, 100.0) is False


def test_validate_stop_loss_zero_entry_invalid():
    assert validate_stop_loss(90.0, 0.0) is False


def test_validate_stop_loss_too_wide_invalid():
    assert validate_stop_loss(85.0, 100.0) is False


def test_get_stop_loss_constants_max_pct():
    constants = get_stop_loss_constants()
    assert constants["max_stop_loss_pct"] == 0.10


def test_build_stop_loss_unsupported_blocked():
    import dataclasses
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    sig2 = dataclasses.replace(sig, buy_point_type=ABCBuyPointType.UNSUPPORTED)
    plan = build_stop_loss_plan(sig2, [])
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_stop_loss_paper_only():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_stop_loss_plan(sig, [])
    assert plan.paper_only is True
