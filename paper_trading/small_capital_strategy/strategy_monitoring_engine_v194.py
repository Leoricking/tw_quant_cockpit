"""
paper_trading/small_capital_strategy/strategy_monitoring_engine_v194.py
Core engine for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


_SCHEMA = "194"
_SAFE_DEFAULTS = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "monitoring_only": True,
    "drift_detection_only": True, "rollback_trigger_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "no_live_strategy_activation": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def validate_monitoring_action(action: str) -> Dict[str, Any]:
    """Validate that an action is allowed for monitoring use."""
    from paper_trading.small_capital_strategy.strategy_monitoring_safety_v194 import (
        is_forbidden_action, is_allowed_action,
    )
    if is_forbidden_action(action):
        return {"valid": False, "blocked": True, "reason": f"forbidden:{action.upper()}",
                **_SAFE_DEFAULTS, "schema_version": _SCHEMA}
    if is_allowed_action(action):
        return {"valid": True, "blocked": False, "reason": "allowed",
                **_SAFE_DEFAULTS, "schema_version": _SCHEMA}
    return {"valid": False, "blocked": False, "reason": f"unknown:{action.upper()}",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA}


def validate_monitoring_status(status: str) -> Dict[str, Any]:
    """Return dict with valid/blocked for a monitoring status."""
    from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import MONITORING_STATUSES
    is_known = status in MONITORING_STATUSES
    return {
        "valid": is_known,
        "blocked": not is_known,
        "block_reasons": [] if is_known else [f"unknown_monitoring_status:{status}"],
        "monitoring_status": status,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def validate_drift_category(category: str) -> Dict[str, Any]:
    """Return dict with valid/blocked for a drift category."""
    from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import DRIFT_CATEGORIES
    is_known = category in DRIFT_CATEGORIES
    return {
        "valid": is_known,
        "blocked": not is_known,
        "block_reasons": [] if is_known else [f"unknown_drift_category:{category}"],
        "drift_category": category,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def run_drift_detection(
    monitoring_id: str,
    baseline_snapshot_id: str,
    current_snapshot_id: str,
    monitoring_window_id: str,
    baseline: Optional[Dict[str, float]] = None,
    current: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Run drift detection comparing baseline to current snapshots.
    Returns blocked if required inputs are missing.
    """
    if not monitoring_id:
        return {
            "monitoring_id": monitoring_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_monitoring_id",
            "block_reasons": ["missing_monitoring_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not baseline_snapshot_id:
        return {
            "monitoring_id": monitoring_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_baseline_monitoring_snapshot",
            "block_reasons": ["missing_baseline_monitoring_snapshot"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not current_snapshot_id:
        return {
            "monitoring_id": monitoring_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_current_monitoring_snapshot",
            "block_reasons": ["missing_current_monitoring_snapshot"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not monitoring_window_id:
        return {
            "monitoring_id": monitoring_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_monitoring_window",
            "block_reasons": ["missing_monitoring_window"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    base = baseline or {}
    curr = current or {}
    drift_signals: List[Dict[str, Any]] = []
    for metric, base_val in base.items():
        curr_val = curr.get(metric, base_val)
        delta = curr_val - base_val
        detected = abs(delta) > 0.01
        severity = "NONE"
        if abs(delta) > 0.20:
            severity = "CRITICAL"
        elif abs(delta) > 0.15:
            severity = "HIGH"
        elif abs(delta) > 0.10:
            severity = "MEDIUM"
        elif abs(delta) > 0.01:
            severity = "LOW"
        if detected:
            drift_signals.append({
                "metric_name": metric,
                "baseline_value": base_val,
                "current_value": curr_val,
                "delta": delta,
                "drift_detected": True,
                "drift_severity": severity,
            })
    max_sev = "NONE"
    sev_order = ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    for sig in drift_signals:
        if sev_order.index(sig["drift_severity"]) > sev_order.index(max_sev):
            max_sev = sig["drift_severity"]
    return {
        "monitoring_id": monitoring_id,
        "blocked": False, "valid": True,
        "block_reasons": [],
        "drift_detected": len(drift_signals) > 0,
        "drift_severity": max_sev,
        "max_severity": max_sev,
        "drift_signal_count": len(drift_signals),
        "drift_signals": drift_signals,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_monitoring_package_snapshot(
    package_id: str,
    promotion_package_source: str,
    rollback_plan_source: str,
) -> Dict[str, Any]:
    """Build a monitoring package snapshot."""
    if not package_id:
        return {
            "package_id": package_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_package_id",
            "block_reasons": ["missing_package_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not promotion_package_source:
        return {
            "package_id": package_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_promotion_package_source",
            "block_reasons": ["missing_promotion_package_source"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not rollback_plan_source:
        return {
            "package_id": package_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_rollback_plan_source",
            "block_reasons": ["missing_rollback_plan_source"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "package_id": package_id,
        "promotion_package_source": promotion_package_source,
        "rollback_plan_source": rollback_plan_source,
        "monitoring_status": "HEALTHY",
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_rollback_alert(
    alert_id: str,
    trigger_type: str,
    severity: str = "MEDIUM",
    description: str = "",
) -> Dict[str, Any]:
    """Build a rollback review alert (paper only — no automatic rollback)."""
    if not alert_id:
        return {
            "alert_id": alert_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_alert_id",
            "block_reasons": ["missing_alert_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not trigger_type:
        return {
            "alert_id": alert_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_trigger_type",
            "block_reasons": ["missing_trigger_type"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "alert_id": alert_id,
        "trigger_type": trigger_type,
        "severity": severity,
        "description": description or f"Rollback review alert: {trigger_type}",
        "auto_rollback": False,
        "requires_review": True,
        "requires_manual_review": True,
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_monitoring_recommendation(
    recommendation_id: str,
    recommendation_type: str,
    rationale: str = "",
) -> Dict[str, Any]:
    """Build a monitoring recommendation."""
    from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import MONITORING_RECOMMENDATIONS
    if not recommendation_id:
        return {
            "recommendation_id": recommendation_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_recommendation_id",
            "block_reasons": ["missing_recommendation_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not rationale:
        return {
            "recommendation_id": recommendation_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_rationale",
            "block_reasons": ["missing_rationale"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if recommendation_type not in MONITORING_RECOMMENDATIONS:
        return {
            "recommendation_id": recommendation_id,
            "blocked": True, "valid": False,
            "block_reason": f"unknown_recommendation_type:{recommendation_type}",
            "block_reasons": [f"unknown_recommendation_type:{recommendation_type}"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "recommendation_id": recommendation_id,
        "recommendation_type": recommendation_type,
        "rationale": rationale,
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_monitoring_evidence_pack(
    evidence_id: str,
    monitoring_id: str,
) -> Dict[str, Any]:
    """Build a monitoring evidence pack."""
    if not evidence_id:
        return {
            "evidence_id": evidence_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_evidence_id",
            "block_reasons": ["missing_evidence_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not monitoring_id:
        return {
            "evidence_id": evidence_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_monitoring_id",
            "block_reasons": ["missing_monitoring_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "evidence_id": evidence_id,
        "monitoring_id": monitoring_id,
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_monitoring_audit_trail(
    audit_id: str,
    monitoring_id: str,
) -> Dict[str, Any]:
    """Build a monitoring audit trail."""
    if not audit_id:
        return {
            "audit_id": audit_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_audit_id",
            "block_reasons": ["missing_audit_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not monitoring_id:
        return {
            "audit_id": audit_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_monitoring_id",
            "block_reasons": ["missing_monitoring_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "audit_id": audit_id,
        "monitoring_id": monitoring_id,
        "events": [f"monitoring_run:{monitoring_id}"],
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_monitoring_dashboard(
    dashboard_id: str,
    monitoring_id: str,
    overall_status: str = "HEALTHY",
) -> Dict[str, Any]:
    """Build a monitoring dashboard."""
    if not dashboard_id:
        return {
            "dashboard_id": dashboard_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_dashboard_id",
            "block_reasons": ["missing_dashboard_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not monitoring_id:
        return {
            "dashboard_id": dashboard_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_monitoring_id",
            "block_reasons": ["missing_monitoring_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "dashboard_id": dashboard_id,
        "monitoring_id": monitoring_id,
        "overall_status": overall_status,
        "drift_count": 0,
        "alert_count": 0,
        "rollback_trigger_count": 0,
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_monitoring_export_manifest(
    manifest_id: str,
    monitoring_id: str,
    export_format: str = "JSON",
) -> Dict[str, Any]:
    """Build a monitoring export manifest."""
    if not manifest_id:
        return {
            "manifest_id": manifest_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_manifest_id",
            "block_reasons": ["missing_manifest_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not monitoring_id:
        return {
            "manifest_id": manifest_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_monitoring_id",
            "block_reasons": ["missing_monitoring_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "manifest_id": manifest_id,
        "monitoring_id": monitoring_id,
        "export_format": export_format,
        "sections": ["drift_detection", "rollback_alerts", "evidence", "audit_trail"],
        "blocked": False, "valid": True,
        "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata dict."""
    from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION,
        FORBIDDEN_MONITORING_ACTIONS, ALLOWED_MONITORING_ACTIONS,
    )
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "schema_version": SCHEMA_VERSION,
        "forbidden_output_actions": FORBIDDEN_MONITORING_ACTIONS,
        "allowed_output_actions": ALLOWED_MONITORING_ACTIONS,
        **_SAFE_DEFAULTS,
    }
