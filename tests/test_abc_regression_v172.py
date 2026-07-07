"""tests/test_abc_regression_v172.py — Regression tests for v1.7.2 ABC execution plan."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_plan_builder_v172 import (
    build_execution_plan,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCExecutionGrade,
    ABCPaperOrderIntentType, ABCTakeProfitMode, ABCStopLossMode, ABCEntryMode,
)
from paper_trading.small_capital_strategy.abc_signal_normalizer_v172 import normalize_signal
from paper_trading.small_capital_strategy.abc_condition_checker_v172 import check_conditions
from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import (
    get_scorecard_weights,
)


def _sig(bpt, tier="MAIN_THEME", regime="BULL", close=100.0, ma20=95.0,
         ma10=98.0, vol_ratio=0.7, financing=0.10, inst_days=5,
         had_first_wave=True, pullback=True, prior_high=96.0):
    return ABCSignalInput(
        symbol="2330", buy_point_type=bpt, close=close,
        ma5=close*0.99, ma10=ma10, ma20=ma20, ma60=close*0.85,
        volume=int(vol_ratio * 1_000_000), avg_volume_20d=1_000_000,
        volume_ratio=vol_ratio, atr_pct=0.05, kd_k=60.0, kd_d=50.0,
        kd_dead_cross=False, financing_ratio=financing,
        institutional_net_buy_days=inst_days, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=prior_high,
        had_first_wave=had_first_wave, pullback_completed=pullback,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier=tier, market_regime=regime,
    )


# ── Safety regressions ──────────────────────────────────────────────────────
def test_regression_no_real_orders_always_true():
    for bpt in [ABCBuyPointType.A_10MA_PULLBACK,
                ABCBuyPointType.B_PLATFORM_BREAKOUT,
                ABCBuyPointType.C_20MA_RECLAIM]:
        plan = build_execution_plan(_sig(bpt, tier="MAIN_THEME"), 0)
        assert plan.no_real_orders is True


def test_regression_paper_only_always_true():
    plan = build_execution_plan(_sig(ABCBuyPointType.A_10MA_PULLBACK), 0)
    assert plan.paper_only is True


def test_regression_not_investment_advice_always_true():
    plan = build_execution_plan(_sig(ABCBuyPointType.A_10MA_PULLBACK), 0)
    assert plan.not_investment_advice is True


def test_regression_broker_execution_disabled():
    plan = build_execution_plan(_sig(ABCBuyPointType.A_10MA_PULLBACK), 0)
    assert plan.paper_intent.broker_execution_requested is False


# ── Block condition regressions ──────────────────────────────────────────────
def test_regression_below_ma20_blocks_a():
    plan = build_execution_plan(
        _sig(ABCBuyPointType.A_10MA_PULLBACK, close=90.0, ma20=95.0), 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_regression_financing_overheated_blocks_a():
    plan = build_execution_plan(
        _sig(ABCBuyPointType.A_10MA_PULLBACK, financing=0.35), 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_regression_excluded_tier_blocks():
    plan = build_execution_plan(_sig(ABCBuyPointType.A_10MA_PULLBACK, tier="EXCLUDED"), 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_regression_bear_non_core_blocks():
    plan = build_execution_plan(
        _sig(ABCBuyPointType.A_10MA_PULLBACK, tier="MAIN_THEME", regime="BEAR"), 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_regression_no_first_wave_blocks_c():
    plan = build_execution_plan(
        _sig(ABCBuyPointType.C_20MA_RECLAIM, tier="SECOND_WAVE",
             had_first_wave=False, ma20=98.0), 0)
    assert plan.status == ABCExecutionStatus.BLOCKED


def test_regression_too_many_holdings_blocks():
    plan = build_execution_plan(_sig(ABCBuyPointType.A_10MA_PULLBACK), 4)
    assert plan.status == ABCExecutionStatus.BLOCKED


# ── Score regression ─────────────────────────────────────────────────────────
def test_regression_weights_sum_invariant():
    w = get_scorecard_weights()
    assert w["sum"] == 100


def test_regression_safety_block_grade_blocked():
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCExecutionBlockReason
    from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import compute_scorecard
    plan = build_execution_plan(_sig(ABCBuyPointType.A_10MA_PULLBACK), 0)
    sc = compute_scorecard(
        "2330", ABCBuyPointType.A_10MA_PULLBACK,
        [], None, None, None, None, None,
        [ABCExecutionBlockReason.REAL_ORDER_REQUESTED],
    )
    assert sc.grade == ABCExecutionGrade.BLOCKED


# ── Condition normalizer regressions ─────────────────────────────────────────
def test_regression_close_above_ma20_normalized():
    sig = _sig(ABCBuyPointType.A_10MA_PULLBACK, close=100.0, ma20=95.0)
    norm = normalize_signal(sig)
    assert norm.above_ma20 is True


def test_regression_close_below_ma20_normalized():
    sig = _sig(ABCBuyPointType.A_10MA_PULLBACK, close=90.0, ma20=95.0)
    norm = normalize_signal(sig)
    assert norm.above_ma20 is False


def test_regression_financing_threshold_30pct():
    sig = _sig(ABCBuyPointType.A_10MA_PULLBACK, financing=0.29)
    norm = normalize_signal(sig)
    assert norm.financing_safe is True
    sig2 = _sig(ABCBuyPointType.A_10MA_PULLBACK, financing=0.31)
    norm2 = normalize_signal(sig2)
    assert norm2.financing_safe is False
