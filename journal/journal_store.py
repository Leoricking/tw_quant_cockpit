"""
journal/journal_store.py — PortfolioJournalStore (v0.4.6).

Stores and retrieves research-only portfolio journal entries.

Outputs:
  journal_data/journal_entries.jsonl          (gitignored — runtime)
  data/backtest_results/portfolio_journal_summary.csv (gitignored — runtime)

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT connect to broker. Does NOT write real orders.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from journal.journal_schema import (
    JournalEntry,
    ALL_ENTRY_TYPES, ALL_STATUSES, ALL_OUTCOME_LABELS, ALL_MISTAKE_TAGS,
    STATUS_REVIEWED, STATUS_CLOSED_SIMULATED, STATUS_ARCHIVED,
    OUTCOME_UNKNOWN,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_JOURNAL_ROOT = os.path.join(BASE_DIR, "journal_data")
_DEFAULT_RESULTS_DIR  = os.path.join(BASE_DIR, "data", "backtest_results")
_JOURNAL_FILENAME     = "journal_entries.jsonl"
_SUMMARY_CSV_FILENAME = "portfolio_journal_summary.csv"

_SUMMARY_CSV_FIELDS = [
    "journal_id", "created_at", "entry_type", "mode", "status",
    "symbol", "side", "timeframe", "signal_source", "outcome_label",
    "actual_return_pct", "holding_days", "mistake_tags",
]


class PortfolioJournalStore:
    """
    Persistence layer for research-only portfolio journal entries.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      IO failures never crash callers.

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        journal_root: str = _DEFAULT_JOURNAL_ROOT,
        results_dir:  str = _DEFAULT_RESULTS_DIR,
    ):
        self._root = journal_root if os.path.isabs(journal_root) else os.path.join(BASE_DIR, journal_root)
        self._results_dir = results_dir if os.path.isabs(results_dir) else os.path.join(BASE_DIR, results_dir)
        self._entries: Dict[str, JournalEntry] = {}
        self._loaded = False
        try:
            os.makedirs(self._root, exist_ok=True)
        except Exception as exc:
            logger.warning("PortfolioJournalStore: cannot create journal_root %s — %s", self._root, exc)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_entry(self, entry: JournalEntry) -> JournalEntry:
        """Add a new JournalEntry. Persists to JSONL. Never raises."""
        try:
            self._ensure_loaded()
            self._entries[entry.journal_id] = entry
            self._append_to_log(entry)
            logger.info(
                "PortfolioJournalStore: added [%s] %s %s",
                entry.entry_type, entry.journal_id, entry.symbol,
            )
        except Exception as exc:
            logger.warning("PortfolioJournalStore.add_entry: %s", exc)
        return entry

    def update_entry(self, journal_id: str, updates: dict) -> Optional[JournalEntry]:
        """Update fields on an existing entry. Returns updated entry or None."""
        try:
            self._ensure_loaded()
            entry = self._entries.get(journal_id)
            if entry is None:
                logger.warning("PortfolioJournalStore.update_entry: %s not found", journal_id)
                return None
            # Apply updates selectively (never override safety invariants)
            _LOCKED = {"journal_id", "read_only", "no_real_orders", "production_blocked"}
            for k, v in updates.items():
                if k in _LOCKED:
                    continue
                if hasattr(entry, k):
                    setattr(entry, k, v)
            entry.touch()
            self._rewrite_log()
            return entry
        except Exception as exc:
            logger.warning("PortfolioJournalStore.update_entry: %s", exc)
            return None

    def get_entry(self, journal_id: str) -> Optional[JournalEntry]:
        """Return a single entry by ID, or None."""
        self._ensure_loaded()
        return self._entries.get(journal_id)

    def list_entries(
        self,
        limit:      int           = 100,
        symbol:     Optional[str] = None,
        status:     Optional[str] = None,
        entry_type: Optional[str] = None,
    ) -> List[JournalEntry]:
        """Return entries newest-first, optionally filtered."""
        self._ensure_loaded()
        entries = sorted(
            self._entries.values(),
            key=lambda e: e.created_at,
            reverse=True,
        )
        if symbol:
            entries = [e for e in entries if e.symbol == symbol]
        if status:
            entries = [e for e in entries if e.status == status]
        if entry_type:
            entries = [e for e in entries if e.entry_type == entry_type]
        return entries[:limit]

    def delete_entry_soft(self, journal_id: str, reason: Optional[str] = None) -> bool:
        """Soft-delete: set status to ARCHIVED. Returns True if found."""
        return self.update_entry(
            journal_id, {"status": STATUS_ARCHIVED, "review_notes": f"[ARCHIVED] {reason or ''}"}
        ) is not None

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_entries(self) -> str:
        """Export summary CSV to data/backtest_results/. Returns path."""
        self._ensure_loaded()
        try:
            os.makedirs(self._results_dir, exist_ok=True)
            path = os.path.join(self._results_dir, _SUMMARY_CSV_FILENAME)
            rows = []
            for e in self._entries.values():
                row = {f: getattr(e, f, "") for f in _SUMMARY_CSV_FIELDS}
                row["mistake_tags"] = "|".join(e.mistake_tags) if e.mistake_tags else ""
                rows.append(row)
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=_SUMMARY_CSV_FIELDS, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("PortfolioJournalStore: exported summary CSV → %s", path)
            return path
        except Exception as exc:
            logger.warning("PortfolioJournalStore.export_entries: %s", exc)
            return ""

    def build_summary(self) -> dict:
        """Return a summary dict of the current journal state."""
        self._ensure_loaded()
        entries = list(self._entries.values())
        by_status: dict = {}
        by_outcome: dict = {}
        mistake_counts: dict = {}
        for e in entries:
            by_status[e.status] = by_status.get(e.status, 0) + 1
            by_outcome[e.outcome_label] = by_outcome.get(e.outcome_label, 0) + 1
            for mt in e.mistake_tags:
                mistake_counts[mt] = mistake_counts.get(mt, 0) + 1

        review_required = sum(1 for e in entries if e.needs_review())
        most_common_mistake = (
            max(mistake_counts, key=lambda k: mistake_counts[k])
            if mistake_counts else ""
        )
        latest_entry = ""
        if entries:
            latest_entry = max(e.created_at for e in entries)

        return {
            "entries_count":        len(entries),
            "by_status":            by_status,
            "by_outcome":           by_outcome,
            "mistake_counts":       mistake_counts,
            "review_required_count": review_required,
            "most_common_mistake":  most_common_mistake,
            "latest_entry_at":      latest_entry[:19] if latest_entry else "",
            "reviewed_count":       by_status.get(STATUS_REVIEWED, 0),
            "open_simulated_count": by_status.get("OPEN_SIMULATED", 0),
            "closed_simulated_count": by_status.get(STATUS_CLOSED_SIMULATED, 0),
            "journal_only":         True,
            "research_only":        True,
            "no_real_orders":       True,
            "production_blocked":   True,
        }

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _journal_path(self) -> str:
        return os.path.join(self._root, _JOURNAL_FILENAME)

    def _append_to_log(self, entry: JournalEntry) -> None:
        try:
            with open(self._journal_path(), "a", encoding="utf-8") as fh:
                fh.write(entry.to_json() + "\n")
        except Exception as exc:
            logger.debug("PortfolioJournalStore._append_to_log: %s", exc)

    def _rewrite_log(self) -> None:
        """Rewrite the JSONL log from current in-memory state."""
        try:
            with open(self._journal_path(), "w", encoding="utf-8") as fh:
                for e in self._entries.values():
                    fh.write(e.to_json() + "\n")
        except Exception as exc:
            logger.debug("PortfolioJournalStore._rewrite_log: %s", exc)

    def _ensure_loaded(self) -> None:
        """Lazy-load entries from JSONL on first access."""
        if self._loaded:
            return
        self._loaded = True
        path = self._journal_path()
        if not os.path.isfile(path):
            return
        try:
            loaded = {}
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        entry = JournalEntry.from_dict(d)
                        loaded[entry.journal_id] = entry
                    except Exception as lex:
                        logger.debug("PortfolioJournalStore: skipping bad line: %s", lex)
            self._entries = loaded
            logger.info("PortfolioJournalStore: loaded %d entries from %s", len(loaded), path)
        except Exception as exc:
            logger.warning("PortfolioJournalStore._ensure_loaded: %s", exc)
