"""
governance_rollup/rollup_query.py — GovernanceRollupQuery v1.1.9

Query interface for rollup data (read-only).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import StableRollupSummary

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent
_OUTPUT_DIR = _BASE_DIR / "data" / "governance_rollup"


class GovernanceRollupQuery:
    """Query interface for rollup data."""

    def latest_summary(self) -> Optional[Dict[str, Any]]:
        """Return the latest rollup summary as dict."""
        from governance_rollup.rollup_store import GovernanceRollupStore
        store = GovernanceRollupStore()
        s = store.load_latest_summary()
        return s.to_dict() if s else None

    def module_consistency(self) -> List[Dict[str, Any]]:
        """Load module consistency results."""
        return self._load_csv("module_consistency.csv")

    def store_inventory(self) -> List[Dict[str, Any]]:
        """Load store inventory results."""
        return self._load_csv("store_inventory.csv")

    def invalid_stores(self) -> List[Dict[str, Any]]:
        """Return stores with non-VALID status."""
        inventory = self.store_inventory()
        return [r for r in inventory if r.get("status", "VALID") != "VALID"]

    def path_issues(self) -> List[Dict[str, Any]]:
        """Return path issue records."""
        return self._load_csv("path_issues.csv")

    def index_issues(self) -> List[Dict[str, Any]]:
        """Return index status records with issues."""
        statuses = self._load_csv("index_status.csv")
        return [s for s in statuses if s.get("stale") == "True" or s.get("status") in ("MISSING", "STALE")]

    def schema_mismatches(self) -> List[Dict[str, Any]]:
        """Return module consistency records with schema mismatches."""
        consistency = self.module_consistency()
        return [c for c in consistency if c.get("schema_version") != "1.1.9"
                and c.get("schema_version") not in ("", "UNKNOWN")]

    def safety_mismatches(self) -> List[Dict[str, Any]]:
        """Return records with safety flag issues."""
        consistency = self.module_consistency()
        return [c for c in consistency if c.get("safety_status") in ("FAIL", "WARN")]

    def qualification_mismatches(self) -> List[Dict[str, Any]]:
        """Return records with qualification consistency issues."""
        consistency = self.module_consistency()
        return [c for c in consistency if c.get("qualification_status") in ("FAIL", "WARN")]

    def recovery_plans(self) -> List[Dict[str, Any]]:
        """Load recovery plans."""
        return self._load_jsonl("recovery_plans.jsonl")

    def migration_plans(self) -> List[Dict[str, Any]]:
        """Load migration plans."""
        return self._load_jsonl("migration_plans.jsonl")

    def latest_health_matrix(self) -> List[Dict[str, Any]]:
        """Load health matrix."""
        return self._load_csv("health_matrix.csv")

    def rollup_history(self) -> List[Dict[str, Any]]:
        """Load full rollup history."""
        from governance_rollup.rollup_store import GovernanceRollupStore
        store = GovernanceRollupStore()
        history = store.load_history()
        return [s.to_dict() for s in history]

    def compare_rollups(self, run_a: str, run_b: str) -> Dict[str, Any]:
        """Compare two rollup runs by generated_at timestamp prefix."""
        history = self.rollup_history()
        run_a_summary = next(
            (r for r in history if r.get("generated_at", "").startswith(run_a)), None
        )
        run_b_summary = next(
            (r for r in history if r.get("generated_at", "").startswith(run_b)), None
        )
        if not run_a_summary or not run_b_summary:
            return {
                "run_a": run_a,
                "run_b": run_b,
                "status": "NOT_FOUND",
                "found_a": run_a_summary is not None,
                "found_b": run_b_summary is not None,
            }
        # Compare key fields
        diff = {}
        for field in ("overall_status", "stable_ready", "known_warnings", "blocking_issues"):
            val_a = run_a_summary.get(field)
            val_b = run_b_summary.get(field)
            if val_a != val_b:
                diff[field] = {"run_a": val_a, "run_b": val_b}
        return {
            "run_a": run_a,
            "run_b": run_b,
            "status": "COMPARED",
            "overall_a": run_a_summary.get("overall_status"),
            "overall_b": run_b_summary.get("overall_status"),
            "stable_ready_a": run_a_summary.get("stable_ready"),
            "stable_ready_b": run_b_summary.get("stable_ready"),
            "differences": diff,
            "changed": len(diff) > 0,
        }

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _load_csv(self, filename: str) -> List[Dict[str, Any]]:
        import csv
        path = _OUTPUT_DIR / filename
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except Exception as exc:
            logger.warning("_load_csv %s error: %s", filename, exc)
            return []

    def _load_jsonl(self, filename: str) -> List[Dict[str, Any]]:
        path = _OUTPUT_DIR / filename
        if not path.exists():
            return []
        results = []
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped:
                        try:
                            results.append(json.loads(stripped))
                        except Exception:
                            pass
        except Exception as exc:
            logger.warning("_load_jsonl %s error: %s", filename, exc)
        return results
