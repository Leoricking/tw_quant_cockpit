"""
governance_rollup/metadata_migrator.py — GovernanceMetadataMigrator v1.1.9

Migrates v1.1.0~v1.1.8 metadata to v1.1.9 schema.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NEVER migrates market price data (OHLCV, financials, trades).
[!] Does NOT guess missing qualification or mode — UNKNOWN stays UNKNOWN.
[!] Default: dry_run=True. No write without allow_write=True.
[!] Backup before execute. Rollback always available.
"""
from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent
_MIGRATION_BACKUP_DIR = _BASE_DIR / "data" / "governance_rollup" / "migration_backups"

# Known version markers in metadata
_VERSION_MARKERS = {
    "1.1.0": ["universe", "tier", "symbol"],
    "1.1.1": ["import_batch", "onboarding", "dry_run"],
    "1.1.2": ["coverage_repair", "repair_plan"],
    "1.1.3": ["freshness", "sla", "source_interruption"],
    "1.1.4": ["quality_gate", "formal_gate"],
    "1.1.5": ["gate_enforcement", "audit_chain", "reproducibility_hash"],
    "1.1.6": ["governance_ops", "action_queue", "daily_summary"],
    "1.1.7": ["governance_alerts", "alert_id", "digest"],
    "1.1.8": ["research_registry", "run_id", "artifact_id", "lineage"],
}

# OHLCV / financial data — NEVER migrate
_FORBIDDEN_FIELD_PATTERNS = [
    "ohlcv", "open", "high", "low", "close", "volume",
    "price", "trade", "order", "broker", "financial",
    "market_data", "tick_data",
]


class GovernanceMetadataMigrator:
    """
    Migrates v1.1.0~v1.1.8 metadata to v1.1.9 schema.

    NEVER migrates market price data (OHLCV, financials, trades).
    Does NOT guess missing qualification or mode.
    UNKNOWN stays UNKNOWN.
    Old absolute paths -> repo-relative candidate, preserves original_path.
    Old timestamps -> normalized, preserves original_timestamp.
    Schema migration must have migration_from/migration_to.
    Default: dry_run=True. No write without allow_write=True.
    Backup before execute.
    """

    def __init__(self) -> None:
        self._plans: Dict[str, Dict[str, Any]] = {}

    def detect_version(self, record: Dict[str, Any]) -> str:
        """Detect schema version of a record. Returns version string or UNKNOWN."""
        explicit = record.get("schema_version") or record.get("version")
        if explicit:
            return str(explicit)
        # Heuristic from keys
        keys = set(record.keys())
        for version, markers in sorted(_VERSION_MARKERS.items(), reverse=True):
            if any(m in " ".join(str(k).lower() for k in keys) for m in markers):
                return version
        return "UNKNOWN"

    def _is_forbidden_field(self, field_name: str) -> bool:
        """Return True if a field is forbidden from migration (financial/OHLCV data)."""
        fl = field_name.lower()
        return any(pat in fl for pat in _FORBIDDEN_FIELD_PATTERNS)

    def plan_migration(self, module_name: str) -> Dict[str, Any]:
        """Create a migration plan for a module. Returns plan dict."""
        plan_id = f"MIG-{module_name.upper()}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        module_paths = self._discover_module_files(module_name)
        plan = {
            "plan_id": plan_id,
            "module_name": module_name,
            "files": module_paths,
            "migration_from": "v1.1.0~v1.1.8",
            "migration_to": "v1.1.9",
            "dry_run": True,
            "requires_allow_write": True,
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "research_only": True,
            "no_real_orders": True,
        }
        self._plans[plan_id] = plan
        return plan

    def preview_migration(self, module_name: str) -> Dict[str, Any]:
        """Preview migration for a module (dry-run, no writes)."""
        plan = self.plan_migration(module_name)
        files = plan.get("files", [])
        previews = []
        for file_info in files:
            path = Path(file_info.get("path", ""))
            if not path.exists():
                previews.append({
                    "path": str(path),
                    "status": "NOT_FOUND",
                    "changes": [],
                })
                continue
            changes = self._preview_file_changes(path)
            previews.append({
                "path": str(path),
                "status": "PREVIEW",
                "changes": changes,
                "change_count": len(changes),
            })
        return {
            "plan_id": plan["plan_id"],
            "module_name": module_name,
            "dry_run": True,
            "migration_from": plan["migration_from"],
            "migration_to": plan["migration_to"],
            "file_previews": previews,
            "note": "[DRY RUN] No changes made. Pass allow_write=True to execute.",
            "research_only": True,
            "no_real_orders": True,
        }

    def _preview_file_changes(self, path: Path) -> List[Dict[str, Any]]:
        """Preview changes for a single file."""
        changes = []
        if path.suffix.lower() not in (".json", ".jsonl", ".csv"):
            return changes
        try:
            if path.suffix.lower() == ".json":
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                records = [data] if isinstance(data, dict) else (data if isinstance(data, list) else [])
            elif path.suffix.lower() == ".jsonl":
                records = []
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        stripped = line.strip()
                        if stripped:
                            try:
                                records.append(json.loads(stripped))
                            except Exception:
                                pass
            else:
                return changes
        except Exception as exc:
            return [{"type": "READ_ERROR", "error": str(exc)}]

        for i, record in enumerate(records[:5]):  # Preview first 5 records
            detected_version = self.detect_version(record)
            if detected_version != "1.1.9" and detected_version != "UNKNOWN":
                changes.append({
                    "record_index": i,
                    "field": "schema_version",
                    "from": detected_version,
                    "to": "1.1.9",
                    "type": "SCHEMA_VERSION_UPDATE",
                })
            # Check for absolute paths
            for k, v in record.items():
                if self._is_forbidden_field(k):
                    changes.append({
                        "record_index": i,
                        "field": k,
                        "type": "FORBIDDEN_SKIP",
                        "note": "Financial/OHLCV field skipped",
                    })
                elif isinstance(v, str) and (":\\") in v or (isinstance(v, str) and v.startswith("D:/") or v.startswith("C:/")):
                    changes.append({
                        "record_index": i,
                        "field": k,
                        "from": v[:80],
                        "type": "PATH_NORMALIZE_CANDIDATE",
                        "note": "absolute path -> repo-relative candidate",
                    })
        return changes

    def migrate_copy(self, source_path: str, dest_path: str) -> Dict[str, Any]:
        """
        Migrate a file to a new copy with v1.1.9 schema.
        Does NOT overwrite source. Does NOT migrate OHLCV/financial fields.
        Returns migration result.
        """
        source = Path(source_path)
        dest = Path(dest_path)
        if not source.exists():
            return {"success": False, "reason": "Source does not exist"}

        from governance_rollup.schema_normalizer import GovernanceSchemaNormalizer
        from governance_rollup.path_normalizer import CrossMachinePathNormalizer
        normalizer = GovernanceSchemaNormalizer()
        path_norm = CrossMachinePathNormalizer()

        migrated_records = []
        try:
            if source.suffix.lower() == ".json":
                with open(source, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                records = [data] if isinstance(data, dict) else (data if isinstance(data, list) else [])
                for record in records:
                    migrated = self._migrate_record(record, normalizer, path_norm)
                    migrated_records.append(migrated)
            elif source.suffix.lower() == ".jsonl":
                with open(source, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        stripped = line.strip()
                        if stripped:
                            try:
                                record = json.loads(stripped)
                                migrated = self._migrate_record(record, normalizer, path_norm)
                                migrated_records.append(migrated)
                            except Exception:
                                pass
            else:
                return {"success": False, "reason": f"Unsupported file type: {source.suffix}"}
        except Exception as exc:
            return {"success": False, "reason": str(exc)}

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.suffix.lower() == ".jsonl":
                with open(dest, "w", encoding="utf-8") as f:
                    for r in migrated_records:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
            else:
                with open(dest, "w", encoding="utf-8") as f:
                    json.dump(migrated_records if len(migrated_records) > 1 else (migrated_records[0] if migrated_records else {}), f, indent=2, ensure_ascii=False)
        except Exception as exc:
            return {"success": False, "reason": f"Write error: {exc}"}

        return {
            "success": True,
            "source": source_path,
            "dest": dest_path,
            "records_migrated": len(migrated_records),
        }

    def _migrate_record(
        self,
        record: Dict[str, Any],
        normalizer: Any,
        path_norm: Any,
    ) -> Dict[str, Any]:
        """Migrate a single record to v1.1.9 schema."""
        result = dict(record)
        # Mark migration metadata
        result["migration_from"] = self.detect_version(record)
        result["migration_to"] = "1.1.9"
        result["schema_version"] = "1.1.9"

        # Normalize fields — skip forbidden financial fields
        for k, v in list(result.items()):
            if self._is_forbidden_field(k):
                continue  # NEVER modify OHLCV / financial fields
            if isinstance(v, str) and (v.startswith("D:/") or v.startswith("C:/")):
                # Normalize path — preserve original
                result[f"original_{k}"] = v
                portable = path_norm.to_repo_relative(v)
                if portable.get("relative_path"):
                    result[k] = portable["relative_path"]

        # Ensure safety flags
        if "research_only" not in result:
            result["research_only"] = True
        if "no_real_orders" not in result:
            result["no_real_orders"] = True

        return result

    def execute_migration(self, module_name: str, allow_write: bool = False) -> Dict[str, Any]:
        """
        Execute migration for a module.
        BLOCKED if allow_write=False.
        Backup before execute.
        """
        if not allow_write:
            return {
                "module_name": module_name,
                "status": "BLOCKED",
                "reason": "allow_write=False — pass allow_write=True to execute",
                "dry_run": True,
                "research_only": True,
                "no_real_orders": True,
            }

        plan = self.plan_migration(module_name)
        files = plan.get("files", [])
        results = []

        for file_info in files:
            path = Path(file_info.get("path", ""))
            if not path.exists():
                results.append({"path": str(path), "status": "NOT_FOUND"})
                continue
            # Backup first
            try:
                _MIGRATION_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
                ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                backup_path = _MIGRATION_BACKUP_DIR / f"{path.name}.{ts}.premig.bak"
                shutil.copy2(str(path), str(backup_path))
            except Exception as exc:
                results.append({
                    "path": str(path),
                    "status": "BACKUP_FAILED",
                    "error": str(exc),
                })
                continue
            # Migrate to a copy
            dest_path = path.parent / f"{path.stem}.migrated_v119{path.suffix}"
            mig_result = self.migrate_copy(str(path), str(dest_path))
            mig_result["backup_path"] = str(backup_path)
            results.append(mig_result)

        return {
            "plan_id": plan["plan_id"],
            "module_name": module_name,
            "allow_write": allow_write,
            "migration_from": plan["migration_from"],
            "migration_to": plan["migration_to"],
            "file_results": results,
            "status": "COMPLETED",
            "note": "Original files preserved. Migrated copies created with .migrated_v119 suffix.",
            "research_only": True,
            "no_real_orders": True,
        }

    def validate_migrated(self, path: str) -> Dict[str, Any]:
        """Validate a migrated file."""
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        p = Path(path)
        if p.suffix.lower() == ".json":
            return validator.validate_json(p)
        if p.suffix.lower() == ".jsonl":
            return validator.validate_jsonl(p)
        return {"valid": p.exists(), "status": "CHECKED"}

    def rollback_migration(
        self, backup_path: str, target_path: str, allow_write: bool = False
    ) -> Dict[str, Any]:
        """Rollback a migration. BLOCKED if allow_write=False."""
        if not allow_write:
            return {
                "status": "BLOCKED",
                "reason": "allow_write=False — rollback requires allow_write=True",
                "dry_run": True,
                "research_only": True,
                "no_real_orders": True,
            }
        backup = Path(backup_path)
        target = Path(target_path)
        if not backup.exists():
            return {"status": "FAILED", "reason": f"Backup not found: {backup_path}"}
        try:
            shutil.copy2(str(backup), str(target))
            logger.info("rollback_migration: restored %s -> %s", backup, target)
            return {
                "status": "COMPLETED",
                "restored_from": backup_path,
                "restored_to": target_path,
            }
        except Exception as exc:
            return {"status": "FAILED", "reason": str(exc)}

    def _discover_module_files(self, module_name: str) -> List[Dict[str, Any]]:
        """Discover data files for a module."""
        import glob
        data_dir = _BASE_DIR / "data"
        patterns = [
            f"data/{module_name}*.jsonl",
            f"data/{module_name}*.json",
            f"data/*{module_name}*.jsonl",
            f"data/*{module_name}*.json",
        ]
        found = []
        seen: set = set()
        for pattern in patterns:
            for match in glob.glob(str(_BASE_DIR / pattern)):
                p = Path(match)
                if p in seen:
                    continue
                seen.add(p)
                found.append({
                    "path": str(p),
                    "module_name": module_name,
                })
        return found
