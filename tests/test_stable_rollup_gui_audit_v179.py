"""
tests/test_stable_rollup_gui_audit_v179.py
Tests for stable_rollup_gui_audit_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179 import (
    run_gui_audit,
    get_required_stable_tabs,
)


def test_get_required_stable_tabs_returns_list():
    tabs = get_required_stable_tabs()
    assert isinstance(tabs, list)


def test_get_required_stable_tabs_count_3():
    tabs = get_required_stable_tabs()
    assert len(tabs) == 3


def test_get_required_stable_tabs_contains_stable_rollup():
    tabs = get_required_stable_tabs()
    assert "stable_rollup" in tabs


def test_get_required_stable_tabs_contains_stable_health():
    tabs = get_required_stable_tabs()
    assert "stable_health" in tabs


def test_get_required_stable_tabs_contains_stable_report():
    tabs = get_required_stable_tabs()
    assert "stable_report" in tabs


def test_run_gui_audit_returns_dict():
    result = run_gui_audit()
    assert isinstance(result, dict)


def test_run_gui_audit_all_tabs_present():
    result = run_gui_audit()
    assert result["all_tabs_present"] is True


def test_run_gui_audit_render_clean():
    result = run_gui_audit()
    assert result["render_clean"] is True


def test_run_gui_audit_panel_version_179():
    result = run_gui_audit()
    assert result["panel_version"] == "1.8.3"


def test_run_gui_audit_no_missing_tabs():
    result = run_gui_audit()
    assert result["missing_tabs"] == []


def test_run_gui_audit_no_error_tabs():
    result = run_gui_audit()
    assert result["error_tabs"] == []


def test_run_gui_audit_paper_only():
    result = run_gui_audit()
    assert result["paper_only"] is True


def test_run_gui_audit_no_real_orders():
    result = run_gui_audit()
    assert result["no_real_orders"] is True


def test_run_gui_audit_stable_tabs_present_list():
    result = run_gui_audit()
    assert isinstance(result["stable_tabs_present"], list)
    assert len(result["stable_tabs_present"]) == 3


def test_run_gui_audit_total_tabs_ge_3():
    result = run_gui_audit()
    assert result["total_tabs"] >= 3
