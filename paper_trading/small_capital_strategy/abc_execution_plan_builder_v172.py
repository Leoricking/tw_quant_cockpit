"""
paper_trading/small_capital_strategy/abc_execution_plan_builder_v172.py
Execution plan builder for A/B/C Buy Point Execution Plan v1.7.2.
Orchestrates all engines and bridges into a complete ABCExecutionPlan.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCExecutionStatus, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCExecutionPlan,
)
from paper_trading.small_capital_strategy.abc_signal_normalizer_v172 import (
    normalize_signal,
)
from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
    check_conditions,
)
from paper_trading.small_capital_strategy.abc_entry_price_engine_v172 import (
    build_entry_plan,
)
from paper_trading.small_capital_strategy.abc_add_price_engine_v172 import (
    build_add_plan,
)
from paper_trading.small_capital_strategy.abc_stop_loss_engine_v172 import (
    build_stop_loss_plan,
)
from paper_trading.small_capital_strategy.abc_take_profit_engine_v172 import (
    build_take_profit_plan,
)
from paper_trading.small_capital_strategy.abc_invalidation_engine_v172 import (
    build_invalidation_plan,
)
from paper_trading.small_capital_strategy.abc_position_sizing_bridge_v172 import (
    compute_position_sizing,
)
from paper_trading.small_capital_strategy.abc_watchlist_bridge_v172 import (
    check_watchlist_compatibility,
)
from paper_trading.small_capital_strategy.abc_market_regime_bridge_v172 import (
    check_market_regime_compatibility,
)
from paper_trading.small_capital_strategy.abc_forbidden_rule_bridge_v172 import (
    check_all_forbidden_rules,
)
from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import (
    compute_scorecard,
)
from paper_trading.small_capital_strategy.abc_paper_order_intent_v172 import (
    build_paper_order_intent,
)


def build_execution_plan(
    signal: ABCSignalInput,
    current_holdings: int = 0,
) -> ABCExecutionPlan:
    """
    Build a complete ABC execution plan for a signal.
    Orchestrates all engines and bridges deterministically.
    """
    symbol     = signal.symbol
    bpt        = signal.buy_point_type
    tier       = signal.tier
    regime     = signal.market_regime

    # 1. Normalize signal
    normalized = normalize_signal(signal)

    # 2. Check conditions
    conditions, block_reasons = check_conditions(normalized, tier, regime)

    # 3. Entry plan
    entry_plan = build_entry_plan(signal, normalized, block_reasons)

    # 4. Add plan
    add_plan = build_add_plan(signal, normalized, block_reasons)

    # 5. Stop loss plan
    stop_loss_plan = build_stop_loss_plan(signal, block_reasons)

    # 6. Take profit plan
    take_profit_plan = build_take_profit_plan(signal, tier, block_reasons)

    # 7. Invalidation plan
    invalidation_plan = build_invalidation_plan(signal, block_reasons)

    # 8. Position sizing bridge
    entry_price = entry_plan.entry_price if entry_plan else signal.close
    stop_price  = stop_loss_plan.stop_loss_price if stop_loss_plan else 0.0
    position_sizing = compute_position_sizing(
        symbol, tier, entry_price, stop_price, current_holdings
    )
    if position_sizing.block_reasons:
        for br in position_sizing.block_reasons:
            if br not in block_reasons:
                block_reasons.append(br)

    # 9. Watchlist bridge
    watchlist_bridge = check_watchlist_compatibility(symbol, tier, bpt)
    if watchlist_bridge.block_reasons:
        for br in watchlist_bridge.block_reasons:
            if br not in block_reasons:
                block_reasons.append(br)

    # 10. Market regime bridge
    regime_bridge = check_market_regime_compatibility(regime, bpt, tier)
    if regime_bridge.block_reasons:
        for br in regime_bridge.block_reasons:
            if br not in block_reasons:
                block_reasons.append(br)

    # 11. Forbidden rule checks
    forbidden_checks = check_all_forbidden_rules(symbol)

    # 12. Scorecard
    scorecard = compute_scorecard(
        symbol, bpt, conditions, stop_loss_plan, take_profit_plan,
        position_sizing, watchlist_bridge, regime_bridge, block_reasons,
    )

    # 13. Paper order intent
    paper_intent = build_paper_order_intent(
        symbol, tier, bpt, entry_plan, stop_loss_plan,
        take_profit_plan, position_sizing, block_reasons,
        warnings=list(regime_bridge.warnings),
    )

    # 14. Determine overall status
    if block_reasons:
        status = ABCExecutionStatus.BLOCKED
    elif entry_plan.status == ABCExecutionStatus.READY:
        status = ABCExecutionStatus.READY
    else:
        status = ABCExecutionStatus.WAITING_CONFIRMATION

    return ABCExecutionPlan(
        symbol=symbol,
        buy_point_type=bpt,
        tier=tier,
        status=status,
        conditions_checked=conditions,
        entry_plan=entry_plan,
        add_plan=add_plan,
        stop_loss_plan=stop_loss_plan,
        take_profit_plan=take_profit_plan,
        invalidation_plan=invalidation_plan,
        position_sizing=position_sizing,
        watchlist_bridge=watchlist_bridge,
        regime_bridge=regime_bridge,
        forbidden_checks=forbidden_checks,
        paper_intent=paper_intent,
        scorecard=scorecard,
        block_reasons=block_reasons,
        warnings=list(regime_bridge.warnings),
    )
