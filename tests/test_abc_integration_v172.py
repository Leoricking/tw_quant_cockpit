"""tests/test_abc_integration_v172.py — Integration tests for v1.7.2 ABC execution pipeline."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_plan_builder_v172 import (
    build_execution_plan,
)
from paper_trading.small_capital_strategy.abc_execution_report_v172 import (
    build_report, render_json, render_markdown,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCPaperOrderIntentType,
)
from paper_trading.small_capital_strategy.abc_execution_health_v172 import run_health_check
from release.abc_buy_point_execution_plan_release_gate_v172 import run_release_gate


def _sig_a(tier="MAIN_THEME", regime="BULL"):
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


def _sig_b():
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


def _sig_c():
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


def test_full_pipeline_a_produces_plan():
    plan = build_execution_plan(_sig_a(), 0)
    assert plan is not None
    assert plan.buy_point_type == ABCBuyPointType.A_10MA_PULLBACK


def test_full_pipeline_b_produces_plan():
    plan = build_execution_plan(_sig_b(), 0)
    assert plan is not None
    assert plan.buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT


def test_full_pipeline_c_produces_plan():
    plan = build_execution_plan(_sig_c(), 0)
    assert plan is not None
    assert plan.buy_point_type == ABCBuyPointType.C_20MA_RECLAIM


def test_full_pipeline_a_paper_intent_not_real():
    plan = build_execution_plan(_sig_a(), 0)
    assert plan.paper_intent.real_order_requested is False


def test_full_pipeline_a_no_real_orders():
    plan = build_execution_plan(_sig_a(), 0)
    assert plan.no_real_orders is True


def test_full_pipeline_a_report_builds():
    plan = build_execution_plan(_sig_a(), 0)
    report = build_report(plan)
    assert report is not None


def test_full_pipeline_a_report_json_valid():
    import json
    plan = build_execution_plan(_sig_a(), 0)
    report = build_report(plan)
    j = render_json(report)
    data = json.loads(j)
    assert data["symbol"] == "2330"


def test_full_pipeline_a_report_markdown_nonempty():
    plan = build_execution_plan(_sig_a(), 0)
    report = build_report(plan)
    md = render_markdown(report)
    assert len(md) > 50


def test_pipeline_excluded_tier_blocked():
    import dataclasses
    sig = _sig_a()
    sig2 = dataclasses.replace(sig, tier="EXCLUDED")
    plan = build_execution_plan(sig2, 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_pipeline_bear_non_core_blocked():
    plan = build_execution_plan(_sig_a(tier="MAIN_THEME", regime="BEAR"), 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_pipeline_bear_core_regime_not_blocked():
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCExecutionBlockReason
    plan = build_execution_plan(_sig_a(tier="CORE", regime="BEAR"), 0)
    # CORE+BEAR should NOT produce BEAR_REGIME_NON_CORE or MARKET_REGIME_BLOCKED
    assert ABCExecutionBlockReason.BEAR_REGIME_NON_CORE not in plan.block_reasons
    assert ABCExecutionBlockReason.MARKET_REGIME_BLOCKED not in plan.block_reasons


def test_health_and_gate_both_pass():
    health = run_health_check()
    gate = run_release_gate()
    assert health["all_passed"] is True
    assert gate["gate_passed"] is True


def test_scorecard_has_weights_sum_100():
    plan = build_execution_plan(_sig_a(), 0)
    assert plan.scorecard.weights_sum == 100


def test_full_pipeline_a_forbidden_checks_all_pass():
    from paper_trading.small_capital_strategy.abc_forbidden_rule_bridge_v172 import all_rules_passed
    plan = build_execution_plan(_sig_a(), 0)
    assert all_rules_passed(plan.forbidden_checks) is True


def test_full_pipeline_b_paper_only():
    plan = build_execution_plan(_sig_b(), 0)
    assert plan.paper_only is True


def test_full_pipeline_c_not_investment_advice():
    plan = build_execution_plan(_sig_c(), 0)
    assert plan.not_investment_advice is True


def test_full_pipeline_a_stop_loss_below_entry():
    plan = build_execution_plan(_sig_a(), 0)
    if plan.stop_loss_plan and plan.stop_loss_plan.stop_loss_price > 0:
        assert plan.stop_loss_plan.stop_loss_price < plan.entry_plan.entry_price
