"""
paper_trading/multi_session/models_v166.py — Multi-session Coordination data models v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from paper_trading.multi_session.enums_v166 import (
    SessionType, SessionLifecycleState, ConflictType, ConflictSeverity,
    ResourceType, ReservationStatus, SessionPriority, DecisionType,
    CoordinationOutcome, LockType, LockStatus, ElectionStatus, BarrierType, BarrierStatus,
)

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


@dataclass
class SessionDescriptor:
    session_id: str
    session_type: SessionType
    name: str
    owner: str
    created_at: datetime
    registered_at: Optional[datetime]
    lifecycle_state: SessionLifecycleState
    priority: SessionPriority
    capabilities: List[str]
    symbols: List[str]
    strategies: List[str]
    data_sources: List[str]
    resource_requirements: Dict[str, Any]
    risk_budget: float
    capital_budget: float
    policy_version: str
    code_version: str
    paper_only: bool = True
    research_only: bool = True
    fixture_only: bool = False

    def __post_init__(self) -> None:
        if not self.session_id:
            raise ValueError("session_id is required")
        if not self.owner:
            raise ValueError("owner is required")
        if not self.policy_version:
            raise ValueError("policy_version is required")
        if self.session_type is None:
            raise ValueError("session_type is required")


@dataclass
class CoordinationPolicy:
    policy_id: str
    version: str
    max_concurrent_sessions: int
    priority_rules: Dict[str, Any]
    fairness_rules: Dict[str, Any]
    resource_rules: Dict[str, Any]
    symbol_overlap_rules: Dict[str, Any]
    strategy_conflict_rules: Dict[str, Any]
    risk_aggregation_rules: Dict[str, Any]
    capital_rules: Dict[str, Any]
    event_ordering_rules: Dict[str, Any]
    pause_rules: Dict[str, Any]
    resume_rules: Dict[str, Any]
    failure_propagation_rules: Dict[str, Any]
    deadlock_rules: Dict[str, Any]
    starvation_rules: Dict[str, Any]
    forbidden_actions: List[str] = field(default_factory=list)


@dataclass
class ResourceReservation:
    reservation_id: str
    session_id: str
    resource_type: ResourceType
    resource_key: str
    quantity: float
    reserved_at: datetime
    expires_at: Optional[datetime]
    priority: SessionPriority
    status: ReservationStatus
    lease_id: Optional[str]
    policy_version: str


@dataclass
class SessionConflict:
    conflict_id: str
    session_ids: List[str]
    conflict_type: ConflictType
    severity: ConflictSeverity
    resource_key: Optional[str]
    symbol: Optional[str]
    strategy: Optional[str]
    detected_at: datetime
    evidence: Dict[str, Any]
    resolution_options: List[str]
    blocking: bool
    policy_version: str


@dataclass
class CoordinationDecision:
    decision_id: str
    session_ids: List[str]
    decision_type: DecisionType
    reason: str
    actor: str
    created_at: datetime
    input_state_hash: str
    policy_version: str
    selected_action: str
    rejected_actions: List[str]
    safety_blocks: List[str]
    expected_state: Dict[str, Any]
    lineage: List[str]


@dataclass
class CoordinationSnapshot:
    snapshot_id: str
    as_of: datetime
    session_states: Dict[str, str]
    resource_state: Dict[str, Any]
    risk_state: Dict[str, Any]
    capital_state: Dict[str, Any]
    symbol_exposure: Dict[str, Any]
    event_positions: Dict[str, int]
    active_conflicts: List[str]
    active_reservations: List[str]
    policy_versions: Dict[str, str]
    content_hash: str


@dataclass
class CoordinationResult:
    coordination_id: str
    sessions_considered: List[str]
    sessions_admitted: List[str]
    sessions_blocked: List[str]
    sessions_paused: List[str]
    sessions_degraded: List[str]
    conflicts_detected: int
    conflicts_resolved: int
    conflicts_unresolved: int
    resource_allocations: Dict[str, Any]
    risk_result: CoordinationOutcome
    capital_result: CoordinationOutcome
    ordering_result: CoordinationOutcome
    reconciliation_result: CoordinationOutcome
    final_state: Dict[str, Any]
    warnings: List[str]
    failures: List[str]
    lineage: List[str]
    reproducibility_hash: str


@dataclass
class HeartbeatRecord:
    session_id: str
    last_seen: datetime
    expected_interval_seconds: float
    stale_threshold_seconds: float
    missed_count: int
    is_stale: bool


@dataclass
class Lease:
    lease_id: str
    owner_session_id: str
    resource_key: str
    issued_at: datetime
    expires_at: datetime
    generation: int
    is_expired: bool = False

    def check_expired(self, now: datetime) -> bool:
        self.is_expired = now >= self.expires_at
        return self.is_expired


@dataclass
class LockRecord:
    lock_id: str
    resource_key: str
    lock_type: LockType
    owner_session_id: str
    acquired_at: datetime
    expires_at: Optional[datetime]
    status: LockStatus
    lease_id: Optional[str]


@dataclass
class ElectionRecord:
    election_id: str
    candidates: List[str]
    winner_session_id: Optional[str]
    status: ElectionStatus
    started_at: datetime
    decided_at: Optional[datetime]
    lease_id: Optional[str]
    generation: int


@dataclass
class EventRecord:
    event_id: str
    source_session_id: str
    event_type: str
    timestamp: datetime
    ingestion_time: datetime
    available_from: datetime
    sequence: int
    global_sequence: Optional[int]
    causal_parent_id: Optional[str]
    correlation_id: Optional[str]
    payload: Dict[str, Any]


@dataclass
class BarrierRecord:
    barrier_id: str
    barrier_type: BarrierType
    required_sessions: List[str]
    arrived_sessions: List[str]
    quorum: int
    status: BarrierStatus
    created_at: datetime
    released_at: Optional[datetime]
    timeout_at: Optional[datetime]
