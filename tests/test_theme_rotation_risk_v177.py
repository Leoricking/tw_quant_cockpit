"""tests/test_theme_rotation_risk_v177.py — v1.7.7 risk score tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
from paper_trading.small_capital_strategy.theme_rotation_risk_v177 import calculate_risk_score


class TestCalculateRiskScore:
    def test_returns_risk_score(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRiskScore
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, False, False, False)
        assert isinstance(result, ThemeRiskScore)

    def test_paper_only_true(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, False, False, False)
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, False, False, False)
        assert result.no_broker is True

    def test_zero_risk_all_false(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.0, False, False, False)
        assert result.score == 0.0

    def test_score_max_100(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 1.0, True, True, True)
        assert result.score == 100.0

    def test_margin_expansion_contribution(self):
        # 0.5 * 40 = 20
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, False, False, False)
        assert abs(result.score - 20.0) < 0.01

    def test_institutional_selling_adds_30(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.0, True, False, False)
        assert result.score == 30.0

    def test_volume_spike_adds_15(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.0, False, True, False)
        assert result.score == 15.0

    def test_overheated_adds_15(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.0, False, False, True)
        assert result.score == 15.0

    def test_all_risks_max_100(self):
        # 1.0*40 + 30 + 15 + 15 = 100
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 1.0, True, True, True)
        assert result.score == 100.0

    def test_score_bounded_min_0(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.0, False, False, False)
        assert result.score >= 0.0

    def test_theme_preserved(self):
        result = calculate_risk_score(ThemeCategory.SEMICONDUCTOR, 0.5, False, False, False)
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_institutional_selling_preserved(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, True, False, False)
        assert result.institutional_selling is True

    def test_volume_spike_preserved(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, False, True, False)
        assert result.volume_spike is True

    def test_overheated_preserved(self):
        result = calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, False, False, True)
        assert result.overheated is True
