"""
paper_trading/strategy/journal_v162.py — Strategy journal for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import json
import logging
import os
import threading
from typing import Any, Dict, List, Optional

from paper_trading.strategy.enums_v162 import JournalEventType
from paper_trading.strategy.models_v162 import JournalEntry, _new_id, _now_iso

logger = logging.getLogger(__name__)


class StrategyJournal:
    """
    Append-only journal for paper strategy events.

    Records all significant events in the strategy lifecycle:
    signals received, decisions made, proposals created, errors, etc.

    Thread-safe. Optionally persists to a JSONL file.
    [!] Research-only audit log. Not a trade ledger.
    """

    def __init__(
        self,
        strategy_id: str,
        persist_path: Optional[str] = None,
    ) -> None:
        self.strategy_id = strategy_id
        self.persist_path = persist_path
        self._lock = threading.Lock()
        self._entries: List[JournalEntry] = []
        self._event_counts: Dict[str, int] = {}

        if persist_path:
            os.makedirs(os.path.dirname(os.path.abspath(persist_path)), exist_ok=True)

    def record(
        self,
        event_type: JournalEventType,
        summary: str,
        detail: Optional[Dict[str, Any]] = None,
        related_ids: Optional[List[str]] = None,
    ) -> JournalEntry:
        """Append a new journal entry. Returns the entry."""
        entry = JournalEntry(
            strategy_id=self.strategy_id,
            event_type=event_type.value,
            summary=summary,
            detail=detail or {},
            related_ids=related_ids or [],
        )
        with self._lock:
            self._entries.append(entry)
            key = event_type.value
            self._event_counts[key] = self._event_counts.get(key, 0) + 1

        if self.persist_path:
            self._append_to_file(entry)

        logger.debug(
            "[v1.6.2][journal] %s %s: %s",
            self.strategy_id[:8], event_type.value, summary[:80]
        )
        return entry

    def _append_to_file(self, entry: JournalEntry) -> None:
        try:
            record = {
                "entry_id": entry.entry_id,
                "strategy_id": entry.strategy_id,
                "event_type": entry.event_type,
                "timestamp": entry.timestamp,
                "summary": entry.summary,
                "detail": entry.detail,
                "related_ids": entry.related_ids,
            }
            with open(self.persist_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError as exc:
            logger.warning("[v1.6.2][journal] Persist error: %s", exc)

    def entries(
        self,
        event_type: Optional[JournalEventType] = None,
        limit: int = 0,
    ) -> List[JournalEntry]:
        with self._lock:
            result = list(self._entries)
        if event_type is not None:
            result = [e for e in result if e.event_type == event_type.value]
        if limit > 0:
            result = result[-limit:]
        return result

    def count(self, event_type: Optional[JournalEventType] = None) -> int:
        with self._lock:
            if event_type is None:
                return len(self._entries)
            return self._event_counts.get(event_type.value, 0)

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "strategy_id": self.strategy_id,
                "total_entries": len(self._entries),
                "event_counts": dict(self._event_counts),
                "persist_path": self.persist_path,
                "paper_only": True,
                "research_only": True,
            }

    def tail(self, n: int = 10) -> List[Dict[str, Any]]:
        """Return the last n entries as dicts."""
        with self._lock:
            recent = self._entries[-n:]
        return [
            {
                "entry_id": e.entry_id,
                "event_type": e.event_type,
                "timestamp": e.timestamp,
                "summary": e.summary,
            }
            for e in recent
        ]
