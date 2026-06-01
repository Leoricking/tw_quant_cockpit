"""
gui/portfolio_journal_adapter.py — PortfolioJournalAdapter (v0.4.6).

GUI bridge between PortfolioJournalPanel and the journal package.
All operations are import-safe and never raise — return dicts or lists.

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT connect to broker. Does NOT submit orders.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_JOURNAL_ROOT = os.path.join(BASE_DIR, "journal_data")
_DEFAULT_REPORT_DIR   = os.path.join(BASE_DIR, "reports")


class PortfolioJournalAdapter:
    """
    GUI adapter for the Portfolio Journal.

    All methods return dicts or lists — never raise (GUI-safe).

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        journal_root: str = _DEFAULT_JOURNAL_ROOT,
        report_dir:   str = _DEFAULT_REPORT_DIR,
        mode:         str = "real",
    ):
        self._journal_root = (
            journal_root if os.path.isabs(journal_root)
            else os.path.join(BASE_DIR, journal_root)
        )
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(BASE_DIR, report_dir)
        )
        self.mode = mode

    # ------------------------------------------------------------------
    # Lazy helpers
    # ------------------------------------------------------------------

    def _get_store(self):
        from journal.journal_store import PortfolioJournalStore
        return PortfolioJournalStore(journal_root=self._journal_root)

    def _get_analytics(self):
        from journal.journal_analytics import JournalAnalytics
        return JournalAnalytics(store=self._get_store())

    # ------------------------------------------------------------------
    # Add entry
    # ------------------------------------------------------------------

    def add_entry(self, payload: dict) -> dict:
        """
        Create a new research journal entry from a payload dict.
        Returns dict with status, journal_id, entry dict.
        """
        try:
            from journal.journal_schema import (
                JournalEntry, ALL_ENTRY_TYPES, ENTRY_MANUAL_NOTE,
                STATUS_PLANNED, ALL_MISTAKE_TAGS,
            )
            # Validate entry_type
            entry_type = payload.get("entry_type", ENTRY_MANUAL_NOTE)
            if entry_type not in ALL_ENTRY_TYPES:
                entry_type = ENTRY_MANUAL_NOTE

            # Validate mistake_tags
            raw_tags = payload.get("mistake_tags", [])
            if isinstance(raw_tags, str):
                raw_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
            mistake_tags = [t for t in raw_tags if t in ALL_MISTAKE_TAGS]

            entry = JournalEntry(
                entry_type=entry_type,
                mode=self.mode,
                status=payload.get("status", STATUS_PLANNED),
                symbol=payload.get("symbol", ""),
                name=payload.get("name", ""),
                side=payload.get("side", ""),
                timeframe=payload.get("timeframe", ""),
                strategy_tags=payload.get("strategy_tags", []),
                signal_source=payload.get("signal_source", ""),
                signal_id=payload.get("signal_id", ""),
                experiment_id=payload.get("experiment_id", ""),
                replay_session_id=payload.get("replay_session_id", ""),
                portfolio_scenario=payload.get("portfolio_scenario", ""),
                planned_entry_price=payload.get("planned_entry_price"),
                planned_exit_price=payload.get("planned_exit_price"),
                planned_stop_loss=payload.get("planned_stop_loss"),
                planned_take_profit=payload.get("planned_take_profit"),
                reason=payload.get("reason", ""),
                thesis=payload.get("thesis", ""),
                invalidation_condition=payload.get("invalidation_condition", ""),
                mistake_tags=mistake_tags,
                confidence_before=payload.get("confidence_before"),
            )
            store = self._get_store()
            store.add_entry(entry)
            return {
                "status":     "OK",
                "journal_id": entry.journal_id,
                "entry":      entry.to_dict(),
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.add_entry: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # List / get entries
    # ------------------------------------------------------------------

    def list_entries(
        self,
        limit:      int           = 100,
        symbol:     Optional[str] = None,
        status:     Optional[str] = None,
        entry_type: Optional[str] = None,
    ) -> List[dict]:
        """Return list of journal entry dicts."""
        try:
            store   = self._get_store()
            entries = store.list_entries(
                limit=limit, symbol=symbol, status=status, entry_type=entry_type,
            )
            return [e.to_dict() for e in entries]
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.list_entries: %s", exc)
            return []

    def get_entry(self, journal_id: str) -> dict:
        """Return a single entry dict, or empty dict if not found."""
        try:
            store = self._get_store()
            entry = store.get_entry(journal_id)
            return entry.to_dict() if entry else {}
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.get_entry: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Update / review
    # ------------------------------------------------------------------

    def update_review(self, journal_id: str, payload: dict) -> dict:
        """
        Update review fields (outcome_label, mistake_tags, review_notes,
        confidence_after, actual_entry_price, actual_exit_price, actual_return_pct).
        Returns dict with status.
        """
        try:
            from journal.journal_schema import (
                ALL_OUTCOME_LABELS, ALL_MISTAKE_TAGS, OUTCOME_UNKNOWN,
                STATUS_REVIEWED,
            )
            updates: dict = {}
            if "outcome_label" in payload:
                ol = payload["outcome_label"]
                updates["outcome_label"] = ol if ol in ALL_OUTCOME_LABELS else OUTCOME_UNKNOWN

            if "mistake_tags" in payload:
                raw = payload["mistake_tags"]
                if isinstance(raw, str):
                    raw = [t.strip() for t in raw.split(",") if t.strip()]
                updates["mistake_tags"] = [t for t in raw if t in ALL_MISTAKE_TAGS]

            for field in ("review_notes", "confidence_after",
                          "actual_entry_price", "actual_exit_price",
                          "actual_return_pct", "max_favorable_excursion",
                          "max_adverse_excursion", "holding_days"):
                if field in payload:
                    updates[field] = payload[field]

            # Auto-set status to REVIEWED if outcome_label is set and not UNKNOWN
            if updates.get("outcome_label") and updates["outcome_label"] != OUTCOME_UNKNOWN:
                updates["status"] = STATUS_REVIEWED

            store   = self._get_store()
            updated = store.update_entry(journal_id, updates)
            if updated:
                return {"status": "OK", "journal_id": journal_id, "entry": updated.to_dict()}
            return {"status": "NOT_FOUND", "journal_id": journal_id}
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.update_review: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    def link_replay_session(self, journal_id: str, replay_session_id: str) -> dict:
        """Link a replay session to a journal entry."""
        try:
            store   = self._get_store()
            updated = store.update_entry(journal_id, {"replay_session_id": replay_session_id})
            if updated:
                return {"status": "OK", "journal_id": journal_id,
                        "replay_session_id": replay_session_id}
            return {"status": "NOT_FOUND", "journal_id": journal_id}
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.link_replay_session: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Summary / analytics
    # ------------------------------------------------------------------

    def build_summary(self) -> dict:
        """Return journal store summary dict."""
        try:
            return self._get_store().build_summary()
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.build_summary: %s", exc)
            return {}

    def run_analytics(self) -> dict:
        """Run journal analytics. Returns analytics dict."""
        try:
            return self._get_analytics().run()
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.run_analytics: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def generate_report(self, mode: Optional[str] = None, dry_run: bool = False) -> dict:
        """Generate Portfolio Journal Markdown report. Returns dict with path."""
        try:
            from reports.portfolio_journal_report import PortfolioJournalReport
            from journal.signal_outcome_tracker import SignalOutcomeTracker
            from journal.replay_training_notes import ReplayTrainingNotes

            store    = self._get_store()
            entries  = store.list_entries(limit=1000)
            summary  = store.build_summary()
            analytics = self._get_analytics().run()

            tracker = SignalOutcomeTracker(journal_store=store)
            signal_outcomes = tracker.build_signal_outcome_summary()

            replay_notes = ReplayTrainingNotes(journal_store=store)
            replay_summary = replay_notes.summarize_replay_notes()

            reporter = PortfolioJournalReport(report_dir=self._report_dir)
            path = reporter.generate(
                entries=entries,
                summary=summary,
                signal_outcomes=signal_outcomes,
                replay_summary=replay_summary,
                analytics=analytics,
                mode=mode or self.mode,
                dry_run=dry_run,
            )
            return {"status": "OK", "report_path": path, "dry_run": dry_run}
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.generate_report: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Latest report path
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """Return path to latest Portfolio Journal report, or None."""
        try:
            pattern = os.path.join(self._report_dir, "portfolio_journal_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_summary_csv(self) -> dict:
        """Export journal summary CSV. Returns dict with status and path."""
        try:
            path = self._get_store().export_entries()
            return {"status": "OK", "path": path}
        except Exception as exc:
            logger.warning("PortfolioJournalAdapter.export_summary_csv: %s", exc)
            return {"status": "ERROR", "error": str(exc)}
