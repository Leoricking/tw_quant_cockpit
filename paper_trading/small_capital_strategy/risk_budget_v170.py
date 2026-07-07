"""
paper_trading/small_capital_strategy/risk_budget_v170.py
Risk budget for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.enums_v170 import RiskBudgetType
from paper_trading.small_capital_strategy.models_v170 import CapitalProfile, RiskBudget


def compute_risk_budget(profile: CapitalProfile, max_loss_override: float = None) -> RiskBudget:
    """Compute a RiskBudget from a CapitalProfile."""
    max_loss = max_loss_override if max_loss_override is not None else profile.max_loss_default

    # Clamp to min/max
    max_loss = max(profile.max_loss_min, min(profile.max_loss_max, max_loss))

    risk_pct = max_loss / profile.capital_twd
    # Clamp risk_pct
    risk_pct = max(profile.risk_pct_min, min(profile.risk_pct_max, risk_pct))

    return RiskBudget(
        template_id=profile.template_id,
        capital_twd=profile.capital_twd,
        max_loss_per_trade=max_loss,
        risk_pct_per_trade=risk_pct,
        max_total_risk_pct=risk_pct * profile.max_holdings_default,
        budget_type=RiskBudgetType.STANDARD,
    )


def validate_risk_budget(budget: RiskBudget) -> Dict[str, Any]:
    """Validate a RiskBudget. Returns {valid, issues}."""
    issues = []

    if budget.capital_twd <= 0:
        issues.append(f"capital_twd must be > 0, got {budget.capital_twd}")

    if budget.max_loss_per_trade <= 0:
        issues.append(f"max_loss_per_trade must be > 0, got {budget.max_loss_per_trade}")

    if not (0 < budget.risk_pct_per_trade <= 1.0):
        issues.append(f"risk_pct_per_trade must be in (0, 1.0], got {budget.risk_pct_per_trade}")

    if budget.risk_pct_per_trade > 0.015:
        issues.append(
            f"risk_pct_per_trade {budget.risk_pct_per_trade:.3f} exceeds max 1.5%"
        )

    if budget.max_loss_per_trade > 4500:
        issues.append(
            f"max_loss_per_trade {budget.max_loss_per_trade} exceeds max 4500 TWD"
        )

    if budget.max_loss_per_trade < 2400:
        issues.append(
            f"max_loss_per_trade {budget.max_loss_per_trade} below min 2400 TWD"
        )

    if not budget.paper_only:
        issues.append("paper_only must be True")

    if not budget.no_real_orders:
        issues.append("no_real_orders must be True")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "template_id": budget.template_id,
    }
