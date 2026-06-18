"""
reports/replay_challenge_summary_report.py — Challenge summary report v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_summary_report(
    attempts: List[Dict[str, Any]],
    date: str = None,
) -> Dict[str, Any]:
    """Build a challenge summary report."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    total = len(attempts)
    completed = sum(1 for a in attempts if a.get("status") == "COMPLETED")
    timed_out = sum(1 for a in attempts if a.get("status") == "TIMEOUT")
    cancelled = sum(1 for a in attempts if a.get("status") == "CANCELLED")

    scores = [a.get("process_score", 0.0) for a in attempts if a.get("process_score", 0.0) > 0]
    total_scores = [a.get("total_score", 0.0) for a in attempts if a.get("total_score", 0.0) > 0]

    return {
        "report_type": "CHALLENGE_SUMMARY",
        "report_date": date,
        "total_attempts": total,
        "completed": completed,
        "timed_out": timed_out,
        "cancelled": cancelled,
        "avg_process_score": round(sum(scores) / len(scores), 1) if scores else 0.0,
        "avg_total_score": round(sum(total_scores) / len(total_scores), 1) if total_scores else 0.0,
        "personal_best": round(max(total_scores), 1) if total_scores else 0.0,
        "public_leaderboard_enabled": False,
        "network_submission_enabled": False,
        "research_only": True,
        "no_real_orders": True,
    }
