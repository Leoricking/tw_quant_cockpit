"""
tests/test_strategy_review_fixtures_v195.py
Tests for strategy review fixtures v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_fixtures_v195 import (
    get_all_fixtures, get_fixture_by_id, get_fixture_ids,
    get_fixtures_by_status, get_fixtures_by_severity,
    get_blocked_fixtures, get_escalated_fixtures, get_drift_fixtures,
)


# ── get_all_fixtures ──────────────────────────────────────────────────────────

def test_fixtures_count_75():
    assert len(get_all_fixtures()) == 75


def test_fixtures_all_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())


def test_fixtures_all_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())


def test_fixtures_all_schema_version_195():
    assert all(f["schema_version"] == "195" for f in get_all_fixtures())


def test_fixtures_all_auto_approval_false():
    assert all(f["auto_approval"] is False for f in get_all_fixtures())


def test_fixtures_all_auto_rollback_false():
    assert all(f["auto_rollback"] is False for f in get_all_fixtures())


def test_fixtures_all_requires_human_review():
    assert all(f["requires_human_review"] is True for f in get_all_fixtures())


def test_fixtures_all_have_fixture_id():
    assert all("fixture_id" in f for f in get_all_fixtures())


def test_fixtures_all_have_review_status():
    assert all("review_status" in f for f in get_all_fixtures())


def test_fixtures_all_have_review_severity():
    assert all("review_severity" in f for f in get_all_fixtures())


def test_fixtures_all_have_review_category():
    assert all("review_category" in f for f in get_all_fixtures())


def test_fixtures_all_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())


def test_fixtures_all_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())


# ── get_fixture_ids ───────────────────────────────────────────────────────────

def test_fixture_ids_count():
    assert len(get_fixture_ids()) == 75


def test_fixture_ids_unique():
    ids = get_fixture_ids()
    assert len(ids) == len(set(ids))


def test_fixture_ids_start_with_smf195():
    assert all(fid.startswith("SMF195-") for fid in get_fixture_ids())


# ── get_fixture_by_id ─────────────────────────────────────────────────────────

def test_get_fixture_by_id_first():
    f = get_fixture_by_id("SMF195-001")
    assert f["fixture_id"] == "SMF195-001"


def test_get_fixture_by_id_last():
    f = get_fixture_by_id("SMF195-075")
    assert f["fixture_id"] == "SMF195-075"


def test_get_fixture_by_id_missing_returns_none():
    assert get_fixture_by_id("SMF195-999") is None


# ── get_fixtures_by_status ────────────────────────────────────────────────────

def test_fixtures_by_status_healthy():
    results = get_fixtures_by_status("HEALTHY")
    assert len(results) >= 1


def test_fixtures_by_status_pending_review():
    results = get_fixtures_by_status("PENDING_REVIEW")
    assert len(results) >= 1


def test_fixtures_by_status_unknown_empty():
    assert get_fixtures_by_status("UNKNOWN_STATUS_XYZ") == []


# ── get_fixtures_by_severity ──────────────────────────────────────────────────

def test_fixtures_by_severity_critical():
    results = get_fixtures_by_severity("CRITICAL")
    assert len(results) >= 1


def test_fixtures_by_severity_low():
    results = get_fixtures_by_severity("LOW")
    assert len(results) >= 1


# ── get_blocked_fixtures ──────────────────────────────────────────────────────

def test_blocked_fixtures_exist():
    assert len(get_blocked_fixtures()) > 0


def test_blocked_fixtures_all_blocked():
    assert all(f["blocked"] is True for f in get_blocked_fixtures())


# ── get_escalated_fixtures ────────────────────────────────────────────────────

def test_escalated_fixtures_exist():
    assert len(get_escalated_fixtures()) > 0


def test_escalated_fixtures_all_escalated():
    assert all(f["escalated"] is True for f in get_escalated_fixtures())


# ── get_drift_fixtures ────────────────────────────────────────────────────────

def test_drift_fixtures_exist():
    assert len(get_drift_fixtures()) > 0


def test_drift_fixtures_all_drift_detected():
    assert all(f["drift_detected"] is True for f in get_drift_fixtures())
