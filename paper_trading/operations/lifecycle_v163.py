"""
Session Lifecycle v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Set, Tuple

from paper_trading.operations.enums_v163 import OperationalStatus

S = OperationalStatus

VALID_TRANSITIONS: dict = {
    S.UNINITIALIZED: {S.STARTING, S.BLOCKED},
    S.STARTING:      {S.RUNNING, S.FAILED, S.BLOCKED},
    S.RUNNING:       {S.PAUSING, S.HALTING, S.DEGRADED, S.COMPLETING, S.FAILED, S.BLOCKED},
    S.DEGRADED:      {S.RUNNING, S.PAUSING, S.HALTING, S.FAILED, S.BLOCKED},
    S.PAUSING:       {S.PAUSED, S.FAILED},
    S.PAUSED:        {S.RUNNING, S.RECOVERING, S.HALTING, S.BLOCKED},
    S.HALTING:       {S.HALTED, S.FAILED},
    S.HALTED:        {S.RECOVERING, S.BLOCKED},
    S.RECOVERING:    {S.RECOVERED, S.FAILED, S.HALTED},
    S.RECOVERED:     {S.RUNNING, S.PAUSED, S.BLOCKED},
    S.COMPLETING:    {S.COMPLETED, S.FAILED},
    S.COMPLETED:     set(),
    S.FAILED:        {S.RECOVERING, S.BLOCKED},
    S.BLOCKED:       set(),
}


def is_valid_transition(current: S, target: S) -> bool:
    return target in VALID_TRANSITIONS.get(current, set())


def validate_transition(current: S, target: S) -> Tuple[bool, str]:
    if is_valid_transition(current, target):
        return True, f"{current} → {target} OK"
    return False, f"Invalid transition {current} → {target} — BLOCKED"


__all__ = ["VALID_TRANSITIONS", "is_valid_transition", "validate_transition"]
