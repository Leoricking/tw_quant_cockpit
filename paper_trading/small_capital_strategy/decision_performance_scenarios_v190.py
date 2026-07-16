"""
paper_trading/small_capital_strategy/decision_performance_scenarios_v190.py
75 scenarios for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA = "190"
_SAFETY = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "review_only": True, "performance_review_only": True,
    "strategy_improvement_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "not_investment_advice": True, "demo_only": True,
    "not_for_production": True, "production_trading_blocked": True,
}


def _s(sid: str, stype: str, desc: str, **kw) -> Dict[str, Any]:
    # _SAFETY always wins — applied last so safety flags cannot be overridden
    return {"scenario_id": sid, "scenario_type": stype, "description": desc,
            "schema_version": _SCHEMA, **kw, **_SAFETY}


SCENARIOS: List[Dict[str, Any]] = [
    # ── 1–5: Complete review scenarios ────────────────────────────────────────
    _s("DP190-001", "complete_performance_review",
       "Full performance review with all journal entries, all metrics computed.",
       journal_entry_count=20, all_metrics=True, blocked=False),
    _s("DP190-002", "complete_performance_review",
       "Complete review with high win rate and positive expectancy.",
       win_rate=0.65, expectancy_r=0.4, quality_grade="EXCELLENT", blocked=False),
    _s("DP190-003", "complete_performance_review",
       "Complete review with poor win rate requiring improvement.",
       win_rate=0.28, expectancy_r=-0.3, quality_grade="POOR", blocked=False),
    _s("DP190-004", "complete_performance_review",
       "Full review with mixed setup performance across A/B/C buy points.",
       setups=["A_10MA_PULLBACK", "B_BASE_BREAKOUT", "C_20MA_RECLAIM"], blocked=False),
    _s("DP190-005", "complete_performance_review",
       "Quarterly performance review with strategy adjustment plan.",
       period="quarterly", plan_generated=True, blocked=False),

    # ── 6–8: Empty journal blocked ────────────────────────────────────────────
    _s("DP190-006", "empty_journal_blocked",
       "Review blocked because no journal entries provided.",
       journal_entry_count=0, blocked=True,
       block_reason="performance_review_without_journal_entries"),
    _s("DP190-007", "empty_journal_blocked",
       "Review with empty period — no decisions recorded.",
       period="empty_week", blocked=True,
       block_reason="performance_review_without_journal_entries"),
    _s("DP190-008", "empty_journal_blocked",
       "Performance review attempted on a no-trade day set.",
       all_no_trade=True, blocked=True,
       block_reason="performance_review_without_journal_entries"),

    # ── 9–11: Malformed review input ─────────────────────────────────────────
    _s("DP190-009", "malformed_review_input",
       "Review blocked due to missing review_id.",
       review_id="", blocked=True, block_reason="malformed_performance_input"),
    _s("DP190-010", "malformed_review_input",
       "Review with forbidden action word in review focus.",
       review_focus="BUY_SIGNALS", blocked=True,
       block_reason="forbidden_action_words"),
    _s("DP190-011", "malformed_review_input",
       "Review with missing paper_only flag.",
       paper_only=False, blocked=True,
       block_reason="missing_paper_only_flags"),

    # ── 12–15: A buy point scenarios ─────────────────────────────────────────
    _s("DP190-012", "A_buy_point_high_quality",
       "A_10MA_PULLBACK setup with strong win rate and positive R.",
       setup_type="A_10MA_PULLBACK", win_rate=0.70, expectancy_r=0.55,
       quality_grade="EXCELLENT", suggestion="KEEP_RULE"),
    _s("DP190-013", "A_buy_point_high_quality",
       "A pullback with market regime alignment and volume confirmation.",
       setup_type="A_10MA_PULLBACK", regime_aligned=True, volume_confirmed=True,
       quality_grade="GOOD"),
    _s("DP190-014", "A_buy_point_poor_quality",
       "A_10MA_PULLBACK with low win rate needing tightening.",
       setup_type="A_10MA_PULLBACK", win_rate=0.30, expectancy_r=-0.2,
       quality_grade="POOR", suggestion="TIGHTEN_RULE"),
    _s("DP190-015", "A_buy_point_poor_quality",
       "A pullback entered without MA confirmation — poor outcome.",
       setup_type="A_10MA_PULLBACK", ma_confirmed=False, quality_grade="REVIEW_REQUIRED",
       suggestion="REQUIRE_MA_CONFIRMATION"),

    # ── 16–19: B breakout scenarios ───────────────────────────────────────────
    _s("DP190-016", "B_breakout_high_quality",
       "B_BASE_BREAKOUT with strong volume and positive R.",
       setup_type="B_BASE_BREAKOUT", volume_confirmed=True, win_rate=0.62,
       quality_grade="GOOD", suggestion="KEEP_RULE"),
    _s("DP190-017", "B_breakout_high_quality",
       "B breakout on leading theme with regime alignment.",
       setup_type="B_BASE_BREAKOUT", theme_aligned=True, quality_grade="EXCELLENT"),
    _s("DP190-018", "B_breakout_chase_high",
       "B_BASE_BREAKOUT entered as chase high — poor risk/reward.",
       setup_type="B_BASE_BREAKOUT", mistake_tag="CHASE_HIGH", quality_grade="POOR",
       suggestion="BLOCK_SETUP"),
    _s("DP190-019", "B_breakout_chase_high",
       "Repeated chase high pattern in B breakouts over 4 weeks.",
       setup_type="B_BASE_BREAKOUT", chase_high_count=4, suggestion="REQUIRE_VOLUME_CONFIRMATION"),

    # ── 20–23: C reclaim scenarios ────────────────────────────────────────────
    _s("DP190-020", "C_reclaim_high_quality",
       "C_20MA_RECLAIM with confirmed market regime and clean setup.",
       setup_type="C_20MA_RECLAIM", win_rate=0.60, quality_grade="GOOD",
       suggestion="KEEP_RULE"),
    _s("DP190-021", "C_reclaim_high_quality",
       "C reclaim with strong theme and low concentration risk.",
       setup_type="C_20MA_RECLAIM", theme_strength="HIGH", quality_grade="EXCELLENT"),
    _s("DP190-022", "C_reclaim_early_entry",
       "C_20MA_RECLAIM entered too early — premature entry mistake.",
       setup_type="C_20MA_RECLAIM", mistake_tag="ENTER_TOO_EARLY", quality_grade="POOR",
       suggestion="TIGHTEN_RULE"),
    _s("DP190-023", "C_reclaim_early_entry",
       "Early entry into C reclaim without waiting for daily close.",
       setup_type="C_20MA_RECLAIM", premature=True,
       suggestion="REQUIRE_MARKET_REGIME_CONFIRMATION"),

    # ── 24–26: Reduce risk scenarios ──────────────────────────────────────────
    _s("DP190-024", "reduce_risk_successful",
       "REDUCE_RISK action taken correctly before regime deterioration.",
       state="REDUCE_RISK", outcome="prevented_loss", quality_grade="GOOD"),
    _s("DP190-025", "reduce_risk_successful",
       "Risk reduced on time — drawdown stayed within budget.",
       state="REDUCE_RISK", drawdown_within_budget=True, quality_grade="EXCELLENT"),
    _s("DP190-026", "reduce_risk_too_late",
       "REDUCE_RISK taken after significant drawdown — late response.",
       state="REDUCE_RISK", late=True, drawdown_exceeded=True,
       quality_grade="REVIEW_REQUIRED", suggestion="REQUIRE_RISK_REVIEW"),

    # ── 27–29: Blocked decision scenarios ─────────────────────────────────────
    _s("DP190-027", "blocked_decision_respected",
       "BLOCKED decision correctly respected — no paper trade initiated.",
       state="BLOCKED", respected=True, quality_grade="EXCELLENT"),
    _s("DP190-028", "blocked_decision_respected",
       "Block condition: weak evidence. Decision stayed blocked.",
       state="BLOCKED", block_reason="MISSING_EVIDENCE", respected=True),
    _s("DP190-029", "blocked_decision_ignored",
       "Block condition ignored — paper trade initiated against block rule.",
       state="BLOCKED", respected=False, quality_grade="POOR",
       mistake_tag="IGNORE_BLOCK_REASON", suggestion="REQUIRE_RISK_REVIEW"),

    # ── 30–32: Over-concentration scenarios ───────────────────────────────────
    _s("DP190-030", "over_concentration_finding",
       "Single theme > 60% of portfolio — concentration finding flagged.",
       concentration_pct=0.62, finding_type="over_concentration",
       suggestion="LOWER_POSITION_SIZE"),
    _s("DP190-031", "over_concentration_finding",
       "Too many positions in same sector without diversification.",
       finding_type="over_concentration", suggestion="REQUIRE_RISK_REVIEW"),
    _s("DP190-032", "over_concentration_finding",
       "Portfolio concentration triggered risk budget breach.",
       finding_type="over_concentration", risk_budget_breached=True,
       suggestion="RAISE_CASH_RESERVE"),

    # ── 33–35: Low cash reserve scenarios ────────────────────────────────────
    _s("DP190-033", "low_cash_reserve_finding",
       "Cash reserve dropped below 30% — paper cash reserve alert.",
       cash_reserve_pct=0.22, finding_type="low_cash_reserve",
       suggestion="RAISE_CASH_RESERVE"),
    _s("DP190-034", "low_cash_reserve_finding",
       "Low cash reserve persisted for 3 consecutive paper weeks.",
       finding_type="low_cash_reserve", consecutive_weeks=3,
       suggestion="LOWER_POSITION_SIZE"),
    _s("DP190-035", "low_cash_reserve_finding",
       "Cash reserve at 15% — improvement plan recommends reducing sizes.",
       cash_reserve_pct=0.15, finding_type="low_cash_reserve",
       quality_grade="REVIEW_REQUIRED"),

    # ── 36–38: Positive expectancy scenarios ─────────────────────────────────
    _s("DP190-036", "positive_expectancy",
       "Positive expectancy R=+0.45 across 20 paper decisions.",
       expectancy_r=0.45, win_rate=0.60, quality_grade="GOOD",
       suggestion="KEEP_RULE"),
    _s("DP190-037", "positive_expectancy",
       "Strong expectancy with profit factor > 1.8.",
       expectancy_r=0.60, profit_factor=1.85, quality_grade="EXCELLENT"),
    _s("DP190-038", "positive_expectancy",
       "Marginal positive expectancy needing monitoring.",
       expectancy_r=0.08, quality_grade="ACCEPTABLE",
       suggestion="NO_CHANGE"),

    # ── 39–41: Negative expectancy scenarios ─────────────────────────────────
    _s("DP190-039", "negative_expectancy",
       "Negative expectancy R=-0.35 — strategy review required.",
       expectancy_r=-0.35, quality_grade="POOR",
       suggestion="TIGHTEN_RULE"),
    _s("DP190-040", "negative_expectancy",
       "Deeply negative expectancy — setup should be blocked.",
       expectancy_r=-0.70, quality_grade="INVALID",
       suggestion="BLOCK_SETUP"),
    _s("DP190-041", "negative_expectancy",
       "Negative expectancy driven by oversized losses.",
       expectancy_r=-0.25, avg_loss_r=-2.5, suggestion="REQUIRE_RISK_REVIEW"),

    # ── 42–44: High drawdown scenarios ───────────────────────────────────────
    _s("DP190-042", "high_drawdown_blocked",
       "Drawdown exceeded budget R=7.2 — review blocked for safety.",
       max_drawdown_r=7.2, drawdown_budget_r=6.0, drawdown_blocked=True,
       suggestion="REQUIRE_RISK_REVIEW"),
    _s("DP190-043", "high_drawdown_blocked",
       "5-consecutive-loss streak caused drawdown breach.",
       consecutive_loss_count=5, drawdown_blocked=True,
       suggestion="LOWER_POSITION_SIZE"),
    _s("DP190-044", "high_drawdown_blocked",
       "Drawdown at 95% of budget — near-block condition.",
       drawdown_budget_usage_pct=95.0, suggestion="RAISE_CASH_RESERVE"),

    # ── 45–47: Weak evidence scenarios ───────────────────────────────────────
    _s("DP190-045", "weak_evidence_blocked",
       "Performance review blocked — improvement suggestion lacks evidence.",
       suggestion_id="S-001", evidence_refs=[], blocked=True,
       block_reason="improvement_suggestion_without_evidence"),
    _s("DP190-046", "weak_evidence_blocked",
       "Setup analysis blocked due to missing evidence refs.",
       setup_type="B_BASE_BREAKOUT", evidence_complete=False, blocked=True),
    _s("DP190-047", "weak_evidence_blocked",
       "Improvement plan rejected — evidence completeness rate < 50%.",
       evidence_completeness_rate=0.43, quality_grade="POOR",
       suggestion="REQUIRE_MORE_EVIDENCE"),

    # ── 48–50: Strategy improvement report scenarios ──────────────────────────
    _s("DP190-048", "strategy_improvement_report",
       "Full improvement report generated with 3 high-priority suggestions.",
       suggestion_count=3, priority="HIGH", report_generated=True),
    _s("DP190-049", "strategy_improvement_report",
       "Improvement report: tighten A pullback, block B chase, keep C reclaim.",
       suggestions=["TIGHTEN_RULE", "BLOCK_SETUP", "KEEP_RULE"], blocked=False),
    _s("DP190-050", "strategy_improvement_report",
       "Markdown improvement report exported to reports/ path.",
       export_format="markdown", export_path="reports/", safe_path=True),

    # ── 51–55: Second wave and watchlist scenarios ────────────────────────────
    _s("DP190-051", "second_wave_scenario",
       "SECOND_WAVE setup review — lower win rate, caution flagged.",
       setup_type="SECOND_WAVE", win_rate=0.38, suggestion="TIGHTEN_RULE"),
    _s("DP190-052", "second_wave_scenario",
       "Late second wave entry — LATE_SECOND_WAVE mistake recorded.",
       setup_type="SECOND_WAVE", mistake_tag="LATE_SECOND_WAVE",
       quality_grade="REVIEW_REQUIRED"),
    _s("DP190-053", "watchlist_only_scenario",
       "WATCHLIST_ONLY period — no entries, research only.",
       setup_type="WATCHLIST_ONLY", paper_entries=0),
    _s("DP190-054", "no_trade_day_scenario",
       "NO_TRADE_DAY — market regime poor, all decisions blocked.",
       setup_type="NO_TRADE_DAY", blocked_count=5, quality_grade="GOOD"),
    _s("DP190-055", "unknown_setup_scenario",
       "UNKNOWN_SETUP type — needs manual review and classification.",
       setup_type="UNKNOWN_SETUP", suggestion="REVIEW_MANUALLY"),

    # ── 56–60: R-multiple analytics scenarios ────────────────────────────────
    _s("DP190-056", "r_multiple_healthy",
       "Average R-multiple healthy: avg_win=1.8R, avg_loss=1.0R.",
       avg_win_r=1.8, avg_loss_r=-1.0, r_multiple_healthy=True),
    _s("DP190-057", "r_multiple_unhealthy",
       "R-multiple skewed: avg_win=0.5R, avg_loss=1.5R — unhealthy.",
       avg_win_r=0.5, avg_loss_r=-1.5, r_multiple_healthy=False,
       suggestion="REQUIRE_RISK_REVIEW"),
    _s("DP190-058", "profit_factor_high",
       "Profit factor 2.1 — strong strategy performance.",
       profit_factor=2.1, quality_grade="EXCELLENT"),
    _s("DP190-059", "profit_factor_low",
       "Profit factor 0.7 — strategy losing overall.",
       profit_factor=0.7, quality_grade="POOR", suggestion="TIGHTEN_RULE"),
    _s("DP190-060", "largest_loss_review",
       "Single trade -3.2R loss reviewed — position oversized.",
       largest_loss_r=-3.2, mistake_tag="OVERSIZE_POSITION",
       suggestion="LOWER_POSITION_SIZE"),

    # ── 61–65: Mistake pattern scenarios ─────────────────────────────────────
    _s("DP190-061", "chase_high_pattern",
       "Chase high: 4 occurrences, 80% loss rate — pattern flagged.",
       mistake_tag="CHASE_HIGH", count=4, loss_rate=0.80,
       suggestion="BLOCK_SETUP"),
    _s("DP190-062", "early_entry_pattern",
       "Early entry: 3 occurrences — tighten entry criteria.",
       mistake_tag="ENTER_TOO_EARLY", count=3,
       suggestion="TIGHTEN_RULE"),
    _s("DP190-063", "ignore_market_regime_pattern",
       "Market regime ignored in 5 decisions — critical finding.",
       mistake_tag="IGNORE_MARKET_REGIME", count=5,
       suggestion="REQUIRE_MARKET_REGIME_CONFIRMATION"),
    _s("DP190-064", "oversize_position_pattern",
       "Oversized positions in 3 setups — lower position size.",
       mistake_tag="OVERSIZE_POSITION", count=3,
       suggestion="LOWER_POSITION_SIZE"),
    _s("DP190-065", "no_mistake_found",
       "Review period: no significant mistake tags — strategy healthy.",
       mistake_count=0, quality_grade="EXCELLENT", suggestion="KEEP_RULE"),

    # ── 66–70: Safety and blocking scenarios ─────────────────────────────────
    _s("DP190-066", "safety_audit_pass",
       "All safety flags pass audit — paper only, no-bkr, no real orders.",
       all_safe=True, broker_execution=False, real_order=False),
    _s("DP190-067", "forbidden_action_blocked",
       "Performance action BUY blocked — not a performance review action.",
       action="BUY", blocked=True, block_reason="forbidden_action_words"),
    _s("DP190-068", "unsafe_export_path_blocked",
       "Export to production_db path blocked — unsafe path detected.",
       export_path="production_db/", safe_path=False, blocked=True,
       block_reason="unsafe_export_path"),
    _s("DP190-069", "missing_broker_flag_blocked",
       "Performance review missing no-bkr safety flag — hard block.",
       no_broker=False, blocked=True, block_reason="missing_no_broker_flags"),
    _s("DP190-070", "missing_journal_source_blocked",
       "Improvement suggestion missing journal source — hard block.",
       blocked=True, block_reason="missing_journal_source"),

    # ── 71–75: Dashboard, evidence, audit scenarios ───────────────────────────
    _s("DP190-071", "performance_dashboard",
       "Full dashboard built with all analytics sections.",
       sections=["strategy_summary", "r_multiple", "drawdown", "expectancy"],
       overall_grade="GOOD", blocked=False),
    _s("DP190-072", "evidence_pack_complete",
       "Evidence pack with 5 evidence items — all evidence present.",
       evidence_count=5, all_evidence_present=True),
    _s("DP190-073", "audit_trail_complete",
       "Audit trail with 4 review steps — deterministic timestamps.",
       step_count=4, audit_complete=True,
       deterministic_timestamp_policy="date_label_only_no_wall_clock"),
    _s("DP190-074", "export_manifest_safe",
       "Export manifest to reports/ — safe path verified.",
       export_path="reports/", safe_path=True, export_format="json"),
    _s("DP190-075", "backward_compat_v189",
       "Performance review references v1.8.9 journal entries — backward compat.",
       journal_version="1.8.9", backward_compat=True, blocked=False),
]

assert len(SCENARIOS) == 75, f"Expected 75 scenarios, got {len(SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 performance review scenarios."""
    return list(SCENARIOS)


def get_scenarios_by_type(scenario_type: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by scenario_type."""
    return [s for s in SCENARIOS if s.get("scenario_type") == scenario_type]


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return a scenario by its ID, or empty dict if not found."""
    for s in SCENARIOS:
        if s.get("scenario_id") == scenario_id:
            return s
    return {}
