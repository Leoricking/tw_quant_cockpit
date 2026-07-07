"""tests/test_abc_scenarios_v172.py — Scenario registry tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_scenario_registry_v172 import (
    ABC_SCENARIO_REGISTRY, get_scenario_count, get_scenario_categories,
    get_scenarios_by_category, get_scenario_by_id,
)


def test_scenario_count_at_least_70():
    assert get_scenario_count() >= 70


def test_scenario_registry_nonempty():
    assert len(ABC_SCENARIO_REGISTRY) > 0


def test_all_scenarios_have_id():
    for s in ABC_SCENARIO_REGISTRY:
        assert "scenario_id" in s
        assert s["scenario_id"]


def test_all_scenarios_have_name():
    for s in ABC_SCENARIO_REGISTRY:
        assert "name" in s


def test_all_scenarios_have_category():
    for s in ABC_SCENARIO_REGISTRY:
        assert "category" in s


def test_all_scenarios_have_fixture_id():
    for s in ABC_SCENARIO_REGISTRY:
        assert "fixture_id" in s


def test_all_scenarios_have_expected_status():
    for s in ABC_SCENARIO_REGISTRY:
        assert "expected_status" in s


def test_scenario_ids_unique():
    ids = [s["scenario_id"] for s in ABC_SCENARIO_REGISTRY]
    assert len(ids) == len(set(ids))


def test_get_scenario_categories_nonempty():
    cats = get_scenario_categories()
    assert len(cats) > 0


def test_a_buy_point_category_exists():
    cats = get_scenario_categories()
    assert "a_buy_point" in cats


def test_b_buy_point_category_exists():
    cats = get_scenario_categories()
    assert "b_buy_point" in cats


def test_c_buy_point_category_exists():
    cats = get_scenario_categories()
    assert "c_buy_point" in cats


def test_get_scenarios_by_category_a():
    scenarios = get_scenarios_by_category("a_buy_point")
    assert len(scenarios) >= 10


def test_get_scenario_by_id_found():
    s = get_scenario_by_id("abc_sc_001")
    assert s is not None
    assert s["scenario_id"] == "abc_sc_001"


def test_get_scenario_by_id_missing_returns_empty():
    s = get_scenario_by_id("abc_sc_NONEXISTENT")
    assert not s  # returns {} for missing


def test_scenarios_have_deterministic_seed():
    for s in ABC_SCENARIO_REGISTRY:
        assert "deterministic_seed" in s
        assert s["deterministic_seed"] == 172
