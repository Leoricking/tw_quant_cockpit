"""
tests/test_decision_workflow_fixtures_v188.py
Tests for decision_workflow_fixtures_v188 — Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
import json
from paper_trading.small_capital_strategy.decision_workflow_fixtures_v188 import (
    get_fixtures, get_fixture_count, get_fixture_dir,
    get_fixture_by_id, get_fixture_as_json, get_fixture_info,
)


def test_fixture_count_75():
    assert get_fixture_count() == 75


def test_get_fixtures_returns_75():
    assert len(get_fixtures()) == 75


def test_get_fixtures_returns_list():
    assert isinstance(get_fixtures(), list)


def test_all_fixtures_have_id():
    for f in get_fixtures():
        assert "fixture_id" in f and f["fixture_id"]


def test_all_fixtures_have_workflow_type():
    for f in get_fixtures():
        assert "workflow_type" in f and f["workflow_type"]


def test_all_fixtures_paper_only():
    for f in get_fixtures():
        assert f.get("paper_only") is True


def test_all_fixtures_research_only():
    for f in get_fixtures():
        assert f.get("research_only") is True


def test_all_fixtures_simulate_only():
    for f in get_fixtures():
        assert f.get("simulate_only") is True


def test_all_fixtures_validation_only():
    for f in get_fixtures():
        assert f.get("validation_only") is True


def test_all_fixtures_decision_only():
    for f in get_fixtures():
        assert f.get("decision_only") is True


def test_all_fixtures_workflow_only():
    for f in get_fixtures():
        assert f.get("workflow_only") is True


def test_all_fixtures_report_only():
    for f in get_fixtures():
        assert f.get("report_only") is True


def test_all_fixtures_audit_only():
    for f in get_fixtures():
        assert f.get("audit_only") is True


def test_all_fixtures_no_real_orders():
    for f in get_fixtures():
        assert f.get("no_real_orders") is True


def test_all_fixtures_no_broker():
    for f in get_fixtures():
        assert f.get("no_broker") is True


def test_all_fixtures_no_margin():
    for f in get_fixtures():
        assert f.get("no_margin") is True


def test_all_fixtures_no_leverage():
    for f in get_fixtures():
        assert f.get("no_leverage") is True


def test_all_fixtures_not_investment_advice():
    for f in get_fixtures():
        assert f.get("not_investment_advice") is True


def test_all_fixtures_demo_only():
    for f in get_fixtures():
        assert f.get("demo_only") is True


def test_all_fixtures_not_for_production():
    for f in get_fixtures():
        assert f.get("not_for_production") is True


def test_all_fixtures_production_trading_blocked():
    for f in get_fixtures():
        assert f.get("production_trading_blocked") is True


def test_fixture_ids_unique():
    ids = [f["fixture_id"] for f in get_fixtures()]
    assert len(ids) == len(set(ids))


def test_get_fixture_by_id_dwf188_001():
    f = get_fixture_by_id("DWF188-001")
    assert f is not None
    assert f["fixture_id"] == "DWF188-001"


def test_get_fixture_by_id_dwf188_075():
    f = get_fixture_by_id("DWF188-075")
    assert f is not None


def test_get_fixture_by_id_nonexistent():
    f = get_fixture_by_id("DWF188-999")
    assert f is None


def test_get_fixture_as_json_returns_str():
    j = get_fixture_as_json("DWF188-001")
    assert isinstance(j, str)


def test_get_fixture_as_json_is_valid_json():
    j = get_fixture_as_json("DWF188-001")
    data = json.loads(j)
    assert isinstance(data, dict)


def test_get_fixture_as_json_nonexistent_returns_empty():
    j = get_fixture_as_json("DWF188-999")
    assert j == "{}"


def test_get_fixture_dir_returns_str():
    d = get_fixture_dir()
    assert isinstance(d, str)
    assert len(d) > 0


def test_get_fixture_info_count():
    info = get_fixture_info()
    assert info["count"] == 75


def test_get_fixture_info_paper_only():
    info = get_fixture_info()
    assert info["paper_only"] is True


def test_get_fixture_info_no_real_orders():
    info = get_fixture_info()
    assert info["no_real_orders"] is True


def test_get_fixture_info_schema_188():
    info = get_fixture_info()
    assert info["schema_version"] == "188"


def test_all_fixtures_have_deterministic_timestamp():
    for f in get_fixtures():
        assert "deterministic_timestamp_policy" in f


def test_all_fixtures_deterministic_policy_date_only():
    for f in get_fixtures():
        assert f["deterministic_timestamp_policy"] == "date_label_only_no_wall_clock"


def test_all_fixtures_expected_paper_only():
    for f in get_fixtures():
        assert f.get("expected_paper_only") is True


def test_all_fixtures_expected_no_real_orders():
    for f in get_fixtures():
        assert f.get("expected_no_real_orders") is True


def test_all_fixtures_expected_no_broker():
    for f in get_fixtures():
        assert f.get("expected_no_broker") is True


def test_all_fixtures_have_capital_stage():
    for f in get_fixtures():
        assert "capital_stage" in f
        assert f["capital_stage"] in ("300K", "500K", "1M", "3M")


def test_all_fixtures_have_candidates_list():
    for f in get_fixtures():
        assert "candidates" in f
        assert isinstance(f["candidates"], list)


def test_all_fixtures_have_total_exposure():
    for f in get_fixtures():
        assert "total_exposure_pct" in f
        assert isinstance(f["total_exposure_pct"], float)


def test_all_fixtures_have_cash_reserve():
    for f in get_fixtures():
        assert "cash_reserve_pct" in f
        assert isinstance(f["cash_reserve_pct"], float)


def test_all_fixtures_have_monte_carlo_ruin():
    for f in get_fixtures():
        assert "monte_carlo_ruin_risk" in f


def test_fixture_json_paper_only():
    j = get_fixture_as_json("DWF188-001")
    data = json.loads(j)
    assert data.get("paper_only") is True
