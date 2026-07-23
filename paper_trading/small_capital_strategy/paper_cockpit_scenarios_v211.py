"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v211.py
v2.0.11 Paper Trade Journal & Execution Discipline Review — Scenarios
[!] Paper Only. Research Only. Journal Review Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "211"

SCENARIOS: List[Dict[str, Any]] = [
    # --- 1-10: trade journal policy scenarios ---
    {"scenario_id": "SC211-001", "schema_version": "211", "paper_only": True, "name": "標準交易日誌政策", "description": "require_planned_entry_before_trade=True，auto_apply_enabled=False", "require_planned_entry_before_trade": True, "auto_apply_enabled": False, "should_auto_apply": False},
    {"scenario_id": "SC211-002", "schema_version": "211", "paper_only": True, "name": "auto_apply_enabled強制False", "description": "__post_init__強制auto_apply_enabled=False", "input_auto_apply_enabled": True, "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"scenario_id": "SC211-003", "schema_version": "211", "paper_only": True, "name": "require_planned_entry強制True", "description": "__post_init__強制require_planned_entry_before_trade=True", "input_require_planned_entry": False, "expected_require_planned_entry": True, "should_auto_apply": False},
    {"scenario_id": "SC211-004", "schema_version": "211", "paper_only": True, "name": "進場滑點限制2%", "description": "max_allowed_entry_slippage_pct=0.02", "max_allowed_entry_slippage_pct": 0.02, "should_auto_apply": False},
    {"scenario_id": "SC211-005", "schema_version": "211", "paper_only": True, "name": "部位偏差限制10%", "description": "max_allowed_size_deviation_pct=0.10", "max_allowed_size_deviation_pct": 0.10, "should_auto_apply": False},
    {"scenario_id": "SC211-006", "schema_version": "211", "paper_only": True, "name": "停損偏差限制5%", "description": "max_allowed_stop_deviation_pct=0.05", "max_allowed_stop_deviation_pct": 0.05, "should_auto_apply": False},
    {"scenario_id": "SC211-007", "schema_version": "211", "paper_only": True, "name": "無計畫加碼限制", "description": "max_allowed_unplanned_add_count=0", "max_allowed_unplanned_add_count": 0, "should_auto_apply": False},
    {"scenario_id": "SC211-008", "schema_version": "211", "paper_only": True, "name": "過度交易上限2次", "description": "max_allowed_overtrade_count=2", "max_allowed_overtrade_count": 2, "should_auto_apply": False},
    {"scenario_id": "SC211-009", "schema_version": "211", "paper_only": True, "name": "最低紀律分數70", "description": "min_discipline_score=70.0", "min_discipline_score": 70.0, "should_auto_apply": False},
    {"scenario_id": "SC211-010", "schema_version": "211", "paper_only": True, "name": "所有execution_action均為建議", "description": "7種execution_action均為紙上建議，不自動執行", "execution_actions": ["compliant","monitor","require_journal_note","require_rescore","flag_discipline_warning","block_followup_action","human_review_required"], "should_auto_apply": False, "auto_apply_enabled": False},
    # --- 11-20: journal entry compliance scenarios ---
    {"scenario_id": "SC211-011", "schema_version": "211", "paper_only": True, "name": "符合計畫進場-compliant", "description": "進場價格、部位大小、停損均符合計畫，execution_action=compliant", "planned_entry_price": 100.0, "actual_entry_price": 100.0, "planned_size": 1000, "actual_size": 1000, "expected_execution_action": "compliant", "should_auto_apply": False},
    {"scenario_id": "SC211-012", "schema_version": "211", "paper_only": True, "name": "進場滑點超標", "description": "actual_entry>planned*1.02，violation=ENTRY_SLIPPAGE_EXCESS", "planned_entry_price": 100.0, "actual_entry_price": 103.5, "expected_violation": "ENTRY_SLIPPAGE_EXCESS", "should_auto_apply": False},
    {"scenario_id": "SC211-013", "schema_version": "211", "paper_only": True, "name": "部位大小超標", "description": "actual_size比planned大10%以上，violation=SIZE_DEVIATION_EXCESS", "planned_size": 1000, "actual_size": 1200, "expected_violation": "SIZE_DEVIATION_EXCESS", "should_auto_apply": False},
    {"scenario_id": "SC211-014", "schema_version": "211", "paper_only": True, "name": "停損設定偏移", "description": "actual_stop距planned超過5%，violation=STOP_DEVIATION_EXCESS", "planned_stop": 94.0, "actual_stop": 88.0, "expected_violation": "STOP_DEVIATION_EXCESS", "should_auto_apply": False},
    {"scenario_id": "SC211-015", "schema_version": "211", "paper_only": True, "name": "缺少出場計畫", "description": "planned_exit_price=0，violation=MISSING_EXIT_PLAN", "planned_exit_price": 0.0, "expected_violation": "MISSING_EXIT_PLAN", "should_auto_apply": False},
    {"scenario_id": "SC211-016", "schema_version": "211", "paper_only": True, "name": "無計畫加碼", "description": "is_unplanned_add=True，violation=UNPLANNED_ADD", "is_unplanned_add": True, "expected_violation": "UNPLANNED_ADD", "should_auto_apply": False},
    {"scenario_id": "SC211-017", "schema_version": "211", "paper_only": True, "name": "過度交易", "description": "is_overtrade=True，violation=OVERTRADE", "is_overtrade": True, "expected_violation": "OVERTRADE", "should_auto_apply": False},
    {"scenario_id": "SC211-018", "schema_version": "211", "paper_only": True, "name": "停損未執行", "description": "stop_loss_violated=True，violation=STOP_LOSS_VIOLATION", "stop_loss_violated": True, "expected_violation": "STOP_LOSS_VIOLATION", "should_auto_apply": False},
    {"scenario_id": "SC211-019", "schema_version": "211", "paper_only": True, "name": "無計畫進場", "description": "planned_entry_price=0，violation=NO_PLANNED_ENTRY", "planned_entry_price": 0.0, "expected_violation": "NO_PLANNED_ENTRY", "should_auto_apply": False},
    {"scenario_id": "SC211-020", "schema_version": "211", "paper_only": True, "name": "should_auto_apply強制False", "description": "JournalEntry.should_auto_apply永遠為False", "input_should_auto_apply": True, "expected_should_auto_apply": False, "should_auto_apply": False},
    # --- 21-30: execution action classification scenarios ---
    {"scenario_id": "SC211-021", "schema_version": "211", "paper_only": True, "name": "execution_action=compliant條件", "description": "無違規且分數>=85，action=compliant", "discipline_score": 95.0, "violation_codes": [], "expected_execution_action": "compliant", "should_auto_apply": False},
    {"scenario_id": "SC211-022", "schema_version": "211", "paper_only": True, "name": "execution_action=monitor條件", "description": "分數>=70且<85，action=monitor", "discipline_score": 80.0, "violation_codes": [], "expected_execution_action": "monitor", "should_auto_apply": False},
    {"scenario_id": "SC211-023", "schema_version": "211", "paper_only": True, "name": "execution_action=require_journal_note", "description": "有違規但分數>=70，action=require_journal_note", "discipline_score": 75.0, "violation_codes": ["ENTRY_SLIPPAGE_EXCESS"], "expected_execution_action": "require_journal_note", "should_auto_apply": False},
    {"scenario_id": "SC211-024", "schema_version": "211", "paper_only": True, "name": "execution_action=require_rescore", "description": "分數>=50且<70，action=require_rescore", "discipline_score": 62.0, "violation_codes": ["ENTRY_SLIPPAGE_EXCESS"], "expected_execution_action": "require_rescore", "should_auto_apply": False},
    {"scenario_id": "SC211-025", "schema_version": "211", "paper_only": True, "name": "execution_action=flag_discipline_warning", "description": "有STOP_LOSS_VIOLATION，action=flag_discipline_warning", "violation_codes": ["STOP_LOSS_VIOLATION"], "expected_execution_action": "flag_discipline_warning", "should_auto_apply": False},
    {"scenario_id": "SC211-026", "schema_version": "211", "paper_only": True, "name": "execution_action=block_followup_action", "description": "分數<50，action=block_followup_action", "discipline_score": 35.0, "violation_codes": ["NO_PLANNED_ENTRY"], "expected_execution_action": "human_review_required", "should_auto_apply": False},
    {"scenario_id": "SC211-027", "schema_version": "211", "paper_only": True, "name": "execution_action=human_review_required", "description": "NO_PLANNED_ENTRY，action=human_review_required", "violation_codes": ["NO_PLANNED_ENTRY"], "expected_execution_action": "human_review_required", "should_auto_apply": False},
    {"scenario_id": "SC211-028", "schema_version": "211", "paper_only": True, "name": "所有execution_action為紙上建議", "description": "execution_action不會觸發真實交易", "paper_only": True, "should_auto_apply": False},
    {"scenario_id": "SC211-029", "schema_version": "211", "paper_only": True, "name": "多違規累積懲罰", "description": "多個violation同時存在，分數遞減", "violation_codes": ["ENTRY_SLIPPAGE_EXCESS","SIZE_DEVIATION_EXCESS","MISSING_EXIT_PLAN"], "expected_score_lt": 75.0, "should_auto_apply": False},
    {"scenario_id": "SC211-030", "schema_version": "211", "paper_only": True, "name": "零違規最高分", "description": "無任何violation，分數=100", "violation_codes": [], "expected_score": 100.0, "should_auto_apply": False},
    # --- 31-40: trade status scenarios ---
    {"scenario_id": "SC211-031", "schema_version": "211", "paper_only": True, "name": "trade_status=planned_only", "description": "只有計畫，尚未進場", "trade_status": "planned_only", "should_auto_apply": False},
    {"scenario_id": "SC211-032", "schema_version": "211", "paper_only": True, "name": "trade_status=entered", "description": "已進場", "trade_status": "entered", "should_auto_apply": False},
    {"scenario_id": "SC211-033", "schema_version": "211", "paper_only": True, "name": "trade_status=reduced", "description": "已減倉", "trade_status": "reduced", "should_auto_apply": False},
    {"scenario_id": "SC211-034", "schema_version": "211", "paper_only": True, "name": "trade_status=exited", "description": "已出場", "trade_status": "exited", "should_auto_apply": False},
    {"scenario_id": "SC211-035", "schema_version": "211", "paper_only": True, "name": "trade_status=stopped_out", "description": "觸發停損出場", "trade_status": "stopped_out", "should_auto_apply": False},
    {"scenario_id": "SC211-036", "schema_version": "211", "paper_only": True, "name": "trade_status=take_profit_done", "description": "已達停利", "trade_status": "take_profit_done", "should_auto_apply": False},
    {"scenario_id": "SC211-037", "schema_version": "211", "paper_only": True, "name": "trade_status=invalidated", "description": "計畫作廢", "trade_status": "invalidated", "should_auto_apply": False},
    {"scenario_id": "SC211-038", "schema_version": "211", "paper_only": True, "name": "trade_status=cancelled", "description": "已取消", "trade_status": "cancelled", "should_auto_apply": False},
    {"scenario_id": "SC211-039", "schema_version": "211", "paper_only": True, "name": "trade_status共8種", "description": "8種trade_status均支援", "trade_status_count": 8, "should_auto_apply": False},
    {"scenario_id": "SC211-040", "schema_version": "211", "paper_only": True, "name": "所有trade_status均為紙上狀態", "description": "trade_status不會觸發真實下單", "paper_only": True, "should_auto_apply": False},
    # --- 41-50: mistake tag scenarios ---
    {"scenario_id": "SC211-041", "schema_version": "211", "paper_only": True, "name": "mistake_tag=chasing_price", "description": "進場滑點>3%，tag=chasing_price", "entry_slippage_pct": 0.035, "expected_mistake_tag": "chasing_price", "should_auto_apply": False},
    {"scenario_id": "SC211-042", "schema_version": "211", "paper_only": True, "name": "mistake_tag=position_oversized", "description": "SIZE_DEVIATION_EXCESS，tag=position_oversized", "violation_codes": ["SIZE_DEVIATION_EXCESS"], "expected_mistake_tag": "position_oversized", "should_auto_apply": False},
    {"scenario_id": "SC211-043", "schema_version": "211", "paper_only": True, "name": "mistake_tag=stop_too_loose", "description": "STOP_DEVIATION_EXCESS，tag=stop_too_loose", "violation_codes": ["STOP_DEVIATION_EXCESS"], "expected_mistake_tag": "stop_too_loose", "should_auto_apply": False},
    {"scenario_id": "SC211-044", "schema_version": "211", "paper_only": True, "name": "mistake_tag=plan_not_followed", "description": "MISSING_EXIT_PLAN，tag=plan_not_followed", "violation_codes": ["MISSING_EXIT_PLAN"], "expected_mistake_tag": "plan_not_followed", "should_auto_apply": False},
    {"scenario_id": "SC211-045", "schema_version": "211", "paper_only": True, "name": "mistake_tag=unplanned_addon", "description": "UNPLANNED_ADD，tag=unplanned_addon", "violation_codes": ["UNPLANNED_ADD"], "expected_mistake_tag": "unplanned_addon", "should_auto_apply": False},
    {"scenario_id": "SC211-046", "schema_version": "211", "paper_only": True, "name": "mistake_tag=overtrading", "description": "OVERTRADE，tag=overtrading", "violation_codes": ["OVERTRADE"], "expected_mistake_tag": "overtrading", "should_auto_apply": False},
    {"scenario_id": "SC211-047", "schema_version": "211", "paper_only": True, "name": "mistake_tag=stop_moved_away", "description": "STOP_LOSS_VIOLATION，tag=stop_moved_away", "violation_codes": ["STOP_LOSS_VIOLATION"], "expected_mistake_tag": "stop_moved_away", "should_auto_apply": False},
    {"scenario_id": "SC211-048", "schema_version": "211", "paper_only": True, "name": "mistake_tag=missing_journal_entry", "description": "NO_PLANNED_ENTRY，tag=missing_journal_entry", "violation_codes": ["NO_PLANNED_ENTRY"], "expected_mistake_tag": "missing_journal_entry", "should_auto_apply": False},
    {"scenario_id": "SC211-049", "schema_version": "211", "paper_only": True, "name": "mistake_tags共9種", "description": "9種mistake_tag均支援", "mistake_tag_count": 9, "should_auto_apply": False},
    {"scenario_id": "SC211-050", "schema_version": "211", "paper_only": True, "name": "無違規無mistake_tag", "description": "零違規時，mistake_tags=[]", "violation_codes": [], "expected_mistake_tags": [], "should_auto_apply": False},
    # --- 51-60: discipline score scenarios ---
    {"scenario_id": "SC211-051", "schema_version": "211", "paper_only": True, "name": "基礎分數100分", "description": "無任何違規，基礎分數100", "violations": [], "expected_score": 100.0, "should_auto_apply": False},
    {"scenario_id": "SC211-052", "schema_version": "211", "paper_only": True, "name": "無計畫進場扣20分", "description": "has_planned_entry=False，扣20分", "has_planned_entry": False, "expected_deduction": 20.0, "should_auto_apply": False},
    {"scenario_id": "SC211-053", "schema_version": "211", "paper_only": True, "name": "進場滑點超標扣10分", "description": "entry_slippage>limit，扣10分", "expected_deduction": 10.0, "should_auto_apply": False},
    {"scenario_id": "SC211-054", "schema_version": "211", "paper_only": True, "name": "部位偏差超標扣10分", "description": "size_deviation>limit，扣10分", "expected_deduction": 10.0, "should_auto_apply": False},
    {"scenario_id": "SC211-055", "schema_version": "211", "paper_only": True, "name": "停損偏差超標扣10分", "description": "stop_deviation>limit，扣10分", "expected_deduction": 10.0, "should_auto_apply": False},
    {"scenario_id": "SC211-056", "schema_version": "211", "paper_only": True, "name": "缺少出場計畫扣15分", "description": "has_exit_plan=False，扣15分", "expected_deduction": 15.0, "should_auto_apply": False},
    {"scenario_id": "SC211-057", "schema_version": "211", "paper_only": True, "name": "無計畫加碼扣5分", "description": "is_unplanned_add=True，扣5分", "expected_deduction": 5.0, "should_auto_apply": False},
    {"scenario_id": "SC211-058", "schema_version": "211", "paper_only": True, "name": "停損未執行扣15分", "description": "stop_loss_violated=True，扣15分", "expected_deduction": 15.0, "should_auto_apply": False},
    {"scenario_id": "SC211-059", "schema_version": "211", "paper_only": True, "name": "分數最低為0", "description": "多重違規累積扣分不低於0", "max_deduction": 100.0, "expected_min_score": 0.0, "should_auto_apply": False},
    {"scenario_id": "SC211-060", "schema_version": "211", "paper_only": True, "name": "A等級分數>=90", "description": "avg_score>=90，discipline_quality_grade=A", "avg_score": 92.0, "expected_grade": "A", "should_auto_apply": False},
    # --- 61-70: discipline grade scenarios ---
    {"scenario_id": "SC211-061", "schema_version": "211", "paper_only": True, "name": "B等級分數75-90", "description": "avg_score=80，discipline_quality_grade=B", "avg_score": 80.0, "expected_grade": "B", "should_auto_apply": False},
    {"scenario_id": "SC211-062", "schema_version": "211", "paper_only": True, "name": "C等級分數50-75", "description": "avg_score=60，discipline_quality_grade=C", "avg_score": 60.0, "expected_grade": "C", "should_auto_apply": False},
    {"scenario_id": "SC211-063", "schema_version": "211", "paper_only": True, "name": "D等級分數<50", "description": "avg_score=40，discipline_quality_grade=D", "avg_score": 40.0, "expected_grade": "D", "should_auto_apply": False},
    {"scenario_id": "SC211-064", "schema_version": "211", "paper_only": True, "name": "計畫遵守率A>=90%", "description": "compliant>=90%，plan_adherence_grade=A", "compliant_pct": 0.92, "expected_grade": "A", "should_auto_apply": False},
    {"scenario_id": "SC211-065", "schema_version": "211", "paper_only": True, "name": "計畫遵守率B>=75%", "description": "compliant=80%，plan_adherence_grade=B", "compliant_pct": 0.80, "expected_grade": "B", "should_auto_apply": False},
    {"scenario_id": "SC211-066", "schema_version": "211", "paper_only": True, "name": "計畫遵守率C>=50%", "description": "compliant=60%，plan_adherence_grade=C", "compliant_pct": 0.60, "expected_grade": "C", "should_auto_apply": False},
    {"scenario_id": "SC211-067", "schema_version": "211", "paper_only": True, "name": "計畫遵守率D<50%", "description": "compliant=40%，plan_adherence_grade=D", "compliant_pct": 0.40, "expected_grade": "D", "should_auto_apply": False},
    {"scenario_id": "SC211-068", "schema_version": "211", "paper_only": True, "name": "空日誌N/A", "description": "total=0，grade=N/A", "total_count": 0, "expected_grade": "N/A", "should_auto_apply": False},
    {"scenario_id": "SC211-069", "schema_version": "211", "paper_only": True, "name": "全部compliant最高分", "description": "所有entry均compliant，discipline_quality_grade=A", "all_compliant": True, "expected_grade": "A", "should_auto_apply": False},
    {"scenario_id": "SC211-070", "schema_version": "211", "paper_only": True, "name": "等級評定不觸發自動操作", "description": "等級評定為建議，不自動調倉", "paper_only": True, "should_auto_apply": False},
    # --- 71-80: safety / paper-only / integration scenarios ---
    {"scenario_id": "SC211-071", "schema_version": "211", "paper_only": True, "name": "NO_REAL_ORDERS=True", "description": "paper_cockpit_v211.NO_REAL_ORDERS必須為True", "expected_no_real_orders": True, "should_auto_apply": False},
    {"scenario_id": "SC211-072", "schema_version": "211", "paper_only": True, "name": "BROKER_EXECUTION_ENABLED=False", "description": "paper_cockpit_v211.BROKER_EXECUTION_ENABLED必須為False", "expected_broker_enabled": False, "should_auto_apply": False},
    {"scenario_id": "SC211-073", "schema_version": "211", "paper_only": True, "name": "PRODUCTION_TRADING_BLOCKED=True", "description": "paper_cockpit_v211.PRODUCTION_TRADING_BLOCKED必須為True", "expected_production_blocked": True, "should_auto_apply": False},
    {"scenario_id": "SC211-074", "schema_version": "211", "paper_only": True, "name": "paper_only_safety_snapshot=True", "description": "journal_review結果的paper_only_safety_snapshot必須為True", "expected_safety_snapshot": True, "should_auto_apply": False},
    {"scenario_id": "SC211-075", "schema_version": "211", "paper_only": True, "name": "v2.0.10向下相容", "description": "paper_cockpit_v210.VERSION仍為2.0.10", "expected_v210_version": "2.0.10", "should_auto_apply": False},
    {"scenario_id": "SC211-076", "schema_version": "211", "paper_only": True, "name": "v2.0.9向下相容", "description": "paper_cockpit_v209.run_sizing_review可呼叫", "expected_v209_callable": True, "should_auto_apply": False},
    {"scenario_id": "SC211-077", "schema_version": "211", "paper_only": True, "name": "export_json有效", "description": "export_journal_json返回is_valid=True", "expected_is_valid": True, "should_auto_apply": False},
    {"scenario_id": "SC211-078", "schema_version": "211", "paper_only": True, "name": "export_md有效", "description": "export_journal_markdown返回is_valid=True", "expected_is_valid": True, "should_auto_apply": False},
    {"scenario_id": "SC211-079", "schema_version": "211", "paper_only": True, "name": "export_csv有效", "description": "export_journal_csv返回is_valid=True", "expected_is_valid": True, "should_auto_apply": False},
    {"scenario_id": "SC211-080", "schema_version": "211", "paper_only": True, "name": "journal_actions均為建議", "description": "所有日誌行動均為建議，不自動套用", "paper_only": True, "auto_apply_enabled": False, "should_auto_apply": False},
]

assert len(SCENARIOS) == 80, f"Expected 80 SCENARIOS, got {len(SCENARIOS)}"
assert all(s["schema_version"] == "211" for s in SCENARIOS)
assert all(s["paper_only"] is True for s in SCENARIOS)
assert all(s["should_auto_apply"] is False for s in SCENARIOS)
