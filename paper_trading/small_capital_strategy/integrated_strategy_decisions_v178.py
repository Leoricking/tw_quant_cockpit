"""
paper_trading/small_capital_strategy/integrated_strategy_decisions_v178.py
Decision logic for Small Capital Strategy Integration v1.7.8.
Hard block rules, no-trade reasons, and action determination.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Tuple

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedNoTradeReasonCode,
    IntegratedBlockReason,
    IntegratedScoreGrade,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput, IntegratedScorecard,
)

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"


# ---------------------------------------------------------------------------
# Hard block conditions
# ---------------------------------------------------------------------------

def check_hard_blocks(inp: IntegratedStrategyInput) -> List[IntegratedBlockReason]:
    """
    Evaluate all hard block conditions.
    Any truthy result forces BLOCKED action regardless of scores.
    """
    blocks: List[IntegratedBlockReason] = []

    if not inp.has_stop_loss:
        blocks.append(IntegratedBlockReason.NO_STOP_LOSS)
    if inp.real_order_requested:
        blocks.append(IntegratedBlockReason.REAL_ORDER_REQUESTED)
    if inp.broker_requested:
        blocks.append(IntegratedBlockReason.BROKER_REQUESTED)
    if inp.margin_requested:
        blocks.append(IntegratedBlockReason.MARGIN_REQUESTED)
    if inp.regime_status == IntegratedRegimeStatus.RISK_OFF and not inp.regime_safety_override:
        blocks.append(IntegratedBlockReason.REGIME_RISK_OFF)
    if inp.behavior_status == IntegratedBehaviorStatus.BLOCKED:
        blocks.append(IntegratedBlockReason.BEHAVIOR_BLOCKED)
    if inp.risk_level == IntegratedRiskLevel.BLOCKED:
        blocks.append(IntegratedBlockReason.RISK_BLOCKED)
    if inp.watchlist_status == IntegratedWatchlistStatus.EXCLUDED:
        blocks.append(IntegratedBlockReason.WATCHLIST_EXCLUDED)
    if inp.theme_status == IntegratedThemeStatus.EXCLUDED:
        blocks.append(IntegratedBlockReason.THEME_EXCLUDED)
    if inp.abc_status == IntegratedABCStatus.BLOCKED:
        blocks.append(IntegratedBlockReason.ABC_BLOCKED)
    if not inp.source_lineage:
        blocks.append(IntegratedBlockReason.LINEAGE_MISSING)
    if inp.production_db_write_attempted:
        blocks.append(IntegratedBlockReason.PRODUCTION_WRITE_ATTEMPTED)

    return blocks


# ---------------------------------------------------------------------------
# No-trade reason collection
# ---------------------------------------------------------------------------

def collect_no_trade_reasons(inp: IntegratedStrategyInput) -> List[IntegratedNoTradeReasonCode]:
    """Collect all applicable no-trade reasons from input state."""
    reasons: List[IntegratedNoTradeReasonCode] = []

    if inp.regime_status in (IntegratedRegimeStatus.RISK_OFF, IntegratedRegimeStatus.BEAR):
        reasons.append(IntegratedNoTradeReasonCode.MARKET_RISK_OFF)
    if inp.theme_status in (IntegratedThemeStatus.WEAK, IntegratedThemeStatus.EXCLUDED, IntegratedThemeStatus.UNKNOWN):
        reasons.append(IntegratedNoTradeReasonCode.THEME_WEAK)
    if inp.watchlist_status == IntegratedWatchlistStatus.EXCLUDED:
        reasons.append(IntegratedNoTradeReasonCode.WATCHLIST_EXCLUDED)
    if inp.abc_status in (IntegratedABCStatus.NOT_READY, IntegratedABCStatus.BLOCKED):
        reasons.append(IntegratedNoTradeReasonCode.ABC_NOT_READY)
    if inp.risk_level in (IntegratedRiskLevel.HIGH, IntegratedRiskLevel.BLOCKED):
        reasons.append(IntegratedNoTradeReasonCode.RISK_BUDGET_EXCEEDED)
    if not inp.has_stop_loss:
        reasons.append(IntegratedNoTradeReasonCode.STOP_LOSS_MISSING)
    if inp.behavior_status in (IntegratedBehaviorStatus.WARNING, IntegratedBehaviorStatus.BLOCKED):
        reasons.append(IntegratedNoTradeReasonCode.BEHAVIOR_RISK_BLOCKED)
    if inp.mistake_repeat_detected:
        reasons.append(IntegratedNoTradeReasonCode.MISTAKE_REPEAT_BLOCKED)
    if inp.behavior_score < 30.0 and inp.behavior_status == IntegratedBehaviorStatus.CAUTION:
        reasons.append(IntegratedNoTradeReasonCode.OVERTRADING_RISK)
    if inp.journal_required and inp.journal_quality_score < 40.0:
        reasons.append(IntegratedNoTradeReasonCode.JOURNAL_REQUIRED)
    if inp.real_order_requested:
        reasons.append(IntegratedNoTradeReasonCode.REAL_ORDER_BLOCKED)
    if inp.broker_requested:
        reasons.append(IntegratedNoTradeReasonCode.BROKER_BLOCKED)
    if inp.margin_requested:
        reasons.append(IntegratedNoTradeReasonCode.MARGIN_BLOCKED)
    if not inp.symbol or not inp.date:
        reasons.append(IntegratedNoTradeReasonCode.DATA_INCOMPLETE)
    if not inp.source_lineage:
        reasons.append(IntegratedNoTradeReasonCode.LINEAGE_MISSING)

    # Deduplicate preserving order
    seen: set = set()
    unique: List[IntegratedNoTradeReasonCode] = []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return unique


# ---------------------------------------------------------------------------
# Action determination
# ---------------------------------------------------------------------------

def determine_action(
    scorecard: IntegratedScorecard,
    blocks: List[IntegratedBlockReason],
    no_trade_reasons: List[IntegratedNoTradeReasonCode],
    inp: IntegratedStrategyInput,
) -> IntegratedDecisionAction:
    """
    Determine the final integrated decision action.
    Returns one of the 9 allowed paper/research actions.
    """
    # Hard block always wins
    if blocks:
        return IntegratedDecisionAction.BLOCKED

    score = scorecard.final_score
    grade = scorecard.grade

    # If there are no-trade reasons and score is insufficient
    critical_reasons = {
        IntegratedNoTradeReasonCode.MARKET_RISK_OFF,
        IntegratedNoTradeReasonCode.REAL_ORDER_BLOCKED,
        IntegratedNoTradeReasonCode.BROKER_BLOCKED,
        IntegratedNoTradeReasonCode.MARGIN_BLOCKED,
        IntegratedNoTradeReasonCode.STOP_LOSS_MISSING,
        IntegratedNoTradeReasonCode.LINEAGE_MISSING,
        IntegratedNoTradeReasonCode.DATA_INCOMPLETE,
    }
    has_critical = any(r in critical_reasons for r in no_trade_reasons)
    if has_critical:
        return IntegratedDecisionAction.NO_TRADE

    if no_trade_reasons and score < 50.0:
        return IntegratedDecisionAction.NO_TRADE

    # Risk reduction signal
    if inp.risk_level == IntegratedRiskLevel.HIGH:
        return IntegratedDecisionAction.REDUCE_RISK

    # Review if behavior caution
    if inp.behavior_status == IntegratedBehaviorStatus.CAUTION and score < 65.0:
        return IntegratedDecisionAction.REVIEW_REQUIRED

    # Journal incomplete
    if inp.journal_required and inp.journal_quality_score < 40.0:
        return IntegratedDecisionAction.REVIEW_REQUIRED

    # Score-based action
    if grade == IntegratedScoreGrade.EXCELLENT and inp.abc_status in (
        IntegratedABCStatus.A_READY, IntegratedABCStatus.B_READY, IntegratedABCStatus.C_READY
    ):
        return IntegratedDecisionAction.PAPER_ENTRY_ALLOWED

    if grade in (IntegratedScoreGrade.EXCELLENT, IntegratedScoreGrade.GOOD):
        return IntegratedDecisionAction.PAPER_PLAN_READY

    if grade == IntegratedScoreGrade.ACCEPTABLE:
        return IntegratedDecisionAction.WAIT

    if grade == IntegratedScoreGrade.MARGINAL:
        return IntegratedDecisionAction.OBSERVE

    # BLOCKED score grade
    if no_trade_reasons:
        return IntegratedDecisionAction.NO_TRADE

    return IntegratedDecisionAction.OBSERVE


def build_decision_summary(
    action: IntegratedDecisionAction,
    scorecard: IntegratedScorecard,
    blocks: List[IntegratedBlockReason],
    no_trade_reasons: List[IntegratedNoTradeReasonCode],
) -> str:
    """Build a human-readable summary of the decision."""
    if blocks:
        block_names = [b.value for b in blocks[:3]]
        return f"BLOCKED: {', '.join(block_names)}"
    if no_trade_reasons:
        reason_names = [r.value for r in no_trade_reasons[:3]]
        return f"{action.value}: {', '.join(reason_names)}"
    return (
        f"{action.value}: score={scorecard.final_score:.1f} "
        f"grade={scorecard.grade.value}"
    )
