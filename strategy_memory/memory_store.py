"""
memory_store.py — Strategy Research Memory Store v0.8.1

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import os
import csv
from typing import List, Optional
from datetime import datetime

from strategy_memory.strategy_memory_schema import (
    StrategyMemoryItem, StrategyMemoryLink, StrategyMemorySummary,
    STATUS_NEW, STATUS_ARCHIVED,
)

import logging
logger = logging.getLogger(__name__)


class StrategyMemoryStore:
    """
    Persists strategy memory items, links, and summaries as CSV files.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    _MEMORIES_FILE  = "strategy_memories.csv"
    _LINKS_FILE     = "strategy_memory_links.csv"
    _SUMMARY_FILE   = "strategy_memory_summary.csv"
    _TIMELINE_FILE  = "strategy_memory_timeline.csv"

    def __init__(self, output_dir: str = "data/backtest_results/strategy_memory"):
        self._dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    # --- Save ---

    def save_memories(self, memories: List[StrategyMemoryItem]) -> None:
        """Write memories list to CSV."""
        if not memories:
            return
        path = os.path.join(self._dir, self._MEMORIES_FILE)
        rows = [m.to_dict() for m in memories]
        _write_csv(path, rows)

    def save_links(self, links: List[StrategyMemoryLink]) -> None:
        if not links:
            return
        path = os.path.join(self._dir, self._LINKS_FILE)
        rows = [lk.to_dict() for lk in links]
        _write_csv(path, rows)

    def save_summary(self, summary: StrategyMemorySummary) -> None:
        path = os.path.join(self._dir, self._SUMMARY_FILE)
        _write_csv(path, [summary.to_dict()])

    def save_timeline(self, memories: List[StrategyMemoryItem]) -> None:
        """Save a timeline view (sorted by created_at desc, includes all fields)."""
        path = os.path.join(self._dir, self._TIMELINE_FILE)
        rows = sorted(
            [m.to_dict() for m in memories],
            key=lambda r: r.get("created_at", ""),
            reverse=True,
        )
        _write_csv(path, rows)

    # --- Load ---

    def load_memories(self) -> List[StrategyMemoryItem]:
        path = os.path.join(self._dir, self._MEMORIES_FILE)
        if not os.path.exists(path):
            return []
        rows = _read_csv(path)
        items = []
        for row in rows:
            try:
                items.append(StrategyMemoryItem.from_dict(row))
            except Exception:
                pass
        return items

    def load_links(self) -> List[StrategyMemoryLink]:
        path = os.path.join(self._dir, self._LINKS_FILE)
        if not os.path.exists(path):
            return []
        rows = _read_csv(path)
        links = []
        for row in rows:
            try:
                links.append(StrategyMemoryLink.from_dict(row))
            except Exception:
                pass
        return links

    def load_latest_summary(self) -> Optional[StrategyMemorySummary]:
        path = os.path.join(self._dir, self._SUMMARY_FILE)
        if not os.path.exists(path):
            return None
        rows = _read_csv(path)
        if not rows:
            return None
        try:
            return StrategyMemorySummary.from_dict(rows[-1])
        except Exception:
            return None

    # --- Upsert ---

    def upsert_memories(self, new_items: List[StrategyMemoryItem]) -> List[StrategyMemoryItem]:
        """
        Merge new_items into existing store.

        Deduplication key: normalized(title) + memory_type + source_module.
        - If duplicate found and existing status in (REVIEWING, VALIDATING, ACCEPTED, REJECTED):
          preserve existing status — do NOT overwrite.
        - If duplicate found and existing status is NEW: update title/summary.
        - If duplicate found: seen_count += 1, last_seen_at = now.
        - If new: insert with status=NEW.
        """
        _PROTECTED_STATUSES = {"REVIEWING", "VALIDATING", "ACCEPTED", "REJECTED"}
        existing = {_upsert_key(m): m for m in self.load_memories()}
        now = datetime.now().isoformat()
        for item in new_items:
            key = _upsert_key(item)
            if key in existing:
                ex = existing[key]
                ex.seen_count += 1
                ex.last_seen_at = now
                ex.updated_at = now
                # Only update title/summary if existing status is still NEW
                if ex.status == STATUS_NEW:
                    ex.title   = item.title
                    ex.summary = item.summary
                # Do NOT overwrite status if it has been progressed by user
                if ex.status not in _PROTECTED_STATUSES:
                    pass  # keep existing status as-is (not NEW means user changed it)
            else:
                existing[key] = item
        merged = list(existing.values())
        self.save_memories(merged)
        self.save_timeline(merged)
        return merged

    # --- Mutations ---

    def update_status(self, memory_id: str, status: str) -> bool:
        """
        Update status of a memory item. Returns True if found.

        v0.8.1: Also sets last_action_at. Validates transition (warns but doesn't block).
        ACCEPTED status always keeps accepted_is_research_only=True.
        """
        _VALID_STATUSES = {"NEW", "REVIEWING", "VALIDATING", "ACCEPTED",
                           "REJECTED", "ARCHIVED", "NEEDS_MORE_EVIDENCE"}
        if status not in _VALID_STATUSES:
            logger.warning("update_status: unknown status '%s' — proceeding anyway", status)
        memories = self.load_memories()
        found = False
        now = datetime.now().isoformat()
        for m in memories:
            if m.memory_id == memory_id:
                old_status = m.status
                m.status = status
                m.updated_at = now
                m.last_action_at = now
                # SAFETY: ACCEPTED never means trading is enabled
                if status == "ACCEPTED":
                    m.accepted_is_research_only = True
                # Log transition
                logger.info("update_status: %s %s → %s (research only)", memory_id, old_status, status)
                found = True
        if found:
            self.save_memories(memories)
            self.save_timeline(memories)
        return found

    def archive_memory(self, memory_id: str) -> bool:
        """Archive a memory item. Returns True if found."""
        memories = self.load_memories()
        found = False
        now = datetime.now().isoformat()
        for m in memories:
            if m.memory_id == memory_id:
                m.status = STATUS_ARCHIVED
                m.archived = True
                m.updated_at = now
                found = True
        if found:
            self.save_memories(memories)
            self.save_timeline(memories)
        return found

    def find_duplicates(self, memories: List[StrategyMemoryItem]) -> List[tuple]:
        """Return list of (mem_a, mem_b) pairs that appear to be duplicates."""
        seen: dict = {}
        dupes = []
        for m in memories:
            key = _upsert_key(m)
            if key in seen:
                dupes.append((seen[key], m))
            else:
                seen[key] = m
        return dupes


# --- Helpers ---

def _normalize_title(title: str) -> str:
    return title.lower().strip().replace(" ", "_")[:60]

def _upsert_key(m: StrategyMemoryItem) -> str:
    return f"{_normalize_title(m.title)}|{m.memory_type}|{m.source_module}"

def _write_csv(path: str, rows: List[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def _read_csv(path: str) -> List[dict]:
    rows = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    except Exception:
        pass
    return rows
