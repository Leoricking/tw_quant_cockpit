"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v209.py
v2.0.9 Paper Position Sizing & Risk Budget Control — Fixtures
[!] Paper Only. Research Only. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "209"

FIXTURES: List[Dict[str, Any]] = [
    # --- 1-10: base sizing fixtures ---
    {"fixture_id": "FX209-001", "schema_version": "209", "paper_only": True, "name": "標準進場-台積電", "symbol": "2330", "entry_price": 900.0, "stop_price": 855.0, "account_equity": 300000.0, "max_single_trade_risk_pct": 0.01, "expected_stop_distance_pct": 0.05, "expected_base_size_twd": 60000, "should_auto_apply": False},
    {"fixture_id": "FX209-002", "schema_version": "209", "paper_only": True, "name": "標準進場-聯發科", "symbol": "2454", "entry_price": 1000.0, "stop_price": 940.0, "account_equity": 300000.0, "max_single_trade_risk_pct": 0.01, "expected_stop_distance_pct": 0.06, "expected_base_size_twd": 50000, "should_auto_apply": False},
    {"fixture_id": "FX209-003", "schema_version": "209", "paper_only": True, "name": "標準進場-廣達", "symbol": "2382", "entry_price": 300.0, "stop_price": 282.0, "account_equity": 300000.0, "max_single_trade_risk_pct": 0.01, "expected_stop_distance_pct": 0.06, "expected_base_size_twd": 50000, "should_auto_apply": False},
    {"fixture_id": "FX209-004", "schema_version": "209", "paper_only": True, "name": "高波動進場-台達電", "symbol": "2308", "entry_price": 400.0, "stop_price": 372.0, "is_high_volatility": True, "expected_volatility_factor": 0.75, "should_auto_apply": False},
    {"fixture_id": "FX209-005", "schema_version": "209", "paper_only": True, "name": "低流動進場-聯電", "symbol": "2303", "entry_price": 55.0, "stop_price": 51.0, "is_low_liquidity": True, "expected_liquidity_factor": 0.60, "should_auto_apply": False},
    {"fixture_id": "FX209-006", "schema_version": "209", "paper_only": True, "name": "Aging候選-鴻海", "symbol": "2317", "entry_price": 120.0, "stop_price": 112.0, "lifecycle_state": "aging", "expected_lifecycle_factor": 0.80, "should_auto_apply": False},
    {"fixture_id": "FX209-007", "schema_version": "209", "paper_only": True, "name": "高集中主題進場-日月光", "symbol": "3711", "entry_price": 150.0, "stop_price": 141.0, "theme_concentration_score": 72.0, "expected_theme_factor": 0.75, "should_auto_apply": False},
    {"fixture_id": "FX209-008", "schema_version": "209", "paper_only": True, "name": "高波動+高集中-緯穎", "symbol": "6669", "entry_price": 2000.0, "stop_price": 1880.0, "is_high_volatility": True, "theme_concentration_score": 78.0, "expected_combined_reduction": True, "should_auto_apply": False},
    {"fixture_id": "FX209-009", "schema_version": "209", "paper_only": True, "name": "零停損距離-阻擋", "symbol": "TEST-001", "entry_price": 100.0, "stop_price": 100.0, "expected_size_action": "block_new_position", "expected_base_size": 0, "should_auto_apply": False},
    {"fixture_id": "FX209-010", "schema_version": "209", "paper_only": True, "name": "無效進場價-阻擋", "symbol": "TEST-002", "entry_price": 0.0, "stop_price": 0.0, "expected_size_action": "block_new_position", "should_auto_apply": False},
    # --- 11-20: risk budget policy fixtures ---
    {"fixture_id": "FX209-011", "schema_version": "209", "paper_only": True, "name": "預設風險預算policy", "policy_id": "default-policy-v209", "account_equity": 300000.0, "max_total_risk_pct": 0.06, "max_single_trade_risk_pct": 0.01, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX209-012", "schema_version": "209", "paper_only": True, "name": "保守風險預算policy", "policy_id": "conservative-policy-v209", "account_equity": 300000.0, "max_total_risk_pct": 0.04, "max_single_trade_risk_pct": 0.005, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX209-013", "schema_version": "209", "paper_only": True, "name": "積極風險預算policy", "policy_id": "aggressive-policy-v209", "account_equity": 300000.0, "max_total_risk_pct": 0.08, "max_single_trade_risk_pct": 0.015, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX209-014", "schema_version": "209", "paper_only": True, "name": "policy.auto_apply強制False", "policy_id": "guard-test-v209", "input_auto_apply_enabled": True, "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX209-015", "schema_version": "209", "paper_only": True, "name": "風險預算充足-全額建倉", "total_risk_pct": 0.02, "max_total_risk_pct": 0.06, "expected_over_budget": False, "should_auto_apply": False},
    {"fixture_id": "FX209-016", "schema_version": "209", "paper_only": True, "name": "風險預算滿載-拒絕新倉", "total_risk_pct": 0.07, "max_total_risk_pct": 0.06, "expected_over_budget": True, "should_auto_apply": False},
    {"fixture_id": "FX209-017", "schema_version": "209", "paper_only": True, "name": "min_cash_buffer驗證", "min_cash_buffer_pct": 0.20, "current_cash_pct": 0.18, "expected_blocked": True, "should_auto_apply": False},
    {"fixture_id": "FX209-018", "schema_version": "209", "paper_only": True, "name": "default_stop_loss_pct=6%", "default_stop_loss_pct": 0.06, "expected_value": 0.06, "should_auto_apply": False},
    {"fixture_id": "FX209-019", "schema_version": "209", "paper_only": True, "name": "單筆風險超過上限-人工審核", "single_trade_risk_pct": 0.015, "max_single_trade_risk_pct": 0.01, "expected_requires_human_review": True, "should_auto_apply": False},
    {"fixture_id": "FX209-020", "schema_version": "209", "paper_only": True, "name": "policy_id唯一識別", "policy_id": "unique-id-test", "expected_policy_id": "unique-id-test", "should_auto_apply": False},
    # --- 21-30: candidate sizing item fixtures ---
    {"fixture_id": "FX209-021", "schema_version": "209", "paper_only": True, "name": "CandidateSizingItem預設建立", "expected_should_auto_apply": False, "expected_size_action": "observation_only", "should_auto_apply": False},
    {"fixture_id": "FX209-022", "schema_version": "209", "paper_only": True, "name": "should_auto_apply強制False", "input_should_auto_apply": True, "expected_should_auto_apply": False, "should_auto_apply": False},
    {"fixture_id": "FX209-023", "schema_version": "209", "paper_only": True, "name": "paper_only=True", "expected_paper_only": True, "should_auto_apply": False},
    {"fixture_id": "FX209-024", "schema_version": "209", "paper_only": True, "name": "no_real_orders=True", "expected_no_real_orders": True, "should_auto_apply": False},
    {"fixture_id": "FX209-025", "schema_version": "209", "paper_only": True, "name": "schema_version=209", "expected_schema_version": "209", "should_auto_apply": False},
    {"fixture_id": "FX209-026", "schema_version": "209", "paper_only": True, "name": "blocked_reasons為清單", "expected_blocked_reasons_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX209-027", "schema_version": "209", "paper_only": True, "name": "final_risk_pct>=0", "expected_final_risk_pct_min": 0.0, "should_auto_apply": False},
    {"fixture_id": "FX209-028", "schema_version": "209", "paper_only": True, "name": "final_recommended_size>=0", "expected_final_size_min": 0, "should_auto_apply": False},
    {"fixture_id": "FX209-029", "schema_version": "209", "paper_only": True, "name": "stop_distance_pct計算正確", "entry_price": 100.0, "stop_price": 94.0, "expected_stop_distance_pct": 0.06, "should_auto_apply": False},
    {"fixture_id": "FX209-030", "schema_version": "209", "paper_only": True, "name": "risk_per_share計算正確", "entry_price": 100.0, "stop_price": 94.0, "expected_risk_per_share": 6.0, "should_auto_apply": False},
    # --- 31-40: size action classification fixtures ---
    {"fixture_id": "FX209-031", "schema_version": "209", "paper_only": True, "name": "size_action=allow_full_paper_size", "ratio": 0.95, "expected_action": "allow_full_paper_size", "should_auto_apply": False},
    {"fixture_id": "FX209-032", "schema_version": "209", "paper_only": True, "name": "size_action=reduce_size", "ratio": 0.70, "expected_action": "reduce_size", "should_auto_apply": False},
    {"fixture_id": "FX209-033", "schema_version": "209", "paper_only": True, "name": "size_action=minimum_probe_size", "ratio": 0.35, "expected_action": "minimum_probe_size", "should_auto_apply": False},
    {"fixture_id": "FX209-034", "schema_version": "209", "paper_only": True, "name": "size_action=observation_only", "ratio": 0.10, "expected_action": "observation_only", "should_auto_apply": False},
    {"fixture_id": "FX209-035", "schema_version": "209", "paper_only": True, "name": "size_action=block_new_position", "final_size": 0, "expected_action": "block_new_position", "should_auto_apply": False},
    {"fixture_id": "FX209-036", "schema_version": "209", "paper_only": True, "name": "size_action=human_review_required", "requires_human_review": True, "expected_action": "human_review_required", "should_auto_apply": False},
    {"fixture_id": "FX209-037", "schema_version": "209", "paper_only": True, "name": "size_action=require_rescore", "rescore_triggered": True, "expected_action_option": "require_rescore", "should_auto_apply": False},
    {"fixture_id": "FX209-038", "schema_version": "209", "paper_only": True, "name": "所有size_action均非auto-apply", "all_actions_non_auto": True, "should_auto_apply": False},
    {"fixture_id": "FX209-039", "schema_version": "209", "paper_only": True, "name": "size_action清單共7項", "expected_action_count": 7, "should_auto_apply": False},
    {"fixture_id": "FX209-040", "schema_version": "209", "paper_only": True, "name": "零倉位->block_new_position", "final_size": 0, "expected_action": "block_new_position", "should_auto_apply": False},
    # --- 41-50: sizing review fixtures ---
    {"fixture_id": "FX209-041", "schema_version": "209", "paper_only": True, "name": "預設sizing review", "expected_all_passed": True, "expected_paper_only": True, "should_auto_apply": False},
    {"fixture_id": "FX209-042", "schema_version": "209", "paper_only": True, "name": "sizing_review_id非空", "expected_id_nonempty": True, "should_auto_apply": False},
    {"fixture_id": "FX209-043", "schema_version": "209", "paper_only": True, "name": "sizing_version=2.0.9", "expected_sizing_version": "2.0.9", "should_auto_apply": False},
    {"fixture_id": "FX209-044", "schema_version": "209", "paper_only": True, "name": "review_period非空", "expected_review_period_nonempty": True, "should_auto_apply": False},
    {"fixture_id": "FX209-045", "schema_version": "209", "paper_only": True, "name": "risk_budget_snapshot非空", "expected_snapshot_nonempty": True, "should_auto_apply": False},
    {"fixture_id": "FX209-046", "schema_version": "209", "paper_only": True, "name": "candidate_sizing_snapshot非空", "expected_snapshot_nonempty": True, "should_auto_apply": False},
    {"fixture_id": "FX209-047", "schema_version": "209", "paper_only": True, "name": "sizing_summary非空", "expected_summary_nonempty": True, "should_auto_apply": False},
    {"fixture_id": "FX209-048", "schema_version": "209", "paper_only": True, "name": "should_auto_apply=False", "expected_should_auto_apply": False, "should_auto_apply": False},
    {"fixture_id": "FX209-049", "schema_version": "209", "paper_only": True, "name": "auto_apply_enabled=False", "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX209-050", "schema_version": "209", "paper_only": True, "name": "paper_only_safety_snapshot=True", "expected_safety_snapshot": True, "should_auto_apply": False},
    # --- 51-60: sizing summary fixtures ---
    {"fixture_id": "FX209-051", "schema_version": "209", "paper_only": True, "name": "total_candidate_count正確", "expected_count_gte_0": True, "should_auto_apply": False},
    {"fixture_id": "FX209-052", "schema_version": "209", "paper_only": True, "name": "total_allocated_risk_pct>=0", "expected_min": 0.0, "should_auto_apply": False},
    {"fixture_id": "FX209-053", "schema_version": "209", "paper_only": True, "name": "remaining_risk_budget_pct>=0", "expected_min": 0.0, "should_auto_apply": False},
    {"fixture_id": "FX209-054", "schema_version": "209", "paper_only": True, "name": "top_risk_contributors為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX209-055", "schema_version": "209", "paper_only": True, "name": "top_size_reduction_reasons為清單", "expected_type": "list", "should_auto_apply": False},
    {"fixture_id": "FX209-056", "schema_version": "209", "paper_only": True, "name": "sizing_quality_grade為A/B/C/D", "expected_values": ["A","B","C","D"], "should_auto_apply": False},
    {"fixture_id": "FX209-057", "schema_version": "209", "paper_only": True, "name": "risk_budget_quality_grade為A/B/C", "expected_values": ["A","B","C"], "should_auto_apply": False},
    {"fixture_id": "FX209-058", "schema_version": "209", "paper_only": True, "name": "blocked_position_count>=0", "expected_min": 0, "should_auto_apply": False},
    {"fixture_id": "FX209-059", "schema_version": "209", "paper_only": True, "name": "human_review_count>=0", "expected_min": 0, "should_auto_apply": False},
    {"fixture_id": "FX209-060", "schema_version": "209", "paper_only": True, "name": "max_single_trade_risk_pct=0.01(預設)", "expected_value": 0.01, "should_auto_apply": False},
    # --- 61-70: export fixtures ---
    {"fixture_id": "FX209-061", "schema_version": "209", "paper_only": True, "name": "JSON匯出is_valid=True", "expected_is_valid": True, "export_format": "json", "should_auto_apply": False},
    {"fixture_id": "FX209-062", "schema_version": "209", "paper_only": True, "name": "JSON匯出content非空", "expected_nonempty": True, "export_format": "json", "should_auto_apply": False},
    {"fixture_id": "FX209-063", "schema_version": "209", "paper_only": True, "name": "Markdown匯出is_valid=True", "expected_is_valid": True, "export_format": "markdown", "should_auto_apply": False},
    {"fixture_id": "FX209-064", "schema_version": "209", "paper_only": True, "name": "Markdown匯出含should_auto_apply=False標記", "expected_marker": "should_auto_apply=False", "export_format": "markdown", "should_auto_apply": False},
    {"fixture_id": "FX209-065", "schema_version": "209", "paper_only": True, "name": "CSV候選倉位is_valid=True", "expected_is_valid": True, "export_format": "csv_sizing", "should_auto_apply": False},
    {"fixture_id": "FX209-066", "schema_version": "209", "paper_only": True, "name": "CSV風險預算is_valid=True", "expected_is_valid": True, "export_format": "csv_risk_budget", "should_auto_apply": False},
    {"fixture_id": "FX209-067", "schema_version": "209", "paper_only": True, "name": "CSV縮倉佇列is_valid=True", "expected_is_valid": True, "export_format": "csv_size_reduction", "should_auto_apply": False},
    {"fixture_id": "FX209-068", "schema_version": "209", "paper_only": True, "name": "Audit snapshot含reproducibility_hash", "expected_hash_present": True, "export_format": "audit_snapshot", "should_auto_apply": False},
    {"fixture_id": "FX209-069", "schema_version": "209", "paper_only": True, "name": "Audit snapshot safety_snapshot含paper_only", "expected_safety_marker": "paper_only=True", "export_format": "audit_snapshot", "should_auto_apply": False},
    {"fixture_id": "FX209-070", "schema_version": "209", "paper_only": True, "name": "所有匯出結果含should_auto_apply=False", "all_exports_non_auto": True, "should_auto_apply": False},
    # --- 71-80: backward compat and safety fixtures ---
    {"fixture_id": "FX209-071", "schema_version": "209", "paper_only": True, "name": "v2.0.8 backward compat", "v208_import_works": True, "v208_run_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX209-072", "schema_version": "209", "paper_only": True, "name": "v2.0.7 backward compat", "v207_import_works": True, "v207_run_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX209-073", "schema_version": "209", "paper_only": True, "name": "v2.0.6 backward compat", "v206_import_works": True, "should_auto_apply": False},
    {"fixture_id": "FX209-074", "schema_version": "209", "paper_only": True, "name": "v2.0.5 backward compat", "v205_import_works": True, "should_auto_apply": False},
    {"fixture_id": "FX209-075", "schema_version": "209", "paper_only": True, "name": "v201 health relative-path compat", "v201_test_file_exists": True, "should_auto_apply": False},
    {"fixture_id": "FX209-076", "schema_version": "209", "paper_only": True, "name": "GUI panel importable", "gui_panel_importable": True, "should_auto_apply": False},
    {"fixture_id": "FX209-077", "schema_version": "209", "paper_only": True, "name": "GUI v2.0.9 tabs 3項", "expected_tab_count": 3, "should_auto_apply": False},
    {"fixture_id": "FX209-078", "schema_version": "209", "paper_only": True, "name": "render_all_tabs無錯誤", "expected_no_error_tabs": True, "should_auto_apply": False},
    {"fixture_id": "FX209-079", "schema_version": "209", "paper_only": True, "name": "CLI handler全部可呼叫", "expected_cli_count": 10, "should_auto_apply": False},
    {"fixture_id": "FX209-080", "schema_version": "209", "paper_only": True, "name": "SAFETY_FLAGS_V209共21項", "expected_safety_flag_count": 21, "should_auto_apply": False},
]

assert len(FIXTURES) == 80, f"Expected 80 fixtures, got {len(FIXTURES)}"
assert all(f["schema_version"] == "209" for f in FIXTURES)
assert all(f["paper_only"] is True for f in FIXTURES)
assert all("fixture_id" in f for f in FIXTURES)
