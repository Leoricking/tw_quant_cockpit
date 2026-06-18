"""
replay/session_lineage_registry.py — ReplaySessionLineageRegistry v1.2.8

Manages session lineage (root, duplicated, forked, challenge-derived,
imported, restored sessions).
No cycles allowed. Lineage is append-only.

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplaySessionLineageRegistry:
    """
    Manages session lineage.

    Supports: root, duplicated, forked, challenge-derived, imported, restored sessions.
    Rules: no cycles, append-only.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self):
        self._records: List[Dict[str, Any]] = []

    def register_lineage(
        self,
        session_id: str,
        parent_session_id: Optional[str] = None,
        lineage_type: str = "root",
        note: str = "",
    ) -> Dict[str, Any]:
        """Register a session lineage record. Raises ValueError on cycle."""
        rec = {
            "lineage_id":        str(uuid.uuid4())[:12],
            "session_id":        session_id,
            "parent_session_id": parent_session_id,
            "lineage_type":      lineage_type,  # root/fork/duplicate/challenge/import/restore
            "created_at":        _now_utc(),
            "note":              note,
            "research_only":     True,
            "no_real_orders":    True,
        }
        self._records.append(rec)
        if not self.validate_no_cycle(self._records):
            self._records.pop()
            raise ValueError(f"Cycle detected: {session_id} -> {parent_session_id}")
        return rec

    def ancestors(self, session_id: str) -> List[str]:
        seen: Set[str] = set()
        result = []
        frontier = [session_id]
        while frontier:
            sid = frontier.pop()
            if sid in seen:
                continue
            seen.add(sid)
            for r in self._records:
                if r["session_id"] == sid and r.get("parent_session_id"):
                    parent = r["parent_session_id"]
                    if parent not in seen:
                        result.append(parent)
                        frontier.append(parent)
        return result

    def descendants(self, session_id: str) -> List[str]:
        seen: Set[str] = set()
        result = []
        frontier = [session_id]
        while frontier:
            sid = frontier.pop()
            if sid in seen:
                continue
            seen.add(sid)
            for r in self._records:
                if r.get("parent_session_id") == sid:
                    child = r["session_id"]
                    if child not in seen:
                        result.append(child)
                        frontier.append(child)
        return result

    def root(self, session_id: str) -> str:
        current = session_id
        for _ in range(100):
            parent = None
            for r in self._records:
                if r["session_id"] == current and r.get("parent_session_id"):
                    parent = r["parent_session_id"]
                    break
            if parent is None:
                break
            current = parent
        return current

    def siblings(self, session_id: str) -> List[str]:
        parent = None
        for r in self._records:
            if r["session_id"] == session_id and r.get("parent_session_id"):
                parent = r["parent_session_id"]
                break
        if not parent:
            return []
        return [
            r["session_id"] for r in self._records
            if r.get("parent_session_id") == parent and r["session_id"] != session_id
        ]

    def validate_no_cycle(self, records: List[Dict[str, Any]]) -> bool:
        """Return True if no cycles exist."""
        graph: Dict[str, List[str]] = {}
        for r in records:
            sid = r["session_id"]
            parent = r.get("parent_session_id")
            graph.setdefault(sid, [])
            if parent:
                graph.setdefault(parent, [])
                graph[sid].append(parent)
        visited: Set[str] = set()
        in_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for nb in graph.get(node, []):
                if nb not in visited:
                    if dfs(nb):
                        return True
                elif nb in in_stack:
                    return True
            in_stack.discard(node)
            return False

        for node in list(graph.keys()):
            if node not in visited:
                if dfs(node):
                    return False
        return True

    def render_tree(self, session_id: str) -> str:
        lines = [f"Lineage tree for session: {session_id}"]
        ancs = self.ancestors(session_id)
        if ancs:
            lines.append("  Ancestors:")
            for a in ancs:
                lines.append(f"    <- {a}")
        descs = self.descendants(session_id)
        if descs:
            lines.append("  Descendants:")
            for d in descs:
                lines.append(f"    -> {d}")
        return "\n".join(lines)

    def summary(self, session_id: str) -> str:
        recs = [r for r in self._records if r["session_id"] == session_id]
        return f"Session {session_id}: {len(recs)} lineage record(s)"
