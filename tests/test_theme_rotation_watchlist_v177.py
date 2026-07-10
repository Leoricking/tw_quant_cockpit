"""tests/test_theme_rotation_watchlist_v177.py — v1.7.7 watchlist tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade
from paper_trading.small_capital_strategy.theme_rotation_watchlist_v177 import (
    build_watchlist_candidate, filter_eligible_candidates, get_watchlist_by_theme,
)


class TestBuildWatchlistCandidate:
    def test_returns_candidate(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeWatchlistCandidate
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "Leader stock")
        assert isinstance(result, ThemeWatchlistCandidate)

    def test_leader_is_eligible(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        assert result.eligible is True

    def test_strong_is_eligible(self):
        result = build_watchlist_candidate("2317", ThemeCategory.AI_SERVER, ThemeGrade.STRONG, "x")
        assert result.eligible is True

    def test_watch_is_not_eligible(self):
        result = build_watchlist_candidate("2395", ThemeCategory.PCB, ThemeGrade.WATCH, "x")
        assert result.eligible is False

    def test_weak_is_not_eligible(self):
        result = build_watchlist_candidate("2395", ThemeCategory.PCB, ThemeGrade.WEAK, "x")
        assert result.eligible is False

    def test_excluded_is_not_eligible(self):
        result = build_watchlist_candidate("2395", ThemeCategory.PCB, ThemeGrade.EXCLUDED, "x")
        assert result.eligible is False

    def test_symbol_preserved(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        assert result.symbol == "2330"

    def test_theme_preserved(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_grade_preserved(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        assert result.grade == ThemeGrade.LEADER

    def test_reason_preserved(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "Strong leader")
        assert result.reason == "Strong leader"

    def test_paper_only_true(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        assert result.no_broker is True


class TestFilterEligibleCandidates:
    def test_empty_list(self):
        result = filter_eligible_candidates([])
        assert result == []

    def test_filters_eligible(self):
        c1 = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        c2 = build_watchlist_candidate("2395", ThemeCategory.PCB, ThemeGrade.WATCH, "x")
        result = filter_eligible_candidates([c1, c2])
        assert len(result) == 1
        assert result[0].symbol == "2330"

    def test_all_eligible(self):
        c1 = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        c2 = build_watchlist_candidate("2317", ThemeCategory.AI_SERVER, ThemeGrade.STRONG, "x")
        result = filter_eligible_candidates([c1, c2])
        assert len(result) == 2

    def test_none_eligible(self):
        c1 = build_watchlist_candidate("2395", ThemeCategory.PCB, ThemeGrade.WATCH, "x")
        result = filter_eligible_candidates([c1])
        assert result == []


class TestGetWatchlistByTheme:
    def test_empty_list(self):
        result = get_watchlist_by_theme([], ThemeCategory.AI_SERVER)
        assert result == []

    def test_filters_by_theme(self):
        c1 = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        c2 = build_watchlist_candidate("2317", ThemeCategory.AI_SERVER, ThemeGrade.LEADER, "x")
        result = get_watchlist_by_theme([c1, c2], ThemeCategory.AI_SERVER)
        assert len(result) == 1
        assert result[0].symbol == "2317"

    def test_no_match_returns_empty(self):
        c1 = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x")
        result = get_watchlist_by_theme([c1], ThemeCategory.ROBOTICS)
        assert result == []
