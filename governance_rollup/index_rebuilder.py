"""
governance_rollup/index_rebuilder.py — GovernanceIndexRebuilder v1.1.9

Rebuilds indexes from append-only history (preview by default).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NEVER modifies append-only history.
[!] Default: dry_run (preview only unless allow_write=True).
[!] Duplicate records: DO NOT silently discard — record warning.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent


class GovernanceIndexRebuilder:
    """
    Rebuilds indexes from append-only history.
    NEVER modifies append-only history.
    Default: dry_run (preview only unless allow_write=True).
    Duplicate records: DO NOT silently discard, record warning.
    """

    SUPPORTED_INDEXES = [
        "research_registry",
        "governance_alerts",
        "governance_ops",
        "gate_enforcement",
        "artifact_index",
        "duplicate_index",
        "action_queue",
        "freshness_summary",
    ]

    # Module -> (history_file_pattern, index_file_pattern)
    _MODULE_PATHS = {
        "research_registry": (
            "data/research_registry/run_history.jsonl",
            "data/research_registry/run_index.json",
        ),
        "governance_alerts": (
            "data/governance_alerts/alerts.jsonl",
            "data/governance_alerts/alert_index.json",
        ),
        "governance_ops": (
            "data/governance_ops/actions.jsonl",
            "data/governance_ops/action_index.json",
        ),
        "gate_enforcement": (
            "data/gate_enforcement/runs.jsonl",
            "data/gate_enforcement/run_index.json",
        ),
        "artifact_index": (
            "data/research_registry/artifacts.jsonl",
            "data/research_registry/artifact_index.json",
        ),
        "duplicate_index": (
            "data/research_registry/run_history.jsonl",
            "data/research_registry/duplicate_index.json",
        ),
        "action_queue": (
            "data/governance_ops/actions.jsonl",
            "data/governance_ops/action_queue_index.json",
        ),
        "freshness_summary": (
            "data/freshness/freshness_history.jsonl",
            "data/freshness/freshness_index.json",
        ),
    }

    def supported_indexes(self) -> List[str]:
        """Return list of supported index module names."""
        return list(self.SUPPORTED_INDEXES)

    def inspect_index(self, module_name: str) -> Dict[str, Any]:
        """Inspect the current state of an index."""
        if module_name not in self._MODULE_PATHS:
            return {
                "module_name": module_name,
                "supported": False,
                "status": "UNSUPPORTED",
            }
        history_path_rel, index_path_rel = self._MODULE_PATHS[module_name]
        history_path = _BASE_DIR / history_path_rel
        index_path = _BASE_DIR / index_path_rel

        history_exists = history_path.exists()
        index_exists = index_path.exists()
        index_entries = 0
        history_records = 0

        if history_exists:
            try:
                with open(history_path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        if line.strip():
                            history_records += 1
            except Exception:
                pass

        if index_exists:
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    entries = data.get("entries", data)
                    if isinstance(entries, dict):
                        index_entries = len(entries)
                    elif isinstance(entries, list):
                        index_entries = len(entries)
            except Exception:
                pass

        stale = history_records != index_entries and index_exists
        return {
            "module_name": module_name,
            "supported": True,
            "history_path": str(history_path),
            "index_path": str(index_path),
            "history_exists": history_exists,
            "index_exists": index_exists,
            "history_records": history_records,
            "index_entries": index_entries,
            "stale": stale,
            "status": "STALE" if stale else ("VALID" if index_exists else "MISSING"),
        }

    def preview_rebuild(self, module_name: str) -> Dict[str, Any]:
        """Preview what a rebuild would do (dry-run, no writes)."""
        inspection = self.inspect_index(module_name)
        if not inspection.get("supported"):
            return {
                "module_name": module_name,
                "dry_run": True,
                "status": "UNSUPPORTED",
                "preview": f"Module '{module_name}' is not in SUPPORTED_INDEXES",
            }

        history_path_rel, _ = self._MODULE_PATHS[module_name]
        history_path = _BASE_DIR / history_path_rel

        records = []
        seen_ids: Dict[str, int] = {}
        duplicates = []
        if history_path.exists():
            try:
                with open(history_path, "r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        stripped = line.strip()
                        if not stripped:
                            continue
                        try:
                            record = json.loads(stripped)
                            # Detect duplicates using first id-like field
                            record_id = (
                                record.get("run_id") or record.get("alert_id") or
                                record.get("action_id") or record.get("artifact_id") or
                                record.get("id") or f"line_{i}"
                            )
                            if record_id in seen_ids:
                                duplicates.append({
                                    "id": record_id,
                                    "first_seen_line": seen_ids[record_id],
                                    "duplicate_line": i,
                                })
                            else:
                                seen_ids[record_id] = i
                            records.append(record)
                        except Exception:
                            pass
            except Exception as exc:
                return {
                    "module_name": module_name,
                    "dry_run": True,
                    "status": "ERROR",
                    "error": str(exc),
                }

        return {
            "module_name": module_name,
            "dry_run": True,
            "records_in_history": len(records),
            "would_create_entries": len(seen_ids),
            "duplicates_found": len(duplicates),
            "duplicates": duplicates,  # DO NOT silently discard
            "current_index_entries": inspection.get("index_entries", 0),
            "action": "REBUILD_INDEX" if len(records) > 0 else "NO_ACTION",
            "note": "[DRY RUN] No changes made. Pass allow_write=True to execute.",
            "research_only": True,
            "no_real_orders": True,
        }

    def rebuild(self, module_name: str, allow_write: bool = False) -> Dict[str, Any]:
        """
        Rebuild an index from history.
        BLOCKED if allow_write=False.
        NEVER modifies history files.
        Duplicates are recorded in warnings, NOT silently discarded.
        """
        if module_name not in self._MODULE_PATHS:
            return {
                "module_name": module_name,
                "status": "UNSUPPORTED",
                "allow_write": allow_write,
            }

        if not allow_write:
            preview = self.preview_rebuild(module_name)
            preview["status"] = "DRY_RUN_ONLY"
            preview["note"] = "[DRY RUN] Pass allow_write=True to execute rebuild."
            return preview

        if module_name not in self._MODULE_PATHS:
            return {
                "module_name": module_name,
                "status": "UNSUPPORTED",
                "allow_write": allow_write,
            }

        history_path_rel, index_path_rel = self._MODULE_PATHS[module_name]
        history_path = _BASE_DIR / history_path_rel
        index_path = _BASE_DIR / index_path_rel

        if not history_path.exists():
            return {
                "module_name": module_name,
                "status": "HISTORY_NOT_FOUND",
                "history_path": str(history_path),
            }

        records: Dict[str, Any] = {}
        seen_ids: Dict[str, int] = {}
        duplicates = []

        try:
            with open(history_path, "r", encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        record = json.loads(stripped)
                        record_id = (
                            record.get("run_id") or record.get("alert_id") or
                            record.get("action_id") or record.get("artifact_id") or
                            record.get("id") or f"line_{i}"
                        )
                        if record_id in seen_ids:
                            # DO NOT silently discard — record warning
                            duplicates.append({
                                "id": record_id,
                                "first_seen_line": seen_ids[record_id],
                                "duplicate_line": i,
                                "warning": "Duplicate record kept for audit; latest overwrites in index",
                            })
                        seen_ids[record_id] = i
                        records[record_id] = record
                    except Exception:
                        pass
        except Exception as exc:
            return {
                "module_name": module_name,
                "status": "ERROR",
                "error": str(exc),
            }

        from datetime import datetime, timezone as _tz
        index_data = {
            "index_version": "1.0",
            "module": module_name,
            "last_updated": datetime.now(_tz.utc).isoformat(),
            "entry_count": len(records),
            "entries": {k: {"summary": str(v)[:200]} for k, v in records.items()},
            "duplicate_warnings": duplicates,
            "research_only": True,
            "no_real_orders": True,
        }

        try:
            index_path.parent.mkdir(parents=True, exist_ok=True)
            with open(index_path, "w", encoding="utf-8") as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            logger.info("rebuild: wrote index for %s to %s", module_name, index_path)
        except Exception as exc:
            return {
                "module_name": module_name,
                "status": "WRITE_ERROR",
                "error": str(exc),
            }

        return {
            "module_name": module_name,
            "status": "COMPLETED",
            "entries_written": len(records),
            "duplicates_found": len(duplicates),
            "duplicates": duplicates,
            "index_path": str(index_path),
            "allow_write": allow_write,
            "note": "Duplicate records were preserved with warnings, not silently discarded.",
        }

    def rebuild_all(self, allow_write: bool = False) -> Dict[str, Any]:
        """Rebuild all supported indexes."""
        results = {}
        for module_name in self.SUPPORTED_INDEXES:
            results[module_name] = self.rebuild(module_name, allow_write=allow_write)
        statuses = [r.get("status", "UNKNOWN") for r in results.values()]
        overall = "PASS" if all(s in ("COMPLETED", "DRY_RUN_ONLY") for s in statuses) else "WARN"
        return {
            "overall_status": overall,
            "allow_write": allow_write,
            "results": results,
            "research_only": True,
            "no_real_orders": True,
        }

    def compare_before_after(
        self, module_name: str, before: Dict[str, Any], after: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare before/after states of an index rebuild."""
        before_count = before.get("index_entries", 0)
        after_count = after.get("entries_written", 0)
        return {
            "module_name": module_name,
            "before_entries": before_count,
            "after_entries": after_count,
            "delta": after_count - before_count,
            "changed": before_count != after_count,
        }

    def verify_index(self, module_name: str) -> Dict[str, Any]:
        """Verify the current index is consistent with history."""
        return self.inspect_index(module_name)
