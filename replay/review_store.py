"""
replay/review_store.py — ReplayReviewStore v1.2.6

Manages data/replay_review/ (append-only JSONL files, atomic current state,
corrupted tail graceful recovery, rebuild index).
Stores only references/review metadata/notes/tags/progress.
NOT raw scores/journal/strategies/outcomes.

Data paths (never committed):
  data/replay_review/dashboard_snapshots.jsonl
  data/replay_review/review_queue.jsonl
  data/replay_review/review_progress.jsonl
  data/replay_review/review_checklists.jsonl
  data/replay_review/review_notes.jsonl
  data/replay_review/review_tags.jsonl
  data/replay_review/review_history.jsonl
  data/replay_review/review_state.json
  data/replay_review/review_index.csv
  data/replay_review/review_audit.jsonl
  data/replay_review/exports/

[!] Research Only. No Real Orders. Append-only. Not Investment Advice.
[!] Stores review metadata only. NOT raw scores/journal/strategies/outcomes.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

DATA_DIR_NAME = "data/replay_review"

FORBIDDEN_STORE_FIELDS = [
    "broker", "order_token", "api_key", "secret", "password",
    "raw_outcome_pnl", "realized_pnl", "forward_return",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _strip_forbidden(record: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in record.items() if k not in FORBIDDEN_STORE_FIELDS}


def _safe_load_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Load JSONL with corrupted tail graceful recovery."""
    if not path.exists():
        return []
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("Skipping corrupted JSONL line in %s", path)
    return records


class ReplayReviewStore:
    """
    Append-only store for replay review metadata.

    [!] Stores only references/review metadata/notes/tags/progress.
    [!] NOT raw scores/journal/strategies/outcomes.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, base_dir: Optional[str] = None) -> None:
        if base_dir:
            self._data_dir = Path(base_dir) / DATA_DIR_NAME
        else:
            repo_root = Path(__file__).parent.parent
            self._data_dir = repo_root / DATA_DIR_NAME
        self._data_dir.mkdir(parents=True, exist_ok=True)
        (self._data_dir / "exports").mkdir(exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self._data_dir / filename

    def _append(self, filename: str, record: Dict[str, Any]) -> bool:
        """Append a record to a JSONL file."""
        try:
            clean = _strip_forbidden(record)
            with open(self._path(filename), "a", encoding="utf-8") as f:
                f.write(json.dumps(clean, ensure_ascii=False) + "\n")
            return True
        except Exception as exc:
            logger.error("Append to %s failed: %s", filename, exc)
            return False

    def _load(self, filename: str) -> List[Dict[str, Any]]:
        return _safe_load_jsonl(self._path(filename))

    # ------------------------------------------------------------------
    # Dashboard snapshots
    # ------------------------------------------------------------------

    def append_snapshot(self, record: Dict[str, Any]) -> bool:
        return self._append("dashboard_snapshots.jsonl", record)

    def get_snapshots(self, limit: int = 10) -> List[Dict[str, Any]]:
        snaps = self._load("dashboard_snapshots.jsonl")
        return snaps[-limit:] if limit else snaps

    # ------------------------------------------------------------------
    # Review queue
    # ------------------------------------------------------------------

    def append_queue_item(self, record: Dict[str, Any]) -> bool:
        return self._append("review_queue.jsonl", record)

    def get_queue(self) -> List[Dict[str, Any]]:
        return self._load("review_queue.jsonl")

    # ------------------------------------------------------------------
    # Review progress
    # ------------------------------------------------------------------

    def append_progress(self, record: Dict[str, Any]) -> bool:
        return self._append("review_progress.jsonl", record)

    def get_progress(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        rows = self._load("review_progress.jsonl")
        if session_id:
            rows = [r for r in rows if r.get("session_id") == session_id]
        return rows

    # ------------------------------------------------------------------
    # Checklists
    # ------------------------------------------------------------------

    def append_checklist_item(self, record: Dict[str, Any]) -> bool:
        return self._append("review_checklists.jsonl", record)

    def get_checklists(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        rows = self._load("review_checklists.jsonl")
        if session_id:
            rows = [r for r in rows if r.get("session_id") == session_id]
        return rows

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    def append_note(self, record: Dict[str, Any]) -> bool:
        return self._append("review_notes.jsonl", record)

    def get_notes(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        rows = self._load("review_notes.jsonl")
        if session_id:
            rows = [r for r in rows if r.get("session_id") == session_id]
        return rows

    # ------------------------------------------------------------------
    # Tags
    # ------------------------------------------------------------------

    def append_tag(self, record: Dict[str, Any]) -> bool:
        return self._append("review_tags.jsonl", record)

    def get_tags(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        rows = self._load("review_tags.jsonl")
        if session_id:
            rows = [r for r in rows if r.get("session_id") == session_id]
        return rows

    # ------------------------------------------------------------------
    # History / Audit
    # ------------------------------------------------------------------

    def append_history(self, record: Dict[str, Any]) -> bool:
        return self._append("review_history.jsonl", record)

    def get_history(self) -> List[Dict[str, Any]]:
        return self._load("review_history.jsonl")

    def append_audit(self, record: Dict[str, Any]) -> bool:
        return self._append("review_audit.jsonl", record)

    # ------------------------------------------------------------------
    # State (atomic write)
    # ------------------------------------------------------------------

    def write_state(self, state: Dict[str, Any]) -> bool:
        """Atomic write of current review state."""
        try:
            path = self._path("review_state.json")
            tmp  = path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
            return True
        except Exception as exc:
            logger.error("write_state failed: %s", exc)
            return False

    def read_state(self) -> Dict[str, Any]:
        path = self._path("review_state.json")
        if not path.exists():
            return {}
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("read_state failed: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Index rebuild
    # ------------------------------------------------------------------

    def rebuild_index(self) -> bool:
        """Rebuild review_index.csv from JSONL data."""
        try:
            progress_rows = self._load("review_progress.jsonl")
            path = self._path("review_index.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write("session_id,status,progress_percent,calculated_at\n")
                for r in progress_rows:
                    f.write(
                        f"{r.get('session_id','')},{r.get('status','')}"
                        f",{r.get('progress_percent',0)},{r.get('calculated_at','')}\n"
                    )
            return True
        except Exception as exc:
            logger.error("rebuild_index failed: %s", exc)
            return False
