"""
tests/test_decision_report_scenarios_v187.py
Tests for decision_report_scenarios_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_report_scenarios_v187 import (
    count_scenarios, get_scenarios, get_scenario_by_id,
    get_scenarios_by_category, get_scenario_ids,
)


def test_count_scenarios_75():
    assert count_scenarios() == 75


def test_get_scenarios_returns_list():
    scenarios = get_scenarios()
    assert isinstance(scenarios, list)


def test_get_scenarios_length_75():
    assert len(get_scenarios()) == 75


def test_get_scenario_by_id_dr187_001():
    s = get_scenario_by_id("DR187-001")
    assert s is not None
    assert s != {}


def test_get_scenario_by_id_dr187_075():
    s = get_scenario_by_id("DR187-075")
    assert s is not None
    assert s != {}


def test_get_scenario_by_id_unknown_returns_empty():
    s = get_scenario_by_id("DR187-UNKNOWN")
    assert s == {}


def test_scenario_has_id_field():
    s = get_scenario_by_id("DR187-001")
    assert "id" in s
    assert s["id"] == "DR187-001"


def test_scenario_has_category_field():
    s = get_scenario_by_id("DR187-001")
    assert "category" in s


def test_scenario_has_description_field():
    s = get_scenario_by_id("DR187-001")
    assert "description" in s
    assert len(s["description"]) > 0


def test_scenario_paper_only():
    s = get_scenario_by_id("DR187-001")
    assert s["paper_only"] is True


def test_scenario_no_real_orders():
    s = get_scenario_by_id("DR187-001")
    assert s["no_real_orders"] is True


def test_scenario_not_investment_advice():
    s = get_scenario_by_id("DR187-001")
    assert s["not_investment_advice"] is True


def test_scenario_production_trading_blocked():
    s = get_scenario_by_id("DR187-001")
    assert s["production_trading_blocked"] is True


def test_scenario_report_only():
    s = get_scenario_by_id("DR187-001")
    assert s["report_only"] is True


def test_scenario_audit_only():
    s = get_scenario_by_id("DR187-001")
    assert s["audit_only"] is True


def test_all_scenarios_have_paper_only():
    for s in get_scenarios():
        assert s.get("paper_only") is True, f"Scenario {s.get('id')} missing paper_only"


def test_all_scenarios_have_production_trading_blocked():
    for s in get_scenarios():
        assert s.get("production_trading_blocked") is True, f"Scenario {s.get('id')} missing production_trading_blocked"


def test_all_scenarios_have_id():
    for s in get_scenarios():
        assert "id" in s and s["id"].startswith("DR187-")


def test_all_scenarios_have_description():
    for s in get_scenarios():
        assert len(s.get("description", "")) > 0, f"Scenario {s.get('id')} missing description"


def test_get_scenarios_by_category_daily():
    cats = get_scenarios_by_category("daily_complete_report")
    assert isinstance(cats, list)
    assert len(cats) >= 1


def test_get_scenarios_by_category_unknown_empty():
    cats = get_scenarios_by_category("unknown_category_xyz")
    assert cats == []


def test_get_scenario_ids_count():
    ids = get_scenario_ids()
    assert len(ids) == 75


def test_get_scenario_ids_contains_001():
    ids = get_scenario_ids()
    assert "DR187-001" in ids


def test_get_scenario_ids_contains_075():
    ids = get_scenario_ids()
    assert "DR187-075" in ids


def test_get_scenario_ids_no_duplicates():
    ids = get_scenario_ids()
    assert len(ids) == len(set(ids))


def test_get_scenarios_is_copy():
    s1 = get_scenarios()
    s2 = get_scenarios()
    s1.append({"id": "FAKE"})
    # modifying copy should not affect next call
    s3 = get_scenarios()
    assert len(s3) == 75


def test_scenario_mid_range_50():
    s = get_scenario_by_id("DR187-050")
    assert s != {}
    assert s["paper_only"] is True


def test_scenario_all_have_no_margin():
    for s in get_scenarios():
        assert s.get("no_margin") is True, f"Scenario {s.get('id')} missing no_margin"


def test_scenario_all_have_research_only():
    for s in get_scenarios():
        assert s.get("research_only") is True, f"Scenario {s.get('id')} missing research_only"
