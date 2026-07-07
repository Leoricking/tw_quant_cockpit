"""tests/test_technical_strength_filter_v171.py — technical strength filter tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import TechnicalStrengthGrade
from paper_trading.small_capital_strategy.technical_strength_filter_v171 import (
    apply_technical_strength_filter, grade_technical_strength, score_technical_grade,
    get_technical_grade_scores,
)


def test_grade_a_above_both_low_atr():
    assert grade_technical_strength(True, True, 0.05) == TechnicalStrengthGrade.A


def test_grade_b_above_both_high_atr():
    assert grade_technical_strength(True, True, 0.10) == TechnicalStrengthGrade.B


def test_grade_c_above_20_only():
    assert grade_technical_strength(True, False, 0.05) == TechnicalStrengthGrade.C


def test_grade_d_below_20_above_60_low_atr():
    assert grade_technical_strength(False, True, 0.08) == TechnicalStrengthGrade.D


def test_grade_f_below_both():
    assert grade_technical_strength(False, False, 0.05) == TechnicalStrengthGrade.F


def test_score_a():
    assert score_technical_grade(TechnicalStrengthGrade.A) == 90.0


def test_score_b():
    assert score_technical_grade(TechnicalStrengthGrade.B) == 75.0


def test_score_c():
    assert score_technical_grade(TechnicalStrengthGrade.C) == 55.0


def test_score_d():
    assert score_technical_grade(TechnicalStrengthGrade.D) == 40.0


def test_score_f():
    assert score_technical_grade(TechnicalStrengthGrade.F) == 20.0


def test_score_blocked():
    assert score_technical_grade(TechnicalStrengthGrade.BLOCKED) == 0.0


def test_filter_a_passes():
    result = apply_technical_strength_filter("X", True, True, 0.05)
    assert result.passed is True


def test_filter_f_fails():
    result = apply_technical_strength_filter("X", False, False, 0.05)
    assert result.passed is False


def test_filter_reason_on_fail():
    result = apply_technical_strength_filter("X", False, False, 0.05)
    assert "weak technical" in result.reason.lower()


def test_filter_reason_empty_on_pass():
    result = apply_technical_strength_filter("X", True, True, 0.05)
    assert result.reason == ""


def test_filter_paper_only():
    result = apply_technical_strength_filter("X", True, True, 0.05)
    assert result.paper_only is True


def test_filter_not_investment_advice():
    result = apply_technical_strength_filter("X", True, True, 0.05)
    assert result.not_investment_advice is True


def test_get_grade_scores_dict():
    scores = get_technical_grade_scores()
    assert isinstance(scores, dict)
    assert scores["A"] == 90.0


def test_get_grade_scores_blocked():
    scores = get_technical_grade_scores()
    assert scores["BLOCKED"] == 0.0


def test_grade_a_boundary_exact_atr():
    # Exactly 0.08 ATR with both MAs above = still A
    assert grade_technical_strength(True, True, 0.08) == TechnicalStrengthGrade.A


def test_grade_b_boundary_above_atr():
    # Just above 0.08 ATR with both MAs above = B
    assert grade_technical_strength(True, True, 0.09) == TechnicalStrengthGrade.B
