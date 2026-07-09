"""tests/test_abc_gui_v172.py — ABC GUI tab tests for v1.7.2."""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V172_ABC,
    get_abc_tab_names, render_all_tabs,
    render_abc_execution_overview_tab,
    render_abc_a_10ma_pullback_tab,
    render_abc_b_platform_breakout_tab,
    render_abc_c_20ma_reclaim_tab,
    render_abc_health_tab,
    render_abc_gate_tab,
    render_abc_safety_tab,
    render_abc_scorecard_tab,
    render_abc_paper_order_intent_tab,
    render_abc_report_tab,
)


def test_panel_version_172():
    assert PANEL_VERSION == "1.7.4"


def test_panel_title_has_172():
    assert "1.7.4" in PANEL_TITLE


def test_tabs_total_55():
    assert len(_TABS) == 84


def test_abc_tabs_count_18():
    assert len(_TABS_V172_ABC) == 18


def test_get_abc_tab_names_count_18():
    names = get_abc_tab_names()
    assert len(names) == 18


def test_render_all_tabs_count_55():
    result = render_all_tabs()
    assert len(result) == 84


def test_render_abc_execution_overview_returns_dict():
    result = render_abc_execution_overview_tab()
    assert isinstance(result, dict)


def test_render_abc_a_pullback_returns_dict():
    result = render_abc_a_10ma_pullback_tab()
    assert isinstance(result, dict)


def test_render_abc_b_breakout_returns_dict():
    result = render_abc_b_platform_breakout_tab()
    assert isinstance(result, dict)


def test_render_abc_c_reclaim_returns_dict():
    result = render_abc_c_20ma_reclaim_tab()
    assert isinstance(result, dict)


def test_render_abc_health_tab_returns_dict():
    result = render_abc_health_tab()
    assert isinstance(result, dict)


def test_render_abc_gate_tab_returns_dict():
    result = render_abc_gate_tab()
    assert isinstance(result, dict)


def test_render_abc_safety_tab_returns_dict():
    result = render_abc_safety_tab()
    assert isinstance(result, dict)


def test_render_abc_scorecard_tab_paper_only():
    result = render_abc_scorecard_tab()
    assert result.get("paper_only") is True


def test_render_abc_paper_order_intent_tab_no_real_orders():
    result = render_abc_paper_order_intent_tab()
    assert result.get("no_real_orders") is True


def test_render_abc_report_tab_returns_dict():
    result = render_abc_report_tab()
    assert isinstance(result, dict)
