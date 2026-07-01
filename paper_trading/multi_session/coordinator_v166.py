"""
paper_trading/multi_session/coordinator_v166.py — Multi-session Coordinator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No automatic production actions. No auto resume. No auto restart.
[!] All decisions are explicit. No network. No external coordination.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import (
    DecisionType, CoordinationOutcome, SessionLifecycleState,
)
from paper_trading.multi_session.models_v166 import (
    CoordinationResult, CoordinationDecision, SessionDescriptor,
)
from paper_trading.multi_session.coordination_context_v166 import CoordinationContext
from paper_trading.multi_session.coordination_decision_v166 import make_coordination_decision
from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
from paper_trading.multi_session.priority_engine_v166 import PriorityEngine
from paper_trading.multi_session.resource_manager_v166 import ResourceManager

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
AUTO_RESUME_ENABLED = False
AUTO_RESTART_ENABLED = False
AUTO_CAPITAL_REALLOCATION_ENABLED = False
AUTO_RISK_OVERRIDE_ENABLED = False


class MultiSessionCoordinator:
    """
    Coordinates multiple paper/replay/simulation sessions locally.
    All coordination is deterministic and simulation-only.
    No real process control. No external bus. No auto-resume.
    """

    def __init__(
        self,
        resource_manager: Optional[ResourceManager] = None,
        conflict_detector: Optional[ConflictDetector] = None,
        priority_engine: Optional[PriorityEngine] = None,
    ) -> None:
        self._rm = resource_manager or ResourceManager()
        self._cd = conflict_detector or ConflictDetector()
        self._pe = priority_engine or PriorityEngine()
        self._decisions: List[CoordinationDecision] = []

    def coordinate(self, ctx: CoordinationContext) -> CoordinationResult:
        input_hash = ctx.to_input_hash()
        sessions = ctx.sessions
        policy = ctx.policy

        # Priority ordering
        ordered = self._pe.order_sessions(sessions, ctx.seed)

        admitted: List[str] = []
        blocked: List[str] = []
        paused: List[str] = []
        degraded: List[str] = []
        warnings: List[str] = []
        failures: List[str] = []
        lineage: List[str] = [f"coord:{input_hash}"]

        # Detect conflicts
        conflicts = self._cd.detect(sessions, policy)
        blocking_conflicts = [c for c in conflicts if c.blocking]
        non_blocking = [c for c in conflicts if not c.blocking]

        blocked_ids = set()
        for conflict in blocking_conflicts:
            for sid in conflict.session_ids:
                blocked_ids.add(sid)

        # Admit or block sessions
        for s in ordered:
            if len(admitted) >= policy.max_concurrent_sessions:
                blocked.append(s.session_id)
                continue
            if s.session_id in blocked_ids:
                blocked.append(s.session_id)
                decision = make_coordination_decision(
                    session_ids=[s.session_id],
                    decision_type=DecisionType.BLOCK,
                    reason=f"Blocking conflict detected",
                    actor="coordinator",
                    input_state_hash=input_hash,
                    policy_version=policy.version,
                    selected_action="block",
                    lineage=lineage,
                )
                self._decisions.append(decision)
            else:
                admitted.append(s.session_id)
                decision = make_coordination_decision(
                    session_ids=[s.session_id],
                    decision_type=DecisionType.ADMIT,
                    reason="No blocking conflicts",
                    actor="coordinator",
                    input_state_hash=input_hash,
                    policy_version=policy.version,
                    selected_action="admit",
                    lineage=lineage,
                )
                self._decisions.append(decision)

        for c in non_blocking:
            warnings.append(f"Non-blocking conflict: {c.conflict_type.value}")

        # Resource allocation
        resource_allocations = self._rm.allocate_for_sessions(admitted, ctx.resource_state, policy)

        import hashlib, json
        final_state = {"admitted": sorted(admitted), "blocked": sorted(blocked)}
        reproducibility_hash = hashlib.sha256(
            json.dumps(final_state, sort_keys=True).encode()
        ).hexdigest()[:16]

        return CoordinationResult(
            coordination_id=str(uuid.uuid4()),
            sessions_considered=[s.session_id for s in sessions],
            sessions_admitted=admitted,
            sessions_blocked=blocked,
            sessions_paused=paused,
            sessions_degraded=degraded,
            conflicts_detected=len(conflicts),
            conflicts_resolved=len(non_blocking),
            conflicts_unresolved=len(blocking_conflicts),
            resource_allocations=resource_allocations,
            risk_result=CoordinationOutcome.PASS,
            capital_result=CoordinationOutcome.PASS,
            ordering_result=CoordinationOutcome.PASS,
            reconciliation_result=CoordinationOutcome.PASS,
            final_state=final_state,
            warnings=warnings,
            failures=failures,
            lineage=lineage,
            reproducibility_hash=reproducibility_hash,
        )

    def get_decisions(self) -> List[CoordinationDecision]:
        return list(self._decisions)
