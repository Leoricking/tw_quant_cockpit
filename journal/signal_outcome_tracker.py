"""
journal/signal_outcome_tracker.py — SignalOutcomeTracker (v0.4.6).

Tracks signal vs actual outcome for research review.
Reads journal entries — does NOT connect to broker or execute trades.

Output: data/backtest_results/signal_outcome_summary.csv  (gitignored)

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from typing import Dict, List, Optional

from journal.journal_schema import JournalEntry, OUTCOME_UNKNOWN

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_RESULTS_DIR = os.path.join(BASE_DIR, "data", "backtest_results")
_OUTCOME_CSV = "signal_outcome_summary.csv"

_OUTCOME_CSV_FIELDS = [
    "signal_id", "journal_id", "symbol", "signal_source",
    "planned_entry", "actual_entry", "actual_exit",
    "return_pct", "mfe", "mae", "holding_days",
    "outcome_label", "process_quality", "review_required",
]


class SignalOutcomeTracker:
    """
    Tracks signal vs actual outcome for research review.

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        journal_store=None,
        results_dir: str = _DEFAULT_RESULTS_DIR,
    ):
        self._store = journal_store
        self._results_dir = (
            results_dir if os.path.isabs(results_dir)
            else os.path.join(BASE_DIR, results_dir)
        )
        # signal_id -> journal_id mapping
        self._links: Dict[str, str] = {}

    def _get_store(self):
        if self._store is not None:
            return self._store
        from journal.journal_store import PortfolioJournalStore
        self._store = PortfolioJournalStore()
        return self._store

    # ------------------------------------------------------------------
    # Signal → journal linking
    # ------------------------------------------------------------------

    def link_signal_to_journal(self, signal_id: str, journal_id: str) -> dict:
        """Link a signal ID to a journal entry ID. Returns result dict."""
        try:
            store = self._get_store()
            entry = store.get_entry(journal_id)
            if entry is None:
                return {"success": False, "error": f"Journal entry {journal_id} not found"}
            # Update the entry with signal_id
            store.update_entry(journal_id, {"signal_id": signal_id})
            self._links[signal_id] = journal_id
            return {"success": True, "signal_id": signal_id, "journal_id": journal_id}
        except Exception as exc:
            logger.warning("SignalOutcomeTracker.link_signal_to_journal: %s", exc)
            return {"success": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Outcome evaluation
    # ------------------------------------------------------------------

    def evaluate_outcome(
        self,
        journal_entry: JournalEntry,
        price_df=None,
    ) -> dict:
        """
        Evaluate outcome for a journal entry.
        price_df (optional): DataFrame with OHLCV data for MFE/MAE calculation.
        Returns outcome dict.
        """
        try:
            result = {
                "journal_id":     journal_entry.journal_id,
                "symbol":         journal_entry.symbol,
                "signal_id":      journal_entry.signal_id,
                "signal_source":  journal_entry.signal_source,
                "planned_entry":  journal_entry.planned_entry_price,
                "actual_entry":   journal_entry.actual_entry_price,
                "actual_exit":    journal_entry.actual_exit_price,
                "return_pct":     journal_entry.actual_return_pct,
                "mfe":            journal_entry.max_favorable_excursion,
                "mae":            journal_entry.max_adverse_excursion,
                "holding_days":   journal_entry.holding_days,
                "outcome_label":  journal_entry.outcome_label,
                "mistake_tags":   journal_entry.mistake_tags,
                "review_required": journal_entry.needs_review(),
                "process_quality": self._assess_process_quality(journal_entry),
            }

            # Basic return calculation if prices are available but not set
            if (
                result["return_pct"] is None
                and result["actual_entry"] is not None
                and result["actual_exit"] is not None
                and result["actual_entry"] != 0
            ):
                side = journal_entry.side.lower() if journal_entry.side else "long"
                if side == "short":
                    result["return_pct"] = (
                        (result["actual_entry"] - result["actual_exit"])
                        / result["actual_entry"] * 100
                    )
                else:
                    result["return_pct"] = (
                        (result["actual_exit"] - result["actual_entry"])
                        / result["actual_entry"] * 100
                    )

            return result
        except Exception as exc:
            logger.warning("SignalOutcomeTracker.evaluate_outcome: %s", exc)
            return {"journal_id": getattr(journal_entry, "journal_id", ""), "error": str(exc)}

    def _assess_process_quality(self, entry: JournalEntry) -> str:
        """
        Simple heuristic process quality assessment.
        GOOD / PARTIAL / POOR based on plan completeness.
        """
        score = 0
        if entry.thesis:           score += 2
        if entry.reason:           score += 1
        if entry.planned_entry_price is not None: score += 1
        if entry.planned_stop_loss is not None:   score += 2
        if entry.invalidation_condition:          score += 1
        if entry.mistake_tags:                    score -= 1  # mistakes reduce quality
        if score >= 5:  return "GOOD"
        if score >= 2:  return "PARTIAL"
        return "POOR"

    # ------------------------------------------------------------------
    # Build summary
    # ------------------------------------------------------------------

    def build_signal_outcome_summary(self) -> dict:
        """Build signal outcome summary across all journal entries."""
        try:
            store = self._get_store()
            entries = store.list_entries(limit=1000)
            outcomes = [self.evaluate_outcome(e) for e in entries if e.signal_id]

            if not outcomes:
                return {
                    "total": 0,
                    "wins": 0, "losses": 0, "false_signals": 0,
                    "review_required": 0,
                    "avg_return_pct": None,
                    "avg_mfe": None, "avg_mae": None,
                    "journal_only": True, "no_real_orders": True,
                }

            wins   = sum(1 for o in outcomes if o.get("outcome_label") == "WIN")
            losses = sum(1 for o in outcomes if o.get("outcome_label") == "LOSS")
            false  = sum(1 for o in outcomes if o.get("outcome_label") == "FALSE_SIGNAL")
            review = sum(1 for o in outcomes if o.get("review_required"))
            returns = [o["return_pct"] for o in outcomes if o.get("return_pct") is not None]
            mfes   = [o["mfe"] for o in outcomes if o.get("mfe") is not None]
            maes   = [o["mae"] for o in outcomes if o.get("mae") is not None]

            return {
                "total":          len(outcomes),
                "wins":           wins,
                "losses":         losses,
                "false_signals":  false,
                "win_rate":       wins / len(outcomes) if outcomes else 0.0,
                "review_required": review,
                "avg_return_pct": sum(returns) / len(returns) if returns else None,
                "avg_mfe":        sum(mfes) / len(mfes) if mfes else None,
                "avg_mae":        sum(maes) / len(maes) if maes else None,
                "outcomes":       outcomes,
                "journal_only":   True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.warning("SignalOutcomeTracker.build_signal_outcome_summary: %s", exc)
            return {"error": str(exc), "total": 0, "no_real_orders": True}

    def load_signal_quality_results(self) -> dict:
        """Load latest signal quality results from data/backtest_results/. Read-only."""
        try:
            path = os.path.join(self._results_dir, "signal_quality_summary.json")
            if not os.path.isfile(path):
                return {}
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            logger.warning("SignalOutcomeTracker.load_signal_quality_results: %s", exc)
            return {}

    def export_summary_csv(self) -> str:
        """Export signal outcome summary to CSV. Returns path."""
        try:
            summary = self.build_signal_outcome_summary()
            outcomes = summary.get("outcomes", [])
            os.makedirs(self._results_dir, exist_ok=True)
            path = os.path.join(self._results_dir, _OUTCOME_CSV)
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=_OUTCOME_CSV_FIELDS, extrasaction="ignore")
                writer.writeheader()
                for o in outcomes:
                    writer.writerow({f: o.get(f, "") for f in _OUTCOME_CSV_FIELDS})
            return path
        except Exception as exc:
            logger.warning("SignalOutcomeTracker.export_summary_csv: %s", exc)
            return ""
