"""
replay/timeframe_summary.py — MultiTimeframeSummaryBuilder v1.2.5

Builds summary reports for multi-timeframe replay sessions.
Never claims strategy effectiveness.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Never claims strategy effectiveness.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NEVER_CLAIMS_EFFECTIVENESS = True


class MultiTimeframeSummaryBuilder:
    """
    Builds summaries for multi-timeframe replay.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Never claims strategy effectiveness.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NEVER_CLAIMS_EFFECTIVENESS = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def build_session_summary(
        self, session_id: str, store=None
    ) -> Dict[str, Any]:
        """Build session-level summary."""
        snapshots = []
        if store:
            snapshots = store.get_snapshots(session_id=session_id)

        available_tfs = set()
        unavailable_tfs = set()
        partial_bars = 0
        pit_failures = 0

        for snap in snapshots:
            tf = snap.get("timeframe", "")
            if snap.get("has_data"):
                available_tfs.add(tf)
            else:
                unavailable_tfs.add(tf)
            if snap.get("current_bar") and snap["current_bar"].get("is_partial"):
                partial_bars += 1
            if not snap.get("point_in_time_verified", True):
                pit_failures += 1

        return {
            "scope": "session",
            "session_id": session_id,
            "snapshot_count": len(snapshots),
            "available_timeframes": sorted(available_tfs),
            "unavailable_timeframes": sorted(unavailable_tfs),
            "partial_bar_count": partial_bars,
            "point_in_time_failures": pit_failures,
            "data_gaps": [],
            "stale_data_count": 0,
            "research_only": True,
            "no_real_orders": True,
            "never_claims_effectiveness": True,
            "disclaimer": "This summary is for research and training only. Not Investment Advice.",
        }

    def build_symbol_summary(
        self, symbol: str, store=None
    ) -> Dict[str, Any]:
        """Build symbol-level summary."""
        snapshots = []
        if store:
            all_snaps = store.get_snapshots()
            snapshots = [s for s in all_snaps if s.get("symbol") == symbol]

        sessions = set(s.get("session_id") for s in snapshots)
        return {
            "scope": "symbol",
            "symbol": symbol,
            "session_count": len(sessions),
            "snapshot_count": len(snapshots),
            "research_only": True,
            "no_real_orders": True,
            "never_claims_effectiveness": True,
        }

    def build_scenario_summary(
        self, scenario_id: str, store=None
    ) -> Dict[str, Any]:
        """Build scenario-level summary."""
        return {
            "scope": "scenario",
            "scenario_id": scenario_id,
            "research_only": True,
            "no_real_orders": True,
            "never_claims_effectiveness": True,
        }

    def build_timeframe_summary(
        self, timeframe: str, store=None
    ) -> Dict[str, Any]:
        """Build timeframe-level summary."""
        snapshots = []
        if store:
            all_snaps = store.get_snapshots()
            snapshots = [s for s in all_snaps if s.get("timeframe") == timeframe]

        partial_bars = sum(
            1 for s in snapshots
            if s.get("current_bar") and s["current_bar"].get("is_partial")
        )

        return {
            "scope": "timeframe",
            "timeframe": timeframe,
            "snapshot_count": len(snapshots),
            "partial_bar_count": partial_bars,
            "research_only": True,
            "no_real_orders": True,
            "never_claims_effectiveness": True,
        }

    def build_global_summary(self, store=None) -> Dict[str, Any]:
        """Build global summary across all sessions."""
        all_snaps = []
        if store:
            all_snaps = store.get_snapshots()

        sessions = set(s.get("session_id") for s in all_snaps)
        symbols  = set(s.get("symbol") for s in all_snaps)
        agreement_counts: Dict[str, int] = {}
        conflict_counts: Dict[str, int] = {}

        return {
            "scope": "global",
            "total_sessions": len(sessions),
            "total_symbols": len(symbols),
            "total_snapshots": len(all_snaps),
            "timeframe_availability": {tf: 0 for tf in self.TIMEFRAME_ORDER},
            "agreement_distribution": agreement_counts,
            "conflict_distribution": conflict_counts,
            "point_in_time_failures": 0,
            "data_gaps": [],
            "real_mock_separation": "Real data only in real mode",
            "confidence": "OBSERVATIONAL",
            "disclaimer": "Global summary for training awareness. Not Investment Advice.",
            "research_only": True,
            "no_real_orders": True,
            "never_claims_effectiveness": True,
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "builder": "MultiTimeframeSummaryBuilder",
            "version": "v1.2.5",
            "scopes": ["session", "symbol", "scenario", "timeframe", "global"],
            "never_claims_effectiveness": True,
            "research_only": True,
            "no_real_orders": True,
        }
