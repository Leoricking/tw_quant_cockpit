"""
replay/timeframe_context_builder.py — MultiTimeframeContextBuilder v1.2.5

Builds full multi-timeframe context dict for a session at replay_timestamp.
Output keys: replay_timestamp, D1, M60, M20, M5, M1, agreement, conflicts,
warnings, point_in_time_verified.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class MultiTimeframeContextBuilder:
    """
    Builds multi-timeframe context for replay sessions.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def build(
        self,
        session_id: str,
        replay_timestamp: str,
        symbol: str = "",
        bars_by_tf: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        session_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Build full multi-timeframe context dict.
        Returns dict with keys: replay_timestamp, D1, M60, M20, M5, M1,
        agreement, conflicts, warnings, point_in_time_verified.
        """
        bars_by_tf     = bars_by_tf or {}
        session_config = session_config or {}
        warnings: List[str] = []
        all_verified = True

        context: Dict[str, Any] = {
            "replay_timestamp": replay_timestamp,
            "session_id": session_id,
            "symbol": symbol,
        }

        # Build per-timeframe context
        for tf in self.TIMEFRAME_ORDER:
            tf_bars = bars_by_tf.get(tf, [])
            try:
                tf_ctx = self.build_timeframe(
                    session_id, replay_timestamp, tf, tf_bars, symbol
                )
                context[tf] = tf_ctx
                if not tf_ctx.get("point_in_time_verified", True):
                    all_verified = False
                warnings.extend(tf_ctx.get("warnings", []))
            except Exception as e:
                context[tf] = self._unavailable_context(tf, str(e))
                warnings.append(f"{tf} context error: {e}")

        # Agreement analysis
        try:
            context["agreement"] = self._build_agreement(context, replay_timestamp)
        except Exception as e:
            context["agreement"] = {"status": "ERROR", "error": str(e)}
            warnings.append(f"Agreement error: {e}")

        # Conflict analysis
        try:
            context["conflicts"] = self._build_conflicts(context, replay_timestamp)
        except Exception as e:
            context["conflicts"] = {"status": "ERROR", "error": str(e)}
            warnings.append(f"Conflict error: {e}")

        context["warnings"]              = warnings
        context["point_in_time_verified"] = all_verified
        context["research_only"]          = True
        context["no_real_orders"]         = True

        return context

    def build_timeframe(
        self,
        session_id: str,
        replay_timestamp: str,
        timeframe: str,
        bars: List[Dict[str, Any]],
        symbol: str = "",
    ) -> Dict[str, Any]:
        """Build context for a single timeframe."""
        warnings: List[str] = []

        from replay.timeframe_alignment import TimeframeAlignmentEngine
        from replay.timeframe_indicator_engine import MultiTimeframeIndicatorEngine
        from replay.timeframe_point_in_time import MultiTimeframePointInTimeVerifier

        alignment_engine = TimeframeAlignmentEngine()
        indicator_engine = MultiTimeframeIndicatorEngine()
        pit_verifier     = MultiTimeframePointInTimeVerifier()

        # Latest completed bar
        latest_completed = alignment_engine.latest_completed_bar(replay_timestamp, timeframe, bars)

        # Current partial bar (if any)
        current_partial = alignment_engine.current_partial_bar(replay_timestamp, timeframe, bars)

        # Indicators (completed bars only)
        indicators = {}
        if bars:
            try:
                indicators = indicator_engine.calculate(bars, timeframe, replay_timestamp)
                warnings.extend(indicators.get("warnings", []))
            except Exception as e:
                indicators = {"status": "ERROR", "error": str(e)}
                warnings.append(f"Indicator calc error [{timeframe}]: {e}")

        # Point-in-time verification
        pit_result = pit_verifier.verify_snapshot(
            {
                "timeframe": timeframe,
                "replay_timestamp": replay_timestamp,
                "current_bar": current_partial,
                "latest_completed_bar": latest_completed,
            },
            replay_timestamp,
        )

        return {
            "timeframe": timeframe,
            "replay_timestamp": replay_timestamp,
            "symbol": symbol,
            "latest_completed_bar": latest_completed,
            "current_partial_bar": current_partial,
            "has_data": latest_completed is not None,
            "indicators": indicators,
            "trend_state": indicators.get("trend_state", "UNKNOWN") if isinstance(indicators, dict) else "UNKNOWN",
            "volume_state": indicators.get("volume_state", "UNKNOWN") if isinstance(indicators, dict) else "UNKNOWN",
            "point_in_time_verified": pit_result.get("verified", False),
            "warnings": warnings,
            "research_only": True,
        }

    def build_daily_context(
        self, session_id: str, replay_timestamp: str, bars: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build D1 context (previous completed daily bar only)."""
        return self.build_timeframe(session_id, replay_timestamp, "D1", bars)

    def build_intraday_context(
        self, session_id: str, replay_timestamp: str, timeframe: str,
        bars: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build intraday context for given timeframe."""
        return self.build_timeframe(session_id, replay_timestamp, timeframe, bars)

    def build_parent_context(
        self, session_id: str, replay_timestamp: str, timeframe: str,
        bars_by_tf: Dict[str, List[Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        """Build context for parent timeframe."""
        from replay.timeframe_registry import ReplayTimeframeRegistry
        registry = ReplayTimeframeRegistry()
        parent_tf = registry.parent(timeframe)
        if not parent_tf:
            return None
        parent_bars = bars_by_tf.get(parent_tf, [])
        return self.build_timeframe(session_id, replay_timestamp, parent_tf, parent_bars)

    def build_child_context(
        self, session_id: str, replay_timestamp: str, timeframe: str,
        bars_by_tf: Dict[str, List[Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        """Build context for child timeframe."""
        from replay.timeframe_registry import ReplayTimeframeRegistry
        registry = ReplayTimeframeRegistry()
        child_tf = registry.child(timeframe)
        if not child_tf:
            return None
        child_bars = bars_by_tf.get(child_tf, [])
        return self.build_timeframe(session_id, replay_timestamp, child_tf, child_bars)

    def build_strategy_context(
        self, session_id: str, replay_timestamp: str, timeframe: str,
        bars: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build strategy context for timeframe (stub)."""
        return {
            "timeframe": timeframe,
            "replay_timestamp": replay_timestamp,
            "strategy_signals": {},
            "research_only": True,
        }

    def build_indicator_context(
        self, replay_timestamp: str, timeframe: str, bars: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build indicator context for timeframe."""
        from replay.timeframe_indicator_engine import MultiTimeframeIndicatorEngine
        engine = MultiTimeframeIndicatorEngine()
        return engine.calculate(bars, timeframe, replay_timestamp)

    def build_availability(
        self, bars_by_tf: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, str]:
        """Build timeframe availability map."""
        availability = {}
        for tf in self.TIMEFRAME_ORDER:
            bars = bars_by_tf.get(tf, [])
            availability[tf] = "AVAILABLE" if bars else "UNAVAILABLE"
        return availability

    def summary(self, session_id: str, replay_timestamp: str) -> Dict[str, Any]:
        return {
            "builder": "MultiTimeframeContextBuilder",
            "version": "v1.2.5",
            "session_id": session_id,
            "replay_timestamp": replay_timestamp,
            "timeframes": self.TIMEFRAME_ORDER,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _unavailable_context(self, timeframe: str, reason: str) -> Dict[str, Any]:
        return {
            "timeframe": timeframe,
            "status": "UNAVAILABLE",
            "reason": reason,
            "has_data": False,
            "point_in_time_verified": False,
            "warnings": [reason],
            "research_only": True,
        }

    def _build_agreement(self, context: Dict[str, Any], replay_timestamp: str) -> Dict[str, Any]:
        """Build agreement analysis from per-TF contexts."""
        from replay.timeframe_agreement import MultiTimeframeAgreementAnalyzer
        analyzer = MultiTimeframeAgreementAnalyzer()
        return analyzer.analyze(context)

    def _build_conflicts(self, context: Dict[str, Any], replay_timestamp: str) -> Dict[str, Any]:
        """Build conflict analysis from per-TF contexts."""
        from replay.timeframe_conflict import MultiTimeframeConflictAnalyzer
        analyzer = MultiTimeframeConflictAnalyzer()
        conflicts = analyzer.detect(context)
        return {"conflicts": conflicts, "count": len(conflicts), "research_only": True}
