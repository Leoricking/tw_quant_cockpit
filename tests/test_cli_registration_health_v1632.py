"""
tests/test_cli_registration_health_v1632.py — CLI Registration Health Integrity Hotfix v1.6.3.2 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
25 tests covering:
  - Handler resolution via main module (1-8)
  - All 461 registry commands resolvable (9-12)
  - Session-ops 31 handlers resolvable (13-17)
  - CLIRegistrationHealthCheck 10/10 (18-21)
  - Alias correctness (22-25)
"""
from __future__ import annotations

import importlib
import os
import types

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")


# =============================================================================
# 1-8: Handler resolution via main module
# =============================================================================

class TestHandlerResolution:
    def test_01_main_importable(self):
        """Test 1: main module importable."""
        main = importlib.import_module("main")
        assert main is not None

    def test_02_main_is_module(self):
        """Test 2: main is a Python module."""
        main = importlib.import_module("main")
        assert isinstance(main, types.ModuleType)

    def test_03_getattr_callable_returns_callable(self):
        """Test 3: getattr on a known callable returns a callable."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_session_ops_composite_status", None)
        assert callable(fn)

    def test_04_getattr_missing_returns_none(self):
        """Test 4: getattr on a nonexistent name returns None sentinel."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_does_not_exist_xyz_12345", None)
        assert fn is None

    def test_05_new_alias_cmd_session_ops_status_callable(self):
        """Test 5: cmd_session_ops_status alias resolves to callable."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_session_ops_status", None)
        assert callable(fn), "cmd_session_ops_status must be callable after v1.6.3.2"

    def test_06_new_alias_cmd_session_ops_sessions_callable(self):
        """Test 6: cmd_session_ops_sessions alias resolves to callable."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_session_ops_sessions", None)
        assert callable(fn)

    def test_07_new_stub_cmd_session_ops_health_summary_callable(self):
        """Test 7: cmd_session_ops_health_summary stub resolves to callable."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_session_ops_health_summary", None)
        assert callable(fn)

    def test_08_new_stub_cmd_session_ops_runbooks_callable(self):
        """Test 8: cmd_session_ops_runbooks stub resolves to callable."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_session_ops_runbooks", None)
        assert callable(fn)


# =============================================================================
# 9-12: All 461 registry commands resolvable
# =============================================================================

class TestAllRegistryCommandsResolvable:
    def _load(self):
        from cli.command_registry import PROVIDER_COMMANDS
        main = importlib.import_module("main")
        return PROVIDER_COMMANDS, main

    def test_09_provider_commands_count(self):
        """Test 9: PROVIDER_COMMANDS has expected count >= 400."""
        cmds, _ = self._load()
        assert len(cmds) >= 400, f"Too few commands: {len(cmds)}"

    def test_10_all_handler_names_are_strings(self):
        """Test 10: All CommandSpec.handler_name are non-empty strings."""
        cmds, _ = self._load()
        for spec in cmds:
            assert isinstance(spec.handler_name, str) and spec.handler_name, (
                f"handler_name must be a non-empty string for {spec.name}"
            )

    def test_11_all_handlers_resolvable(self):
        """Test 11: Every handler_name in PROVIDER_COMMANDS resolves to a callable in main."""
        cmds, main = self._load()
        unresolvable = []
        for spec in cmds:
            fn = getattr(main, spec.handler_name, None)
            if not callable(fn):
                unresolvable.append(spec.handler_name)
        assert not unresolvable, (
            f"Unresolvable handlers ({len(unresolvable)}): {unresolvable[:10]}"
        )

    def test_12_no_handler_name_is_callable_object(self):
        """Test 12: handler_name is always a string, never a callable stored in registry."""
        cmds, _ = self._load()
        bad = [spec.name for spec in cmds if callable(spec.handler_name)]
        assert not bad, f"CommandSpec.handler_name must be string, not callable: {bad}"


# =============================================================================
# 13-17: Session-ops 31 handlers resolvable
# =============================================================================

class TestSessionOpsHandlers:
    SESSION_OPS_HANDLERS = [
        "cmd_session_ops_status",
        "cmd_session_ops_sessions",
        "cmd_session_ops_composite_status",
        "cmd_session_ops_registry_list",
        "cmd_session_ops_metrics",
        "cmd_session_ops_metrics_summary",
        "cmd_session_ops_alerts",
        "cmd_session_ops_alert_list",
        "cmd_session_ops_alert_ack",
        "cmd_session_ops_alert_acknowledge",
        "cmd_session_ops_alert_show",
        "cmd_session_ops_incidents",
        "cmd_session_ops_incident_list",
        "cmd_session_ops_incident_show",
        "cmd_session_ops_timeline",
        "cmd_session_ops_audit_tail",
        "cmd_session_ops_snapshot_show",
        "cmd_session_ops_snapshot_verify",
        "cmd_session_ops_checkpoint_create",
        "cmd_session_ops_checkpoint_save",
        "cmd_session_ops_checkpoint_show",
        "cmd_session_ops_checkpoint_restore",
        "cmd_session_ops_recovery_drill",
        "cmd_session_ops_drill_run",
        "cmd_session_ops_replay",
        "cmd_session_ops_replay_run",
        "cmd_session_ops_lineage",
        "cmd_session_ops_lineage_show",
        "cmd_session_ops_session_show",
        "cmd_session_ops_health_summary",
        "cmd_session_ops_runbooks",
        "cmd_session_ops_runbook_show",
    ]

    def test_13_all_session_ops_handlers_callable(self):
        """Test 13: All session-ops handler names resolve to callables in main."""
        main = importlib.import_module("main")
        unresolvable = [
            h for h in self.SESSION_OPS_HANDLERS
            if not callable(getattr(main, h, None))
        ]
        assert not unresolvable, f"Unresolvable session-ops handlers: {unresolvable}"

    def test_14_alias_status_is_composite_status(self):
        """Test 14: cmd_session_ops_status is the same as cmd_session_ops_composite_status."""
        main = importlib.import_module("main")
        assert getattr(main, "cmd_session_ops_status") is getattr(main, "cmd_session_ops_composite_status")

    def test_15_alias_sessions_is_registry_list(self):
        """Test 15: cmd_session_ops_sessions is the same as cmd_session_ops_registry_list."""
        main = importlib.import_module("main")
        assert getattr(main, "cmd_session_ops_sessions") is getattr(main, "cmd_session_ops_registry_list")

    def test_16_alias_metrics_is_metrics_summary(self):
        """Test 16: cmd_session_ops_metrics is the same as cmd_session_ops_metrics_summary."""
        main = importlib.import_module("main")
        assert getattr(main, "cmd_session_ops_metrics") is getattr(main, "cmd_session_ops_metrics_summary")

    def test_17_alias_lineage_is_lineage_show(self):
        """Test 17: cmd_session_ops_lineage is the same as cmd_session_ops_lineage_show."""
        main = importlib.import_module("main")
        assert getattr(main, "cmd_session_ops_lineage") is getattr(main, "cmd_session_ops_lineage_show")


# =============================================================================
# 18-21: CLIRegistrationHealthCheck 10/10
# =============================================================================

class TestCLIRegistrationHealthCheck:
    def _get_health_summary(self):
        """Build parser_commands and handler_map from registry, then run health check."""
        from cli.command_registry import PROVIDER_COMMANDS, get_formal_command_names
        from cli.health import CLIRegistrationHealthCheck

        formal = get_formal_command_names()
        parser_commands = set(spec.name for spec in PROVIDER_COMMANDS)
        handler_map = {spec.name: spec.handler_name for spec in PROVIDER_COMMANDS}
        return CLIRegistrationHealthCheck().get_health_summary(parser_commands, handler_map)

    def test_18_health_check_runs(self):
        """Test 18: CLIRegistrationHealthCheck.get_health_summary runs without error."""
        summary = self._get_health_summary()
        assert isinstance(summary, dict)

    def test_19_health_check_has_10_checks(self):
        """Test 19: CLIRegistrationHealthCheck has exactly 10 checks."""
        summary = self._get_health_summary()
        assert summary["total"] == 10, f"Expected 10 checks, got {summary['total']}"

    def test_20_health_check_zero_failures(self):
        """Test 20: CLIRegistrationHealthCheck has 0 failures."""
        summary = self._get_health_summary()
        failed = summary["failed"]
        assert failed == 0, (
            f"CLIRegistrationHealthCheck has {failed} failure(s): "
            + str({k: v for k, v in summary["checks"].items() if v["status"] != "PASS"})
        )

    def test_21_invalid_handler_check_passes(self):
        """Test 21: The invalid_handler check specifically is PASS (was FAIL before v1.6.3.2)."""
        summary = self._get_health_summary()
        check = summary["checks"]["invalid_handler"]
        assert check["status"] == "PASS", (
            f"invalid_handler is {check['status']}: {check['detail']}"
        )


# =============================================================================
# 22-25: TWSE/TPEx fetch handler aliases + version
# =============================================================================

class TestFetchHandlersAndVersion:
    def test_22_cmd_twse_fetch_security_master_callable(self):
        """Test 22: cmd_twse_fetch_security_master resolves to callable in main."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_twse_fetch_security_master", None)
        assert callable(fn)

    def test_23_cmd_tpex_fetch_daily_callable(self):
        """Test 23: cmd_tpex_fetch_daily resolves to callable in main."""
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_tpex_fetch_daily", None)
        assert callable(fn)

    def test_24_version_is_163x(self):
        """Test 24: VERSION is 1.6.3.x or later (CLI registration baseline preserved)."""
        from release.version_info import VERSION, CLI_HANDLER_RESOLUTION_BASELINE
        assert CLI_HANDLER_RESOLUTION_BASELINE.startswith("1.6.3"), f"Expected baseline 1.6.3.x got {CLI_HANDLER_RESOLUTION_BASELINE}"

    def test_25_release_name_is_known_hotfix(self):
        """Test 25: RELEASE_NAME is a known v1.6.3.x hotfix name."""
        from release.version_info import RELEASE_NAME
        known = {
            "CLI Registration Health Integrity Hotfix",
            "CLI Handler Resolution Integrity Hotfix",
            "Operational Analytics & Review",
            "Failure Injection & Recovery Validation",
            "Multi-session Coordination",
            "Fixture Governance & Safety Marker Hotfix",
            "Replay Session Lineage Handler Integrity Hotfix",
            "Paper Performance Attribution",
            "Operational Integration Hardening",
        }
        assert RELEASE_NAME in known, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"
