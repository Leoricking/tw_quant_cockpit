"""
paper_trading/failure_validation/baseline_snapshot_v165.py — Baseline snapshot for failure injection v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] Immutable, content-addressed, deterministic. No external system reads.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.failure_validation.models_v165 import BaselineSnapshot

REAL_FAILURE_INJECTION_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BaselineSnapshotManager:
    """Manages immutable baseline snapshots for failure injection validation."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, BaselineSnapshot] = {}

    def capture(self, component: str, state_data: Dict[str, Any], seed: int = 42) -> BaselineSnapshot:
        """Capture an immutable baseline snapshot."""
        snap = BaselineSnapshot(
            component=component,
            state_data=state_data,
            seed=seed,
            deterministic=True,
        )
        self._snapshots[snap.snapshot_id] = snap
        return snap

    def verify(self, snapshot_id: str) -> bool:
        """Verify a stored snapshot's integrity."""
        snap = self._snapshots.get(snapshot_id)
        if snap is None:
            return False
        return snap.verify_integrity()

    def get(self, snapshot_id: str) -> Optional[BaselineSnapshot]:
        return self._snapshots.get(snapshot_id)

    def compare(self, snap_a_id: str, snap_b_id: str) -> Dict[str, Any]:
        """Compare two snapshots by content hash."""
        snap_a = self._snapshots.get(snap_a_id)
        snap_b = self._snapshots.get(snap_b_id)
        if snap_a is None or snap_b is None:
            return {"match": False, "reason": "One or both snapshots not found"}
        match = snap_a.content_hash == snap_b.content_hash
        return {
            "match": match,
            "hash_a": snap_a.content_hash,
            "hash_b": snap_b.content_hash,
            "component_a": snap_a.component,
            "component_b": snap_b.component,
        }

    def all_snapshot_ids(self) -> List[str]:
        return list(self._snapshots.keys())

    def count(self) -> int:
        return len(self._snapshots)


def build_deterministic_state(component: str, seed: int, version: str = "1.6.5") -> Dict[str, Any]:
    """Build a deterministic synthetic state for a component (for testing)."""
    import random
    rng = random.Random(seed)
    return {
        "component": component,
        "version": version,
        "seed": seed,
        "values": [rng.randint(0, 1000) for _ in range(5)],
        "flags": {
            "healthy": True,
            "paper_only": True,
            "research_only": True,
        },
        "generated_at": "2026-01-01T00:00:00+00:00",  # Deterministic, not real time
    }
