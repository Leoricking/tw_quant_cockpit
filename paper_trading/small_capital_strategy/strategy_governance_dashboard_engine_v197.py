"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_engine_v197.py
Core engine for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

_VERSION = "1.9.7"
_SCHEMA = "197"
_PAPER_HEADER = {
    "paper_only": True,
    "governance_analytics_only": True,
    "dashboard_only": True,
    "quality_analytics_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "analytics_executes_decision": False,
    "dashboard_mutates_strategy": False,
    "schema_version": _SCHEMA,
}

_FORBIDDEN = frozenset(["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                         "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"])
_ALLOWED_ACTIONS = frozenset([
    "GOVERNANCE_DASHBOARD_VERSION", "GOVERNANCE_DASHBOARD_RUN", "GOVERNANCE_DASHBOARD_QUALITY",
    "GOVERNANCE_DASHBOARD_SCORECARD", "GOVERNANCE_DASHBOARD_EVIDENCE", "GOVERNANCE_DASHBOARD_OUTCOMES",
    "GOVERNANCE_DASHBOARD_VIOLATIONS", "GOVERNANCE_DASHBOARD_ROLLBACK_FREQUENCY",
    "GOVERNANCE_DASHBOARD_LINEAGE_HEALTH", "GOVERNANCE_DASHBOARD_AUDIT_HEALTH",
    "GOVERNANCE_DASHBOARD_REPORT", "GOVERNANCE_DASHBOARD_EXPORT", "GOVERNANCE_DASHBOARD_HEALTH",
    "GOVERNANCE_DASHBOARD_GATE", "GOVERNANCE_DASHBOARD_SCENARIOS", "GOVERNANCE_DASHBOARD_FIXTURES",
    "GOVERNANCE_DASHBOARD_SAFETY_AUDIT", "QUALITY_ANALYTICS",
])
_VALID_ANALYTICS_WINDOWS = frozenset([
    "DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "FULL_HISTORY",
])
_VALID_QUALITY_GRADES = frozenset([
    "EXCELLENT", "GOOD", "WATCH", "WEAK", "INVALID",
])
_VALID_DASHBOARD_PANELS = frozenset([
    "quality_overview", "evidence_coverage", "decision_outcome",
    "approval_quality", "rejection_quality", "keep_monitoring_quality",
    "rollback_review_frequency", "governance_violations",
    "decision_lineage_health", "audit_trail_health", "safety_summary", "export_manifest",
])
_UNSAFE_PATH_PATTERNS = (
    "production", "prod_db", "live_db", "broker_", "real_trade", "real_order",
    "/etc/", "\\etc\\", "c:/windows/", "c:/program files/",
)


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        **_PAPER_HEADER,
        "valid": False,
        "blocked": True,
        "block_reason": reason,
        "reason": reason,
        "block_reasons": [reason],
    }


def _ok(**extra) -> Dict[str, Any]:
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "block_reason": "",
        "reason": "",
        "block_reasons": [],
        **extra,
    }


def _is_unsafe_path(path: str) -> bool:
    if not path:
        return True
    lower = path.lower()
    if path.startswith("/") or (len(path) > 1 and path[1] == ":"):
        safe_absolute = ("c:/users/", "c:/tmp/")
        if not any(lower.startswith(p) for p in safe_absolute):
            return True
    return any(d in lower for d in _UNSAFE_PATH_PATTERNS)


def validate_dashboard_action(action: str) -> Dict[str, Any]:
    """Validate a dashboard action against allowed/forbidden lists."""
    upper = action.upper() if action else ""
    if upper in _FORBIDDEN:
        return _blocked(f"forbidden_dashboard_action: {action}")
    if upper in _ALLOWED_ACTIONS:
        return _ok(action=action)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_dashboard_action: {action}",
            "reason": f"unknown_dashboard_action: {action}",
            "block_reasons": [f"unknown_dashboard_action: {action}"]}


def validate_analytics_window(window: str) -> Dict[str, Any]:
    """Validate an analytics window type."""
    if not window:
        return _blocked("missing_analytics_window")
    if window.upper() in _VALID_ANALYTICS_WINDOWS:
        return _ok(window=window)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_analytics_window: {window}",
            "reason": f"unknown_analytics_window: {window}",
            "block_reasons": [f"unknown_analytics_window: {window}"]}


def validate_quality_grade(grade: str) -> Dict[str, Any]:
    """Validate a quality grade value."""
    if not grade:
        return _blocked("missing_quality_grade")
    if grade.upper() in _VALID_QUALITY_GRADES:
        return _ok(grade=grade)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_quality_grade: {grade}",
            "reason": f"unknown_quality_grade: {grade}",
            "block_reasons": [f"unknown_quality_grade: {grade}"]}


def validate_dashboard_panel(panel: str) -> Dict[str, Any]:
    """Validate a dashboard panel name."""
    if not panel:
        return _blocked("missing_dashboard_panel")
    if panel.lower() in _VALID_DASHBOARD_PANELS:
        return _ok(panel=panel)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_dashboard_panel: {panel}",
            "reason": f"unknown_dashboard_panel: {panel}",
            "block_reasons": [f"unknown_dashboard_panel: {panel}"]}


def build_dashboard_input(registry_source: str, analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build and validate a governance dashboard input. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    if analytics_window.upper() not in _VALID_ANALYTICS_WINDOWS:
        return _blocked(f"unknown_analytics_window: {analytics_window}")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        decision_ids=[],
    )


def build_quality_score(decision_id: str, metrics: Dict[str, float] = None) -> Dict[str, Any]:
    """Build a quality score for a decision. Blocks on missing decision_id."""
    if not decision_id:
        return _blocked("missing_decision_id")
    m = metrics or {}
    composite = sum(m.values()) / max(len(m), 1) if m else 0.0
    return _ok(
        decision_id=decision_id,
        evidence_coverage_score=m.get("evidence_coverage_score", 0.0),
        rationale_completeness_score=m.get("rationale_completeness_score", 0.0),
        checklist_completeness_score=m.get("checklist_completeness_score", 0.0),
        lineage_completeness_score=m.get("lineage_completeness_score", 0.0),
        audit_trail_completeness_score=m.get("audit_trail_completeness_score", 0.0),
        outcome_consistency_score=m.get("outcome_consistency_score", 0.0),
        rollback_review_frequency_score=m.get("rollback_review_frequency_score", 0.0),
        governance_violation_score=m.get("governance_violation_score", 0.0),
        paper_only_safety_score=m.get("paper_only_safety_score", 0.0),
        decision_latency_score=m.get("decision_latency_score", 0.0),
        review_quality_score=m.get("review_quality_score", 0.0),
        registry_integrity_score=m.get("registry_integrity_score", 0.0),
        composite_score=composite,
    )


def build_quality_grade(decision_id: str, composite_score: float = 0.0) -> Dict[str, Any]:
    """Assign a quality grade based on composite score. Blocks on missing decision_id."""
    if not decision_id:
        return _blocked("missing_decision_id")
    if composite_score >= 0.85:
        grade = "EXCELLENT"
    elif composite_score >= 0.70:
        grade = "GOOD"
    elif composite_score >= 0.50:
        grade = "WATCH"
    elif composite_score > 0.0:
        grade = "WEAK"
    else:
        grade = "INVALID"
    return _ok(
        decision_id=decision_id,
        grade=grade,
        composite_score=composite_score,
        grade_reason=f"composite_score={composite_score:.3f}",
    )


def build_quality_summary(registry_source: str, analytics_window: str = "FULL_HISTORY",
                           decision_scores: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Build a quality summary across decisions. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    scores = decision_scores or []
    total = len(scores)
    avg = sum(s.get("composite_score", 0.0) for s in scores) / max(total, 1)
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_decisions=total,
        average_composite_score=avg,
    )


def build_evidence_coverage_summary(registry_source: str,
                                     analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build evidence coverage summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_decisions=0,
        decisions_with_full_evidence=0,
        decisions_with_partial_evidence=0,
        decisions_with_no_evidence=0,
        average_evidence_score=0.0,
    )


def build_outcome_summary(registry_source: str,
                           analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build decision outcome summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_decisions=0,
        approved_count=0,
        rejected_count=0,
        keep_monitoring_count=0,
        rollback_review_count=0,
    )


def build_violation_summary(registry_source: str,
                             analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build governance violation summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_violations=0,
        unique_violation_types=0,
        most_common_violation="",
    )


def build_rollback_review_frequency(registry_source: str,
                                     analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build rollback review frequency report. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_rollback_reviews=0,
        rollback_review_rate=0.0,
        auto_rollback=False,
        requires_human_review=True,
    )


def build_approval_quality_summary(registry_source: str,
                                    analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build approval quality summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_approved=0,
        average_quality_score=0.0,
        high_quality_count=0,
        low_quality_count=0,
        auto_approval=False,
        no_production_mutation=True,
    )


def build_rejection_quality_summary(registry_source: str,
                                     analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build rejection quality summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_rejected=0,
        average_quality_score=0.0,
        most_common_rejection_reason="",
    )


def build_monitoring_quality_summary(registry_source: str,
                                      analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build keep-monitoring decision quality summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_keep_monitoring=0,
        average_quality_score=0.0,
        decisions_needing_followup=[],
    )


def build_consistency_summary(registry_source: str,
                               analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build decision consistency summary. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        total_decisions=0,
        consistent_decisions=0,
        inconsistent_decisions=0,
        consistency_rate=0.0,
    )


def build_decision_trend(registry_source: str,
                          analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build decision quality trend data. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        trend_direction="STABLE",
        quality_delta=0.0,
        period_scores=[],
    )


def build_dashboard_panel(panel_name: str, registry_source: str = "") -> Dict[str, Any]:
    """Build a single dashboard panel. Blocks on unknown panel name."""
    if not panel_name:
        return _blocked("missing_panel_name")
    if panel_name.lower() not in _VALID_DASHBOARD_PANELS:
        return _blocked(f"unknown_dashboard_panel: {panel_name}")
    return _ok(
        panel_name=panel_name,
        registry_source=registry_source,
        data={},
        empty_state=f"No data for panel {panel_name}.",
    )


def build_dashboard_export(export_path: str, panels: List[str] = None) -> Dict[str, Any]:
    """Build dashboard export manifest. Blocks on unsafe paths."""
    if _is_unsafe_path(export_path):
        return _blocked("unsafe_export_path")
    return _ok(
        export_path=export_path,
        panels_included=list(panels or []),
        export_format="JSON",
        safe_path_only=True,
    )


def build_quality_report(registry_source: str,
                          analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Build a full quality analytics report. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        report_sections=[
            "quality_overview", "evidence_coverage", "decision_outcome",
            "approval_quality", "rejection_quality", "governance_violations",
            "rollback_review_frequency", "consistency_summary", "trend",
        ],
        total_decisions_analyzed=0,
        report_only=True,
    )


def build_quality_audit_trail(analytics_run_id: str) -> Dict[str, Any]:
    """Build an audit trail for the analytics run. Blocks on missing run_id."""
    if not analytics_run_id:
        return _blocked("missing_analytics_run_id")
    return _ok(
        analytics_run_id=analytics_run_id,
        entries=[],
        immutable=True,
        audit_only=True,
    )


def build_quality_health_summary(all_passed: bool = False,
                                  passed: int = 0, failed: int = 0,
                                  total: int = 0) -> Dict[str, Any]:
    """Build a quality health summary."""
    return _ok(
        all_passed=all_passed,
        status="PASS" if all_passed else "FAIL",
        passed=passed,
        failed=failed,
        total=total,
    )


def build_validation_result(registry_source: str,
                              analytics_window: str = "FULL_HISTORY") -> Dict[str, Any]:
    """Validate a dashboard analytics input. Blocks on missing registry_source."""
    if not registry_source:
        return _blocked("missing_registry_source")
    violations = []
    if analytics_window.upper() not in _VALID_ANALYTICS_WINDOWS:
        violations.append(f"unknown_analytics_window: {analytics_window}")
    return _ok(
        registry_source=registry_source,
        analytics_window=analytics_window,
        violations=violations,
        governance_passed=len(violations) == 0,
    )


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return _ok(
        version=_VERSION,
        engine="strategy_governance_dashboard_engine_v197",
        functions=[
            "validate_dashboard_action", "validate_analytics_window",
            "validate_quality_grade", "validate_dashboard_panel",
            "build_dashboard_input", "build_quality_score", "build_quality_grade",
            "build_quality_summary", "build_evidence_coverage_summary",
            "build_outcome_summary", "build_violation_summary",
            "build_rollback_review_frequency", "build_approval_quality_summary",
            "build_rejection_quality_summary", "build_monitoring_quality_summary",
            "build_consistency_summary", "build_decision_trend",
            "build_dashboard_panel", "build_dashboard_export",
            "build_quality_report", "build_quality_audit_trail",
            "build_quality_health_summary", "build_validation_result",
        ],
    )
