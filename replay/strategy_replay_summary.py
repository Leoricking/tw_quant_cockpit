"""
replay/strategy_replay_summary.py — Summary builder for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] NEVER claims strategy effectiveness.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class StrategyReplaySummaryBuilder:
    """
    Builds summaries for strategy replay data.

    Supports: session, journal, symbol, scenario, module, global summaries.
    NEVER claims strategy effectiveness.
    After Outcome Reveal: can add OBSERVATIONAL signal/outcome comparison.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        if store is not None:
            self._store = store
        else:
            from replay.strategy_replay_store import StrategyReplayStore
            self._store = StrategyReplayStore(repo_root=repo_root)

    def session_summary(self, session_id: str) -> Dict[str, Any]:
        """Build summary for a single session."""
        snapshots = self._store.load_by_session("snapshot", session_id)
        agreements = self._store.load_by_session("agreement", session_id)
        conflicts = self._store.load_by_session("conflict", session_id)
        reviews = self._store.load_by_session("rule_review", session_id)

        module_availability = self._module_availability(snapshots)
        bullish_signals = self._signal_distribution(snapshots, "bullish_modules")
        bearish_signals = self._signal_distribution(snapshots, "bearish_modules")
        warning_signals = self._signal_distribution(snapshots, "warning_modules")

        return {
            "session_id": session_id,
            "snapshots_count": len(snapshots),
            "module_availability": module_availability,
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "warning_signals": warning_signals,
            "agreement_distribution": self._agreement_distribution(agreements),
            "conflict_distribution": self._conflict_distribution(conflicts),
            "rule_followed": sum(1 for r in reviews if r.get("relationship") == "FOLLOWED"),
            "rule_ignored": sum(1 for r in reviews if r.get("relationship") == "IGNORED"),
            "rule_contradicted": sum(1 for r in reviews if r.get("relationship") == "CONTRADICTED"),
            "suggested_reviews": sum(1 for r in reviews if r.get("status") in ("SUGGESTED", "NEEDS_REVIEW")),
            "confirmed_reviews": sum(1 for r in reviews if r.get("status") == "CONFIRMED"),
            "timing_warnings": self._count_timing_warnings(snapshots),
            "insufficient_modules": self._count_insufficient(snapshots),
            "confidence": "OBSERVATIONAL",
            "sample_count": len(snapshots),
            "research_only": True,
            "no_real_orders": True,
            "note": "NEVER claims strategy effectiveness. Research use only.",
        }

    def symbol_summary(self, symbol: str) -> Dict[str, Any]:
        """Build summary for all sessions with a symbol."""
        all_snaps = self._store.load_snapshots()
        snapshots = [s for s in all_snaps if s.get("symbol") == symbol]
        return {
            "symbol": symbol,
            "snapshots_count": len(snapshots),
            "module_availability": self._module_availability(snapshots),
            "research_only": True,
            "note": "NEVER claims strategy effectiveness.",
        }

    def scenario_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Build summary for a scenario."""
        all_snaps = self._store.load_snapshots()
        snapshots = [
            s for s in all_snaps
            if s.get("source_metadata", {}).get("scenario_id") == scenario_id
        ]
        return {
            "scenario_id": scenario_id,
            "snapshots_count": len(snapshots),
            "module_availability": self._module_availability(snapshots),
            "research_only": True,
        }

    def module_summary(self, module_name: str) -> Dict[str, Any]:
        """Build summary for a single module across all sessions."""
        all_results = self._store.load_module_results()
        results = [r for r in all_results if r.get("module_name") == module_name]
        signals = [r.get("signal", "") for r in results]
        available_count = sum(1 for r in results if r.get("available", False))
        return {
            "module_name": module_name,
            "total_evaluations": len(results),
            "available_count": available_count,
            "unavailable_count": len(results) - available_count,
            "signal_distribution": self._count_values(signals),
            "research_only": True,
        }

    def global_summary(self) -> Dict[str, Any]:
        """Global summary across all data."""
        all_snaps = self._store.load_snapshots()
        all_reviews = self._store.load_rule_reviews()
        sessions = set(s.get("session_id", "") for s in all_snaps)
        return {
            "total_sessions": len(sessions),
            "total_snapshots": len(all_snaps),
            "total_rule_reviews": len(all_reviews),
            "suggested_reviews": sum(1 for r in all_reviews if r.get("status") == "SUGGESTED"),
            "confirmed_reviews": sum(1 for r in all_reviews if r.get("status") == "CONFIRMED"),
            "research_only": True,
            "note": "NEVER claims strategy effectiveness. Research use only.",
        }

    def _module_availability(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        availability: Dict[str, Dict[str, int]] = {}
        for snap in snapshots:
            for mod in snap.get("modules", []):
                name = mod.get("module_name", "")
                if name not in availability:
                    availability[name] = {"available": 0, "unavailable": 0}
                if mod.get("available", False):
                    availability[name]["available"] += 1
                else:
                    availability[name]["unavailable"] += 1
        return availability

    def _signal_distribution(
        self, snapshots: List[Dict[str, Any]], field: str
    ) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for snap in snapshots:
            for mod_name in snap.get(field, []):
                counts[mod_name] = counts.get(mod_name, 0) + 1
        return counts

    def _agreement_distribution(
        self, agreements: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for agr in agreements:
            status = agr.get("status", "UNKNOWN")
            counts[status] = counts.get(status, 0) + 1
        return counts

    def _conflict_distribution(
        self, conflicts: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for conf in conflicts:
            ct = conf.get("conflict_type", "UNKNOWN")
            counts[ct] = counts.get(ct, 0) + 1
        return counts

    def _count_timing_warnings(self, snapshots: List[Dict[str, Any]]) -> int:
        count = 0
        for snap in snapshots:
            for mod in snap.get("modules", []):
                if mod.get("timing_warning"):
                    count += 1
        return count

    def _count_insufficient(self, snapshots: List[Dict[str, Any]]) -> int:
        return sum(
            1 for snap in snapshots
            if len(snap.get("unavailable_modules", [])) > 5
        )

    def _count_values(self, values: List[str]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in values:
            counts[v] = counts.get(v, 0) + 1
        return counts
