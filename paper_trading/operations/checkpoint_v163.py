"""
Checkpoint v1.6.3 — Hash-verified, restore as PAUSED only.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import OperationalStatus
from paper_trading.operations.models_v163 import _new_id, _now_utc


@dataclass
class OperationsCheckpoint:
    checkpoint_id:     str
    supervisor_id:     str
    version:           str
    supervisor_state:  Dict[str, Any]    = field(default_factory=dict)
    managed_sessions:  List[str]         = field(default_factory=list)
    dependency_graph:  Dict[str, Any]    = field(default_factory=dict)
    metric_counters:   Dict[str, float]  = field(default_factory=dict)
    alert_state:       List[str]         = field(default_factory=list)
    incident_state:    List[str]         = field(default_factory=list)
    operation_sequence: int              = 0
    event_bus_sequence: int              = 0
    journal_hash:      str               = ""
    snapshot_hash:     str               = ""
    policy_versions:   Dict[str, str]    = field(default_factory=dict)
    content_hash:      str               = ""
    created_at:        Optional[datetime] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = _now_utc()
        if not self.content_hash:
            self.content_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        data = {
            "checkpoint_id":    self.checkpoint_id,
            "supervisor_id":    self.supervisor_id,
            "version":          self.version,
            "managed_sessions": sorted(self.managed_sessions),
            "operation_sequence": self.operation_sequence,
            "event_bus_sequence": self.event_bus_sequence,
            "journal_hash":     self.journal_hash,
            "snapshot_hash":    self.snapshot_hash,
        }
        serialized = json.dumps(data, sort_keys=True, default=str)
        return "sha256:" + hashlib.sha256(serialized.encode()).hexdigest()


class CheckpointService:
    def create(
        self,
        supervisor_id:     str,
        version:           str = "1.6.3",
        managed_sessions:  Optional[List[str]]        = None,
        metric_counters:   Optional[Dict[str, float]] = None,
        journal_hash:      str = "",
        snapshot_hash:     str = "",
        operation_sequence: int = 0,
        event_bus_sequence: int = 0,
        policy_versions:   Optional[Dict[str, str]]  = None,
    ) -> OperationsCheckpoint:
        return OperationsCheckpoint(
            checkpoint_id=_new_id("chk_"),
            supervisor_id=supervisor_id,
            version=version,
            managed_sessions=managed_sessions or [],
            metric_counters=metric_counters or {},
            journal_hash=journal_hash,
            snapshot_hash=snapshot_hash,
            operation_sequence=operation_sequence,
            event_bus_sequence=event_bus_sequence,
            policy_versions=policy_versions or {"default": version},
        )

    def verify(self, checkpoint: OperationsCheckpoint) -> Tuple[bool, str]:
        expected = checkpoint._compute_hash()
        if expected != checkpoint.content_hash:
            return False, f"Checkpoint hash mismatch: expected {expected[:20]}... got {checkpoint.content_hash[:20]}..."
        return True, "Checkpoint valid"

    def restore_status(self) -> OperationalStatus:
        """Restore always returns PAUSED — no auto-RUNNING."""
        return OperationalStatus.PAUSED


__all__ = ["OperationsCheckpoint", "CheckpointService"]
