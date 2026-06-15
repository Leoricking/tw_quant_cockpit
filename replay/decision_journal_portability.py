"""
replay/decision_journal_portability.py — DecisionJournalPortability for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Export: metadata/journal text only. No credentials. No future returns.
[!] Import: dry-run by default. Requires dry_run=False AND allow_write=True.
[!] No auto session open after import. No auto decision creation.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_EXPORT_FIELDS = [
    "api_key", "secret", "broker", "order_token", "password",
    "realized_return", "future_return", "hindsight_score",
    "realized_pnl", "final_result", "broker_credential",
]

KNOWN_REPO_PATHS = [
    "D:/code/Claude/tw_quant_cockpit",
    "C:/Users/Rossi/Documents/Claude/trading_master",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ImportResult:
    """Result of an import operation."""
    status: str
    dry_run: bool
    allow_write: bool
    entry_count: int
    imported_count: int
    skipped_count: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    entries: List[Dict[str, Any]] = field(default_factory=list)
    message: str = ""
    created_at: str = field(default_factory=_now_utc)


@dataclass
class ValidationResult:
    """Result of import file validation."""
    valid: bool
    entry_count: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    forbidden_fields_found: List[str] = field(default_factory=list)
    checked_at: str = field(default_factory=_now_utc)


class DecisionJournalPortability:
    """
    Handles export/import of decision journal metadata.

    [!] Export: strips secrets, no future returns, no PnL.
    [!] Import: dry_run=True by default. Blocked without allow_write=True.
    [!] Supports cross-machine path normalization.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        self._repo_root = repo_root
        if store is None:
            from replay.decision_journal_store import DecisionJournalStore
            self._store = DecisionJournalStore(repo_root=repo_root)

    def export_entry(
        self,
        entry_id: str,
        output_path: str = "",
        format: str = "jsonl",
    ) -> Dict[str, Any]:
        """Export a single journal entry (metadata only, no secrets)."""
        entry = self._store.get_entry(entry_id)
        if not entry:
            return {"status": "error", "message": f"Entry {entry_id} not found"}

        safe = self.redact_sensitive_fields(entry)
        safe = self.normalize_paths(safe)

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                if format == "jsonl":
                    f.write(json.dumps(safe, ensure_ascii=False) + "\n")
                else:
                    json.dump(safe, f, ensure_ascii=False, indent=2)

        return {"status": "ok", "entry": safe, "output_path": output_path}

    def export_entries(
        self,
        entry_ids: List[str],
        output_path: str,
        format: str = "jsonl",
    ) -> Dict[str, Any]:
        """Export multiple entries to a file."""
        entries = []
        for eid in entry_ids:
            e = self._store.get_entry(eid)
            if e:
                safe = self.redact_sensitive_fields(e)
                safe = self.normalize_paths(safe)
                entries.append(safe)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for e in entries:
                if format == "jsonl":
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
                else:
                    json.dump(e, f, ensure_ascii=False, indent=2)

        return {
            "status": "ok",
            "exported_count": len(entries),
            "output_path": output_path,
        }

    def export_session_journal(
        self, session_id: str, output_path: str = "", format: str = "jsonl"
    ) -> Dict[str, Any]:
        """Export all journal entries for a session."""
        all_entries = self._store.load_entries()
        latest: Dict[str, Dict[str, Any]] = {}
        for e in all_entries:
            eid = e.get("journal_entry_id", "")
            if eid and e.get("session_id") == session_id:
                latest[eid] = e

        entries = [self.redact_sensitive_fields(self.normalize_paths(e)) for e in latest.values()]

        if not output_path:
            exports_dir = Path(self._store._store_dir) / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(exports_dir / f"journal_session_{session_id}.jsonl")

        path = Path(output_path)
        with open(path, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

        return {
            "status": "ok",
            "session_id": session_id,
            "exported_count": len(entries),
            "output_path": output_path,
        }

    def import_entries(
        self,
        source_path: str,
        dry_run: bool = True,
        allow_write: bool = False,
    ) -> ImportResult:
        """
        Import entries from a file.
        BLOCKED unless dry_run=False AND allow_write=True.
        """
        validation = self.validate_import_file(source_path)

        if not validation.valid:
            return ImportResult(
                status="blocked",
                dry_run=dry_run,
                allow_write=allow_write,
                entry_count=0,
                imported_count=0,
                skipped_count=0,
                errors=validation.errors,
                message="Import blocked: validation failed",
            )

        if dry_run or not allow_write:
            return ImportResult(
                status="dry_run",
                dry_run=True,
                allow_write=allow_write,
                entry_count=validation.entry_count,
                imported_count=0,
                skipped_count=0,
                warnings=validation.warnings,
                entries=[],
                message=(
                    f"Dry run: {validation.entry_count} entries would be imported. "
                    "Use dry_run=False AND allow_write=True to execute."
                ),
            )

        # Execute import
        entries = self._load_source_file(source_path)
        imported = 0
        skipped = 0
        errors = []

        for entry in entries:
            safe = self.redact_sensitive_fields(entry)
            val = self._validate_entry_for_import(safe)
            if not val["valid"]:
                skipped += 1
                errors.extend(val["errors"])
                continue
            self._store.save_entry(safe)
            imported += 1

        return ImportResult(
            status="imported",
            dry_run=False,
            allow_write=True,
            entry_count=len(entries),
            imported_count=imported,
            skipped_count=skipped,
            errors=errors,
            message=f"Imported {imported}/{len(entries)} entries.",
        )

    def import_entry(
        self,
        entry_dict: Dict[str, Any],
        dry_run: bool = True,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Import a single entry dict."""
        safe = self.redact_sensitive_fields(entry_dict)

        if dry_run or not allow_write:
            val = self._validate_entry_for_import(safe)
            return {
                "status": "dry_run",
                "dry_run": True,
                "allow_write": allow_write,
                "validation": val,
                "message": "Dry run. Use dry_run=False AND allow_write=True to write.",
            }

        val = self._validate_entry_for_import(safe)
        if not val["valid"]:
            return {"status": "blocked", "errors": val["errors"]}

        self._store.save_entry(safe)
        return {"status": "imported", "journal_entry_id": safe.get("journal_entry_id")}

    def import_session_journal(
        self, source_path: str, dry_run: bool = True, allow_write: bool = False
    ) -> ImportResult:
        """Alias for import_entries."""
        return self.import_entries(source_path, dry_run=dry_run, allow_write=allow_write)

    def validate_import_file(self, path: str) -> ValidationResult:
        """Validate an import file before writing."""
        errors = []
        warnings = []
        forbidden_found = []

        entries = self._load_source_file(path)
        if not entries:
            errors.append("No valid entries found in import file")

        for i, entry in enumerate(entries):
            for fld in FORBIDDEN_EXPORT_FIELDS:
                if fld in entry:
                    forbidden_found.append(fld)
                    errors.append(f"Entry {i}: forbidden field '{fld}'")

        return ValidationResult(
            valid=len(errors) == 0,
            entry_count=len(entries),
            errors=errors,
            warnings=warnings,
            forbidden_fields_found=list(set(forbidden_found)),
        )

    def normalize_paths(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize absolute paths to repo-relative paths for portability."""
        result = dict(d)
        # Replace known machine-specific paths with relative markers
        for key, val in result.items():
            if isinstance(val, str):
                for repo_path in KNOWN_REPO_PATHS:
                    if repo_path in val:
                        result[key] = val.replace(repo_path, "<REPO_ROOT>")
        return result

    def redact_sensitive_fields(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive/forbidden fields from a dict."""
        return {k: v for k, v in d.items() if k not in FORBIDDEN_EXPORT_FIELDS}

    def portability_report(self, session_id: str) -> Dict[str, Any]:
        """Generate portability report for a session."""
        entries = self._store.load_entries()
        session_entries = [e for e in entries if e.get("session_id") == session_id]

        return {
            "session_id": session_id,
            "total_entries": len(session_entries),
            "exportable_entries": len(session_entries),
            "redacted_fields": FORBIDDEN_EXPORT_FIELDS,
            "supported_paths": KNOWN_REPO_PATHS,
            "simulation_only": True,
        }

    def _load_source_file(self, path: str) -> List[Dict[str, Any]]:
        """Load entries from a source file (JSONL or JSON)."""
        entries = []
        try:
            p = Path(path)
            if not p.exists():
                return entries
            with open(p, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                return entries
            # Try JSONL first
            lines = [l.strip() for l in content.splitlines() if l.strip()]
            for line in lines:
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        entries.append(obj)
                    elif isinstance(obj, list):
                        entries.extend(obj)
                except json.JSONDecodeError:
                    pass
        except Exception as exc:
            logger.error("Failed to load source file %s: %s", path, exc)
        return entries

    def _validate_entry_for_import(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an entry for import."""
        errors = []
        from replay.decision_journal_schema import JOURNAL_ID_PREFIX, FORBIDDEN_JOURNAL_FIELDS
        eid = entry.get("journal_entry_id", "")
        if not eid.startswith(JOURNAL_ID_PREFIX):
            errors.append(f"journal_entry_id must start with {JOURNAL_ID_PREFIX}")
        for fld in FORBIDDEN_JOURNAL_FIELDS:
            if fld in entry:
                errors.append(f"Forbidden field: {fld}")
        return {"valid": len(errors) == 0, "errors": errors}
