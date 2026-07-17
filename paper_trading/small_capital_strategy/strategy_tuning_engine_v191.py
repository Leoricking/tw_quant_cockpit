"""
paper_trading/small_capital_strategy/strategy_tuning_engine_v191.py
Core engine for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


_SCHEMA = "191"
_SAFE_DEFAULTS = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "tuning_only": True, "guardrail_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "not_investment_advice": True, "demo_only": True,
    "not_for_production": True, "production_trading_blocked": True,
}


def validate_tuning_action(action: str) -> Dict[str, Any]:
    """Validate that an action is allowed for tuning."""
    from paper_trading.small_capital_strategy.strategy_tuning_safety_v191 import (
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


def validate_rule_category(category: str) -> bool:
    """Return True if category is a known rule category."""
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import RULE_CATEGORIES
    return category in RULE_CATEGORIES


def validate_guardrail_trigger(trigger: str) -> bool:
    """Return True if trigger is a known guardrail trigger."""
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import GUARDRAIL_TRIGGERS
    return trigger in GUARDRAIL_TRIGGERS


def validate_tuning_recommendation(recommendation: str) -> bool:
    """Return True if recommendation is a known tuning recommendation."""
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import TUNING_RECOMMENDATIONS
    return recommendation in TUNING_RECOMMENDATIONS


def validate_approval_state(state: str) -> bool:
    """Return True if state is a known approval state."""
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import APPROVAL_STATES
    return state in APPROVAL_STATES


def _recommend_from_metrics(
    win_rate: float,
    expectancy: float,
    mistake_rate: float,
    drawdown_usage: float,
) -> str:
    """Derive a tuning recommendation from performance metrics."""
    if expectancy < -0.5:
        return "DISABLE_SETUP"
    if mistake_rate > 0.4:
        return "ADD_GUARDRAIL"
    if drawdown_usage > 0.8:
        return "LOWER_POSITION_SIZE"
    if win_rate < 0.3:
        return "TIGHTEN_RULE"
    if win_rate < 0.4 and expectancy < 0.0:
        return "REQUIRE_MORE_EVIDENCE"
    if expectancy > 0.5 and win_rate > 0.6:
        return "KEEP_RULE"
    if expectancy > 0.2:
        return "NO_CHANGE"
    return "ESCALATE_TO_REVIEW"


def _check_guardrail_trigger(
    trigger_type: str,
    value: float,
    threshold: float,
) -> bool:
    """Return True if the guardrail trigger fires."""
    if trigger_type == "EXPECTANCY_NEGATIVE":
        return value < 0.0
    if trigger_type == "WIN_RATE_TOO_LOW":
        return value < threshold
    if trigger_type == "AVERAGE_LOSS_TOO_HIGH":
        return abs(value) > threshold
    if trigger_type == "DRAWDOWN_BUDGET_EXCEEDED":
        return value > threshold
    if trigger_type == "MISTAKE_RATE_TOO_HIGH":
        return value > threshold
    return value > threshold


def run_tuning_review(
    tuning_id: str,
    performance_source: str,
    journal_source: str,
    period_label: str = "tuning_period",
) -> Dict[str, Any]:
    """
    Run a paper rule tuning review.
    Returns blocked if performance_source or journal_source is empty.
    """
    if not performance_source:
        return {
            "tuning_id": tuning_id, "blocked": True,
            "block_reason": "missing_performance_source",
            "total_rules_reviewed": 0,
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    if not journal_source:
        return {
            "tuning_id": tuning_id, "blocked": True,
            "block_reason": "missing_journal_source",
            "total_rules_reviewed": 0,
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import RULE_CATEGORIES
    return {
        "tuning_id": tuning_id,
        "period_label": period_label,
        "performance_source": performance_source,
        "journal_source": journal_source,
        "blocked": False,
        "total_rules_reviewed": len(RULE_CATEGORIES),
        "approval_state": "PROPOSED",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_rule_candidate(
    rule_id: str,
    rule_name: str,
    rule_category: str,
    win_rate: float,
    expectancy: float,
    mistake_rate: float,
    drawdown_usage: float = 0.0,
    evidence_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a strategy rule candidate for tuning review."""
    refs = evidence_refs or []
    recommendation = _recommend_from_metrics(win_rate, expectancy, mistake_rate, drawdown_usage)
    return {
        "rule_id": rule_id,
        "rule_name": rule_name,
        "rule_category": rule_category,
        "win_rate": win_rate,
        "expectancy": expectancy,
        "mistake_rate": mistake_rate,
        "drawdown_usage": drawdown_usage,
        "recommendation": recommendation,
        "evidence_refs": refs,
        "approval_state": "PROPOSED",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_rule_adjustment(
    adjustment_id: str,
    rule_id: str,
    rule_category: str,
    adjustment_type: str,
    rationale: str,
    evidence_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a strategy rule adjustment. Blocks if no evidence provided."""
    refs = evidence_refs or []
    if not refs:
        return {
            "adjustment_id": adjustment_id,
            "blocked": True,
            "block_reason": "rule_adjustment_without_evidence",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "adjustment_id": adjustment_id,
        "rule_id": rule_id,
        "rule_category": rule_category,
        "adjustment_type": adjustment_type,
        "rationale": rationale,
        "evidence_refs": refs,
        "approval_state": "PROPOSED",
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_guardrail(
    guardrail_id: str,
    guardrail_name: str,
    trigger: str,
    severity: str,
    action: str,
    threshold: float = 0.0,
) -> Dict[str, Any]:
    """Build a strategy guardrail. Blocks if trigger is missing."""
    if not trigger:
        return {
            "guardrail_id": guardrail_id,
            "blocked": True,
            "block_reason": "guardrail_without_trigger",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "guardrail_id": guardrail_id,
        "guardrail_name": guardrail_name,
        "trigger": trigger,
        "severity": severity,
        "action": action,
        "threshold": threshold,
        "active": True,
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def evaluate_guardrail_triggers(
    metrics: Dict[str, float],
) -> List[Dict[str, Any]]:
    """Evaluate all guardrail triggers against provided metrics."""
    from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import GUARDRAIL_TRIGGERS
    _thresholds = {
        "EXPECTANCY_NEGATIVE": 0.0,
        "WIN_RATE_TOO_LOW": 0.35,
        "AVERAGE_LOSS_TOO_HIGH": 2.0,
        "DRAWDOWN_BUDGET_EXCEEDED": 1.0,
        "MISTAKE_RATE_TOO_HIGH": 0.30,
        "CHASE_HIGH_REPEATED": 0.15,
        "EARLY_ENTRY_REPEATED": 0.15,
        "OVER_CONCENTRATION_REPEATED": 0.25,
        "LOW_CASH_RESERVE_REPEATED": 0.20,
        "BLOCK_REASON_IGNORED": 0.05,
        "EVIDENCE_MISSING_REPEATED": 0.20,
        "MARKET_REGIME_MISMATCH": 0.25,
        "VOLUME_CONFIRMATION_MISSING": 0.30,
        "MA_BREAK_IGNORED": 0.20,
        "NO_CLEAR_STOP": 0.10,
        "NO_CLEAR_TAKE_PROFIT": 0.10,
    }
    _metric_map = {
        "EXPECTANCY_NEGATIVE": "expectancy_r",
        "WIN_RATE_TOO_LOW": "win_rate",
        "AVERAGE_LOSS_TOO_HIGH": "average_loss_r",
        "DRAWDOWN_BUDGET_EXCEEDED": "drawdown_budget_usage_pct",
        "MISTAKE_RATE_TOO_HIGH": "mistake_rate",
        "CHASE_HIGH_REPEATED": "chase_high_rate",
        "EARLY_ENTRY_REPEATED": "early_entry_rate",
        "OVER_CONCENTRATION_REPEATED": "over_concentration_rate",
        "LOW_CASH_RESERVE_REPEATED": "low_cash_reserve_rate",
        "BLOCK_REASON_IGNORED": "block_reason_ignored_rate",
        "EVIDENCE_MISSING_REPEATED": "evidence_missing_rate",
        "MARKET_REGIME_MISMATCH": "market_regime_mismatch_rate",
        "VOLUME_CONFIRMATION_MISSING": "volume_confirmation_missing_rate",
        "MA_BREAK_IGNORED": "ma_break_ignored_rate",
        "NO_CLEAR_STOP": "no_clear_stop_rate",
        "NO_CLEAR_TAKE_PROFIT": "no_clear_take_profit_rate",
    }
    results = []
    for trigger_type in GUARDRAIL_TRIGGERS:
        metric_key = _metric_map.get(trigger_type, trigger_type.lower())
        value = metrics.get(metric_key, 0.0)
        threshold = _thresholds.get(trigger_type, 0.0)
        triggered = _check_guardrail_trigger(trigger_type, value, threshold)
        results.append({
            "trigger_type": trigger_type,
            "triggered": triggered,
            "trigger_value": value,
            "threshold": threshold,
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        })
    return results


def build_tuning_recommendation(
    recommendation_id: str,
    recommendation_type: str,
    rule_category: str,
    rule_target: str,
    rationale: str,
    evidence_refs: Optional[List[str]] = None,
    priority: str = "LOW",
) -> Dict[str, Any]:
    """Build a tuning recommendation. Blocks if no evidence."""
    refs = evidence_refs or []
    if not refs:
        return {
            "recommendation_id": recommendation_id,
            "blocked": True,
            "block_reason": "rule_adjustment_without_evidence",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "recommendation_id": recommendation_id,
        "recommendation_type": recommendation_type,
        "rule_category": rule_category,
        "rule_target": rule_target,
        "rationale": rationale,
        "evidence_refs": refs,
        "priority": priority,
        "approval_state": "PROPOSED",
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_backtest_snapshot(
    snapshot_id: str,
    rule_id: str,
    rule_category: str,
    win_rate_before: float,
    win_rate_after: float,
    expectancy_before: float,
    expectancy_after: float,
) -> Dict[str, Any]:
    """Build a backtest snapshot comparing before/after rule tuning."""
    improvement = (expectancy_after > expectancy_before) and (win_rate_after >= win_rate_before)
    return {
        "snapshot_id": snapshot_id,
        "rule_id": rule_id,
        "rule_category": rule_category,
        "win_rate_before": win_rate_before,
        "win_rate_after": win_rate_after,
        "expectancy_before": expectancy_before,
        "expectancy_after": expectancy_after,
        "improvement_detected": improvement,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_dashboard(
    dashboard_id: str,
    period_label: str,
    candidates: Optional[List[Dict]] = None,
    triggered_guardrails: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Build a rule tuning dashboard dict."""
    cands = candidates or []
    guards = triggered_guardrails or []
    to_tighten = sum(1 for c in cands if c.get("recommendation") == "TIGHTEN_RULE")
    to_keep = sum(1 for c in cands if c.get("recommendation") == "KEEP_RULE")
    to_disable = sum(1 for c in cands if c.get("recommendation") == "DISABLE_SETUP")
    triggered = sum(1 for g in guards if g.get("triggered", False))
    return {
        "dashboard_id": dashboard_id,
        "period_label": period_label,
        "total_rules_reviewed": len(cands),
        "rules_to_tighten": to_tighten,
        "rules_to_keep": to_keep,
        "rules_to_disable": to_disable,
        "guardrails_triggered": triggered,
        "overall_approval_state": "PROPOSED",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_evidence_pack(
    pack_id: str,
    tuning_id: str,
    evidence_items: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Build a rule tuning evidence pack."""
    items = evidence_items or []
    return {
        "pack_id": pack_id,
        "tuning_id": tuning_id,
        "evidence_items": items,
        "evidence_count": len(items),
        "all_evidence_present": len(items) > 0,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_audit_trail(
    trail_id: str,
    tuning_id: str,
    steps: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Build a rule tuning audit trail."""
    step_list = steps or []
    return {
        "trail_id": trail_id,
        "tuning_id": tuning_id,
        "steps": step_list,
        "audit_complete": len(step_list) > 0,
        "deterministic_timestamp_policy": "date_label_only_no_wall_clock",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_export_manifest(
    manifest_id: str,
    period_label: str,
    export_path: str = "reports/",
    sections: Optional[List[str]] = None,
    export_format: str = "json",
) -> Dict[str, Any]:
    """Build a rule tuning export manifest. Redirects unsafe paths."""
    from paper_trading.small_capital_strategy.strategy_tuning_safety_v191 import is_safe_output_path
    safe_path = is_safe_output_path(export_path)
    final_path = export_path if safe_path else "reports/"
    return {
        "manifest_id": manifest_id,
        "export_path": final_path,
        "period_label": period_label,
        "sections": sections or ["candidates", "guardrails", "recommendations", "evidence"],
        "export_format": export_format,
        "safe_path": safe_path,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "engine": "strategy_tuning_engine_v191",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        "functions": [
            "run_tuning_review", "build_rule_candidate", "build_rule_adjustment",
            "build_guardrail", "evaluate_guardrail_triggers",
            "build_tuning_recommendation", "build_backtest_snapshot",
            "build_dashboard", "build_evidence_pack", "build_audit_trail",
            "build_export_manifest", "validate_tuning_action",
            "validate_rule_category", "validate_guardrail_trigger",
            "validate_tuning_recommendation", "validate_approval_state",
        ],
        **_SAFE_DEFAULTS,
    }
