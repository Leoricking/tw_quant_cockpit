"""
tests/test_market_regime_fixtures_v173.py
Tests for Market Regime Position Control fixture_registry_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_fixture_schema_v173 import (
    validate_fixture, make_fixture, get_required_fields, get_required_input_fields,
)
from paper_trading.small_capital_strategy.market_regime_fixture_registry_v173 import (
    get_all_fixtures, get_fixture_by_id, get_fixtures_by_category,
    count_fixtures, validate_registry, MIN_FIXTURES, DETERMINISTIC_SEED,
)


class TestFixtureCount:
    def test_count_ge_65(self):
        assert count_fixtures() >= MIN_FIXTURES

    def test_count_ge_65_direct(self):
        assert count_fixtures() >= 65

    def test_get_all_returns_list(self):
        assert isinstance(get_all_fixtures(), list)

    def test_get_all_length_matches_count(self):
        assert len(get_all_fixtures()) == count_fixtures()


class TestFixtureStructure:
    def test_all_have_fixture_id(self):
        for f in get_all_fixtures():
            assert "fixture_id" in f

    def test_all_have_name(self):
        for f in get_all_fixtures():
            assert "name" in f

    def test_all_have_category(self):
        for f in get_all_fixtures():
            assert "category" in f

    def test_all_have_scenario_id(self):
        for f in get_all_fixtures():
            assert "scenario_id" in f

    def test_all_paper_only_true(self):
        for f in get_all_fixtures():
            assert f.get("paper_only") is True

    def test_all_no_real_orders_true(self):
        for f in get_all_fixtures():
            assert f.get("no_real_orders") is True

    def test_all_deterministic_seed_173(self):
        for f in get_all_fixtures():
            assert f["deterministic_seed"] == DETERMINISTIC_SEED

    def test_no_duplicate_ids(self):
        ids = [f["fixture_id"] for f in get_all_fixtures()]
        assert len(ids) == len(set(ids))


class TestGetFixtureById:
    def test_f173_001_found(self):
        f = get_fixture_by_id("F173-001")
        assert f.get("fixture_id") == "F173-001"

    def test_not_found_returns_empty(self):
        f = get_fixture_by_id("NONEXISTENT-999")
        assert not f

    def test_f173_065_found(self):
        f = get_fixture_by_id("F173-065")
        assert f.get("fixture_id") == "F173-065"


class TestGetFixturesByCategory:
    def test_bull_detection_category(self):
        fixtures = get_fixtures_by_category("bull_detection")
        assert len(fixtures) >= 1

    def test_cash_ratio_category(self):
        fixtures = get_fixtures_by_category("cash_ratio")
        assert len(fixtures) >= 1


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


class TestValidateFixture:
    def test_valid_fixture_passes(self):
        f = make_fixture(
            "F173-TEST", "test_fixture", "test", "S173-001",
            {"index_close": 20000.0, "index_ma20": 19500.0, "index_ma60": 18800.0,
             "index_ma120": 17500.0, "index_ma240": 16000.0},
            {"regime": "BULL"},
        )
        result = validate_fixture(f)
        assert result["valid"] is True

    def test_missing_field_fails(self):
        f = {"fixture_id": "F173-X", "name": "test", "paper_only": True, "no_real_orders": True,
             "inputs": {"index_close": 1.0, "index_ma20": 1.0, "index_ma60": 1.0, "index_ma120": 1.0, "index_ma240": 1.0},
             "expected": {}, "deterministic_seed": 173}
        # missing category and scenario_id
        result = validate_fixture(f)
        assert result["valid"] is False

    def test_paper_only_false_fails(self):
        f = make_fixture("F173-X", "t", "c", "S173-001",
                        {"index_close": 1.0, "index_ma20": 1.0, "index_ma60": 1.0, "index_ma120": 1.0, "index_ma240": 1.0},
                        {})
        f["paper_only"] = False
        result = validate_fixture(f)
        assert result["valid"] is False


class TestRequiredFields:
    def test_get_required_fields_not_empty(self):
        assert len(get_required_fields()) > 0

    def test_fixture_id_required(self):
        assert "fixture_id" in get_required_fields()

    def test_required_input_fields_not_empty(self):
        assert len(get_required_input_fields()) > 0

    def test_index_close_required(self):
        assert "index_close" in get_required_input_fields()
