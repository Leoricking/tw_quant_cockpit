"""
tests/test_failure_validation_circuit_breaker_v165.py — Circuit Breaker tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import CircuitBreakerState
from paper_trading.failure_validation.circuit_breaker_v165 import (
    CircuitBreakerRegistry,
    PAPER_ONLY,
    REAL_FAILURE_INJECTION_ENABLED,
    RESEARCH_ONLY,
    simulate_circuit_breaker_trip,
)
from paper_trading.failure_validation.models_v165 import CircuitBreakerModel


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestCircuitBreakerSafetyFlags:
    def test_real_failure_injection_disabled(self):
        assert REAL_FAILURE_INJECTION_ENABLED is False

    def test_paper_only_true(self):
        assert PAPER_ONLY is True

    def test_research_only_true(self):
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# CircuitBreakerRegistry
# ---------------------------------------------------------------------------

class TestCircuitBreakerRegistry:
    def test_empty_registry(self):
        reg = CircuitBreakerRegistry()
        assert reg.breaker_count() == 0

    def test_get_or_create_creates_breaker(self):
        reg = CircuitBreakerRegistry()
        cb = reg.get_or_create("test_cb")
        assert cb is not None
        assert reg.breaker_count() == 1

    def test_get_or_create_returns_same_instance(self):
        reg = CircuitBreakerRegistry()
        cb1 = reg.get_or_create("cb_a")
        cb2 = reg.get_or_create("cb_a")
        assert cb1 is cb2

    def test_get_missing_returns_none(self):
        reg = CircuitBreakerRegistry()
        assert reg.get("nonexistent") is None

    def test_all_states_returns_dict(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("cb_1")
        reg.get_or_create("cb_2")
        states = reg.all_states()
        assert "cb_1" in states
        assert "cb_2" in states

    def test_initial_all_closed(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("cb_1")
        reg.get_or_create("cb_2")
        for state in reg.all_states().values():
            assert state == "CLOSED"

    def test_count_by_state_closed(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("cb_1")
        reg.get_or_create("cb_2")
        assert reg.count_by_state(CircuitBreakerState.CLOSED) == 2

    def test_count_by_state_open_after_trip(self):
        reg = CircuitBreakerRegistry()
        cb = reg.get_or_create("tripped", failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        assert reg.count_by_state(CircuitBreakerState.OPEN) == 1

    def test_summary_has_required_keys(self):
        reg = CircuitBreakerRegistry()
        summary = reg.summary()
        assert "total" in summary
        assert "closed" in summary
        assert "open" in summary
        assert "half_open" in summary
        assert "states" in summary

    def test_summary_total_matches_count(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("x")
        reg.get_or_create("y")
        assert reg.summary()["total"] == 2

    def test_custom_thresholds_respected(self):
        reg = CircuitBreakerRegistry()
        cb = reg.get_or_create("custom_cb", failure_threshold=5, cooldown_ms=10000)
        assert cb.failure_threshold == 5
        assert cb.cooldown_ms == 10000


# ---------------------------------------------------------------------------
# simulate_circuit_breaker_trip
# ---------------------------------------------------------------------------

class TestSimulateCircuitBreakerTrip:
    def test_trips_to_open_after_failures(self):
        result = simulate_circuit_breaker_trip(
            name="test_trip",
            failure_threshold=3,
            failures_to_inject=3,
            clock_advance_ms=6000,
            success_after_half_open=2,
        )
        assert result["state_after_failures"] == "OPEN"

    def test_advances_to_half_open_after_cooldown(self):
        result = simulate_circuit_breaker_trip(
            name="test_trip2",
            failure_threshold=2,
            failures_to_inject=2,
            clock_advance_ms=6000,
            success_after_half_open=2,
        )
        assert result["state_after_cooldown"] == "HALF_OPEN"

    def test_recovers_to_closed_after_successes(self):
        result = simulate_circuit_breaker_trip(
            name="test_trip3",
            failure_threshold=2,
            failures_to_inject=2,
            clock_advance_ms=6000,
            success_after_half_open=2,
        )
        assert result["state_after_recovery"] == "CLOSED"
        assert result["final_state"] == "CLOSED"

    def test_result_has_transitions(self):
        result = simulate_circuit_breaker_trip(
            name="test_trip4",
            failure_threshold=3,
            failures_to_inject=3,
            clock_advance_ms=6000,
            success_after_half_open=2,
        )
        assert len(result["transitions"]) >= 2  # CLOSED→OPEN, OPEN→HALF_OPEN, HALF_OPEN→CLOSED

    def test_result_has_required_keys(self):
        result = simulate_circuit_breaker_trip()
        assert "name" in result
        assert "state_after_failures" in result
        assert "state_after_cooldown" in result
        assert "state_after_recovery" in result
        assert "transitions" in result
        assert "final_state" in result
        assert "failure_count" in result

    def test_insufficient_failures_does_not_trip(self):
        result = simulate_circuit_breaker_trip(
            name="no_trip",
            failure_threshold=5,
            failures_to_inject=2,
            clock_advance_ms=1000,
            success_after_half_open=0,
        )
        assert result["state_after_failures"] == "CLOSED"

    def test_cooldown_not_reached_stays_open(self):
        result = simulate_circuit_breaker_trip(
            name="stays_open",
            failure_threshold=2,
            failures_to_inject=2,
            clock_advance_ms=100,  # much less than default cooldown of 5000
            success_after_half_open=2,
        )
        # cooldown=5000, advanced only 100ms — should remain OPEN
        assert result["state_after_cooldown"] == "OPEN"
