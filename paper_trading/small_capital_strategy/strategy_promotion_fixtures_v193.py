"""
paper_trading/small_capital_strategy/strategy_promotion_fixtures_v193.py
75 JSON fixtures for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA = "193"
_SAFETY: Dict[str, Any] = dict(
    paper_only=True,
    research_only=True,
    simulate_only=True,
    validation_only=True,
    promotion_package_only=True,
    rollback_plan_only=True,
    review_only=True,
    report_only=True,
    audit_only=True,
    no_real_orders=True,
    no_broker=True,
    no_margin=True,
    no_leverage=True,
    no_production_strategy_mutation=True,
    no_live_strategy_activation=True,
    not_investment_advice=True,
    demo_only=True,
    not_for_production=True,
    production_trading_blocked=True,
)

_APPROVAL_STATES: List[str] = [
    "DRAFT",
    "SHADOW_ONLY",
    "PAPER_PROMOTION_READY",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "REGRESSION_DETECTED",
    "ROLLBACK_REQUIRED",
    "INVALID",
]

_RECOMMENDATIONS: List[str] = [
    "KEEP_BASELINE",
    "PROMOTE_TO_PAPER_PACKAGE",
    "KEEP_SHADOW_ONLY",
    "REQUIRE_MORE_DATA",
    "REQUIRE_MANUAL_REVIEW",
    "BLOCK_CANDIDATE",
    "ROLLBACK_TO_BASELINE",
    "SPLIT_PACKAGE",
    "TIGHTEN_ROLLBACK_TRIGGER",
    "ADD_MONITORING_RULE",
    "NO_CHANGE",
]

_ROLLBACK_TRIGGERS: List[str] = [
    "WIN_RATE_DETERIORATION",
    "EXPECTANCY_DETERIORATION",
    "DRAWDOWN_INCREASED",
    "PROFIT_FACTOR_DETERIORATION",
    "MISTAKE_RATE_INCREASED",
    "SIGNAL_COUNT_COLLAPSE",
    "OPPORTUNITY_LOSS_TOO_HIGH",
    "GUARDRAIL_FALSE_POSITIVE_TOO_HIGH",
    "BLOCKED_CONDITION_BREACH",
    "EVIDENCE_MISSING",
    "MANUAL_REVIEW_FAILED",
    "SAFETY_FLAG_MISSING",
]


def _f(fid: str, **kw) -> Dict[str, Any]:
    idx = int(fid.split("-")[1]) - 1
    state = _APPROVAL_STATES[idx % len(_APPROVAL_STATES)]
    rec = _RECOMMENDATIONS[idx % len(_RECOMMENDATIONS)]
    trigger = _ROLLBACK_TRIGGERS[idx % len(_ROLLBACK_TRIGGERS)]
    return {
        "fixture_id": fid,
        "promotion_id": f"PROMO-{fid}",
        "period_label": f"period_{fid.lower()}",
        "approval_state": kw.pop("approval_state", state),
        "recommendation": kw.pop("recommendation", rec),
        "primary_trigger": kw.pop("primary_trigger", trigger),
        "rollback_trigger": kw.pop("rollback_trigger", trigger),
        "win_rate": round(0.42 + (idx % 20) * 0.01, 2),
        "expectancy_r": round(0.35 + (idx % 15) * 0.02, 2),
        "max_drawdown_r": round(-(1.2 + (idx % 10) * 0.1), 1),
        "rollback_plan_present": kw.pop("rollback_plan_present", True),
        "evidence_count": kw.pop("evidence_count", 3 + idx % 5),
        "sandbox_validation_source": kw.pop("sandbox_validation_source", f"sandbox_{fid}"),
        "shadow_comparison_source": kw.pop("shadow_comparison_source", f"shadow_{fid}"),
        "schema_version": _SCHEMA,
        **kw,
        **_SAFETY,
    }


FIXTURES: List[Dict[str, Any]] = [
    # ── SPF193-001 to SPF193-010 ──────────────────────────────────────────────
    _f("SPF193-001", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, checklist_complete=True),
    _f("SPF193-002", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       rollback_plan_present=True),
    _f("SPF193-003", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       rollback_plan_present=False, blocked=True, block_reason="missing_rollback_plan"),
    _f("SPF193-004", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       rollback_plan_present=True, regression_detected=True),
    _f("SPF193-005", approval_state="REVIEW_REQUIRED", recommendation="REQUIRE_MANUAL_REVIEW",
       rollback_plan_present=True),
    _f("SPF193-006", approval_state="DRAFT", recommendation="REQUIRE_MORE_DATA",
       rollback_plan_present=True),
    _f("SPF193-007", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       win_rate=0.58, expectancy_r=0.72, rollback_plan_present=True),
    _f("SPF193-008", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_sandbox_validation_source",
       sandbox_validation_source=""),
    _f("SPF193-009", approval_state="ROLLBACK_REQUIRED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="DRAWDOWN_INCREASED", rollback_plan_present=True),
    _f("SPF193-010", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       rollback_plan_present=True, primary_trigger="WIN_RATE_DETERIORATION"),
    # ── SPF193-011 to SPF193-020 ──────────────────────────────────────────────
    _f("SPF193-011", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=5),
    _f("SPF193-012", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_shadow_comparison_source",
       shadow_comparison_source=""),
    _f("SPF193-013", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="EXPECTANCY_DETERIORATION", rollback_plan_present=True),
    _f("SPF193-014", approval_state="REVIEW_REQUIRED", recommendation="REQUIRE_MORE_DATA",
       rollback_plan_present=True),
    _f("SPF193-015", approval_state="PAPER_PROMOTION_READY", recommendation="SPLIT_PACKAGE",
       rollback_plan_present=True),
    _f("SPF193-016", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="promotion_package_without_approval_checklist",
       checklist_complete=False),
    _f("SPF193-017", approval_state="SHADOW_ONLY", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True),
    _f("SPF193-018", approval_state="DRAFT", recommendation="NO_CHANGE",
       rollback_plan_present=True),
    _f("SPF193-019", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="candidate_rule_without_validation_evidence",
       evidence_count=0),
    _f("SPF193-020", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, primary_trigger="SAFETY_FLAG_MISSING"),
    # ── SPF193-021 to SPF193-030 ──────────────────────────────────────────────
    _f("SPF193-021", approval_state="ROLLBACK_REQUIRED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="PROFIT_FACTOR_DETERIORATION", rollback_plan_present=True),
    _f("SPF193-022", approval_state="REVIEW_REQUIRED", recommendation="TIGHTEN_ROLLBACK_TRIGGER",
       rollback_plan_present=True),
    _f("SPF193-023", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       win_rate=0.55, rollback_plan_present=True),
    _f("SPF193-024", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_evidence"),
    _f("SPF193-025", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       primary_trigger="MISTAKE_RATE_INCREASED"),
    _f("SPF193-026", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="SIGNAL_COUNT_COLLAPSE", rollback_plan_present=True),
    _f("SPF193-027", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       checklist_complete=True, rollback_plan_present=True),
    _f("SPF193-028", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="unsafe_export_path"),
    _f("SPF193-029", approval_state="REVIEW_REQUIRED", recommendation="REQUIRE_MANUAL_REVIEW",
       rollback_plan_present=True, primary_trigger="OPPORTUNITY_LOSS_TOO_HIGH"),
    _f("SPF193-030", approval_state="SHADOW_ONLY", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True),
    # ── SPF193-031 to SPF193-040 ──────────────────────────────────────────────
    _f("SPF193-031", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=6),
    _f("SPF193-032", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="forbidden_action_words"),
    _f("SPF193-033", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="GUARDRAIL_FALSE_POSITIVE_TOO_HIGH", rollback_plan_present=True),
    _f("SPF193-034", approval_state="DRAFT", recommendation="REQUIRE_MORE_DATA",
       rollback_plan_present=True),
    _f("SPF193-035", approval_state="PAPER_PROMOTION_READY", recommendation="SPLIT_PACKAGE",
       rollback_plan_present=True, evidence_count=4),
    _f("SPF193-036", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="malformed_promotion_input"),
    _f("SPF193-037", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       rollback_plan_present=True),
    _f("SPF193-038", approval_state="ROLLBACK_REQUIRED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="BLOCKED_CONDITION_BREACH", rollback_plan_present=True),
    _f("SPF193-039", approval_state="REVIEW_REQUIRED", recommendation="TIGHTEN_ROLLBACK_TRIGGER",
       rollback_plan_present=True),
    _f("SPF193-040", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, win_rate=0.60),
    # ── SPF193-041 to SPF193-050 ──────────────────────────────────────────────
    _f("SPF193-041", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_paper_only_flags"),
    _f("SPF193-042", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       primary_trigger="MANUAL_REVIEW_FAILED"),
    _f("SPF193-043", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=7),
    _f("SPF193-044", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="DRAWDOWN_INCREASED", rollback_plan_present=True),
    _f("SPF193-045", approval_state="REVIEW_REQUIRED", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True),
    _f("SPF193-046", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="live_strategy_activation_attempted"),
    _f("SPF193-047", approval_state="SHADOW_ONLY", recommendation="REQUIRE_MORE_DATA",
       rollback_plan_present=True),
    _f("SPF193-048", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, checklist_complete=True, evidence_count=5),
    _f("SPF193-049", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="production_strategy_mutation_attempted"),
    _f("SPF193-050", approval_state="ROLLBACK_REQUIRED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="EXPECTANCY_DETERIORATION", rollback_plan_present=True),
    # ── SPF193-051 to SPF193-060 ──────────────────────────────────────────────
    _f("SPF193-051", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       rollback_plan_present=True),
    _f("SPF193-052", approval_state="PAPER_PROMOTION_READY", recommendation="SPLIT_PACKAGE",
       rollback_plan_present=True, evidence_count=4),
    _f("SPF193-053", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_not_investment_advice_flags"),
    _f("SPF193-054", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="WIN_RATE_DETERIORATION", rollback_plan_present=True),
    _f("SPF193-055", approval_state="REVIEW_REQUIRED", recommendation="REQUIRE_MANUAL_REVIEW",
       rollback_plan_present=True),
    _f("SPF193-056", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, win_rate=0.56, expectancy_r=0.68),
    _f("SPF193-057", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="broker_requested"),
    _f("SPF193-058", approval_state="SHADOW_ONLY", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True, primary_trigger="PROFIT_FACTOR_DETERIORATION"),
    _f("SPF193-059", approval_state="ROLLBACK_REQUIRED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="MISTAKE_RATE_INCREASED", rollback_plan_present=True),
    _f("SPF193-060", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=8, checklist_complete=True),
    # ── SPF193-061 to SPF193-075 ──────────────────────────────────────────────
    _f("SPF193-061", approval_state="DRAFT", recommendation="NO_CHANGE",
       rollback_plan_present=True),
    _f("SPF193-062", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_no_broker_flags"),
    _f("SPF193-063", approval_state="SHADOW_ONLY", recommendation="KEEP_SHADOW_ONLY",
       primary_trigger="SIGNAL_COUNT_COLLAPSE"),
    _f("SPF193-064", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=3),
    _f("SPF193-065", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="GUARDRAIL_FALSE_POSITIVE_TOO_HIGH", rollback_plan_present=True),
    _f("SPF193-066", approval_state="REVIEW_REQUIRED", recommendation="TIGHTEN_ROLLBACK_TRIGGER",
       rollback_plan_present=True),
    _f("SPF193-067", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="real_order_requested"),
    _f("SPF193-068", approval_state="PAPER_PROMOTION_READY", recommendation="SPLIT_PACKAGE",
       rollback_plan_present=True, evidence_count=6),
    _f("SPF193-069", approval_state="SHADOW_ONLY", recommendation="REQUIRE_MORE_DATA",
       rollback_plan_present=True, primary_trigger="OPPORTUNITY_LOSS_TOO_HIGH"),
    _f("SPF193-070", approval_state="ROLLBACK_REQUIRED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="BLOCKED_CONDITION_BREACH", rollback_plan_present=True),
    _f("SPF193-071", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=5, win_rate=0.57),
    _f("SPF193-072", approval_state="BLOCKED", recommendation="BLOCK_CANDIDATE",
       blocked=True, block_reason="missing_rollback_plan", rollback_plan_present=False),
    _f("SPF193-073", approval_state="REVIEW_REQUIRED", recommendation="ADD_MONITORING_RULE",
       rollback_plan_present=True),
    _f("SPF193-074", approval_state="REGRESSION_DETECTED", recommendation="ROLLBACK_TO_BASELINE",
       primary_trigger="DRAWDOWN_INCREASED", rollback_plan_present=True),
    _f("SPF193-075", approval_state="PAPER_PROMOTION_READY", recommendation="PROMOTE_TO_PAPER_PACKAGE",
       rollback_plan_present=True, evidence_count=7, checklist_complete=True,
       win_rate=0.59, expectancy_r=0.74),
]

assert len(FIXTURES) == 75, f"Expected 75 fixtures, got {len(FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 promotion fixtures."""
    return list(FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Optional[Dict[str, Any]]:
    """Return fixture by ID or None."""
    for f in FIXTURES:
        if f["fixture_id"] == fixture_id:
            return f
    return None


def get_fixtures_by_approval_state(state: str) -> List[Dict[str, Any]]:
    """Return fixtures with the given approval state."""
    return [f for f in FIXTURES if f.get("approval_state") == state]
