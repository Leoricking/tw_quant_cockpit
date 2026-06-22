"""
portfolio/sizing/concentration_cap_v151.py — Concentration Cap Constraint v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Wraps WeightCapConstraint for single-name concentration enforcement.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class ConcentrationCapConstraint:
    """
    Enforces single-name concentration limits using WeightCapConstraint.
    """

    RESEARCH_ONLY = True

    def apply(self, request, raw_quantity: Decimal, policy) -> Dict[str, Any]:
        from .weight_cap_v151 import WeightCapConstraint
        wcc = WeightCapConstraint()
        max_w: Optional[Decimal] = request.max_position_weight or policy.max_single_position_weight
        result = wcc.apply(
            request,
            raw_quantity,
            policy,
            max_weight=max_w,
            constraint_label="SINGLE_NAME_LIMIT",
        )
        result["constraint_type"] = "SINGLE_NAME_LIMIT"
        return result
