"""
paper_trading/small_capital_strategy/abc_position_sizing_bridge_v172.py
Position sizing bridge for A/B/C Buy Point Execution Plan v1.7.2.
Bridges v1.7.0 capital profile: 300k TWD, max 4 holdings, training cap 15000.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCRiskPermission, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCPositionSizingBridgeResult,
)
from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier

# v1.7.0 capital profile constants
CAPITAL_300K          = 300_000.0
MAX_HOLDINGS          = 4
TRAINING_MAX_AMOUNT   = 15_000.0
MAX_RISK_PCT_PER_TRADE = 0.01   # 1% of capital = 3000 TWD
MAX_POSITION_PCT       = 0.25   # max 25% of capital per position = 75000 TWD
_UNIT_SIZE             = 1000   # Taiwan stock 1 unit = 1000 shares

_EXCLUDED_TIERS = {WatchlistTier.EXCLUDED.value}


def compute_position_sizing(
    symbol: str,
    tier: str,
    entry_price: float,
    stop_loss_price: float,
    current_holdings: int = 0,
) -> ABCPositionSizingBridgeResult:
    """Compute position sizing using v1.7.0 capital profile."""
    block_reasons: List[ABCExecutionBlockReason] = []
    training_cap_applied = False

    # EXCLUDED → BLOCKED
    if tier in _EXCLUDED_TIERS:
        block_reasons.append(ABCExecutionBlockReason.WATCHLIST_EXCLUDED)

    # Holdings limit
    if current_holdings >= MAX_HOLDINGS:
        block_reasons.append(ABCExecutionBlockReason.TOO_MANY_HOLDINGS)

    if block_reasons:
        return ABCPositionSizingBridgeResult(
            symbol=symbol,
            capital_twd=CAPITAL_300K,
            max_holdings=MAX_HOLDINGS,
            position_amount=0.0,
            quantity_estimate=0,
            max_loss_amount=0.0,
            risk_pct=0.0,
            training_cap_applied=False,
            risk_permission=ABCRiskPermission.BLOCKED,
            block_reasons=block_reasons,
        )

    if entry_price <= 0 or stop_loss_price <= 0:
        return ABCPositionSizingBridgeResult(
            symbol=symbol,
            capital_twd=CAPITAL_300K,
            max_holdings=MAX_HOLDINGS,
            position_amount=0.0,
            quantity_estimate=0,
            max_loss_amount=0.0,
            risk_pct=0.0,
            training_cap_applied=False,
            risk_permission=ABCRiskPermission.BLOCKED,
            block_reasons=[ABCExecutionBlockReason.NO_STOP_LOSS],
        )

    # Risk per share
    risk_per_share = entry_price - stop_loss_price
    if risk_per_share <= 0:
        return ABCPositionSizingBridgeResult(
            symbol=symbol,
            capital_twd=CAPITAL_300K,
            max_holdings=MAX_HOLDINGS,
            position_amount=0.0,
            quantity_estimate=0,
            max_loss_amount=0.0,
            risk_pct=0.0,
            training_cap_applied=False,
            risk_permission=ABCRiskPermission.BLOCKED,
            block_reasons=[ABCExecutionBlockReason.NO_STOP_LOSS],
        )

    max_loss = CAPITAL_300K * MAX_RISK_PCT_PER_TRADE   # 3000 TWD
    shares_by_risk = max_loss / risk_per_share
    # Round down to nearest 1000 (Taiwan market unit)
    units = max(1, int(shares_by_risk / _UNIT_SIZE))
    position_amount = units * _UNIT_SIZE * entry_price

    # Training cap
    if tier == WatchlistTier.TRAINING.value:
        if position_amount > TRAINING_MAX_AMOUNT:
            training_units = max(1, int(TRAINING_MAX_AMOUNT / (entry_price * _UNIT_SIZE)))
            position_amount = training_units * _UNIT_SIZE * entry_price
            units = training_units
            training_cap_applied = True

    # Max position cap
    max_pos = CAPITAL_300K * MAX_POSITION_PCT
    if position_amount > max_pos:
        capped_units = max(1, int(max_pos / (entry_price * _UNIT_SIZE)))
        position_amount = capped_units * _UNIT_SIZE * entry_price
        units = capped_units

    actual_max_loss = units * _UNIT_SIZE * risk_per_share
    risk_pct = actual_max_loss / CAPITAL_300K

    if risk_pct > MAX_RISK_PCT_PER_TRADE * 2:
        block_reasons.append(ABCExecutionBlockReason.RISK_EXCEEDS_BUDGET)

    if position_amount <= 0:
        block_reasons.append(ABCExecutionBlockReason.INSUFFICIENT_CAPITAL)

    if block_reasons:
        return ABCPositionSizingBridgeResult(
            symbol=symbol,
            capital_twd=CAPITAL_300K,
            max_holdings=MAX_HOLDINGS,
            position_amount=position_amount,
            quantity_estimate=units * _UNIT_SIZE,
            max_loss_amount=actual_max_loss,
            risk_pct=round(risk_pct, 6),
            training_cap_applied=training_cap_applied,
            risk_permission=ABCRiskPermission.BLOCKED,
            block_reasons=block_reasons,
        )

    permission = ABCRiskPermission.ALLOWED
    if training_cap_applied:
        permission = ABCRiskPermission.DEGRADED

    return ABCPositionSizingBridgeResult(
        symbol=symbol,
        capital_twd=CAPITAL_300K,
        max_holdings=MAX_HOLDINGS,
        position_amount=round(position_amount, 2),
        quantity_estimate=units * _UNIT_SIZE,
        max_loss_amount=round(actual_max_loss, 2),
        risk_pct=round(risk_pct, 6),
        training_cap_applied=training_cap_applied,
        risk_permission=permission,
        block_reasons=[],
    )


def get_capital_constants() -> dict:
    """Return capital profile constants."""
    return {
        "capital_300k": CAPITAL_300K,
        "max_holdings": MAX_HOLDINGS,
        "training_max_amount": TRAINING_MAX_AMOUNT,
        "max_risk_pct_per_trade": MAX_RISK_PCT_PER_TRADE,
        "max_position_pct": MAX_POSITION_PCT,
    }
