"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v210.py
v2.0.10 Paper Exit Plan & Stop-Loss Discipline Control — Scenarios
[!] Paper Only. Research Only. Exit Plan Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "210"

SCENARIOS: List[Dict[str, Any]] = [
    # --- 1-10: exit plan basic scenarios ---
    {"scenario_id": "SC210-001", "schema_version": "210", "paper_only": True, "name": "標準出場計畫-台積電", "description": "停損6%、1R停利、標準出場計畫", "entry_price": 900.0, "stop_price": 855.0, "expected_stop_distance_pct": 0.05, "expected_rr_ratio_min": 1.0, "should_auto_apply": False},
    {"scenario_id": "SC210-002", "schema_version": "210", "paper_only": True, "name": "停損距離正常-允許進場", "description": "停損距離<=12%，R/R>=2，允許帶出場計畫進場", "entry_price": 100.0, "stop_price": 94.0, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"scenario_id": "SC210-003", "schema_version": "210", "paper_only": True, "name": "停損距離過大-要求收緊", "description": "停損距離>12%，要求收緊停損", "entry_price": 100.0, "stop_price": 85.0, "expected_exit_action": "require_tighter_stop", "should_auto_apply": False},
    {"scenario_id": "SC210-004", "schema_version": "210", "paper_only": True, "name": "無停損設定-阻擋進場", "description": "stop_price=0或無效，阻擋進場", "entry_price": 100.0, "stop_price": 0.0, "expected_exit_action": "block_entry_missing_stop", "should_auto_apply": False},
    {"scenario_id": "SC210-005", "schema_version": "210", "paper_only": True, "name": "停損高於進場價-阻擋", "description": "stop_price>entry_price，無效設定", "entry_price": 90.0, "stop_price": 100.0, "expected_stop_loss_valid": False, "should_auto_apply": False},
    {"scenario_id": "SC210-006", "schema_version": "210", "paper_only": True, "name": "R/R不足-阻擋進場", "description": "R/R<2，阻擋進場", "entry_price": 100.0, "stop_price": 98.0, "first_tp_price": 101.0, "expected_exit_action": "block_entry_bad_reward_risk", "should_auto_apply": False},
    {"scenario_id": "SC210-007", "schema_version": "210", "paper_only": True, "name": "所有exit_action均為建議", "description": "所有8種exit_action均為紙上建議，不自動執行", "exit_actions": ["allow_with_exit_plan","require_tighter_stop","reduce_size_before_entry","observation_only","block_entry_missing_stop","block_entry_bad_reward_risk","require_rescore","human_review_required"], "should_auto_apply": False, "auto_apply_enabled": False},
    {"scenario_id": "SC210-008", "schema_version": "210", "paper_only": True, "name": "require_stop_loss_before_entry=True", "description": "進場前必須有停損計畫", "require_stop_loss_before_entry": True, "should_auto_apply": False},
    {"scenario_id": "SC210-009", "schema_version": "210", "paper_only": True, "name": "auto_apply_enabled=False不變", "description": "__post_init__強制auto_apply_enabled=False", "input_auto_apply_enabled": True, "expected_auto_apply_enabled": False, "should_auto_apply": False},
    {"scenario_id": "SC210-010", "schema_version": "210", "paper_only": True, "name": "should_auto_apply=False不變", "description": "__post_init__強制should_auto_apply=False", "input_should_auto_apply": True, "expected_should_auto_apply": False, "should_auto_apply": False},
    # --- 11-20: stop-loss calculation scenarios ---
    {"scenario_id": "SC210-011", "schema_version": "210", "paper_only": True, "name": "停損距離5%計算正確", "description": "entry=100,stop=95，停損距離5%", "entry_price": 100.0, "stop_price": 95.0, "expected_stop_distance_pct": 0.05, "should_auto_apply": False},
    {"scenario_id": "SC210-012", "schema_version": "210", "paper_only": True, "name": "停損距離6%計算正確", "description": "entry=1000,stop=940，停損距離6%", "entry_price": 1000.0, "stop_price": 940.0, "expected_stop_distance_pct": 0.06, "should_auto_apply": False},
    {"scenario_id": "SC210-013", "schema_version": "210", "paper_only": True, "name": "停損距離12%邊界值", "description": "停損距離剛好=12%，允許", "entry_price": 100.0, "stop_price": 88.0, "expected_stop_distance_pct": 0.12, "should_auto_apply": False},
    {"scenario_id": "SC210-014", "schema_version": "210", "paper_only": True, "name": "停損距離13%-過大阻擋", "description": "停損距離13%>12%，要求收緊", "entry_price": 100.0, "stop_price": 87.0, "expected_exit_action": "require_tighter_stop", "should_auto_apply": False},
    {"scenario_id": "SC210-015", "schema_version": "210", "paper_only": True, "name": "最大虧損金額計算", "description": "max_loss_amount=account_equity*max_loss_pct", "account_equity": 300000.0, "max_loss_pct": 0.08, "expected_max_loss_amount": 24000.0, "should_auto_apply": False},
    {"scenario_id": "SC210-016", "schema_version": "210", "paper_only": True, "name": "停損有效性驗證-正常", "description": "stop<entry且stop>0，停損有效", "entry_price": 100.0, "stop_price": 94.0, "expected_stop_loss_valid": True, "should_auto_apply": False},
    {"scenario_id": "SC210-017", "schema_version": "210", "paper_only": True, "name": "停損有效性驗證-無效零", "description": "stop_price=0，停損無效", "entry_price": 100.0, "stop_price": 0.0, "expected_stop_loss_valid": False, "should_auto_apply": False},
    {"scenario_id": "SC210-018", "schema_version": "210", "paper_only": True, "name": "停損有效性驗證-反轉", "description": "stop>entry，停損無效", "entry_price": 90.0, "stop_price": 100.0, "expected_stop_loss_valid": False, "should_auto_apply": False},
    {"scenario_id": "SC210-019", "schema_version": "210", "paper_only": True, "name": "停損計畫進場必填", "description": "blocked_by_missing_stop=True時，exit_action=block_entry_missing_stop", "stop_price": 0.0, "expected_blocked_by_missing_stop": True, "should_auto_apply": False},
    {"scenario_id": "SC210-020", "schema_version": "210", "paper_only": True, "name": "停損計畫有效進場允許", "description": "stop_loss_valid=True且R/R充足，允許進場", "entry_price": 100.0, "stop_price": 94.0, "expected_stop_loss_valid": True, "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    # --- 21-30: take-profit scenarios ---
    {"scenario_id": "SC210-021", "schema_version": "210", "paper_only": True, "name": "第一停利目標1R", "description": "first_tp=entry+1R_risk", "entry_price": 100.0, "stop_price": 94.0, "expected_first_tp_price": 106.0, "should_auto_apply": False},
    {"scenario_id": "SC210-022", "schema_version": "210", "paper_only": True, "name": "第二停利目標2R", "description": "second_tp=entry+2R_risk", "entry_price": 100.0, "stop_price": 94.0, "expected_second_tp_price": 112.0, "should_auto_apply": False},
    {"scenario_id": "SC210-023", "schema_version": "210", "paper_only": True, "name": "追蹤停利設定", "description": "trailing_stop_price=entry*(1-trail_pct)", "entry_price": 100.0, "trail_pct": 0.03, "expected_trailing_stop_price": 97.0, "should_auto_apply": False},
    {"scenario_id": "SC210-024", "schema_version": "210", "paper_only": True, "name": "R/R=2標準目標", "description": "entry=100,stop=94,first_tp=112，R/R=2", "entry_price": 100.0, "stop_price": 94.0, "first_tp_price": 112.0, "expected_rr_ratio": 2.0, "should_auto_apply": False},
    {"scenario_id": "SC210-025", "schema_version": "210", "paper_only": True, "name": "R/R=3優良目標", "description": "entry=100,stop=97,first_tp=109，R/R=3", "entry_price": 100.0, "stop_price": 97.0, "first_tp_price": 109.0, "expected_rr_ratio": 3.0, "should_auto_apply": False},
    {"scenario_id": "SC210-026", "schema_version": "210", "paper_only": True, "name": "R/R=1不足-阻擋", "description": "R/R<2，阻擋進場", "entry_price": 100.0, "stop_price": 98.0, "first_tp_price": 102.0, "expected_rr_ratio": 1.0, "expected_blocked_bad_rr": True, "should_auto_apply": False},
    {"scenario_id": "SC210-027", "schema_version": "210", "paper_only": True, "name": "停損距離=0-TP無效", "description": "stop_distance=0，取profits點無效", "entry_price": 100.0, "stop_price": 100.0, "expected_first_tp_price": 100.0, "should_auto_apply": False},
    {"scenario_id": "SC210-028", "schema_version": "210", "paper_only": True, "name": "分批停利計畫-第一批1R", "description": "部分1R停利，部分追蹤停利", "partial_tp_1r": True, "partial_tp_trailing": True, "should_auto_apply": False},
    {"scenario_id": "SC210-029", "schema_version": "210", "paper_only": True, "name": "停利不自動執行", "description": "停利建議不自動執行，僅供參考", "auto_apply_take_profit": False, "should_auto_apply": False},
    {"scenario_id": "SC210-030", "schema_version": "210", "paper_only": True, "name": "停利快照記錄完整", "description": "take_profit_snapshot包含first_tp/second_tp/rr", "expected_tp_snapshot_keys": ["first_tp", "second_tp", "reward_risk_ratio"], "should_auto_apply": False},
    # --- 31-40: reward/risk validation scenarios ---
    {"scenario_id": "SC210-031", "schema_version": "210", "paper_only": True, "name": "R/R=2最低門檻驗證", "description": "min_reward_risk_ratio=2，剛好通過", "min_reward_risk_ratio": 2.0, "actual_rr": 2.0, "expected_pass": True, "should_auto_apply": False},
    {"scenario_id": "SC210-032", "schema_version": "210", "paper_only": True, "name": "R/R=1.9不足-阻擋", "description": "1.9<2.0，阻擋進場", "min_reward_risk_ratio": 2.0, "actual_rr": 1.9, "expected_exit_action": "block_entry_bad_reward_risk", "should_auto_apply": False},
    {"scenario_id": "SC210-033", "schema_version": "210", "paper_only": True, "name": "R/R=3良好-通過", "description": "3.0>=2.0，允許帶出場計畫進場", "min_reward_risk_ratio": 2.0, "actual_rr": 3.0, "expected_pass": True, "should_auto_apply": False},
    {"scenario_id": "SC210-034", "schema_version": "210", "paper_only": True, "name": "R/R=0無效-阻擋", "description": "rr_ratio=0，無法計算，阻擋", "actual_rr": 0.0, "expected_blocked_bad_rr": True, "should_auto_apply": False},
    {"scenario_id": "SC210-035", "schema_version": "210", "paper_only": True, "name": "R/R計算公式驗證", "description": "(tp-entry)/(entry-stop)=rr", "entry_price": 100.0, "stop_price": 95.0, "tp_price": 110.0, "expected_rr": 2.0, "should_auto_apply": False},
    {"scenario_id": "SC210-036", "schema_version": "210", "paper_only": True, "name": "R/R評估-多候選股平均", "description": "evaluate_reward_risk()計算平均R/R", "expected_avg_rr_positive": True, "should_auto_apply": False},
    {"scenario_id": "SC210-037", "schema_version": "210", "paper_only": True, "name": "R/R不足候選記錄", "description": "lowest_reward_risk_candidates記錄最差R/R", "expected_lowest_rr_list": True, "should_auto_apply": False},
    {"scenario_id": "SC210-038", "schema_version": "210", "paper_only": True, "name": "R/R=2.5-通過且縮減", "description": "R/R充足但高波動，reduce_size_before_entry", "actual_rr": 2.5, "is_high_volatility": True, "expected_exit_action": "reduce_size_before_entry", "should_auto_apply": False},
    {"scenario_id": "SC210-039", "schema_version": "210", "paper_only": True, "name": "R/R評估paper_only確認", "description": "evaluate_reward_risk()結果paper_only=True", "expected_paper_only": True, "should_auto_apply": False},
    {"scenario_id": "SC210-040", "schema_version": "210", "paper_only": True, "name": "R/R評估auto_apply=False", "description": "evaluate_reward_risk()結果auto_apply=False", "expected_should_auto_apply": False, "should_auto_apply": False},
    # --- 41-50: market regime exit scenarios ---
    {"scenario_id": "SC210-041", "schema_version": "210", "paper_only": True, "name": "risk_off-僅觀察模式", "description": "market_state=risk_off，觀察模式", "market_state": "risk_off", "expected_exit_action": "observation_only", "should_auto_apply": False},
    {"scenario_id": "SC210-042", "schema_version": "210", "paper_only": True, "name": "downtrend-人工審核", "description": "market_state=downtrend，需人工審核", "market_state": "downtrend", "expected_exit_action": "human_review_required", "should_auto_apply": False},
    {"scenario_id": "SC210-043", "schema_version": "210", "paper_only": True, "name": "range_bound-正常出場計畫", "description": "market_state=range_bound，正常出場計畫", "market_state": "range_bound", "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"scenario_id": "SC210-044", "schema_version": "210", "paper_only": True, "name": "strong_uptrend-正常出場計畫", "description": "market_state=strong_uptrend，正常出場計畫", "market_state": "strong_uptrend", "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"scenario_id": "SC210-045", "schema_version": "210", "paper_only": True, "name": "高波動市場-縮減前進場", "description": "is_high_volatility=True，縮減倉位再進場", "is_high_volatility": True, "expected_exit_action": "reduce_size_before_entry", "should_auto_apply": False},
    {"scenario_id": "SC210-046", "schema_version": "210", "paper_only": True, "name": "market_regime整合v2.0.7", "description": "出場計畫整合v2.0.7 market regime", "market_state_from_v207": "risk_off", "expected_blocked": True, "should_auto_apply": False},
    {"scenario_id": "SC210-047", "schema_version": "210", "paper_only": True, "name": "regime不同出場模式驗證", "description": "不同regime對應不同出場模式", "regime_exit_mode_map": {"risk_off": "observation_only", "downtrend": "human_review_required", "range_bound": "allow_with_exit_plan"}, "should_auto_apply": False},
    {"scenario_id": "SC210-048", "schema_version": "210", "paper_only": True, "name": "regime出場建議不自動執行", "description": "所有regime出場建議均只供參考", "auto_apply_exit": False, "should_auto_apply": False},
    {"scenario_id": "SC210-049", "schema_version": "210", "paper_only": True, "name": "risk_off整合停損紀律", "description": "risk_off+停損紀律=雙重保護", "market_state": "risk_off", "stop_loss_required": True, "should_auto_apply": False},
    {"scenario_id": "SC210-050", "schema_version": "210", "paper_only": True, "name": "市場趨勢警示", "description": "downtrend候選加入警示隊列", "market_state": "downtrend", "expected_in_warning_queue": True, "should_auto_apply": False},
    # --- 51-60: lifecycle and stop discipline scenarios ---
    {"scenario_id": "SC210-051", "schema_version": "210", "paper_only": True, "name": "expired候選-停損違規", "description": "lifecycle_state=expired，觀察模式不建倉", "lifecycle_state": "expired", "expected_exit_action": "observation_only", "should_auto_apply": False},
    {"scenario_id": "SC210-052", "schema_version": "210", "paper_only": True, "name": "cooldown候選-觀察模式", "description": "lifecycle_state=cooldown，觀察模式", "lifecycle_state": "cooldown", "expected_exit_action": "observation_only", "should_auto_apply": False},
    {"scenario_id": "SC210-053", "schema_version": "210", "paper_only": True, "name": "active候選-允許出場計畫", "description": "lifecycle_state=active，正常出場計畫", "lifecycle_state": "active", "expected_exit_action": "allow_with_exit_plan", "should_auto_apply": False},
    {"scenario_id": "SC210-054", "schema_version": "210", "paper_only": True, "name": "停損紀律評估-全通過", "description": "所有候選停損有效，停損紀律A", "expected_discipline_grade": "A", "should_auto_apply": False},
    {"scenario_id": "SC210-055", "schema_version": "210", "paper_only": True, "name": "停損紀律評估-部分失敗", "description": "部分候選停損無效，停損紀律C/D", "missing_stop_count": 3, "expected_low_grade": True, "should_auto_apply": False},
    {"scenario_id": "SC210-056", "schema_version": "210", "paper_only": True, "name": "停損違規隊列建立", "description": "build_stop_violation_queue()列出違規候選", "expected_violation_queue": True, "should_auto_apply": False},
    {"scenario_id": "SC210-057", "schema_version": "210", "paper_only": True, "name": "出場警示隊列建立", "description": "build_exit_warning_queue()列出警示候選", "expected_warning_queue": True, "should_auto_apply": False},
    {"scenario_id": "SC210-058", "schema_version": "210", "paper_only": True, "name": "人工審核升級", "description": "requires_human_review=True候選進入人工審核隊列", "requires_human_review": True, "expected_in_human_review_queue": True, "should_auto_apply": False},
    {"scenario_id": "SC210-059", "schema_version": "210", "paper_only": True, "name": "停損紀律品質評分", "description": "stop_discipline_quality_grade計算正確", "expected_quality_grade_in": ["A", "B", "C", "D", "N/A"], "should_auto_apply": False},
    {"scenario_id": "SC210-060", "schema_version": "210", "paper_only": True, "name": "出場計畫品質評分", "description": "exit_plan_quality_grade計算正確", "expected_quality_grade_in": ["A", "B", "C", "D", "N/A"], "should_auto_apply": False},
    # --- 61-70: integration and export scenarios ---
    {"scenario_id": "SC210-061", "schema_version": "210", "paper_only": True, "name": "整合v2.0.9倉位計算", "description": "出場計畫整合v2.0.9 position sizing", "integration_v209": True, "should_auto_apply": False},
    {"scenario_id": "SC210-062", "schema_version": "210", "paper_only": True, "name": "整合v2.0.8曝險控制", "description": "出場計畫整合v2.0.8 exposure control", "integration_v208": True, "should_auto_apply": False},
    {"scenario_id": "SC210-063", "schema_version": "210", "paper_only": True, "name": "整合v2.0.6候選生命週期", "description": "出場計畫整合v2.0.6 lifecycle", "integration_v206": True, "should_auto_apply": False},
    {"scenario_id": "SC210-064", "schema_version": "210", "paper_only": True, "name": "整合v2.0.5觀察名單", "description": "出場計畫整合v2.0.5 watchlist", "integration_v205": True, "should_auto_apply": False},
    {"scenario_id": "SC210-065", "schema_version": "210", "paper_only": True, "name": "出場計畫JSON匯出", "description": "export_exit_plan_json()返回ExitExportResult", "expected_export_format": "json", "should_auto_apply": False},
    {"scenario_id": "SC210-066", "schema_version": "210", "paper_only": True, "name": "出場計畫Markdown匯出", "description": "export_exit_plan_markdown()返回ExitExportResult", "expected_export_format": "markdown", "should_auto_apply": False},
    {"scenario_id": "SC210-067", "schema_version": "210", "paper_only": True, "name": "候選出場CSV匯出", "description": "export_candidate_exit_csv()返回CandidateExitCSV", "expected_export_type": "CandidateExitCSV", "should_auto_apply": False},
    {"scenario_id": "SC210-068", "schema_version": "210", "paper_only": True, "name": "停損紀律CSV匯出", "description": "export_stop_discipline_csv()返回StopDisciplineCSV", "expected_export_type": "StopDisciplineCSV", "should_auto_apply": False},
    {"scenario_id": "SC210-069", "schema_version": "210", "paper_only": True, "name": "出場警示CSV匯出", "description": "export_exit_warning_csv()返回ExitWarningCSV", "expected_export_type": "ExitWarningCSV", "should_auto_apply": False},
    {"scenario_id": "SC210-070", "schema_version": "210", "paper_only": True, "name": "稽核快照匯出", "description": "export_exit_audit_snapshot()返回ExitAuditSnapshot", "expected_export_type": "ExitAuditSnapshot", "should_auto_apply": False},
    # --- 71-80: safety invariants and edge cases ---
    {"scenario_id": "SC210-071", "schema_version": "210", "paper_only": True, "name": "paper_only安全旗標23項", "description": "SAFETY_FLAGS_V210有23項", "expected_safety_flag_count": 23, "should_auto_apply": False},
    {"scenario_id": "SC210-072", "schema_version": "210", "paper_only": True, "name": "no_real_orders=True不可更改", "description": "NO_REAL_ORDERS必須為True", "expected_no_real_orders": True, "should_auto_apply": False},
    {"scenario_id": "SC210-073", "schema_version": "210", "paper_only": True, "name": "broker_execution=False不可更改", "description": "BROKER_EXECUTION_ENABLED必須為False", "expected_broker_disabled": True, "should_auto_apply": False},
    {"scenario_id": "SC210-074", "schema_version": "210", "paper_only": True, "name": "production_trading=blocked不可更改", "description": "PRODUCTION_TRADING_BLOCKED必須為True", "expected_production_blocked": True, "should_auto_apply": False},
    {"scenario_id": "SC210-075", "schema_version": "210", "paper_only": True, "name": "出場計畫不自動套用", "description": "exit actions recommendation only，不自動套用", "should_auto_apply": False, "auto_apply_enabled": False},
    {"scenario_id": "SC210-076", "schema_version": "210", "paper_only": True, "name": "v2.0.9向後相容", "description": "v2.0.9功能不因v2.0.10受損", "backward_compat_v209": True, "should_auto_apply": False},
    {"scenario_id": "SC210-077", "schema_version": "210", "paper_only": True, "name": "v201健康檢查相對路徑相容", "description": "v201健康檢查相對路徑不回歸", "v201_health_compat": True, "should_auto_apply": False},
    {"scenario_id": "SC210-078", "schema_version": "210", "paper_only": True, "name": "時間停損規則", "description": "time_stop_days=20，超過20天觸發時間停損", "time_stop_days": 20, "days_held": 21, "expected_time_stop_triggered": True, "should_auto_apply": False},
    {"scenario_id": "SC210-079", "schema_version": "210", "paper_only": True, "name": "跳空下跌風險規則", "description": "gap_down_exit_pct=5%，跳空>5%觸發出場", "gap_down_exit_pct": 0.05, "actual_gap_pct": 0.06, "expected_gap_exit_triggered": True, "should_auto_apply": False},
    {"scenario_id": "SC210-080", "schema_version": "210", "paper_only": True, "name": "突破失敗出場規則", "description": "failed_breakout_days=5，5日內跌破進場價觸發出場", "failed_breakout_days": 5, "days_below_entry": 5, "expected_failed_breakout": True, "should_auto_apply": False},
]

assert len(SCENARIOS) == 80, f"Expected 80 scenarios, got {len(SCENARIOS)}"
assert all(s["schema_version"] == "210" for s in SCENARIOS), "All scenarios must have schema_version='210'"
assert all(s["paper_only"] is True for s in SCENARIOS), "All scenarios must have paper_only=True"
assert all(s["should_auto_apply"] is False for s in SCENARIOS), "All scenarios must have should_auto_apply=False"
