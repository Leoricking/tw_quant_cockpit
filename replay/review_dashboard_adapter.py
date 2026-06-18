"""
replay/review_dashboard_adapter.py — ReplayReviewDashboardAdapter v1.2.6

Loads and bridges data from all replay sub-modules into the review dashboard.
All imports are try/except — missing modules show UNAVAILABLE, not crash.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Auto Review Complete. No Auto Outcome Reveal. No Auto Confirm.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import (
    ReplayReviewDashboardSnapshot,
    ReplayReviewSessionRow,
    _new_id,
    _now_utc,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_UNAVAILABLE = {"status": "UNAVAILABLE", "data": [], "reason": "Module not loaded"}


def safe_unavailable(module_name: str, exc: Exception) -> Dict[str, Any]:
    """Return standard UNAVAILABLE sentinel when a module fails to import."""
    logger.warning("Module %s unavailable: %s", module_name, exc)
    return {"status": "UNAVAILABLE", "module": module_name, "reason": str(exc), "data": []}


class ReplayReviewDashboardAdapter:
    """
    Bridges data from all replay sub-modules for the review dashboard.

    [!] Research Only. No Real Orders. Missing modules → UNAVAILABLE (no crash).
    [!] Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, mode: str = "real") -> None:
        self._mode = mode

    # ------------------------------------------------------------------
    # Session loading
    # ------------------------------------------------------------------

    def load_sessions(self) -> Dict[str, Any]:
        """Load all replay sessions via SessionManager."""
        try:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager()
            sessions = mgr.list_sessions()
            return {"status": "OK", "data": sessions, "count": len(sessions)}
        except Exception as exc:
            return safe_unavailable("session_manager", exc)

    def load_session_detail(self, session_id: str) -> Dict[str, Any]:
        """Load detail for a single session."""
        try:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager()
            detail = mgr.get_session(session_id)
            return {"status": "OK", "data": detail}
        except Exception as exc:
            return safe_unavailable("session_manager", exc)

    # ------------------------------------------------------------------
    # Journal
    # ------------------------------------------------------------------

    def load_journal_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Load decision journal summary."""
        try:
            from replay.decision_journal_summary import DecisionJournalSummary
            s = DecisionJournalSummary()
            if session_id:
                data = s.session_summary(session_id)
            else:
                data = s.global_summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("decision_journal_summary", exc)

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def load_scoring_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Load scoring summary (process only; outcome hidden until revealed)."""
        try:
            from replay.scoring_query import ScoringQuery
            q = ScoringQuery()
            if session_id:
                data = q.session_summary(session_id)
            else:
                data = q.global_summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("scoring_query", exc)

    # ------------------------------------------------------------------
    # Mistakes
    # ------------------------------------------------------------------

    def load_mistake_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Load mistake summary."""
        try:
            from replay.mistake_review_manager import MistakeReviewManager
            mgr = MistakeReviewManager()
            if session_id:
                data = mgr.session_summary(session_id)
            else:
                data = mgr.global_summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("mistake_review_manager", exc)

    # ------------------------------------------------------------------
    # Strategy
    # ------------------------------------------------------------------

    def load_strategy_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Load strategy knowledge replay summary."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            q = StrategyReplayQuery()
            if session_id:
                data = q.session_summary(session_id)
            else:
                data = q.global_summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("strategy_replay_query", exc)

    # ------------------------------------------------------------------
    # Timeframe
    # ------------------------------------------------------------------

    def load_timeframe_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Load multi-timeframe summary."""
        try:
            from replay.timeframe_summary import MultiTimeframeSummaryBuilder
            b = MultiTimeframeSummaryBuilder()
            if session_id:
                data = b.build_session_summary(session_id)
            else:
                data = b.build_global_summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("timeframe_summary", exc)

    # ------------------------------------------------------------------
    # Registry
    # ------------------------------------------------------------------

    def load_registry_summary(self) -> Dict[str, Any]:
        """Load research registry summary."""
        try:
            from research_registry.registry_query import RegistryQuery
            q = RegistryQuery()
            data = q.summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("registry_query", exc)

    # ------------------------------------------------------------------
    # Governance
    # ------------------------------------------------------------------

    def load_governance_summary(self) -> Dict[str, Any]:
        """Load governance dashboard summary."""
        try:
            from governance_ops.governance_adapters import GovernanceDashboardAdapter
            adapter = GovernanceDashboardAdapter()
            data = adapter.summary()
            return {"status": "OK", "data": data}
        except Exception as exc:
            return safe_unavailable("governance_adapters", exc)

    # ------------------------------------------------------------------
    # Build helpers
    # ------------------------------------------------------------------

    def build_session_row(self, session: Dict[str, Any]) -> ReplayReviewSessionRow:
        """Build a ReplayReviewSessionRow from raw session dict."""
        session_id = session.get("session_id", "UNKNOWN")
        symbol = session.get("symbol", "UNKNOWN")

        # Load scoring (process only; outcome hidden)
        scoring = self.load_scoring_summary(session_id)
        scoring_data = scoring.get("data", {}) or {}

        process_score = None
        outcome_score = None
        composite_score = None
        outcome_revealed = bool(scoring_data.get("outcome_revealed", False))
        classification = scoring_data.get("classification", "UNCLASSIFIED")

        if scoring.get("status") == "OK":
            process_score = scoring_data.get("process_score")
            if outcome_revealed:
                outcome_score = scoring_data.get("outcome_score")
                composite_score = scoring_data.get("composite_score")

        # Mistakes
        mistakes = self.load_mistake_summary(session_id)
        mistakes_data = mistakes.get("data", {}) or {}
        mistake_count = int(mistakes_data.get("suggested_count", 0)) if mistakes.get("status") == "OK" else 0
        confirmed_count = int(mistakes_data.get("confirmed_count", 0)) if mistakes.get("status") == "OK" else 0

        # Strategy conflicts
        strategy = self.load_strategy_summary(session_id)
        strategy_data = strategy.get("data", {}) or {}
        strategy_conflicts = int(strategy_data.get("conflict_count", 0)) if strategy.get("status") == "OK" else 0

        # MTF conflicts
        timeframe = self.load_timeframe_summary(session_id)
        tf_data = timeframe.get("data", {}) or {}
        mtf_conflicts = int(tf_data.get("conflict_count", 0)) if timeframe.get("status") == "OK" else 0

        return ReplayReviewSessionRow(
            session_id=session_id,
            symbol=symbol,
            scenario_id=session.get("scenario_id"),
            status=session.get("status", "UNKNOWN"),
            review_progress=session.get("review_progress", "NOT_STARTED"),
            process_score=process_score,
            outcome_score=outcome_score,
            composite_score=composite_score,
            classification=classification,
            mistake_count=mistake_count,
            confirmed_mistake_count=confirmed_count,
            strategy_conflicts=strategy_conflicts,
            mtf_conflicts=mtf_conflicts,
            outcome_revealed=outcome_revealed,
            pit_verified=bool(session.get("pit_verified", False)),
            elapsed_seconds=float(session.get("elapsed_seconds", 0.0)),
            confidence=session.get("confidence", "INSUFFICIENT"),
            warnings=session.get("warnings", []),
            review_complete=bool(session.get("review_complete", False)),
            mode=self._mode,
        )

    def build_dashboard_snapshot(self, mode: str = "real") -> ReplayReviewDashboardSnapshot:
        """Build a full dashboard snapshot from all sub-modules."""
        snapshot_id = _new_id("RRD-")

        sessions_result = self.load_sessions()
        sessions = sessions_result.get("data", []) or []

        rows = []
        for s in sessions:
            try:
                row = self.build_session_row(s)
                rows.append(row.to_dict())
            except Exception as exc:
                logger.warning("Failed to build row for session %s: %s", s.get("session_id"), exc)

        total = len(sessions)
        active = sum(1 for s in sessions if s.get("status") == "ACTIVE")
        completed = sum(1 for s in sessions if s.get("status") == "COMPLETED")
        archived = sum(1 for s in sessions if s.get("status") == "ARCHIVED")
        review_complete = sum(1 for s in sessions if s.get("review_complete"))
        review_incomplete = total - review_complete

        # Scoring aggregates
        scoring_summary = self.load_scoring_summary()
        scoring_data = scoring_summary.get("data", {}) or {}
        avg_process = scoring_data.get("avg_process_score") if scoring_summary.get("status") == "OK" else None

        # Mistakes
        mistake_summary = self.load_mistake_summary()
        mistake_data = mistake_summary.get("data", {}) or {}
        suggested = int(mistake_data.get("suggested_count", 0)) if mistake_summary.get("status") == "OK" else 0
        confirmed = int(mistake_data.get("confirmed_count", 0)) if mistake_summary.get("status") == "OK" else 0
        dismissed = int(mistake_data.get("dismissed_count", 0)) if mistake_summary.get("status") == "OK" else 0

        # Strategy
        strategy_summary = self.load_strategy_summary()
        strategy_data = strategy_summary.get("data", {}) or {}
        strategy_conflicts = int(strategy_data.get("conflict_count", 0)) if strategy_summary.get("status") == "OK" else 0
        strategy_warnings = int(strategy_data.get("warning_count", 0)) if strategy_summary.get("status") == "OK" else 0

        # Timeframe
        tf_summary = self.load_timeframe_summary()
        tf_data = tf_summary.get("data", {}) or {}
        tf_conflicts = int(tf_data.get("conflict_count", 0)) if tf_summary.get("status") == "OK" else 0

        return ReplayReviewDashboardSnapshot(
            snapshot_id=snapshot_id,
            mode=mode,
            total_sessions=total,
            active_sessions=active,
            completed_sessions=completed,
            archived_sessions=archived,
            review_complete_sessions=review_complete,
            review_incomplete_sessions=review_incomplete,
            avg_process_score=avg_process,
            suggested_mistakes=suggested,
            confirmed_mistakes=confirmed,
            dismissed_mistakes=dismissed,
            strategy_conflicts=strategy_conflicts,
            strategy_warnings=strategy_warnings,
            timeframe_conflicts=tf_conflicts,
            confidence="INSUFFICIENT" if total == 0 else "LOW",
            session_rows=rows,
        )
