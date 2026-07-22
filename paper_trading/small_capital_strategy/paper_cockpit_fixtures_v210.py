"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v210.py
v2.0.10 Paper Exit Plan & Stop-Loss Discipline Control — Fixtures
[!] Paper Only. Research Only. Exit Plan Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "210"

FIXTURES: List[Dict[str, Any]] = [
    # --- 1-10: base exit plan fixtures ---
    {"fixture_id": "FX210-001", "schema_version": "210", "paper_only": True, "name": "標準進場-台積電出場計畫", "symbol": "2330", "entry_price": 900.0, "stop_price": 855.0, "expected_stop_distance_pct": 0.05, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-002", "schema_version": "210", "paper_only": True, "name": "標準進場-聯發科出場計畫", "symbol": "2454", "entry_price": 1000.0, "stop_price": 940.0, "expected_stop_distance_pct": 0.06, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-003", "schema_version": "210", "paper_only": True, "name": "標準進場-廣達出場計畫", "symbol": "2382", "entry_price": 300.0, "stop_price": 282.0, "expected_stop_distance_pct": 0.06, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-004", "schema_version": "210", "paper_only": True, "name": "高波動進場-台達電縮減", "symbol": "2308", "entry_price": 400.0, "stop_price": 372.0, "is_high_volatility": True, "expected_exit_action": "reduce_size_before_entry", "should_auto_apply": False},
    {"fixture_id": "FX210-005", "schema_version": "210", "paper_only": True, "name": "低流動進場-聯電出場計畫", "symbol": "2303", "entry_price": 55.0, "stop_price": 51.0, "is_low_liquidity": True, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-006", "schema_version": "210", "paper_only": True, "name": "Aging候選-鴻海出場計畫", "symbol": "2317", "entry_price": 120.0, "stop_price": 112.0, "lifecycle_state": "aging", "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-007", "schema_version": "210", "paper_only": True, "name": "SEMI主題-日月光出場計畫", "symbol": "3711", "entry_price": 150.0, "stop_price": 141.0, "theme_id": "THEME-SEMI", "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-008", "schema_version": "210", "paper_only": True, "name": "高波動AI主題-緯穎縮減", "symbol": "6669", "entry_price": 2000.0, "stop_price": 1880.0, "is_high_volatility": True, "theme_id": "THEME-AI", "expected_exit_action": "reduce_size_before_entry", "should_auto_apply": False},
    {"fixture_id": "FX210-009", "schema_version": "210", "paper_only": True, "name": "零停損距離-阻擋進場", "symbol": "TEST-001", "entry_price": 100.0, "stop_price": 100.0, "expected_exit_action": "block_entry_missing_stop", "should_auto_apply": False},
    {"fixture_id": "FX210-010", "schema_version": "210", "paper_only": True, "name": "無效進場價-阻擋進場", "symbol": "TEST-002", "entry_price": 0.0, "stop_price": 0.0, "expected_exit_action": "block_entry_missing_stop", "should_auto_apply": False},
    # --- 11-20: exit plan policy fixtures ---
    {"fixture_id": "FX210-011", "schema_version": "210", "paper_only": True, "name": "預設出場計畫policy", "policy_id": "default-policy-v210", "default_stop_loss_pct": 0.06, "max_allowed_loss_pct": 0.08, "max_stop_distance_pct": 0.12, "min_reward_risk_ratio": 2.0, "auto_apply_enabled": False, "require_stop_loss_before_entry": True, "should_auto_apply": False},
    {"fixture_id": "FX210-012", "schema_version": "210", "paper_only": True, "name": "保守出場policy", "policy_id": "conservative-policy-v210", "default_stop_loss_pct": 0.05, "max_allowed_loss_pct": 0.06, "max_stop_distance_pct": 0.08, "min_reward_risk_ratio": 2.5, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX210-013", "schema_version": "210", "paper_only": True, "name": "積極出場policy", "policy_id": "aggressive-policy-v210", "default_stop_loss_pct": 0.08, "max_allowed_loss_pct": 0.10, "max_stop_distance_pct": 0.15, "min_reward_risk_ratio": 1.5, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX210-014", "schema_version": "210", "paper_only": True, "name": "policy.auto_apply強制False", "policy_id": "guard-test-v210", "input_auto_apply_enabled": True, "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX210-015", "schema_version": "210", "paper_only": True, "name": "policy.require_stop強制True", "policy_id": "guard-stop-v210", "input_require_stop": False, "expected_require_stop_loss_before_entry": True, "should_auto_apply": False},
    {"fixture_id": "FX210-016", "schema_version": "210", "paper_only": True, "name": "policy_time_stop=20天", "time_stop_days": 20, "expected_value": 20, "should_auto_apply": False},
    {"fixture_id": "FX210-017", "schema_version": "210", "paper_only": True, "name": "policy_gap_down=5%", "gap_down_exit_pct": 0.05, "expected_value": 0.05, "should_auto_apply": False},
    {"fixture_id": "FX210-018", "schema_version": "210", "paper_only": True, "name": "policy_failed_breakout=5天", "failed_breakout_days": 5, "expected_value": 5, "should_auto_apply": False},
    {"fixture_id": "FX210-019", "schema_version": "210", "paper_only": True, "name": "policy_trailing_stop_ma=20", "trailing_stop_ma": 20, "expected_value": 20, "should_auto_apply": False},
    {"fixture_id": "FX210-020", "schema_version": "210", "paper_only": True, "name": "policy_id唯一識別", "policy_id": "unique-id-v210-test", "expected_policy_id": "unique-id-v210-test", "should_auto_apply": False},
    # --- 21-30: candidate exit plan schema fixtures ---
    {"fixture_id": "FX210-021", "schema_version": "210", "paper_only": True, "name": "CandidateExitPlan預設建立", "expected_should_auto_apply": False, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-022", "schema_version": "210", "paper_only": True, "name": "should_auto_apply強制False", "input_should_auto_apply": True, "expected_should_auto_apply": False, "should_auto_apply": False},
    {"fixture_id": "FX210-023", "schema_version": "210", "paper_only": True, "name": "paper_only=True", "expected_paper_only": True, "should_auto_apply": False},
    {"fixture_id": "FX210-024", "schema_version": "210", "paper_only": True, "name": "no_real_orders=True", "expected_no_real_orders": True, "should_auto_apply": False},
    {"fixture_id": "FX210-025", "schema_version": "210", "paper_only": True, "name": "schema_version=210", "expected_schema_version": "210", "should_auto_apply": False},
    {"fixture_id": "FX210-026", "schema_version": "210", "paper_only": True, "name": "stop_loss_required=True", "expected_stop_loss_required": True, "should_auto_apply": False},
    {"fixture_id": "FX210-027", "schema_version": "210", "paper_only": True, "name": "reward_risk_ratio>=0", "expected_rr_ratio_min": 0.0, "should_auto_apply": False},
    {"fixture_id": "FX210-028", "schema_version": "210", "paper_only": True, "name": "first_take_profit_price>=entry", "entry_price": 100.0, "stop_price": 94.0, "expected_tp_ge_entry": True, "should_auto_apply": False},
    {"fixture_id": "FX210-029", "schema_version": "210", "paper_only": True, "name": "stop_distance_pct計算正確", "entry_price": 100.0, "stop_price": 94.0, "expected_stop_distance_pct": 0.06, "should_auto_apply": False},
    {"fixture_id": "FX210-030", "schema_version": "210", "paper_only": True, "name": "max_loss_amount計算正確", "account_equity": 300000.0, "max_loss_pct": 0.08, "expected_max_loss_amount": 24000.0, "should_auto_apply": False},
    # --- 31-40: exit action classification fixtures ---
    {"fixture_id": "FX210-031", "schema_version": "210", "paper_only": True, "name": "exit_action=allow_with_exit_plan", "entry_price": 100.0, "stop_price": 94.0, "market_state": "range_bound", "lifecycle_state": "active", "is_high_volatility": False, "expected_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"fixture_id": "FX210-032", "schema_version": "210", "paper_only": True, "name": "exit_action=require_tighter_stop", "entry_price": 100.0, "stop_price": 85.0, "expected_action": "require_tighter_stop", "should_auto_apply": False},
    {"fixture_id": "FX210-033", "schema_version": "210", "paper_only": True, "name": "exit_action=reduce_size_before_entry", "entry_price": 100.0, "stop_price": 94.0, "is_high_volatility": True, "expected_action": "reduce_size_before_entry", "should_auto_apply": False},
    {"fixture_id": "FX210-034", "schema_version": "210", "paper_only": True, "name": "exit_action=observation_only_riskoff", "market_state": "risk_off", "entry_price": 100.0, "stop_price": 94.0, "expected_action": "observation_only", "should_auto_apply": False},
    {"fixture_id": "FX210-035", "schema_version": "210", "paper_only": True, "name": "exit_action=block_entry_missing_stop", "entry_price": 100.0, "stop_price": 0.0, "expected_action": "block_entry_missing_stop", "should_auto_apply": False},
    {"fixture_id": "FX210-036", "schema_version": "210", "paper_only": True, "name": "exit_action=block_entry_bad_rr", "entry_price": 100.0, "stop_price": 99.0, "first_tp_price": 100.5, "expected_action": "block_entry_bad_reward_risk", "should_auto_apply": False},
    {"fixture_id": "FX210-037", "schema_version": "210", "paper_only": True, "name": "exit_action=human_review_required", "market_state": "downtrend", "entry_price": 100.0, "stop_price": 94.0, "expected_action": "human_review_required", "should_auto_apply": False},
    {"fixture_id": "FX210-038", "schema_version": "210", "paper_only": True, "name": "observation_only_lifecycle_expired", "lifecycle_state": "expired", "entry_price": 100.0, "stop_price": 94.0, "expected_action": "observation_only", "should_auto_apply": False},
    {"fixture_id": "FX210-039", "schema_version": "210", "paper_only": True, "name": "observation_only_lifecycle_cooldown", "lifecycle_state": "cooldown", "entry_price": 100.0, "stop_price": 94.0, "expected_action": "observation_only", "should_auto_apply": False},
    {"fixture_id": "FX210-040", "schema_version": "210", "paper_only": True, "name": "所有8種exit_action有效", "exit_actions": ["allow_with_exit_plan","require_tighter_stop","reduce_size_before_entry","observation_only","block_entry_missing_stop","block_entry_bad_reward_risk","require_rescore","human_review_required"], "expected_count": 8, "should_auto_apply": False},
    # --- 41-50: stop discipline summary fixtures ---
    {"fixture_id": "FX210-041", "schema_version": "210", "paper_only": True, "name": "StopDisciplineSummary預設建立", "expected_schema_version": "210", "expected_paper_only": True, "should_auto_apply": False},
    {"fixture_id": "FX210-042", "schema_version": "210", "paper_only": True, "name": "total_candidate_count=8", "total_candidate_count": 8, "expected_value": 8, "should_auto_apply": False},
    {"fixture_id": "FX210-043", "schema_version": "210", "paper_only": True, "name": "valid_exit_plan_count>=0", "expected_valid_count_min": 0, "should_auto_apply": False},
    {"fixture_id": "FX210-044", "schema_version": "210", "paper_only": True, "name": "exit_plan_quality_grade有效", "expected_grade_in": ["A","B","C","D","N/A"], "should_auto_apply": False},
    {"fixture_id": "FX210-045", "schema_version": "210", "paper_only": True, "name": "stop_discipline_quality_grade有效", "expected_grade_in": ["A","B","C","D","N/A"], "should_auto_apply": False},
    {"fixture_id": "FX210-046", "schema_version": "210", "paper_only": True, "name": "average_reward_risk_ratio>=0", "expected_avg_rr_min": 0.0, "should_auto_apply": False},
    {"fixture_id": "FX210-047", "schema_version": "210", "paper_only": True, "name": "lowest_reward_risk_candidates為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX210-048", "schema_version": "210", "paper_only": True, "name": "top_exit_risk_reasons為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX210-049", "schema_version": "210", "paper_only": True, "name": "blocked_entry_count>=0", "expected_blocked_min": 0, "should_auto_apply": False},
    {"fixture_id": "FX210-050", "schema_version": "210", "paper_only": True, "name": "missing_stop_count>=0", "expected_missing_min": 0, "should_auto_apply": False},
    # --- 51-60: exit review result fixtures ---
    {"fixture_id": "FX210-051", "schema_version": "210", "paper_only": True, "name": "ExitReviewResult預設建立", "expected_schema_version": "210", "expected_paper_only": True, "should_auto_apply": False},
    {"fixture_id": "FX210-052", "schema_version": "210", "paper_only": True, "name": "exit_version=2.0.10", "expected_exit_version": "2.0.10", "should_auto_apply": False},
    {"fixture_id": "FX210-053", "schema_version": "210", "paper_only": True, "name": "paper_only_safety_snapshot=True", "expected_safety_snapshot": True, "should_auto_apply": False},
    {"fixture_id": "FX210-054", "schema_version": "210", "paper_only": True, "name": "ExitReviewResult.should_auto_apply強制False", "input_should_auto_apply": True, "expected_should_auto_apply": False, "should_auto_apply": False},
    {"fixture_id": "FX210-055", "schema_version": "210", "paper_only": True, "name": "ExitReviewResult.auto_apply_enabled強制False", "input_auto_apply_enabled": True, "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX210-056", "schema_version": "210", "paper_only": True, "name": "exit_plan_snapshot為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX210-057", "schema_version": "210", "paper_only": True, "name": "stop_loss_snapshot為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX210-058", "schema_version": "210", "paper_only": True, "name": "take_profit_snapshot為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX210-059", "schema_version": "210", "paper_only": True, "name": "exit_warning_queue為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX210-060", "schema_version": "210", "paper_only": True, "name": "stop_discipline_violation_queue為清單", "expected_type": "list", "should_auto_apply": False},
    # --- 61-70: export result fixtures ---
    {"fixture_id": "FX210-061", "schema_version": "210", "paper_only": True, "name": "ExitExportResult_json有效", "export_format": "json", "expected_is_valid": True, "should_auto_apply": False},
    {"fixture_id": "FX210-062", "schema_version": "210", "paper_only": True, "name": "ExitExportResult_markdown有效", "export_format": "markdown", "expected_is_valid": True, "should_auto_apply": False},
    {"fixture_id": "FX210-063", "schema_version": "210", "paper_only": True, "name": "CandidateExitCSV有效", "expected_is_valid": True, "expected_row_count_min": 0, "should_auto_apply": False},
    {"fixture_id": "FX210-064", "schema_version": "210", "paper_only": True, "name": "StopDisciplineCSV有效", "expected_is_valid": True, "should_auto_apply": False},
    {"fixture_id": "FX210-065", "schema_version": "210", "paper_only": True, "name": "ExitWarningCSV有效", "expected_is_valid": True, "should_auto_apply": False},
    {"fixture_id": "FX210-066", "schema_version": "210", "paper_only": True, "name": "ExitAuditSnapshot稽核快照", "expected_export_status": "complete", "should_auto_apply": False},
    {"fixture_id": "FX210-067", "schema_version": "210", "paper_only": True, "name": "JSON內容含paper_only", "expected_json_key": "paper_only", "should_auto_apply": False},
    {"fixture_id": "FX210-068", "schema_version": "210", "paper_only": True, "name": "Markdown含警告聲明", "expected_md_contains": "Paper Only", "should_auto_apply": False},
    {"fixture_id": "FX210-069", "schema_version": "210", "paper_only": True, "name": "CSV含should_auto_apply欄位", "expected_csv_col": "should_auto_apply", "should_auto_apply": False},
    {"fixture_id": "FX210-070", "schema_version": "210", "paper_only": True, "name": "稽核快照含再現性哈希", "expected_hash_field": "reproducibility_hash", "should_auto_apply": False},
    # --- 71-80: v2.0.9 backward compat and safety fixtures ---
    {"fixture_id": "FX210-071", "schema_version": "210", "paper_only": True, "name": "v2.0.9 run_sizing_review不受影響", "integration_v209": True, "expected_v209_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX210-072", "schema_version": "210", "paper_only": True, "name": "v2.0.8 run_exposure_review不受影響", "integration_v208": True, "expected_v208_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX210-073", "schema_version": "210", "paper_only": True, "name": "v2.0.7 market_regime不受影響", "integration_v207": True, "expected_v207_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX210-074", "schema_version": "210", "paper_only": True, "name": "v2.0.6 candidate_lifecycle不受影響", "integration_v206": True, "expected_v206_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX210-075", "schema_version": "210", "paper_only": True, "name": "v2.0.5 watchlist_rotation不受影響", "integration_v205": True, "expected_v205_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX210-076", "schema_version": "210", "paper_only": True, "name": "SAFETY_FLAGS_V210包含所有必要旗標", "expected_flag_count": 23, "required_flags": ["paper_only", "no_real_orders", "should_auto_apply_always_false", "auto_apply_enabled_always_false", "require_stop_loss_before_entry_always_true"], "should_auto_apply": False},
    {"fixture_id": "FX210-077", "schema_version": "210", "paper_only": True, "name": "模型數量14個", "expected_model_count": 14, "should_auto_apply": False},
    {"fixture_id": "FX210-078", "schema_version": "210", "paper_only": True, "name": "CLI命令數量10個", "expected_cli_count": 10, "should_auto_apply": False},
    {"fixture_id": "FX210-079", "schema_version": "210", "paper_only": True, "name": "GUI標籤數量3個", "expected_gui_tab_count": 3, "should_auto_apply": False},
    {"fixture_id": "FX210-080", "schema_version": "210", "paper_only": True, "name": "v201健康相對路徑相容", "v201_health_compat": True, "expected_path_exists": True, "should_auto_apply": False},
]

assert len(FIXTURES) == 80, f"Expected 80 fixtures, got {len(FIXTURES)}"
assert all(f["schema_version"] == "210" for f in FIXTURES), "All fixtures must have schema_version='210'"
assert all(f["paper_only"] is True for f in FIXTURES), "All fixtures must have paper_only=True"
assert all("fixture_id" in f for f in FIXTURES), "All fixtures must have fixture_id"
assert all(f["should_auto_apply"] is False for f in FIXTURES), "All fixtures must have should_auto_apply=False"
