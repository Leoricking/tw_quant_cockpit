"""tests/test_theme_rotation_dashboard_v177.py — v1.7.7 dashboard tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore
from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import rank_themes
from paper_trading.small_capital_strategy.theme_rotation_dashboard_v177 import build_dashboard


def _ranks():
    ss = [
        ThemeStrengthScore(theme=ThemeCategory.AI_SERVER, score=90.0, grade=ThemeGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.SEMICONDUCTOR, score=80.0, grade=ThemeGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.GPU_SERVER, score=70.0, grade=ThemeGrade.STRONG),
        ThemeStrengthScore(theme=ThemeCategory.PCB, score=50.0, grade=ThemeGrade.WATCH),
        ThemeStrengthScore(theme=ThemeCategory.CCL, score=35.0, grade=ThemeGrade.WEAK),
        ThemeStrengthScore(theme=ThemeCategory.BIOTECH, score=20.0, grade=ThemeGrade.EXCLUDED),
    ]
    return rank_themes(ss)


class TestBuildDashboard:
    def test_returns_dashboard(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationDashboard
        result = build_dashboard(_ranks(), "2026-07-10")
        assert isinstance(result, ThemeRotationDashboard)

    def test_paper_only_true(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.no_broker is True

    def test_no_real_orders_true(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.no_real_orders is True

    def test_date_preserved(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.date == "2026-07-10"

    def test_market_regime_default_bull(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.market_regime == "BULL"

    def test_market_regime_custom(self):
        result = build_dashboard(_ranks(), "2026-07-10", "RISK_OFF")
        assert result.market_regime == "RISK_OFF"

    def test_top_themes_max_5(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert len(result.top_themes) <= 5

    def test_total_themes_count(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.total_themes == 6

    def test_leader_count(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.leader_count == 2

    def test_strong_count(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert result.strong_count == 1

    def test_sections_count_4(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert len(result.sections) == 4

    def test_sections_contains_theme_ranking(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert "theme_ranking" in result.sections

    def test_sections_contains_leader_themes(self):
        result = build_dashboard(_ranks(), "2026-07-10")
        assert "leader_themes" in result.sections

    def test_empty_ranks_dashboard(self):
        result = build_dashboard([], "2026-07-10")
        assert result.total_themes == 0
        assert result.leader_count == 0
