"""tests/test_strategy_promotion_scenarios_v193.py — v1.9.3 scenario tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_scenarios_v193 import (
    get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
)


# ── count ─────────────────────────────────────────────────────────────────────
def test_scenarios_count_75(): assert len(get_all_scenarios()) == 75

# ── safety flags on all ───────────────────────────────────────────────────────
def test_all_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())

def test_all_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())

def test_all_no_broker():
    assert all(s["no_broker"] is True for s in get_all_scenarios())

def test_all_promotion_package_only():
    assert all(s["promotion_package_only"] is True for s in get_all_scenarios())

def test_all_rollback_plan_only():
    assert all(s["rollback_plan_only"] is True for s in get_all_scenarios())

def test_all_schema_193():
    assert all(s["schema_version"] == "193" for s in get_all_scenarios())

# ── IDs ───────────────────────────────────────────────────────────────────────
def test_first_scenario_id():
    assert get_all_scenarios()[0]["scenario_id"] == "SP193-001"

def test_last_scenario_id():
    assert get_all_scenarios()[-1]["scenario_id"] == "SP193-075"

def test_scenario_ids_unique():
    ids = [s["scenario_id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))

# ── get_scenario_by_id ────────────────────────────────────────────────────────
def test_get_scenario_001():
    s = get_scenario_by_id("SP193-001")
    assert s is not None
    assert s["scenario_id"] == "SP193-001"

def test_get_scenario_075():
    s = get_scenario_by_id("SP193-075")
    assert s is not None

def test_get_scenario_not_found():
    assert get_scenario_by_id("SP193-999") is None

# ── get_scenarios_by_type ─────────────────────────────────────────────────────
def test_complete_promotion_package_type():
    results = get_scenarios_by_type("complete_promotion_package")
    assert len(results) >= 1
    assert all(s["scenario_type"] == "complete_promotion_package" for s in results)

def test_rollback_to_baseline_type():
    results = get_scenarios_by_type("rollback_to_baseline")
    assert len(results) >= 1

def test_blocked_candidate_type():
    results = get_scenarios_by_type("blocked_candidate")
    assert isinstance(results, list)

def test_safety_audit_type():
    results = get_scenarios_by_type("safety_audit")
    assert isinstance(results, list)

def test_unknown_type_empty():
    results = get_scenarios_by_type("nonexistent_type_xyz")
    assert results == []

def test_missing_sandbox_validation_blocked():
    results = get_scenarios_by_type("missing_sandbox_validation_blocked")
    assert isinstance(results, list)

def test_missing_rollback_plan_blocked():
    results = get_scenarios_by_type("missing_rollback_plan_blocked")
    assert isinstance(results, list)

def test_evidence_pack_complete():
    results = get_scenarios_by_type("evidence_pack_complete")
    assert isinstance(results, list)

def test_keep_baseline_type():
    results = get_scenarios_by_type("keep_baseline")
    assert isinstance(results, list)

# ── fields present ────────────────────────────────────────────────────────────
def test_scenario_has_type():
    s = get_scenario_by_id("SP193-001")
    assert "scenario_type" in s

def test_scenario_returns_list():
    assert isinstance(get_all_scenarios(), list)

def test_scenarios_by_type_returns_list():
    assert isinstance(get_scenarios_by_type("rollback_to_baseline"), list)
