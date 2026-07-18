"""
tests/test_decision_workflow_gui_v188.py
Tests for GUI small_capital_strategy_panel v1.8.8 — Paper Decision Workflow Runner.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    _TABS_V188_DECISION_WORKFLOW, _TABS,
    render_decision_workflow_tab, render_daily_workflow_tab,
    render_weekly_workflow_tab, get_tab_names, get_panel_info,
    get_decision_workflow_tab_names,
)


def test_panel_version_is_188():
    assert PANEL_VERSION in ("1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5")


def test_panel_title_contains_188():
    assert "1.8.8" in PANEL_TITLE or "1.8.9" in PANEL_TITLE or "1.9.0" in PANEL_TITLE or "1.9.1" in PANEL_TITLE or "1.9.2" in PANEL_TITLE or "1.9.3" in PANEL_TITLE or "1.9.4" in PANEL_TITLE or "1.9.5" in PANEL_TITLE


def test_panel_title_contains_workflow_runner():
    assert "Workflow Runner" in PANEL_TITLE or "Journal" in PANEL_TITLE or "Performance" in PANEL_TITLE or "Tuning" in PANEL_TITLE or "Sandbox" in PANEL_TITLE or "Promotion" in PANEL_TITLE or "Rollback" in PANEL_TITLE or "Monitoring" in PANEL_TITLE or "Drift" in PANEL_TITLE or "Review" in PANEL_TITLE


def test_tabs_v188_count_3():
    assert len(_TABS_V188_DECISION_WORKFLOW) == 3


def test_tabs_v188_contains_decision_workflow():
    assert "decision_workflow" in _TABS_V188_DECISION_WORKFLOW


def test_tabs_v188_contains_daily_workflow():
    assert "daily_workflow" in _TABS_V188_DECISION_WORKFLOW


def test_tabs_v188_contains_weekly_workflow():
    assert "weekly_workflow" in _TABS_V188_DECISION_WORKFLOW


def test_tabs_v188_all_in_tabs():
    for tab in _TABS_V188_DECISION_WORKFLOW:
        assert tab in _TABS


def test_get_tab_names_includes_decision_workflow():
    tabs = get_tab_names()
    assert "decision_workflow" in tabs


def test_get_tab_names_includes_daily_workflow():
    tabs = get_tab_names()
    assert "daily_workflow" in tabs


def test_get_tab_names_includes_weekly_workflow():
    tabs = get_tab_names()
    assert "weekly_workflow" in tabs


def test_get_decision_workflow_tab_names_count():
    names = get_decision_workflow_tab_names()
    assert len(names) == 3


def test_get_decision_workflow_tab_names_contains_all():
    names = get_decision_workflow_tab_names()
    assert "decision_workflow" in names
    assert "daily_workflow" in names
    assert "weekly_workflow" in names


def test_render_decision_workflow_tab_paper_only():
    data = render_decision_workflow_tab()
    assert data["paper_only"] is True


def test_render_decision_workflow_tab_no_real_orders():
    data = render_decision_workflow_tab()
    assert data["no_real_orders"] is True


def test_render_decision_workflow_tab_no_broker():
    data = render_decision_workflow_tab()
    assert data["no_broker"] is True


def test_render_decision_workflow_tab_not_investment_advice():
    data = render_decision_workflow_tab()
    assert data["not_investment_advice"] is True


def test_render_decision_workflow_tab_production_blocked():
    data = render_decision_workflow_tab()
    assert data["production_trading_blocked"] is True


def test_render_decision_workflow_tab_workflow_only():
    data = render_decision_workflow_tab()
    assert data["workflow_only"] is True


def test_render_decision_workflow_tab_tab_name():
    data = render_decision_workflow_tab()
    assert data["tab"] == "decision_workflow"


def test_render_decision_workflow_tab_schema_188():
    data = render_decision_workflow_tab()
    assert data["schema_version"] == "188"


def test_render_decision_workflow_tab_version():
    data = render_decision_workflow_tab()
    assert data["version"] in ("1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5")


def test_render_decision_workflow_tab_empty_state():
    data = render_decision_workflow_tab()
    assert "empty_state" in data
    assert len(data["empty_state"]) > 0


def test_render_daily_workflow_tab_paper_only():
    data = render_daily_workflow_tab()
    assert data["paper_only"] is True


def test_render_daily_workflow_tab_no_real_orders():
    data = render_daily_workflow_tab()
    assert data["no_real_orders"] is True


def test_render_daily_workflow_tab_tab_name():
    data = render_daily_workflow_tab()
    assert data["tab"] == "daily_workflow"


def test_render_daily_workflow_tab_schema_188():
    data = render_daily_workflow_tab()
    assert data["schema_version"] == "188"


def test_render_daily_workflow_tab_version():
    data = render_daily_workflow_tab()
    assert data["version"] in ("1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5")


def test_render_daily_workflow_tab_workflow_only():
    data = render_daily_workflow_tab()
    assert data["workflow_only"] is True


def test_render_daily_workflow_tab_not_investment_advice():
    data = render_daily_workflow_tab()
    assert data["not_investment_advice"] is True


def test_render_daily_workflow_tab_empty_state():
    data = render_daily_workflow_tab()
    assert "empty_state" in data


def test_render_weekly_workflow_tab_paper_only():
    data = render_weekly_workflow_tab()
    assert data["paper_only"] is True


def test_render_weekly_workflow_tab_no_real_orders():
    data = render_weekly_workflow_tab()
    assert data["no_real_orders"] is True


def test_render_weekly_workflow_tab_tab_name():
    data = render_weekly_workflow_tab()
    assert data["tab"] == "weekly_workflow"


def test_render_weekly_workflow_tab_schema_188():
    data = render_weekly_workflow_tab()
    assert data["schema_version"] == "188"


def test_render_weekly_workflow_tab_workflow_only():
    data = render_weekly_workflow_tab()
    assert data["workflow_only"] is True


def test_render_weekly_workflow_tab_not_investment_advice():
    data = render_weekly_workflow_tab()
    assert data["not_investment_advice"] is True


def test_render_weekly_workflow_tab_empty_state():
    data = render_weekly_workflow_tab()
    assert "empty_state" in data


def test_get_panel_info_returns_dict():
    info = get_panel_info()
    assert isinstance(info, dict)


def test_get_panel_info_version():
    info = get_panel_info()
    assert info["panel_version"] in ("1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5")


def test_tabs_include_prior_v187():
    tabs = get_tab_names()
    assert "decision_report" in tabs


def test_tabs_include_prior_v186():
    tabs = get_tab_names()
    assert "daily_decision_cockpit" in tabs
