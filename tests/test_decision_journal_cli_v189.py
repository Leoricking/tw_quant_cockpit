"""
tests/test_decision_journal_cli_v189.py
Tests for v1.8.9 CLI commands — Paper Decision Journal & Review Loop.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import (
    get_all_commands, get_command, get_commands_by_group, get_formal_command_names,
)

_DJ_V189_NAMES = [
    "decision-journal-version",
    "decision-journal-create",
    "decision-journal-add-entry",
    "decision-journal-review",
    "decision-journal-daily-review",
    "decision-journal-weekly-review",
    "decision-journal-monthly-review",
    "decision-journal-mistakes",
    "decision-journal-quality",
    "decision-journal-dashboard",
    "decision-journal-export",
    "decision-journal-evidence",
    "decision-journal-audit",
    "decision-journal-health",
    "decision-journal-gate",
    "decision-journal-scenarios",
    "decision-journal-fixtures",
    "decision-journal-safety-audit",
]


def test_decision_journal_commands_registered():
    names = get_formal_command_names()
    for cmd in _DJ_V189_NAMES:
        assert cmd in names, f"Command not registered: {cmd}"


def test_decision_journal_command_count():
    group_cmds = get_commands_by_group("decision_journal")
    dj189 = [c for c in group_cmds if c.introduced_in == "1.8.9"]
    assert len(dj189) == 18


def test_decision_journal_version_command_exists():
    assert get_command("decision-journal-version") is not None


def test_decision_journal_create_command_exists():
    assert get_command("decision-journal-create") is not None


def test_decision_journal_add_entry_command_exists():
    assert get_command("decision-journal-add-entry") is not None


def test_decision_journal_review_command_exists():
    assert get_command("decision-journal-review") is not None


def test_decision_journal_daily_review_command_exists():
    assert get_command("decision-journal-daily-review") is not None


def test_decision_journal_weekly_review_command_exists():
    assert get_command("decision-journal-weekly-review") is not None


def test_decision_journal_monthly_review_command_exists():
    assert get_command("decision-journal-monthly-review") is not None


def test_decision_journal_mistakes_command_exists():
    assert get_command("decision-journal-mistakes") is not None


def test_decision_journal_quality_command_exists():
    assert get_command("decision-journal-quality") is not None


def test_decision_journal_dashboard_command_exists():
    assert get_command("decision-journal-dashboard") is not None


def test_decision_journal_export_command_exists():
    assert get_command("decision-journal-export") is not None


def test_decision_journal_evidence_command_exists():
    assert get_command("decision-journal-evidence") is not None


def test_decision_journal_audit_command_exists():
    assert get_command("decision-journal-audit") is not None


def test_decision_journal_health_command_exists():
    assert get_command("decision-journal-health") is not None


def test_decision_journal_gate_command_exists():
    assert get_command("decision-journal-gate") is not None


def test_decision_journal_scenarios_command_exists():
    assert get_command("decision-journal-scenarios") is not None


def test_decision_journal_fixtures_command_exists():
    assert get_command("decision-journal-fixtures") is not None


def test_decision_journal_safety_audit_command_exists():
    assert get_command("decision-journal-safety-audit") is not None


def test_all_dj189_commands_group():
    for name in _DJ_V189_NAMES:
        cmd = get_command(name)
        assert cmd is not None
        assert cmd.group == "decision_journal"


def test_all_dj189_commands_introduced_in_189():
    for name in _DJ_V189_NAMES:
        cmd = get_command(name)
        assert cmd.introduced_in == "1.8.9"


def test_all_dj189_commands_safety_classification():
    for name in _DJ_V189_NAMES:
        cmd = get_command(name)
        assert cmd.safety_classification == "RESEARCH_ONLY"


def test_all_dj189_commands_have_help():
    for name in _DJ_V189_NAMES:
        cmd = get_command(name)
        assert cmd.help is not None and len(cmd.help) > 0


def test_all_dj189_commands_have_handler_name():
    for name in _DJ_V189_NAMES:
        cmd = get_command(name)
        assert cmd.handler_name.startswith("cmd_decision_journal_")


def test_dj189_commands_no_duplicates():
    names = [c.name for c in get_all_commands()]
    for name in _DJ_V189_NAMES:
        assert names.count(name) == 1, f"Duplicate command: {name}"


def test_dj189_version_command_help_contains_189():
    cmd = get_command("decision-journal-version")
    assert "1.8.9" in cmd.help


def test_dj189_health_command_help_contains_health():
    cmd = get_command("decision-journal-health")
    assert "health" in cmd.help.lower()


def test_dj189_gate_command_help_contains_gate():
    cmd = get_command("decision-journal-gate")
    assert "gate" in cmd.help.lower()


def test_total_dj189_commands_at_least_18():
    dj189 = [c for c in get_all_commands() if c.introduced_in == "1.8.9"]
    assert len(dj189) >= 18
