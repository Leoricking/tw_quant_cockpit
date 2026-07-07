"""
tests/test_market_regime_scenarios_v173.py
Tests for Market Regime Position Control scenario_registry_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_scenario_registry_v173 import (
    get_all_scenarios, get_scenario_by_id, get_scenarios_by_category,
    count_scenarios, validate_registry, DETERMINISTIC_SEED, MIN_SCENARIOS,
    SCENARIO_CATEGORIES,
)


class TestScenarioCount:
    def test_count_ge_65(self):
        assert count_scenarios() >= MIN_SCENARIOS

    def test_count_ge_65_direct(self):
        assert count_scenarios() >= 65

    def test_get_all_returns_list(self):
        assert isinstance(get_all_scenarios(), list)

    def test_get_all_length_matches_count(self):
        assert len(get_all_scenarios()) == count_scenarios()


class TestScenarioStructure:
    def test_all_have_scenario_id(self):
        for s in get_all_scenarios():
            assert "scenario_id" in s

    def test_all_have_name(self):
        for s in get_all_scenarios():
            assert "name" in s

    def test_all_have_category(self):
        for s in get_all_scenarios():
            assert "category" in s

    def test_all_have_fixture_id(self):
        for s in get_all_scenarios():
            assert "fixture_id" in s

    def test_all_have_expected_status(self):
        for s in get_all_scenarios():
            assert "expected_status" in s

    def test_all_deterministic_seed_173(self):
        for s in get_all_scenarios():
            assert s["deterministic_seed"] == DETERMINISTIC_SEED

    def test_all_paper_only_true(self):
        for s in get_all_scenarios():
            assert s.get("paper_only") is True

    def test_all_no_real_orders_true(self):
        for s in get_all_scenarios():
            assert s.get("no_real_orders") is True

    def test_no_duplicate_ids(self):
        ids = [s["scenario_id"] for s in get_all_scenarios()]
        assert len(ids) == len(set(ids))


class TestGetScenarioById:
    def test_s173_001_found(self):
        s = get_scenario_by_id("S173-001")
        assert s.get("scenario_id") == "S173-001"

    def test_not_found_returns_empty(self):
        s = get_scenario_by_id("NONEXISTENT-999")
        assert not s

    def test_s173_065_found(self):
        s = get_scenario_by_id("S173-065")
        assert s.get("scenario_id") == "S173-065"


class TestGetScenariosByCategory:
    def test_bull_detection_category(self):
        scenarios = get_scenarios_by_category("bull_detection")
        assert len(scenarios) >= 1

    def test_cash_ratio_category(self):
        scenarios = get_scenarios_by_category("cash_ratio")
        assert len(scenarios) >= 1

    def test_unknown_category_empty(self):
        scenarios = get_scenarios_by_category("nonexistent_category")
        assert scenarios == []


class TestValidateRegistry:
    def test_valid_returns_true(self):
        result = validate_registry()
        assert result["valid"] is True

    def test_no_errors(self):
        result = validate_registry()
        assert result["errors"] == []

    def test_count_in_result(self):
        result = validate_registry()
        assert "count" in result

    def test_count_matches(self):
        result = validate_registry()
        assert result["count"] == count_scenarios()


class TestConstants:
    def test_deterministic_seed_173(self):
        assert DETERMINISTIC_SEED == 173

    def test_min_scenarios_65(self):
        assert MIN_SCENARIOS == 65

    def test_scenario_categories_not_empty(self):
        assert len(SCENARIO_CATEGORIES) > 0
