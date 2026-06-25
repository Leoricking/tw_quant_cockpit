"""paper_trading/snapshot_v160.py — Paper Session Snapshot v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .models_v160 import PaperSessionSnapshot


class SnapshotService:
    """Creates and stores paper session snapshots."""

    def __init__(self) -> None:
        self._snapshots: List[PaperSessionSnapshot] = []

    def create(
        self,
        session_id: str,
        as_of: Optional[str] = None,
        positions: Optional[List[Dict[str, Any]]] = None,
        cash: Optional[Dict[str, Any]] = None,
        orders: Optional[List[Dict[str, Any]]] = None,
        fills: Optional[List[Dict[str, Any]]] = None,
        realized_pnl: Decimal = Decimal("0"),
        unrealized_pnl: Decimal = Decimal("0"),
        exposure: Decimal = Decimal("0"),
        drawdown: Decimal = Decimal("0"),
        risk_status: str = "PASS",
        event_sequence: int = 0,
        ledger_hash: str = "",
    ) -> PaperSessionSnapshot:
        if as_of is None:
            as_of = datetime.now(timezone.utc).isoformat()
        snapshot_id = f"snap_{uuid.uuid4().hex[:12]}"
        snap = PaperSessionSnapshot(
            snapshot_id=snapshot_id,
            session_id=session_id,
            as_of=as_of,
            positions=positions or [],
            cash=cash,
            orders=orders or [],
            fills=fills or [],
            realized_pnl=realized_pnl,
            unrealized_pnl=unrealized_pnl,
            total_pnl=realized_pnl + unrealized_pnl,
            exposure=exposure,
            drawdown=drawdown,
            risk_status=risk_status,
            event_sequence=event_sequence,
            ledger_hash=ledger_hash,
        )
        snap.content_hash = snap.compute_content_hash()
        self._snapshots.append(snap)
        return snap

    def get_latest(self) -> Optional[PaperSessionSnapshot]:
        return self._snapshots[-1] if self._snapshots else None

    def get_all(self) -> List[PaperSessionSnapshot]:
        return list(self._snapshots)

    def count(self) -> int:
        return len(self._snapshots)
