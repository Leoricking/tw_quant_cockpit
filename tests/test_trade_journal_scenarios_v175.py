"""
tests/test_trade_journal_scenarios_v175.py
Tests for Trade Journal scenarios v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_scenarios_v175 import (
    SCENARIOS, get_scenarios, get_scenario_by_id, count_scenarios, MIN_SCENARIOS,
)


class TestScenarioCount:
    def test_count_ge_55(self):
        assert count_scenarios() >= 55

    def test_count_matches_scenarios_list(self):
        assert count_scenarios() == len(SCENARIOS)

    def test_min_scenarios_constant(self):
        assert MIN_SCENARIOS >= 55

    def test_count_meets_minimum(self):
        assert count_scenarios() >= MIN_SCENARIOS


class TestGetScenarios:
    def test_returns_list(self):
        assert isinstance(get_scenarios(), list)

    def test_all_paper_only(self):
        assert all(s["paper_only"] for s in get_scenarios())

    def test_all_research_only(self):
        assert all(s["research_only"] for s in get_scenarios())

    def test_all_no_real_orders(self):
        assert all(s["no_real_orders"] for s in get_scenarios())

    def test_all_no_broker(self):
        assert all(s["no_broker"] for s in get_scenarios())

    def test_all_not_investment_advice(self):
        assert all(s["not_investment_advice"] for s in get_scenarios())

    def test_all_demo_only(self):
        assert all(s["demo_only"] for s in get_scenarios())

    def test_all_not_for_production(self):
        assert all(s["not_for_production"] for s in get_scenarios())

    def test_all_have_id(self):
        assert all("id" in s for s in get_scenarios())

    def test_all_have_name(self):
        assert all("name" in s for s in get_scenarios())

    def test_all_have_regime(self):
        assert all("regime" in s for s in get_scenarios())

    def test_all_have_outcome(self):
        assert all("outcome" in s for s in get_scenarios())

    def test_all_have_abc_pattern(self):
        assert all("abc_pattern" in s for s in get_scenarios())

    def test_all_have_entry_quality(self):
        assert all("entry_quality" in s for s in get_scenarios())

    def test_all_have_exit_quality(self):
        assert all("exit_quality" in s for s in get_scenarios())


class TestGetScenarioById:
    def test_existing_id_found(self):
        assert get_scenario_by_id("SC175-001") is not None

    def test_last_scenario_found(self):
        assert get_scenario_by_id("SC175-055") is not None

    def test_nonexistent_id_returns_none(self):
        assert get_scenario_by_id("SC175-999") is None

    def test_found_scenario_paper_only(self):
        s = get_scenario_by_id("SC175-001")
        assert s["paper_only"] is True

    def test_schema_version_in_scenario(self):
        s = get_scenario_by_id("SC175-001")
        assert s.get("schema_version") == "175"


class TestScenarioIds:
    def test_all_ids_unique(self):
        ids = [s["id"] for s in get_scenarios()]
        assert len(ids) == len(set(ids))

    def test_first_id_sc175_001(self):
        assert SCENARIOS[0]["id"] == "SC175-001"

    def test_ids_start_with_sc175(self):
        assert all(s["id"].startswith("SC175-") for s in get_scenarios())
