"""
replay/decision_journal_store.py — DecisionJournalStore for v1.2.2

Manages append-only journal storage in data/replay_journal/.
[!] Research Only. No Real Orders. Replay Training Only.
[!] Runtime data — NOT committed to git.
[!] No future returns. No realized PnL. No credentials.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class DecisionJournalStore:
    """
    Append-only store for decision journal data.

    Files:
      journal_entries.jsonl     — append-only
      journal_revisions.jsonl   — append-only
      journal_links.jsonl       — append-only
      emotional_states.jsonl    — append-only
      discipline_checklists.jsonl — append-only
      journal_state.json        — atomic write
      journal_index.csv         — rebuild from entries
      journal_audit.jsonl       — append-only
      exports/                  — export subdirectory

    [!] Never overwrites existing records.
    [!] No future returns. No PnL. No secrets.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store_dir: Optional[str] = None, repo_root: Optional[str] = None):
        if store_dir:
            self._store_dir = Path(store_dir)
        elif repo_root:
            self._store_dir = Path(repo_root) / "data" / "replay_journal"
        else:
            base = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self._store_dir = base / "data" / "replay_journal"

        self._entries_file = self._store_dir / "journal_entries.jsonl"
        self._revisions_file = self._store_dir / "journal_revisions.jsonl"
        self._links_file = self._store_dir / "journal_links.jsonl"
        self._emotional_states_file = self._store_dir / "emotional_states.jsonl"
        self._checklists_file = self._store_dir / "discipline_checklists.jsonl"
        self._state_file = self._store_dir / "journal_state.json"
        self._index_file = self._store_dir / "journal_index.csv"
        self._audit_file = self._store_dir / "journal_audit.jsonl"
        self._exports_dir = self._store_dir / "exports"

        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        try:
            self._store_dir.mkdir(parents=True, exist_ok=True)
            self._exports_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.warning("Could not create journal store dirs: %s", exc)

    def _append_jsonl(self, path: Path, record: Dict[str, Any]) -> None:
        """Append one JSON record to a JSONL file."""
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.error("Failed to append to %s: %s", path, exc)

    def _load_jsonl(self, path: Path) -> List[Dict[str, Any]]:
        """Load all valid records from a JSONL file. Graceful on corrupted tail."""
        records = []
        if not path.exists():
            return records
        try:
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning("Corrupted line %d in %s — skipping", i + 1, path)
        except Exception as exc:
            logger.error("Failed to load %s: %s", path, exc)
        return records

    def save_entry(self, entry_dict: Dict[str, Any]) -> None:
        """Append a journal entry (append-only, never overwrites)."""
        self._append_jsonl(self._entries_file, entry_dict)
        self._write_audit("ENTRY_SAVED", {"journal_entry_id": entry_dict.get("journal_entry_id")})

    def save_revision(self, revision_dict: Dict[str, Any]) -> None:
        """Append a revision record (append-only)."""
        self._append_jsonl(self._revisions_file, revision_dict)
        self._write_audit("REVISION_SAVED", {"revision_id": revision_dict.get("revision_id")})

    def save_link(self, link_dict: Dict[str, Any]) -> None:
        """Append a journal link."""
        self._append_jsonl(self._links_file, link_dict)

    def save_emotional_state(self, state_dict: Dict[str, Any]) -> None:
        """Append an emotional state record (append-only)."""
        self._append_jsonl(self._emotional_states_file, state_dict)

    def save_checklist(self, checklist_dict: Dict[str, Any]) -> None:
        """Append a discipline checklist result (append-only)."""
        self._append_jsonl(self._checklists_file, checklist_dict)

    def load_entries(self) -> List[Dict[str, Any]]:
        """Load all journal entries."""
        return self._load_jsonl(self._entries_file)

    def load_revisions(self) -> List[Dict[str, Any]]:
        """Load all revision records."""
        return self._load_jsonl(self._revisions_file)

    def load_links(self) -> List[Dict[str, Any]]:
        """Load all journal links."""
        return self._load_jsonl(self._links_file)

    def load_emotional_states(self) -> List[Dict[str, Any]]:
        """Load all emotional state records."""
        return self._load_jsonl(self._emotional_states_file)

    def load_checklists(self) -> List[Dict[str, Any]]:
        """Load all discipline checklist results."""
        return self._load_jsonl(self._checklists_file)

    def get_entry(self, journal_entry_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest version of an entry by ID."""
        entries = self.load_entries()
        # Return last occurrence (latest status update)
        result = None
        for e in entries:
            if e.get("journal_entry_id") == journal_entry_id:
                result = e
        return result

    def rebuild_index(self) -> int:
        """Rebuild the CSV index from entries. Returns count."""
        entries = self.load_entries()
        # Deduplicate — keep last record per journal_entry_id
        latest: Dict[str, Dict[str, Any]] = {}
        for e in entries:
            eid = e.get("journal_entry_id", "")
            if eid:
                latest[eid] = e

        count = 0
        try:
            with open(self._index_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "journal_entry_id", "session_id", "decision_id",
                    "replay_date", "action", "symbol", "status",
                    "revision_count", "created_at",
                ])
                writer.writeheader()
                for e in latest.values():
                    writer.writerow({
                        "journal_entry_id": e.get("journal_entry_id", ""),
                        "session_id": e.get("session_id", ""),
                        "decision_id": e.get("decision_id", ""),
                        "replay_date": e.get("replay_date", ""),
                        "action": e.get("action", ""),
                        "symbol": e.get("symbol", ""),
                        "status": e.get("status", ""),
                        "revision_count": e.get("revision_count", 0),
                        "created_at": e.get("created_at", ""),
                    })
                    count += 1
        except Exception as exc:
            logger.error("Failed to rebuild index: %s", exc)

        return count

    def save_state(self, state: Dict[str, Any]) -> None:
        """Atomic write of journal state."""
        try:
            tmp = self._state_file.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            tmp.replace(self._state_file)
        except Exception as exc:
            logger.error("Failed to save journal state: %s", exc)

    def load_state(self) -> Dict[str, Any]:
        """Load journal state."""
        if not self._state_file.exists():
            return {"store_version": "1.2.2", "entry_count": 0, "updated_at": _now_utc()}
        try:
            with open(self._state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("Failed to load journal state: %s", exc)
            return {}

    def _write_audit(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Write to audit log."""
        record = {
            "event_type": event_type,
            "payload": payload,
            "created_at": _now_utc(),
            "simulation_only": True,
            "no_real_orders": True,
        }
        self._append_jsonl(self._audit_file, record)

    def get_store_health(self) -> Dict[str, Any]:
        """Check store health."""
        checks = []
        issues = []
        status = "OK"

        checks.append({"name": "store_dir_exists", "passed": self._store_dir.exists()})
        if not self._store_dir.exists():
            issues.append("store directory missing")
            status = "WARN"

        entry_count = 0
        try:
            entries = self.load_entries()
            entry_count = len(entries)
            checks.append({"name": "entries_loadable", "passed": True})
        except Exception as exc:
            checks.append({"name": "entries_loadable", "passed": False, "error": str(exc)})
            issues.append(f"entries load error: {exc}")
            status = "FAIL"

        # Check all entries have DJR- prefix
        from replay.decision_journal_schema import JOURNAL_ID_PREFIX
        bad_ids = [e.get("journal_entry_id", "") for e in (self.load_entries() if entry_count > 0 else [])
                   if not e.get("journal_entry_id", "").startswith(JOURNAL_ID_PREFIX)]
        if bad_ids:
            issues.append(f"Entries without DJR- prefix: {bad_ids[:3]}")
            status = "FAIL"
        checks.append({"name": "entries_have_djr_prefix", "passed": len(bad_ids) == 0})

        # Check simulation_only enforced
        non_sim = [e for e in (self.load_entries() if entry_count > 0 else [])
                   if not e.get("simulation_only", True)]
        if non_sim:
            issues.append(f"Entries with simulation_only=False: {len(non_sim)}")
            status = "FAIL"
        checks.append({"name": "simulation_only_enforced", "passed": len(non_sim) == 0})

        return {
            "status": status,
            "store_dir": str(self._store_dir),
            "entry_count": entry_count,
            "checks": checks,
            "issues": issues,
            "checked_at": _now_utc(),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Return summary stats (no performance metrics)."""
        entries = self.load_entries()
        revisions = self.load_revisions()

        status_counts: Dict[str, int] = {}
        for e in entries:
            s = e.get("status", "UNKNOWN")
            status_counts[s] = status_counts.get(s, 0) + 1

        return {
            "total_entries": len(entries),
            "total_revisions": len(revisions),
            "status_distribution": status_counts,
            "store_dir": str(self._store_dir),
        }
