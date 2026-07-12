"""
tests/test_trade_journal_gui_v175.py
Tests for GUI panel trade journal tabs v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V175_TRADE_JOURNAL,
    get_trade_journal_tab_names,
    render_trade_journal_overview_tab,
    render_trade_journal_entry_tab,
    render_trade_journal_scorecard_tab,
    render_trade_journal_scenarios_tab,
    render_trade_journal_health_tab,
)


class TestPanelVersion:
    def test_panel_version_175(self):
        assert PANEL_VERSION == "1.8.4"

    def test_panel_title_has_175(self):
        assert "1.8.4" in PANEL_TITLE

    def test_panel_title_has_trade_journal(self):
        assert "Small Capital" in PANEL_TITLE


class TestTabCount:
    def test_trade_journal_tabs_14(self):
        assert len(_TABS_V175_TRADE_JOURNAL) == 14

    def test_total_tabs_98(self):
        assert len(_TABS) == 135


class TestTradeJournalTabs:
    def test_has_trade_journal_overview(self):
        assert "trade_journal_overview" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_entry(self):
        assert "trade_journal_entry" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_review_entry(self):
        assert "trade_journal_review_entry" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_review_exit(self):
        assert "trade_journal_review_exit" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_abc_review(self):
        assert "trade_journal_abc_review" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_watchlist_review(self):
        assert "trade_journal_watchlist_review" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_risk_review(self):
        assert "trade_journal_risk_review" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_regime_review(self):
        assert "trade_journal_regime_review" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_mistake_taxonomy(self):
        assert "trade_journal_mistake_taxonomy" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_scorecard(self):
        assert "trade_journal_scorecard" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_report(self):
        assert "trade_journal_report" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_scenarios(self):
        assert "trade_journal_scenarios" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_health(self):
        assert "trade_journal_health" in _TABS_V175_TRADE_JOURNAL

    def test_has_trade_journal_gate(self):
        assert "trade_journal_gate" in _TABS_V175_TRADE_JOURNAL


class TestGetTradeJournalTabNames:
    def test_returns_list(self):
        assert isinstance(get_trade_journal_tab_names(), list)

    def test_count_14(self):
        assert len(get_trade_journal_tab_names()) == 14

    def test_matches_tabs_v175(self):
        assert get_trade_journal_tab_names() == _TABS_V175_TRADE_JOURNAL


class TestRenderOverviewTab:
    def test_returns_dict(self):
        assert isinstance(render_trade_journal_overview_tab(), dict)

    def test_version_175(self):
        r = render_trade_journal_overview_tab()
        assert r["version"] == "1.7.5"

    def test_paper_only_true(self):
        r = render_trade_journal_overview_tab()
        assert r["paper_only"] is True

    def test_not_investment_advice_true(self):
        r = render_trade_journal_overview_tab()
        assert r["not_investment_advice"] is True


class TestRenderEntryTab:
    def test_returns_dict(self):
        assert isinstance(render_trade_journal_entry_tab(), dict)

    def test_paper_only_true(self):
        assert render_trade_journal_entry_tab()["paper_only"] is True


class TestRenderScorecardTab:
    def test_returns_dict(self):
        assert isinstance(render_trade_journal_scorecard_tab(), dict)

    def test_paper_only_true(self):
        assert render_trade_journal_scorecard_tab()["paper_only"] is True

    def test_has_grade(self):
        r = render_trade_journal_scorecard_tab()
        assert "grade" in r


class TestRenderScenariosTab:
    def test_returns_dict(self):
        assert isinstance(render_trade_journal_scenarios_tab(), dict)

    def test_scenario_count_ge_55(self):
        r = render_trade_journal_scenarios_tab()
        assert r["scenario_count"] >= 55


class TestRenderHealthTab:
    def test_returns_dict(self):
        assert isinstance(render_trade_journal_health_tab(), dict)

    def test_status_pass(self):
        r = render_trade_journal_health_tab()
        assert r["status"] == "PASS"

    def test_all_passed_true(self):
        r = render_trade_journal_health_tab()
        assert r["all_passed"] is True
