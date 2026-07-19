"""
tests/test_paper_cockpit_cli_v200.py
v2.0.0 Paper Cockpit — CLI Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from cli.command_registry import PROVIDER_COMMANDS, get_commands_by_group, get_command

_COCKPIT_COMMANDS = [
    "paper-cockpit-version",
    "paper-cockpit-run",
    "paper-cockpit-watchlist",
    "paper-cockpit-score",
    "paper-cockpit-abc-check",
    "paper-cockpit-risk-check",
    "paper-cockpit-sizing-check",
    "paper-cockpit-no-entry",
    "paper-cockpit-decision-ticket",
    "paper-cockpit-dashboard",
    "paper-cockpit-report",
    "paper-cockpit-export",
    "paper-cockpit-health",
    "paper-cockpit-gate",
    "paper-cockpit-scenarios",
    "paper-cockpit-fixtures",
    "paper-cockpit-safety-audit",
]

_ALL_NAMES = {c.name for c in PROVIDER_COMMANDS}


def test_total_cockpit_commands_17():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    assert len(cockpit_cmds) == 17

def test_all_cockpit_commands_registered():
    for cmd in _COCKPIT_COMMANDS:
        assert cmd in _ALL_NAMES, f"Command '{cmd}' not registered"

def test_paper_cockpit_version_registered():
    assert "paper-cockpit-version" in _ALL_NAMES

def test_paper_cockpit_run_registered():
    assert "paper-cockpit-run" in _ALL_NAMES

def test_paper_cockpit_watchlist_registered():
    assert "paper-cockpit-watchlist" in _ALL_NAMES

def test_paper_cockpit_score_registered():
    assert "paper-cockpit-score" in _ALL_NAMES

def test_paper_cockpit_abc_check_registered():
    assert "paper-cockpit-abc-check" in _ALL_NAMES

def test_paper_cockpit_risk_check_registered():
    assert "paper-cockpit-risk-check" in _ALL_NAMES

def test_paper_cockpit_sizing_check_registered():
    assert "paper-cockpit-sizing-check" in _ALL_NAMES

def test_paper_cockpit_no_entry_registered():
    assert "paper-cockpit-no-entry" in _ALL_NAMES

def test_paper_cockpit_decision_ticket_registered():
    assert "paper-cockpit-decision-ticket" in _ALL_NAMES

def test_paper_cockpit_dashboard_registered():
    assert "paper-cockpit-dashboard" in _ALL_NAMES

def test_paper_cockpit_report_registered():
    assert "paper-cockpit-report" in _ALL_NAMES

def test_paper_cockpit_export_registered():
    assert "paper-cockpit-export" in _ALL_NAMES

def test_paper_cockpit_health_registered():
    assert "paper-cockpit-health" in _ALL_NAMES

def test_paper_cockpit_gate_registered():
    assert "paper-cockpit-gate" in _ALL_NAMES

def test_paper_cockpit_scenarios_registered():
    assert "paper-cockpit-scenarios" in _ALL_NAMES

def test_paper_cockpit_fixtures_registered():
    assert "paper-cockpit-fixtures" in _ALL_NAMES

def test_paper_cockpit_safety_audit_registered():
    assert "paper-cockpit-safety-audit" in _ALL_NAMES

def test_all_cockpit_commands_in_paper_cockpit_group():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    cockpit_names = {c.name for c in cockpit_cmds}
    for cmd in _COCKPIT_COMMANDS:
        assert cmd in cockpit_names, f"'{cmd}' not in paper_cockpit group"

def test_all_cockpit_commands_introduced_in_200():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    for cmd in cockpit_cmds:
        assert cmd.introduced_in == "2.0.0", f"'{cmd.name}' introduced_in should be 2.0.0"

def test_all_cockpit_commands_safety_research_only():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    for cmd in cockpit_cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY", f"'{cmd.name}' safety should be RESEARCH_ONLY"

def test_get_command_paper_cockpit_version():
    cmd = get_command("paper-cockpit-version")
    assert cmd is not None
    assert cmd.group == "paper_cockpit"

def test_get_command_paper_cockpit_run():
    cmd = get_command("paper-cockpit-run")
    assert cmd is not None
    assert cmd.handler_name == "cmd_paper_cockpit_run"

def test_get_command_paper_cockpit_health():
    cmd = get_command("paper-cockpit-health")
    assert cmd is not None
    assert cmd.introduced_in == "2.0.0"

def test_get_command_paper_cockpit_gate():
    cmd = get_command("paper-cockpit-gate")
    assert cmd is not None
    assert cmd.safety_classification == "RESEARCH_ONLY"

def test_cockpit_commands_all_have_handler_name():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    for cmd in cockpit_cmds:
        assert cmd.handler_name.startswith("cmd_paper_cockpit_"), f"Bad handler name: {cmd.handler_name}"

def test_no_duplicate_cockpit_commands():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    names = [c.name for c in cockpit_cmds]
    assert len(names) == len(set(names))

def test_cockpit_commands_have_research_in_help():
    cockpit_cmds = get_commands_by_group("paper_cockpit")
    for cmd in cockpit_cmds:
        assert "[Research]" in cmd.help, f"'{cmd.name}' help should contain [Research]"
