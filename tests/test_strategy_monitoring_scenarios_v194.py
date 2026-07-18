"""
tests/test_strategy_monitoring_scenarios_v194.py
Tests for strategy_monitoring_scenarios_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_scenarios_v194 import (
    get_all_scenarios, get_scenario_by_id, get_scenario_ids,
    get_scenarios_by_type, get_blocked_scenarios, get_drift_scenarios,
)


# ── count ─────────────────────────────────────────────────────────────────────

def test_scenarios_count_75():
    assert len(get_all_scenarios()) == 75


def test_scenarios_min_75():
    assert len(get_all_scenarios()) >= 75


def test_scenario_ids_count():
    assert len(get_scenario_ids()) == 75


# ── safety flags ──────────────────────────────────────────────────────────────

def test_all_scenarios_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())


def test_all_scenarios_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())


def test_all_scenarios_monitoring_only():
    assert all(s["monitoring_only"] is True for s in get_all_scenarios())


def test_all_scenarios_not_investment_advice():
    assert all(s["not_investment_advice"] is True for s in get_all_scenarios())


def test_all_scenarios_drift_detection_only():
    assert all(s["drift_detection_only"] is True for s in get_all_scenarios())


# ── scenario structure ────────────────────────────────────────────────────────

def test_all_scenarios_have_scenario_id():
    assert all("scenario_id" in s for s in get_all_scenarios())


def test_all_scenarios_have_name():
    assert all("name" in s for s in get_all_scenarios())


def test_all_scenarios_have_scenario_type():
    assert all("scenario_type" in s for s in get_all_scenarios())


def test_all_scenarios_have_expected_outcome():
    assert all("expected_outcome" in s for s in get_all_scenarios())


def test_all_scenarios_have_schema_version():
    assert all(s.get("schema_version") == "194" for s in get_all_scenarios())


# ── scenario IDs ──────────────────────────────────────────────────────────────

def test_scenario_ids_start_with_sp194():
    assert all(sid.startswith("SP194-") for sid in get_scenario_ids())


def test_scenario_first_id():
    assert "SP194-001" in get_scenario_ids()


def test_scenario_last_id():
    assert "SP194-075" in get_scenario_ids()


def test_scenario_ids_unique():
    ids = get_scenario_ids()
    assert len(ids) == len(set(ids))


# ── get_scenario_by_id ────────────────────────────────────────────────────────

def test_get_scenario_by_id_001():
    s = get_scenario_by_id("SP194-001")
    assert s["scenario_id"] == "SP194-001"


def test_get_scenario_by_id_075():
    s = get_scenario_by_id("SP194-075")
    assert s["scenario_id"] == "SP194-075"


def test_get_scenario_by_id_missing_returns_empty():
    result = get_scenario_by_id("SP194-999")
    assert result == {} or result is None


def test_get_scenario_by_id_paper_only():
    s = get_scenario_by_id("SP194-001")
    assert s["paper_only"] is True


# ── get_scenarios_by_type ─────────────────────────────────────────────────────

def test_get_scenarios_by_type_complete_monitoring():
    result = get_scenarios_by_type("complete_monitoring")
    assert len(result) >= 1


def test_get_scenarios_by_type_healthy_monitoring():
    result = get_scenarios_by_type("healthy_monitoring")
    assert isinstance(result, list)


def test_get_scenarios_by_type_drift_detection():
    result = get_scenarios_by_type("drift_detection")
    assert len(result) >= 1


def test_get_scenarios_by_type_rollback_alert():
    result = get_scenarios_by_type("rollback_alert")
    assert len(result) >= 1


def test_get_scenarios_by_type_monitoring_recommendation():
    result = get_scenarios_by_type("monitoring_recommendation")
    assert isinstance(result, list)


def test_get_scenarios_by_type_safety_block():
    result = get_scenarios_by_type("safety_block")
    assert len(result) >= 1


def test_get_scenarios_by_type_unknown_empty():
    result = get_scenarios_by_type("unknown_type_xyz")
    assert result == []


# ── get_blocked_scenarios ─────────────────────────────────────────────────────

def test_get_blocked_scenarios_returns_list():
    assert isinstance(get_blocked_scenarios(), list)


def test_get_blocked_scenarios_all_blocked():
    blocked = get_blocked_scenarios()
    assert len(blocked) >= 1
    assert all(s.get("blocked") is True for s in blocked)


# ── get_drift_scenarios ───────────────────────────────────────────────────────

def test_get_drift_scenarios_returns_list():
    assert isinstance(get_drift_scenarios(), list)


def test_get_drift_scenarios_have_drift_detected():
    drift = get_drift_scenarios()
    assert len(drift) >= 1
    assert all(s.get("drift_detected") is True for s in drift)


# ── auto_rollback not present ─────────────────────────────────────────────────

def test_no_scenario_has_auto_rollback_true():
    for s in get_all_scenarios():
        assert s.get("auto_rollback", False) is not True
