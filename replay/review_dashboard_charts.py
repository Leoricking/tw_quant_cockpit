"""
replay/review_dashboard_charts.py — Chart Data Spec Builders v1.2.6

Not GUI-framework-specific. Returns dicts with type/labels/data/title/metadata.
Rules: Process/Outcome not mixed, Mock/Real separated, Missing/Insufficient
visible, no future data.

[!] Research Only. No Real Orders. Process/Outcome Strictly Separated.
[!] Outcome data excluded unless outcome_revealed=True. Not Investment Advice.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _chart(
    chart_type: str,
    title: str,
    labels: List[str],
    data: List[Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "type":     chart_type,
        "title":    title,
        "labels":   labels,
        "data":     data,
        "metadata": metadata or {},
        "research_only":     True,
        "no_real_orders":    True,
        "no_future_data":    True,
        "process_outcome_separated": True,
    }


def build_review_progress_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution of review progress statuses."""
    counts = Counter(r.get("review_progress", "NOT_STARTED") for r in rows)
    labels = ["NOT_STARTED", "IN_PROGRESS", "REVIEW_COMPLETE", "BLOCKED", "INSUFFICIENT"]
    data   = [counts.get(l, 0) for l in labels]
    return _chart("bar", "Review Progress Distribution", labels, data)


def build_process_score_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution of process scores (process only — no outcome)."""
    scores = [r["process_score"] for r in rows if r.get("process_score") is not None]
    buckets = ["0-20", "21-40", "41-60", "61-80", "81-100"]
    ranges  = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
    data    = [sum(1 for s in scores if lo <= s <= hi) for lo, hi in ranges]
    return _chart("histogram", "Process Score Distribution (Process Only — No Outcome)", buckets, data,
                  metadata={"note": "Process scores use NO future data, NO outcome, NO PnL"})


def build_outcome_score_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution of outcome scores — only for revealed sessions."""
    revealed_rows = [r for r in rows if r.get("outcome_revealed") and r.get("outcome_score") is not None]
    scores = [r["outcome_score"] for r in revealed_rows]
    buckets = ["0-20", "21-40", "41-60", "61-80", "81-100"]
    ranges  = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
    data    = [sum(1 for s in scores if lo <= s <= hi) for lo, hi in ranges]
    return _chart("histogram", "Outcome Score Distribution (Revealed Sessions Only)", buckets, data,
                  metadata={"hidden_count": len(rows) - len(revealed_rows),
                             "note": "Outcome scores shown only for sessions with outcome_revealed=True"})


def build_composite_classification_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Composite classification distribution — only for revealed sessions."""
    revealed = [r for r in rows if r.get("outcome_revealed")]
    counts = Counter(r.get("classification", "UNCLASSIFIED") for r in revealed)
    labels = list(counts.keys())
    data   = [counts[l] for l in labels]
    return _chart("pie", "Composite Classification Distribution (Revealed Only)", labels, data)


def build_mistake_type_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution of mistake counts per session."""
    labels = ["0 Mistakes", "1 Mistake", "2 Mistakes", "3+ Mistakes"]
    data = [
        sum(1 for r in rows if r.get("mistake_count", 0) == 0),
        sum(1 for r in rows if r.get("mistake_count", 0) == 1),
        sum(1 for r in rows if r.get("mistake_count", 0) == 2),
        sum(1 for r in rows if r.get("mistake_count", 0) >= 3),
    ]
    return _chart("bar", "Suggested Mistake Count Distribution", labels, data,
                  metadata={"note": "Suggested only — not confirmed"})


def build_mistake_severity_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder — requires mistake detail rows."""
    return _chart("bar", "Mistake Severity Distribution", [], [],
                  metadata={"status": "REQUIRES_DETAIL_DATA"})


def build_strategy_conflict_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution of strategy conflicts per session."""
    labels = ["No Conflict", "1 Conflict", "2+ Conflicts"]
    data = [
        sum(1 for r in rows if r.get("strategy_conflicts", 0) == 0),
        sum(1 for r in rows if r.get("strategy_conflicts", 0) == 1),
        sum(1 for r in rows if r.get("strategy_conflicts", 0) >= 2),
    ]
    return _chart("bar", "Strategy Conflict Distribution (Training Only)", labels, data)


def build_timeframe_conflict_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution of MTF conflicts per session."""
    labels = ["No MTF Conflict", "1 Conflict", "2+ Conflicts"]
    data = [
        sum(1 for r in rows if r.get("mtf_conflicts", 0) == 0),
        sum(1 for r in rows if r.get("mtf_conflicts", 0) == 1),
        sum(1 for r in rows if r.get("mtf_conflicts", 0) >= 2),
    ]
    return _chart("bar", "Multi-Timeframe Conflict Distribution", labels, data)


def build_module_availability_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder for module availability."""
    return _chart("bar", "Module Availability", [], [], metadata={"status": "REQUIRES_HEALTH_DATA"})


def build_timeframe_availability_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder for timeframe availability per session."""
    return _chart("bar", "Timeframe Availability", ["D1", "M60", "M20", "M5", "M1"],
                  [0, 0, 0, 0, 0], metadata={"status": "REQUIRES_MTF_DATA"})


def build_review_time_trend(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Review time trend per session."""
    labels = [r.get("session_id", "?") for r in rows]
    data   = [r.get("elapsed_seconds", 0.0) for r in rows]
    return _chart("line", "Review Time Trend (seconds per session)", labels, data)


def build_sessions_reviewed_per_day(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Sessions reviewed per day."""
    from collections import Counter
    day_counts = Counter(r.get("updated_at", "")[:10] for r in rows if r.get("review_complete"))
    labels = sorted(day_counts.keys())
    data   = [day_counts[l] for l in labels]
    return _chart("line", "Sessions Reviewed Per Day", labels, data)


def build_confidence_distribution(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Confidence level distribution across sessions."""
    counts = Counter(r.get("confidence", "INSUFFICIENT") for r in rows)
    labels = ["SUFFICIENT", "LOW", "INSUFFICIENT"]
    data   = [counts.get(l, 0) for l in labels]
    return _chart("bar", "Confidence Distribution", labels, data)


def build_scenario_comparison(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process score comparison across scenarios (process only)."""
    from collections import defaultdict
    by_scenario: dict = defaultdict(list)
    for r in rows:
        scen = r.get("scenario_id") or "UNKNOWN"
        ps = r.get("process_score")
        if ps is not None:
            by_scenario[scen].append(ps)
    labels = list(by_scenario.keys())
    data   = [round(sum(v) / len(v), 2) if v else 0 for v in by_scenario.values()]
    return _chart("bar", "Scenario Comparison — Avg Process Score", labels, data,
                  metadata={"note": "Process scores only. No outcome."})


def build_symbol_comparison(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process score comparison across symbols (process only)."""
    from collections import defaultdict
    by_symbol: dict = defaultdict(list)
    for r in rows:
        sym = r.get("symbol") or "UNKNOWN"
        ps = r.get("process_score")
        if ps is not None:
            by_symbol[sym].append(ps)
    labels = list(by_symbol.keys())
    data   = [round(sum(v) / len(v), 2) if v else 0 for v in by_symbol.values()]
    return _chart("bar", "Symbol Comparison — Avg Process Score", labels, data,
                  metadata={"note": "Process scores only. No outcome."})
