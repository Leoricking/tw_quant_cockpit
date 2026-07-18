"""
tests/test_strategy_review_scenarios_v195.py
Tests for strategy review scenarios v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_scenarios_v195 import (
    get_all_scenarios, get_scenario_by_id, get_scenario_ids,
    get_scenarios_by_type, get_blocked_scenarios,
    get_escalated_scenarios, get_drift_scenarios,
)


# ── get_all_scenarios ─────────────────────────────────────────────────────────

def test_scenarios_count_75():
    assert len(get_all_scenarios()) == 75


def test_scenarios_all_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())


def test_scenarios_all_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())


def test_scenarios_all_schema_version_195():
    assert all(s["schema_version"] == "195" for s in get_all_scenarios())


def test_scenarios_all_auto_approval_false():
    assert all(s["auto_approval"] is False for s in get_all_scenarios())


def test_scenarios_all_auto_rollback_false():
    assert all(s["auto_rollback"] is False for s in get_all_scenarios())


def test_scenarios_all_have_scenario_id():
    assert all("scenario_id" in s for s in get_all_scenarios())


def test_scenarios_all_have_scenario_type():
    assert all("scenario_type" in s for s in get_all_scenarios())


def test_scenarios_all_have_expected_outcome():
    assert all("expected_outcome" in s for s in get_all_scenarios())


# ── get_scenario_ids ──────────────────────────────────────────────────────────

def test_scenario_ids_count():
    assert len(get_scenario_ids()) == 75


def test_scenario_ids_unique():
    ids = get_scenario_ids()
    assert len(ids) == len(set(ids))


def test_scenario_ids_start_with_sp195():
    assert all(sid.startswith("SP195-") for sid in get_scenario_ids())


# ── get_scenario_by_id ────────────────────────────────────────────────────────

def test_get_scenario_by_id_first():
    s = get_scenario_by_id("SP195-001")
    assert s["scenario_id"] == "SP195-001"


def test_get_scenario_by_id_last():
    s = get_scenario_by_id("SP195-075")
    assert s["scenario_id"] == "SP195-075"


def test_get_scenario_by_id_missing_returns_empty():
    assert get_scenario_by_id("SP195-999") == {}


# ── get_scenarios_by_type ─────────────────────────────────────────────────────

def test_scenarios_by_type_complete_review():
    results = get_scenarios_by_type("complete_review")
    assert len(results) >= 1


def test_scenarios_by_type_safety_block():
    results = get_scenarios_by_type("safety_block")
    assert len(results) >= 1


def test_scenarios_by_type_manual_approval_required():
    results = get_scenarios_by_type("manual_approval_required")
    assert len(results) >= 1


def test_scenarios_by_type_rollback_review_ticket():
    results = get_scenarios_by_type("rollback_review_ticket")
    assert len(results) >= 1


def test_scenarios_by_type_unknown_empty():
    assert get_scenarios_by_type("does_not_exist_type") == []


# ── get_blocked_scenarios ─────────────────────────────────────────────────────

def test_blocked_scenarios_exist():
    assert len(get_blocked_scenarios()) > 0


def test_blocked_scenarios_all_blocked():
    assert all(s["blocked"] is True for s in get_blocked_scenarios())


# ── get_escalated_scenarios ───────────────────────────────────────────────────

def test_escalated_scenarios_exist():
    assert len(get_escalated_scenarios()) > 0


def test_escalated_scenarios_all_escalated():
    assert all(s["escalated"] is True for s in get_escalated_scenarios())


# ── get_drift_scenarios ───────────────────────────────────────────────────────

def test_drift_scenarios_exist():
    assert len(get_drift_scenarios()) > 0


def test_drift_scenarios_all_drift_detected():
    assert all(s["drift_detected"] is True for s in get_drift_scenarios())
