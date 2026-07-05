"""
tests/test_stable_rollup_contract_aggregator_v169.py
Tests for contract_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.contract_aggregator_v169 import run


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "contract_aggregator_v169"


def test_run_has_total_checks():
    result = run()
    assert "total_checks" in result
    assert result["total_checks"] > 0


def test_run_has_passed():
    result = run()
    assert "passed" in result


def test_run_has_failed():
    result = run()
    assert "failed" in result
    assert result["failed"] == 0


def test_run_all_pass():
    result = run()
    assert result["all_pass"] is True


def test_run_status_pass():
    result = run()
    assert result["status"] == "PASS"


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_run_has_details():
    result = run()
    assert "details" in result
    assert isinstance(result["details"], list)


def test_run_total_is_8():
    result = run()
    assert result["total_checks"] == 8


def test_run_version():
    result = run()
    assert result["version"] == "1.6.9"
