"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v205.py
v2.0.5 Paper Watchlist Rotation & Candidate Promotion Queue — Scenarios
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA = "205"
_PAPER_ONLY = True
_NO_REAL_ORDERS = True


def _s(n: int, name: str, category: str, expected: str, **kw) -> Dict[str, Any]:
    sid = f"PC205-{n:03d}"
    return {
        "id": sid,
        "scenario_id": sid,
        "schema_version": _SCHEMA,
        "paper_only": _PAPER_ONLY,
        "no_real_orders": _NO_REAL_ORDERS,
        "should_auto_apply": False,
        "name": name,
        "category": category,
        "expected_result": expected,
        **kw,
    }


SCENARIOS: List[Dict[str, Any]] = [
    # --- watchlist rotation engine (1-15) ---
    _s(1,  "watchlist_rotation_engine_basic",              "rotation",    "rotation_result_returned"),
    _s(2,  "watchlist_rotation_paper_only_flag",           "rotation",    "paper_only_true"),
    _s(3,  "watchlist_rotation_no_real_orders_flag",       "rotation",    "no_real_orders_true"),
    _s(4,  "watchlist_rotation_no_broker_flag",            "rotation",    "no_broker_true"),
    _s(5,  "watchlist_rotation_all_passed_flag",           "rotation",    "all_passed_true"),
    _s(6,  "watchlist_rotation_should_auto_apply_false",   "rotation",    "should_auto_apply_false"),
    _s(7,  "watchlist_rotation_rotation_id_generated",     "rotation",    "rotation_id_not_empty"),
    _s(8,  "watchlist_rotation_version_205",               "rotation",    "rotation_version_2.0.5"),
    _s(9,  "watchlist_rotation_period_set",                "rotation",    "rotation_period_set"),
    _s(10, "watchlist_rotation_queue_summary_built",       "rotation",    "queue_summary_not_none"),
    _s(11, "watchlist_rotation_multiple_items",            "rotation",    "handles_multiple_items"),
    _s(12, "watchlist_rotation_empty_watchlist",           "rotation",    "handles_empty_watchlist"),
    _s(13, "watchlist_rotation_single_item",               "rotation",    "handles_single_item"),
    _s(14, "watchlist_rotation_input_snapshot_set",        "rotation",    "input_snapshot_not_empty"),
    _s(15, "watchlist_rotation_paper_safety_snapshot",     "rotation",    "paper_safety_snapshot_true"),
    # --- watchlist item schema (16-25) ---
    _s(16, "watchlist_item_schema_basic",                  "schema",      "item_created"),
    _s(17, "watchlist_item_symbol_field",                  "schema",      "symbol_field_exists"),
    _s(18, "watchlist_item_status_active_watchlist",       "schema",      "status_active_watchlist"),
    _s(19, "watchlist_item_status_promoted_candidate",     "schema",      "status_promoted_candidate"),
    _s(20, "watchlist_item_status_quarantined_no_entry",   "schema",      "status_quarantined_no_entry"),
    _s(21, "watchlist_item_score_field",                   "schema",      "score_field_exists"),
    _s(22, "watchlist_item_trend_quality_field",           "schema",      "trend_quality_field_exists"),
    _s(23, "watchlist_item_no_entry_reasons_field",        "schema",      "no_entry_reasons_list"),
    _s(24, "watchlist_item_promotion_reasons_field",       "schema",      "promotion_reasons_list"),
    _s(25, "watchlist_item_next_review_action_field",      "schema",      "next_review_action_field_exists"),
    # --- promotion decision schema (26-35) ---
    _s(26, "promotion_decision_schema_basic",              "schema",      "decision_created"),
    _s(27, "promotion_decision_should_auto_apply_false",   "schema",      "should_auto_apply_false"),
    _s(28, "promotion_decision_force_false_even_if_true",  "schema",      "force_false_via_post_init"),
    _s(29, "promotion_decision_symbol_field",              "schema",      "symbol_field_exists"),
    _s(30, "promotion_decision_from_status_field",         "schema",      "from_status_field_exists"),
    _s(31, "promotion_decision_to_status_field",           "schema",      "to_status_field_exists"),
    _s(32, "promotion_decision_promotion_score_field",     "schema",      "promotion_score_field"),
    _s(33, "promotion_decision_risk_score_field",          "schema",      "risk_score_field"),
    _s(34, "promotion_decision_requires_human_review",     "schema",      "requires_human_review_field"),
    _s(35, "promotion_decision_blocked_reasons_field",     "schema",      "blocked_reasons_list"),
    # --- queue summary (36-42) ---
    _s(36, "queue_summary_schema_basic",                   "schema",      "summary_created"),
    _s(37, "queue_summary_total_count_field",              "schema",      "total_watchlist_count_field"),
    _s(38, "queue_summary_promote_count_field",            "schema",      "promote_count_field"),
    _s(39, "queue_summary_weekly_rotation_grade_field",    "schema",      "weekly_rotation_grade_field"),
    _s(40, "queue_summary_top_promo_candidates_field",     "schema",      "top_promotion_candidates_list"),
    _s(41, "queue_summary_top_quarantine_reasons_field",   "schema",      "top_quarantine_reasons_list"),
    _s(42, "queue_summary_avg_promotion_score_field",      "schema",      "avg_promotion_score_field"),
    # --- keep / promote / demote / remove logic (43-50) ---
    _s(43, "keep_logic_low_score_no_demotion_reasons",     "logic",       "item_kept"),
    _s(44, "promote_logic_high_score_no_entry_reasons",    "logic",       "item_promoted"),
    _s(45, "demote_logic_low_score_with_demotion_reasons", "logic",       "item_demoted"),
    _s(46, "remove_logic_very_low_score",                  "logic",       "item_removed"),
    _s(47, "quarantine_logic_3_no_entry_reasons",          "logic",       "item_quarantined"),
    _s(48, "human_review_logic_has_review_reasons",        "logic",       "item_human_review"),
    _s(49, "promote_score_threshold_75",                   "logic",       "score_75_triggers_promote"),
    _s(50, "keep_score_threshold_middle_range",            "logic",       "middle_range_keeps"),
    # --- no-entry quarantine logic (51-55) ---
    _s(51, "quarantine_3_no_entry_reasons",                "quarantine",  "quarantined_no_entry"),
    _s(52, "quarantine_human_review_takes_priority",       "quarantine",  "human_review_before_quarantine"),
    _s(53, "quarantine_paper_only_safety",                 "quarantine",  "quarantine_paper_only"),
    _s(54, "quarantine_no_real_orders",                    "quarantine",  "quarantine_no_real_orders"),
    _s(55, "quarantine_status_quarantined_no_entry",       "quarantine",  "status_set_correctly"),
    # --- risk-budget-aware promotion (56-60) ---
    _s(56, "risk_budget_aware_promotion_basic",            "risk",        "risk_budget_affects_promotion"),
    _s(57, "risk_budget_penalty_reduces_score",            "risk",        "risk_penalty_applied"),
    _s(58, "risk_budget_zero_prevents_promote",            "risk",        "zero_budget_prevents_promote"),
    _s(59, "risk_budget_high_allows_promote",              "risk",        "high_budget_allows_promote"),
    _s(60, "risk_budget_score_in_decision",                "risk",        "risk_score_in_decision"),
    # --- strategy-profile-aware promotion (61-63) ---
    _s(61, "strategy_profile_aware_promotion_basic",       "strategy",    "profile_id_affects_result"),
    _s(62, "strategy_profile_in_rotation_input",           "strategy",    "profile_id_stored"),
    _s(63, "strategy_profile_no_real_orders",              "strategy",    "no_real_orders_true"),
    # --- simulation-ranking-aware promotion (64-66) ---
    _s(64, "simulation_ranking_aware_promotion_basic",     "simulation",  "ranking_ids_stored"),
    _s(65, "simulation_ranking_snapshot_set",              "simulation",  "simulation_snapshot_set"),
    _s(66, "simulation_ranking_no_real_orders",            "simulation",  "no_real_orders_true"),
    # --- export integration (67-72) ---
    _s(67, "export_json_valid",                            "export",      "is_valid_true"),
    _s(68, "export_markdown_valid",                        "export",      "is_valid_true"),
    _s(69, "export_promotion_csv_valid",                   "export",      "is_valid_true"),
    _s(70, "export_demotion_csv_valid",                    "export",      "is_valid_true"),
    _s(71, "export_audit_snapshot_valid",                  "export",      "audit_snapshot_created"),
    _s(72, "export_paper_only_confirmed",                  "export",      "paper_only_confirmed_true"),
    # --- weekly improvement pack integration (73-74) ---
    _s(73, "weekly_improvement_pack_v204_still_works",     "compat",      "v204_pack_callable"),
    _s(74, "weekly_improvement_pack_auto_apply_false",     "compat",      "should_auto_apply_false"),
    # --- backward compat with v2.0.4 (75-76) ---
    _s(75, "backward_compat_v204_run_portfolio_review",    "compat",      "v204_callable"),
    _s(76, "backward_compat_v204_version_unchanged",       "compat",      "v204_version_2.0.4"),
    # --- paper-only safety (77-78) ---
    _s(77, "paper_only_safety_no_broker",                  "safety",      "no_broker_flag_true"),
    _s(78, "paper_only_safety_no_auto_rebalance",          "safety",      "no_automatic_rebalance_true"),
    # --- health / gate (79-80) ---
    _s(79, "health_check_all_passed",                      "health",      "all_passed_true"),
    _s(80, "release_gate_gate_passed",                     "gate",        "gate_passed_true"),
]

assert len(SCENARIOS) == 80, f"Expected 80 scenarios, got {len(SCENARIOS)}"
