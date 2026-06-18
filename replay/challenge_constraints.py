"""
replay/challenge_constraints.py — Challenge constraint definitions v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_constraints(
    max_duration_seconds: Optional[int] = None,
    max_steps: Optional[int] = None,
    max_actions: Optional[int] = None,
    max_hints: int = 3,
    enabled_timeframes: Optional[List[str]] = None,
    visible_modules: Optional[List[str]] = None,
    hidden_modules: Optional[List[str]] = None,
    allowed_decisions: Optional[List[str]] = None,
    required_review_fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a constraints dict for a challenge."""
    return {
        "max_duration_seconds": max_duration_seconds,
        "max_steps": max_steps,
        "max_actions": max_actions,
        "max_hints": max_hints,
        "enabled_timeframes": enabled_timeframes or ["D1"],
        "visible_modules": visible_modules or [],
        "hidden_modules": hidden_modules or [],
        "allowed_decisions": allowed_decisions or [
            "DECIDE_WAIT", "DECIDE_ENTER", "DECIDE_ADD",
            "DECIDE_REDUCE", "DECIDE_EXIT", "DECIDE_SKIP",
        ],
        "required_review_fields": required_review_fields or ["thesis", "risk_plan"],
        "research_only": True,
        "no_real_orders": True,
        "future_firewall": True,
    }


def check_constraints(
    constraints: Dict[str, Any],
    attempt: Dict[str, Any],
    elapsed_seconds: float = 0.0,
) -> Dict[str, Any]:
    """Check if attempt is within constraints. Returns violations."""
    violations = []
    warnings = []

    max_dur = constraints.get("max_duration_seconds")
    if max_dur is not None and elapsed_seconds > max_dur:
        violations.append(f"Duration exceeded: {elapsed_seconds:.0f}s > {max_dur}s")

    max_actions = constraints.get("max_actions")
    actions_count = len(attempt.get("actions", []))
    if max_actions is not None and actions_count > max_actions:
        violations.append(f"Action limit exceeded: {actions_count} > {max_actions}")

    max_hints = constraints.get("max_hints", 3)
    hints_used = attempt.get("hints_used", 0)
    if hints_used > max_hints:
        violations.append(f"Hint limit exceeded: {hints_used} > {max_hints}")

    max_steps = constraints.get("max_steps")
    steps_used = attempt.get("steps_used", 0)
    if max_steps is not None and steps_used > max_steps:
        violations.append(f"Step limit exceeded: {steps_used} > {max_steps}")

    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "warnings": warnings,
        "research_only": True,
    }
