"""
portfolio/sizing/what_if_v151.py — Position Sizing What-If Engine v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] HYPOTHETICAL_ONLY, NO_LEDGER_WRITE, NO_ORDER_CREATED, NO_BROKER_CALL.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
WHAT_IF_LABELS = [
    "HYPOTHETICAL_ONLY",
    "NO_LEDGER_WRITE",
    "NO_ORDER_CREATED",
    "NO_BROKER_CALL",
    "RESEARCH_ONLY",
]


@dataclass
class WhatIfResult:
    baseline_proposal: Any
    scenario_proposal: Any
    scenario_overrides: Dict[str, Any]
    delta_quantity: Decimal
    delta_value: Decimal
    delta_risk: Decimal
    delta_weight: Decimal
    binding_constraint_change: bool
    labels: List[str] = field(default_factory=lambda: [
        "HYPOTHETICAL_ONLY", "NO_LEDGER_WRITE", "NO_ORDER_CREATED",
        "NO_BROKER_CALL", "RESEARCH_ONLY",
    ])
    research_only: bool = True
    order_created: bool = False
    persisted_to_ledger: bool = False
    broker_called: bool = False


class SizingWhatIfEngine:
    """
    Runs a baseline sizing and a scenario sizing, returns the delta.
    No writes anywhere. HYPOTHETICAL_ONLY.
    """

    RESEARCH_ONLY = True
    NO_LEDGER_WRITE = True
    NO_ORDER_CREATED = True
    NO_BROKER_CALL = True

    def run(self, baseline_request, scenario_overrides: Dict[str, Any], policy) -> WhatIfResult:
        """
        baseline_request: PositionSizingRequest
        scenario_overrides: dict of field overrides to apply to scenario request
        policy: PositionSizingPolicy
        Returns WhatIfResult.
        """
        from .query_v151 import PositionSizingQueryService
        svc = PositionSizingQueryService()

        baseline_proposal = svc.build_sizing_proposal(baseline_request, policy)

        # Build scenario request by applying overrides
        scenario_request = self._apply_overrides(baseline_request, scenario_overrides)
        scenario_proposal = svc.build_sizing_proposal(scenario_request, policy)

        # Compute deltas
        bq = baseline_proposal.proposed_final_quantity
        sq = scenario_proposal.proposed_final_quantity
        delta_quantity = sq - bq

        entry = baseline_request.planned_entry_price or baseline_request.reference_price or Decimal("0")
        delta_value = delta_quantity * entry

        b_risk = baseline_proposal.risk_amount
        s_risk = scenario_proposal.risk_amount
        delta_risk = s_risk - b_risk

        b_weight = baseline_proposal.estimated_final_weight
        s_weight = scenario_proposal.estimated_final_weight
        delta_weight = s_weight - b_weight

        binding_change = (
            baseline_proposal.binding_constraint != scenario_proposal.binding_constraint
        )

        return WhatIfResult(
            baseline_proposal=baseline_proposal,
            scenario_proposal=scenario_proposal,
            scenario_overrides=scenario_overrides,
            delta_quantity=delta_quantity,
            delta_value=delta_value,
            delta_risk=delta_risk,
            delta_weight=delta_weight,
            binding_constraint_change=binding_change,
        )

    @staticmethod
    def _apply_overrides(request, overrides: Dict[str, Any]):
        """Apply scenario overrides to create a new request object."""
        import copy
        from decimal import Decimal as D
        scenario = copy.copy(request)
        for k, v in overrides.items():
            if hasattr(scenario, k):
                # Convert numeric strings to Decimal
                if isinstance(v, str):
                    try:
                        v = D(v)
                    except Exception:
                        pass
                setattr(scenario, k, v)
        # New request_id for scenario
        scenario.request_id = request.request_id + "_WHATIF"
        return scenario
