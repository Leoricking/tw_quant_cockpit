"""
replay/challenge_summary.py — Challenge summary builder v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeSummaryBuilder:
    """
    Builds summaries for challenges: global, per-challenge, per-attempt,
    per-type, per-difficulty, per-mistake, daily, weekly.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def global_summary(self, attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build global summary across all challenges."""
        if not attempts:
            return self._empty_global()
        total = len(attempts)
        completed = sum(1 for a in attempts if a.get("status") == "COMPLETED")
        timed_out = sum(1 for a in attempts if a.get("status") == "TIMEOUT")
        cancelled = sum(1 for a in attempts if a.get("status") == "CANCELLED")
        scores = [a.get("process_score", 0.0) for a in attempts if a.get("process_score", 0.0) > 0]
        total_scores = [a.get("total_score", 0.0) for a in attempts if a.get("total_score", 0.0) > 0]
        hints = [a.get("hints_used", 0) for a in attempts]
        reviewed = sum(1 for a in attempts if a.get("review_status") == "FINALIZED")

        return {
            "total_attempts": total,
            "completed": completed,
            "timed_out": timed_out,
            "cancelled": cancelled,
            "avg_process_score": round(sum(scores) / len(scores), 1) if scores else 0.0,
            "avg_total_score": round(sum(total_scores) / len(total_scores), 1) if total_scores else 0.0,
            "hint_usage_avg": round(sum(hints) / len(hints), 1) if hints else 0.0,
            "review_completion": reviewed,
            "personal_best": round(max(total_scores), 1) if total_scores else 0.0,
            "insufficient_count": sum(1 for a in attempts if a.get("status") == "INSUFFICIENT"),
            "research_only": True,
            "no_real_orders": True,
            "real_mock_separated": True,
            "public_leaderboard_enabled": False,
            "network_submission_enabled": False,
        }

    def challenge_summary(self, challenge_id: str, attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summary for a specific challenge."""
        relevant = [a for a in attempts if a.get("challenge_id") == challenge_id]
        return {
            "challenge_id": challenge_id,
            **self.global_summary(relevant),
        }

    def attempt_summary(self, attempt: Dict[str, Any]) -> Dict[str, Any]:
        """Summary for a single attempt."""
        return {
            "attempt_id": attempt.get("attempt_id", ""),
            "challenge_id": attempt.get("challenge_id", ""),
            "status": attempt.get("status", ""),
            "process_score": attempt.get("process_score", 0.0),
            "total_score": attempt.get("total_score", 0.0),
            "hints_used": attempt.get("hints_used", 0),
            "active_elapsed_seconds": attempt.get("active_elapsed_seconds", 0.0),
            "review_status": attempt.get("review_status", "NOT_REVIEWED"),
            "research_only": True,
            "no_real_orders": True,
        }

    def type_summary(self, challenge_type: str, attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
        relevant = [a for a in attempts if a.get("challenge_type") == challenge_type]
        return {"challenge_type": challenge_type, **self.global_summary(relevant)}

    def difficulty_summary(self, difficulty: str, attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
        relevant = [a for a in attempts if a.get("difficulty") == difficulty]
        return {"difficulty": difficulty, **self.global_summary(relevant)}

    def _empty_global(self) -> Dict[str, Any]:
        return {
            "total_attempts": 0,
            "completed": 0,
            "timed_out": 0,
            "cancelled": 0,
            "avg_process_score": 0.0,
            "avg_total_score": 0.0,
            "hint_usage_avg": 0.0,
            "review_completion": 0,
            "personal_best": 0.0,
            "insufficient_count": 0,
            "research_only": True,
            "no_real_orders": True,
            "real_mock_separated": True,
            "public_leaderboard_enabled": False,
            "network_submission_enabled": False,
        }
