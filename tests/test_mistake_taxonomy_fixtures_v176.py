"""tests/test_mistake_taxonomy_fixtures_v176.py — v1.7.6 fixture tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_fixture_registry_v176 import (
    get_fixtures, count_fixtures, validate_registry,
    get_fixtures_by_week, get_fixtures_by_category,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_fixture_schema_v176 import (
    validate_fixture, validate_all_fixtures, REQUIRED_SAFETY_FIELDS,
)


class TestFixtureCount:
    def test_count_ge_60(self):
        assert count_fixtures() >= 60

    def test_count_matches_list(self):
        assert count_fixtures() == len(get_fixtures())


class TestFixtureContent:
    def test_all_paper_only(self):
        assert all(f["paper_only"] is True for f in get_fixtures())

    def test_all_research_only(self):
        assert all(f["research_only"] is True for f in get_fixtures())

    def test_all_no_real_orders(self):
        assert all(f["no_real_orders"] is True for f in get_fixtures())

    def test_all_no_broker(self):
        assert all(f["no_broker"] is True for f in get_fixtures())

    def test_all_not_investment_advice(self):
        assert all(f["not_investment_advice"] is True for f in get_fixtures())

    def test_all_demo_only(self):
        assert all(f["demo_only"] is True for f in get_fixtures())

    def test_all_not_for_production(self):
        assert all(f["not_for_production"] is True for f in get_fixtures())

    def test_all_have_id(self):
        assert all(len(f["id"]) > 0 for f in get_fixtures())

    def test_all_have_symbol(self):
        assert all(len(f["symbol"]) > 0 for f in get_fixtures())

    def test_all_have_week_label(self):
        assert all(len(f["week_label"]) > 0 for f in get_fixtures())

    def test_blocking_fixtures_exist(self):
        assert any(f["severity"] == "BLOCKING" for f in get_fixtures())

    def test_high_severity_fixtures_exist(self):
        assert any(f["severity"] == "HIGH" for f in get_fixtures())


class TestValidateRegistry:
    def test_registry_valid(self):
        result = validate_registry()
        assert result["all_valid"] is True

    def test_registry_zero_invalid(self):
        result = validate_registry()
        assert result["invalid_count"] == 0


class TestGetFixtureHelpers:
    def test_get_by_week_w01(self):
        fx = get_fixtures_by_week("2026-W01")
        assert len(fx) > 0

    def test_get_by_week_nonexistent(self):
        fx = get_fixtures_by_week("1900-W99")
        assert fx == []

    def test_get_by_category_no_stop_loss(self):
        fx = get_fixtures_by_category("NO_STOP_LOSS")
        assert len(fx) > 0

    def test_get_by_category_none_type(self):
        fx = get_fixtures_by_category("NONE")
        assert isinstance(fx, list)


class TestFixtureSchemaValidation:
    def test_required_safety_fields_list(self):
        assert isinstance(REQUIRED_SAFETY_FIELDS, list)
        assert len(REQUIRED_SAFETY_FIELDS) == 7

    def test_validate_fixture_valid(self):
        fx = get_fixtures()[0]
        result = validate_fixture(fx)
        assert result["valid"] is True

    def test_validate_all_fixtures_all_valid(self):
        result = validate_all_fixtures(get_fixtures())
        assert result["all_valid"] is True
