"""
replay/challenge_result.py — Challenge result builder v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ChallengeResultBuilder:
    """
    Build ReplayChallengeResult from completed attempt data.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def build_result(
        self,
        attempt: Dict[str, Any],
        challenge: Dict[str, Any],
        score: Optional[Dict[str, Any]] = None,
        objectives_status: Optional[List[Dict[str, Any]]] = None,
        rules_status: Optional[List[Dict[str, Any]]] = None,
        suggested_mistakes: Optional[List[str]] = None,
        badges: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build a challenge result dict."""
        from replay.challenge_schema import ReplayChallengeResult, _now_utc, _new_id

        status = attempt.get("status", "UNKNOWN")
        completed = status == "COMPLETED"
        timed_out = status == "TIMEOUT"
        cancelled = status == "CANCELLED"

        objs = objectives_status or []
        obj_completed = [o["objective_type"] for o in objs if o.get("completed")]
        obj_failed = [o["objective_type"] for o in objs if not o.get("completed")]

        rules = rules_status or []
        rules_followed = [r["rule_type"] for r in rules if r.get("passed")]
        rules_violated = [r["rule_type"] for r in rules if not r.get("passed")]

        score_data = score or {}
        score_obj = score_data.get("score")
        process_score = float(getattr(score_obj, "process_score", 0.0)) if score_obj else 0.0
        total_score = float(getattr(score_obj, "total_score", 0.0)) if score_obj else 0.0

        result = ReplayChallengeResult(
            result_id=_new_id("CRS-"),
            attempt_id=attempt.get("attempt_id", ""),
            challenge_id=attempt.get("challenge_id", ""),
            completed=completed,
            timed_out=timed_out,
            cancelled=cancelled,
            objectives_completed=obj_completed,
            objectives_failed=obj_failed,
            rules_followed=rules_followed,
            rules_violated=rules_violated,
            hints_used=attempt.get("hints_used", 0),
            mistakes_suggested=suggested_mistakes or [],
            process_score=round(process_score, 1),
            total_score=round(total_score, 1),
            personal_best=False,  # determined by leaderboard comparison
            badges_awarded=badges or [],
            review_required=True,
            generated_at=_now_utc(),
        )
        return result.to_dict()
