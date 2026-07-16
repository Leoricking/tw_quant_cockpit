"""
tests/test_decision_journal_fixtures_v189.py
Tests for decision_journal_fixtures_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import json
import pytest
from paper_trading.small_capital_strategy.decision_journal_fixtures_v189 import (
    get_fixtures, get_fixture_count, get_fixture_dir,
    get_fixture_by_id, get_fixture_as_json, get_fixture_info,
)


def test_get_fixture_count_75():
    assert get_fixture_count() == 75


def test_get_fixtures_returns_list():
    assert isinstance(get_fixtures(), list)


def test_get_fixtures_length_75():
    assert len(get_fixtures()) == 75


def test_all_fixtures_have_id():
    for f in get_fixtures():
        assert "fixture_id" in f
        assert f["fixture_id"].startswith("DJF189-")


def test_all_fixtures_have_safety_flags():
    for f in get_fixtures():
        assert f.get("paper_only") is True
        assert f.get("no_real_orders") is True
        assert f.get("no_broker") is True
        assert f.get("not_investment_advice") is True
        assert f.get("production_trading_blocked") is True
        assert f.get("journal_only") is True
        assert f.get("review_only") is True
        assert f.get("audit_only") is True


def test_all_fixtures_have_expected_safety():
    for f in get_fixtures():
        assert f.get("expected_paper_only") is True
        assert f.get("expected_no_real_orders") is True
        assert f.get("expected_no_broker") is True
        assert f.get("expected_not_investment_advice") is True
        assert f.get("expected_production_trading_blocked") is True


def test_get_fixture_by_id_001():
    f = get_fixture_by_id("DJF189-001")
    assert f is not None
    assert f["fixture_id"] == "DJF189-001"


def test_get_fixture_by_id_075():
    f = get_fixture_by_id("DJF189-075")
    assert f is not None
    assert f["fixture_id"] == "DJF189-075"


def test_get_fixture_by_id_unknown_none():
    assert get_fixture_by_id("DJF189-999") is None


def test_get_fixture_as_json_returns_str():
    result = get_fixture_as_json("DJF189-001")
    assert isinstance(result, str)


def test_get_fixture_as_json_parseable():
    result = get_fixture_as_json("DJF189-001")
    data = json.loads(result)
    assert isinstance(data, dict)


def test_get_fixture_as_json_paper_only():
    data = json.loads(get_fixture_as_json("DJF189-001"))
    assert data["paper_only"] is True


def test_get_fixture_as_json_unknown_returns_empty():
    result = get_fixture_as_json("DJF189-999")
    assert result == "{}"


def test_get_fixture_dir_is_str():
    assert isinstance(get_fixture_dir(), str)


def test_get_fixture_dir_contains_189():
    assert "189" in get_fixture_dir()


def test_get_fixture_info_count():
    info = get_fixture_info()
    assert info["count"] == 75


def test_get_fixture_info_paper_only():
    assert get_fixture_info()["paper_only"] is True


def test_get_fixture_info_journal_only():
    assert get_fixture_info()["journal_only"] is True


def test_get_fixture_info_schema_version():
    assert get_fixture_info()["schema_version"] == "189"


def test_get_fixture_info_entry_states_present():
    info = get_fixture_info()
    assert "entry_states" in info
    assert len(info["entry_states"]) == 16


def test_all_fixtures_have_deterministic_timestamp():
    for f in get_fixtures():
        assert f.get("deterministic_timestamp_policy") == "date_label_only_no_wall_clock"


def test_all_fixtures_have_safe_export_path():
    for f in get_fixtures():
        export_path = f.get("export_path", "")
        assert "production_db" not in export_path
        assert "live_orders" not in export_path


def test_all_fixtures_have_audit_trail_complete():
    for f in get_fixtures():
        assert f.get("audit_trail_complete") is True


def test_fixtures_have_diverse_entry_states():
    states = set(f.get("entry_state", "") for f in get_fixtures())
    assert len(states) >= 10


def test_fixtures_have_diverse_review_types():
    types = set(f.get("review_type", "") for f in get_fixtures())
    assert len(types) >= 3


def test_fixtures_have_diverse_quality_grades():
    grades = set(f.get("quality_grade", "") for f in get_fixtures())
    assert len(grades) >= 4


def test_fixture_ids_all_unique():
    ids = [f["fixture_id"] for f in get_fixtures()]
    assert len(ids) == len(set(ids))


def test_fixture_names_all_present():
    for f in get_fixtures():
        assert "fixture_name" in f
        assert len(f["fixture_name"]) > 0
