"""
paper_trading/operational_integration/lineage_bridge_v168.py
Lineage Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import LineageRecord
from .enums_v168 import LineageStatus

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class LineageBridge:
    """Tracks and validates lineage chains across components."""

    def __init__(self) -> None:
        self._records: Dict[str, LineageRecord] = {}

    def record(
        self,
        component_id: str,
        parent_lineage_id: str,
        lineage_type: str,
        is_fixture: bool = False,
        is_mock: bool = False,
        is_paper: bool = True,
    ) -> LineageRecord:
        """Record a new lineage entry."""
        import uuid
        lineage_id = f"lin_{component_id}_{len(self._records)}"
        rec = LineageRecord(
            lineage_id=lineage_id,
            component_id=component_id,
            parent_lineage_id=parent_lineage_id,
            lineage_type=lineage_type,
            source_lineage=f"{component_id}:{lineage_type}",
            created_at=_utcnow_iso(),
            is_fixture=is_fixture,
            is_mock=is_mock,
            is_paper=is_paper,
        )
        self._records[lineage_id] = rec
        return rec

    def check_chain(self, lineage_id: str) -> Dict[str, Any]:
        """Walk the chain from lineage_id to root, detecting breaks."""
        chain = []
        current = lineage_id
        visited = set()
        broken = False
        while current:
            if current in visited:
                broken = True
                break
            visited.add(current)
            rec = self._records.get(current)
            if rec is None:
                broken = current != "" and current != "ROOT"
                break
            chain.append(current)
            current = rec.parent_lineage_id
        return {
            "lineage_id": lineage_id,
            "chain_length": len(chain),
            "chain": chain,
            "broken": broken,
            "status": LineageStatus.BROKEN_CHAIN.value if broken else LineageStatus.COMPLETE.value,
            "paper_only": True,
        }

    def check_duplicates(self) -> List[Dict[str, Any]]:
        """Check for duplicate lineage IDs."""
        seen = {}
        duplicates = []
        for lid, rec in self._records.items():
            key = (rec.component_id, rec.parent_lineage_id, rec.lineage_type)
            if key in seen:
                duplicates.append({
                    "lineage_id": lid,
                    "duplicate_of": seen[key],
                    "component_id": rec.component_id,
                })
            else:
                seen[key] = lid
        return duplicates

    def check_broken_chains(self) -> List[Dict[str, Any]]:
        """Check all chains and return those that are broken."""
        broken = []
        for lid in self._records:
            result = self.check_chain(lid)
            if result["broken"]:
                broken.append(result)
        return broken

    def check_stale(self, lineage_id: str, max_age_seconds: float) -> bool:
        """Return True if lineage record is older than max_age_seconds."""
        rec = self._records.get(lineage_id)
        if rec is None:
            return True
        now = datetime.now(timezone.utc)
        try:
            ts = datetime.fromisoformat(rec.created_at.replace("Z", "+00:00"))
            age = (now - ts).total_seconds()
            return age > max_age_seconds
        except Exception:
            return True

    def check_fixture_contamination(self, lineage_id: str) -> bool:
        """Return True if any record in the chain is a fixture."""
        chain_result = self.check_chain(lineage_id)
        for lid in chain_result["chain"]:
            rec = self._records.get(lid)
            if rec and rec.is_fixture:
                return True
        return False

    def rebuild_chain(self, lineage_id: str) -> List[LineageRecord]:
        """Return ordered list of records from root to lineage_id."""
        chain_ids = []
        current = lineage_id
        visited = set()
        while current and current not in visited:
            visited.add(current)
            rec = self._records.get(current)
            if rec is None:
                break
            chain_ids.append(current)
            current = rec.parent_lineage_id
        chain_ids.reverse()
        return [self._records[lid] for lid in chain_ids if lid in self._records]

    def summarize(self) -> Dict[str, Any]:
        """Return summary of all lineage records."""
        total = len(self._records)
        fixture_count = sum(1 for r in self._records.values() if r.is_fixture)
        mock_count = sum(1 for r in self._records.values() if r.is_mock)
        broken_chains = len(self.check_broken_chains())
        duplicates = len(self.check_duplicates())
        return {
            "total_records": total,
            "fixture_records": fixture_count,
            "mock_records": mock_count,
            "broken_chains": broken_chains,
            "duplicate_records": duplicates,
            "paper_only": True,
            "research_only": True,
        }
