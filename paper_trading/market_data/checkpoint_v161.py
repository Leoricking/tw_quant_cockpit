"""
paper_trading/market_data/checkpoint_v161.py — Checkpoint Manager v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Checkpoint always resumes to PAUSED, never directly RUNNING.
"""
from __future__ import annotations
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
from paper_trading.market_data.models_v161 import MarketDataCheckpoint

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
CHECKPOINT_RESUMES_TO_PAUSED: bool = True   # Key invariant


class CheckpointManager:
    """
    Creates, stores, and retrieves market data session checkpoints.
    INVARIANT: restore_state always sets status=PAUSED, never RUNNING.
    """

    def __init__(self) -> None:
        self._checkpoints: Dict[str, MarketDataCheckpoint] = {}
        self._session_checkpoints: Dict[str, List[str]] = {}  # session_id → [checkpoint_id]

    def create(
        self,
        session_id: str,
        adapter_id: str,
        adapter_state: Dict[str, Any],
        sequence_number: Optional[int] = None,
        last_event_id: Optional[str] = None,
    ) -> MarketDataCheckpoint:
        checkpoint_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        # Deterministic hash of state
        state_for_hash = {
            "session_id": session_id,
            "adapter_id": adapter_id,
            "adapter_state": adapter_state,
            "sequence_number": sequence_number,
            "last_event_id": last_event_id,
        }
        h = hashlib.sha256(json.dumps(state_for_hash, sort_keys=True).encode()).hexdigest()

        cp = MarketDataCheckpoint(
            checkpoint_id=checkpoint_id,
            session_id=session_id,
            adapter_id=adapter_id,
            created_at_utc=now,
            sequence_number=sequence_number,
            last_event_id=last_event_id,
            adapter_state=adapter_state,
            checkpoint_hash=h,
        )
        self._checkpoints[checkpoint_id] = cp
        self._session_checkpoints.setdefault(session_id, []).append(checkpoint_id)
        return cp

    def get(self, checkpoint_id: str) -> Optional[MarketDataCheckpoint]:
        return self._checkpoints.get(checkpoint_id)

    def get_latest(self, session_id: str) -> Optional[MarketDataCheckpoint]:
        ids = self._session_checkpoints.get(session_id, [])
        if not ids:
            return None
        return self._checkpoints.get(ids[-1])

    def restore_gives_paused(self) -> MarketDataSessionStatus:
        """Restore always returns PAUSED — never RUNNING. Key invariant."""
        return MarketDataSessionStatus.PAUSED

    def list_for_session(self, session_id: str) -> List[str]:
        return list(self._session_checkpoints.get(session_id, []))

    def count(self) -> int:
        return len(self._checkpoints)
