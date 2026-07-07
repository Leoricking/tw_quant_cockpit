"""tests/test_financing_risk_filter_v171.py — financing risk filter tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import FinancingRiskGrade
from paper_trading.small_capital_strategy.financing_risk_filter_v171 import (
    apply_financing_risk_filter, grade_financing_risk, score_financing_grade,
    get_financing_thresholds,
    FINANCING_HEALTHY_MAX, FINANCING_MODERATE_MAX,
    FINANCING_ELEVATED_MAX, FINANCING_OVERHEATED_THRESHOLD,
)


def test_healthy_max_constant():
    assert FINANCING_HEALTHY_MAX == 0.10


def test_moderate_max_constant():
    assert FINANCING_MODERATE_MAX == 0.20


def test_elevated_max_constant():
    assert FINANCING_ELEVATED_MAX == 0.30


def test_overheated_threshold_constant():
    assert FINANCING_OVERHEATED_THRESHOLD == 0.30


def test_grade_healthy():
    assert grade_financing_risk(0.05) == FinancingRiskGrade.HEALTHY


def test_grade_healthy_boundary():
    assert grade_financing_risk(0.10) == FinancingRiskGrade.HEALTHY


def test_grade_moderate():
    assert grade_financing_risk(0.15) == FinancingRiskGrade.MODERATE


def test_grade_moderate_boundary():
    assert grade_financing_risk(0.20) == FinancingRiskGrade.MODERATE


def test_grade_elevated():
    assert grade_financing_risk(0.25) == FinancingRiskGrade.ELEVATED


def test_grade_elevated_boundary():
    assert grade_financing_risk(0.30) == FinancingRiskGrade.ELEVATED


def test_grade_overheated():
    assert grade_financing_risk(0.35) == FinancingRiskGrade.OVERHEATED


def test_score_healthy():
    assert score_financing_grade(FinancingRiskGrade.HEALTHY) == 95.0


def test_score_moderate():
    assert score_financing_grade(FinancingRiskGrade.MODERATE) == 70.0


def test_score_elevated():
    assert score_financing_grade(FinancingRiskGrade.ELEVATED) == 40.0


def test_score_overheated():
    assert score_financing_grade(FinancingRiskGrade.OVERHEATED) == 0.0


def test_filter_healthy_passes():
    result = apply_financing_risk_filter("X", 0.05)
    assert result.passed is True


def test_filter_moderate_passes():
    result = apply_financing_risk_filter("X", 0.15)
    assert result.passed is True


def test_filter_elevated_passes():
    result = apply_financing_risk_filter("X", 0.25)
    assert result.passed is True


def test_filter_overheated_fails():
    result = apply_financing_risk_filter("X", 0.35)
    assert result.passed is False


def test_filter_reason_on_fail():
    result = apply_financing_risk_filter("X", 0.35)
    assert "overheated" in result.reason.lower()


def test_filter_reason_empty_on_pass():
    result = apply_financing_risk_filter("X", 0.05)
    assert result.reason == ""


def test_filter_paper_only():
    result = apply_financing_risk_filter("X", 0.05)
    assert result.paper_only is True


def test_filter_not_investment_advice():
    result = apply_financing_risk_filter("X", 0.05)
    assert result.not_investment_advice is True


def test_get_thresholds_dict():
    t = get_financing_thresholds()
    assert isinstance(t, dict)
    assert t["healthy_max"] == FINANCING_HEALTHY_MAX


def test_get_thresholds_overheated():
    t = get_financing_thresholds()
    assert t["overheated_above"] == FINANCING_OVERHEATED_THRESHOLD
