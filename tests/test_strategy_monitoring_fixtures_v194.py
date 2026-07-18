"""
tests/test_strategy_monitoring_fixtures_v194.py
Tests for strategy_monitoring_fixtures_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_fixtures_v194 import (
    get_all_fixtures, get_fixture_by_id, get_fixture_ids,
    get_fixtures_by_status, get_fixtures_by_severity,
    get_blocked_fixtures, get_drift_fixtures,
)


# ── count ─────────────────────────────────────────────────────────────────────

def test_fixtures_count_75():
    assert len(get_all_fixtures()) == 75


def test_fixtures_min_75():
    assert len(get_all_fixtures()) >= 75


def test_fixture_ids_count():
    assert len(get_fixture_ids()) == 75


# ── safety flags ──────────────────────────────────────────────────────────────

def test_all_fixtures_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())


def test_all_fixtures_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())


def test_all_fixtures_monitoring_only():
    assert all(f["monitoring_only"] is True for f in get_all_fixtures())


def test_all_fixtures_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())


def test_all_fixtures_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())


def test_all_fixtures_drift_detection_only():
    assert all(f["drift_detection_only"] is True for f in get_all_fixtures())


# ── fixture structure ─────────────────────────────────────────────────────────

def test_all_fixtures_have_fixture_id():
    assert all("fixture_id" in f for f in get_all_fixtures())


def test_all_fixtures_have_drift_category():
    assert all("drift_category" in f for f in get_all_fixtures())


def test_all_fixtures_have_monitoring_status():
    assert all("monitoring_status" in f for f in get_all_fixtures())


def test_all_fixtures_have_drift_severity():
    assert all("drift_severity" in f for f in get_all_fixtures())


def test_all_fixtures_have_schema_version():
    assert all(f.get("schema_version") == "194" for f in get_all_fixtures())


# ── fixture IDs ───────────────────────────────────────────────────────────────

def test_fixture_ids_start_with_smf194():
    assert all(fid.startswith("SMF194-") for fid in get_fixture_ids())


def test_fixture_first_id():
    assert "SMF194-001" in get_fixture_ids()


def test_fixture_last_id():
    assert "SMF194-075" in get_fixture_ids()


def test_fixture_ids_unique():
    ids = get_fixture_ids()
    assert len(ids) == len(set(ids))


# ── get_fixture_by_id ─────────────────────────────────────────────────────────

def test_get_fixture_by_id_001():
    f = get_fixture_by_id("SMF194-001")
    assert f is not None
    assert f["fixture_id"] == "SMF194-001"


def test_get_fixture_by_id_075():
    f = get_fixture_by_id("SMF194-075")
    assert f is not None
    assert f["fixture_id"] == "SMF194-075"


def test_get_fixture_by_id_missing_returns_none():
    assert get_fixture_by_id("SMF194-999") is None


def test_get_fixture_by_id_paper_only():
    f = get_fixture_by_id("SMF194-001")
    assert f["paper_only"] is True


# ── get_fixtures_by_status ────────────────────────────────────────────────────

def test_get_fixtures_by_status_healthy():
    healthy = get_fixtures_by_status("HEALTHY")
    assert len(healthy) >= 1
    assert all(f["monitoring_status"] == "HEALTHY" for f in healthy)


def test_get_fixtures_by_status_watch():
    watch = get_fixtures_by_status("WATCH")
    assert isinstance(watch, list)


def test_get_fixtures_by_status_review_required():
    review = get_fixtures_by_status("REVIEW_REQUIRED")
    assert isinstance(review, list)


def test_get_fixtures_by_status_blocked():
    blocked = get_fixtures_by_status("BLOCKED")
    assert isinstance(blocked, list)


# ── get_fixtures_by_severity ──────────────────────────────────────────────────

def test_get_fixtures_by_severity_none():
    result = get_fixtures_by_severity("NONE")
    assert isinstance(result, list)
    assert len(result) >= 1


def test_get_fixtures_by_severity_high():
    result = get_fixtures_by_severity("HIGH")
    assert isinstance(result, list)


def test_get_fixtures_by_severity_critical():
    result = get_fixtures_by_severity("CRITICAL")
    assert isinstance(result, list)


# ── get_blocked_fixtures ──────────────────────────────────────────────────────

def test_get_blocked_fixtures_returns_list():
    assert isinstance(get_blocked_fixtures(), list)


def test_get_blocked_fixtures_all_blocked():
    blocked = get_blocked_fixtures()
    if blocked:
        assert all(f.get("blocked") is True for f in blocked)


# ── get_drift_fixtures ────────────────────────────────────────────────────────

def test_get_drift_fixtures_returns_list():
    assert isinstance(get_drift_fixtures(), list)


def test_get_drift_fixtures_have_drift():
    drift = get_drift_fixtures()
    assert len(drift) >= 1
    assert all(f.get("drift_detected") is True for f in drift)


# ── auto_rollback not present in fixtures ────────────────────────────────────

def test_no_fixture_has_auto_rollback_true():
    for f in get_all_fixtures():
        assert f.get("auto_rollback", False) is not True
