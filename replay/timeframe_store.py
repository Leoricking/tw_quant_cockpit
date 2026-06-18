"""
replay/timeframe_store.py — MultiTimeframeReplayStore v1.2.5

Runtime data store for multi-timeframe replay.
Append-only. Atomic state. Corrupted tail graceful recovery.
Rebuildable index. No future outcomes. No secrets. No broker data.

Data paths (never committed):
  data/replay_timeframes/timeframe_snapshots.jsonl
  data/replay_timeframes/multi_snapshots.jsonl
  data/replay_timeframes/alignment_results.jsonl
  data/replay_timeframes/timeframe_agreements.jsonl
  data/replay_timeframes/timeframe_conflicts.jsonl
  data/replay_timeframes/timeline_events.jsonl
  data/replay_timeframes/timeframe_state.json
  data/replay_timeframes/timeframe_index.csv
  data/replay_timeframes/timeframe_audit.jsonl
  data/replay_timeframes/exports/

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Append-only. No future outcomes. No secrets. No broker data.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_STORE_FIELDS = [
    "outcome", "forward_return", "realized_pnl", "hindsight_score",
    "broker", "order_token", "api_key", "secret", "password",
]

DATA_DIR_NAME = "data/replay_timeframes"


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class MultiTimeframeReplayStore:
    """
    Append-only store for multi-timeframe replay data.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Append-only. Corrupted tail: graceful recovery.
    [!] No future outcomes. No secrets. No broker data.
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

    # ------------------------------------------------------------------
    # File paths
    # ------------------------------------------------------------------

    def _path(self, filename: str) -> Path:
        return self._data_dir / filename

    # ------------------------------------------------------------------
    # Snapshot storage
    # ------------------------------------------------------------------

    def append_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """Append a timeframe snapshot. Returns True on success."""
        return self._append_jsonl("timeframe_snapshots.jsonl", snapshot)

    def append_multi_snapshot(self, multi_snapshot: Dict[str, Any]) -> bool:
        """Append a multi-timeframe snapshot."""
        return self._append_jsonl("multi_snapshots.jsonl", multi_snapshot)

    def append_alignment(self, alignment: Dict[str, Any]) -> bool:
        """Append an alignment result."""
        return self._append_jsonl("alignment_results.jsonl", alignment)

    def append_agreement(self, agreement: Dict[str, Any]) -> bool:
        """Append an agreement result."""
        return self._append_jsonl("timeframe_agreements.jsonl", agreement)

    def append_conflict(self, conflict: Dict[str, Any]) -> bool:
        """Append a conflict record."""
        return self._append_jsonl("timeframe_conflicts.jsonl", conflict)

    def append_timeline_event(self, event: Dict[str, Any]) -> bool:
        """Append a timeline event."""
        return self._append_jsonl("timeline_events.jsonl", event)

    def append_audit(self, audit: Dict[str, Any]) -> bool:
        """Append an audit record."""
        return self._append_jsonl("timeframe_audit.jsonl", audit)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_snapshots(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load all snapshots with graceful corrupted tail recovery."""
        records = self._load_jsonl("timeframe_snapshots.jsonl")
        if session_id:
            records = [r for r in records if r.get("session_id") == session_id]
        return records

    def get_multi_snapshot(
        self, session_id: str, timestamp: str
    ) -> Optional[Dict[str, Any]]:
        """Load multi-snapshot for session at timestamp."""
        records = self._load_jsonl("multi_snapshots.jsonl")
        for r in records:
            if r.get("session_id") == session_id and r.get("replay_timestamp") == timestamp:
                return r
        return None

    def get_alignment_results(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load alignment results."""
        records = self._load_jsonl("alignment_results.jsonl")
        if session_id:
            records = [r for r in records if r.get("session_id") == session_id]
        return records

    def get_agreements(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load agreement results."""
        records = self._load_jsonl("timeframe_agreements.jsonl")
        if session_id:
            records = [r for r in records if r.get("session_id") == session_id]
        return records

    def get_conflicts(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load conflict records."""
        records = self._load_jsonl("timeframe_conflicts.jsonl")
        if session_id:
            records = [r for r in records if r.get("session_id") == session_id]
        return records

    def get_timeline(self, session_id: str) -> List[Dict[str, Any]]:
        """Load timeline events for session."""
        records = self._load_jsonl("timeline_events.jsonl")
        return [r for r in records if r.get("session_id") == session_id]

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def save_state(self, state: Dict[str, Any]) -> bool:
        """Save current state atomically."""
        # Strip forbidden fields
        safe_state = {k: v for k, v in state.items() if k not in FORBIDDEN_STORE_FIELDS}
        safe_state["saved_at"] = _now_utc()
        safe_state["research_only"] = True
        try:
            path = self._path("timeframe_state.json")
            tmp_path = path.with_suffix(".json.tmp")
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(safe_state, f, ensure_ascii=False, indent=2)
            tmp_path.replace(path)
            return True
        except Exception as e:
            logger.error("[MTFStore] save_state error: %s", e)
            return False

    def load_state(self) -> Dict[str, Any]:
        """Load current state."""
        path = self._path("timeframe_state.json")
        if not path.exists():
            return {"status": "EMPTY", "research_only": True}
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("[MTFStore] load_state error: %s", e)
            return {"status": "ERROR", "error": str(e), "research_only": True}

    def rebuild_index(self) -> bool:
        """Rebuild timeframe_index.csv from JSONL files."""
        try:
            records = self._load_jsonl("timeframe_snapshots.jsonl")
            index_path = self._path("timeframe_index.csv")
            import csv
            with open(index_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["snapshot_id", "session_id", "symbol", "timeframe", "replay_timestamp", "generated_at"],
                    extrasaction="ignore",
                )
                writer.writeheader()
                for r in records:
                    writer.writerow(r)
            return True
        except Exception as e:
            logger.error("[MTFStore] rebuild_index error: %s", e)
            return False

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _append_jsonl(self, filename: str, record: Dict[str, Any]) -> bool:
        """Append record to JSONL file. Strip forbidden fields."""
        safe = {k: v for k, v in record.items() if k not in FORBIDDEN_STORE_FIELDS}
        safe["research_only"] = True
        safe["no_real_orders"] = True
        try:
            path = self._path(filename)
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(safe, ensure_ascii=False) + "\n")
            return True
        except Exception as e:
            logger.error("[MTFStore] append_jsonl %s error: %s", filename, e)
            return False

    def _load_jsonl(self, filename: str) -> List[Dict[str, Any]]:
        """Load JSONL with graceful corrupted tail recovery."""
        path = self._path(filename)
        if not path.exists():
            return []
        records = []
        try:
            with open(path, encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning(
                            "[MTFStore] Skipping corrupted line %d in %s", lineno, filename
                        )
                        # Graceful recovery — continue with remaining records
        except Exception as e:
            logger.error("[MTFStore] load_jsonl %s error: %s", filename, e)
        return records
