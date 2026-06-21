"""
portfolio/snapshot_v150.py — Immutable snapshot builder for v1.5.0.

Snapshots are frozen at creation time. They cannot be modified.
Each snapshot has a unique snapshot_id and as_of timestamp.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True


def _make_snapshot_id(portfolio_id: str, as_of: str, seq: int = 0) -> str:
    raw = f"{portfolio_id}::{as_of}::{seq}"
    return "SNAP-" + hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def _decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Not serializable: {type(obj)}")


class PortfolioSnapshotBuilder:
    RESEARCH_ONLY = True

    def build(
        self,
        portfolio_id: str,
        as_of: str,
        positions: List[Dict],
        cash_balances: List[Dict],
        valuation: Optional[Dict],
        metadata: Optional[Dict] = None,
        seq: int = 0,
    ) -> Dict[str, Any]:
        """
        Build an immutable snapshot dict.

        The snapshot is frozen: a content hash is computed and stored.
        The original data is not modified.
        """
        snapshot_id = _make_snapshot_id(portfolio_id, as_of, seq)
        created_at = datetime.now(timezone.utc).isoformat()

        snapshot = {
            "snapshot_id": snapshot_id,
            "portfolio_id": portfolio_id,
            "as_of": as_of,
            "created_at": created_at,
            "positions": positions,
            "cash_balances": cash_balances,
            "valuation": valuation,
            "metadata": metadata or {},
            "research_only": True,
            "immutable": True,
        }

        # Content hash for integrity verification
        canonical = json.dumps(snapshot, sort_keys=True, default=_decimal_serializer)
        snapshot["content_hash"] = hashlib.sha256(canonical.encode()).hexdigest()

        return snapshot

    def verify_integrity(self, snapshot: Dict[str, Any]) -> bool:
        """Verify snapshot content hash. Returns True if intact."""
        stored_hash = snapshot.get("content_hash")
        if not stored_hash:
            return False
        test = {k: v for k, v in snapshot.items() if k != "content_hash"}
        canonical = json.dumps(test, sort_keys=True, default=_decimal_serializer)
        return hashlib.sha256(canonical.encode()).hexdigest() == stored_hash
