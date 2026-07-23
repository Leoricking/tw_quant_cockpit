"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v211.py
v2.0.11 Paper Trade Journal & Execution Discipline Review — Fixtures
[!] Paper Only. Research Only. Journal Review Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "211"

FIXTURES: List[Dict[str, Any]] = [
    # --- 1-10: trade journal policy fixtures ---
    {"fixture_id": "FX211-001", "schema_version": "211", "paper_only": True, "name": "標準日誌政策", "policy_id": "default-policy-v211", "require_planned_entry_before_trade": True, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-002", "schema_version": "211", "paper_only": True, "name": "寬鬆滑點政策", "policy_id": "loose-slippage-v211", "max_allowed_entry_slippage_pct": 0.05, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-003", "schema_version": "211", "paper_only": True, "name": "嚴格部位政策", "policy_id": "strict-size-v211", "max_allowed_size_deviation_pct": 0.05, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-004", "schema_version": "211", "paper_only": True, "name": "高紀律分數政策", "policy_id": "high-discipline-v211", "min_discipline_score": 85.0, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-005", "schema_version": "211", "paper_only": True, "name": "零加碼政策", "policy_id": "no-addon-v211", "max_allowed_unplanned_add_count": 0, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-006", "schema_version": "211", "paper_only": True, "name": "auto_apply強制False", "policy_id": "forced-no-apply-v211", "input_auto_apply_enabled": True, "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-007", "schema_version": "211", "paper_only": True, "name": "require_planned_entry強制True", "policy_id": "forced-planned-entry-v211", "input_require_planned_entry": False, "expected_require_planned_entry_before_trade": True, "should_auto_apply": False},
    {"fixture_id": "FX211-008", "schema_version": "211", "paper_only": True, "name": "標準停損偏差限制", "policy_id": "std-stop-dev-v211", "max_allowed_stop_deviation_pct": 0.05, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-009", "schema_version": "211", "paper_only": True, "name": "過度交易限制2次", "policy_id": "overtrade-limit-v211", "max_allowed_overtrade_count": 2, "auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-010", "schema_version": "211", "paper_only": True, "name": "最低紀律分數標準", "policy_id": "min-discipline-v211", "min_discipline_score": 70.0, "auto_apply_enabled": False, "should_auto_apply": False},
    # --- 11-20: compliant journal entry fixtures ---
    {"fixture_id": "FX211-011", "schema_version": "211", "paper_only": True, "name": "台積電-完全符合計畫", "journal_entry_id": "JE-2330-FX-011", "symbol": "2330", "name_": "台積電", "planned_entry_price": 900.0, "actual_entry_price": 900.0, "planned_size": 1000, "actual_size": 1000, "planned_stop": 855.0, "actual_stop": 855.0, "planned_exit": 945.0, "trade_status": "entered", "expected_execution_action": "compliant", "should_auto_apply": False},
    {"fixture_id": "FX211-012", "schema_version": "211", "paper_only": True, "name": "聯發科-完全符合計畫", "journal_entry_id": "JE-2454-FX-012", "symbol": "2454", "name_": "聯發科", "planned_entry_price": 1000.0, "actual_entry_price": 1000.0, "planned_size": 500, "actual_size": 500, "planned_stop": 940.0, "actual_stop": 940.0, "planned_exit": 1060.0, "trade_status": "entered", "expected_execution_action": "compliant", "should_auto_apply": False},
    {"fixture_id": "FX211-013", "schema_version": "211", "paper_only": True, "name": "廣達-正常出場", "journal_entry_id": "JE-2382-FX-013", "symbol": "2382", "name_": "廣達", "planned_entry_price": 300.0, "actual_entry_price": 300.0, "planned_size": 2000, "actual_size": 2000, "planned_stop": 282.0, "actual_stop": 282.0, "planned_exit": 318.0, "trade_status": "exited", "expected_execution_action": "compliant", "should_auto_apply": False},
    {"fixture_id": "FX211-014", "schema_version": "211", "paper_only": True, "name": "日月光-停利達標", "journal_entry_id": "JE-3711-FX-014", "symbol": "3711", "name_": "日月光", "planned_entry_price": 150.0, "actual_entry_price": 150.0, "planned_size": 2000, "actual_size": 2000, "planned_stop": 141.0, "actual_stop": 141.0, "planned_exit": 159.0, "trade_status": "take_profit_done", "expected_execution_action": "compliant", "should_auto_apply": False},
    {"fixture_id": "FX211-015", "schema_version": "211", "paper_only": True, "name": "聯電-正常取消", "journal_entry_id": "JE-2303-FX-015", "symbol": "2303", "name_": "聯電", "planned_entry_price": 55.0, "actual_entry_price": 0.0, "planned_size": 3000, "actual_size": 0, "planned_stop": 51.0, "actual_stop": 0.0, "planned_exit": 59.0, "trade_status": "cancelled", "expected_trade_status": "cancelled", "should_auto_apply": False},
    {"fixture_id": "FX211-016", "schema_version": "211", "paper_only": True, "name": "台達電-計畫失效", "journal_entry_id": "JE-2308-FX-016", "symbol": "2308", "name_": "台達電", "planned_entry_price": 400.0, "actual_entry_price": 0.0, "planned_size": 1000, "actual_size": 0, "planned_stop": 372.0, "actual_stop": 0.0, "planned_exit": 428.0, "trade_status": "invalidated", "expected_trade_status": "invalidated", "should_auto_apply": False},
    {"fixture_id": "FX211-017", "schema_version": "211", "paper_only": True, "name": "鴻海-減倉", "journal_entry_id": "JE-2317-FX-017", "symbol": "2317", "name_": "鴻海", "planned_entry_price": 120.0, "actual_entry_price": 120.0, "planned_size": 1000, "actual_size": 500, "planned_stop": 112.0, "actual_stop": 112.0, "planned_exit": 128.0, "trade_status": "reduced", "expected_trade_status": "reduced", "should_auto_apply": False},
    {"fixture_id": "FX211-018", "schema_version": "211", "paper_only": True, "name": "緯穎-符合計畫進場", "journal_entry_id": "JE-6669-FX-018", "symbol": "6669", "name_": "緯穎", "planned_entry_price": 2000.0, "actual_entry_price": 2000.0, "planned_size": 300, "actual_size": 300, "planned_stop": 1880.0, "actual_stop": 1880.0, "planned_exit": 2120.0, "trade_status": "entered", "expected_execution_action": "compliant", "should_auto_apply": False},
    {"fixture_id": "FX211-019", "schema_version": "211", "paper_only": True, "name": "空計畫僅紀錄", "journal_entry_id": "JE-0000-FX-019", "symbol": "0000", "name_": "示範股", "planned_entry_price": 100.0, "actual_entry_price": 0.0, "planned_size": 1000, "actual_size": 0, "planned_stop": 93.0, "actual_stop": 0.0, "planned_exit": 107.0, "trade_status": "planned_only", "expected_trade_status": "planned_only", "should_auto_apply": False},
    {"fixture_id": "FX211-020", "schema_version": "211", "paper_only": True, "name": "觸發停損出場", "journal_entry_id": "JE-2303-FX-020", "symbol": "2303", "name_": "聯電", "planned_entry_price": 55.0, "actual_entry_price": 55.0, "planned_size": 3000, "actual_size": 3000, "planned_stop": 51.0, "actual_stop": 51.0, "planned_exit": 59.0, "trade_status": "stopped_out", "expected_trade_status": "stopped_out", "should_auto_apply": False},
    # --- 21-30: violation fixtures ---
    {"fixture_id": "FX211-021", "schema_version": "211", "paper_only": True, "name": "進場滑點超標-聯發科", "journal_entry_id": "JE-2454-FX-021", "symbol": "2454", "planned_entry_price": 1000.0, "actual_entry_price": 1035.0, "expected_violation": "ENTRY_SLIPPAGE_EXCESS", "should_auto_apply": False},
    {"fixture_id": "FX211-022", "schema_version": "211", "paper_only": True, "name": "部位超標-緯穎", "journal_entry_id": "JE-6669-FX-022", "symbol": "6669", "planned_size": 300, "actual_size": 500, "expected_violation": "SIZE_DEVIATION_EXCESS", "should_auto_apply": False},
    {"fixture_id": "FX211-023", "schema_version": "211", "paper_only": True, "name": "無計畫進場-鴻海", "journal_entry_id": "JE-2317-FX-023", "symbol": "2317", "planned_entry_price": 0.0, "actual_entry_price": 120.0, "expected_violation": "NO_PLANNED_ENTRY", "should_auto_apply": False},
    {"fixture_id": "FX211-024", "schema_version": "211", "paper_only": True, "name": "停損未執行-聯電", "journal_entry_id": "JE-2303-FX-024", "symbol": "2303", "stop_loss_violated": True, "expected_violation": "STOP_LOSS_VIOLATION", "should_auto_apply": False},
    {"fixture_id": "FX211-025", "schema_version": "211", "paper_only": True, "name": "缺少出場計畫", "journal_entry_id": "JE-2330-FX-025", "symbol": "2330", "planned_exit_price": 0.0, "expected_violation": "MISSING_EXIT_PLAN", "should_auto_apply": False},
    {"fixture_id": "FX211-026", "schema_version": "211", "paper_only": True, "name": "無計畫加碼-緯穎", "journal_entry_id": "JE-6669-FX-026", "symbol": "6669", "is_unplanned_add": True, "expected_violation": "UNPLANNED_ADD", "should_auto_apply": False},
    {"fixture_id": "FX211-027", "schema_version": "211", "paper_only": True, "name": "過度交易", "journal_entry_id": "JE-0000-FX-027", "symbol": "0000", "is_overtrade": True, "expected_violation": "OVERTRADE", "should_auto_apply": False},
    {"fixture_id": "FX211-028", "schema_version": "211", "paper_only": True, "name": "停損設定偏移過大", "journal_entry_id": "JE-2308-FX-028", "symbol": "2308", "planned_stop": 372.0, "actual_stop": 350.0, "expected_violation": "STOP_DEVIATION_EXCESS", "should_auto_apply": False},
    {"fixture_id": "FX211-029", "schema_version": "211", "paper_only": True, "name": "多重違規組合", "journal_entry_id": "JE-0000-FX-029", "symbol": "0000", "is_unplanned_add": True, "stop_loss_violated": True, "planned_exit_price": 0.0, "expected_violations": ["UNPLANNED_ADD", "STOP_LOSS_VIOLATION", "MISSING_EXIT_PLAN"], "should_auto_apply": False},
    {"fixture_id": "FX211-030", "schema_version": "211", "paper_only": True, "name": "零違規基準", "journal_entry_id": "JE-2330-FX-030", "symbol": "2330", "planned_entry_price": 900.0, "actual_entry_price": 900.0, "planned_size": 1000, "actual_size": 1000, "expected_violations": [], "should_auto_apply": False},
    # --- 31-40: execution discipline summary fixtures ---
    {"fixture_id": "FX211-031", "schema_version": "211", "paper_only": True, "name": "全compliant摘要", "total": 5, "compliant": 5, "expected_grade": "A", "expected_adherence": "A", "should_auto_apply": False},
    {"fixture_id": "FX211-032", "schema_version": "211", "paper_only": True, "name": "80%compliant摘要", "total": 10, "compliant": 8, "expected_adherence": "B", "should_auto_apply": False},
    {"fixture_id": "FX211-033", "schema_version": "211", "paper_only": True, "name": "60%compliant摘要", "total": 10, "compliant": 6, "expected_adherence": "C", "should_auto_apply": False},
    {"fixture_id": "FX211-034", "schema_version": "211", "paper_only": True, "name": "40%compliant摘要", "total": 10, "compliant": 4, "expected_adherence": "D", "should_auto_apply": False},
    {"fixture_id": "FX211-035", "schema_version": "211", "paper_only": True, "name": "空日誌摘要N/A", "total": 0, "compliant": 0, "expected_adherence": "N/A", "should_auto_apply": False},
    {"fixture_id": "FX211-036", "schema_version": "211", "paper_only": True, "name": "摘要包含平均分數", "expected_has_avg_score": True, "should_auto_apply": False},
    {"fixture_id": "FX211-037", "schema_version": "211", "paper_only": True, "name": "摘要包含最差symbol", "expected_has_worst_symbols": True, "should_auto_apply": False},
    {"fixture_id": "FX211-038", "schema_version": "211", "paper_only": True, "name": "摘要包含top_mistake_tags", "expected_has_top_tags": True, "should_auto_apply": False},
    {"fixture_id": "FX211-039", "schema_version": "211", "paper_only": True, "name": "摘要包含top_violation_codes", "expected_has_top_codes": True, "should_auto_apply": False},
    {"fixture_id": "FX211-040", "schema_version": "211", "paper_only": True, "name": "摘要schema_version為211", "expected_schema_version": "211", "should_auto_apply": False},
    # --- 41-50: improvement suggestion fixtures ---
    {"fixture_id": "FX211-041", "schema_version": "211", "paper_only": True, "name": "NO_PLANNED_ENTRY建議", "violation_codes": ["NO_PLANNED_ENTRY"], "expected_suggestion_contains": "計畫", "should_auto_apply": False},
    {"fixture_id": "FX211-042", "schema_version": "211", "paper_only": True, "name": "MISSING_EXIT_PLAN建議", "violation_codes": ["MISSING_EXIT_PLAN"], "expected_suggestion_contains": "出場", "should_auto_apply": False},
    {"fixture_id": "FX211-043", "schema_version": "211", "paper_only": True, "name": "STOP_LOSS_VIOLATION建議", "violation_codes": ["STOP_LOSS_VIOLATION"], "expected_suggestion_contains": "停損", "should_auto_apply": False},
    {"fixture_id": "FX211-044", "schema_version": "211", "paper_only": True, "name": "ENTRY_SLIPPAGE_EXCESS建議", "violation_codes": ["ENTRY_SLIPPAGE_EXCESS"], "expected_suggestion_contains": "追高", "should_auto_apply": False},
    {"fixture_id": "FX211-045", "schema_version": "211", "paper_only": True, "name": "SIZE_DEVIATION_EXCESS建議", "violation_codes": ["SIZE_DEVIATION_EXCESS"], "expected_suggestion_contains": "部位", "should_auto_apply": False},
    {"fixture_id": "FX211-046", "schema_version": "211", "paper_only": True, "name": "UNPLANNED_ADD建議", "violation_codes": ["UNPLANNED_ADD"], "expected_suggestion_contains": "加碼", "should_auto_apply": False},
    {"fixture_id": "FX211-047", "schema_version": "211", "paper_only": True, "name": "OVERTRADE建議", "violation_codes": ["OVERTRADE"], "expected_suggestion_contains": "過度交易", "should_auto_apply": False},
    {"fixture_id": "FX211-048", "schema_version": "211", "paper_only": True, "name": "無違規無建議", "violation_codes": [], "expected_suggestion_count": 0, "should_auto_apply": False},
    {"fixture_id": "FX211-049", "schema_version": "211", "paper_only": True, "name": "建議不自動套用", "expected_auto_apply": False, "should_auto_apply": False},
    {"fixture_id": "FX211-050", "schema_version": "211", "paper_only": True, "name": "建議為紙上僅供參考", "paper_only": True, "should_auto_apply": False},
    # --- 51-60: journal review result fixtures ---
    {"fixture_id": "FX211-051", "schema_version": "211", "paper_only": True, "name": "預設日誌審查可執行", "expected_callable": True, "should_auto_apply": False},
    {"fixture_id": "FX211-052", "schema_version": "211", "paper_only": True, "name": "審查結果paper_only=True", "expected_paper_only": True, "should_auto_apply": False},
    {"fixture_id": "FX211-053", "schema_version": "211", "paper_only": True, "name": "審查結果should_auto_apply=False", "expected_should_auto_apply": False, "should_auto_apply": False},
    {"fixture_id": "FX211-054", "schema_version": "211", "paper_only": True, "name": "審查結果auto_apply_enabled=False", "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"fixture_id": "FX211-055", "schema_version": "211", "paper_only": True, "name": "審查結果all_passed=True", "expected_all_passed": True, "should_auto_apply": False},
    {"fixture_id": "FX211-056", "schema_version": "211", "paper_only": True, "name": "審查結果含journal_version", "expected_journal_version": "2.0.11", "should_auto_apply": False},
    {"fixture_id": "FX211-057", "schema_version": "211", "paper_only": True, "name": "審查結果含discipline_summary", "expected_has_summary": True, "should_auto_apply": False},
    {"fixture_id": "FX211-058", "schema_version": "211", "paper_only": True, "name": "審查結果含mistake_review_queue", "expected_has_mistake_queue": True, "should_auto_apply": False},
    {"fixture_id": "FX211-059", "schema_version": "211", "paper_only": True, "name": "審查結果含violation_queue", "expected_has_violation_queue": True, "should_auto_apply": False},
    {"fixture_id": "FX211-060", "schema_version": "211", "paper_only": True, "name": "審查結果含improvement_suggestions", "expected_has_suggestions": True, "should_auto_apply": False},
    # --- 61-70: export fixtures ---
    {"fixture_id": "FX211-061", "schema_version": "211", "paper_only": True, "name": "JSON匯出有效", "expected_is_valid": True, "export_format": "json", "should_auto_apply": False},
    {"fixture_id": "FX211-062", "schema_version": "211", "paper_only": True, "name": "JSON含paper_only=True", "expected_contains_paper_only": True, "export_format": "json", "should_auto_apply": False},
    {"fixture_id": "FX211-063", "schema_version": "211", "paper_only": True, "name": "Markdown匯出有效", "expected_is_valid": True, "export_format": "markdown", "should_auto_apply": False},
    {"fixture_id": "FX211-064", "schema_version": "211", "paper_only": True, "name": "Markdown含版本資訊", "expected_contains_version": True, "export_format": "markdown", "should_auto_apply": False},
    {"fixture_id": "FX211-065", "schema_version": "211", "paper_only": True, "name": "Journal CSV有效", "expected_is_valid": True, "export_format": "journal_csv", "should_auto_apply": False},
    {"fixture_id": "FX211-066", "schema_version": "211", "paper_only": True, "name": "Discipline CSV有效", "expected_is_valid": True, "export_format": "discipline_csv", "should_auto_apply": False},
    {"fixture_id": "FX211-067", "schema_version": "211", "paper_only": True, "name": "Mistake CSV有效", "expected_is_valid": True, "export_format": "mistake_csv", "should_auto_apply": False},
    {"fixture_id": "FX211-068", "schema_version": "211", "paper_only": True, "name": "Violation CSV有效", "expected_is_valid": True, "export_format": "violation_csv", "should_auto_apply": False},
    {"fixture_id": "FX211-069", "schema_version": "211", "paper_only": True, "name": "Audit Snapshot完整", "expected_export_status": "complete", "export_format": "audit_snapshot", "should_auto_apply": False},
    {"fixture_id": "FX211-070", "schema_version": "211", "paper_only": True, "name": "所有匯出均paper_only_confirmed", "expected_paper_only_confirmed": True, "should_auto_apply": False},
    # --- 71-80: safety / integration / health fixtures ---
    {"fixture_id": "FX211-071", "schema_version": "211", "paper_only": True, "name": "safety_flags共24個", "expected_safety_flag_count": 24, "should_auto_apply": False},
    {"fixture_id": "FX211-072", "schema_version": "211", "paper_only": True, "name": "safety_paper_only=True", "expected_flag": "paper_only", "expected_value": True, "should_auto_apply": False},
    {"fixture_id": "FX211-073", "schema_version": "211", "paper_only": True, "name": "safety_no_broker=True", "expected_flag": "no_broker", "expected_value": True, "should_auto_apply": False},
    {"fixture_id": "FX211-074", "schema_version": "211", "paper_only": True, "name": "safety_should_auto_apply_always_false=True", "expected_flag": "should_auto_apply_always_false", "expected_value": True, "should_auto_apply": False},
    {"fixture_id": "FX211-075", "schema_version": "211", "paper_only": True, "name": "safety_require_planned_entry_always_true=True", "expected_flag": "require_planned_entry_before_trade_always_true", "expected_value": True, "should_auto_apply": False},
    {"fixture_id": "FX211-076", "schema_version": "211", "paper_only": True, "name": "v2.0.10向下相容", "expected_v210_importable": True, "should_auto_apply": False},
    {"fixture_id": "FX211-077", "schema_version": "211", "paper_only": True, "name": "v2.0.9向下相容", "expected_v209_importable": True, "should_auto_apply": False},
    {"fixture_id": "FX211-078", "schema_version": "211", "paper_only": True, "name": "GUI panel可匯入", "expected_gui_importable": True, "should_auto_apply": False},
    {"fixture_id": "FX211-079", "schema_version": "211", "paper_only": True, "name": "CLI commands共10個", "expected_cli_command_count": 10, "should_auto_apply": False},
    {"fixture_id": "FX211-080", "schema_version": "211", "paper_only": True, "name": "GUI tabs共3個", "expected_gui_tab_count": 3, "should_auto_apply": False},
]

assert len(FIXTURES) == 80, f"Expected 80 FIXTURES, got {len(FIXTURES)}"
assert all(f["schema_version"] == "211" for f in FIXTURES)
assert all(f["paper_only"] is True for f in FIXTURES)
assert all("fixture_id" in f for f in FIXTURES)
assert all(f["should_auto_apply"] is False for f in FIXTURES)
