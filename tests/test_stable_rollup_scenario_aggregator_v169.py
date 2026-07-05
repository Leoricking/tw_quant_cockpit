"""
tests/test_stable_rollup_scenario_aggregator_v169.py
Tests for scenario_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.scenario_aggregator_v169 import run


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "scenario_aggregator_v169"


def test_run_total_ge_80():
    result = run()
    assert result["total"] >= 80


def test_run_has_categories():
    result = run()
    assert "categories" in result
    assert isinstance(result["categories"], dict)


def test_run_has_status():
    result = run()
    assert "status" in result


def test_run_status_pass():
    result = run()
    assert result["status"] == "PASS"


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_run_categories_non_empty():
    result = run()
    assert len(result["categories"]) > 0


def test_run_has_passed():
    result = run()
    assert "passed" in result
    assert result["passed"] >= 0


def test_run_has_failed():
    result = run()
    assert "failed" in result


def test_run_validation_status_pass():
    result = run()
    assert result.get("validation_status") == "PASS"


def test_categories_include_release_identity():
    result = run()
    assert "release_identity" in result["categories"]
