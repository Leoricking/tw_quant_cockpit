"""
tests/test_paper_cockpit_gui_v201.py
v2.0.1 Paper Cockpit — GUI Tests (25+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_VERSION_V201, PANEL_TITLE, get_tab_names, get_cockpit_tab_names,
    get_v201_tab_names,
    render_daily_workflow_v201_tab, render_no_entry_reason_detail_tab,
    render_decision_ticket_v201_tab, get_panel_info,
)


# --- PANEL_VERSION tests ---

def test_panel_version_v201_is_201():
    assert PANEL_VERSION_V201 == "2.0.1"

def test_panel_version_v200_unchanged():
    assert PANEL_VERSION == "2.0.0"

def test_panel_title_contains_200():
    assert "2.0.0" in PANEL_TITLE


# --- Tab presence tests ---

def test_daily_workflow_v201_tab_in_tab_names():
    tabs = get_tab_names()
    assert "daily_workflow_v201" in tabs

def test_no_entry_reason_detail_tab_in_tab_names():
    tabs = get_tab_names()
    assert "no_entry_reason_detail" in tabs

def test_decision_ticket_v201_tab_in_tab_names():
    tabs = get_tab_names()
    assert "decision_ticket_v201" in tabs

def test_v200_tabs_still_present():
    tabs = get_tab_names()
    assert "paper_cockpit" in tabs
    assert "strategy_decision_console" in tabs
    assert "decision_ticket" in tabs


# --- get_v201_tab_names tests ---

def test_get_v201_tab_names_returns_list():
    names = get_v201_tab_names()
    assert isinstance(names, list)

def test_get_v201_tab_names_count():
    names = get_v201_tab_names()
    assert len(names) == 3

def test_get_v201_tab_names_contains_daily_workflow():
    names = get_v201_tab_names()
    assert "daily_workflow_v201" in names

def test_get_v201_tab_names_contains_no_entry_reason():
    names = get_v201_tab_names()
    assert "no_entry_reason_detail" in names

def test_get_v201_tab_names_contains_decision_ticket():
    names = get_v201_tab_names()
    assert "decision_ticket_v201" in names


# --- get_cockpit_tab_names tests ---

def test_get_cockpit_tab_names_count():
    names = get_cockpit_tab_names()
    assert len(names) == 3

def test_get_cockpit_tab_names_v200_tabs():
    names = get_cockpit_tab_names()
    assert "paper_cockpit" in names
    assert "strategy_decision_console" in names
    assert "decision_ticket" in names


# --- render_daily_workflow_v201_tab tests ---

def test_render_daily_workflow_v201_tab_returns_dict():
    result = render_daily_workflow_v201_tab()
    assert isinstance(result, dict)

def test_render_daily_workflow_v201_tab_name():
    result = render_daily_workflow_v201_tab()
    assert result["tab"] == "daily_workflow_v201"

def test_render_daily_workflow_v201_tab_paper_only():
    result = render_daily_workflow_v201_tab()
    assert result["paper_only"] is True

def test_render_daily_workflow_v201_tab_no_real_orders():
    result = render_daily_workflow_v201_tab()
    assert result["no_real_orders"] is True

def test_render_daily_workflow_v201_tab_human_review():
    result = render_daily_workflow_v201_tab()
    assert result["human_review_required"] is True

def test_render_daily_workflow_v201_tab_production_blocked():
    result = render_daily_workflow_v201_tab()
    assert result["production_trading_blocked"] is True

def test_render_daily_workflow_v201_tab_schema_version():
    result = render_daily_workflow_v201_tab()
    assert result["schema_version"] == "201"

def test_render_daily_workflow_v201_tab_final_actions():
    result = render_daily_workflow_v201_tab()
    assert "final_actions" in result
    assert "PAPER_BUY_PLAN" in result["final_actions"]


# --- render_no_entry_reason_detail_tab tests ---

def test_render_no_entry_reason_detail_tab_returns_dict():
    result = render_no_entry_reason_detail_tab()
    assert isinstance(result, dict)

def test_render_no_entry_reason_detail_tab_name():
    result = render_no_entry_reason_detail_tab()
    assert result["tab"] == "no_entry_reason_detail"

def test_render_no_entry_reason_detail_tab_paper_only():
    result = render_no_entry_reason_detail_tab()
    assert result["paper_only"] is True

def test_render_no_entry_reason_detail_tab_no_entry_reasons():
    result = render_no_entry_reason_detail_tab()
    assert "no_entry_reasons" in result
    assert len(result["no_entry_reasons"]) == 13

def test_render_no_entry_reason_detail_tab_schema_version():
    result = render_no_entry_reason_detail_tab()
    assert result["schema_version"] == "201"


# --- render_decision_ticket_v201_tab tests ---

def test_render_decision_ticket_v201_tab_returns_dict():
    result = render_decision_ticket_v201_tab()
    assert isinstance(result, dict)

def test_render_decision_ticket_v201_tab_name():
    result = render_decision_ticket_v201_tab()
    assert result["tab"] == "decision_ticket_v201"

def test_render_decision_ticket_v201_tab_paper_only():
    result = render_decision_ticket_v201_tab()
    assert result["paper_only"] is True

def test_render_decision_ticket_v201_tab_ticket_triggers_broker_false():
    result = render_decision_ticket_v201_tab()
    assert result["ticket_triggers_broker"] is False

def test_render_decision_ticket_v201_tab_ticket_fields():
    result = render_decision_ticket_v201_tab()
    assert "ticket_fields" in result
    assert len(result["ticket_fields"]) == 22

def test_render_decision_ticket_v201_tab_schema_version():
    result = render_decision_ticket_v201_tab()
    assert result["schema_version"] == "201"


# --- get_panel_info tests ---

def test_get_panel_info_version():
    info = get_panel_info()
    assert info["panel_version"] in ("2.0.0", "2.0.1")

def test_get_panel_info_paper_only():
    info = get_panel_info()
    assert info["paper_only"] is True
