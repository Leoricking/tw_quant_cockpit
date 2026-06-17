"""
replay/scoring_query.py — Scoring query interface for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoringQuery:
    """
    Query interface for replay scoring data.
    [!] Research Only. No Real Orders.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        if store is not None:
            self._store = store
        else:
            from replay.scoring_store import ReplayScoringStore
            self._store = ReplayScoringStore(repo_root=repo_root)

    def get_process_score(self, score_id: str) -> Optional[Dict[str, Any]]:
        return self._store.load_by_id("process_score", score_id, "score_id")

    def get_outcome_score(self, score_id: str) -> Optional[Dict[str, Any]]:
        return self._store.load_by_id("outcome_score", score_id, "score_id")

    def get_composite_score(self, score_id: str) -> Optional[Dict[str, Any]]:
        return self._store.load_by_id("composite_score", score_id, "score_id")

    def get_reveal_record(self, reveal_id: str) -> Optional[Dict[str, Any]]:
        return self._store.load_by_id("reveal", reveal_id, "reveal_id")

    def get_mistake(self, mistake_id: str) -> Optional[Dict[str, Any]]:
        return self._store.load_by_id("mistake", mistake_id, "mistake_id")

    def get_mistake_reviews(self, mistake_id: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._store.load_all("mistake_review")
            if r.get("mistake_id") == mistake_id
        ]

    def list_session_process_scores(self, session_id: str) -> List[Dict[str, Any]]:
        return self._store.load_by_session("process_score", session_id)

    def list_session_mistakes(self, session_id: str) -> List[Dict[str, Any]]:
        return self._store.load_by_session("mistake", session_id)

    def list_session_reveals(self, session_id: str) -> List[Dict[str, Any]]:
        return self._store.load_by_session("reveal", session_id)

    def list_session_composite_scores(self, session_id: str) -> List[Dict[str, Any]]:
        return self._store.load_by_session("composite_score", session_id)

    def list_all_process_scores(self) -> List[Dict[str, Any]]:
        return self._store.load_all("process_score")

    def list_all_mistakes(self) -> List[Dict[str, Any]]:
        return self._store.load_all("mistake")

    def list_mistakes_by_status(self, status: str) -> List[Dict[str, Any]]:
        return [
            m for m in self._store.load_all("mistake")
            if m.get("status") == status
        ]

    def list_mistakes_by_type(self, mistake_type: str) -> List[Dict[str, Any]]:
        return [
            m for m in self._store.load_all("mistake")
            if m.get("mistake_type") == mistake_type
        ]

    def list_mistakes_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return [
            m for m in self._store.load_all("mistake")
            if m.get("symbol") == symbol
        ]

    def list_mistakes_by_category(self, category: str) -> List[Dict[str, Any]]:
        return [
            m for m in self._store.load_all("mistake")
            if m.get("category") == category
        ]

    def list_scores_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return [
            s for s in self._store.load_all("process_score")
            if s.get("symbol") == symbol
        ]

    def count_mistakes(self, session_id: Optional[str] = None) -> Dict[str, int]:
        if session_id:
            mistakes = self._store.load_by_session("mistake", session_id)
        else:
            mistakes = self._store.load_all("mistake")

        counts = {"total": 0, "suggested": 0, "confirmed": 0, "dismissed": 0, "needs_review": 0}
        for m in mistakes:
            counts["total"] += 1
            status = m.get("status", "").lower()
            if status in counts:
                counts[status] += 1
        return counts

    def get_latest_process_score(self, session_id: str) -> Optional[Dict[str, Any]]:
        scores = self._store.load_by_session("process_score", session_id)
        if not scores:
            return None
        return sorted(scores, key=lambda s: s.get("scored_at", ""), reverse=True)[0]

    def get_latest_reveal(self, session_id: str) -> Optional[Dict[str, Any]]:
        reveals = self._store.load_by_session("reveal", session_id)
        if not reveals:
            return None
        confirmed = [r for r in reveals if r.get("reveal_confirmed")]
        if confirmed:
            return sorted(confirmed, key=lambda r: r.get("revealed_at", ""), reverse=True)[0]
        return None
