"""
tests/test_stable_rollup_cli_v169.py
Tests for CLI registration of stable rollup commands.
"""
import pytest
from cli.command_registry import get_all_commands, get_formal_command_names, get_commands_by_group


STABLE_ROLLUP_COMMANDS = [
    "stable-rollup-version",
    "stable-rollup-capabilities",
    "stable-rollup-releases",
    "stable-rollup-manifest",
    "stable-rollup-release",
    "stable-rollup-lineage",
    "stable-rollup-components",
    "stable-rollup-safety",
    "stable-rollup-compatibility",
    "stable-rollup-health",
    "stable-rollup-gates",
    "stable-rollup-cli",
    "stable-rollup-gui",
    "stable-rollup-fixtures",
    "stable-rollup-scenarios",
    "stable-rollup-contract",
    "stable-rollup-validate",
    "stable-rollup-reconcile",
    "stable-rollup-scorecard",
    "stable-rollup-regression",
    "stable-rollup-snapshot",
    "stable-rollup-report",
    "stable-rollup-query",
    "stable-rollup-migration-readiness",
    "stable-rollup-safety-audit",
    "stable-rollup-gate",
]


def test_stable_rollup_group_commands():
    cmds = get_commands_by_group("stable_rollup")
    assert len(cmds) >= 26


def test_all_stable_rollup_commands_registered():
    formal_names = get_formal_command_names()
    for cmd_name in STABLE_ROLLUP_COMMANDS:
        assert cmd_name in formal_names, f"Command {cmd_name!r} not registered"


def test_stable_rollup_version_registered():
    formal_names = get_formal_command_names()
    assert "stable-rollup-version" in formal_names


def test_stable_rollup_health_registered():
    formal_names = get_formal_command_names()
    assert "stable-rollup-health" in formal_names


def test_stable_rollup_gate_registered():
    formal_names = get_formal_command_names()
    assert "stable-rollup-gate" in formal_names


def test_stable_rollup_report_registered():
    formal_names = get_formal_command_names()
    assert "stable-rollup-report" in formal_names


def test_stable_rollup_migration_readiness_registered():
    formal_names = get_formal_command_names()
    assert "stable-rollup-migration-readiness" in formal_names


def test_stable_rollup_safety_audit_registered():
    formal_names = get_formal_command_names()
    assert "stable-rollup-safety-audit" in formal_names


def test_all_sr_commands_group_is_stable_rollup():
    cmds = get_commands_by_group("stable_rollup")
    for cmd in cmds:
        assert cmd.group == "stable_rollup"


def test_sr_commands_introduced_in_169():
    # Only check v1.6.9 stable rollup commands (names starting with "sr-"), not v1.7.9 ones
    cmds = get_commands_by_group("stable_rollup")
    sr_cmds = [c for c in cmds if c.name.startswith("sr-")]
    for cmd in sr_cmds:
        assert cmd.introduced_in == "1.6.9"


def test_sr_commands_research_only():
    cmds = get_commands_by_group("stable_rollup")
    for cmd in cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY"


def test_no_duplicate_commands():
    all_cmds = get_all_commands()
    names = [c.name for c in all_cmds]
    assert len(set(names)) == len(names)


def test_count_26_stable_rollup_commands():
    assert len(STABLE_ROLLUP_COMMANDS) == 26
