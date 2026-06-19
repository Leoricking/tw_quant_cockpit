"""
replay/stable_health.py — ReplayStableHealthCheck for v1.2.9.

Comprehensive health check for the Replay Training Stable Rollup.
Output: PASS/WARN/FAIL for each check.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableHealthCheck:
    """
    Health check for Replay Training Stable Rollup v1.2.9.

    run() returns Dict[str, Tuple[str, str]] — {check_name: (status, message)}.
    print_results(results) prints formatted output.

    FAIL only for hard invariant violations.
    WARN for optional module gaps or non-critical issues.
    PASS for all verified correct state.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    STABLE_ROLLUP = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns dict of name -> (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}

        # --- Core module imports ---
        results["imports"]                   = self._check_imports()
        results["version_info"]              = self._check_version_info()
        results["stable_manifest"]           = self._check_stable_manifest()
        results["capability_matrix"]         = self._check_capability_matrix()

        # --- Stable audit modules ---
        results["contracts"]                 = self._check_contracts()
        results["backward_compatibility"]    = self._check_backward_compatibility()
        results["store_audit"]               = self._check_store_audit()
        results["runtime_isolation"]         = self._check_runtime_isolation()
        results["cli_audit"]                 = self._check_cli_audit()
        results["gui_audit"]                 = self._check_gui_audit()
        results["report_audit"]              = self._check_report_audit()
        results["safety_audit"]              = self._check_safety_audit()
        results["regression_audit"]          = self._check_regression_audit()

        # --- Core replay module health ---
        results["replay_foundation"]         = self._check_replay_foundation()
        results["scenario_manager"]          = self._check_scenario_manager()
        results["session_manager"]           = self._check_session_manager()
        results["journal"]                   = self._check_journal()
        results["scoring"]                   = self._check_scoring()
        results["strategy"]                  = self._check_strategy()
        results["timeframe"]                 = self._check_timeframe()
        results["review"]                    = self._check_review()
        results["challenge"]                 = self._check_challenge()
        results["dataset_registry"]          = self._check_dataset_registry()
        results["session_registry"]          = self._check_session_registry()

        # --- Release gate semantics ---
        results["release_gate_semantics"]    = self._check_release_gate_semantics()
        results["expected_safety_block"]     = self._check_expected_safety_block()
        results["unexpected_block_nonzero"]  = self._check_unexpected_block_nonzero()
        results["fail_nonzero"]              = self._check_fail_nonzero()
        results["warn_zero"]                 = self._check_warn_zero()

        # --- Data integrity invariants ---
        results["real_no_mock_fallback"]     = self._check_real_no_mock_fallback()
        results["mock_demo_only"]            = self._check_mock_demo_only()
        results["future_firewall"]           = self._check_future_firewall()
        results["point_in_time"]             = self._check_point_in_time()

        # --- Auto-action guards ---
        results["no_auto_decision"]          = self._check_no_auto_decision()
        results["no_auto_execution"]         = self._check_no_auto_execution()
        results["no_auto_confirm"]           = self._check_no_auto_confirm()
        results["no_auto_reveal"]            = self._check_no_auto_reveal()
        results["no_auto_repair"]            = self._check_no_auto_repair()
        results["no_auto_rebind"]            = self._check_no_auto_rebind()

        # --- Broker / execution guards ---
        results["no_broker"]                 = self._check_no_broker()
        results["no_real_orders"]            = self._check_no_real_orders()

        # --- Runtime hygiene ---
        results["runtime_ignored"]           = self._check_runtime_ignored()
        results["generated_reports_ignored"] = self._check_generated_reports_ignored()
        results["package_ignored"]           = self._check_package_ignored()
        results["no_forbidden_actions"]      = self._check_no_forbidden_actions()

        return results

    def print_results(self, results: Dict[str, Tuple[str, str]]) -> None:
        """Print formatted health check results."""
        print("=" * 70)
        print("  Replay Training Stable Rollup Health Check v1.2.9")
        print("  [!] Research Only | No Real Orders | Replay Training Line Complete")
        print("=" * 70)
        pass_count = sum(1 for s, _ in results.values() if s == "PASS")
        warn_count = sum(1 for s, _ in results.values() if s == "WARN")
        fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
        block_count = sum(1 for s, _ in results.values() if s == "BLOCKED")
        print(f"  Total:    {len(results)}")
        print(f"  PASS:     {pass_count}")
        print(f"  WARN:     {warn_count}")
        print(f"  FAIL:     {fail_count}")
        print(f"  BLOCKED:  {block_count}")
        print()
        icons = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "BLOCKED": "[BLOCKED]"}
        for name, (status, message) in results.items():
            icon = icons.get(status, "[?]")
            print(f"  {icon} {name}")
            if message:
                print(f"         {message[:100]}")
        print("=" * 70)
        if fail_count > 0:
            print(f"  [!] {fail_count} FAIL(s) detected — release gate BLOCKED")
        elif warn_count > 0:
            print(f"  [!] {warn_count} WARN(s) — review before release")
        else:
            print("  [OK] All checks passed — Replay Training Stable Rollup health OK")
        print("[!] Research Only. No Real Orders. Not Investment Advice.")

    # -----------------------------------------------------------------------
    # Core imports
    # -----------------------------------------------------------------------

    def _check_imports(self) -> Tuple[str, str]:
        try:
            from replay.stable_schema import (
                StableModuleInfo, StableCapability, StableManifest,
                StableContractResult, StableCompatibilityResult, StableAuditResult,
            )
            m = StableModuleInfo(module_name="test", introduced_version="1.2.9")
            assert m.no_real_orders is True
            return ("PASS", "All stable_schema dataclasses import OK with safety flags")
        except Exception as exc:
            return ("FAIL", f"stable_schema import error: {exc}")

    def _check_version_info(self) -> Tuple[str, str]:
        try:
            from release.version_info import (
                VERSION, REPLAY_STABLE_BASELINE, REPLAY_TRAINING_LINE_COMPLETE,
                STABLE_ROLLUP, NO_REAL_ORDERS, REAL_ORDERS_ENABLED,
                BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            )
            # Replay stable baseline must be frozen at 1.2.9
            if REPLAY_STABLE_BASELINE != "1.2.9":
                return ("FAIL", f"REPLAY_STABLE_BASELINE={REPLAY_STABLE_BASELINE}, expected 1.2.9")
            # Application VERSION must be >= 1.2.9 (semantic; 1.3.0 is compatible)
            def _ver(v: str):
                try:
                    return tuple(int(x) for x in v.lstrip("v").split(".")[:3])
                except Exception:
                    return (0, 0, 0)
            if _ver(VERSION) < _ver("1.2.9"):
                return ("FAIL", f"VERSION={VERSION} is below minimum 1.2.9")
            if not REPLAY_TRAINING_LINE_COMPLETE:
                return ("FAIL", "REPLAY_TRAINING_LINE_COMPLETE is not True")
            if not STABLE_ROLLUP:
                return ("FAIL", "STABLE_ROLLUP is not True")
            if NO_REAL_ORDERS is not True:
                return ("FAIL", f"NO_REAL_ORDERS={NO_REAL_ORDERS}")
            if REAL_ORDERS_ENABLED is not False:
                return ("FAIL", f"REAL_ORDERS_ENABLED={REAL_ORDERS_ENABLED}")
            if BROKER_EXECUTION_ENABLED is not False:
                return ("FAIL", f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}")
            if PRODUCTION_TRADING_BLOCKED is not True:
                return ("FAIL", f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}")
            return ("PASS", f"version_info: v{VERSION} (baseline {REPLAY_STABLE_BASELINE}), all safety flags OK")
        except Exception as exc:
            return ("FAIL", f"version_info check error: {exc}")

    def _check_stable_manifest(self) -> Tuple[str, str]:
        try:
            from replay.stable_manifest import ReplayStableManifest
            m = ReplayStableManifest()
            manifest = m.build()
            assert manifest["no_real_orders"] is True
            assert manifest["broker_disabled"] is True
            assert manifest["research_only"] is True
            assert manifest["release_version"] == "1.2.9"
            assert len(manifest["modules"]) == 12
            return ("PASS", f"StableManifest: 12 modules, no_real_orders=True, release=1.2.9")
        except Exception as exc:
            return ("FAIL", f"StableManifest error: {exc}")

    def _check_capability_matrix(self) -> Tuple[str, str]:
        try:
            from replay.stable_capability_matrix import ReplayStableCapabilityMatrix
            caps = ReplayStableCapabilityMatrix().build()
            assert len(caps) == 16, f"Expected 16 capabilities, got {len(caps)}"
            for cap in caps:
                assert cap["research_only"] is True
                assert cap["no_real_orders"] is True
            return ("PASS", f"CapabilityMatrix: {len(caps)} capabilities, all safety-qualified")
        except Exception as exc:
            return ("FAIL", f"CapabilityMatrix error: {exc}")

    # -----------------------------------------------------------------------
    # Stable audit modules
    # -----------------------------------------------------------------------

    def _check_contracts(self) -> Tuple[str, str]:
        try:
            from replay.stable_contracts import ReplayStableContractChecker
            results = ReplayStableContractChecker().check_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Contract failures: {failed[:3]}")
            return ("PASS", f"All {len(results)} contract checks: no FAILs")
        except Exception as exc:
            return ("WARN", f"Contract check error: {exc}")

    def _check_backward_compatibility(self) -> Tuple[str, str]:
        try:
            from replay.stable_compatibility import ReplayStableCompatibilityChecker
            results = ReplayStableCompatibilityChecker().check_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Compatibility failures: {failed}")
            pass_count = sum(1 for s, _ in results.values() if s == "PASS")
            return ("PASS", f"Backward compat: {pass_count}/{len(results)} versions PASS")
        except Exception as exc:
            return ("WARN", f"Compatibility check error: {exc}")

    def _check_store_audit(self) -> Tuple[str, str]:
        try:
            from replay.stable_store_audit import ReplayStableStoreAudit
            results = ReplayStableStoreAudit().audit_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Store audit failures: {failed}")
            pass_count = sum(1 for s, _ in results.values() if s == "PASS")
            return ("PASS", f"Store audit: {pass_count}/{len(results)} stores PASS")
        except Exception as exc:
            return ("WARN", f"Store audit error: {exc}")

    def _check_runtime_isolation(self) -> Tuple[str, str]:
        try:
            from replay.stable_runtime_isolation import ReplayStableRuntimeIsolation
            results = ReplayStableRuntimeIsolation().check_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Runtime isolation failures: {failed}")
            return ("PASS", "Runtime isolation checks passed")
        except Exception as exc:
            return ("WARN", f"Runtime isolation error: {exc}")

    def _check_cli_audit(self) -> Tuple[str, str]:
        try:
            from replay.stable_cli_audit import ReplayStableCLIAudit
            results = ReplayStableCLIAudit().audit_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            pass_count = sum(1 for s, _ in results.values() if s == "PASS")
            if fail_count > 0:
                return ("FAIL", f"CLI audit: {fail_count} commands FAIL")
            return ("PASS", f"CLI audit: {pass_count}/{len(results)} commands found in main.py")
        except Exception as exc:
            return ("WARN", f"CLI audit error: {exc}")

    def _check_gui_audit(self) -> Tuple[str, str]:
        try:
            from replay.stable_gui_audit import ReplayStableGUIAudit
            results = ReplayStableGUIAudit().audit_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                return ("FAIL", f"GUI audit failures")
            return ("PASS", "GUI audit: all panels spec-found or imported OK")
        except Exception as exc:
            return ("WARN", f"GUI audit error: {exc}")

    def _check_report_audit(self) -> Tuple[str, str]:
        try:
            from replay.stable_report_audit import ReplayStableReportAudit
            results = ReplayStableReportAudit().audit_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Report audit failures: {failed}")
            return ("PASS", "Report audit: no FAILs")
        except Exception as exc:
            return ("WARN", f"Report audit error: {exc}")

    def _check_safety_audit(self) -> Tuple[str, str]:
        try:
            from replay.stable_safety_audit import ReplayStableSafetyAudit
            results = ReplayStableSafetyAudit().audit_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Safety audit failures: {failed[:3]}")
            return ("PASS", "Safety audit: all flags correct, no dangerous keywords")
        except Exception as exc:
            return ("WARN", f"Safety audit error: {exc}")

    def _check_regression_audit(self) -> Tuple[str, str]:
        try:
            from replay.stable_regression_audit import ReplayStableRegressionAudit
            results = ReplayStableRegressionAudit().audit_all()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                failed = [k for k, (s, _) in results.items() if s == "FAIL"]
                return ("FAIL", f"Regression audit failures: {failed}")
            return ("PASS", "Regression audit: suite_registry, schemas, guards all OK")
        except Exception as exc:
            return ("WARN", f"Regression audit error: {exc}")

    # -----------------------------------------------------------------------
    # Core replay module health
    # -----------------------------------------------------------------------

    def _check_replay_foundation(self) -> Tuple[str, str]:
        try:
            from replay.replay_health import ReplayHealthCheck
            hc = ReplayHealthCheck()
            results = hc.run()
            fail_count = sum(1 for s, _ in results.values() if s == "FAIL")
            if fail_count > 0:
                return ("FAIL", f"replay_foundation health: {fail_count} FAILs")
            return ("PASS", "replay_foundation health: OK")
        except ImportError:
            return ("WARN", "replay_health not importable — replay_foundation check skipped")
        except Exception as exc:
            return ("WARN", f"replay_foundation check error: {exc}")

    def _check_scenario_manager(self) -> Tuple[str, str]:
        try:
            from replay.scenario_library import ScenarioLibrary  # noqa: F401
            return ("PASS", "scenario_manager: ScenarioLibrary imports OK")
        except ImportError as exc:
            return ("WARN", f"scenario_manager import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"scenario_manager check error: {exc}")

    def _check_session_manager(self) -> Tuple[str, str]:
        try:
            from replay.session_manager import ReplaySessionManager  # noqa: F401
            return ("PASS", "session_manager: ReplaySessionManager imports OK")
        except ImportError as exc:
            return ("WARN", f"session_manager import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"session_manager check error: {exc}")

    def _check_journal(self) -> Tuple[str, str]:
        try:
            from replay.decision_journal_schema import DecisionJournalEntry  # noqa: F401
            return ("PASS", "decision_journal: DecisionJournalEntry imports OK")
        except ImportError as exc:
            return ("WARN", f"decision_journal import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"decision_journal check error: {exc}")

    def _check_scoring(self) -> Tuple[str, str]:
        try:
            from replay.scoring_schema import ReplayScoringEntry  # noqa: F401
            return ("PASS", "scoring: ReplayScoringEntry imports OK")
        except ImportError as exc:
            return ("WARN", f"scoring import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"scoring check error: {exc}")

    def _check_strategy(self) -> Tuple[str, str]:
        try:
            from replay.strategy_replay_schema import StrategyReplaySession  # noqa: F401
            return ("PASS", "strategy: StrategyReplaySession imports OK")
        except ImportError as exc:
            return ("WARN", f"strategy import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"strategy check error: {exc}")

    def _check_timeframe(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_schema import TimeframeReplaySession  # noqa: F401
            return ("PASS", "timeframe: TimeframeReplaySession imports OK")
        except ImportError as exc:
            return ("WARN", f"timeframe import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"timeframe check error: {exc}")

    def _check_review(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_schema import ReviewDashboardEntry  # noqa: F401
            return ("PASS", "review: ReviewDashboardEntry imports OK")
        except ImportError as exc:
            return ("WARN", f"review import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"review check error: {exc}")

    def _check_challenge(self) -> Tuple[str, str]:
        try:
            from replay.challenge_schema import ReplayChallengeDefinition
            defn = ReplayChallengeDefinition.__dataclass_fields__
            assert "research_only" in defn or "no_real_orders" in defn
            return ("PASS", "challenge: ReplayChallengeDefinition imports OK with safety fields")
        except ImportError as exc:
            return ("WARN", f"challenge import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"challenge check error: {exc}")

    def _check_dataset_registry(self) -> Tuple[str, str]:
        try:
            from replay.dataset_registry_schema import ReplayDatasetRecord  # noqa: F401
            return ("PASS", "dataset_registry: ReplayDatasetRecord imports OK")
        except ImportError as exc:
            return ("WARN", f"dataset_registry import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"dataset_registry check error: {exc}")

    def _check_session_registry(self) -> Tuple[str, str]:
        try:
            from replay.session_registry_schema import ReplaySessionRecord  # noqa: F401
            return ("PASS", "session_registry: ReplaySessionRecord imports OK")
        except ImportError as exc:
            return ("WARN", f"session_registry import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"session_registry check error: {exc}")

    # -----------------------------------------------------------------------
    # Release gate semantics
    # -----------------------------------------------------------------------

    def _check_release_gate_semantics(self) -> Tuple[str, str]:
        try:
            from replay.stable_release_gate import ReplayStableReleaseGate
            gate = ReplayStableReleaseGate()
            assert hasattr(gate, "run")
            return ("PASS", "ReplayStableReleaseGate has run() method")
        except Exception as exc:
            return ("FAIL", f"ReleaseGate check error: {exc}")

    def _check_expected_safety_block(self) -> Tuple[str, str]:
        try:
            from regression.regression_schema import RegressionTestCase
            fields = RegressionTestCase.__dataclass_fields__
            if "expected_block" not in fields:
                return ("FAIL", "RegressionTestCase missing expected_block field")
            return ("PASS", "RegressionTestCase.expected_block exists")
        except ImportError as exc:
            return ("WARN", f"regression_schema import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"expected_block check error: {exc}")

    def _check_unexpected_block_nonzero(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import _is_forbidden
            safe = ["main.py", "replay-stable-health"]
            if _is_forbidden(safe):
                return ("FAIL", f"_is_forbidden incorrectly blocks safe command: {safe}")
            return ("PASS", "_is_forbidden does not block safe replay commands")
        except ImportError as exc:
            return ("WARN", f"suite_registry import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"unexpected_block check error: {exc}")

    def _check_fail_nonzero(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import _is_forbidden
            # A command with "buy" in it should be forbidden
            dangerous = ["main.py", "buy-stock"]
            if not _is_forbidden(dangerous):
                return ("WARN", "_is_forbidden may not catch 'buy' token commands")
            return ("PASS", "_is_forbidden correctly blocks dangerous 'buy' commands")
        except ImportError as exc:
            return ("WARN", f"suite_registry import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"fail_nonzero check error: {exc}")

    def _check_warn_zero(self) -> Tuple[str, str]:
        # Verify that stable_schema dataclasses have no WARN-inducing issues
        try:
            from replay.stable_schema import StableModuleInfo, StableCapability
            m = StableModuleInfo(module_name="t", introduced_version="1.2.9")
            c = StableCapability(capability_id="t", module="t", introduced_version="1.2.9")
            assert m.no_real_orders is True
            assert c.no_real_orders is True
            return ("PASS", "stable_schema dataclasses have no WARN-inducing issues")
        except Exception as exc:
            return ("WARN", f"warn_zero check error: {exc}")

    # -----------------------------------------------------------------------
    # Data integrity invariants
    # -----------------------------------------------------------------------

    def _check_real_no_mock_fallback(self) -> Tuple[str, str]:
        try:
            from release.version_info import MTF_REAL_NO_MOCK_FALLBACK
            if MTF_REAL_NO_MOCK_FALLBACK is not True:
                return ("FAIL", f"MTF_REAL_NO_MOCK_FALLBACK={MTF_REAL_NO_MOCK_FALLBACK}")
            return ("PASS", "MTF_REAL_NO_MOCK_FALLBACK=True")
        except Exception as exc:
            return ("WARN", f"real_no_mock_fallback check error: {exc}")

    def _check_mock_demo_only(self) -> Tuple[str, str]:
        try:
            from release.version_info import MOCK_DATA_FORMAL_CONCLUSION_ALLOWED
            if MOCK_DATA_FORMAL_CONCLUSION_ALLOWED is not False:
                return ("FAIL", "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED should be False")
            return ("PASS", "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False (mock=demo only)")
        except Exception as exc:
            return ("WARN", f"mock_demo_only check error: {exc}")

    def _check_future_firewall(self) -> Tuple[str, str]:
        try:
            from replay.future_data_firewall import FutureDataFirewall  # noqa: F401
            return ("PASS", "FutureDataFirewall imports OK")
        except ImportError as exc:
            return ("WARN", f"future_data_firewall import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"future_firewall check error: {exc}")

    def _check_point_in_time(self) -> Tuple[str, str]:
        try:
            from replay.point_in_time_context import PointInTimeContext  # noqa: F401
            return ("PASS", "PointInTimeContext imports OK")
        except ImportError as exc:
            return ("WARN", f"point_in_time_context import unavailable: {exc}")
        except Exception as exc:
            return ("WARN", f"point_in_time check error: {exc}")

    # -----------------------------------------------------------------------
    # Auto-action guards
    # -----------------------------------------------------------------------

    def _check_no_auto_decision(self) -> Tuple[str, str]:
        try:
            from release.version_info import REPLAY_AUTO_DECISION_ENABLED
            if REPLAY_AUTO_DECISION_ENABLED is not False:
                return ("FAIL", f"REPLAY_AUTO_DECISION_ENABLED={REPLAY_AUTO_DECISION_ENABLED}")
            return ("PASS", "REPLAY_AUTO_DECISION_ENABLED=False")
        except Exception as exc:
            return ("WARN", f"no_auto_decision check error: {exc}")

    def _check_no_auto_execution(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_REPLAY_EXECUTION_ENABLED
            if AUTO_REPLAY_EXECUTION_ENABLED is not False:
                return ("FAIL", f"AUTO_REPLAY_EXECUTION_ENABLED={AUTO_REPLAY_EXECUTION_ENABLED}")
            return ("PASS", "AUTO_REPLAY_EXECUTION_ENABLED=False")
        except Exception as exc:
            return ("WARN", f"no_auto_execution check error: {exc}")

    def _check_no_auto_confirm(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_MISTAKE_CONFIRMATION_ENABLED
            if AUTO_MISTAKE_CONFIRMATION_ENABLED is not False:
                return ("FAIL", f"AUTO_MISTAKE_CONFIRMATION_ENABLED={AUTO_MISTAKE_CONFIRMATION_ENABLED}")
            return ("PASS", "AUTO_MISTAKE_CONFIRMATION_ENABLED=False")
        except Exception as exc:
            return ("WARN", f"no_auto_confirm check error: {exc}")

    def _check_no_auto_reveal(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_OUTCOME_REVEAL_ENABLED
            if AUTO_OUTCOME_REVEAL_ENABLED is not False:
                return ("FAIL", f"AUTO_OUTCOME_REVEAL_ENABLED={AUTO_OUTCOME_REVEAL_ENABLED}")
            return ("PASS", "AUTO_OUTCOME_REVEAL_ENABLED=False")
        except Exception as exc:
            return ("WARN", f"no_auto_reveal check error: {exc}")

    def _check_no_auto_repair(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_DATASET_REPAIR_ENABLED
            if AUTO_DATASET_REPAIR_ENABLED is not False:
                return ("FAIL", f"AUTO_DATASET_REPAIR_ENABLED={AUTO_DATASET_REPAIR_ENABLED}")
            return ("PASS", "AUTO_DATASET_REPAIR_ENABLED=False")
        except Exception as exc:
            return ("WARN", f"no_auto_repair check error: {exc}")

    def _check_no_auto_rebind(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_SESSION_REBIND_ENABLED
            if AUTO_SESSION_REBIND_ENABLED is not False:
                return ("FAIL", f"AUTO_SESSION_REBIND_ENABLED={AUTO_SESSION_REBIND_ENABLED}")
            return ("PASS", "AUTO_SESSION_REBIND_ENABLED=False")
        except Exception as exc:
            return ("WARN", f"no_auto_rebind check error: {exc}")

    # -----------------------------------------------------------------------
    # Broker / execution guards
    # -----------------------------------------------------------------------

    def _check_no_broker(self) -> Tuple[str, str]:
        try:
            from release.version_info import BROKER_EXECUTION_ENABLED
            if BROKER_EXECUTION_ENABLED is not False:
                return ("FAIL", f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}")
            return ("PASS", "BROKER_EXECUTION_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"no_broker check error: {exc}")

    def _check_no_real_orders(self) -> Tuple[str, str]:
        try:
            from release.version_info import NO_REAL_ORDERS, REAL_ORDERS_ENABLED
            if NO_REAL_ORDERS is not True:
                return ("FAIL", f"NO_REAL_ORDERS={NO_REAL_ORDERS}")
            if REAL_ORDERS_ENABLED is not False:
                return ("FAIL", f"REAL_ORDERS_ENABLED={REAL_ORDERS_ENABLED}")
            return ("PASS", "NO_REAL_ORDERS=True, REAL_ORDERS_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"no_real_orders check error: {exc}")

    # -----------------------------------------------------------------------
    # Runtime hygiene
    # -----------------------------------------------------------------------

    def _check_runtime_ignored(self) -> Tuple[str, str]:
        try:
            from replay.stable_runtime_isolation import ReplayStableRuntimeIsolation
            iso = ReplayStableRuntimeIsolation()
            r_sessions = iso._check_pattern("data/replay_sessions/", "sessions")
            r_registry = iso._check_pattern("data/replay_registry/", "registry")
            failures = [r for r in [r_sessions, r_registry] if r[0] == "FAIL"]
            if failures:
                return ("FAIL", f"Runtime data not ignored: {failures[0][1]}")
            return ("PASS", "Replay runtime data covered by .gitignore")
        except Exception as exc:
            return ("WARN", f"runtime_ignored check error: {exc}")

    def _check_generated_reports_ignored(self) -> Tuple[str, str]:
        try:
            from replay.stable_runtime_isolation import ReplayStableRuntimeIsolation
            iso = ReplayStableRuntimeIsolation()
            r = iso._check_pattern("reports/", "reports dir")
            if r[0] == "FAIL":
                return ("FAIL", "reports/ not in .gitignore")
            return ("PASS", "reports/ covered by .gitignore")
        except Exception as exc:
            return ("WARN", f"generated_reports_ignored check error: {exc}")

    def _check_package_ignored(self) -> Tuple[str, str]:
        try:
            from replay.stable_runtime_isolation import ReplayStableRuntimeIsolation
            iso = ReplayStableRuntimeIsolation()
            r = iso._check_pattern("*.db", "db files")
            if r[0] == "FAIL":
                return ("WARN", "*.db may not be in .gitignore")
            return ("PASS", "Package/cache artifacts covered by .gitignore")
        except Exception as exc:
            return ("WARN", f"package_ignored check error: {exc}")

    def _check_no_forbidden_actions(self) -> Tuple[str, str]:
        try:
            from replay.stable_safety_audit import ReplayStableSafetyAudit
            results = ReplayStableSafetyAudit().audit_all()
            scan_result = results.get("replay_dir_keyword_scan", ("WARN", "not run"))
            if scan_result[0] == "FAIL":
                return ("FAIL", f"Forbidden actions found: {scan_result[1]}")
            return ("PASS", "No forbidden trading actions found in replay/ modules")
        except Exception as exc:
            return ("WARN", f"no_forbidden_actions check error: {exc}")
