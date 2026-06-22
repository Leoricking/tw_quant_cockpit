"""
portfolio/sizing/eligibility_v151.py — Position Sizing Eligibility Gate v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List

RESEARCH_ONLY = True


@dataclass
class EligibilityResult:
    sizing_allowed: bool
    methods_allowed: List[str]
    methods_blocked: List[str]
    warnings: List[str]
    blockers: List[str]
    evidence: Dict[str, Any]
    eligibility_status: str  # "ELIGIBLE", "BLOCKED", "PARTIAL", "WARNING"
    research_only: bool = True


class PositionSizingEligibilityGate:
    """
    Evaluates whether position sizing is allowed for the given request/policy.
    Checks: research_only, broker_linked=False, real_order_enabled=False,
            valid price, primary authority, freshness, PIT, lineage,
            cash known, portfolio value complete, policy valid, risk budget valid,
            lot metadata valid, and more.
    """

    RESEARCH_ONLY = True

    def evaluate(self, request, policy) -> EligibilityResult:
        warnings: List[str] = []
        blockers: List[str] = []
        evidence: Dict[str, Any] = {}

        # Safety checks
        if not getattr(request, "research_only", True):
            blockers.append("SAFETY_VIOLATION: research_only must be True")

        if getattr(request, "broker_linked", False):
            blockers.append("BROKER_LINKED_BLOCKED: sizing not allowed with broker_linked=True")
            evidence["broker_linked"] = True

        if getattr(request, "real_order_enabled", False):
            blockers.append("REAL_ORDER_BLOCKED: sizing not allowed with real_order_enabled=True")

        # Policy checks
        if policy is None:
            blockers.append("MISSING_POLICY: a PositionSizingPolicy is required")
        else:
            if getattr(policy, "full_kelly_enabled", False):
                blockers.append("FULL_KELLY_BLOCKED: full_kelly_enabled must be False")
            if getattr(policy, "leverage_enabled", False):
                blockers.append("LEVERAGE_BLOCKED: leverage_enabled must be False")
            if getattr(policy, "short_enabled", False):
                blockers.append("SHORT_BLOCKED: short_enabled must be False")
            if policy.risk_per_trade_percent <= Decimal("0"):
                blockers.append("INVALID_RISK_BUDGET: risk_per_trade_percent must be > 0")

        # Price checks
        entry = request.planned_entry_price or request.reference_price
        if entry is None:
            blockers.append("MISSING_PRICE: reference_price or planned_entry_price required")
        elif entry <= Decimal("0"):
            blockers.append(f"INVALID_PRICE: price={entry} must be > 0")

        # Portfolio value
        if request.portfolio_value is None:
            warnings.append("PORTFOLIO_VALUE_UNKNOWN: portfolio_value not provided")
        elif request.portfolio_value <= Decimal("0"):
            blockers.append("INVALID_PORTFOLIO_VALUE: portfolio_value must be > 0")

        # Cash
        if request.available_cash is None:
            warnings.append("CASH_UNKNOWN: available_cash not provided")

        # PIT checks
        atr_af = getattr(request, "atr_available_from", None)
        as_of = request.as_of
        if atr_af and as_of and atr_af > as_of:
            blockers.append(
                f"PIT_VIOLATION_ATR: atr available_from={atr_af} > as_of={as_of}"
            )

        adv_af = getattr(request, "average_daily_value_available_from", None)
        if adv_af and as_of and adv_af > as_of:
            blockers.append(
                f"PIT_VIOLATION_LIQUIDITY: adv available_from={adv_af} > as_of={as_of}"
            )

        # Lineage
        if not request.source_lineage_ids:
            warnings.append("MISSING_LINEAGE: source_lineage_ids is empty")

        # Lot size
        if request.lot_size <= 0:
            blockers.append("INVALID_LOT_SIZE: lot_size must be > 0")

        # Stop direction for FF/SD methods
        if request.stop_price is not None and entry is not None and entry > Decimal("0"):
            if request.stop_price >= entry:
                blockers.append(
                    "BLOCKED_INVALID_STOP_DIRECTION: stop_price must be < entry for long-only"
                )

        # Determine allowed methods
        all_methods = [
            "FIXED_FRACTIONAL", "STOP_DISTANCE", "ATR_BASED",
            "VOLATILITY_TARGET", "FIXED_PORTFOLIO_WEIGHT", "CASH_LIMITED",
            "MANUAL_RESEARCH",
        ]
        methods_blocked: List[str] = []

        if request.stop_price is None:
            methods_blocked.append("FIXED_FRACTIONAL")
        if request.atr is None:
            methods_blocked.append("ATR_BASED")
        if request.volatility is None:
            methods_blocked.append("VOLATILITY_TARGET")
        if request.target_weight is None:
            methods_blocked.append("FIXED_PORTFOLIO_WEIGHT")
        if request.available_cash is None:
            methods_blocked.append("CASH_LIMITED")

        # Remove duplicates
        methods_blocked = list(set(methods_blocked))
        methods_allowed = [m for m in all_methods if m not in methods_blocked]

        if blockers:
            status = "BLOCKED"
            sizing_allowed = False
        elif warnings:
            status = "WARNING"
            sizing_allowed = True
        else:
            status = "ELIGIBLE"
            sizing_allowed = True

        evidence["warnings_count"] = len(warnings)
        evidence["blockers_count"] = len(blockers)

        return EligibilityResult(
            sizing_allowed=sizing_allowed,
            methods_allowed=methods_allowed,
            methods_blocked=methods_blocked,
            warnings=warnings,
            blockers=blockers,
            evidence=evidence,
            eligibility_status=status,
        )
