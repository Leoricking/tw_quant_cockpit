"""
release/failure_injection_recovery_release_gate_v165.py — Failure Injection & Recovery Release Gate v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] 45/45 gate checks. All must PASS for release gate to clear.
[!] REAL_FAILURE_INJECTION_ENABLED = False. PRODUCTION_CHAOS_ENABLED = False.
"""
from __future__ import annotations

from typing import Any, Dict, List

REAL_FAILURE_INJECTION_ENABLED = False
PRODUCTION_CHAOS_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


def _pass(detail: str = "") -> Dict[str, str]:
    return {"status": "PASS", "detail": detail}


def _fail(detail: str = "") -> Dict[str, str]:
    return {"status": "FAIL", "detail": detail}


class FailureInjectionRecoveryReleaseGateV165:
    """
    Release gate with 45 checks for the Failure Injection & Recovery Validation subsystem.
    All checks must PASS for the gate to clear (gate_passed=True).
    """

    EXPECTED_CHECKS = 45

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, Dict[str, str]] = {}

        # ---- Version checks (5) ----
        checks["version_is_165"] = self._check_version()
        checks["release_name_correct"] = self._check_release_name()
        checks["base_release_correct"] = self._check_base_release()
        checks["operational_analytics_baseline_set"] = self._check_analytics_baseline()
        checks["failure_injection_baseline_set"] = self._check_fi_baseline()

        # ---- Safety flag checks (10) ----
        checks["real_failure_injection_disabled"] = self._check_flag("REAL_FAILURE_INJECTION_ENABLED", False)
        checks["production_chaos_disabled"] = self._check_flag("PRODUCTION_CHAOS_ENABLED", False)
        checks["production_recovery_disabled"] = self._check_flag("PRODUCTION_RECOVERY_ENABLED", False)
        checks["auto_recovery_disabled"] = self._check_flag("AUTO_RECOVERY_EXECUTION_ENABLED", False)
        checks["auto_failover_disabled"] = self._check_flag("AUTO_FAILOVER_ENABLED", False)
        checks["auto_restart_disabled"] = self._check_flag("AUTO_RESTART_ENABLED", False)
        checks["auto_resume_running_disabled"] = self._check_flag("AUTO_RESUME_RUNNING", False)
        checks["broker_injection_disabled"] = self._check_flag("BROKER_FAILURE_INJECTION_ENABLED", False)
        checks["network_injection_disabled"] = self._check_flag("NETWORK_FAILURE_INJECTION_ENABLED", False)
        checks["external_mutation_disabled"] = self._check_flag("EXTERNAL_SYSTEM_MUTATION_ENABLED", False)

        # ---- Package checks (5) ----
        checks["package_importable"] = self._check_package_import()
        checks["enums_importable"] = self._check_module_import("paper_trading.failure_validation.enums_v165")
        checks["models_importable"] = self._check_module_import("paper_trading.failure_validation.models_v165")
        checks["injector_importable"] = self._check_module_import("paper_trading.failure_validation.injector_v165")
        checks["health_importable"] = self._check_module_import("paper_trading.failure_validation.health_v165")

        # ---- Enum correctness (5) ----
        checks["failure_domain_17"] = self._check_enum_count("paper_trading.failure_validation.enums_v165", "FailureDomain", 17)
        checks["failure_type_28"] = self._check_enum_count("paper_trading.failure_validation.enums_v165", "FailureType", 28)
        checks["failure_severity_5"] = self._check_enum_count("paper_trading.failure_validation.enums_v165", "FailureSeverity", 5)
        checks["expected_outcome_9"] = self._check_enum_count("paper_trading.failure_validation.enums_v165", "ExpectedOutcome", 9)
        checks["recovery_state_8"] = self._check_enum_count("paper_trading.failure_validation.enums_v165", "RecoveryState", 8)

        # ---- Scorecard checks (3) ----
        checks["scorecard_weights_sum_100"] = self._check_scorecard_weights()
        checks["scorecard_10_dimensions"] = self._check_scorecard_dimensions()
        checks["scorecard_computes"] = self._check_scorecard_compute()

        # ---- Scenario registry checks (3) ----
        checks["scenario_count_ge_60"] = self._check_scenario_count()
        checks["all_scenarios_safety_markers"] = self._check_all_scenario_markers()
        checks["cascading_scenarios_ge_6"] = self._check_cascading_count()

        # ---- Safety precheck checks (3) ----
        checks["precheck_blocks_unsafe"] = self._check_precheck_blocks()
        checks["precheck_passes_safe"] = self._check_precheck_passes()
        checks["precheck_blocked_by_safety_label"] = self._check_precheck_label()

        # ---- Injector checks (3) ----
        checks["injector_deterministic"] = self._check_injector_deterministic()
        checks["injector_bounded"] = self._check_injector_bounded()
        checks["injector_blocked_by_safety"] = self._check_injector_blocked()

        # ---- Recovery validator checks (3) ----
        checks["invalid_transition_blocked"] = self._check_invalid_transition()
        checks["verification_required_transition"] = self._check_verification_required()
        checks["recovery_validation_runs"] = self._check_recovery_validation()

        # ---- Health check checks (3) ----
        checks["health_check_runs"] = self._check_health_runs()
        checks["health_check_50_checks"] = self._check_health_count()
        checks["health_check_passes"] = self._check_health_passes()

        # ---- Module count check (1) ----
        checks["module_count_ge_62"] = self._check_module_count()

        # ---- Store checks (1) ----
        checks["store_no_production_db"] = self._check_store()

        total = len(checks)
        assert total == self.EXPECTED_CHECKS, f"Expected {self.EXPECTED_CHECKS} checks, got {total}"

        failed = {k: v for k, v in checks.items() if v["status"] != "PASS"}
        passed_count = total - len(failed)

        return {
            "gate_name": "FailureInjectionRecoveryReleaseGateV165",
            "version": "1.6.5",
            "total": total,
            "passed": passed_count,
            "failed": len(failed),
            "all_pass": len(failed) == 0,
            "gate_passed": len(failed) == 0,
            "checks": checks,
            "failed_checks": list(failed.keys()),
        }

    # ---- Version checks ----

    def _check_version(self) -> Dict[str, str]:
        try:
            from release.version_info import VERSION
            if VERSION >= "1.6.5":
                return _pass(f"VERSION={VERSION} >= 1.6.5")
            return _fail(f"Expected >= 1.6.5, got {VERSION}")
        except Exception as e:
            return _fail(str(e))

    def _check_release_name(self) -> Dict[str, str]:
        try:
            from release.version_info import RELEASE_NAME
            _known = {"Failure Injection & Recovery Validation", "Multi-session Coordination"}
            if RELEASE_NAME in _known:
                return _pass(f"RELEASE_NAME={RELEASE_NAME}")
            return _fail(f"Got: {RELEASE_NAME}")
        except Exception as e:
            return _fail(str(e))

    def _check_base_release(self) -> Dict[str, str]:
        try:
            from release.version_info import BASE_RELEASE
            if "1.6.4" in BASE_RELEASE or "1.6.5" in BASE_RELEASE:
                return _pass(f"BASE_RELEASE: {BASE_RELEASE}")
            return _fail(f"BASE_RELEASE should contain 1.6.4 or 1.6.5: {BASE_RELEASE}")
        except Exception as e:
            return _fail(str(e))

    def _check_analytics_baseline(self) -> Dict[str, str]:
        try:
            from release.version_info import OPERATIONAL_ANALYTICS_BASELINE
            if OPERATIONAL_ANALYTICS_BASELINE == "1.6.4":
                return _pass("OPERATIONAL_ANALYTICS_BASELINE=1.6.4")
            return _fail(f"Got: {OPERATIONAL_ANALYTICS_BASELINE}")
        except Exception as e:
            return _fail(str(e))

    def _check_fi_baseline(self) -> Dict[str, str]:
        try:
            from release.version_info import FAILURE_INJECTION_RECOVERY_BASELINE
            if FAILURE_INJECTION_RECOVERY_BASELINE == "1.6.5":
                return _pass("FAILURE_INJECTION_RECOVERY_BASELINE=1.6.5")
            return _fail(f"Got: {FAILURE_INJECTION_RECOVERY_BASELINE}")
        except Exception as e:
            return _fail(str(e))

    # ---- Safety flag checks ----

    def _check_flag(self, flag_name: str, expected: bool) -> Dict[str, str]:
        try:
            from release import version_info
            val = getattr(version_info, flag_name, None)
            if val is None:
                return _fail(f"{flag_name} not found in version_info")
            if val == expected:
                return _pass(f"{flag_name}={val}")
            return _fail(f"{flag_name}={val}, expected {expected}")
        except Exception as e:
            return _fail(str(e))

    # ---- Package/module checks ----

    def _check_package_import(self) -> Dict[str, str]:
        try:
            import paper_trading.failure_validation as pkg
            if pkg.REAL_FAILURE_INJECTION_ENABLED is False:
                return _pass("Package importable, REAL_FAILURE_INJECTION_ENABLED=False")
            return _fail("REAL_FAILURE_INJECTION_ENABLED must be False")
        except Exception as e:
            return _fail(str(e))

    def _check_module_import(self, module_path: str) -> Dict[str, str]:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            return _pass(f"{module_path} importable")
        except Exception as e:
            return _fail(f"{module_path}: {e}")

    # ---- Enum checks ----

    def _check_enum_count(self, module_path: str, enum_name: str, expected: int) -> Dict[str, str]:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            enum_cls = getattr(mod, enum_name)
            count = len(list(enum_cls))
            if count == expected:
                return _pass(f"{enum_name} has {count} members")
            return _fail(f"{enum_name}: expected {expected}, got {count}")
        except Exception as e:
            return _fail(str(e))

    # ---- Scorecard checks ----

    def _check_scorecard_weights(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.enums_v165 import SCORECARD_WEIGHTS
            total = sum(SCORECARD_WEIGHTS.values())
            if total == 100:
                return _pass(f"Scorecard weights sum={total}")
            return _fail(f"Scorecard weights sum={total}, expected 100")
        except Exception as e:
            return _fail(str(e))

    def _check_scorecard_dimensions(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.enums_v165 import SCORECARD_WEIGHTS
            if len(SCORECARD_WEIGHTS) == 10:
                return _pass("Scorecard has 10 dimensions")
            return _fail(f"Expected 10 dimensions, got {len(SCORECARD_WEIGHTS)}")
        except Exception as e:
            return _fail(str(e))

    def _check_scorecard_compute(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.models_v165 import FailureScorecard
            from paper_trading.failure_validation.enums_v165 import ScorecardDimension
            sc = FailureScorecard()
            for dim in ScorecardDimension:
                sc.dimension_scores[dim.value] = 100
            total = sc.compute()
            if total == 100:
                return _pass(f"Scorecard.compute()={total}")
            return _fail(f"Expected 100, got {total}")
        except Exception as e:
            return _fail(str(e))

    # ---- Scenario registry checks ----

    def _check_scenario_count(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.scenario_registry_v165 import BUILTIN_SCENARIOS
            n = len(BUILTIN_SCENARIOS)
            if n >= 60:
                return _pass(f"BUILTIN_SCENARIOS={n} (≥60)")
            return _fail(f"Expected ≥60, got {n}")
        except Exception as e:
            return _fail(str(e))

    def _check_all_scenario_markers(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.scenario_registry_v165 import BUILTIN_SCENARIOS
            bad = [s.name for s in BUILTIN_SCENARIOS if not s.all_safety_markers_set()]
            if not bad:
                return _pass("All scenarios have all 10 safety markers set")
            return _fail(f"Scenarios missing markers: {bad[:3]}")
        except Exception as e:
            return _fail(str(e))

    def _check_cascading_count(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.scenario_registry_v165 import get_cascading_scenarios
            n = len(get_cascading_scenarios())
            if n >= 6:
                return _pass(f"Cascading scenarios={n} (≥6)")
            return _fail(f"Expected ≥6, got {n}")
        except Exception as e:
            return _fail(str(e))

    # ---- Safety precheck checks ----

    def _check_precheck_blocks(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.safety_precheck_v165 import run_safety_precheck
            from paper_trading.failure_validation.models_v165 import FailureInjectionRequest
            req = FailureInjectionRequest(fixture_only=False, scenario=None)
            r = run_safety_precheck(req)
            if not r.passed:
                return _pass("Precheck blocks unsafe request")
            return _fail("Should have blocked")
        except Exception as e:
            return _fail(str(e))

    def _check_precheck_passes(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.safety_precheck_v165 import run_safety_precheck
            from paper_trading.failure_validation.models_v165 import FailureInjectionRequest, FailureScenario
            from paper_trading.failure_validation.enums_v165 import FailureDomain, FailureType, FailureSeverity, ExpectedOutcome
            s = FailureScenario(domain=FailureDomain.MARKET_DATA, failure_type=FailureType.TIMEOUT,
                                severity=FailureSeverity.LOW, expected_outcomes=[ExpectedOutcome.DETECTED])
            req = FailureInjectionRequest(scenario=s)
            r = run_safety_precheck(req)
            if r.passed:
                return _pass("Precheck passes safe request")
            return _fail(f"Should have passed: {r.violations}")
        except Exception as e:
            return _fail(str(e))

    def _check_precheck_label(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.safety_precheck_v165 import run_safety_precheck
            from paper_trading.failure_validation.models_v165 import FailureInjectionRequest
            req = FailureInjectionRequest(fixture_only=False, scenario=None)
            r = run_safety_precheck(req)
            if r.blocked_reason and "BLOCKED_BY_SAFETY" in r.blocked_reason:
                return _pass("blocked_reason has BLOCKED_BY_SAFETY label")
            return _fail(f"blocked_reason: {r.blocked_reason!r}")
        except Exception as e:
            return _fail(str(e))

    # ---- Injector checks ----

    def _check_injector_deterministic(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector
            from paper_trading.failure_validation.models_v165 import FailureInjectionRequest, FailureScenario
            from paper_trading.failure_validation.enums_v165 import FailureDomain, FailureType, FailureSeverity, ExpectedOutcome
            s = FailureScenario(domain=FailureDomain.MARKET_DATA, failure_type=FailureType.TIMEOUT,
                                severity=FailureSeverity.LOW, expected_outcomes=[ExpectedOutcome.DETECTED], seed=99)
            r1 = DeterministicFailureInjector().inject(FailureInjectionRequest(scenario=s))
            r2 = DeterministicFailureInjector().inject(FailureInjectionRequest(scenario=s))
            if r1.detection_confirmed == r2.detection_confirmed:
                return _pass("Injector deterministic")
            return _fail("Injector non-deterministic")
        except Exception as e:
            return _fail(str(e))

    def _check_injector_bounded(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.scenario_registry_v165 import BUILTIN_SCENARIOS
            unbounded = [s for s in BUILTIN_SCENARIOS if s.max_duration_ms > 60000]
            if not unbounded:
                return _pass("All scenarios bounded ≤60000ms")
            return _fail(f"Unbounded scenarios: {[s.name for s in unbounded[:2]]}")
        except Exception as e:
            return _fail(str(e))

    def _check_injector_blocked(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector
            from paper_trading.failure_validation.models_v165 import FailureInjectionRequest, FailureScenario
            from paper_trading.failure_validation.enums_v165 import (
                FailureDomain, FailureType, FailureSeverity, ExpectedOutcome, InjectionStatus
            )
            s = FailureScenario(domain=FailureDomain.MARKET_DATA, failure_type=FailureType.TIMEOUT,
                                severity=FailureSeverity.LOW, expected_outcomes=[ExpectedOutcome.DETECTED],
                                fixture_only=False)
            r = DeterministicFailureInjector().inject(FailureInjectionRequest(scenario=s, fixture_only=False))
            if r.status == InjectionStatus.BLOCKED_BY_SAFETY:
                return _pass("Injector returns BLOCKED_BY_SAFETY")
            return _fail(f"Expected BLOCKED_BY_SAFETY, got {r.status}")
        except Exception as e:
            return _fail(str(e))

    # ---- Recovery validator checks ----

    def _check_invalid_transition(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
            from paper_trading.failure_validation.enums_v165 import RecoveryState
            v = RecoveryValidator()
            allowed, _ = v.validate_transition(RecoveryState.FAILED, RecoveryState.HEALTHY)
            if not allowed:
                return _pass("FAILED→HEALTHY blocked")
            return _fail("FAILED→HEALTHY should be blocked")
        except Exception as e:
            return _fail(str(e))

    def _check_verification_required(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
            from paper_trading.failure_validation.enums_v165 import RecoveryState
            v = RecoveryValidator()
            allowed, _ = v.validate_transition(RecoveryState.RECOVERING, RecoveryState.RECOVERED, False)
            if not allowed:
                return _pass("RECOVERING→RECOVERED without verification blocked")
            return _fail("Should be blocked without verification")
        except Exception as e:
            return _fail(str(e))

    def _check_recovery_validation(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
            from paper_trading.failure_validation.models_v165 import FailureInjectionResult
            from paper_trading.failure_validation.enums_v165 import InjectionStatus, RecoveryState
            from decimal import Decimal
            result = FailureInjectionResult(
                status=InjectionStatus.CONTAINED,
                detection_confirmed=True,
                containment_confirmed=True,
                recovery_triggered=True,
            )
            v = RecoveryValidator()
            plan = v.build_recovery_plan(result, Decimal("2000"), Decimal("500"))
            vr = v.execute_validation(plan, result, RecoveryState.DEGRADED)
            if vr.final_state is not None:
                return _pass(f"Recovery validation ran: final_state={vr.final_state.value}")
            return _fail("final_state is None")
        except Exception as e:
            return _fail(str(e))

    # ---- Health check checks ----

    def _check_health_runs(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.health_v165 import FailureInjectionRecoveryHealthCheck
            summary = FailureInjectionRecoveryHealthCheck().get_health_summary()
            if isinstance(summary, dict) and "total" in summary:
                return _pass("Health check runs")
            return _fail("Health check did not return expected dict")
        except Exception as e:
            return _fail(str(e))

    def _check_health_count(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.health_v165 import FailureInjectionRecoveryHealthCheck
            summary = FailureInjectionRecoveryHealthCheck().get_health_summary()
            total = summary.get("total", 0)
            if total >= 50:
                return _pass(f"Health check has {total} checks (≥50)")
            return _fail(f"Expected ≥50 checks, got {total}")
        except Exception as e:
            return _fail(str(e))

    def _check_health_passes(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.health_v165 import FailureInjectionRecoveryHealthCheck
            summary = FailureInjectionRecoveryHealthCheck().get_health_summary()
            failed = summary.get("failed", 0)
            if failed == 0:
                return _pass(f"Health check: 0 failures (all pass)")
            failed_names = [k for k, v in summary.get("checks", {}).items() if v["status"] != "PASS"]
            return _fail(f"Health check has {failed} failure(s): {failed_names[:3]}")
        except Exception as e:
            return _fail(str(e))

    # ---- Module count check ----

    def _check_module_count(self) -> Dict[str, str]:
        try:
            import os
            pkg_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "paper_trading", "failure_validation",
            )
            py_files = [f for f in os.listdir(pkg_dir) if f.endswith(".py")]
            count = len(py_files)
            if count >= 62:
                return _pass(f"Module count={count} (≥62)")
            return _fail(f"Expected ≥62 modules, got {count}")
        except Exception as e:
            return _fail(str(e))

    # ---- Store check ----

    def _check_store(self) -> Dict[str, str]:
        try:
            from paper_trading.failure_validation.store_v165 import PRODUCTION_DB_ENABLED
            if not PRODUCTION_DB_ENABLED:
                return _pass("Store PRODUCTION_DB_ENABLED=False")
            return _fail("Store PRODUCTION_DB_ENABLED must be False")
        except Exception as e:
            return _fail(str(e))
