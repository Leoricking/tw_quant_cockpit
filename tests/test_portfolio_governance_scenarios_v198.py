"""
tests/test_portfolio_governance_scenarios_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Scenario Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_scenarios_v198 import (
    _SCENARIOS, get_scenarios, get_scenario_by_id,
)

REQUIRED_FIELDS = [
    "id", "scenario_id", "schema_version", "name",
    "paper_only", "research_only", "simulate_only", "validation_only",
    "portfolio_governance_only", "risk_overlay_only", "dashboard_only",
    "report_only", "audit_only", "no_real_orders", "no_broker",
    "no_margin", "no_leverage", "no_production_strategy_mutation",
    "no_automatic_rollback", "no_live_strategy_activation",
    "not_investment_advice", "demo_only", "not_for_production",
    "production_trading_blocked", "expected_outcome",
]


class TestGetScenarios:
    def test_returns_list(self):
        assert isinstance(get_scenarios(), list)

    def test_count_75(self):
        assert len(get_scenarios()) == 75

    def test_all_paper_only_True(self):
        assert all(s["paper_only"] is True for s in get_scenarios())

    def test_all_no_real_orders_True(self):
        assert all(s["no_real_orders"] is True for s in get_scenarios())

    def test_all_schema_version_198(self):
        assert all(s["schema_version"] == "198" for s in get_scenarios())

    def test_all_not_investment_advice_True(self):
        assert all(s["not_investment_advice"] is True for s in get_scenarios())

    def test_all_demo_only_True(self):
        assert all(s["demo_only"] is True for s in get_scenarios())

    def test_all_production_trading_blocked_True(self):
        assert all(s["production_trading_blocked"] is True for s in get_scenarios())

    def test_all_have_required_fields(self):
        for s in get_scenarios():
            for field in REQUIRED_FIELDS:
                assert field in s, f"Scenario {s.get('scenario_id')} missing field: {field}"

    def test_all_ids_unique(self):
        ids = [s["scenario_id"] for s in get_scenarios()]
        assert len(ids) == len(set(ids))

    def test_first_id_is_PG198_001(self):
        assert get_scenarios()[0]["scenario_id"] == "PG198-001"

    def test_last_id_is_PG198_075(self):
        assert get_scenarios()[74]["scenario_id"] == "PG198-075"

    def test_all_names_are_strings(self):
        assert all(isinstance(s["name"], str) for s in get_scenarios())

    def test_all_expected_outcomes_are_strings(self):
        assert all(isinstance(s["expected_outcome"], str) for s in get_scenarios())


class TestGetScenarioById:
    def test_returns_dict_for_valid_id(self):
        assert isinstance(get_scenario_by_id("PG198-001"), dict)

    def test_returns_correct_scenario(self):
        s = get_scenario_by_id("PG198-001")
        assert s["scenario_id"] == "PG198-001"

    def test_returns_PG198_025(self):
        s = get_scenario_by_id("PG198-025")
        assert s["scenario_id"] == "PG198-025"

    def test_returns_PG198_075(self):
        s = get_scenario_by_id("PG198-075")
        assert s["scenario_id"] == "PG198-075"

    def test_unknown_id_returns_empty_dict(self):
        assert get_scenario_by_id("UNKNOWN-999") == {}

    def test_empty_string_returns_empty_dict(self):
        assert get_scenario_by_id("") == {}

    def test_found_scenario_paper_only_True(self):
        s = get_scenario_by_id("PG198-010")
        assert s["paper_only"] is True


class TestScenarioRaw:
    def test_raw_count_75(self):
        assert len(_SCENARIOS) == 75

    def test_scenario_1_has_governance_name(self):
        s = _SCENARIOS[0]
        assert "governance" in s["name"].lower() or "snapshot" in s["name"].lower()

    def test_scenario_17_is_overlay_blocked(self):
        s = get_scenario_by_id("PG198-017")
        assert "blocked" in s["expected_outcome"] or "overlay" in s["expected_outcome"]

    def test_all_no_broker_True(self):
        assert all(s["no_broker"] is True for s in _SCENARIOS)
