"""
tests/test_stable_rollup_cli_audit_v179.py
Tests for stable_rollup_cli_audit_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_cli_audit_v179 import (
    run_cli_audit,
    get_required_stable_commands,
)


def test_get_required_stable_commands_returns_list():
    cmds = get_required_stable_commands()
    assert isinstance(cmds, list)


def test_get_required_stable_commands_count_12():
    cmds = get_required_stable_commands()
    assert len(cmds) == 12


def test_get_required_stable_commands_contains_version():
    cmds = get_required_stable_commands()
    assert "small-capital-stable-version" in cmds


def test_get_required_stable_commands_contains_manifest():
    cmds = get_required_stable_commands()
    assert "small-capital-stable-manifest" in cmds


def test_get_required_stable_commands_contains_health():
    cmds = get_required_stable_commands()
    assert "small-capital-stable-health" in cmds


def test_get_required_stable_commands_contains_gate():
    cmds = get_required_stable_commands()
    assert "small-capital-stable-gate" in cmds


def test_get_required_stable_commands_contains_report():
    cmds = get_required_stable_commands()
    assert "small-capital-stable-report" in cmds


def test_run_cli_audit_returns_dict():
    result = run_cli_audit()
    assert isinstance(result, dict)


def test_run_cli_audit_all_registered():
    result = run_cli_audit()
    assert result["all_registered"] is True


def test_run_cli_audit_registered_count_12():
    result = run_cli_audit()
    assert result["registered_count"] == 12


def test_run_cli_audit_missing_count_zero():
    result = run_cli_audit()
    assert result["missing_count"] == 0


def test_run_cli_audit_missing_is_empty():
    result = run_cli_audit()
    assert result["missing"] == []


def test_run_cli_audit_paper_only():
    result = run_cli_audit()
    assert result["paper_only"] is True


def test_run_cli_audit_no_real_orders():
    result = run_cli_audit()
    assert result["no_real_orders"] is True


def test_run_cli_audit_total_required_12():
    result = run_cli_audit()
    assert result["total_required"] == 12
