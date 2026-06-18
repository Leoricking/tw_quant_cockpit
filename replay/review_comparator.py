"""
replay/review_comparator.py — ReplayReviewComparator v1.2.6

Compares sessions, symbols, scenarios, reviews, progress, scores, mistakes,
strategy, and timeframes.
Outcome not revealed → show NOT_AVAILABLE.

[!] Research Only. No Real Orders. Outcome NOT_AVAILABLE if not revealed.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

NOT_AVAILABLE = "NOT_AVAILABLE"


def _safe_score(row: Dict[str, Any], field: str) -> Any:
    """Return score if outcome_revealed, else NOT_AVAILABLE for outcome fields."""
    if field in ("outcome_score", "composite_score"):
        if not row.get("outcome_revealed"):
            return NOT_AVAILABLE
    return row.get(field)


class ReplayReviewComparator:
    """
    Compares two replay review sessions or groups.

    [!] Outcome not revealed → NOT_AVAILABLE.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def compare_sessions(
        self, row_a: Dict[str, Any], row_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two session rows field-by-field."""
        fields = [
            "symbol", "scenario_id", "status", "review_progress",
            "process_score", "outcome_score", "composite_score",
            "classification", "mistake_count", "confirmed_mistake_count",
            "strategy_conflicts", "mtf_conflicts", "outcome_revealed",
            "pit_verified", "elapsed_seconds", "confidence",
        ]
        comparison = {}
        for f in fields:
            va = _safe_score(row_a, f)
            vb = _safe_score(row_b, f)
            comparison[f] = {"session_a": va, "session_b": vb, "equal": va == vb}
        return {
            "session_a":    row_a.get("session_id"),
            "session_b":    row_b.get("session_id"),
            "comparison":   comparison,
            "research_only": True,
            "no_real_orders": True,
            "outcome_note": "outcome_score and composite_score are NOT_AVAILABLE until outcome_revealed=True",
        }

    def compare_symbols(
        self, rows_a: List[Dict], rows_b: List[Dict], symbol_a: str, symbol_b: str
    ) -> Dict[str, Any]:
        """Compare two symbols by aggregate process scores."""
        def _avg(rows: List[Dict], field: str) -> Optional[float]:
            vals = [r[field] for r in rows if r.get(field) is not None]
            return round(sum(vals) / len(vals), 2) if vals else None

        return {
            "symbol_a":          symbol_a,
            "symbol_b":          symbol_b,
            "avg_process_score_a": _avg(rows_a, "process_score"),
            "avg_process_score_b": _avg(rows_b, "process_score"),
            "avg_outcome_score_a": NOT_AVAILABLE,
            "avg_outcome_score_b": NOT_AVAILABLE,
            "outcome_note":      "Outcome scores NOT_AVAILABLE at aggregate level",
            "research_only":     True,
        }

    def compare_scenarios(
        self, rows_a: List[Dict], rows_b: List[Dict], scenario_a: str, scenario_b: str
    ) -> Dict[str, Any]:
        """Compare two scenarios by aggregate process scores."""
        def _avg(rows: List[Dict]) -> Optional[float]:
            vals = [r["process_score"] for r in rows if r.get("process_score") is not None]
            return round(sum(vals) / len(vals), 2) if vals else None

        return {
            "scenario_a": scenario_a,
            "scenario_b": scenario_b,
            "avg_process_score_a": _avg(rows_a),
            "avg_process_score_b": _avg(rows_b),
            "outcome_note": "Outcome NOT_AVAILABLE",
            "research_only": True,
        }

    def compare_reviews(
        self, review_a: Dict, review_b: Dict
    ) -> Dict[str, Any]:
        """Compare two review progress records."""
        return {
            "review_a": review_a,
            "review_b": review_b,
            "a_complete": review_a.get("process_review_complete"),
            "b_complete": review_b.get("process_review_complete"),
            "research_only": True,
        }

    def compare_progress(
        self, progress_a: Dict, progress_b: Dict
    ) -> Dict[str, Any]:
        """Compare two progress records."""
        return {
            "progress_pct_a": progress_a.get("progress_percent", 0),
            "progress_pct_b": progress_b.get("progress_percent", 0),
            "diff": round((progress_a.get("progress_percent", 0) or 0) -
                          (progress_b.get("progress_percent", 0) or 0), 1),
            "research_only": True,
        }

    def compare_scores(
        self, row_a: Dict, row_b: Dict
    ) -> Dict[str, Any]:
        """Compare process scores between two sessions. Outcome NOT_AVAILABLE if not revealed."""
        return {
            "process_score_a": row_a.get("process_score"),
            "process_score_b": row_b.get("process_score"),
            "outcome_score_a": _safe_score(row_a, "outcome_score"),
            "outcome_score_b": _safe_score(row_b, "outcome_score"),
            "research_only":   True,
            "outcome_note":    "outcome_score is NOT_AVAILABLE if not revealed",
        }

    def compare_mistakes(self, row_a: Dict, row_b: Dict) -> Dict[str, Any]:
        return {
            "mistake_count_a": row_a.get("mistake_count", 0),
            "mistake_count_b": row_b.get("mistake_count", 0),
            "confirmed_a":     row_a.get("confirmed_mistake_count", 0),
            "confirmed_b":     row_b.get("confirmed_mistake_count", 0),
            "research_only":   True,
        }

    def compare_strategy(self, row_a: Dict, row_b: Dict) -> Dict[str, Any]:
        return {
            "conflicts_a": row_a.get("strategy_conflicts", 0),
            "conflicts_b": row_b.get("strategy_conflicts", 0),
            "research_only": True,
        }

    def compare_timeframes(self, row_a: Dict, row_b: Dict) -> Dict[str, Any]:
        return {
            "mtf_conflicts_a": row_a.get("mtf_conflicts", 0),
            "mtf_conflicts_b": row_b.get("mtf_conflicts", 0),
            "research_only": True,
        }

    def summarize(self, comparison: Dict[str, Any]) -> str:
        """One-line text summary of a comparison."""
        sa = comparison.get("session_a", "A")
        sb = comparison.get("session_b", "B")
        return f"Session {sa} vs {sb}: see 'comparison' field for per-field diff."

    def render_markdown(self, comparison: Dict[str, Any]) -> str:
        """Render comparison as markdown."""
        sa = comparison.get("session_a", "A")
        sb = comparison.get("session_b", "B")
        lines = [f"## Session Comparison: {sa} vs {sb}", ""]
        lines.append("| Field | Session A | Session B | Equal |")
        lines.append("|---|---|---|---|")
        for field, vals in comparison.get("comparison", {}).items():
            lines.append(f"| {field} | {vals['session_a']} | {vals['session_b']} | {vals['equal']} |")
        lines.append("")
        lines.append("> [!] Research Only. No Real Orders. Outcome NOT_AVAILABLE if not revealed.")
        return "\n".join(lines)
