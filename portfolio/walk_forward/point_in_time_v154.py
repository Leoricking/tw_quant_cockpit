"""
portfolio/walk_forward/point_in_time_v154.py — Walk-forward PIT Validator v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Reject fetched_at as proxy for available_from. Each window validated independently.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
PIT_VERSION = "1.5.4"

PIT_VALIDATED_DATA_TYPES = [
    "prices", "returns", "classifications", "etf_holdings", "benchmark",
    "atr", "volatility", "correlation", "risk_policy", "sizing_policy",
    "corporate_actions",
]


class PortfolioWalkForwardPITValidator:
    """Validate PIT constraints for walk-forward data. Each window validated independently."""

    def __init__(self):
        self.version = PIT_VERSION

    def validate(self, data_item: Dict[str, Any], as_of: str) -> Dict[str, Any]:
        """
        Validate PIT for a data item.
        Check available_from <= as_of for all data types.
        Reject fetched_at as proxy for available_from.
        """
        violations = []
        evidence = {}

        if data_item is None:
            return {
                "is_valid": False,
                "violations": ["data_item is None"],
                "evidence": {},
            }

        available_from = data_item.get("available_from")
        fetched_at = data_item.get("fetched_at")
        data_type = data_item.get("data_type", "unknown")

        # Reject fetched_at as proxy for available_from
        if available_from is None and fetched_at is not None:
            violations.append(
                f"fetched_at ({fetched_at}) cannot be used as available_from — "
                "use actual available_from date"
            )
            evidence["fetched_at_rejected"] = True

        if available_from is not None:
            if available_from > as_of:
                violations.append(
                    f"{data_type}: available_from ({available_from}) > as_of ({as_of}) — "
                    "future data violation"
                )
                evidence["future_data"] = True

        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "evidence": evidence,
            "data_type": data_type,
            "as_of": as_of,
            "available_from": available_from,
            "research_only": True,
        }

    def validate_window(self, window, data_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate all data items for a window independently."""
        window_id = getattr(window, "window_id", "unknown")
        val_start = getattr(window, "validation_start", "")
        as_of = val_start  # Use validation start as the as_of boundary

        window_violations = []
        item_results = []

        for item in data_items:
            result = self.validate(item, as_of)
            item_results.append(result)
            if not result["is_valid"]:
                window_violations.extend(result["violations"])

        return {
            "window_id": window_id,
            "as_of": as_of,
            "is_valid": len(window_violations) == 0,
            "violations": window_violations,
            "item_results": item_results,
            "research_only": True,
        }
