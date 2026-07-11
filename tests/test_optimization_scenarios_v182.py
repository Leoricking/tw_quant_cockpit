"""
tests/test_optimization_scenarios_v182.py
Tests for optimization scenarios v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_scenarios_v182 import (
    get_scenario_count, get_all_scenarios, get_scenario_by_id,
    get_scenarios_by_category, get_scenario_categories, get_scenario_ids,
    get_scenarios_info,
)

_VALID_ACTIONS = {
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
}

_ALL_IDS = [f"OP182-{i:03d}" for i in range(1, 76)]


# --- Counts ---
def test_scenario_count_75():
    assert get_scenario_count() == 75

def test_all_scenarios_count_75():
    assert len(get_all_scenarios()) == 75

def test_scenario_ids_count_75():
    assert len(get_scenario_ids()) == 75


# --- Types ---
def test_all_scenarios_list():
    assert isinstance(get_all_scenarios(), list)

def test_scenario_ids_list():
    assert isinstance(get_scenario_ids(), list)


# --- Categories ---
def test_categories_10():
    assert len(get_scenario_categories()) == 10

def test_categories_parameter_valid():
    assert "parameter_valid" in get_scenario_categories()

def test_categories_parameter_blocked():
    assert "parameter_blocked" in get_scenario_categories()

def test_categories_walk_forward_pass():
    assert "walk_forward_pass" in get_scenario_categories()

def test_categories_walk_forward_fail():
    assert "walk_forward_fail" in get_scenario_categories()

def test_categories_overfitting_low():
    assert "overfitting_low" in get_scenario_categories()

def test_categories_overfitting_high():
    assert "overfitting_high" in get_scenario_categories()

def test_categories_stability_check():
    assert "stability_check" in get_scenario_categories()

def test_categories_sensitivity_high():
    assert "sensitivity_high" in get_scenario_categories()

def test_categories_regime_dependency():
    assert "regime_dependency" in get_scenario_categories()

def test_categories_robustness_ranking():
    assert "robustness_ranking" in get_scenario_categories()


# --- Category counts ---
def test_parameter_valid_count_10():
    assert len(get_scenarios_by_category("parameter_valid")) == 10

def test_parameter_blocked_count_12():
    assert len(get_scenarios_by_category("parameter_blocked")) == 12

def test_walk_forward_pass_count_8():
    assert len(get_scenarios_by_category("walk_forward_pass")) == 8

def test_walk_forward_fail_count_8():
    assert len(get_scenarios_by_category("walk_forward_fail")) == 8

def test_overfitting_low_count_7():
    assert len(get_scenarios_by_category("overfitting_low")) == 7

def test_overfitting_high_count_7():
    assert len(get_scenarios_by_category("overfitting_high")) == 7

def test_stability_check_count_8():
    assert len(get_scenarios_by_category("stability_check")) == 8

def test_sensitivity_high_count_7():
    assert len(get_scenarios_by_category("sensitivity_high")) == 7

def test_regime_dependency_count_5():
    assert len(get_scenarios_by_category("regime_dependency")) == 5

def test_robustness_ranking_count_3():
    assert len(get_scenarios_by_category("robustness_ranking")) == 3


# --- get_scenario_by_id ---
def test_get_scenario_first():
    s = get_scenario_by_id("OP182-001")
    assert s is not None
    assert s["id"] == "OP182-001"

def test_get_scenario_last():
    s = get_scenario_by_id("OP182-075")
    assert s is not None
    assert s["id"] == "OP182-075"

def test_get_scenario_not_found():
    assert get_scenario_by_id("OP999-999") is None


# --- get_scenarios_info ---
def test_info_count():
    assert get_scenarios_info()["count"] == 75

def test_info_paper_only():
    assert get_scenarios_info()["paper_only"] is True

def test_info_validation_only():
    assert get_scenarios_info()["validation_only"] is True

def test_info_no_real_orders():
    assert get_scenarios_info()["no_real_orders"] is True


# --- Field checks ---
def test_all_scenarios_have_id():
    for s in get_all_scenarios():
        assert "id" in s

def test_all_scenarios_have_category():
    for s in get_all_scenarios():
        assert "category" in s

def test_all_scenarios_have_expected_action():
    for s in get_all_scenarios():
        assert "expected_action" in s

def test_all_scenarios_have_market_regime():
    for s in get_all_scenarios():
        assert "market_regime" in s

def test_all_scenarios_paper_only():
    for s in get_all_scenarios():
        assert s["paper_only"] is True

def test_all_scenarios_research_only():
    for s in get_all_scenarios():
        assert s["research_only"] is True

def test_all_scenarios_validation_only():
    for s in get_all_scenarios():
        assert s["validation_only"] is True

def test_all_scenarios_no_real_orders():
    for s in get_all_scenarios():
        assert s["no_real_orders"] is True

def test_all_scenarios_not_investment_advice():
    for s in get_all_scenarios():
        assert s["not_investment_advice"] is True

def test_all_scenarios_stress_test_only():
    for s in get_all_scenarios():
        assert s["stress_test_only"] is True


# --- IDs format ---
def test_all_ids_start_with_op182():
    for sid in get_scenario_ids():
        assert sid.startswith("OP182-")

def test_ids_sequential():
    ids = get_scenario_ids()
    for i, sid in enumerate(ids):
        assert sid == f"OP182-{i+1:03d}"


# --- Actions valid ---
def test_all_actions_valid():
    for s in get_all_scenarios():
        assert s["expected_action"] in _VALID_ACTIONS, \
            f"{s['id']}: invalid action {s['expected_action']}"


# --- Parametrized ---
@pytest.mark.parametrize("scenario_id", _ALL_IDS)
def test_scenario_exists(scenario_id):
    s = get_scenario_by_id(scenario_id)
    assert s is not None

@pytest.mark.parametrize("scenario_id", _ALL_IDS)
def test_scenario_paper_only(scenario_id):
    s = get_scenario_by_id(scenario_id)
    assert s["paper_only"] is True

@pytest.mark.parametrize("scenario_id", _ALL_IDS)
def test_scenario_action_valid(scenario_id):
    s = get_scenario_by_id(scenario_id)
    assert s["expected_action"] in _VALID_ACTIONS
