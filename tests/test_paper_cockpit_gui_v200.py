"""
tests/test_paper_cockpit_gui_v200.py
v2.0.0 Paper Cockpit — GUI Panel Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    render_paper_cockpit_tab,
    render_strategy_decision_console_tab,
    render_decision_ticket_tab,
    get_cockpit_tab_names,
    get_tab_names,
    get_panel_info,
)


def test_panel_version_is_200():
    assert PANEL_VERSION == "2.0.0"

def test_panel_title_contains_200():
    assert "2.0.0" in PANEL_TITLE

def test_panel_title_contains_cockpit_or_console():
    assert any(kw in PANEL_TITLE for kw in ("Cockpit", "Console", "Unified"))

def test_panel_title_is_string():
    assert isinstance(PANEL_TITLE, str)

def test_get_cockpit_tab_names_returns_list():
    assert isinstance(get_cockpit_tab_names(), list)

def test_get_cockpit_tab_names_count_3():
    assert len(get_cockpit_tab_names()) == 3

def test_paper_cockpit_in_cockpit_tab_names():
    assert "paper_cockpit" in get_cockpit_tab_names()

def test_strategy_decision_console_in_cockpit_tab_names():
    assert "strategy_decision_console" in get_cockpit_tab_names()

def test_decision_ticket_in_cockpit_tab_names():
    assert "decision_ticket" in get_cockpit_tab_names()

def test_paper_cockpit_in_all_tab_names():
    assert "paper_cockpit" in get_tab_names()

def test_strategy_decision_console_in_all_tab_names():
    assert "strategy_decision_console" in get_tab_names()

def test_decision_ticket_in_all_tab_names():
    assert "decision_ticket" in get_tab_names()

def test_render_paper_cockpit_tab_returns_dict():
    assert isinstance(render_paper_cockpit_tab(), dict)

def test_render_paper_cockpit_tab_tab_is_correct():
    assert render_paper_cockpit_tab()["tab"] == "paper_cockpit"

def test_render_paper_cockpit_tab_paper_only_true():
    assert render_paper_cockpit_tab()["paper_only"] is True

def test_render_paper_cockpit_tab_no_real_orders_true():
    assert render_paper_cockpit_tab()["no_real_orders"] is True

def test_render_paper_cockpit_tab_no_broker_true():
    assert render_paper_cockpit_tab()["no_broker"] is True

def test_render_paper_cockpit_tab_not_investment_advice_true():
    assert render_paper_cockpit_tab()["not_investment_advice"] is True

def test_render_paper_cockpit_tab_schema_version_200():
    assert render_paper_cockpit_tab()["schema_version"] == "200"

def test_render_paper_cockpit_tab_cockpit_executes_order_false():
    assert render_paper_cockpit_tab()["cockpit_executes_order"] is False

def test_render_paper_cockpit_tab_cockpit_mutates_strategy_false():
    assert render_paper_cockpit_tab()["cockpit_mutates_strategy"] is False

def test_render_paper_cockpit_tab_has_empty_state():
    assert "empty_state" in render_paper_cockpit_tab()

def test_render_paper_cockpit_tab_production_trading_blocked():
    assert render_paper_cockpit_tab()["production_trading_blocked"] is True

def test_render_paper_cockpit_tab_human_review_required():
    assert render_paper_cockpit_tab()["human_review_required"] is True

def test_render_strategy_decision_console_tab_returns_dict():
    assert isinstance(render_strategy_decision_console_tab(), dict)

def test_render_strategy_decision_console_tab_tab_correct():
    assert render_strategy_decision_console_tab()["tab"] == "strategy_decision_console"

def test_render_strategy_decision_console_tab_paper_only_true():
    assert render_strategy_decision_console_tab()["paper_only"] is True

def test_render_strategy_decision_console_tab_no_real_orders_true():
    assert render_strategy_decision_console_tab()["no_real_orders"] is True

def test_render_strategy_decision_console_tab_schema_version_200():
    assert render_strategy_decision_console_tab()["schema_version"] == "200"

def test_render_strategy_decision_console_tab_no_execution():
    assert render_strategy_decision_console_tab()["cockpit_executes_order"] is False

def test_render_strategy_decision_console_tab_no_mutation():
    assert render_strategy_decision_console_tab()["cockpit_mutates_strategy"] is False

def test_render_strategy_decision_console_tab_has_empty_state():
    assert "empty_state" in render_strategy_decision_console_tab()

def test_render_strategy_decision_console_tab_production_trading_blocked():
    assert render_strategy_decision_console_tab()["production_trading_blocked"] is True

def test_render_decision_ticket_tab_returns_dict():
    assert isinstance(render_decision_ticket_tab(), dict)

def test_render_decision_ticket_tab_tab_correct():
    assert render_decision_ticket_tab()["tab"] == "decision_ticket"

def test_render_decision_ticket_tab_paper_only_true():
    assert render_decision_ticket_tab()["paper_only"] is True

def test_render_decision_ticket_tab_no_real_orders_true():
    assert render_decision_ticket_tab()["no_real_orders"] is True

def test_render_decision_ticket_tab_no_broker_true():
    assert render_decision_ticket_tab()["no_broker"] is True

def test_render_decision_ticket_tab_schema_version_200():
    assert render_decision_ticket_tab()["schema_version"] == "200"

def test_render_decision_ticket_tab_ticket_triggers_broker_false():
    assert render_decision_ticket_tab()["ticket_triggers_broker"] is False

def test_render_decision_ticket_tab_ticket_executes_order_false():
    assert render_decision_ticket_tab()["ticket_executes_order"] is False

def test_render_decision_ticket_tab_ticket_mutates_strategy_false():
    assert render_decision_ticket_tab()["ticket_mutates_strategy"] is False

def test_render_decision_ticket_tab_human_review_required():
    assert render_decision_ticket_tab()["human_review_required"] is True

def test_render_decision_ticket_tab_has_empty_state():
    assert "empty_state" in render_decision_ticket_tab()

def test_render_decision_ticket_tab_production_trading_blocked():
    assert render_decision_ticket_tab()["production_trading_blocked"] is True

def test_all_3_cockpit_tabs_paper_only_true():
    tabs = [
        render_paper_cockpit_tab(),
        render_strategy_decision_console_tab(),
        render_decision_ticket_tab(),
    ]
    assert all(t["paper_only"] is True for t in tabs)

def test_all_3_cockpit_tabs_no_real_orders_true():
    tabs = [
        render_paper_cockpit_tab(),
        render_strategy_decision_console_tab(),
        render_decision_ticket_tab(),
    ]
    assert all(t["no_real_orders"] is True for t in tabs)

def test_all_3_cockpit_tabs_schema_version_200():
    tabs = [
        render_paper_cockpit_tab(),
        render_strategy_decision_console_tab(),
        render_decision_ticket_tab(),
    ]
    assert all(t["schema_version"] == "200" for t in tabs)

def test_paper_cockpit_tab_idempotent():
    r1 = render_paper_cockpit_tab()
    r2 = render_paper_cockpit_tab()
    assert r1["tab"] == r2["tab"]
    assert r1["paper_only"] == r2["paper_only"]

def test_strategy_decision_console_tab_idempotent():
    r1 = render_strategy_decision_console_tab()
    r2 = render_strategy_decision_console_tab()
    assert r1["tab"] == r2["tab"]
    assert r1["paper_only"] == r2["paper_only"]

def test_decision_ticket_tab_idempotent():
    r1 = render_decision_ticket_tab()
    r2 = render_decision_ticket_tab()
    assert r1["tab"] == r2["tab"]
    assert r1["paper_only"] == r2["paper_only"]

def test_get_panel_info_panel_version_200():
    assert get_panel_info()["panel_version"] == "2.0.0"

def test_get_panel_info_has_paper_cockpit_tab():
    pi = get_panel_info()
    tabs = pi.get("tabs", [])
    assert "paper_cockpit" in tabs

def test_get_panel_info_has_decision_ticket_tab():
    pi = get_panel_info()
    tabs = pi.get("tabs", [])
    assert "decision_ticket" in tabs

def test_get_panel_info_has_strategy_decision_console_tab():
    pi = get_panel_info()
    tabs = pi.get("tabs", [])
    assert "strategy_decision_console" in tabs

def test_get_panel_info_returns_dict():
    assert isinstance(get_panel_info(), dict)

def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True

def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True

def test_get_panel_info_headless_safe():
    assert get_panel_info()["headless_safe"] is True

def test_old_v1910_tabs_still_present():
    tabs = get_tab_names()
    assert "governance_stack_audit" in tabs
    assert "release_audit" in tabs
    assert "compatibility_summary" in tabs

def test_old_v199_tabs_still_present():
    tabs = get_tab_names()
    assert "portfolio_risk_report" in tabs
    assert "position_sizing_policy" in tabs
    assert "risk_budget_dashboard" in tabs

def test_old_overview_tab_still_present():
    assert "overview" in get_tab_names()

def test_old_safety_tab_still_present():
    assert "safety" in get_tab_names()
