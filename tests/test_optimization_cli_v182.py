"""
tests/test_optimization_cli_v182.py
Tests for optimization CLI commands v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from cli.command_registry import (
    get_formal_command_names, get_commands_by_group, get_all_commands,
)


_OPTIMIZATION_COMMAND_NAMES = [
    "optimization-version",
    "optimization-run",
    "optimization-config",
    "optimization-grid",
    "optimization-parameter-set",
    "optimization-ranking",
    "optimization-walk-forward",
    "optimization-stability",
    "optimization-sensitivity",
    "optimization-overfitting-risk",
    "optimization-dashboard",
    "optimization-report",
    "optimization-scenarios",
    "optimization-fixtures",
    "optimization-health",
    "optimization-gate",
    "optimization-safety-audit",
]


def test_optimization_group_count_17():
    cmds = get_commands_by_group("optimization")
    assert len(cmds) == 17


def test_optimization_commands_in_formal_names():
    formal = get_formal_command_names()
    for name in _OPTIMIZATION_COMMAND_NAMES:
        assert name in formal, f"{name} not in formal command names"


@pytest.mark.parametrize("cmd_name", _OPTIMIZATION_COMMAND_NAMES)
def test_command_exists(cmd_name):
    formal = get_formal_command_names()
    assert cmd_name in formal


@pytest.mark.parametrize("cmd_name", _OPTIMIZATION_COMMAND_NAMES)
def test_command_in_group(cmd_name):
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert cmd_name in names


def test_all_optimization_research_only():
    cmds = get_commands_by_group("optimization")
    for cmd in cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY"


def test_all_optimization_introduced_182():
    cmds = get_commands_by_group("optimization")
    for cmd in cmds:
        assert cmd.introduced_in == "1.8.2"


def test_all_optimization_group_name():
    cmds = get_commands_by_group("optimization")
    for cmd in cmds:
        assert cmd.group == "optimization"


def test_all_optimization_research_flag():
    cmds = get_commands_by_group("optimization")
    for cmd in cmds:
        assert cmd.research_only is True


def test_optimization_version_cmd():
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert "optimization-version" in names


def test_optimization_run_cmd():
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert "optimization-run" in names


def test_optimization_walk_forward_cmd():
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert "optimization-walk-forward" in names


def test_optimization_health_cmd():
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert "optimization-health" in names


def test_optimization_gate_cmd():
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert "optimization-gate" in names


def test_optimization_safety_audit_cmd():
    cmds = get_commands_by_group("optimization")
    names = [c.name for c in cmds]
    assert "optimization-safety-audit" in names
