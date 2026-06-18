"""
replay/challenge_streak.py — Challenge streak tracker v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeStreakTracker:
    """
    Tracks challenge completion streaks.

    Streaks: daily_training, weekly_challenge_completion, discipline,
             no_chase, journal_completion.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._streaks: Dict[str, int] = {
            "daily_training": 0,
            "weekly_challenge_completion": 0,
            "discipline": 0,
            "no_chase": 0,
            "journal_completion": 0,
        }
        self._history: List[Dict[str, Any]] = []

    def record_attempt(self, attempt: Dict[str, Any]) -> None:
        """Update streaks from a completed attempt."""
        status = attempt.get("status", "")
        if status == "COMPLETED":
            self._streaks["daily_training"] += 1
            self._streaks["weekly_challenge_completion"] += 1
            actions = attempt.get("actions", [])
            types = [a.get("action_type", "") for a in actions]
            if "WRITE_THESIS" in types and "WRITE_RISK_PLAN" in types and "WRITE_CHECKLIST" in types:
                self._streaks["journal_completion"] += 1
            challenge_type = attempt.get("challenge_type", "")
            if challenge_type == "NO_CHASE":
                self._streaks["no_chase"] += 1
                self._streaks["discipline"] += 1
        elif status in ("TIMEOUT", "CANCELLED"):
            self._streaks["daily_training"] = 0

    def get_all_streaks(self) -> Dict[str, Any]:
        return {
            **self._streaks,
            "research_only": True,
            "no_real_orders": True,
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "streaks": self._streaks,
            "research_only": True,
            "no_real_orders": True,
        }
