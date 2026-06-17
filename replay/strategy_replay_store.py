"""
replay/strategy_replay_store.py — Append-only JSONL store for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Append-only JSONL files in data/replay_strategy/.
[!] Corrupted tail lines are skipped gracefully.
[!] Never commits runtime data (data/replay_strategy/ is in .gitignore).
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

STRATEGY_DATA_DIR = "data/replay_strategy"

STORE_FILES = {
    "snapshot": "strategy_snapshots.jsonl",
    "module_result": "module_results.jsonl",
    "timeline": "signal_timeline.jsonl",
    "agreement": "agreements.jsonl",
    "conflict": "conflicts.jsonl",
    "rule_review": "rule_reviews.jsonl",
    "review_history": "review_history.jsonl",
    "audit": "strategy_audit.jsonl",
}

STATE_FILE = "strategy_state.json"
INDEX_FILE = "strategy_index.csv"


class StrategyReplayStore:
    """
    Append-only JSONL store for strategy replay data.

    [!] Research Only. No Real Orders.
    [!] Corrupted tail lines are skipped — does NOT crash.
    [!] Never commits to git (data/replay_strategy/ in .gitignore).
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        if repo_root:
            self._base_dir = os.path.join(repo_root, STRATEGY_DATA_DIR)
        else:
            self._base_dir = STRATEGY_DATA_DIR
        os.makedirs(self._base_dir, exist_ok=True)

    def _path(self, store_type: str) -> str:
        filename = STORE_FILES.get(store_type, f"{store_type}.jsonl")
        return os.path.join(self._base_dir, filename)

    def _append(self, store_type: str, record: Dict[str, Any]) -> None:
        path = self._path(store_type)
        record["_stored_at"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.error("Failed to append to %s: %s", path, exc)
            raise

    def _load_all(self, store_type: str) -> List[Dict[str, Any]]:
        """Load all records. Skips corrupted tail lines — does NOT crash."""
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
                except json.JSONDecodeError:
                    logger.warning("Skipping corrupted line %d in %s", line_num, path)
        return records

    def append_snapshot(self, snapshot: Any) -> None:
        record = snapshot.to_dict() if hasattr(snapshot, "to_dict") else snapshot
        self._append("snapshot", record)

    def append_module_result(self, result: Any) -> None:
        record = result.to_dict() if hasattr(result, "to_dict") else result
        self._append("module_result", record)

    def append_timeline_record(self, record: Any) -> None:
        rec = record.to_dict() if hasattr(record, "to_dict") else record
        self._append("timeline", rec)

    def append_agreement(self, agreement: Any) -> None:
        record = agreement.to_dict() if hasattr(agreement, "to_dict") else agreement
        self._append("agreement", record)

    def append_conflict(self, conflict: Dict[str, Any]) -> None:
        self._append("conflict", conflict)

    def append_rule_review(self, review: Any) -> None:
        record = review.to_dict() if hasattr(review, "to_dict") else review
        self._append("rule_review", record)

    def append_review_history(self, history_entry: Dict[str, Any]) -> None:
        self._append("review_history", history_entry)

    def append_audit(self, entry: Dict[str, Any]) -> None:
        self._append("audit", entry)

    def update_state(self, state_dict: Dict[str, Any]) -> None:
        """Atomic write to state JSON file."""
        path = os.path.join(self._base_dir, STATE_FILE)
        state_dict["_updated_at"] = datetime.now(timezone.utc).isoformat()
        tmp_path = path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(state_dict, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, path)
        except Exception as exc:
            logger.error("Failed to update state: %s", exc)
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            raise

    def load_state(self) -> Dict[str, Any]:
        path = os.path.join(self._base_dir, STATE_FILE)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_snapshots(self) -> List[Dict[str, Any]]:
        return self._load_all("snapshot")

    def load_module_results(self) -> List[Dict[str, Any]]:
        return self._load_all("module_result")

    def load_timeline(self) -> List[Dict[str, Any]]:
        return self._load_all("timeline")

    def load_agreements(self) -> List[Dict[str, Any]]:
        return self._load_all("agreement")

    def load_conflicts(self) -> List[Dict[str, Any]]:
        return self._load_all("conflict")

    def load_rule_reviews(self) -> List[Dict[str, Any]]:
        return self._load_all("rule_review")

    def load_review_history(self) -> List[Dict[str, Any]]:
        return self._load_all("review_history")

    def rebuild_index(self) -> int:
        """Rebuild the CSV index from snapshots. Returns row count."""
        snapshots = self.load_snapshots()
        index_path = os.path.join(self._base_dir, INDEX_FILE)
        rows = []
        for snap in snapshots:
            rows.append({
                "strategy_snapshot_id": snap.get("strategy_snapshot_id", ""),
                "session_id": snap.get("session_id", ""),
                "symbol": snap.get("symbol", ""),
                "replay_date": snap.get("replay_date", ""),
                "agreement_score": snap.get("agreement_score", ""),
                "conflict_score": snap.get("conflict_score", ""),
                "generated_at": snap.get("generated_at", ""),
            })
        if rows:
            with open(index_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        return len(rows)

    def load_by_session(
        self, store_type: str, session_id: str
    ) -> List[Dict[str, Any]]:
        return [
            r for r in self._load_all(store_type)
            if r.get("session_id") == session_id
        ]

    def load_by_symbol(
        self, store_type: str, symbol: str
    ) -> List[Dict[str, Any]]:
        return [
            r for r in self._load_all(store_type)
            if r.get("symbol") == symbol
        ]
