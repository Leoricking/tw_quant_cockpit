"""
gui/replay_timeframe_batch_dialog.py — ReplayTimeframeBatchDialog v1.2.5

Batch management dialog with per-item and total timing.
Cancel preserves elapsed. Default preview mode (no execute).

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
DEFAULT_PREVIEW_MODE = True
NO_AUTO_EXECUTE = True


class ReplayTimeframeBatchDialog:
    """
    Batch management dialog for multi-timeframe replay.
    Per-item and total timing with monotonic clock.
    Cancel preserves elapsed time.
    Default preview mode — blocked without --execute --allow-write.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    DEFAULT_PREVIEW_MODE = True
    NO_AUTO_EXECUTE = True

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._items: List[Dict[str, Any]] = []
        self._preview_mode: bool = True
        self._allow_write: bool = False
        self._execute: bool = False
        self._running: bool = False
        self._cancelled: bool = False
        self._start_time: Optional[float] = None
        self._elapsed_at_cancel: Optional[float] = None
        self._current_item_index: int = -1

    def set_items(self, items: List[Dict[str, Any]]) -> None:
        self._items = list(items)

    def set_execute(self, execute: bool, allow_write: bool) -> None:
        self._execute = execute
        self._allow_write = allow_write
        self._preview_mode = not (execute and allow_write)

    def start(self) -> Dict[str, Any]:
        if self._preview_mode:
            return {
                "status": "BLOCKED",
                "reason": "Preview mode. Use --execute --allow-write to run.",
                "preview_mode": True,
                "research_only": True,
            }
        self._running = True
        self._cancelled = False
        self._start_time = time.monotonic()
        self._elapsed_at_cancel = None
        self._current_item_index = 0
        return {"status": "STARTED", "item_count": len(self._items), "research_only": True}

    def cancel(self) -> Dict[str, Any]:
        """Cancel batch. Preserves elapsed time."""
        if self._running and self._start_time is not None:
            self._elapsed_at_cancel = time.monotonic() - self._start_time
        self._running = False
        self._cancelled = True
        return {
            "status": "CANCELLED",
            "elapsed_seconds": self._elapsed_at_cancel,
            "items_completed": self._current_item_index,
            "items_total": len(self._items),
            "research_only": True,
        }

    def get_total_elapsed(self) -> Optional[float]:
        if self._elapsed_at_cancel is not None:
            return self._elapsed_at_cancel
        if self._running and self._start_time is not None:
            return time.monotonic() - self._start_time
        return None

    def get_display_data(self) -> Dict[str, Any]:
        return {
            "items": self._items,
            "item_count": len(self._items),
            "preview_mode": self._preview_mode,
            "running": self._running,
            "cancelled": self._cancelled,
            "current_item_index": self._current_item_index,
            "elapsed_seconds": self.get_total_elapsed(),
            "no_auto_execute": True,
            "research_only": True,
        }

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "widget": "ReplayTimeframeBatchDialog",
            "version": "v1.2.5",
            "preview_mode": self._preview_mode,
            "no_auto_execute": True,
            "research_only": True,
        }
