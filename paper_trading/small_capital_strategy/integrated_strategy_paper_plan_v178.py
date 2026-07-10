"""
paper_trading/small_capital_strategy/integrated_strategy_paper_plan_v178.py
Paper plan generation for Small Capital Strategy Integration v1.7.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import uuid
from typing import Optional

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction, IntegratedABCStatus,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput, IntegratedStrategyDecision, IntegratedPaperPlan,
)

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"
_LINEAGE = "paper_trading.small_capital_strategy.integrated_strategy_paper_plan_v178"

# Risk params
_DEFAULT_RISK_PCT   = 0.02   # 2% per trade
_DEFAULT_STOP_PCT   = 0.07   # 7% stop loss from entry
_DEFAULT_TARGET_PCT = 0.20   # 20% take profit target


def _abc_to_buy_point_label(status: IntegratedABCStatus) -> str:
    _map = {
        IntegratedABCStatus.A_READY: "A: 10MA Pullback",
        IntegratedABCStatus.B_READY: "B: Platform Breakout",
        IntegratedABCStatus.C_READY: "C: 20MA Second Wave",
        IntegratedABCStatus.NOT_READY: "Not Ready",
        IntegratedABCStatus.BLOCKED: "Blocked",
    }
    return _map.get(status, "Unknown")


def build_paper_plan(
    inp: IntegratedStrategyInput,
    decision: IntegratedStrategyDecision,
    reference_price: float = 0.0,
) -> IntegratedPaperPlan:
    """
    Build a paper-only plan.
    No real orders. No broker execution. Research only.
    """
    plan_id = f"PP178-{inp.symbol or 'UNKNOWN'}-{inp.date or '00000000'}-{uuid.uuid4().hex[:6].upper()}"
    buy_point_label = _abc_to_buy_point_label(inp.abc_status)

    # Price estimates (paper only — no real prices)
    entry_low  = round(reference_price * 0.99, 2) if reference_price > 0 else 0.0
    entry_high = round(reference_price * 1.01, 2) if reference_price > 0 else 0.0
    stop_price = round(entry_low * (1 - _DEFAULT_STOP_PCT), 2) if entry_low > 0 else 0.0
    target_price = round(entry_high * (1 + _DEFAULT_TARGET_PCT), 2) if entry_high > 0 else 0.0

    # Position sizing (paper only)
    capital = inp.capital_twd
    risk_amount = round(capital * _DEFAULT_RISK_PCT, 0)
    shares = 0
    if stop_price > 0 and entry_low > 0:
        loss_per_share = entry_low - stop_price
        if loss_per_share > 0:
            shares = max(0, int(risk_amount / loss_per_share))

    plan_valid = (
        decision.action in (
            IntegratedDecisionAction.PAPER_PLAN_READY,
            IntegratedDecisionAction.PAPER_ENTRY_ALLOWED,
            IntegratedDecisionAction.PAPER_ADD_ALLOWED,
        )
        and inp.has_stop_loss
        and not inp.real_order_requested
        and not inp.broker_requested
        and not inp.margin_requested
    )

    notes_parts = [
        "PAPER ONLY. NO REAL ORDERS. RESEARCH ONLY.",
        f"Action: {decision.action.value}",
        f"Score: {decision.final_score:.1f} | Grade: {decision.grade.value}",
        f"Buy Point: {buy_point_label}",
        f"Theme: {inp.top_theme or 'N/A'}",
        f"Regime: {inp.regime_status.value}",
    ]
    if decision.no_trade_reasons:
        notes_parts.append(f"No-trade reasons: {[r.value for r in decision.no_trade_reasons[:3]]}")

    return IntegratedPaperPlan(
        plan_id=plan_id,
        symbol=inp.symbol,
        date=inp.date,
        source_lineage=_LINEAGE,
        buy_point_type=buy_point_label,
        entry_price_range_low=entry_low,
        entry_price_range_high=entry_high,
        stop_loss_price=stop_price,
        stop_loss_pct=_DEFAULT_STOP_PCT,
        target_price=target_price,
        position_size_shares=shares,
        max_capital_twd=capital,
        risk_amount_twd=risk_amount,
        risk_pct=_DEFAULT_RISK_PCT,
        top_theme=inp.top_theme,
        regime=inp.regime_status.value,
        abc_buy_point=buy_point_label,
        plan_valid=plan_valid,
        plan_notes=" | ".join(notes_parts),
        broker_execution_enabled=False,
    )
