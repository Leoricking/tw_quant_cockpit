"""
paper_trading/small_capital_strategy/small_capital_risk_adapter_v174.py
Small capital risk adapter — aggregates all monitors into dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskBlockReason,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput, SmallAccountRiskDashboard,
)
from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import evaluate_single_trade_risk
from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import evaluate_portfolio_exposure
from paper_trading.small_capital_strategy.drawdown_monitor_v174 import evaluate_drawdown
from paper_trading.small_capital_strategy.losing_streak_monitor_v174 import evaluate_losing_streak
from paper_trading.small_capital_strategy.cash_ratio_risk_monitor_v174 import evaluate_cash_ratio
from paper_trading.small_capital_strategy.concentration_risk_monitor_v174 import evaluate_concentration_risk
from paper_trading.small_capital_strategy.theme_exposure_monitor_v174 import evaluate_theme_exposure
from paper_trading.small_capital_strategy.position_count_monitor_v174 import evaluate_position_count
from paper_trading.small_capital_strategy.stop_loss_coverage_monitor_v174 import evaluate_stop_loss_coverage
from paper_trading.small_capital_strategy.risk_budget_monitor_v174 import evaluate_risk_budget

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"


def build_risk_dashboard(inp: SmallAccountRiskInput) -> SmallAccountRiskDashboard:
    """Build the full Small Account Risk Dashboard from input state."""
    single_trade = evaluate_single_trade_risk(inp)
    exposure     = evaluate_portfolio_exposure(inp)
    drawdown     = evaluate_drawdown(inp)
    losing       = evaluate_losing_streak(inp)
    cash_ratio   = evaluate_cash_ratio(inp)
    concentration = evaluate_concentration_risk(inp)
    theme        = evaluate_theme_exposure(inp)
    pos_count    = evaluate_position_count(inp)
    stop_loss    = evaluate_stop_loss_coverage(inp)
    budget       = evaluate_risk_budget(inp)

    # Cascade: ABC blocked => dashboard blocked
    if inp.abc_plan_blocked and single_trade.status != RiskStatus.BLOCKED:
        single_trade.block_reasons.append(RiskBlockReason.STOP_LOSS_COVERAGE_INCOMPLETE)
        single_trade.status = RiskStatus.BLOCKED

    # Cascade: watchlist excluded => dashboard blocked
    if inp.watchlist_candidate_excluded and exposure.status != RiskStatus.BLOCKED:
        exposure.block_reasons.append(RiskBlockReason.SAFETY_VIOLATION)
        exposure.status = RiskStatus.BLOCKED

    # Safety hard blocks
    if inp.real_order_requested:
        single_trade.block_reasons.append(RiskBlockReason.REAL_ORDER_REQUESTED)
        single_trade.status = RiskStatus.BLOCKED
    if inp.broker_requested:
        single_trade.block_reasons.append(RiskBlockReason.BROKER_REQUESTED)
        single_trade.status = RiskStatus.BLOCKED
    if inp.margin_requested:
        single_trade.block_reasons.append(RiskBlockReason.MARGIN_NOT_ALLOWED)
        single_trade.status = RiskStatus.BLOCKED

    # Aggregate block reasons
    all_blocks: List[RiskBlockReason] = []
    for sub in [single_trade, exposure, drawdown, losing, cash_ratio,
                concentration, theme, pos_count, stop_loss, budget]:
        all_blocks.extend(sub.block_reasons)
    # Deduplicate preserving order
    seen = set()
    unique_blocks = []
    for b in all_blocks:
        if b not in seen:
            seen.add(b)
            unique_blocks.append(b)

    # Overall status: any BLOCKED => BLOCKED
    sub_statuses = [
        single_trade.status, exposure.status, drawdown.status, losing.status,
        cash_ratio.status, concentration.status, theme.status, pos_count.status,
        stop_loss.status, budget.status,
    ]
    if any(s == RiskStatus.BLOCKED for s in sub_statuses):
        overall = RiskStatus.BLOCKED
    elif any(s == RiskStatus.WARNING for s in sub_statuses):
        overall = RiskStatus.WARNING
    elif any(s == RiskStatus.WATCH for s in sub_statuses):
        overall = RiskStatus.WATCH
    else:
        overall = RiskStatus.PASS

    summary = (
        f"Overall: {overall.value} | "
        f"Blocks: {len(unique_blocks)} | "
        f"Research Only | Paper Only | No Real Orders | Not Investment Advice"
    )

    return SmallAccountRiskDashboard(
        overall_status=overall,
        single_trade=single_trade,
        exposure=exposure,
        drawdown=drawdown,
        losing_streak=losing,
        cash_ratio=cash_ratio,
        concentration=concentration,
        theme_exposure=theme,
        position_count=pos_count,
        stop_loss_coverage=stop_loss,
        risk_budget=budget,
        all_block_reasons=unique_blocks,
        summary=summary,
    )


def get_default_pass_input() -> SmallAccountRiskInput:
    """Return a default PASS-state input for 300k capital."""
    return SmallAccountRiskInput(
        capital_twd=300_000.0,
        total_invested_twd=90_000.0,
        total_invested_pct=30.0,
        cash_twd=210_000.0,
        cash_pct=70.0,
        holdings_count=2,
        position_size_amount=50_000.0,
        stop_loss_pct=0.05,
        has_stop_loss=True,
        current_drawdown_pct=2.0,
        losing_streak_count=1,
        max_single_position_pct=20.0,
        theme_exposure_pct=30.0,
        sector_exposure_pct=40.0,
        short_term_training_amount=5_000.0,
        market_regime="BULL",
        abc_plan_blocked=False,
        watchlist_candidate_excluded=False,
        real_order_requested=False,
        broker_requested=False,
        margin_requested=False,
    )
