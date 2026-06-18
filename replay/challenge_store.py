"""
replay/challenge_store.py — ChallengeStore v1.2.7

Data paths: data/replay_challenges/
Append-only history. Atomic current state write. Corrupted tail graceful.
Rebuild index. Active payload and review answer key separated.

[!] No future outcome. No broker credentials. No secrets. No raw market data copies.
[!] Research Only. No Real Orders. Not Investment Advice.
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

DATA_DIR_NAME = "data/replay_challenges"

FORBIDDEN_STORE_FIELDS = [
    "broker", "order_token", "api_key", "secret", "password",
    "forward_return", "realized_pnl",
    "answer_key", "best_action", "expected_result",
]

STORE_FILES = [
    "challenges.jsonl",
    "attempts.jsonl",
    "actions.jsonl",
    "hints.jsonl",
    "scores.jsonl",
    "results.jsonl",
    "reviews.jsonl",
    "progress.jsonl",
    "streaks.jsonl",
    "badges.jsonl",
    "challenge_audit.jsonl",
]

STATE_FILE = "challenge_state.json"
INDEX_FILE = "challenge_index.csv"
EXPORTS_DIR = "exports"


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


class ChallengeStore:
    """
    Append-only store for challenge data.

    [!] Active payload and answer key are stored separately.
    [!] No future outcome in active store.
    [!] No broker credentials. No secrets.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    ACTIVE_AND_ANSWER_KEY_SEPARATED = True

    def __init__(self, repo_root: Optional[str] = None) -> None:
        self._root = Path(repo_root or os.getcwd())
        self._data_dir = self._root / DATA_DIR_NAME
        self._data_dir.mkdir(parents=True, exist_ok=True)
        (self._data_dir / EXPORTS_DIR).mkdir(exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self._data_dir / filename

    def append(self, store_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Append a record to a JSONL store."""
        filename = f"{store_name}.jsonl"
        path = self._path(filename)
        safe = _strip_forbidden(record)
        safe["_stored_at"] = _now_utc()
        safe["research_only"] = True
        safe["no_real_orders"] = True
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(safe, ensure_ascii=False) + "\n")
            return {"status": "APPENDED", "store": store_name}
        except Exception as exc:
            logger.error("Store append error (%s): %s", store_name, exc)
            return {"status": "ERROR", "error": str(exc)}

    def load_all(self, store_name: str) -> List[Dict[str, Any]]:
        """Load all records from a JSONL store."""
        return _safe_load_jsonl(self._path(f"{store_name}.jsonl"))

    def load_state(self) -> Dict[str, Any]:
        """Load current state (atomic JSON file)."""
        path = self._path(STATE_FILE)
        if not path.exists():
            return {}
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            logger.warning("State file corrupted, returning empty")
            return {}

    def save_state(self, state: Dict[str, Any]) -> None:
        """Save current state (atomic write)."""
        path = self._path(STATE_FILE)
        state["research_only"] = True
        state["no_real_orders"] = True
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(_strip_forbidden(state), f, ensure_ascii=False, indent=2)
        tmp.replace(path)

    def rebuild_index(self) -> Dict[str, Any]:
        """Rebuild the challenge index CSV."""
        challenges = self.load_all("challenges")
        path = self._path(INDEX_FILE)
        lines = ["challenge_id,title,challenge_type,difficulty,archived,created_at\n"]
        for c in challenges:
            line = ",".join([
                str(c.get("challenge_id", "")),
                str(c.get("title", "")).replace(",", " "),
                str(c.get("challenge_type", "")),
                str(c.get("difficulty", "")),
                str(c.get("archived", False)),
                str(c.get("created_at", "")),
            ])
            lines.append(line + "\n")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return {"status": "OK", "count": len(challenges)}
        except Exception as exc:
            return {"status": "ERROR", "error": str(exc)}

    def summary(self) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for name in STORE_FILES:
            store_name = name.replace(".jsonl", "")
            records = self.load_all(store_name)
            counts[store_name] = len(records)
        return {
            "data_dir": str(self._data_dir),
            "counts": counts,
            "active_and_answer_key_separated": True,
            "no_future_outcome": True,
            "no_broker_credentials": True,
            "no_secrets": True,
            "research_only": True,
            "no_real_orders": True,
        }
