"""
tests/test_monte_carlo_scenarios_v183.py
Tests for Monte Carlo scenario registry (75 scenarios) v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.monte_carlo_scenarios_v183 import (
    get_scenario_count,
    get_all_scenarios,
    get_scenario_by_id,
    get_scenario_categories,
    get_scenarios_by_category,
    get_scenario_ids,
    get_scenarios_info,
)


# ---------------------------------------------------------------------------
# Counts and types
# ---------------------------------------------------------------------------

def test_get_scenario_count_returns_int():
    assert isinstance(get_scenario_count(), int)


def test_get_scenario_count_equals_75():
    assert get_scenario_count() == 75


def test_get_all_scenarios_returns_list():
    assert isinstance(get_all_scenarios(), list)


def test_get_all_scenarios_length_75():
    assert len(get_all_scenarios()) == 75


# ---------------------------------------------------------------------------
# IDs
# ---------------------------------------------------------------------------

def test_get_scenario_ids_returns_list():
    assert isinstance(get_scenario_ids(), list)


def test_get_scenario_ids_length_75():
    assert len(get_scenario_ids()) == 75


def test_get_scenario_ids_first():
    assert get_scenario_ids()[0] == "MC183-001"


def test_get_scenario_ids_last():
    assert get_scenario_ids()[-1] == "MC183-075"


# ---------------------------------------------------------------------------
# get_scenario_by_id()
# ---------------------------------------------------------------------------

def test_get_scenario_by_id_mc183_001_not_none():
    assert get_scenario_by_id("MC183-001") is not None


def test_get_scenario_by_id_mc183_001_category():
    assert get_scenario_by_id("MC183-001")["category"] == "monte_carlo_robust"


def test_get_scenario_by_id_mc183_075_not_none():
    assert get_scenario_by_id("MC183-075") is not None


def test_get_scenario_by_id_mc183_075_category():
    assert get_scenario_by_id("MC183-075")["category"] == "robustness_ranking"


def test_get_scenario_by_id_unknown_returns_none():
    assert get_scenario_by_id("UNKNOWN-999") is None


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

def test_get_scenario_categories_returns_list():
    assert isinstance(get_scenario_categories(), list)


def test_get_scenario_categories_count_10():
    assert len(get_scenario_categories()) == 10


def test_get_scenario_categories_contains_monte_carlo_robust():
    assert "monte_carlo_robust" in get_scenario_categories()


def test_get_scenario_categories_contains_monte_carlo_blocked():
    assert "monte_carlo_blocked" in get_scenario_categories()


def test_get_scenario_categories_contains_risk_of_ruin_low():
    assert "risk_of_ruin_low" in get_scenario_categories()


def test_get_scenario_categories_contains_risk_of_ruin_high():
    assert "risk_of_ruin_high" in get_scenario_categories()


def test_get_scenario_categories_contains_bootstrap_pass():
    assert "bootstrap_pass" in get_scenario_categories()


def test_get_scenario_categories_contains_bootstrap_fail():
    assert "bootstrap_fail" in get_scenario_categories()


def test_get_scenario_categories_contains_robustness_ranking():
    assert "robustness_ranking" in get_scenario_categories()


# ---------------------------------------------------------------------------
# get_scenarios_by_category()
# ---------------------------------------------------------------------------

def test_get_scenarios_by_category_monte_carlo_robust_count():
    assert len(get_scenarios_by_category("monte_carlo_robust")) == 10


def test_get_scenarios_by_category_monte_carlo_blocked_count():
    assert len(get_scenarios_by_category("monte_carlo_blocked")) == 10


def test_get_scenarios_by_category_robustness_ranking_count():
    assert len(get_scenarios_by_category("robustness_ranking")) == 12


def test_get_scenarios_by_category_unknown_returns_empty():
    assert get_scenarios_by_category("unknown_cat") == []


# ---------------------------------------------------------------------------
# Safety flags on all scenarios
# ---------------------------------------------------------------------------

def test_all_scenarios_paper_only():
    for s in get_all_scenarios():
        assert s["paper_only"] is True, f"{s['id']} missing paper_only"


def test_all_scenarios_monte_carlo_only():
    for s in get_all_scenarios():
        assert s["monte_carlo_only"] is True, f"{s['id']} missing monte_carlo_only"


def test_all_scenarios_no_real_orders():
    for s in get_all_scenarios():
        assert s["no_real_orders"] is True, f"{s['id']} missing no_real_orders"


def test_all_scenarios_production_trading_blocked():
    for s in get_all_scenarios():
        assert s["production_trading_blocked"] is True, f"{s['id']} missing production_trading_blocked"


# ---------------------------------------------------------------------------
# get_scenarios_info()
# ---------------------------------------------------------------------------

def test_get_scenarios_info_count():
    assert get_scenarios_info()["count"] == 75


def test_get_scenarios_info_paper_only():
    assert get_scenarios_info()["paper_only"] is True
