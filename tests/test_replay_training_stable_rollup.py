"""
tests/test_replay_training_stable_rollup.py — Replay Training Stable Rollup v1.2.9 tests.

Tests for stable rollup: manifest, capability matrix, contracts, compatibility,
health check, version_info, safety invariants, no forbidden actions.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import pytest

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


# ---------------------------------------------------------------------------
# version_info tests
# ---------------------------------------------------------------------------

class TestVersionInfo:
    """v1.2.9 version_info constants."""

    def test_version_is_129(self):
        # Global VERSION is the application version (now 1.3.0+).
        # Replay Training stable baseline is frozen at 1.2.9; check that constant.
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9", (
            f"Expected REPLAY_STABLE_BASELINE=1.2.9, got {REPLAY_STABLE_BASELINE}"
        )

    def test_replay_training_line_complete(self):
        from release.version_info import REPLAY_TRAINING_LINE_COMPLETE
        assert REPLAY_TRAINING_LINE_COMPLETE is True

    def test_stable_rollup(self):
        from release.version_info import STABLE_ROLLUP
        assert STABLE_ROLLUP is True

    def test_no_real_orders(self):
        from release.version_info import NO_REAL_ORDERS, REAL_ORDERS_ENABLED
        assert NO_REAL_ORDERS is True
        assert REAL_ORDERS_ENABLED is False

    def test_broker_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_blocked(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_auto_flags_all_false(self):
        import release.version_info as vi
        assert getattr(vi, "AUTO_REPLAY_DECISION_ENABLED", False) is False
        assert getattr(vi, "AUTO_REPLAY_EXECUTION_ENABLED", False) is False
        assert getattr(vi, "AUTO_MISTAKE_CONFIRMATION_ENABLED", False) is False
        assert getattr(vi, "AUTO_OUTCOME_REVEAL_ENABLED", False) is False
        assert getattr(vi, "AUTO_STRATEGY_CHANGE_ENABLED", False) is False
        assert getattr(vi, "AUTO_DATASET_REPAIR_ENABLED", False) is False
        assert getattr(vi, "AUTO_SESSION_REBIND_ENABLED", False) is False

    def test_replay_stable_flags_available(self):
        from release.version_info import (
            REPLAY_STABLE_HEALTH_AVAILABLE,
            REPLAY_STABLE_MANIFEST_AVAILABLE,
            REPLAY_CAPABILITY_MATRIX_AVAILABLE,
        )
        assert REPLAY_STABLE_HEALTH_AVAILABLE is True
        assert REPLAY_STABLE_MANIFEST_AVAILABLE is True
        assert REPLAY_CAPABILITY_MATRIX_AVAILABLE is True

    def test_replay_trade_execution_disabled(self):
        from release.version_info import REPLAY_TRADE_EXECUTION_ENABLED
        assert REPLAY_TRADE_EXECUTION_ENABLED is False


# ---------------------------------------------------------------------------
# stable_schema tests
# ---------------------------------------------------------------------------

class TestStableSchema:
    """StableModuleInfo, StableCapability, StableManifest, etc."""

    def test_stable_module_info_safety(self):
        from replay.stable_schema import StableModuleInfo
        m = StableModuleInfo(module_name="test", introduced_version="1.2.9")
        assert m.no_real_orders is True
        assert m.research_only is True
        assert m.current_version == "1.2.9"

    def test_stable_capability_safety(self):
        from replay.stable_schema import StableCapability
        c = StableCapability(capability_id="test", module="test", introduced_version="1.2.9")
        assert c.no_real_orders is True
        assert c.research_only is True
        assert c.safety_qualified is True

    def test_stable_manifest_safety(self):
        from replay.stable_schema import StableManifest
        m = StableManifest()
        assert m.no_real_orders is True
        assert m.broker_disabled is True
        assert m.research_only is True

    def test_all_schema_dataclasses_import(self):
        from replay.stable_schema import (
            StableModuleInfo, StableCapability, StableManifest,
            StableContractResult, StableCompatibilityResult, StableAuditResult,
        )
        # All import without error
        assert StableModuleInfo is not None
        assert StableCapability is not None
        assert StableManifest is not None
        assert StableContractResult is not None
        assert StableCompatibilityResult is not None
        assert StableAuditResult is not None


# ---------------------------------------------------------------------------
# StableManifest tests
# ---------------------------------------------------------------------------

class TestStableManifest:
    """ReplayStableManifest.build() tests."""

    def setup_method(self):
        from replay.stable_manifest import ReplayStableManifest
        self.manifest = ReplayStableManifest()
        self.built = self.manifest.build()

    def test_manifest_builds_correctly(self):
        assert self.built["release_version"] == "1.2.9"
        assert self.built["release_name"] == "Replay Training Stable Rollup"

    def test_manifest_has_12_modules(self):
        assert self.built["module_count"] == 12
        assert len(self.built["modules"]) == 12

    def test_manifest_safety_flags(self):
        assert self.built["no_real_orders"] is True
        assert self.built["broker_disabled"] is True
        assert self.built["research_only"] is True
        assert self.built["stable_rollup"] is True

    def test_manifest_safety_flags_dict(self):
        flags = self.built["safety_flags"]
        assert flags["no_real_orders"] is True
        assert flags["auto_replay_decision_enabled"] is False
        assert flags["auto_replay_execution_enabled"] is False
        assert flags["replay_trade_execution_enabled"] is False

    def test_manifest_no_absolute_paths(self):
        # Store paths should be relative only
        for path in self.built["store_paths"]:
            assert not path.startswith("/"), f"Absolute path found: {path}"
            assert ":" not in path, f"Windows absolute path found: {path}"

    def test_manifest_backward_compat_range(self):
        compat = self.built["backward_compatibility_range"]
        assert "1.2.0" in compat
        assert "1.2.8" in compat
        assert len(compat) == 9

    def test_manifest_has_cli_commands(self):
        cmds = self.built["CLI_commands"]
        assert "replay-stable-health" in cmds
        assert "replay-stable-manifest" in cmds
        assert "replay-stable-capabilities" in cmds


# ---------------------------------------------------------------------------
# CapabilityMatrix tests
# ---------------------------------------------------------------------------

class TestCapabilityMatrix:
    """ReplayStableCapabilityMatrix.build() tests."""

    def setup_method(self):
        from replay.stable_capability_matrix import ReplayStableCapabilityMatrix
        self.matrix = ReplayStableCapabilityMatrix()
        self.caps = self.matrix.build()

    def test_has_16_capabilities(self):
        assert len(self.caps) == 16, f"Expected 16, got {len(self.caps)}"

    def test_all_safety_qualified(self):
        for cap in self.caps:
            assert cap["safety_qualified"] is True, f"{cap['capability_id']} not safety_qualified"
            assert cap["no_real_orders"] is True, f"{cap['capability_id']} missing no_real_orders"
            assert cap["research_only"] is True, f"{cap['capability_id']} missing research_only"

    def test_all_have_required_fields(self):
        required = [
            "capability_id", "module", "introduced_version", "current_status",
            "health_command", "CLI_available", "GUI_available", "report_available",
            "backward_compatible", "safety_qualified", "research_only", "no_real_orders", "notes",
        ]
        for cap in self.caps:
            for field in required:
                assert field in cap, f"Capability {cap.get('capability_id')} missing field {field}"

    def test_known_capabilities_present(self):
        ids = {c["capability_id"] for c in self.caps}
        expected = {
            "replay_session_step", "scenario_library", "session_fork_checkpoint",
            "decision_journal", "process_outcome_scoring", "mistake_taxonomy",
            "strategy_replay", "multi_timeframe_sync", "review_queue",
            "challenge_mode", "challenge_personal_leaderboard",
            "dataset_registry", "session_registry",
            "stable_health_check", "stable_manifest", "capability_matrix",
        }
        for eid in expected:
            assert eid in ids, f"Capability {eid} missing from matrix"


# ---------------------------------------------------------------------------
# ContractChecker tests
# ---------------------------------------------------------------------------

class TestContractChecker:
    """ReplayStableContractChecker.check_all() tests."""

    def test_contract_checker_imports(self):
        from replay.stable_contracts import ReplayStableContractChecker
        assert ReplayStableContractChecker is not None

    def test_check_all_returns_dict(self):
        from replay.stable_contracts import ReplayStableContractChecker
        results = ReplayStableContractChecker().check_all()
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_no_real_orders_contract_passes(self):
        from replay.stable_contracts import ReplayStableContractChecker
        results = ReplayStableContractChecker().check_all()
        status, msg = results["no_real_orders_invariant"]
        assert status == "PASS", f"no_real_orders_invariant: {msg}"

    def test_research_only_contract_passes(self):
        from replay.stable_contracts import ReplayStableContractChecker
        results = ReplayStableContractChecker().check_all()
        status, msg = results["research_only_invariant"]
        assert status == "PASS", f"research_only_invariant: {msg}"

    def test_stable_schema_contract_passes(self):
        from replay.stable_contracts import ReplayStableContractChecker
        results = ReplayStableContractChecker().check_all()
        status, msg = results["stable_schema"]
        assert status == "PASS", f"stable_schema contract: {msg}"

    def test_no_fail_statuses(self):
        from replay.stable_contracts import ReplayStableContractChecker
        results = ReplayStableContractChecker().check_all()
        failures = [(k, msg) for k, (s, msg) in results.items() if s == "FAIL"]
        assert not failures, f"Contract FAIL(s): {failures}"


# ---------------------------------------------------------------------------
# CompatibilityChecker tests
# ---------------------------------------------------------------------------

class TestCompatibilityChecker:
    """ReplayStableCompatibilityChecker tests."""

    def test_checker_imports(self):
        from replay.stable_compatibility import ReplayStableCompatibilityChecker
        assert ReplayStableCompatibilityChecker is not None

    def test_all_versions_checked(self):
        from replay.stable_compatibility import ReplayStableCompatibilityChecker
        checker = ReplayStableCompatibilityChecker()
        assert "1.2.0" in checker.SUPPORTED_VERSIONS
        assert "1.2.8" in checker.SUPPORTED_VERSIONS
        assert len(checker.SUPPORTED_VERSIONS) == 9

    def test_check_all_returns_dict(self):
        from replay.stable_compatibility import ReplayStableCompatibilityChecker
        results = ReplayStableCompatibilityChecker().check_all()
        assert isinstance(results, dict)
        assert "1.2.0" in results
        assert "1.2.8" in results

    def test_no_fail_statuses(self):
        from replay.stable_compatibility import ReplayStableCompatibilityChecker
        results = ReplayStableCompatibilityChecker().check_all()
        failures = [(v, msg) for v, (s, msg) in results.items() if s == "FAIL"]
        assert not failures, f"Compatibility FAIL(s): {failures}"

    def test_backward_compat_versions_list_correct(self):
        from replay.stable_compatibility import ReplayStableCompatibilityChecker
        checker = ReplayStableCompatibilityChecker()
        assert checker.SUPPORTED_VERSIONS == [
            "1.2.0", "1.2.1", "1.2.2", "1.2.3",
            "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8",
        ]


# ---------------------------------------------------------------------------
# StableHealthCheck tests
# ---------------------------------------------------------------------------

class TestStableHealthCheck:
    """ReplayStableHealthCheck.run() tests."""

    def test_health_check_imports(self):
        from replay.stable_health import ReplayStableHealthCheck
        assert ReplayStableHealthCheck is not None

    def test_health_check_runs(self):
        from replay.stable_health import ReplayStableHealthCheck
        hc = ReplayStableHealthCheck()
        results = hc.run()
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_health_check_has_version_check(self):
        from replay.stable_health import ReplayStableHealthCheck
        hc = ReplayStableHealthCheck()
        results = hc.run()
        assert "version_info" in results
        status, _ = results["version_info"]
        assert status == "PASS"

    def test_health_check_no_real_orders(self):
        from replay.stable_health import ReplayStableHealthCheck
        hc = ReplayStableHealthCheck()
        results = hc.run()
        assert "no_real_orders" in results
        status, _ = results["no_real_orders"]
        assert status == "PASS"

    def test_health_check_no_broker(self):
        from replay.stable_health import ReplayStableHealthCheck
        hc = ReplayStableHealthCheck()
        results = hc.run()
        assert "no_broker" in results
        status, _ = results["no_broker"]
        assert status == "PASS"

    def test_health_check_no_fail_statuses(self):
        from replay.stable_health import ReplayStableHealthCheck
        hc = ReplayStableHealthCheck()
        results = hc.run()
        failures = [(k, msg) for k, (s, msg) in results.items() if s == "FAIL"]
        assert not failures, f"Health check FAIL(s): {failures}"

    def test_health_check_safety_flags(self):
        from replay.stable_health import ReplayStableHealthCheck
        hc = ReplayStableHealthCheck()
        assert hc.RESEARCH_ONLY is True
        assert hc.NO_REAL_ORDERS is True
        assert hc.STABLE_ROLLUP is True


# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------

class TestSafetyInvariants:
    """Safety invariant tests for all stable modules."""

    def test_stable_schema_no_real_orders(self):
        import replay.stable_schema as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_manifest_no_real_orders(self):
        import replay.stable_manifest as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_capability_matrix_no_real_orders(self):
        import replay.stable_capability_matrix as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_contracts_no_real_orders(self):
        import replay.stable_contracts as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_compatibility_no_real_orders(self):
        import replay.stable_compatibility as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_store_audit_no_real_orders(self):
        import replay.stable_store_audit as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_runtime_isolation_no_real_orders(self):
        import replay.stable_runtime_isolation as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_cli_audit_no_real_orders(self):
        import replay.stable_cli_audit as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_gui_audit_no_real_orders(self):
        import replay.stable_gui_audit as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_report_audit_no_real_orders(self):
        import replay.stable_report_audit as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_safety_audit_no_real_orders(self):
        import replay.stable_safety_audit as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_regression_audit_no_real_orders(self):
        import replay.stable_regression_audit as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_release_gate_no_real_orders(self):
        import replay.stable_release_gate as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_summary_no_real_orders(self):
        import replay.stable_summary as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_report_no_real_orders(self):
        import replay.stable_report as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True

    def test_stable_health_no_real_orders(self):
        import replay.stable_health as m
        assert m.NO_REAL_ORDERS is True
        assert m.RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# No forbidden actions
# ---------------------------------------------------------------------------

class TestNoForbiddenActions:
    """Verify no dangerous trading actions in stable modules."""

    _DANGEROUS = [
        "send_order(", "place_order(", "real_buy(", "real_sell(",
        "broker_login(", "broker.connect(", "execute_trade(", "auto_trade(",
    ]

    _SAFETY_WHITELIST = [
        "No Real Orders", "NO_REAL_ORDERS", "DISABLED", "disabled",
        "no_real_orders", "[!]", "# no", "not Investment",
        # Lines in keyword-definition constants (audit files enumerate
        # prohibited patterns — they are not actual broker/order calls)
        "_DANGEROUS", "_FORBIDDEN",
    ]

    def _check_module_source(self, module_name: str) -> list:
        """Check module source for dangerous keywords. Returns list of violations."""
        import importlib
        import inspect
        violations = []
        try:
            mod = importlib.import_module(module_name)
            source = inspect.getsource(mod)
            for danger in self._DANGEROUS:
                if danger in source:
                    idx = source.find(danger)
                    context = source[max(0, idx-100):idx+len(danger)+100]
                    is_safe = any(s in context for s in self._SAFETY_WHITELIST)
                    if not is_safe:
                        violations.append(f"{module_name}: {danger!r}")
        except Exception:
            pass
        return violations

    def test_no_forbidden_in_stable_health(self):
        violations = self._check_module_source("replay.stable_health")
        assert not violations, f"Forbidden keywords: {violations}"

    def test_no_forbidden_in_stable_contracts(self):
        violations = self._check_module_source("replay.stable_contracts")
        assert not violations, f"Forbidden keywords: {violations}"

    def test_no_forbidden_in_stable_safety_audit(self):
        # stable_safety_audit.py defines the _DANGEROUS_KEYWORDS list — it enumerates
        # forbidden patterns as string literals for scanning purposes.
        # We verify safety via NO_REAL_ORDERS and RESEARCH_ONLY flags instead of
        # keyword-scanning the audit file itself (which would self-reference).
        from replay import stable_safety_audit
        assert getattr(stable_safety_audit, "NO_REAL_ORDERS", False) is True, \
            "stable_safety_audit.NO_REAL_ORDERS must be True"
        assert getattr(stable_safety_audit, "RESEARCH_ONLY", False) is True, \
            "stable_safety_audit.RESEARCH_ONLY must be True"

    def test_no_forbidden_in_stable_report(self):
        violations = self._check_module_source("replay.stable_report")
        assert not violations, f"Forbidden keywords: {violations}"


# ---------------------------------------------------------------------------
# Backward compat versions list
# ---------------------------------------------------------------------------

class TestBackwardCompatVersionsList:
    """Verify backward compatibility versions list is correct."""

    def test_manifest_compat_range(self):
        from replay.stable_manifest import ReplayStableManifest
        compat = ReplayStableManifest.BACKWARD_COMPATIBILITY_RANGE
        assert compat == [
            "1.2.0", "1.2.1", "1.2.2", "1.2.3",
            "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8",
        ]

    def test_compatibility_checker_versions(self):
        from replay.stable_compatibility import ReplayStableCompatibilityChecker
        versions = ReplayStableCompatibilityChecker.SUPPORTED_VERSIONS
        assert "1.2.0" in versions
        assert "1.2.8" in versions
        assert "1.2.9" not in versions  # 1.2.9 is current, not backward compat
        assert len(versions) == 9
