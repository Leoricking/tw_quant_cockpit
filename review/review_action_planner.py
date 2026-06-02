"""
review/review_action_planner.py — ReviewActionPlanner (v0.4.7).

Converts ReviewItems and Scorecard into a prioritized Action Plan.

All suggested commands are research-only. No buy/sell/order suggestions.

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Dict, List

from review.review_schema import (
    ReviewItem,
    SEV_CRITICAL, SEV_BLOCKED, SEV_ERROR, SEV_WARNING, SEV_NOTICE,
    CAT_SAFETY, CAT_DATA, CAT_PROVIDER, CAT_MODEL, CAT_RULE,
    CAT_REPLAY, CAT_JOURNAL, CAT_EXPERIMENT,
    STATUS_OPEN,
)

logger = logging.getLogger(__name__)

# Action type constants
ACTION_FIX_DATA           = "fix_data"
ACTION_REVIEW_RULE        = "review_rule"
ACTION_PRACTICE_REPLAY    = "practice_replay"
ACTION_REVIEW_JOURNAL     = "review_journal"
ACTION_CHECK_PROVIDER     = "check_provider"
ACTION_RERUN_BACKTEST     = "rerun_backtest"
ACTION_INSPECT_MODEL_DRIFT = "inspect_model_drift"
ACTION_READ_REPORT        = "read_report"
ACTION_UPDATE_NOTES       = "update_notes"
ACTION_SAFETY_CHECK       = "safety_check"

ALL_ACTION_TYPES = [
    ACTION_FIX_DATA, ACTION_REVIEW_RULE, ACTION_PRACTICE_REPLAY,
    ACTION_REVIEW_JOURNAL, ACTION_CHECK_PROVIDER, ACTION_RERUN_BACKTEST,
    ACTION_INSPECT_MODEL_DRIFT, ACTION_READ_REPORT, ACTION_UPDATE_NOTES,
    ACTION_SAFETY_CHECK,
]

# Priority labels
PRIORITY_P0 = 0
PRIORITY_P1 = 1
PRIORITY_P2 = 2
PRIORITY_P3 = 3

# Action status
ACTION_STATUS_PENDING  = "PENDING"
ACTION_STATUS_DONE     = "DONE"
ACTION_STATUS_SKIPPED  = "SKIPPED"

# Allowed research-only suggested commands
_RESEARCH_COMMANDS = {
    ACTION_FIX_DATA:            "python main.py data-quality-gate --mode real",
    ACTION_CHECK_PROVIDER:      "python main.py provider-reliability --mode real",
    ACTION_REVIEW_RULE:         "python main.py rule-governance --mode real",
    ACTION_REVIEW_JOURNAL:      "python main.py journal-summary",
    ACTION_PRACTICE_REPLAY:     "python main.py intraday-replay --mode real",
    ACTION_INSPECT_MODEL_DRIFT: "python main.py model-monitoring --mode real",
    ACTION_RERUN_BACKTEST:      "python main.py hardened-backtest --mode real",
    ACTION_READ_REPORT:         "python main.py auto-report --mode real --profile daily",
    ACTION_UPDATE_NOTES:        "python main.py journal-summary",
    ACTION_SAFETY_CHECK:        "python main.py stable-release-check --mode real",
}

# Forbidden keywords in suggested commands (safety guard)
_FORBIDDEN_KEYWORDS = ["buy", "sell", "submit_order", "place_order", "broker", "auto_trade", "real_order"]


def _safe_command(cmd: str) -> str:
    """Strip or block any forbidden trading command."""
    for kw in _FORBIDDEN_KEYWORDS:
        if kw in cmd.lower():
            return "# BLOCKED: no trading commands allowed"
    return cmd


class ReviewActionPlanner:
    """
    Builds a prioritized action plan from ReviewItems and Scorecard.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      Suggested commands are research-only. No buy/sell/order suggestions.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(self):
        pass

    def build_action_plan(
        self,
        review_items: List[ReviewItem],
        scorecard: dict,
    ) -> List[dict]:
        """
        Convert review items and scorecard into a prioritized action plan.

        Returns list of action dicts. Sorted by priority (P0 first).
        """
        actions: List[dict] = []

        for item in review_items:
            if not item.action_required:
                continue
            action_type, priority = self._classify(item, scorecard)
            cmd = _safe_command(
                item.recommended_action or _RESEARCH_COMMANDS.get(action_type, "")
            )
            actions.append(self._make_action(
                action_type=action_type,
                priority=priority,
                title=item.title,
                description=item.summary,
                source_review_id=item.review_id,
                related_module=item.source_module,
                suggested_command=cmd,
                due_type="daily" if item.priority <= 1 else "weekly",
            ))

        # Add scorecard-driven actions
        actions += self._scorecard_actions(scorecard)

        # Sort by priority
        actions.sort(key=lambda a: a["priority"])
        return actions

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _classify(self, item: ReviewItem, scorecard: dict):
        """Return (action_type, priority) for a ReviewItem."""
        sev = item.severity
        cat = item.category

        if cat == CAT_SAFETY or sev in (SEV_CRITICAL, SEV_BLOCKED):
            return ACTION_SAFETY_CHECK, PRIORITY_P0

        if cat == CAT_DATA:
            return ACTION_FIX_DATA, PRIORITY_P1

        if cat == CAT_PROVIDER:
            return ACTION_CHECK_PROVIDER, PRIORITY_P1

        if cat == CAT_MODEL:
            return ACTION_INSPECT_MODEL_DRIFT, PRIORITY_P2

        if cat == CAT_RULE:
            return ACTION_REVIEW_RULE, PRIORITY_P2

        if cat == CAT_REPLAY:
            return ACTION_PRACTICE_REPLAY, PRIORITY_P2

        if cat == CAT_JOURNAL:
            return ACTION_REVIEW_JOURNAL, PRIORITY_P2

        if cat == CAT_EXPERIMENT:
            return ACTION_READ_REPORT, PRIORITY_P3

        return ACTION_READ_REPORT, PRIORITY_P3

    def _scorecard_actions(self, scorecard: dict) -> List[dict]:
        """Generate actions based on scorecard grades."""
        actions = []

        if scorecard.get("data_health_grade", "UNKNOWN") in ("WEAK", "BLOCKED"):
            actions.append(self._make_action(
                action_type=ACTION_FIX_DATA,
                priority=PRIORITY_P1,
                title="Data health weak — run data quality gate",
                description="Data health score is low. Fix data quality issues.",
                suggested_command=_RESEARCH_COMMANDS[ACTION_FIX_DATA],
            ))

        if scorecard.get("replay_training_grade", "UNKNOWN") in ("WEAK", "BLOCKED", "PARTIAL"):
            actions.append(self._make_action(
                action_type=ACTION_PRACTICE_REPLAY,
                priority=PRIORITY_P2,
                title="Replay training overdue",
                description="Practice intraday replay scenarios: fake breakout, VWAP, opening range.",
                suggested_command=_RESEARCH_COMMANDS[ACTION_PRACTICE_REPLAY],
            ))

        if scorecard.get("journal_completion_grade", "UNKNOWN") in ("WEAK", "BLOCKED"):
            actions.append(self._make_action(
                action_type=ACTION_REVIEW_JOURNAL,
                priority=PRIORITY_P2,
                title="Journal completion low — review journal",
                description="Many journal entries are pending review.",
                suggested_command=_RESEARCH_COMMANDS[ACTION_REVIEW_JOURNAL],
            ))

        return actions

    @staticmethod
    def _make_action(
        action_type:      str,
        priority:         int,
        title:            str,
        description:      str,
        source_review_id: str = "",
        related_module:   str = "",
        suggested_command: str = "",
        due_type:         str = "daily",
        status:           str = ACTION_STATUS_PENDING,
    ) -> dict:
        return {
            "action_id":        str(uuid.uuid4())[:8],
            "created_at":       datetime.now().isoformat(timespec="seconds"),
            "priority":         priority,
            "action_type":      action_type,
            "title":            title,
            "description":      description,
            "source_review_id": source_review_id,
            "related_module":   related_module,
            "suggested_command": _safe_command(suggested_command),
            "due_type":         due_type,
            "status":           status,
            # Safety
            "no_real_orders":     True,
            "production_blocked": True,
        }
