"""
automation/task_log.py - Automation task log reader/writer (v0.3.17).

Writes to:
  logs/automation/task_runs.jsonl
  logs/automation/latest_status.json

[!] Read Only. Research Only. No Real Orders.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_LOG_DIR = os.path.join(_BASE_DIR, "logs", "automation")


class AutomationTaskLog:
    """
    Read/write task run logs for the automation scheduler.

    Parameters
    ----------
    log_dir : directory for log files (default: logs/automation/)
    """

    RUNS_FILE   = "task_runs.jsonl"
    STATUS_FILE = "latest_status.json"

    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir = log_dir or _DEFAULT_LOG_DIR

    # ------------------------------------------------------------------
    # Internal paths
    # ------------------------------------------------------------------

    @property
    def _runs_path(self) -> str:
        return os.path.join(self.log_dir, self.RUNS_FILE)

    @property
    def _status_path(self) -> str:
        return os.path.join(self.log_dir, self.STATUS_FILE)

    def _ensure_dir(self) -> None:
        os.makedirs(self.log_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # task_runs.jsonl
    # ------------------------------------------------------------------

    def append_run(self, result: dict) -> None:
        """Append a single task result dict to task_runs.jsonl."""
        self._ensure_dir()
        try:
            line = json.dumps(result, ensure_ascii=False, default=str)
            with open(self._runs_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception as exc:
            logger.error("AutomationTaskLog.append_run failed: %s", exc)

    def load_recent_runs(self, limit: int = 50) -> List[dict]:
        """
        Return the most recent `limit` task run dicts from task_runs.jsonl.
        Returns empty list if file does not exist.
        """
        if not os.path.isfile(self._runs_path):
            return []
        try:
            lines = []
            with open(self._runs_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            lines.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
            return lines[-limit:]
        except Exception as exc:
            logger.error("AutomationTaskLog.load_recent_runs failed: %s", exc)
            return []

    # ------------------------------------------------------------------
    # latest_status.json
    # ------------------------------------------------------------------

    def load_latest_status(self) -> dict:
        """
        Return the latest status dict from latest_status.json.
        Returns empty dict if file does not exist.
        """
        if not os.path.isfile(self._status_path):
            return {}
        try:
            with open(self._status_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("AutomationTaskLog.load_latest_status failed: %s", exc)
            return {}

    def write_latest_status(self, status: dict) -> None:
        """Write the given status dict to latest_status.json."""
        self._ensure_dir()
        try:
            with open(self._status_path, "w", encoding="utf-8") as f:
                json.dump(status, f, ensure_ascii=False, indent=2, default=str)
        except Exception as exc:
            logger.error("AutomationTaskLog.write_latest_status failed: %s", exc)

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------

    def summarize_runs(self, limit: int = 100) -> dict:
        """
        Return a summary dict over the most recent runs.

        Keys: total, ok, failed, warning, last_run_at, last_status,
              task_counts (dict task_name -> count)
        """
        runs = self.load_recent_runs(limit=limit)
        if not runs:
            return {
                "total": 0, "ok": 0, "failed": 0, "warning": 0,
                "last_run_at": None, "last_status": None,
                "task_counts": {},
            }

        ok      = sum(1 for r in runs if r.get("status") == "ok")
        failed  = sum(1 for r in runs if r.get("status") == "failed")
        warning = sum(1 for r in runs if r.get("status") == "warning")

        task_counts: Dict[str, int] = {}
        for r in runs:
            name = r.get("task_name", "unknown")
            task_counts[name] = task_counts.get(name, 0) + 1

        last = runs[-1]
        return {
            "total":       len(runs),
            "ok":          ok,
            "failed":      failed,
            "warning":     warning,
            "last_run_at": last.get("finished_at") or last.get("started_at"),
            "last_status": last.get("status"),
            "task_counts": task_counts,
        }

    def last_run_for_task(self, task_name: str) -> Optional[dict]:
        """Return the most recent run dict for the given task_name, or None."""
        runs = self.load_recent_runs(limit=200)
        for r in reversed(runs):
            if r.get("task_name") == task_name:
                return r
        return None
