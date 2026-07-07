"""tests/test_watchlist_scenarios_v171.py — scenario registry tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_scenario_registry_v171 import (
    WATCHLIST_SCENARIO_REGISTRY,
    get_scenario_count,
    get_scenario_categories,
)


def test_scenario_registry_is_list():
    assert isinstance(WATCHLIST_SCENARIO_REGISTRY, list)


def test_scenario_count_ge_70():
    assert get_scenario_count() >= 70


def test_scenario_registry_len_matches():
    assert len(WATCHLIST_SCENARIO_REGISTRY) == get_scenario_count()


def test_all_scenarios_have_scenario_id():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "scenario_id" in sc, f"Missing scenario_id in {sc}"


def test_all_scenarios_have_category():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "category" in sc, f"Missing category in {sc}"


def test_all_scenarios_have_name():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "name" in sc, f"Missing name in {sc}"


def test_all_scenarios_have_description():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "description" in sc, f"Missing description in {sc}"


def test_all_scenarios_have_expected_status():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "expected_status" in sc, f"Missing expected_status in {sc}"


def test_all_scenarios_have_fixture_id():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "fixture_id" in sc, f"Missing fixture_id in {sc}"


def test_all_scenarios_expected_status_valid():
    valid = {"PASS", "FAIL"}
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert sc["expected_status"] in valid, (
            f"Invalid expected_status '{sc['expected_status']}' in {sc['scenario_id']}"
        )


def test_scenario_ids_start_with_wl_sc():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert sc["scenario_id"].startswith("wl_sc_"), (
            f"Bad scenario_id: {sc['scenario_id']}"
        )


def test_scenario_ids_unique():
    ids = [sc["scenario_id"] for sc in WATCHLIST_SCENARIO_REGISTRY]
    assert len(ids) == len(set(ids)), "Duplicate scenario IDs found"


def test_get_scenario_categories_is_list():
    cats = get_scenario_categories()
    assert isinstance(cats, list)


def test_get_scenario_categories_not_empty():
    assert len(get_scenario_categories()) > 0


def test_scenario_categories_has_profile():
    assert "profile" in get_scenario_categories()


def test_scenario_categories_has_scoring():
    assert "scoring" in get_scenario_categories()


def test_all_scenarios_have_deterministic_seed():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert "deterministic_seed" in sc, f"Missing deterministic_seed in {sc['scenario_id']}"


def test_all_deterministic_seeds_numeric():
    for sc in WATCHLIST_SCENARIO_REGISTRY:
        assert isinstance(sc["deterministic_seed"], int), (
            f"Non-int seed in {sc['scenario_id']}"
        )
