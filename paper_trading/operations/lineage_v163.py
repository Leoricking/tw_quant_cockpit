"""
Session Operations Lineage v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from paper_trading.operations.models_v163 import _new_id


@dataclass
class LineageRecord:
    lineage_id:     str
    entity_type:    str    # snapshot, metric, alert, incident, operation, checkpoint
    entity_id:      str
    parent_ids:     List[str]        = field(default_factory=list)
    source_session: Optional[str]    = None
    policy_version: str              = "1.6.3"
    code_version:   str              = "1.6.3"
    metadata:       Dict[str, Any]   = field(default_factory=dict)


class LineageService:
    """
    Tracks lineage from Snapshot → ManagedSession → Health → Metrics →
    Alerts → Incidents → Operations → Checkpoints → Source Session Events.

    Requirements:
    - orphan metric = 0
    - orphan alert = 0
    - orphan incident = 0
    - orphan operation = 0
    - orphan checkpoint = 0
    - missing policy version = 0
    - missing code version = 0
    - missing source session = 0
    """

    def __init__(self):
        self._records: Dict[str, LineageRecord] = {}

    def record(
        self,
        entity_type:    str,
        entity_id:      str,
        parent_ids:     Optional[List[str]] = None,
        source_session: Optional[str] = None,
        policy_version: str = "1.6.3",
        code_version:   str = "1.6.3",
        metadata:       Optional[Dict[str, Any]] = None,
    ) -> LineageRecord:
        rec = LineageRecord(
            lineage_id=_new_id("lin_"),
            entity_type=entity_type,
            entity_id=entity_id,
            parent_ids=parent_ids or [],
            source_session=source_session,
            policy_version=policy_version,
            code_version=code_version,
            metadata=metadata or {},
        )
        self._records[rec.lineage_id] = rec
        return rec

    def find_by_entity(self, entity_id: str) -> Optional[LineageRecord]:
        for rec in self._records.values():
            if rec.entity_id == entity_id:
                return rec
        return None

    def orphans(self, entity_type: str) -> List[LineageRecord]:
        """Records of given type with no parent lineage."""
        return [r for r in self._records.values()
                if r.entity_type == entity_type and not r.parent_ids and not r.source_session]

    def audit_summary(self) -> Dict[str, int]:
        from collections import Counter
        c = Counter(r.entity_type for r in self._records.values())
        orphan_counts: Dict[str, int] = {}
        for et in ["metric", "alert", "incident", "operation", "checkpoint"]:
            orphan_counts[f"orphan_{et}"] = len(self.orphans(et))
        return {**dict(c), **orphan_counts}

    def total_records(self) -> int:
        return len(self._records)

    def verify_completeness(self) -> Tuple[bool, List[str]]:
        issues = []
        for rec in self._records.values():
            if not rec.policy_version:
                issues.append(f"{rec.entity_id}: missing policy_version")
            if not rec.code_version:
                issues.append(f"{rec.entity_id}: missing code_version")
        return len(issues) == 0, issues


__all__ = ["LineageRecord", "LineageService"]
