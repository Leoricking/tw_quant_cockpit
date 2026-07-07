"""
paper_trading/small_capital_strategy/position_sizing_v170.py
Position sizing formula for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Formula: position_size = max_loss_amount / stop_loss_pct
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.enums_v170 import AllocationBucket
from paper_trading.small_capital_strategy.models_v170 import (
    PositionSizingInput, PositionSizingResult,
)

# Defaults
MAX_SINGLE_POSITION_PCT = 0.35
MAX_SINGLE_POSITION_AMOUNT = 105000.0
SHORT_TERM_TRAINING_MAX = 15000.0
STOP_LOSS_PCT_TOO_WIDE_THRESHOLD = 0.20  # 20%
MIN_MEANINGFUL_AMOUNT = 5000.0


def compute_position_size(inp: PositionSizingInput) -> PositionSizingResult:
    """
    Compute position size using: position_size = max_loss_amount / stop_loss_pct.
    Applies all constraints and returns a PositionSizingResult.
    """
    symbol = inp.symbol
    max_loss = inp.max_loss_amount
    stop_pct = inp.stop_loss_pct

    # BLOCKED: stop_loss_pct <= 0
    if stop_pct <= 0:
        return PositionSizingResult(
            symbol=symbol, position_size_twd=0.0,
            stop_loss_pct=stop_pct, max_loss_amount=max_loss,
            bucket=inp.bucket, status="BLOCKED",
            reason="stop_loss_pct must be > 0",
        )

    # BLOCKED: total holdings >= max
    if inp.total_current_holdings >= inp.max_holdings:
        return PositionSizingResult(
            symbol=symbol, position_size_twd=0.0,
            stop_loss_pct=stop_pct, max_loss_amount=max_loss,
            bucket=inp.bucket, status="BLOCKED",
            reason=f"total_holdings {inp.total_current_holdings} >= max {inp.max_holdings}",
        )

    # Core formula
    raw_size = max_loss / stop_pct

    # Check wide stop
    status = "VALID"
    reason = ""
    capped_by = ""

    if stop_pct > STOP_LOSS_PCT_TOO_WIDE_THRESHOLD:
        status = "DEGRADED"
        reason = f"stop_loss_pct {stop_pct:.1%} > wide threshold {STOP_LOSS_PCT_TOO_WIDE_THRESHOLD:.1%}"

    # Cap: bucket_remaining_budget
    if raw_size > inp.bucket_remaining_budget:
        raw_size = inp.bucket_remaining_budget
        capped_by = "bucket_remaining_budget"

    # Cap: max_single_position_pct
    pct_cap = inp.capital_twd * inp.max_single_position_pct
    if raw_size > pct_cap:
        raw_size = pct_cap
        capped_by = "max_single_position_pct"

    # Cap: max_single_position_amount
    if raw_size > inp.max_single_position_amount:
        raw_size = inp.max_single_position_amount
        capped_by = "max_single_position_amount"

    # Cap: short-term training bucket
    if inp.bucket == AllocationBucket.SHORT_TERM_TRAINING and raw_size > SHORT_TERM_TRAINING_MAX:
        raw_size = SHORT_TERM_TRAINING_MAX
        capped_by = "short_term_training_cap"

    # Minimum meaningful
    if raw_size < MIN_MEANINGFUL_AMOUNT:
        return PositionSizingResult(
            symbol=symbol, position_size_twd=0.0,
            stop_loss_pct=stop_pct, max_loss_amount=max_loss,
            bucket=inp.bucket, status="BLOCKED",
            reason=f"computed size {raw_size:.0f} < min meaningful {MIN_MEANINGFUL_AMOUNT:.0f}",
        )

    return PositionSizingResult(
        symbol=symbol,
        position_size_twd=round(raw_size, 2),
        stop_loss_pct=stop_pct,
        max_loss_amount=max_loss,
        bucket=inp.bucket,
        status=status,
        reason=reason,
        capped_by=capped_by,
    )


def validate_position_sizing_inputs(inp: PositionSizingInput) -> Dict[str, Any]:
    """Validate PositionSizingInput before computing. Returns {valid, issues}."""
    issues = []
    if inp.capital_twd <= 0:
        issues.append(f"capital_twd must be > 0, got {inp.capital_twd}")
    if inp.max_loss_amount <= 0:
        issues.append(f"max_loss_amount must be > 0, got {inp.max_loss_amount}")
    if inp.bucket_remaining_budget < 0:
        issues.append(f"bucket_remaining_budget must be >= 0, got {inp.bucket_remaining_budget}")
    if not inp.paper_only:
        issues.append("paper_only must be True")
    if not inp.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
