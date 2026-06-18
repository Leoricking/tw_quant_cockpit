"""
replay/dataset_snapshot.py — ReplayDatasetSnapshot v1.2.8

Records point-in-time snapshots of dataset manifests.
Snapshots store manifest, hashes, file references, relative paths,
qualification, lineage, and source metadata — NOT raw data.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayDatasetSnapshot:
    """
    Point-in-time snapshot of a dataset manifest.

    Stores: manifest, hashes, file references, relative paths,
    qualification, lineage, source metadata.
    Does NOT copy raw data.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self):
        self._snapshots: List[Dict[str, Any]] = []

    def take_snapshot(
        self,
        dataset_id: str,
        version: str,
        manifest_hash: str,
        content_hash: str,
        fingerprint: str,
        relative_paths: List[str],
        qualification: str,
        lineage_refs: Optional[List[str]] = None,
        source_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Take a snapshot of the current dataset state."""
        snap = {
            "snapshot_id":   str(uuid.uuid4())[:12],
            "dataset_id":    dataset_id,
            "version":       version,
            "taken_at":      _now_utc(),
            "manifest_hash": manifest_hash,
            "content_hash":  content_hash,
            "fingerprint":   fingerprint,
            "relative_paths": relative_paths,
            "qualification": qualification,
            "lineage_refs":  lineage_refs or [],
            "source_metadata": source_metadata or {},
            "research_only": True,
            "no_real_orders": True,
        }
        self._snapshots.append(snap)
        return snap

    def list_snapshots(self, dataset_id: str) -> List[Dict[str, Any]]:
        return [s for s in self._snapshots if s["dataset_id"] == dataset_id]

    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        for s in self._snapshots:
            if s["snapshot_id"] == snapshot_id:
                return s
        return None

    def verify_snapshot(self, snapshot_id: str, current_fingerprint: str) -> bool:
        """Return True if snapshot fingerprint still matches current."""
        snap = self.get_snapshot(snapshot_id)
        if not snap:
            return False
        return snap["fingerprint"] == current_fingerprint
