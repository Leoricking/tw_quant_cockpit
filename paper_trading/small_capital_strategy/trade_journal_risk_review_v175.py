"""
paper_trading/small_capital_strategy/trade_journal_risk_review_v175.py
Risk violation review for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Optional

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import ReviewStatus
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, TradeDecisionSnapshot, RiskViolationReview,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

# Risk thresholds
MAX_POSITION_SIZE_TWD = 90_000.0   # 30% of 300k capital
MAX_STOP_LOSS_PCT_MISSING = 0.0


def detect_violations(
    entry: TradeJournalEntry,
    decision_snapshot: Optional[TradeDecisionSnapshot] = None,
) -> List[str]:
    """Detect risk violations in a trade. Returns list of violation strings."""
    violations: List[str] = []

    # Oversize check
    if entry.position_size_twd > MAX_POSITION_SIZE_TWD:
        violations.append("OVERSIZE")

    # No stop loss
    if entry.stop_loss_pct <= 0 or entry.stop_loss_price <= 0:
        violations.append("NO_STOP_LOSS")

    # Regime mismatch
    if entry.market_regime in ("BEAR", "RISK_OFF"):
        violations.append("REGIME_MISMATCH")

    # ABC plan violated
    if decision_snapshot is not None:
        snap_regime = decision_snapshot.market_regime
        if snap_regime in ("BEAR", "RISK_OFF") and entry.position_size_twd > 0:
            violations.append("ABC_PLAN_VIOLATED")

    return violations


def review_risk_violations(
    entry: TradeJournalEntry,
    decision_snapshot: Optional[TradeDecisionSnapshot] = None,
) -> RiskViolationReview:
    """Review risk violations and return RiskViolationReview."""
    violations = detect_violations(entry, decision_snapshot)

    oversize_detected       = "OVERSIZE" in violations
    no_stop_loss_detected   = "NO_STOP_LOSS" in violations
    regime_mismatch_detected = "REGIME_MISMATCH" in violations
    abc_plan_violated       = "ABC_PLAN_VIOLATED" in violations

    # Severity
    if len(violations) >= 3:
        severity = "CRITICAL"
        review_status = ReviewStatus.FAIL
    elif len(violations) == 2:
        severity = "HIGH"
        review_status = ReviewStatus.FAIL
    elif len(violations) == 1:
        severity = "MEDIUM"
        review_status = ReviewStatus.WARN
    else:
        severity = "NONE"
        review_status = ReviewStatus.PASS

    violation_type = ", ".join(violations) if violations else "NONE"

    return RiskViolationReview(
        symbol=entry.symbol,
        violation_date=entry.entry_date,
        violation_type=violation_type,
        severity=severity,
        oversize_detected=oversize_detected,
        no_stop_loss_detected=no_stop_loss_detected,
        regime_mismatch_detected=regime_mismatch_detected,
        abc_plan_violated=abc_plan_violated,
        notes=entry.notes,
        review_status=review_status,
    )
