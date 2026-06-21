"""
data/governance/lineage_registry_v145.py — Source Lineage Registry v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] In-memory storage for offline/tests. SQLite optional for runtime.
[!] No token storage. No auth header storage.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from data.governance.models_v145 import (
    ProvenanceGateResult, SourceIdentity, SourceLineageRecord,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class SourceLineageRegistry:
    """
    Registry for source identities and lineage records.
    Storage: in-memory dict for offline/tests.
    """

    def __init__(self) -> None:
        self._sources: Dict[str, SourceIdentity] = {}
        self._lineage: Dict[str, SourceLineageRecord] = {}
        self._parent_map: Dict[str, List[str]] = {}  # child_id → [parent_ids]

    # ------------------------------------------------------------------
    # Source identity
    # ------------------------------------------------------------------

    def register_source(self, identity: SourceIdentity) -> str:
        self._sources[identity.source_id] = identity
        return identity.source_id

    def get_source(self, source_id: str) -> Optional[SourceIdentity]:
        return self._sources.get(source_id)

    def list_sources(self, provider_id: Optional[str] = None) -> List[Dict[str, Any]]:
        sources = list(self._sources.values())
        if provider_id is not None:
            sources = [s for s in sources if s.provider_id == provider_id]
        return [s.to_dict() for s in sources]

    # ------------------------------------------------------------------
    # Lineage records
    # ------------------------------------------------------------------

    def record_lineage(self, record: SourceLineageRecord) -> str:
        self._lineage[record.lineage_id] = record
        self._parent_map.setdefault(record.lineage_id, list(record.parent_lineage_ids))
        return record.lineage_id

    def link_parent_lineage(self, child_id: str, parent_id: str) -> None:
        if child_id not in self._parent_map:
            self._parent_map[child_id] = []
        if parent_id not in self._parent_map[child_id]:
            self._parent_map[child_id].append(parent_id)

    def get_lineage(self, lineage_id: str) -> Optional[SourceLineageRecord]:
        return self._lineage.get(lineage_id)

    def trace_to_root(self, lineage_id: str) -> List[str]:
        """Return chain from lineage_id up to root (BFS)."""
        chain: List[str] = []
        visited = set()
        queue = [lineage_id]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            chain.append(current)
            parents = self._parent_map.get(current, [])
            queue.extend(p for p in parents if p not in visited)
        return chain

    def trace_transformations(self, lineage_id: str) -> List[str]:
        record = self._lineage.get(lineage_id)
        if record is None:
            return []
        return list(record.transformation_ids)

    def get_record_lineage(self, record_key: str, provider_id: str) -> List[Dict[str, Any]]:
        results = []
        for rec in self._lineage.values():
            if rec.record_key == record_key and rec.provider_id == provider_id:
                results.append(rec.to_dict())
        return results

    def validate_lineage(self, lineage_id: str) -> Dict[str, Any]:
        record = self._lineage.get(lineage_id)
        if record is None:
            return {"is_valid": False, "issues": ["lineage_id not found"]}
        issues = []
        if not record.provider_id:
            issues.append("missing provider_id")
        if not record.source_id:
            issues.append("missing source_id")
        if not record.fetched_at:
            issues.append("missing fetched_at")
        if not record.source_content_hash:
            issues.append("missing source_content_hash")
        return {"is_valid": len(issues) == 0, "issues": issues}

    def validate_authority(self, lineage_id: str) -> Dict[str, Any]:
        record = self._lineage.get(lineage_id)
        if record is None:
            return {"valid": False, "reason": "lineage_id not found"}
        return {
            "lineage_id": lineage_id,
            "authority_level": record.authority_level,
            "formal_use_allowed": record.formal_use_allowed,
            "valid": True,
        }

    def validate_provenance_completeness(self, lineage_id: str) -> ProvenanceGateResult:
        record = self._lineage.get(lineage_id)
        if record is None:
            return ProvenanceGateResult.FAIL
        required = [
            record.provider_id, record.source_id, record.authority_level,
            record.dataset, record.request_fingerprint, record.fetched_at,
            record.source_content_hash, record.normalized_content_hash,
            record.schema_version, record.parser_version,
        ]
        if not all(required):
            return ProvenanceGateResult.FAIL
        if not (record.observation_date or record.reporting_period):
            return ProvenanceGateResult.FAIL
        if record.authority_level in ("MOCK", "TEST_FIXTURE"):
            return ProvenanceGateResult.BLOCKED
        return ProvenanceGateResult.PASS

    def compare_lineage(self, lineage_id_a: str, lineage_id_b: str) -> Dict[str, Any]:
        a = self._lineage.get(lineage_id_a)
        b = self._lineage.get(lineage_id_b)
        return {
            "lineage_id_a": lineage_id_a,
            "lineage_id_b": lineage_id_b,
            "a_found": a is not None,
            "b_found": b is not None,
            "same_provider": (a is not None and b is not None and a.provider_id == b.provider_id),
            "same_dataset": (a is not None and b is not None and a.dataset == b.dataset),
        }

    def list_incomplete_lineage(self, provider_id: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for rec in self._lineage.values():
            if provider_id and rec.provider_id != provider_id:
                continue
            v = self.validate_lineage(rec.lineage_id)
            if not v["is_valid"] or not rec.provenance_complete:
                results.append(rec.to_dict())
        return results
