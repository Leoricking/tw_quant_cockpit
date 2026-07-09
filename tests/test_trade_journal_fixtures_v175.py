"""
tests/test_trade_journal_fixtures_v175.py
Tests for Trade Journal fixture registry v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_fixture_registry_v175 import (
    FIXTURES, get_fixtures, get_fixture_by_id, count_fixtures, validate_registry, MIN_FIXTURES,
)
from paper_trading.small_capital_strategy.trade_journal_fixture_schema_v175 import (
    validate_fixture, get_fixture_schema, REQUIRED_FIXTURE_FIELDS, REQUIRED_SAFETY_MARKERS,
)


class TestFixtureCount:
    def test_count_ge_55(self):
        assert count_fixtures() >= 55

    def test_count_matches_fixtures_list(self):
        assert count_fixtures() == len(FIXTURES)

    def test_min_fixtures_constant(self):
        assert MIN_FIXTURES >= 55

    def test_count_meets_minimum(self):
        assert count_fixtures() >= MIN_FIXTURES


class TestGetFixtures:
    def test_returns_list(self):
        assert isinstance(get_fixtures(), list)

    def test_all_paper_only(self):
        assert all(f["paper_only"] for f in get_fixtures())

    def test_all_research_only(self):
        assert all(f["research_only"] for f in get_fixtures())

    def test_all_no_real_orders(self):
        assert all(f["no_real_orders"] for f in get_fixtures())

    def test_all_no_broker(self):
        assert all(f["no_broker"] for f in get_fixtures())

    def test_all_not_investment_advice(self):
        assert all(f["not_investment_advice"] for f in get_fixtures())

    def test_all_demo_only(self):
        assert all(f["demo_only"] for f in get_fixtures())

    def test_all_not_for_production(self):
        assert all(f["not_for_production"] for f in get_fixtures())

    def test_all_have_symbol(self):
        assert all("symbol" in f for f in get_fixtures())

    def test_all_have_entry_price(self):
        assert all("entry_price" in f for f in get_fixtures())

    def test_all_have_outcome(self):
        assert all("outcome" in f for f in get_fixtures())

    def test_all_have_abc_pattern(self):
        assert all("abc_pattern" in f for f in get_fixtures())

    def test_all_have_market_regime(self):
        assert all("market_regime" in f for f in get_fixtures())


class TestValidateRegistry:
    def test_registry_valid(self):
        result = validate_registry()
        assert result["valid"] is True

    def test_no_errors(self):
        result = validate_registry()
        assert result["errors"] == []


class TestGetFixtureById:
    def test_existing_id_found(self):
        assert get_fixture_by_id("F175-001") is not None

    def test_last_fixture_found(self):
        assert get_fixture_by_id("F175-055") is not None

    def test_nonexistent_returns_none(self):
        assert get_fixture_by_id("F175-999") is None

    def test_found_fixture_paper_only(self):
        f = get_fixture_by_id("F175-001")
        assert f["paper_only"] is True

    def test_first_fixture_2330(self):
        f = get_fixture_by_id("F175-001")
        assert f["symbol"] == "2330"


class TestFixtureSchema:
    def test_required_fields_list(self):
        assert isinstance(REQUIRED_FIXTURE_FIELDS, list)

    def test_required_fields_nonempty(self):
        assert len(REQUIRED_FIXTURE_FIELDS) > 0

    def test_required_safety_markers_nonempty(self):
        assert len(REQUIRED_SAFETY_MARKERS) > 0

    def test_get_fixture_schema_returns_dict(self):
        assert isinstance(get_fixture_schema(), dict)

    def test_validate_fixture_passes_good_fixture(self):
        f = get_fixture_by_id("F175-001")
        assert validate_fixture(f) is True

    def test_validate_fixture_fails_missing_field(self):
        bad = {"paper_only": True}
        assert validate_fixture(bad) is False


class TestFixtureIds:
    def test_all_ids_unique(self):
        ids = [f["id"] for f in get_fixtures()]
        assert len(ids) == len(set(ids))

    def test_ids_start_with_f175(self):
        assert all(f["id"].startswith("F175-") for f in get_fixtures())
