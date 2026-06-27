"""
paper_trading/failure_validation/circuit_breaker_v165.py — Virtual circuit breaker v1.6.5.
[!] Research Only. No Real Orders. No Real Network Calls. Not Investment Advice.
[!] Virtual clock only. No real sleep. No real network.
"""
from __future__ import annotations

from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import CircuitBreakerState
from paper_trading.failure_validation.models_v165 import CircuitBreakerModel

REAL_FAILURE_INJECTION_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


class CircuitBreakerRegistry:
    """Registry of virtual circuit breakers."""

    def __init__(self) -> None:
        self._breakers: Dict[str, CircuitBreakerModel] = {}

    def get_or_create(self, name: str, failure_threshold: int = 3,
                      success_threshold: int = 2, cooldown_ms: int = 5000) -> CircuitBreakerModel:
        if name not in self._breakers:
            self._breakers[name] = CircuitBreakerModel(
                name=name,
                failure_threshold=failure_threshold,
                success_threshold=success_threshold,
                cooldown_ms=cooldown_ms,
            )
        return self._breakers[name]

    def get(self, name: str) -> CircuitBreakerModel | None:
        return self._breakers.get(name)

    def all_states(self) -> Dict[str, str]:
        return {name: b.state.value for name, b in self._breakers.items()}

    def count_by_state(self, state: CircuitBreakerState) -> int:
        return sum(1 for b in self._breakers.values() if b.state == state)

    def breaker_count(self) -> int:
        return len(self._breakers)

    def summary(self) -> Dict[str, Any]:
        return {
            "total": self.breaker_count(),
            "closed": self.count_by_state(CircuitBreakerState.CLOSED),
            "open": self.count_by_state(CircuitBreakerState.OPEN),
            "half_open": self.count_by_state(CircuitBreakerState.HALF_OPEN),
            "states": self.all_states(),
        }


def simulate_circuit_breaker_trip(
    name: str = "test_breaker",
    failure_threshold: int = 3,
    failures_to_inject: int = 3,
    clock_advance_ms: int = 6000,
    success_after_half_open: int = 2,
) -> Dict[str, Any]:
    """
    Simulate a full CLOSED→OPEN→HALF_OPEN→CLOSED circuit breaker trip.
    No real network calls. Virtual clock only.
    """
    registry = CircuitBreakerRegistry()
    breaker = registry.get_or_create(name, failure_threshold=failure_threshold)

    # Inject failures
    for _ in range(failures_to_inject):
        breaker.record_failure()

    state_after_failures = breaker.state.value

    # Advance virtual clock past cooldown
    breaker.advance_clock(clock_advance_ms)
    state_after_cooldown = breaker.state.value

    # Inject successes to recover
    for _ in range(success_after_half_open):
        breaker.record_success()

    state_after_recovery = breaker.state.value

    return {
        "name": name,
        "state_after_failures": state_after_failures,
        "state_after_cooldown": state_after_cooldown,
        "state_after_recovery": state_after_recovery,
        "transitions": breaker.transitions,
        "final_state": breaker.state.value,
        "failure_count": breaker.failure_count,
    }
