"""
replay/timeframe_agreement.py — MultiTimeframeAgreementAnalyzer v1.2.5

Analyzes trend/momentum/volume/support/strategy alignment across timeframes.
Agreement for training only — no auto-trade.
Unavailable timeframe ≠ bearish.
Partial bar ≠ confirmed signal.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Agreement is for training awareness only. No auto-trade. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_AUTO_TRADE = True

AGREEMENT_STATES = [
    "HIGHER_TIMEFRAME_BULLISH_LOWER_TIMEFRAME_PULLBACK",
    "HIGHER_TIMEFRAME_BEARISH_LOWER_TIMEFRAME_REBOUND",
    "FULL_BULLISH_ALIGNMENT",
    "FULL_BEARISH_ALIGNMENT",
    "MIXED_STRUCTURE",
    "INSUFFICIENT",
]


class MultiTimeframeAgreementAnalyzer:
    """
    Analyzes cross-timeframe agreement for replay training.

    Rules:
    - Higher TF not always right; lower TF not noise.
    - Unavailable ≠ bearish.
    - Partial bar ≠ confirmed signal.
    - Agreement for training only — no auto-trade.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_AUTO_TRADE = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def analyze(self, multi_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze agreement across all timeframes.
        Returns agreement dict with status, scores, explanations.
        """
        replay_timestamp = multi_context.get("replay_timestamp", "")
        bullish = []
        bearish = []
        neutral = []
        unavailable = []

        for tf in self.TIMEFRAME_ORDER:
            tf_ctx = multi_context.get(tf) or {}
            if not tf_ctx.get("has_data", False):
                unavailable.append(tf)
                continue
            trend = tf_ctx.get("trend_state", "UNKNOWN")
            trend_class = self.classify_trend(trend)
            if trend_class == "BULLISH":
                bullish.append(tf)
            elif trend_class == "BEARISH":
                bearish.append(tf)
            else:
                neutral.append(tf)

        agreement_score = self.calculate_agreement(bullish, bearish, neutral, unavailable)
        conflict_score  = self.calculate_conflict(bullish, bearish, neutral, unavailable)

        status = self._determine_status(bullish, bearish, neutral, unavailable)

        dominant_tf = self.determine_dominant_timeframe(bullish, bearish, neutral)
        trigger_tf  = self.determine_trigger_timeframe(multi_context)

        explanation = self.explain(status, bullish, bearish, neutral, unavailable)

        warnings = []
        if unavailable:
            warnings.append(f"Unavailable timeframes (not bearish): {unavailable}")

        return {
            "status": status,
            "agreement_score": agreement_score,
            "conflict_score": conflict_score,
            "bullish_timeframes": bullish,
            "bearish_timeframes": bearish,
            "neutral_timeframes": neutral,
            "unavailable_timeframes": unavailable,
            "dominant_timeframe": dominant_tf,
            "trigger_timeframe": trigger_tf,
            "explanation": explanation,
            "warnings": warnings,
            "replay_timestamp": replay_timestamp,
            "research_only": True,
            "no_auto_trade": True,
            "training_only": True,
        }

    def classify_trend(self, trend_state: str) -> str:
        """Classify trend state as BULLISH/BEARISH/NEUTRAL."""
        if trend_state in ("UPTREND",):
            return "BULLISH"
        if trend_state in ("DOWNTREND",):
            return "BEARISH"
        if trend_state in ("UNKNOWN", "UNAVAILABLE", "INSUFFICIENT", "ERROR"):
            return "NEUTRAL"
        return "NEUTRAL"

    def classify_momentum(self, indicators: Dict[str, Any]) -> str:
        """Classify momentum from indicators."""
        try:
            rsi = indicators.get("RSI")
            if rsi is None:
                return "NEUTRAL"
            if rsi > 60:
                return "BULLISH"
            if rsi < 40:
                return "BEARISH"
            return "NEUTRAL"
        except Exception:
            return "NEUTRAL"

    def calculate_agreement(
        self,
        bullish: List[str],
        bearish: List[str],
        neutral: List[str],
        unavailable: List[str],
    ) -> float:
        """Calculate agreement score 0.0–1.0. Unavailable = neutral (not bearish)."""
        total = len(bullish) + len(bearish) + len(neutral)
        if total == 0:
            return 0.0
        majority = max(len(bullish), len(bearish))
        return round(majority / total, 3)

    def calculate_conflict(
        self,
        bullish: List[str],
        bearish: List[str],
        neutral: List[str],
        unavailable: List[str],
    ) -> float:
        """Calculate conflict score 0.0–1.0."""
        total = len(bullish) + len(bearish)
        if total == 0:
            return 0.0
        minority = min(len(bullish), len(bearish))
        return round(minority / total, 3)

    def determine_dominant_timeframe(
        self, bullish: List[str], bearish: List[str], neutral: List[str]
    ) -> Optional[str]:
        """Return dominant timeframe (highest with clear direction)."""
        for tf in self.TIMEFRAME_ORDER:
            if tf in bullish or tf in bearish:
                return tf
        return None

    def determine_trigger_timeframe(self, multi_context: Dict[str, Any]) -> Optional[str]:
        """Return trigger timeframe from session config or default."""
        session_config = multi_context.get("session_config") or {}
        return session_config.get("trigger_timeframe", "M5")

    def explain(
        self,
        status: str,
        bullish: List[str],
        bearish: List[str],
        neutral: List[str],
        unavailable: List[str],
    ) -> str:
        """Generate human-readable explanation."""
        parts = []
        if bullish:
            parts.append(f"Bullish: {', '.join(bullish)}")
        if bearish:
            parts.append(f"Bearish: {', '.join(bearish)}")
        if neutral:
            parts.append(f"Neutral: {', '.join(neutral)}")
        if unavailable:
            parts.append(f"Unavailable (not bearish): {', '.join(unavailable)}")
        parts.append(f"Status: {status}")
        parts.append("[Research Only | No Auto Trade]")
        return " | ".join(parts)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _determine_status(
        self,
        bullish: List[str],
        bearish: List[str],
        neutral: List[str],
        unavailable: List[str],
    ) -> str:
        """Determine agreement status."""
        available = bullish + bearish + neutral
        if len(available) < 2:
            return "INSUFFICIENT"
        # Full alignment
        if len(bearish) == 0 and len(bullish) >= 3:
            return "FULL_BULLISH_ALIGNMENT"
        if len(bullish) == 0 and len(bearish) >= 3:
            return "FULL_BEARISH_ALIGNMENT"
        # Higher bullish, lower pullback
        higher_tfs = ["D1", "M60"]
        lower_tfs  = ["M5", "M1"]
        higher_bullish = [tf for tf in bullish if tf in higher_tfs]
        lower_bearish  = [tf for tf in bearish  if tf in lower_tfs]
        if higher_bullish and lower_bearish:
            return "HIGHER_TIMEFRAME_BULLISH_LOWER_TIMEFRAME_PULLBACK"
        higher_bearish = [tf for tf in bearish  if tf in higher_tfs]
        lower_bullish  = [tf for tf in bullish  if tf in lower_tfs]
        if higher_bearish and lower_bullish:
            return "HIGHER_TIMEFRAME_BEARISH_LOWER_TIMEFRAME_REBOUND"
        return "MIXED_STRUCTURE"
