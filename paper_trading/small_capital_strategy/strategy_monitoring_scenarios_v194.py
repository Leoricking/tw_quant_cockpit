"""
paper_trading/small_capital_strategy/strategy_monitoring_scenarios_v194.py
75 scenarios for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA = "194"
_SAFETY: Dict[str, Any] = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, monitoring_only=True, drift_detection_only=True,
    rollback_trigger_only=True, review_only=True, report_only=True,
    audit_only=True, no_real_orders=True, no_broker=True, no_margin=True,
    no_leverage=True, no_production_strategy_mutation=True,
    no_live_strategy_activation=True, not_investment_advice=True,
    demo_only=True, not_for_production=True, production_trading_blocked=True,
)


def _s(sid: str, name: str, stype: str, expected_outcome: str,
        monitoring_status: str = "HEALTHY", drift_detected: bool = False,
        blocked: bool = False, **kw: Any) -> Dict[str, Any]:
    return {
        "scenario_id": sid,
        "name": name,
        "scenario_type": stype,
        "expected_outcome": expected_outcome,
        "monitoring_status": monitoring_status,
        "drift_detected": drift_detected,
        "blocked": blocked,
        "schema_version": _SCHEMA,
        **_SAFETY,
        **kw,
    }


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 monitoring scenarios."""
    return [
        # ── Complete Package (1-5) ────────────────────────────────────────────
        _s("SP194-001", "complete_monitoring_package",
           "complete_monitoring", "monitoring_package_built",
           monitoring_id="MON-001",
           promotion_package_source="pkg-193-001",
           rollback_plan_source="rollback-193-001",
           baseline_snapshot_id="BASE-001",
           current_snapshot_id="CURR-001",
           monitoring_window_id="WIN-001"),
        _s("SP194-002", "monitoring_version_check",
           "version_validation", "version_194_confirmed",
           expected_version="1.9.4"),
        _s("SP194-003", "safety_audit_pass",
           "safety_validation", "all_safe_true",
           expected_all_safe=True),
        _s("SP194-004", "engine_info_check",
           "engine_metadata", "engine_info_returned",
           expected_schema="194"),
        _s("SP194-005", "full_monitoring_pack_export",
           "full_export", "full_pack_exported",
           monitoring_id="MON-005", export_format="JSON"),

        # ── Healthy Promoted Paper Package (6-10) ────────────────────────────
        _s("SP194-006", "healthy_promoted_package_no_drift",
           "healthy_monitoring", "status_healthy",
           monitoring_status="HEALTHY",
           baseline_win_rate=0.55, current_win_rate=0.55),
        _s("SP194-007", "healthy_package_continue_monitoring",
           "healthy_monitoring", "recommendation_continue_monitoring",
           monitoring_status="HEALTHY",
           recommendation="CONTINUE_MONITORING"),
        _s("SP194-008", "healthy_package_no_rollback_trigger",
           "healthy_monitoring", "no_rollback_trigger",
           monitoring_status="HEALTHY", rollback_trigger=False),
        _s("SP194-009", "healthy_package_no_alerts",
           "healthy_monitoring", "no_alerts",
           monitoring_status="HEALTHY", alert_count=0),
        _s("SP194-010", "healthy_package_evidence_complete",
           "healthy_monitoring", "evidence_complete",
           monitoring_status="HEALTHY", evidence_completeness=1.0),

        # ── Win Rate Drift (11-15) ────────────────────────────────────────────
        _s("SP194-011", "win_rate_drift_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           baseline_win_rate=0.55, current_win_rate=0.52,
           drift_category="WIN_RATE_DRIFT", drift_severity="LOW"),
        _s("SP194-012", "win_rate_drift_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           baseline_win_rate=0.55, current_win_rate=0.45,
           drift_category="WIN_RATE_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-013", "win_rate_drift_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           baseline_win_rate=0.55, current_win_rate=0.38,
           drift_category="WIN_RATE_DRIFT", drift_severity="HIGH"),
        _s("SP194-014", "win_rate_drift_critical",
           "drift_detection", "rollback_required_critical",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           baseline_win_rate=0.55, current_win_rate=0.28,
           drift_category="WIN_RATE_DRIFT", drift_severity="CRITICAL"),
        _s("SP194-015", "win_rate_drift_extend_window",
           "drift_detection", "extend_monitoring_window",
           monitoring_status="WATCH",
           recommendation="EXTEND_MONITORING_WINDOW"),

        # ── Expectancy Drift (16-20) ──────────────────────────────────────────
        _s("SP194-016", "expectancy_drift_detected",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           baseline_expectancy=1.8, current_expectancy=1.6,
           drift_category="EXPECTANCY_DRIFT", drift_severity="LOW"),
        _s("SP194-017", "expectancy_drift_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           drift_category="EXPECTANCY_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-018", "expectancy_drift_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="EXPECTANCY_DRIFT", drift_severity="HIGH"),
        _s("SP194-019", "expectancy_drift_critical",
           "drift_detection", "rollback_required_critical",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="EXPECTANCY_DRIFT", drift_severity="CRITICAL"),
        _s("SP194-020", "expectancy_drift_rollback_review",
           "drift_detection", "trigger_rollback_review",
           drift_detected=True, recommendation="TRIGGER_ROLLBACK_REVIEW"),

        # ── Profit Factor Drift (21-24) ───────────────────────────────────────
        _s("SP194-021", "profit_factor_drift_detected",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           drift_category="PROFIT_FACTOR_DRIFT", drift_severity="LOW"),
        _s("SP194-022", "profit_factor_drift_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           drift_category="PROFIT_FACTOR_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-023", "profit_factor_drift_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="PROFIT_FACTOR_DRIFT", drift_severity="HIGH"),
        _s("SP194-024", "profit_factor_drift_critical",
           "drift_detection", "rollback_required_critical",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="PROFIT_FACTOR_DRIFT", drift_severity="CRITICAL"),

        # ── Drawdown Drift (25-28) ────────────────────────────────────────────
        _s("SP194-025", "drawdown_drift_detected",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           baseline_dd=0.08, current_dd=0.10,
           drift_category="DRAWDOWN_DRIFT", drift_severity="LOW"),
        _s("SP194-026", "drawdown_drift_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           drift_category="DRAWDOWN_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-027", "drawdown_drift_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="DRAWDOWN_DRIFT", drift_severity="HIGH"),
        _s("SP194-028", "drawdown_drift_critical",
           "drift_detection", "rollback_required_critical",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="DRAWDOWN_DRIFT", drift_severity="CRITICAL"),

        # ── Signal Count Collapse (29-32) ─────────────────────────────────────
        _s("SP194-029", "signal_count_collapse_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           baseline_signals=12, current_signals=9,
           drift_category="SIGNAL_COUNT_DRIFT", drift_severity="LOW"),
        _s("SP194-030", "signal_count_collapse_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           baseline_signals=12, current_signals=5,
           drift_category="SIGNAL_COUNT_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-031", "signal_count_collapse_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           baseline_signals=12, current_signals=2,
           drift_category="SIGNAL_COUNT_DRIFT", drift_severity="HIGH"),
        _s("SP194-032", "signal_count_collapse_suspend_rule",
           "drift_detection", "suspend_candidate_rule",
           drift_detected=True, recommendation="SUSPEND_CANDIDATE_RULE"),

        # ── Guardrail False Positive Too High (33-36) ─────────────────────────
        _s("SP194-033", "guardrail_fp_too_high_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           fp_rate=0.15, drift_category="GUARDRAIL_FALSE_POSITIVE_DRIFT",
           drift_severity="LOW", recommendation="TIGHTEN_GUARDRAIL"),
        _s("SP194-034", "guardrail_fp_too_high_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           fp_rate=0.30, drift_category="GUARDRAIL_FALSE_POSITIVE_DRIFT",
           drift_severity="MEDIUM"),
        _s("SP194-035", "guardrail_fp_too_high_loosen",
           "drift_detection", "loosen_guardrail",
           drift_detected=True, recommendation="LOOSEN_GUARDRAIL"),
        _s("SP194-036", "guardrail_fn_drift",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           drift_category="GUARDRAIL_FALSE_NEGATIVE_DRIFT", drift_severity="LOW"),

        # ── Opportunity Loss Too High (37-39) ─────────────────────────────────
        _s("SP194-037", "opportunity_loss_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           opportunity_loss_pct=0.10,
           drift_category="OPPORTUNITY_LOSS_DRIFT", drift_severity="LOW"),
        _s("SP194-038", "opportunity_loss_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           opportunity_loss_pct=0.25,
           drift_category="OPPORTUNITY_LOSS_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-039", "opportunity_loss_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           opportunity_loss_pct=0.40,
           drift_category="OPPORTUNITY_LOSS_DRIFT", drift_severity="HIGH"),

        # ── Evidence Completeness Drift (40-42) ───────────────────────────────
        _s("SP194-040", "evidence_completeness_drift_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           evidence_completeness=0.80,
           drift_category="EVIDENCE_COMPLETENESS_DRIFT", drift_severity="LOW"),
        _s("SP194-041", "evidence_completeness_drift_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           evidence_completeness=0.60,
           drift_category="EVIDENCE_COMPLETENESS_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-042", "evidence_completeness_drift_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           evidence_completeness=0.40,
           drift_category="EVIDENCE_COMPLETENESS_DRIFT", drift_severity="HIGH"),

        # ── Market Regime Mismatch (43-45) ────────────────────────────────────
        _s("SP194-043", "market_regime_mismatch_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           regime_match=False,
           drift_category="MARKET_REGIME_MISMATCH_DRIFT", drift_severity="LOW"),
        _s("SP194-044", "market_regime_mismatch_medium",
           "drift_detection", "review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           drift_category="MARKET_REGIME_MISMATCH_DRIFT", drift_severity="MEDIUM"),
        _s("SP194-045", "market_regime_mismatch_high",
           "drift_detection", "rollback_review_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_category="MARKET_REGIME_MISMATCH_DRIFT", drift_severity="HIGH"),

        # ── Rollback Review Required (46-49) ──────────────────────────────────
        _s("SP194-046", "rollback_review_required_win_rate",
           "rollback_alert", "rollback_alert_generated",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           trigger_type="WIN_RATE_DETERIORATION", auto_rollback=False),
        _s("SP194-047", "rollback_review_required_drawdown",
           "rollback_alert", "rollback_alert_generated",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           trigger_type="DRAWDOWN_INCREASED", auto_rollback=False),
        _s("SP194-048", "rollback_review_no_auto_rollback",
           "rollback_alert", "auto_rollback_blocked",
           auto_rollback=False, requires_manual_review=True),
        _s("SP194-049", "rollback_review_multiple_triggers",
           "rollback_alert", "multiple_triggers_flagged",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           trigger_count=3),

        # ── Continue Monitoring (50-52) ───────────────────────────────────────
        _s("SP194-050", "continue_monitoring_healthy",
           "monitoring_recommendation", "continue_monitoring",
           monitoring_status="HEALTHY", recommendation="CONTINUE_MONITORING"),
        _s("SP194-051", "continue_monitoring_watch",
           "monitoring_recommendation", "continue_monitoring_watch",
           monitoring_status="WATCH", recommendation="CONTINUE_MONITORING",
           drift_detected=True, drift_severity="LOW"),
        _s("SP194-052", "no_change_recommendation",
           "monitoring_recommendation", "no_change",
           recommendation="NO_CHANGE"),

        # ── Require More Data (53-54) ─────────────────────────────────────────
        _s("SP194-053", "require_more_data_insufficient_obs",
           "monitoring_recommendation", "require_more_data",
           observation_count=3, min_observations=10,
           recommendation="REQUIRE_MORE_DATA"),
        _s("SP194-054", "require_more_data_short_window",
           "monitoring_recommendation", "require_more_data",
           window_days=5, min_window_days=20,
           recommendation="REQUIRE_MORE_DATA"),

        # ── Malformed Input (55-57) ───────────────────────────────────────────
        _s("SP194-055", "malformed_monitoring_input_empty_id",
           "safety_block", "blocked_missing_id",
           blocked=True, monitoring_id="",
           block_reason="missing_monitoring_id"),
        _s("SP194-056", "malformed_monitoring_input_invalid_status",
           "safety_block", "blocked_invalid_status",
           monitoring_status="INVALID",
           invalid_status="NOT_A_STATUS"),
        _s("SP194-057", "malformed_monitoring_input_bad_snapshot",
           "safety_block", "blocked_missing_snapshot",
           blocked=True, baseline_snapshot_id="",
           block_reason="missing_baseline_monitoring_snapshot"),

        # ── Missing Promotion Package Blocked (58-59) ─────────────────────────
        _s("SP194-058", "missing_promotion_package_blocked",
           "safety_block", "blocked_missing_package_source",
           blocked=True, promotion_package_source="",
           block_reason="missing_promotion_package_source"),
        _s("SP194-059", "missing_rollback_plan_blocked",
           "safety_block", "blocked_missing_rollback_plan",
           blocked=True, rollback_plan_source="",
           block_reason="missing_rollback_plan_source"),

        # ── Unsafe Export Blocked (60) ────────────────────────────────────────
        _s("SP194-060", "unsafe_export_path_blocked",
           "safety_block", "blocked_unsafe_export_path",
           blocked=True, export_path="production_db/monitoring",
           block_reason="unsafe_export_path"),

        # ── Production Mutation Blocked (61-62) ───────────────────────────────
        _s("SP194-061", "production_mutation_blocked",
           "safety_block", "blocked_production_mutation",
           blocked=True, block_reason="production_strategy_mutation_attempted",
           no_production_strategy_mutation=True),
        _s("SP194-062", "live_activation_blocked",
           "safety_block", "blocked_live_activation",
           blocked=True, block_reason="live_strategy_activation_attempted",
           no_live_strategy_activation=True),

        # ── Forbidden Action Blocked (63-65) ──────────────────────────────────
        _s("SP194-063", "forbidden_action_buy_blocked",
           "safety_block", "blocked_forbidden_action",
           blocked=True, action="BUY", block_reason="forbidden_action_words"),
        _s("SP194-064", "forbidden_action_sell_blocked",
           "safety_block", "blocked_forbidden_action",
           blocked=True, action="SELL", block_reason="forbidden_action_words"),
        _s("SP194-065", "forbidden_action_broker_order_blocked",
           "safety_block", "blocked_forbidden_action",
           blocked=True, action="BROKER_ORDER",
           block_reason="forbidden_action_words"),

        # ── Cash / Position Sizing (66-68) ────────────────────────────────────
        _s("SP194-066", "cash_reserve_drift_raise_cash",
           "drift_detection", "raise_cash_reserve",
           drift_detected=True, monitoring_status="WATCH",
           drift_category="CASH_RESERVE_DRIFT",
           recommendation="RAISE_CASH_RESERVE"),
        _s("SP194-067", "over_concentration_drift_lower_size",
           "drift_detection", "lower_position_size",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           drift_category="OVER_CONCENTRATION_DRIFT",
           recommendation="LOWER_POSITION_SIZE"),
        _s("SP194-068", "average_loss_drift_low",
           "drift_detection", "drift_severity_low",
           drift_detected=True, monitoring_status="WATCH",
           drift_category="AVERAGE_LOSS_DRIFT", drift_severity="LOW"),

        # ── Keep Shadow Only (69-70) ──────────────────────────────────────────
        _s("SP194-069", "keep_shadow_only_risk",
           "monitoring_recommendation", "keep_shadow_only",
           drift_detected=True, monitoring_status="WATCH",
           recommendation="KEEP_SHADOW_ONLY"),
        _s("SP194-070", "keep_shadow_only_evidence_gap",
           "monitoring_recommendation", "keep_shadow_only",
           drift_detected=True,
           recommendation="KEEP_SHADOW_ONLY"),

        # ── Multi-Drift Scenarios (71-75) ─────────────────────────────────────
        _s("SP194-071", "multi_drift_win_rate_and_expectancy",
           "multi_drift_detection", "multi_drift_rollback_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_categories=["WIN_RATE_DRIFT", "EXPECTANCY_DRIFT"],
           drift_severity="CRITICAL"),
        _s("SP194-072", "multi_drift_signal_and_guardrail",
           "multi_drift_detection", "multi_drift_review_required",
           drift_detected=True, monitoring_status="REVIEW_REQUIRED",
           drift_categories=["SIGNAL_COUNT_DRIFT", "GUARDRAIL_FALSE_POSITIVE_DRIFT"],
           drift_severity="MEDIUM"),
        _s("SP194-073", "multi_drift_drawdown_and_cash",
           "multi_drift_detection", "multi_drift_rollback_required",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_categories=["DRAWDOWN_DRIFT", "CASH_RESERVE_DRIFT"],
           drift_severity="HIGH"),
        _s("SP194-074", "multi_drift_regime_and_opportunity",
           "multi_drift_detection", "multi_drift_watch",
           drift_detected=True, monitoring_status="WATCH",
           drift_categories=["MARKET_REGIME_MISMATCH_DRIFT", "OPPORTUNITY_LOSS_DRIFT"],
           drift_severity="LOW"),
        _s("SP194-075", "multi_drift_complete_rollback_package",
           "multi_drift_detection", "complete_rollback_package_generated",
           drift_detected=True, monitoring_status="ROLLBACK_REQUIRED",
           drift_categories=["WIN_RATE_DRIFT", "EXPECTANCY_DRIFT", "DRAWDOWN_DRIFT"],
           drift_severity="CRITICAL",
           recommendation="ROLLBACK_TO_BASELINE"),
    ]


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return a scenario dict by ID, or empty dict if not found."""
    for sc in get_all_scenarios():
        if sc["scenario_id"] == scenario_id:
            return sc
    return {}


def get_scenario_ids() -> List[str]:
    """Return list of all scenario IDs."""
    return [sc["scenario_id"] for sc in get_all_scenarios()]


def get_scenarios_by_type(scenario_type: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by scenario_type."""
    return [sc for sc in get_all_scenarios() if sc.get("scenario_type") == scenario_type]


def get_blocked_scenarios() -> List[Dict[str, Any]]:
    """Return all blocked scenarios."""
    return [sc for sc in get_all_scenarios() if sc.get("blocked") is True]


def get_drift_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios with drift detected."""
    return [sc for sc in get_all_scenarios() if sc.get("drift_detected") is True]
