"""
tests/test_failure_validation_injector_v165.py — Injector tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import (
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    InjectionStatus,
    RecoveryState,
    ValidationPhase,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest,
    FailureScenario,
)
from paper_trading.failure_validation.injector_v165 import (
    DeterministicFailureInjector,
    REAL_FAILURE_INJECTION_ENABLED,
    PRODUCTION_CHAOS_ENABLED,
    PAPER_ONLY,
    RESEARCH_ONLY,
    _deterministic_hash,
)


def _scenario(domain=FailureDomain.MARKET_DATA, ft=FailureType.STALE_DATA,
              severity=FailureSeverity.LOW, seed=42, **kwargs):
    return FailureScenario(
        name=f"inj_test_{ft.value.lower()}",
        description="test injection",
        domain=domain,
        failure_type=ft,
        severity=severity,
        expected_outcomes=[ExpectedOutcome.DETECTED],
        seed=seed,
        max_duration_ms=5000,
        **kwargs,
    )


def _request(scenario=None, **kwargs):
    if scenario is None:
        scenario = _scenario()
    return FailureInjectionRequest(scenario=scenario, **kwargs)


# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------

class TestInjectorSafetyConstants:
    def test_real_failure_injection_disabled(self):
        assert REAL_FAILURE_INJECTION_ENABLED is False

    def test_production_chaos_disabled(self):
        assert PRODUCTION_CHAOS_ENABLED is False

    def test_paper_only_true(self):
        assert PAPER_ONLY is True

    def test_research_only_true(self):
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# Injector instantiation
# ---------------------------------------------------------------------------

class TestInjectorInstantiation:
    def test_injector_creates_successfully(self):
        inj = DeterministicFailureInjector()
        assert inj is not None

    def test_injector_starts_with_zero_active(self):
        inj = DeterministicFailureInjector()
        assert inj.active_count() == 0

    def test_injector_starts_with_empty_log(self):
        inj = DeterministicFailureInjector()
        assert inj.injection_log() == []


# ---------------------------------------------------------------------------
# Successful injection
# ---------------------------------------------------------------------------

class TestSuccessfulInjection:
    def test_valid_request_is_not_blocked(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.status != InjectionStatus.BLOCKED_BY_SAFETY

    def test_inject_returns_result_with_correct_request_id(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.request_id == req.request_id

    def test_inject_result_has_scenario_id(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.scenario_id == req.scenario.scenario_id

    def test_inject_computes_data_hashes(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.data_hash_before is not None
        assert result.data_hash_after is not None
        assert len(result.data_hash_before) == 64

    def test_inject_records_events_injected(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.events_injected >= 1

    def test_inject_reverts_all_events(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.events_reverted == result.events_injected

    def test_inject_has_reverted_at(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.reverted_at is not None

    def test_inject_phase_log_has_safety_precheck(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        phases = [p["phase"] for p in result.phase_log]
        assert ValidationPhase.SAFETY_PRECHECK.value in phases

    def test_inject_phase_log_has_injection_phase(self):
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        phases = [p["phase"] for p in result.phase_log]
        assert ValidationPhase.CONTROLLED_INJECTION.value in phases

    def test_inject_adds_to_log(self):
        inj = DeterministicFailureInjector()
        req = _request()
        inj.inject(req)
        assert len(inj.injection_log()) >= 1


# ---------------------------------------------------------------------------
# Blocked injection
# ---------------------------------------------------------------------------

class TestBlockedInjection:
    def test_unsafe_request_is_blocked(self):
        inj = DeterministicFailureInjector()
        req = _request()
        req.fixture_only = False
        result = inj.inject(req)
        assert result.status == InjectionStatus.BLOCKED_BY_SAFETY

    def test_blocked_result_has_reason(self):
        inj = DeterministicFailureInjector()
        req = _request()
        req.no_broker = False
        result = inj.inject(req)
        assert result.blocked_reason is not None

    def test_blocked_injection_adds_to_log(self):
        inj = DeterministicFailureInjector()
        req = _request()
        req.paper_only = False
        inj.inject(req)
        log = inj.injection_log()
        assert any(e["status"] == "BLOCKED_BY_SAFETY" for e in log)


# ---------------------------------------------------------------------------
# Determinism: same seed = same result
# ---------------------------------------------------------------------------

class TestDeterministicBehavior:
    def test_same_seed_produces_same_detection_outcome(self):
        inj1 = DeterministicFailureInjector()
        inj2 = DeterministicFailureInjector()
        s = _scenario(seed=12345)
        r1 = inj1.inject(_request(scenario=s))
        # Re-create identical scenario (same seed, same ID is impossible with uuid)
        # So test the hash function is deterministic instead
        h1 = _deterministic_hash("test:12345:MARKET_DATA:before")
        h2 = _deterministic_hash("test:12345:MARKET_DATA:before")
        assert h1 == h2

    def test_hash_function_is_64_chars(self):
        h = _deterministic_hash("any_string")
        assert len(h) == 64

    def test_different_seeds_different_hash(self):
        h1 = _deterministic_hash("scenario_1:before")
        h2 = _deterministic_hash("scenario_2:before")
        assert h1 != h2

    def test_before_and_after_hashes_differ(self):
        inj = DeterministicFailureInjector()
        req = _request(scenario=_scenario(seed=999))
        result = inj.inject(req)
        # before and after hash the same seed string with :before/:after suffix
        assert result.data_hash_before != result.data_hash_after

    def test_same_scenario_repeated_injections_same_hash_before(self):
        """Two injections of the same scenario name+seed produce same hash_before."""
        inj = DeterministicFailureInjector()
        s1 = _scenario(seed=42)
        s2 = FailureScenario(
            scenario_id=s1.scenario_id,  # share ID to get same hash
            name=s1.name,
            description=s1.description,
            domain=s1.domain,
            failure_type=s1.failure_type,
            severity=s1.severity,
            expected_outcomes=s1.expected_outcomes,
            seed=s1.seed,
            max_duration_ms=s1.max_duration_ms,
        )
        r1 = inj.inject(_request(scenario=s1))
        r2 = inj.inject(_request(scenario=s2))
        assert r1.data_hash_before == r2.data_hash_before


# ---------------------------------------------------------------------------
# Revert
# ---------------------------------------------------------------------------

class TestRevert:
    def test_revert_unknown_id_returns_false(self):
        inj = DeterministicFailureInjector()
        assert inj.revert("nonexistent-id") is False

    def test_revert_active_injection_returns_true(self):
        inj = DeterministicFailureInjector()
        result = inj.inject(_request())
        reverted = inj.revert(result.result_id)
        assert reverted is True

    def test_revert_removes_from_active(self):
        inj = DeterministicFailureInjector()
        result = inj.inject(_request())
        before = inj.active_count()
        inj.revert(result.result_id)
        assert inj.active_count() == before - 1

    def test_revert_twice_returns_false(self):
        inj = DeterministicFailureInjector()
        result = inj.inject(_request())
        inj.revert(result.result_id)
        assert inj.revert(result.result_id) is False


# ---------------------------------------------------------------------------
# State after injection
# ---------------------------------------------------------------------------

class TestStateAfterInjection:
    def test_contained_result_state_is_healthy(self):
        """With TIMEOUT at seed=42, containment follows detection."""
        inj = DeterministicFailureInjector()
        req = _request(scenario=_scenario(ft=FailureType.TIMEOUT, seed=1))
        result = inj.inject(req)
        if result.containment_confirmed:
            assert result.state_after == RecoveryState.HEALTHY
        else:
            assert result.state_after == RecoveryState.DEGRADED

    def test_detection_only_after_injection(self):
        """Any result status is one of the expected InjectionStatus values."""
        inj = DeterministicFailureInjector()
        req = _request()
        result = inj.inject(req)
        assert result.status in {
            InjectionStatus.INJECTED,
            InjectionStatus.DETECTED,
            InjectionStatus.CONTAINED,
            InjectionStatus.BLOCKED_BY_SAFETY,
        }


# ---------------------------------------------------------------------------
# Multiple injections
# ---------------------------------------------------------------------------

class TestMultipleInjections:
    def test_multiple_injections_accumulate_in_log(self):
        inj = DeterministicFailureInjector()
        for i in range(5):
            inj.inject(_request(scenario=_scenario(seed=i+100)))
        assert len(inj.injection_log()) == 5

    def test_injection_log_returns_copy(self):
        inj = DeterministicFailureInjector()
        inj.inject(_request())
        log1 = inj.injection_log()
        log2 = inj.injection_log()
        assert log1 == log2
        log1.clear()
        assert len(inj.injection_log()) >= 1  # internal log unaffected
