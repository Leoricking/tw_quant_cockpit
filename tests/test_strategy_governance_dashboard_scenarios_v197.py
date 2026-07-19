"""
tests/test_strategy_governance_dashboard_scenarios_v197.py
Tests for strategy_governance_dashboard_scenarios_v197.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_scenarios_v197 import (
    get_all_scenarios, get_scenario_count, get_scenario_by_id,
    get_scenarios_by_category, get_scenario_categories,
)


# ── count ──────────────────────────────────────────────────────────────────────
def test_scenario_count_75(): assert get_scenario_count() == 75
def test_all_scenarios_length_75(): assert len(get_all_scenarios()) == 75
def test_all_scenarios_returns_list(): assert isinstance(get_all_scenarios(), list)

# ── safety flags in all scenarios ────────────────────────────────────────────
def test_all_scenarios_paper_only(): assert all(s["paper_only"] is True for s in get_all_scenarios())
def test_all_scenarios_no_real_orders(): assert all(s["no_real_orders"] is True for s in get_all_scenarios())
def test_all_scenarios_not_investment_advice(): assert all(s["not_investment_advice"] is True for s in get_all_scenarios())
def test_all_scenarios_no_broker(): assert all(s["no_broker"] is True for s in get_all_scenarios())
def test_all_scenarios_production_trading_blocked(): assert all(s["production_trading_blocked"] is True for s in get_all_scenarios())
def test_all_scenarios_governance_analytics_only(): assert all(s["governance_analytics_only"] is True for s in get_all_scenarios())
def test_all_scenarios_demo_only(): assert all(s["demo_only"] is True for s in get_all_scenarios())
def test_all_scenarios_schema_version_197(): assert all(s["schema_version"] == "197" for s in get_all_scenarios())

# ── required fields ───────────────────────────────────────────────────────────
def test_all_scenarios_have_id(): assert all("id" in s for s in get_all_scenarios())
def test_all_scenarios_have_scenario_id(): assert all("scenario_id" in s for s in get_all_scenarios())
def test_all_scenarios_have_name(): assert all("name" in s for s in get_all_scenarios())
def test_all_scenarios_have_category(): assert all("category" in s for s in get_all_scenarios())

# ── unique IDs ────────────────────────────────────────────────────────────────
def test_scenario_ids_unique():
    ids = [s["scenario_id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))

def test_scenario_ids_prefix_sp197():
    assert all(s["scenario_id"].startswith("SP197-") for s in get_all_scenarios())

# ── get_scenario_by_id ────────────────────────────────────────────────────────
def test_get_scenario_by_id_001(): assert get_scenario_by_id("SP197-001")["scenario_id"] == "SP197-001"
def test_get_scenario_by_id_075(): assert get_scenario_by_id("SP197-075")["scenario_id"] == "SP197-075"
def test_get_scenario_by_id_missing_returns_empty(): assert get_scenario_by_id("SP197-999") == {}
def test_get_scenario_by_id_returns_dict(): assert isinstance(get_scenario_by_id("SP197-001"), dict)

# ── categories ────────────────────────────────────────────────────────────────
def test_categories_returns_list(): assert isinstance(get_scenario_categories(), list)
def test_categories_not_empty(): assert len(get_scenario_categories()) > 0
def test_category_complete_governance_dashboard_exists():
    assert "complete_governance_dashboard" in get_scenario_categories()
def test_category_excellent_decision_quality_exists():
    assert "excellent_decision_quality" in get_scenario_categories()
def test_category_unsafe_export_blocked_exists():
    assert "unsafe_export_blocked" in get_scenario_categories()
def test_category_broker_request_blocked_exists():
    assert "broker_request_blocked" in get_scenario_categories()

# ── get_scenarios_by_category ─────────────────────────────────────────────────
def test_get_scenarios_by_category_complete():
    cats = get_scenarios_by_category("complete_governance_dashboard")
    assert len(cats) == 5
def test_get_scenarios_by_category_excellent():
    cats = get_scenarios_by_category("excellent_decision_quality")
    assert len(cats) == 5
def test_get_scenarios_by_category_missing_returns_empty():
    assert get_scenarios_by_category("nonexistent_category") == []
def test_get_scenarios_by_category_returns_list():
    assert isinstance(get_scenarios_by_category("complete_governance_dashboard"), list)

# ── specific scenario content ─────────────────────────────────────────────────
def test_scenario_001_registry_source(): s = get_scenario_by_id("SP197-001"); assert s.get("registry_source") == "REG-001"
def test_scenario_001_analytics_window(): s = get_scenario_by_id("SP197-001"); assert s.get("analytics_window") == "FULL_HISTORY"
def test_scenario_006_grade_excellent(): s = get_scenario_by_id("SP197-006"); assert s.get("grade") == "EXCELLENT"
def test_scenario_048_blocked_true(): s = get_scenario_by_id("SP197-048"); assert s.get("blocked") is True
def test_scenario_063_no_real_orders(): s = get_scenario_by_id("SP197-063"); assert s.get("no_real_orders") is True
