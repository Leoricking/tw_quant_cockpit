"""
paper_trading/small_capital_strategy/strategy_tuning_scenarios_v191.py
75 scenarios for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA = "191"
_SAFETY = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "tuning_only": True, "guardrail_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "not_investment_advice": True, "demo_only": True,
    "not_for_production": True, "production_trading_blocked": True,
}


def _s(sid: str, stype: str, desc: str, **kw) -> Dict[str, Any]:
    return {"scenario_id": sid, "scenario_type": stype, "description": desc,
            "schema_version": _SCHEMA, **kw, **_SAFETY}


SCENARIOS: List[Dict[str, Any]] = [
    # ── 1–5: Complete rule tuning review ─────────────────────────────────────
    _s("ST191-001", "complete_rule_tuning_review",
       "Full rule tuning review with all rule categories evaluated.",
       rule_categories=14, all_metrics=True, blocked=False),
    _s("ST191-002", "complete_rule_tuning_review",
       "Complete tuning with positive expectancy across ABC setups.",
       expectancy_r=0.35, win_rate=0.60, blocked=False),
    _s("ST191-003", "complete_rule_tuning_review",
       "Complete review finding multiple rules to tighten.",
       rules_to_tighten=4, win_rate=0.28, blocked=False),
    _s("ST191-004", "complete_rule_tuning_review",
       "Quarterly rule tuning with guardrail evidence pack.",
       period="quarterly", evidence_pack=True, blocked=False),
    _s("ST191-005", "complete_rule_tuning_review",
       "Full review generating tuning audit trail and report.",
       audit_trail=True, report_generated=True, blocked=False),

    # ── 6–8: Empty performance source blocked ────────────────────────────────
    _s("ST191-006", "empty_performance_source_blocked",
       "Tuning blocked because performance_source is empty.",
       performance_source="", blocked=True,
       block_reason="missing_performance_source"),
    _s("ST191-007", "empty_performance_source_blocked",
       "Tuning blocked because journal_source is empty.",
       journal_source="", blocked=True,
       block_reason="missing_journal_source"),
    _s("ST191-008", "empty_performance_source_blocked",
       "Tuning blocked with both sources missing.",
       performance_source="", journal_source="", blocked=True,
       block_reason="missing_performance_source"),

    # ── 9–11: Malformed tuning input ─────────────────────────────────────────
    _s("ST191-009", "malformed_tuning_input",
       "Tuning blocked due to missing tuning_id.",
       tuning_id="", blocked=True, block_reason="malformed_tuning_input"),
    _s("ST191-010", "malformed_tuning_input",
       "Tuning with forbidden action word in tuning_id.",
       tuning_id="BUY_SIGNALS_REVIEW", blocked=True,
       block_reason="forbidden_action_words"),
    _s("ST191-011", "malformed_tuning_input",
       "Tuning with missing paper_only flag.",
       paper_only=False, blocked=True,
       block_reason="missing_paper_only_flags"),

    # ── 12–16: Keep A buy point rule ─────────────────────────────────────────
    _s("ST191-012", "keep_a_buy_point_rule",
       "A_10MA_PULLBACK with strong win rate and positive expectancy — keep rule.",
       rule_category="ABC_BUY_POINT", win_rate=0.68, expectancy_r=0.55,
       recommendation="KEEP_RULE", blocked=False),
    _s("ST191-013", "keep_a_buy_point_rule",
       "A pullback with regime alignment and volume confirmation — keep rule.",
       rule_category="ABC_BUY_POINT", regime_aligned=True, volume_confirmed=True,
       recommendation="KEEP_RULE", blocked=False),
    _s("ST191-014", "keep_a_buy_point_rule",
       "A pullback stable performance — no change needed.",
       rule_category="ABC_BUY_POINT", win_rate=0.62, expectancy_r=0.30,
       recommendation="NO_CHANGE", blocked=False),
    _s("ST191-015", "keep_a_buy_point_rule",
       "A pullback with excellent R-multiple ratio — keep rule.",
       rule_category="ABC_BUY_POINT", avg_win_r=2.1, avg_loss_r=-1.0,
       recommendation="KEEP_RULE", blocked=False),
    _s("ST191-016", "keep_a_buy_point_rule",
       "A pullback borderline — escalate for manual review.",
       rule_category="ABC_BUY_POINT", win_rate=0.45, expectancy_r=0.05,
       recommendation="ESCALATE_TO_REVIEW", blocked=False),

    # ── 17–20: Tighten A buy point rule ──────────────────────────────────────
    _s("ST191-017", "tighten_a_buy_point_rule",
       "A buy point win rate too low — tighten entry criteria.",
       rule_category="ABC_BUY_POINT", win_rate=0.29, expectancy_r=-0.1,
       recommendation="TIGHTEN_RULE", blocked=False),
    _s("ST191-018", "tighten_a_buy_point_rule",
       "A buy point chase-high mistake repeated — require more evidence.",
       rule_category="ABC_BUY_POINT", chase_high_rate=0.22,
       recommendation="REQUIRE_MORE_EVIDENCE", blocked=False),
    _s("ST191-019", "tighten_a_buy_point_rule",
       "A early entry repeated — tighten timing rule.",
       rule_category="ABC_BUY_POINT", early_entry_rate=0.18,
       recommendation="TIGHTEN_RULE", blocked=False),
    _s("ST191-020", "tighten_a_buy_point_rule",
       "A buy point without MA confirmation — require MA filter.",
       rule_category="ABC_BUY_POINT", ma_break_ignored_rate=0.25,
       recommendation="REQUIRE_MA_CONFIRMATION", blocked=False),

    # ── 21–24: Tighten B breakout rule ───────────────────────────────────────
    _s("ST191-021", "tighten_b_breakout_rule",
       "B_BASE_BREAKOUT without volume confirmation — require volume filter.",
       rule_category="ABC_BUY_POINT", volume_confirmation_missing_rate=0.35,
       recommendation="REQUIRE_VOLUME_CONFIRMATION", blocked=False),
    _s("ST191-022", "tighten_b_breakout_rule",
       "B breakout in bad market regime — require regime filter.",
       rule_category="ABC_BUY_POINT", market_regime_mismatch_rate=0.28,
       recommendation="REQUIRE_MARKET_REGIME_CONFIRMATION", blocked=False),
    _s("ST191-023", "tighten_b_breakout_rule",
       "B breakout early entry pattern — tighten base width rule.",
       rule_category="ABC_BUY_POINT", early_entry_rate=0.20,
       recommendation="TIGHTEN_RULE", blocked=False),
    _s("ST191-024", "tighten_b_breakout_rule",
       "B breakout loss average too high — tighten stop placement.",
       rule_category="STOP_LOSS", average_loss_r=-2.8,
       recommendation="TIGHTEN_RULE", blocked=False),

    # ── 25–27: Disable weak setup ─────────────────────────────────────────────
    _s("ST191-025", "disable_weak_setup",
       "Setup with negative expectancy — disable.",
       expectancy_r=-0.6, win_rate=0.22,
       recommendation="DISABLE_SETUP", blocked=False),
    _s("ST191-026", "disable_weak_setup",
       "SECOND_WAVE_ENTRY with consistently negative R — disable.",
       rule_category="SECOND_WAVE_ENTRY", expectancy_r=-0.4,
       recommendation="DISABLE_SETUP", blocked=False),
    _s("ST191-027", "disable_weak_setup",
       "C_20MA_RECLAIM failing majority of the time — disable.",
       rule_category="ABC_BUY_POINT", win_rate=0.20, mistake_rate=0.45,
       recommendation="DISABLE_SETUP", blocked=False),

    # ── 28–30: Add chase-high guardrail ──────────────────────────────────────
    _s("ST191-028", "add_chase_high_guardrail",
       "Chase-high pattern detected — add guardrail.",
       guardrail_trigger="CHASE_HIGH_REPEATED", chase_high_rate=0.20,
       recommendation="ADD_GUARDRAIL", blocked=False),
    _s("ST191-029", "add_chase_high_guardrail",
       "Chase high in trending market — add severity=CRITICAL guardrail.",
       guardrail_trigger="CHASE_HIGH_REPEATED", severity="CRITICAL",
       recommendation="ADD_GUARDRAIL", blocked=False),
    _s("ST191-030", "add_chase_high_guardrail",
       "Chase high with over-concentration — dual guardrail.",
       guardrail_trigger="CHASE_HIGH_REPEATED",
       secondary_trigger="OVER_CONCENTRATION_REPEATED",
       recommendation="ADD_GUARDRAIL", blocked=False),

    # ── 31–33: Add early entry guardrail ─────────────────────────────────────
    _s("ST191-031", "add_early_entry_guardrail",
       "Early entry pattern repeated — add guardrail.",
       guardrail_trigger="EARLY_ENTRY_REPEATED", early_entry_rate=0.18,
       recommendation="ADD_GUARDRAIL", blocked=False),
    _s("ST191-032", "add_early_entry_guardrail",
       "Early entry causing large losses — add HARD_BLOCK guardrail.",
       guardrail_trigger="EARLY_ENTRY_REPEATED", severity="HARD_BLOCK",
       recommendation="ADD_GUARDRAIL", blocked=False),
    _s("ST191-033", "add_early_entry_guardrail",
       "Early entry without MA confirmation — combined guardrail.",
       guardrail_trigger="EARLY_ENTRY_REPEATED",
       secondary_trigger="MA_BREAK_IGNORED",
       recommendation="ADD_GUARDRAIL", blocked=False),

    # ── 34–36: Lower position size ────────────────────────────────────────────
    _s("ST191-034", "lower_position_size",
       "Drawdown budget exceeded — lower position size.",
       guardrail_trigger="DRAWDOWN_BUDGET_EXCEEDED", drawdown_usage=0.85,
       recommendation="LOWER_POSITION_SIZE", blocked=False),
    _s("ST191-035", "lower_position_size",
       "High mistake rate — auto-degrade position sizing.",
       mistake_rate=0.38, recommendation="LOWER_POSITION_SIZE", blocked=False),
    _s("ST191-036", "lower_position_size",
       "Negative expectancy period — reduce size until improved.",
       expectancy_r=-0.25, recommendation="LOWER_POSITION_SIZE", blocked=False),

    # ── 37–39: Raise cash reserve ─────────────────────────────────────────────
    _s("ST191-037", "raise_cash_reserve",
       "Low cash reserve pattern repeated — raise threshold.",
       guardrail_trigger="LOW_CASH_RESERVE_REPEATED", low_cash_rate=0.22,
       recommendation="RAISE_CASH_RESERVE", blocked=False),
    _s("ST191-038", "raise_cash_reserve",
       "Over-concentration with low cash — raise reserve.",
       guardrail_trigger="OVER_CONCENTRATION_REPEATED",
       recommendation="RAISE_CASH_RESERVE", blocked=False),
    _s("ST191-039", "raise_cash_reserve",
       "Volatile market regime with low cash — defensive raise.",
       market_regime="CHOPPY", recommendation="RAISE_CASH_RESERVE", blocked=False),

    # ── 40–41: Lower concentration limit ─────────────────────────────────────
    _s("ST191-040", "lower_concentration_limit",
       "Over-concentration repeated — lower max position limit.",
       guardrail_trigger="OVER_CONCENTRATION_REPEATED",
       recommendation="LOWER_CONCENTRATION_LIMIT", blocked=False),
    _s("ST191-041", "lower_concentration_limit",
       "Single sector concentration — tighten concentration rule.",
       concentration_pct=0.40, recommendation="LOWER_CONCENTRATION_LIMIT", blocked=False),

    # ── 42–44: Require more evidence ─────────────────────────────────────────
    _s("ST191-042", "require_more_evidence",
       "Evidence missing repeatedly — require fuller evidence pack.",
       guardrail_trigger="EVIDENCE_MISSING_REPEATED",
       recommendation="REQUIRE_MORE_EVIDENCE", blocked=False),
    _s("ST191-043", "require_more_evidence",
       "Block-reason ignored — require evidence of compliance.",
       guardrail_trigger="BLOCK_REASON_IGNORED",
       recommendation="REQUIRE_MORE_EVIDENCE", blocked=False),
    _s("ST191-044", "require_more_evidence",
       "Marginal setups passing without sufficient backing.",
       evidence_completeness_rate=0.55,
       recommendation="REQUIRE_MORE_EVIDENCE", blocked=False),

    # ── 45–46: Require market regime confirmation ─────────────────────────────
    _s("ST191-045", "require_market_regime_confirmation",
       "Market regime mismatch rate too high — require regime filter.",
       guardrail_trigger="MARKET_REGIME_MISMATCH",
       recommendation="REQUIRE_MARKET_REGIME_CONFIRMATION", blocked=False),
    _s("ST191-046", "require_market_regime_confirmation",
       "Entries in choppy market causing losses — require regime check.",
       market_regime_mismatch_rate=0.30,
       recommendation="REQUIRE_MARKET_REGIME_CONFIRMATION", blocked=False),

    # ── 47–48: Require volume confirmation ───────────────────────────────────
    _s("ST191-047", "require_volume_confirmation",
       "Volume confirmation missing repeatedly — require volume filter.",
       guardrail_trigger="VOLUME_CONFIRMATION_MISSING",
       recommendation="REQUIRE_VOLUME_CONFIRMATION", blocked=False),
    _s("ST191-048", "require_volume_confirmation",
       "Breakout without volume causing false breakouts — add volume gate.",
       volume_confirmation_missing_rate=0.32,
       recommendation="REQUIRE_VOLUME_CONFIRMATION", blocked=False),

    # ── 49–50: Require MA confirmation ───────────────────────────────────────
    _s("ST191-049", "require_ma_confirmation",
       "MA break ignored repeatedly — require MA filter before entry.",
       guardrail_trigger="MA_BREAK_IGNORED",
       recommendation="REQUIRE_MA_CONFIRMATION", blocked=False),
    _s("ST191-050", "require_ma_confirmation",
       "Entry below key MA without justification — require MA gate.",
       ma_break_ignored_rate=0.22,
       recommendation="REQUIRE_MA_CONFIRMATION", blocked=False),

    # ── 51–52: Manual review required ────────────────────────────────────────
    _s("ST191-051", "manual_review_required",
       "Borderline rule — escalate to human review.",
       recommendation="REQUIRE_MANUAL_REVIEW", blocked=False,
       approval_state="REVIEW_REQUIRED"),
    _s("ST191-052", "manual_review_required",
       "Conflicting signals — manual review before any rule change.",
       conflicting_signals=True, recommendation="REQUIRE_MANUAL_REVIEW",
       approval_state="REVIEW_REQUIRED", blocked=False),

    # ── 53–54: Production mutation blocked ───────────────────────────────────
    _s("ST191-053", "production_mutation_blocked",
       "Attempt to write production strategy — hard blocked.",
       blocked=True, block_reason="production_strategy_mutation_attempted"),
    _s("ST191-054", "production_mutation_blocked",
       "Auto-approve of rule change without review — hard blocked.",
       blocked=True, block_reason="production_strategy_mutation_attempted",
       auto_approve_attempted=True),

    # ── 55–56: Forbidden action word blocked ─────────────────────────────────
    _s("ST191-055", "forbidden_action_word_blocked",
       "Tuning input containing a forbidden trading word — hard blocked.",
       blocked=True, block_reason="forbidden_action_words",
       forbidden_word="SUBMIT_ORDER"),
    _s("ST191-056", "forbidden_action_word_blocked",
       "Recommendation output containing a forbidden trading keyword — hard blocked.",
       blocked=True, block_reason="forbidden_action_words",
       forbidden_word="EXECUTE"),

    # ── 57–58: Complete tuning evidence pack ─────────────────────────────────
    _s("ST191-057", "complete_tuning_evidence_pack",
       "Full evidence pack with all required items — complete.",
       evidence_count=12, all_evidence_present=True, blocked=False),
    _s("ST191-058", "complete_tuning_evidence_pack",
       "Evidence pack with performance, journal, and backtest data.",
       evidence_types=["performance", "journal", "backtest"],
       all_evidence_present=True, blocked=False),

    # ── 59–61: Guardrail trigger scenarios ───────────────────────────────────
    _s("ST191-059", "guardrail_expectancy_negative",
       "Expectancy negative — guardrail fires.",
       guardrail_trigger="EXPECTANCY_NEGATIVE", expectancy_r=-0.3,
       triggered=True, blocked=False),
    _s("ST191-060", "guardrail_win_rate_low",
       "Win rate below threshold — guardrail fires.",
       guardrail_trigger="WIN_RATE_TOO_LOW", win_rate=0.28,
       triggered=True, blocked=False),
    _s("ST191-061", "guardrail_drawdown_exceeded",
       "Drawdown budget exceeded — guardrail hard-block.",
       guardrail_trigger="DRAWDOWN_BUDGET_EXCEEDED", drawdown_usage=0.95,
       triggered=True, severity="HARD_BLOCK", blocked=False),

    # ── 62–64: Position sizing scenarios ─────────────────────────────────────
    _s("ST191-062", "position_sizing_review",
       "Position sizing within budget — no change needed.",
       rule_category="POSITION_SIZING", drawdown_usage=0.40,
       recommendation="NO_CHANGE", blocked=False),
    _s("ST191-063", "position_sizing_review",
       "Position sizing too aggressive — lower position size.",
       rule_category="POSITION_SIZING", drawdown_usage=0.82,
       recommendation="LOWER_POSITION_SIZE", blocked=False),
    _s("ST191-064", "position_sizing_review",
       "Auto position size degradation after 3 losses.",
       consecutive_losses=3, recommendation="LOWER_POSITION_SIZE", blocked=False),

    # ── 65–66: Cash reserve scenarios ────────────────────────────────────────
    _s("ST191-065", "cash_reserve_review",
       "Cash reserve adequate — keep rule.",
       rule_category="CASH_RESERVE", cash_reserve_pct=0.30,
       recommendation="KEEP_RULE", blocked=False),
    _s("ST191-066", "cash_reserve_review",
       "Cash reserve below minimum — raise reserve target.",
       rule_category="CASH_RESERVE", cash_reserve_pct=0.12,
       recommendation="RAISE_CASH_RESERVE", blocked=False),

    # ── 67–68: Concentration limit scenarios ─────────────────────────────────
    _s("ST191-067", "concentration_limit_review",
       "Concentration within limit — no change.",
       rule_category="CONCENTRATION_LIMIT", max_single_pct=0.15,
       recommendation="NO_CHANGE", blocked=False),
    _s("ST191-068", "concentration_limit_review",
       "Concentration too high — lower limit.",
       rule_category="CONCENTRATION_LIMIT", max_single_pct=0.35,
       recommendation="LOWER_CONCENTRATION_LIMIT", blocked=False),

    # ── 69–70: Approval state scenarios ──────────────────────────────────────
    _s("ST191-069", "approval_state_proposed",
       "New tuning proposal — state = PROPOSED.",
       approval_state="PROPOSED", blocked=False),
    _s("ST191-070", "approval_state_review_required",
       "High-impact rule change — state = REVIEW_REQUIRED.",
       approval_state="REVIEW_REQUIRED", blocked=False),

    # ── 71–72: Backtest snapshot scenarios ───────────────────────────────────
    _s("ST191-071", "backtest_snapshot_improvement",
       "Rule adjustment improves expectancy — improvement_detected=True.",
       expectancy_before=-0.1, expectancy_after=0.3,
       improvement_detected=True, blocked=False),
    _s("ST191-072", "backtest_snapshot_no_improvement",
       "Rule adjustment shows no improvement — improvement_detected=False.",
       expectancy_before=0.2, expectancy_after=0.15,
       improvement_detected=False, blocked=False),

    # ── 73–75: Safety audit scenarios ────────────────────────────────────────
    _s("ST191-073", "safety_audit_all_safe",
       "Safety audit passes — all flags correct.",
       all_safe=True, blocked=False),
    _s("ST191-074", "safety_audit_guardrail_without_trigger",
       "Guardrail created without trigger — blocked.",
       blocked=True, block_reason="guardrail_without_trigger"),
    _s("ST191-075", "safety_audit_no_production_mutation",
       "No production strategy mutation flag present — all safe.",
       no_production_strategy_mutation=True, all_safe=True, blocked=False),
]


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 tuning scenarios."""
    return list(SCENARIOS)


def get_scenarios_by_type(scenario_type: str) -> List[Dict[str, Any]]:
    """Return scenarios matching a given type."""
    return [s for s in SCENARIOS if s.get("scenario_type") == scenario_type]


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return a scenario by ID, or empty dict if not found."""
    for s in SCENARIOS:
        if s.get("scenario_id") == scenario_id:
            return s
    return {}
