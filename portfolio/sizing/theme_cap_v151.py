"""
portfolio/sizing/theme_cap_v151.py — Theme Cap Constraint v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Supports overlapping themes — uses the most restrictive cap.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True


class ThemeCapConstraint:
    """
    Caps position for theme exposure limits.
    If multiple themes overlap, the most restrictive (lowest cap) is used.
    """

    RESEARCH_ONLY = True

    def apply(
        self,
        request,
        raw_quantity: Decimal,
        policy,
        theme_exposures: Optional[Dict[str, Decimal]] = None,
    ) -> Dict[str, Any]:
        """
        theme_exposures: {theme_name: current_exposure_value}
        """
        theme = getattr(request, "theme", None)
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        pv: Optional[Decimal] = request.portfolio_value
        max_w = getattr(request, "max_theme_weight", None) or policy.max_theme_weight

        if theme is None or theme == "":
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "THEME_UNKNOWN: no theme specified, skip theme cap",
                "severity": "INFO",
                "research_only": True,
            }

        if pv is None or pv <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "THEME_CAP_SKIP: portfolio_value unknown",
                "severity": "WARNING",
                "research_only": True,
            }

        if entry is None or entry <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "THEME_CAP_SKIP: entry_price unknown",
                "severity": "WARNING",
                "research_only": True,
            }

        themes: List[str] = theme if isinstance(theme, list) else [theme]
        exposures = theme_exposures or {}

        # Most restrictive: smallest room across all themes
        binding_theme = None
        min_room = None
        for t in themes:
            existing = exposures.get(t, Decimal("0"))
            max_value = pv * max_w
            room = max_value - existing
            if min_room is None or room < min_room:
                min_room = room
                binding_theme = t

        if min_room is None:
            min_room = pv * max_w

        if min_room <= Decimal("0"):
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": f"THEME_LIMIT_BLOCKED: theme={binding_theme} at cap={max_w}",
                "severity": "BLOCKING",
                "research_only": True,
            }

        max_qty = (min_room / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")
        if raw_quantity > max_qty:
            return {
                "capped_quantity": max_qty,
                "applied": True,
                "reason": (
                    f"THEME_LIMIT: raw={raw_quantity} > theme_max={max_qty} "
                    f"(binding_theme={binding_theme}, cap={max_w})"
                ),
                "severity": "HARD_CAP",
                "research_only": True,
            }

        return {
            "capped_quantity": raw_quantity,
            "applied": False,
            "reason": "THEME_OK",
            "severity": "INFO",
            "research_only": True,
        }
