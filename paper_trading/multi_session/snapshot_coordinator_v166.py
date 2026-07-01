"""
paper_trading/multi_session/snapshot_coordinator_v166.py — Snapshot Coordinator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List
from paper_trading.multi_session.models_v166 import CoordinationSnapshot

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class SnapshotCoordinator:
    """Creates immutable content-addressed coordination snapshots."""

    def create(
        self,
        session_states: Dict[str, str],
        resource_state: Dict[str, Any],
        risk_state: Dict[str, Any],
        capital_state: Dict[str, Any],
        symbol_exposure: Dict[str, Any],
        event_positions: Dict[str, int],
        active_conflicts: List[str],
        active_reservations: List[str],
        policy_versions: Dict[str, str],
    ) -> CoordinationSnapshot:
        now = datetime.now(timezone.utc)
        payload = {
            "session_states": dict(sorted(session_states.items())),
            "resource_state": resource_state,
            "risk_state": risk_state,
            "capital_state": capital_state,
            "symbol_exposure": symbol_exposure,
        }
        content_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
        return CoordinationSnapshot(
            snapshot_id=str(uuid.uuid4()),
            as_of=now,
            session_states=session_states,
            resource_state=resource_state,
            risk_state=risk_state,
            capital_state=capital_state,
            symbol_exposure=symbol_exposure,
            event_positions=event_positions,
            active_conflicts=active_conflicts,
            active_reservations=active_reservations,
            policy_versions=policy_versions,
            content_hash=content_hash,
        )
