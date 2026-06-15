"""
governance_ops.operations_store — OperationsStore v1.1.6

Runtime outputs for governance operations. NOT committed to git.
- governance_summary.json
- module_health.csv
- symbol_status.csv
- action_queue.csv
- source_health.csv
- gate_summary.csv
- enforcement_runs.csv
- audit_summary.csv
- daily_history.jsonl (append-only, never overwrite)
- dashboard_state.json
- action_audit.jsonl (append-only, audit of action metadata changes)

Snapshot rules:
- Each governance-dashboard or governance-report run appends one daily snapshot to daily_history.jsonl
- Multiple runs same day = multiple entries with timestamps
- Never overwrite history
- No secrets in snapshots

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Runtime outputs are NOT committed. See .gitignore.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STORE_DIR = os.path.join(BASE_DIR, "data", "governance_ops")


class OperationsStore:
    """
    Manages runtime outputs for governance operations.

    [!] Research Only. No Real Orders.
    [!] Runtime outputs are NOT committed to git.
    """

    def __init__(self, store_dir: str = DEFAULT_STORE_DIR):
        self._dir = store_dir
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        try:
            os.makedirs(self._dir, exist_ok=True)
        except Exception as exc:
            logger.warning("OperationsStore._ensure_dir error: %s", exc)

    def _path(self, filename: str) -> str:
        return os.path.join(self._dir, filename)

    # -----------------------------------------------------------------------
    # Governance summary
    # -----------------------------------------------------------------------

    def save_summary(self, summary_dict: dict) -> str:
        path = self._path("governance_summary.json")
        try:
            # Strip any secrets (defensive)
            safe = _strip_secrets(summary_dict)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(safe, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("save_summary error: %s", exc)
        return path

    def load_summary(self) -> Optional[dict]:
        path = self._path("governance_summary.json")
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("load_summary: corrupt/missing: %s", exc)
            return None

    # -----------------------------------------------------------------------
    # Module health CSV
    # -----------------------------------------------------------------------

    def save_module_health(self, module_rows: List[dict]) -> str:
        path = self._path("module_health.csv")
        try:
            _write_csv(path, module_rows)
        except Exception as exc:
            logger.warning("save_module_health error: %s", exc)
        return path

    def load_module_health(self) -> List[dict]:
        path = self._path("module_health.csv")
        return _read_csv(path)

    # -----------------------------------------------------------------------
    # Symbol status CSV
    # -----------------------------------------------------------------------

    def save_symbol_status(self, symbol_rows: List[dict]) -> str:
        path = self._path("symbol_status.csv")
        try:
            _write_csv(path, symbol_rows)
        except Exception as exc:
            logger.warning("save_symbol_status error: %s", exc)
        return path

    def load_symbol_status(self) -> List[dict]:
        path = self._path("symbol_status.csv")
        return _read_csv(path)

    # -----------------------------------------------------------------------
    # Action queue CSV
    # -----------------------------------------------------------------------

    def save_action_queue(self, action_rows: List[dict]) -> str:
        path = self._path("action_queue.csv")
        try:
            _write_csv(path, action_rows)
        except Exception as exc:
            logger.warning("save_action_queue error: %s", exc)
        return path

    def load_action_queue(self) -> List[dict]:
        path = self._path("action_queue.csv")
        return _read_csv(path)

    # -----------------------------------------------------------------------
    # Enforcement runs CSV
    # -----------------------------------------------------------------------

    def save_enforcement_runs(self, run_rows: List[dict]) -> str:
        path = self._path("enforcement_runs.csv")
        try:
            _write_csv(path, run_rows)
        except Exception as exc:
            logger.warning("save_enforcement_runs error: %s", exc)
        return path

    def load_enforcement_runs(self) -> List[dict]:
        path = self._path("enforcement_runs.csv")
        return _read_csv(path)

    # -----------------------------------------------------------------------
    # Audit summary CSV
    # -----------------------------------------------------------------------

    def save_audit_summary(self, audit_rows: List[dict]) -> str:
        path = self._path("audit_summary.csv")
        try:
            _write_csv(path, audit_rows)
        except Exception as exc:
            logger.warning("save_audit_summary error: %s", exc)
        return path

    def load_audit_summary(self) -> List[dict]:
        path = self._path("audit_summary.csv")
        return _read_csv(path)

    # -----------------------------------------------------------------------
    # Daily history JSONL (append-only, never overwrite)
    # -----------------------------------------------------------------------

    def append_daily_snapshot(self, snapshot: dict) -> str:
        """Append one snapshot to daily_history.jsonl. Never overwrites existing entries."""
        path = self._path("daily_history.jsonl")
        try:
            safe = _strip_secrets(snapshot)
            safe["_appended_at"] = datetime.now(timezone.utc).isoformat()
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(safe, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("append_daily_snapshot error: %s", exc)
        return path

    def load_daily_history(self) -> List[dict]:
        """Load all daily snapshots from daily_history.jsonl."""
        path = self._path("daily_history.jsonl")
        return _read_jsonl(path)

    # -----------------------------------------------------------------------
    # Dashboard state
    # -----------------------------------------------------------------------

    def save_dashboard_state(self, state: dict) -> str:
        path = self._path("dashboard_state.json")
        try:
            safe = _strip_secrets(state)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(safe, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("save_dashboard_state error: %s", exc)
        return path

    def load_dashboard_state(self) -> Optional[dict]:
        path = self._path("dashboard_state.json")
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("load_dashboard_state: corrupt/missing: %s", exc)
            return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_csv(path: str, rows: List[dict]) -> None:
    """Write list of dicts to CSV."""
    if not rows:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: str) -> List[dict]:
    """Read CSV to list of dicts. Returns empty list on missing/corrupt file."""
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]
    except Exception as exc:
        logger.warning("_read_csv corrupt/missing: %s: %s", path, exc)
        return []


def _read_jsonl(path: str) -> List[dict]:
    """Read JSONL file. Returns empty list on missing/corrupt file."""
    if not os.path.isfile(path):
        return []
    result = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    result.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    logger.warning("_read_jsonl: line %d corrupt: %s", line_no, exc)
    except Exception as exc:
        logger.warning("_read_jsonl corrupt/missing: %s: %s", path, exc)
    return result


_SECRET_KEYS = {
    "api_key", "token", "password", "secret", "credential",
    "auth", "bearer", "access_token", "refresh_token",
}


def _strip_secrets(data: Any) -> Any:
    """Recursively strip secret fields from a dict/list (defensive, no real secrets should be present)."""
    if isinstance(data, dict):
        return {
            k: "REDACTED" if any(s in k.lower() for s in _SECRET_KEYS) else _strip_secrets(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [_strip_secrets(item) for item in data]
    return data
