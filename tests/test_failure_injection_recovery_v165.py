"""
tests/test_failure_injection_recovery_v165.py — Main integration & identity tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
[!] Version, release identity, baseline integration, end-to-end chain, safety summary, regression contract.
"""
from decimal import Decimal

import pytest

from release.version_info import VERSION

# ---------------------------------------------------------------------------
# Version & Release Identity
# ---------------------------------------------------------------------------

class TestVersionIdentity:
    def test_version_is_165(self):
        assert VERSION == "1.6.5"

    def test_version_format(self):
        parts = VERSION.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_version_info_165_flags(self):
        from release.version_info import (
            REAL_FAILURE_INJECTION_ENABLED,
            PRODUCTION_CHAOS_ENABLED,
            FAILURE_INJECTION_RESEARCH_ONLY,
        )
        assert REAL_FAILURE_INJECTION_ENABLED is False
        assert PRODUCTION_CHAOS_ENABLED is False
        assert FAILURE_INJECTION_RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# Baseline: package imports
# ---------------------------------------------------------------------------

class TestBaselineImports:
    def test_enums_importable(self):
        from paper_trading.failure_validation.enums_v165 import FailureDomain, FailureType
        assert FailureDomain is not None

    def test_models_importable(self):
        from paper_trading.failure_validation.models_v165 import FailureScenario
        assert FailureScenario is not None

    def test_safety_precheck_importable(self):
        from paper_trading.failure_validation.safety_precheck_v165 import run_safety_precheck
        assert callable(run_safety_precheck)

    def test_injector_importable(self):
        from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector
        assert DeterministicFailureInjector is not None

    def test_scenario_registry_importable(self):
        from paper_trading.failure_validation.scenario_registry_v165 import BUILTIN_SCENARIOS
        assert len(BUILTIN_SCENARIOS) >= 60

    def test_recovery_validator_importable(self):
        from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
        assert RecoveryValidator is not None

    def test_scorecard_importable(self):
        from paper_trading.failure_validation.scorecard_v165 import compute_scorecard
        assert callable(compute_scorecard)

    def test_cascading_importable(self):
        from paper_trading.failure_validation.cascading_v165 import simulate_cascading_failure
        assert callable(simulate_cascading_failure)

    def test_health_importable(self):
        from paper_trading.failure_validation.health_v165 import FailureInjectionRecoveryHealthCheck
        assert FailureInjectionRecoveryHealthCheck is not None

    def test_release_gate_importable(self):
        from release.failure_injection_recovery_release_gate_v165 import FailureInjectionRecoveryReleaseGateV165
        assert FailureInjectionRecoveryReleaseGateV165 is not None

    def test_gui_panel_importable(self):
        from gui.failure_injection_recovery_panel import FailureInjectionRecoveryPanel
        assert FailureInjectionRecoveryPanel is not None


# ---------------------------------------------------------------------------
# Integration: Vertical slice — stale data injection → full chain
# ---------------------------------------------------------------------------

class TestVerticalSliceIntegration:
    """Tests the complete chain: Baseline → Safety → Inject → Detect → Contain → Recover → Score."""

    def _make_stale_scenario(self):
        from paper_trading.failure_validation.scenario_registry_v165 import get_scenario
        return get_scenario("md_stale_001")

    def test_slice_baseline_snapshot(self):
        from paper_trading.failure_validation.baseline_snapshot_v165 import BaselineSnapshotManager
        mgr = BaselineSnapshotManager()
        snap = mgr.capture("market_data", {"price": 100, "ts": "2024-01-01"}, seed=42)
        assert snap is not None
        assert snap.verify_integrity() is True

    def test_slice_safety_precheck_passes(self):
        from paper_trading.failure_validation.safety_precheck_v165 import run_safety_precheck
        from paper_trading.failure_validation.models_v165 import FailureInjectionRequest
        s = self._make_stale_scenario()
        req = FailureInjectionRequest(scenario=s)
        result = run_safety_precheck(req)
        assert result.passed is True

    def test_slice_injection(self):
        from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector
        from paper_trading.failure_validation.models_v165 import FailureInjectionRequest
        from paper_trading.failure_validation.enums_v165 import InjectionStatus
        s = self._make_stale_scenario()
        req = FailureInjectionRequest(scenario=s)
        inj = DeterministicFailureInjector()
        result = inj.inject(req)
        assert result.status != InjectionStatus.BLOCKED_BY_SAFETY

    def test_slice_detection_confirmed(self):
        from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector
        from paper_trading.failure_validation.models_v165 import FailureInjectionRequest
        s = self._make_stale_scenario()
        result = DeterministicFailureInjector().inject(FailureInjectionRequest(scenario=s))
        # Detection confirmed is set based on deterministic seed
        assert isinstance(result.detection_confirmed, bool)

    def test_slice_containment(self):
        from paper_trading.failure_validation.containment_v165 import simulate_containment
        result = simulate_containment("market_data", detection_confirmed=True, seed=42)
        assert result.contained is True

    def test_slice_recovery_plan(self):
        from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
        from paper_trading.failure_validation.models_v165 import FailureInjectionResult
        from paper_trading.failure_validation.enums_v165 import InjectionStatus
        inj_result = FailureInjectionResult(
            detection_confirmed=True,
            containment_confirmed=True,
            recovery_triggered=True,
            status=InjectionStatus.CONTAINED,
        )
        rv = RecoveryValidator()
        plan = rv.build_recovery_plan(inj_result, rto_budget_ms=Decimal("5000"))
        assert plan is not None
        assert plan.auto_execution_enabled is False

    def test_slice_recovery_execution(self):
        from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
        from paper_trading.failure_validation.models_v165 import FailureInjectionResult
        from paper_trading.failure_validation.enums_v165 import InjectionStatus, RecoveryState
        inj_result = FailureInjectionResult(
            detection_confirmed=True,
            containment_confirmed=True,
            recovery_triggered=True,
            status=InjectionStatus.CONTAINED,
        )
        rv = RecoveryValidator()
        plan = rv.build_recovery_plan(inj_result)
        vr = rv.execute_validation(plan, inj_result, seed=42)
        assert vr.final_state is not None

    def test_slice_scorecard(self):
        from paper_trading.failure_validation.scorecard_v165 import compute_scorecard
        from paper_trading.failure_validation.models_v165 import FailureInjectionResult, RecoveryValidationResult
        from paper_trading.failure_validation.enums_v165 import InjectionStatus, RecoveryState
        inj_result = FailureInjectionResult(
            detection_confirmed=True,
            alert_generated=True,
            containment_confirmed=True,
            status=InjectionStatus.CONTAINED,
        )
        vr = RecoveryValidationResult(
            final_state=RecoveryState.RECOVERED,
            data_reconciled=True,
            replay_verified=True,
            idempotency_verified=True,
            rto_met=True,
            rpo_met=True,
        )
        sc = compute_scorecard(inj_result, vr)
        assert sc.total_score == 100

    def test_slice_replay(self):
        from paper_trading.failure_validation.replay_v165 import simulate_replay
        result = simulate_replay("md_stale_001", seed=1002, original_events=5)
        assert result.match is True

    def test_slice_report(self):
        from paper_trading.failure_validation.report_v165 import FailureInjectionReport, ReportStore
        report = FailureInjectionReport(run_id="integration_1", scenario_name="md_stale_001")
        report.add_section("Detection", {"detected": True})
        report.add_section("Recovery", {"state": "RECOVERED"})
        store = ReportStore()
        store.store(report)
        assert store.count() == 1
        assert report.summary()["sections"] == 2


# ---------------------------------------------------------------------------
# End-to-end: Cascading failure
# ---------------------------------------------------------------------------

class TestE2ECascadingFailure:
    def test_cascading_chain_runs(self):
        from paper_trading.failure_validation.cascading_v165 import simulate_cascading_failure
        from paper_trading.failure_validation.scenario_registry_v165 import get_scenario
        s = get_scenario("casc_md_signal_order_001")
        result = simulate_cascading_failure(s, seed=42)
        assert result is not None
        assert result["chain_length"] >= 1

    def test_cascading_full_chain(self):
        from paper_trading.failure_validation.cascading_v165 import simulate_cascading_failure
        from paper_trading.failure_validation.scenario_registry_v165 import get_scenario
        s = get_scenario("casc_md_signal_alert_incident_001")
        result = simulate_cascading_failure(s, seed=42)
        assert result["chain_length"] >= 1
        assert "primary_detected" in result
        assert "all_contained" in result


# ---------------------------------------------------------------------------
# Safety Summary: global safety audit
# ---------------------------------------------------------------------------

class TestSafetySummary:
    def test_no_broker_domain_in_permitted(self):
        from paper_trading.failure_validation.enums_v165 import PERMITTED_DOMAINS, FORBIDDEN_DOMAINS
        assert "BROKER" in FORBIDDEN_DOMAINS
        assert "BROKER" not in PERMITTED_DOMAINS

    def test_auto_resume_globally_disabled(self):
        from paper_trading.failure_validation.enums_v165 import AUTO_RESUME_RUNNING_ENABLED
        assert AUTO_RESUME_RUNNING_ENABLED is False

    def test_all_safety_flags_false_across_modules(self):
        from paper_trading.failure_validation.enums_v165 import (
            REAL_FAILURE_INJECTION_ENABLED, PRODUCTION_CHAOS_ENABLED
        )
        from paper_trading.failure_validation.safety_precheck_v165 import (
            PRODUCTION_RECOVERY_ENABLED, AUTO_RECOVERY_EXECUTION_ENABLED,
            AUTO_FAILOVER_ENABLED, AUTO_RESTART_ENABLED, BROKER_FAILURE_INJECTION_ENABLED,
            NETWORK_FAILURE_INJECTION_ENABLED, EXTERNAL_SYSTEM_MUTATION_ENABLED,
        )
        assert REAL_FAILURE_INJECTION_ENABLED is False
        assert PRODUCTION_CHAOS_ENABLED is False
        assert PRODUCTION_RECOVERY_ENABLED is False
        assert AUTO_RECOVERY_EXECUTION_ENABLED is False
        assert AUTO_FAILOVER_ENABLED is False
        assert AUTO_RESTART_ENABLED is False
        assert BROKER_FAILURE_INJECTION_ENABLED is False
        assert NETWORK_FAILURE_INJECTION_ENABLED is False
        assert EXTERNAL_SYSTEM_MUTATION_ENABLED is False

    def test_failed_to_healthy_transition_blocked(self):
        from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
        from paper_trading.failure_validation.enums_v165 import RecoveryState
        rv = RecoveryValidator()
        allowed, _ = rv.validate_transition(RecoveryState.FAILED, RecoveryState.HEALTHY)
        assert allowed is False

    def test_recovery_plan_auto_execution_always_false(self):
        from paper_trading.failure_validation.models_v165 import RecoveryPlan
        plan = RecoveryPlan()
        assert plan.auto_execution_enabled is False

    def test_cascading_module_safety_flags(self):
        from paper_trading.failure_validation.cascading_v165 import (
            REAL_FAILURE_INJECTION_ENABLED, PAPER_ONLY, RESEARCH_ONLY
        )
        assert REAL_FAILURE_INJECTION_ENABLED is False
        assert PAPER_ONLY is True
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# Regression Contract: counts and thresholds
# ---------------------------------------------------------------------------

class TestRegressionContract:
    def test_scenario_count_ge_60(self):
        from paper_trading.failure_validation.scenario_registry_v165 import scenario_count
        assert scenario_count() >= 60

    def test_scorecard_weights_sum_100(self):
        from paper_trading.failure_validation.enums_v165 import SCORECARD_WEIGHTS
        assert sum(SCORECARD_WEIGHTS.values()) == 100

    def test_failure_domain_count_17(self):
        from paper_trading.failure_validation.enums_v165 import FailureDomain
        assert len(FailureDomain) == 17

    def test_failure_type_count_28(self):
        from paper_trading.failure_validation.enums_v165 import FailureType
        assert len(FailureType) == 28

    def test_recovery_state_count_8(self):
        from paper_trading.failure_validation.enums_v165 import RecoveryState
        assert len(RecoveryState) == 8

    def test_circuit_breaker_states_3(self):
        from paper_trading.failure_validation.enums_v165 import CircuitBreakerState
        assert len(CircuitBreakerState) == 3

    def test_gui_tabs_16(self):
        from gui.failure_injection_recovery_panel import tab_count
        assert tab_count() == 16

    def test_health_check_total_ge_50(self):
        from paper_trading.failure_validation.health_v165 import FailureInjectionRecoveryHealthCheck
        assert FailureInjectionRecoveryHealthCheck.EXPECTED_TOTAL >= 50

    def test_release_gate_expected_45(self):
        from release.failure_injection_recovery_release_gate_v165 import FailureInjectionRecoveryReleaseGateV165
        assert FailureInjectionRecoveryReleaseGateV165.EXPECTED_CHECKS == 45

    def test_fixture_count_ge_70(self):
        import os
        fixture_dir = os.path.join("tests", "fixtures", "failure_injection")
        count = len([f for f in os.listdir(fixture_dir) if f.endswith(".json")])
        assert count >= 70

    def test_required_safety_markers_count_10(self):
        from paper_trading.failure_validation.fixtures_validator_v165 import REQUIRED_SAFETY_MARKERS
        assert len(REQUIRED_SAFETY_MARKERS) == 10

    def test_forbidden_domains_count_ge_6(self):
        from paper_trading.failure_validation.enums_v165 import FORBIDDEN_DOMAINS
        assert len(FORBIDDEN_DOMAINS) >= 6

    def test_invalid_recovery_transitions_count_2(self):
        from paper_trading.failure_validation.enums_v165 import INVALID_RECOVERY_TRANSITIONS
        assert len(INVALID_RECOVERY_TRANSITIONS) == 2
