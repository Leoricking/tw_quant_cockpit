"""
governance_rollup/rollup_store.py — GovernanceRollupStore v1.1.9

Reads/writes rollup runtime output files to data/governance_rollup/.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Runtime output files are NOT committed to git.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import (
    StableRollupSummary, StoreInventoryRecord, RecoveryPlan,
    ModuleConsistencyResult,
)

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent


class GovernanceRollupStore:
    """
    Reads/writes rollup runtime output files.
    Output dir: data/governance_rollup/
    These files are NOT committed to git.
    """

    OUTPUT_DIR = "data/governance_rollup"

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self._base_dir = base_dir or _BASE_DIR
        self._output_dir = self._base_dir / self.OUTPUT_DIR

    def _ensure_dir(self) -> None:
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def save_module_consistency(self, results: List[ModuleConsistencyResult]) -> Path:
        """Save module consistency results to CSV."""
        self._ensure_dir()
        path = self._output_dir / "module_consistency.csv"
        if not results:
            return path
        fieldnames = list(results[0].to_dict().keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                d = r.to_dict()
                # Flatten lists for CSV
                for k, v in d.items():
                    if isinstance(v, list):
                        d[k] = "|".join(str(x) for x in v)
                writer.writerow(d)
        logger.info("save_module_consistency: wrote %d records to %s", len(results), path)
        return path

    def save_store_inventory(self, records: List[StoreInventoryRecord]) -> Path:
        """Save store inventory to CSV."""
        self._ensure_dir()
        path = self._output_dir / "store_inventory.csv"
        if not records:
            return path
        fieldnames = list(records[0].to_dict().keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(r.to_dict())
        logger.info("save_store_inventory: wrote %d records to %s", len(records), path)
        return path

    def save_store_validation(self, results: List[Dict[str, Any]]) -> Path:
        """Save store validation results to CSV."""
        self._ensure_dir()
        path = self._output_dir / "store_validation.csv"
        if not results:
            return path
        all_keys: set = set()
        for r in results:
            all_keys.update(r.keys())
        fieldnames = sorted(all_keys)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in results:
                writer.writerow({k: str(r.get(k, "")) for k in fieldnames})
        return path

    def save_recovery_plans(self, plans: List[RecoveryPlan]) -> Path:
        """Save recovery plans to JSONL."""
        self._ensure_dir()
        path = self._output_dir / "recovery_plans.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for p in plans:
                f.write(json.dumps(p.to_dict(), ensure_ascii=False) + "\n")
        logger.info("save_recovery_plans: wrote %d plans", len(plans))
        return path

    def save_migration_plans(self, plans: List[Dict[str, Any]]) -> Path:
        """Save migration plans to JSONL."""
        self._ensure_dir()
        path = self._output_dir / "migration_plans.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for p in plans:
                f.write(json.dumps(p, ensure_ascii=False, default=str) + "\n")
        return path

    def save_index_status(self, statuses: List[Dict[str, Any]]) -> Path:
        """Save index status to CSV."""
        self._ensure_dir()
        path = self._output_dir / "index_status.csv"
        if not statuses:
            return path
        all_keys: set = set()
        for s in statuses:
            all_keys.update(s.keys())
        fieldnames = sorted(all_keys)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for s in statuses:
                writer.writerow({k: str(s.get(k, "")) for k in fieldnames})
        return path

    def save_path_issues(self, issues: List[Dict[str, Any]]) -> Path:
        """Save path issues to CSV."""
        self._ensure_dir()
        path = self._output_dir / "path_issues.csv"
        if not issues:
            return path
        all_keys: set = set()
        for i in issues:
            all_keys.update(i.keys())
        fieldnames = sorted(all_keys)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for i in issues:
                writer.writerow({k: str(i.get(k, "")) for k in fieldnames})
        return path

    def save_health_matrix(self, matrix: Dict[str, Any]) -> Path:
        """Save health matrix to CSV."""
        self._ensure_dir()
        path = self._output_dir / "health_matrix.csv"
        rows = matrix.get("matrix", [])
        if not rows:
            return path
        all_keys: set = set()
        for r in rows:
            all_keys.update(r.keys())
        fieldnames = sorted(all_keys)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                writer.writerow({k: str(r.get(k, "")) for k in fieldnames})
        return path

    def save_rollup_summary(self, summary: StableRollupSummary) -> Path:
        """Save stable rollup summary to JSON."""
        self._ensure_dir()
        path = self._output_dir / "stable_rollup_summary.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("save_rollup_summary: wrote to %s", path)
        return path

    def append_rollup_history(self, summary: StableRollupSummary) -> Path:
        """Append rollup summary to history JSONL."""
        self._ensure_dir()
        path = self._output_dir / "rollup_history.jsonl"
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(summary.to_dict(), ensure_ascii=False) + "\n")
        return path

    def append_rollup_audit(self, entry: Dict[str, Any]) -> Path:
        """Append an audit entry to rollup audit JSONL."""
        self._ensure_dir()
        path = self._output_dir / "rollup_audit.jsonl"
        entry["audit_ts"] = datetime.now(timezone.utc).isoformat()
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
        return path

    def load_latest_summary(self) -> Optional[StableRollupSummary]:
        """Load the latest rollup summary from disk."""
        path = self._output_dir / "stable_rollup_summary.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return StableRollupSummary.from_dict(data)
        except Exception as exc:
            logger.warning("load_latest_summary error: %s", exc)
            return None

    def load_history(self) -> List[StableRollupSummary]:
        """Load rollup history from JSONL."""
        path = self._output_dir / "rollup_history.jsonl"
        if not path.exists():
            return []
        summaries = []
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped:
                        try:
                            data = json.loads(stripped)
                            summaries.append(StableRollupSummary.from_dict(data))
                        except Exception:
                            pass
        except Exception as exc:
            logger.warning("load_history error: %s", exc)
        return summaries
