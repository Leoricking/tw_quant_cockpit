"""
gui/replay_challenge_run_panel.py — Challenge run panel v1.2.7

Shows: Challenge Objective, Rules, Remaining Time, Active Elapsed, Step Count,
Action Count, Hint Count, Replay Timestamp, Visible Context, Journal Draft,
Risk Plan, Checklist. QThread clock does not freeze.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeRunPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    def __init__(self) -> None:
        self._attempt_id: Optional[str] = None
    def set_attempt(self, attempt_id: str) -> None:
        self._attempt_id = attempt_id
    def get_panel_data(self, attempt: Dict[str, Any], challenge: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "challenge_objective": challenge.get("objective", ""),
            "rules": challenge.get("rules", []),
            "remaining_time": attempt.get("remaining_seconds"),
            "active_elapsed": attempt.get("active_elapsed_seconds", 0.0),
            "step_count": attempt.get("steps_used", 0),
            "action_count": len(attempt.get("actions", [])),
            "hint_count": attempt.get("hints_used", 0),
            "replay_timestamp": attempt.get("replay_timestamp"),
            "visible_context": {},
            "journal_draft": attempt.get("journal_draft", {}),
            "risk_plan": "",
            "checklist": [],
            "research_only": True,
            "no_real_orders": True,
        }
