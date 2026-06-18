"""
replay/challenge_objectives.py — Challenge objective types v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ObjectiveType:
    COMPLETE_DECISION           = "COMPLETE_DECISION"
    AVOID_CHASE                 = "AVOID_CHASE"
    RESPECT_SUPPORT             = "RESPECT_SUPPORT"
    WAIT_FOR_CONFIRMATION       = "WAIT_FOR_CONFIRMATION"
    BUILD_RISK_PLAN             = "BUILD_RISK_PLAN"
    IDENTIFY_CONFLICT           = "IDENTIFY_CONFLICT"
    IDENTIFY_PARTIAL_BAR        = "IDENTIFY_PARTIAL_BAR"
    IDENTIFY_DATA_INSUFFICIENCY = "IDENTIFY_DATA_INSUFFICIENCY"
    COMPLETE_JOURNAL            = "COMPLETE_JOURNAL"
    PRESERVE_DISCIPLINE         = "PRESERVE_DISCIPLINE"

    ALL = [
        COMPLETE_DECISION, AVOID_CHASE, RESPECT_SUPPORT,
        WAIT_FOR_CONFIRMATION, BUILD_RISK_PLAN, IDENTIFY_CONFLICT,
        IDENTIFY_PARTIAL_BAR, IDENTIFY_DATA_INSUFFICIENCY,
        COMPLETE_JOURNAL, PRESERVE_DISCIPLINE,
    ]


def build_objective(
    objective_type: str,
    description: str = "",
    required: bool = True,
    params: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Build an objective definition dict."""
    return {
        "objective_type": objective_type,
        "description": description or objective_type,
        "required": required,
        "params": params or {},
        "research_only": True,
        "no_real_orders": True,
    }


def evaluate_objective(
    objective: Dict[str, Any],
    attempt_actions: List[Dict[str, Any]],
    attempt: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Evaluate whether an objective is completed."""
    obj_type = objective.get("objective_type", "")
    action_types = [a.get("action_type", "") for a in attempt_actions]
    completed = False
    reason = ""

    if obj_type == ObjectiveType.COMPLETE_DECISION:
        decision_actions = [a for a in attempt_actions if a.get("action_type", "").startswith("DECIDE_")]
        completed = len(decision_actions) > 0
        reason = "Decision made" if completed else "No decision recorded"
    elif obj_type == ObjectiveType.BUILD_RISK_PLAN:
        completed = "WRITE_RISK_PLAN" in action_types
        reason = "Risk plan built" if completed else "Risk plan not built"
    elif obj_type == ObjectiveType.COMPLETE_JOURNAL:
        completed = (
            "WRITE_THESIS" in action_types
            and "WRITE_RISK_PLAN" in action_types
            and "WRITE_CHECKLIST" in action_types
        )
        reason = "Journal complete" if completed else "Journal incomplete"
    elif obj_type == ObjectiveType.WAIT_FOR_CONFIRMATION:
        completed = "WRITE_THESIS" in action_types and any(
            a.get("action_type") in ("DECIDE_WAIT", "DECIDE_SKIP") for a in attempt_actions
        )
        reason = "Waited for confirmation" if completed else "Did not wait"
    elif obj_type == ObjectiveType.AVOID_CHASE:
        # Evaluated based on context — default pass if WAIT/SKIP chosen
        completed = any(
            a.get("action_type") in ("DECIDE_WAIT", "DECIDE_SKIP") for a in attempt_actions
        )
        reason = "Chase avoided" if completed else "Chase risk — evaluated in review"
    else:
        completed = False
        reason = f"Objective {obj_type}: not yet evaluated"

    return {
        "objective_type": obj_type,
        "completed": completed,
        "reason": reason,
        "research_only": True,
    }
