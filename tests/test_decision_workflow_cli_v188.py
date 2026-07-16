"""
tests/test_decision_workflow_cli_v188.py
Tests for CLI command_registry v1.8.8 — Paper Decision Workflow Runner.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import (
    get_all_commands, get_commands_by_group, CommandSpec,
)


_DW_COMMANDS = get_commands_by_group("decision_workflow")
_DW_NAMES = {c.name for c in _DW_COMMANDS}


def test_decision_workflow_group_exists():
    assert len(_DW_COMMANDS) >= 21


def test_decision_workflow_count_is_21():
    assert len(_DW_COMMANDS) == 21


def test_decision_workflow_version_command_exists():
    assert "decision-workflow-version" in _DW_NAMES


def test_decision_workflow_run_command_exists():
    assert "decision-workflow-run" in _DW_NAMES


def test_decision_workflow_config_command_exists():
    assert "decision-workflow-config" in _DW_NAMES


def test_decision_workflow_daily_command_exists():
    assert "decision-workflow-daily" in _DW_NAMES


def test_decision_workflow_weekly_command_exists():
    assert "decision-workflow-weekly" in _DW_NAMES


def test_decision_workflow_pre_market_command_exists():
    assert "decision-workflow-pre-market" in _DW_NAMES


def test_decision_workflow_post_market_command_exists():
    assert "decision-workflow-post-market" in _DW_NAMES


def test_decision_workflow_watchlist_command_exists():
    assert "decision-workflow-watchlist" in _DW_NAMES


def test_decision_workflow_candidates_command_exists():
    assert "decision-workflow-candidates" in _DW_NAMES


def test_decision_workflow_risk_command_exists():
    assert "decision-workflow-risk" in _DW_NAMES


def test_decision_workflow_portfolio_command_exists():
    assert "decision-workflow-portfolio" in _DW_NAMES


def test_decision_workflow_report_command_exists():
    assert "decision-workflow-report" in _DW_NAMES


def test_decision_workflow_evidence_command_exists():
    assert "decision-workflow-evidence" in _DW_NAMES


def test_decision_workflow_audit_command_exists():
    assert "decision-workflow-audit" in _DW_NAMES


def test_decision_workflow_dashboard_command_exists():
    assert "decision-workflow-dashboard" in _DW_NAMES


def test_decision_workflow_export_command_exists():
    assert "decision-workflow-export" in _DW_NAMES


def test_decision_workflow_scenarios_command_exists():
    assert "decision-workflow-scenarios" in _DW_NAMES


def test_decision_workflow_fixtures_command_exists():
    assert "decision-workflow-fixtures" in _DW_NAMES


def test_decision_workflow_health_command_exists():
    assert "decision-workflow-health" in _DW_NAMES


def test_decision_workflow_gate_command_exists():
    assert "decision-workflow-gate" in _DW_NAMES


def test_decision_workflow_safety_audit_command_exists():
    assert "decision-workflow-safety-audit" in _DW_NAMES


def test_all_commands_research_only():
    for c in _DW_COMMANDS:
        assert c.research_only is True


def test_all_commands_safety_classification():
    for c in _DW_COMMANDS:
        assert c.safety_classification == "RESEARCH_ONLY"


def test_all_commands_introduced_in_188():
    for c in _DW_COMMANDS:
        assert c.introduced_in == "1.8.8"


def test_all_commands_group_decision_workflow():
    for c in _DW_COMMANDS:
        assert c.group == "decision_workflow"


def test_all_commands_have_handler_name():
    for c in _DW_COMMANDS:
        assert c.handler_name.startswith("cmd_decision_workflow_")


def test_all_commands_have_help_text():
    for c in _DW_COMMANDS:
        assert len(c.help) > 0
        assert "1.8.8" in c.help


def test_version_command_handler():
    cmds = {c.name: c for c in _DW_COMMANDS}
    assert cmds["decision-workflow-version"].handler_name == "cmd_decision_workflow_version"


def test_run_command_handler():
    cmds = {c.name: c for c in _DW_COMMANDS}
    assert cmds["decision-workflow-run"].handler_name == "cmd_decision_workflow_run"


def test_all_names_unique():
    names = [c.name for c in _DW_COMMANDS]
    assert len(names) == len(set(names))


def test_all_commands_in_all_commands_registry():
    all_names = {c.name for c in get_all_commands()}
    for c in _DW_COMMANDS:
        assert c.name in all_names
