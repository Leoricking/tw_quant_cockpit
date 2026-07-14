"""
paper_trading/small_capital_strategy/decision_report_scenarios_v187.py
75 Decision Report scenarios for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict, Any

_SAFETY_META = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "decision_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_SCENARIOS: List[Dict[str, Any]] = [
    # ── Daily Report Scenarios (10) ──────────────────────────────────────────
    {"id": "DR187-001", "category": "daily_complete_report",
     "description": "Daily complete report: BULL + 3 candidates ready + full evidence → COMPLETE", **_SAFETY_META},
    {"id": "DR187-002", "category": "daily_bull_one_ready",
     "description": "Daily BULL regime + 1 paper-entry candidate → COMPLETE daily report", **_SAFETY_META},
    {"id": "DR187-003", "category": "daily_blocked_regime",
     "description": "Daily BEAR regime → all candidates BLOCKED → daily report BLOCKED", **_SAFETY_META},
    {"id": "DR187-004", "category": "daily_reduce_risk",
     "description": "Daily REDUCE_RISK grade → daily report REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DR187-005", "category": "daily_no_candidates",
     "description": "Daily report with 0 candidates → COMPLETE (empty valid report)", **_SAFETY_META},
    {"id": "DR187-006", "category": "daily_high_ruin_risk",
     "description": "Daily report + Monte Carlo ruin > 20% → BLOCKED report grade", **_SAFETY_META},
    {"id": "DR187-007", "category": "daily_low_cash",
     "description": "Daily report + cash reserve < 5% → BLOCKED", **_SAFETY_META},
    {"id": "DR187-008", "category": "daily_300k_stage",
     "description": "Daily 300K capital stage with 2 candidates → COMPLETE", **_SAFETY_META},
    {"id": "DR187-009", "category": "daily_500k_stage",
     "description": "Daily 500K capital stage + B breakout candidate → COMPLETE", **_SAFETY_META},
    {"id": "DR187-010", "category": "daily_mixed_candidates",
     "description": "Daily mixed: 1 ready + 1 watch + 1 blocked → REVIEW_REQUIRED", **_SAFETY_META},

    # ── Weekly Report Scenarios (10) ─────────────────────────────────────────
    {"id": "DR187-011", "category": "weekly_complete_report",
     "description": "Weekly complete report: BULL + portfolio healthy → COMPLETE", **_SAFETY_META},
    {"id": "DR187-012", "category": "weekly_rebalance_needed",
     "description": "Weekly report + concentration > 50% → rebalance_needed → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DR187-013", "category": "weekly_reduce_risk",
     "description": "Weekly REDUCE_RISK action → REVIEW_REQUIRED report grade", **_SAFETY_META},
    {"id": "DR187-014", "category": "weekly_blocked",
     "description": "Weekly BLOCKED cockpit grade → BLOCKED report", **_SAFETY_META},
    {"id": "DR187-015", "category": "weekly_no_trade",
     "description": "Weekly NO_TRADE day (holiday) → COMPLETE empty report", **_SAFETY_META},
    {"id": "DR187-016", "category": "weekly_high_exposure",
     "description": "Weekly total exposure > 70% → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DR187-017", "category": "weekly_portfolio_review",
     "description": "Weekly portfolio review: 3 holdings, diversified → COMPLETE", **_SAFETY_META},
    {"id": "DR187-018", "category": "weekly_1m_stage",
     "description": "Weekly 1M capital stage + 4 holdings review → COMPLETE", **_SAFETY_META},
    {"id": "DR187-019", "category": "weekly_3m_stage",
     "description": "Weekly 3M stage + 5 holdings, theme rotation → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DR187-020", "category": "weekly_drawdown_budget",
     "description": "Weekly drawdown budget usage 90% → REVIEW_REQUIRED", **_SAFETY_META},

    # ── Watchlist Report Scenarios (5) ───────────────────────────────────────
    {"id": "DR187-021", "category": "watchlist_only_report",
     "description": "Watchlist-only report: 5 candidates, 2 watch-ready → COMPLETE", **_SAFETY_META},
    {"id": "DR187-022", "category": "watchlist_empty",
     "description": "Watchlist empty → COMPLETE (valid empty watchlist report)", **_SAFETY_META},
    {"id": "DR187-023", "category": "watchlist_all_watch",
     "description": "Watchlist 10 candidates, all in WATCH state → COMPLETE", **_SAFETY_META},
    {"id": "DR187-024", "category": "watchlist_theme_rotation",
     "description": "Watchlist with theme rotation active → COMPLETE with rotation flag", **_SAFETY_META},
    {"id": "DR187-025", "category": "watchlist_regime_neutral",
     "description": "Watchlist under NEUTRAL regime → candidates adjusted → COMPLETE", **_SAFETY_META},

    # ── All Blocked Scenarios (5) ────────────────────────────────────────────
    {"id": "DR187-026", "category": "all_candidates_blocked_report",
     "description": "All 5 candidates blocked (regime) → report BLOCKED", **_SAFETY_META},
    {"id": "DR187-027", "category": "blocked_due_to_ruin_risk",
     "description": "All blocked: Monte Carlo ruin > 20% → BLOCKED", **_SAFETY_META},
    {"id": "DR187-028", "category": "blocked_due_to_cash",
     "description": "All blocked: cash reserve 2% → BLOCKED", **_SAFETY_META},
    {"id": "DR187-029", "category": "blocked_due_to_exposure",
     "description": "All blocked: exposure 98% → BLOCKED", **_SAFETY_META},
    {"id": "DR187-030", "category": "blocked_behavior_risk",
     "description": "All blocked: behavior_risk_blocked=True → BLOCKED", **_SAFETY_META},

    # ── Evidence Pack Scenarios (10) ─────────────────────────────────────────
    {"id": "DR187-031", "category": "partial_evidence_report_blocked",
     "description": "Evidence pack missing for paper entry candidate → BLOCKED gate", **_SAFETY_META},
    {"id": "DR187-032", "category": "missing_audit_trail_blocked",
     "description": "Missing audit trail → BLOCKED report grade", **_SAFETY_META},
    {"id": "DR187-033", "category": "blocked_candidate_without_reason_blocked",
     "description": "Blocked candidate with no block reason → BLOCKED + error", **_SAFETY_META},
    {"id": "DR187-034", "category": "paper_plan_ready_with_complete_evidence",
     "description": "2 paper-plan-ready candidates with full evidence → COMPLETE", **_SAFETY_META},
    {"id": "DR187-035", "category": "reduce_risk_with_risk_evidence",
     "description": "Reduce risk report with risk + portfolio + MC evidence → COMPLETE", **_SAFETY_META},
    {"id": "DR187-036", "category": "evidence_pack_12_fields",
     "description": "Evidence pack covering all 12 traceable fields → COMPLETE", **_SAFETY_META},
    {"id": "DR187-037", "category": "evidence_pack_empty_candidates",
     "description": "Evidence pack with 0 candidates → COMPLETE (empty valid)", **_SAFETY_META},
    {"id": "DR187-038", "category": "evidence_buy_point_a",
     "description": "BuyPointEvidence A_10MA_PULLBACK condition met → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DR187-039", "category": "evidence_buy_point_b",
     "description": "BuyPointEvidence B_BREAKOUT with volume breakout → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DR187-040", "category": "evidence_buy_point_c",
     "description": "BuyPointEvidence C_20MA_RECLAIM with KD recovering → PAPER_PLAN_READY", **_SAFETY_META},

    # ── Portfolio / Exposure Scenarios (5) ───────────────────────────────────
    {"id": "DR187-041", "category": "portfolio_exposure_report",
     "description": "Portfolio exposure report: 3 holdings, exposure 45% → COMPLETE", **_SAFETY_META},
    {"id": "DR187-042", "category": "high_concentration_evidence",
     "description": "Portfolio concentration score 75 → concentration blocked in evidence", **_SAFETY_META},
    {"id": "DR187-043", "category": "overexposed_theme",
     "description": "Single theme > 80% of exposure → concentration evidence flagged", **_SAFETY_META},
    {"id": "DR187-044", "category": "rebalance_required_evidence",
     "description": "Portfolio rebalance required → portfolio evidence reflects rebalance", **_SAFETY_META},
    {"id": "DR187-045", "category": "diversified_portfolio_evidence",
     "description": "Diversified portfolio: concentration 20%, 4 themes → COMPLETE", **_SAFETY_META},

    # ── Monte Carlo Scenarios (5) ────────────────────────────────────────────
    {"id": "DR187-046", "category": "monte_carlo_risk_report",
     "description": "MC report: ruin 3% → LOW risk → COMPLETE", **_SAFETY_META},
    {"id": "DR187-047", "category": "monte_carlo_medium_risk",
     "description": "MC evidence: ruin 12% → MEDIUM risk → add not allowed", **_SAFETY_META},
    {"id": "DR187-048", "category": "monte_carlo_high_risk",
     "description": "MC evidence: ruin 25% → HIGH risk → BLOCKED", **_SAFETY_META},
    {"id": "DR187-049", "category": "monte_carlo_low_medium_risk",
     "description": "MC evidence: ruin 7% → LOW_MEDIUM → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DR187-050", "category": "monte_carlo_zero_ruin",
     "description": "MC evidence: ruin 0% → LOW → all allowed → COMPLETE", **_SAFETY_META},

    # ── A/B/C Buy Point Report Scenarios (5) ─────────────────────────────────
    {"id": "DR187-051", "category": "abc_buy_point_report",
     "description": "A/B/C report: all 3 types present, 2 met → COMPLETE", **_SAFETY_META},
    {"id": "DR187-052", "category": "abc_a_met",
     "description": "A buy point met: above 10MA + contracting volume + KD low → ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DR187-053", "category": "abc_b_met",
     "description": "B buy point met: volume breakout + above both MAs → ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DR187-054", "category": "abc_c_met",
     "description": "C buy point met: 20MA reclaim + KD recovering → PLAN_READY", **_SAFETY_META},
    {"id": "DR187-055", "category": "abc_none_met",
     "description": "No buy point conditions met → all WAIT → COMPLETE", **_SAFETY_META},

    # ── Export Format Scenarios (5) ──────────────────────────────────────────
    {"id": "DR187-056", "category": "deterministic_json_export",
     "description": "JSON export: deterministic sort_keys=True, no wall clock → COMPLETE", **_SAFETY_META},
    {"id": "DR187-057", "category": "deterministic_markdown_export",
     "description": "Markdown export: deterministic sections, no forbidden words → COMPLETE", **_SAFETY_META},
    {"id": "DR187-058", "category": "deterministic_csv_rows_export",
     "description": "CSV rows export: deterministic field order, paper flags all true → COMPLETE", **_SAFETY_META},
    {"id": "DR187-059", "category": "console_summary_export",
     "description": "Console summary: compact 7-line output, no forbidden words → COMPLETE", **_SAFETY_META},
    {"id": "DR187-060", "category": "dashboard_payload_export",
     "description": "Dashboard payload: dict with all required keys, paper flags → COMPLETE", **_SAFETY_META},

    # ── Safety / Block Scenarios (5) ─────────────────────────────────────────
    {"id": "DR187-061", "category": "no_trade_day_report",
     "description": "No trade day (holiday) → WAIT action → COMPLETE report", **_SAFETY_META},
    {"id": "DR187-062", "category": "malformed_input_report_blocked",
     "description": "Malformed input (paper_only=False) → validation error → BLOCKED", **_SAFETY_META},
    {"id": "DR187-063", "category": "unsafe_output_path_blocked",
     "description": "Output path contains 'production_db' → safety gate blocked", **_SAFETY_META},
    {"id": "DR187-064", "category": "low_cash_reserve_evidence",
     "description": "Cash reserve 4% → evidence shows cash_reserve_status=BLOCKED", **_SAFETY_META},
    {"id": "DR187-065", "category": "market_regime_blocked_evidence",
     "description": "RISK_OFF regime → regime evidence shows regime_blocked=True", **_SAFETY_META},

    # ── Report Grade Scenarios (5) ───────────────────────────────────────────
    {"id": "DR187-066", "category": "report_grade_complete",
     "description": "All conditions clear → final_report_grade = COMPLETE", **_SAFETY_META},
    {"id": "DR187-067", "category": "report_grade_review_required",
     "description": "Block reasons present but not hard blocked → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DR187-068", "category": "report_grade_partial",
     "description": "Partial evidence available → PARTIAL report grade", **_SAFETY_META},
    {"id": "DR187-069", "category": "report_grade_blocked",
     "description": "Hard block condition triggered → BLOCKED report grade", **_SAFETY_META},
    {"id": "DR187-070", "category": "report_grade_invalid",
     "description": "Forbidden action in daily_action → INVALID report grade", **_SAFETY_META},

    # ── Backward Compatibility + Audit Trail Scenarios (5) ───────────────────
    {"id": "DR187-071", "category": "backward_compat_v170",
     "description": "v1.8.7 report generation backward compat with v1.7.0 baseline", **_SAFETY_META},
    {"id": "DR187-072", "category": "backward_compat_v186",
     "description": "v1.8.7 report wraps v1.8.6 cockpit result without modification", **_SAFETY_META},
    {"id": "DR187-073", "category": "audit_trail_complete",
     "description": "Full audit trail: regime + daily_action + cockpit_grade entries → COMPLETE", **_SAFETY_META},
    {"id": "DR187-074", "category": "audit_trail_with_blocks",
     "description": "Audit trail with 2 block entries + resolution guidance → COMPLETE", **_SAFETY_META},
    {"id": "DR187-075", "category": "report_health_gate_pass",
     "description": "Report health check all 60+ checks pass → gate PASS", **_SAFETY_META},
]

assert len(_SCENARIOS) == 75, f"Expected 75 scenarios, got {len(_SCENARIOS)}"


def count_scenarios() -> int:
    """Return number of scenarios."""
    return len(_SCENARIOS)


def get_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios."""
    return list(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return scenario by ID or empty dict."""
    for s in _SCENARIOS:
        if s["id"] == scenario_id:
            return dict(s)
    return {}


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return scenarios matching category."""
    return [dict(s) for s in _SCENARIOS if s.get("category") == category]


def get_scenario_ids() -> List[str]:
    """Return all scenario IDs."""
    return [s["id"] for s in _SCENARIOS]
