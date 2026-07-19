"""
tests/test_strategy_governance_dashboard_cli_v197.py
Tests for Paper Strategy Governance Dashboard CLI commands v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest
from cli.command_registry import PROVIDER_COMMANDS, CommandSpec


# ── Helper ──────────────────────────────────────────────────────────────────────

def _get_sgd_commands():
    return [c for c in PROVIDER_COMMANDS if getattr(c, "group", None) == "strategy_governance_dashboard"]

def _get_sgd_command_names():
    return [c.name for c in _get_sgd_commands()]


# ── Count ───────────────────────────────────────────────────────────────────────

def test_sgd_commands_present():
    assert len(_get_sgd_commands()) >= 16

def test_provider_commands_is_list():
    assert isinstance(PROVIDER_COMMANDS, list)

def test_all_sgd_commands_are_command_spec():
    for cmd in _get_sgd_commands():
        assert isinstance(cmd, CommandSpec)


# ── Required command names ──────────────────────────────────────────────────────

def test_cmd_version_present():
    assert "strategy-governance-dashboard-version" in _get_sgd_command_names()

def test_cmd_run_present():
    assert "strategy-governance-dashboard-run" in _get_sgd_command_names()

def test_cmd_quality_present():
    assert "strategy-governance-dashboard-quality" in _get_sgd_command_names()

def test_cmd_scorecard_present():
    assert "strategy-governance-dashboard-scorecard" in _get_sgd_command_names()

def test_cmd_evidence_present():
    assert "strategy-governance-dashboard-evidence" in _get_sgd_command_names()

def test_cmd_outcomes_present():
    assert "strategy-governance-dashboard-outcomes" in _get_sgd_command_names()

def test_cmd_violations_present():
    assert "strategy-governance-dashboard-violations" in _get_sgd_command_names()

def test_cmd_rollback_frequency_present():
    assert "strategy-governance-dashboard-rollback-frequency" in _get_sgd_command_names()

def test_cmd_lineage_health_present():
    assert "strategy-governance-dashboard-lineage-health" in _get_sgd_command_names()

def test_cmd_audit_health_present():
    assert "strategy-governance-dashboard-audit-health" in _get_sgd_command_names()

def test_cmd_report_present():
    assert "strategy-governance-dashboard-report" in _get_sgd_command_names()

def test_cmd_export_present():
    assert "strategy-governance-dashboard-export" in _get_sgd_command_names()

def test_cmd_health_present():
    assert "strategy-governance-dashboard-health" in _get_sgd_command_names()

def test_cmd_gate_present():
    assert "strategy-governance-dashboard-gate" in _get_sgd_command_names()

def test_cmd_scenarios_present():
    assert "strategy-governance-dashboard-scenarios" in _get_sgd_command_names()

def test_cmd_fixtures_present():
    assert "strategy-governance-dashboard-fixtures" in _get_sgd_command_names()

def test_cmd_safety_audit_present():
    assert "strategy-governance-dashboard-safety-audit" in _get_sgd_command_names()


# ── Uniqueness ──────────────────────────────────────────────────────────────────

def test_sgd_command_names_unique():
    names = _get_sgd_command_names()
    assert len(names) == len(set(names))


# ── Group field ─────────────────────────────────────────────────────────────────

def test_all_sgd_commands_have_group():
    for cmd in _get_sgd_commands():
        assert cmd.group == "strategy_governance_dashboard", f"{cmd.name} has wrong group"


# ── introduced_in field ─────────────────────────────────────────────────────────

def test_all_sgd_commands_introduced_in_197():
    for cmd in _get_sgd_commands():
        assert cmd.introduced_in == "1.9.7", f"{cmd.name} has wrong introduced_in"


# ── safety_classification field ─────────────────────────────────────────────────

def test_all_sgd_commands_safety_research_only():
    for cmd in _get_sgd_commands():
        assert cmd.safety_classification == "RESEARCH_ONLY", f"{cmd.name} safety_classification not RESEARCH_ONLY"


# ── help text ───────────────────────────────────────────────────────────────────

def test_all_sgd_commands_have_help():
    for cmd in _get_sgd_commands():
        assert isinstance(cmd.help, str) and len(cmd.help) > 0, f"{cmd.name} missing help"

def test_all_sgd_commands_help_contains_research():
    for cmd in _get_sgd_commands():
        assert "[Research]" in cmd.help or "Research" in cmd.help, f"{cmd.name} help missing Research"

def test_all_sgd_commands_help_no_forbidden_words():
    forbidden = {"BUY", "SELL", "ORDER", "EXECUTE", "BROKER", "REAL_TRADE", "LIVE_TRADE"}
    for cmd in _get_sgd_commands():
        for word in forbidden:
            assert word not in cmd.help.upper(), f"{cmd.name} help contains forbidden word {word}"


# ── handler_name field ──────────────────────────────────────────────────────────

def test_all_sgd_commands_have_handler_name():
    for cmd in _get_sgd_commands():
        assert isinstance(cmd.handler_name, str) and len(cmd.handler_name) > 0, f"{cmd.name} missing handler_name"

def test_all_sgd_handler_names_start_with_cmd():
    for cmd in _get_sgd_commands():
        assert cmd.handler_name.startswith("cmd_"), f"{cmd.name} handler_name does not start with cmd_"

def test_all_sgd_handler_names_contain_governance_dashboard():
    for cmd in _get_sgd_commands():
        assert "governance_dashboard" in cmd.handler_name, f"{cmd.name} handler_name missing 'governance_dashboard'"


# ── No forbidden action words in command names ─────────────────────────────────

def test_sgd_command_names_no_buy():
    assert all("buy" not in n.lower() for n in _get_sgd_command_names())

def test_sgd_command_names_no_sell():
    assert all("sell" not in n.lower() for n in _get_sgd_command_names())

def test_sgd_command_names_no_order():
    assert all("order" not in n.lower() for n in _get_sgd_command_names())

def test_sgd_command_names_no_broker():
    assert all("broker" not in n.lower() for n in _get_sgd_command_names())


# ── Specific command detail checks ─────────────────────────────────────────────

def test_version_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-version"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_version"

def test_run_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-run"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_run"

def test_health_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-health"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_health"

def test_gate_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-gate"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_gate"

def test_safety_audit_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-safety-audit"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_safety_audit"

def test_export_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-export"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_export"

def test_report_cmd_handler():
    cmds = {c.name: c for c in _get_sgd_commands()}
    cmd = cmds["strategy-governance-dashboard-report"]
    assert cmd.handler_name == "cmd_strategy_governance_dashboard_report"
