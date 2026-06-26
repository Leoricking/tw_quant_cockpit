"""
Operational State Mapping v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import OperationalStatus


S = OperationalStatus


def resolve_composite_status(
    market_data:    S,
    paper_trading:  S,
    paper_strategy: S,
    *,
    safety_blocked: bool = False,
) -> Tuple[S, str]:
    """Deterministic composite status from three session statuses."""

    if safety_blocked:
        return S.BLOCKED, "Safety violation — composite BLOCKED"

    statuses = [market_data, paper_trading, paper_strategy]

    # Any BLOCKED → BLOCKED
    if S.BLOCKED in statuses:
        return S.BLOCKED, "At least one session BLOCKED"

    # Any FAILED → composite FAILED
    if S.FAILED in statuses:
        return S.FAILED, "At least one session FAILED"

    # Any HALTED → HALTED
    if S.HALTED in statuses:
        return S.HALTED, "At least one session HALTED"

    # Recovering
    if S.RECOVERING in statuses:
        return S.RECOVERING, "Recovery in progress"

    # RECOVERED but not RESUMED → keep RECOVERED
    if S.RECOVERED in statuses and S.RUNNING not in statuses:
        return S.RECOVERED, "Awaiting explicit resume"

    # Completing
    if S.COMPLETING in statuses:
        return S.COMPLETING, "Session completing"

    # All COMPLETED
    if all(s == S.COMPLETED for s in statuses):
        return S.COMPLETED, "All sessions completed"

    # Any PAUSED
    if S.PAUSED in statuses:
        return S.PAUSED, "At least one session PAUSED"

    # Any PAUSING
    if S.PAUSING in statuses:
        return S.PAUSING, "At least one session PAUSING"

    # Any HALTING
    if S.HALTING in statuses:
        return S.HALTING, "At least one session HALTING"

    # Any DEGRADED
    if S.DEGRADED in statuses:
        return S.DEGRADED, "At least one session DEGRADED"

    # All RUNNING
    if all(s == S.RUNNING for s in statuses):
        return S.RUNNING, "All sessions running"

    # Any STARTING
    if S.STARTING in statuses:
        return S.STARTING, "Startup in progress"

    # Dependency mismatch / inconsistent
    known_up = {S.RUNNING, S.STARTING, S.RECOVERING, S.RECOVERED}
    if market_data not in known_up and paper_trading == S.RUNNING:
        return S.DEGRADED, "Dependency mismatch: market data not running but paper trading is"

    # Unknown combination
    if S.UNINITIALIZED in statuses:
        return S.UNINITIALIZED, "Not yet initialized"

    return S.BLOCKED, f"Unknown state combination: {market_data}/{paper_trading}/{paper_strategy}"


def explain_composite_status(
    market_data:    S,
    paper_trading:  S,
    paper_strategy: S,
    *,
    safety_blocked: bool = False,
) -> Dict[str, object]:
    status, reason = resolve_composite_status(
        market_data, paper_trading, paper_strategy,
        safety_blocked=safety_blocked,
    )
    return {
        "composite_status":    str(status),
        "reason":              reason,
        "market_data":         str(market_data),
        "paper_trading":       str(paper_trading),
        "paper_strategy":      str(paper_strategy),
        "safety_blocked":      safety_blocked,
        "deterministic":       True,
        "optimistic_override": False,
    }


__all__ = ["resolve_composite_status", "explain_composite_status"]
