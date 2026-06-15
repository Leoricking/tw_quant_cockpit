"""
governance_rollup/store_inventory.py — GovernanceStoreInventory v1.1.9

Scans governance stores in data/ directory (read-only).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT scan .env, cookies, broker credentials, or secrets.
[!] Read-only — never writes to stores.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import (
    StoreInventoryRecord,
    STORE_TYPE_JSON, STORE_TYPE_JSONL, STORE_TYPE_CSV,
    STORE_TYPE_SQLITE, STORE_TYPE_DIRECTORY, STORE_TYPE_MARKDOWN, STORE_TYPE_OTHER,
)

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent


class GovernanceStoreInventory:
    """
    Scans governance stores in data/ directory.
    Does NOT scan .env, cookies, broker credentials, or secrets.
    Read-only — never writes to stores.
    """

    DATA_PATTERNS = [
        "data/universe*",
        "data/import*",
        "data/repair*",
        "data/freshness*",
        "data/quality_gate*",
        "data/governance_ops*",
        "data/governance_alerts*",
        "data/research_registry*",
        "data/governance_rollup*",
    ]

    # Explicitly excluded patterns — never scan these
    _EXCLUDED_PATTERNS = [
        ".env", ".env.*", "cookies", "credentials",
        "secrets", "broker_token", "api_key", "password",
    ]

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self._base_dir = base_dir or _BASE_DIR

    def _is_excluded(self, path: Path) -> bool:
        """Return True if path matches excluded patterns (secrets/credentials)."""
        name_lower = path.name.lower()
        for pattern in self._EXCLUDED_PATTERNS:
            if pattern.lower() in name_lower:
                return True
        return False

    def discover_stores(self) -> List[Path]:
        """Discover all governance store files matching DATA_PATTERNS."""
        import glob
        found: List[Path] = []
        seen: set = set()
        for pattern in self.DATA_PATTERNS:
            full_pattern = str(self._base_dir / pattern)
            for match in glob.glob(full_pattern, recursive=False):
                mp = Path(match)
                if mp in seen:
                    continue
                if self._is_excluded(mp):
                    logger.debug("Skipping excluded path: %s", mp)
                    continue
                seen.add(mp)
                found.append(mp)
        return sorted(found)

    def inspect_store(self, path: Path) -> StoreInventoryRecord:
        """Inspect a single store file/directory and return a StoreInventoryRecord."""
        store_id = self._make_store_id(path)
        module_name = self._infer_module(path)
        store_type = self.classify_store(path)
        relative_path = ""
        try:
            relative_path = str(path.relative_to(self._base_dir)).replace("\\", "/")
        except ValueError:
            relative_path = str(path).replace("\\", "/")

        exists = path.exists()
        readable = False
        writable = False
        size_bytes = 0
        last_modified = ""

        if exists:
            try:
                readable = os.access(str(path), os.R_OK)
                writable = os.access(str(path), os.W_OK)
                stat = path.stat()
                if path.is_file():
                    size_bytes = stat.st_size
                last_modified = datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat()
            except Exception as exc:
                logger.debug("inspect_store stat error for %s: %s", path, exc)

        record_count = self.count_records(path) if exists and readable else 0
        checksum = self.calculate_checksum(path) if exists and readable and path.is_file() and size_bytes < 10 * 1024 * 1024 else ""
        append_only = self.detect_append_only(path)
        index_available = self.detect_index(path)
        backup_available = self.detect_backup(path)

        status = "VALID" if exists and readable else ("MISSING" if not exists else "UNREADABLE")
        reason = "" if status == "VALID" else status.lower()

        return StoreInventoryRecord(
            store_id=store_id,
            module_name=module_name,
            store_type=store_type,
            path=str(path).replace("\\", "/"),
            relative_path=relative_path,
            exists=exists,
            readable=readable,
            writable=writable,
            size_bytes=size_bytes,
            record_count=record_count,
            last_modified=last_modified,
            append_only=append_only,
            index_available=index_available,
            backup_available=backup_available,
            corruption_detected=False,
            corrupted_tail_detected=False,
            checksum=checksum,
            status=status,
            reason=reason,
        )

    def classify_store(self, path: Path) -> str:
        """Classify store type by file extension or directory."""
        if path.is_dir():
            return STORE_TYPE_DIRECTORY
        suffix = path.suffix.lower()
        if suffix == ".json":
            return STORE_TYPE_JSON
        if suffix == ".jsonl":
            return STORE_TYPE_JSONL
        if suffix == ".csv":
            return STORE_TYPE_CSV
        if suffix in (".db", ".sqlite", ".sqlite3"):
            return STORE_TYPE_SQLITE
        if suffix == ".md":
            return STORE_TYPE_MARKDOWN
        return STORE_TYPE_OTHER

    def count_records(self, path: Path) -> int:
        """Count records in a store. Returns 0 on error."""
        if not path.is_file():
            return 0
        suffix = path.suffix.lower()
        try:
            if suffix == ".jsonl":
                count = 0
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            count += 1
                return count
            elif suffix == ".csv":
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                # Subtract header row if present
                return max(0, len(rows) - 1) if rows else 0
            elif suffix == ".json":
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return len(data)
                if isinstance(data, dict):
                    # Check for entries sub-dict
                    if "entries" in data and isinstance(data["entries"], dict):
                        return len(data["entries"])
                    return 1
                return 1
        except Exception as exc:
            logger.debug("count_records error for %s: %s", path, exc)
        return 0

    def calculate_checksum(self, path: Path) -> str:
        """Calculate SHA256 checksum of a file. Returns empty string on error."""
        try:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as exc:
            logger.debug("calculate_checksum error for %s: %s", path, exc)
            return ""

    def detect_append_only(self, path: Path) -> bool:
        """Detect if a store is append-only (JSONL convention = append-only)."""
        if path.suffix.lower() == ".jsonl":
            return True
        # Also treat history files as append-only
        name_lower = path.name.lower()
        if "history" in name_lower or "audit" in name_lower or "log" in name_lower:
            return True
        return False

    def detect_index(self, path: Path) -> bool:
        """Detect if an index file exists for this store."""
        parent = path.parent
        stem = path.stem
        # Look for <stem>_index.json or <stem>.index.json
        index_candidates = [
            parent / f"{stem}_index.json",
            parent / f"{stem}.index.json",
            parent / f"{stem}_state.json",
            parent / "index.json",
        ]
        for candidate in index_candidates:
            if candidate.exists() and candidate != path:
                return True
        return False

    def detect_backup(self, path: Path) -> bool:
        """Detect if a backup exists for this store."""
        parent = path.parent
        stem = path.stem
        suffix = path.suffix
        backup_candidates = [
            parent / f"{stem}.backup{suffix}",
            parent / f"{stem}_backup{suffix}",
            parent / "backups" / path.name,
        ]
        for candidate in backup_candidates:
            if candidate.exists():
                return True
        return False

    def build_inventory(self) -> List[StoreInventoryRecord]:
        """Discover and inspect all governance stores. Returns list of records."""
        stores = self.discover_stores()
        records = []
        for store_path in stores:
            try:
                record = self.inspect_store(store_path)
                records.append(record)
            except Exception as exc:
                logger.warning("build_inventory: error inspecting %s: %s", store_path, exc)
        logger.info("build_inventory: found %d stores", len(records))
        return records

    def inventory_summary(self) -> Dict[str, Any]:
        """Build summary stats for the inventory."""
        records = self.build_inventory()
        total = len(records)
        valid = sum(1 for r in records if r.status == "VALID")
        missing = sum(1 for r in records if r.status == "MISSING")
        unreadable = sum(1 for r in records if r.status == "UNREADABLE")
        corrupted = sum(1 for r in records if r.corruption_detected)
        return {
            "total_stores": total,
            "valid": valid,
            "missing": missing,
            "unreadable": unreadable,
            "corrupted": corrupted,
            "research_only": True,
            "no_real_orders": True,
        }

    def _make_store_id(self, path: Path) -> str:
        """Generate a deterministic store ID from path."""
        try:
            rel = str(path.relative_to(self._base_dir)).replace("\\", "/")
        except ValueError:
            rel = str(path).replace("\\", "/")
        return rel.replace("/", "_").replace(".", "_").upper()

    def _infer_module(self, path: Path) -> str:
        """Infer module name from path."""
        parts = path.parts
        for i, part in enumerate(parts):
            if part == "data" and i + 1 < len(parts):
                data_sub = parts[i + 1]
                # Map data directory name to module name
                for module in ("universe", "import", "repair", "freshness",
                               "quality_gate", "governance_ops", "governance_alerts",
                               "research_registry", "governance_rollup"):
                    if module in data_sub.lower():
                        return module
        return "unknown"
