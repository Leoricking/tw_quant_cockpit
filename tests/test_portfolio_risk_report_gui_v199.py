"""
tests/test_portfolio_risk_report_gui_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — GUI Panel Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    PANEL_TITLE,
    render_portfolio_risk_report_tab,
    render_position_sizing_policy_tab,
    render_risk_budget_dashboard_tab,
    get_risk_report_tab_names,
    get_panel_info,
)


def test_panel_version_is_1_9_9():
    assert PANEL_VERSION in ("1.9.9", "1.9.10")


def test_panel_title_contains_1_9_9():
    assert "1.9.9" in PANEL_TITLE or "1.9.10" in PANEL_TITLE


def test_panel_title_contains_expected_keyword():
    assert any(kw in PANEL_TITLE for kw in ("Risk Report", "Position Sizing", "Portfolio", "Governance", "Consolidation"))


def test_panel_title_is_string():
    assert isinstance(PANEL_TITLE, str)


def test_get_risk_report_tab_names_returns_list():
    assert isinstance(get_risk_report_tab_names(), list)


def test_get_risk_report_tab_names_count_is_3():
    assert len(get_risk_report_tab_names()) == 3


def test_portfolio_risk_report_in_tab_names():
    assert "portfolio_risk_report" in get_risk_report_tab_names()


def test_position_sizing_policy_in_tab_names():
    assert "position_sizing_policy" in get_risk_report_tab_names()


def test_risk_budget_dashboard_in_tab_names():
    assert "risk_budget_dashboard" in get_risk_report_tab_names()


def test_render_portfolio_risk_report_tab_returns_dict():
    assert isinstance(render_portfolio_risk_report_tab(), dict)


def test_render_portfolio_risk_report_tab_tab_is_correct():
    assert render_portfolio_risk_report_tab()["tab"] == "portfolio_risk_report"


def test_render_portfolio_risk_report_tab_paper_only_True():
    assert render_portfolio_risk_report_tab()["paper_only"] is True


def test_render_portfolio_risk_report_tab_no_real_orders_True():
    assert render_portfolio_risk_report_tab()["no_real_orders"] is True


def test_render_portfolio_risk_report_tab_schema_version_is_199():
    assert render_portfolio_risk_report_tab()["schema_version"] == "199"


def test_render_portfolio_risk_report_tab_dashboard_mutates_strategy_False():
    assert render_portfolio_risk_report_tab()["dashboard_mutates_strategy"] is False


def test_render_portfolio_risk_report_tab_report_triggers_rebalance_False():
    assert render_portfolio_risk_report_tab()["report_triggers_rebalance"] is False


def test_render_portfolio_risk_report_tab_has_empty_state():
    assert "empty_state" in render_portfolio_risk_report_tab()


def test_render_position_sizing_policy_tab_returns_dict():
    assert isinstance(render_position_sizing_policy_tab(), dict)


def test_render_position_sizing_policy_tab_tab_is_correct():
    assert render_position_sizing_policy_tab()["tab"] == "position_sizing_policy"


def test_render_position_sizing_policy_tab_paper_only_True():
    assert render_position_sizing_policy_tab()["paper_only"] is True


def test_render_position_sizing_policy_tab_sizing_executes_order_False():
    assert render_position_sizing_policy_tab()["sizing_executes_order"] is False


def test_render_position_sizing_policy_tab_sizing_mutates_strategy_False():
    assert render_position_sizing_policy_tab()["sizing_mutates_strategy"] is False


def test_render_position_sizing_policy_tab_schema_version_is_199():
    assert render_position_sizing_policy_tab()["schema_version"] == "199"


def test_render_risk_budget_dashboard_tab_returns_dict():
    assert isinstance(render_risk_budget_dashboard_tab(), dict)


def test_render_risk_budget_dashboard_tab_tab_is_correct():
    assert render_risk_budget_dashboard_tab()["tab"] == "risk_budget_dashboard"


def test_render_risk_budget_dashboard_tab_paper_only_True():
    assert render_risk_budget_dashboard_tab()["paper_only"] is True


def test_render_risk_budget_dashboard_tab_dashboard_mutates_strategy_False():
    assert render_risk_budget_dashboard_tab()["dashboard_mutates_strategy"] is False


def test_render_risk_budget_dashboard_tab_dashboard_places_real_order_False():
    assert render_risk_budget_dashboard_tab()["dashboard_places_real_order"] is False


def test_render_risk_budget_dashboard_tab_schema_version_is_199():
    assert render_risk_budget_dashboard_tab()["schema_version"] == "199"


def test_all_3_tab_renders_paper_only_True():
    tabs = [
        render_portfolio_risk_report_tab(),
        render_position_sizing_policy_tab(),
        render_risk_budget_dashboard_tab(),
    ]
    assert all(t["paper_only"] is True for t in tabs)


def test_portfolio_risk_report_tab_idempotent():
    r1 = render_portfolio_risk_report_tab()
    r2 = render_portfolio_risk_report_tab()
    assert r1["tab"] == r2["tab"]
    assert r1["paper_only"] == r2["paper_only"]


def test_position_sizing_policy_tab_idempotent():
    r1 = render_position_sizing_policy_tab()
    r2 = render_position_sizing_policy_tab()
    assert r1["tab"] == r2["tab"]
    assert r1["paper_only"] == r2["paper_only"]


def test_risk_budget_dashboard_tab_idempotent():
    r1 = render_risk_budget_dashboard_tab()
    r2 = render_risk_budget_dashboard_tab()
    assert r1["tab"] == r2["tab"]
    assert r1["paper_only"] == r2["paper_only"]


def test_get_panel_info_panel_version_is_1_9_9():
    assert get_panel_info()["panel_version"] in ("1.9.9", "1.9.10")


def test_get_panel_info_has_portfolio_risk_report_tab():
    pi = get_panel_info()
    tabs = pi.get("risk_report_tab_names", pi.get("tabs", []))
    assert "portfolio_risk_report" in tabs


def test_get_panel_info_has_position_sizing_policy_tab():
    pi = get_panel_info()
    tabs = pi.get("risk_report_tab_names", pi.get("tabs", []))
    assert "position_sizing_policy" in tabs


def test_get_panel_info_has_risk_budget_dashboard_tab():
    pi = get_panel_info()
    tabs = pi.get("risk_report_tab_names", pi.get("tabs", []))
    assert "risk_budget_dashboard" in tabs


def test_get_panel_info_returns_dict():
    assert isinstance(get_panel_info(), dict)
