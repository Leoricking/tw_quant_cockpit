"""tests/test_theme_rotation_fixtures_v177.py — v1.7.7 fixture tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_fixture_registry_v177 import (
    get_fixtures, count_fixtures, validate_registry, validate_all_fixtures, get_fixtures_by_theme,
)


class TestGetFixtures:
    def test_returns_list(self):
        result = get_fixtures()
        assert isinstance(result, list)

    def test_count_ge_65(self):
        result = get_fixtures()
        assert len(result) >= 65

    def test_all_paper_only(self):
        for f in get_fixtures():
            assert f["paper_only"] is True

    def test_all_no_real_orders(self):
        for f in get_fixtures():
            assert f["no_real_orders"] is True

    def test_all_no_broker(self):
        for f in get_fixtures():
            assert f["no_broker"] is True

    def test_all_demo_only(self):
        for f in get_fixtures():
            assert f["demo_only"] is True

    def test_all_have_id(self):
        for f in get_fixtures():
            assert "id" in f

    def test_all_have_theme(self):
        for f in get_fixtures():
            assert "theme" in f

    def test_all_have_symbol(self):
        for f in get_fixtures():
            assert "symbol" in f


class TestCountFixtures:
    def test_count_ge_65(self):
        assert count_fixtures() >= 65

    def test_count_matches_list(self):
        assert count_fixtures() == len(get_fixtures())


class TestValidateRegistry:
    def test_returns_dict(self):
        result = validate_registry()
        assert isinstance(result, dict)

    def test_valid_true(self):
        result = validate_registry()
        assert result["valid"] is True

    def test_count_correct(self):
        result = validate_registry()
        assert result["count"] == count_fixtures()

    def test_errors_empty(self):
        result = validate_registry()
        assert result["errors"] == []


class TestGetFixturesByTheme:
    def test_ai_server_fixtures(self):
        result = get_fixtures_by_theme("AI_SERVER")
        assert len(result) > 0

    def test_semiconductor_fixtures(self):
        result = get_fixtures_by_theme("SEMICONDUCTOR")
        assert len(result) > 0

    def test_unknown_theme_empty(self):
        result = get_fixtures_by_theme("NONEXISTENT_THEME")
        assert result == []

    def test_filtered_by_theme(self):
        result = get_fixtures_by_theme("COOLING")
        for f in result:
            assert f["theme"] == "COOLING"
