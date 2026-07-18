"""
paper_trading/small_capital_strategy/strategy_sandbox_engine_v192.py
Core engine for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


_SCHEMA = "192"
_SAFE_DEFAULTS = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "sandbox_only": True, "shadow_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "no_live_strategy_activation": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def validate_sandbox_action(action: str) -> Dict[str, Any]:
    """Validate that an action is allowed for sandbox use."""
    from paper_trading.small_capital_strategy.strategy_sandbox_safety_v192 import (
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


def validate_sandbox_mode(mode: str) -> bool:
    """Return True if mode is a known sandbox mode."""
    from paper_trading.small_capital_strategy.strategy_sandbox_version_v192 import SANDBOX_MODES
    return mode in SANDBOX_MODES


def validate_sandbox_approval_state(state: str) -> bool:
    """Return True if state is a known sandbox approval state."""
    from paper_trading.small_capital_strategy.strategy_sandbox_version_v192 import SANDBOX_APPROVAL_STATES
    return state in SANDBOX_APPROVAL_STATES


def run_sandbox_validation(
    sandbox_id: str,
    tuning_proposal_source: str,
    baseline_snapshot_id: str,
    candidate_snapshot_id: str,
    sandbox_mode: str = "SHADOW_COMPARE",
) -> Dict[str, Any]:
    """
    Run a paper sandbox validation.
    Returns blocked if required sources or snapshot IDs are missing.
    """
    if not tuning_proposal_source:
        return {
            "sandbox_id": sandbox_id,
            "blocked": True,
            "block_reason": "missing_tuning_proposal_source",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not baseline_snapshot_id:
        return {
            "sandbox_id": sandbox_id,
            "blocked": True,
            "block_reason": "missing_baseline_strategy_snapshot",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not candidate_snapshot_id:
        return {
            "sandbox_id": sandbox_id,
            "blocked": True,
            "block_reason": "missing_candidate_strategy_snapshot",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "sandbox_id": sandbox_id,
        "blocked": False,
        "approval_state": "SHADOW_ONLY",
        "sandbox_mode": sandbox_mode,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_baseline_snapshot(
    snapshot_id: str,
    period_label: str,
    rule_categories: Optional[List[str]] = None,
    guardrails: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a baseline strategy snapshot for sandbox comparison."""
    cats = rule_categories or []
    guards = guardrails or []
    return {
        "snapshot_id": snapshot_id,
        "period_label": period_label,
        "rule_categories": cats,
        "guardrail_count": len(guards),
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_candidate_snapshot(
    snapshot_id: str,
    period_label: str,
    tuning_proposal_source: str,
    rule_changes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a candidate strategy snapshot. Blocks if tuning_proposal_source is missing."""
    if not tuning_proposal_source:
        return {
            "snapshot_id": snapshot_id,
            "blocked": True,
            "block_reason": "missing_tuning_proposal_source",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    changes = rule_changes or []
    return {
        "snapshot_id": snapshot_id,
        "period_label": period_label,
        "tuning_proposal_source": tuning_proposal_source,
        "rule_changes": changes,
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def run_shadow_comparison(
    comparison_id: str,
    baseline_snapshot_id: str,
    candidate_snapshot_id: str,
    dimensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Run a shadow comparison between baseline and candidate snapshots."""
    if not baseline_snapshot_id:
        return {
            "comparison_id": comparison_id,
            "blocked": True,
            "block_reason": "shadow_comparison_without_baseline",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    dims = dimensions or []
    return {
        "comparison_id": comparison_id,
        "baseline_snapshot_id": baseline_snapshot_id,
        "candidate_snapshot_id": candidate_snapshot_id,
        "dimensions_compared": dims,
        "improvement_detected": False,
        "regression_detected": False,
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def compute_performance_delta(
    delta_id: str,
    sandbox_id: str,
    baseline_metrics: Optional[Dict[str, float]] = None,
    candidate_metrics: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Compute performance delta between baseline and candidate metrics."""
    base = baseline_metrics or {}
    cand = candidate_metrics or {}
    win_rate_delta = cand.get("win_rate", 0.0) - base.get("win_rate", 0.0)
    expectancy_delta_r = cand.get("expectancy_r", 0.0) - base.get("expectancy_r", 0.0)
    profit_factor_delta = cand.get("profit_factor", 0.0) - base.get("profit_factor", 0.0)
    improvement_detected = expectancy_delta_r > 0 and win_rate_delta >= 0
    return {
        "delta_id": delta_id,
        "sandbox_id": sandbox_id,
        "win_rate_delta": win_rate_delta,
        "expectancy_delta_r": expectancy_delta_r,
        "profit_factor_delta": profit_factor_delta,
        "improvement_detected": improvement_detected,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def compute_risk_delta(
    delta_id: str,
    sandbox_id: str,
    baseline_metrics: Optional[Dict[str, float]] = None,
    candidate_metrics: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Compute risk delta between baseline and candidate metrics."""
    base = baseline_metrics or {}
    cand = candidate_metrics or {}
    baseline_max_drawdown_r = base.get("max_drawdown_r", 0.0)
    candidate_max_drawdown_r = cand.get("max_drawdown_r", 0.0)
    max_drawdown_delta_r = candidate_max_drawdown_r - baseline_max_drawdown_r
    drawdown_budget_usage_delta_pct = (
        cand.get("drawdown_budget_usage_pct", 0.0)
        - base.get("drawdown_budget_usage_pct", 0.0)
    )
    risk_reduction_score = max(0.0, -max_drawdown_delta_r) / max(1.0, abs(baseline_max_drawdown_r))
    return {
        "delta_id": delta_id,
        "sandbox_id": sandbox_id,
        "max_drawdown_delta_r": max_drawdown_delta_r,
        "drawdown_budget_usage_delta_pct": drawdown_budget_usage_delta_pct,
        "risk_reduction_score": risk_reduction_score,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def compute_signal_delta(
    delta_id: str,
    sandbox_id: str,
    baseline_metrics: Optional[Dict[str, float]] = None,
    candidate_metrics: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Compute signal quality delta between baseline and candidate metrics."""
    base = baseline_metrics or {}
    cand = candidate_metrics or {}
    signal_count_delta = cand.get("signal_count", 0.0) - base.get("signal_count", 0.0)
    chase_high_delta = cand.get("chase_high_rate", 0.0) - base.get("chase_high_rate", 0.0)
    early_entry_delta = cand.get("early_entry_rate", 0.0) - base.get("early_entry_rate", 0.0)
    return {
        "delta_id": delta_id,
        "sandbox_id": sandbox_id,
        "signal_count_delta": signal_count_delta,
        "chase_high_delta": chase_high_delta,
        "early_entry_delta": early_entry_delta,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_sandbox_recommendation(
    recommendation_id: str,
    sandbox_id: str,
    recommendation_type: str,
    rationale: str,
    evidence_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a sandbox recommendation. Blocks if no evidence provided."""
    refs = evidence_refs or []
    if not refs:
        return {
            "recommendation_id": recommendation_id,
            "blocked": True,
            "block_reason": "candidate_rule_without_evidence",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "recommendation_id": recommendation_id,
        "sandbox_id": sandbox_id,
        "recommendation_type": recommendation_type,
        "rationale": rationale,
        "evidence_refs": refs,
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_sandbox_evidence_pack(
    pack_id: str,
    sandbox_id: str,
    evidence_items: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """Build a sandbox evidence pack."""
    items = evidence_items or []
    return {
        "pack_id": pack_id,
        "sandbox_id": sandbox_id,
        "evidence_items": items,
        "evidence_count": len(items),
        "all_evidence_present": len(items) > 0,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_sandbox_audit_trail(
    trail_id: str,
    sandbox_id: str,
    steps: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """Build a sandbox audit trail."""
    step_list = steps or []
    return {
        "trail_id": trail_id,
        "sandbox_id": sandbox_id,
        "steps": step_list,
        "audit_complete": len(step_list) > 0,
        "deterministic_timestamp_policy": "date_label_only_no_wall_clock",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_sandbox_dashboard(
    dashboard_id: str,
    period_label: str,
    sandbox_mode: str = "SHADOW_COMPARE",
    approval_state: str = "SHADOW_ONLY",
    regression_detected: bool = False,
) -> Dict[str, Any]:
    """Build a sandbox dashboard dict."""
    return {
        "dashboard_id": dashboard_id,
        "period_label": period_label,
        "sandbox_mode": sandbox_mode,
        "approval_state": approval_state,
        "regression_detected": regression_detected,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_sandbox_export_manifest(
    manifest_id: str,
    sandbox_id: str,
    export_path: str = "reports/",
    sections: Optional[List[str]] = None,
    export_format: str = "json",
) -> Dict[str, Any]:
    """Build a sandbox export manifest. Redirects unsafe paths."""
    from paper_trading.small_capital_strategy.strategy_sandbox_safety_v192 import is_safe_output_path
    safe_path = is_safe_output_path(export_path)
    final_path = export_path if safe_path else "reports/"
    return {
        "manifest_id": manifest_id,
        "sandbox_id": sandbox_id,
        "export_path": final_path,
        "sections": sections or ["baseline", "candidate", "comparison", "recommendation", "evidence"],
        "export_format": export_format,
        "safe_path": safe_path,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "engine": "strategy_sandbox_engine_v192",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        "functions": [
            "validate_sandbox_action",
            "validate_sandbox_mode",
            "validate_sandbox_approval_state",
            "run_sandbox_validation",
            "build_baseline_snapshot",
            "build_candidate_snapshot",
            "run_shadow_comparison",
            "compute_performance_delta",
            "compute_risk_delta",
            "compute_signal_delta",
            "build_sandbox_recommendation",
            "build_sandbox_evidence_pack",
            "build_sandbox_audit_trail",
            "build_sandbox_dashboard",
            "build_sandbox_export_manifest",
        ],
        **_SAFE_DEFAULTS,
    }
