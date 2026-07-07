"""tests/test_abc_scorecard_v172.py — Execution scorecard tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import (
    compute_scorecard, get_scorecard_weights,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionGrade, ABCExecutionBlockReason,
    ABCConditionStatus, ABCRiskPermission, ABCWatchlistCompatibility, ABCMarketCompatibility,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCConditionCheck, ABCStopLossExecutionPlan, ABCTakeProfitExecutionPlan,
    ABCPositionSizingBridgeResult, ABCWatchlistBridgeResult, ABCMarketRegimeBridgeResult,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCStopLossMode, ABCTakeProfitMode,
)


def _make_good_scorecard_inputs():
    checks = [
        ABCConditionCheck(
            condition_name=f"cond_{i}",
            buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
            status=ABCConditionStatus.MET,
            is_blocking=False,
        )
        for i in range(8)
    ]
    sl = ABCStopLossExecutionPlan(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        stop_loss_mode=ABCStopLossMode.MA10_BREAK_REF,
        stop_loss_price=93.0, stop_loss_pct_from_entry=0.07,
    )
    tp = ABCTakeProfitExecutionPlan(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        take_profit_mode=ABCTakeProfitMode.SWING_25_40_PCT,
        take_profit_references=[125.0, 140.0],
    )
    ps = ABCPositionSizingBridgeResult(
        symbol="2330", capital_twd=300_000.0, max_holdings=4,
        position_amount=30_000.0, quantity_estimate=1000,
        max_loss_amount=2_100.0, risk_pct=0.007,
        training_cap_applied=False,
        risk_permission=ABCRiskPermission.ALLOWED,
        block_reasons=[],
    )
    wb = ABCWatchlistBridgeResult(
        symbol="2330", tier="MAIN_THEME",
        compatibility=ABCWatchlistCompatibility.FULLY_COMPATIBLE,
        allowed_buy_points=[ABCBuyPointType.A_10MA_PULLBACK],
        preferred_buy_points=[ABCBuyPointType.A_10MA_PULLBACK],
        block_reasons=[], training_cap=0.0,
    )
    rb = ABCMarketRegimeBridgeResult(
        market_regime="BULL", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        tier="MAIN_THEME", compatibility=ABCMarketCompatibility.COMPATIBLE,
        block_reasons=[], warnings=[],
    )
    return checks, sl, tp, ps, wb, rb


def test_scorecard_weights_sum_100():
    w = get_scorecard_weights()
    assert w["sum"] == 100


def test_scorecard_weights_keys():
    w = get_scorecard_weights()
    assert "buy_point_condition" in w
    assert "risk_sizing" in w
    assert "stop_loss" in w
    assert "safety" in w


def test_scorecard_good_inputs_not_blocked():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.grade != ABCExecutionGrade.BLOCKED


def test_scorecard_good_inputs_score_positive():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.total_score > 0


def test_scorecard_safety_block_grade_blocked():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb,
                           [ABCExecutionBlockReason.REAL_ORDER_REQUESTED])
    assert sc.grade == ABCExecutionGrade.BLOCKED


def test_scorecard_safety_block_score_zero():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb,
                           [ABCExecutionBlockReason.REAL_ORDER_REQUESTED])
    assert sc.total_score == 0.0


def test_scorecard_position_blocked_grade_blocked():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    import dataclasses
    ps_blocked = dataclasses.replace(ps,
        risk_permission=ABCRiskPermission.BLOCKED,
        block_reasons=[ABCExecutionBlockReason.TOO_MANY_HOLDINGS])
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps_blocked, wb, rb, [])
    assert sc.grade == ABCExecutionGrade.BLOCKED


def test_scorecard_no_conditions_low_score():
    _, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           [], sl, tp, ps, wb, rb, [])
    assert sc.buy_point_condition_score == 0.0


def test_scorecard_weights_sum_field():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.weights_sum == 100


def test_scorecard_paper_only():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.paper_only is True


def test_scorecard_not_investment_advice():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.not_investment_advice is True


def test_scorecard_good_inputs_safety_score_100():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.safety_score == 100.0


def test_scorecard_blocking_condition_blocked():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    blocking_check = ABCConditionCheck(
        condition_name="bad_cond",
        buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        status=ABCConditionStatus.NOT_MET,
        is_blocking=True,
    )
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           [blocking_check], sl, tp, ps, wb, rb, [])
    assert sc.grade == ABCExecutionGrade.BLOCKED


def test_scorecard_b_buy_point():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.B_PLATFORM_BREAKOUT,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT


def test_scorecard_component_scores_nonnegative():
    checks, sl, tp, ps, wb, rb = _make_good_scorecard_inputs()
    sc = compute_scorecard("2330", ABCBuyPointType.A_10MA_PULLBACK,
                           checks, sl, tp, ps, wb, rb, [])
    assert sc.buy_point_condition_score >= 0
    assert sc.risk_sizing_score >= 0
    assert sc.watchlist_tier_score >= 0
    assert sc.market_regime_score >= 0
    assert sc.stop_loss_score >= 0
    assert sc.take_profit_score >= 0
