"""
paper_trading/failure_validation/models_v165.py — Failure Injection & Recovery data models v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] REAL_FAILURE_INJECTION_ENABLED = False. PRODUCTION_CHAOS_ENABLED = False.
[!] All injection is in-memory/fixture only. No external system mutation.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.failure_validation.enums_v165 import (
    CircuitBreakerState,
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    InjectionStatus,
    RecoveryState,
    ScorecardDimension,
    SCORECARD_WEIGHTS,
    ValidationPhase,
)

REAL_FAILURE_INJECTION_ENABLED = False
PRODUCTION_CHAOS_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# FailureScenario
# ---------------------------------------------------------------------------

@dataclass
class FailureScenario:
    """Definition of a controlled failure scenario (research/paper only)."""
    scenario_id: str = field(default_factory=_new_id)
    name: str = ""
    description: str = ""
    domain: FailureDomain = FailureDomain.MARKET_DATA
    failure_type: FailureType = FailureType.TIMEOUT
    severity: FailureSeverity = FailureSeverity.LOW
    expected_outcomes: List[ExpectedOutcome] = field(default_factory=list)
    seed: int = 42
    max_duration_ms: int = 5000
    reversible: bool = True
    bounded: bool = True
    fixture_only: bool = True
    research_only: bool = True
    paper_only: bool = True
    no_broker: bool = True
    no_real_account: bool = True
    no_real_order: bool = True
    not_for_production: bool = True
    not_live: bool = True
    failure_injection_only: bool = True
    demo_only: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
    cascading_targets: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=_utcnow)

    def safety_markers(self) -> Dict[str, bool]:
        return {
            "TEST_FIXTURE": True,
            "DEMO_ONLY": self.demo_only,
            "PAPER_ONLY": self.paper_only,
            "RESEARCH_ONLY": self.research_only,
            "NOT_LIVE": self.not_live,
            "NO_BROKER": self.no_broker,
            "NO_REAL_ACCOUNT": self.no_real_account,
            "NO_REAL_ORDER": self.no_real_order,
            "NOT_FOR_PRODUCTION": self.not_for_production,
            "FAILURE_INJECTION_ONLY": self.failure_injection_only,
        }

    def all_safety_markers_set(self) -> bool:
        return all(self.safety_markers().values())


# ---------------------------------------------------------------------------
# FailureInjectionRequest
# ---------------------------------------------------------------------------

@dataclass
class FailureInjectionRequest:
    """A request to inject a failure scenario (will be safety-checked before execution)."""
    request_id: str = field(default_factory=_new_id)
    scenario: Optional[FailureScenario] = None
    requested_by: str = "test_harness"
    target_component: str = ""
    injection_context: Dict[str, Any] = field(default_factory=dict)
    requested_at: datetime = field(default_factory=_utcnow)
    idempotency_key: str = field(default_factory=_new_id)

    # These must all be True for any injection to proceed
    fixture_only: bool = True
    research_only: bool = True
    paper_only: bool = True
    no_broker: bool = True
    no_real_account: bool = True
    no_real_order: bool = True
    not_for_production: bool = True
    not_live: bool = True
    failure_injection_only: bool = True
    demo_only: bool = True


# ---------------------------------------------------------------------------
# FailureInjectionResult
# ---------------------------------------------------------------------------

@dataclass
class FailureInjectionResult:
    """Result of a controlled failure injection attempt."""
    result_id: str = field(default_factory=_new_id)
    request_id: str = ""
    scenario_id: str = ""
    status: InjectionStatus = InjectionStatus.PENDING
    blocked_reason: Optional[str] = None
    injected_at: Optional[datetime] = None
    reverted_at: Optional[datetime] = None
    detection_confirmed: bool = False
    alert_generated: bool = False
    incident_created: bool = False
    containment_confirmed: bool = False
    recovery_triggered: bool = False
    state_after: Optional[RecoveryState] = None
    data_hash_before: Optional[str] = None
    data_hash_after: Optional[str] = None
    hash_matches: Optional[bool] = None
    events_injected: int = 0
    events_reverted: int = 0
    phase_log: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utcnow)

    def log_phase(self, phase: ValidationPhase, outcome: str, detail: str = "") -> None:
        self.phase_log.append({
            "phase": phase.value,
            "outcome": outcome,
            "detail": detail,
            "ts": _utcnow().isoformat(),
        })


# ---------------------------------------------------------------------------
# RecoveryPlan
# ---------------------------------------------------------------------------

@dataclass
class RecoveryPlan:
    """Plan for recovering from an injected failure (simulation only)."""
    plan_id: str = field(default_factory=_new_id)
    scenario_id: str = ""
    result_id: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    rollback_steps: List[Dict[str, Any]] = field(default_factory=list)
    rto_budget_ms: Optional[Decimal] = None
    rpo_budget_ms: Optional[Decimal] = None
    requires_verification: bool = True
    auto_execution_enabled: bool = False  # Always False — no auto recovery
    created_at: datetime = field(default_factory=_utcnow)


# ---------------------------------------------------------------------------
# RecoveryValidationResult
# ---------------------------------------------------------------------------

@dataclass
class RecoveryValidationResult:
    """Result of validating a recovery from an injected failure."""
    validation_id: str = field(default_factory=_new_id)
    plan_id: str = ""
    result_id: str = ""
    initial_state: Optional[RecoveryState] = None
    final_state: Optional[RecoveryState] = None
    state_transitions: List[Dict[str, Any]] = field(default_factory=list)
    rto_actual_ms: Optional[Decimal] = None
    rpo_actual_ms: Optional[Decimal] = None
    rto_met: Optional[bool] = None
    rpo_met: Optional[bool] = None
    data_reconciled: bool = False
    replay_verified: bool = False
    idempotency_verified: bool = False
    invalid_transitions_detected: List[str] = field(default_factory=list)
    verification_passed: bool = False
    errors: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=_utcnow)

    def add_transition(self, from_state: RecoveryState, to_state: RecoveryState,
                       allowed: bool, reason: str = "") -> None:
        self.state_transitions.append({
            "from": from_state.value,
            "to": to_state.value,
            "allowed": allowed,
            "reason": reason,
            "ts": _utcnow().isoformat(),
        })
        if not allowed:
            self.invalid_transitions_detected.append(
                f"{from_state.value}->{to_state.value}: {reason}"
            )


# ---------------------------------------------------------------------------
# FailureScorecard
# ---------------------------------------------------------------------------

@dataclass
class FailureScorecard:
    """Weighted scorecard for a failure injection & recovery validation run."""
    scorecard_id: str = field(default_factory=_new_id)
    scenario_id: str = ""
    validation_id: str = ""
    dimension_scores: Dict[str, Optional[int]] = field(default_factory=dict)
    dimension_notes: Dict[str, str] = field(default_factory=dict)
    total_score: Optional[int] = None
    max_score: int = 100
    computed_at: Optional[datetime] = None

    def compute(self) -> int:
        """Compute weighted total score. Unknown dimensions contribute 0."""
        total = 0
        for dim, weight in SCORECARD_WEIGHTS.items():
            raw = self.dimension_scores.get(dim)
            if raw is not None:
                # Raw score is 0-100 per dimension; weight it
                total += int(round(raw * weight / 100))
        self.total_score = total
        self.computed_at = _utcnow()
        return total

    def summary(self) -> Dict[str, Any]:
        return {
            "scorecard_id": self.scorecard_id,
            "scenario_id": self.scenario_id,
            "validation_id": self.validation_id,
            "total_score": self.total_score,
            "max_score": self.max_score,
            "dimensions": {
                dim: {
                    "score": self.dimension_scores.get(dim),
                    "weight": SCORECARD_WEIGHTS.get(dim, 0),
                    "note": self.dimension_notes.get(dim, ""),
                }
                for dim in SCORECARD_WEIGHTS
            },
            "computed_at": self.computed_at.isoformat() if self.computed_at else None,
        }


# ---------------------------------------------------------------------------
# BaselineSnapshot
# ---------------------------------------------------------------------------

@dataclass
class BaselineSnapshot:
    """Immutable, content-addressed baseline snapshot before injection."""
    snapshot_id: str = field(default_factory=_new_id)
    component: str = ""
    state_data: Dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""
    captured_at: datetime = field(default_factory=_utcnow)
    seed: int = 42
    deterministic: bool = True

    def __post_init__(self) -> None:
        if not self.content_hash:
            self.content_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = json.dumps(self.state_data, sort_keys=True, default=str)
        return hashlib.sha256(payload.encode()).hexdigest()

    def verify_integrity(self) -> bool:
        return self.content_hash == self._compute_hash()


# ---------------------------------------------------------------------------
# CircuitBreakerModel
# ---------------------------------------------------------------------------

@dataclass
class CircuitBreakerModel:
    """Virtual circuit breaker model (no real network calls)."""
    breaker_id: str = field(default_factory=_new_id)
    name: str = ""
    state: CircuitBreakerState = CircuitBreakerState.CLOSED
    failure_count: int = 0
    failure_threshold: int = 3
    success_count: int = 0
    success_threshold: int = 2
    virtual_clock_ms: int = 0
    cooldown_ms: int = 5000
    opened_at_clock_ms: Optional[int] = None
    transitions: List[Dict[str, Any]] = field(default_factory=list)

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.state == CircuitBreakerState.CLOSED and self.failure_count >= self.failure_threshold:
            self._transition_to(CircuitBreakerState.OPEN)
            self.opened_at_clock_ms = self.virtual_clock_ms

    def record_success(self) -> None:
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._transition_to(CircuitBreakerState.CLOSED)
                self.failure_count = 0
                self.success_count = 0

    def advance_clock(self, ms: int) -> None:
        self.virtual_clock_ms += ms
        if (self.state == CircuitBreakerState.OPEN
                and self.opened_at_clock_ms is not None
                and self.virtual_clock_ms - self.opened_at_clock_ms >= self.cooldown_ms):
            self._transition_to(CircuitBreakerState.HALF_OPEN)
            self.success_count = 0

    def _transition_to(self, new_state: CircuitBreakerState) -> None:
        self.transitions.append({
            "from": self.state.value,
            "to": new_state.value,
            "clock_ms": self.virtual_clock_ms,
        })
        self.state = new_state


# ---------------------------------------------------------------------------
# RetryRecord
# ---------------------------------------------------------------------------

@dataclass
class RetryRecord:
    """Record of a retry attempt (virtual clock, no real sleep)."""
    retry_id: str = field(default_factory=_new_id)
    idempotency_key: str = ""
    attempt_number: int = 0
    max_attempts: int = 3
    virtual_clock_ms: int = 0
    backoff_ms: int = 100
    succeeded: bool = False
    exhausted: bool = False
    attempts: List[Dict[str, Any]] = field(default_factory=list)

    def record_attempt(self, success: bool, detail: str = "") -> None:
        self.attempt_number += 1
        self.attempts.append({
            "attempt": self.attempt_number,
            "clock_ms": self.virtual_clock_ms,
            "success": success,
            "detail": detail,
        })
        if success:
            self.succeeded = True
        elif self.attempt_number >= self.max_attempts:
            self.exhausted = True
        else:
            self.virtual_clock_ms += self.backoff_ms * (2 ** (self.attempt_number - 1))
