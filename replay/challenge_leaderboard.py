"""
replay/challenge_leaderboard.py — ReplayChallengeLeaderboard v1.2.7

LOCAL personal leaderboard ONLY.
[!] NO public leaderboard. NO cloud upload. NO network submission.
[!] NO user-to-user competition. NO real PnL ranking. NO broker ranking.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
PUBLIC_LEADERBOARD_ENABLED = False
NETWORK_SCORE_SUBMISSION_ENABLED = False
USER_TO_USER_COMPETITION = False
REAL_PNL_RANKING = False
BROKER_PERFORMANCE_RANKING = False


class ReplayChallengeLeaderboard:
    """
    Local personal leaderboard for challenge attempts.

    [!] LOCAL ONLY — no network submission, no public leaderboard.
    [!] Fields: rank, challenge_type, difficulty, attempt_id,
        total_score, process_score, elapsed_seconds, hints_used,
        mistakes, completed_at.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    PUBLIC_LEADERBOARD_ENABLED = False
    NETWORK_SCORE_SUBMISSION_ENABLED = False
    USER_TO_USER_COMPETITION = False
    REAL_PNL_RANKING = False
    BROKER_PERFORMANCE_RANKING = False

    def __init__(self) -> None:
        self._entries: List[Dict[str, Any]] = []

    def record(self, result: Dict[str, Any], score: Dict[str, Any], attempt: Dict[str, Any]) -> None:
        """Record a result to the personal leaderboard."""
        score_obj = score.get("score")
        total_score = float(getattr(score_obj, "total_score", 0.0)) if score_obj else result.get("total_score", 0.0)
        process_score = float(getattr(score_obj, "process_score", 0.0)) if score_obj else result.get("process_score", 0.0)
        self._entries.append({
            "attempt_id":      result.get("attempt_id", ""),
            "challenge_id":    result.get("challenge_id", ""),
            "challenge_type":  attempt.get("challenge_type", ""),
            "difficulty":      attempt.get("difficulty", ""),
            "total_score":     round(total_score, 1),
            "process_score":   round(process_score, 1),
            "elapsed_seconds": attempt.get("active_elapsed_seconds", 0.0),
            "hints_used":      result.get("hints_used", 0),
            "mistakes":        result.get("mistakes_suggested", []),
            "completed_at":    result.get("generated_at", ""),
            "completed":       result.get("completed", False),
            "local_only":      True,
            "no_network":      True,
            "research_only":   True,
        })

    def best_score(
        self,
        challenge_id: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return the personal best score entry."""
        entries = self._filter(challenge_id=challenge_id, difficulty=difficulty, completed_only=True)
        if not entries:
            return None
        return max(entries, key=lambda e: e["total_score"])

    def fastest_valid_completion(
        self,
        challenge_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return the fastest completed entry with process_score >= 50."""
        entries = [e for e in self._entries if e.get("completed") and e.get("process_score", 0) >= 50.0]
        if challenge_id:
            entries = [e for e in entries if e.get("challenge_id") == challenge_id]
        if not entries:
            return None
        return min(entries, key=lambda e: e["elapsed_seconds"])

    def best_process_score(self, challenge_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        entries = self._filter(challenge_id=challenge_id, completed_only=True)
        if not entries:
            return None
        return max(entries, key=lambda e: e["process_score"])

    def least_hints(self, challenge_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        entries = self._filter(challenge_id=challenge_id, completed_only=True)
        if not entries:
            return None
        return min(entries, key=lambda e: e["hints_used"])

    def most_improved(self, challenge_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Return entry with best improvement from first to latest."""
        entries = self._filter(challenge_id=challenge_id)
        if len(entries) < 2:
            return None
        first = entries[0]["total_score"]
        best = max(e["total_score"] for e in entries[1:])
        improvement = best - first
        return {"improvement": improvement, "from_score": first, "to_score": best}

    def ranked_list(
        self,
        difficulty: Optional[str] = None,
        challenge_type: Optional[str] = None,
        top_n: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return ranked local leaderboard."""
        entries = self._entries
        if difficulty:
            entries = [e for e in entries if e.get("difficulty") == difficulty]
        if challenge_type:
            entries = [e for e in entries if e.get("challenge_type") == challenge_type]
        entries = sorted(entries, key=lambda e: e["total_score"], reverse=True)
        result = []
        for rank, entry in enumerate(entries[:top_n], 1):
            result.append({"rank": rank, **entry})
        return result

    def _filter(
        self,
        challenge_id: Optional[str] = None,
        difficulty: Optional[str] = None,
        completed_only: bool = False,
    ) -> List[Dict[str, Any]]:
        entries = self._entries
        if challenge_id:
            entries = [e for e in entries if e.get("challenge_id") == challenge_id]
        if difficulty:
            entries = [e for e in entries if e.get("difficulty") == difficulty]
        if completed_only:
            entries = [e for e in entries if e.get("completed")]
        return entries

    def summary(self) -> Dict[str, Any]:
        completed = [e for e in self._entries if e.get("completed")]
        scores = [e["total_score"] for e in completed]
        return {
            "total_entries": len(self._entries),
            "completed_entries": len(completed),
            "best_score": max(scores) if scores else 0.0,
            "avg_score": round(sum(scores) / len(scores), 1) if scores else 0.0,
            "local_only": True,
            "public_leaderboard_enabled": False,
            "network_submission_enabled": False,
            "user_to_user_competition": False,
            "real_pnl_ranking": False,
            "broker_performance_ranking": False,
            "research_only": True,
            "no_real_orders": True,
        }
