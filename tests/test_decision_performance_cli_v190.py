"""tests/test_decision_performance_cli_v190.py
Tests for decision performance CLI commands v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from cli.command_registry import (
    get_commands_by_group, get_command, get_formal_command_names,
)

dp_cmds = [c for c in get_commands_by_group("decision_performance") if c.introduced_in == "1.9.0"]


def test_dp_cmds_at_least_18():
    assert len(dp_cmds) >= 18


def test_dp_cmds_exactly_18():
    assert len(dp_cmds) == 18


def test_dp_cmds_all_group_decision_performance():
    assert all(c.group == "decision_performance" for c in dp_cmds)


def test_dp_cmds_all_introduced_in_190():
    assert all(c.introduced_in == "1.9.0" for c in dp_cmds)


def test_dp_cmds_all_safety_research_only():
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in dp_cmds)


def test_dp_cmds_all_names_start_with_decision_performance():
    assert all(c.name.startswith("decision-performance-") for c in dp_cmds)


def test_dp_cmds_all_handler_names_start_with_cmd_decision_performance():
    assert all(c.handler_name.startswith("cmd_decision_performance_") for c in dp_cmds)


def test_dp_cmd_version_present():
    assert "decision-performance-version" in [c.name for c in dp_cmds]


def test_dp_cmd_review_present():
    assert "decision-performance-review" in [c.name for c in dp_cmds]


def test_dp_cmd_health_present():
    assert "decision-performance-health" in [c.name for c in dp_cmds]


def test_dp_cmd_safety_audit_present():
    assert "decision-performance-safety-audit" in [c.name for c in dp_cmds]


def test_dp_cmd_dashboard_present():
    assert "decision-performance-dashboard" in [c.name for c in dp_cmds]


def test_dp_cmd_export_present():
    assert "decision-performance-export" in [c.name for c in dp_cmds]


def test_dp_cmd_scenarios_present():
    assert "decision-performance-scenarios" in [c.name for c in dp_cmds]


def test_dp_cmd_fixtures_present():
    assert "decision-performance-fixtures" in [c.name for c in dp_cmds]


def test_dp_cmd_improvement_present():
    assert "decision-performance-improvement" in [c.name for c in dp_cmds]


def test_dp_cmd_r_multiple_present():
    assert "decision-performance-r-multiple" in [c.name for c in dp_cmds]


def test_dp_cmd_drawdown_present():
    assert "decision-performance-drawdown" in [c.name for c in dp_cmds]


def test_dp_cmd_expectancy_present():
    assert "decision-performance-expectancy" in [c.name for c in dp_cmds]


def test_dp_cmd_win_rate_present():
    assert "decision-performance-win-rate" in [c.name for c in dp_cmds]


def test_dp_cmd_quality_present():
    assert "decision-performance-quality" in [c.name for c in dp_cmds]


def test_dp_cmd_setup_analytics_present():
    assert "decision-performance-setup-analytics" in [c.name for c in dp_cmds]


def test_dp_cmd_evidence_present():
    assert "decision-performance-evidence" in [c.name for c in dp_cmds]


def test_dp_cmd_audit_present():
    assert "decision-performance-audit" in [c.name for c in dp_cmds]


def test_dp_cmd_mistakes_present():
    assert "decision-performance-mistakes" in [c.name for c in dp_cmds]


def test_get_command_version_not_none():
    assert get_command("decision-performance-version") is not None


def test_get_command_version_introduced_in_190():
    assert get_command("decision-performance-version").introduced_in == "1.9.0"
