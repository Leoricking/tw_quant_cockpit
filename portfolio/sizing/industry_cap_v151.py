"""
portfolio/sizing/industry_cap_v151.py — Industry Cap Constraint v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
If industry unknown: returns WARNING (not assume 0%).
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class IndustryCapConstraint:
    """
    Caps position if industry exposure limit would be exceeded.
    Unknown industry → WARNING, not BLOCKED.
    """

    RESEARCH_ONLY = True

    def apply(
        self,
        request,
        raw_quantity: Decimal,
        policy,
        current_industry_value: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        industry = getattr(request, "industry", None)
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        pv: Optional[Decimal] = request.portfolio_value
        max_w = getattr(request, "max_industry_weight", None) or policy.max_industry_weight

        if industry is None or industry == "":
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "INDUSTRY_UNKNOWN: cannot verify industry cap — WARNING only",
                "severity": "WARNING",
                "research_only": True,
            }

        if pv is None or pv <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "INDUSTRY_CAP_SKIP: portfolio_value unknown",
                "severity": "WARNING",
                "research_only": True,
            }

        if entry is None or entry <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "INDUSTRY_CAP_SKIP: entry_price unknown",
                "severity": "WARNING",
                "research_only": True,
            }

        existing = current_industry_value or Decimal("0")
        max_value = pv * max_w
        room = max_value - existing
        if room <= Decimal("0"):
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": (
                    f"INDUSTRY_LIMIT_BLOCKED: industry={industry} existing={existing} "
                    f"already at cap={max_w}"
                ),
                "severity": "BLOCKING",
                "research_only": True,
            }

        max_qty = (room / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")
        if raw_quantity > max_qty:
            return {
                "capped_quantity": max_qty,
                "applied": True,
                "reason": (
                    f"INDUSTRY_LIMIT: raw={raw_quantity} > industry_max={max_qty} "
                    f"(industry={industry}, cap={max_w})"
                ),
                "severity": "HARD_CAP",
                "research_only": True,
            }

        return {
            "capped_quantity": raw_quantity,
            "applied": False,
            "reason": "INDUSTRY_OK",
            "severity": "INFO",
            "research_only": True,
        }
