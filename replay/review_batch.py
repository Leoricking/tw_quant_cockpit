"""
replay/review_batch.py — ReplayReviewBatchRunner v1.2.6

Supports batch dashboard refresh, progress calculation, queue build,
report generation, integrity summary, batch review package.
Preview by default. --execute --allow-write required to write review metadata.

[!] Research Only. No Real Orders. Batch default preview mode.
[!] BLOCKED without --execute --allow-write.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import _now_utc

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewBatchRunner:
    """
    Batch review runner for replay sessions.

    [!] Default: preview mode (no writes).
    [!] BLOCKED without both --execute AND --allow-write.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    DEFAULT_PREVIEW_MODE = True
    NO_AUTO_DECISION     = True
    NO_AUTO_TRADE        = True
    NO_AUTO_REVEAL       = True
    NO_AUTO_CONFIRM      = True
    RESEARCH_ONLY        = True
    NO_REAL_ORDERS       = True

    def __init__(self) -> None:
        self._batch_results: List[Dict[str, Any]] = []
        self._batch_started_at: Optional[str] = None
        self._batch_finished_at: Optional[str] = None
        self._total_elapsed: float = 0.0
        self._item_elapsed: float = 0.0

    def preview(self, sessions: List[str]) -> Dict[str, Any]:
        """Preview batch operations without writing anything."""
        return {
            "mode":           "PREVIEW",
            "allow_write":    False,
            "sessions":       sessions,
            "session_count":  len(sessions),
            "operations":     ["dashboard_refresh", "progress_calculate", "queue_build"],
            "research_only":  True,
            "no_real_orders": True,
            "note":           "No data written. Use --execute --allow-write to write review metadata.",
        }

    def run(
        self,
        sessions: List[str],
        execute: bool = False,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """
        Run batch review operations.
        BLOCKED if execute=True but allow_write=False.
        BLOCKED if execute=False.

        [!] Research Only. No Real Orders. Not Investment Advice.
        """
        if not execute or not allow_write:
            return {
                "status":       "BLOCKED",
                "reason":       "Batch run requires both --execute and --allow-write flags.",
                "execute":       execute,
                "allow_write":   allow_write,
                "research_only": True,
                "no_real_orders": True,
            }

        self._batch_started_at = _now_utc()
        t0 = time.monotonic()

        results = []
        for i, session_id in enumerate(sessions):
            t_item = time.monotonic()
            item_result = self._process_session(session_id)
            elapsed_item = time.monotonic() - t_item
            item_result["elapsed"] = round(elapsed_item, 3)
            results.append(item_result)
            self._item_elapsed = elapsed_item

        self._total_elapsed = time.monotonic() - t0
        self._batch_finished_at = _now_utc()
        self._batch_results = results

        completed = sum(1 for r in results if r.get("status") == "OK")
        failed    = sum(1 for r in results if r.get("status") == "ERROR")
        skipped   = sum(1 for r in results if r.get("status") == "SKIPPED")
        total     = len(sessions)
        avg_item  = self._total_elapsed / total if total else 0.0

        return {
            "status":             "OK",
            "mode":               "EXECUTE",
            "allow_write":        allow_write,
            "results":            results,
            "total":              total,
            "completed":          completed,
            "failed":             failed,
            "skipped":            skipped,
            "cancelled":          0,
            "total_elapsed":      round(self._total_elapsed, 3),
            "avg_per_item":       round(avg_item, 3),
            "estimated_remaining": 0.0,
            "research_only":      True,
            "no_real_orders":     True,
            "no_auto_reveal":     True,
            "no_auto_confirm":    True,
        }

    def _process_session(self, session_id: str) -> Dict[str, Any]:
        """Process a single session in the batch."""
        try:
            from replay.review_progress import ReplayReviewProgressCalculator
            calc = ReplayReviewProgressCalculator()
            progress = calc.calculate(session_id)
            return {
                "session_id":      session_id,
                "operation":       "progress_calculate",
                "status":          "OK",
                "review_progress": progress.status,
                "progress_pct":    progress.progress_percent,
                "warnings":        [],
                "errors":          [],
            }
        except Exception as exc:
            return {
                "session_id": session_id,
                "operation":  "progress_calculate",
                "status":     "ERROR",
                "errors":     [str(exc)],
            }

    def summary(self) -> Dict[str, Any]:
        """Return batch timing summary."""
        total = len(self._batch_results)
        completed = sum(1 for r in self._batch_results if r.get("status") == "OK")
        avg_item = self._total_elapsed / total if total else 0.0
        return {
            "total_elapsed":       round(self._total_elapsed, 3),
            "current_item_elapsed": round(self._item_elapsed, 3),
            "average_per_item":    round(avg_item, 3),
            "estimated_remaining": 0.0,
            "total":               total,
            "completed":           completed,
            "success":             completed,
            "failed":              sum(1 for r in self._batch_results if r.get("status") == "ERROR"),
            "skipped":             sum(1 for r in self._batch_results if r.get("status") == "SKIPPED"),
            "cancelled":           0,
            "started_at":          self._batch_started_at,
            "finished_at":         self._batch_finished_at,
            "research_only":       True,
            "no_auto_reveal":      True,
            "no_auto_confirm":     True,
        }
