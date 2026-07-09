"""
tests/test_risk_dashboard_gui_v174.py
Tests for GUI panel risk dashboard tabs v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V174_RISK_DASHBOARD,
    get_risk_dashboard_tab_names,
    render_risk_dashboard_overview_tab,
)


class TestPanelVersion:
    def test_panel_version_174(self):
        assert PANEL_VERSION == "1.7.4"

    def test_panel_title_has_174(self):
        assert "1.7.4" in PANEL_TITLE

    def test_panel_title_has_risk_dashboard(self):
        assert "Risk Dashboard" in PANEL_TITLE


class TestTabCount:
    def test_total_tabs_84(self):
        assert len(_TABS) == 84

    def test_risk_dashboard_tabs_15(self):
        assert len(_TABS_V174_RISK_DASHBOARD) == 15


class TestRiskDashboardTabs:
    def test_has_risk_dashboard_overview(self):
        assert "risk_dashboard_overview" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_single_trade(self):
        assert "risk_single_trade" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_portfolio_exposure(self):
        assert "risk_portfolio_exposure" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_cash_ratio(self):
        assert "risk_cash_ratio" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_drawdown(self):
        assert "risk_drawdown" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_losing_streak(self):
        assert "risk_losing_streak" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_concentration(self):
        assert "risk_concentration" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_scorecard(self):
        assert "risk_scorecard" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_stop_loss_coverage(self):
        assert "risk_stop_loss_coverage" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_abc_risk(self):
        assert "risk_abc_risk" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_watchlist_risk(self):
        assert "risk_watchlist_risk" in _TABS_V174_RISK_DASHBOARD

    def test_has_risk_market_regime_risk(self):
        assert "risk_market_regime_risk" in _TABS_V174_RISK_DASHBOARD


class TestGetRiskDashboardTabNames:
    def test_returns_list(self):
        assert isinstance(get_risk_dashboard_tab_names(), list)

    def test_length_15(self):
        assert len(get_risk_dashboard_tab_names()) == 15

    def test_matches_tabs_v174(self):
        assert get_risk_dashboard_tab_names() == _TABS_V174_RISK_DASHBOARD


class TestRiskDashboardOverviewRender:
    def test_render_returns_dict(self):
        assert isinstance(render_risk_dashboard_overview_tab(), dict)

    def test_render_has_version(self):
        result = render_risk_dashboard_overview_tab()
        assert "version" in result

    def test_render_paper_only(self):
        result = render_risk_dashboard_overview_tab()
        assert result.get("paper_only") is True

    def test_render_no_real_orders(self):
        result = render_risk_dashboard_overview_tab()
        assert result.get("no_real_orders") is True

    def test_render_version_174(self):
        result = render_risk_dashboard_overview_tab()
        assert result["version"] == "1.7.4"
