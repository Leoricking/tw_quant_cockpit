"""
paper_trading/multi_session/coordination_context_v166.py — Coordination Context v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.models_v166 import SessionDescriptor, CoordinationPolicy, CoordinationSnapshot

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


@dataclass
class CoordinationContext:
    sessions: List[SessionDescriptor]
    policy: CoordinationPolicy
    virtual_clock: datetime
    seed: int
    resource_state: Dict[str, Any] = field(default_factory=dict)
    risk_state: Dict[str, Any] = field(default_factory=dict)
    capital_state: Dict[str, Any] = field(default_factory=dict)
    symbol_exposure: Dict[str, Any] = field(default_factory=dict)
    event_positions: Dict[str, int] = field(default_factory=dict)
    active_conflicts: List[str] = field(default_factory=list)
    active_reservations: List[str] = field(default_factory=list)
    prior_snapshot: Optional[CoordinationSnapshot] = None

    @property
    def session_ids(self) -> List[str]:
        return [s.session_id for s in self.sessions]

    def to_input_hash(self) -> str:
        import hashlib, json
        data = {
            "sessions": sorted(self.session_ids),
            "policy": self.policy.policy_id,
            "virtual_clock": self.virtual_clock.isoformat(),
            "seed": self.seed,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]
