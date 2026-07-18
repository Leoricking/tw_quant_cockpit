"""
paper_trading/small_capital_strategy/strategy_monitoring_report_v194.py
Report export functions for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA = "194"
_SAFE = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, monitoring_only=True, drift_detection_only=True,
    rollback_trigger_only=True, review_only=True, report_only=True,
    audit_only=True, no_real_orders=True, no_broker=True, no_margin=True,
    no_leverage=True, no_production_strategy_mutation=True,
    no_live_strategy_activation=True, not_investment_advice=True,
    demo_only=True, not_for_production=True, production_trading_blocked=True,
)


def export_monitoring_summary(monitoring_id: str, period_label: str = "") -> Dict[str, Any]:
    """Export a monitoring summary report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "monitoring_summary",
        "monitoring_id": monitoring_id,
        "period_label": period_label,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_drift_report(monitoring_id: str, drift_signals: Optional[List] = None) -> Dict[str, Any]:
    """Export a drift detection report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "drift_report",
        "monitoring_id": monitoring_id,
        "drift_signal_count": len(drift_signals) if drift_signals else 0,
        "drift_signals": drift_signals or [],
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_rollback_trigger_report(monitoring_id: str, triggers: Optional[List] = None) -> Dict[str, Any]:
    """Export a rollback trigger report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "rollback_trigger_report",
        "monitoring_id": monitoring_id,
        "trigger_count": len(triggers) if triggers else 0,
        "triggers": triggers or [],
        "auto_rollback": False,
        "requires_manual_review": True,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_evidence_pack_report(monitoring_id: str, evidence_id: str = "") -> Dict[str, Any]:
    """Export an evidence pack report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "evidence_pack_report",
        "monitoring_id": monitoring_id,
        "evidence_id": evidence_id,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_audit_trail_report(monitoring_id: str, audit_id: str = "") -> Dict[str, Any]:
    """Export an audit trail report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "audit_trail_report",
        "monitoring_id": monitoring_id,
        "audit_id": audit_id,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_dashboard_report(monitoring_id: str, dashboard_id: str = "") -> Dict[str, Any]:
    """Export a dashboard report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "dashboard_report",
        "monitoring_id": monitoring_id,
        "dashboard_id": dashboard_id,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_performance_comparison_report(
    monitoring_id: str,
    baseline_snapshot_id: str = "",
    current_snapshot_id: str = "",
) -> Dict[str, Any]:
    """Export a performance comparison report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "performance_comparison_report",
        "monitoring_id": monitoring_id,
        "baseline_snapshot_id": baseline_snapshot_id,
        "current_snapshot_id": current_snapshot_id,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_signal_quality_report(monitoring_id: str, period_label: str = "") -> Dict[str, Any]:
    """Export a signal quality monitoring report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "signal_quality_report",
        "monitoring_id": monitoring_id,
        "period_label": period_label,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_guardrail_status_report(monitoring_id: str, period_label: str = "") -> Dict[str, Any]:
    """Export a guardrail status monitoring report."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "guardrail_status_report",
        "monitoring_id": monitoring_id,
        "period_label": period_label,
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def export_full_monitoring_pack(monitoring_id: str, export_format: str = "JSON") -> Dict[str, Any]:
    """Export a full monitoring pack containing all sub-reports."""
    if not monitoring_id:
        return {"blocked": True, "valid": False,
                "block_reason": "missing_monitoring_id", **_SAFE, "schema_version": _SCHEMA}
    return {
        "report_type": "full_monitoring_pack",
        "monitoring_id": monitoring_id,
        "export_format": export_format,
        "sections": [
            "monitoring_summary",
            "drift_report",
            "rollback_trigger_report",
            "evidence_pack_report",
            "audit_trail_report",
            "dashboard_report",
            "performance_comparison_report",
            "signal_quality_report",
            "guardrail_status_report",
        ],
        "blocked": False, "valid": True,
        **_SAFE, "schema_version": _SCHEMA,
    }


def get_report_section_names() -> List[str]:
    """Return list of monitoring report section names."""
    return [
        "monitoring_summary",
        "drift_report",
        "rollback_trigger_report",
        "evidence_pack_report",
        "audit_trail_report",
        "dashboard_report",
        "performance_comparison_report",
        "signal_quality_report",
        "guardrail_status_report",
        "full_monitoring_pack",
    ]
