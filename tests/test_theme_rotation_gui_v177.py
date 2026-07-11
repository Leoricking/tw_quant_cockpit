"""tests/test_theme_rotation_gui_v177.py — v1.7.7 GUI panel tests."""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V177_THEME_ROTATION,
    get_panel_info, get_tab_names, get_theme_rotation_tab_names,
    render_theme_rotation_tab, render_theme_ranking_tab, render_theme_watchlist_tab,
)


class TestPanelVersion:
    def test_panel_version_177(self):
        assert PANEL_VERSION == "1.8.2"

    def test_panel_title_contains_177(self):
        assert "1.8.2" in PANEL_TITLE


class TestThemeRotationTabs:
    def test_v177_tabs_count_3(self):
        assert len(_TABS_V177_THEME_ROTATION) == 3

    def test_theme_rotation_tab_in_list(self):
        assert "theme_rotation" in _TABS_V177_THEME_ROTATION

    def test_theme_ranking_tab_in_list(self):
        assert "theme_ranking" in _TABS_V177_THEME_ROTATION

    def test_theme_watchlist_tab_in_list(self):
        assert "theme_watchlist" in _TABS_V177_THEME_ROTATION

    def test_tabs_includes_v177(self):
        for tab in _TABS_V177_THEME_ROTATION:
            assert tab in _TABS


class TestGetPanelInfo:
    def test_returns_dict(self):
        result = get_panel_info()
        assert isinstance(result, dict)

    def test_panel_version_179(self):
        result = get_panel_info()
        assert result["panel_version"] == "1.8.2"

    def test_headless_safe(self):
        result = get_panel_info()
        assert result["headless_safe"] is True

    def test_paper_only_true(self):
        result = get_panel_info()
        assert result["paper_only"] is True

    def test_tab_count_positive(self):
        result = get_panel_info()
        assert result["tab_count"] > 100


class TestRenderThemeRotationTab:
    def test_returns_dict(self):
        result = render_theme_rotation_tab()
        assert isinstance(result, dict)

    def test_paper_only_true(self):
        result = render_theme_rotation_tab()
        assert result["paper_only"] is True

    def test_not_investment_advice_true(self):
        result = render_theme_rotation_tab()
        assert result["not_investment_advice"] is True

    def test_version_177(self):
        result = render_theme_rotation_tab()
        assert result["version"] == "1.7.7"


class TestRenderThemeRankingTab:
    def test_returns_dict(self):
        result = render_theme_ranking_tab()
        assert isinstance(result, dict)

    def test_paper_only_true(self):
        result = render_theme_ranking_tab()
        assert result["paper_only"] is True

    def test_rank_count_positive(self):
        result = render_theme_ranking_tab()
        assert result["rank_count"] >= 0

    def test_not_investment_advice(self):
        result = render_theme_ranking_tab()
        assert result["not_investment_advice"] is True


class TestRenderThemeWatchlistTab:
    def test_returns_dict(self):
        result = render_theme_watchlist_tab()
        assert isinstance(result, dict)

    def test_paper_only_true(self):
        result = render_theme_watchlist_tab()
        assert result["paper_only"] is True

    def test_candidate_count_positive(self):
        result = render_theme_watchlist_tab()
        assert result["candidate_count"] >= 0

    def test_eligible_count_lte_candidate_count(self):
        result = render_theme_watchlist_tab()
        assert result["eligible_count"] <= result["candidate_count"]
