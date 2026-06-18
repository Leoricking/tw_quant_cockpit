"""
replay/timeframe_conflict.py — MultiTimeframeConflictAnalyzer v1.2.5

Detects cross-timeframe conflicts. Conflict can only suggest NEEDS_REVIEW.
Cannot auto-block Decision, auto-create Decision, auto-Confirm Mistake,
auto-modify Score, or auto-trade.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Conflict suggests NEEDS_REVIEW only. No auto-block. No auto-decision.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_AUTO_BLOCK = True
NO_AUTO_DECISION = True

CONFLICT_TYPES = [
    "DAILY_BULLISH_INTRADAY_BEARISH",
    "DAILY_BEARISH_INTRADAY_BULLISH",
    "HIGHER_TF_TREND_LOWER_TF_REVERSAL",
    "HIGHER_TF_SUPPORT_LOWER_TF_BREAKDOWN",
    "LOWER_TF_BREAKOUT_WITH_HIGHER_TF_RESISTANCE",
    "LOWER_TF_BUY_SIGNAL_WITH_DAILY_NO_CHASE",
    "INTRADAY_ENTRY_WITH_DAILY_FUNDAMENTAL_WARNING",
    "M1_SIGNAL_WITH_M5_UNCONFIRMED",
    "M5_SIGNAL_WITH_M20_CONFLICT",
    "M20_SIGNAL_WITH_M60_CONFLICT",
    "PARTIAL_BAR_CONFLICT",
    "DATA_AVAILABILITY_CONFLICT",
    "STALE_TIMEFRAME_CONFLICT",
    "UNKNOWN",
]

SEVERITY_LEVELS = ["P0", "P1", "P2", "P3"]


@staticmethod
def _classify_trend(trend_state: str) -> str:
    if trend_state in ("UPTREND",):
        return "BULLISH"
    if trend_state in ("DOWNTREND",):
        return "BEARISH"
    return "NEUTRAL"


class ConflictRecord:
    """A single conflict detection result."""

    def __init__(
        self,
        conflict_type: str,
        severity: str,
        evidence: str,
        needs_review: bool = True,
        timeframes_involved: Optional[List[str]] = None,
    ) -> None:
        self.conflict_type = conflict_type
        self.severity = severity
        self.evidence = evidence
        self.needs_review = needs_review
        self.timeframes_involved = timeframes_involved or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conflict_type": self.conflict_type,
            "severity": self.severity,
            "evidence": self.evidence,
            "needs_review": self.needs_review,
            "timeframes_involved": self.timeframes_involved,
            "auto_block": False,
            "auto_decision": False,
            "auto_confirm_mistake": False,
            "auto_modify_score": False,
            "auto_trade": False,
            "research_only": True,
        }


class MultiTimeframeConflictAnalyzer:
    """
    Detects cross-timeframe conflicts in replay.

    Rules:
    - Conflict → NEEDS_REVIEW, suggest Journal, suggest Mistake.
    - Cannot auto-block Decision.
    - Cannot auto-create Decision.
    - Cannot auto-Confirm Mistake.
    - Cannot auto-modify Score.
    - Cannot auto-trade.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_AUTO_BLOCK = True
    NO_AUTO_DECISION = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def detect(self, multi_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect all conflicts in multi-timeframe context.
        Returns list of conflict dicts.
        """
        conflicts: List[ConflictRecord] = []

        # Get trend states per TF
        trends = {}
        for tf in self.TIMEFRAME_ORDER:
            tf_ctx = multi_context.get(tf) or {}
            trend = tf_ctx.get("trend_state", "UNKNOWN")
            trends[tf] = _classify_trend(trend)

        # D1 vs intraday
        d1_trend = trends.get("D1", "NEUTRAL")
        m60_trend = trends.get("M60", "NEUTRAL")
        m20_trend = trends.get("M20", "NEUTRAL")
        m5_trend  = trends.get("M5", "NEUTRAL")
        m1_trend  = trends.get("M1", "NEUTRAL")

        if d1_trend == "BULLISH" and m60_trend == "BEARISH":
            conflicts.append(ConflictRecord(
                "DAILY_BULLISH_INTRADAY_BEARISH", "P1",
                f"D1=BULLISH vs M60=BEARISH",
                timeframes_involved=["D1", "M60"],
            ))

        if d1_trend == "BEARISH" and m60_trend == "BULLISH":
            conflicts.append(ConflictRecord(
                "DAILY_BEARISH_INTRADAY_BULLISH", "P1",
                f"D1=BEARISH vs M60=BULLISH",
                timeframes_involved=["D1", "M60"],
            ))

        # M5 vs M20
        if m5_trend == "BULLISH" and m20_trend == "BEARISH":
            conflicts.append(ConflictRecord(
                "M5_SIGNAL_WITH_M20_CONFLICT", "P2",
                f"M5=BULLISH vs M20=BEARISH",
                timeframes_involved=["M5", "M20"],
            ))

        # M20 vs M60
        if m20_trend == "BULLISH" and m60_trend == "BEARISH":
            conflicts.append(ConflictRecord(
                "M20_SIGNAL_WITH_M60_CONFLICT", "P2",
                f"M20=BULLISH vs M60=BEARISH",
                timeframes_involved=["M20", "M60"],
            ))

        # M1 vs M5
        if m1_trend == "BULLISH" and m5_trend == "BEARISH":
            conflicts.append(ConflictRecord(
                "M1_SIGNAL_WITH_M5_UNCONFIRMED", "P2",
                f"M1=BULLISH vs M5=BEARISH",
                timeframes_involved=["M1", "M5"],
            ))

        # Partial bar conflict
        for tf in self.TIMEFRAME_ORDER:
            tf_ctx = multi_context.get(tf) or {}
            if tf_ctx.get("current_partial_bar"):
                conflicts.append(ConflictRecord(
                    "PARTIAL_BAR_CONFLICT", "P3",
                    f"{tf} has partial bar — signals unconfirmed",
                    timeframes_involved=[tf],
                ))

        # Data availability conflict
        unavailable = [
            tf for tf in self.TIMEFRAME_ORDER
            if not (multi_context.get(tf) or {}).get("has_data", False)
        ]
        if unavailable:
            conflicts.append(ConflictRecord(
                "DATA_AVAILABILITY_CONFLICT", "P3",
                f"Unavailable timeframes: {unavailable}",
                timeframes_involved=unavailable,
            ))

        return [c.to_dict() for c in conflicts]

    def severity(self, conflict_type: str) -> str:
        """Return default severity for conflict type."""
        severity_map = {
            "DAILY_BULLISH_INTRADAY_BEARISH": "P1",
            "DAILY_BEARISH_INTRADAY_BULLISH": "P1",
            "HIGHER_TF_TREND_LOWER_TF_REVERSAL": "P1",
            "HIGHER_TF_SUPPORT_LOWER_TF_BREAKDOWN": "P0",
            "LOWER_TF_BREAKOUT_WITH_HIGHER_TF_RESISTANCE": "P1",
            "LOWER_TF_BUY_SIGNAL_WITH_DAILY_NO_CHASE": "P1",
            "INTRADAY_ENTRY_WITH_DAILY_FUNDAMENTAL_WARNING": "P1",
            "M1_SIGNAL_WITH_M5_UNCONFIRMED": "P2",
            "M5_SIGNAL_WITH_M20_CONFLICT": "P2",
            "M20_SIGNAL_WITH_M60_CONFLICT": "P2",
            "PARTIAL_BAR_CONFLICT": "P3",
            "DATA_AVAILABILITY_CONFLICT": "P3",
            "STALE_TIMEFRAME_CONFLICT": "P2",
            "UNKNOWN": "P3",
        }
        return severity_map.get(conflict_type, "P3")

    def evidence(self, conflict: Dict[str, Any]) -> str:
        """Return evidence string for conflict."""
        return conflict.get("evidence", "No evidence recorded")

    def explain(self, conflict: Dict[str, Any]) -> str:
        """Return human-readable explanation for conflict."""
        ct = conflict.get("conflict_type", "UNKNOWN")
        ev = conflict.get("evidence", "")
        sv = conflict.get("severity", "P3")
        tfs = conflict.get("timeframes_involved", [])
        return (
            f"[{sv}] {ct}: {ev} | Timeframes: {tfs} | "
            "Status: NEEDS_REVIEW (cannot auto-block or auto-confirm)"
        )

    def requires_review(self, conflict: Dict[str, Any]) -> bool:
        """Return True if conflict requires manual review."""
        return conflict.get("needs_review", True)

    def summary(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "total_conflicts": len(conflicts),
            "by_severity": {
                sev: len([c for c in conflicts if c.get("severity") == sev])
                for sev in SEVERITY_LEVELS
            },
            "needs_review_count": len([c for c in conflicts if c.get("needs_review")]),
            "auto_block": False,
            "auto_decision": False,
            "auto_confirm_mistake": False,
            "auto_modify_score": False,
            "auto_trade": False,
            "research_only": True,
            "no_real_orders": True,
        }
