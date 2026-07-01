"""
paper_trading/multi_session/market_data_sharing_v166.py — Market Data Sharing v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Only verified research/paper snapshots. No live→fixture fallback. No stale=healthy.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_LIVE_TO_FIXTURE_FALLBACK = True
NO_STALE_DATA_AS_HEALTHY = True
NO_MISSING_DATA_AS_ZERO = True


@dataclass
class SharedDataSnapshot:
    snapshot_id: str
    symbol: str
    provider: str
    as_of: datetime
    available_from: datetime
    quality_score: float
    source_lineage: str
    permitted_sessions: List[str]
    data: Dict[str, Any]
    is_fresh: bool
    pit_verified: bool


class MarketDataSharing:
    """Manages sharing of verified research/paper data snapshots between sessions."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, SharedDataSnapshot] = {}

    def register_snapshot(self, snapshot: SharedDataSnapshot) -> None:
        self._snapshots[snapshot.snapshot_id] = snapshot

    def get_for_session(
        self,
        session_id: str,
        symbol: str,
        as_of: datetime,
    ) -> Optional[SharedDataSnapshot]:
        for snap in self._snapshots.values():
            if (snap.symbol == symbol
                    and session_id in snap.permitted_sessions
                    and snap.available_from <= as_of
                    and snap.pit_verified
                    and snap.is_fresh):
                return snap
        return None

    def validate_access(
        self,
        session_id: str,
        snapshot_id: str,
    ) -> bool:
        snap = self._snapshots.get(snapshot_id)
        if snap is None:
            return False
        return session_id in snap.permitted_sessions

    def check_future_leakage(self, snapshot: SharedDataSnapshot, query_as_of: datetime) -> bool:
        return snapshot.available_from > query_as_of
