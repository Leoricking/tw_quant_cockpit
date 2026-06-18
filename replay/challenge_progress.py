"""
replay/challenge_progress.py — Challenge progress tracker v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeProgressTracker:
    """
    Tracks challenge progress metrics.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._attempts: List[Dict[str, Any]] = []

    def record_attempt(self, attempt: Dict[str, Any]) -> None:
        """Record an attempt for progress tracking."""
        self._attempts.append({
            "attempt_id": attempt.get("attempt_id", ""),
            "challenge_id": attempt.get("challenge_id", ""),
            "challenge_type": attempt.get("challenge_type", ""),
            "difficulty": attempt.get("difficulty", ""),
            "status": attempt.get("status", ""),
            "process_score": attempt.get("process_score", 0.0),
            "total_score": attempt.get("total_score", 0.0),
            "hints_used": attempt.get("hints_used", 0),
            "active_elapsed_seconds": attempt.get("active_elapsed_seconds", 0.0),
            "finished_at": attempt.get("finished_at", ""),
            "review_status": attempt.get("review_status", "NOT_REVIEWED"),
        })

    def get_summary(self) -> Dict[str, Any]:
        """Return overall progress summary."""
        if not self._attempts:
            return self._empty_summary()

        attempted = len(self._attempts)
        completed = sum(1 for a in self._attempts if a["status"] == "COMPLETED")
        timed_out = sum(1 for a in self._attempts if a["status"] == "TIMEOUT")
        cancelled = sum(1 for a in self._attempts if a["status"] == "CANCELLED")

        scores = [a["process_score"] for a in self._attempts if a["process_score"] > 0]
        total_scores = [a["total_score"] for a in self._attempts if a["total_score"] > 0]
        avg_process = sum(scores) / len(scores) if scores else 0.0
        avg_total = sum(total_scores) / len(total_scores) if total_scores else 0.0
        best_score = max(total_scores) if total_scores else 0.0

        reviewed = sum(1 for a in self._attempts if a["review_status"] == "FINALIZED")

        return {
            "challenges_attempted": attempted,
            "challenges_completed": completed,
            "challenges_timed_out": timed_out,
            "challenges_cancelled": cancelled,
            "avg_process_score": round(avg_process, 1),
            "avg_total_score": round(avg_total, 1),
            "personal_best": round(best_score, 1),
            "review_completion": reviewed,
            "research_only": True,
            "no_real_orders": True,
        }

    def get_score_trend(self) -> List[float]:
        """Return process score trend."""
        return [a["process_score"] for a in self._attempts]

    def get_difficulty_progression(self) -> Dict[str, int]:
        """Return count of attempts per difficulty."""
        result: Dict[str, int] = {}
        for a in self._attempts:
            d = a.get("difficulty", "UNKNOWN")
            result[d] = result.get(d, 0) + 1
        return result

    def _empty_summary(self) -> Dict[str, Any]:
        return {
            "challenges_attempted": 0,
            "challenges_completed": 0,
            "challenges_timed_out": 0,
            "challenges_cancelled": 0,
            "avg_process_score": 0.0,
            "avg_total_score": 0.0,
            "personal_best": 0.0,
            "review_completion": 0,
            "research_only": True,
            "no_real_orders": True,
        }
