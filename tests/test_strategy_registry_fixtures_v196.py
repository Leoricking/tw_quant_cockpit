"""
tests/test_strategy_registry_fixtures_v196.py
Tests for strategy_registry_fixtures_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_fixtures_v196 import (
    get_all_fixtures,
    get_fixture_count,
    get_fixture_by_id,
)


# ── count ─────────────────────────────────────────────────────────────────────

def test_fixtures_count_75():
    assert len(get_all_fixtures()) == 75

def test_fixture_count_fn_75():
    assert get_fixture_count() == 75


# ── structure ─────────────────────────────────────────────────────────────────

def test_fixtures_is_list():
    assert isinstance(get_all_fixtures(), list)

def test_fixtures_each_is_dict():
    for f in get_all_fixtures():
        assert isinstance(f, dict)

def test_fixtures_all_have_id():
    for f in get_all_fixtures():
        assert "id" in f


# ── safety flags ──────────────────────────────────────────────────────────────

def test_fixtures_all_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())

def test_fixtures_all_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())

def test_fixtures_all_schema_196():
    assert all(f["schema_version"] == "196" for f in get_all_fixtures())

def test_fixtures_all_governance_only():
    assert all(f["governance_only"] is True for f in get_all_fixtures())

def test_fixtures_all_registry_only():
    assert all(f["registry_only"] is True for f in get_all_fixtures())

def test_fixtures_all_decision_record_only():
    assert all(f["decision_record_only"] is True for f in get_all_fixtures())

def test_fixtures_all_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())

def test_fixtures_all_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())

def test_fixtures_all_no_margin():
    assert all(f["no_margin"] is True for f in get_all_fixtures())

def test_fixtures_all_no_leverage():
    assert all(f["no_leverage"] is True for f in get_all_fixtures())


# ── get_fixture_by_id ─────────────────────────────────────────────────────────

def test_get_fixture_by_id_first():
    f = get_fixture_by_id("SMF196-001")
    assert f is not None
    assert f["id"] == "SMF196-001"

def test_get_fixture_by_id_last():
    f = get_fixture_by_id("SMF196-075")
    assert f is not None
    assert f["id"] == "SMF196-075"

def test_get_fixture_by_id_missing_returns_none():
    assert get_fixture_by_id("SMF196-999") is None


# ── unique ids ────────────────────────────────────────────────────────────────

def test_fixture_ids_are_unique():
    ids = [f["id"] for f in get_all_fixtures()]
    assert len(ids) == len(set(ids))
