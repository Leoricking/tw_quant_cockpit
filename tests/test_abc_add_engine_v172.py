"""tests/test_abc_add_engine_v172.py — Add price engine tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_add_price_engine_v172 import (
    build_add_plan, build_a_add_plan, build_b_add_plan, build_c_add_plan,
)
from paper_trading.small_capital_strategy.abc_signal_normalizer_v172 import normalize_signal
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCAddMode, ABCExecutionBlockReason,
)


def _make_sig(bpt, close=100.0, tier="MAIN_THEME"):
    return ABCSignalInput(
        symbol="2330", buy_point_type=bpt, close=close, ma5=close*0.99,
        ma10=close*0.98, ma20=close*0.95, ma60=close*0.85,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False, financing_ratio=0.10,
        institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=close*0.96,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier=tier, market_regime="BULL",
    )


def test_build_a_add_plan_ma5_reclaim():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    norm = normalize_signal(sig)
    plan = build_a_add_plan(sig, norm, [])
    assert plan.add_mode == ABCAddMode.MA5_RECLAIM
    assert plan.add_price > 0


def test_build_a_add_plan_blocked():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    norm = normalize_signal(sig)
    plan = build_a_add_plan(sig, norm, [ABCExecutionBlockReason.BELOW_20MA])
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_build_b_add_plan_second_day_hold():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    norm = normalize_signal(sig)
    plan = build_b_add_plan(sig, norm, [])
    assert plan.add_mode == ABCAddMode.SECOND_DAY_HOLD


def test_build_b_add_plan_blocked():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    norm = normalize_signal(sig)
    plan = build_b_add_plan(sig, norm, [ABCExecutionBlockReason.MARKET_REGIME_BLOCKED])
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_build_c_add_plan_reaction_high():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    norm = normalize_signal(sig)
    plan = build_c_add_plan(sig, norm, [])
    assert plan.add_mode == ABCAddMode.REACTION_HIGH


def test_build_add_plan_dispatches_a():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    norm = normalize_signal(sig)
    plan = build_add_plan(sig, norm, [])
    assert plan.buy_point_type == ABCBuyPointType.A_10MA_PULLBACK


def test_build_add_plan_dispatches_b():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    norm = normalize_signal(sig)
    plan = build_add_plan(sig, norm, [])
    assert plan.buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT


def test_build_add_plan_dispatches_c():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    norm = normalize_signal(sig)
    plan = build_add_plan(sig, norm, [])
    assert plan.buy_point_type == ABCBuyPointType.C_20MA_RECLAIM


def test_add_plan_max_add_units_1():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    norm = normalize_signal(sig)
    plan = build_add_plan(sig, norm, [])
    assert plan.max_add_units == 1


def test_add_plan_paper_only():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    norm = normalize_signal(sig)
    plan = build_add_plan(sig, norm, [])
    assert plan.paper_only is True


def test_build_add_plan_unsupported_blocked():
    import dataclasses
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    sig2 = dataclasses.replace(sig, buy_point_type=ABCBuyPointType.UNSUPPORTED)
    norm = normalize_signal(sig2)
    plan = build_add_plan(sig2, norm, [])
    assert plan.status == ABCExecutionStatus.BLOCKED
