"""
gui/replay_challenge_progress_panel.py — Challenge progress panel v1.2.7

Shows: Attempts, Completed, Personal Best, Score Trend, Mistake Recurrence, Badges, Streak.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeProgressPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    def get_display(self, progress: Dict[str, Any], badges: list, streaks: dict) -> Dict[str, Any]:
        return {
            "attempts": progress.get("challenges_attempted", 0),
            "completed": progress.get("challenges_completed", 0),
            "personal_best": progress.get("personal_best", 0.0),
            "score_trend": progress.get("score_trend", []),
            "mistake_recurrence": progress.get("mistake_recurrence", {}),
            "badges": badges,
            "streaks": streaks,
            "badges_training_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
