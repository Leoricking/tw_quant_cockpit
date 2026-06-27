"""
tests/test_failure_validation_cli_v165.py — CLI tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from cli.command_registry import get_all_commands, CommandSpec


# ---------------------------------------------------------------------------
# CLI registry helpers
# ---------------------------------------------------------------------------

def _get_all_commands_as_dict():
    commands = get_all_commands()
    return {c.name: c for c in commands}


FAILURE_COMMANDS = [
    "failure-health",
    "failure-gate",
    "failure-scenarios",
    "failure-scenario-show",
    "failure-inject",
    "failure-inject-status",
    "failure-revert",
    "failure-safety-check",
    "failure-baseline",
    "failure-baseline-verify",
    "failure-cascading",
    "failure-detection",
    "failure-alerts",
    "failure-incidents",
    "failure-containment",
    "failure-circuit-breaker",
    "failure-retry",
    "failure-scorecard",
    "failure-scorecard-summary",
    "failure-report",
    "failure-lineage",
    "failure-audit-tail",
    "failure-store-summary",
    "failure-fixtures-validate",
    "recovery-plan",
    "recovery-run",
    "recovery-state",
    "recovery-validate-transition",
    "recovery-rto-rpo",
    "recovery-data-reconcile",
    "recovery-replay",
    "recovery-post-validate",
    "recovery-rollback",
    "recovery-idempotency",
]


# ---------------------------------------------------------------------------
# Command registry structure
# ---------------------------------------------------------------------------

class TestCLIRegistryStructure:
    def test_get_all_commands_returns_list(self):
        commands = get_all_commands()
        assert isinstance(commands, list)

    def test_get_all_commands_non_empty(self):
        commands = get_all_commands()
        assert len(commands) > 0

    def test_all_commands_are_command_spec(self):
        commands = get_all_commands()
        for c in commands:
            assert isinstance(c, CommandSpec)


# ---------------------------------------------------------------------------
# Failure injection commands in registry
# ---------------------------------------------------------------------------

class TestFailureCommandsInRegistry:
    def test_failure_health_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-health" in cmds

    def test_failure_gate_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-gate" in cmds

    def test_failure_scenarios_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-scenarios" in cmds

    def test_failure_inject_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-inject" in cmds

    def test_failure_safety_check_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-safety-check" in cmds

    def test_failure_baseline_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-baseline" in cmds

    def test_failure_cascading_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-cascading" in cmds

    def test_failure_circuit_breaker_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-circuit-breaker" in cmds

    def test_failure_scorecard_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-scorecard" in cmds

    def test_failure_report_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "failure-report" in cmds

    def test_recovery_plan_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "recovery-plan" in cmds

    def test_recovery_run_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "recovery-run" in cmds

    def test_recovery_rto_rpo_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "recovery-rto-rpo" in cmds

    def test_recovery_replay_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "recovery-replay" in cmds

    def test_recovery_rollback_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "recovery-rollback" in cmds

    def test_recovery_idempotency_registered(self):
        cmds = _get_all_commands_as_dict()
        assert "recovery-idempotency" in cmds

    def test_all_34_failure_commands_registered(self):
        cmds = _get_all_commands_as_dict()
        missing = [name for name in FAILURE_COMMANDS if name not in cmds]
        assert missing == [], f"Missing CLI commands: {missing}"


# ---------------------------------------------------------------------------
# Command spec attributes
# ---------------------------------------------------------------------------

class TestFailureCommandSpecAttributes:
    def test_failure_health_has_help(self):
        cmds = _get_all_commands_as_dict()
        assert cmds["failure-health"].help

    def test_failure_gate_has_help(self):
        cmds = _get_all_commands_as_dict()
        assert cmds["failure-gate"].help

    def test_failure_health_group_is_failure_injection(self):
        cmds = _get_all_commands_as_dict()
        assert cmds["failure-health"].group == "failure_injection"

    def test_all_failure_commands_have_group(self):
        cmds = _get_all_commands_as_dict()
        for name in FAILURE_COMMANDS:
            if name in cmds:
                assert cmds[name].group is not None, f"Command {name} has no group"

    def test_all_failure_commands_have_help(self):
        cmds = _get_all_commands_as_dict()
        for name in FAILURE_COMMANDS:
            if name in cmds:
                assert cmds[name].help, f"Command {name} has no help text"

    def test_failure_commands_group_values(self):
        cmds = _get_all_commands_as_dict()
        for name in FAILURE_COMMANDS:
            if name in cmds:
                assert cmds[name].group in {"failure_injection", "recovery"}, (
                    f"Command {name} has unexpected group: {cmds[name].group}"
                )


# ---------------------------------------------------------------------------
# Runtime dispatch — handlers in main.py
# ---------------------------------------------------------------------------

class TestRuntimeDispatch:
    def test_cmd_failure_health_callable(self):
        from main import cmd_failure_health
        assert callable(cmd_failure_health)

    def test_cmd_failure_gate_callable(self):
        from main import cmd_failure_gate
        assert callable(cmd_failure_gate)

    def test_cmd_failure_scenarios_callable(self):
        from main import cmd_failure_scenarios
        assert callable(cmd_failure_scenarios)

    def test_cmd_failure_inject_callable(self):
        from main import cmd_failure_inject
        assert callable(cmd_failure_inject)

    def test_cmd_failure_safety_check_callable(self):
        from main import cmd_failure_safety_check
        assert callable(cmd_failure_safety_check)

    def test_cmd_failure_baseline_callable(self):
        from main import cmd_failure_baseline
        assert callable(cmd_failure_baseline)

    def test_cmd_failure_cascading_callable(self):
        from main import cmd_failure_cascading
        assert callable(cmd_failure_cascading)

    def test_cmd_failure_scorecard_callable(self):
        from main import cmd_failure_scorecard
        assert callable(cmd_failure_scorecard)

    def test_cmd_recovery_plan_callable(self):
        from main import cmd_recovery_plan
        assert callable(cmd_recovery_plan)

    def test_cmd_recovery_run_callable(self):
        from main import cmd_recovery_run
        assert callable(cmd_recovery_run)

    def test_cmd_recovery_rto_rpo_callable(self):
        from main import cmd_recovery_rto_rpo
        assert callable(cmd_recovery_rto_rpo)

    def test_cmd_recovery_replay_callable(self):
        from main import cmd_recovery_replay
        assert callable(cmd_recovery_replay)

    def test_cmd_recovery_rollback_callable(self):
        from main import cmd_recovery_rollback
        assert callable(cmd_recovery_rollback)

    def test_cmd_recovery_idempotency_callable(self):
        from main import cmd_recovery_idempotency
        assert callable(cmd_recovery_idempotency)
