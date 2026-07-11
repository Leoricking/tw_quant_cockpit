"""
tests/test_simulation_matrix_scenarios_v181.py
Tests for simulation_matrix_scenarios_v181 — 75 scenarios.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_scenarios_v181 import (
    get_scenario_count, get_all_scenarios, get_scenario_by_id,
    get_scenarios_by_category, get_scenario_categories,
    get_scenario_ids, get_scenarios_info,
)

_VALID_ACTIONS = {
    "PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY", "OBSERVE", "WAIT",
    "BLOCKED", "REDUCE_RISK", "REVIEW_REQUIRED", "NO_TRADE",
    "PAPER_ADD_ALLOWED", "STRESS_TEST_ONLY", "SIMULATE_ONLY",
    "RESEARCH_ONLY", "READ_REPORT",
}

# ── get_scenario_count() ───────────────────────────────────────────────────────

def test_scenario_count_ge_75():
    assert get_scenario_count() >= 75

def test_scenario_count_equals_75():
    assert get_scenario_count() == 75

def test_scenario_count_equals_len_all():
    assert get_scenario_count() == len(get_all_scenarios())


# ── get_all_scenarios() ────────────────────────────────────────────────────────

def test_all_scenarios_is_list():
    assert isinstance(get_all_scenarios(), list)

def test_all_scenarios_each_has_id():
    assert all("id" in s for s in get_all_scenarios())

def test_all_scenarios_each_has_category():
    assert all("category" in s for s in get_all_scenarios())

def test_all_scenarios_each_has_expected_action():
    assert all("expected_action" in s for s in get_all_scenarios())

def test_all_scenarios_paper_only():
    assert all(s.get("paper_only") is True for s in get_all_scenarios())

def test_all_scenarios_research_only():
    assert all(s.get("research_only") is True for s in get_all_scenarios())

def test_all_scenarios_simulate_only():
    assert all(s.get("simulate_only") is True for s in get_all_scenarios())

def test_all_scenarios_stress_test_only():
    assert all(s.get("stress_test_only") is True for s in get_all_scenarios())

def test_all_scenarios_no_real_orders():
    assert all(s.get("no_real_orders") is True for s in get_all_scenarios())

def test_all_scenarios_not_investment_advice():
    assert all(s.get("not_investment_advice") is True for s in get_all_scenarios())

def test_all_scenarios_ids_unique():
    ids = [s["id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))

def test_all_scenarios_ids_start_with_sm181():
    assert all(s["id"].startswith("SM181-") for s in get_all_scenarios())

def test_all_scenarios_expected_actions_valid():
    for s in get_all_scenarios():
        assert s["expected_action"] in _VALID_ACTIONS, f"{s['id']} has invalid action {s['expected_action']}"

def test_all_scenarios_have_market_regime():
    assert all("market_regime" in s for s in get_all_scenarios())

def test_all_scenarios_have_theme_rank():
    assert all("theme_rank" in s for s in get_all_scenarios())

def test_all_scenarios_have_abc_signal():
    assert all("abc_signal" in s for s in get_all_scenarios())

def test_all_scenarios_have_mistake_injection():
    assert all("mistake_injection" in s for s in get_all_scenarios())

def test_all_scenarios_initial_capital_positive():
    assert all(s.get("initial_capital", 1.0) > 0 for s in get_all_scenarios())


# ── get_scenario_by_id() ──────────────────────────────────────────────────────

def test_get_scenario_sm181_001():
    s = get_scenario_by_id("SM181-001")
    assert s is not None
    assert s["id"] == "SM181-001"

def test_get_scenario_sm181_075():
    s = get_scenario_by_id("SM181-075")
    assert s is not None
    assert s["id"] == "SM181-075"

def test_get_scenario_not_found_returns_none():
    assert get_scenario_by_id("SM181-999") is None

def test_get_scenario_empty_id_returns_none():
    assert get_scenario_by_id("") is None

def test_get_scenario_paper_only():
    s = get_scenario_by_id("SM181-001")
    assert s["paper_only"] is True


# ── get_scenarios_by_category() ───────────────────────────────────────────────

def test_get_scenarios_entry_allowed_category():
    cats = get_scenarios_by_category("entry_allowed")
    assert len(cats) >= 1

def test_get_scenarios_blocked_category():
    cats = get_scenarios_by_category("blocked")
    assert len(cats) >= 1

def test_get_scenarios_observe_category():
    cats = get_scenarios_by_category("observe")
    assert len(cats) >= 1

def test_get_scenarios_unknown_category_empty():
    cats = get_scenarios_by_category("nonexistent_category_xyz")
    assert cats == []

def test_get_scenarios_entry_allowed_action():
    cats = get_scenarios_by_category("entry_allowed")
    assert all(s["expected_action"] == "PAPER_ENTRY_ALLOWED" for s in cats)

def test_get_scenarios_blocked_action():
    cats = get_scenarios_by_category("blocked")
    assert all(s["expected_action"] == "BLOCKED" for s in cats)


# ── get_scenario_categories() ─────────────────────────────────────────────────

def test_get_scenario_categories_is_list():
    assert isinstance(get_scenario_categories(), list)

def test_get_scenario_categories_ge_5():
    assert len(get_scenario_categories()) >= 5

def test_get_scenario_categories_contains_entry_allowed():
    assert "entry_allowed" in get_scenario_categories()

def test_get_scenario_categories_contains_blocked():
    assert "blocked" in get_scenario_categories()

def test_get_scenario_categories_contains_observe():
    assert "observe" in get_scenario_categories()

def test_get_scenario_categories_unique():
    cats = get_scenario_categories()
    assert len(cats) == len(set(cats))


# ── get_scenario_ids() ────────────────────────────────────────────────────────

def test_get_scenario_ids_is_list():
    assert isinstance(get_scenario_ids(), list)

def test_get_scenario_ids_count_75():
    assert len(get_scenario_ids()) == 75

def test_get_scenario_ids_sm181_001_in_list():
    assert "SM181-001" in get_scenario_ids()

def test_get_scenario_ids_sm181_075_in_list():
    assert "SM181-075" in get_scenario_ids()

def test_get_scenario_ids_unique():
    ids = get_scenario_ids()
    assert len(ids) == len(set(ids))


# ── get_scenarios_info() ──────────────────────────────────────────────────────

def test_get_scenarios_info_is_dict():
    assert isinstance(get_scenarios_info(), dict)

def test_get_scenarios_info_count():
    info = get_scenarios_info()
    assert info["count"] >= 75

def test_get_scenarios_info_paper_only():
    assert get_scenarios_info()["paper_only"] is True

def test_get_scenarios_info_stress_test_only():
    assert get_scenarios_info()["stress_test_only"] is True

def test_get_scenarios_info_no_real_orders():
    assert get_scenarios_info()["no_real_orders"] is True


# ── Parametrized: all scenario IDs have SM181 prefix ─────────────────────────

@pytest.mark.parametrize("idx", list(range(1, 76)))
def test_scenario_ids_format(idx):
    sid = f"SM181-{idx:03d}"
    scenario = get_scenario_by_id(sid)
    assert scenario is not None, f"Scenario {sid} not found"
    assert scenario["paper_only"] is True
