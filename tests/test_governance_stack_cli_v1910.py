"""
tests/test_governance_stack_cli_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit — CLI Tests
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
from cli.command_registry import get_command, get_all_commands, get_commands_by_group


_GS_COMMANDS = [
    "governance-stack-version",
    "governance-stack-audit",
    "governance-stack-summary",
    "governance-stack-cli-audit",
    "governance-stack-gui-audit",
    "governance-stack-health-audit",
    "governance-stack-gate-audit",
    "governance-stack-fixture-audit",
    "governance-stack-scenario-audit",
    "governance-stack-safety-audit",
    "governance-stack-compatibility",
    "governance-stack-report",
    "governance-stack-health",
    "governance-stack-gate",
]


def test_governance_stack_version_registered():
    assert get_command("governance-stack-version") is not None

def test_governance_stack_audit_registered():
    assert get_command("governance-stack-audit") is not None

def test_governance_stack_summary_registered():
    assert get_command("governance-stack-summary") is not None

def test_governance_stack_cli_audit_registered():
    assert get_command("governance-stack-cli-audit") is not None

def test_governance_stack_gui_audit_registered():
    assert get_command("governance-stack-gui-audit") is not None

def test_governance_stack_health_audit_registered():
    assert get_command("governance-stack-health-audit") is not None

def test_governance_stack_gate_audit_registered():
    assert get_command("governance-stack-gate-audit") is not None

def test_governance_stack_fixture_audit_registered():
    assert get_command("governance-stack-fixture-audit") is not None

def test_governance_stack_scenario_audit_registered():
    assert get_command("governance-stack-scenario-audit") is not None

def test_governance_stack_safety_audit_registered():
    assert get_command("governance-stack-safety-audit") is not None

def test_governance_stack_compatibility_registered():
    assert get_command("governance-stack-compatibility") is not None

def test_governance_stack_report_registered():
    assert get_command("governance-stack-report") is not None

def test_governance_stack_health_registered():
    assert get_command("governance-stack-health") is not None

def test_governance_stack_gate_registered():
    assert get_command("governance-stack-gate") is not None

def test_all_14_governance_stack_commands_registered():
    for cmd in _GS_COMMANDS:
        assert get_command(cmd) is not None, f"Missing command: {cmd}"

def test_governance_stack_group_has_14_commands():
    group_cmds = get_commands_by_group("governance_stack")
    assert len(group_cmds) == 14

def test_governance_stack_version_handler_name():
    spec = get_command("governance-stack-version")
    assert spec.handler_name == "cmd_governance_stack_version"

def test_governance_stack_audit_handler_name():
    spec = get_command("governance-stack-audit")
    assert spec.handler_name == "cmd_governance_stack_audit"

def test_governance_stack_health_handler_name():
    spec = get_command("governance-stack-health")
    assert spec.handler_name == "cmd_governance_stack_health"

def test_governance_stack_gate_handler_name():
    spec = get_command("governance-stack-gate")
    assert spec.handler_name == "cmd_governance_stack_gate"

def test_governance_stack_compatibility_handler_name():
    spec = get_command("governance-stack-compatibility")
    assert spec.handler_name == "cmd_governance_stack_compatibility"

def test_governance_stack_commands_introduced_in_1910():
    for cmd in _GS_COMMANDS:
        spec = get_command(cmd)
        assert spec.introduced_in == "1.9.10"

def test_governance_stack_commands_safety_research_only():
    for cmd in _GS_COMMANDS:
        spec = get_command(cmd)
        assert spec.safety_classification == "RESEARCH_ONLY"

def test_governance_stack_commands_group():
    for cmd in _GS_COMMANDS:
        spec = get_command(cmd)
        assert spec.group == "governance_stack"

def test_governance_stack_version_help_contains_research():
    spec = get_command("governance-stack-version")
    assert "[Research]" in spec.help or "Research" in spec.help

def test_all_commands_count_includes_1910():
    all_cmds = get_all_commands()
    gs_cmds = [c for c in all_cmds if c.group == "governance_stack"]
    assert len(gs_cmds) == 14
