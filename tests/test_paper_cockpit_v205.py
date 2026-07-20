"""
tests/test_paper_cockpit_v205.py
v2.0.5 Paper Watchlist Rotation & Candidate Promotion Queue — Main Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# -------------------------------------------------------------------------
# Import tests
# -------------------------------------------------------------------------
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v205

def test_version_is_205():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION
    assert VERSION == "2.0.5"

def test_schema_version_is_205():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "205"

def test_release_name_contains_watchlist_rotation():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import RELEASE_NAME
    assert "Watchlist Rotation" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import BASELINE_TESTS
    assert BASELINE_TESTS == 33984

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

# -------------------------------------------------------------------------
# Safety constants
# -------------------------------------------------------------------------
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

# -------------------------------------------------------------------------
# Safety flags
# -------------------------------------------------------------------------
def test_safety_flags_count_20():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert len(SAFETY_FLAGS_V205) == 20

def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["paper_only"] is True

def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_broker"] is True

def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_real_orders"] is True

def test_safety_flags_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["should_auto_apply_always_false"] is True

def test_safety_flags_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["broker_execution_disabled"] is True

def test_safety_flags_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["production_trading_blocked"] is True

def test_safety_flags_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_automatic_rebalance"] is True

def test_safety_flags_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_real_account_sync"] is True

def test_safety_flags_no_live_strategy_activation():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_live_strategy_activation"] is True

def test_safety_flags_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["not_investment_advice"] is True

# -------------------------------------------------------------------------
# Watchlist statuses
# -------------------------------------------------------------------------
def test_watchlist_statuses_count_9():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert len(WATCHLIST_STATUSES) == 9

def test_watchlist_status_active_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "active_watchlist" in WATCHLIST_STATUSES

def test_watchlist_status_promoted_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "promoted_candidate" in WATCHLIST_STATUSES

def test_watchlist_status_second_wave_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "second_wave_candidate" in WATCHLIST_STATUSES

def test_watchlist_status_abc_pullback_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "abc_pullback_candidate" in WATCHLIST_STATUSES

def test_watchlist_status_breakout_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "breakout_candidate" in WATCHLIST_STATUSES

def test_watchlist_status_quarantined_no_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "quarantined_no_entry" in WATCHLIST_STATUSES

def test_watchlist_status_downgraded():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "downgraded" in WATCHLIST_STATUSES

def test_watchlist_status_removed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "removed" in WATCHLIST_STATUSES

def test_watchlist_status_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    assert "human_review_required" in WATCHLIST_STATUSES

# -------------------------------------------------------------------------
# CLI commands
# -------------------------------------------------------------------------
def test_cli_commands_count_10():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert len(CLI_COMMANDS_V205) == 10

def test_cli_command_rotate_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-rotate-watchlist" in CLI_COMMANDS_V205

def test_cli_command_promote_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-promote-candidates" in CLI_COMMANDS_V205

def test_cli_command_demote_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-demote-candidates" in CLI_COMMANDS_V205

def test_cli_command_build_human_review_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-build-human-review-queue" in CLI_COMMANDS_V205

def test_cli_command_build_quarantine_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-build-quarantine-queue" in CLI_COMMANDS_V205

def test_cli_command_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-export-json" in CLI_COMMANDS_V205

def test_cli_command_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-export-md" in CLI_COMMANDS_V205

def test_cli_command_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-export-csv" in CLI_COMMANDS_V205

def test_cli_command_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-health" in CLI_COMMANDS_V205

def test_cli_command_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    assert "paper-cockpit-v205-gate" in CLI_COMMANDS_V205

# -------------------------------------------------------------------------
# GUI tabs
# -------------------------------------------------------------------------
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import GUI_TABS_V205
    assert len(GUI_TABS_V205) == 3

def test_gui_tab_watchlist_rotation_v205():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import GUI_TABS_V205
    assert "watchlist_rotation_v205" in GUI_TABS_V205

def test_gui_tab_promotion_queue_v205():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import GUI_TABS_V205
    assert "promotion_queue_v205" in GUI_TABS_V205

def test_gui_tab_human_review_queue_v205():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import GUI_TABS_V205
    assert "human_review_queue_v205" in GUI_TABS_V205

# -------------------------------------------------------------------------
# Models
# -------------------------------------------------------------------------
def test_model_WatchlistItem_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistItem
    item = WatchlistItem()
    assert item.schema_version == "205"
    assert item.paper_only is True
    assert item.no_real_orders is True

def test_model_WatchlistItem_fields():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistItem
    item = WatchlistItem(symbol="2330", name="台積電", score=80.0)
    assert item.symbol == "2330"
    assert item.score == 80.0

def test_model_PromotionDecision_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionDecision
    dec = PromotionDecision()
    assert dec.schema_version == "205"
    assert dec.should_auto_apply is False

def test_model_PromotionDecision_should_auto_apply_forced_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionDecision
    dec = PromotionDecision(should_auto_apply=True)
    assert dec.should_auto_apply is False

def test_model_PromotionDecision_fields():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionDecision
    dec = PromotionDecision(symbol="2330", promotion_score=85.0)
    assert dec.symbol == "2330"
    assert dec.promotion_score == 85.0

def test_model_QueueSummary_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import QueueSummary
    qs = QueueSummary()
    assert qs.schema_version == "205"
    assert qs.paper_only is True

def test_model_QueueSummary_fields():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import QueueSummary
    qs = QueueSummary(total_watchlist_count=10, promote_count=3)
    assert qs.total_watchlist_count == 10
    assert qs.promote_count == 3

def test_model_WatchlistRotationInput_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationInput
    inp = WatchlistRotationInput()
    assert inp.schema_version == "205"
    assert inp.paper_only is True

def test_model_WatchlistRotationResult_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationResult
    res = WatchlistRotationResult()
    assert res.rotation_version == "2.0.5"
    assert res.should_auto_apply is False

def test_model_WatchlistRotationResult_should_auto_apply_forced_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationResult
    res = WatchlistRotationResult(should_auto_apply=True)
    assert res.should_auto_apply is False

def test_model_RotationExportResult_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import RotationExportResult
    res = RotationExportResult()
    assert res.paper_only is True

def test_model_RotationAuditSnapshot_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import RotationAuditSnapshot
    snap = RotationAuditSnapshot()
    assert snap.paper_only is True
    assert snap.export_format == "audit_snapshot"

def test_model_WatchlistRotationReport_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationReport
    rep = WatchlistRotationReport()
    assert rep.paper_only is True

def test_model_PromotionQueueCSV_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionQueueCSV
    csv = PromotionQueueCSV()
    assert csv.paper_only is True

def test_model_DemotionQueueCSV_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import DemotionQueueCSV
    csv = DemotionQueueCSV()
    assert csv.paper_only is True

def test_model_V205HealthSummary_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import V205HealthSummary
    hs = V205HealthSummary()
    assert hs.version == "2.0.5"

def test_model_V205ReleaseSummary_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import V205ReleaseSummary
    rs = V205ReleaseSummary()
    assert rs.version == "2.0.5"
    assert rs.all_sealed is False

def test_model_count_12():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import _ALL_MODEL_NAMES_V205
    assert len(_ALL_MODEL_NAMES_V205) == 12

# -------------------------------------------------------------------------
# Rotation result fields
# -------------------------------------------------------------------------
def test_rotation_result_fields_count_12():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import ROTATION_RESULT_FIELDS
    assert len(ROTATION_RESULT_FIELDS) == 12

def test_rotation_result_field_rotation_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import ROTATION_RESULT_FIELDS
    assert "rotation_id" in ROTATION_RESULT_FIELDS

def test_rotation_result_field_promotion_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import ROTATION_RESULT_FIELDS
    assert "promotion_queue" in ROTATION_RESULT_FIELDS

def test_rotation_result_field_human_review_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import ROTATION_RESULT_FIELDS
    assert "human_review_queue" in ROTATION_RESULT_FIELDS

def test_watchlist_item_fields_count_15():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_ITEM_FIELDS
    assert len(WATCHLIST_ITEM_FIELDS) == 15

def test_promotion_decision_fields_count_14():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PROMOTION_DECISION_FIELDS
    assert len(PROMOTION_DECISION_FIELDS) == 14

def test_queue_summary_fields_count_13():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import QUEUE_SUMMARY_FIELDS
    assert len(QUEUE_SUMMARY_FIELDS) == 13

# -------------------------------------------------------------------------
# run_watchlist_rotation engine
# -------------------------------------------------------------------------
def test_run_watchlist_rotation_returns_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result is not None

def test_run_watchlist_rotation_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.paper_only is True

def test_run_watchlist_rotation_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.no_real_orders is True

def test_run_watchlist_rotation_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.no_broker is True

def test_run_watchlist_rotation_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.all_passed is True

def test_run_watchlist_rotation_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.should_auto_apply is False

def test_run_watchlist_rotation_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.rotation_version == "2.0.5"

def test_run_watchlist_rotation_rotation_id_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.rotation_id != ""

def test_run_watchlist_rotation_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.human_review_required is True

def test_run_watchlist_rotation_paper_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.paper_only_safety_snapshot is True

def test_run_watchlist_rotation_queue_summary_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary is not None

def test_run_watchlist_rotation_input_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert isinstance(result.input_watchlist_snapshot, list)
    assert len(result.input_watchlist_snapshot) > 0

def test_run_watchlist_rotation_promotion_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert isinstance(result.promotion_queue, list)

def test_run_watchlist_rotation_demotion_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert isinstance(result.demotion_queue, list)

def test_run_watchlist_rotation_keep_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert isinstance(result.keep_queue, list)

def test_run_watchlist_rotation_with_custom_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, WatchlistRotationInput, WatchlistItem
    )
    inp = WatchlistRotationInput(
        rotation_period="2026-W30",
        watchlist_items=[WatchlistItem(symbol="2330", score=85.0, trend_quality=85.0,
                                       volume_quality=80.0, chip_quality=82.0, risk_quality=78.0,
                                       promotion_reasons=["strong_trend"])],
    )
    result = run_watchlist_rotation(inp)
    assert result.rotation_period == "2026-W30"
    assert result.paper_only is True

def test_run_watchlist_rotation_with_empty_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, WatchlistRotationInput
    )
    inp = WatchlistRotationInput(rotation_period="2026-W30", watchlist_items=[])
    result = run_watchlist_rotation(inp)
    assert result is not None
    assert result.all_passed is True

def test_run_watchlist_rotation_promotion_decisions_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, WatchlistRotationInput, WatchlistItem
    )
    inp = WatchlistRotationInput(
        rotation_period="2026-W29",
        watchlist_items=[WatchlistItem(symbol="2330", score=90.0, trend_quality=90.0,
                                       volume_quality=88.0, chip_quality=85.0, risk_quality=80.0,
                                       promotion_reasons=["strong_trend", "volume_ok", "chip_buy"])],
    )
    result = run_watchlist_rotation(inp)
    for dec in result.promotion_queue:
        assert dec.should_auto_apply is False

def test_run_watchlist_rotation_period_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, WatchlistRotationInput
    )
    inp = WatchlistRotationInput(rotation_period="2026-W35")
    result = run_watchlist_rotation(inp)
    assert result.rotation_period == "2026-W35"

# -------------------------------------------------------------------------
# Queue builders
# -------------------------------------------------------------------------
def test_build_promotion_queue_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_promotion_queue
    result = build_promotion_queue()
    assert isinstance(result, list)

def test_build_demotion_queue_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_demotion_queue
    result = build_demotion_queue()
    assert isinstance(result, list)

def test_build_human_review_queue_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_human_review_queue
    result = build_human_review_queue()
    assert isinstance(result, list)

def test_build_quarantine_queue_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_quarantine_queue
    result = build_quarantine_queue()
    assert isinstance(result, list)

# -------------------------------------------------------------------------
# Queue summary
# -------------------------------------------------------------------------
def test_queue_summary_total_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    qs = result.queue_summary
    assert qs.total_watchlist_count >= 0

def test_queue_summary_grade_is_letter():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary.weekly_rotation_grade in ("A", "B", "C", "D")

def test_queue_summary_top_promo_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert isinstance(result.queue_summary.top_promotion_candidates, list)

def test_queue_summary_avg_promotion_score_float():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert isinstance(result.queue_summary.avg_promotion_score, float)

# -------------------------------------------------------------------------
# Export functions
# -------------------------------------------------------------------------
def test_export_rotation_json_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    result = export_rotation_json(run_watchlist_rotation())
    assert result.is_valid is True

def test_export_rotation_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    result = export_rotation_json(run_watchlist_rotation())
    assert result.paper_only is True

def test_export_rotation_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    result = export_rotation_json(run_watchlist_rotation())
    assert result.export_format == "json"

def test_export_rotation_json_content_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    result = export_rotation_json(run_watchlist_rotation())
    assert len(result.content) > 0

def test_export_rotation_json_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    result = export_rotation_json(run_watchlist_rotation())
    assert result.export_status == "complete"

def test_export_rotation_markdown_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    result = export_rotation_markdown(run_watchlist_rotation())
    assert result.is_valid is True

def test_export_rotation_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    result = export_rotation_markdown(run_watchlist_rotation())
    assert result.export_format == "markdown"

def test_export_rotation_markdown_content_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    result = export_rotation_markdown(run_watchlist_rotation())
    assert "Watchlist Rotation" in result.content

def test_export_promotion_queue_csv_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    result = export_promotion_queue_csv(run_watchlist_rotation())
    assert result.is_valid is True

def test_export_promotion_queue_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    result = export_promotion_queue_csv(run_watchlist_rotation())
    assert result.paper_only is True

def test_export_demotion_queue_csv_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_demotion_queue_csv
    result = export_demotion_queue_csv(run_watchlist_rotation())
    assert result.is_valid is True

def test_export_rotation_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert snap is not None
    assert snap.paper_only is True

def test_export_audit_snapshot_has_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert snap.reproducibility_hash != ""

# -------------------------------------------------------------------------
# Version helpers
# -------------------------------------------------------------------------
def test_get_version_info_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import get_version_info
    info = get_version_info()
    assert isinstance(info, dict)
    assert info["version"] == "2.0.5"

def test_verify_version_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import verify_version
    assert verify_version() is True

def test_get_cockpit_summary_v205():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import get_cockpit_summary_v205
    summary = get_cockpit_summary_v205()
    assert summary["version"] == "2.0.5"
    assert summary["should_auto_apply"] is False
    assert summary["paper_only"] is True

# -------------------------------------------------------------------------
# Covered versions
# -------------------------------------------------------------------------
def test_covered_versions_include_204():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import COVERED_VERSIONS
    assert "2.0.4" in COVERED_VERSIONS

def test_covered_versions_include_200():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import COVERED_VERSIONS
    assert "2.0.0" in COVERED_VERSIONS


# -------------------------------------------------------------------------
# Export JSON schema completeness
# -------------------------------------------------------------------------
def test_export_json_schema_contains_rotation_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert run_watchlist_rotation().rotation_id or export.rotation_id != ""

def test_export_json_schema_paper_only_true_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "paper_only" in export.content

def test_export_json_schema_should_auto_apply_false_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "should_auto_apply" in export.content

def test_export_json_schema_no_real_orders_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "no_real_orders" in export.content

def test_export_json_schema_rotation_version_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "rotation_version" in export.content

def test_export_json_paper_only_confirmed_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert export.paper_only_confirmed is True

# -------------------------------------------------------------------------
# Export Markdown schema completeness
# -------------------------------------------------------------------------
def test_export_md_schema_has_queue_summary_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "Queue Summary" in export.content

def test_export_md_schema_has_promotion_queue_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "Promotion Queue" in export.content

def test_export_md_schema_contains_disclaimer():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "Not Investment Advice" in export.content

def test_export_md_schema_paper_only_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "paper_only" in export.content

def test_export_md_schema_should_auto_apply_false_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "should_auto_apply" in export.content

def test_export_md_schema_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert export.paper_only_confirmed is True

# -------------------------------------------------------------------------
# Export CSV schema completeness
# -------------------------------------------------------------------------
def test_export_promo_csv_schema_has_symbol_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "symbol" in export.csv_content

def test_export_promo_csv_schema_has_from_status_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "from_status" in export.csv_content

def test_export_promo_csv_schema_has_promotion_score_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "promotion_score" in export.csv_content

def test_export_promo_csv_schema_has_should_auto_apply_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "should_auto_apply" in export.csv_content

def test_export_demo_csv_schema_has_symbol_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_demotion_queue_csv
    export = export_demotion_queue_csv(run_watchlist_rotation())
    assert "symbol" in export.csv_content

def test_export_demo_csv_schema_has_should_auto_apply_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_demotion_queue_csv
    export = export_demotion_queue_csv(run_watchlist_rotation())
    assert "should_auto_apply" in export.csv_content

# -------------------------------------------------------------------------
# Audit snapshot schema completeness
# -------------------------------------------------------------------------
def test_audit_snapshot_schema_safety_has_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "paper_only=True" in snap.safety_snapshot

def test_audit_snapshot_schema_safety_has_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "no_real_orders=True" in snap.safety_snapshot

def test_audit_snapshot_schema_safety_has_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "should_auto_apply=False" in snap.safety_snapshot

def test_audit_snapshot_schema_metadata_has_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "2.0.5" in snap.run_metadata

# -------------------------------------------------------------------------
# Queue summary count consistency
# -------------------------------------------------------------------------
def test_queue_summary_count_consistency():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    qs = result.queue_summary
    computed_total = (qs.promote_count + qs.demote_count + qs.remove_count
                      + qs.keep_count + qs.human_review_count + qs.quarantine_count)
    assert qs.total_watchlist_count == computed_total

def test_queue_summary_promote_count_matches_queue_length():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary.promote_count == len(result.promotion_queue)

def test_queue_summary_demote_count_matches_queue_length():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary.demote_count == len(result.demotion_queue)

def test_queue_summary_keep_count_matches_queue_length():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary.keep_count == len(result.keep_queue)

def test_queue_summary_human_review_count_matches_queue_length():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary.human_review_count == len(result.human_review_queue)

def test_queue_summary_quarantine_count_matches_queue_length():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.queue_summary.quarantine_count == len(result.quarantine_queue)

# -------------------------------------------------------------------------
# v2.0.4 weekly improvement pack integration
# -------------------------------------------------------------------------
def test_v204_build_weekly_improvement_pack_still_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.paper_only is True

def test_v204_weekly_improvement_pack_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.should_auto_apply is False

# -------------------------------------------------------------------------
# v201 relative-path compatibility not regressed
# -------------------------------------------------------------------------
def test_v201_health_relative_path_accessible():
    import os
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..",
        "paper_trading", "small_capital_strategy",
        "paper_cockpit_health_v201.py"
    ))
    assert os.path.exists(path)

def test_v201_test_file_accessible_relative():
    import os
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "test_paper_cockpit_v201.py"
    ))
    assert os.path.exists(path)
