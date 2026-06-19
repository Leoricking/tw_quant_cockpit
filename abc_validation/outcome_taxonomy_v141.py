"""
abc_validation/outcome_taxonomy_v141.py — Outcome taxonomy for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Outcome determined only by predefined holding period or exit rule
(no post-hoc high-price labeling).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ABCOutcomeType:
    """Outcome type constants for A/B/C buy point validation."""

    SUCCESS_TREND_CONTINUATION = "SUCCESS_TREND_CONTINUATION"
    SUCCESS_QUICK_REBOUND       = "SUCCESS_QUICK_REBOUND"
    SUCCESS_SECOND_WAVE         = "SUCCESS_SECOND_WAVE"

    FAILED_SUPPORT_BREAK        = "FAILED_SUPPORT_BREAK"
    FALSE_BREAKOUT              = "FALSE_BREAKOUT"
    FALSE_RECLAIM               = "FALSE_RECLAIM"
    SIDEWAYS_CHOP               = "SIDEWAYS_CHOP"
    GAP_FAILURE                 = "GAP_FAILURE"
    STOPPED_THEN_RECOVERED      = "STOPPED_THEN_RECOVERED"
    TARGET_THEN_REVERSED        = "TARGET_THEN_REVERSED"
    NO_FILL                     = "NO_FILL"
    NO_FOLLOW_THROUGH           = "NO_FOLLOW_THROUGH"
    END_OF_DATA                 = "END_OF_DATA"
    INSUFFICIENT_DATA           = "INSUFFICIENT_DATA"
    BLOCKED                     = "BLOCKED"

    @classmethod
    def all_types(cls) -> List[str]:
        return [
            cls.SUCCESS_TREND_CONTINUATION, cls.SUCCESS_QUICK_REBOUND, cls.SUCCESS_SECOND_WAVE,
            cls.FAILED_SUPPORT_BREAK, cls.FALSE_BREAKOUT, cls.FALSE_RECLAIM,
            cls.SIDEWAYS_CHOP, cls.GAP_FAILURE, cls.STOPPED_THEN_RECOVERED,
            cls.TARGET_THEN_REVERSED, cls.NO_FILL, cls.NO_FOLLOW_THROUGH,
            cls.END_OF_DATA, cls.INSUFFICIENT_DATA, cls.BLOCKED,
        ]

    @classmethod
    def success_types(cls) -> List[str]:
        return [cls.SUCCESS_TREND_CONTINUATION, cls.SUCCESS_QUICK_REBOUND, cls.SUCCESS_SECOND_WAVE]

    @classmethod
    def failure_types(cls) -> List[str]:
        return [
            cls.FAILED_SUPPORT_BREAK, cls.FALSE_BREAKOUT, cls.FALSE_RECLAIM,
            cls.SIDEWAYS_CHOP, cls.GAP_FAILURE,
        ]


def classify_outcome(
    signal: dict,
    trade: Optional[dict],
    holding_period: int = 5,
    buy_point_type: str = "A",
) -> str:
    """
    Classify trade outcome using only predefined exit rule or holding period.
    No post-hoc high-price labeling.
    """
    if trade is None:
        return ABCOutcomeType.NO_FILL

    exit_reason = trade.get("exit_reason", "")
    net_return = trade.get("net_return")

    if net_return is None:
        return ABCOutcomeType.INSUFFICIENT_DATA

    if exit_reason == "BLOCKED":
        return ABCOutcomeType.BLOCKED

    if exit_reason.startswith("STOP"):
        # Stopped out — check if it recovered later (separate analysis only, not here)
        return ABCOutcomeType.FAILED_SUPPORT_BREAK

    if net_return > 0.03:
        # Differentiate success types by holding period
        if holding_period <= 3:
            return ABCOutcomeType.SUCCESS_QUICK_REBOUND
        elif signal.get("is_second_wave"):
            return ABCOutcomeType.SUCCESS_SECOND_WAVE
        else:
            return ABCOutcomeType.SUCCESS_TREND_CONTINUATION

    if net_return < -0.03:
        if buy_point_type == "C":
            return ABCOutcomeType.FALSE_RECLAIM
        elif buy_point_type == "B" and signal.get("was_breakout"):
            return ABCOutcomeType.FALSE_BREAKOUT
        else:
            return ABCOutcomeType.FAILED_SUPPORT_BREAK

    # Small return — sideways or no follow-through
    if abs(net_return) <= 0.01:
        return ABCOutcomeType.SIDEWAYS_CHOP

    return ABCOutcomeType.NO_FOLLOW_THROUGH
