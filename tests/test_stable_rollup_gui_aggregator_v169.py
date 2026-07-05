"""
tests/test_stable_rollup_gui_aggregator_v169.py
Tests for gui_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.gui_aggregator_v169 import run


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "gui_aggregator_v169"


def test_run_has_panels_found():
    result = run()
    assert "panels_found" in result


def test_run_has_headless_safe():
    result = run()
    assert "headless_safe" in result


def test_run_headless_safe_true():
    result = run()
    assert result["headless_safe"] is True


def test_run_has_no_broker():
    result = run()
    assert "no_broker" in result
    assert result["no_broker"] is True


def test_run_has_no_production():
    result = run()
    assert "no_production" in result
    assert result["no_production"] is True


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_run_status():
    result = run()
    assert "status" in result
    assert result["status"] in ("PASS", "DEGRADED")


def test_panels_found_ge_1():
    result = run()
    assert result["panels_found"] >= 1


def test_run_has_empty_state_ok():
    result = run()
    assert "empty_state_ok" in result
