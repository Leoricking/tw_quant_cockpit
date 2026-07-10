"""tests/test_theme_rotation_continuation_v177.py — v1.7.7 continuation score tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
from paper_trading.small_capital_strategy.theme_rotation_continuation_v177 import calculate_continuation_score


class TestCalculateContinuationScore:
    def test_returns_continuation_score(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeContinuationScore
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 3, True, True)
        assert isinstance(result, ThemeContinuationScore)

    def test_paper_only_true(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 3, True, True)
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 3, True, True)
        assert result.no_broker is True

    def test_score_zero_all_false(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 0, False, False)
        assert result.score == 0.0

    def test_score_pulls_both_booleans(self):
        # 3*10 + 20 + 20 = 70
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 3, True, True)
        assert result.score == 70.0

    def test_score_only_pullback_shallow(self):
        # 0 + 20 + 0 = 20
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 0, True, False)
        assert result.score == 20.0

    def test_score_only_holding_gain(self):
        # 0 + 0 + 20 = 20
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 0, False, True)
        assert result.score == 20.0

    def test_score_capped_at_100(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 20, True, True)
        assert result.score == 100.0

    def test_score_bounded_min_0(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 0, False, False)
        assert result.score >= 0.0

    def test_consecutive_up_days_preserved(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 5, False, False)
        assert result.consecutive_up_days == 5

    def test_pullback_shallow_preserved(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 0, True, False)
        assert result.pullback_shallow is True

    def test_holding_gain_preserved(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 0, False, True)
        assert result.holding_gain is True

    def test_theme_preserved(self):
        result = calculate_continuation_score(ThemeCategory.SEMICONDUCTOR, 3, True, True)
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_schema_version_177(self):
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 3, True, True)
        assert result.schema_version == "177"

    def test_five_up_days(self):
        # 5*10 + 0 + 0 = 50
        result = calculate_continuation_score(ThemeCategory.AI_SERVER, 5, False, False)
        assert result.score == 50.0
