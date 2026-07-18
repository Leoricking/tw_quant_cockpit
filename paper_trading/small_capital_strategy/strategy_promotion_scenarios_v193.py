"""
paper_trading/small_capital_strategy/strategy_promotion_scenarios_v193.py
75 scenarios for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA = "193"
_SAFETY = {
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


def _s(sid: str, stype: str, desc: str, **kw) -> Dict[str, Any]:
    return {"scenario_id": sid, "scenario_type": stype, "description": desc,
            "schema_version": _SCHEMA, **kw, **_SAFETY}


SCENARIOS: List[Dict[str, Any]] = [
    # ── 1–8: complete_promotion_package ──────────────────────────────────────
    _s("SP193-001", "complete_promotion_package",
       "Full promotion package with all validation, checklist, and rollback plan complete.",
       approval_state="PAPER_PROMOTION_READY", rollback_plan_present=True,
       checklist_complete=True, regression_detected=False, blocked=False),
    _s("SP193-002", "complete_promotion_package",
       "Complete promotion package with positive expectancy delta and evidence pack.",
       approval_state="PAPER_PROMOTION_READY", expectancy_delta_r=0.18,
       rollback_plan_present=True, blocked=False),
    _s("SP193-003", "complete_promotion_package",
       "Promotion package with complete audit trail and shadow comparison confirmed.",
       approval_state="PAPER_PROMOTION_READY", audit_trail=True,
       shadow_comparison_confirmed=True, rollback_plan_present=True, blocked=False),
    _s("SP193-004", "complete_promotion_package",
       "Quarterly promotion package with full rollback checklist and evidence pack.",
       approval_state="PAPER_PROMOTION_READY", period="quarterly",
       evidence_pack=True, rollback_plan_present=True, blocked=False),
    _s("SP193-005", "complete_promotion_package",
       "Promotion package confirming candidate improves win rate without regression.",
       approval_state="PAPER_PROMOTION_READY", win_rate_delta=0.08,
       regression_detected=False, rollback_plan_present=True, blocked=False),
    _s("SP193-006", "complete_promotion_package",
       "Complete promotion with dashboard, recommendations, and rollback plan.",
       approval_state="PAPER_PROMOTION_READY", dashboard_generated=True,
       rollback_plan_present=True, blocked=False),
    _s("SP193-007", "complete_promotion_package",
       "Promotion package confirming baseline rule stability — candidate stays shadow.",
       approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       rollback_plan_present=True, blocked=False),
    _s("SP193-008", "complete_promotion_package",
       "Full promotion evaluation across A/B/C rules — all rule dimensions pass.",
       approval_state="PAPER_PROMOTION_READY", rule_dimensions_passed=12,
       rollback_plan_present=True, blocked=False),

    # ── 9–11: shadow_only_candidate ───────────────────────────────────────────
    _s("SP193-009", "shadow_only_candidate",
       "Candidate rule passes sandbox but needs more shadow data — stays SHADOW_ONLY.",
       approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       rollback_plan_present=True, blocked=False),
    _s("SP193-010", "shadow_only_candidate",
       "Candidate with marginal win rate improvement — insufficient for promotion.",
       approval_state="SHADOW_ONLY", win_rate_delta=0.01,
       recommendation="REQUIRE_MORE_DATA", blocked=False),
    _s("SP193-011", "shadow_only_candidate",
       "Shadow-only mode: guardrail false positive rate too high for promotion.",
       approval_state="SHADOW_ONLY", guardrail_false_positive_rate=0.35,
       recommendation="TIGHTEN_ROLLBACK_TRIGGER", blocked=False),

    # ── 12–14: paper_promotion_ready ──────────────────────────────────────────
    _s("SP193-012", "paper_promotion_ready",
       "Candidate achieves full paper promotion approval after complete validation.",
       approval_state="PAPER_PROMOTION_READY",
       recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, checklist_complete=True, blocked=False),
    _s("SP193-013", "paper_promotion_ready",
       "Candidate with improved expectancy and reduced drawdown — paper-approved.",
       approval_state="PAPER_PROMOTION_READY", expectancy_delta_r=0.22,
       max_drawdown_delta_r=-0.15, rollback_plan_present=True, blocked=False),
    _s("SP193-014", "paper_promotion_ready",
       "Split-package promotion: only A-rule subset approved, B/C remain shadow.",
       approval_state="PAPER_PROMOTION_READY", recommendation="SPLIT_PACKAGE",
       rollback_plan_present=True, blocked=False),

    # ── 15–17: blocked_candidate ──────────────────────────────────────────────
    _s("SP193-015", "blocked_candidate",
       "Candidate blocked — missing sandbox validation source.",
       blocked=True, block_reason="missing_sandbox_validation_source",
       approval_state="BLOCKED"),
    _s("SP193-016", "blocked_candidate",
       "Candidate blocked — missing shadow comparison source.",
       blocked=True, block_reason="missing_shadow_comparison_source",
       approval_state="BLOCKED"),
    _s("SP193-017", "blocked_candidate",
       "Candidate blocked — promotion package lacks approval checklist.",
       blocked=True, block_reason="promotion_package_without_approval_checklist",
       approval_state="BLOCKED"),

    # ── 18–20: regression_detected ────────────────────────────────────────────
    _s("SP193-018", "regression_detected",
       "Regression detected — candidate win rate deteriorated vs baseline.",
       approval_state="REGRESSION_DETECTED",
       primary_trigger="WIN_RATE_DETERIORATION",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),
    _s("SP193-019", "regression_detected",
       "Regression detected — candidate drawdown exceeds baseline threshold.",
       approval_state="REGRESSION_DETECTED",
       primary_trigger="DRAWDOWN_INCREASED",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),
    _s("SP193-020", "regression_detected",
       "Regression detected — candidate expectancy deteriorated significantly.",
       approval_state="REGRESSION_DETECTED",
       primary_trigger="EXPECTANCY_DETERIORATION",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),

    # ── 21–22: missing_sandbox_validation_blocked ─────────────────────────────
    _s("SP193-021", "missing_sandbox_validation_blocked",
       "Promotion input blocked — sandbox validation source is empty.",
       blocked=True, block_reason="missing_sandbox_validation_source",
       sandbox_validation_source="", approval_state="BLOCKED"),
    _s("SP193-022", "missing_sandbox_validation_blocked",
       "Promotion blocked — sandbox source references invalid session ID.",
       blocked=True, block_reason="missing_sandbox_validation_source",
       approval_state="BLOCKED"),

    # ── 23–24: missing_shadow_comparison_blocked ──────────────────────────────
    _s("SP193-023", "missing_shadow_comparison_blocked",
       "Promotion blocked — shadow comparison source is empty.",
       blocked=True, block_reason="missing_shadow_comparison_source",
       shadow_comparison_source="", approval_state="BLOCKED"),
    _s("SP193-024", "missing_shadow_comparison_blocked",
       "Promotion blocked — shadow comparison never completed for this candidate.",
       blocked=True, block_reason="missing_shadow_comparison_source",
       approval_state="BLOCKED"),

    # ── 25–27: missing_rollback_plan_blocked ──────────────────────────────────
    _s("SP193-025", "missing_rollback_plan_blocked",
       "Promotion blocked — rollback plan not provided.",
       blocked=True, block_reason="missing_rollback_plan",
       rollback_plan_present=False, approval_state="BLOCKED"),
    _s("SP193-026", "missing_rollback_plan_blocked",
       "Promotion blocked — rollback triggers not defined.",
       blocked=True, block_reason="missing_rollback_plan",
       rollback_triggers=[], approval_state="BLOCKED"),
    _s("SP193-027", "missing_rollback_plan_blocked",
       "Promotion blocked — rollback steps are empty.",
       blocked=True, block_reason="missing_rollback_plan",
       rollback_steps=[], approval_state="BLOCKED"),

    # ── 28–29: malformed_promotion_input ─────────────────────────────────────
    _s("SP193-028", "malformed_promotion_input",
       "Malformed promotion input — promotion ID is empty.",
       blocked=True, block_reason="malformed_promotion_input",
       promotion_id="", approval_state="BLOCKED"),
    _s("SP193-029", "malformed_promotion_input",
       "Malformed promotion input — forbidden action words in promotion ID.",
       blocked=True, block_reason="forbidden_action_words",
       approval_state="BLOCKED"),

    # ── 30–32: rollback_to_baseline ───────────────────────────────────────────
    _s("SP193-030", "rollback_to_baseline",
       "Rollback triggered — profit factor deteriorated past threshold.",
       approval_state="ROLLBACK_REQUIRED",
       primary_trigger="PROFIT_FACTOR_DETERIORATION",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),
    _s("SP193-031", "rollback_to_baseline",
       "Rollback triggered — mistake rate increased beyond guardrail.",
       approval_state="ROLLBACK_REQUIRED",
       primary_trigger="MISTAKE_RATE_INCREASED",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),
    _s("SP193-032", "rollback_to_baseline",
       "Rollback triggered — signal count collapsed after rule tightening.",
       approval_state="ROLLBACK_REQUIRED",
       primary_trigger="SIGNAL_COUNT_COLLAPSE",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),

    # ── 33–35: split_package_required ────────────────────────────────────────
    _s("SP193-033", "split_package_required",
       "Candidate split — A-rule approved but B-rule needs more shadow data.",
       approval_state="PAPER_PROMOTION_READY",
       recommendation="SPLIT_PACKAGE", rollback_plan_present=True, blocked=False),
    _s("SP193-034", "split_package_required",
       "Split required — guardrail set approved but position sizing still shadow.",
       approval_state="PAPER_PROMOTION_READY",
       recommendation="SPLIT_PACKAGE", rollback_plan_present=True, blocked=False),
    _s("SP193-035", "split_package_required",
       "Split required — C-reclaim rule approved, B-breakout needs review.",
       approval_state="REVIEW_REQUIRED",
       recommendation="SPLIT_PACKAGE", rollback_plan_present=True, blocked=False),

    # ── 36–37: require_more_data ──────────────────────────────────────────────
    _s("SP193-036", "require_more_data",
       "Promotion deferred — insufficient shadow comparison data points.",
       approval_state="DRAFT", recommendation="REQUIRE_MORE_DATA",
       rollback_plan_present=True, blocked=False),
    _s("SP193-037", "require_more_data",
       "Promotion deferred — less than 30 shadow periods compared.",
       approval_state="SHADOW_ONLY", recommendation="REQUIRE_MORE_DATA",
       shadow_periods_compared=18, rollback_plan_present=True, blocked=False),

    # ── 38–39: manual_review_required ────────────────────────────────────────
    _s("SP193-038", "manual_review_required",
       "Promotion deferred — manual review required before paper-approval.",
       approval_state="REVIEW_REQUIRED",
       recommendation="REQUIRE_MANUAL_REVIEW",
       rollback_plan_present=True, blocked=False),
    _s("SP193-039", "manual_review_required",
       "Manual review required — opportunity loss score borderline.",
       approval_state="REVIEW_REQUIRED", opportunity_loss_score=0.41,
       recommendation="REQUIRE_MANUAL_REVIEW", rollback_plan_present=True, blocked=False),

    # ── 40–41: unsafe_export_blocked ─────────────────────────────────────────
    _s("SP193-040", "unsafe_export_blocked",
       "Export blocked — path references production_strategy directory.",
       blocked=True, block_reason="unsafe_export_path",
       export_path="production_strategy/", approval_state="BLOCKED"),
    _s("SP193-041", "unsafe_export_blocked",
       "Export blocked — path references live_db directory.",
       blocked=True, block_reason="unsafe_export_path",
       export_path="live_db/", approval_state="BLOCKED"),

    # ── 42–43: production_mutation_blocked ────────────────────────────────────
    _s("SP193-042", "production_mutation_blocked",
       "Promotion blocked — production strategy mutation attempted.",
       blocked=True, block_reason="production_strategy_mutation_attempted",
       approval_state="BLOCKED"),
    _s("SP193-043", "production_mutation_blocked",
       "Promotion blocked — live strategy activation attempted.",
       blocked=True, block_reason="live_strategy_activation_attempted",
       approval_state="BLOCKED"),

    # ── 44–45: live_activation_blocked ────────────────────────────────────────
    _s("SP193-044", "live_activation_blocked",
       "Promotion blocked — live strategy activation flag set.",
       blocked=True, block_reason="live_strategy_activation_attempted",
       approval_state="BLOCKED"),
    _s("SP193-045", "live_activation_blocked",
       "Promotion blocked — production DB write attempted.",
       blocked=True, block_reason="production_db_write_attempted",
       approval_state="BLOCKED"),

    # ── 46–48: evidence_pack_complete ─────────────────────────────────────────
    _s("SP193-046", "evidence_pack_complete",
       "Complete evidence pack with sandbox, shadow, and performance evidence.",
       approval_state="PAPER_PROMOTION_READY", evidence_count=5,
       all_evidence_present=True, rollback_plan_present=True, blocked=False),
    _s("SP193-047", "evidence_pack_complete",
       "Evidence pack complete — 7 evidence items covering all validation dimensions.",
       approval_state="PAPER_PROMOTION_READY", evidence_count=7,
       all_evidence_present=True, rollback_plan_present=True, blocked=False),
    _s("SP193-048", "evidence_pack_complete",
       "Quarterly evidence pack with complete audit trail.",
       approval_state="PAPER_PROMOTION_READY", evidence_count=6,
       audit_trail=True, rollback_plan_present=True, blocked=False),

    # ── 49–50: evidence_missing_blocked ───────────────────────────────────────
    _s("SP193-049", "evidence_missing_blocked",
       "Promotion blocked — evidence pack is empty.",
       blocked=True, block_reason="missing_evidence",
       evidence_count=0, approval_state="BLOCKED"),
    _s("SP193-050", "evidence_missing_blocked",
       "Candidate rule blocked — no validation evidence references provided.",
       blocked=True, block_reason="candidate_rule_without_validation_evidence",
       approval_state="BLOCKED"),

    # ── 51–53: promotion_checklist_complete ──────────────────────────────────
    _s("SP193-051", "promotion_checklist_complete",
       "Full promotion checklist complete — all 7 items confirmed.",
       approval_state="PAPER_PROMOTION_READY", checklist_complete=True,
       all_items_checked=True, rollback_plan_present=True, blocked=False),
    _s("SP193-052", "promotion_checklist_complete",
       "Checklist complete — sandbox, shadow, evidence, rollback, safety verified.",
       approval_state="PAPER_PROMOTION_READY", checklist_complete=True,
       safety_flags_verified=True, rollback_plan_present=True, blocked=False),
    _s("SP193-053", "promotion_checklist_complete",
       "Monthly promotion checklist with manual review completed.",
       approval_state="PAPER_PROMOTION_READY", checklist_complete=True,
       manual_review_completed=True, rollback_plan_present=True, blocked=False),

    # ── 54–56: rollback_checklist_complete ───────────────────────────────────
    _s("SP193-054", "rollback_checklist_complete",
       "Rollback checklist complete — 4 triggers and 5 rollback steps defined.",
       rollback_triggers=4, rollback_steps=5,
       rollback_checklist_complete=True, rollback_plan_present=True, blocked=False),
    _s("SP193-055", "rollback_checklist_complete",
       "Rollback checklist with WIN_RATE_DETERIORATION and DRAWDOWN_INCREASED triggers.",
       rollback_triggers=2, rollback_steps=3,
       rollback_checklist_complete=True, rollback_plan_present=True, blocked=False),
    _s("SP193-056", "rollback_checklist_complete",
       "Full rollback plan with all 12 trigger types checked.",
       rollback_triggers=12, rollback_steps=8,
       rollback_checklist_complete=True, rollback_plan_present=True, blocked=False),

    # ── 57–60: safety_audit_scenarios ────────────────────────────────────────
    _s("SP193-057", "safety_audit",
       "Safety audit PASS — all 19 positive flags set, all 8 negative flags clear.",
       all_safe=True, safety_issues_count=0, blocked=False),
    _s("SP193-058", "safety_audit",
       "Safety audit blocked — broker_execution flag set to True.",
       blocked=True, block_reason="missing_no_broker_flags", all_safe=False),
    _s("SP193-059", "safety_audit",
       "Safety audit blocked — real_order flag True.",
       blocked=True, block_reason="missing_paper_only_flags", all_safe=False),
    _s("SP193-060", "safety_audit",
       "Safety audit PASS — promote_to_paper_package action is allowed.",
       all_safe=True, action="PROMOTION_BUILD", blocked=False),

    # ── 61–63: add_monitoring_rule ────────────────────────────────────────────
    _s("SP193-061", "add_monitoring_rule",
       "Monitoring rule added — shadow opportunity_loss_score elevated.",
       approval_state="SHADOW_ONLY", recommendation="ADD_MONITORING_RULE",
       opportunity_loss_score=0.38, rollback_plan_present=True, blocked=False),
    _s("SP193-062", "add_monitoring_rule",
       "Monitoring rule for guardrail false positive tracking.",
       approval_state="REVIEW_REQUIRED", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True, blocked=False),
    _s("SP193-063", "add_monitoring_rule",
       "Monitoring rule for position sizing regression detection.",
       approval_state="SHADOW_ONLY", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True, blocked=False),

    # ── 64–66: tighten_rollback_trigger ──────────────────────────────────────
    _s("SP193-064", "tighten_rollback_trigger",
       "Rollback trigger tightened — WIN_RATE_DETERIORATION threshold lowered.",
       approval_state="REVIEW_REQUIRED",
       recommendation="TIGHTEN_ROLLBACK_TRIGGER",
       primary_trigger="WIN_RATE_DETERIORATION",
       rollback_plan_present=True, blocked=False),
    _s("SP193-065", "tighten_rollback_trigger",
       "Rollback trigger tightened — DRAWDOWN_INCREASED threshold reduced.",
       approval_state="REVIEW_REQUIRED",
       recommendation="TIGHTEN_ROLLBACK_TRIGGER",
       primary_trigger="DRAWDOWN_INCREASED",
       rollback_plan_present=True, blocked=False),
    _s("SP193-066", "tighten_rollback_trigger",
       "Rollback trigger tightened after candidate showed borderline expectancy drop.",
       approval_state="SHADOW_ONLY",
       recommendation="TIGHTEN_ROLLBACK_TRIGGER",
       primary_trigger="EXPECTANCY_DETERIORATION",
       rollback_plan_present=True, blocked=False),

    # ── 67–69: keep_baseline ──────────────────────────────────────────────────
    _s("SP193-067", "keep_baseline",
       "Keep baseline — candidate shows no improvement over baseline.",
       approval_state="SHADOW_ONLY", recommendation="KEEP_BASELINE",
       win_rate_delta=0.0, expectancy_delta_r=0.0, blocked=False),
    _s("SP193-068", "keep_baseline",
       "Keep baseline — candidate regression detected, baseline retained.",
       approval_state="REGRESSION_DETECTED", recommendation="KEEP_BASELINE",
       rollback_plan_present=True, blocked=False),
    _s("SP193-069", "keep_baseline",
       "Keep baseline — opportunity loss too high with candidate rules.",
       approval_state="SHADOW_ONLY", recommendation="KEEP_BASELINE",
       opportunity_loss_score=0.52, blocked=False),

    # ── 70–72: rollback_trigger_scenarios ────────────────────────────────────
    _s("SP193-070", "rollback_trigger",
       "Rollback trigger fired — OPPORTUNITY_LOSS_TOO_HIGH threshold exceeded.",
       approval_state="ROLLBACK_REQUIRED",
       primary_trigger="OPPORTUNITY_LOSS_TOO_HIGH",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),
    _s("SP193-071", "rollback_trigger",
       "Rollback trigger fired — SAFETY_FLAG_MISSING detected in candidate.",
       approval_state="ROLLBACK_REQUIRED",
       primary_trigger="SAFETY_FLAG_MISSING",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),
    _s("SP193-072", "rollback_trigger",
       "Rollback trigger fired — EVIDENCE_MISSING detected post-promotion.",
       approval_state="ROLLBACK_REQUIRED",
       primary_trigger="EVIDENCE_MISSING",
       recommendation="ROLLBACK_TO_BASELINE", rollback_plan_present=True),

    # ── 73–75: backward_compat ────────────────────────────────────────────────
    _s("SP193-073", "backward_compat",
       "Backward compat v1.9.2 — sandbox validation source from v1.9.2 session.",
       approval_state="PAPER_PROMOTION_READY",
       sandbox_validation_source="v192_sandbox_001",
       rollback_plan_present=True, blocked=False),
    _s("SP193-074", "backward_compat",
       "Backward compat v1.9.1 — tuning proposal from v1.9.1 rule tuning lab.",
       approval_state="SHADOW_ONLY",
       tuning_proposal_source="v191_tuning_001",
       rollback_plan_present=True, blocked=False),
    _s("SP193-075", "backward_compat",
       "Backward compat v1.9.0 — performance review from v1.9.0 as evidence source.",
       approval_state="PAPER_PROMOTION_READY",
       performance_review_source="v190_review_001",
       rollback_plan_present=True, blocked=False),
]

assert len(SCENARIOS) == 75, f"Expected 75 scenarios, got {len(SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 promotion scenarios."""
    return list(SCENARIOS)


def get_scenarios_by_type(scenario_type: str) -> List[Dict[str, Any]]:
    """Return scenarios with the given type."""
    return [s for s in SCENARIOS if s.get("scenario_type") == scenario_type]


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Return scenario by ID or None."""
    for s in SCENARIOS:
        if s["scenario_id"] == scenario_id:
            return s
    return None
