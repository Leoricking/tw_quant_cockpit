"""tests/test_strategy_sandbox_fixtures_v192.py
Tests for strategy sandbox fixtures v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_fixtures_v192 import (
    FIXTURES, get_all_fixtures, get_fixture_by_id,
)


# ── Count ─────────────────────────────────────────────────────────────────────

def test_get_all_fixtures_count_75():
    assert len(get_all_fixtures()) == 75

def test_fixtures_constant_count_75():
    assert len(FIXTURES) == 75


# ── Universal safety flags ────────────────────────────────────────────────────

def test_all_fixtures_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())

def test_all_fixtures_sandbox_only():
    assert all(f["sandbox_only"] is True for f in get_all_fixtures())

def test_all_fixtures_shadow_only():
    assert all(f["shadow_only"] is True for f in get_all_fixtures())

def test_all_fixtures_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())

def test_all_fixtures_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())

def test_all_fixtures_no_margin():
    assert all(f["no_margin"] is True for f in get_all_fixtures())

def test_all_fixtures_no_leverage():
    assert all(f["no_leverage"] is True for f in get_all_fixtures())

def test_all_fixtures_no_production_strategy_mutation():
    assert all(f["no_production_strategy_mutation"] is True for f in get_all_fixtures())

def test_all_fixtures_no_live_strategy_activation():
    assert all(f["no_live_strategy_activation"] is True for f in get_all_fixtures())

def test_all_fixtures_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())

def test_all_fixtures_demo_only():
    assert all(f["demo_only"] is True for f in get_all_fixtures())

def test_all_fixtures_not_for_production():
    assert all(f["not_for_production"] is True for f in get_all_fixtures())

def test_all_fixtures_production_trading_blocked():
    assert all(f["production_trading_blocked"] is True for f in get_all_fixtures())

def test_all_fixtures_schema_version_192():
    assert all(f["schema_version"] == "192" for f in get_all_fixtures())


# ── Required fixture fields ───────────────────────────────────────────────────

def test_all_fixtures_have_fixture_id():
    assert all("fixture_id" in f for f in get_all_fixtures())

def test_all_fixtures_have_sandbox_id():
    assert all("sandbox_id" in f for f in get_all_fixtures())

def test_all_fixtures_have_baseline_snapshot_id():
    assert all("baseline_snapshot_id" in f for f in get_all_fixtures())

def test_all_fixtures_have_candidate_snapshot_id():
    assert all("candidate_snapshot_id" in f for f in get_all_fixtures())

def test_all_fixtures_have_sandbox_mode():
    assert all("sandbox_mode" in f for f in get_all_fixtures())

def test_all_fixtures_have_approval_state():
    assert all("approval_state" in f for f in get_all_fixtures())

def test_all_fixtures_have_recommendation():
    assert all("recommendation" in f for f in get_all_fixtures())

def test_all_fixtures_have_evidence_count():
    assert all("evidence_count" in f for f in get_all_fixtures())

def test_all_fixtures_have_tuning_proposal_source():
    assert all("tuning_proposal_source" in f for f in get_all_fixtures())


# ── get_fixture_by_id ─────────────────────────────────────────────────────────

def test_get_fixture_by_id_001_not_none():
    assert get_fixture_by_id("SSF192-001") is not None

def test_get_fixture_by_id_075_not_none():
    assert get_fixture_by_id("SSF192-075") is not None

def test_get_fixture_by_id_nonexistent_is_none():
    assert get_fixture_by_id("SSF192-999") is None

def test_get_fixture_by_id_empty_is_none():
    assert get_fixture_by_id("") is None

def test_get_fixture_by_id_001_is_dict():
    result = get_fixture_by_id("SSF192-001")
    assert isinstance(result, dict)

def test_get_fixture_by_id_001_paper_only():
    result = get_fixture_by_id("SSF192-001")
    assert result["paper_only"] is True

def test_get_fixture_by_id_001_schema_192():
    result = get_fixture_by_id("SSF192-001")
    assert result["schema_version"] == "192"


# ── Unique fixture IDs ────────────────────────────────────────────────────────

def test_all_fixture_ids_unique():
    ids = [f["fixture_id"] for f in get_all_fixtures()]
    assert len(ids) == len(set(ids))

def test_fixture_ids_follow_ssf192_pattern():
    ids = [f["fixture_id"] for f in get_all_fixtures()]
    assert all(fid.startswith("SSF192-") for fid in ids)


# ── Sandbox IDs not empty ─────────────────────────────────────────────────────

def test_all_fixture_sandbox_ids_not_empty():
    assert all(f["sandbox_id"] != "" for f in get_all_fixtures())

def test_all_fixture_baseline_snapshot_ids_not_empty():
    assert all(f["baseline_snapshot_id"] != "" for f in get_all_fixtures())

def test_all_fixture_candidate_snapshot_ids_not_empty():
    assert all(f["candidate_snapshot_id"] != "" for f in get_all_fixtures())

def test_all_fixture_evidence_count_positive():
    assert all(f["evidence_count"] > 0 for f in get_all_fixtures())
