"""
tests/test_paper_cockpit_backward_compat_v202.py
v2.0.2 Paper Cockpit — Backward Compatibility Tests (25+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# v2.0.1 backward compat
# ---------------------------------------------------------------------------

def test_import_v201_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION
    assert VERSION == "2.0.1"


def test_v201_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "201"


def test_v201_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True


def test_v201_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False


def test_v201_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


def test_v201_run_daily_workflow_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    result = run_daily_workflow()
    assert result is not None


def test_v201_run_daily_workflow_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    result = run_daily_workflow()
    assert result.paper_only is True


def test_v201_run_daily_workflow_no_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    result = run_daily_workflow()
    assert result.cockpit_executes_order is False


def test_v201_no_entry_reasons_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_ENTRY_REASONS
    assert len(NO_ENTRY_REASONS) == 13


def test_v201_daily_final_actions_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import DAILY_FINAL_ACTIONS
    assert len(DAILY_FINAL_ACTIONS) == 7


def test_v201_has_paper_buy_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import DAILY_FINAL_ACTIONS
    assert "PAPER_BUY_PLAN" in DAILY_FINAL_ACTIONS


def test_v201_has_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_ENTRY_REASONS
    assert "human_review_required" in NO_ENTRY_REASONS


def test_v201_models_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import _ALL_MODEL_NAMES_V201
    assert len(_ALL_MODEL_NAMES_V201) == 12


# ---------------------------------------------------------------------------
# v2.0.0 backward compat
# ---------------------------------------------------------------------------

def test_import_v200_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION
    assert VERSION == "2.0.0"


def test_v200_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "200"


def test_v200_paper_only():
    """v2.0.0 module should be importable and VERSION should be 2.0.0."""
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION
    assert VERSION == "2.0.0"


# ---------------------------------------------------------------------------
# GUI backward compat
# ---------------------------------------------------------------------------

def test_gui_panel_version_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"


def test_gui_panel_version_v201_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V201
    assert PANEL_VERSION_V201 == "2.0.1"


def test_gui_panel_version_v202_new():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    assert PANEL_VERSION_V202 == "2.0.2"


def test_gui_v201_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "daily_workflow_v201" in tabs
    assert "no_entry_reason_detail" in tabs
    assert "decision_ticket_v201" in tabs


def test_gui_v200_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "paper_cockpit" in tabs
    assert "strategy_decision_console" in tabs
    assert "decision_ticket" in tabs


def test_gui_v202_tabs_added():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "report_export_v202" in tabs
    assert "audit_pack_v202" in tabs
    assert "export_status_v202" in tabs


def test_v202_covered_versions_includes_201():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    assert "2.0.1" in COVERED_VERSIONS


def test_v202_covered_versions_includes_200():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    assert "2.0.0" in COVERED_VERSIONS


def test_v202_covered_versions_includes_170():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    assert "1.7.0" in COVERED_VERSIONS


def test_v201_get_v201_tab_names_unchanged():
    from gui.small_capital_strategy_panel import get_v201_tab_names
    tabs = get_v201_tab_names()
    assert len(tabs) == 3
    assert "daily_workflow_v201" in tabs
