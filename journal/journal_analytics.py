"""
journal/journal_analytics.py — JournalAnalytics (v0.4.6).

Statistical analysis of portfolio journal entries.
Read-only — does NOT modify entries, strategies, or weights.

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from collections import Counter
from typing import Dict, List, Optional

from journal.journal_schema import (
    JournalEntry,
    OUTCOME_WIN, OUTCOME_LOSS, OUTCOME_FALSE_SIGNAL,
    OUTCOME_GOOD_PROCESS_BAD_OUTCOME, OUTCOME_BAD_PROCESS_GOOD_OUTCOME,
    STATUS_REVIEWED, STATUS_CLOSED_SIMULATED,
)

logger = logging.getLogger(__name__)


class JournalAnalytics:
    """
    Statistical analytics over portfolio journal entries.

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self, store=None):
        self._store = store

    def _get_store(self):
        if self._store is not None:
            return self._store
        from journal.journal_store import PortfolioJournalStore
        self._store = PortfolioJournalStore()
        return self._store

    def _all_entries(self, limit: int = 1000) -> List[JournalEntry]:
        return self._get_store().list_entries(limit=limit)

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run all analytics. Returns comprehensive summary dict."""
        try:
            entries = self._all_entries()
            return {
                "total_entries":        len(entries),
                "by_symbol":            self.summarize_by_symbol(entries),
                "by_strategy":          self.summarize_by_strategy(entries),
                "by_mistake_tag":       self.summarize_by_mistake_tag(entries),
                "by_outcome":           self.summarize_by_outcome(entries),
                "process_quality":      self.summarize_process_quality(entries),
                "win_rate":             self._win_rate(entries),
                "avg_return":           self._avg_return(entries),
                "avg_mfe":              self._avg_field(entries, "max_favorable_excursion"),
                "avg_mae":              self._avg_field(entries, "max_adverse_excursion"),
                "most_common_mistakes": self._most_common_mistakes(entries),
                "best_process_tags":    self._best_process_tags(entries),
                "worst_process_tags":   self._worst_process_tags(entries),
                "review_required_count": sum(1 for e in entries if e.needs_review()),
                "journal_only":         True,
                "research_only":        True,
                "no_real_orders":       True,
            }
        except Exception as exc:
            logger.warning("JournalAnalytics.run: %s", exc)
            return {"error": str(exc), "no_real_orders": True}

    # ------------------------------------------------------------------
    # Dimension breakdowns
    # ------------------------------------------------------------------

    def summarize_by_symbol(self, entries: Optional[List[JournalEntry]] = None) -> List[dict]:
        """Win rate and avg return by symbol."""
        if entries is None:
            entries = self._all_entries()
        by_sym: Dict[str, List[JournalEntry]] = {}
        for e in entries:
            if e.symbol:
                by_sym.setdefault(e.symbol, []).append(e)
        result = []
        for sym, es in sorted(by_sym.items()):
            result.append({
                "symbol":     sym,
                "count":      len(es),
                "win_rate":   self._win_rate(es),
                "avg_return": self._avg_return(es),
            })
        return sorted(result, key=lambda x: -x["count"])

    def summarize_by_strategy(self, entries: Optional[List[JournalEntry]] = None) -> List[dict]:
        """Win rate by strategy_tags."""
        if entries is None:
            entries = self._all_entries()
        by_tag: Dict[str, List[JournalEntry]] = {}
        for e in entries:
            for tag in (e.strategy_tags or []):
                by_tag.setdefault(tag, []).append(e)
        result = []
        for tag, es in sorted(by_tag.items()):
            result.append({
                "strategy_tag": tag,
                "count":        len(es),
                "win_rate":     self._win_rate(es),
                "avg_return":   self._avg_return(es),
            })
        return sorted(result, key=lambda x: -x["count"])

    def summarize_by_mistake_tag(self, entries: Optional[List[JournalEntry]] = None) -> List[dict]:
        """Count and win rate for entries with each mistake tag."""
        if entries is None:
            entries = self._all_entries()
        by_tag: Dict[str, List[JournalEntry]] = {}
        for e in entries:
            for mt in (e.mistake_tags or []):
                by_tag.setdefault(mt, []).append(e)
        result = []
        for tag, es in sorted(by_tag.items(), key=lambda x: -len(x[1])):
            result.append({
                "mistake_tag": tag,
                "count":       len(es),
                "win_rate":    self._win_rate(es),
                "avg_return":  self._avg_return(es),
            })
        return result

    def summarize_by_outcome(self, entries: Optional[List[JournalEntry]] = None) -> dict:
        """Distribution of outcome labels."""
        if entries is None:
            entries = self._all_entries()
        counts = Counter(e.outcome_label for e in entries)
        return dict(counts.most_common())

    def summarize_process_quality(self, entries: Optional[List[JournalEntry]] = None) -> dict:
        """Process quality metrics."""
        if entries is None:
            entries = self._all_entries()
        has_thesis   = sum(1 for e in entries if e.thesis)
        has_stop     = sum(1 for e in entries if e.planned_stop_loss is not None)
        has_inv_cond = sum(1 for e in entries if e.invalidation_condition)
        has_review   = sum(1 for e in entries if e.review_notes)
        n = len(entries) or 1
        return {
            "total":                len(entries),
            "with_thesis":          has_thesis,
            "with_stop_loss":       has_stop,
            "with_invalidation":    has_inv_cond,
            "with_review_notes":    has_review,
            "thesis_pct":           round(has_thesis / n * 100, 1),
            "stop_loss_pct":        round(has_stop / n * 100, 1),
            "review_completion_pct": round(has_review / n * 100, 1),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _win_rate(self, entries: List[JournalEntry]) -> Optional[float]:
        reviewed = [e for e in entries if e.outcome_label in (OUTCOME_WIN, OUTCOME_LOSS)]
        if not reviewed:
            return None
        wins = sum(1 for e in reviewed if e.outcome_label == OUTCOME_WIN)
        return round(wins / len(reviewed), 3)

    def _avg_return(self, entries: List[JournalEntry]) -> Optional[float]:
        returns = [e.actual_return_pct for e in entries if e.actual_return_pct is not None]
        if not returns:
            return None
        return round(sum(returns) / len(returns), 3)

    def _avg_field(self, entries: List[JournalEntry], field: str) -> Optional[float]:
        vals = [getattr(e, field) for e in entries if getattr(e, field, None) is not None]
        if not vals:
            return None
        return round(sum(vals) / len(vals), 3)

    def _most_common_mistakes(self, entries: List[JournalEntry], top: int = 5) -> List[str]:
        all_tags = [t for e in entries for t in e.mistake_tags]
        return [t for t, _ in Counter(all_tags).most_common(top)]

    def _best_process_tags(self, entries: List[JournalEntry]) -> List[str]:
        """Strategy tags associated with WIN outcomes."""
        wins = [e for e in entries if e.outcome_label == OUTCOME_WIN]
        all_tags = [t for e in wins for t in e.strategy_tags]
        return [t for t, _ in Counter(all_tags).most_common(5)]

    def _worst_process_tags(self, entries: List[JournalEntry]) -> List[str]:
        """Strategy tags associated with LOSS + mistake entries."""
        bad = [
            e for e in entries
            if e.outcome_label in (OUTCOME_LOSS, OUTCOME_FALSE_SIGNAL,
                                   OUTCOME_BAD_PROCESS_GOOD_OUTCOME)
        ]
        all_tags = [t for e in bad for t in e.strategy_tags]
        return [t for t, _ in Counter(all_tags).most_common(5)]

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard integration
    # ------------------------------------------------------------------

    def build_review_summary(self) -> dict:
        """
        Build a compact review summary for the Research Review Dashboard.

        Returns dict with top_mistakes, review_required, process_quality.
        Does NOT modify any entries, strategies, or weights.

        [!] Review Only. Research Only. No Real Orders.
        """
        try:
            entries = self._all_entries()
            by_mistake = self.summarize_by_mistake_tag(entries)
            top_mistake = by_mistake[0]["mistake_tag"] if by_mistake else ""
            review_req = sum(1 for e in entries if e.needs_review())
            open_sim = sum(
                1 for e in entries
                if getattr(e, "status", "") not in (STATUS_REVIEWED, STATUS_CLOSED_SIMULATED)
            )
            return {
                "total_entries":       len(entries),
                "review_required":     review_req,
                "top_mistakes":        by_mistake[:5],
                "most_common_mistake": top_mistake,
                "process_quality":     self.summarize_process_quality(entries),
                "open_simulated":      open_sim,
                "read_only":           True,
                "no_real_orders":      True,
                "production_blocked":  True,
            }
        except Exception as exc:
            logger.warning("JournalAnalytics.build_review_summary: %s", exc)
            return {
                "total_entries": 0, "review_required": 0,
                "top_mistakes": [], "most_common_mistake": "",
                "process_quality": [], "open_simulated": 0,
                "no_real_orders": True,
            }

    # ------------------------------------------------------------------
    # v0.4.8 Research Assistant / Coach integration
    # ------------------------------------------------------------------

    def coach_summary(self) -> dict:
        """
        Return a summary for the Research Assistant / Coach.

        Returns top_mistakes, process_focus, review_backlog.
        Does NOT modify entries, strategies, or weights.

        [!] Coaching Only. Research Only. No Real Orders.
        """
        try:
            entries = self._all_entries()
            by_mistake = self.summarize_by_mistake_tag(entries)
            top_mistakes = [m["mistake_tag"] for m in by_mistake[:5]]
            most_common  = top_mistakes[0] if top_mistakes else ""
            review_backlog = sum(1 for e in entries if e.needs_review())
            process = self.summarize_process_quality(entries)
            process_focus = ""
            if isinstance(process, dict):
                with_stop = process.get("with_stop_loss_pct", 0.0)
                with_thesis = process.get("with_thesis_pct", 0.0)
                if with_stop < 0.5:
                    process_focus = "Improve stop-loss discipline"
                elif with_thesis < 0.5:
                    process_focus = "Document thesis before entry"
            return {
                "top_mistakes":    top_mistakes,
                "most_common_mistake": most_common,
                "review_backlog":  review_backlog,
                "process_focus":   process_focus,
                "total_entries":   len(entries),
                "read_only":       True,
                "no_real_orders":  True,
                "coaching_only":   True,
            }
        except Exception as exc:
            logger.warning("JournalAnalytics.coach_summary: %s", exc)
            return {
                "top_mistakes": [], "most_common_mistake": "",
                "review_backlog": 0, "process_focus": "",
                "total_entries": 0, "no_real_orders": True,
            }
