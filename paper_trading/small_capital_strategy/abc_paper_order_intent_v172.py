"""
paper_trading/small_capital_strategy/abc_paper_order_intent_v172.py
Paper order intent generator for A/B/C Buy Point Execution Plan v1.7.2.
No real orders. No broker execution.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import uuid
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCPaperOrderIntentType,
    ABCExecutionBlockReason, ABCExecutionWarningReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCEntryPricePlan, ABCStopLossExecutionPlan, ABCTakeProfitExecutionPlan,
    ABCPositionSizingBridgeResult, ABCPaperOrderIntent,
)


def _make_intent_id(symbol: str) -> str:
    return f"abc_paper_{symbol}_{uuid.uuid4().hex[:8]}"


def build_paper_order_intent(
    symbol: str,
    tier: str,
    buy_point_type: ABCBuyPointType,
    entry_plan: ABCEntryPricePlan,
    stop_loss_plan: ABCStopLossExecutionPlan,
    take_profit_plan: ABCTakeProfitExecutionPlan,
    position_sizing: ABCPositionSizingBridgeResult,
    block_reasons: List[ABCExecutionBlockReason],
    warnings: List[ABCExecutionWarningReason] = None,
    real_order_requested: bool = False,
    broker_execution_requested: bool = False,
) -> ABCPaperOrderIntent:
    """Build paper order intent. Blocks if real order or broker requested."""
    warnings = warnings or []

    # Hard block conditions
    if real_order_requested:
        if ABCExecutionBlockReason.REAL_ORDER_REQUESTED not in block_reasons:
            block_reasons = list(block_reasons) + [ABCExecutionBlockReason.REAL_ORDER_REQUESTED]
        return ABCPaperOrderIntent(
            intent_id=_make_intent_id(symbol),
            symbol=symbol,
            buy_point_type=buy_point_type,
            tier=tier,
            action=ABCPaperOrderIntentType.PAPER_BLOCK,
            reference_price=0.0,
            quantity_estimate=0,
            position_size_amount=0.0,
            max_loss_amount=0.0,
            stop_loss_price=0.0,
            block_reasons=block_reasons,
            warnings=warnings,
            real_order_requested=real_order_requested,
            broker_execution_requested=broker_execution_requested,
        )

    if broker_execution_requested:
        if ABCExecutionBlockReason.BROKER_REQUESTED not in block_reasons:
            block_reasons = list(block_reasons) + [ABCExecutionBlockReason.BROKER_REQUESTED]
        return ABCPaperOrderIntent(
            intent_id=_make_intent_id(symbol),
            symbol=symbol,
            buy_point_type=buy_point_type,
            tier=tier,
            action=ABCPaperOrderIntentType.PAPER_BLOCK,
            reference_price=0.0,
            quantity_estimate=0,
            position_size_amount=0.0,
            max_loss_amount=0.0,
            stop_loss_price=0.0,
            block_reasons=block_reasons,
            warnings=warnings,
            real_order_requested=real_order_requested,
            broker_execution_requested=broker_execution_requested,
        )

    if block_reasons:
        return ABCPaperOrderIntent(
            intent_id=_make_intent_id(symbol),
            symbol=symbol,
            buy_point_type=buy_point_type,
            tier=tier,
            action=ABCPaperOrderIntentType.PAPER_BLOCK,
            reference_price=entry_plan.entry_price if entry_plan else 0.0,
            quantity_estimate=0,
            position_size_amount=0.0,
            max_loss_amount=0.0,
            stop_loss_price=stop_loss_plan.stop_loss_price if stop_loss_plan else 0.0,
            take_profit_references=take_profit_plan.take_profit_references if take_profit_plan else [],
            block_reasons=block_reasons,
            warnings=warnings,
        )

    # Determine action
    if entry_plan and entry_plan.status == ABCExecutionStatus.READY:
        action = ABCPaperOrderIntentType.PAPER_BUY
    elif entry_plan and entry_plan.status == ABCExecutionStatus.WAITING_CONFIRMATION:
        action = ABCPaperOrderIntentType.PAPER_WAIT
    elif entry_plan and entry_plan.status == ABCExecutionStatus.DEGRADED:
        action = ABCPaperOrderIntentType.PAPER_WAIT
    else:
        action = ABCPaperOrderIntentType.PAPER_WAIT

    # Invalidation conditions
    inv_conditions = []
    if stop_loss_plan and stop_loss_plan.stop_loss_price > 0:
        inv_conditions.append(f"Stop loss at {stop_loss_plan.stop_loss_price:.2f}")

    return ABCPaperOrderIntent(
        intent_id=_make_intent_id(symbol),
        symbol=symbol,
        buy_point_type=buy_point_type,
        tier=tier,
        action=action,
        reference_price=entry_plan.entry_price if entry_plan else 0.0,
        quantity_estimate=position_sizing.quantity_estimate if position_sizing else 0,
        position_size_amount=position_sizing.position_amount if position_sizing else 0.0,
        max_loss_amount=position_sizing.max_loss_amount if position_sizing else 0.0,
        stop_loss_price=stop_loss_plan.stop_loss_price if stop_loss_plan else 0.0,
        take_profit_references=take_profit_plan.take_profit_references if take_profit_plan else [],
        invalidation_conditions=inv_conditions,
        block_reasons=[],
        warnings=warnings,
        real_order_requested=False,
        broker_execution_requested=False,
    )


def get_paper_intent_actions() -> List[str]:
    """Return all valid paper intent action values."""
    return [a.value for a in ABCPaperOrderIntentType]
