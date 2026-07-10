"""tests/test_theme_rotation_breadth_v177.py — v1.7.7 breadth score tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
from paper_trading.small_capital_strategy.theme_rotation_breadth_v177 import calculate_breadth_score


class TestCalculateBreadthScore:
    def test_returns_breadth_score(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeBreadthScore
        result = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
        assert isinstance(result, ThemeBreadthScore)

    def test_score_80_percent(self):
        result = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
        assert result.score == 80.0

    def test_score_100_percent(self):
        result = calculate_breadth_score(10, 0, 10, ThemeCategory.AI_SERVER)
        assert result.score == 100.0

    def test_score_zero_percent(self):
        result = calculate_breadth_score(0, 10, 10, ThemeCategory.AI_SERVER)
        assert result.score == 0.0

    def test_zero_total_score_zero(self):
        result = calculate_breadth_score(0, 0, 0, ThemeCategory.AI_SERVER)
        assert result.score == 0.0

    def test_advance_decline_ratio(self):
        result = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
        assert result.advance_decline_ratio == 4.0

    def test_advance_decline_ratio_zero_declining(self):
        result = calculate_breadth_score(8, 0, 8, ThemeCategory.AI_SERVER)
        assert result.advance_decline_ratio == 8.0

    def test_advancing_count_preserved(self):
        result = calculate_breadth_score(7, 3, 10, ThemeCategory.AI_SERVER)
        assert result.advancing == 7

    def test_declining_count_preserved(self):
        result = calculate_breadth_score(7, 3, 10, ThemeCategory.AI_SERVER)
        assert result.declining == 3

    def test_total_count_preserved(self):
        result = calculate_breadth_score(7, 3, 10, ThemeCategory.AI_SERVER)
        assert result.total == 10

    def test_theme_preserved(self):
        result = calculate_breadth_score(5, 5, 10, ThemeCategory.SEMICONDUCTOR)
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_paper_only_true(self):
        result = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
        assert result.no_broker is True

    def test_score_bounded_max_100(self):
        result = calculate_breadth_score(100, 0, 100, ThemeCategory.AI_SERVER)
        assert result.score <= 100.0

    def test_score_bounded_min_0(self):
        result = calculate_breadth_score(0, 100, 100, ThemeCategory.AI_SERVER)
        assert result.score >= 0.0
