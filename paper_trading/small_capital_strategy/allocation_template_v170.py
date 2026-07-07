"""
paper_trading/small_capital_strategy/allocation_template_v170.py
Allocation templates for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.enums_v170 import AllocationBucket, MarketRegime
from paper_trading.small_capital_strategy.models_v170 import AllocationBucketPlan, AllocationTemplate

# Bull / normal regime allocation
BULL_ALLOCATION = {
    AllocationBucket.CORE: 0.40,
    AllocationBucket.MAIN_THEME_SWING: 0.35,
    AllocationBucket.SECOND_WAVE_SETUP: 0.15,
    AllocationBucket.SHORT_TERM_TRAINING: 0.05,
    AllocationBucket.CASH: 0.05,
}

# Range regime allocation
RANGE_ALLOCATION = {
    AllocationBucket.CORE: 0.35,
    AllocationBucket.MAIN_THEME_SWING: 0.25,
    AllocationBucket.SECOND_WAVE_SETUP: 0.10,
    AllocationBucket.SHORT_TERM_TRAINING: 0.05,
    AllocationBucket.CASH: 0.25,
}

# Bear / risk-off regime allocation
BEAR_ALLOCATION = {
    AllocationBucket.CORE: 0.30,
    AllocationBucket.MAIN_THEME_SWING: 0.15,
    AllocationBucket.SECOND_WAVE_SETUP: 0.05,
    AllocationBucket.SHORT_TERM_TRAINING: 0.00,
    AllocationBucket.CASH: 0.50,
}

# Unknown regime allocation (conservative)
UNKNOWN_ALLOCATION = {
    AllocationBucket.CORE: 0.30,
    AllocationBucket.MAIN_THEME_SWING: 0.20,
    AllocationBucket.SECOND_WAVE_SETUP: 0.05,
    AllocationBucket.SHORT_TERM_TRAINING: 0.00,
    AllocationBucket.CASH: 0.40,  # Wait -- but unknown requires cash_min=40%
}

_REGIME_ALLOCATION_MAP = {
    MarketRegime.BULL: BULL_ALLOCATION,
    MarketRegime.RANGE: RANGE_ALLOCATION,
    MarketRegime.BEAR: BEAR_ALLOCATION,
    MarketRegime.RISK_OFF: BEAR_ALLOCATION,
    MarketRegime.UNKNOWN: UNKNOWN_ALLOCATION,
}


def get_allocation_for_regime(
    regime: MarketRegime,
    template_id: str,
    capital_twd: float,
) -> AllocationTemplate:
    """Return an AllocationTemplate for the given regime and capital."""
    allocation_map = _REGIME_ALLOCATION_MAP.get(regime, UNKNOWN_ALLOCATION)
    buckets: List[AllocationBucketPlan] = []

    for bucket, pct in allocation_map.items():
        buckets.append(AllocationBucketPlan(
            bucket=bucket,
            target_pct=pct,
            amount_twd=round(capital_twd * pct, 2),
            max_pct=pct,
            margin_enabled=False,
        ))

    cash_pct = allocation_map.get(AllocationBucket.CASH, 0.0)
    total_invested_pct = 1.0 - cash_pct

    return AllocationTemplate(
        template_id=template_id,
        regime=regime,
        buckets=buckets,
        total_invested_pct=round(total_invested_pct, 4),
        cash_pct=round(cash_pct, 4),
    )


def validate_allocation(template: AllocationTemplate) -> Dict[str, Any]:
    """Validate an AllocationTemplate. Returns {valid, issues}."""
    issues = []

    # Total must be 100%
    total = sum(b.target_pct for b in template.buckets)
    if abs(total - 1.0) > 0.001:
        issues.append(f"allocation total {total:.4f} != 1.0")

    # Cash cannot be negative
    cash_buckets = [b for b in template.buckets if b.bucket == AllocationBucket.CASH]
    for cb in cash_buckets:
        if cb.target_pct < 0:
            issues.append(f"CASH bucket target_pct {cb.target_pct} < 0")

    # Short-term training cannot exceed 5%
    st_buckets = [b for b in template.buckets if b.bucket == AllocationBucket.SHORT_TERM_TRAINING]
    for sb in st_buckets:
        if sb.target_pct > 0.05 + 0.001:
            issues.append(
                f"SHORT_TERM_TRAINING {sb.target_pct:.3f} > 5%"
            )

    # No bucket may enable margin
    for b in template.buckets:
        if b.margin_enabled:
            issues.append(f"Bucket {b.bucket.value} has margin_enabled=True")

    if not template.paper_only:
        issues.append("paper_only must be True")

    if not template.no_real_orders:
        issues.append("no_real_orders must be True")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "template_id": template.template_id,
        "total": round(total, 4),
    }
