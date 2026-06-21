"""
data/governance/cache_lineage_v145.py — Cache Lineage Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Corrupt cache → invalid lineage. Mock cache → no real lineage. Stale → no fresh status.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CacheLineageService:
    """
    Tracks lineage from cache entries back to source lineage.
    Rules:
    - Corrupt cache → invalid lineage
    - Mock cache → no real lineage
    - Stale → no fresh status
    """

    def __init__(self) -> None:
        self._entries: Dict[str, Dict[str, Any]] = {}
        self._invalidated: Dict[str, str] = {}  # cache_entry_id → reason

    def record_cache_entry(
        self,
        cache_entry_id: str,
        provider_id: str,
        request_fingerprint: str,
        source_lineage_id: str,
        schema_version: str,
        parser_version: str,
        content_hash: str,
        mode: str,
        authority: str,
        freshness_at_write: str,
    ) -> None:
        self._entries[cache_entry_id] = {
            "cache_entry_id": cache_entry_id,
            "provider_id": provider_id,
            "request_fingerprint": request_fingerprint,
            "source_lineage_id": source_lineage_id,
            "schema_version": schema_version,
            "parser_version": parser_version,
            "content_hash": content_hash,
            "mode": mode,
            "authority": authority,
            "freshness_at_write": freshness_at_write,
            "invalidated": False,
        }

    def get_cache_entry(self, cache_entry_id: str) -> Optional[Dict[str, Any]]:
        return self._entries.get(cache_entry_id)

    def invalidate(self, cache_entry_id: str, reason: str) -> None:
        if cache_entry_id in self._entries:
            self._entries[cache_entry_id]["invalidated"] = True
            self._invalidated[cache_entry_id] = reason

    def trace_to_source(self, cache_entry_id: str) -> Dict[str, Any]:
        entry = self._entries.get(cache_entry_id)
        if entry is None:
            return {"cache_entry_id": cache_entry_id, "found": False, "source_lineage_chain": []}
        chain = []
        if entry.get("source_lineage_id"):
            chain.append(entry["source_lineage_id"])
        return {
            "cache_entry_id": cache_entry_id,
            "found": True,
            "source_lineage_chain": chain,
            "invalidated": entry.get("invalidated", False),
        }

    def validate_cache_lineage(self, cache_entry_id: str) -> Dict[str, Any]:
        entry = self._entries.get(cache_entry_id)
        if entry is None:
            return {"is_complete": False, "issues": ["cache_entry_id not found"]}

        issues: List[str] = []
        if entry.get("invalidated"):
            reason = self._invalidated.get(cache_entry_id, "unknown")
            issues.append(f"cache invalidated: {reason}")
        if entry.get("authority") in ("MOCK", "TEST_FIXTURE"):
            issues.append("mock/fixture cache has no real lineage")
        if not entry.get("source_lineage_id"):
            issues.append("missing source_lineage_id")
        if not entry.get("content_hash"):
            issues.append("missing content_hash")

        return {
            "is_complete": len(issues) == 0,
            "issues": issues,
            "cache_entry_id": cache_entry_id,
        }
