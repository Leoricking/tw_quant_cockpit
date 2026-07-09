"""
tests/test_risk_dashboard_fixtures_v174.py
Tests for fixture registry v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_fixture_registry_v174 import (
    get_all_fixtures, count_fixtures, validate_registry,
    MIN_FIXTURES, DETERMINISTIC_SEED,
)
from paper_trading.small_capital_strategy.risk_dashboard_fixture_schema_v174 import (
    make_fixture, validate_fixture,
)


class TestRegistryConstants:
    def test_min_fixtures_65(self):
        assert MIN_FIXTURES == 65

    def test_deterministic_seed_174(self):
        assert DETERMINISTIC_SEED == 174


class TestCountFixtures:
    def test_count_ge_65(self):
        assert count_fixtures() >= 65

    def test_count_ge_min(self):
        assert count_fixtures() >= MIN_FIXTURES

    def test_count_matches_list(self):
        assert count_fixtures() == len(get_all_fixtures())


class TestGetAllFixtures:
    def setup_method(self):
        self.fixtures = get_all_fixtures()

    def test_returns_list(self):
        assert isinstance(self.fixtures, list)

    def test_not_empty(self):
        assert len(self.fixtures) > 0

    def test_each_has_fixture_id(self):
        for f in self.fixtures:
            assert "fixture_id" in f

    def test_each_has_name(self):
        for f in self.fixtures:
            assert "name" in f

    def test_each_has_category(self):
        for f in self.fixtures:
            assert "category" in f

    def test_ids_start_with_f174(self):
        for f in self.fixtures:
            assert f["fixture_id"].startswith("F174-")

    def test_first_fixture_id(self):
        ids = [f["fixture_id"] for f in self.fixtures]
        assert "F174-001" in ids

    def test_unique_ids(self):
        ids = [f["fixture_id"] for f in self.fixtures]
        assert len(ids) == len(set(ids))

    def test_each_paper_only_true(self):
        for f in self.fixtures:
            assert f["paper_only"] is True

    def test_each_no_real_orders_true(self):
        for f in self.fixtures:
            assert f["no_real_orders"] is True

    def test_each_research_only_true(self):
        for f in self.fixtures:
            assert f["research_only"] is True

    def test_each_not_investment_advice_true(self):
        for f in self.fixtures:
            assert f["not_investment_advice"] is True


class TestMakeFixture:
    def test_make_fixture_returns_dict(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert isinstance(f, dict)

    def test_make_fixture_paper_only_true(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert f["paper_only"] is True

    def test_make_fixture_no_real_orders_true(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert f["no_real_orders"] is True

    def test_make_fixture_research_only_true(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert f["research_only"] is True

    def test_make_fixture_not_investment_advice_true(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert f["not_investment_advice"] is True

    def test_make_fixture_has_fixture_id(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert f["fixture_id"] == "F174-T01"

    def test_make_fixture_has_scenario_id(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        assert f["scenario_id"] == "S174-001"


class TestValidateFixture:
    def test_valid_fixture_passes(self):
        f = make_fixture("F174-T01", "test", "single_trade_risk", "S174-001", {}, {})
        result = validate_fixture(f)
        assert result["valid"] is True


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
