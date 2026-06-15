"""
replay/replay_summary.py — ReplaySessionSummaryBuilder v1.2.0

Builds session summary.
v1.2.0: does NOT include future performance evaluation.
Does NOT show: realized returns, future max gain/loss, accuracy, hindsight score.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Future Performance Evaluation in v1.2.0.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionSummaryBuilder:
    """
    Builds session summary.
    v1.2.0: does NOT include future performance evaluation.
    Does NOT show: realized returns, future max gain/loss, accuracy, hindsight score.
    """

    NO_FUTURE_PERFORMANCE_EVALUATION = True

    def __init__(self, store=None):
        self._store = store

    def build(self, session_id: str) -> Dict[str, Any]:
        """Build complete session summary."""
        config = self._store.load_session_config(session_id) if self._store else {}
        state = self._store.load_session_state(session_id) if self._store else {}
        decisions = self._store.load_decisions(session_id) if self._store else []
        annotations = self._store.load_annotations(session_id) if self._store else []

        config = config or {}
        state = state or {}

        return {
            "session_id": session_id,
            "metadata": self._session_metadata(config, state),
            "timeline_progress": self._timeline_progress(state),
            "decision_counts": self._decision_counts(decisions),
            "action_distribution": self._action_distribution(decisions),
            "annotation_count": self._annotation_count(annotations),
            "data_availability": self._data_availability(state),
            "warnings": self._warnings(state),
            "qualification": self._qualification(state),
            "safety_status": self._safety_status(),
            "no_future_performance_evaluation": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def _session_metadata(self, config: Dict, state: Dict) -> Dict[str, Any]:
        return {
            "session_id": config.get("session_id", ""),
            "session_name": config.get("session_name", ""),
            "symbol": config.get("symbol", ""),
            "mode": config.get("mode", ""),
            "start_date": config.get("start_date", ""),
            "end_date": config.get("end_date", ""),
            "current_date": state.get("current_date", ""),
            "status": state.get("status", ""),
            "created_at": config.get("created_at", ""),
        }

    def _timeline_progress(self, state: Dict) -> Dict[str, Any]:
        current_index = int(state.get("current_index", 0))
        total_steps = int(state.get("total_steps", 0))
        pct = round(current_index / total_steps * 100, 1) if total_steps > 0 else 0.0
        return {
            "current_index": current_index,
            "total_steps": total_steps,
            "progress_pct": pct,
            "completed": bool(state.get("completed", False)),
        }

    def _decision_counts(self, decisions: List[Dict]) -> Dict[str, Any]:
        # Deduplicate by decision_id, keep latest
        seen: Dict[str, Dict] = {}
        for d in decisions:
            did = d.get("decision_id", "")
            if did:
                seen[did] = d
        unique = list(seen.values())
        return {
            "total": len(unique),
            "simulation_decision_only": True,
        }

    def _action_distribution(self, decisions: List[Dict]) -> Dict[str, int]:
        seen: Dict[str, Dict] = {}
        for d in decisions:
            did = d.get("decision_id", "")
            if did:
                seen[did] = d
        dist: Dict[str, int] = {}
        for d in seen.values():
            action = d.get("action", "UNKNOWN")
            dist[action] = dist.get(action, 0) + 1
        return dist

    def _annotation_count(self, annotations: List[Dict]) -> int:
        seen = set()
        for a in annotations:
            aid = a.get("annotation_id", "")
            if aid:
                seen.add(aid)
        return len(seen)

    def _data_availability(self, state: Dict) -> Dict[str, Any]:
        return {
            "qualification": state.get("qualification", "UNKNOWN"),
            "available_records": state.get("available_records", 0),
            "visible_from": state.get("visible_from", ""),
            "visible_to": state.get("visible_to", ""),
        }

    def _warnings(self, state: Dict) -> List[str]:
        return state.get("warnings", [])

    def _qualification(self, state: Dict) -> str:
        return state.get("qualification", "UNKNOWN")

    def _safety_status(self) -> Dict[str, Any]:
        return {
            "research_only": True,
            "no_real_orders": True,
            "simulation_decision_only": True,
            "no_future_performance_evaluation": True,
            "replay_training_only": True,
            "broker_execution_disabled": True,
            "not_investment_advice": True,
        }
