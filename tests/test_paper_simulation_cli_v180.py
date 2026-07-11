"""tests/test_paper_simulation_cli_v180.py — v1.8.0 Paper Simulation CLI command tests"""
from __future__ import annotations
import pytest
from cli.command_registry import get_formal_command_names, get_command, PROVIDER_COMMANDS


# ---------------------------------------------------------------------------
# Presence of all 19 paper-simulation commands in the formal command names
# ---------------------------------------------------------------------------

def test_paper_simulation_version_registered() -> None:
    assert "paper-simulation-version" in get_formal_command_names()


def test_paper_simulation_run_registered() -> None:
    assert "paper-simulation-run" in get_formal_command_names()


def test_paper_simulation_config_registered() -> None:
    assert "paper-simulation-config" in get_formal_command_names()


def test_paper_simulation_scenario_registered() -> None:
    assert "paper-simulation-scenario" in get_formal_command_names()


def test_paper_simulation_metrics_registered() -> None:
    assert "paper-simulation-metrics" in get_formal_command_names()


def test_paper_simulation_equity_curve_registered() -> None:
    assert "paper-simulation-equity-curve" in get_formal_command_names()


def test_paper_simulation_drawdown_registered() -> None:
    assert "paper-simulation-drawdown" in get_formal_command_names()


def test_paper_simulation_risk_registered() -> None:
    assert "paper-simulation-risk" in get_formal_command_names()


def test_paper_simulation_regime_registered() -> None:
    assert "paper-simulation-regime" in get_formal_command_names()


def test_paper_simulation_theme_registered() -> None:
    assert "paper-simulation-theme" in get_formal_command_names()


def test_paper_simulation_abc_registered() -> None:
    assert "paper-simulation-abc" in get_formal_command_names()


def test_paper_simulation_mistake_impact_registered() -> None:
    assert "paper-simulation-mistake-impact" in get_formal_command_names()


def test_paper_simulation_dashboard_registered() -> None:
    assert "paper-simulation-dashboard" in get_formal_command_names()


def test_paper_simulation_report_registered() -> None:
    assert "paper-simulation-report" in get_formal_command_names()


def test_paper_simulation_scenarios_registered() -> None:
    assert "paper-simulation-scenarios" in get_formal_command_names()


def test_paper_simulation_fixtures_registered() -> None:
    assert "paper-simulation-fixtures" in get_formal_command_names()


def test_paper_simulation_health_registered() -> None:
    assert "paper-simulation-health" in get_formal_command_names()


def test_paper_simulation_gate_registered() -> None:
    assert "paper-simulation-gate" in get_formal_command_names()


def test_paper_simulation_safety_audit_registered() -> None:
    assert "paper-simulation-safety-audit" in get_formal_command_names()


# ---------------------------------------------------------------------------
# get_command() lookup and field values
# ---------------------------------------------------------------------------

def test_get_command_paper_simulation_version_not_none() -> None:
    assert get_command("paper-simulation-version") is not None


def test_get_command_paper_simulation_health_group() -> None:
    cmd = get_command("paper-simulation-health")
    assert cmd is not None
    assert cmd.group == "paper_simulation"


def test_get_command_paper_simulation_run_safety_classification() -> None:
    cmd = get_command("paper-simulation-run")
    assert cmd is not None
    assert cmd.safety_classification == "RESEARCH_ONLY"


def test_get_command_paper_simulation_gate_introduced_in() -> None:
    cmd = get_command("paper-simulation-gate")
    assert cmd is not None
    assert cmd.introduced_in == "1.8.0"


# ---------------------------------------------------------------------------
# Group count: exactly 19 paper_simulation commands in PROVIDER_COMMANDS
# ---------------------------------------------------------------------------

def test_paper_simulation_group_count_is_19() -> None:
    paper_sim_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_simulation"]
    assert len(paper_sim_cmds) == 19


# ---------------------------------------------------------------------------
# Safety invariant: every paper_simulation command must be RESEARCH_ONLY
# ---------------------------------------------------------------------------

def test_all_paper_simulation_commands_are_research_only() -> None:
    paper_sim_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_simulation"]
    non_research = [c.name for c in paper_sim_cmds if c.safety_classification != "RESEARCH_ONLY"]
    assert non_research == [], f"Non-RESEARCH_ONLY paper_simulation commands: {non_research}"
