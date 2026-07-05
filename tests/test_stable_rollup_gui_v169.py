"""
tests/test_stable_rollup_gui_v169.py
Tests for GUI panel.
"""
import pytest
import gui.live_paper_trading_stable_rollup_panel as panel_module
from gui.live_paper_trading_stable_rollup_panel import (
    LivePaperTradingStableRollupPanel, PANEL_TITLE, PANEL_VERSION, PANEL_TABS,
    headless_safe, NO_REAL_ORDERS, PRODUCTION_BLOCKED,
)


def test_panel_module_importable():
    assert panel_module is not None


def test_panel_title():
    assert PANEL_TITLE == "Live Paper Trading Stable Rollup"


def test_panel_version():
    assert PANEL_VERSION == "1.6.9"


def test_headless_safe_true():
    assert headless_safe is True


def test_no_real_orders_true():
    assert NO_REAL_ORDERS is True


def test_production_blocked_true():
    assert PRODUCTION_BLOCKED is True


def test_panel_tabs_count_21():
    assert len(PANEL_TABS) == 21


def test_panel_tabs_has_overview():
    assert "Overview" in PANEL_TABS


def test_panel_tabs_has_releases():
    assert "Releases" in PANEL_TABS


def test_panel_tabs_has_safety():
    assert "Safety" in PANEL_TABS


def test_panel_tabs_has_scorecard():
    assert "Scorecard" in PANEL_TABS


def test_panel_tabs_has_migration_readiness():
    assert "Migration Readiness" in PANEL_TABS


def test_panel_instantiable():
    p = LivePaperTradingStableRollupPanel()
    assert p is not None


def test_panel_get_tab_names():
    p = LivePaperTradingStableRollupPanel()
    tabs = p.get_tab_names()
    assert isinstance(tabs, list)
    assert len(tabs) == 21


def test_panel_render_tab_0():
    p = LivePaperTradingStableRollupPanel()
    result = p.render_tab(0)
    assert isinstance(result, dict)
    assert result["tab_name"] == "Overview"


def test_panel_render_tab_invalid():
    p = LivePaperTradingStableRollupPanel()
    result = p.render_tab(99)
    assert "error" in result


def test_panel_render_overview():
    p = LivePaperTradingStableRollupPanel()
    result = p.render_overview()
    assert result["version"] == "1.6.9"
    assert result["paper_only"] is True


def test_panel_headless_safe_attr():
    p = LivePaperTradingStableRollupPanel()
    assert p.headless_safe is True


def test_panel_no_real_orders_attr():
    p = LivePaperTradingStableRollupPanel()
    assert p.NO_REAL_ORDERS is True


def test_panel_to_text():
    p = LivePaperTradingStableRollupPanel()
    text = p.to_text()
    assert isinstance(text, str)
    assert "1.6.9" in text
