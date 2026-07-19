"""
tests/test_portfolio_governance_fixtures_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Fixture Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_fixtures_v198 import (
    _FIXTURES, get_fixtures, get_fixture_by_id,
)

REQUIRED_FIELDS = [
    "id", "fixture_id", "schema_version", "name",
    "paper_only", "research_only", "simulate_only", "validation_only",
    "portfolio_governance_only", "risk_overlay_only", "dashboard_only",
    "report_only", "audit_only", "no_real_orders", "no_broker",
    "no_margin", "no_leverage", "no_production_strategy_mutation",
    "no_automatic_rollback", "no_live_strategy_activation",
    "not_investment_advice", "demo_only", "not_for_production",
    "production_trading_blocked", "expected_outcome",
]


class TestGetFixtures:
    def test_returns_list(self):
        assert isinstance(get_fixtures(), list)

    def test_count_75(self):
        assert len(get_fixtures()) == 75

    def test_all_paper_only_True(self):
        assert all(f["paper_only"] is True for f in get_fixtures())

    def test_all_no_real_orders_True(self):
        assert all(f["no_real_orders"] is True for f in get_fixtures())

    def test_all_schema_version_198(self):
        assert all(f["schema_version"] == "198" for f in get_fixtures())

    def test_all_not_investment_advice_True(self):
        assert all(f["not_investment_advice"] is True for f in get_fixtures())

    def test_all_demo_only_True(self):
        assert all(f["demo_only"] is True for f in get_fixtures())

    def test_all_production_trading_blocked_True(self):
        assert all(f["production_trading_blocked"] is True for f in get_fixtures())

    def test_all_have_required_fields(self):
        for f in get_fixtures():
            for field in REQUIRED_FIELDS:
                assert field in f, f"Fixture {f.get('fixture_id')} missing field: {field}"

    def test_all_ids_unique(self):
        ids = [f["fixture_id"] for f in get_fixtures()]
        assert len(ids) == len(set(ids))

    def test_first_id_is_PGF198_001(self):
        assert get_fixtures()[0]["fixture_id"] == "PGF198-001"

    def test_last_id_is_PGF198_075(self):
        assert get_fixtures()[74]["fixture_id"] == "PGF198-075"

    def test_all_names_are_strings(self):
        assert all(isinstance(f["name"], str) for f in get_fixtures())

    def test_all_expected_outcomes_are_strings(self):
        assert all(isinstance(f["expected_outcome"], str) for f in get_fixtures())


class TestGetFixtureById:
    def test_returns_dict_for_valid_id(self):
        assert isinstance(get_fixture_by_id("PGF198-001"), dict)

    def test_returns_correct_fixture(self):
        f = get_fixture_by_id("PGF198-001")
        assert f["fixture_id"] == "PGF198-001"

    def test_returns_PGF198_025(self):
        f = get_fixture_by_id("PGF198-025")
        assert f["fixture_id"] == "PGF198-025"

    def test_returns_PGF198_075(self):
        f = get_fixture_by_id("PGF198-075")
        assert f["fixture_id"] == "PGF198-075"

    def test_unknown_id_returns_empty_dict(self):
        assert get_fixture_by_id("UNKNOWN-999") == {}

    def test_empty_string_returns_empty_dict(self):
        assert get_fixture_by_id("") == {}

    def test_found_fixture_paper_only_True(self):
        f = get_fixture_by_id("PGF198-010")
        assert f["paper_only"] is True


class TestFixtureRaw:
    def test_raw_count_75(self):
        assert len(_FIXTURES) == 75

    def test_all_no_broker_True(self):
        assert all(f["no_broker"] is True for f in _FIXTURES)

    def test_fixture_1_is_valid_input(self):
        f = _FIXTURES[0]
        assert "valid" in f["name"].lower() or "input" in f["name"].lower()

    def test_fixture_65_has_assert_safe(self):
        f = get_fixture_by_id("PGF198-065")
        assert "safe" in f["name"].lower() or "ValueError" in f["expected_outcome"]

    def test_all_no_leverage_True(self):
        assert all(f["no_leverage"] is True for f in _FIXTURES)
