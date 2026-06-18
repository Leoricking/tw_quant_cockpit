"""
replay/review_dashboard_cards.py — Dashboard Card Builders v1.2.6

Returns card dicts (value, status, confidence, tooltip, source, updated_at) for all
card categories: Session, Queue, Score, Integrity, Strategy, Timeframe, Timing.

[!] Research Only. No Real Orders. Process/Outcome Strictly Separated.
[!] Outcome Hidden Until Explicit Reveal. Not Investment Advice.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _card(
    label: str,
    value: Any,
    status: str = "OK",
    confidence: str = "SUFFICIENT",
    tooltip: str = "",
    source: str = "replay_review_dashboard",
    updated_at: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "label":      label,
        "value":      value,
        "status":     status,
        "confidence": confidence,
        "tooltip":    tooltip,
        "source":     source,
        "updated_at": updated_at or _now(),
    }


# ---------------------------------------------------------------------------
# Session Cards
# ---------------------------------------------------------------------------

def build_session_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return session count cards."""
    total = snapshot.get("total_sessions", 0)
    conf = "INSUFFICIENT" if total == 0 else "SUFFICIENT"
    return [
        _card("Total Sessions",          total,                                confidence=conf),
        _card("Active Sessions",         snapshot.get("active_sessions", 0),   confidence=conf),
        _card("Completed Sessions",      snapshot.get("completed_sessions", 0), confidence=conf),
        _card("Archived Sessions",       snapshot.get("archived_sessions", 0), confidence=conf),
        _card("Review Complete",         snapshot.get("review_complete_sessions", 0), confidence=conf),
        _card("Review Incomplete",       snapshot.get("review_incomplete_sessions", 0), confidence=conf),
    ]


# ---------------------------------------------------------------------------
# Review Queue Cards
# ---------------------------------------------------------------------------

def build_queue_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return pending review queue cards."""
    total = snapshot.get("total_pending_queue", 0)
    conf = "SUFFICIENT" if total >= 0 else "INSUFFICIENT"
    return [
        _card("Pending Outcome Reveal",    snapshot.get("pending_outcome_reveal", 0),    confidence=conf,
              tooltip="Sessions awaiting outcome reveal (explicit action required)"),
        _card("Pending Mistake Review",    snapshot.get("pending_mistake_review", 0),    confidence=conf),
        _card("Pending Strategy Review",   snapshot.get("pending_strategy_review", 0),   confidence=conf),
        _card("Pending Timeframe Review",  snapshot.get("pending_timeframe_review", 0),  confidence=conf),
        _card("Low Confidence",            snapshot.get("low_confidence_count", 0),      confidence=conf),
        _card("Insufficient Data",         snapshot.get("insufficient_data_count", 0),   confidence=conf),
    ]


# ---------------------------------------------------------------------------
# Score Cards
# ---------------------------------------------------------------------------

def build_score_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return score cards. Outcome scores hidden until revealed."""
    avg_process = snapshot.get("avg_process_score")
    ps_label = f"{avg_process:.1f}" if avg_process is not None else "N/A"
    return [
        _card("Avg Process Score",         ps_label,
              tooltip="Process score uses NO future data, NO outcome, NO PnL",
              confidence="SUFFICIENT" if avg_process is not None else "INSUFFICIENT"),
        _card("Avg Outcome Score",         "NOT_REVEALED",
              status="HIDDEN",
              tooltip="Outcome score hidden until explicit reveal per session",
              confidence="HIDDEN"),
        _card("Avg Composite Score",       "NOT_REVEALED",
              status="HIDDEN",
              tooltip="Composite score hidden until outcome revealed",
              confidence="HIDDEN"),
        _card("Good Process / Bad Outcome", "NOT_REVEALED",
              status="HIDDEN",
              tooltip="Classification hidden until outcome revealed"),
        _card("Bad Process / Good Outcome", "NOT_REVEALED",
              status="HIDDEN"),
        _card("Process Only",              "N/A",
              tooltip="Process-only review complete without outcome reveal"),
    ]


# ---------------------------------------------------------------------------
# Integrity Cards
# ---------------------------------------------------------------------------

def build_integrity_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return data integrity cards."""
    pit_fail = snapshot.get("pit_failures", 0)
    fw_blocks = snapshot.get("firewall_blocks", 0)
    pit_status = "WARN" if pit_fail > 0 else "OK"
    fw_status  = "WARN" if fw_blocks > 0 else "OK"
    return [
        _card("PIT Pass",           "N/A",      status="INFO"),
        _card("PIT Fail",           pit_fail,   status=pit_status,
              tooltip="Point-in-time verification failures"),
        _card("Firewall Blocks",    fw_blocks,  status=fw_status,
              tooltip="Future data firewall blocks"),
        _card("Partial Bar Reviews","N/A",      status="INFO"),
        _card("Missing Timeframes", "N/A",      status="INFO"),
        _card("Timing Approximate", "N/A",      status="INFO"),
    ]


# ---------------------------------------------------------------------------
# Strategy Cards
# ---------------------------------------------------------------------------

def build_strategy_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return strategy knowledge cards."""
    conflicts = snapshot.get("strategy_conflicts", 0)
    warnings  = snapshot.get("strategy_warnings", 0)
    c_status  = "WARN" if conflicts > 0 else "OK"
    return [
        _card("Strategy Conflicts",    conflicts, status=c_status,
              tooltip="Multi-module strategy conflicts (training only)"),
        _card("Strategy Warnings",     warnings,  status="INFO"),
        _card("Rule Followed",         "N/A",     status="INFO"),
        _card("Rule Contradicted",     "N/A",     status="INFO"),
        _card("Module Unavailable",    "N/A",     status="INFO"),
    ]


# ---------------------------------------------------------------------------
# Timeframe Cards
# ---------------------------------------------------------------------------

def build_timeframe_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return multi-timeframe availability cards."""
    tf_conflicts = snapshot.get("timeframe_conflicts", 0)
    c_status = "WARN" if tf_conflicts > 0 else "OK"
    return [
        _card("D1 Available",      "N/A", status="INFO"),
        _card("M60 Available",     "N/A", status="INFO"),
        _card("M20 Available",     "N/A", status="INFO"),
        _card("M5 Available",      "N/A", status="INFO"),
        _card("M1 Available",      "N/A", status="INFO"),
        _card("MTF Conflicts",     tf_conflicts, status=c_status,
              tooltip="Multi-timeframe alignment conflicts (training only)"),
    ]


# ---------------------------------------------------------------------------
# Timing Cards
# ---------------------------------------------------------------------------

def build_timing_cards(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return review timing cards."""
    total_elapsed = snapshot.get("total_review_elapsed_seconds", 0.0)
    avg_elapsed   = snapshot.get("avg_review_elapsed_seconds", 0.0)
    total_label = f"{int(total_elapsed)}s" if total_elapsed else "0s"
    avg_label   = f"{avg_elapsed:.1f}s" if avg_elapsed else "N/A"
    return [
        _card("Total Review Time",       total_label),
        _card("Avg Review Time",         avg_label),
        _card("Longest Review",          "N/A"),
        _card("Batch Total Elapsed",     "N/A"),
        _card("Current Batch Elapsed",   "N/A"),
    ]
