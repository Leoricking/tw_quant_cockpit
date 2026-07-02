"""
paper_trading/performance_attribution/contribution_engine_v167.py
Unified contribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Deterministic. Stable ordering. No random. Decimal precision.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _to_decimal(v: float, places: int = 8) -> Decimal:
    quantize_str = "1." + "0" * places
    return Decimal(str(v)).quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


class ContributionEngine:
    """
    Unified contribution engine.
    Supports: amount, return, bps, percent, normalized contributions.
    Deterministic ordering. No random. Stable sort with tie-breaking by ID.
    """

    def __init__(
        self,
        precision: int = 8,
        deterministic_seed: int = 42,
    ) -> None:
        self._precision = precision
        self._seed = deterministic_seed

    def amount_contribution(
        self, entity_id: str, pnl: float, portfolio_pnl: float
    ) -> float:
        """Contribution by amount."""
        return round(pnl, self._precision)

    def return_contribution(
        self, entity_id: str, entity_return: float, entity_weight: float
    ) -> float:
        """Weight * entity_return."""
        return round(entity_weight * entity_return, self._precision)

    def bps_contribution(
        self, entity_id: str, entity_return: float, entity_weight: float
    ) -> float:
        """Basis-point contribution."""
        return round(entity_weight * entity_return * 10_000, self._precision)

    def percent_contribution(
        self, entity_id: str, entity_pnl: float, portfolio_pnl: float
    ) -> float:
        """Percent of total PnL."""
        if portfolio_pnl == 0:
            return 0.0
        return round(entity_pnl / portfolio_pnl * 100, self._precision)

    def normalized_contribution(
        self, entity_id: str, entity_value: float, total_value: float
    ) -> float:
        """Normalized: entity / total."""
        if total_value == 0:
            return 0.0
        return round(entity_value / total_value, self._precision)

    def hierarchical_aggregate(
        self,
        children: List[Dict[str, Any]],
        value_key: str,
    ) -> float:
        """Sum child values. Deterministic."""
        total = Decimal("0")
        for child in children:
            total += _to_decimal(child.get(value_key, 0.0))
        return float(total)

    def reconcile_parent_child(
        self,
        parent_value: float,
        child_sum: float,
        tolerance: float = 1e-8,
    ) -> Dict[str, Any]:
        """Verify parent ≈ child_sum within tolerance."""
        diff = abs(parent_value - child_sum)
        return {
            "parent_value": parent_value,
            "child_sum": child_sum,
            "difference": diff,
            "reconciled": diff <= tolerance,
            "tolerance": tolerance,
        }

    def top_n(
        self,
        items: List[Dict[str, Any]],
        value_key: str,
        id_key: str,
        n: int,
    ) -> List[Dict[str, Any]]:
        """Return top N items by value_key. Stable, deterministic (tie-break by id_key)."""
        sorted_items = sorted(
            items,
            key=lambda x: (-x.get(value_key, 0.0), x.get(id_key, "")),
        )
        return sorted_items[:n]

    def bottom_n(
        self,
        items: List[Dict[str, Any]],
        value_key: str,
        id_key: str,
        n: int,
    ) -> List[Dict[str, Any]]:
        """Return bottom N items. Stable, deterministic."""
        sorted_items = sorted(
            items,
            key=lambda x: (x.get(value_key, 0.0), x.get(id_key, "")),
        )
        return sorted_items[:n]

    def handle_missing(
        self,
        item: Dict[str, Any],
        value_key: str,
        default: float = 0.0,
        missing_label: str = "MISSING",
    ) -> float:
        """Return value or default if missing, tagging as missing."""
        if value_key not in item:
            item[f"_{value_key}_status"] = missing_label
            return default
        return item[value_key]

    def rounding_control(
        self,
        values: List[float],
        total: float,
        places: int = 8,
    ) -> Tuple[List[float], float]:
        """
        Round individual values and compute rounding residual.
        Returns (rounded_values, rounding_residual).
        """
        rounded = [round(v, places) for v in values]
        rounded_sum = sum(rounded)
        rounding_residual = total - rounded_sum
        return rounded, rounding_residual
