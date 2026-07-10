"""tests/test_theme_rotation_momentum_v177.py — v1.7.7 momentum score tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
from paper_trading.small_capital_strategy.theme_rotation_momentum_v177 import calculate_momentum_score


class TestCalculateMomentumScore:
    def test_returns_momentum_score(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeMomentumScore
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert isinstance(result, ThemeMomentumScore)

    def test_paper_only_true(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.no_broker is True

    def test_score_bounded_min_0(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, -100.0, -100.0, -100.0)
        assert result.score >= 0.0

    def test_score_bounded_max_100(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 200.0, 200.0, 200.0)
        assert result.score <= 100.0

    def test_zero_inputs_zero_score(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 0.0, 0.0, 0.0)
        assert result.score == 0.0

    def test_week_change_preserved(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.week_change_pct == 10.0

    def test_month_change_preserved(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.month_change_pct == 20.0

    def test_relative_strength_preserved(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.relative_strength == 30.0

    def test_theme_preserved(self):
        result = calculate_momentum_score(ThemeCategory.SEMICONDUCTOR, 10.0, 20.0, 30.0)
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_weighted_formula(self):
        # score = 10*0.4 + 20*0.3 + 30*0.3 = 4 + 6 + 9 = 19
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert abs(result.score - 19.0) < 0.01

    def test_schema_version_177(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.schema_version == "177"

    def test_negative_inputs_clamped(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, -50.0, -50.0, -50.0)
        assert result.score == 0.0

    def test_high_inputs_clamped(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 500.0, 500.0, 500.0)
        assert result.score == 100.0

    def test_not_investment_advice_true(self):
        result = calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0)
        assert result.not_investment_advice is True
