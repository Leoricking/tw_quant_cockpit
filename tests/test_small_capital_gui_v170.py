"""tests/test_small_capital_gui_v170.py — GUI panel tests for v1.7.0."""
import pytest
from gui.small_capital_strategy_panel import (
    get_tab_names, get_panel_info, render_overview_tab, render_version_info_tab,
    render_safety_tab, render_capital_profile_tab, render_risk_budget_tab,
    render_allocation_tab, render_market_regime_tab, render_scorecard_tab,
    render_paper_simulation_tab, render_scenarios_tab, render_all_tabs,
    PANEL_VERSION, PANEL_TITLE, _TABS,
)


def test_panel_version():
    # Panel updated to v1.7.2 to include ABC execution tabs
    assert PANEL_VERSION == "1.7.2"


def test_panel_title_contains_v170():
    # Title updated for v1.7.1 Watchlist Strategy Layer
    assert "Small Capital" in PANEL_TITLE


def test_tab_count_22():
    # v1.7.2 adds 18 ABC tabs on top of 37 (22+15) = 55 total
    assert len(_TABS) == 55


def test_get_tab_names_returns_22():
    # v1.7.2 extended panel has 55 tabs (22 v1.7.0 + 15 watchlist + 18 ABC)
    tabs = get_tab_names()
    assert len(tabs) == 55


def test_get_panel_info_returns_dict():
    info = get_panel_info()
    assert isinstance(info, dict)


def test_get_panel_info_tab_count_22():
    # v1.7.2 extended panel has 55 tabs
    info = get_panel_info()
    assert info["tab_count"] == 55


def test_get_panel_info_paper_only():
    info = get_panel_info()
    assert info["paper_only"] is True


def test_get_panel_info_headless_safe():
    info = get_panel_info()
    assert info["headless_safe"] is True


def test_render_overview_tab():
    data = render_overview_tab()
    assert isinstance(data, dict)
    assert data["paper_only"] is True


def test_render_version_info_tab():
    data = render_version_info_tab()
    assert isinstance(data, dict)
    assert data["version"] == "1.7.0"


def test_render_safety_tab():
    data = render_safety_tab()
    assert isinstance(data, dict)
    assert "flags" in data


def test_render_capital_profile_tab():
    data = render_capital_profile_tab()
    assert isinstance(data, dict)
    assert data["capital_twd"] == 300000.0


def test_render_risk_budget_tab():
    data = render_risk_budget_tab()
    assert isinstance(data, dict)
    assert data["max_loss_per_trade"] == 3000.0


def test_render_allocation_tab_bull():
    data = render_allocation_tab("BULL")
    assert isinstance(data, dict)
    assert data["regime"] == "BULL"


def test_render_allocation_tab_bear():
    data = render_allocation_tab("BEAR")
    assert data["cash_pct"] >= 0.49


def test_render_market_regime_tab_bull():
    data = render_market_regime_tab("BULL")
    assert isinstance(data, dict)
    assert data["trade_allowed"] is True


def test_render_scorecard_tab():
    data = render_scorecard_tab()
    assert isinstance(data, dict)
    assert data["weights_sum"] == 100


def test_render_paper_simulation_tab():
    data = render_paper_simulation_tab()
    assert isinstance(data, dict)
    assert data["paper_only"] is True


def test_render_scenarios_tab():
    data = render_scenarios_tab()
    assert isinstance(data, dict)
    assert data["total"] == 80


def test_render_all_tabs_returns_dict():
    # v1.7.2 extended panel renders 55 tabs (22 v1.7.0 + 15 watchlist + 18 ABC)
    data = render_all_tabs()
    assert isinstance(data, dict)
    assert len(data) == 55


def test_render_all_tabs_no_import_errors():
    data = render_all_tabs()
    for tab_name, tab_data in data.items():
        assert "error" not in tab_data or tab_data.get("error") is None, \
            f"Tab '{tab_name}' has error: {tab_data.get('error')}"


def test_tab_names_include_overview():
    assert "overview" in get_tab_names()


def test_tab_names_include_health_gate():
    assert "health_gate" in get_tab_names()


def test_tab_names_include_scorecard():
    assert "scorecard" in get_tab_names()
