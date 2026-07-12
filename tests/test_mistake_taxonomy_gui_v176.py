"""tests/test_mistake_taxonomy_gui_v176.py — v1.7.6 GUI panel tests."""
import pytest
from gui.small_capital_strategy_panel import (
    get_panel_info, get_tab_names, get_mistake_taxonomy_tab_names,
    render_mistake_review_overview_tab, render_behavior_risk_score_tab,
    PANEL_VERSION, PANEL_TITLE,
    _TABS_V176_MISTAKE_TAXONOMY,
)


class TestPanelMetadata:
    def test_panel_version_176(self):
        assert PANEL_VERSION == "1.8.3"

    def test_panel_title_contains_176(self):
        assert "1.8.3" in PANEL_TITLE

    def test_tab_count_ge_111(self):
        info = get_panel_info()
        assert info["tab_count"] >= 111

    def test_panel_paper_only(self):
        info = get_panel_info()
        assert info["paper_only"] is True

    def test_panel_research_only(self):
        info = get_panel_info()
        assert info["research_only"] is True

    def test_panel_headless_safe(self):
        info = get_panel_info()
        assert info["headless_safe"] is True

    def test_panel_no_real_orders(self):
        info = get_panel_info()
        assert info["no_real_orders"] is True


class TestMistakeTaxonomyTabs:
    def test_mistake_taxonomy_tabs_count_13(self):
        assert len(_TABS_V176_MISTAKE_TAXONOMY) == 13

    def test_get_mistake_taxonomy_tab_names_ge_13(self):
        assert len(get_mistake_taxonomy_tab_names()) >= 13

    def test_weekly_review_tab_exists(self):
        assert "weekly_review" in _TABS_V176_MISTAKE_TAXONOMY

    def test_monthly_review_tab_exists(self):
        assert "monthly_review" in _TABS_V176_MISTAKE_TAXONOMY

    def test_behavior_risk_score_tab_exists(self):
        assert "behavior_risk_score" in _TABS_V176_MISTAKE_TAXONOMY

    def test_review_dashboard_tab_exists(self):
        assert "review_dashboard" in _TABS_V176_MISTAKE_TAXONOMY

    def test_review_health_tab_exists(self):
        assert "review_health" in _TABS_V176_MISTAKE_TAXONOMY

    def test_review_gate_tab_exists(self):
        assert "review_gate" in _TABS_V176_MISTAKE_TAXONOMY

    def test_all_tabs_include_mistake_taxonomy_tabs(self):
        all_tabs = get_tab_names()
        for tab in _TABS_V176_MISTAKE_TAXONOMY:
            assert tab in all_tabs


class TestRenderTabs:
    def test_render_overview_paper_only(self):
        result = render_mistake_review_overview_tab()
        assert result["paper_only"] is True

    def test_render_overview_not_investment_advice(self):
        result = render_mistake_review_overview_tab()
        assert result["not_investment_advice"] is True

    def test_render_behavior_risk_score_paper_only(self):
        result = render_behavior_risk_score_tab()
        assert result["paper_only"] is True

    def test_render_behavior_risk_score_has_score(self):
        result = render_behavior_risk_score_tab()
        assert "score" in result

    def test_render_behavior_risk_score_has_level(self):
        result = render_behavior_risk_score_tab()
        assert result["level"] in ("PASS", "WATCH", "WARNING", "BLOCKED")
