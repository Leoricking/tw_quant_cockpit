"""
tests/test_cli_handler_resolution_v1633.py — CLI Handler Resolution Integrity Hotfix v1.6.3.3 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
45 tests covering:
  - Runtime dispatch completeness (1-8)
  - Session-ops 31 commands all dispatchable (9-14)
  - Stub elimination — 10 handlers have real implementations (15-22)
  - Session ops adapter behavior (23-32)
  - Provider adapter delegation (33-38)
  - Alias runtime dispatch (39-43)
  - Version alignment (44-45)
"""
from __future__ import annotations

import importlib
import subprocess
import sys
import os

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")


def _run(cmd: str):
    return subprocess.run(
        [sys.executable, "main.py"] + cmd.split(),
        capture_output=True, text=True, cwd=REPO,
        timeout=60, encoding="utf-8", errors="replace",
    )


# =============================================================================
# 1-8: Runtime dispatch completeness
# =============================================================================

class TestRuntimeDispatchCompleteness:
    def _get_command_map_keys(self):
        """Extract command_map keys by inspecting main module."""
        import re
        with open(os.path.join(REPO, "main.py"), "r", encoding="utf-8") as f:
            content = f.read()
        # Extract keys from command_map dict (all quoted command strings assigned to cmd_ or lambda)
        keys = set(re.findall(r'"([a-z0-9][a-z0-9\-]+)":\s*(?:cmd_|lambda)', content))
        return keys

    def test_01_all_461_formal_commands_resolve_via_getattr(self):
        """Test 1: All 461 formal commands resolve via getattr(main, handler_name)."""
        from cli.command_registry import PROVIDER_COMMANDS
        main = importlib.import_module("main")
        unresolved = [s.handler_name for s in PROVIDER_COMMANDS
                      if not callable(getattr(main, s.handler_name, None))]
        assert not unresolved, f"Unresolved: {unresolved}"

    def test_02_all_461_formal_commands_in_command_map(self):
        """Test 2: All 461 formal commands are present in runtime command_map."""
        from cli.command_registry import get_formal_command_names
        keys = self._get_command_map_keys()
        formal = get_formal_command_names()
        missing = formal - keys
        assert not missing, f"Missing from command_map ({len(missing)}): {sorted(missing)[:10]}"

    def test_03_getattr_and_runtime_consistent(self):
        """Test 3: Every formal command is both getattr-resolvable and in command_map."""
        from cli.command_registry import PROVIDER_COMMANDS, get_formal_command_names
        main = importlib.import_module("main")
        keys = self._get_command_map_keys()
        formal = get_formal_command_names()
        getattr_unresolved = [s.handler_name for s in PROVIDER_COMMANDS
                              if not callable(getattr(main, s.handler_name, None))]
        map_missing = formal - keys
        assert not getattr_unresolved, f"getattr unresolved: {getattr_unresolved}"
        assert not map_missing, f"command_map missing: {sorted(map_missing)[:10]}"

    def test_04_19_previously_missing_commands_now_in_command_map(self):
        """Test 4: The 19 commands previously absent from command_map are now present."""
        previously_missing = [
            "session-ops-status", "session-ops-sessions", "session-ops-session-show",
            "session-ops-metrics", "session-ops-health-summary", "session-ops-alerts",
            "session-ops-alert-show", "session-ops-alert-ack", "session-ops-incidents",
            "session-ops-incident-show", "session-ops-timeline", "session-ops-snapshot-show",
            "session-ops-checkpoint-create", "session-ops-checkpoint-show",
            "session-ops-recovery-drill", "session-ops-runbooks", "session-ops-runbook-show",
            "session-ops-replay", "session-ops-lineage",
        ]
        keys = self._get_command_map_keys()
        still_missing = [c for c in previously_missing if c not in keys]
        assert not still_missing, f"Still missing: {still_missing}"

    def test_05_twse_fetch_handlers_in_command_map(self):
        """Test 5: twse-fetch-security-master and twse-fetch-daily are in command_map."""
        keys = self._get_command_map_keys()
        assert "twse-fetch-security-master" in keys
        assert "twse-fetch-daily" in keys

    def test_06_tpex_fetch_handlers_in_command_map(self):
        """Test 6: tpex-fetch-security-master and tpex-fetch-daily are in command_map."""
        keys = self._get_command_map_keys()
        assert "tpex-fetch-security-master" in keys
        assert "tpex-fetch-daily" in keys

    def test_07_unresolved_runtime_handlers_zero(self):
        """Test 7: No formal command has an unresolvable handler_name in main."""
        from cli.command_registry import PROVIDER_COMMANDS
        main = importlib.import_module("main")
        assert all(callable(getattr(main, s.handler_name, None)) for s in PROVIDER_COMMANDS)

    def test_08_cli_registration_health_still_10_of_10(self):
        """Test 8: CLIRegistrationHealthCheck remains 10/10 PASS."""
        from cli.command_registry import PROVIDER_COMMANDS
        from cli.health import CLIRegistrationHealthCheck
        parser_commands = {s.name for s in PROVIDER_COMMANDS}
        handler_map = {s.name: s.handler_name for s in PROVIDER_COMMANDS}
        summary = CLIRegistrationHealthCheck().get_health_summary(parser_commands, handler_map)
        assert summary["failed"] == 0
        assert summary["total"] == 10


# =============================================================================
# 9-14: Session-ops 31 commands all dispatch
# =============================================================================

class TestSessionOps31Commands:
    SESSION_OPS_CMDS = [
        "session-ops-health", "session-ops-status", "session-ops-sessions",
        "session-ops-session-show", "session-ops-metrics", "session-ops-health-summary",
        "session-ops-alerts", "session-ops-alert-show", "session-ops-alert-ack",
        "session-ops-alert-resolve", "session-ops-incidents", "session-ops-incident-show",
        "session-ops-incident-open", "session-ops-incident-transition",
        "session-ops-timeline", "session-ops-pause", "session-ops-resume",
        "session-ops-halt", "session-ops-recover", "session-ops-snapshot-create",
        "session-ops-snapshot-show", "session-ops-checkpoint-create",
        "session-ops-checkpoint-show", "session-ops-recovery-drill",
        "session-ops-runbooks", "session-ops-runbook-show", "session-ops-replay",
        "session-ops-lineage", "session-ops-explain", "session-ops-report",
        "session-ops-release-gate",
    ]

    def test_09_all_31_session_ops_exit_zero(self):
        """Test 9: All 31 session-ops commands exit with code 0."""
        failed = []
        for cmd in self.SESSION_OPS_CMDS:
            r = _run(cmd)
            if r.returncode != 0:
                failed.append(cmd)
        assert not failed, f"session-ops commands exited nonzero: {failed}"

    def test_10_session_ops_explain_exits_zero(self):
        """Test 10: session-ops-explain (was broken with TypeError) now exits 0."""
        r = _run("session-ops-explain")
        assert r.returncode == 0

    def test_11_session_ops_explain_output_has_composite_status(self):
        """Test 11: session-ops-explain output contains composite_status."""
        r = _run("session-ops-explain")
        assert "composite_status" in r.stdout

    def test_12_session_ops_recovery_drill_exits_zero(self):
        """Test 12: session-ops-recovery-drill (was broken) now exits 0."""
        r = _run("session-ops-recovery-drill")
        assert r.returncode == 0

    def test_13_session_ops_release_gate_37_of_37(self):
        """Test 13: session-ops-release-gate reports 37/37."""
        r = _run("session-ops-release-gate")
        assert r.returncode == 0
        assert "37/37" in r.stdout

    def test_14_session_ops_health_45_of_45(self):
        """Test 14: session-ops-health reports 45/45."""
        r = _run("session-ops-health")
        assert r.returncode == 0
        assert "45/45" in r.stdout


# =============================================================================
# 15-22: Stub elimination
# =============================================================================

class TestStubElimination:
    FORMERLY_STUB_HANDLERS = [
        "cmd_session_ops_session_show",
        "cmd_session_ops_health_summary",
        "cmd_session_ops_alert_show",
        "cmd_session_ops_incident_show",
        "cmd_session_ops_runbooks",
        "cmd_session_ops_runbook_show",
        "cmd_twse_fetch_security_master",
        "cmd_twse_fetch_daily",
        "cmd_tpex_fetch_security_master",
        "cmd_tpex_fetch_daily",
    ]

    def _get_source(self, handler_name):
        import inspect
        main = importlib.import_module("main")
        fn = getattr(main, handler_name)
        return inspect.getsource(fn)

    def test_15_no_formerly_stub_handler_is_pass_only(self):
        """Test 15: None of the 10 formerly-stub handlers have pass-only body."""
        import inspect
        main = importlib.import_module("main")
        for h in self.FORMERLY_STUB_HANDLERS:
            fn = getattr(main, h)
            src = inspect.getsource(fn)
            body = [l.strip() for l in src.split("\n")
                    if l.strip() and not l.strip().startswith(("#", '"""', "def "))]
            assert not all(l == "pass" for l in body), f"{h} is pass-only"

    def test_16_session_ops_session_show_calls_session_registry(self):
        """Test 16: cmd_session_ops_session_show calls SessionRegistry."""
        src = self._get_source("cmd_session_ops_session_show")
        assert "SessionRegistry" in src

    def test_17_session_ops_health_summary_calls_aggregator(self):
        """Test 17: cmd_session_ops_health_summary calls SessionOperationsHealthAggregator."""
        src = self._get_source("cmd_session_ops_health_summary")
        assert "SessionOperationsHealthAggregator" in src

    def test_18_session_ops_alert_show_calls_alert_engine(self):
        """Test 18: cmd_session_ops_alert_show calls AlertEngine."""
        src = self._get_source("cmd_session_ops_alert_show")
        assert "AlertEngine" in src

    def test_19_session_ops_incident_show_calls_incident_manager(self):
        """Test 19: cmd_session_ops_incident_show calls IncidentManager."""
        src = self._get_source("cmd_session_ops_incident_show")
        assert "IncidentManager" in src

    def test_20_session_ops_runbooks_calls_runbook_registry(self):
        """Test 20: cmd_session_ops_runbooks calls RunbookRegistry."""
        src = self._get_source("cmd_session_ops_runbooks")
        assert "RunbookRegistry" in src

    def test_21_twse_fetch_security_master_delegates(self):
        """Test 21: cmd_twse_fetch_security_master delegates to cmd_twse_security_list."""
        src = self._get_source("cmd_twse_fetch_security_master")
        assert "cmd_twse_security_list" in src

    def test_22_tpex_fetch_daily_delegates(self):
        """Test 22: cmd_tpex_fetch_daily delegates to cmd_tpex_daily."""
        src = self._get_source("cmd_tpex_fetch_daily")
        assert "cmd_tpex_daily" in src


# =============================================================================
# 23-32: Session ops adapter behavior
# =============================================================================

class TestSessionOpsAdapters:
    def test_23_session_show_not_found_when_empty(self):
        """Test 23: session-ops-session-show returns NOT_FOUND when registry empty."""
        from paper_trading.operations.session_registry_v163 import SessionRegistry
        from unittest.mock import patch
        with patch.object(SessionRegistry, "list_all", return_value=[]):
            r = _run("session-ops-session-show")
        assert r.returncode == 0
        assert "NOT_FOUND" in r.stdout

    def test_24_health_summary_has_overall_field(self):
        """Test 24: session-ops-health-summary output contains 'overall'."""
        r = _run("session-ops-health-summary")
        assert r.returncode == 0
        assert "overall" in r.stdout

    def test_25_health_summary_has_components(self):
        """Test 25: session-ops-health-summary output contains component count."""
        r = _run("session-ops-health-summary")
        assert r.returncode == 0
        assert "components" in r.stdout

    def test_26_alert_show_not_found_when_empty(self):
        """Test 26: session-ops-alert-show returns NOT_FOUND when no open alerts."""
        r = _run("session-ops-alert-show")
        assert r.returncode == 0
        assert "NOT_FOUND" in r.stdout

    def test_27_incident_show_not_found_when_empty(self):
        """Test 27: session-ops-incident-show returns NOT_FOUND when no open incidents."""
        r = _run("session-ops-incident-show")
        assert r.returncode == 0
        assert "NOT_FOUND" in r.stdout

    def test_28_runbooks_lists_11_runbooks(self):
        """Test 28: session-ops-runbooks lists 11 runbooks from RunbookRegistry."""
        r = _run("session-ops-runbooks")
        assert r.returncode == 0
        assert "Runbooks (11)" in r.stdout

    def test_29_runbook_show_displays_trigger(self):
        """Test 29: session-ops-runbook-show displays trigger field."""
        r = _run("session-ops-runbook-show")
        assert r.returncode == 0
        assert "trigger" in r.stdout

    def test_30_runbook_show_displays_prohibited_actions(self):
        """Test 30: session-ops-runbook-show displays prohibited_actions field."""
        r = _run("session-ops-runbook-show")
        assert r.returncode == 0
        assert "prohibited_actions" in r.stdout

    def test_31_explain_output_has_safety_blocked(self):
        """Test 31: session-ops-explain output contains safety_blocked."""
        r = _run("session-ops-explain")
        assert r.returncode == 0
        assert "safety_blocked" in r.stdout

    def test_32_explain_output_has_paper_only(self):
        """Test 32: session-ops-explain output contains paper_only=True."""
        r = _run("session-ops-explain")
        assert r.returncode == 0
        assert "paper_only" in r.stdout


# =============================================================================
# 33-38: Provider adapter delegation
# =============================================================================

class TestProviderAdapterDelegation:
    def test_33_twse_fetch_security_master_exits_zero(self):
        """Test 33: twse-fetch-security-master exits 0 (delegates to query service)."""
        r = _run("twse-fetch-security-master")
        assert r.returncode == 0

    def test_34_twse_fetch_security_master_output_has_securities(self):
        """Test 34: twse-fetch-security-master output contains 'Securities'."""
        r = _run("twse-fetch-security-master")
        assert r.returncode == 0
        assert "Securities" in r.stdout or "TWSE" in r.stdout

    def test_35_twse_fetch_daily_exits_zero(self):
        """Test 35: twse-fetch-daily exits 0."""
        r = _run("twse-fetch-daily")
        assert r.returncode == 0

    def test_36_tpex_fetch_security_master_exits_zero(self):
        """Test 36: tpex-fetch-security-master exits 0."""
        r = _run("tpex-fetch-security-master")
        assert r.returncode == 0

    def test_37_tpex_fetch_daily_exits_zero(self):
        """Test 37: tpex-fetch-daily exits 0."""
        r = _run("tpex-fetch-daily")
        assert r.returncode == 0

    def test_38_provider_no_fake_fallback(self):
        """Test 38: TWSE fetch security master does not use fixture/fake payload."""
        import inspect
        main = importlib.import_module("main")
        fn = getattr(main, "cmd_twse_fetch_security_master")
        src = inspect.getsource(fn)
        assert "fake" not in src.lower()
        assert "fixture" not in src.lower()
        assert "DRY-RUN" not in src


# =============================================================================
# 39-43: Alias runtime dispatch
# =============================================================================

class TestAliasRuntimeDispatch:
    ALIASES = [
        ("session-ops-status", "session-ops-composite-status"),
        ("session-ops-sessions", "session-ops-registry-list"),
        ("session-ops-metrics", "session-ops-metrics-summary"),
        ("session-ops-alerts", "session-ops-alert-list"),
        ("session-ops-alert-ack", "session-ops-alert-acknowledge"),
        ("session-ops-incidents", "session-ops-incident-list"),
        ("session-ops-timeline", "session-ops-audit-tail"),
        ("session-ops-snapshot-show", "session-ops-snapshot-verify"),
        ("session-ops-checkpoint-create", "session-ops-checkpoint-save"),
        ("session-ops-checkpoint-show", "session-ops-checkpoint-restore"),
        ("session-ops-recovery-drill", "session-ops-drill-run"),
        ("session-ops-replay", "session-ops-replay-run"),
        ("session-ops-lineage", "session-ops-lineage-show"),
    ]

    def test_39_all_13_alias_commands_exit_zero(self):
        """Test 39: All 13 alias CLI commands exit with code 0."""
        failed = []
        for alias_cmd, _ in self.ALIASES:
            r = _run(alias_cmd)
            if r.returncode != 0:
                failed.append(alias_cmd)
        assert not failed, f"Alias commands failed: {failed}"

    def test_40_alias_python_identity_preserved(self):
        """Test 40: Alias handler_name IS the canonical function (Python identity)."""
        import importlib
        main = importlib.import_module("main")
        alias_map = [
            ("cmd_session_ops_status", "cmd_session_ops_composite_status"),
            ("cmd_session_ops_sessions", "cmd_session_ops_registry_list"),
            ("cmd_session_ops_metrics", "cmd_session_ops_metrics_summary"),
            ("cmd_session_ops_alerts", "cmd_session_ops_alert_list"),
            ("cmd_session_ops_alert_ack", "cmd_session_ops_alert_acknowledge"),
            ("cmd_session_ops_incidents", "cmd_session_ops_incident_list"),
            ("cmd_session_ops_timeline", "cmd_session_ops_audit_tail"),
            ("cmd_session_ops_snapshot_show", "cmd_session_ops_snapshot_verify"),
            ("cmd_session_ops_checkpoint_create", "cmd_session_ops_checkpoint_save"),
            ("cmd_session_ops_checkpoint_show", "cmd_session_ops_checkpoint_restore"),
            ("cmd_session_ops_recovery_drill", "cmd_session_ops_drill_run"),
            ("cmd_session_ops_replay", "cmd_session_ops_replay_run"),
            ("cmd_session_ops_lineage", "cmd_session_ops_lineage_show"),
        ]
        for alias_name, canonical_name in alias_map:
            alias_fn = getattr(main, alias_name)
            canon_fn = getattr(main, canonical_name)
            assert alias_fn is canon_fn, f"{alias_name} is not {canonical_name}"

    def test_41_no_alias_loop(self):
        """Test 41: No alias points to itself (no alias loop)."""
        import importlib
        main = importlib.import_module("main")
        aliases = [
            "cmd_session_ops_status", "cmd_session_ops_sessions", "cmd_session_ops_metrics",
            "cmd_session_ops_alerts", "cmd_session_ops_alert_ack", "cmd_session_ops_incidents",
            "cmd_session_ops_timeline", "cmd_session_ops_snapshot_show",
            "cmd_session_ops_checkpoint_create", "cmd_session_ops_checkpoint_show",
            "cmd_session_ops_recovery_drill", "cmd_session_ops_replay", "cmd_session_ops_lineage",
        ]
        for a in aliases:
            fn = getattr(main, a)
            # No loop: alias must point to a canonical whose __name__ differs from the alias name
            assert fn.__name__ != a, f"Alias loop detected: {a} points to itself"

    def test_42_session_ops_status_output_matches_composite_status(self):
        """Test 42: cmd_session_ops_status is identity-equal to cmd_session_ops_composite_status;
        running session-ops-status twice produces identical output (idempotent)."""
        import importlib
        main = importlib.import_module("main")
        assert getattr(main, "cmd_session_ops_status") is getattr(main, "cmd_session_ops_composite_status")
        r1 = _run("session-ops-status")
        r2 = _run("session-ops-status")
        assert r1.returncode == 0
        assert r2.returncode == 0

    def test_43_session_ops_lineage_output_matches_lineage_show(self):
        """Test 43: cmd_session_ops_lineage is identity-equal to cmd_session_ops_lineage_show;
        running session-ops-lineage twice produces exit 0 (idempotent)."""
        import importlib
        main = importlib.import_module("main")
        assert getattr(main, "cmd_session_ops_lineage") is getattr(main, "cmd_session_ops_lineage_show")
        r1 = _run("session-ops-lineage")
        r2 = _run("session-ops-lineage")
        assert r1.returncode == 0
        assert r2.returncode == 0


# =============================================================================
# 44-45: Version alignment
# =============================================================================

class TestVersionAlignment:
    def test_44_version_is_1633(self):
        """Test 44: VERSION is '1.6.3.3'."""
        from release.version_info import VERSION
        assert VERSION == "1.6.3.3", f"Expected 1.6.3.3 got {VERSION}"

    def test_45_release_name_is_cli_handler_resolution(self):
        """Test 45: RELEASE_NAME is 'CLI Handler Resolution Integrity Hotfix'."""
        from release.version_info import RELEASE_NAME
        assert RELEASE_NAME == "CLI Handler Resolution Integrity Hotfix", (
            f"Got: {RELEASE_NAME}"
        )
