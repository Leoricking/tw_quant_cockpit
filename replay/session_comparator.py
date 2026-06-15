"""
replay/session_comparator.py — ReplaySessionComparator v1.2.1

Compares two replay sessions on decision process and session state.
FORBIDDEN in output: realized_return, future_return, hindsight_score, final_result,
future_max_gain, future_max_loss.
This version compares decision process and session state, NOT performance.

[!] Research Only. No Real Orders. Replay Training Only.
[!] NO FUTURE PERFORMANCE COMPARISON.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_COMPARISON_FIELDS = [
    "realized_return", "future_return", "hindsight_score",
    "final_result", "future_max_gain", "future_max_loss",
]


class ReplaySessionComparator:
    """
    Compares two replay sessions on: scenario, symbol, date range, progress,
    qualification, data availability, warning counts, decision counts/actions,
    confidence, stop/target plans, annotations, PIT verification, future rows blocked,
    timeline position, checkpoints, status.
    FORBIDDEN: realized_return, future_return, hindsight_score, final_result,
    future_max_gain, future_max_loss.
    """

    FORBIDDEN_COMPARISON_FIELDS = FORBIDDEN_COMPARISON_FIELDS
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root=None):
        self._store = store
        self._repo_root = repo_root

    def _load_session(self, session_id: str) -> Dict[str, Any]:
        if self._store is None:
            return {}
        config = self._store.load_session_config(session_id) or {}
        state = self._store.load_session_state(session_id) or {}
        decisions = self._store.load_decisions(session_id) if self._store else []
        annotations = self._store.load_annotations(session_id) if self._store else []
        return {"config": config, "state": state, "decisions": decisions, "annotations": annotations}

    def compare(self, session_id_a: str, session_id_b: str) -> Dict[str, Any]:
        data_a = self._load_session(session_id_a)
        data_b = self._load_session(session_id_b)
        config_comparison = self.compare_config(data_a.get("config", {}), data_b.get("config", {}))
        progress_comparison = self.compare_progress(data_a.get("state", {}), data_b.get("state", {}))
        decision_comparison = self.compare_decisions(data_a.get("decisions", []), data_b.get("decisions", []))
        annotation_comparison = self.compare_annotations(data_a.get("annotations", []), data_b.get("annotations", []))
        quality_comparison = self.compare_quality(data_a.get("state", {}), data_b.get("state", {}))
        warning_comparison = self.compare_warnings(data_a.get("state", {}), data_b.get("state", {}))

        result = {
            "session_a": session_id_a,
            "session_b": session_id_b,
            "config": config_comparison,
            "progress": progress_comparison,
            "decisions": decision_comparison,
            "annotations": annotation_comparison,
            "quality": quality_comparison,
            "warnings": warning_comparison,
            "research_only": True,
            "no_real_orders": True,
            "no_future_performance_comparison": True,
        }
        # Ensure no forbidden fields leak in
        for ff in FORBIDDEN_COMPARISON_FIELDS:
            result.pop(ff, None)
        return result

    def compare_config(self, config_a: Dict, config_b: Dict) -> Dict[str, Any]:
        return {
            "symbol_match": config_a.get("symbol") == config_b.get("symbol"),
            "symbol_a": config_a.get("symbol"),
            "symbol_b": config_b.get("symbol"),
            "start_date_a": config_a.get("start_date"),
            "start_date_b": config_b.get("start_date"),
            "end_date_a": config_a.get("end_date"),
            "end_date_b": config_b.get("end_date"),
            "date_range_match": (config_a.get("start_date") == config_b.get("start_date") and
                                  config_a.get("end_date") == config_b.get("end_date")),
            "scenario_id_a": config_a.get("scenario_id"),
            "scenario_id_b": config_b.get("scenario_id"),
            "scenario_match": config_a.get("scenario_id") == config_b.get("scenario_id"),
        }

    def compare_progress(self, state_a: Dict, state_b: Dict) -> Dict[str, Any]:
        return {
            "current_index_a": state_a.get("current_index", 0),
            "current_index_b": state_b.get("current_index", 0),
            "total_steps_a": state_a.get("total_steps", 0),
            "total_steps_b": state_b.get("total_steps", 0),
            "current_date_a": state_a.get("current_date"),
            "current_date_b": state_b.get("current_date"),
            "status_a": state_a.get("status"),
            "status_b": state_b.get("status"),
            "pit_verified_a": state_a.get("point_in_time_verified", False),
            "pit_verified_b": state_b.get("point_in_time_verified", False),
        }

    def compare_decisions(self, decisions_a: List, decisions_b: List) -> Dict[str, Any]:
        count_a = len(decisions_a)
        count_b = len(decisions_b)
        actions_a = [d.get("action") for d in decisions_a]
        actions_b = [d.get("action") for d in decisions_b]
        conf_a = [d.get("confidence", 50) for d in decisions_a]
        conf_b = [d.get("confidence", 50) for d in decisions_b]
        avg_conf_a = sum(conf_a) / len(conf_a) if conf_a else 0
        avg_conf_b = sum(conf_b) / len(conf_b) if conf_b else 0
        return {
            "count_a": count_a,
            "count_b": count_b,
            "actions_a": actions_a,
            "actions_b": actions_b,
            "avg_confidence_a": round(avg_conf_a, 1),
            "avg_confidence_b": round(avg_conf_b, 1),
            "simulation_decision_only": True,
        }

    def compare_annotations(self, annotations_a: List, annotations_b: List) -> Dict[str, Any]:
        return {
            "count_a": len(annotations_a),
            "count_b": len(annotations_b),
            "types_a": list({a.get("annotation_type") for a in annotations_a}),
            "types_b": list({a.get("annotation_type") for a in annotations_b}),
        }

    def compare_data_availability(self, snapshot_a: Dict, snapshot_b: Dict) -> Dict[str, Any]:
        return {
            "available_a": snapshot_a.get("available_sections", []),
            "available_b": snapshot_b.get("available_sections", []),
            "unavailable_a": snapshot_a.get("unavailable_sections", []),
            "unavailable_b": snapshot_b.get("unavailable_sections", []),
        }

    def compare_quality(self, state_a: Dict, state_b: Dict) -> Dict[str, Any]:
        return {
            "qualification_a": state_a.get("qualification"),
            "qualification_b": state_b.get("qualification"),
        }

    def compare_warnings(self, state_a: Dict, state_b: Dict) -> Dict[str, Any]:
        wa = state_a.get("warnings", [])
        wb = state_b.get("warnings", [])
        return {
            "warning_count_a": len(wa),
            "warning_count_b": len(wb),
        }

    def summarize(self, comparison: Dict[str, Any]) -> str:
        a = comparison.get("session_a", "A")
        b = comparison.get("session_b", "B")
        cfg = comparison.get("config", {})
        prog = comparison.get("progress", {})
        dec = comparison.get("decisions", {})
        lines = [
            f"Session Comparison: {a} vs {b}",
            f"  Symbol match: {cfg.get('symbol_match')}",
            f"  Progress A: {prog.get('current_index_a')}/{prog.get('total_steps_a')} | B: {prog.get('current_index_b')}/{prog.get('total_steps_b')}",
            f"  Decisions A: {dec.get('count_a')} | B: {dec.get('count_b')}",
            f"  Avg Confidence A: {dec.get('avg_confidence_a')} | B: {dec.get('avg_confidence_b')}",
            f"  [!] Research Only | No Future Performance | No Real Orders",
        ]
        return "\n".join(lines)

    def render_markdown(self, comparison: Dict[str, Any]) -> str:
        lines = [
            "# Session Comparison Report",
            "",
            "> [!] Research Only | No Future Performance Comparison | No Real Orders",
            "",
            f"**Session A:** {comparison.get('session_a')}",
            f"**Session B:** {comparison.get('session_b')}",
            "",
            "## Configuration",
        ]
        cfg = comparison.get("config", {})
        lines += [
            f"- Symbol A: {cfg.get('symbol_a')} | Symbol B: {cfg.get('symbol_b')} | Match: {cfg.get('symbol_match')}",
            f"- Scenario A: {cfg.get('scenario_id_a')} | Scenario B: {cfg.get('scenario_id_b')}",
            "",
            "## Progress",
        ]
        prog = comparison.get("progress", {})
        lines += [
            f"- Status A: {prog.get('status_a')} | Status B: {prog.get('status_b')}",
            f"- Progress A: {prog.get('current_index_a')}/{prog.get('total_steps_a')}",
            f"- Progress B: {prog.get('current_index_b')}/{prog.get('total_steps_b')}",
            "",
            "## Decisions (Process Only — No Performance)",
        ]
        dec = comparison.get("decisions", {})
        lines += [
            f"- Decisions A: {dec.get('count_a')} | Decisions B: {dec.get('count_b')}",
            f"- Avg Confidence A: {dec.get('avg_confidence_a')} | B: {dec.get('avg_confidence_b')}",
            "",
            "---",
            "*Research Only. No Real Orders. No Future Performance Evaluation.*",
        ]
        return "\n".join(lines)
