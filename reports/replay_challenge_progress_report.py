"""
reports/replay_challenge_progress_report.py — Challenge progress report v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_progress_report(
    progress: Dict[str, Any],
    badges: List[str] = None,
    streaks: Dict[str, int] = None,
    date: str = None,
) -> Dict[str, Any]:
    """Build a challenge progress report."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return {
        "report_type": "CHALLENGE_PROGRESS",
        "report_date": date,
        "challenges_attempted": progress.get("challenges_attempted", 0),
        "challenges_completed": progress.get("challenges_completed", 0),
        "challenges_timed_out": progress.get("challenges_timed_out", 0),
        "challenges_cancelled": progress.get("challenges_cancelled", 0),
        "avg_process_score": progress.get("avg_process_score", 0.0),
        "personal_best": progress.get("personal_best", 0.0),
        "badges": badges or [],
        "streaks": streaks or {},
        "review_completion": progress.get("review_completion", 0),
        "badges_training_only": True,
        "badges_not_investment_ability": True,
        "research_only": True,
        "no_real_orders": True,
    }
