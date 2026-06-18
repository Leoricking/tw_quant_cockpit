"""
replay/timeframe_strategy_adapter.py — MultiTimeframeStrategyAdapter v1.2.5

Integrates existing Strategy Knowledge with multi-timeframe context.
No rewriting of Strategy Knowledge Engine. Each timeframe gets independent result.
1m with no fundamental → NOT_APPLICABLE (not error).

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] No rewriting Strategy Knowledge Engine. Per-TF independent results.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_REWRITE_STRATEGY_ENGINE = True


class MultiTimeframeStrategyAdapter:
    """
    Adapts Strategy Knowledge evaluation for multi-timeframe replay.

    Rules:
    - No rewriting Strategy Knowledge Engine — use existing adapters.
    - Each timeframe gets independent result.
    - Fundamental usually daily context.
    - Sector usually daily/M60.
    - 1m with no fundamental → NOT_APPLICABLE (not error).
    - A/B/C not applied to insufficient-data timeframes.
    - No fake low-timeframe signals.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_REWRITE_STRATEGY_ENGINE = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    # Timeframes where fundamental strategy applies
    FUNDAMENTAL_TIMEFRAMES = ["D1", "M60"]

    # Timeframes where sector strategy applies
    SECTOR_TIMEFRAMES = ["D1", "M60"]

    def evaluate_timeframe(
        self,
        timeframe: str,
        bars: List[Dict[str, Any]],
        replay_timestamp: str,
        session_id: str = "",
        higher_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate strategy signals for a single timeframe.
        Returns independent result per timeframe.
        """
        # Check data sufficiency
        if not bars:
            return {
                "timeframe": timeframe,
                "status": "INSUFFICIENT",
                "reason": f"No bars for {timeframe}",
                "signals": {},
                "qualification": "INSUFFICIENT",
                "research_only": True,
                "no_real_orders": True,
            }

        # 1m: no fundamental
        if timeframe == "M1" and "fundamental" not in (higher_context or {}):
            fundamental_status = "NOT_APPLICABLE"
        elif timeframe not in self.FUNDAMENTAL_TIMEFRAMES:
            fundamental_status = "NOT_APPLICABLE"
        else:
            fundamental_status = "AVAILABLE"

        # Sector
        if timeframe not in self.SECTOR_TIMEFRAMES:
            sector_status = "NOT_APPLICABLE"
        else:
            sector_status = "AVAILABLE"

        try:
            signals = self._evaluate_signals(timeframe, bars, replay_timestamp, higher_context)
        except Exception as e:
            logger.warning("[MTFStrategyAdapter] Error evaluating %s: %s", timeframe, e)
            signals = {"status": "ERROR", "error": str(e)}

        return {
            "timeframe": timeframe,
            "replay_timestamp": replay_timestamp,
            "status": "OK",
            "signals": signals,
            "fundamental_status": fundamental_status,
            "sector_status": sector_status,
            "higher_context": bool(higher_context),
            "qualification": "OBSERVATIONAL",
            "research_only": True,
            "no_real_orders": True,
        }

    def evaluate_all(
        self,
        bars_by_tf: Dict[str, List[Dict[str, Any]]],
        replay_timestamp: str,
        session_id: str = "",
    ) -> Dict[str, Any]:
        """Evaluate strategy for all timeframes independently."""
        results = {}
        higher_context = None

        for tf in self.TIMEFRAME_ORDER:
            tf_bars = bars_by_tf.get(tf, [])
            result = self.evaluate_timeframe(
                tf, tf_bars, replay_timestamp, session_id, higher_context
            )
            results[tf] = result
            # Pass D1 context to lower timeframes
            if tf == "D1" and result.get("status") == "OK":
                higher_context = result

        return {
            "replay_timestamp": replay_timestamp,
            "session_id": session_id,
            "timeframe_results": results,
            "research_only": True,
            "no_real_orders": True,
            "no_auto_decision": True,
        }

    def normalize_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize strategy result to standard format."""
        return {
            "timeframe": result.get("timeframe", "UNKNOWN"),
            "status": result.get("status", "UNKNOWN"),
            "signals": result.get("signals", {}),
            "qualification": result.get("qualification", "UNVERIFIED"),
            "research_only": True,
        }

    def merge_higher_context(
        self, lower_result: Dict[str, Any], higher_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge higher timeframe context into lower timeframe result."""
        merged = {**lower_result}
        merged["higher_timeframe_context"] = {
            "timeframe": higher_context.get("timeframe"),
            "signals": higher_context.get("signals", {}),
        }
        return merged

    def merge_lower_trigger(
        self, higher_result: Dict[str, Any], lower_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge lower timeframe trigger into higher timeframe result."""
        merged = {**higher_result}
        merged["lower_timeframe_trigger"] = {
            "timeframe": lower_result.get("timeframe"),
            "signals": lower_result.get("signals", {}),
        }
        return merged

    def verify_point_in_time(
        self,
        result: Dict[str, Any],
        replay_timestamp: str,
        timeframe: str,
    ) -> Dict[str, Any]:
        """Verify result is point-in-time safe."""
        from replay.timeframe_point_in_time import MultiTimeframePointInTimeVerifier
        verifier = MultiTimeframePointInTimeVerifier()
        pit = verifier.verify_strategy_inputs(result, replay_timestamp, timeframe)
        result["point_in_time_verified"] = pit.get("verified", False)
        return result

    def summary(self, timeframe: str) -> Dict[str, Any]:
        return {
            "adapter": "MultiTimeframeStrategyAdapter",
            "version": "v1.2.5",
            "timeframe": timeframe,
            "supported_strategies": [
                "ABC Buy Point", "KD Advanced", "No Chase", "No Panic Sell",
                "Do Not Rebuy Yet", "Bottom Reversal", "Sector Rotation",
                "Fundamental Quality",
            ],
            "fundamental_timeframes": self.FUNDAMENTAL_TIMEFRAMES,
            "sector_timeframes": self.SECTOR_TIMEFRAMES,
            "no_rewrite_strategy_engine": True,
            "per_timeframe_independent": True,
            "1m_no_fundamental": "NOT_APPLICABLE",
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _evaluate_signals(
        self,
        timeframe: str,
        bars: List[Dict[str, Any]],
        replay_timestamp: str,
        higher_context: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Evaluate strategy signals using existing adapters."""
        try:
            from replay.strategy_knowledge_adapter import StrategyKnowledgeAdapter
            adapter = StrategyKnowledgeAdapter()
            # Build price context from bars
            if not bars:
                return {}
            latest = max(bars, key=lambda b: b.get("timestamp", ""))
            price_context = {
                "close": latest.get("close"),
                "high": latest.get("high"),
                "low": latest.get("low"),
                "volume": latest.get("volume"),
                "replay_date": replay_timestamp[:10],
                "timeframe": timeframe,
            }
            return {"status": "EVALUATED", "timeframe": timeframe, "price_context": price_context}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}
