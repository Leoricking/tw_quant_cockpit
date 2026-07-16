"""tests/test_decision_performance_scenarios_v190.py
Tests for decision performance scenarios v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_scenarios_v190 import (
    get_all_scenarios,
    get_scenarios_by_type,
    get_scenario_by_id,
)


def test_get_all_scenarios_count_exact():
    assert len(get_all_scenarios()) == 75


def test_get_all_scenarios_count_ge():
    assert len(get_all_scenarios()) >= 75


def test_all_scenarios_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())


def test_all_scenarios_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())


def test_all_scenarios_performance_review_only():
    assert all(s["performance_review_only"] is True for s in get_all_scenarios())


def test_all_scenarios_strategy_improvement_only():
    assert all(s["strategy_improvement_only"] is True for s in get_all_scenarios())


def test_all_scenarios_have_scenario_id():
    assert all("scenario_id" in s for s in get_all_scenarios())


def test_all_scenarios_have_description():
    assert all("description" in s for s in get_all_scenarios())


def test_all_scenarios_have_scenario_type():
    assert all("scenario_type" in s for s in get_all_scenarios())


def test_all_scenarios_have_no_broker():
    assert all("no_broker" in s for s in get_all_scenarios())


def test_get_scenarios_by_type_complete_performance_review():
    assert len(get_scenarios_by_type("complete_performance_review")) >= 1


def test_get_scenarios_by_type_r_multiple_healthy():
    assert len(get_scenarios_by_type("r_multiple_healthy")) >= 1


def test_get_scenarios_by_type_positive_expectancy():
    assert len(get_scenarios_by_type("positive_expectancy")) >= 1


def test_get_scenarios_by_type_negative_expectancy():
    assert len(get_scenarios_by_type("negative_expectancy")) >= 1


def test_get_scenarios_by_type_high_drawdown_blocked():
    assert len(get_scenarios_by_type("high_drawdown_blocked")) >= 1


def test_get_all_scenarios_returns_list():
    assert isinstance(get_all_scenarios(), list)


def test_get_scenarios_by_type_returns_list():
    assert isinstance(get_scenarios_by_type("complete_performance_review"), list)


def test_get_scenario_by_id_dp190_001_found():
    assert get_scenario_by_id("DP190-001") != {}


def test_get_scenario_by_id_dp190_001_paper_only():
    assert get_scenario_by_id("DP190-001")["paper_only"] is True


def test_get_scenario_by_id_dp190_075_found():
    assert get_scenario_by_id("DP190-075") != {}


def test_get_scenario_by_id_notfound_returns_empty():
    assert get_scenario_by_id("NOTFOUND") == {}


def test_all_scenarios_no_forbidden_words_in_description():
    forbidden = ["BUY_SIGNAL", "SUBMIT_ORDER", "BROKER"]
    assert all(
        not any(w in s.get("description", "").upper() for w in forbidden)
        for s in get_all_scenarios()
    )


def test_all_scenarios_no_broker_true():
    assert all(s["no_broker"] is True for s in get_all_scenarios())


def test_get_scenario_by_id_dp190_001_performance_review_only():
    assert get_scenario_by_id("DP190-001")["performance_review_only"] is True


def test_get_scenario_by_id_dp190_001_no_real_orders():
    assert get_scenario_by_id("DP190-001")["no_real_orders"] is True


def test_get_scenario_by_id_dp190_001_returns_dict():
    assert isinstance(get_scenario_by_id("DP190-001"), dict)


def test_get_scenario_by_id_dp190_001_strategy_improvement_only():
    assert get_scenario_by_id("DP190-001")["strategy_improvement_only"] is True


def test_all_scenarios_not_investment_advice():
    assert all(s["not_investment_advice"] is True for s in get_all_scenarios())


def test_get_scenarios_by_type_nonexistent_empty():
    assert len(get_scenarios_by_type("nonexistent_type")) == 0


def test_all_scenarios_have_schema_version():
    assert all("schema_version" in s for s in get_all_scenarios())
