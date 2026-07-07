"""
paper_trading/small_capital_strategy/strategy_template_v170.py
Strategy template builder for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

from paper_trading.small_capital_strategy.enums_v170 import (
    MarketRegime, StrategyTemplateStatus,
)
from paper_trading.small_capital_strategy.models_v170 import SmallCapitalStrategyTemplate
from paper_trading.small_capital_strategy.capital_profile_v170 import (
    get_300k_template, validate_capital_profile, TEMPLATE_300K_ID,
)
from paper_trading.small_capital_strategy.risk_budget_v170 import compute_risk_budget
from paper_trading.small_capital_strategy.allocation_template_v170 import get_allocation_for_regime
from paper_trading.small_capital_strategy.market_regime_filter_v170 import get_regime_control
from paper_trading.small_capital_strategy.watchlist_profile_v170 import create_default_watchlist_profile


def build_300k_template(
    regime: MarketRegime = MarketRegime.BULL,
    max_loss_override: Optional[float] = None,
) -> SmallCapitalStrategyTemplate:
    """Build the canonical 300k strategy template for the given regime."""
    profile = get_300k_template()
    risk_budget = compute_risk_budget(profile, max_loss_override)
    allocation = get_allocation_for_regime(regime, TEMPLATE_300K_ID, profile.capital_twd)
    regime_result = get_regime_control(regime)
    watchlist = create_default_watchlist_profile()

    return SmallCapitalStrategyTemplate(
        template_id=TEMPLATE_300K_ID,
        capital_profile=profile,
        risk_budget=risk_budget,
        allocation=allocation,
        regime=regime_result,
        watchlist=watchlist,
        status=StrategyTemplateStatus.ACTIVE,
    )


def validate_strategy_template(template: SmallCapitalStrategyTemplate) -> Dict[str, Any]:
    """Validate a SmallCapitalStrategyTemplate. Returns {valid, issues}."""
    issues = []

    # Validate capital profile
    cp_result = validate_capital_profile(template.capital_profile)
    if not cp_result["valid"]:
        issues.extend([f"capital_profile: {i}" for i in cp_result["issues"]])

    # Check safety flags
    if not template.paper_only:
        issues.append("paper_only must be True")
    if not template.no_real_orders:
        issues.append("no_real_orders must be True")
    if not template.not_investment_advice:
        issues.append("not_investment_advice must be True")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "template_id": template.template_id,
    }


def get_template_summary(template: SmallCapitalStrategyTemplate) -> Dict[str, Any]:
    """Return a summary dict of the strategy template."""
    return {
        "template_id": template.template_id,
        "status": template.status.value,
        "capital_twd": template.capital_profile.capital_twd,
        "max_loss_default": template.capital_profile.max_loss_default,
        "risk_pct_default": template.capital_profile.risk_pct_default,
        "max_holdings": template.capital_profile.max_holdings_default,
        "regime": template.regime.regime.value,
        "cash_min_pct": template.regime.cash_min_pct,
        "max_invested_pct": template.regime.max_invested_pct,
        "paper_only": template.paper_only,
        "research_only": template.research_only,
        "no_real_orders": template.no_real_orders,
        "not_investment_advice": template.not_investment_advice,
        "schema_version": template.schema_version,
        "policy_version": template.policy_version,
        "source_lineage": template.source_lineage,
    }
