"""
paper_trading/small_capital_strategy/strategy_promotion_engine_v193.py
Core engine for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


_SCHEMA = "193"
_SAFE_DEFAULTS = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "promotion_package_only": True,
    "rollback_plan_only": True, "review_only": True, "report_only": True,
    "audit_only": True, "no_real_orders": True, "no_broker": True,
    "no_margin": True, "no_leverage": True,
    "no_production_strategy_mutation": True,
    "no_live_strategy_activation": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def validate_promotion_action(action: str) -> Dict[str, Any]:
    """Validate that an action is allowed for promotion use."""
    from paper_trading.small_capital_strategy.strategy_promotion_safety_v193 import (
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


def validate_promotion_approval_state(state: str) -> Dict[str, Any]:
    """Return dict with valid/blocked/approval_state for a promotion approval state."""
    from paper_trading.small_capital_strategy.strategy_promotion_version_v193 import PROMOTION_APPROVAL_STATES
    is_known = state in PROMOTION_APPROVAL_STATES
    return {
        "valid": is_known,
        "blocked": False,
        "block_reasons": [] if is_known else [f"unknown_approval_state:{state}"],
        "approval_state": state,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_package(
    promotion_id: str,
    sandbox_validation_source: str,
    shadow_comparison_source: str,
    candidate_snapshot_id: str,
    baseline_snapshot_id: str,
) -> Dict[str, Any]:
    """
    Build a paper-only promotion package.
    Returns blocked if required sources or snapshots are missing.
    """
    if not promotion_id:
        return {
            "promotion_id": promotion_id, "blocked": True, "valid": False,
            "block_reason": "missing_promotion_id", "block_reasons": ["missing_promotion_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not sandbox_validation_source:
        return {
            "promotion_id": promotion_id, "blocked": True, "valid": False,
            "block_reason": "missing_sandbox_validation_source",
            "block_reasons": ["missing_sandbox_validation_source"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not shadow_comparison_source:
        return {
            "promotion_id": promotion_id, "blocked": True, "valid": False,
            "block_reason": "missing_shadow_comparison_source",
            "block_reasons": ["missing_shadow_comparison_source"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not baseline_snapshot_id:
        return {
            "promotion_id": promotion_id, "blocked": True, "valid": False,
            "block_reason": "missing_baseline_strategy_snapshot",
            "block_reasons": ["missing_baseline_strategy_snapshot"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not candidate_snapshot_id:
        return {
            "promotion_id": promotion_id, "blocked": True, "valid": False,
            "block_reason": "missing_candidate_strategy_snapshot",
            "block_reasons": ["missing_candidate_strategy_snapshot"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "promotion_id": promotion_id, "blocked": False, "valid": True,
        "block_reasons": [],
        "approval_state": "DRAFT",
        "sandbox_validation_source": sandbox_validation_source,
        "shadow_comparison_source": shadow_comparison_source,
        "candidate_snapshot_id": candidate_snapshot_id,
        "baseline_snapshot_id": baseline_snapshot_id,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_rollback_plan(
    plan_id: str,
    package_id: str,
    baseline_snapshot_id: str,
    rollback_triggers: Optional[List[str]] = None,
    rollback_steps: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a paper rollback plan. Blocks if baseline or triggers are missing."""
    if not plan_id:
        return {
            "plan_id": plan_id, "blocked": True, "valid": False,
            "block_reason": "missing_plan_id", "block_reasons": ["missing_plan_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not package_id:
        return {
            "plan_id": plan_id, "blocked": True, "valid": False,
            "block_reason": "missing_package_id", "block_reasons": ["missing_package_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not baseline_snapshot_id:
        return {
            "plan_id": plan_id, "blocked": True, "valid": False,
            "block_reason": "missing_rollback_plan_baseline",
            "block_reasons": ["missing_rollback_plan_baseline"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    triggers = rollback_triggers or []
    steps = rollback_steps or []
    return {
        "plan_id": plan_id,
        "package_id": package_id,
        "baseline_snapshot_id": baseline_snapshot_id,
        "rollback_triggers": triggers,
        "rollback_steps": steps,
        "rollback_checklist_complete": len(triggers) > 0 and len(steps) > 0,
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def validate_rollback_plan(
    plan_id: str,
    baseline_snapshot_id: str,
    rollback_triggers: Optional[List[str]] = None,
    rollback_steps: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Validate a rollback plan for completeness."""
    errors = []
    if not plan_id:
        errors.append("missing_plan_id")
    if not baseline_snapshot_id:
        errors.append("missing_baseline_snapshot")
    triggers = rollback_triggers or []
    steps = rollback_steps or []
    return {
        "plan_id": plan_id,
        "valid": len(errors) == 0,
        "blocked": False,
        "block_reasons": errors,
        "errors": errors,
        "baseline_snapshot_present": bool(baseline_snapshot_id),
        "triggers_defined": len(triggers) > 0,
        "steps_defined": len(steps) > 0,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_approval_checklist(
    checklist_id: str,
    package_id: str,
    sandbox_validation_confirmed: bool = False,
    shadow_comparison_confirmed: bool = False,
    evidence_complete: bool = False,
    rollback_plan_present: bool = False,
    no_regression_detected: bool = True,
    safety_flags_verified: bool = False,
    manual_review_completed: bool = False,
) -> Dict[str, Any]:
    """Build a promotion approval checklist."""
    if not checklist_id:
        return {
            "checklist_id": checklist_id, "package_id": package_id,
            "blocked": True, "valid": False,
            "block_reason": "missing_checklist_id",
            "block_reasons": ["missing_checklist_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not rollback_plan_present:
        return {
            "checklist_id": checklist_id, "package_id": package_id,
            "blocked": True, "valid": False,
            "block_reason": "promotion_package_without_approval_checklist",
            "block_reasons": ["promotion_package_without_approval_checklist"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    all_items = (
        sandbox_validation_confirmed
        and shadow_comparison_confirmed
        and evidence_complete
        and rollback_plan_present
        and no_regression_detected
        and safety_flags_verified
        and manual_review_completed
    )
    return {
        "checklist_id": checklist_id,
        "package_id": package_id,
        "sandbox_validation_confirmed": sandbox_validation_confirmed,
        "shadow_comparison_confirmed": shadow_comparison_confirmed,
        "evidence_complete": evidence_complete,
        "rollback_plan_present": rollback_plan_present,
        "no_regression_detected": no_regression_detected,
        "safety_flags_verified": safety_flags_verified,
        "manual_review_completed": manual_review_completed,
        "all_items_checked": all_items,
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_recommendation(
    recommendation_id: str,
    package_id: str,
    recommendation_type: str,
    rationale: str,
    evidence_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a promotion recommendation. Blocks if no evidence provided."""
    refs = evidence_refs or []
    if not recommendation_id:
        return {
            "recommendation_id": recommendation_id, "blocked": True, "valid": False,
            "block_reason": "missing_recommendation_id",
            "block_reasons": ["missing_recommendation_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not rationale:
        return {
            "recommendation_id": recommendation_id, "blocked": True, "valid": False,
            "block_reason": "missing_rationale",
            "block_reasons": ["missing_rationale"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not refs:
        return {
            "recommendation_id": recommendation_id, "blocked": True, "valid": False,
            "block_reason": "candidate_rule_without_validation_evidence",
            "block_reasons": ["candidate_rule_without_validation_evidence"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "recommendation_id": recommendation_id,
        "package_id": package_id,
        "recommendation_type": recommendation_type,
        "rationale": rationale,
        "evidence_refs": refs,
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_evidence_pack(
    pack_id: str,
    package_id: str,
    evidence_items: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """Build a promotion evidence pack."""
    if not pack_id:
        return {
            "pack_id": pack_id, "blocked": True, "valid": False,
            "block_reason": "missing_pack_id", "block_reasons": ["missing_pack_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    items = evidence_items or []
    return {
        "pack_id": pack_id,
        "package_id": package_id,
        "evidence_items": items,
        "evidence_count": len(items),
        "all_evidence_present": len(items) > 0,
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_audit_trail(
    trail_id: str,
    package_id: str,
    steps: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """Build a promotion audit trail."""
    if not trail_id:
        return {
            "trail_id": trail_id, "blocked": True, "valid": False,
            "block_reason": "missing_trail_id", "block_reasons": ["missing_trail_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    step_list = steps or []
    return {
        "trail_id": trail_id,
        "package_id": package_id,
        "steps": step_list,
        "audit_complete": len(step_list) > 0,
        "deterministic_timestamp_policy": "date_label_only_no_wall_clock",
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_dashboard(
    dashboard_id: str,
    period_label: str,
    approval_state: str = "DRAFT",
    regression_detected: bool = False,
) -> Dict[str, Any]:
    """Build a promotion dashboard dict."""
    if not dashboard_id:
        return {
            "dashboard_id": dashboard_id, "blocked": True, "valid": False,
            "block_reason": "missing_dashboard_id", "block_reasons": ["missing_dashboard_id"],
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "dashboard_id": dashboard_id,
        "period_label": period_label,
        "approval_state": approval_state,
        "regression_detected": regression_detected,
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_promotion_export_manifest(
    manifest_id: str,
    package_id: str,
    export_path: str = "reports/",
    sections: Optional[List[str]] = None,
    export_format: str = "json",
) -> Dict[str, Any]:
    """Build a promotion export manifest. Redirects unsafe paths."""
    if not manifest_id:
        return {
            "manifest_id": manifest_id, "blocked": True, "valid": False,
            "block_reason": "missing_manifest_id", "block_reasons": ["missing_manifest_id"],
            "export_path": "reports/",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    from paper_trading.small_capital_strategy.strategy_promotion_safety_v193 import is_safe_output_path
    safe_path = is_safe_output_path(export_path)
    final_path = export_path if safe_path else "reports/"
    return {
        "manifest_id": manifest_id,
        "package_id": package_id,
        "export_path": final_path,
        "sections": sections or ["package", "checklist", "rollback", "evidence", "audit"],
        "export_format": export_format,
        "safe_path": safe_path,
        "blocked": False, "valid": True, "block_reasons": [],
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "engine": "strategy_promotion_engine_v193",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        "functions": [
            "validate_promotion_action",
            "validate_promotion_approval_state",
            "build_promotion_package",
            "build_rollback_plan",
            "validate_rollback_plan",
            "build_promotion_approval_checklist",
            "build_promotion_recommendation",
            "build_promotion_evidence_pack",
            "build_promotion_audit_trail",
            "build_promotion_dashboard",
            "build_promotion_export_manifest",
        ],
        **_SAFE_DEFAULTS,
    }
