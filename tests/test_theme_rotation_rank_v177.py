"""tests/test_theme_rotation_rank_v177.py — v1.7.7 rank tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore
from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import (
    rank_themes, get_top_n_themes, get_leader_themes,
)


def _make_ss(theme, score, grade):
    return ThemeStrengthScore(theme=theme, score=score, grade=grade)


class TestRankThemes:
    def test_empty_list_returns_empty(self):
        result = rank_themes([])
        assert result == []

    def test_single_item_rank_1(self):
        ss = [_make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER)]
        result = rank_themes(ss)
        assert len(result) == 1
        assert result[0].rank == 1

    def test_sorted_descending(self):
        ss = [
            _make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER),
            _make_ss(ThemeCategory.SEMICONDUCTOR, 70.0, ThemeGrade.STRONG),
            _make_ss(ThemeCategory.PCB, 40.0, ThemeGrade.WEAK),
        ]
        result = rank_themes(ss)
        assert result[0].strength_score == 90.0
        assert result[1].strength_score == 70.0
        assert result[2].strength_score == 40.0

    def test_ranks_sequential(self):
        ss = [
            _make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER),
            _make_ss(ThemeCategory.SEMICONDUCTOR, 70.0, ThemeGrade.STRONG),
        ]
        result = rank_themes(ss)
        assert result[0].rank == 1
        assert result[1].rank == 2

    def test_paper_only_in_ranks(self):
        ss = [_make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER)]
        result = rank_themes(ss)
        assert result[0].paper_only is True

    def test_grade_preserved(self):
        ss = [_make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER)]
        result = rank_themes(ss)
        assert result[0].grade == ThemeGrade.LEADER


class TestGetTopNThemes:
    def test_top_3_from_5(self):
        ss = [
            _make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER),
            _make_ss(ThemeCategory.SEMICONDUCTOR, 70.0, ThemeGrade.STRONG),
            _make_ss(ThemeCategory.GPU_SERVER, 65.0, ThemeGrade.STRONG),
            _make_ss(ThemeCategory.PCB, 50.0, ThemeGrade.WATCH),
            _make_ss(ThemeCategory.CCL, 35.0, ThemeGrade.WEAK),
        ]
        ranks = rank_themes(ss)
        top3 = get_top_n_themes(ranks, 3)
        assert len(top3) == 3

    def test_top_n_larger_than_list(self):
        ss = [_make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER)]
        ranks = rank_themes(ss)
        top5 = get_top_n_themes(ranks, 5)
        assert len(top5) == 1

    def test_top_n_order_preserved(self):
        ss = [
            _make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER),
            _make_ss(ThemeCategory.SEMICONDUCTOR, 70.0, ThemeGrade.STRONG),
        ]
        ranks = rank_themes(ss)
        top2 = get_top_n_themes(ranks, 2)
        assert top2[0].strength_score == 90.0

    def test_top_0_returns_empty(self):
        ss = [_make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER)]
        ranks = rank_themes(ss)
        top0 = get_top_n_themes(ranks, 0)
        assert top0 == []


class TestGetLeaderThemes:
    def test_filters_leaders_only(self):
        ss = [
            _make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER),
            _make_ss(ThemeCategory.SEMICONDUCTOR, 70.0, ThemeGrade.STRONG),
            _make_ss(ThemeCategory.PCB, 40.0, ThemeGrade.WEAK),
        ]
        ranks = rank_themes(ss)
        leaders = get_leader_themes(ranks)
        assert len(leaders) == 1
        assert leaders[0].theme == ThemeCategory.AI_SERVER

    def test_no_leaders_returns_empty(self):
        ss = [_make_ss(ThemeCategory.PCB, 50.0, ThemeGrade.WATCH)]
        ranks = rank_themes(ss)
        leaders = get_leader_themes(ranks)
        assert leaders == []

    def test_multiple_leaders(self):
        ss = [
            _make_ss(ThemeCategory.AI_SERVER, 90.0, ThemeGrade.LEADER),
            _make_ss(ThemeCategory.SEMICONDUCTOR, 85.0, ThemeGrade.LEADER),
        ]
        ranks = rank_themes(ss)
        leaders = get_leader_themes(ranks)
        assert len(leaders) == 2
