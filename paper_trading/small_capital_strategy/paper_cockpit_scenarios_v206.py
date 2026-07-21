"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v206.py
v2.0.6 Paper Candidate Lifecycle & Setup Aging Control — Scenarios
[!] Paper Only. Research Only. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "206"

SCENARIOS: List[Dict[str, Any]] = [
    # --- 1-10: basic lifecycle states ---
    {"scenario_id": "SC206-001", "schema_version": "206", "paper_only": True, "description": "Newly promoted candidate enters pool", "lifecycle_state": "newly_promoted", "days_in_pool": 1, "expected_action": "keep_active"},
    {"scenario_id": "SC206-002", "schema_version": "206", "paper_only": True, "description": "Active candidate within fresh bucket", "lifecycle_state": "active_candidate", "days_in_pool": 3, "expected_action": "keep_active"},
    {"scenario_id": "SC206-003", "schema_version": "206", "paper_only": True, "description": "Candidate waiting for buy point", "lifecycle_state": "waiting_buy_point", "days_in_pool": 10, "expected_action": "keep_waiting"},
    {"scenario_id": "SC206-004", "schema_version": "206", "paper_only": True, "description": "Second wave candidate waiting", "lifecycle_state": "second_wave_waiting", "days_in_pool": 8, "expected_action": "keep_waiting"},
    {"scenario_id": "SC206-005", "schema_version": "206", "paper_only": True, "description": "ABC pullback candidate waiting", "lifecycle_state": "abc_pullback_waiting", "days_in_pool": 12, "expected_action": "keep_waiting"},
    {"scenario_id": "SC206-006", "schema_version": "206", "paper_only": True, "description": "Breakout candidate waiting", "lifecycle_state": "breakout_waiting", "days_in_pool": 9, "expected_action": "keep_waiting"},
    {"scenario_id": "SC206-007", "schema_version": "206", "paper_only": True, "description": "Candidate entering cooldown", "lifecycle_state": "cooling_down", "days_in_pool": 20, "expected_action": "move_to_cooldown"},
    {"scenario_id": "SC206-008", "schema_version": "206", "paper_only": True, "description": "Stale setup detected", "lifecycle_state": "stale_setup", "days_in_pool": 35, "expected_action": "require_rescore"},
    {"scenario_id": "SC206-009", "schema_version": "206", "paper_only": True, "description": "Expired candidate detected", "lifecycle_state": "expired_candidate", "days_in_pool": 70, "expected_action": "require_human_review"},
    {"scenario_id": "SC206-010", "schema_version": "206", "paper_only": True, "description": "Rescore required triggered", "lifecycle_state": "rescore_required", "days_in_pool": 28, "expected_action": "require_rescore"},
    # --- 11-20: aging bucket boundaries ---
    {"scenario_id": "SC206-011", "schema_version": "206", "paper_only": True, "description": "Fresh bucket boundary (day 5)", "days_in_pool": 5, "expected_bucket": "fresh"},
    {"scenario_id": "SC206-012", "schema_version": "206", "paper_only": True, "description": "Normal bucket entry (day 6)", "days_in_pool": 6, "expected_bucket": "normal"},
    {"scenario_id": "SC206-013", "schema_version": "206", "paper_only": True, "description": "Normal bucket boundary (day 14)", "days_in_pool": 14, "expected_bucket": "normal"},
    {"scenario_id": "SC206-014", "schema_version": "206", "paper_only": True, "description": "Aging bucket entry (day 15)", "days_in_pool": 15, "expected_bucket": "aging"},
    {"scenario_id": "SC206-015", "schema_version": "206", "paper_only": True, "description": "Aging bucket boundary (day 30)", "days_in_pool": 30, "expected_bucket": "aging"},
    {"scenario_id": "SC206-016", "schema_version": "206", "paper_only": True, "description": "Stale bucket entry (day 31)", "days_in_pool": 31, "expected_bucket": "stale"},
    {"scenario_id": "SC206-017", "schema_version": "206", "paper_only": True, "description": "Stale bucket boundary (day 60)", "days_in_pool": 60, "expected_bucket": "stale"},
    {"scenario_id": "SC206-018", "schema_version": "206", "paper_only": True, "description": "Expired bucket entry (day 61)", "days_in_pool": 61, "expected_bucket": "expired"},
    {"scenario_id": "SC206-019", "schema_version": "206", "paper_only": True, "description": "Zero days fresh bucket", "days_in_pool": 0, "expected_bucket": "fresh"},
    {"scenario_id": "SC206-020", "schema_version": "206", "paper_only": True, "description": "Very long wait (day 120)", "days_in_pool": 120, "expected_bucket": "expired"},
    # --- 21-30: signal aging ---
    {"scenario_id": "SC206-021", "schema_version": "206", "paper_only": True, "description": "Signal fresh (day 1)", "days_since_signal": 1, "expected_signal_bucket": "fresh"},
    {"scenario_id": "SC206-022", "schema_version": "206", "paper_only": True, "description": "Signal fresh boundary (day 3)", "days_since_signal": 3, "expected_signal_bucket": "fresh"},
    {"scenario_id": "SC206-023", "schema_version": "206", "paper_only": True, "description": "Signal normal entry (day 4)", "days_since_signal": 4, "expected_signal_bucket": "normal"},
    {"scenario_id": "SC206-024", "schema_version": "206", "paper_only": True, "description": "Signal normal boundary (day 7)", "days_since_signal": 7, "expected_signal_bucket": "normal"},
    {"scenario_id": "SC206-025", "schema_version": "206", "paper_only": True, "description": "Signal aging entry (day 8)", "days_since_signal": 8, "expected_signal_bucket": "aging"},
    {"scenario_id": "SC206-026", "schema_version": "206", "paper_only": True, "description": "Signal stale boundary (day 14)", "days_since_signal": 14, "expected_signal_bucket": "stale"},
    {"scenario_id": "SC206-027", "schema_version": "206", "paper_only": True, "description": "Signal expired (day 15)", "days_since_signal": 15, "expected_signal_bucket": "expired"},
    {"scenario_id": "SC206-028", "schema_version": "206", "paper_only": True, "description": "No signal refresh for 20 days", "days_since_signal": 20, "expected_action": "remove_from_candidate_pool"},
    {"scenario_id": "SC206-029", "schema_version": "206", "paper_only": True, "description": "Signal refreshed today", "days_since_signal": 0, "expected_signal_bucket": "fresh"},
    {"scenario_id": "SC206-030", "schema_version": "206", "paper_only": True, "description": "Signal half policy threshold", "days_since_signal": 7, "expected_signal_bucket": "normal"},
    # --- 31-40: score update aging ---
    {"scenario_id": "SC206-031", "schema_version": "206", "paper_only": True, "description": "Score fresh (day 0)", "days_since_score_update": 0, "expected_theme_bucket": "fresh"},
    {"scenario_id": "SC206-032", "schema_version": "206", "paper_only": True, "description": "Score normal (day 7)", "days_since_score_update": 7, "expected_theme_bucket": "normal"},
    {"scenario_id": "SC206-033", "schema_version": "206", "paper_only": True, "description": "Score aging (day 11)", "days_since_score_update": 11, "expected_theme_bucket": "aging"},
    {"scenario_id": "SC206-034", "schema_version": "206", "paper_only": True, "description": "Score stale (day 21)", "days_since_score_update": 21, "expected_theme_bucket": "stale"},
    {"scenario_id": "SC206-035", "schema_version": "206", "paper_only": True, "description": "Score expired (day 25)", "days_since_score_update": 25, "expected_theme_bucket": "expired"},
    {"scenario_id": "SC206-036", "schema_version": "206", "paper_only": True, "description": "Score update triggers rescore", "days_since_score_update": 22, "expected_action": "require_rescore"},
    {"scenario_id": "SC206-037", "schema_version": "206", "paper_only": True, "description": "Score fresh after rescore", "days_since_score_update": 2, "expected_theme_bucket": "fresh"},
    {"scenario_id": "SC206-038", "schema_version": "206", "paper_only": True, "description": "Score boundary day 3", "days_since_score_update": 3, "expected_theme_bucket": "fresh"},
    {"scenario_id": "SC206-039", "schema_version": "206", "paper_only": True, "description": "Score boundary day 10", "days_since_score_update": 10, "expected_theme_bucket": "aging"},
    {"scenario_id": "SC206-040", "schema_version": "206", "paper_only": True, "description": "Score boundary day 4", "days_since_score_update": 4, "expected_theme_bucket": "normal"},
    # --- 41-50: downgrade/remove logic ---
    {"scenario_id": "SC206-041", "schema_version": "206", "paper_only": True, "description": "Candidate downgraded to watchlist", "downgrade_reasons": ["weak_volume"], "expected_action": "downgrade_to_watchlist"},
    {"scenario_id": "SC206-042", "schema_version": "206", "paper_only": True, "description": "Candidate removed from pool", "days_in_pool": 65, "expected_action": "require_human_review"},
    {"scenario_id": "SC206-043", "schema_version": "206", "paper_only": True, "description": "Multiple downgrade reasons", "downgrade_reasons": ["weak_volume", "no_theme_support"], "expected_action": "downgrade_to_watchlist"},
    {"scenario_id": "SC206-044", "schema_version": "206", "paper_only": True, "description": "Human review required before remove", "require_human_review_before_remove": True, "days_in_pool": 70},
    {"scenario_id": "SC206-045", "schema_version": "206", "paper_only": True, "description": "Auto remove when no human review gate", "require_human_review_before_remove": False, "days_in_pool": 70},
    {"scenario_id": "SC206-046", "schema_version": "206", "paper_only": True, "description": "Cooldown period respected", "lifecycle_state": "cooling_down", "cooldown_days": 14},
    {"scenario_id": "SC206-047", "schema_version": "206", "paper_only": True, "description": "Rescore triggers after stale score", "stale_score_threshold": 40.0, "current_score": 35.0},
    {"scenario_id": "SC206-048", "schema_version": "206", "paper_only": True, "description": "Remove below remove threshold", "remove_score_threshold": 20.0, "current_score": 15.0},
    {"scenario_id": "SC206-049", "schema_version": "206", "paper_only": True, "description": "Human review with stale + downgrade reasons"},
    {"scenario_id": "SC206-050", "schema_version": "206", "paper_only": True, "description": "Max days active candidate exceeded", "days_in_pool": 61, "max_days_active": 60},
    # --- 51-60: export integration ---
    {"scenario_id": "SC206-051", "schema_version": "206", "paper_only": True, "description": "JSON export contains lifecycle_review_id", "export_format": "json"},
    {"scenario_id": "SC206-052", "schema_version": "206", "paper_only": True, "description": "JSON export has paper_only=true", "export_format": "json"},
    {"scenario_id": "SC206-053", "schema_version": "206", "paper_only": True, "description": "JSON export has should_auto_apply=false", "export_format": "json"},
    {"scenario_id": "SC206-054", "schema_version": "206", "paper_only": True, "description": "Markdown report header present", "export_format": "markdown"},
    {"scenario_id": "SC206-055", "schema_version": "206", "paper_only": True, "description": "Markdown includes Paper Only disclaimer", "export_format": "markdown"},
    {"scenario_id": "SC206-056", "schema_version": "206", "paper_only": True, "description": "Stale setup CSV header correct", "export_format": "csv"},
    {"scenario_id": "SC206-057", "schema_version": "206", "paper_only": True, "description": "Expired candidate CSV has rows", "export_format": "csv"},
    {"scenario_id": "SC206-058", "schema_version": "206", "paper_only": True, "description": "Action CSV has should_auto_apply=False column", "export_format": "csv"},
    {"scenario_id": "SC206-059", "schema_version": "206", "paper_only": True, "description": "Audit snapshot reproducibility_hash set", "export_format": "audit_snapshot"},
    {"scenario_id": "SC206-060", "schema_version": "206", "paper_only": True, "description": "Audit snapshot safety_snapshot contains paper_only", "export_format": "audit_snapshot"},
    # --- 61-70: safety flags ---
    {"scenario_id": "SC206-061", "schema_version": "206", "paper_only": True, "description": "should_auto_apply always False on LifecycleAction"},
    {"scenario_id": "SC206-062", "schema_version": "206", "paper_only": True, "description": "auto_apply_enabled always False on SetupAgingPolicy"},
    {"scenario_id": "SC206-063", "schema_version": "206", "paper_only": True, "description": "LifecycleReviewResult should_auto_apply always False"},
    {"scenario_id": "SC206-064", "schema_version": "206", "paper_only": True, "description": "NO_REAL_ORDERS constant True"},
    {"scenario_id": "SC206-065", "schema_version": "206", "paper_only": True, "description": "BROKER_EXECUTION_ENABLED constant False"},
    {"scenario_id": "SC206-066", "schema_version": "206", "paper_only": True, "description": "PRODUCTION_TRADING_BLOCKED constant True"},
    {"scenario_id": "SC206-067", "schema_version": "206", "paper_only": True, "description": "Safety flags count 20"},
    {"scenario_id": "SC206-068", "schema_version": "206", "paper_only": True, "description": "No broker connection in lifecycle engine"},
    {"scenario_id": "SC206-069", "schema_version": "206", "paper_only": True, "description": "No automatic lifecycle action applied"},
    {"scenario_id": "SC206-070", "schema_version": "206", "paper_only": True, "description": "Human review required before any state change"},
    # --- 71-80: backward compatibility and summary ---
    {"scenario_id": "SC206-071", "schema_version": "206", "paper_only": True, "description": "v2.0.5 watchlist rotation still importable"},
    {"scenario_id": "SC206-072", "schema_version": "206", "paper_only": True, "description": "v2.0.5 run_watchlist_rotation callable"},
    {"scenario_id": "SC206-073", "schema_version": "206", "paper_only": True, "description": "v2.0.4 portfolio review callable"},
    {"scenario_id": "SC206-074", "schema_version": "206", "paper_only": True, "description": "Lifecycle summary grade A when avg pool < 10 days"},
    {"scenario_id": "SC206-075", "schema_version": "206", "paper_only": True, "description": "Lifecycle summary grade D when avg pool > 35 days"},
    {"scenario_id": "SC206-076", "schema_version": "206", "paper_only": True, "description": "Lifecycle quality grade reflects pool freshness"},
    {"scenario_id": "SC206-077", "schema_version": "206", "paper_only": True, "description": "Top stale reasons aggregated correctly"},
    {"scenario_id": "SC206-078", "schema_version": "206", "paper_only": True, "description": "Top remove reasons aggregated correctly"},
    {"scenario_id": "SC206-079", "schema_version": "206", "paper_only": True, "description": "GUI render_all_tabs has no error tabs"},
    {"scenario_id": "SC206-080", "schema_version": "206", "paper_only": True, "description": "CLI commands all registered in command_registry"},
]

assert len(SCENARIOS) == 80, f"Expected 80 scenarios, got {len(SCENARIOS)}"
assert all(s["schema_version"] == "206" for s in SCENARIOS)
assert all(s["paper_only"] is True for s in SCENARIOS)
