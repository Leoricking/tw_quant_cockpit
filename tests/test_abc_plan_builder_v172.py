"""tests/test_abc_plan_builder_v172.py — Execution plan builder tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_plan_builder_v172 import (
    build_execution_plan,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus,
)


def _make_sig_a(tier="MAIN_THEME", regime="BULL"):
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        close=100.0, ma5=99.0, ma10=98.0, ma20=95.0, ma60=85.0,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False, financing_ratio=0.10,
        institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier=tier, market_regime=regime,
    )


def _make_sig_b():
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        close=105.0, ma5=103.0, ma10=100.0, ma20=95.0, ma60=85.0,
        volume=2_000_000, avg_volume_20d=1_000_000, volume_ratio=2.0, atr_pct=0.05,
        kd_k=65.0, kd_d=55.0, kd_dead_cross=False, financing_ratio=0.10,
        institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=102.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=False, kd_golden_cross=True,
        institutional_reaccumulation=True, tier="MAIN_THEME", market_regime="BULL",
    )


def _make_sig_c():
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        close=100.0, ma5=99.0, ma10=98.0, ma20=98.0, ma60=85.0,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False, financing_ratio=0.10,
        institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier="SECOND_WAVE", market_regime="BULL",
    )


def test_plan_builder_a_returns_plan():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan is not None


def test_plan_builder_a_buy_point_type():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.buy_point_type == ABCBuyPointType.A_10MA_PULLBACK


def test_plan_builder_b_returns_plan():
    sig = _make_sig_b()
    plan = build_execution_plan(sig, 0)
    assert plan is not None


def test_plan_builder_c_returns_plan():
    sig = _make_sig_c()
    plan = build_execution_plan(sig, 0)
    assert plan is not None


def test_plan_has_conditions_checked():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.conditions_checked is not None


def test_plan_has_entry_plan():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.entry_plan is not None


def test_plan_has_stop_loss():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.stop_loss_plan is not None


def test_plan_has_scorecard():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.scorecard is not None


def test_plan_has_paper_intent():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.paper_intent is not None


def test_plan_excluded_tier_blocked():
    import dataclasses
    sig = _make_sig_a()
    sig2 = dataclasses.replace(sig, tier="EXCLUDED")
    plan = build_execution_plan(sig2, 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_plan_too_many_holdings_blocked():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 4)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_plan_paper_only():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.paper_only is True


def test_plan_no_real_orders():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.no_real_orders is True


def test_plan_not_investment_advice():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.not_investment_advice is True


def test_plan_has_forbidden_checks():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.forbidden_checks is not None
    assert len(plan.forbidden_checks) == 8


def test_plan_has_watchlist_bridge():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.watchlist_bridge is not None


def test_plan_has_regime_bridge():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.regime_bridge is not None


def test_plan_has_take_profit():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.take_profit_plan is not None


def test_plan_has_add_plan():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.add_plan is not None


def test_plan_has_invalidation_plan():
    sig = _make_sig_a()
    plan = build_execution_plan(sig, 0)
    assert plan.invalidation_plan is not None


def test_plan_b_has_stop_loss():
    sig = _make_sig_b()
    plan = build_execution_plan(sig, 0)
    assert plan.stop_loss_plan is not None


def test_plan_c_has_entry_plan():
    sig = _make_sig_c()
    plan = build_execution_plan(sig, 0)
    assert plan.entry_plan is not None
