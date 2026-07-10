"""tests/test_theme_rotation_scenarios_v177.py — v1.7.7 scenarios tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_scenarios_v177 import (
    get_scenarios, count_scenarios, get_scenario_by_id,
)


class TestGetScenarios:
    def test_returns_list(self):
        result = get_scenarios()
        assert isinstance(result, list)

    def test_count_ge_65(self):
        result = get_scenarios()
        assert len(result) >= 65

    def test_all_paper_only(self):
        for s in get_scenarios():
            assert s["paper_only"] is True

    def test_all_research_only(self):
        for s in get_scenarios():
            assert s["research_only"] is True

    def test_all_no_real_orders(self):
        for s in get_scenarios():
            assert s["no_real_orders"] is True

    def test_all_no_broker(self):
        for s in get_scenarios():
            assert s["no_broker"] is True

    def test_all_demo_only(self):
        for s in get_scenarios():
            assert s["demo_only"] is True

    def test_all_not_for_production(self):
        for s in get_scenarios():
            assert s["not_for_production"] is True

    def test_all_have_id(self):
        for s in get_scenarios():
            assert "id" in s
            assert s["id"].startswith("SC177-")

    def test_all_have_theme(self):
        for s in get_scenarios():
            assert "theme" in s

    def test_all_have_expected_grade(self):
        for s in get_scenarios():
            assert "expected_grade" in s


class TestCountScenarios:
    def test_count_ge_65(self):
        assert count_scenarios() >= 65

    def test_count_matches_list(self):
        assert count_scenarios() == len(get_scenarios())


class TestGetScenarioById:
    def test_find_sc177_001(self):
        result = get_scenario_by_id("SC177-001")
        assert result is not None

    def test_find_sc177_065(self):
        result = get_scenario_by_id("SC177-065")
        assert result is not None

    def test_not_found_returns_none(self):
        result = get_scenario_by_id("SC177-NOTEXIST")
        assert result is None

    def test_found_scenario_has_correct_id(self):
        result = get_scenario_by_id("SC177-001")
        assert result["id"] == "SC177-001"
