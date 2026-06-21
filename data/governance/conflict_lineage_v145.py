"""
data/governance/conflict_lineage_v145.py — Conflict Lineage Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Primary always wins. No auto-repair. Resolution auditable. Old record NOT deleted.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from data.governance.models_v145 import ConflictLineage

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ConflictLineageService:
    """
    Service for tracking data conflicts between providers.
    Rules:
    - Primary always wins
    - No auto-repair
    - Resolution is auditable (old record preserved, not deleted)
    """

    def __init__(self) -> None:
        self._conflicts: Dict[str, ConflictLineage] = {}
        self._resolutions: Dict[str, Dict[str, Any]] = {}
        self._order: List[str] = []

    def record_conflict(self, conflict: ConflictLineage) -> str:
        if not conflict.conflict_id:
            conflict.conflict_id = str(uuid.uuid4())
        self._conflicts[conflict.conflict_id] = conflict
        if conflict.conflict_id not in self._order:
            self._order.append(conflict.conflict_id)
        return conflict.conflict_id

    def get_conflict(self, conflict_id: str) -> Optional[ConflictLineage]:
        return self._conflicts.get(conflict_id)

    def list_conflicts(
        self,
        primary_provider: Optional[str] = None,
        secondary_provider: Optional[str] = None,
        unresolved_only: bool = False,
    ) -> List[Dict[str, Any]]:
        results = []
        for cid in self._order:
            c = self._conflicts[cid]
            if primary_provider and c.primary_provider != primary_provider:
                continue
            if secondary_provider and c.secondary_provider != secondary_provider:
                continue
            if unresolved_only and c.reviewed:
                continue
            results.append(c.to_dict())
        return results

    def list_blocking_conflicts(self) -> List[Dict[str, Any]]:
        return [
            self._conflicts[cid].to_dict()
            for cid in self._order
            if self._conflicts[cid].formal_use_blocked
        ]

    def resolve_conflict(
        self,
        conflict_id: str,
        resolution: str,
        reviewer: str,
    ) -> None:
        """
        Mark conflict as reviewed with resolution. Old record preserved.
        [!] No auto-repair. Auditable only.
        """
        conflict = self._conflicts.get(conflict_id)
        if conflict is None:
            return
        # Preserve old record by storing resolution metadata separately
        self._resolutions[conflict_id] = {
            "resolution": resolution,
            "reviewer": reviewer,
            "previous_reviewed": conflict.reviewed,
            "previous_resolution": conflict.resolution,
        }
        # Update conflict (old record preserved in _resolutions)
        conflict.reviewed = True
        conflict.resolution = resolution
