"""tests/test_abc_take_profit_engine_v172.py — Take profit engine tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_take_profit_engine_v172 import (
    build_take_profit_plan, build_a_take_profit_plan,
    build_b_take_profit_plan, build_c_take_profit_plan,
    get_take_profit_constants,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCTakeProfitMode, ABCExecutionBlockReason,
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


def test_build_a_take_profit_swing_core():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK, tier="CORE")
    plan = build_a_take_profit_plan(sig, "CORE", [])
    assert plan.take_profit_mode == ABCTakeProfitMode.SWING_25_40_PCT


def test_build_a_take_profit_swing_main_theme():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK, tier="MAIN_THEME")
    plan = build_a_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.take_profit_mode == ABCTakeProfitMode.SWING_25_40_PCT


def test_build_a_take_profit_partial_second_wave():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK, tier="SECOND_WAVE")
    plan = build_a_take_profit_plan(sig, "SECOND_WAVE", [])
    assert plan.take_profit_mode == ABCTakeProfitMode.PARTIAL_10_15_PCT


def test_build_a_take_profit_blocked():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_take_profit_plan(sig, "MAIN_THEME", [ABCExecutionBlockReason.BELOW_20MA])
    assert plan.take_profit_mode == ABCTakeProfitMode.NO_PLAN


def test_build_b_take_profit_staged():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.take_profit_mode == ABCTakeProfitMode.STAGED


def test_build_b_take_profit_references_nonempty():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_take_profit_plan(sig, "MAIN_THEME", [])
    assert len(plan.take_profit_references) > 0


def test_build_b_take_profit_blocked():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_take_profit_plan(sig, "MAIN_THEME", [ABCExecutionBlockReason.VOLUME_NOT_CONFIRMED])
    assert plan.take_profit_mode == ABCTakeProfitMode.NO_PLAN


def test_build_c_take_profit_swing():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    plan = build_c_take_profit_plan(sig, "SECOND_WAVE", [])
    assert plan.take_profit_mode == ABCTakeProfitMode.SWING_25_40_PCT


def test_build_c_take_profit_references_above_entry():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, close=100.0, tier="SECOND_WAVE")
    plan = build_c_take_profit_plan(sig, "SECOND_WAVE", [])
    assert all(r > sig.close for r in plan.take_profit_references)


def test_build_take_profit_dispatches_a():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.buy_point_type == ABCBuyPointType.A_10MA_PULLBACK


def test_build_take_profit_dispatches_b():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT


def test_build_take_profit_dispatches_c():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    plan = build_take_profit_plan(sig, "SECOND_WAVE", [])
    assert plan.buy_point_type == ABCBuyPointType.C_20MA_RECLAIM


def test_build_take_profit_unsupported_no_plan():
    import dataclasses
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    sig2 = dataclasses.replace(sig, buy_point_type=ABCBuyPointType.UNSUPPORTED)
    plan = build_take_profit_plan(sig2, "MAIN_THEME", [])
    assert plan.take_profit_mode == ABCTakeProfitMode.NO_PLAN


def test_get_take_profit_constants_partial_low():
    c = get_take_profit_constants()
    assert c["partial_pct_low"] == 0.10


def test_get_take_profit_constants_swing_high():
    c = get_take_profit_constants()
    assert c["swing_pct_high"] == 0.40


def test_take_profit_paper_only():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.paper_only is True


def test_build_a_take_profit_no_real_orders():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.no_real_orders is True


def test_build_b_take_profit_references_above_entry():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT, close=100.0)
    plan = build_b_take_profit_plan(sig, "MAIN_THEME", [])
    assert all(r > sig.close for r in plan.take_profit_references)


def test_build_a_swing_references_count():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK, tier="CORE")
    plan = build_a_take_profit_plan(sig, "CORE", [])
    assert len(plan.take_profit_references) >= 2


def test_build_a_partial_references_nonempty():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK, tier="SECOND_WAVE")
    plan = build_a_take_profit_plan(sig, "SECOND_WAVE", [])
    assert len(plan.take_profit_references) >= 1


def test_build_c_take_profit_references_two():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    plan = build_c_take_profit_plan(sig, "SECOND_WAVE", [])
    assert len(plan.take_profit_references) == 2


def test_get_take_profit_constants_partial_high():
    c = get_take_profit_constants()
    assert c["partial_pct_high"] == 0.15


def test_get_take_profit_constants_swing_low():
    c = get_take_profit_constants()
    assert c["swing_pct_low"] == 0.25


def test_build_b_staged_partial_pct():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.partial_pct_first == 0.10


def test_build_c_take_profit_swing_pct():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    plan = build_c_take_profit_plan(sig, "SECOND_WAVE", [])
    assert plan.swing_pct_target == 0.25


def test_blocked_c_take_profit_no_plan():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE")
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCExecutionBlockReason
    plan = build_c_take_profit_plan(sig, "SECOND_WAVE", [ABCExecutionBlockReason.NO_FIRST_WAVE])
    assert plan.take_profit_mode == ABCTakeProfitMode.NO_PLAN


def test_take_profit_not_investment_advice():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_take_profit_plan(sig, "MAIN_THEME", [])
    assert plan.not_investment_advice is True
