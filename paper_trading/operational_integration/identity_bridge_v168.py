"""
paper_trading/operational_integration/identity_bridge_v168.py
Identity Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import IdentityRecord
from .enums_v168 import IdentityStatus

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_FIXTURE_PREFIXES = ("fixture_", "fx_", "test_", "mock_", "demo_")


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class IdentityBridge:
    """Tracks and validates entity identities. Research only."""

    def __init__(self) -> None:
        self._records: List[IdentityRecord] = []
        self._entity_index: Dict[str, List[IdentityRecord]] = {}

    def register(
        self,
        entity_type: str,
        entity_id: str,
        component_id: str,
        session_id: str,
    ) -> IdentityRecord:
        """Register an entity identity."""
        identity_id = f"id_{entity_type}_{entity_id}_{component_id}"
        rec = IdentityRecord(
            identity_id=identity_id,
            component_id=component_id,
            run_id="",
            session_id=session_id,
            status=IdentityStatus.VALID,
        )
        self._records.append(rec)
        key = entity_type
        if key not in self._entity_index:
            self._entity_index[key] = []
        self._entity_index[key].append(rec)
        return rec

    def check_duplicates(self, entity_type: str) -> List[Dict[str, Any]]:
        """Return duplicate identity records for entity_type."""
        records = self._entity_index.get(entity_type, [])
        seen: Dict[str, str] = {}
        duplicates = []
        for rec in records:
            key = f"{rec.component_id}:{rec.session_id}"
            if key in seen:
                duplicates.append({
                    "identity_id": rec.identity_id,
                    "duplicate_of": seen[key],
                    "entity_type": entity_type,
                })
            else:
                seen[key] = rec.identity_id
        return duplicates

    def check_missing(self, required_ids: List[str], entity_type: str) -> List[str]:
        """Return required_ids not found in registered identities."""
        registered = {r.identity_id for r in self._entity_index.get(entity_type, [])}
        return [rid for rid in required_ids if rid not in registered]

    def check_conflicts(self, entity_type: str) -> List[Dict[str, Any]]:
        """Return identities with conflicting session assignments."""
        records = self._entity_index.get(entity_type, [])
        session_map: Dict[str, str] = {}
        conflicts = []
        for rec in records:
            if rec.component_id in session_map:
                if session_map[rec.component_id] != rec.session_id:
                    conflicts.append({
                        "component_id": rec.component_id,
                        "session_1": session_map[rec.component_id],
                        "session_2": rec.session_id,
                        "identity_id": rec.identity_id,
                    })
            else:
                session_map[rec.component_id] = rec.session_id
        return conflicts

    def check_session_collision(self, session_id1: str, session_id2: str) -> bool:
        """Return True if both sessions have overlapping component assignments."""
        components_1 = {r.component_id for r in self._records if r.session_id == session_id1}
        components_2 = {r.component_id for r in self._records if r.session_id == session_id2}
        return len(components_1 & components_2) > 0

    def normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol to uppercase, strip whitespace."""
        if not symbol:
            return ""
        normalized = symbol.strip().upper()
        # Remove common suffixes for TW stocks
        for suffix in [".TW", ".TWO"]:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
        return normalized

    def check_fixture_leakage(self, entity_id: str) -> bool:
        """Return True if entity_id appears to be a fixture/test identity."""
        lower = entity_id.lower()
        return any(lower.startswith(prefix) for prefix in _FIXTURE_PREFIXES)

    def get_orphans(self, entity_type: str) -> List[Dict[str, Any]]:
        """Return records that have no valid session assignment."""
        records = self._entity_index.get(entity_type, [])
        orphans = []
        valid_sessions = {r.session_id for r in self._records if r.session_id}
        for rec in records:
            if rec.session_id not in valid_sessions or not rec.session_id:
                orphans.append({
                    "identity_id": rec.identity_id,
                    "component_id": rec.component_id,
                    "session_id": rec.session_id,
                    "status": IdentityStatus.ORPHAN.value,
                })
        return orphans

    def summarize(self) -> Dict[str, Any]:
        """Return summary of identity records."""
        total = len(self._records)
        entity_types = len(self._entity_index)
        fixture_leaked = sum(1 for r in self._records if self.check_fixture_leakage(r.identity_id))
        return {
            "total_identities": total,
            "entity_types": entity_types,
            "fixture_leaked_count": fixture_leaked,
            "paper_only": True,
            "research_only": True,
        }
