"""
tests/test_failure_validation_partial_cascade_v165.py — Partial & Cascade tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import (
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    RecoveryState,
    AUTO_RESUME_RUNNING_ENABLED,
)
from paper_trading.failure_validation.models_v165 import FailureScenario
from paper_trading.failure_validation.cascading_v165 import (
    PAPER_ONLY as CASC_PAPER_ONLY,
    REAL_FAILURE_INJECTION_ENABLED as CASC_RFI,
    RESEARCH_ONLY as CASC_RESEARCH_ONLY,
    _cascading_failure_type,
    simulate_cascading_failure,
)
from paper_trading.failure_validation.degraded_mode_v165 import (
    DegradedModeResult,
    PAPER_ONLY as DEGR_PAPER_ONLY,
    RESEARCH_ONLY as DEGR_RESEARCH_ONLY,
    simulate_degraded_mode,
)


def _cascade_scenario(seed=20001, cascading_targets=None):
    return FailureScenario(
        name="test_cascade",
        description="cascade test",
        domain=FailureDomain.MARKET_DATA,
        failure_type=FailureType.STALE_DATA,
        severity=FailureSeverity.HIGH,
        expected_outcomes=[ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED],
        seed=seed,
        max_duration_ms=5000,
        cascading_targets=cascading_targets or [],
    )


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestPartialCascadeSafetyFlags:
    def test_cascading_real_failure_injection_disabled(self):
        assert CASC_RFI is False

    def test_cascading_paper_only(self):
        assert CASC_PAPER_ONLY is True

    def test_cascading_research_only(self):
        assert CASC_RESEARCH_ONLY is True

    def test_degraded_paper_only(self):
        assert DEGR_PAPER_ONLY is True

    def test_degraded_research_only(self):
        assert DEGR_RESEARCH_ONLY is True

    def test_auto_resume_running_disabled(self):
        assert AUTO_RESUME_RUNNING_ENABLED is False


# ---------------------------------------------------------------------------
# simulate_cascading_failure — no targets
# ---------------------------------------------------------------------------

class TestCascadingFailureNoTargets:
    def test_no_targets_chain_has_one_step(self):
        s = _cascade_scenario(cascading_targets=[])
        result = simulate_cascading_failure(s, seed=42)
        assert result["chain_length"] == 1

    def test_result_has_scenario_id(self):
        s = _cascade_scenario()
        result = simulate_cascading_failure(s, seed=42)
        assert result["scenario_id"] == s.scenario_id

    def test_result_has_scenario_name(self):
        s = _cascade_scenario()
        result = simulate_cascading_failure(s, seed=42)
        assert result["scenario_name"] == s.name

    def test_result_has_final_state(self):
        s = _cascade_scenario()
        result = simulate_cascading_failure(s, seed=42)
        assert result["final_state"] in {"HEALTHY", "DEGRADED", "BLOCKED"}

    def test_result_has_all_contained_flag(self):
        s = _cascade_scenario()
        result = simulate_cascading_failure(s, seed=42)
        assert "all_contained" in result


# ---------------------------------------------------------------------------
# simulate_cascading_failure — with targets
# ---------------------------------------------------------------------------

class TestCascadingFailureWithTargets:
    def test_two_targets_chain_length_up_to_3(self):
        s = _cascade_scenario(cascading_targets=["SESSION_STATE", "ALERT"])
        result = simulate_cascading_failure(s, seed=42)
        assert result["chain_length"] >= 1  # primary + targets (some may not propagate)

    def test_chain_list_has_step_keys(self):
        s = _cascade_scenario(cascading_targets=["EVENT_STREAM"])
        result = simulate_cascading_failure(s, seed=42)
        for step in result["chain"]:
            assert "step" in step

    def test_primary_step_is_step_0(self):
        s = _cascade_scenario(cascading_targets=["ALERT"])
        result = simulate_cascading_failure(s, seed=42)
        assert result["chain"][0]["step"] == 0

    def test_primary_step_has_domain(self):
        s = _cascade_scenario(cascading_targets=["ALERT"])
        result = simulate_cascading_failure(s, seed=42)
        assert result["chain"][0]["domain"] == FailureDomain.MARKET_DATA.value

    def test_deterministic_same_seed(self):
        s1 = _cascade_scenario(seed=12345, cascading_targets=["SESSION_STATE"])
        s2 = FailureScenario(
            scenario_id=s1.scenario_id,
            name=s1.name, description=s1.description,
            domain=s1.domain, failure_type=s1.failure_type,
            severity=s1.severity, expected_outcomes=s1.expected_outcomes,
            seed=s1.seed, max_duration_ms=s1.max_duration_ms,
            cascading_targets=s1.cascading_targets,
        )
        r1 = simulate_cascading_failure(s1, seed=42)
        r2 = simulate_cascading_failure(s2, seed=42)
        assert r1["final_state"] == r2["final_state"]

    def test_unknown_domain_produces_skipped_step(self):
        s = _cascade_scenario(cascading_targets=["UNKNOWN_DOMAIN_XYZ"])
        result = simulate_cascading_failure(s, seed=42)
        skipped = [step for step in result["chain"] if step.get("status") == "SKIPPED"]
        assert len(skipped) == 1

    def test_all_contained_is_bool(self):
        s = _cascade_scenario(cascading_targets=["STORE"])
        result = simulate_cascading_failure(s, seed=42)
        assert isinstance(result["all_contained"], bool)

    def test_primary_detected_flag_present(self):
        s = _cascade_scenario(cascading_targets=["RECOVERY"])
        result = simulate_cascading_failure(s, seed=42)
        assert "primary_detected" in result

    def test_primary_contained_flag_present(self):
        s = _cascade_scenario(cascading_targets=["RECOVERY"])
        result = simulate_cascading_failure(s, seed=42)
        assert "primary_contained" in result

    def test_chain_length_matches_chain_list(self):
        s = _cascade_scenario(cascading_targets=["ALERT", "SESSION_STATE", "RECOVERY"])
        result = simulate_cascading_failure(s, seed=42)
        assert result["chain_length"] == len(result["chain"])

    def test_multiple_targets_chain_not_empty(self):
        s = _cascade_scenario(
            cascading_targets=["SESSION_STATE", "ALERT", "INCIDENT", "RECOVERY"]
        )
        result = simulate_cascading_failure(s, seed=42)
        assert len(result["chain"]) >= 1


# ---------------------------------------------------------------------------
# _cascading_failure_type helper
# ---------------------------------------------------------------------------

class TestCascadingFailureTypeHelper:
    def test_returns_failure_type_for_market_data(self):
        import random
        rng = random.Random(42)
        ft = _cascading_failure_type(FailureDomain.MARKET_DATA, rng)
        assert isinstance(ft, FailureType)

    def test_returns_failure_type_for_checkpoint(self):
        import random
        rng = random.Random(99)
        ft = _cascading_failure_type(FailureDomain.CHECKPOINT, rng)
        assert ft in {FailureType.CHECKPOINT_CORRUPTION, FailureType.HASH_MISMATCH}

    def test_returns_failure_type_for_alert(self):
        import random
        rng = random.Random(1)
        ft = _cascading_failure_type(FailureDomain.ALERT, rng)
        assert ft in {FailureType.ALERT_LOSS, FailureType.INCIDENT_CREATION_FAILURE}

    def test_all_domains_return_valid_type(self):
        import random
        rng = random.Random(42)
        for domain in FailureDomain:
            ft = _cascading_failure_type(domain, rng)
            assert isinstance(ft, FailureType)


# ---------------------------------------------------------------------------
# DegradedModeResult
# ---------------------------------------------------------------------------

class TestDegradedModeResult:
    def test_default_auto_resume_blocked(self):
        r = DegradedModeResult(component="session")
        assert r.auto_resume_blocked is True

    def test_default_auto_resume_not_attempted(self):
        r = DegradedModeResult(component="session")
        assert r.auto_resume_attempted is False

    def test_manual_resume_required_true(self):
        r = DegradedModeResult(component="session")
        assert r.manual_resume_required is True

    def test_state_is_degraded(self):
        r = DegradedModeResult(component="session")
        assert r.state == RecoveryState.DEGRADED

    def test_as_dict_has_required_keys(self):
        r = DegradedModeResult(component="c")
        d = r.as_dict()
        assert "component" in d
        assert "entered_degraded" in d
        assert "auto_resume_attempted" in d
        assert "auto_resume_blocked" in d
        assert "manual_resume_required" in d
        assert "capabilities_disabled" in d
        assert "state" in d


# ---------------------------------------------------------------------------
# simulate_degraded_mode
# ---------------------------------------------------------------------------

class TestSimulateDegradedMode:
    def test_entered_degraded_true(self):
        r = simulate_degraded_mode("session", ["order_submission"], seed=42)
        assert r.entered_degraded is True

    def test_auto_resume_never_attempted(self):
        r = simulate_degraded_mode("session", ["analysis"], seed=42)
        assert r.auto_resume_attempted is False

    def test_auto_resume_always_blocked(self):
        r = simulate_degraded_mode("session", ["execution"], seed=42)
        assert r.auto_resume_blocked is True

    def test_manual_resume_required(self):
        r = simulate_degraded_mode("session", ["trading"], seed=42)
        assert r.manual_resume_required is True

    def test_capabilities_disabled_preserved(self):
        caps = ["order_submission", "strategy_execution"]
        r = simulate_degraded_mode("session", caps, seed=42)
        assert r.capabilities_disabled == caps

    def test_component_preserved(self):
        r = simulate_degraded_mode("market_data_feed", [], seed=42)
        assert r.component == "market_data_feed"

    def test_state_remains_degraded(self):
        r = simulate_degraded_mode("any_component", [], seed=42)
        assert r.state == RecoveryState.DEGRADED
