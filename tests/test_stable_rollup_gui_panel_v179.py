"""
tests/test_stable_rollup_gui_panel_v179.py
Tests for GUI panel stable rollup tabs (v1.7.9).
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    PANEL_TITLE,
    _TABS,
    _TABS_V179_STABLE_ROLLUP,
    render_stable_rollup_tab,
    render_stable_health_tab,
    render_stable_report_tab,
    render_all_tabs,
    get_stable_rollup_tab_names,
    get_tab_names,
)


def test_panel_version_is_179():
    assert PANEL_VERSION >= "1.8.4"


def test_panel_title_contains_179():
    assert "Small Capital Strategy" in PANEL_TITLE


def test_tabs_v179_stable_rollup_count_3():
    assert len(_TABS_V179_STABLE_ROLLUP) == 3


def test_tabs_v179_contains_stable_rollup():
    assert "stable_rollup" in _TABS_V179_STABLE_ROLLUP


def test_tabs_v179_contains_stable_health():
    assert "stable_health" in _TABS_V179_STABLE_ROLLUP


def test_tabs_v179_contains_stable_report():
    assert "stable_report" in _TABS_V179_STABLE_ROLLUP


def test_all_tabs_contains_stable_rollup():
    assert "stable_rollup" in _TABS


def test_all_tabs_contains_stable_health():
    assert "stable_health" in _TABS


def test_render_stable_rollup_tab_returns_dict():
    result = render_stable_rollup_tab()
    assert isinstance(result, dict)


def test_render_stable_rollup_tab_tab_key():
    result = render_stable_rollup_tab()
    assert result["tab"] == "stable_rollup"


def test_render_stable_rollup_tab_version_179():
    result = render_stable_rollup_tab()
    assert result["version"] == "1.7.9"


def test_render_stable_rollup_tab_paper_only():
    result = render_stable_rollup_tab()
    assert result["paper_only"] is True


def test_render_stable_rollup_tab_no_real_orders():
    result = render_stable_rollup_tab()
    assert result["no_real_orders"] is True


def test_render_stable_rollup_tab_not_investment_advice():
    result = render_stable_rollup_tab()
    assert result["not_investment_advice"] is True


def test_render_stable_rollup_tab_included_releases_9():
    result = render_stable_rollup_tab()
    assert result["included_releases"] == 9


def test_render_stable_health_tab_returns_dict():
    result = render_stable_health_tab()
    assert isinstance(result, dict)


def test_render_stable_health_tab_tab_key():
    result = render_stable_health_tab()
    assert result["tab"] == "stable_health"


def test_render_stable_health_tab_paper_only():
    result = render_stable_health_tab()
    assert result["paper_only"] is True


def test_render_stable_health_tab_status_ready():
    result = render_stable_health_tab()
    assert result.get("status") == "READY"


def test_render_stable_health_tab_no_error():
    result = render_stable_health_tab()
    assert result.get("error") is None


def test_render_stable_report_tab_returns_dict():
    result = render_stable_report_tab()
    assert isinstance(result, dict)


def test_render_stable_report_tab_tab_key():
    result = render_stable_report_tab()
    assert result["tab"] == "stable_report"


def test_render_stable_report_tab_paper_only():
    result = render_stable_report_tab()
    assert result["paper_only"] is True


def test_render_stable_report_tab_report_sections_11():
    result = render_stable_report_tab()
    assert result["report_sections"] == 11


def test_render_all_tabs_returns_dict():
    result = render_all_tabs()
    assert isinstance(result, dict)


def test_render_all_tabs_contains_stable_rollup():
    result = render_all_tabs()
    assert "stable_rollup" in result


def test_render_all_tabs_contains_stable_health():
    result = render_all_tabs()
    assert "stable_health" in result


def test_render_all_tabs_no_error_in_stable_rollup():
    result = render_all_tabs()
    tab_data = result.get("stable_rollup", {})
    assert tab_data.get("error") is None


def test_get_stable_rollup_tab_names_returns_list():
    names = get_stable_rollup_tab_names()
    assert isinstance(names, list)


def test_get_stable_rollup_tab_names_count_3():
    names = get_stable_rollup_tab_names()
    assert len(names) == 3


def test_get_tab_names_contains_all_stable_tabs():
    names = get_tab_names()
    for tab in ["stable_rollup", "stable_health", "stable_report"]:
        assert tab in names
