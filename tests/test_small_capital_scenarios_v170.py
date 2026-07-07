"""tests/test_small_capital_scenarios_v170.py — scenario registry tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.scenario_registry_v170 import (
    SCENARIO_REGISTRY, get_scenarios_by_category, get_registry,
)


def count_scenarios():
    return len(SCENARIO_REGISTRY)


def get_all_categories():
    return sorted(set(s["category"] for s in SCENARIO_REGISTRY))


def list_scenarios():
    return list(SCENARIO_REGISTRY)

EXPECTED_CATEGORIES = [
    "capital_profile", "allocation", "position_sizing", "buy_points",
    "forbidden", "watchlist", "market_regime", "reports", "safety",
    "scorecard", "version_identity", "exit_plan",
]


def test_scenario_registry_is_list():
    assert isinstance(SCENARIO_REGISTRY, list)


def test_scenario_registry_count_80():
    assert count_scenarios() == 80


def test_scenario_registry_len_80():
    assert len(SCENARIO_REGISTRY) == 80


def test_all_scenarios_have_scenario_id():
    for s in SCENARIO_REGISTRY:
        assert "scenario_id" in s, f"Missing scenario_id: {s}"


def test_all_scenarios_have_category():
    for s in SCENARIO_REGISTRY:
        assert "category" in s, f"Missing category: {s}"


def test_all_scenarios_have_description():
    for s in SCENARIO_REGISTRY:
        assert "description" in s, f"Missing description: {s}"


def test_all_scenarios_have_name():
    for s in SCENARIO_REGISTRY:
        assert "name" in s or "description" in s, f"Missing name/description: {s['scenario_id']}"


def test_all_scenarios_have_expected_status():
    for s in SCENARIO_REGISTRY:
        assert "expected_status" in s, f"Missing expected_status: {s['scenario_id']}"


def test_capital_profile_category_10():
    assert len(get_scenarios_by_category("capital_profile")) == 10


def test_allocation_category_8():
    assert len(get_scenarios_by_category("allocation")) == 8


def test_position_sizing_category_8():
    assert len(get_scenarios_by_category("position_sizing")) == 8


def test_buy_points_category_8():
    assert len(get_scenarios_by_category("buy_points")) == 8


def test_forbidden_category_8():
    assert len(get_scenarios_by_category("forbidden")) == 8


def test_watchlist_category_8():
    assert len(get_scenarios_by_category("watchlist")) == 8


def test_market_regime_category_5():
    assert len(get_scenarios_by_category("market_regime")) == 5


def test_reports_category_4():
    assert len(get_scenarios_by_category("reports")) == 4


def test_safety_category_8():
    assert len(get_scenarios_by_category("safety")) == 8


def test_scorecard_category_5():
    assert len(get_scenarios_by_category("scorecard")) == 5


def test_version_identity_category_5():
    assert len(get_scenarios_by_category("version_identity")) == 5


def test_exit_plan_category_3():
    assert len(get_scenarios_by_category("exit_plan")) == 3


def test_get_all_categories_returns_list():
    cats = get_all_categories()
    assert isinstance(cats, list)


def test_all_expected_categories_present():
    cats = get_all_categories()
    for cat in EXPECTED_CATEGORIES:
        assert cat in cats, f"Missing category: {cat}"


def test_list_scenarios_returns_list():
    scenarios = list_scenarios()
    assert isinstance(scenarios, list)
    assert len(scenarios) == 80


def test_scenario_ids_unique():
    ids = [s["scenario_id"] for s in SCENARIO_REGISTRY]
    assert len(ids) == len(set(ids)), "Duplicate scenario IDs found"
