"""
paper_trading/small_capital_strategy/trade_plan_validator_v170.py
Trade plan validator for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.enums_v170 import (
    EntryPlanStatus, ForbiddenTradeReason, TradePermissionStatus,
)
from paper_trading.small_capital_strategy.models_v170 import (
    TradePlan, TradePlanValidationResult,
)
from paper_trading.small_capital_strategy.forbidden_trade_rules_v170 import get_permission_status


def validate_trade_plan(plan: TradePlan) -> TradePlanValidationResult:
    """
    Validate a TradePlan. Checks all forbidden rules, entry, exit, stop loss.
    Returns TradePlanValidationResult.
    """
    issues: List[str] = []
    forbidden_reasons: List[ForbiddenTradeReason] = []

    # Check permission status
    permission = get_permission_status(plan.forbidden_checks)
    if permission == TradePermissionStatus.BLOCKED:
        blocked_checks = [c for c in plan.forbidden_checks if c.blocked]
        for bc in blocked_checks:
            issues.append(f"BLOCKED: {bc.reason.value} — {bc.detail}")
            forbidden_reasons.append(bc.reason)

    # Check entry plan
    if plan.entry.status == EntryPlanStatus.BLOCKED:
        issues.append("entry plan status is BLOCKED")
        forbidden_reasons.extend(plan.entry.forbidden_reasons)

    if plan.entry.position_size_twd <= 0 and plan.entry.status == EntryPlanStatus.VALID:
        issues.append("position_size_twd must be > 0 for VALID entry plan")

    if plan.entry.stop_loss.stop_loss_price <= 0:
        issues.append("stop_loss_price must be > 0")
        if ForbiddenTradeReason.NO_STOP_LOSS not in forbidden_reasons:
            forbidden_reasons.append(ForbiddenTradeReason.NO_STOP_LOSS)

    # Safety checks
    if not plan.paper_only:
        issues.append("paper_only must be True")
    if not plan.no_real_orders:
        issues.append("no_real_orders must be True")
    if not plan.not_investment_advice:
        issues.append("not_investment_advice must be True")

    valid = len(issues) == 0
    status = "PASS" if valid else ("BLOCKED" if forbidden_reasons else "FAIL")

    # Deduplicate reasons
    seen = set()
    unique_reasons = []
    for r in forbidden_reasons:
        if r not in seen:
            seen.add(r)
            unique_reasons.append(r)

    return TradePlanValidationResult(
        symbol=plan.symbol,
        valid=valid,
        status=status,
        issues=issues,
        forbidden_reasons=unique_reasons,
    )


def validate_trade_plan_dict(plan_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Light validation of a trade plan represented as a dict.
    Returns {valid, issues}.
    """
    issues = []
    if not plan_dict.get("symbol"):
        issues.append("symbol must be non-empty")
    if not plan_dict.get("paper_only", False):
        issues.append("paper_only must be True")
    if not plan_dict.get("no_real_orders", False):
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
