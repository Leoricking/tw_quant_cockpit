"""tests/test_decision_performance_fixtures_v190.py
Tests for decision performance fixtures v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_fixtures_v190 import (
    get_all_fixtures,
    get_fixture_by_id,
    get_fixtures_by_grade,
)


def test_get_all_fixtures_count_exact():
    assert len(get_all_fixtures()) == 75


def test_get_all_fixtures_count_ge():
    assert len(get_all_fixtures()) >= 75


def test_all_fixtures_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())


def test_all_fixtures_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())


def test_all_fixtures_performance_review_only():
    assert all(f["performance_review_only"] is True for f in get_all_fixtures())


def test_all_fixtures_strategy_improvement_only():
    assert all(f["strategy_improvement_only"] is True for f in get_all_fixtures())


def test_all_fixtures_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())


def test_all_fixtures_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())


def test_all_fixtures_production_trading_blocked():
    assert all(f["production_trading_blocked"] is True for f in get_all_fixtures())


def test_all_fixtures_have_fixture_id():
    assert all("fixture_id" in f for f in get_all_fixtures())


def test_all_fixtures_have_quality_grade():
    assert all("quality_grade" in f for f in get_all_fixtures())


def test_all_fixtures_have_win_rate():
    assert all("win_rate" in f for f in get_all_fixtures())


def test_all_fixtures_have_expectancy_r():
    assert all("expectancy_r" in f for f in get_all_fixtures())


def test_all_fixtures_have_improvement_suggestion():
    assert all("improvement_suggestion" in f for f in get_all_fixtures())


def test_all_fixtures_have_schema_version():
    assert all("schema_version" in f for f in get_all_fixtures())


def test_all_fixtures_schema_version_190():
    assert all(f["schema_version"] == "190" for f in get_all_fixtures())


def test_get_fixture_by_id_dpf190_001_found():
    assert get_fixture_by_id("DPF190-001") != {}


def test_get_fixture_by_id_dpf190_001_paper_only():
    assert get_fixture_by_id("DPF190-001")["paper_only"] is True


def test_get_fixture_by_id_dpf190_075_found():
    assert get_fixture_by_id("DPF190-075") != {}


def test_get_fixture_by_id_notfound_returns_empty():
    assert get_fixture_by_id("NOTFOUND") == {}


def test_get_fixtures_by_grade_excellent():
    assert len(get_fixtures_by_grade("EXCELLENT")) >= 1


def test_get_fixtures_by_grade_good():
    assert len(get_fixtures_by_grade("GOOD")) >= 1


def test_get_fixtures_by_grade_excellent_all_correct_grade():
    assert all(f["quality_grade"] == "EXCELLENT" for f in get_fixtures_by_grade("EXCELLENT"))


def test_get_fixtures_by_grade_poor_all_correct_grade():
    assert all(f["quality_grade"] == "POOR" for f in get_fixtures_by_grade("POOR"))


def test_get_all_fixtures_returns_list():
    assert isinstance(get_all_fixtures(), list)


def test_get_fixture_by_id_returns_dict():
    assert isinstance(get_fixture_by_id("DPF190-001"), dict)


def test_get_fixture_by_id_dpf190_001_performance_review_only():
    assert get_fixture_by_id("DPF190-001")["performance_review_only"] is True


def test_get_fixture_by_id_dpf190_001_no_broker():
    assert get_fixture_by_id("DPF190-001")["no_broker"] is True


def test_get_fixtures_by_grade_nonexistent_empty():
    assert len(get_fixtures_by_grade("NONEXISTENT")) == 0


def test_all_fixtures_drawdown_within_budget():
    assert all(f["drawdown_within_budget"] is True for f in get_all_fixtures())
