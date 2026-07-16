"""
paper_trading/small_capital_strategy/decision_journal_scenarios_v189.py
Scenarios for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Optional

_SAFETY = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, decision_only=True, journal_only=True,
    review_only=True, report_only=True, audit_only=True,
    no_real_orders=True, no_broker=True, no_margin=True, no_leverage=True,
    not_investment_advice=True, demo_only=True,
    not_for_production=True, production_trading_blocked=True,
)

_SCENARIOS: List[Dict] = [
    # 1. complete daily journal
    {"id": "DJ189-001", "name": "complete_daily_journal_bull", "scenario_type": "complete_daily_journal",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 30.0, **_SAFETY},

    # 2. complete weekly review
    {"id": "DJ189-002", "name": "complete_weekly_review_bull", "scenario_type": "complete_weekly_review",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 40.0, **_SAFETY},

    # 3. empty journal
    {"id": "DJ189-003", "name": "empty_journal_no_entries", "scenario_type": "empty_journal",
     "market_regime": "BULL", "entry_state": "", "expected_grade": "ACCEPTABLE",
     "has_evidence": False, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},

    # 4. malformed journal entry
    {"id": "DJ189-004", "name": "malformed_journal_entry_missing_state", "scenario_type": "malformed_journal_entry",
     "market_regime": "BULL", "entry_state": "INVALID_STATE", "expected_grade": "INVALID",
     "expected_blocked": True, "block_reason": "malformed_journal_entry",
     "has_evidence": False, "has_workflow_id": False, "total_exposure_pct": 0.0, **_SAFETY},

    # 5. paper plan ready reviewed
    {"id": "DJ189-005", "name": "paper_plan_ready_reviewed", "scenario_type": "paper_plan_ready_reviewed",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 15.0,
     "symbol": "TSMC", "rationale": "A-point breakout with strong relative strength", **_SAFETY},

    # 6. paper entry allowed reviewed
    {"id": "DJ189-006", "name": "paper_entry_allowed_reviewed", "scenario_type": "paper_entry_allowed_reviewed",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0,
     "symbol": "MEDIATEK", "rationale": "B-point confirmed with volume", **_SAFETY},

    # 7. reduce risk reviewed
    {"id": "DJ189-007", "name": "reduce_risk_reviewed", "scenario_type": "reduce_risk_reviewed",
     "market_regime": "WATCH", "entry_state": "REDUCE_RISK", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 60.0,
     "rationale": "Market regime shifted to WATCH, reducing exposure", **_SAFETY},

    # 8. blocked decision reviewed
    {"id": "DJ189-008", "name": "blocked_decision_reviewed", "scenario_type": "blocked_decision_reviewed",
     "market_regime": "BEAR", "entry_state": "BLOCKED", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0,
     "block_reason": "market_regime_bear_blocked", **_SAFETY},

    # 9. no trade day reviewed
    {"id": "DJ189-009", "name": "no_trade_day_reviewed", "scenario_type": "no_trade_day_reviewed",
     "market_regime": "WATCH", "entry_state": "NO_TRADE", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0,
     "rationale": "No qualifying setups found", **_SAFETY},

    # 10. missing evidence blocked
    {"id": "DJ189-010", "name": "missing_evidence_blocked", "scenario_type": "missing_evidence_blocked",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "expected_blocked": False, "has_evidence": False, "has_workflow_id": True,
     "total_exposure_pct": 20.0, **_SAFETY},

    # 11. unsafe export blocked
    {"id": "DJ189-011", "name": "unsafe_export_blocked", "scenario_type": "unsafe_export_blocked",
     "market_regime": "BULL", "entry_state": "REPORT_ONLY", "expected_grade": "INVALID",
     "expected_blocked": True, "block_reason": "unsafe_export_path",
     "has_evidence": True, "has_workflow_id": True, "export_path": "production_db/exports",
     "total_exposure_pct": 0.0, **_SAFETY},

    # 12. over concentration finding
    {"id": "DJ189-012", "name": "over_concentration_finding", "scenario_type": "over_concentration_finding",
     "market_regime": "BULL", "entry_state": "REDUCE_RISK", "expected_grade": "REVIEW_REQUIRED",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 85.0,
     "expected_finding": "OVER_CONCENTRATION", **_SAFETY},

    # 13. low cash reserve finding
    {"id": "DJ189-013", "name": "low_cash_reserve_finding", "scenario_type": "low_cash_reserve_finding",
     "market_regime": "BULL", "entry_state": "OBSERVE", "expected_grade": "REVIEW_REQUIRED",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 92.0,
     "cash_reserve_pct": 8.0, "expected_finding": "LOW_CASH_RESERVE", **_SAFETY},

    # 14. chase high mistake
    {"id": "DJ189-014", "name": "chase_high_mistake", "scenario_type": "chase_high_mistake",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "has_evidence": False, "has_workflow_id": True, "total_exposure_pct": 25.0,
     "expected_mistake_tag": "CHASE_HIGH", "planned_size_pct": 30.0, **_SAFETY},

    # 15. early entry mistake
    {"id": "DJ189-015", "name": "early_entry_mistake", "scenario_type": "early_entry_mistake",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "has_evidence": False, "has_workflow_id": True, "total_exposure_pct": 10.0,
     "expected_mistake_tag": "ENTER_TOO_EARLY", **_SAFETY},

    # 16. ignored market regime mistake
    {"id": "DJ189-016", "name": "ignored_market_regime_mistake", "scenario_type": "ignored_market_regime_mistake",
     "market_regime": "BEAR", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0,
     "expected_mistake_tag": "IGNORE_MARKET_REGIME", **_SAFETY},

    # 17. ignored block reason mistake
    {"id": "DJ189-017", "name": "ignored_block_reason_mistake", "scenario_type": "ignored_block_reason_mistake",
     "market_regime": "BULL", "entry_state": "BLOCKED", "expected_grade": "POOR",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 10.0,
     "block_reason": "", "expected_mistake_tag": "IGNORE_BLOCK_REASON", **_SAFETY},

    # 18. no mistake found
    {"id": "DJ189-018", "name": "no_mistake_found_excellent", "scenario_type": "no_mistake_found",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "EXCELLENT",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0,
     "expected_mistake_tag": "NO_MISTAKE_FOUND", **_SAFETY},

    # 19. excellent quality score
    {"id": "DJ189-019", "name": "excellent_quality_score", "scenario_type": "excellent_quality_score",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "EXCELLENT",
     "expected_quality_score_min": 0.85, "has_evidence": True, "has_workflow_id": True,
     "total_exposure_pct": 20.0, "stop_loss_pct": 7.0, "take_profit_pct": 20.0,
     "rationale": "Perfect setup with all evidence and risk controls", **_SAFETY},

    # 20. poor quality score
    {"id": "DJ189-020", "name": "poor_quality_score", "scenario_type": "poor_quality_score",
     "market_regime": "BEAR", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "expected_quality_score_max": 0.4, "has_evidence": False, "has_workflow_id": False,
     "total_exposure_pct": 90.0, **_SAFETY},

    # 21-30: OBSERVE and WAIT state scenarios
    {"id": "DJ189-021", "name": "observe_bull_market", "scenario_type": "observe_state",
     "market_regime": "BULL", "entry_state": "OBSERVE", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-022", "name": "wait_watch_market", "scenario_type": "wait_state",
     "market_regime": "WATCH", "entry_state": "WAIT", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 10.0, **_SAFETY},
    {"id": "DJ189-023", "name": "observe_bear_market", "scenario_type": "observe_state",
     "market_regime": "BEAR", "entry_state": "OBSERVE", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-024", "name": "wait_blocked_market", "scenario_type": "wait_state",
     "market_regime": "BLOCKED", "entry_state": "WAIT", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-025", "name": "observe_risk_off", "scenario_type": "observe_state",
     "market_regime": "RISK_OFF", "entry_state": "OBSERVE", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 5.0, **_SAFETY},

    # 26-30: Research/Simulation/Validation/Decision/Report/Audit Only states
    {"id": "DJ189-026", "name": "research_only_state", "scenario_type": "research_only",
     "market_regime": "BULL", "entry_state": "RESEARCH_ONLY", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-027", "name": "simulate_only_state", "scenario_type": "simulate_only",
     "market_regime": "BULL", "entry_state": "SIMULATE_ONLY", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-028", "name": "validation_only_state", "scenario_type": "validation_only",
     "market_regime": "BULL", "entry_state": "VALIDATION_ONLY", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-029", "name": "decision_only_state", "scenario_type": "decision_only",
     "market_regime": "BULL", "entry_state": "DECISION_ONLY", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-030", "name": "report_only_state", "scenario_type": "report_only",
     "market_regime": "BULL", "entry_state": "REPORT_ONLY", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},

    # 31-40: Mistake tag scenarios
    {"id": "DJ189-031", "name": "mistake_oversize_position", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "planned_size_pct": 35.0, "expected_mistake_tag": "OVERSIZE_POSITION",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 35.0, **_SAFETY},
    {"id": "DJ189-032", "name": "mistake_over_concentration", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "REVIEW_REQUIRED",
     "planned_size_pct": 10.0, "expected_mistake_tag": "OVER_CONCENTRATION",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 88.0, **_SAFETY},
    {"id": "DJ189-033", "name": "mistake_missing_evidence", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "expected_mistake_tag": "MISSING_EVIDENCE", "has_evidence": False, "has_workflow_id": True,
     "total_exposure_pct": 15.0, **_SAFETY},
    {"id": "DJ189-034", "name": "mistake_no_clear_stop", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "stop_loss_pct": 0.0, "expected_mistake_tag": "NO_CLEAR_STOP",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 15.0, **_SAFETY},
    {"id": "DJ189-035", "name": "mistake_no_clear_take_profit", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "take_profit_pct": 0.0, "stop_loss_pct": 7.0, "expected_mistake_tag": "NO_CLEAR_TAKE_PROFIT",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 15.0, **_SAFETY},
    {"id": "DJ189-036", "name": "mistake_low_cash_reserve", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "OBSERVE", "expected_grade": "REVIEW_REQUIRED",
     "expected_mistake_tag": "LOW_CASH_RESERVE", "has_evidence": True, "has_workflow_id": True,
     "cash_reserve_pct": 5.0, "total_exposure_pct": 95.0, **_SAFETY},
    {"id": "DJ189-037", "name": "mistake_plan_not_followed", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "expected_mistake_tag": "MISSING_EVIDENCE", "has_evidence": False, "has_workflow_id": True,
     "total_exposure_pct": 20.0, "rationale": "", **_SAFETY},
    {"id": "DJ189-038", "name": "mistake_late_second_wave", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "expected_mistake_tag": "MISSING_EVIDENCE", "has_evidence": False, "has_workflow_id": True,
     "total_exposure_pct": 25.0, **_SAFETY},
    {"id": "DJ189-039", "name": "mistake_weak_theme", "scenario_type": "mistake_tag",
     "market_regime": "WATCH", "entry_state": "PAPER_PLAN_READY", "expected_grade": "ACCEPTABLE",
     "expected_mistake_tag": "NO_MISTAKE_FOUND", "has_evidence": True, "has_workflow_id": True,
     "total_exposure_pct": 10.0, "theme": "WEAK_SECTOR", **_SAFETY},
    {"id": "DJ189-040", "name": "mistake_ignore_volume_risk", "scenario_type": "mistake_tag",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "expected_mistake_tag": "MISSING_EVIDENCE", "has_evidence": False, "has_workflow_id": True,
     "total_exposure_pct": 20.0, **_SAFETY},

    # 41-50: Quality grade scenarios
    {"id": "DJ189-041", "name": "grade_excellent_all_signals", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "EXCELLENT",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 15.0,
     "stop_loss_pct": 7.0, "take_profit_pct": 21.0, "planned_size_pct": 10.0,
     "rationale": "Full evidence, strong regime, ABC point confirmed", **_SAFETY},
    {"id": "DJ189-042", "name": "grade_good_minor_warning", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 30.0,
     "stop_loss_pct": 7.0, "take_profit_pct": 15.0, "planned_size_pct": 12.0, **_SAFETY},
    {"id": "DJ189-043", "name": "grade_acceptable_watch_regime", "scenario_type": "quality_grade",
     "market_regime": "WATCH", "entry_state": "OBSERVE", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0, **_SAFETY},
    {"id": "DJ189-044", "name": "grade_review_required_high_exposure", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "REDUCE_RISK", "expected_grade": "REVIEW_REQUIRED",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 82.0, **_SAFETY},
    {"id": "DJ189-045", "name": "grade_poor_bear_entry", "scenario_type": "quality_grade",
     "market_regime": "BEAR", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "has_evidence": False, "has_workflow_id": False, "total_exposure_pct": 25.0, **_SAFETY},
    {"id": "DJ189-046", "name": "grade_invalid_missing_flags", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "INVALID_STATE", "expected_grade": "INVALID",
     "has_evidence": False, "has_workflow_id": False, "total_exposure_pct": 0.0,
     "expected_blocked": True, **_SAFETY},
    {"id": "DJ189-047", "name": "grade_poor_no_stop_or_target", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "POOR",
     "stop_loss_pct": 0.0, "take_profit_pct": 0.0, "has_evidence": False, "has_workflow_id": True,
     "total_exposure_pct": 20.0, **_SAFETY},
    {"id": "DJ189-048", "name": "grade_acceptable_reduce_risk", "scenario_type": "quality_grade",
     "market_regime": "WATCH", "entry_state": "REDUCE_RISK", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 50.0, **_SAFETY},
    {"id": "DJ189-049", "name": "grade_good_add_allowed", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "PAPER_ADD_ALLOWED", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0,
     "stop_loss_pct": 7.0, "take_profit_pct": 21.0, "rationale": "Pyramid into confirmed winner", **_SAFETY},
    {"id": "DJ189-050", "name": "grade_excellent_decision_only", "scenario_type": "quality_grade",
     "market_regime": "BULL", "entry_state": "DECISION_ONLY", "expected_grade": "EXCELLENT",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0,
     "rationale": "Decision reviewed with full evidence", **_SAFETY},

    # 51-60: Weekly review scenarios
    {"id": "DJ189-051", "name": "weekly_review_3_days_bull", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "day_count": 3, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 25.0, **_SAFETY},
    {"id": "DJ189-052", "name": "weekly_review_5_days_mixed", "scenario_type": "weekly_review",
     "market_regime": "WATCH", "entry_state": "OBSERVE", "expected_grade": "ACCEPTABLE",
     "day_count": 5, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 30.0, **_SAFETY},
    {"id": "DJ189-053", "name": "weekly_review_recurring_mistakes", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "REVIEW_REQUIRED",
     "day_count": 5, "recurring_mistake_tag": "MISSING_EVIDENCE", "has_evidence": False,
     "has_workflow_id": True, "total_exposure_pct": 40.0, **_SAFETY},
    {"id": "DJ189-054", "name": "weekly_review_no_trades", "scenario_type": "weekly_review",
     "market_regime": "BEAR", "entry_state": "NO_TRADE", "expected_grade": "ACCEPTABLE",
     "day_count": 5, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-055", "name": "weekly_review_high_quality", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "EXCELLENT",
     "day_count": 3, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0,
     "stop_loss_pct": 7.0, "take_profit_pct": 21.0, **_SAFETY},
    {"id": "DJ189-056", "name": "weekly_review_risk_budget_exceeded", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "REDUCE_RISK", "expected_grade": "REVIEW_REQUIRED",
     "day_count": 5, "risk_budget_usage_pct": 95.0, "has_evidence": True, "has_workflow_id": True,
     "total_exposure_pct": 80.0, **_SAFETY},
    {"id": "DJ189-057", "name": "weekly_review_blocked_market", "scenario_type": "weekly_review",
     "market_regime": "BLOCKED", "entry_state": "BLOCKED", "expected_grade": "ACCEPTABLE",
     "day_count": 5, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-058", "name": "weekly_review_watch_then_bull", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "day_count": 5, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 15.0, **_SAFETY},
    {"id": "DJ189-059", "name": "weekly_review_concentrate_risk", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED", "expected_grade": "REVIEW_REQUIRED",
     "day_count": 5, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 85.0,
     "expected_finding": "OVER_CONCENTRATION", **_SAFETY},
    {"id": "DJ189-060", "name": "weekly_review_low_cash", "scenario_type": "weekly_review",
     "market_regime": "BULL", "entry_state": "OBSERVE", "expected_grade": "REVIEW_REQUIRED",
     "day_count": 5, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 93.0,
     "cash_reserve_pct": 7.0, "expected_finding": "LOW_CASH_RESERVE", **_SAFETY},

    # 61-70: Audit and evidence scenarios
    {"id": "DJ189-061", "name": "audit_trail_complete", "scenario_type": "audit_trail",
     "market_regime": "BULL", "entry_state": "DECISION_ONLY", "expected_grade": "EXCELLENT",
     "has_evidence": True, "has_workflow_id": True, "audit_complete": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-062", "name": "evidence_pack_complete", "scenario_type": "evidence_pack",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "evidence_count": 3, "total_exposure_pct": 15.0, **_SAFETY},
    {"id": "DJ189-063", "name": "journal_export_manifest_complete", "scenario_type": "export_manifest",
     "market_regime": "BULL", "entry_state": "REPORT_ONLY", "expected_grade": "ACCEPTABLE",
     "has_evidence": True, "has_workflow_id": True, "export_path": "reports/journal/",
     "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-064", "name": "lifecycle_observe_to_plan", "scenario_type": "lifecycle",
     "market_regime": "BULL", "entry_state": "PAPER_PLAN_READY", "expected_grade": "GOOD",
     "has_evidence": True, "has_workflow_id": True, "lifecycle_states": ["OBSERVE", "PAPER_PLAN_READY"],
     "total_exposure_pct": 10.0, **_SAFETY},
    {"id": "DJ189-065", "name": "lifecycle_plan_to_entry", "scenario_type": "lifecycle",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED",
     "lifecycle_states": ["OBSERVE", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED"],
     "expected_grade": "GOOD", "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 15.0, **_SAFETY},
    {"id": "DJ189-066", "name": "lifecycle_entry_to_reduce", "scenario_type": "lifecycle",
     "market_regime": "WATCH", "entry_state": "REDUCE_RISK",
     "lifecycle_states": ["PAPER_ENTRY_ALLOWED", "REDUCE_RISK"],
     "expected_grade": "ACCEPTABLE", "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 40.0, **_SAFETY},
    {"id": "DJ189-067", "name": "journal_checklist_complete", "scenario_type": "review_checklist",
     "market_regime": "BULL", "entry_state": "DECISION_ONLY", "expected_grade": "EXCELLENT",
     "has_evidence": True, "has_workflow_id": True, "checklist_complete": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-068", "name": "review_finding_high_severity", "scenario_type": "review_finding",
     "market_regime": "BULL", "entry_state": "REDUCE_RISK", "expected_grade": "REVIEW_REQUIRED",
     "has_evidence": True, "has_workflow_id": True, "finding_severity": "HIGH", "total_exposure_pct": 70.0, **_SAFETY},
    {"id": "DJ189-069", "name": "review_action_item_open", "scenario_type": "review_action_item",
     "market_regime": "BULL", "entry_state": "REVIEW_REQUIRED", "expected_grade": "REVIEW_REQUIRED",
     "has_evidence": True, "has_workflow_id": True, "action_open": True, "total_exposure_pct": 20.0, **_SAFETY},
    {"id": "DJ189-070", "name": "monthly_review_3_weeks", "scenario_type": "monthly_review",
     "market_regime": "BULL", "entry_state": "DECISION_ONLY", "expected_grade": "ACCEPTABLE",
     "week_count": 3, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 25.0, **_SAFETY},

    # 71-75: Safety and blocking scenarios
    {"id": "DJ189-071", "name": "safety_audit_all_safe", "scenario_type": "safety_audit",
     "market_regime": "BULL", "entry_state": "AUDIT_ONLY", "expected_grade": "EXCELLENT",
     "expected_all_safe": True, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0, **_SAFETY},
    {"id": "DJ189-072", "name": "block_missing_paper_only_flag", "scenario_type": "hard_block",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED",
     "expected_blocked": True, "block_reason": "missing_paper_only_flags",
     "missing_flag": "paper_only", "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 10.0,
     **{k: v for k, v in _SAFETY.items()}},
    {"id": "DJ189-073", "name": "block_missing_workflow_id", "scenario_type": "hard_block",
     "market_regime": "BULL", "entry_state": "PAPER_ENTRY_ALLOWED",
     "expected_blocked": True, "block_reason": "review_without_source_workflow_id",
     "has_evidence": True, "has_workflow_id": False, "total_exposure_pct": 10.0, **_SAFETY},
    {"id": "DJ189-074", "name": "block_forbidden_action_in_entry", "scenario_type": "hard_block",
     "market_regime": "BULL", "entry_state": "BLOCKED",
     "expected_blocked": True, "block_reason": "forbidden_action_words",
     "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 0.0,
     "forbidden_word_in_rationale": "BUY", **_SAFETY},
    {"id": "DJ189-075", "name": "complete_journal_with_monthly_review", "scenario_type": "monthly_review",
     "market_regime": "BULL", "entry_state": "DECISION_ONLY", "expected_grade": "GOOD",
     "week_count": 4, "has_evidence": True, "has_workflow_id": True, "total_exposure_pct": 20.0,
     "monthly_consistency_score_min": 0.7, **_SAFETY},
]

assert len(_SCENARIOS) == 75, f"Expected 75 scenarios, got {len(_SCENARIOS)}"


def get_scenarios() -> List[Dict]:
    """Return all 75 scenarios."""
    return list(_SCENARIOS)


def count_scenarios() -> int:
    """Return total scenario count."""
    return len(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Optional[Dict]:
    """Return scenario by ID, or None."""
    for s in _SCENARIOS:
        if s["id"] == scenario_id:
            return dict(s)
    return None


def get_scenarios_by_type(scenario_type: str) -> List[Dict]:
    """Return all scenarios of a given type."""
    return [dict(s) for s in _SCENARIOS if s.get("scenario_type") == scenario_type]


def get_scenario_ids() -> List[str]:
    """Return list of all scenario IDs."""
    return [s["id"] for s in _SCENARIOS]


def get_scenario_info() -> Dict:
    """Return scenario registry info."""
    return {
        "count": len(_SCENARIOS),
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
        "scenario_types": list(dict.fromkeys(s.get("scenario_type", "") for s in _SCENARIOS)),
    }
