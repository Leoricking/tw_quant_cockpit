"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v206.py
v2.0.6 Paper Candidate Lifecycle & Setup Aging Control — Fixtures
[!] Paper Only. Research Only. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "206"

FIXTURES: List[Dict[str, Any]] = [
    # --- 1-10: basic candidate items ---
    {"fixture_id": "FX206-001", "schema_version": "206", "paper_only": True, "symbol": "2330", "name": "台積電", "candidate_id": "CAND-2330-001", "lifecycle_state": "newly_promoted", "days_in_pool": 1, "days_since_signal": 0, "days_since_score_update": 0, "setup_type": "breakout"},
    {"fixture_id": "FX206-002", "schema_version": "206", "paper_only": True, "symbol": "2317", "name": "鴻海", "candidate_id": "CAND-2317-001", "lifecycle_state": "active_candidate", "days_in_pool": 5, "days_since_signal": 2, "days_since_score_update": 3, "setup_type": "abc_pullback"},
    {"fixture_id": "FX206-003", "schema_version": "206", "paper_only": True, "symbol": "2454", "name": "聯發科", "candidate_id": "CAND-2454-001", "lifecycle_state": "waiting_buy_point", "days_in_pool": 12, "days_since_signal": 5, "days_since_score_update": 7, "setup_type": "10ma_pullback"},
    {"fixture_id": "FX206-004", "schema_version": "206", "paper_only": True, "symbol": "2308", "name": "台達電", "candidate_id": "CAND-2308-001", "lifecycle_state": "second_wave_waiting", "days_in_pool": 8, "days_since_signal": 3, "days_since_score_update": 4, "setup_type": "second_wave"},
    {"fixture_id": "FX206-005", "schema_version": "206", "paper_only": True, "symbol": "3711", "name": "日月光", "candidate_id": "CAND-3711-001", "lifecycle_state": "abc_pullback_waiting", "days_in_pool": 10, "days_since_signal": 4, "days_since_score_update": 5, "setup_type": "abc_pullback"},
    {"fixture_id": "FX206-006", "schema_version": "206", "paper_only": True, "symbol": "2382", "name": "廣達", "candidate_id": "CAND-2382-001", "lifecycle_state": "breakout_waiting", "days_in_pool": 7, "days_since_signal": 2, "days_since_score_update": 3, "setup_type": "breakout"},
    {"fixture_id": "FX206-007", "schema_version": "206", "paper_only": True, "symbol": "2303", "name": "聯電", "candidate_id": "CAND-2303-001", "lifecycle_state": "cooling_down", "days_in_pool": 20, "days_since_signal": 8, "days_since_score_update": 10, "setup_type": "none"},
    {"fixture_id": "FX206-008", "schema_version": "206", "paper_only": True, "symbol": "2412", "name": "中華電", "candidate_id": "CAND-2412-001", "lifecycle_state": "stale_setup", "days_in_pool": 35, "days_since_signal": 15, "days_since_score_update": 20, "setup_type": "none", "stale_reasons": ["old_breakout", "no_volume_refresh"]},
    {"fixture_id": "FX206-009", "schema_version": "206", "paper_only": True, "symbol": "2409", "name": "友達", "candidate_id": "CAND-2409-001", "lifecycle_state": "expired_candidate", "days_in_pool": 70, "days_since_signal": 30, "days_since_score_update": 35, "setup_type": "none", "remove_reasons": ["pool_max_exceeded"]},
    {"fixture_id": "FX206-010", "schema_version": "206", "paper_only": True, "symbol": "2357", "name": "華碩", "candidate_id": "CAND-2357-001", "lifecycle_state": "rescore_required", "days_in_pool": 28, "days_since_signal": 14, "days_since_score_update": 21, "setup_type": "abc_pullback"},
    # --- 11-20: aging policy fixtures ---
    {"fixture_id": "FX206-011", "schema_version": "206", "paper_only": True, "policy_id": "default_aging_policy_v206", "max_days_active_candidate": 60, "max_days_waiting_buy_point": 30, "max_days_without_signal_refresh": 14, "max_days_without_score_update": 21, "stale_score_threshold": 40.0, "remove_score_threshold": 20.0, "cooldown_days": 14, "require_human_review_before_remove": True, "auto_apply_enabled": False},
    {"fixture_id": "FX206-012", "schema_version": "206", "paper_only": True, "policy_id": "strict_aging_policy", "max_days_active_candidate": 30, "max_days_waiting_buy_point": 14, "max_days_without_signal_refresh": 7, "max_days_without_score_update": 10, "stale_score_threshold": 50.0, "remove_score_threshold": 30.0, "cooldown_days": 7, "require_human_review_before_remove": True, "auto_apply_enabled": False},
    {"fixture_id": "FX206-013", "schema_version": "206", "paper_only": True, "policy_id": "lenient_aging_policy", "max_days_active_candidate": 90, "max_days_waiting_buy_point": 45, "max_days_without_signal_refresh": 21, "max_days_without_score_update": 30, "stale_score_threshold": 30.0, "remove_score_threshold": 15.0, "cooldown_days": 21, "require_human_review_before_remove": True, "auto_apply_enabled": False},
    {"fixture_id": "FX206-014", "schema_version": "206", "paper_only": True, "policy_id": "aggressive_removal_policy", "max_days_active_candidate": 20, "max_days_waiting_buy_point": 10, "max_days_without_signal_refresh": 5, "max_days_without_score_update": 7, "stale_score_threshold": 60.0, "remove_score_threshold": 40.0, "cooldown_days": 5, "require_human_review_before_remove": False, "auto_apply_enabled": False},
    {"fixture_id": "FX206-015", "schema_version": "206", "paper_only": True, "policy_id": "balanced_policy", "max_days_active_candidate": 45, "max_days_waiting_buy_point": 21, "max_days_without_signal_refresh": 10, "max_days_without_score_update": 14, "stale_score_threshold": 45.0, "remove_score_threshold": 25.0, "cooldown_days": 10, "require_human_review_before_remove": True, "auto_apply_enabled": False},
    # --- 16-25: lifecycle action fixtures ---
    {"fixture_id": "FX206-016", "schema_version": "206", "paper_only": True, "action_type": "keep_active", "from_state": "active_candidate", "to_state": "active_candidate", "should_auto_apply": False},
    {"fixture_id": "FX206-017", "schema_version": "206", "paper_only": True, "action_type": "keep_waiting", "from_state": "waiting_buy_point", "to_state": "waiting_buy_point", "should_auto_apply": False},
    {"fixture_id": "FX206-018", "schema_version": "206", "paper_only": True, "action_type": "move_to_cooldown", "from_state": "active_candidate", "to_state": "cooling_down", "should_auto_apply": False},
    {"fixture_id": "FX206-019", "schema_version": "206", "paper_only": True, "action_type": "mark_stale", "from_state": "active_candidate", "to_state": "stale_setup", "should_auto_apply": False},
    {"fixture_id": "FX206-020", "schema_version": "206", "paper_only": True, "action_type": "require_rescore", "from_state": "stale_setup", "to_state": "rescore_required", "should_auto_apply": False},
    {"fixture_id": "FX206-021", "schema_version": "206", "paper_only": True, "action_type": "downgrade_to_watchlist", "from_state": "active_candidate", "to_state": "downgraded_to_watchlist", "should_auto_apply": False},
    {"fixture_id": "FX206-022", "schema_version": "206", "paper_only": True, "action_type": "remove_from_candidate_pool", "from_state": "expired_candidate", "to_state": "removed_from_pool", "should_auto_apply": False},
    {"fixture_id": "FX206-023", "schema_version": "206", "paper_only": True, "action_type": "require_human_review", "from_state": "expired_candidate", "to_state": "human_review_required", "should_auto_apply": False},
    {"fixture_id": "FX206-024", "schema_version": "206", "paper_only": True, "action_type": "keep_active", "from_state": "newly_promoted", "to_state": "active_candidate", "should_auto_apply": False},
    {"fixture_id": "FX206-025", "schema_version": "206", "paper_only": True, "action_type": "keep_waiting", "from_state": "abc_pullback_waiting", "to_state": "abc_pullback_waiting", "should_auto_apply": False},
    # --- 26-35: lifecycle summary fixtures ---
    {"fixture_id": "FX206-026", "schema_version": "206", "paper_only": True, "total_candidate_count": 10, "active_count": 4, "waiting_count": 3, "cooling_down_count": 1, "stale_count": 1, "expired_count": 1, "lifecycle_quality_grade": "A"},
    {"fixture_id": "FX206-027", "schema_version": "206", "paper_only": True, "total_candidate_count": 20, "active_count": 5, "waiting_count": 8, "cooling_down_count": 2, "stale_count": 3, "expired_count": 2, "lifecycle_quality_grade": "B"},
    {"fixture_id": "FX206-028", "schema_version": "206", "paper_only": True, "total_candidate_count": 5, "active_count": 2, "waiting_count": 1, "cooling_down_count": 0, "stale_count": 1, "expired_count": 1, "lifecycle_quality_grade": "D"},
    {"fixture_id": "FX206-029", "schema_version": "206", "paper_only": True, "avg_days_in_candidate_pool": 5.0, "expected_grade": "A"},
    {"fixture_id": "FX206-030", "schema_version": "206", "paper_only": True, "avg_days_in_candidate_pool": 15.0, "expected_grade": "B"},
    {"fixture_id": "FX206-031", "schema_version": "206", "paper_only": True, "avg_days_in_candidate_pool": 25.0, "expected_grade": "C"},
    {"fixture_id": "FX206-032", "schema_version": "206", "paper_only": True, "avg_days_in_candidate_pool": 40.0, "expected_grade": "D"},
    {"fixture_id": "FX206-033", "schema_version": "206", "paper_only": True, "top_stale_reasons": ["old_breakout", "no_volume_refresh", "theme_faded"], "top_remove_reasons": ["pool_max_exceeded"]},
    {"fixture_id": "FX206-034", "schema_version": "206", "paper_only": True, "rescore_required_count": 2, "human_review_count": 1, "downgrade_count": 1, "remove_count": 0},
    {"fixture_id": "FX206-035", "schema_version": "206", "paper_only": True, "lifecycle_quality_grade": "C", "avg_days_in_candidate_pool": 28.0, "avg_days_since_last_signal": 9.0},
    # --- 36-45: export fixtures ---
    {"fixture_id": "FX206-036", "schema_version": "206", "paper_only": True, "export_format": "json", "is_valid": True, "export_status": "complete", "paper_only_confirmed": True},
    {"fixture_id": "FX206-037", "schema_version": "206", "paper_only": True, "export_format": "markdown", "is_valid": True, "export_status": "complete", "paper_only_confirmed": True},
    {"fixture_id": "FX206-038", "schema_version": "206", "paper_only": True, "export_format": "csv", "is_valid": True, "export_status": "complete", "paper_only_confirmed": True},
    {"fixture_id": "FX206-039", "schema_version": "206", "paper_only": True, "export_format": "audit_snapshot", "is_valid": True, "export_status": "complete", "paper_only_confirmed": True},
    {"fixture_id": "FX206-040", "schema_version": "206", "paper_only": True, "stale_csv_header": "symbol,current_lifecycle_state,days_in_candidate_pool,setup_age_bucket,should_auto_apply"},
    {"fixture_id": "FX206-041", "schema_version": "206", "paper_only": True, "expired_csv_header": "symbol,current_lifecycle_state,days_in_candidate_pool,signal_age_bucket,should_auto_apply"},
    {"fixture_id": "FX206-042", "schema_version": "206", "paper_only": True, "action_csv_header": "symbol,from_state,to_state,action_type,age_score,should_auto_apply"},
    {"fixture_id": "FX206-043", "schema_version": "206", "paper_only": True, "json_key": "lifecycle_review_id", "expected_present": True},
    {"fixture_id": "FX206-044", "schema_version": "206", "paper_only": True, "json_key": "should_auto_apply", "expected_value": "false"},
    {"fixture_id": "FX206-045", "schema_version": "206", "paper_only": True, "md_section": "Lifecycle Summary", "expected_present": True},
    # --- 46-55: safety fixtures ---
    {"fixture_id": "FX206-046", "schema_version": "206", "paper_only": True, "flag": "NO_REAL_ORDERS", "expected_value": True},
    {"fixture_id": "FX206-047", "schema_version": "206", "paper_only": True, "flag": "BROKER_EXECUTION_ENABLED", "expected_value": False},
    {"fixture_id": "FX206-048", "schema_version": "206", "paper_only": True, "flag": "PRODUCTION_TRADING_BLOCKED", "expected_value": True},
    {"fixture_id": "FX206-049", "schema_version": "206", "paper_only": True, "flag": "should_auto_apply_always_false", "expected_value": True},
    {"fixture_id": "FX206-050", "schema_version": "206", "paper_only": True, "flag": "auto_apply_enabled_always_false", "expected_value": True},
    {"fixture_id": "FX206-051", "schema_version": "206", "paper_only": True, "flag": "broker_execution_disabled", "expected_value": True},
    {"fixture_id": "FX206-052", "schema_version": "206", "paper_only": True, "flag": "production_trading_blocked", "expected_value": True},
    {"fixture_id": "FX206-053", "schema_version": "206", "paper_only": True, "flag": "no_automatic_rebalance", "expected_value": True},
    {"fixture_id": "FX206-054", "schema_version": "206", "paper_only": True, "flag": "no_real_account_sync", "expected_value": True},
    {"fixture_id": "FX206-055", "schema_version": "206", "paper_only": True, "safety_flags_count": 20},
    # --- 56-65: CLI fixtures ---
    {"fixture_id": "FX206-056", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-review-lifecycle"},
    {"fixture_id": "FX206-057", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-evaluate-aging"},
    {"fixture_id": "FX206-058", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-build-stale-queue"},
    {"fixture_id": "FX206-059", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-build-expired-queue"},
    {"fixture_id": "FX206-060", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-build-rescore-queue"},
    {"fixture_id": "FX206-061", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-build-cooldown-queue"},
    {"fixture_id": "FX206-062", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-export-json"},
    {"fixture_id": "FX206-063", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-export-md"},
    {"fixture_id": "FX206-064", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-export-csv"},
    {"fixture_id": "FX206-065", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-health"},
    # --- 66-70: more CLI and GUI ---
    {"fixture_id": "FX206-066", "schema_version": "206", "paper_only": True, "cli_command": "paper-cockpit-v206-gate"},
    {"fixture_id": "FX206-067", "schema_version": "206", "paper_only": True, "gui_tab": "candidate_lifecycle_v206"},
    {"fixture_id": "FX206-068", "schema_version": "206", "paper_only": True, "gui_tab": "setup_aging_v206"},
    {"fixture_id": "FX206-069", "schema_version": "206", "paper_only": True, "gui_tab": "stale_candidate_queue_v206"},
    {"fixture_id": "FX206-070", "schema_version": "206", "paper_only": True, "gui_tab_count": 3, "expected_error_count": 0},
    # --- 71-80: boundary and backward compat ---
    {"fixture_id": "FX206-071", "schema_version": "206", "paper_only": True, "description": "Lifecycle states count 13"},
    {"fixture_id": "FX206-072", "schema_version": "206", "paper_only": True, "description": "Aging buckets count 5"},
    {"fixture_id": "FX206-073", "schema_version": "206", "paper_only": True, "description": "Action types count 8"},
    {"fixture_id": "FX206-074", "schema_version": "206", "paper_only": True, "description": "Model count 13"},
    {"fixture_id": "FX206-075", "schema_version": "206", "paper_only": True, "description": "v2.0.5 VERSION unchanged"},
    {"fixture_id": "FX206-076", "schema_version": "206", "paper_only": True, "description": "v2.0.5 run_watchlist_rotation callable"},
    {"fixture_id": "FX206-077", "schema_version": "206", "paper_only": True, "description": "v201 health file exists via relative path"},
    {"fixture_id": "FX206-078", "schema_version": "206", "paper_only": True, "description": "80 scenarios with schema_version 206"},
    {"fixture_id": "FX206-079", "schema_version": "206", "paper_only": True, "description": "Health check all_passed True"},
    {"fixture_id": "FX206-080", "schema_version": "206", "paper_only": True, "description": "Gate check gate_passed True"},
]

assert len(FIXTURES) == 80, f"Expected 80 fixtures, got {len(FIXTURES)}"
assert all(f["schema_version"] == "206" for f in FIXTURES)
assert all(f["paper_only"] is True for f in FIXTURES)
assert all("fixture_id" in f for f in FIXTURES)
