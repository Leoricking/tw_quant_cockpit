"""tests/test_strategy_promotion_fixtures_v193.py — v1.9.3 fixture tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_fixtures_v193 import (
    get_all_fixtures, get_fixture_by_id, get_fixtures_by_approval_state,
)


# ── count ─────────────────────────────────────────────────────────────────────
def test_fixtures_count_75(): assert len(get_all_fixtures()) == 75

# ── safety flags on all ───────────────────────────────────────────────────────
def test_all_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())

def test_all_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())

def test_all_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())

def test_all_promotion_package_only():
    assert all(f["promotion_package_only"] is True for f in get_all_fixtures())

def test_all_rollback_plan_only():
    assert all(f["rollback_plan_only"] is True for f in get_all_fixtures())

def test_all_no_margin():
    assert all(f["no_margin"] is True for f in get_all_fixtures())

def test_all_no_leverage():
    assert all(f["no_leverage"] is True for f in get_all_fixtures())

def test_all_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())

def test_all_demo_only():
    assert all(f["demo_only"] is True for f in get_all_fixtures())

def test_all_not_for_production():
    assert all(f["not_for_production"] is True for f in get_all_fixtures())

def test_all_production_trading_blocked():
    assert all(f["production_trading_blocked"] is True for f in get_all_fixtures())

def test_all_schema_193():
    assert all(f["schema_version"] == "193" for f in get_all_fixtures())

# ── IDs ───────────────────────────────────────────────────────────────────────
def test_first_fixture_id():
    fixtures = get_all_fixtures()
    assert fixtures[0]["fixture_id"] == "SPF193-001"

def test_last_fixture_id():
    fixtures = get_all_fixtures()
    assert fixtures[-1]["fixture_id"] == "SPF193-075"

def test_fixture_ids_unique():
    ids = [f["fixture_id"] for f in get_all_fixtures()]
    assert len(ids) == len(set(ids))

# ── get_fixture_by_id ─────────────────────────────────────────────────────────
def test_get_fixture_by_id_001():
    f = get_fixture_by_id("SPF193-001")
    assert f is not None
    assert f["fixture_id"] == "SPF193-001"

def test_get_fixture_by_id_075():
    f = get_fixture_by_id("SPF193-075")
    assert f is not None
    assert f["fixture_id"] == "SPF193-075"

def test_get_fixture_by_id_not_found():
    assert get_fixture_by_id("SPF193-999") is None

def test_get_fixture_by_id_paper_only():
    f = get_fixture_by_id("SPF193-010")
    assert f["paper_only"] is True

# ── get_fixtures_by_approval_state ───────────────────────────────────────────
def test_fixtures_by_approval_state_draft():
    results = get_fixtures_by_approval_state("DRAFT")
    assert isinstance(results, list)
    assert all(f["approval_state"] == "DRAFT" for f in results)

def test_fixtures_by_approval_state_paper_ready():
    results = get_fixtures_by_approval_state("PAPER_PROMOTION_READY")
    assert isinstance(results, list)

def test_fixtures_by_approval_state_blocked():
    results = get_fixtures_by_approval_state("BLOCKED")
    assert isinstance(results, list)

def test_fixtures_by_unknown_state():
    results = get_fixtures_by_approval_state("NONEXISTENT_STATE")
    assert results == []

# ── fields present ────────────────────────────────────────────────────────────
def test_fixture_has_approval_state():
    f = get_fixture_by_id("SPF193-001")
    assert "approval_state" in f

def test_fixture_has_recommendation():
    f = get_fixture_by_id("SPF193-001")
    assert "recommendation" in f

def test_fixture_has_rollback_trigger():
    f = get_fixture_by_id("SPF193-001")
    assert "rollback_trigger" in f

def test_fixture_returns_list():
    assert isinstance(get_all_fixtures(), list)
