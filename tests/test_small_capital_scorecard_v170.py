"""tests/test_small_capital_scorecard_v170.py — scorecard tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
    compute_scorecard, get_scorecard_weights, validate_scorecard, SCORE_WEIGHTS,
)
from paper_trading.small_capital_strategy.enums_v170 import SmallCapitalGrade

TEMPLATE_ID = "small_capital_300k_v170"

_ALL_PERFECT = {
    "risk_budget_compliance": 1.0,
    "position_sizing_correctness": 1.0,
    "buy_point_quality": 1.0,
    "market_regime_alignment": 1.0,
    "watchlist_quality": 1.0,
    "exit_plan_completeness": 1.0,
    "safety_compliance": 1.0,
}

_ALL_ZERO = {k: 0.0 for k in _ALL_PERFECT}


def test_weights_sum_100():
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_risk_budget_weight_25():
    assert SCORE_WEIGHTS["risk_budget_compliance"] == 25


def test_position_sizing_weight_20():
    assert SCORE_WEIGHTS["position_sizing_correctness"] == 20


def test_buy_point_weight_15():
    assert SCORE_WEIGHTS["buy_point_quality"] == 15


def test_market_regime_weight_15():
    assert SCORE_WEIGHTS["market_regime_alignment"] == 15


def test_watchlist_weight_10():
    assert SCORE_WEIGHTS["watchlist_quality"] == 10


def test_exit_plan_weight_10():
    assert SCORE_WEIGHTS["exit_plan_completeness"] == 10


def test_safety_weight_5():
    assert SCORE_WEIGHTS["safety_compliance"] == 5


def test_perfect_score_100():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_PERFECT)
    assert sc.score == 100.0


def test_perfect_grade_a():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_PERFECT)
    assert sc.grade == SmallCapitalGrade.A


def test_zero_score_0():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_ZERO)
    assert sc.score == 0.0


def test_zero_grade_f():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_ZERO)
    assert sc.grade == SmallCapitalGrade.F


def test_safety_blocked_grade():
    sc = compute_scorecard(TEMPLATE_ID, {}, safety_blocked=True)
    assert sc.grade == SmallCapitalGrade.BLOCKED


def test_safety_blocked_score_zero():
    sc = compute_scorecard(TEMPLATE_ID, {}, safety_blocked=True)
    assert sc.score == 0.0


def test_safety_blocked_flag():
    sc = compute_scorecard(TEMPLATE_ID, {}, safety_blocked=True)
    assert sc.safety_blocked is True


def test_grade_b_threshold():
    # Score ~72: risk_budget=0.8*25 + position=0.8*20 + bpq=0.8*15 + mra=0.8*15 + wq=0.0 + epc=0.0 + sc=0.8*5 = 20+16+12+12+0+0+4 = 64... adjust
    scores = {k: 0.8 for k in _ALL_PERFECT}
    sc = compute_scorecard(TEMPLATE_ID, scores)
    assert sc.score == pytest.approx(80.0, abs=0.01)
    assert sc.grade == SmallCapitalGrade.B


def test_grade_c_threshold():
    scores = {k: 0.6 for k in _ALL_PERFECT}
    sc = compute_scorecard(TEMPLATE_ID, scores)
    assert sc.score == pytest.approx(60.0, abs=0.01)
    assert sc.grade == SmallCapitalGrade.C


def test_grade_d_threshold():
    scores = {k: 0.4 for k in _ALL_PERFECT}
    sc = compute_scorecard(TEMPLATE_ID, scores)
    assert sc.score == pytest.approx(40.0, abs=0.01)
    assert sc.grade == SmallCapitalGrade.D


def test_scorecard_paper_only():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_PERFECT)
    assert sc.paper_only is True


def test_scorecard_no_real_orders():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_PERFECT)
    assert sc.no_real_orders is True


def test_scorecard_template_id():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_PERFECT)
    assert sc.template_id == TEMPLATE_ID


def test_validate_scorecard_pass():
    sc = compute_scorecard(TEMPLATE_ID, _ALL_PERFECT)
    result = validate_scorecard(sc)
    assert result["valid"] is True


def test_get_scorecard_weights_returns_dict():
    weights = get_scorecard_weights()
    assert isinstance(weights, dict)
    assert sum(weights.values()) == 100


def test_component_scores_clamped_above_1():
    scores = {k: 2.0 for k in _ALL_PERFECT}
    sc = compute_scorecard(TEMPLATE_ID, scores)
    assert sc.score == 100.0


def test_component_scores_clamped_below_0():
    scores = {k: -1.0 for k in _ALL_PERFECT}
    sc = compute_scorecard(TEMPLATE_ID, scores)
    assert sc.score == 0.0


def test_no_a_plus_grade():
    assert not hasattr(SmallCapitalGrade, "A_PLUS")
