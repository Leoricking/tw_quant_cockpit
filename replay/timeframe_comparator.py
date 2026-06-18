"""
replay/timeframe_comparator.py — MultiTimeframeReplayComparator v1.2.5

Compares multi-timeframe snapshots across timestamps, timeframes, and sessions.
Before Outcome Reveal: no forward_return, PnL, final result, future high/low.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Before Outcome Reveal: no future data. No PnL. No final result.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_COMPARE_FIELDS = [
    "forward_return", "realized_pnl", "final_result",
    "future_high", "future_low", "hindsight_score",
    "outcome", "final_session_high", "final_session_low",
]


class MultiTimeframeReplayComparator:
    """
    Compares multi-timeframe replay snapshots.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Before Outcome Reveal: no future data, no PnL, no final result.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def compare_timestamps(
        self,
        session_id: str,
        timestamp_a: str,
        timestamp_b: str,
        snapshots_a: Optional[Dict[str, Any]] = None,
        snapshots_b: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Compare multi-timeframe snapshot at two timestamps."""
        return {
            "comparison_type": "timestamps",
            "session_id": session_id,
            "timestamp_a": timestamp_a,
            "timestamp_b": timestamp_b,
            "timeframe_diffs": self._diff_snapshots(snapshots_a or {}, snapshots_b or {}),
            "no_future_reveal": True,
            "research_only": True,
        }

    def compare_timeframes(
        self,
        session_id: str,
        timestamp: str,
        timeframe_a: str,
        timeframe_b: str,
        snapshot_a: Optional[Dict[str, Any]] = None,
        snapshot_b: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Compare two timeframe snapshots at same timestamp."""
        return {
            "comparison_type": "timeframes",
            "session_id": session_id,
            "timestamp": timestamp,
            "timeframe_a": timeframe_a,
            "timeframe_b": timeframe_b,
            "diff": self._diff_snapshots(
                {timeframe_a: snapshot_a or {}},
                {timeframe_b: snapshot_b or {}},
            ),
            "no_future_reveal": True,
            "research_only": True,
        }

    def compare_sessions(
        self,
        session_a: str,
        session_b: str,
        snapshot_a: Optional[Dict[str, Any]] = None,
        snapshot_b: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Compare snapshots from two different sessions."""
        return {
            "comparison_type": "sessions",
            "session_a": session_a,
            "session_b": session_b,
            "diff": self._diff_snapshots(snapshot_a or {}, snapshot_b or {}),
            "no_future_reveal": True,
            "research_only": True,
        }

    def compare_forks(
        self,
        session_id: str,
        fork_id: str,
        snapshot_main: Optional[Dict[str, Any]] = None,
        snapshot_fork: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Compare main session vs fork at fork boundary."""
        return {
            "comparison_type": "forks",
            "session_id": session_id,
            "fork_id": fork_id,
            "diff": self._diff_snapshots(snapshot_main or {}, snapshot_fork or {}),
            "no_post_fork_data": True,
            "no_future_reveal": True,
            "research_only": True,
        }

    def compare_indicators(
        self,
        indicators_a: Dict[str, Any],
        indicators_b: Dict[str, Any],
        timeframe: str,
    ) -> Dict[str, Any]:
        """Compare indicator values between two snapshots."""
        diffs = {}
        all_keys = set(indicators_a) | set(indicators_b)
        for k in all_keys:
            if k in FORBIDDEN_COMPARE_FIELDS:
                continue
            va = indicators_a.get(k)
            vb = indicators_b.get(k)
            if va != vb:
                diffs[k] = {"a": va, "b": vb}
        return {
            "timeframe": timeframe,
            "indicator_diffs": diffs,
            "changed_count": len(diffs),
            "research_only": True,
        }

    def compare_strategy(
        self,
        strategy_a: Dict[str, Any],
        strategy_b: Dict[str, Any],
        timeframe: str,
    ) -> Dict[str, Any]:
        """Compare strategy signals between two snapshots."""
        # Strip forbidden fields
        safe_a = {k: v for k, v in strategy_a.items() if k not in FORBIDDEN_COMPARE_FIELDS}
        safe_b = {k: v for k, v in strategy_b.items() if k not in FORBIDDEN_COMPARE_FIELDS}
        diffs = {}
        all_keys = set(safe_a) | set(safe_b)
        for k in all_keys:
            if safe_a.get(k) != safe_b.get(k):
                diffs[k] = {"a": safe_a.get(k), "b": safe_b.get(k)}
        return {
            "timeframe": timeframe,
            "strategy_diffs": diffs,
            "changed_count": len(diffs),
            "no_future_reveal": True,
            "research_only": True,
        }

    def summarize(self, comparison: Dict[str, Any]) -> str:
        """Return human-readable summary of comparison."""
        comp_type = comparison.get("comparison_type", "unknown")
        return (
            f"[MTF Comparison] Type: {comp_type} | "
            f"No Future Reveal | Research Only | No Real Orders"
        )

    def render_markdown(self, comparison: Dict[str, Any]) -> str:
        """Render comparison as markdown."""
        lines = [
            "## Multi-Timeframe Replay Comparison",
            f"**Type**: {comparison.get('comparison_type', 'unknown')}",
            f"**Session**: {comparison.get('session_id', 'N/A')}",
            "",
            "> Research Only | No Real Orders | No Future Data Revealed",
            "",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _diff_snapshots(
        self, snap_a: Dict[str, Any], snap_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute diff between two snapshot dicts, excluding forbidden fields."""
        safe_a = {k: v for k, v in snap_a.items() if k not in FORBIDDEN_COMPARE_FIELDS}
        safe_b = {k: v for k, v in snap_b.items() if k not in FORBIDDEN_COMPARE_FIELDS}
        diffs = {}
        all_keys = set(safe_a) | set(safe_b)
        for k in all_keys:
            va = safe_a.get(k)
            vb = safe_b.get(k)
            if va != vb:
                diffs[k] = {"a": va, "b": vb}
        return diffs
