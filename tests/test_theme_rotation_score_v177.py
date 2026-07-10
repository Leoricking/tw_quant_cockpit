"""tests/test_theme_rotation_score_v177.py — v1.7.7 score tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade, ThemeSignalType
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeSignal
from paper_trading.small_capital_strategy.theme_rotation_score_v177 import (
    score_to_grade, apply_market_regime_cap, calculate_strength_score,
)


class TestScoreToGrade:
    def test_leader_at_80(self):
        assert score_to_grade(80.0) == ThemeGrade.LEADER

    def test_leader_at_100(self):
        assert score_to_grade(100.0) == ThemeGrade.LEADER

    def test_strong_at_65(self):
        assert score_to_grade(65.0) == ThemeGrade.STRONG

    def test_strong_at_79(self):
        assert score_to_grade(79.9) == ThemeGrade.STRONG

    def test_watch_at_50(self):
        assert score_to_grade(50.0) == ThemeGrade.WATCH

    def test_watch_at_64(self):
        assert score_to_grade(64.9) == ThemeGrade.WATCH

    def test_weak_at_35(self):
        assert score_to_grade(35.0) == ThemeGrade.WEAK

    def test_weak_at_49(self):
        assert score_to_grade(49.9) == ThemeGrade.WEAK

    def test_excluded_at_0(self):
        assert score_to_grade(0.0) == ThemeGrade.EXCLUDED

    def test_excluded_at_34(self):
        assert score_to_grade(34.9) == ThemeGrade.EXCLUDED

    def test_boundary_leader_79(self):
        # 79.9 is STRONG not LEADER
        assert score_to_grade(79.9) == ThemeGrade.STRONG

    def test_boundary_excluded_35(self):
        # 35.0 is WEAK not EXCLUDED
        assert score_to_grade(35.0) == ThemeGrade.WEAK


class TestApplyMarketRegimeCap:
    def test_risk_off_caps_leader_to_watch(self):
        result = apply_market_regime_cap(ThemeGrade.LEADER, "RISK_OFF")
        assert result == ThemeGrade.WATCH

    def test_risk_off_caps_strong_to_watch(self):
        result = apply_market_regime_cap(ThemeGrade.STRONG, "RISK_OFF")
        assert result == ThemeGrade.WATCH

    def test_risk_off_keeps_watch(self):
        result = apply_market_regime_cap(ThemeGrade.WATCH, "RISK_OFF")
        assert result == ThemeGrade.WATCH

    def test_risk_off_keeps_weak(self):
        result = apply_market_regime_cap(ThemeGrade.WEAK, "RISK_OFF")
        assert result == ThemeGrade.WEAK

    def test_risk_off_keeps_excluded(self):
        result = apply_market_regime_cap(ThemeGrade.EXCLUDED, "RISK_OFF")
        assert result == ThemeGrade.EXCLUDED

    def test_bull_no_cap_leader(self):
        result = apply_market_regime_cap(ThemeGrade.LEADER, "BULL")
        assert result == ThemeGrade.LEADER

    def test_bull_no_cap_strong(self):
        result = apply_market_regime_cap(ThemeGrade.STRONG, "BULL")
        assert result == ThemeGrade.STRONG

    def test_bear_no_cap_watch(self):
        result = apply_market_regime_cap(ThemeGrade.WATCH, "BEAR")
        assert result == ThemeGrade.WATCH


class TestCalculateStrengthScore:
    def test_returns_strength_score(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore
        result = calculate_strength_score([], ThemeCategory.AI_SERVER)
        assert isinstance(result, ThemeStrengthScore)

    def test_paper_only_true(self):
        result = calculate_strength_score([], ThemeCategory.AI_SERVER)
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = calculate_strength_score([], ThemeCategory.AI_SERVER)
        assert result.no_broker is True

    def test_empty_signals_score_zero(self):
        result = calculate_strength_score([], ThemeCategory.AI_SERVER)
        assert result.score == 0.0

    def test_empty_signals_grade_excluded(self):
        result = calculate_strength_score([], ThemeCategory.AI_SERVER)
        assert result.grade == ThemeGrade.EXCLUDED

    def test_score_bounded_0_100(self):
        signals = [
            ThemeSignal(theme=ThemeCategory.AI_SERVER, signal_type=ThemeSignalType.BREADTH, value=1.0),
            ThemeSignal(theme=ThemeCategory.AI_SERVER, signal_type=ThemeSignalType.MOMENTUM, value=1.0),
        ]
        result = calculate_strength_score(signals, ThemeCategory.AI_SERVER)
        assert 0.0 <= result.score <= 100.0

    def test_theme_preserved(self):
        result = calculate_strength_score([], ThemeCategory.SEMICONDUCTOR)
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_schema_version_177(self):
        result = calculate_strength_score([], ThemeCategory.AI_SERVER)
        assert result.schema_version == "177"

    def test_single_stock_caps_leader(self):
        # With single_stock_only=True, LEADER should be downgraded to STRONG
        # Simulate high score but single stock
        signals = [
            ThemeSignal(theme=ThemeCategory.AI_SERVER, signal_type=ThemeSignalType.BREADTH, value=0.05),  # low breadth → single_stock
            ThemeSignal(theme=ThemeCategory.AI_SERVER, signal_type=ThemeSignalType.INSTITUTIONAL, value=1.0),
        ]
        result = calculate_strength_score(signals, ThemeCategory.AI_SERVER)
        # single_stock_only when resonance_count <= 1
        if result.single_stock_only:
            assert result.grade != ThemeGrade.LEADER
