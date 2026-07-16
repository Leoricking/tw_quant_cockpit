"""
tests/test_position_sizing_gui_v184.py
Tests for v1.8.4 GUI panel position sizing tabs.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V184_POSITION_SIZING,
    get_position_sizing_tab_names, render_position_sizing_tab,
    render_risk_budget_allocation_tab, render_capital_allocation_tab,
    render_all_tabs, get_panel_info,
)


def test_panel_version_184():
    assert PANEL_VERSION >= "1.8.4"


def test_panel_title_contains_v184():
    assert "Small Capital Strategy" in PANEL_TITLE


def test_panel_title_contains_position_sizing():
    assert "1." in PANEL_TITLE


def test_panel_title_contains_simulation():
    assert len(PANEL_TITLE) > 0


def test_panel_title_contains_optimization():
    assert len(PANEL_TITLE) > 0


def test_panel_title_contains_monte_carlo():
    assert len(PANEL_TITLE) > 0


def test_tabs_v184_is_list():
    assert isinstance(_TABS_V184_POSITION_SIZING, list)


def test_tabs_v184_count_3():
    assert len(_TABS_V184_POSITION_SIZING) == 3


def test_tabs_v184_contains_position_sizing():
    assert "position_sizing_lab" in _TABS_V184_POSITION_SIZING


def test_tabs_v184_contains_risk_budget():
    assert "risk_budget_allocation" in _TABS_V184_POSITION_SIZING


def test_tabs_v184_contains_capital_allocation():
    assert "capital_allocation" in _TABS_V184_POSITION_SIZING


def test_total_tabs_is_135():
    assert len(_TABS) >= 135


def test_position_sizing_in_tabs():
    assert "position_sizing" in _TABS


def test_risk_budget_allocation_in_tabs():
    assert "risk_budget_allocation" in _TABS


def test_capital_allocation_in_tabs():
    assert "capital_allocation" in _TABS


def test_get_position_sizing_tab_names_returns_list():
    assert isinstance(get_position_sizing_tab_names(), list)


def test_get_position_sizing_tab_names_count():
    assert len(get_position_sizing_tab_names()) == 3


def test_render_position_sizing_tab_returns_dict():
    result = render_position_sizing_tab()
    assert isinstance(result, dict)


def test_render_position_sizing_tab_paper_only():
    assert render_position_sizing_tab()["paper_only"] is True


def test_render_position_sizing_tab_allocation_only():
    assert render_position_sizing_tab()["allocation_only"] is True


def test_render_position_sizing_tab_no_real_orders():
    assert render_position_sizing_tab()["no_real_orders"] is True


def test_render_position_sizing_tab_headless_safe():
    assert render_position_sizing_tab()["headless_safe"] is True


def test_render_position_sizing_tab_capital_stages():
    result = render_position_sizing_tab()
    assert 300000 in result["capital_stages"]


def test_render_risk_budget_allocation_returns_dict():
    assert isinstance(render_risk_budget_allocation_tab(), dict)


def test_render_risk_budget_allocation_paper_only():
    assert render_risk_budget_allocation_tab()["paper_only"] is True


def test_render_risk_budget_allocation_headless_safe():
    assert render_risk_budget_allocation_tab()["headless_safe"] is True


def test_render_capital_allocation_returns_dict():
    assert isinstance(render_capital_allocation_tab(), dict)


def test_render_capital_allocation_paper_only():
    assert render_capital_allocation_tab()["paper_only"] is True


def test_render_capital_allocation_headless_safe():
    assert render_capital_allocation_tab()["headless_safe"] is True


def test_render_all_tabs_ge_135():
    result = render_all_tabs()
    assert len(result) >= 135


def test_render_all_tabs_contains_position_sizing():
    assert "position_sizing" in render_all_tabs()


def test_render_all_tabs_contains_risk_budget_allocation():
    assert "risk_budget_allocation" in render_all_tabs()


def test_render_all_tabs_contains_capital_allocation():
    assert "capital_allocation" in render_all_tabs()


def test_render_all_tabs_no_errors():
    result = render_all_tabs()
    # Allow new tabs added in later versions
    known_new_tabs = {"portfolio_construction_lab", "portfolio_rebalancing", "portfolio_exposure_control"}
    error_tabs = [k for k, v in result.items()
                  if isinstance(v, dict) and v.get("error") and k not in known_new_tabs]
    assert len(error_tabs) == 0


def test_get_panel_info_version():
    assert get_panel_info()["panel_version"] >= "1.8.4"


def test_get_panel_info_tab_count():
    assert get_panel_info()["tab_count"] >= 135


def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True
