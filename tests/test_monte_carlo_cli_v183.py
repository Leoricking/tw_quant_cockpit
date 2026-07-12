"""
tests/test_monte_carlo_cli_v183.py
Tests for Monte Carlo CLI commands in command registry v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from cli.command_registry import (
    get_formal_command_names,
    get_commands_by_group,
    get_command,
)

_MC_COMMAND_NAMES = [
    "monte-carlo-version",
    "monte-carlo-run",
    "monte-carlo-config",
    "monte-carlo-trial",
    "monte-carlo-bootstrap",
    "monte-carlo-risk-of-ruin",
    "monte-carlo-drawdown-distribution",
    "monte-carlo-return-distribution",
    "monte-carlo-sequence-risk",
    "monte-carlo-tail-risk",
    "monte-carlo-slippage-shock",
    "monte-carlo-cost-shock",
    "monte-carlo-robustness-probability",
    "monte-carlo-dashboard",
    "monte-carlo-report",
    "monte-carlo-scenarios",
    "monte-carlo-fixtures",
    "monte-carlo-health",
    "monte-carlo-gate",
    "monte-carlo-safety-audit",
]


# ---------------------------------------------------------------------------
# Group membership
# ---------------------------------------------------------------------------

def test_get_commands_by_group_monte_carlo_returns_list():
    result = get_commands_by_group("monte_carlo")
    assert isinstance(result, list)


def test_get_commands_by_group_monte_carlo_count_ge_18():
    assert len(get_commands_by_group("monte_carlo")) >= 18


# ---------------------------------------------------------------------------
# Each command present in formal names (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cmd_name", _MC_COMMAND_NAMES)
def test_command_in_formal_names(cmd_name):
    assert cmd_name in get_formal_command_names(), f"{cmd_name} not in formal command names"


@pytest.mark.parametrize("cmd_name", _MC_COMMAND_NAMES)
def test_command_in_monte_carlo_group(cmd_name):
    group_names = [c.name for c in get_commands_by_group("monte_carlo")]
    assert cmd_name in group_names, f"{cmd_name} not in monte_carlo group"


# ---------------------------------------------------------------------------
# Individual presence checks (non-parametrized, per spec)
# ---------------------------------------------------------------------------

def test_monte_carlo_version_in_formal_names():
    assert "monte-carlo-version" in get_formal_command_names()


def test_monte_carlo_run_in_formal_names():
    assert "monte-carlo-run" in get_formal_command_names()


def test_monte_carlo_config_in_formal_names():
    assert "monte-carlo-config" in get_formal_command_names()


def test_monte_carlo_trial_in_formal_names():
    assert "monte-carlo-trial" in get_formal_command_names()


def test_monte_carlo_bootstrap_in_formal_names():
    assert "monte-carlo-bootstrap" in get_formal_command_names()


def test_monte_carlo_risk_of_ruin_in_formal_names():
    assert "monte-carlo-risk-of-ruin" in get_formal_command_names()


def test_monte_carlo_drawdown_distribution_in_formal_names():
    assert "monte-carlo-drawdown-distribution" in get_formal_command_names()


def test_monte_carlo_return_distribution_in_formal_names():
    assert "monte-carlo-return-distribution" in get_formal_command_names()


def test_monte_carlo_sequence_risk_in_formal_names():
    assert "monte-carlo-sequence-risk" in get_formal_command_names()


def test_monte_carlo_tail_risk_in_formal_names():
    assert "monte-carlo-tail-risk" in get_formal_command_names()


def test_monte_carlo_slippage_shock_in_formal_names():
    assert "monte-carlo-slippage-shock" in get_formal_command_names()


def test_monte_carlo_cost_shock_in_formal_names():
    assert "monte-carlo-cost-shock" in get_formal_command_names()


def test_monte_carlo_robustness_probability_in_formal_names():
    assert "monte-carlo-robustness-probability" in get_formal_command_names()


def test_monte_carlo_dashboard_in_formal_names():
    assert "monte-carlo-dashboard" in get_formal_command_names()


def test_monte_carlo_report_in_formal_names():
    assert "monte-carlo-report" in get_formal_command_names()


def test_monte_carlo_scenarios_in_formal_names():
    assert "monte-carlo-scenarios" in get_formal_command_names()


def test_monte_carlo_fixtures_in_formal_names():
    assert "monte-carlo-fixtures" in get_formal_command_names()


def test_monte_carlo_health_in_formal_names():
    assert "monte-carlo-health" in get_formal_command_names()


def test_monte_carlo_gate_in_formal_names():
    assert "monte-carlo-gate" in get_formal_command_names()


def test_monte_carlo_safety_audit_in_formal_names():
    assert "monte-carlo-safety-audit" in get_formal_command_names()


# ---------------------------------------------------------------------------
# Safety classification and introduced_in
# ---------------------------------------------------------------------------

def test_all_monte_carlo_commands_research_only():
    cmds = get_commands_by_group("monte_carlo")
    for c in cmds:
        assert c.safety_classification == "RESEARCH_ONLY", \
            f"{c.name} has unexpected safety_classification: {c.safety_classification}"


def test_all_monte_carlo_commands_introduced_in_183():
    cmds = get_commands_by_group("monte_carlo")
    for c in cmds:
        assert c.introduced_in == "1.8.3", \
            f"{c.name} has unexpected introduced_in: {c.introduced_in}"


# ---------------------------------------------------------------------------
# get_command() spot-checks
# ---------------------------------------------------------------------------

def test_get_command_monte_carlo_version_not_none():
    assert get_command("monte-carlo-version") is not None


def test_get_command_monte_carlo_version_group():
    cmd = get_command("monte-carlo-version")
    assert cmd.group == "monte_carlo"
