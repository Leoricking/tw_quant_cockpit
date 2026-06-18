"""
replay/review_dashboard_engine.py — ReplayReviewDashboardEngine v1.2.6

Builds dashboard views (global, session, symbol, scenario, timeframe) by
composing cards, tables, charts, queue, and progress from the adapter.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Auto Review Complete. No Auto Outcome Reveal. No Auto Confirm.
[!] No Auto Decision. No Auto Execution. No Score-to-Trade. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewDashboardEngine:
    """
    Engine that assembles all dashboard views.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, mode: str = "real") -> None:
        self._mode = mode
        from replay.review_dashboard_adapter import ReplayReviewDashboardAdapter
        self._adapter = ReplayReviewDashboardAdapter(mode=mode)
        self._last_snapshot = None

    # ------------------------------------------------------------------
    # Top-level dashboard builders
    # ------------------------------------------------------------------

    def build_global_dashboard(self, mode: str = "real") -> Dict[str, Any]:
        """Build global dashboard snapshot with cards, tables, charts, queue, progress."""
        snapshot = self._adapter.build_dashboard_snapshot(mode=mode)
        self._last_snapshot = snapshot
        cards = self.build_cards(snapshot.to_dict())
        tables = self.build_tables(snapshot.to_dict())
        charts = self.build_charts(snapshot.to_dict())
        queue = self.build_queue(snapshot.to_dict())
        progress = self.build_progress(snapshot.to_dict())
        return {
            "dashboard_type": "GLOBAL",
            "mode": mode,
            "snapshot": snapshot.to_dict(),
            "cards": cards,
            "tables": tables,
            "charts": charts,
            "queue": queue,
            "progress": progress,
            "research_only": True,
            "no_real_orders": True,
            "generated_at": snapshot.generated_at,
        }

    def build_session_dashboard(self, session_id: str) -> Dict[str, Any]:
        """Build per-session dashboard."""
        detail = self._adapter.load_session_detail(session_id)
        scoring = self._adapter.load_scoring_summary(session_id)
        journal = self._adapter.load_journal_summary(session_id)
        mistakes = self._adapter.load_mistake_summary(session_id)
        strategy = self._adapter.load_strategy_summary(session_id)
        timeframe = self._adapter.load_timeframe_summary(session_id)
        return {
            "dashboard_type": "SESSION",
            "session_id": session_id,
            "mode": self._mode,
            "detail": detail,
            "scoring": scoring,
            "journal": journal,
            "mistakes": mistakes,
            "strategy": strategy,
            "timeframe": timeframe,
            "research_only": True,
            "no_real_orders": True,
        }

    def build_symbol_dashboard(self, symbol: str) -> Dict[str, Any]:
        """Build per-symbol dashboard."""
        sessions = self._adapter.load_sessions()
        rows = [
            s for s in (sessions.get("data") or [])
            if s.get("symbol") == symbol
        ]
        return {
            "dashboard_type": "SYMBOL",
            "symbol": symbol,
            "mode": self._mode,
            "session_count": len(rows),
            "sessions": rows,
            "research_only": True,
            "no_real_orders": True,
        }

    def build_scenario_dashboard(self, scenario_id: str) -> Dict[str, Any]:
        """Build per-scenario dashboard."""
        sessions = self._adapter.load_sessions()
        rows = [
            s for s in (sessions.get("data") or [])
            if s.get("scenario_id") == scenario_id
        ]
        return {
            "dashboard_type": "SCENARIO",
            "scenario_id": scenario_id,
            "mode": self._mode,
            "session_count": len(rows),
            "sessions": rows,
            "research_only": True,
            "no_real_orders": True,
        }

    def build_timeframe_dashboard(self, timeframe: str) -> Dict[str, Any]:
        """Build per-timeframe dashboard."""
        tf_summary = self._adapter.load_timeframe_summary()
        return {
            "dashboard_type": "TIMEFRAME",
            "timeframe": timeframe,
            "mode": self._mode,
            "timeframe_summary": tf_summary,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Refresh / drill-down
    # ------------------------------------------------------------------

    def refresh(self) -> Dict[str, Any]:
        """Rebuild global dashboard."""
        return self.build_global_dashboard(mode=self._mode)

    def drill_down(self, context: str, value: str) -> Dict[str, Any]:
        """Drill into session, symbol, or scenario."""
        if context == "session":
            return self.build_session_dashboard(value)
        if context == "symbol":
            return self.build_symbol_dashboard(value)
        if context == "scenario":
            return self.build_scenario_dashboard(value)
        return {"status": "UNKNOWN_CONTEXT", "context": context, "value": value}

    # ------------------------------------------------------------------
    # Component builders
    # ------------------------------------------------------------------

    def build_cards(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Build all dashboard card categories from snapshot data."""
        try:
            from replay.review_dashboard_cards import (
                build_session_cards, build_queue_cards,
                build_score_cards, build_integrity_cards,
                build_strategy_cards, build_timeframe_cards,
                build_timing_cards,
            )
            return {
                "session":   build_session_cards(snapshot),
                "queue":     build_queue_cards(snapshot),
                "score":     build_score_cards(snapshot),
                "integrity": build_integrity_cards(snapshot),
                "strategy":  build_strategy_cards(snapshot),
                "timeframe": build_timeframe_cards(snapshot),
                "timing":    build_timing_cards(snapshot),
            }
        except Exception as exc:
            logger.warning("build_cards failed: %s", exc)
            return {"status": "UNAVAILABLE", "reason": str(exc)}

    def build_tables(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Build review tables from snapshot data."""
        try:
            from replay.review_dashboard_tables import (
                build_session_review_table,
                build_pending_review_queue_table,
            )
            rows = snapshot.get("session_rows", [])
            return {
                "sessions": build_session_review_table(rows),
                "pending_queue": build_pending_review_queue_table(rows),
            }
        except Exception as exc:
            logger.warning("build_tables failed: %s", exc)
            return {"status": "UNAVAILABLE", "reason": str(exc)}

    def build_charts(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Build chart data specs from snapshot data."""
        try:
            from replay.review_dashboard_charts import (
                build_review_progress_distribution,
                build_process_score_distribution,
                build_mistake_type_distribution,
            )
            rows = snapshot.get("session_rows", [])
            return {
                "review_progress": build_review_progress_distribution(rows),
                "process_score":   build_process_score_distribution(rows),
                "mistake_types":   build_mistake_type_distribution(rows),
            }
        except Exception as exc:
            logger.warning("build_charts failed: %s", exc)
            return {"status": "UNAVAILABLE", "reason": str(exc)}

    def build_queue(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Build review queue summary from snapshot data."""
        try:
            from replay.review_queue import ReplayReviewQueueManager
            mgr = ReplayReviewQueueManager()
            return mgr.summary()
        except Exception as exc:
            logger.warning("build_queue failed: %s", exc)
            return {"status": "UNAVAILABLE", "reason": str(exc), "open_count": 0}

    def build_progress(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Build review progress summary from snapshot data."""
        rows = snapshot.get("session_rows", [])
        review_complete = sum(1 for r in rows if r.get("review_complete"))
        total = len(rows)
        pct = round(review_complete / total * 100, 1) if total > 0 else 0.0
        return {
            "total_sessions":       total,
            "review_complete":      review_complete,
            "review_incomplete":    total - review_complete,
            "progress_percent":     pct,
            "outcome_reveal_required": False,
            "research_only": True,
        }

    def summary(self) -> Dict[str, Any]:
        """Return a concise global summary."""
        snap = self._last_snapshot
        if snap is None:
            result = self.build_global_dashboard(mode=self._mode)
            snap = self._last_snapshot
        d = snap.to_dict() if snap else {}
        return {
            "version": "1.2.6",
            "mode": self._mode,
            "total_sessions": d.get("total_sessions", 0),
            "review_complete": d.get("review_complete_sessions", 0),
            "pending_queue": d.get("total_pending_queue", 0),
            "avg_process_score": d.get("avg_process_score"),
            "suggested_mistakes": d.get("suggested_mistakes", 0),
            "strategy_conflicts": d.get("strategy_conflicts", 0),
            "confidence": d.get("confidence", "INSUFFICIENT"),
            "research_only": True,
            "no_real_orders": True,
        }
