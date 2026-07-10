"""tests/test_mistake_taxonomy_scenarios_v176.py — v1.7.6 scenario tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_scenarios_v176 import (
    get_scenarios, count_scenarios, get_scenario_by_id,
)

_REQUIRED_SAFETY = [
    "paper_only", "research_only", "no_real_orders", "no_broker",
    "not_investment_advice", "demo_only", "not_for_production",
]


class TestScenarioCount:
    def test_count_ge_60(self):
        assert count_scenarios() >= 60

    def test_count_matches_list_length(self):
        assert count_scenarios() == len(get_scenarios())


class TestScenarioContent:
    def test_all_paper_only(self):
        assert all(s["paper_only"] is True for s in get_scenarios())

    def test_all_research_only(self):
        assert all(s["research_only"] is True for s in get_scenarios())

    def test_all_no_real_orders(self):
        assert all(s["no_real_orders"] is True for s in get_scenarios())

    def test_all_no_broker(self):
        assert all(s["no_broker"] is True for s in get_scenarios())

    def test_all_not_investment_advice(self):
        assert all(s["not_investment_advice"] is True for s in get_scenarios())

    def test_all_demo_only(self):
        assert all(s["demo_only"] is True for s in get_scenarios())

    def test_all_not_for_production(self):
        assert all(s["not_for_production"] is True for s in get_scenarios())

    def test_all_have_id(self):
        assert all(len(s["id"]) > 0 for s in get_scenarios())

    def test_all_have_name(self):
        assert all(len(s["name"]) > 0 for s in get_scenarios())

    def test_all_have_severity(self):
        valid = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL", "BLOCKING"}
        assert all(s["severity"] in valid for s in get_scenarios())

    def test_blocking_scenarios_exist(self):
        assert any(s["severity"] == "BLOCKING" for s in get_scenarios())

    def test_pass_scenarios_exist(self):
        assert any(s["expected_behavior_level"] == "PASS" for s in get_scenarios())

    def test_blocked_scenarios_exist(self):
        assert any(s["expected_behavior_level"] == "BLOCKED" for s in get_scenarios())


class TestGetScenarioById:
    def test_first_scenario_found(self):
        sc = get_scenario_by_id("SC176-001")
        assert sc != {}
        assert sc["id"] == "SC176-001"

    def test_nonexistent_returns_empty(self):
        sc = get_scenario_by_id("SC176-999")
        assert sc == {}

    def test_last_scenario_found(self):
        scenarios = get_scenarios()
        last_id = scenarios[-1]["id"]
        assert get_scenario_by_id(last_id) != {}
