"""tests/test_institutional_filter_v171.py — institutional filter tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import InstitutionalGrade
from paper_trading.small_capital_strategy.institutional_filter_v171 import (
    apply_institutional_filter, grade_institutional, score_institutional_grade,
    get_institutional_thresholds,
    INST_ACCUMULATING_THRESHOLD, INST_NEUTRAL_THRESHOLD,
)


def test_accumulating_threshold_constant():
    assert INST_ACCUMULATING_THRESHOLD == 10


def test_neutral_threshold_constant():
    assert INST_NEUTRAL_THRESHOLD == 4


def test_grade_accumulating():
    assert grade_institutional(12) == InstitutionalGrade.ACCUMULATING


def test_grade_accumulating_boundary():
    assert grade_institutional(10) == InstitutionalGrade.ACCUMULATING


def test_grade_neutral():
    assert grade_institutional(6) == InstitutionalGrade.NEUTRAL


def test_grade_neutral_boundary():
    assert grade_institutional(4) == InstitutionalGrade.NEUTRAL


def test_grade_distributing():
    assert grade_institutional(2) == InstitutionalGrade.DISTRIBUTING


def test_grade_distributing_zero():
    assert grade_institutional(0) == InstitutionalGrade.DISTRIBUTING


def test_grade_blocked():
    assert grade_institutional(-1) == InstitutionalGrade.BLOCKED


def test_grade_blocked_large_negative():
    assert grade_institutional(-10) == InstitutionalGrade.BLOCKED


def test_score_accumulating():
    assert score_institutional_grade(InstitutionalGrade.ACCUMULATING) == 90.0


def test_score_neutral():
    assert score_institutional_grade(InstitutionalGrade.NEUTRAL) == 60.0


def test_score_distributing():
    assert score_institutional_grade(InstitutionalGrade.DISTRIBUTING) == 35.0


def test_score_blocked():
    assert score_institutional_grade(InstitutionalGrade.BLOCKED) == 0.0


def test_filter_accumulating_passes():
    result = apply_institutional_filter("X", 12)
    assert result.passed is True


def test_filter_neutral_passes():
    result = apply_institutional_filter("X", 6)
    assert result.passed is True


def test_filter_distributing_passes():
    result = apply_institutional_filter("X", 2)
    assert result.passed is True


def test_filter_blocked_fails():
    result = apply_institutional_filter("X", -1)
    assert result.passed is False


def test_filter_reason_on_fail():
    result = apply_institutional_filter("X", -3)
    assert "heavy selling" in result.reason.lower()


def test_filter_reason_empty_on_pass():
    result = apply_institutional_filter("X", 10)
    assert result.reason == ""


def test_filter_paper_only():
    result = apply_institutional_filter("X", 10)
    assert result.paper_only is True


def test_filter_not_investment_advice():
    result = apply_institutional_filter("X", 10)
    assert result.not_investment_advice is True


def test_get_thresholds_dict():
    t = get_institutional_thresholds()
    assert isinstance(t, dict)
    assert t["accumulating"] == INST_ACCUMULATING_THRESHOLD


def test_get_thresholds_neutral():
    t = get_institutional_thresholds()
    assert t["neutral"] == INST_NEUTRAL_THRESHOLD
