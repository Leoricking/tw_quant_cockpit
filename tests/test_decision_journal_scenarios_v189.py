"""
tests/test_decision_journal_scenarios_v189.py
Tests for decision_journal_scenarios_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_journal_scenarios_v189 import (
    count_scenarios, get_scenarios, get_scenario_by_id,
    get_scenarios_by_type, get_scenario_ids, get_scenario_info,
)


def test_count_scenarios_75():
    assert count_scenarios() == 75


def test_get_scenarios_returns_list():
    assert isinstance(get_scenarios(), list)


def test_get_scenarios_length_75():
    assert len(get_scenarios()) == 75


def test_all_scenarios_have_id():
    for s in get_scenarios():
        assert "id" in s and s["id"].startswith("DJ189-")


def test_all_scenarios_have_safety_flags():
    for s in get_scenarios():
        assert s.get("paper_only") is True
        assert s.get("no_real_orders") is True
        assert s.get("no_broker") is True
        assert s.get("not_investment_advice") is True
        assert s.get("production_trading_blocked") is True
        assert s.get("journal_only") is True
        assert s.get("review_only") is True
        assert s.get("audit_only") is True


def test_get_scenario_by_id_001():
    s = get_scenario_by_id("DJ189-001")
    assert s is not None
    assert s["id"] == "DJ189-001"


def test_get_scenario_by_id_075():
    s = get_scenario_by_id("DJ189-075")
    assert s is not None
    assert s["id"] == "DJ189-075"


def test_get_scenario_by_id_unknown_none():
    assert get_scenario_by_id("DJ189-999") is None


def test_scenario_001_complete_daily_journal():
    s = get_scenario_by_id("DJ189-001")
    assert s["scenario_type"] == "complete_daily_journal"


def test_scenario_003_empty_journal():
    s = get_scenario_by_id("DJ189-003")
    assert s["scenario_type"] == "empty_journal"


def test_scenario_004_malformed_entry():
    s = get_scenario_by_id("DJ189-004")
    assert s.get("expected_blocked") is True


def test_scenario_010_missing_evidence():
    s = get_scenario_by_id("DJ189-010")
    assert s.get("has_evidence") is False


def test_scenario_011_unsafe_export_blocked():
    s = get_scenario_by_id("DJ189-011")
    assert s.get("expected_blocked") is True
    assert "production_db" in s.get("export_path", "")


def test_scenario_012_over_concentration():
    s = get_scenario_by_id("DJ189-012")
    assert s.get("total_exposure_pct", 0) > 80


def test_scenario_018_no_mistake_found():
    s = get_scenario_by_id("DJ189-018")
    assert s.get("expected_mistake_tag") == "NO_MISTAKE_FOUND"


def test_scenario_019_excellent_quality():
    s = get_scenario_by_id("DJ189-019")
    assert s.get("expected_grade") == "EXCELLENT"


def test_scenario_020_poor_quality():
    s = get_scenario_by_id("DJ189-020")
    assert s.get("expected_grade") == "POOR"


def test_scenario_071_safety_audit():
    s = get_scenario_by_id("DJ189-071")
    assert s.get("expected_all_safe") is True


def test_get_scenarios_by_type_complete_daily():
    results = get_scenarios_by_type("complete_daily_journal")
    assert len(results) >= 1


def test_get_scenarios_by_type_unknown_empty():
    results = get_scenarios_by_type("unknown_type_xyz")
    assert results == []


def test_get_scenario_ids_count():
    ids = get_scenario_ids()
    assert len(ids) == 75


def test_get_scenario_ids_all_unique():
    ids = get_scenario_ids()
    assert len(ids) == len(set(ids))


def test_get_scenario_info_paper_only():
    info = get_scenario_info()
    assert info["paper_only"] is True


def test_get_scenario_info_count():
    info = get_scenario_info()
    assert info["count"] == 75


def test_get_scenario_info_schema_version():
    info = get_scenario_info()
    assert info["schema_version"] == "189"


def test_all_scenarios_no_forbidden_entry_states():
    forbidden = {"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                 "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"}
    for s in get_scenarios():
        state = s.get("entry_state", "")
        assert state not in forbidden, f"Forbidden state {state!r} in scenario {s['id']}"


def test_scenario_demo_only_flags():
    for s in get_scenarios():
        assert s.get("demo_only") is True
        assert s.get("not_for_production") is True
