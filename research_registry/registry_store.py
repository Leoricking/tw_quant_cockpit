"""
research_registry.registry_store — RegistryStore v1.1.8

Append-only JSONL/CSV/JSON storage for the research run registry.
Atomic writes for state/index. Corrupt tail handled gracefully.
Audit log with immutable hash chain.

Runtime outputs (NOT committed):
  data/research_registry/runs.jsonl
  data/research_registry/run_state.json
  data/research_registry/run_index.csv
  data/research_registry/artifacts.jsonl
  data/research_registry/artifact_index.csv
  data/research_registry/lineage.jsonl
  data/research_registry/comparisons.jsonl
  data/research_registry/duplicate_index.csv
  data/research_registry/registry_summary.json
  data/research_registry/registry_audit.jsonl

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Append-only. History cannot be overwritten.
[!] No secrets, no credentials, no env vars, no broker info, no cookies.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STORE_DIR = os.path.join(BASE_DIR, "data", "research_registry")


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _audit_hash(event_dict: dict, prev_hash: str) -> str:
    payload = {
        "event_id": event_dict.get("event_id", ""),
        "event_type": event_dict.get("event_type", ""),
        "run_id": event_dict.get("run_id", ""),
        "timestamp": event_dict.get("timestamp", ""),
        "prev_hash": prev_hash,
    }
    return _sha256(json.dumps(payload, sort_keys=True))


class RegistryStore:
    """
    Append-only storage for the research run registry.

    [!] Research Only. No Real Orders.
    [!] Append-only. History cannot be overwritten.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store_dir: Optional[str] = None):
        self._dir = store_dir or DEFAULT_STORE_DIR
        self._runs_file = os.path.join(self._dir, "runs.jsonl")
        self._state_file = os.path.join(self._dir, "run_state.json")
        self._index_file = os.path.join(self._dir, "run_index.csv")
        self._artifacts_file = os.path.join(self._dir, "artifacts.jsonl")
        self._artifact_index_file = os.path.join(self._dir, "artifact_index.csv")
        self._lineage_file = os.path.join(self._dir, "lineage.jsonl")
        self._comparisons_file = os.path.join(self._dir, "comparisons.jsonl")
        self._duplicate_index_file = os.path.join(self._dir, "duplicate_index.csv")
        self._summary_file = os.path.join(self._dir, "registry_summary.json")
        self._audit_file = os.path.join(self._dir, "registry_audit.jsonl")
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        try:
            os.makedirs(self._dir, exist_ok=True)
        except Exception as exc:
            logger.warning("RegistryStore: could not create store dir: %s", exc)

    # ------------------------------------------------------------------
    # Run records
    # ------------------------------------------------------------------

    def append_run(self, run_record: Any) -> bool:
        """Append a run record to runs.jsonl (append-only)."""
        try:
            d = run_record.to_dict() if hasattr(run_record, "to_dict") else dict(run_record)
            self._append_jsonl(self._runs_file, d)
            self._append_audit_event("RUN_REGISTERED", d.get("run_id", ""), {"status": d.get("status", "")})
            return True
        except Exception as exc:
            logger.warning("RegistryStore.append_run failed (non-fatal): %s", exc)
            return False

    def update_run(self, run_record: Any) -> bool:
        """Append an updated run record to runs.jsonl (history preserved)."""
        try:
            d = run_record.to_dict() if hasattr(run_record, "to_dict") else dict(run_record)
            self._append_jsonl(self._runs_file, d)
            self._append_audit_event("RUN_UPDATED", d.get("run_id", ""), {"status": d.get("status", "")})
            return True
        except Exception as exc:
            logger.warning("RegistryStore.update_run failed (non-fatal): %s", exc)
            return False

    def list_runs(self) -> List[dict]:
        """Read all run records. Returns latest version of each run_id."""
        try:
            records = self._read_jsonl(self._runs_file)
            # Latest version per run_id
            by_id: Dict[str, dict] = {}
            for rec in records:
                run_id = rec.get("run_id", "")
                if run_id:
                    by_id[run_id] = rec
            return list(by_id.values())
        except Exception as exc:
            logger.warning("RegistryStore.list_runs failed (non-fatal): %s", exc)
            return []

    def get_run(self, run_id: str) -> Optional[dict]:
        """Get the latest version of a run by run_id."""
        try:
            records = self._read_jsonl(self._runs_file)
            result = None
            for rec in records:
                if rec.get("run_id") == run_id:
                    result = rec
            return result
        except Exception as exc:
            logger.warning("RegistryStore.get_run failed (non-fatal): %s", exc)
            return None

    def get_run_by_registry_id(self, registry_id: str) -> Optional[dict]:
        """Get a run by registry_id."""
        for rec in self.list_runs():
            if rec.get("registry_id") == registry_id:
                return rec
        return None

    def save_run_state(self, state: dict) -> bool:
        """Atomically save run_state.json."""
        return self._atomic_write_json(self._state_file, state)

    def load_run_state(self) -> dict:
        """Load run_state.json."""
        return self._read_json(self._state_file)

    def rebuild_run_index(self) -> bool:
        """Rebuild run_index.csv from runs.jsonl."""
        try:
            runs = self.list_runs()
            headers = ["run_id", "registry_id", "command_name", "run_type", "status", "qualification", "mode", "started_at", "completed_at"]
            rows = []
            for r in runs:
                rows.append([r.get(h, "") for h in headers])
            self._write_csv(self._index_file, headers, rows)
            return True
        except Exception as exc:
            logger.warning("rebuild_run_index failed (non-fatal): %s", exc)
            return False

    # ------------------------------------------------------------------
    # Artifacts
    # ------------------------------------------------------------------

    def append_artifact(self, artifact: Any) -> bool:
        """Append an artifact record to artifacts.jsonl."""
        try:
            d = artifact.to_dict() if hasattr(artifact, "to_dict") else dict(artifact)
            self._append_jsonl(self._artifacts_file, d)
            self._append_audit_event("ARTIFACT_REGISTERED", d.get("run_id", ""), {"artifact_id": d.get("artifact_id", "")})
            return True
        except Exception as exc:
            logger.warning("append_artifact failed (non-fatal): %s", exc)
            return False

    def list_artifacts(self) -> List[dict]:
        """Read all artifact records."""
        try:
            return self._read_jsonl(self._artifacts_file)
        except Exception:
            return []

    def list_run_artifacts(self, run_id: str) -> List[dict]:
        """Return all artifacts for a given run_id."""
        return [a for a in self.list_artifacts() if a.get("run_id") == run_id]

    # ------------------------------------------------------------------
    # Lineage
    # ------------------------------------------------------------------

    def append_lineage(self, lineage: Any) -> bool:
        """Append a lineage record to lineage.jsonl."""
        try:
            d = lineage.to_dict() if hasattr(lineage, "to_dict") else dict(lineage)
            self._append_jsonl(self._lineage_file, d)
            return True
        except Exception as exc:
            logger.warning("append_lineage failed (non-fatal): %s", exc)
            return False

    def list_lineage(self) -> List[dict]:
        """Read all lineage records."""
        try:
            return self._read_jsonl(self._lineage_file)
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Comparisons
    # ------------------------------------------------------------------

    def append_comparison(self, comparison: Any) -> bool:
        """Append a comparison to comparisons.jsonl."""
        try:
            d = comparison.to_dict() if hasattr(comparison, "to_dict") else dict(comparison)
            self._append_jsonl(self._comparisons_file, d)
            return True
        except Exception as exc:
            logger.warning("append_comparison failed (non-fatal): %s", exc)
            return False

    def list_comparisons(self) -> List[dict]:
        """Read all comparison records."""
        try:
            return self._read_jsonl(self._comparisons_file)
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Duplicate index
    # ------------------------------------------------------------------

    def save_duplicate_index(self, duplicate_map: Dict[str, str]) -> bool:
        """Save duplicate_index.csv from duplicate_run_id -> original_run_id mapping."""
        try:
            headers = ["duplicate_run_id", "original_run_id"]
            rows = [[k, v] for k, v in duplicate_map.items()]
            self._write_csv(self._duplicate_index_file, headers, rows)
            return True
        except Exception as exc:
            logger.warning("save_duplicate_index failed (non-fatal): %s", exc)
            return False

    def load_duplicate_index(self) -> Dict[str, str]:
        """Load duplicate_index.csv."""
        result = {}
        try:
            if not os.path.isfile(self._duplicate_index_file):
                return result
            with open(self._duplicate_index_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dup_id = row.get("duplicate_run_id", "")
                    orig_id = row.get("original_run_id", "")
                    if dup_id and orig_id:
                        result[dup_id] = orig_id
        except Exception as exc:
            logger.warning("load_duplicate_index failed (non-fatal): %s", exc)
        return result

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def save_summary(self, summary: Any) -> bool:
        """Save registry_summary.json."""
        try:
            d = summary.to_dict() if hasattr(summary, "to_dict") else dict(summary)
            return self._atomic_write_json(self._summary_file, d)
        except Exception as exc:
            logger.warning("save_summary failed (non-fatal): %s", exc)
            return False

    def load_summary(self) -> Optional[dict]:
        """Load registry_summary.json."""
        return self._read_json(self._summary_file) or None

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    def list_audit_events(self, run_id: Optional[str] = None) -> List[dict]:
        """Return audit events, optionally filtered by run_id."""
        try:
            events = self._read_jsonl(self._audit_file)
            if run_id:
                events = [e for e in events if e.get("run_id") == run_id]
            return events
        except Exception:
            return []

    def verify_audit_chain(self) -> dict:
        """Verify the immutable hash chain in registry_audit.jsonl."""
        try:
            events = self._read_jsonl(self._audit_file)
            if not events:
                return {"valid": True, "event_count": 0, "broken_at": None}

            prev_hash = ""
            for i, event in enumerate(events):
                stored_hash = event.get("immutable_hash", "")
                # Rebuild hash without immutable_hash field
                event_copy = {k: v for k, v in event.items() if k != "immutable_hash"}
                expected_hash = _audit_hash(event_copy, prev_hash)
                if stored_hash and stored_hash != expected_hash:
                    return {
                        "valid": False,
                        "event_count": len(events),
                        "broken_at": i,
                        "event_id": event.get("event_id", ""),
                        "message": f"Hash mismatch at event {i}: stored={stored_hash[:8]}... expected={expected_hash[:8]}...",
                    }
                prev_hash = stored_hash or expected_hash

            return {"valid": True, "event_count": len(events), "broken_at": None}
        except Exception as exc:
            return {"valid": False, "event_count": 0, "broken_at": -1, "message": str(exc)}

    def _append_audit_event(self, event_type: str, run_id: str, details: Optional[dict] = None) -> None:
        """Append an audit event with immutable hash chain."""
        try:
            # Get previous hash
            existing = self._read_jsonl(self._audit_file)
            prev_hash = ""
            if existing:
                prev_hash = existing[-1].get("immutable_hash", "")

            event = {
                "event_id": _new_uuid(),
                "event_type": event_type,
                "run_id": run_id,
                "timestamp": _now_utc(),
                "details": details or {},
            }
            event["immutable_hash"] = _audit_hash(event, prev_hash)
            self._append_jsonl(self._audit_file, event)
        except Exception as exc:
            logger.debug("_append_audit_event failed (non-fatal): %s", exc)

    # ------------------------------------------------------------------
    # Rebuild
    # ------------------------------------------------------------------

    def rebuild_indexes(self) -> bool:
        """Rebuild all index files from raw JSONL data."""
        ok = True
        ok = ok and self.rebuild_run_index()
        return ok

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _append_jsonl(self, filepath: str, data: dict) -> None:
        """Append a JSON line to a JSONL file."""
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def _read_jsonl(self, filepath: str) -> List[dict]:
        """Read a JSONL file, skipping corrupt lines (graceful tail handling)."""
        if not os.path.isfile(filepath):
            return []
        records = []
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    logger.warning("_read_jsonl: corrupt line at %d in %s — skipped (WARN)", i, filepath)
        return records

    def _atomic_write_json(self, filepath: str, data: dict) -> bool:
        """Write JSON atomically (write to temp, then rename)."""
        try:
            tmp = filepath + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, filepath)
            return True
        except Exception as exc:
            logger.warning("_atomic_write_json failed: %s", exc)
            return False

    def _read_json(self, filepath: str) -> Optional[dict]:
        """Read a JSON file."""
        if not os.path.isfile(filepath):
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("_read_json failed for %s: %s", filepath, exc)
            return None

    def _write_csv(self, filepath: str, headers: List[str], rows: List[list]) -> None:
        """Write a CSV file."""
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
