"""
replay/scoring_summary.py — ReplayScoringSummaryBuilder for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Summary data is for research training only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoringSummaryBuilder:
    """
    Builds scoring summaries for sessions, symbols, and scenarios.
    [!] Research Only. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        if store is not None:
            self._store = store
        else:
            from replay.scoring_store import ReplayScoringStore
            self._store = ReplayScoringStore(repo_root=repo_root)

    def overall_summary(self) -> Dict[str, Any]:
        """Build overall scoring summary across all sessions."""
        process_scores = self._store.load_all("process_score")
        composite_scores = self._store.load_all("composite_score")
        mistakes = self._store.load_all("mistake")
        reveals = self._store.load_all("reveal")

        confirmed_reveals = [r for r in reveals if r.get("reveal_confirmed")]
        ps_totals = [float(s.get("total_score", 0)) for s in process_scores]
        avg_process = sum(ps_totals) / len(ps_totals) if ps_totals else 0.0

        # Classification breakdown
        classifications: Dict[str, int] = {}
        for cs in composite_scores:
            clf = cs.get("classification", "UNKNOWN")
            classifications[clf] = classifications.get(clf, 0) + 1

        # Mistake breakdown
        mistake_types: Dict[str, int] = {}
        mistake_statuses: Dict[str, int] = {}
        for m in mistakes:
            mt = m.get("mistake_type", "UNKNOWN")
            mistake_types[mt] = mistake_types.get(mt, 0) + 1
            ms = m.get("status", "UNKNOWN")
            mistake_statuses[ms] = mistake_statuses.get(ms, 0) + 1

        return {
            "total_process_scores": len(process_scores),
            "total_composite_scores": len(composite_scores),
            "total_reveals": len(reveals),
            "confirmed_reveals": len(confirmed_reveals),
            "total_mistakes": len(mistakes),
            "avg_process_score": round(avg_process, 2),
            "classification_breakdown": classifications,
            "mistake_type_breakdown": mistake_types,
            "mistake_status_breakdown": mistake_statuses,
            "confidence_note": (
                f"{'INSUFFICIENT' if len(process_scores) < 10 else 'OBSERVATIONAL'} — "
                f"{len(process_scores)} sessions scored."
            ),
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def session_summary(self, session_id: str) -> Dict[str, Any]:
        """Build scoring summary for a single session."""
        from replay.scoring_query import ReplayScoringQuery
        q = ReplayScoringQuery(store=self._store)

        ps = q.get_latest_process_score(session_id)
        reveal = q.get_latest_reveal(session_id)
        composite_scores = q.list_session_composite_scores(session_id)
        mistakes = q.list_session_mistakes(session_id)
        mistake_counts = q.count_mistakes(session_id)

        latest_composite = None
        if composite_scores:
            latest_composite = sorted(
                composite_scores, key=lambda s: s.get("scored_at", ""), reverse=True
            )[0]

        return {
            "session_id": session_id,
            "process_score": ps.get("total_score") if ps else None,
            "process_score_id": ps.get("score_id") if ps else None,
            "process_score_status": ps.get("status") if ps else "NOT_SCORED",
            "outcome_revealed": reveal is not None,
            "outcome_reveal_id": reveal.get("reveal_id") if reveal else None,
            "composite_classification": latest_composite.get("classification") if latest_composite else "BLOCKED",
            "composite_score": latest_composite.get("composite_score") if latest_composite else None,
            "mistake_count": mistake_counts["total"],
            "confirmed_mistake_count": mistake_counts.get("confirmed", 0),
            "suggested_mistake_count": mistake_counts.get("suggested", 0),
            "dismissed_mistake_count": mistake_counts.get("dismissed", 0),
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def symbol_summary(self, symbol: str) -> Dict[str, Any]:
        """Build scoring summary for a symbol."""
        from replay.scoring_query import ReplayScoringQuery
        q = ReplayScoringQuery(store=self._store)

        scores = q.list_scores_by_symbol(symbol)
        mistakes = q.list_mistakes_by_symbol(symbol)
        totals = [float(s.get("total_score", 0)) for s in scores]
        avg = sum(totals) / len(totals) if totals else 0.0

        from replay.score_confidence import ReplayScoreConfidence
        confidence_engine = ReplayScoreConfidence()
        conf_level, conf_note = confidence_engine.assess(entry_count=len(scores))

        return {
            "symbol": symbol,
            "scored_sessions": len(scores),
            "avg_process_score": round(avg, 2),
            "total_mistakes": len(mistakes),
            "confirmed_mistakes": sum(1 for m in mistakes if m.get("status") == "CONFIRMED"),
            "confidence_level": conf_level,
            "confidence_note": conf_note,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def scenario_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Build scoring summary for a scenario."""
        scores = [
            s for s in self._store.load_all("process_score")
            if s.get("scenario_id") == scenario_id
        ]
        totals = [float(s.get("total_score", 0)) for s in scores]
        avg = sum(totals) / len(totals) if totals else 0.0

        return {
            "scenario_id": scenario_id,
            "scored_sessions": len(scores),
            "avg_process_score": round(avg, 2),
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
