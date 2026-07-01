"""
paper_trading/multi_session/capital_allocator_v166.py — Capital Allocator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Paper budget only. No real capital movement. No bank API. No auto reallocation.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import CoordinationOutcome, SessionPriority
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_REAL_CAPITAL_MOVEMENT = True
NO_AUTO_REALLOCATION = True
PAPER_CAPITAL_ONLY = True


class CapitalAllocator:
    """Paper capital budget allocator. No real funds."""

    def allocate(
        self,
        sessions: List[SessionDescriptor],
        global_paper_budget: float,
        rules: Dict[str, Any],
    ) -> Dict[str, Any]:
        requested = sum(s.capital_budget for s in sessions)
        allow_partial = rules.get("partial_grant_allowed", True)
        outcome = CoordinationOutcome.PASS
        warnings: List[str] = []
        allocations: Dict[str, float] = {}

        if requested > global_paper_budget:
            if allow_partial:
                ratio = global_paper_budget / requested
                for s in sessions:
                    allocations[s.session_id] = s.capital_budget * ratio
                outcome = CoordinationOutcome.WARN
                warnings.append(f"Partial allocation: requested {requested:.0f} > budget {global_paper_budget:.0f}")
            else:
                outcome = CoordinationOutcome.BLOCK
                warnings.append(f"Capital overallocation: {requested:.0f} > {global_paper_budget:.0f}")
        else:
            for s in sessions:
                allocations[s.session_id] = s.capital_budget

        return {
            "outcome": outcome.value,
            "requested": requested,
            "budget": global_paper_budget,
            "allocations": allocations,
            "warnings": warnings,
        }

    def reconcile(
        self,
        allocations: Dict[str, float],
        actuals: Dict[str, float],
    ) -> Dict[str, Any]:
        mismatches = {
            sid: {"allocated": allocations.get(sid), "actual": actuals.get(sid)}
            for sid in set(list(allocations.keys()) + list(actuals.keys()))
            if abs((allocations.get(sid, 0) or 0) - (actuals.get(sid, 0) or 0)) > 0.01
        }
        return {"reconciled": len(mismatches) == 0, "mismatches": mismatches}
