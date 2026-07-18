"""
tests/test_strategy_monitoring_cli_v194.py
Tests for CLI commands introduced in v1.9.4 — Paper Strategy Monitoring & Drift Detection Lab.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, get_commands_by_group


# ── command group ─────────────────────────────────────────────────────────────

def test_strategy_monitoring_commands_in_provider_commands():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "strategy-monitoring-version" in names


def test_strategy_monitoring_commands_count_ge_18():
    sm_cmds = [c for c in get_commands_by_group("strategy_monitoring")
               if c.introduced_in == "1.9.4"]
    assert len(sm_cmds) >= 18


# ── individual command presence ───────────────────────────────────────────────

def test_cli_strategy_monitoring_version():
    assert any(c.name == "strategy-monitoring-version" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_run():
    assert any(c.name == "strategy-monitoring-run" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_drift():
    assert any(c.name == "strategy-monitoring-drift" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_package():
    assert any(c.name == "strategy-monitoring-package" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_rules():
    assert any(c.name == "strategy-monitoring-rules" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_window():
    assert any(c.name == "strategy-monitoring-window" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_alerts():
    assert any(c.name == "strategy-monitoring-alerts" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_rollback():
    assert any(c.name == "strategy-monitoring-rollback" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_report():
    assert any(c.name == "strategy-monitoring-report" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_dashboard():
    assert any(c.name == "strategy-monitoring-dashboard" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_export():
    assert any(c.name == "strategy-monitoring-export" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_evidence():
    assert any(c.name == "strategy-monitoring-evidence" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_audit():
    assert any(c.name == "strategy-monitoring-audit" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_health():
    assert any(c.name == "strategy-monitoring-health" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_gate():
    assert any(c.name == "strategy-monitoring-gate" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_scenarios():
    assert any(c.name == "strategy-monitoring-scenarios" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_fixtures():
    assert any(c.name == "strategy-monitoring-fixtures" for c in PROVIDER_COMMANDS)


def test_cli_strategy_monitoring_safety_audit():
    assert any(c.name == "strategy-monitoring-safety-audit" for c in PROVIDER_COMMANDS)


# ── command attributes ────────────────────────────────────────────────────────

def test_all_monitoring_commands_have_group():
    sm_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-monitoring-")]
    assert all(c.group == "strategy_monitoring" for c in sm_cmds)


def test_all_monitoring_commands_introduced_in_194():
    sm_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-monitoring-")]
    assert all(c.introduced_in == "1.9.4" for c in sm_cmds)


def test_all_monitoring_commands_research_only():
    sm_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-monitoring-")]
    assert all(c.research_only is True for c in sm_cmds)


def test_all_monitoring_commands_have_help():
    sm_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-monitoring-")]
    assert all(len(c.help) > 0 for c in sm_cmds)
