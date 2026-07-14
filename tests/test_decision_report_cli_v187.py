"""
tests/test_decision_report_cli_v187.py
Tests for CLI command_registry v1.8.7 — Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import (
    get_all_commands, get_commands_by_group, CommandSpec,
)


_DR_COMMANDS = get_commands_by_group("decision_report")
_DR_NAMES = {c.name for c in _DR_COMMANDS}


def test_decision_report_group_exists():
    assert len(_DR_COMMANDS) >= 23


def test_decision_report_count_is_23():
    assert len(_DR_COMMANDS) == 23


def test_decision_report_version_command_exists():
    assert "decision-report-version" in _DR_NAMES


def test_decision_report_run_command_exists():
    assert "decision-report-run" in _DR_NAMES


def test_decision_report_config_command_exists():
    assert "decision-report-config" in _DR_NAMES


def test_decision_report_daily_command_exists():
    assert "decision-report-daily" in _DR_NAMES


def test_decision_report_weekly_command_exists():
    assert "decision-report-weekly" in _DR_NAMES


def test_decision_report_watchlist_command_exists():
    assert "decision-report-watchlist" in _DR_NAMES


def test_decision_report_blocked_command_exists():
    assert "decision-report-blocked" in _DR_NAMES


def test_decision_report_reduce_risk_command_exists():
    assert "decision-report-reduce-risk" in _DR_NAMES


def test_decision_report_paper_plan_command_exists():
    assert "decision-report-paper-plan" in _DR_NAMES


def test_decision_report_portfolio_command_exists():
    assert "decision-report-portfolio" in _DR_NAMES


def test_decision_report_monte_carlo_command_exists():
    assert "decision-report-monte-carlo" in _DR_NAMES


def test_decision_report_buy_points_command_exists():
    assert "decision-report-buy-points" in _DR_NAMES


def test_decision_report_evidence_command_exists():
    assert "decision-report-evidence" in _DR_NAMES


def test_decision_report_audit_trail_command_exists():
    assert "decision-report-audit-trail" in _DR_NAMES


def test_decision_report_export_json_command_exists():
    assert "decision-report-export-json" in _DR_NAMES


def test_decision_report_export_markdown_command_exists():
    assert "decision-report-export-markdown" in _DR_NAMES


def test_decision_report_export_rows_command_exists():
    assert "decision-report-export-rows" in _DR_NAMES


def test_decision_report_dashboard_command_exists():
    assert "decision-report-dashboard" in _DR_NAMES


def test_decision_report_scenarios_command_exists():
    assert "decision-report-scenarios" in _DR_NAMES


def test_decision_report_fixtures_command_exists():
    assert "decision-report-fixtures" in _DR_NAMES


def test_decision_report_health_command_exists():
    assert "decision-report-health" in _DR_NAMES


def test_decision_report_gate_command_exists():
    assert "decision-report-gate" in _DR_NAMES


def test_decision_report_safety_audit_command_exists():
    assert "decision-report-safety-audit" in _DR_NAMES


def test_all_dr_commands_research_only():
    for cmd in _DR_COMMANDS:
        assert cmd.safety_classification == "RESEARCH_ONLY", \
            f"Command {cmd.name} has wrong safety_classification: {cmd.safety_classification}"


def test_all_dr_commands_introduced_in_187():
    for cmd in _DR_COMMANDS:
        assert cmd.introduced_in == "1.8.7", \
            f"Command {cmd.name} has wrong introduced_in: {cmd.introduced_in}"


def test_all_dr_commands_in_decision_report_group():
    for cmd in _DR_COMMANDS:
        assert cmd.group == "decision_report", \
            f"Command {cmd.name} has wrong group: {cmd.group}"


def test_all_dr_commands_have_handler_name():
    for cmd in _DR_COMMANDS:
        assert cmd.handler_name.startswith("cmd_decision_report"), \
            f"Command {cmd.name} has unexpected handler: {cmd.handler_name}"


def test_all_dr_commands_have_help_text():
    for cmd in _DR_COMMANDS:
        assert len(cmd.help) > 0, f"Command {cmd.name} has no help text"


def test_all_dr_commands_have_research_in_help():
    for cmd in _DR_COMMANDS:
        assert "Research" in cmd.help, f"Command {cmd.name} help does not contain [Research]"


def test_get_all_commands_includes_dr_group():
    all_cmds = get_all_commands()
    dr_in_all = [c for c in all_cmds if c.group == "decision_report"]
    assert len(dr_in_all) == 23


def test_command_spec_is_correct_type():
    for cmd in _DR_COMMANDS:
        assert isinstance(cmd, CommandSpec)
