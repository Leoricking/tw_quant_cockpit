"""
replay/scoring_store.py — Scoring store for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Append-only JSONL files in data/replay_scoring/.
[!] Corrupted tail lines are skipped — does NOT crash.
[!] Never commits runtime data (data/replay_scoring/ is in .gitignore).
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SCORING_DATA_DIR = "data/replay_scoring"
STORE_FILES = {
    "process_score": "process_scores.jsonl",
    "outcome_score": "outcome_scores.jsonl",
    "composite_score": "composite_scores.jsonl",
    "reveal": "outcome_reveals.jsonl",
    "mistake": "mistakes.jsonl",
    "mistake_review": "mistake_reviews.jsonl",
    "plan_adherence": "plan_adherence.jsonl",
}


class ReplayScoringStore:
    """
    Append-only JSONL store for replay scoring data.

    [!] Research Only. No Real Orders.
    [!] Corrupted tail lines are skipped — does NOT crash.
    [!] Never commits to git (data/replay_scoring/ in .gitignore).
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        if repo_root:
            self._base_dir = os.path.join(repo_root, SCORING_DATA_DIR)
        else:
            self._base_dir = SCORING_DATA_DIR
        os.makedirs(self._base_dir, exist_ok=True)

    def _path(self, store_type: str) -> str:
        filename = STORE_FILES.get(store_type, f"{store_type}.jsonl")
        return os.path.join(self._base_dir, filename)

    def append(self, store_type: str, record: Dict[str, Any]) -> None:
        """Append a record to the JSONL store."""
        path = self._path(store_type)
        record["_stored_at"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.error("Failed to append to %s: %s", path, exc)
            raise

    def load_all(self, store_type: str) -> List[Dict[str, Any]]:
        """
        Load all records from the JSONL store.
        Skips corrupted tail lines — does NOT crash.
        """
        path = self._path(store_type)
        records = []
        if not os.path.exists(path):
            return records

        with open(path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    logger.warning(
                        "Skipping corrupted line %d in %s: %s",
                        line_num, path, exc,
                    )
                    continue  # Skip corrupted lines — do NOT crash
        return records

    def load_by_session(self, store_type: str, session_id: str) -> List[Dict[str, Any]]:
        """Load records for a specific session."""
        return [
            r for r in self.load_all(store_type)
            if r.get("session_id") == session_id
        ]

    def load_by_id(self, store_type: str, record_id: str, id_field: str = "score_id") -> Optional[Dict[str, Any]]:
        """Load a single record by ID."""
        for r in self.load_all(store_type):
            if r.get(id_field) == record_id:
                return r
        return None

    def count(self, store_type: str) -> int:
        """Count records in store."""
        return len(self.load_all(store_type))

    def store_exists(self, store_type: str) -> bool:
        return os.path.exists(self._path(store_type))

    def store_path(self, store_type: str) -> str:
        return self._path(store_type)

    def all_store_types(self) -> List[str]:
        return list(STORE_FILES.keys())

    def health(self) -> Dict[str, Any]:
        """Return health info for all stores."""
        result = {
            "base_dir": self._base_dir,
            "base_dir_exists": os.path.exists(self._base_dir),
            "stores": {},
        }
        for stype in STORE_FILES:
            path = self._path(stype)
            exists = os.path.exists(path)
            count = 0
            corrupted = 0
            if exists:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            json.loads(line)
                            count += 1
                        except json.JSONDecodeError:
                            corrupted += 1
            result["stores"][stype] = {
                "path": path,
                "exists": exists,
                "record_count": count,
                "corrupted_lines": corrupted,
            }
        return result
