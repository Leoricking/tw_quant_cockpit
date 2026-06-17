"""
replay/replay_timing.py — Operation timing for replay batch operations v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
Uses monotonic clock for duration, wall clock for display.
Elapsed is always recorded even for FAILED or CANCELLED operations.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class ReplayOperationTiming:
    """Timing data for a replay batch operation."""
    operation_id: str
    operation_name: str
    started_at: str
    finished_at: Optional[str]
    elapsed_seconds: float
    elapsed_display: str  # format: 00:00:08, 00:12:35, 02:15:08, 1d 03:12:44
    item_count: int
    completed_count: int
    failed_count: int
    average_item_seconds: Optional[float]
    estimated_remaining_seconds: Optional[float]
    status: str  # RUNNING, COMPLETED, FAILED, CANCELLED


class ReplayOperationTimer:
    """
    Uses monotonic clock for duration measurement.
    Uses wall clock for display timestamps.
    Elapsed is always recorded even for FAILED or CANCELLED operations.
    """

    def __init__(self):
        self._operation_id: str = ""
        self._operation_name: str = ""
        self._started_at_wall: Optional[str] = None
        self._started_mono: Optional[float] = None
        self._finished_at_wall: Optional[str] = None
        self._finished_mono: Optional[float] = None
        self._item_count: int = 0
        self._completed_count: int = 0
        self._failed_count: int = 0
        self._item_timings: List[Dict[str, Any]] = []
        self._status: str = "RUNNING"

    def start(self, operation_name: str, item_count: int = 0) -> "ReplayOperationTimer":
        self._operation_id = f"OPR-{uuid.uuid4().hex[:12].upper()}"
        self._operation_name = operation_name
        self._started_at_wall = datetime.now(timezone.utc).isoformat()
        self._started_mono = time.monotonic()
        self._finished_at_wall = None
        self._finished_mono = None
        self._item_count = item_count
        self._completed_count = 0
        self._failed_count = 0
        self._item_timings = []
        self._status = "RUNNING"
        return self

    def mark_item_started(self, item_id: str) -> None:
        self._item_timings.append({
            "item_id": item_id,
            "started_mono": time.monotonic(),
            "finished_mono": None,
            "status": "RUNNING",
        })

    def mark_item_finished(self, item_id: str, status: str) -> None:
        for item in self._item_timings:
            if item["item_id"] == item_id and item["finished_mono"] is None:
                item["finished_mono"] = time.monotonic()
                item["status"] = status
                if status == "COMPLETED":
                    self._completed_count += 1
                elif status == "FAILED":
                    self._failed_count += 1
                break

    def elapsed_seconds(self) -> float:
        """Uses monotonic clock."""
        if self._started_mono is None:
            return 0.0
        if self._finished_mono is not None:
            return self._finished_mono - self._started_mono
        return time.monotonic() - self._started_mono

    def elapsed_display(self) -> str:
        """Format: 00:00:08, 00:12:35, 02:15:08, 1d 03:12:44"""
        total = int(self.elapsed_seconds())
        days = total // 86400
        hours = (total % 86400) // 3600
        mins = (total % 3600) // 60
        secs = total % 60
        if days > 0:
            return f"{days}d {hours:02d}:{mins:02d}:{secs:02d}"
        return f"{hours:02d}:{mins:02d}:{secs:02d}"

    def average_item_seconds(self) -> Optional[float]:
        finished = [
            t for t in self._item_timings
            if t.get("finished_mono") is not None and t.get("started_mono") is not None
        ]
        if not finished:
            return None
        total_time = sum(t["finished_mono"] - t["started_mono"] for t in finished)
        return total_time / len(finished)

    def estimated_remaining_seconds(self) -> Optional[float]:
        avg = self.average_item_seconds()
        if avg is None:
            return None
        remaining_items = self._item_count - self._completed_count - self._failed_count
        if remaining_items <= 0:
            return 0.0
        return avg * remaining_items

    def finish(self, status: str) -> "ReplayOperationTimer":
        """Records finished_at even if status is FAILED or CANCELLED."""
        self._finished_mono = time.monotonic()
        self._finished_at_wall = datetime.now(timezone.utc).isoformat()
        self._status = status
        return self

    def summary(self) -> ReplayOperationTiming:
        """Returns ReplayOperationTiming with all fields."""
        elapsed = self.elapsed_seconds()
        return ReplayOperationTiming(
            operation_id=self._operation_id,
            operation_name=self._operation_name,
            started_at=self._started_at_wall or "",
            finished_at=self._finished_at_wall,
            elapsed_seconds=elapsed,
            elapsed_display=self.elapsed_display(),
            item_count=self._item_count,
            completed_count=self._completed_count,
            failed_count=self._failed_count,
            average_item_seconds=self.average_item_seconds(),
            estimated_remaining_seconds=self.estimated_remaining_seconds(),
            status=self._status,
        )

    def print_summary(self) -> None:
        """Print timing summary to stdout."""
        t = self.summary()
        print(f"  Elapsed Time  : {t.elapsed_display}")
        print(f"  Items         : {t.item_count}")
        print(f"  Completed     : {t.completed_count}")
        print(f"  Failed        : {t.failed_count}")
        print(f"  Status        : {t.status}")
        if t.average_item_seconds is not None:
            print(f"  Avg/Item      : {t.average_item_seconds:.2f}s")
        if t.estimated_remaining_seconds is not None:
            print(f"  Est Remaining : {t.estimated_remaining_seconds:.1f}s")
