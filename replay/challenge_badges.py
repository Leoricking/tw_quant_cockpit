"""
replay/challenge_badges.py — Challenge badges v1.2.7

[!] Badges are training encouragement ONLY.
[!] Badges do NOT represent investment or profit ability.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
BADGES_REPRESENT_INVESTMENT_ABILITY = False
BADGES_REPRESENT_PROFIT_ABILITY = False


class BadgeType:
    FIRST_CHALLENGE              = "FIRST_CHALLENGE"
    FIRST_COMPLETE               = "FIRST_COMPLETE"
    PROCESS_FIRST                = "PROCESS_FIRST"
    NO_HINT_COMPLETE             = "NO_HINT_COMPLETE"
    JOURNAL_DISCIPLINE           = "JOURNAL_DISCIPLINE"
    RISK_PLANNER                 = "RISK_PLANNER"
    NO_CHASE_DISCIPLINE          = "NO_CHASE_DISCIPLINE"
    MTF_AWARENESS                = "MTF_AWARENESS"
    STRATEGY_CONFLICT_REVIEWER   = "STRATEGY_CONFLICT_REVIEWER"
    POINT_IN_TIME_GUARDIAN       = "POINT_IN_TIME_GUARDIAN"
    TEN_CHALLENGES               = "TEN_CHALLENGES"
    FIFTY_CHALLENGES             = "FIFTY_CHALLENGES"

    ALL = [
        FIRST_CHALLENGE, FIRST_COMPLETE, PROCESS_FIRST, NO_HINT_COMPLETE,
        JOURNAL_DISCIPLINE, RISK_PLANNER, NO_CHASE_DISCIPLINE,
        MTF_AWARENESS, STRATEGY_CONFLICT_REVIEWER, POINT_IN_TIME_GUARDIAN,
        TEN_CHALLENGES, FIFTY_CHALLENGES,
    ]


BADGE_DESCRIPTIONS: Dict[str, str] = {
    BadgeType.FIRST_CHALLENGE: "Completed your first challenge attempt.",
    BadgeType.FIRST_COMPLETE:  "Completed your first challenge.",
    BadgeType.PROCESS_FIRST:   "Process score >= 80 on first attempt.",
    BadgeType.NO_HINT_COMPLETE: "Completed a challenge without using any hints.",
    BadgeType.JOURNAL_DISCIPLINE: "Completed thesis, risk plan, and checklist in a challenge.",
    BadgeType.RISK_PLANNER:    "Built a complete risk plan in every attempt this week.",
    BadgeType.NO_CHASE_DISCIPLINE: "Passed a No Chase challenge.",
    BadgeType.MTF_AWARENESS:   "Reviewed all timeframes before deciding.",
    BadgeType.STRATEGY_CONFLICT_REVIEWER: "Completed a Strategy Conflict challenge.",
    BadgeType.POINT_IN_TIME_GUARDIAN: "Passed a Point-in-Time Integrity challenge.",
    BadgeType.TEN_CHALLENGES:  "Completed 10 challenges.",
    BadgeType.FIFTY_CHALLENGES: "Completed 50 challenges.",
}


class ChallengeBadgeManager:
    """
    Awards training encouragement badges.

    [!] Badges are training encouragement ONLY.
    [!] Badges do NOT represent investment or profit ability.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    BADGES_REPRESENT_INVESTMENT_ABILITY = False
    BADGES_REPRESENT_PROFIT_ABILITY = False

    def __init__(self) -> None:
        self._awarded: List[Dict[str, Any]] = []

    def evaluate(self, attempt: Dict[str, Any], total_completed: int = 0) -> List[str]:
        """Evaluate which badges to award for an attempt."""
        from replay.challenge_schema import _now_utc
        awarded = []
        action_types = [a.get("action_type", "") for a in attempt.get("actions", [])]

        if total_completed == 0:
            awarded.append(BadgeType.FIRST_CHALLENGE)
        if attempt.get("status") == "COMPLETED":
            if total_completed == 0:
                awarded.append(BadgeType.FIRST_COMPLETE)
            if attempt.get("hints_used", 0) == 0:
                awarded.append(BadgeType.NO_HINT_COMPLETE)
            if ("WRITE_THESIS" in action_types and "WRITE_RISK_PLAN" in action_types
                    and "WRITE_CHECKLIST" in action_types):
                awarded.append(BadgeType.JOURNAL_DISCIPLINE)
            if "WRITE_RISK_PLAN" in action_types:
                awarded.append(BadgeType.RISK_PLANNER)
            if "VIEW_TIMEFRAME" in action_types:
                awarded.append(BadgeType.MTF_AWARENESS)
            ctype = attempt.get("challenge_type", "")
            if ctype == "NO_CHASE":
                awarded.append(BadgeType.NO_CHASE_DISCIPLINE)
            if ctype == "STRATEGY_CONFLICT":
                awarded.append(BadgeType.STRATEGY_CONFLICT_REVIEWER)
            if ctype == "POINT_IN_TIME":
                awarded.append(BadgeType.POINT_IN_TIME_GUARDIAN)
            if attempt.get("process_score", 0.0) >= 80 and total_completed == 0:
                awarded.append(BadgeType.PROCESS_FIRST)
            if total_completed + 1 == 10:
                awarded.append(BadgeType.TEN_CHALLENGES)
            if total_completed + 1 == 50:
                awarded.append(BadgeType.FIFTY_CHALLENGES)

        for badge in awarded:
            self._awarded.append({
                "badge": badge,
                "description": BADGE_DESCRIPTIONS.get(badge, ""),
                "attempt_id": attempt.get("attempt_id", ""),
                "awarded_at": _now_utc(),
                "training_only": True,
                "investment_ability": False,
            })
        return awarded

    def get_all_badges(self) -> List[Dict[str, Any]]:
        return list(self._awarded)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_badges": len(self._awarded),
            "badges": [b["badge"] for b in self._awarded],
            "training_encouragement_only": True,
            "investment_ability": False,
            "profit_ability": False,
            "research_only": True,
            "no_real_orders": True,
        }
