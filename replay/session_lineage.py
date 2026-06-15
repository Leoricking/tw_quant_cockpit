"""
replay/session_lineage.py — ReplaySessionLineage and ReplaySessionLineageManager v1.2.1

Tracks parent/child relationships between replay sessions.
No cycles allowed. Missing parent: WARN, don't crash.
root_session_id must be stable.
Imported session without parent: marked ORPHAN_IMPORTED.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

RELATION_TYPES = ["ROOT", "DUPLICATE", "FORK", "FORK_FROM_CHECKPOINT", "RESTORED", "IMPORTED", "ORPHAN_IMPORTED"]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ReplaySessionLineage:
    session_id: str
    root_session_id: str
    parent_session_id: Optional[str]
    source_scenario_id: Optional[str]
    source_checkpoint_id: Optional[str]
    relation_type: str
    children_session_ids: List[str] = field(default_factory=list)
    lineage_depth: int = 0
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "root_session_id": self.root_session_id,
            "parent_session_id": self.parent_session_id,
            "source_scenario_id": self.source_scenario_id,
            "source_checkpoint_id": self.source_checkpoint_id,
            "relation_type": self.relation_type,
            "children_session_ids": self.children_session_ids,
            "lineage_depth": self.lineage_depth,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplaySessionLineage":
        return cls(
            session_id=d.get("session_id", ""),
            root_session_id=d.get("root_session_id", ""),
            parent_session_id=d.get("parent_session_id"),
            source_scenario_id=d.get("source_scenario_id"),
            source_checkpoint_id=d.get("source_checkpoint_id"),
            relation_type=d.get("relation_type", "ROOT"),
            children_session_ids=d.get("children_session_ids", []),
            lineage_depth=int(d.get("lineage_depth", 0)),
            created_at=d.get("created_at", ""),
        )


class ReplaySessionLineageManager:
    """
    Tracks parent/child relationships between replay sessions.
    No cycles allowed. Missing parent: WARN, don't crash.
    Imported session without parent: marked ORPHAN_IMPORTED.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root=None):
        self._repo_root = repo_root or "."
        self._store = store
        self._lineage_cache: Dict[str, ReplaySessionLineage] = {}
        self._load_from_store()

    def _get_lineage_file(self) -> Path:
        return Path(self._repo_root) / "data" / "replay_sessions" / "session_lineage.jsonl"

    def _load_from_store(self):
        lf = self._get_lineage_file()
        if not lf.exists():
            return
        try:
            with open(str(lf), "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        lin = ReplaySessionLineage.from_dict(d)
                        self._lineage_cache[lin.session_id] = lin
                    except Exception:
                        pass
        except Exception as exc:
            logger.warning("[LineageManager] Load failed: %s", exc)

    def _save_lineage(self, lineage: ReplaySessionLineage):
        lf = self._get_lineage_file()
        lf.parent.mkdir(parents=True, exist_ok=True)
        self._lineage_cache[lineage.session_id] = lineage
        try:
            with open(str(lf), "a", encoding="utf-8") as f:
                f.write(json.dumps(lineage.to_dict(), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[LineageManager] Save failed: %s", exc)

    def create_root(self, session_id: str, scenario_id: Optional[str] = None) -> ReplaySessionLineage:
        lin = ReplaySessionLineage(
            session_id=session_id,
            root_session_id=session_id,
            parent_session_id=None,
            source_scenario_id=scenario_id,
            source_checkpoint_id=None,
            relation_type="ROOT",
            children_session_ids=[],
            lineage_depth=0,
            created_at=_now_utc(),
        )
        self._save_lineage(lin)
        return lin

    def link_child(self, parent_id: str, child_id: str, relation_type: str) -> Optional[ReplaySessionLineage]:
        if self.detect_cycle(child_id):
            logger.warning("[LineageManager] Cycle detected, not linking %s -> %s", parent_id, child_id)
            return None
        parent = self._lineage_cache.get(parent_id)
        if parent is None:
            logger.warning("[LineageManager] Parent not found: %s — creating orphan", parent_id)
            root_id = parent_id
            depth = 1
        else:
            root_id = parent.root_session_id
            depth = parent.lineage_depth + 1
            # Update parent children list
            if child_id not in parent.children_session_ids:
                parent.children_session_ids.append(child_id)
                self._save_lineage(parent)

        child = ReplaySessionLineage(
            session_id=child_id,
            root_session_id=root_id,
            parent_session_id=parent_id,
            source_scenario_id=parent.source_scenario_id if parent else None,
            source_checkpoint_id=None,
            relation_type=relation_type,
            children_session_ids=[],
            lineage_depth=depth,
            created_at=_now_utc(),
        )
        self._save_lineage(child)
        return child

    def mark_duplicate(self, original_id: str, new_id: str) -> Optional[ReplaySessionLineage]:
        return self.link_child(original_id, new_id, "DUPLICATE")

    def mark_fork(self, parent_id: str, new_id: str, checkpoint_id: Optional[str] = None) -> Optional[ReplaySessionLineage]:
        lin = self.link_child(parent_id, new_id, "FORK_FROM_CHECKPOINT" if checkpoint_id else "FORK")
        if lin and checkpoint_id:
            lin.source_checkpoint_id = checkpoint_id
            self._save_lineage(lin)
        return lin

    def get_lineage(self, session_id: str) -> Optional[ReplaySessionLineage]:
        return self._lineage_cache.get(session_id)

    def get_root(self, session_id: str) -> Optional[str]:
        lin = self._lineage_cache.get(session_id)
        return lin.root_session_id if lin else session_id

    def get_children(self, session_id: str) -> List[str]:
        lin = self._lineage_cache.get(session_id)
        return lin.children_session_ids if lin else []

    def lineage_tree(self, session_id: str) -> Dict[str, Any]:
        lin = self._lineage_cache.get(session_id)
        if lin is None:
            return {"session_id": session_id, "not_found": True}
        children_trees = [self.lineage_tree(cid) for cid in lin.children_session_ids]
        return {
            "session_id": session_id,
            "root_session_id": lin.root_session_id,
            "parent_session_id": lin.parent_session_id,
            "relation_type": lin.relation_type,
            "depth": lin.lineage_depth,
            "children": children_trees,
        }

    def detect_cycle(self, session_id: str) -> bool:
        visited = set()
        current = session_id
        while current:
            if current in visited:
                return True
            visited.add(current)
            lin = self._lineage_cache.get(current)
            if lin is None:
                break
            current = lin.parent_session_id
        return False

    def validate_lineage(self, session_id: str) -> Dict[str, Any]:
        lin = self._lineage_cache.get(session_id)
        if lin is None:
            return {"valid": False, "error": f"Lineage not found for {session_id}"}
        has_cycle = self.detect_cycle(session_id)
        return {
            "valid": not has_cycle,
            "session_id": session_id,
            "cycle_detected": has_cycle,
            "depth": lin.lineage_depth,
            "root": lin.root_session_id,
        }
