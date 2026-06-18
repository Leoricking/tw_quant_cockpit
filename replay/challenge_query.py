"""
replay/challenge_query.py — Challenge data query interface v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeQuery:
    """
    Query interface for challenge data.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None) -> None:
        self._store = store

    def _load(self, name: str) -> List[Dict[str, Any]]:
        if self._store:
            return self._store.load_all(name)
        return []

    def challenges(self) -> List[Dict[str, Any]]:
        return self._load("challenges")

    def challenge(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        return next((c for c in self.challenges() if c.get("challenge_id") == challenge_id), None)

    def attempts(self) -> List[Dict[str, Any]]:
        return self._load("attempts")

    def attempt(self, attempt_id: str) -> Optional[Dict[str, Any]]:
        return next((a for a in self.attempts() if a.get("attempt_id") == attempt_id), None)

    def actions(self, attempt_id: Optional[str] = None) -> List[Dict[str, Any]]:
        acts = self._load("actions")
        if attempt_id:
            acts = [a for a in acts if a.get("attempt_id") == attempt_id]
        return acts

    def scores(self, attempt_id: Optional[str] = None) -> List[Dict[str, Any]]:
        s = self._load("scores")
        if attempt_id:
            s = [x for x in s if x.get("attempt_id") == attempt_id]
        return s

    def results(self, attempt_id: Optional[str] = None) -> List[Dict[str, Any]]:
        r = self._load("results")
        if attempt_id:
            r = [x for x in r if x.get("attempt_id") == attempt_id]
        return r

    def reviews(self, attempt_id: Optional[str] = None) -> List[Dict[str, Any]]:
        r = self._load("reviews")
        if attempt_id:
            r = [x for x in r if x.get("attempt_id") == attempt_id]
        return r

    def progress(self) -> List[Dict[str, Any]]:
        return self._load("progress")

    def streaks(self) -> List[Dict[str, Any]]:
        return self._load("streaks")

    def badges(self) -> List[Dict[str, Any]]:
        return self._load("badges")

    def leaderboard(self, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        results = self._load("results")
        if difficulty:
            results = [r for r in results if r.get("difficulty") == difficulty]
        return sorted(results, key=lambda r: r.get("total_score", 0.0), reverse=True)

    def by_type(self, challenge_type: str) -> List[Dict[str, Any]]:
        return [c for c in self.challenges() if c.get("challenge_type") == challenge_type]

    def by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        return [c for c in self.challenges() if c.get("difficulty") == difficulty]

    def by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return [c for c in self.challenges() if c.get("symbol") == symbol]

    def by_scenario(self, scenario_id: str) -> List[Dict[str, Any]]:
        return [c for c in self.challenges() if c.get("scenario_id") == scenario_id]

    def by_mistake(self, mistake_type: str) -> List[Dict[str, Any]]:
        return [c for c in self.challenges() if c.get("challenge_type") == "MISTAKE_CORRECTION"
                and mistake_type in str(c.get("source_mistake_id", ""))]

    def pending_reviews(self) -> List[Dict[str, Any]]:
        return [a for a in self.attempts() if a.get("review_status") == "NOT_REVIEWED"
                and a.get("status") == "COMPLETED"]

    def best_attempt(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        attempts = [a for a in self.attempts() if a.get("challenge_id") == challenge_id]
        if not attempts:
            return None
        return max(attempts, key=lambda a: a.get("total_score", 0.0))

    def search(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        return [
            c for c in self.challenges()
            if q in c.get("title", "").lower()
            or q in c.get("description", "").lower()
            or q in c.get("challenge_type", "").lower()
        ]
