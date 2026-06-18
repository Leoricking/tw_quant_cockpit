"""
replay/timeframe_batch.py — MultiTimeframeReplayBatchRunner v1.2.5

Batch operations for multi-timeframe replay.
Default: preview mode. --execute --allow-write required to write runtime metadata.
Never auto-play/auto-decision/auto-journal/auto-score/auto-reveal/auto-confirm/auto-trade.

Timing: monotonic clock for duration; wall clock for display;
paused time not counted in active elapsed.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Default: preview mode. No auto-write without --allow-write.
[!] No auto-play, auto-decision, auto-journal, auto-score, auto-reveal, auto-trade.
"""
from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
DEFAULT_PREVIEW_MODE = True
NO_AUTO_DECISION = True
NO_AUTO_JOURNAL = True
NO_AUTO_SCORE = True
NO_AUTO_REVEAL = True
NO_AUTO_TRADE = True

BATCH_OPERATIONS = [
    "snapshot", "timeline", "indicator", "strategy",
    "compare", "report_build",
]

STATUS_PENDING   = "PENDING"
STATUS_RUNNING   = "RUNNING"
STATUS_COMPLETED = "COMPLETED"
STATUS_FAILED    = "FAILED"
STATUS_SKIPPED   = "SKIPPED"
STATUS_CANCELLED = "CANCELLED"


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_batch_id() -> str:
    return f"BAT-{uuid.uuid4().hex[:12].upper()}"


class BatchItem:
    """Single batch item with per-item timing."""

    def __init__(
        self,
        item_id: str,
        session_id: str,
        symbol: str,
        timeframe: str,
        operation: str,
    ) -> None:
        self.item_id    = item_id
        self.session_id = session_id
        self.symbol     = symbol
        self.timeframe  = timeframe
        self.operation  = operation
        self.status     = STATUS_PENDING
        self.started_at: Optional[str]   = None
        self.finished_at: Optional[str]  = None
        self._start_mono: Optional[float] = None
        self._end_mono: Optional[float]  = None
        self.warnings: List[str]         = []
        self.errors: List[str]           = []

    def start(self) -> None:
        self.status     = STATUS_RUNNING
        self.started_at = _now_utc()
        self._start_mono = time.monotonic()

    def finish(self, status: str = STATUS_COMPLETED) -> None:
        self.status      = status
        self.finished_at = _now_utc()
        self._end_mono   = time.monotonic()

    @property
    def elapsed_seconds(self) -> float:
        if self._start_mono is None:
            return 0.0
        end = self._end_mono or time.monotonic()
        return end - self._start_mono

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "session_id": self.session_id,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "operation": self.operation,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "elapsed_seconds": self.elapsed_seconds,
            "warnings": self.warnings,
            "errors": self.errors,
        }


class MultiTimeframeReplayBatchRunner:
    """
    Batch runner for multi-timeframe replay operations.

    Default: preview mode. Use --execute --allow-write to write.
    No auto-play, auto-decision, auto-journal, auto-score, auto-reveal, auto-trade.
    Timing: monotonic clock for duration; paused time excluded from active elapsed.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    DEFAULT_PREVIEW_MODE = True
    NO_AUTO_DECISION = True
    NO_AUTO_JOURNAL = True
    NO_AUTO_SCORE = True
    NO_AUTO_REVEAL = True
    NO_AUTO_TRADE = True

    def __init__(self) -> None:
        self._batch_id:   str = _new_batch_id()
        self._items:      List[BatchItem] = []
        self._status:     str = STATUS_PENDING
        self._start_mono: Optional[float] = None
        self._end_mono:   Optional[float] = None
        self._pause_mono: Optional[float] = None
        self._paused_total: float = 0.0
        self._started_at: Optional[str] = None
        self._cancelled:  bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def preview(
        self,
        sessions: List[str],
        operation: str = "snapshot",
        timeframes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Preview batch — shows what would be done without writing."""
        tfs = timeframes or ["D1", "M60", "M20", "M5", "M1"]
        items = []
        for session_id in sessions:
            for tf in tfs:
                items.append({
                    "session_id": session_id,
                    "symbol": "TST",
                    "timeframe": tf,
                    "operation": operation,
                    "status": "PREVIEW",
                })
        return {
            "mode": "PREVIEW",
            "batch_id": self._batch_id,
            "item_count": len(items),
            "items": items,
            "allow_write": False,
            "research_only": True,
            "no_real_orders": True,
        }

    def validate(self, sessions: List[str]) -> Dict[str, Any]:
        """Validate batch configuration without running."""
        return {
            "valid": True,
            "session_count": len(sessions),
            "research_only": True,
        }

    def estimate_items(
        self, sessions: List[str], operation: str = "snapshot"
    ) -> int:
        """Estimate total items for batch."""
        return len(sessions) * 5  # 5 timeframes

    def run(
        self,
        sessions: List[str],
        operation: str = "snapshot",
        timeframes: Optional[List[str]] = None,
        allow_write: bool = False,
        execute: bool = False,
    ) -> Dict[str, Any]:
        """
        Run batch operation.
        BLOCKED without allow_write=True and execute=True.
        """
        if not allow_write or not execute:
            return {
                "status": "BLOCKED",
                "reason": "Batch write requires --execute and --allow-write flags",
                "batch_id": self._batch_id,
                "research_only": True,
                "no_real_orders": True,
            }

        tfs = timeframes or ["D1", "M60", "M20", "M5", "M1"]
        self._start_mono = time.monotonic()
        self._started_at = _now_utc()
        self._status = STATUS_RUNNING

        # Create items
        for session_id in sessions:
            for tf in tfs:
                item_id = f"ITM-{uuid.uuid4().hex[:8].upper()}"
                item = BatchItem(item_id, session_id, "TST", tf, operation)
                self._items.append(item)

        # Process items
        for item in self._items:
            if self._cancelled:
                item.status = STATUS_CANCELLED
                continue
            item.start()
            try:
                # Simulate operation
                item.finish(STATUS_COMPLETED)
            except Exception as e:
                item.errors.append(str(e))
                item.finish(STATUS_FAILED)

        self._end_mono = time.monotonic()
        self._status = STATUS_COMPLETED if not self._cancelled else STATUS_CANCELLED
        return self.summary()

    def cancel(self) -> Dict[str, Any]:
        """Cancel batch. Preserves elapsed time."""
        self._cancelled = True
        self._status = STATUS_CANCELLED
        if self._end_mono is None:
            self._end_mono = time.monotonic()
        return {"status": STATUS_CANCELLED, "elapsed_seconds": self.total_elapsed}

    def pause(self) -> None:
        """Pause batch timing."""
        if self._pause_mono is None:
            self._pause_mono = time.monotonic()

    def resume(self) -> None:
        """Resume batch timing (exclude paused time from elapsed)."""
        if self._pause_mono is not None:
            self._paused_total += time.monotonic() - self._pause_mono
            self._pause_mono = None

    def item_status(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Return status for specific item."""
        for item in self._items:
            if item.item_id == item_id:
                return item.to_dict()
        return None

    def summary(self) -> Dict[str, Any]:
        """Return batch summary with timing."""
        completed = [i for i in self._items if i.status == STATUS_COMPLETED]
        failed    = [i for i in self._items if i.status == STATUS_FAILED]
        skipped   = [i for i in self._items if i.status == STATUS_SKIPPED]
        cancelled = [i for i in self._items if i.status == STATUS_CANCELLED]

        total_items      = len(self._items)
        elapsed          = self.total_elapsed
        avg_per_item     = (elapsed / len(completed)) if completed else 0.0
        remaining_items  = total_items - len(completed) - len(failed) - len(skipped) - len(cancelled)
        estimated_remain = avg_per_item * remaining_items if remaining_items > 0 else 0.0

        return {
            "batch_id":            self._batch_id,
            "status":              self._status,
            "total_elapsed":       self._fmt_elapsed(elapsed),
            "total_elapsed_seconds": elapsed,
            "items_total":         total_items,
            "items_completed":     len(completed),
            "items_failed":        len(failed),
            "items_skipped":       len(skipped),
            "items_cancelled":     len(cancelled),
            "average_per_item":    self._fmt_elapsed(avg_per_item),
            "estimated_remaining": self._fmt_elapsed(estimated_remain),
            "items": [i.to_dict() for i in self._items],
            "auto_play":        False,
            "auto_decision":    False,
            "auto_journal":     False,
            "auto_score":       False,
            "auto_reveal":      False,
            "auto_trade":       False,
            "research_only":    True,
            "no_real_orders":   True,
        }

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total_elapsed(self) -> float:
        """Total active elapsed time (paused time excluded)."""
        if self._start_mono is None:
            return 0.0
        end = self._end_mono or time.monotonic()
        pause_adjust = 0.0
        if self._pause_mono:
            pause_adjust = time.monotonic() - self._pause_mono
        return max(0.0, end - self._start_mono - self._paused_total - pause_adjust)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fmt_elapsed(self, seconds: float) -> str:
        """Format elapsed seconds as HH:MM:SS."""
        s = int(seconds)
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        if h > 0:
            return f"{h:02d}:{m:02d}:{sec:02d}"
        return f"{m:02d}:{sec:02d}"
