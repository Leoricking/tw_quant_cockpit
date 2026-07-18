"""
paper_trading/small_capital_strategy/strategy_sandbox_scenarios_v192.py
75 scenarios for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA = "192"
_SAFETY = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "sandbox_only": True, "shadow_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "no_live_strategy_activation": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def _s(sid: str, stype: str, desc: str, **kw) -> Dict[str, Any]:
    return {"scenario_id": sid, "scenario_type": stype, "description": desc,
            "schema_version": _SCHEMA, **kw, **_SAFETY}


SCENARIOS: List[Dict[str, Any]] = [
    # ── 1–8: complete_sandbox_validation ─────────────────────────────────────
    _s("SS192-001", "complete_sandbox_validation",
       "Full sandbox validation with baseline and candidate compared across all dimensions.",
       sandbox_mode="FULL_RULESET_COMPARE", all_dimensions=True,
       approval_state="PAPER_APPROVED", regression_detected=False, blocked=False),
    _s("SS192-002", "complete_sandbox_validation",
       "Complete shadow validation with positive expectancy delta — candidate approved for paper.",
       sandbox_mode="SHADOW_COMPARE", expectancy_delta_r=0.18,
       approval_state="PAPER_APPROVED", regression_detected=False, blocked=False),
    _s("SS192-003", "complete_sandbox_validation",
       "Complete sandbox run with all rule categories evaluated and no regression.",
       sandbox_mode="FULL_RULESET_COMPARE", rule_categories=14,
       regression_detected=False, approval_state="SHADOW_ONLY", blocked=False),
    _s("SS192-004", "complete_sandbox_validation",
       "Quarterly sandbox validation with evidence pack and audit trail generated.",
       sandbox_mode="SHADOW_COMPARE", period="quarterly",
       evidence_pack=True, audit_trail=True, blocked=False),
    _s("SS192-005", "complete_sandbox_validation",
       "Full sandbox run finding candidate improves win rate without increasing drawdown.",
       sandbox_mode="FULL_RULESET_COMPARE", win_rate_delta=0.08,
       max_drawdown_delta_r=0.0, regression_detected=False, blocked=False),
    _s("SS192-006", "complete_sandbox_validation",
       "Complete sandbox with shadow comparison producing dashboard and recommendations.",
       sandbox_mode="SHADOW_COMPARE", dashboard_generated=True,
       recommendations_generated=True, blocked=False),
    _s("SS192-007", "complete_sandbox_validation",
       "Sandbox validation confirming baseline rule stability with no candidate changes needed.",
       sandbox_mode="BASELINE_ONLY", approval_state="KEEP_SHADOW_TESTING",
       regression_detected=False, blocked=False),
    _s("SS192-008", "complete_sandbox_validation",
       "Complete sandbox run across A/B/C rule compare mode — all rule dimensions evaluated.",
       sandbox_mode="A_B_RULE_COMPARE", rule_dimensions_passed=12,
       approval_state="PAPER_APPROVED", blocked=False),

    # ── 9–12: shadow_compare_baseline_vs_candidate ────────────────────────────
    _s("SS192-009", "shadow_compare_baseline_vs_candidate",
       "Shadow compare shows candidate improves expectancy by +0.22R.",
       sandbox_mode="SHADOW_COMPARE", expectancy_delta_r=0.22,
       improvement_detected=True, regression_detected=False, blocked=False),
    _s("SS192-010", "shadow_compare_baseline_vs_candidate",
       "Shadow compare detects candidate regression on profit factor — keep baseline.",
       sandbox_mode="SHADOW_COMPARE", profit_factor_delta=-0.35,
       regression_detected=True, approval_state="REGRESSION_DETECTED", blocked=False),
    _s("SS192-011", "shadow_compare_baseline_vs_candidate",
       "Shadow compare with multiple dimensions — candidate marginally better, keep shadow testing.",
       sandbox_mode="SHADOW_COMPARE", shadow_validation_score=0.61,
       approval_state="KEEP_SHADOW_TESTING", blocked=False),
    _s("SS192-012", "shadow_compare_baseline_vs_candidate",
       "Shadow compare confirms candidate reduces chase-high rate and improves risk score.",
       sandbox_mode="SHADOW_COMPARE", chase_high_delta=-0.12,
       risk_reduction_score=0.72, improvement_detected=True, blocked=False),

    # ── 13–14: empty_baseline_blocked ────────────────────────────────────────
    _s("SS192-013", "empty_baseline_blocked",
       "Sandbox blocked because baseline_snapshot_id is empty.",
       sandbox_mode="SHADOW_COMPARE", baseline_snapshot_id="",
       blocked=True, block_reason="missing_baseline_strategy_snapshot"),
    _s("SS192-014", "empty_baseline_blocked",
       "Sandbox blocked when baseline strategy snapshot contains no rules.",
       sandbox_mode="FULL_RULESET_COMPARE", baseline_rule_count=0,
       blocked=True, block_reason="missing_baseline_strategy_snapshot"),

    # ── 15–16: empty_candidate_blocked ───────────────────────────────────────
    _s("SS192-015", "empty_candidate_blocked",
       "Sandbox blocked because candidate_snapshot_id is empty.",
       sandbox_mode="SHADOW_COMPARE", candidate_snapshot_id="",
       blocked=True, block_reason="missing_candidate_strategy_snapshot"),
    _s("SS192-016", "empty_candidate_blocked",
       "Sandbox blocked when candidate snapshot contains no rule changes.",
       sandbox_mode="A_B_RULE_COMPARE", candidate_rule_change_count=0,
       blocked=True, block_reason="missing_candidate_strategy_snapshot"),

    # ── 17–19: malformed_sandbox_input ───────────────────────────────────────
    _s("SS192-017", "malformed_sandbox_input",
       "Sandbox blocked due to missing sandbox_id.",
       sandbox_mode="SHADOW_COMPARE", sandbox_id="",
       blocked=True, block_reason="malformed_sandbox_input"),
    _s("SS192-018", "malformed_sandbox_input",
       "Sandbox blocked due to forbidden action word in sandbox_id.",
       sandbox_mode="SHADOW_COMPARE", sandbox_id="EXECUTE_TRADE_REVIEW",
       blocked=True, block_reason="forbidden_action_words"),
    _s("SS192-019", "malformed_sandbox_input",
       "Sandbox blocked due to paper_only flag set to False.",
       sandbox_mode="SHADOW_COMPARE", paper_only=False,
       blocked=True, block_reason="missing_paper_only_flags"),

    # ── 20–22: a_rule_tightening_improves_risk ────────────────────────────────
    _s("SS192-020", "a_rule_tightening_improves_risk",
       "Tightening A_10MA_PULLBACK entry window reduces average loss from -2.1R to -1.4R.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="A_10MA_PULLBACK",
       avg_loss_before_r=-2.1, avg_loss_after_r=-1.4,
       risk_reduction_score=0.68, blocked=False),
    _s("SS192-021", "a_rule_tightening_improves_risk",
       "Requiring MA confirmation on A entries reduces max drawdown delta by 0.5R.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="A_MA_CONFIRMATION",
       max_drawdown_delta_r=-0.5, improvement_detected=True, blocked=False),
    _s("SS192-022", "a_rule_tightening_improves_risk",
       "A entry width tightening cuts early entry rate from 18% to 6% improving risk profile.",
       sandbox_mode="A_B_RULE_COMPARE", early_entry_rate_before=0.18,
       early_entry_rate_after=0.06, risk_reduction_score=0.75, blocked=False),

    # ── 23–24: a_rule_tightening_reduces_signals ──────────────────────────────
    _s("SS192-023", "a_rule_tightening_reduces_signals",
       "Tightening A entry window reduces signal count by 30% — acceptable trade-off.",
       sandbox_mode="A_B_RULE_COMPARE", signal_count_delta=-30,
       quality_delta=0.15, approval_state="PAPER_APPROVED", blocked=False),
    _s("SS192-024", "a_rule_tightening_reduces_signals",
       "Strict A MA filter cuts signals by 45% — require more data before accepting.",
       sandbox_mode="A_B_RULE_COMPARE", signal_count_delta=-45,
       approval_state="REQUIRE_MORE_DATA", blocked=False),

    # ── 25–27: b_breakout_tightening_blocks_chase_high ────────────────────────
    _s("SS192-025", "b_breakout_tightening_blocks_chase_high",
       "Adding volume gate to B_BASE_BREAKOUT blocks 80% of chase-high entries.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="B_BASE_BREAKOUT",
       chase_high_blocked_pct=0.80, improvement_detected=True, blocked=False),
    _s("SS192-026", "b_breakout_tightening_blocks_chase_high",
       "B breakout requiring 1.5x average volume blocks chasing extended breakouts.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="B_VOLUME_FILTER",
       volume_threshold=1.5, chase_high_delta=-0.14, blocked=False),
    _s("SS192-027", "b_breakout_tightening_blocks_chase_high",
       "Tightened B base width rule prevents chasing extended handles — signal quality up.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="B_BASE_WIDTH",
       base_width_min_weeks=6, chase_high_delta=-0.10,
       quality_delta=0.18, blocked=False),

    # ── 28–30: c_reclaim_reduces_early_entry ──────────────────────────────────
    _s("SS192-028", "c_reclaim_reduces_early_entry",
       "C_20MA_RECLAIM tightening requires 2-day close above MA — reduces early entry rate.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="C_20MA_RECLAIM",
       min_close_days=2, early_entry_delta=-0.11, blocked=False),
    _s("SS192-029", "c_reclaim_reduces_early_entry",
       "Adding volume confirmation to C reclaim cuts early entry from 22% to 9%.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="C_20MA_RECLAIM",
       early_entry_rate_before=0.22, early_entry_rate_after=0.09,
       improvement_detected=True, blocked=False),
    _s("SS192-030", "c_reclaim_reduces_early_entry",
       "C reclaim with regime filter requirement blocks early entries in choppy markets.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="C_20MA_RECLAIM",
       regime_filter_required=True, early_entry_delta=-0.09, blocked=False),

    # ── 31–33: guardrail_reduces_repeated_mistakes ────────────────────────────
    _s("SS192-031", "guardrail_reduces_repeated_mistakes",
       "Adding CHASE_HIGH_REPEATED guardrail reduces chase-high rate from 20% to 5%.",
       sandbox_mode="GUARDRAIL_COMPARE",
       guardrail_trigger="CHASE_HIGH_REPEATED",
       chase_high_rate_before=0.20, chase_high_rate_after=0.05,
       improvement_detected=True, blocked=False),
    _s("SS192-032", "guardrail_reduces_repeated_mistakes",
       "EARLY_ENTRY_REPEATED guardrail with HARD_BLOCK severity eliminates early entries.",
       sandbox_mode="GUARDRAIL_COMPARE",
       guardrail_trigger="EARLY_ENTRY_REPEATED", severity="HARD_BLOCK",
       early_entry_delta=-0.18, improvement_detected=True, blocked=False),
    _s("SS192-033", "guardrail_reduces_repeated_mistakes",
       "LOW_CASH_RESERVE_REPEATED guardrail enforces minimum 25% cash — risk improved.",
       sandbox_mode="GUARDRAIL_COMPARE",
       guardrail_trigger="LOW_CASH_RESERVE_REPEATED",
       cash_reserve_min_pct=0.25, risk_reduction_score=0.65, blocked=False),

    # ── 34–36: position_sizing_downgrade_reduces_drawdown ─────────────────────
    _s("SS192-034", "position_sizing_downgrade_reduces_drawdown",
       "Auto-downgrade position size after 3 consecutive losses reduces max drawdown.",
       sandbox_mode="POSITION_SIZING_COMPARE",
       consecutive_losses_trigger=3, max_drawdown_delta_r=-0.8,
       improvement_detected=True, blocked=False),
    _s("SS192-035", "position_sizing_downgrade_reduces_drawdown",
       "Reducing position size from 8% to 5% of capital cuts drawdown budget usage from 85% to 50%.",
       sandbox_mode="POSITION_SIZING_COMPARE",
       position_size_before_pct=0.08, position_size_after_pct=0.05,
       drawdown_budget_usage_delta_pct=-0.35, blocked=False),
    _s("SS192-036", "position_sizing_downgrade_reduces_drawdown",
       "Position size degradation in choppy regime reduces drawdown without blocking all signals.",
       sandbox_mode="POSITION_SIZING_COMPARE",
       market_regime="CHOPPY", drawdown_budget_usage_delta_pct=-0.28,
       signal_count_delta=-10, blocked=False),

    # ── 37–39: cash_reserve_increase_reduces_risk ─────────────────────────────
    _s("SS192-037", "cash_reserve_increase_reduces_risk",
       "Raising minimum cash reserve from 15% to 30% reduces over-concentration rate.",
       sandbox_mode="CASH_RESERVE_COMPARE",
       cash_reserve_before_pct=0.15, cash_reserve_after_pct=0.30,
       over_concentration_delta=-0.12, blocked=False),
    _s("SS192-038", "cash_reserve_increase_reduces_risk",
       "Defensive cash reserve increase in distribution market regime cuts risk score.",
       sandbox_mode="CASH_RESERVE_COMPARE",
       market_regime="DISTRIBUTION", cash_reserve_pct=0.40,
       risk_reduction_score=0.80, improvement_detected=True, blocked=False),
    _s("SS192-039", "cash_reserve_increase_reduces_risk",
       "Cash reserve gate raised after losing streak — reduces drawdown budget usage.",
       sandbox_mode="CASH_RESERVE_COMPARE",
       consecutive_losses=4, cash_reserve_after_pct=0.35,
       drawdown_budget_usage_delta_pct=-0.22, blocked=False),

    # ── 40–42: concentration_limit_tightening_improves_diversification ─────────
    _s("SS192-040", "concentration_limit_tightening_improves_diversification",
       "Lowering single position max from 20% to 12% improves diversification score.",
       sandbox_mode="CONCENTRATION_LIMIT_COMPARE",
       max_single_pct_before=0.20, max_single_pct_after=0.12,
       diversification_score_delta=0.18, blocked=False),
    _s("SS192-041", "concentration_limit_tightening_improves_diversification",
       "Sector concentration limit tightened from 35% to 20% — reduces systemic risk.",
       sandbox_mode="CONCENTRATION_LIMIT_COMPARE",
       max_sector_pct_before=0.35, max_sector_pct_after=0.20,
       risk_reduction_score=0.70, improvement_detected=True, blocked=False),
    _s("SS192-042", "concentration_limit_tightening_improves_diversification",
       "Tighter concentration limit prevents repeated over-concentration mistake.",
       sandbox_mode="CONCENTRATION_LIMIT_COMPARE",
       over_concentration_rate_before=0.22, over_concentration_rate_after=0.04,
       improvement_detected=True, blocked=False),

    # ── 43–45: candidate_strategy_regression_detected ─────────────────────────
    _s("SS192-043", "candidate_strategy_regression_detected",
       "Candidate strategy shows expectancy regression from +0.25R to -0.10R — blocked.",
       sandbox_mode="SHADOW_COMPARE",
       expectancy_before_r=0.25, expectancy_after_r=-0.10,
       regression_detected=True, approval_state="REGRESSION_DETECTED", blocked=False),
    _s("SS192-044", "candidate_strategy_regression_detected",
       "Candidate profit factor drops below 1.0 in shadow compare — regression flagged.",
       sandbox_mode="SHADOW_COMPARE",
       profit_factor_candidate=0.88, regression_detected=True,
       approval_state="REGRESSION_DETECTED", blocked=False),
    _s("SS192-045", "candidate_strategy_regression_detected",
       "Candidate max drawdown 40% worse than baseline — regression detected, keep baseline.",
       sandbox_mode="SHADOW_COMPARE",
       max_drawdown_delta_r=1.8, regression_detected=True,
       approval_state="REGRESSION_DETECTED", blocked=False),

    # ── 46–48: candidate_strategy_paper_approved ──────────────────────────────
    _s("SS192-046", "candidate_strategy_paper_approved",
       "Candidate strategy approved for paper after improving win rate and reducing drawdown.",
       sandbox_mode="FULL_RULESET_COMPARE",
       win_rate_delta=0.06, max_drawdown_delta_r=-0.4,
       approval_state="PAPER_APPROVED", regression_detected=False, blocked=False),
    _s("SS192-047", "candidate_strategy_paper_approved",
       "Shadow validation confirms candidate improves shadow_validation_score to 0.82 — approved.",
       sandbox_mode="SHADOW_COMPARE", shadow_validation_score=0.82,
       approval_state="PAPER_APPROVED", regression_detected=False, blocked=False),
    _s("SS192-048", "candidate_strategy_paper_approved",
       "Candidate with tighter A/B/C rules and updated guardrails approved for paper trading.",
       sandbox_mode="FULL_RULESET_COMPARE",
       rule_changes=3, guardrail_changes=2,
       approval_state="PAPER_APPROVED", blocked=False),

    # ── 49–51: candidate_strategy_blocked ─────────────────────────────────────
    _s("SS192-049", "candidate_strategy_blocked",
       "Candidate strategy hard-blocked due to missing evidence for rule change.",
       sandbox_mode="SHADOW_COMPARE",
       blocked=True, block_reason="candidate_rule_without_evidence"),
    _s("SS192-050", "candidate_strategy_blocked",
       "Candidate blocked because it contains a forbidden action word in rule label.",
       sandbox_mode="A_B_RULE_COMPARE",
       blocked=True, block_reason="forbidden_action_words",
       forbidden_word="BUY"),
    _s("SS192-051", "candidate_strategy_blocked",
       "Candidate blocked due to auto-approve attempt without manual review.",
       sandbox_mode="FULL_RULESET_COMPARE",
       auto_approve_attempted=True,
       blocked=True, block_reason="production_strategy_mutation_attempted"),

    # ── 52–53: require_more_data ──────────────────────────────────────────────
    _s("SS192-052", "require_more_data",
       "Insufficient sandbox data — fewer than 20 trades, require more data before deciding.",
       sandbox_mode="SHADOW_COMPARE", trade_count=12,
       approval_state="REQUIRE_MORE_DATA", blocked=False),
    _s("SS192-053", "require_more_data",
       "Shadow validation period too short — extend to full 13-week period before approval.",
       sandbox_mode="SHADOW_COMPARE", period_weeks=4,
       approval_state="REQUIRE_MORE_DATA", blocked=False),

    # ── 54–55: unsafe_export_blocked ─────────────────────────────────────────
    _s("SS192-054", "unsafe_export_blocked",
       "Export blocked due to unsafe export path outside reports/ directory.",
       sandbox_mode="SAFETY_ONLY",
       export_path="/prod/live/strategy.json",
       blocked=True, block_reason="unsafe_export_path"),
    _s("SS192-055", "unsafe_export_blocked",
       "Export blocked because export format targets a live broker API endpoint.",
       sandbox_mode="SAFETY_ONLY",
       export_format="broker_api_call",
       blocked=True, block_reason="unsafe_export_path"),

    # ── 56–57: production_mutation_blocked ────────────────────────────────────
    _s("SS192-056", "production_mutation_blocked",
       "Attempt to write candidate strategy to production database — hard blocked.",
       sandbox_mode="SAFETY_ONLY",
       blocked=True, block_reason="production_strategy_mutation_attempted"),
    _s("SS192-057", "production_mutation_blocked",
       "Attempt to activate candidate strategy live without paper approval — hard blocked.",
       sandbox_mode="SAFETY_ONLY",
       live_activation_attempted=True,
       blocked=True, block_reason="production_strategy_mutation_attempted"),

    # ── 58–60: complete_sandbox_evidence_pack ────────────────────────────────
    _s("SS192-058", "complete_sandbox_evidence_pack",
       "Full evidence pack with performance, journal, backtest, and guardrail evidence.",
       sandbox_mode="FULL_RULESET_COMPARE",
       evidence_types=["performance", "journal", "backtest", "guardrail"],
       evidence_count=14, all_evidence_present=True, blocked=False),
    _s("SS192-059", "complete_sandbox_evidence_pack",
       "Evidence pack confirms all rule changes have supporting evidence — pack complete.",
       sandbox_mode="SHADOW_COMPARE",
       evidence_count=8, all_evidence_present=True,
       evidence_complete=True, blocked=False),
    _s("SS192-060", "complete_sandbox_evidence_pack",
       "Quarterly sandbox evidence pack with audit trail, dashboard, and recommendations.",
       sandbox_mode="FULL_RULESET_COMPARE",
       period="quarterly", evidence_count=12,
       audit_trail=True, dashboard=True, recommendations=True, blocked=False),

    # ── 61–64: complete_sandbox_validation (extra) ────────────────────────────
    _s("SS192-061", "complete_sandbox_validation",
       "Regression-only sandbox run confirms baseline has no regression over 26 weeks.",
       sandbox_mode="REGRESSION_ONLY", period_weeks=26,
       regression_detected=False, approval_state="SHADOW_ONLY", blocked=False),
    _s("SS192-062", "complete_sandbox_validation",
       "Safety-only sandbox run confirms all safety flags correct — health check passes.",
       sandbox_mode="SAFETY_ONLY", all_safe=True,
       health_check_passed=True, blocked=False),
    _s("SS192-063", "complete_sandbox_validation",
       "Guardrail compare mode finds candidate guardrails reduce mistake rate by 30%.",
       sandbox_mode="GUARDRAIL_COMPARE",
       mistake_rate_delta=-0.30, improvement_detected=True, blocked=False),
    _s("SS192-064", "complete_sandbox_validation",
       "Position sizing compare confirms candidate sizing rules reduce drawdown without signals loss.",
       sandbox_mode="POSITION_SIZING_COMPARE",
       signal_count_delta=0, drawdown_budget_usage_delta_pct=-0.20,
       improvement_detected=True, blocked=False),

    # ── 65–66: shadow_compare_baseline_vs_candidate (extra) ───────────────────
    _s("SS192-065", "shadow_compare_baseline_vs_candidate",
       "Shadow compare: candidate improves opportunity loss score — fewer missed entries.",
       sandbox_mode="SHADOW_COMPARE", opportunity_loss_score_delta=-0.15,
       improvement_detected=True, blocked=False),
    _s("SS192-066", "shadow_compare_baseline_vs_candidate",
       "Shadow compare confirms rule stability score of candidate above threshold — stable.",
       sandbox_mode="SHADOW_COMPARE", rule_stability_score=0.88,
       approval_state="KEEP_SHADOW_TESTING", blocked=False),

    # ── 67: a_rule_tightening_improves_risk (extra) ───────────────────────────
    _s("SS192-067", "a_rule_tightening_improves_risk",
       "A entry regime filter requirement reduces trades in choppy markets — risk reduced.",
       sandbox_mode="A_B_RULE_COMPARE", rule_target="A_REGIME_FILTER",
       choppy_market_entries_blocked=True, risk_reduction_score=0.71, blocked=False),

    # ── 68: guardrail_reduces_repeated_mistakes (extra) ───────────────────────
    _s("SS192-068", "guardrail_reduces_repeated_mistakes",
       "OVER_CONCENTRATION_REPEATED guardrail reduces concentration violations from 18% to 2%.",
       sandbox_mode="GUARDRAIL_COMPARE",
       guardrail_trigger="OVER_CONCENTRATION_REPEATED",
       over_concentration_rate_before=0.18, over_concentration_rate_after=0.02,
       improvement_detected=True, blocked=False),

    # ── 69: candidate_strategy_paper_approved (extra) ─────────────────────────
    _s("SS192-069", "candidate_strategy_paper_approved",
       "Candidate with updated B breakout volume gate and C reclaim timing approved for paper.",
       sandbox_mode="FULL_RULESET_COMPARE",
       rule_targets=["B_VOLUME_GATE", "C_RECLAIM_TIMING"],
       approval_state="PAPER_APPROVED", regression_detected=False, blocked=False),

    # ── 70: candidate_strategy_blocked (extra) ────────────────────────────────
    _s("SS192-070", "candidate_strategy_blocked",
       "Candidate blocked because no_broker flag missing from candidate snapshot.",
       sandbox_mode="SAFETY_ONLY",
       blocked=True, block_reason="missing_no_broker_flags"),

    # ── 71–72: complete_sandbox_evidence_pack (extra) ─────────────────────────
    _s("SS192-071", "complete_sandbox_evidence_pack",
       "Evidence pack with rule comparison, shadow comparison, and dashboard exported.",
       sandbox_mode="SHADOW_COMPARE",
       sections=["rule_comparison", "shadow_comparison", "dashboard"],
       all_evidence_present=True, blocked=False),
    _s("SS192-072", "complete_sandbox_evidence_pack",
       "Monthly sandbox evidence pack with all findings, recommendations, and safety audit.",
       sandbox_mode="FULL_RULESET_COMPARE",
       period="monthly", evidence_count=10,
       safety_audit=True, all_evidence_present=True, blocked=False),

    # ── 73–75: safety_audit_scenarios ────────────────────────────────────────
    _s("SS192-073", "safety_audit_all_safe",
       "Safety audit passes — all sandbox safety flags verified correct.",
       sandbox_mode="SAFETY_ONLY",
       all_safe=True, blocked=False),
    _s("SS192-074", "safety_audit_missing_not_investment_advice",
       "Safety audit fails — not_investment_advice flag missing from candidate snapshot.",
       sandbox_mode="SAFETY_ONLY",
       blocked=True, block_reason="missing_not_investment_advice_flags"),
    _s("SS192-075", "safety_audit_no_production_mutation",
       "Safety audit confirms no production strategy mutation attempted — all safe.",
       sandbox_mode="SAFETY_ONLY",
       no_production_strategy_mutation=True, all_safe=True, blocked=False),
]

assert len(SCENARIOS) == 75, f"Expected 75 scenarios, got {len(SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 sandbox scenarios."""
    return list(SCENARIOS)


def get_scenarios_by_type(scenario_type: str) -> List[Dict[str, Any]]:
    """Return scenarios matching a given scenario_type."""
    return [s for s in SCENARIOS if s.get("scenario_type") == scenario_type]


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Return a scenario by ID, or None if not found."""
    for s in SCENARIOS:
        if s.get("scenario_id") == scenario_id:
            return s
    return None
