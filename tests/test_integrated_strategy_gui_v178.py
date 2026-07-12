"""tests/test_integrated_strategy_gui_v178.py — v1.7.8 integrated strategy GUI panel tests."""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    PANEL_TITLE,
    get_panel_info,
    get_tab_names,
    get_integrated_strategy_tab_names,
    render_integrated_strategy_tab,
    render_integrated_decision_dashboard_tab,
    render_integrated_paper_plan_tab,
)


class TestPanelVersionAndTitle:
    def test_panel_version_is_178(self):
        assert PANEL_VERSION == "1.8.4"

    def test_panel_title_contains_178(self):
        assert "1.8.4" in PANEL_TITLE


class TestGetTabNames:
    def test_integrated_strategy_in_tab_names(self):
        assert "integrated_strategy" in get_tab_names()

    def test_integrated_decision_dashboard_in_tab_names(self):
        assert "integrated_decision_dashboard" in get_tab_names()

    def test_integrated_paper_plan_in_tab_names(self):
        assert "integrated_paper_plan" in get_tab_names()

    def test_tab_names_ge_117(self):
        tabs = get_tab_names()
        assert len(tabs) >= 117, f"Only {len(tabs)} tabs found, expected >= 117"


class TestGetIntegratedStrategyTabNames:
    def test_returns_list(self):
        result = get_integrated_strategy_tab_names()
        assert isinstance(result, list)

    def test_length_equals_3(self):
        result = get_integrated_strategy_tab_names()
        assert len(result) == 3

    def test_integrated_strategy_in_list(self):
        result = get_integrated_strategy_tab_names()
        assert "integrated_strategy" in result

    def test_integrated_decision_dashboard_in_list(self):
        result = get_integrated_strategy_tab_names()
        assert "integrated_decision_dashboard" in result

    def test_integrated_paper_plan_in_list(self):
        result = get_integrated_strategy_tab_names()
        assert "integrated_paper_plan" in result


class TestGetPanelInfo:
    def test_panel_version_179(self):
        result = get_panel_info()
        assert result["panel_version"] == "1.8.4"

    def test_paper_only_true(self):
        result = get_panel_info()
        assert result["paper_only"] is True

    def test_research_only_true(self):
        result = get_panel_info()
        assert result["research_only"] is True

    def test_no_real_orders_true(self):
        result = get_panel_info()
        assert result["no_real_orders"] is True

    def test_headless_safe_true(self):
        result = get_panel_info()
        assert result["headless_safe"] is True


class TestRenderIntegratedStrategyTab:
    def test_returns_dict_empty_call(self):
        result = render_integrated_strategy_tab()
        assert isinstance(result, dict)

    def test_paper_only_true(self):
        result = render_integrated_strategy_tab()
        assert result["paper_only"] is True

    def test_research_only_true(self):
        result = render_integrated_strategy_tab()
        assert result["research_only"] is True

    def test_no_real_orders_true(self):
        result = render_integrated_strategy_tab()
        assert result["no_real_orders"] is True

    def test_not_investment_advice_true(self):
        result = render_integrated_strategy_tab()
        assert result["not_investment_advice"] is True

    def test_with_symbol_and_date_tab_key(self):
        result = render_integrated_strategy_tab("2330", "2026-07-10")
        assert result["tab"] == "integrated_strategy"


class TestRenderIntegratedDecisionDashboardTab:
    def test_returns_dict_empty_call(self):
        result = render_integrated_decision_dashboard_tab()
        assert isinstance(result, dict)

    def test_paper_only_true(self):
        result = render_integrated_decision_dashboard_tab()
        assert result["paper_only"] is True

    def test_no_real_orders_true(self):
        result = render_integrated_decision_dashboard_tab()
        assert result["no_real_orders"] is True

    def test_with_symbol_and_date_tab_key(self):
        result = render_integrated_decision_dashboard_tab("2330", "2026-07-10")
        assert result["tab"] == "integrated_decision_dashboard"


class TestRenderIntegratedPaperPlanTab:
    def test_returns_dict_empty_call(self):
        result = render_integrated_paper_plan_tab()
        assert isinstance(result, dict)

    def test_paper_only_true(self):
        result = render_integrated_paper_plan_tab()
        assert result["paper_only"] is True

    def test_no_real_orders_true(self):
        result = render_integrated_paper_plan_tab()
        assert result["no_real_orders"] is True

    def test_broker_execution_enabled_false(self):
        result = render_integrated_paper_plan_tab()
        assert result["broker_execution_enabled"] is False
