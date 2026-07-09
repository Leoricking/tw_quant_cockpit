"""
tests/test_risk_dashboard_scenarios_v174.py
Tests for scenario registry v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_scenario_registry_v174 import (
    get_all_scenarios, count_scenarios, validate_registry,
    MIN_SCENARIOS, DETERMINISTIC_SEED, SCENARIO_CATEGORIES,
)


class TestRegistryConstants:
    def test_min_scenarios_65(self):
        assert MIN_SCENARIOS == 65

    def test_deterministic_seed_174(self):
        assert DETERMINISTIC_SEED == 174

    def test_categories_list(self):
        assert isinstance(SCENARIO_CATEGORIES, list)

    def test_has_single_trade_category(self):
        assert "single_trade_risk" in SCENARIO_CATEGORIES

    def test_has_portfolio_exposure_category(self):
        assert "portfolio_exposure" in SCENARIO_CATEGORIES

    def test_has_safety_category(self):
        assert "safety" in SCENARIO_CATEGORIES

    def test_has_scorecard_category(self):
        assert "scorecard" in SCENARIO_CATEGORIES

    def test_has_report_category(self):
        assert "report" in SCENARIO_CATEGORIES

    def test_has_abc_cascade_category(self):
        assert "abc_cascade" in SCENARIO_CATEGORIES


class TestCountScenarios:
    def test_count_ge_65(self):
        assert count_scenarios() >= 65

    def test_count_ge_min(self):
        assert count_scenarios() >= MIN_SCENARIOS

    def test_count_matches_list(self):
        assert count_scenarios() == len(get_all_scenarios())


class TestGetAllScenarios:
    def setup_method(self):
        self.scenarios = get_all_scenarios()

    def test_returns_list(self):
        assert isinstance(self.scenarios, list)

    def test_not_empty(self):
        assert len(self.scenarios) > 0

    def test_each_has_scenario_id(self):
        for s in self.scenarios:
            assert "scenario_id" in s

    def test_each_has_name(self):
        for s in self.scenarios:
            assert "name" in s

    def test_each_has_category(self):
        for s in self.scenarios:
            assert "category" in s

    def test_each_has_expected_status(self):
        for s in self.scenarios:
            assert "expected_status" in s

    def test_each_paper_only_true(self):
        for s in self.scenarios:
            assert s["paper_only"] is True

    def test_each_no_real_orders_true(self):
        for s in self.scenarios:
            assert s["no_real_orders"] is True

    def test_ids_start_with_s174(self):
        for s in self.scenarios:
            assert s["scenario_id"].startswith("S174-")

    def test_first_scenario_id(self):
        ids = [s["scenario_id"] for s in self.scenarios]
        assert "S174-001" in ids

    def test_deterministic_seed_on_each(self):
        for s in self.scenarios:
            assert s["deterministic_seed"] == 174

    def test_unique_ids(self):
        ids = [s["scenario_id"] for s in self.scenarios]
        assert len(ids) == len(set(ids))

    def test_schema_version_174(self):
        for s in self.scenarios:
            assert s["schema_version"] == "174"


class TestValidateRegistry:
    def test_validate_returns_dict(self):
        assert isinstance(validate_registry(), dict)

    def test_validate_valid_true(self):
        assert validate_registry()["valid"] is True

    def test_validate_count_ge_65(self):
        assert validate_registry()["count"] >= 65

    def test_validate_errors_empty(self):
        result = validate_registry()
        assert result.get("errors", []) == []
