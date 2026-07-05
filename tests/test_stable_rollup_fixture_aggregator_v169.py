"""
tests/test_stable_rollup_fixture_aggregator_v169.py
Tests for fixture_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.fixture_aggregator_v169 import run


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "fixture_aggregator_v169"


def test_run_has_total():
    result = run()
    assert "total" in result
    assert isinstance(result["total"], int)


def test_run_has_valid():
    result = run()
    assert "valid" in result


def test_run_has_invalid():
    result = run()
    assert "invalid" in result


def test_run_has_status():
    result = run()
    assert "status" in result


def test_run_total_ge_80():
    result = run()
    assert result["total"] >= 80


def test_run_valid_ge_80():
    result = run()
    assert result["valid"] >= 80


def test_run_invalid_zero():
    result = run()
    assert result["invalid"] == 0


def test_run_missing_markers_zero():
    result = run()
    assert result["missing_markers"] == 0


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_run_status_pass():
    result = run()
    assert result["status"] == "PASS"


def test_run_has_fixture_root():
    result = run()
    assert "fixture_root" in result
