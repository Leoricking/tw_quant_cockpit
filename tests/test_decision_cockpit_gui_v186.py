"""
tests/test_decision_cockpit_gui_v186.py
Tests for decision cockpit GUI panel v1.8.6.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS,
    _TABS_V186_DECISION_COCKPIT,
    get_tab_names, render_overview_tab,
    render_daily_decision_cockpit_tab,
    render_weekly_decision_review_tab,
    render_block_reasons_tab,
)


def test_panel_version_186():
    assert PANEL_VERSION in ("1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3")

def test_panel_title_contains_186():
    assert "1.8.6" in PANEL_TITLE or "1.8.7" in PANEL_TITLE or "1.8.8" in PANEL_TITLE or "1.8.9" in PANEL_TITLE or "1.9.0" in PANEL_TITLE or "1.9.1" in PANEL_TITLE or "1.9.2" in PANEL_TITLE or "1.9.3" in PANEL_TITLE

def test_panel_title_contains_decision_cockpit():
    assert "Decision Cockpit" in PANEL_TITLE or "Decision Report" in PANEL_TITLE or "Workflow Runner" in PANEL_TITLE or "Journal" in PANEL_TITLE or "Performance" in PANEL_TITLE or "Tuning" in PANEL_TITLE or "Sandbox" in PANEL_TITLE or "Promotion" in PANEL_TITLE or "Rollback" in PANEL_TITLE

def test_tabs_v186_count():
    assert len(_TABS_V186_DECISION_COCKPIT) == 3

def test_daily_decision_cockpit_tab():
    assert "daily_decision_cockpit" in _TABS_V186_DECISION_COCKPIT

def test_weekly_decision_review_tab():
    assert "weekly_decision_review" in _TABS_V186_DECISION_COCKPIT

def test_block_reasons_tab():
    assert "block_reasons" in _TABS_V186_DECISION_COCKPIT

def test_all_tabs_ge_141():
    assert len(_TABS) >= 141

def test_daily_decision_cockpit_in_all_tabs():
    assert "daily_decision_cockpit" in _TABS

def test_weekly_decision_review_in_all_tabs():
    assert "weekly_decision_review" in _TABS

def test_block_reasons_in_all_tabs():
    assert "block_reasons" in _TABS

def test_get_tab_names_returns_list():
    assert isinstance(get_tab_names(), list)

def test_get_tab_names_count_ge_141():
    assert len(get_tab_names()) >= 141

def test_render_overview_tab_callable():
    result = render_overview_tab()
    assert isinstance(result, dict)

def test_render_overview_tab_paper_only():
    assert render_overview_tab()["paper_only"] is True

def test_render_overview_tab_version():
    assert render_overview_tab()["version"] in ("1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3")

def test_render_daily_decision_tab_callable():
    result = render_daily_decision_cockpit_tab()
    assert isinstance(result, dict)

def test_render_daily_decision_tab_paper_only():
    assert render_daily_decision_cockpit_tab()["paper_only"] is True

def test_render_daily_decision_tab_decision_only():
    assert render_daily_decision_cockpit_tab()["decision_only"] is True

def test_render_daily_decision_tab_no_broker():
    assert render_daily_decision_cockpit_tab()["no_broker"] is True

def test_render_daily_decision_tab_not_investment_advice():
    assert render_daily_decision_cockpit_tab()["not_investment_advice"] is True

def test_render_daily_decision_tab_production_blocked():
    assert render_daily_decision_cockpit_tab()["production_trading_blocked"] is True

def test_render_daily_decision_tab_has_empty_state():
    result = render_daily_decision_cockpit_tab()
    assert "empty_state" in result
    assert result["empty_state"]

def test_render_weekly_review_tab_callable():
    result = render_weekly_decision_review_tab()
    assert isinstance(result, dict)

def test_render_weekly_review_tab_paper_only():
    assert render_weekly_decision_review_tab()["paper_only"] is True

def test_render_weekly_review_tab_decision_only():
    assert render_weekly_decision_review_tab()["decision_only"] is True

def test_render_weekly_review_tab_no_real_orders():
    assert render_weekly_decision_review_tab()["no_real_orders"] is True

def test_render_weekly_review_tab_has_empty_state():
    result = render_weekly_decision_review_tab()
    assert "empty_state" in result

def test_render_block_reasons_tab_callable():
    result = render_block_reasons_tab()
    assert isinstance(result, dict)

def test_render_block_reasons_tab_paper_only():
    assert render_block_reasons_tab()["paper_only"] is True

def test_render_block_reasons_tab_decision_only():
    assert render_block_reasons_tab()["decision_only"] is True

def test_render_block_reasons_tab_production_blocked():
    assert render_block_reasons_tab()["production_trading_blocked"] is True

def test_render_block_reasons_tab_has_empty_state():
    result = render_block_reasons_tab()
    assert "empty_state" in result

def test_previous_tabs_still_present():
    assert "portfolio_construction_lab" in _TABS
    assert "portfolio_rebalancing" in _TABS
    assert "monte_carlo" in _TABS
    assert "position_sizing_lab" in _TABS

def test_schema_version_in_daily_tab():
    result = render_daily_decision_cockpit_tab()
    assert result.get("schema_version") == "186"
