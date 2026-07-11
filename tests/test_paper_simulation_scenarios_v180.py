"""tests/test_paper_simulation_scenarios_v180.py — v1.8.0 Paper Simulation scenario tests"""
from __future__ import annotations

import pytest

from paper_trading.small_capital_strategy.paper_simulation_scenarios_v180 import (
    get_scenario_count,
    get_all_scenarios,
    get_scenario_by_id,
    get_scenarios_by_category,
    get_scenario_categories,
    get_scenarios_info,
    get_scenario_ids,
)


# ---------------------------------------------------------------------------
# Count tests
# ---------------------------------------------------------------------------

def test_scenario_count_at_least_70() -> None:
    assert get_scenario_count() >= 70


def test_scenario_count_equals_70() -> None:
    assert get_scenario_count() == 70


def test_get_all_scenarios_length_70() -> None:
    assert len(get_all_scenarios()) == 70


# ---------------------------------------------------------------------------
# get_scenario_by_id
# ---------------------------------------------------------------------------

def test_get_scenario_by_id_sc180_001_exists() -> None:
    assert get_scenario_by_id("SC180-001") is not None


def test_get_scenario_by_id_sc180_070_exists() -> None:
    assert get_scenario_by_id("SC180-070") is not None


def test_get_scenario_by_id_fake_id_returns_none() -> None:
    assert get_scenario_by_id("SC180-999") is None


def test_get_scenario_by_id_sc180_001_expected_action() -> None:
    s = get_scenario_by_id("SC180-001")
    assert s["expected_action"] == "PAPER_ENTRY_ALLOWED"


def test_get_scenario_by_id_sc180_011_blocked() -> None:
    s = get_scenario_by_id("SC180-011")
    assert s["expected_action"] == "BLOCKED"


def test_get_scenario_by_id_sc180_021_observe() -> None:
    s = get_scenario_by_id("SC180-021")
    assert s["expected_action"] == "OBSERVE"


def test_get_scenario_by_id_sc180_029_wait() -> None:
    s = get_scenario_by_id("SC180-029")
    assert s["expected_action"] == "WAIT"


def test_get_scenario_by_id_sc180_037_plan_ready() -> None:
    s = get_scenario_by_id("SC180-037")
    assert s["expected_action"] == "PAPER_PLAN_READY"


def test_get_scenario_by_id_sc180_044_reduce_risk() -> None:
    s = get_scenario_by_id("SC180-044")
    assert s["expected_action"] == "REDUCE_RISK"


def test_get_scenario_by_id_sc180_050_review_required() -> None:
    s = get_scenario_by_id("SC180-050")
    assert s["expected_action"] == "REVIEW_REQUIRED"


def test_get_scenario_by_id_sc180_056_no_trade() -> None:
    s = get_scenario_by_id("SC180-056")
    assert s["expected_action"] == "NO_TRADE"


def test_get_scenario_by_id_sc180_063_add_allowed() -> None:
    s = get_scenario_by_id("SC180-063")
    assert s["expected_action"] == "PAPER_ADD_ALLOWED"


# ---------------------------------------------------------------------------
# All scenarios structural checks
# ---------------------------------------------------------------------------

def test_all_scenarios_have_id_key() -> None:
    for s in get_all_scenarios():
        assert "id" in s


def test_all_scenario_ids_are_unique() -> None:
    ids = [s["id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))


def test_all_scenarios_have_expected_action() -> None:
    for s in get_all_scenarios():
        assert "expected_action" in s


def test_all_scenarios_paper_only_true() -> None:
    for s in get_all_scenarios():
        assert s["paper_only"] is True


def test_all_scenarios_research_only_true() -> None:
    for s in get_all_scenarios():
        assert s["research_only"] is True


def test_all_scenarios_no_real_orders_true() -> None:
    for s in get_all_scenarios():
        assert s["no_real_orders"] is True


def test_all_scenarios_no_broker_true() -> None:
    for s in get_all_scenarios():
        assert s["no_broker"] is True


def test_all_scenarios_not_investment_advice_true() -> None:
    for s in get_all_scenarios():
        assert s["not_investment_advice"] is True


def test_all_scenarios_demo_only_true() -> None:
    for s in get_all_scenarios():
        assert s["demo_only"] is True


def test_all_scenarios_not_for_production_true() -> None:
    for s in get_all_scenarios():
        assert s["not_for_production"] is True


def test_all_scenarios_simulate_only_true() -> None:
    for s in get_all_scenarios():
        assert s["simulate_only"] is True


# ---------------------------------------------------------------------------
# No forbidden actions
# ---------------------------------------------------------------------------

def test_no_scenario_expected_action_is_buy() -> None:
    for s in get_all_scenarios():
        assert s["expected_action"] != "BUY"


def test_no_scenario_expected_action_is_sell() -> None:
    for s in get_all_scenarios():
        assert s["expected_action"] != "SELL"


def test_no_scenario_expected_action_is_order() -> None:
    for s in get_all_scenarios():
        assert s["expected_action"] != "ORDER"


# ---------------------------------------------------------------------------
# get_scenarios_by_category counts
# ---------------------------------------------------------------------------

def test_entry_allowed_category_has_10() -> None:
    assert len(get_scenarios_by_category("entry_allowed")) == 10


def test_blocked_category_has_10() -> None:
    assert len(get_scenarios_by_category("blocked")) == 10


def test_observe_category_has_8() -> None:
    assert len(get_scenarios_by_category("observe")) == 8


def test_wait_category_has_8() -> None:
    assert len(get_scenarios_by_category("wait")) == 8


def test_plan_ready_category_has_7() -> None:
    assert len(get_scenarios_by_category("plan_ready")) == 7


def test_reduce_risk_category_has_6() -> None:
    assert len(get_scenarios_by_category("reduce_risk")) == 6


def test_review_required_category_has_6() -> None:
    assert len(get_scenarios_by_category("review_required")) == 6


def test_no_trade_category_has_7() -> None:
    assert len(get_scenarios_by_category("no_trade")) == 7


def test_add_allowed_category_has_7() -> None:
    assert len(get_scenarios_by_category("add_allowed")) == 7


def test_fake_category_returns_empty_list() -> None:
    assert get_scenarios_by_category("FAKE_CATEGORY") == []


# ---------------------------------------------------------------------------
# get_scenario_categories
# ---------------------------------------------------------------------------

def test_get_scenario_categories_returns_list() -> None:
    assert isinstance(get_scenario_categories(), list)


def test_get_scenario_categories_at_least_5() -> None:
    assert len(get_scenario_categories()) >= 5


def test_entry_allowed_in_categories() -> None:
    assert "entry_allowed" in get_scenario_categories()


def test_blocked_in_categories() -> None:
    assert "blocked" in get_scenario_categories()


def test_observe_in_categories() -> None:
    assert "observe" in get_scenario_categories()


def test_wait_in_categories() -> None:
    assert "wait" in get_scenario_categories()


def test_no_trade_in_categories() -> None:
    assert "no_trade" in get_scenario_categories()


# ---------------------------------------------------------------------------
# get_scenarios_info
# ---------------------------------------------------------------------------

def test_get_scenarios_info_returns_dict() -> None:
    assert isinstance(get_scenarios_info(), dict)


def test_get_scenarios_info_paper_only_true() -> None:
    assert get_scenarios_info()["paper_only"] is True


def test_get_scenarios_info_count_equals_70() -> None:
    assert get_scenarios_info()["count"] == 70


def test_get_scenarios_info_no_real_orders_true() -> None:
    assert get_scenarios_info()["no_real_orders"] is True


def test_get_scenarios_info_research_only_true() -> None:
    assert get_scenarios_info()["research_only"] is True


def test_get_scenarios_info_categories_present() -> None:
    info = get_scenarios_info()
    assert "categories" in info


# ---------------------------------------------------------------------------
# get_scenario_ids
# ---------------------------------------------------------------------------

def test_get_scenario_ids_has_70_items() -> None:
    assert len(get_scenario_ids()) == 70


def test_all_scenario_ids_start_with_sc180() -> None:
    for sid in get_scenario_ids():
        assert sid.startswith("SC180-")


def test_scenario_ids_are_unique() -> None:
    ids = get_scenario_ids()
    assert len(ids) == len(set(ids))


def test_sc180_001_in_scenario_ids() -> None:
    assert "SC180-001" in get_scenario_ids()


def test_sc180_070_in_scenario_ids() -> None:
    assert "SC180-070" in get_scenario_ids()
