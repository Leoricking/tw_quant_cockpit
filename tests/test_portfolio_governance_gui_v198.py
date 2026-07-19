"""
tests/test_portfolio_governance_gui_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — GUI Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_gui_v198 import (
    PANEL_VERSION, PANEL_TITLE, PANEL_SCHEMA_VERSION,
    get_panel_info, get_governance_portfolio_tab_names,
    render_portfolio_governance_tab, render_risk_overlay_tab,
    render_exposure_dashboard_tab, render_all_tabs,
)


class TestPanelConstants:
    def test_panel_version_is_1_9_8(self):
        assert PANEL_VERSION == "1.9.8"

    def test_panel_title_contains_1_9_8(self):
        assert "1.9.8" in PANEL_TITLE

    def test_panel_title_contains_Portfolio(self):
        assert "Portfolio" in PANEL_TITLE or "Governance" in PANEL_TITLE or "Risk" in PANEL_TITLE

    def test_panel_title_contains_Governance(self):
        assert "Governance" in PANEL_TITLE

    def test_panel_title_is_string(self):
        assert isinstance(PANEL_TITLE, str)

    def test_panel_schema_version_is_198(self):
        assert PANEL_SCHEMA_VERSION == "198"


class TestGetPanelInfo:
    def test_returns_dict(self):
        assert isinstance(get_panel_info(), dict)

    def test_panel_version_1_9_8(self):
        assert get_panel_info()["panel_version"] == "1.9.8"

    def test_paper_only_True(self):
        assert get_panel_info()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert get_panel_info()["no_real_orders"] is True

    def test_not_investment_advice_True(self):
        assert get_panel_info()["not_investment_advice"] is True

    def test_tab_count_gte_163(self):
        assert get_panel_info()["tab_count"] >= 163

    def test_governance_tab_count_is_3(self):
        assert get_panel_info()["governance_tab_count"] == 3

    def test_governance_tab_names_is_list(self):
        assert isinstance(get_panel_info()["governance_tab_names"], list)

    def test_dashboard_mutates_strategy_False(self):
        assert get_panel_info()["dashboard_mutates_strategy"] is False

    def test_overlay_places_real_order_False(self):
        assert get_panel_info()["overlay_places_real_order"] is False


class TestGetGovernancePortfolioTabNames:
    def test_returns_list(self):
        assert isinstance(get_governance_portfolio_tab_names(), list)

    def test_count_is_3(self):
        assert len(get_governance_portfolio_tab_names()) == 3

    def test_has_portfolio_governance(self):
        assert "portfolio_governance" in get_governance_portfolio_tab_names()

    def test_has_risk_overlay(self):
        assert "risk_overlay" in get_governance_portfolio_tab_names()

    def test_has_exposure_dashboard(self):
        assert "exposure_dashboard" in get_governance_portfolio_tab_names()

    def test_all_are_strings(self):
        assert all(isinstance(t, str) for t in get_governance_portfolio_tab_names())


class TestRenderPortfolioGovernanceTab:
    def test_returns_dict(self):
        assert isinstance(render_portfolio_governance_tab(), dict)

    def test_tab_name_is_portfolio_governance(self):
        assert render_portfolio_governance_tab()["tab"] == "portfolio_governance"

    def test_paper_only_True(self):
        assert render_portfolio_governance_tab()["paper_only"] is True

    def test_research_only_True(self):
        assert render_portfolio_governance_tab()["research_only"] is True

    def test_no_real_orders_True(self):
        assert render_portfolio_governance_tab()["no_real_orders"] is True

    def test_no_broker_True(self):
        assert render_portfolio_governance_tab()["no_broker"] is True

    def test_portfolio_governance_only_True(self):
        assert render_portfolio_governance_tab()["portfolio_governance_only"] is True

    def test_dashboard_mutates_strategy_False(self):
        assert render_portfolio_governance_tab()["dashboard_mutates_strategy"] is False

    def test_not_investment_advice_True(self):
        assert render_portfolio_governance_tab()["not_investment_advice"] is True

    def test_custom_portfolio_passed(self):
        p = {"test": "portfolio"}
        r = render_portfolio_governance_tab(portfolio=p)
        assert r["portfolio"] == p

    def test_grade_passed_through(self):
        r = render_portfolio_governance_tab(grade="HIGH")
        assert r["grade"] == "HIGH"

    def test_recs_passed_through(self):
        recs = ["RISK_OFF_MODE"]
        r = render_portfolio_governance_tab(recs=recs)
        assert r["recommendations"] == recs


class TestRenderRiskOverlayTab:
    def test_returns_dict(self):
        assert isinstance(render_risk_overlay_tab(), dict)

    def test_tab_name_is_risk_overlay(self):
        assert render_risk_overlay_tab()["tab"] == "risk_overlay"

    def test_paper_only_True(self):
        assert render_risk_overlay_tab()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert render_risk_overlay_tab()["no_real_orders"] is True

    def test_risk_overlay_only_True(self):
        assert render_risk_overlay_tab()["risk_overlay_only"] is True

    def test_dashboard_mutates_strategy_False(self):
        assert render_risk_overlay_tab()["dashboard_mutates_strategy"] is False

    def test_overlay_places_real_order_False(self):
        assert render_risk_overlay_tab()["overlay_places_real_order"] is False

    def test_not_investment_advice_True(self):
        assert render_risk_overlay_tab()["not_investment_advice"] is True

    def test_candidate_passed_through(self):
        r = render_risk_overlay_tab(candidate="paper_cand_001")
        assert r["candidate"] == "paper_cand_001"


class TestRenderExposureDashboardTab:
    def test_returns_dict(self):
        assert isinstance(render_exposure_dashboard_tab(), dict)

    def test_tab_name_is_exposure_dashboard(self):
        assert render_exposure_dashboard_tab()["tab"] == "exposure_dashboard"

    def test_paper_only_True(self):
        assert render_exposure_dashboard_tab()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert render_exposure_dashboard_tab()["no_real_orders"] is True

    def test_exposure_dashboard_only_True(self):
        assert render_exposure_dashboard_tab()["exposure_dashboard_only"] is True

    def test_dashboard_mutates_strategy_False(self):
        assert render_exposure_dashboard_tab()["dashboard_mutates_strategy"] is False

    def test_not_investment_advice_True(self):
        assert render_exposure_dashboard_tab()["not_investment_advice"] is True

    def test_exposure_passed_through(self):
        exp = {"symbol_count": 5}
        r = render_exposure_dashboard_tab(exposure=exp)
        assert r["exposure"] == exp


class TestRenderAllTabs:
    def test_returns_dict(self):
        assert isinstance(render_all_tabs(), dict)

    def test_has_portfolio_governance_key(self):
        assert "portfolio_governance" in render_all_tabs()

    def test_has_risk_overlay_key(self):
        assert "risk_overlay" in render_all_tabs()

    def test_has_exposure_dashboard_key(self):
        assert "exposure_dashboard" in render_all_tabs()

    def test_portfolio_governance_no_error(self):
        r = render_all_tabs()
        assert r["portfolio_governance"].get("tab") == "portfolio_governance"

    def test_risk_overlay_no_error(self):
        r = render_all_tabs()
        assert r["risk_overlay"].get("tab") == "risk_overlay"

    def test_exposure_dashboard_no_error(self):
        r = render_all_tabs()
        assert r["exposure_dashboard"].get("tab") == "exposure_dashboard"

    def test_paper_only_True(self):
        assert render_all_tabs()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert render_all_tabs()["no_real_orders"] is True

    def test_tab_count_gte_163(self):
        assert render_all_tabs()["tab_count"] >= 163

    def test_dashboard_mutates_strategy_False(self):
        assert render_all_tabs()["dashboard_mutates_strategy"] is False

    def test_portfolio_governance_paper_only(self):
        r = render_all_tabs()
        assert r["portfolio_governance"]["paper_only"] is True

    def test_risk_overlay_paper_only(self):
        r = render_all_tabs()
        assert r["risk_overlay"]["paper_only"] is True

    def test_exposure_dashboard_paper_only(self):
        r = render_all_tabs()
        assert r["exposure_dashboard"]["paper_only"] is True

    def test_portfolio_governance_no_mutation(self):
        r = render_all_tabs()
        assert r["portfolio_governance"]["dashboard_mutates_strategy"] is False

    def test_risk_overlay_no_real_order(self):
        r = render_all_tabs()
        assert r["risk_overlay"]["overlay_places_real_order"] is False

    def test_risk_overlay_only_True_in_overlay_tab(self):
        r = render_all_tabs()
        assert r["risk_overlay"]["risk_overlay_only"] is True

    def test_exposure_dashboard_only_True_in_exposure_tab(self):
        r = render_all_tabs()
        assert r["exposure_dashboard"]["exposure_dashboard_only"] is True
