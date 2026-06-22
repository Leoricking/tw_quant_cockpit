"""
portfolio/sizing/validation_v151.py — Position Sizing Request Validator v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import List

RESEARCH_ONLY = True


class PositionSizingValidator:
    """Validates a PositionSizingRequest before calculation."""

    RESEARCH_ONLY = True

    def validate_request(self, request) -> List[str]:
        """
        Returns a list of issue strings. Empty list = valid.
        """
        issues: List[str] = []

        # Safety check
        if not getattr(request, "research_only", True):
            issues.append("SAFETY_VIOLATION: research_only must be True")

        # Symbol required
        if not request.symbol:
            issues.append("MISSING_SYMBOL: symbol is required")

        # Portfolio value
        if request.portfolio_value is not None:
            if request.portfolio_value <= Decimal("0"):
                issues.append("INVALID_PORTFOLIO_VALUE: portfolio_value must be > 0")

        # Available cash
        if request.available_cash is not None:
            if request.available_cash < Decimal("0"):
                issues.append("INVALID_AVAILABLE_CASH: available_cash must be >= 0")

        # Reference / entry price
        entry = request.planned_entry_price or request.reference_price
        if entry is not None and entry <= Decimal("0"):
            issues.append("INVALID_ENTRY_PRICE: planned_entry_price must be > 0")

        # Stop price direction (long-only: stop < entry)
        if request.stop_price is not None and entry is not None:
            if request.stop_price >= entry:
                issues.append(
                    "BLOCKED_INVALID_STOP_DIRECTION: stop_price must be < entry for long-only"
                )
            if request.stop_price <= Decimal("0"):
                issues.append("INVALID_STOP_PRICE: stop_price must be > 0")

        # Risk budget
        if request.risk_budget_percent is not None:
            if request.risk_budget_percent <= Decimal("0"):
                issues.append("INVALID_RISK_BUDGET: risk_budget_percent must be > 0")
            if request.risk_budget_percent > Decimal("1"):
                issues.append("INVALID_RISK_BUDGET: risk_budget_percent must be <= 1 (100%)")

        # ATR
        if request.atr is not None:
            if request.atr <= Decimal("0"):
                issues.append("INVALID_ATR: atr must be > 0")
        # PIT check for ATR
        if request.atr_available_from and request.as_of:
            if request.atr_available_from > request.as_of:
                issues.append(
                    f"PIT_VIOLATION_ATR: atr available_from={request.atr_available_from} > as_of={request.as_of}"
                )

        # Volatility
        if request.volatility is not None:
            if request.volatility <= Decimal("0"):
                issues.append("INVALID_VOLATILITY: volatility must be > 0")

        # Target weight
        if request.target_weight is not None:
            if not (Decimal("0") < request.target_weight <= Decimal("1")):
                issues.append("INVALID_TARGET_WEIGHT: target_weight must be in (0, 1]")

        # Lot size
        if request.lot_size <= 0:
            issues.append("INVALID_LOT_SIZE: lot_size must be > 0")

        # Liquidity PIT
        if request.average_daily_value_available_from and request.as_of:
            if request.average_daily_value_available_from > request.as_of:
                issues.append(
                    f"PIT_VIOLATION_LIQUIDITY: liquidity available_from={request.average_daily_value_available_from} > as_of={request.as_of}"
                )

        # Lineage
        if not request.source_lineage_ids:
            issues.append("MISSING_LINEAGE: source_lineage_ids is empty")

        return issues
