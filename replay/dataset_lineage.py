"""
replay/dataset_lineage.py — ReplayDatasetLineageManager v1.2.8

Manages dataset lineage (parent/child version relationships).
Lineage is append-only; no cycles allowed.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from replay.dataset_registry_schema import ReplayDatasetLineageRecord, LineageOperation

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayDatasetLineageManager:
    """
    Manages dataset lineage records.

    Rules:
    - No cycles (validated on each registration)
    - Lineage is append-only
    - Parent version is immutable
    - Child must record the operation
    - Aggregate dataset records source resolution
    - Package import preserves original lineage references

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self):
        self._records: List[ReplayDatasetLineageRecord] = []

    def register_parent_child(
        self,
        parent_id: str,
        parent_version: str,
        child_id: str,
        child_version: str,
        operation: str = LineageOperation.DERIVE.value,
        source_ref: str = "",
        note: str = "",
    ) -> ReplayDatasetLineageRecord:
        """Register a parent→child lineage link. Raises ValueError on cycle."""
        rec = ReplayDatasetLineageRecord(
            lineage_id=str(uuid.uuid4())[:12],
            dataset_id=child_id,
            version=child_version,
            parent_dataset_id=parent_id,
            parent_version=parent_version,
            operation=operation,
            source_reference=source_ref,
            created_at=_now_utc(),
            note=note,
        )
        self._records.append(rec)
        if not self.validate_no_cycle(self._records):
            self._records.pop()
            raise ValueError(
                f"Cycle detected: {child_id}@{child_version} -> {parent_id}@{parent_version}"
            )
        return rec

    def list_lineage(self, dataset_id: str) -> List[ReplayDatasetLineageRecord]:
        return [r for r in self._records if r.dataset_id == dataset_id]

    def ancestors(self, dataset_id: str, version: str) -> List[str]:
        """Return list of ancestor dataset_id@version strings."""
        seen: Set[str] = set()
        result = []
        frontier = [(dataset_id, version)]
        while frontier:
            did, ver = frontier.pop()
            key = f"{did}@{ver}"
            if key in seen:
                continue
            seen.add(key)
            for r in self._records:
                if r.dataset_id == did and r.version == ver and r.parent_dataset_id:
                    anc = f"{r.parent_dataset_id}@{r.parent_version}"
                    if anc not in seen:
                        result.append(anc)
                        frontier.append((r.parent_dataset_id, r.parent_version or ""))
        return result

    def descendants(self, dataset_id: str, version: str) -> List[str]:
        """Return list of descendant dataset_id@version strings."""
        seen: Set[str] = set()
        result = []
        frontier = [(dataset_id, version)]
        while frontier:
            did, ver = frontier.pop()
            key = f"{did}@{ver}"
            if key in seen:
                continue
            seen.add(key)
            for r in self._records:
                if r.parent_dataset_id == did and r.parent_version == ver:
                    desc = f"{r.dataset_id}@{r.version}"
                    if desc not in seen:
                        result.append(desc)
                        frontier.append((r.dataset_id, r.version))
        return result

    def root(self, dataset_id: str) -> str:
        """Return the root ancestor dataset_id."""
        current = dataset_id
        for _ in range(100):  # cycle guard
            parent = None
            for r in self._records:
                if r.dataset_id == current and r.parent_dataset_id:
                    parent = r.parent_dataset_id
                    break
            if parent is None:
                break
            current = parent
        return current

    def validate_no_cycle(self, records: List[ReplayDatasetLineageRecord]) -> bool:
        """Return True if the lineage graph has no cycles."""
        graph: Dict[str, List[str]] = {}
        for r in records:
            graph.setdefault(r.dataset_id, [])
            if r.parent_dataset_id:
                graph.setdefault(r.parent_dataset_id, [])
                graph[r.dataset_id].append(r.parent_dataset_id)
        visited: Set[str] = set()
        in_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in in_stack:
                    return True
            in_stack.discard(node)
            return False

        for node in list(graph.keys()):
            if node not in visited:
                if dfs(node):
                    return False
        return True

    def render_tree(self, dataset_id: str) -> str:
        """Render a simple text tree of the lineage."""
        lines = [f"Lineage tree for: {dataset_id}"]
        ancestors = self.ancestors(dataset_id, "")
        if ancestors:
            lines.append("  Ancestors:")
            for a in ancestors:
                lines.append(f"    <- {a}")
        descendants = self.descendants(dataset_id, "")
        if descendants:
            lines.append("  Descendants:")
            for d in descendants:
                lines.append(f"    -> {d}")
        return "\n".join(lines)

    def summary(self, dataset_id: str) -> str:
        recs = self.list_lineage(dataset_id)
        return f"Dataset {dataset_id}: {len(recs)} lineage record(s)"
