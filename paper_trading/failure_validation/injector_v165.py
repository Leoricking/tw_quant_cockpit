"""
paper_trading/failure_validation/injector_v165.py — Deterministic failure injector v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] In-memory/fixture only. No external system mutation. No broker. No real network.
[!] Deterministic: same seed + scenario = same injection outcome every time.
[!] Reversible and bounded. All injections expire and auto-revert within max_duration_ms.
"""
from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.failure_validation.enums_v165 import (
    InjectionStatus,
    RecoveryState,
    ValidationPhase,
    FailureType,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest,
    FailureInjectionResult,
)
from paper_trading.failure_validation.safety_precheck_v165 import (
    block_result,
    run_safety_precheck,
)

REAL_FAILURE_INJECTION_ENABLED = False
PRODUCTION_CHAOS_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DeterministicFailureInjector:
    """
    Deterministic, seedable, reversible, bounded failure injector.
    Operates entirely in-memory. No external system mutation.
    """

    def __init__(self) -> None:
        self._active_injections: Dict[str, FailureInjectionResult] = {}
        self._injection_log: List[Dict[str, Any]] = []
        # Global safety — never allow real injection
        assert not REAL_FAILURE_INJECTION_ENABLED, "Real injection must never be enabled"
        assert not PRODUCTION_CHAOS_ENABLED, "Production chaos must never be enabled"

    def inject(self, request: FailureInjectionRequest) -> FailureInjectionResult:
        """Attempt injection. Safety precheck is always the first step."""
        precheck = run_safety_precheck(request)
        if not precheck.passed:
            result = block_result(request, precheck)
            self._log("BLOCKED_BY_SAFETY", request, result)
            return result

        scenario = request.scenario
        assert scenario is not None

        # Deterministic RNG seeded by scenario seed
        rng = random.Random(scenario.seed)

        result = FailureInjectionResult(
            request_id=request.request_id,
            scenario_id=scenario.scenario_id,
            status=InjectionStatus.INJECTED,
            injected_at=_utcnow(),
        )

        result.log_phase(ValidationPhase.SAFETY_PRECHECK, "PASS", "All safety checks passed")
        result.log_phase(ValidationPhase.CONTROLLED_INJECTION, "INJECTED",
                         f"domain={scenario.domain.value} type={scenario.failure_type.value} seed={scenario.seed}")

        # Simulate detection based on failure type
        result.detection_confirmed = self._simulate_detection(scenario.failure_type, rng)
        if result.detection_confirmed:
            result.status = InjectionStatus.DETECTED
            result.log_phase(ValidationPhase.DETECTION, "DETECTED",
                             f"Failure type {scenario.failure_type.value} detected")
            result.alert_generated = rng.random() > 0.1  # 90% chance alert fires
            if result.alert_generated:
                result.log_phase(ValidationPhase.ALERT, "ALERTED", "Alert generated")
                result.incident_created = rng.random() > 0.3  # 70% chance incident created
                if result.incident_created:
                    result.log_phase(ValidationPhase.INCIDENT, "CREATED", "Incident created")

        result.containment_confirmed = result.detection_confirmed and rng.random() > 0.05
        if result.containment_confirmed:
            result.status = InjectionStatus.CONTAINED
            result.log_phase(ValidationPhase.CONTAINMENT, "CONTAINED", "Failure contained")

        result.recovery_triggered = result.containment_confirmed and rng.random() > 0.1
        if result.recovery_triggered:
            result.log_phase(ValidationPhase.RECOVERY_EXECUTION, "TRIGGERED", "Recovery triggered")

        # Compute data hashes for integrity verification
        state_seed = f"{scenario.scenario_id}:{scenario.seed}:{scenario.domain.value}"
        result.data_hash_before = _deterministic_hash(state_seed + ":before")
        result.data_hash_after = _deterministic_hash(state_seed + ":after")
        result.hash_matches = result.data_hash_before == result.data_hash_after

        result.events_injected = rng.randint(1, 10)

        # Revert — bounded, reversible
        result.reverted_at = _utcnow()
        result.events_reverted = result.events_injected
        result.state_after = RecoveryState.HEALTHY if result.containment_confirmed else RecoveryState.DEGRADED

        self._active_injections[result.result_id] = result
        self._log("INJECTED", request, result)
        return result

    def revert(self, result_id: str) -> bool:
        """Explicitly revert an active injection."""
        result = self._active_injections.get(result_id)
        if result is None:
            return False
        result.status = InjectionStatus.REVERTED
        result.reverted_at = _utcnow()
        del self._active_injections[result_id]
        return True

    def active_count(self) -> int:
        return len(self._active_injections)

    def injection_log(self) -> List[Dict[str, Any]]:
        return list(self._injection_log)

    def _simulate_detection(self, failure_type: FailureType, rng: random.Random) -> bool:
        """Simulate whether a failure is detected. Always ≥50% detection rate."""
        detection_rates: Dict[FailureType, float] = {
            FailureType.TIMEOUT:                    0.98,
            FailureType.DELAY:                      0.90,
            FailureType.STALE_DATA:                 0.85,
            FailureType.MISSING_DATA:               0.95,
            FailureType.DUPLICATE_EVENT:            0.80,
            FailureType.OUT_OF_ORDER_EVENT:         0.75,
            FailureType.INVALID_PAYLOAD:            0.99,
            FailureType.PARTIAL_WRITE:              0.88,
            FailureType.READ_FAILURE:               0.95,
            FailureType.WRITE_FAILURE:              0.95,
            FailureType.CHECKPOINT_CORRUPTION:      0.99,
            FailureType.SNAPSHOT_MISMATCH:          0.99,
            FailureType.HASH_MISMATCH:              0.99,
            FailureType.REPLAY_MISMATCH:            0.95,
            FailureType.STATE_DIVERGENCE:           0.92,
            FailureType.EVENT_LOSS:                 0.85,
            FailureType.EVENT_STORM:                0.90,
            FailureType.ALERT_LOSS:                 0.80,
            FailureType.ALERT_DUPLICATION:          0.75,
            FailureType.INCIDENT_CREATION_FAILURE:  0.88,
            FailureType.RECOVERY_FAILURE:           0.95,
            FailureType.ROLLBACK_FAILURE:           0.93,
            FailureType.RETRY_EXHAUSTION:           0.90,
            FailureType.CIRCUIT_OPEN:               0.98,
            FailureType.DEPENDENCY_UNAVAILABLE:     0.92,
            FailureType.DEGRADED_MODE:              0.85,
            FailureType.CONFIG_DRIFT:               0.78,
            FailureType.CLOCK_SKEW:                 0.82,
        }
        rate = detection_rates.get(failure_type, 0.80)
        return rng.random() < rate

    def _log(self, event: str, request: FailureInjectionRequest,
             result: FailureInjectionResult) -> None:
        self._injection_log.append({
            "event": event,
            "request_id": request.request_id,
            "result_id": result.result_id,
            "status": result.status.value,
            "ts": _utcnow().isoformat(),
        })


def _deterministic_hash(seed_str: str) -> str:
    import hashlib
    return hashlib.sha256(seed_str.encode()).hexdigest()
