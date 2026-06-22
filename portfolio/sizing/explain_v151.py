"""
portfolio/sizing/explain_v151.py — Position Sizing Explainer v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Produces a human-readable step-by-step calculation explanation.
"""
from __future__ import annotations

from typing import Any, Dict

RESEARCH_ONLY = True


class PositionSizingExplainer:
    """
    Generates human-readable explanation for a PositionSizingProposal.
    """

    RESEARCH_ONLY = True

    def explain(self, proposal) -> Dict[str, Any]:
        """
        Returns a dict with step-by-step explanation of the sizing result.
        """
        steps = []

        steps.append({
            "step": 1,
            "name": "raw_sizing",
            "description": f"Method: {proposal.method}",
            "raw_quantity": str(proposal.raw_quantity),
            "reference_price": str(proposal.reference_price),
        })

        for i, c in enumerate(proposal.constraints, start=2):
            steps.append({
                "step": i,
                "name": f"constraint_{c.get('constraint_type', 'UNKNOWN')}",
                "before": str(c.get("before_quantity", "")),
                "after": str(c.get("after_quantity", "")),
                "applied": c.get("applied", False),
                "reason": c.get("reason", ""),
                "severity": c.get("severity", ""),
            })

        result = {
            "proposal_id": proposal.proposal_id,
            "symbol": proposal.symbol,
            "as_of": proposal.as_of,
            "method": proposal.method,
            "steps": steps,
            "raw_quantity": str(proposal.raw_quantity),
            "capped_quantity": str(proposal.capped_quantity),
            "normalized_quantity": str(proposal.normalized_quantity),
            "proposed_final_quantity": str(proposal.proposed_final_quantity),
            "binding_constraint": proposal.binding_constraint,
            "sizing_status": proposal.sizing_status,
            "warnings": proposal.warnings,
            "blockers": proposal.blockers,
            "assumptions": [
                "Long-only: stop_price < entry_price",
                "Research-only: no broker execution",
                "Lot normalization: ROUND_DOWN always",
                "PIT: all inputs validated against as_of",
                "Fractional shares not supported (ROUND_DOWN to integer)",
            ],
            "safety_labels": [
                "RESEARCH_ONLY", "NOT_AN_ORDER", "NOT_EXECUTABLE",
                "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NO_AUTO_REBALANCE",
            ],
            "research_only": True,
            "executable": False,
            "order_created": False,
        }
        return result
