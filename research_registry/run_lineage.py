"""
research_registry.run_lineage — ResearchRunLineageManager v1.1.8

Manages run parent/child/rerun/duplicate relationships.
No cycles allowed. Parent missing → WARN. rerun does NOT overwrite original.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ResearchRunLineageManager:
    """
    Manages run lineage: root, child, rerun, duplicate, derived, report_of, etc.

    [!] No cycles. rerun does NOT overwrite original. duplicate does NOT delete.
    """

    no_real_orders = True
    research_only = True

    def __init__(self):
        self._lineage: Dict[str, dict] = {}

    def create_root(self, run_id: str) -> Any:
        """Create a root lineage record for a run."""
        from research_registry.registry_schema import RunLineage
        lin = RunLineage(
            run_id=run_id,
            root_run_id=run_id,
            relation_type="ROOT",
            created_at=_now_utc(),
        )
        self._lineage[run_id] = lin.to_dict()
        return lin

    def link_child(self, parent_run_id: str, child_run_id: str, relation_type: str = "CHILD") -> Any:
        """Link a child run to a parent run."""
        from research_registry.registry_schema import RunLineage

        if parent_run_id not in self._lineage:
            logger.warning(
                "ResearchRunLineageManager.link_child: parent '%s' not found — WARN (non-fatal)",
                parent_run_id,
            )

        # Cycle detection
        if self._would_create_cycle(parent_run_id, child_run_id):
            logger.warning(
                "ResearchRunLineageManager.link_child: would create cycle %s→%s — skipped",
                parent_run_id, child_run_id,
            )
            return self.get_lineage(child_run_id)

        parent_lin = self._lineage.get(parent_run_id, {})
        root_id = parent_lin.get("root_run_id", parent_run_id)
        parent_depth = int(parent_lin.get("lineage_depth", 0))

        lin = RunLineage(
            run_id=child_run_id,
            parent_run_id=parent_run_id,
            root_run_id=root_id,
            lineage_depth=parent_depth + 1,
            relation_type=relation_type,
            created_at=_now_utc(),
        )
        self._lineage[child_run_id] = lin.to_dict()

        # Update parent's children list
        if parent_run_id in self._lineage:
            children = self._lineage[parent_run_id].get("children_run_ids", [])
            if not isinstance(children, list):
                children = []
            if child_run_id not in children:
                children.append(child_run_id)
            self._lineage[parent_run_id]["children_run_ids"] = children

        return lin

    def mark_rerun(self, run_id: str, original_run_id: str) -> Any:
        """Mark a run as a rerun of an original run (does NOT overwrite original)."""
        from research_registry.registry_schema import RunLineage
        existing = self._lineage.get(run_id, {})
        lin = RunLineage(
            run_id=run_id,
            parent_run_id=existing.get("parent_run_id", ""),
            root_run_id=existing.get("root_run_id", run_id),
            children_run_ids=existing.get("children_run_ids", []),
            rerun_of=original_run_id,
            duplicate_of=existing.get("duplicate_of", ""),
            lineage_depth=existing.get("lineage_depth", 0),
            relation_type="RERUN",
            created_at=existing.get("created_at", _now_utc()),
        )
        self._lineage[run_id] = lin.to_dict()
        return lin

    def mark_duplicate(self, run_id: str, duplicate_of: str) -> Any:
        """Mark a run as a duplicate (does NOT delete original)."""
        from research_registry.registry_schema import RunLineage
        existing = self._lineage.get(run_id, {})
        lin = RunLineage(
            run_id=run_id,
            parent_run_id=existing.get("parent_run_id", ""),
            root_run_id=existing.get("root_run_id", run_id),
            children_run_ids=existing.get("children_run_ids", []),
            rerun_of=existing.get("rerun_of", ""),
            duplicate_of=duplicate_of,
            lineage_depth=existing.get("lineage_depth", 0),
            relation_type="DUPLICATE",
            created_at=existing.get("created_at", _now_utc()),
        )
        self._lineage[run_id] = lin.to_dict()
        return lin

    def get_lineage(self, run_id: str) -> Optional[Any]:
        """Return RunLineage for a run_id."""
        from research_registry.registry_schema import RunLineage
        lin_dict = self._lineage.get(run_id)
        if lin_dict is None:
            return None
        return RunLineage.from_dict(lin_dict)

    def get_children(self, run_id: str) -> List[str]:
        """Return list of child run IDs for a run."""
        lin_dict = self._lineage.get(run_id, {})
        children = lin_dict.get("children_run_ids", [])
        if not isinstance(children, list):
            return []
        return children

    def get_root(self, run_id: str) -> str:
        """Return the root run_id for a run."""
        lin_dict = self._lineage.get(run_id, {})
        return lin_dict.get("root_run_id", run_id)

    def lineage_tree(self, run_id: str, _depth: int = 0, _visited: Optional[set] = None) -> dict:
        """Return a nested lineage tree for a run."""
        if _visited is None:
            _visited = set()
        if run_id in _visited or _depth > 50:
            return {"run_id": run_id, "cycle": True}
        _visited.add(run_id)

        lin = self.get_lineage(run_id)
        if lin is None:
            return {"run_id": run_id, "not_found": True}

        children = [
            self.lineage_tree(child_id, _depth + 1, _visited)
            for child_id in lin.children_run_ids
        ]
        return {
            "run_id": run_id,
            "relation_type": lin.relation_type,
            "parent_run_id": lin.parent_run_id,
            "root_run_id": lin.root_run_id,
            "rerun_of": lin.rerun_of,
            "duplicate_of": lin.duplicate_of,
            "lineage_depth": lin.lineage_depth,
            "children": children,
        }

    def validate_lineage(self) -> dict:
        """Validate all lineage records for integrity issues."""
        issues = []
        cycles = self.detect_cycle()
        if cycles:
            issues.append({"type": "CYCLE", "run_ids": cycles})

        for run_id, lin_dict in self._lineage.items():
            parent_id = lin_dict.get("parent_run_id", "")
            if parent_id and parent_id not in self._lineage:
                issues.append({"type": "MISSING_PARENT", "run_id": run_id, "parent_id": parent_id})

        return {
            "valid": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues,
        }

    def detect_cycle(self) -> List[str]:
        """Detect cycles in the lineage graph. Returns list of run_ids involved."""
        visited = set()
        in_stack = set()
        cycle_nodes = []

        def dfs(node: str) -> bool:
            if node in in_stack:
                cycle_nodes.append(node)
                return True
            if node in visited:
                return False
            visited.add(node)
            in_stack.add(node)

            lin_dict = self._lineage.get(node, {})
            parent = lin_dict.get("parent_run_id", "")
            if parent and parent in self._lineage:
                if dfs(parent):
                    return True

            in_stack.discard(node)
            return False

        for run_id in list(self._lineage.keys()):
            if run_id not in visited:
                dfs(run_id)

        return cycle_nodes

    def _would_create_cycle(self, parent_id: str, child_id: str) -> bool:
        """Return True if linking child to parent would create a cycle."""
        if parent_id == child_id:
            return True
        # Walk up the parent chain
        visited = set()
        current = parent_id
        while current:
            if current in visited:
                break
            if current == child_id:
                return True
            visited.add(current)
            lin_dict = self._lineage.get(current, {})
            current = lin_dict.get("parent_run_id", "")
        return False

    def load_from_records(self, lineage_records: List[dict]) -> None:
        """Load lineage records from a list of dicts (e.g., from JSONL store)."""
        for rec in lineage_records:
            run_id = rec.get("run_id", "")
            if run_id:
                self._lineage[run_id] = rec

    def all_lineage(self) -> List[dict]:
        """Return all lineage records as a list of dicts."""
        return list(self._lineage.values())
