"""tests/test_theme_rotation_report_v177.py — v1.7.7 report tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore, ThemeRotationDashboard
from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import rank_themes
from paper_trading.small_capital_strategy.theme_rotation_dashboard_v177 import build_dashboard
from paper_trading.small_capital_strategy.theme_rotation_report_v177 import build_report, get_report_sections


def _dash():
    ss = [
        ThemeStrengthScore(theme=ThemeCategory.AI_SERVER, score=90.0, grade=ThemeGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.SEMICONDUCTOR, score=70.0, grade=ThemeGrade.STRONG),
    ]
    ranks = rank_themes(ss)
    return build_dashboard(ranks, "2026-07-10", "BULL")


class TestBuildReport:
    def test_returns_report(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationReport
        result = build_report(_dash())
        assert isinstance(result, ThemeRotationReport)

    def test_paper_only_true(self):
        result = build_report(_dash())
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = build_report(_dash())
        assert result.no_broker is True

    def test_sections_count_5(self):
        result = build_report(_dash())
        assert len(result.sections) == 5

    def test_sections_has_executive_summary(self):
        result = build_report(_dash())
        assert "executive_summary" in result.sections

    def test_sections_has_theme_ranking(self):
        result = build_report(_dash())
        assert "theme_ranking" in result.sections

    def test_sections_has_leader_analysis(self):
        result = build_report(_dash())
        assert "leader_analysis" in result.sections

    def test_sections_has_risk_flags(self):
        result = build_report(_dash())
        assert "risk_flags" in result.sections

    def test_sections_has_watchlist_candidates(self):
        result = build_report(_dash())
        assert "watchlist_candidates" in result.sections

    def test_top_theme_is_ai_server(self):
        result = build_report(_dash())
        assert result.top_theme == ThemeCategory.AI_SERVER

    def test_date_from_dashboard(self):
        result = build_report(_dash())
        assert result.date == "2026-07-10"

    def test_format_text(self):
        result = build_report(_dash())
        assert result.report_format == "text"

    def test_schema_version_177(self):
        result = build_report(_dash())
        assert result.schema_version == "177"

    def test_empty_dashboard_top_theme_unknown(self):
        empty_dash = ThemeRotationDashboard(date="2026-07-10", top_themes=[])
        result = build_report(empty_dash)
        assert result.top_theme == ThemeCategory.UNKNOWN


class TestGetReportSections:
    def test_returns_list(self):
        result = get_report_sections()
        assert isinstance(result, list)

    def test_count_5(self):
        result = get_report_sections()
        assert len(result) == 5

    def test_has_executive_summary(self):
        assert "executive_summary" in get_report_sections()

    def test_has_watchlist_candidates(self):
        assert "watchlist_candidates" in get_report_sections()
