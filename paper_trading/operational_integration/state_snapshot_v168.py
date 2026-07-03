"""
paper_trading/operational_integration/state_snapshot_v168.py
State Snapshot Manager for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import IntegrationSnapshot
from .enums_v168 import SnapshotType

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class StateSnapshotManager:
    """Manages integration state snapshots. Research only."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, IntegrationSnapshot] = {}

    def take_snapshot(
        self,
        run_id: str,
        components: Dict[str, Any],
        snapshot_type: SnapshotType = SnapshotType.FULL,
    ) -> IntegrationSnapshot:
        """Take a snapshot of current integration state."""
        snapshot_id = f"snap_{run_id}_{len(self._snapshots)}"
        snapshot = IntegrationSnapshot(
            snapshot_id=snapshot_id,
            run_id=run_id,
            snapshot_type=snapshot_type,
            components=dict(components),
            created_at=_utcnow_iso(),
        )
        self._snapshots[snapshot_id] = snapshot
        return snapshot

    def restore_snapshot(self, snapshot_id: str) -> Optional[IntegrationSnapshot]:
        """Restore a snapshot by ID. Returns None if not found."""
        return self._snapshots.get(snapshot_id)

    def compare_snapshots(self, s1_id: str, s2_id: str) -> Dict[str, Any]:
        """Compare two snapshots and return differences."""
        s1 = self._snapshots.get(s1_id)
        s2 = self._snapshots.get(s2_id)
        if s1 is None:
            return {"error": f"snapshot not found: {s1_id}", "paper_only": True}
        if s2 is None:
            return {"error": f"snapshot not found: {s2_id}", "paper_only": True}

        keys1 = set(s1.components.keys())
        keys2 = set(s2.components.keys())
        added = keys2 - keys1
        removed = keys1 - keys2
        common = keys1 & keys2
        changed = [k for k in common if s1.components[k] != s2.components[k]]

        return {
            "snapshot_1": s1_id,
            "snapshot_2": s2_id,
            "added_components": list(added),
            "removed_components": list(removed),
            "changed_components": changed,
            "identical": len(added) == 0 and len(removed) == 0 and len(changed) == 0,
            "paper_only": True,
        }

    def list_snapshots(self) -> List[Dict[str, Any]]:
        """Return list of all snapshot summaries."""
        return [
            {
                "snapshot_id": s.snapshot_id,
                "run_id": s.run_id,
                "snapshot_type": s.snapshot_type.value,
                "created_at": s.created_at,
                "component_count": len(s.components),
            }
            for s in self._snapshots.values()
        ]

    def export_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Export a snapshot as a plain dict."""
        snap = self._snapshots.get(snapshot_id)
        if snap is None:
            return {"error": f"snapshot not found: {snapshot_id}", "paper_only": True}
        return {
            "snapshot_id": snap.snapshot_id,
            "run_id": snap.run_id,
            "snapshot_type": snap.snapshot_type.value,
            "components": dict(snap.components),
            "created_at": snap.created_at,
            "paper_only": True,
            "research_only": True,
        }
