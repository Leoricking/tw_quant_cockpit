"""
tests/test_strategy_registry_scenarios_v196.py
Tests for strategy_registry_scenarios_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_scenarios_v196 import (
    get_all_scenarios,
    get_scenario_count,
    get_scenario_by_id,
    get_scenarios_by_category,
    get_scenario_categories,
)


# ── count ─────────────────────────────────────────────────────────────────────

def test_scenarios_count_75():
    assert len(get_all_scenarios()) == 75

def test_scenario_count_fn_75():
    assert get_scenario_count() == 75


# ── structure ─────────────────────────────────────────────────────────────────

def test_scenarios_is_list():
    assert isinstance(get_all_scenarios(), list)

def test_scenarios_each_is_dict():
    for s in get_all_scenarios():
        assert isinstance(s, dict)

def test_scenarios_all_have_id():
    for s in get_all_scenarios():
        assert "id" in s

def test_scenarios_all_have_category():
    for s in get_all_scenarios():
        assert "category" in s


# ── safety flags ──────────────────────────────────────────────────────────────

def test_scenarios_all_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())

def test_scenarios_all_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())

def test_scenarios_all_schema_196():
    assert all(s["schema_version"] == "196" for s in get_all_scenarios())

def test_scenarios_all_governance_only():
    assert all(s["governance_only"] is True for s in get_all_scenarios())


# ── get_scenario_by_id ────────────────────────────────────────────────────────

def test_get_scenario_by_id_first():
    s = get_scenario_by_id("SP196-001")
    assert s["id"] == "SP196-001"

def test_get_scenario_by_id_last():
    s = get_scenario_by_id("SP196-075")
    assert s["id"] == "SP196-075"

def test_get_scenario_by_id_missing_returns_empty():
    assert get_scenario_by_id("SP196-999") == {}


# ── get_scenarios_by_category ─────────────────────────────────────────────────

def test_scenarios_have_complete_registry_category():
    assert len(get_scenarios_by_category("complete_registry")) >= 1

def test_scenarios_have_approved_for_paper_category():
    assert len(get_scenarios_by_category("approved_for_paper")) >= 1

def test_scenarios_have_hard_block_category():
    assert len(get_scenarios_by_category("hard_block")) >= 1

def test_scenarios_have_governance_evidence_category():
    assert len(get_scenarios_by_category("governance_evidence")) >= 1


# ── get_scenario_categories ───────────────────────────────────────────────────

def test_scenario_categories_is_list():
    assert isinstance(get_scenario_categories(), list)

def test_scenario_categories_not_empty():
    assert len(get_scenario_categories()) > 0

def test_scenario_categories_contains_expected():
    cats = get_scenario_categories()
    assert "complete_registry" in cats or "approved_for_paper" in cats


# ── unique ids ────────────────────────────────────────────────────────────────

def test_scenario_ids_are_unique():
    ids = [s["id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))
