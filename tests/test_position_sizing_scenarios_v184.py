"""
tests/test_position_sizing_scenarios_v184.py
Tests for position_sizing_scenarios_v184 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.position_sizing_scenarios_v184 import (
    get_scenarios, count_scenarios, get_scenarios_by_category, get_scenario_categories,
)


def test_count_scenarios_ge_75():
    assert count_scenarios() >= 75

def test_count_scenarios_is_75():
    assert count_scenarios() == 75

def test_get_scenarios_returns_list():
    assert isinstance(get_scenarios(), list)

def test_get_scenarios_length_75():
    assert len(get_scenarios()) == 75

def test_all_scenarios_have_id():
    for s in get_scenarios():
        assert "id" in s

def test_all_scenarios_have_category():
    for s in get_scenarios():
        assert "category" in s

def test_all_scenarios_have_description():
    for s in get_scenarios():
        assert "description" in s

def test_all_scenarios_paper_only():
    assert all(s["paper_only"] is True for s in get_scenarios())

def test_all_scenarios_research_only():
    assert all(s["research_only"] is True for s in get_scenarios())

def test_all_scenarios_allocation_only():
    assert all(s["allocation_only"] is True for s in get_scenarios())

def test_all_scenarios_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_scenarios())

def test_all_scenarios_no_broker():
    assert all(s["no_broker"] is True for s in get_scenarios())

def test_all_scenarios_no_margin():
    assert all(s["no_margin"] is True for s in get_scenarios())

def test_all_scenarios_no_leverage():
    assert all(s["no_leverage"] is True for s in get_scenarios())

def test_all_scenarios_not_investment_advice():
    assert all(s["not_investment_advice"] is True for s in get_scenarios())

def test_all_scenarios_demo_only():
    assert all(s["demo_only"] is True for s in get_scenarios())

def test_all_scenarios_not_for_production():
    assert all(s["not_for_production"] is True for s in get_scenarios())

def test_all_scenarios_production_trading_blocked():
    assert all(s["production_trading_blocked"] is True for s in get_scenarios())

def test_scenario_ids_start_with_PS184():
    for s in get_scenarios():
        assert s["id"].startswith("PS184-")

def test_scenario_ids_unique():
    ids = [s["id"] for s in get_scenarios()]
    assert len(ids) == len(set(ids))

def test_get_scenario_categories_returns_list():
    cats = get_scenario_categories()
    assert isinstance(cats, list)

def test_get_scenario_categories_not_empty():
    assert len(get_scenario_categories()) > 0

def test_get_scenarios_by_category_fixed_risk():
    cats = get_scenarios_by_category("fixed_risk_safe")
    assert len(cats) >= 9

def test_get_scenarios_by_category_blocked():
    cats = get_scenarios_by_category("blocked")
    assert len(cats) >= 9

def test_get_scenarios_by_category_abc():
    cats = get_scenarios_by_category("abc_staged")
    assert len(cats) >= 9

def test_get_scenarios_by_category_safety():
    cats = get_scenarios_by_category("safety_compliance")
    assert len(cats) >= 5

def test_category_drawdown_exists():
    assert "drawdown_budget" in get_scenario_categories()

def test_category_exposure_exists():
    assert "exposure_limit" in get_scenario_categories()

def test_category_mc_adjusted_exists():
    assert "monte_carlo_adjusted" in get_scenario_categories()

def test_first_scenario_id():
    scenarios = get_scenarios()
    assert scenarios[0]["id"] == "PS184-001"

def test_last_scenario_id():
    scenarios = get_scenarios()
    assert scenarios[-1]["id"] == "PS184-075"
