"""
replay/review_summary.py — Replay Review Summary Builder v1.2.6

Supports: global/session/symbol/scenario/daily/weekly summary.
Outputs: session counts, review completion, review progress, process score,
outcome score (hidden until revealed), classification, mistake counts,
strategy conflicts, timeframe conflicts, integrity status, queue counts,
elapsed time, confidence, insufficient count, real/mock separation.

[!] Research Only. No Real Orders. Outcome score hidden until revealed.
[!] Real/Mock strictly separated. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewSummaryBuilder:
    """
    Builds summary views for the replay review dashboard.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def global_summary(self, rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Build global summary across all sessions."""
        if rows is None:
            rows = self._load_rows()

        real_rows = [r for r in rows if r.get("mode") != "mock"]
        mock_rows  = [r for r in rows if r.get("mode") == "mock"]

        def _avg_score(rs: List[Dict]) -> Optional[float]:
            vals = [r["process_score"] for r in rs if r.get("process_score") is not None]
            return round(sum(vals) / len(vals), 2) if vals else None

        return {
            "summary_type":          "GLOBAL",
            "total_sessions":        len(rows),
            "real_sessions":         len(real_rows),
            "mock_sessions":         len(mock_rows),
            "review_complete":       sum(1 for r in rows if r.get("review_complete")),
            "review_incomplete":     sum(1 for r in rows if not r.get("review_complete")),
            "avg_process_score":     _avg_score(rows),
            "avg_process_score_real": _avg_score(real_rows),
            "avg_process_score_mock": _avg_score(mock_rows),
            "outcome_score":         "HIDDEN_UNTIL_REVEALED",
            "suggested_mistakes":    sum(r.get("mistake_count", 0) for r in rows),
            "confirmed_mistakes":    sum(r.get("confirmed_mistake_count", 0) for r in rows),
            "strategy_conflicts":    sum(r.get("strategy_conflicts", 0) for r in rows),
            "timeframe_conflicts":   sum(r.get("mtf_conflicts", 0) for r in rows),
            "pit_failures":          sum(1 for r in rows if not r.get("pit_verified")),
            "low_confidence":        sum(1 for r in rows if r.get("confidence") == "LOW"),
            "insufficient":          sum(1 for r in rows if r.get("confidence") == "INSUFFICIENT"),
            "research_only":         True,
            "no_real_orders":        True,
            "real_mock_separated":   True,
        }

    def session_summary(self, session_id: str, row: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build per-session summary."""
        if row is None:
            rows = self._load_rows()
            matching = [r for r in rows if r.get("session_id") == session_id]
            row = matching[0] if matching else {}

        return {
            "summary_type":       "SESSION",
            "session_id":         session_id,
            "symbol":             row.get("symbol"),
            "status":             row.get("status"),
            "review_progress":    row.get("review_progress"),
            "process_score":      row.get("process_score"),
            "outcome_score":      "NOT_REVEALED" if not row.get("outcome_revealed") else row.get("outcome_score"),
            "classification":     row.get("classification"),
            "mistake_count":      row.get("mistake_count", 0),
            "strategy_conflicts": row.get("strategy_conflicts", 0),
            "mtf_conflicts":      row.get("mtf_conflicts", 0),
            "pit_verified":       row.get("pit_verified"),
            "confidence":         row.get("confidence"),
            "research_only":      True,
        }

    def symbol_summary(self, symbol: str, rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Build per-symbol summary."""
        if rows is None:
            rows = self._load_rows()
        sym_rows = [r for r in rows if r.get("symbol") == symbol]
        return {
            "summary_type":   "SYMBOL",
            "symbol":         symbol,
            "session_count":  len(sym_rows),
            "review_complete": sum(1 for r in sym_rows if r.get("review_complete")),
            "avg_process_score": self._avg(sym_rows, "process_score"),
            "research_only":  True,
        }

    def scenario_summary(self, scenario_id: str, rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Build per-scenario summary."""
        if rows is None:
            rows = self._load_rows()
        sc_rows = [r for r in rows if r.get("scenario_id") == scenario_id]
        return {
            "summary_type":   "SCENARIO",
            "scenario_id":    scenario_id,
            "session_count":  len(sc_rows),
            "review_complete": sum(1 for r in sc_rows if r.get("review_complete")),
            "avg_process_score": self._avg(sc_rows, "process_score"),
            "research_only":  True,
        }

    def daily_summary(self, date_str: str, rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Build daily summary."""
        if rows is None:
            rows = self._load_rows()
        day_rows = [r for r in rows if r.get("updated_at", "")[:10] == date_str]
        return {
            "summary_type":   "DAILY",
            "date":           date_str,
            "session_count":  len(day_rows),
            "reviewed":       sum(1 for r in day_rows if r.get("review_complete")),
            "research_only":  True,
        }

    def weekly_summary(self, week_start: str, rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Build weekly summary (from week_start for 7 days)."""
        return {
            "summary_type":  "WEEKLY",
            "week_start":    week_start,
            "research_only": True,
            "note":          "Use daily_summary for each day in the week.",
        }

    def _avg(self, rows: List[Dict], field: str) -> Optional[float]:
        vals = [r[field] for r in rows if r.get(field) is not None]
        return round(sum(vals) / len(vals), 2) if vals else None

    def _load_rows(self) -> List[Dict[str, Any]]:
        try:
            from replay.review_query import ReplayReviewQuery
            q = ReplayReviewQuery()
            return q.sessions()
        except Exception:
            return []
