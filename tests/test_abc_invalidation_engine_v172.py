"""tests/test_abc_invalidation_engine_v172.py — Invalidation engine tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_invalidation_engine_v172 import (
    build_invalidation_plan, build_a_invalidation_plan,
    build_b_invalidation_plan, build_c_invalidation_plan,
    get_invalidation_bars,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCInvalidationReason,
)


def _make_sig(bpt, close=100.0, ma20=95.0, prior_high=96.0):
    return ABCSignalInput(
        symbol="2330", buy_point_type=bpt, close=close, ma5=close*0.99,
        ma10=close*0.98, ma20=ma20, ma60=close*0.85,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False, financing_ratio=0.10,
        institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=prior_high,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier="MAIN_THEME", market_regime="BULL",
    )


def test_a_invalidation_bars_3():
    assert get_invalidation_bars(ABCBuyPointType.A_10MA_PULLBACK) == 3


def test_b_invalidation_bars_2():
    assert get_invalidation_bars(ABCBuyPointType.B_PLATFORM_BREAKOUT) == 2


def test_c_invalidation_bars_3():
    assert get_invalidation_bars(ABCBuyPointType.C_20MA_RECLAIM) == 3


def test_unsupported_invalidation_bars_0():
    assert get_invalidation_bars(ABCBuyPointType.UNSUPPORTED) == 0


def test_build_a_invalidation_plan_bars():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_invalidation_plan(sig, [])
    assert plan.bars_to_confirm == 3


def test_build_a_invalidation_stop_loss_reason():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_invalidation_plan(sig, [])
    assert ABCInvalidationReason.STOP_LOSS_HIT in plan.invalidation_reasons


def test_build_b_invalidation_plan_bars():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_invalidation_plan(sig, [])
    assert plan.bars_to_confirm == 2


def test_build_b_invalidation_breakout_back_reason():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_invalidation_plan(sig, [])
    assert ABCInvalidationReason.BREAKOUT_BACK_INTO_PLATFORM in plan.invalidation_reasons


def test_build_c_invalidation_plan_bars():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, ma20=98.0)
    plan = build_c_invalidation_plan(sig, [])
    assert plan.bars_to_confirm == 3


def test_build_c_invalidation_reclaim_fails_reason():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, ma20=98.0)
    plan = build_c_invalidation_plan(sig, [])
    assert ABCInvalidationReason.RECLAIM_FAILS_N_BARS in plan.invalidation_reasons


def test_build_invalidation_dispatches_a():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_invalidation_plan(sig, [])
    assert plan.buy_point_type == ABCBuyPointType.A_10MA_PULLBACK


def test_build_invalidation_dispatches_b():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_invalidation_plan(sig, [])
    assert plan.buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT


def test_build_invalidation_dispatches_c():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, ma20=98.0)
    plan = build_invalidation_plan(sig, [])
    assert plan.buy_point_type == ABCBuyPointType.C_20MA_RECLAIM


def test_build_invalidation_unsupported_not_set():
    import dataclasses
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    sig2 = dataclasses.replace(sig, buy_point_type=ABCBuyPointType.UNSUPPORTED)
    plan = build_invalidation_plan(sig2, [])
    assert ABCInvalidationReason.NOT_SET in plan.invalidation_reasons


def test_invalidation_plan_has_notes():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_invalidation_plan(sig, [])
    assert len(plan.invalidation_notes) > 0


def test_invalidation_plan_paper_only():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_invalidation_plan(sig, [])
    assert plan.paper_only is True


def test_a_invalidation_ma20_reason():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_invalidation_plan(sig, [])
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCInvalidationReason
    assert ABCInvalidationReason.CLOSE_BELOW_MA20 in plan.invalidation_reasons


def test_a_invalidation_ma10_reclaim_fails():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_invalidation_plan(sig, [])
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCInvalidationReason
    assert ABCInvalidationReason.MA10_RECLAIM_FAILS in plan.invalidation_reasons


def test_b_invalidation_volume_collapse():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_invalidation_plan(sig, [])
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCInvalidationReason
    assert ABCInvalidationReason.VOLUME_COLLAPSE in plan.invalidation_reasons


def test_b_invalidation_stop_loss():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_invalidation_plan(sig, [])
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCInvalidationReason
    assert ABCInvalidationReason.STOP_LOSS_HIT in plan.invalidation_reasons


def test_c_invalidation_below_ma20():
    sig = _make_sig(ABCBuyPointType.C_20MA_RECLAIM, ma20=98.0)
    plan = build_c_invalidation_plan(sig, [])
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCInvalidationReason
    assert ABCInvalidationReason.CLOSE_BELOW_MA20 in plan.invalidation_reasons


def test_invalidation_plan_three_reasons_a():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_invalidation_plan(sig, [])
    assert len(plan.invalidation_reasons) == 3


def test_invalidation_plan_three_notes_a():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_a_invalidation_plan(sig, [])
    assert len(plan.invalidation_notes) == 3


def test_invalidation_not_investment_advice():
    sig = _make_sig(ABCBuyPointType.A_10MA_PULLBACK)
    plan = build_invalidation_plan(sig, [])
    assert plan.not_investment_advice is True


def test_b_invalidation_three_reasons():
    sig = _make_sig(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    plan = build_b_invalidation_plan(sig, [])
    assert len(plan.invalidation_reasons) == 3
