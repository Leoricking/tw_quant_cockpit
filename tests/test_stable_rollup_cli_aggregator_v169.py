"""
tests/test_stable_rollup_cli_aggregator_v169.py
Tests for cli_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.cli_aggregator_v169 import run, MIN_STABLE_ROLLUP_COMMANDS


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "cli_aggregator_v169"


def test_run_has_version():
    result = run()
    assert result["version"] == "1.6.9"


def test_run_has_status():
    result = run()
    assert "status" in result


def test_run_has_formal():
    result = run()
    assert "formal" in result
    assert isinstance(result["formal"], int)


def test_run_has_stable_rollup_commands():
    result = run()
    assert "stable_rollup_commands" in result


def test_stable_rollup_commands_ge_26():
    result = run()
    assert result["stable_rollup_commands"] >= MIN_STABLE_ROLLUP_COMMANDS


def test_run_unresolved_zero():
    result = run()
    assert result.get("unresolved", 0) == 0


def test_run_no_duplicates():
    result = run()
    assert result.get("duplicate_names", []) == []


def test_min_stable_rollup_commands_is_26():
    assert MIN_STABLE_ROLLUP_COMMANDS == 26


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_run_total_commands_positive():
    result = run()
    assert result["total_commands"] > 0


def test_run_has_resolved():
    result = run()
    assert "resolved" in result
    assert result["resolved"] >= 0


def test_run_status_pass_or_partial():
    result = run()
    assert result["status"] in ("PASS", "PARTIAL", "DEGRADED")
