"""
abc_validation/failure_rate_analyzer_v141.py — Failure rate analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .outcome_taxonomy_v141 import ABCOutcomeType


class ABCFailureRateAnalyzer:
    """
    Computes failure rates per buy point type.

    Per type: signal_failure_rate, stop_out_rate, no_follow_through_rate,
    false_breakout_rate, false_reclaim_rate, support_break_rate,
    stopped_then_recovered_rate, target_then_reversed_rate, no_fill_rate.
    """

    def analyze(
        self,
        signals: List[dict],
        trades: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Compute failure rates for all signals."""
        trades = trades or []

        trade_by_signal = {t.get("signal_id"): t for t in trades}

        outcome_counts: Dict[str, int] = {o: 0 for o in ABCOutcomeType.all_types()}
        total = len(signals)

        for sig in signals:
            sig_id = sig.get("signal_id", "")
            trade = trade_by_signal.get(sig_id)
            from .outcome_taxonomy_v141 import classify_outcome
            outcome = classify_outcome(sig, trade, buy_point_type=buy_point_type)
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1

        def rate(count: int) -> Optional[float]:
            if total == 0:
                return None
            return count / total

        filled_total = total - outcome_counts.get(ABCOutcomeType.NO_FILL, 0)

        signal_failure_rate = rate(
            outcome_counts.get(ABCOutcomeType.FAILED_SUPPORT_BREAK, 0) +
            outcome_counts.get(ABCOutcomeType.FALSE_BREAKOUT, 0) +
            outcome_counts.get(ABCOutcomeType.FALSE_RECLAIM, 0) +
            outcome_counts.get(ABCOutcomeType.GAP_FAILURE, 0)
        )

        stop_out_rate = rate(
            outcome_counts.get(ABCOutcomeType.FAILED_SUPPORT_BREAK, 0)
        )

        no_follow_through_rate = rate(
            outcome_counts.get(ABCOutcomeType.NO_FOLLOW_THROUGH, 0) +
            outcome_counts.get(ABCOutcomeType.SIDEWAYS_CHOP, 0)
        )

        return {
            "buy_point_type": buy_point_type,
            "total_signals": total,
            "filled_total": filled_total,
            "outcome_counts": outcome_counts,
            "signal_failure_rate": signal_failure_rate,
            "stop_out_rate": stop_out_rate,
            "no_follow_through_rate": no_follow_through_rate,
            "false_breakout_rate": rate(outcome_counts.get(ABCOutcomeType.FALSE_BREAKOUT, 0)),
            "false_reclaim_rate": rate(outcome_counts.get(ABCOutcomeType.FALSE_RECLAIM, 0)),
            "support_break_rate": rate(outcome_counts.get(ABCOutcomeType.FAILED_SUPPORT_BREAK, 0)),
            "stopped_then_recovered_rate": rate(outcome_counts.get(ABCOutcomeType.STOPPED_THEN_RECOVERED, 0)),
            "target_then_reversed_rate": rate(outcome_counts.get(ABCOutcomeType.TARGET_THEN_REVERSED, 0)),
            "no_fill_rate": rate(outcome_counts.get(ABCOutcomeType.NO_FILL, 0)),
            "no_real_orders": True,
        }
