"""
tests/test_paper_cockpit_gui_v202.py
v2.0.2 Paper Cockpit — GUI Tests (25+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# Panel version constants
# ---------------------------------------------------------------------------

def test_panel_version_v202():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    assert PANEL_VERSION_V202 == "2.0.2"


def test_panel_version_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"


def test_panel_version_v201_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V201
    assert PANEL_VERSION_V201 == "2.0.1"


def test_panel_version_v202_string():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    assert isinstance(PANEL_VERSION_V202, str)


# ---------------------------------------------------------------------------
# Tab names
# ---------------------------------------------------------------------------

def test_get_tab_names_has_report_export_v202():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "report_export_v202" in get_tab_names()


def test_get_tab_names_has_audit_pack_v202():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "audit_pack_v202" in get_tab_names()


def test_get_tab_names_has_export_status_v202():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "export_status_v202" in get_tab_names()


def test_get_v202_tab_names_returns_list():
    from gui.small_capital_strategy_panel import get_v202_tab_names
    result = get_v202_tab_names()
    assert isinstance(result, list)


def test_get_v202_tab_names_count():
    from gui.small_capital_strategy_panel import get_v202_tab_names
    assert len(get_v202_tab_names()) == 3


def test_get_v202_tab_names_has_report_export():
    from gui.small_capital_strategy_panel import get_v202_tab_names
    assert "report_export_v202" in get_v202_tab_names()


def test_get_v202_tab_names_has_audit_pack():
    from gui.small_capital_strategy_panel import get_v202_tab_names
    assert "audit_pack_v202" in get_v202_tab_names()


def test_get_v202_tab_names_has_export_status():
    from gui.small_capital_strategy_panel import get_v202_tab_names
    assert "export_status_v202" in get_v202_tab_names()


# ---------------------------------------------------------------------------
# Render functions
# ---------------------------------------------------------------------------

def test_render_report_export_v202_tab_callable():
    from gui.small_capital_strategy_panel import render_report_export_v202_tab
    result = render_report_export_v202_tab()
    assert result is not None


def test_render_report_export_v202_tab_key():
    from gui.small_capital_strategy_panel import render_report_export_v202_tab
    result = render_report_export_v202_tab()
    assert result["tab"] == "report_export_v202"


def test_render_report_export_v202_tab_version():
    from gui.small_capital_strategy_panel import render_report_export_v202_tab
    result = render_report_export_v202_tab()
    assert result["version"] == "2.0.2"


def test_render_report_export_v202_tab_paper_only():
    from gui.small_capital_strategy_panel import render_report_export_v202_tab
    result = render_report_export_v202_tab()
    assert result["paper_only"] is True


def test_render_report_export_v202_tab_no_real_orders():
    from gui.small_capital_strategy_panel import render_report_export_v202_tab
    result = render_report_export_v202_tab()
    assert result["no_real_orders"] is True


def test_render_audit_pack_v202_tab_callable():
    from gui.small_capital_strategy_panel import render_audit_pack_v202_tab
    result = render_audit_pack_v202_tab()
    assert result is not None


def test_render_audit_pack_v202_tab_key():
    from gui.small_capital_strategy_panel import render_audit_pack_v202_tab
    result = render_audit_pack_v202_tab()
    assert result["tab"] == "audit_pack_v202"


def test_render_audit_pack_v202_tab_paper_only():
    from gui.small_capital_strategy_panel import render_audit_pack_v202_tab
    result = render_audit_pack_v202_tab()
    assert result["paper_only"] is True


def test_render_audit_pack_v202_tab_fields():
    from gui.small_capital_strategy_panel import render_audit_pack_v202_tab
    result = render_audit_pack_v202_tab()
    assert "audit_pack_fields" in result
    assert len(result["audit_pack_fields"]) == 11


def test_render_export_status_v202_tab_callable():
    from gui.small_capital_strategy_panel import render_export_status_v202_tab
    result = render_export_status_v202_tab()
    assert result is not None


def test_render_export_status_v202_tab_key():
    from gui.small_capital_strategy_panel import render_export_status_v202_tab
    result = render_export_status_v202_tab()
    assert result["tab"] == "export_status_v202"


def test_render_export_status_v202_tab_paper_only():
    from gui.small_capital_strategy_panel import render_export_status_v202_tab
    result = render_export_status_v202_tab()
    assert result["paper_only"] is True


def test_render_export_status_v202_tab_formats():
    from gui.small_capital_strategy_panel import render_export_status_v202_tab
    result = render_export_status_v202_tab()
    assert "formats_available" in result
    assert len(result["formats_available"]) == 4


def test_render_export_status_v202_tab_paper_guard():
    from gui.small_capital_strategy_panel import render_export_status_v202_tab
    result = render_export_status_v202_tab()
    assert result["paper_only_guard_enabled"] is True


def test_v202_tab_render_map_present():
    from gui.small_capital_strategy_panel import _TAB_RENDER_MAP_V202
    assert "report_export_v202" in _TAB_RENDER_MAP_V202
    assert "audit_pack_v202" in _TAB_RENDER_MAP_V202
    assert "export_status_v202" in _TAB_RENDER_MAP_V202
