"""
tests/test_paper_cockpit_v211.py
v2.0.11 Paper Trade Journal & Execution Discipline Review — Main Tests
[!] Paper Only. Research Only. Journal Review Recommendation Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Section 1: Module import & version constants
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v211

def test_version_is_211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VERSION
    assert VERSION == "2.0.11"

def test_schema_version_is_211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "211"

def test_release_name_contains_journal():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import RELEASE_NAME
    assert "Journal" in RELEASE_NAME or "Trade" in RELEASE_NAME

def test_release_name_contains_discipline():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import RELEASE_NAME
    assert "Discipline" in RELEASE_NAME or "Execution" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import BASELINE_TESTS
    assert BASELINE_TESTS == 35613

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import verify_version
    assert verify_version() is True


# =========================================================================
# Section 2: Safety constants
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Section 3: EXECUTION_ACTIONS
# =========================================================================
def test_execution_actions_count_7():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert len(EXECUTION_ACTIONS) == 7

def test_execution_action_compliant():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "compliant" in EXECUTION_ACTIONS

def test_execution_action_monitor():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "monitor" in EXECUTION_ACTIONS

def test_execution_action_require_journal_note():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "require_journal_note" in EXECUTION_ACTIONS

def test_execution_action_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "require_rescore" in EXECUTION_ACTIONS

def test_execution_action_flag_discipline_warning():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "flag_discipline_warning" in EXECUTION_ACTIONS

def test_execution_action_block_followup_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "block_followup_action" in EXECUTION_ACTIONS

def test_execution_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    assert "human_review_required" in EXECUTION_ACTIONS


# =========================================================================
# Section 4: TRADE_STATUSES
# =========================================================================
def test_trade_statuses_count_8():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert len(TRADE_STATUSES) == 8

def test_trade_status_planned_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "planned_only" in TRADE_STATUSES

def test_trade_status_entered():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "entered" in TRADE_STATUSES

def test_trade_status_reduced():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "reduced" in TRADE_STATUSES

def test_trade_status_exited():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "exited" in TRADE_STATUSES

def test_trade_status_stopped_out():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "stopped_out" in TRADE_STATUSES

def test_trade_status_take_profit_done():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "take_profit_done" in TRADE_STATUSES

def test_trade_status_invalidated():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "invalidated" in TRADE_STATUSES

def test_trade_status_cancelled():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    assert "cancelled" in TRADE_STATUSES


# =========================================================================
# Section 5: VIOLATION_CODES
# =========================================================================
def test_violation_codes_count_8():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert len(VIOLATION_CODES) == 8

def test_violation_code_entry_slippage():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "ENTRY_SLIPPAGE_EXCESS" in VIOLATION_CODES

def test_violation_code_size_deviation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "SIZE_DEVIATION_EXCESS" in VIOLATION_CODES

def test_violation_code_stop_deviation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "STOP_DEVIATION_EXCESS" in VIOLATION_CODES

def test_violation_code_missing_exit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "MISSING_EXIT_PLAN" in VIOLATION_CODES

def test_violation_code_unplanned_add():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "UNPLANNED_ADD" in VIOLATION_CODES

def test_violation_code_overtrade():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "OVERTRADE" in VIOLATION_CODES

def test_violation_code_stop_loss_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "STOP_LOSS_VIOLATION" in VIOLATION_CODES

def test_violation_code_no_planned_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VIOLATION_CODES
    assert "NO_PLANNED_ENTRY" in VIOLATION_CODES


# =========================================================================
# Section 6: MISTAKE_TAGS
# =========================================================================
def test_mistake_tags_count_9():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert len(MISTAKE_TAGS) == 9

def test_mistake_tag_chasing_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "chasing_price" in MISTAKE_TAGS

def test_mistake_tag_position_oversized():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "position_oversized" in MISTAKE_TAGS

def test_mistake_tag_stop_too_loose():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "stop_too_loose" in MISTAKE_TAGS

def test_mistake_tag_plan_not_followed():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "plan_not_followed" in MISTAKE_TAGS

def test_mistake_tag_unplanned_addon():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "unplanned_addon" in MISTAKE_TAGS

def test_mistake_tag_overtrading():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "overtrading" in MISTAKE_TAGS

def test_mistake_tag_stop_moved_away():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "stop_moved_away" in MISTAKE_TAGS

def test_mistake_tag_missing_journal_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "missing_journal_entry" in MISTAKE_TAGS

def test_mistake_tag_position_undersized():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MISTAKE_TAGS
    assert "position_undersized" in MISTAKE_TAGS


# =========================================================================
# Section 7: CLI commands
# =========================================================================
def test_cli_commands_count_10():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert len(CLI_COMMANDS_V211) == 10

def test_cli_cmd_review_journal():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-review-journal" in CLI_COMMANDS_V211

def test_cli_cmd_evaluate_discipline():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-evaluate-discipline" in CLI_COMMANDS_V211

def test_cli_cmd_build_mistake_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-build-mistake-queue" in CLI_COMMANDS_V211

def test_cli_cmd_build_violation_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-build-violation-queue" in CLI_COMMANDS_V211

def test_cli_cmd_build_improvement_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-build-improvement-queue" in CLI_COMMANDS_V211

def test_cli_cmd_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-export-json" in CLI_COMMANDS_V211

def test_cli_cmd_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-export-md" in CLI_COMMANDS_V211

def test_cli_cmd_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-export-csv" in CLI_COMMANDS_V211

def test_cli_cmd_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-health" in CLI_COMMANDS_V211

def test_cli_cmd_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert "paper-cockpit-v211-gate" in CLI_COMMANDS_V211


# =========================================================================
# Section 8: GUI tabs
# =========================================================================
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import GUI_TABS_V211
    assert len(GUI_TABS_V211) == 3

def test_gui_tab_trade_journal_v211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import GUI_TABS_V211
    assert "trade_journal_v211" in GUI_TABS_V211

def test_gui_tab_execution_discipline_v211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import GUI_TABS_V211
    assert "execution_discipline_v211" in GUI_TABS_V211

def test_gui_tab_mistake_review_queue_v211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import GUI_TABS_V211
    assert "mistake_review_queue_v211" in GUI_TABS_V211


# =========================================================================
# Section 9: SAFETY_FLAGS_V211
# =========================================================================
def test_safety_flags_count_24():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert len(SAFETY_FLAGS_V211) == 24

def test_safety_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["paper_only"] is True

def test_safety_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["research_only"] is True

def test_safety_journal_review_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["journal_review_recommendation_only"] is True

def test_safety_journal_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["journal_actions_recommendation_only"] is True

def test_safety_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_real_orders"] is True

def test_safety_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_broker"] is True

def test_safety_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["should_auto_apply_always_false"] is True

def test_safety_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["auto_apply_enabled_always_false"] is True

def test_safety_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["broker_execution_disabled"] is True

def test_safety_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["production_trading_blocked"] is True

def test_safety_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_rebalance"] is True

def test_safety_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_real_account_sync"] is True

def test_safety_no_automatic_journal_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_journal_apply"] is True

def test_safety_no_automatic_stop_loss_execution():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_stop_loss_execution"] is True

def test_safety_no_automatic_take_profit_execution():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_take_profit_execution"] is True

def test_safety_require_planned_entry_before_trade_always_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["require_planned_entry_before_trade_always_true"] is True

def test_safety_journal_actions_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["journal_actions_paper_only"] is True

def test_safety_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["not_investment_advice"] is True


# =========================================================================
# Section 10: Field list counts
# =========================================================================
def test_journal_review_fields_count_11():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_REVIEW_FIELDS
    assert len(JOURNAL_REVIEW_FIELDS) == 11

def test_trade_journal_policy_fields_count_11():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_JOURNAL_POLICY_FIELDS
    assert len(TRADE_JOURNAL_POLICY_FIELDS) == 11

def test_journal_entry_fields_count_26():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_ENTRY_FIELDS
    assert len(JOURNAL_ENTRY_FIELDS) == 26

def test_execution_discipline_summary_fields_count_16():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_DISCIPLINE_SUMMARY_FIELDS
    assert len(EXECUTION_DISCIPLINE_SUMMARY_FIELDS) == 16

def test_journal_review_fields_contains_journal_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_REVIEW_FIELDS
    assert "journal_review_id" in JOURNAL_REVIEW_FIELDS

def test_journal_review_fields_contains_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_REVIEW_FIELDS
    assert "paper_only_safety_snapshot" in JOURNAL_REVIEW_FIELDS

def test_policy_fields_contains_require_planned_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_JOURNAL_POLICY_FIELDS
    assert "require_planned_entry_before_trade" in TRADE_JOURNAL_POLICY_FIELDS

def test_policy_fields_contains_auto_apply_enabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_JOURNAL_POLICY_FIELDS
    assert "auto_apply_enabled" in TRADE_JOURNAL_POLICY_FIELDS

def test_entry_fields_contains_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_ENTRY_FIELDS
    assert "should_auto_apply" in JOURNAL_ENTRY_FIELDS

def test_entry_fields_contains_violation_codes():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_ENTRY_FIELDS
    assert "violation_codes" in JOURNAL_ENTRY_FIELDS

def test_entry_fields_contains_execution_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JOURNAL_ENTRY_FIELDS
    assert "execution_action" in JOURNAL_ENTRY_FIELDS

def test_discipline_summary_fields_contains_discipline_quality_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_DISCIPLINE_SUMMARY_FIELDS
    assert "discipline_quality_grade" in EXECUTION_DISCIPLINE_SUMMARY_FIELDS

def test_discipline_summary_fields_contains_plan_adherence_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_DISCIPLINE_SUMMARY_FIELDS
    assert "plan_adherence_grade" in EXECUTION_DISCIPLINE_SUMMARY_FIELDS


# =========================================================================
# Section 11: Dataclass models
# =========================================================================
def test_model_count_15():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _ALL_MODEL_NAMES_V211
    assert len(_ALL_MODEL_NAMES_V211) == 15

def test_model_trade_journal_policy_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p is not None

def test_model_journal_entry_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalEntry
    e = JournalEntry()
    assert e is not None

def test_model_execution_discipline_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import ExecutionDisciplineSummary
    s = ExecutionDisciplineSummary()
    assert s is not None

def test_model_journal_review_input_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalReviewInput
    i = JournalReviewInput()
    assert i is not None

def test_model_journal_review_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalReviewResult
    r = JournalReviewResult()
    assert r is not None

def test_model_journal_export_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalExportResult
    e = JournalExportResult()
    assert e is not None

def test_model_journal_audit_snapshot_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalAuditSnapshot
    a = JournalAuditSnapshot()
    assert a is not None

def test_model_journal_markdown_report_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalMarkdownReport
    m = JournalMarkdownReport()
    assert m is not None

def test_model_journal_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalCSV
    c = JournalCSV()
    assert c is not None

def test_model_execution_discipline_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import ExecutionDisciplineCSV
    c = ExecutionDisciplineCSV()
    assert c is not None

def test_model_mistake_review_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import MistakeReviewCSV
    c = MistakeReviewCSV()
    assert c is not None

def test_model_violation_queue_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import ViolationQueueCSV
    c = ViolationQueueCSV()
    assert c is not None

def test_model_v211_health_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import V211HealthSummary
    h = V211HealthSummary()
    assert h is not None

def test_model_v211_release_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import V211ReleaseSummary
    r = V211ReleaseSummary()
    assert r is not None

def test_model_journal_safety_guard_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g is not None


# =========================================================================
# Section 12: require_planned_entry_before_trade always True
# =========================================================================
def test_policy_require_planned_entry_before_trade_default_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.require_planned_entry_before_trade is True

def test_policy_require_planned_entry_before_trade_forced_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy(require_planned_entry_before_trade=False)
    assert p.require_planned_entry_before_trade is True

def test_policy_auto_apply_enabled_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.auto_apply_enabled is False

def test_policy_auto_apply_enabled_forced_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy(auto_apply_enabled=True)
    assert p.auto_apply_enabled is False

def test_policy_schema_version_211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.schema_version == "211"

def test_policy_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.paper_only is True

def test_policy_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.no_real_orders is True

def test_policy_default_slippage_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.max_allowed_entry_slippage_pct == 0.02

def test_policy_default_size_deviation_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.max_allowed_size_deviation_pct == 0.10

def test_policy_default_stop_deviation_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.max_allowed_stop_deviation_pct == 0.05

def test_policy_default_min_discipline_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.min_discipline_score == 70.0


# =========================================================================
# Section 13: should_auto_apply always False
# =========================================================================
def test_journal_entry_should_auto_apply_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalEntry
    e = JournalEntry()
    assert e.should_auto_apply is False

def test_journal_entry_should_auto_apply_forced_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalEntry
    e = JournalEntry(should_auto_apply=True)
    assert e.should_auto_apply is False

def test_journal_review_result_should_auto_apply_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalReviewResult
    r = JournalReviewResult()
    assert r.should_auto_apply is False

def test_journal_review_result_should_auto_apply_forced_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalReviewResult
    r = JournalReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False

def test_journal_review_result_auto_apply_enabled_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalReviewResult
    r = JournalReviewResult()
    assert r.auto_apply_enabled is False

def test_journal_review_result_auto_apply_enabled_forced_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalReviewResult
    r = JournalReviewResult(auto_apply_enabled=True)
    assert r.auto_apply_enabled is False

def test_journal_export_result_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalExportResult
    e = JournalExportResult()
    assert e.should_auto_apply is False

def test_journal_export_result_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalExportResult
    e = JournalExportResult()
    assert e.auto_apply_enabled is False

def test_journal_safety_guard_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g.should_auto_apply is False

def test_journal_safety_guard_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g.auto_apply_enabled is False


# =========================================================================
# Section 14: planned vs actual entry comparison
# =========================================================================
def test_evaluate_journal_entry_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e is not None

def test_evaluate_journal_entry_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.paper_only is True

def test_evaluate_journal_entry_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.should_auto_apply is False

def test_evaluate_journal_entry_schema_version_211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.schema_version == "211"

def test_compliant_entry_no_violations():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-002", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.violation_codes == []

def test_compliant_entry_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-002", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.execution_action in ("compliant", "monitor")

def test_no_planned_entry_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-003", "2317", "鴻海", "CAND-003", "THEME-EV", "SECTOR-MFGR",
        0.0, 120.0, 0, 1000, 0.0, 110.0, 0.0, 0.0
    )
    assert "NO_PLANNED_ENTRY" in e.violation_codes

def test_no_planned_entry_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-003", "2317", "鴻海", "CAND-003", "THEME-EV", "SECTOR-MFGR",
        0.0, 120.0, 0, 1000, 0.0, 110.0, 0.0, 0.0
    )
    assert e.execution_action == "human_review_required"
    assert e.requires_human_review is True

def test_entry_slippage_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-004", "2454", "聯發科", "CAND-004", "THEME-AI", "SECTOR-TECH",
        1000.0, 1035.0, 500, 500, 940.0, 940.0, 1060.0, 0.0
    )
    assert "ENTRY_SLIPPAGE_EXCESS" in e.violation_codes

def test_size_deviation_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-005", "6669", "緯穎", "CAND-005", "THEME-AI", "SECTOR-TECH",
        2000.0, 2000.0, 300, 500, 1880.0, 1880.0, 2120.0, 0.0
    )
    assert "SIZE_DEVIATION_EXCESS" in e.violation_codes


# =========================================================================
# Section 15: Position size deviation detection
# =========================================================================
def test_size_within_limit_no_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-006", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1050, 855.0, 855.0, 945.0, 0.0
    )
    assert "SIZE_DEVIATION_EXCESS" not in e.violation_codes

def test_size_exactly_at_limit_no_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-007", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1100, 855.0, 855.0, 945.0, 0.0
    )
    assert "SIZE_DEVIATION_EXCESS" not in e.violation_codes

def test_size_over_limit_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-008", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1200, 855.0, 855.0, 945.0, 0.0
    )
    assert "SIZE_DEVIATION_EXCESS" in e.violation_codes

def test_size_deviation_mistake_tag():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-009", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1500, 855.0, 855.0, 945.0, 0.0
    )
    assert "position_oversized" in e.mistake_tags


# =========================================================================
# Section 16: Stop deviation detection
# =========================================================================
def test_stop_deviation_within_limit_no_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-010", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 852.0, 945.0, 0.0
    )
    assert "STOP_DEVIATION_EXCESS" not in e.violation_codes

def test_stop_deviation_over_limit_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-011", "2308", "台達電", "CAND-002", "THEME-EV", "SECTOR-ELEC",
        400.0, 400.0, 1000, 1000, 372.0, 350.0, 428.0, 0.0
    )
    assert "STOP_DEVIATION_EXCESS" in e.violation_codes

def test_stop_deviation_mistake_tag():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-012", "2308", "台達電", "CAND-002", "THEME-EV", "SECTOR-ELEC",
        400.0, 400.0, 1000, 1000, 372.0, 350.0, 428.0, 0.0
    )
    assert "stop_too_loose" in e.mistake_tags


# =========================================================================
# Section 17: Exit plan adherence detection
# =========================================================================
def test_missing_exit_plan_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-013", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 0.0, 0.0
    )
    assert "MISSING_EXIT_PLAN" in e.violation_codes

def test_missing_exit_plan_mistake_tag():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-014", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 0.0, 0.0
    )
    assert "plan_not_followed" in e.mistake_tags

def test_exit_plan_present_no_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-015", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert "MISSING_EXIT_PLAN" not in e.violation_codes


# =========================================================================
# Section 18: Unplanned add-on detection
# =========================================================================
def test_unplanned_add_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-016", "6669", "緯穎", "CAND-005", "THEME-AI", "SECTOR-TECH",
        2000.0, 2000.0, 300, 300, 1880.0, 1880.0, 2120.0, 0.0,
        is_unplanned_add=True
    )
    assert "UNPLANNED_ADD" in e.violation_codes

def test_unplanned_add_mistake_tag():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-017", "6669", "緯穎", "CAND-005", "THEME-AI", "SECTOR-TECH",
        2000.0, 2000.0, 300, 300, 1880.0, 1880.0, 2120.0, 0.0,
        is_unplanned_add=True
    )
    assert "unplanned_addon" in e.mistake_tags

def test_planned_add_no_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-018", "6669", "緯穎", "CAND-005", "THEME-AI", "SECTOR-TECH",
        2000.0, 2000.0, 300, 300, 1880.0, 1880.0, 2120.0, 0.0,
        is_unplanned_add=False
    )
    assert "UNPLANNED_ADD" not in e.violation_codes


# =========================================================================
# Section 19: Overtrade detection
# =========================================================================
def test_overtrade_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-019", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0,
        is_overtrade=True
    )
    assert "OVERTRADE" in e.violation_codes

def test_overtrade_mistake_tag():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-020", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0,
        is_overtrade=True
    )
    assert "overtrading" in e.mistake_tags


# =========================================================================
# Section 20: Stop-loss violation detection
# =========================================================================
def test_stop_loss_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-021", "2303", "聯電", "CAND-006", "THEME-SEMI", "SECTOR-TECH",
        55.0, 55.0, 3000, 3000, 51.0, 51.0, 59.0, 0.0,
        stop_loss_violated=True
    )
    assert "STOP_LOSS_VIOLATION" in e.violation_codes

def test_stop_loss_violation_mistake_tag():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-022", "2303", "聯電", "CAND-006", "THEME-SEMI", "SECTOR-TECH",
        55.0, 55.0, 3000, 3000, 51.0, 51.0, 59.0, 0.0,
        stop_loss_violated=True
    )
    assert "stop_moved_away" in e.mistake_tags

def test_stop_loss_not_violated_no_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-023", "2303", "聯電", "CAND-006", "THEME-SEMI", "SECTOR-TECH",
        55.0, 55.0, 3000, 3000, 51.0, 51.0, 59.0, 0.0,
        stop_loss_violated=False
    )
    assert "STOP_LOSS_VIOLATION" not in e.violation_codes


# =========================================================================
# Section 21: Mistake tag classification
# =========================================================================
def test_no_violations_no_mistake_tags():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-024", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.mistake_tags == []

def test_chasing_price_tag_on_high_slippage():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-025", "2454", "聯發科", "CAND-004", "THEME-AI", "SECTOR-TECH",
        1000.0, 1040.0, 500, 500, 940.0, 940.0, 1060.0, 0.0
    )
    assert "chasing_price" in e.mistake_tags


# =========================================================================
# Section 22: Violation code classification
# =========================================================================
def test_multiple_violations_detected():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-026", "2317", "鴻海", "CAND-003", "THEME-EV", "SECTOR-MFGR",
        0.0, 120.0, 0, 1000, 0.0, 110.0, 0.0, 0.0
    )
    assert len(e.violation_codes) >= 1

def test_violation_codes_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-027", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert isinstance(e.violation_codes, list)


# =========================================================================
# Section 23: Discipline score calculation
# =========================================================================
def test_discipline_score_calculation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _calc_discipline_score, TradeJournalPolicy
    policy = TradeJournalPolicy()
    score = _calc_discipline_score(
        entry_slippage_pct=0.0,
        size_deviation_pct=0.0,
        stop_deviation_pct=0.0,
        has_exit_plan=True,
        is_unplanned_add=False,
        is_overtrade=False,
        stop_loss_violated=False,
        has_planned_entry=True,
        policy=policy,
    )
    assert score == 100.0

def test_discipline_score_deduction_no_planned_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _calc_discipline_score, TradeJournalPolicy
    policy = TradeJournalPolicy()
    score = _calc_discipline_score(
        entry_slippage_pct=0.0,
        size_deviation_pct=0.0,
        stop_deviation_pct=0.0,
        has_exit_plan=True,
        is_unplanned_add=False,
        is_overtrade=False,
        stop_loss_violated=False,
        has_planned_entry=False,
        policy=policy,
    )
    assert score == 80.0

def test_discipline_score_minimum_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _calc_discipline_score, TradeJournalPolicy
    policy = TradeJournalPolicy()
    score = _calc_discipline_score(
        entry_slippage_pct=1.0,
        size_deviation_pct=1.0,
        stop_deviation_pct=1.0,
        has_exit_plan=False,
        is_unplanned_add=True,
        is_overtrade=True,
        stop_loss_violated=True,
        has_planned_entry=False,
        policy=policy,
    )
    assert score >= 0.0

def test_discipline_score_slippage_deduction():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _calc_discipline_score, TradeJournalPolicy
    policy = TradeJournalPolicy()
    score = _calc_discipline_score(
        entry_slippage_pct=0.05,
        size_deviation_pct=0.0,
        stop_deviation_pct=0.0,
        has_exit_plan=True,
        is_unplanned_add=False,
        is_overtrade=False,
        stop_loss_violated=False,
        has_planned_entry=True,
        policy=policy,
    )
    assert score == 90.0


# =========================================================================
# Section 24: Execution action classification
# =========================================================================
def test_classify_action_compliant():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _classify_execution_action, TradeJournalPolicy
    policy = TradeJournalPolicy()
    action = _classify_execution_action(95.0, [], policy)
    assert action == "compliant"

def test_classify_action_monitor():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _classify_execution_action, TradeJournalPolicy
    policy = TradeJournalPolicy()
    action = _classify_execution_action(82.0, [], policy)
    assert action == "monitor"

def test_classify_action_require_journal_note():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _classify_execution_action, TradeJournalPolicy
    policy = TradeJournalPolicy()
    action = _classify_execution_action(75.0, ["ENTRY_SLIPPAGE_EXCESS"], policy)
    assert action == "require_journal_note"

def test_classify_action_flag_discipline_warning_stop_violation():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _classify_execution_action, TradeJournalPolicy
    policy = TradeJournalPolicy()
    action = _classify_execution_action(80.0, ["STOP_LOSS_VIOLATION"], policy)
    assert action == "flag_discipline_warning"

def test_classify_action_human_review_no_planned_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _classify_execution_action, TradeJournalPolicy
    policy = TradeJournalPolicy()
    action = _classify_execution_action(30.0, ["NO_PLANNED_ENTRY"], policy)
    assert action == "human_review_required"

def test_classify_action_block_followup():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _classify_execution_action, TradeJournalPolicy
    policy = TradeJournalPolicy()
    action = _classify_execution_action(35.0, ["SIZE_DEVIATION_EXCESS", "STOP_DEVIATION_EXCESS", "MISSING_EXIT_PLAN"], policy)
    assert action == "block_followup_action"


# =========================================================================
# Section 25: Mistake review queue
# =========================================================================
def test_build_mistake_review_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_mistake_review_queue
    queue = build_mistake_review_queue()
    assert queue is not None

def test_build_mistake_review_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_mistake_review_queue
    queue = build_mistake_review_queue()
    assert isinstance(queue, list)

def test_build_mistake_review_queue_has_mistakes():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_mistake_review_queue
    queue = build_mistake_review_queue()
    assert len(queue) >= 1

def test_mistake_queue_entries_have_violations():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_mistake_review_queue
    queue = build_mistake_review_queue()
    for e in queue:
        assert e.violation_codes or e.mistake_tags


# =========================================================================
# Section 26: Rule violation queue
# =========================================================================
def test_build_violation_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_violation_queue
    queue = build_violation_queue()
    assert queue is not None

def test_build_violation_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_violation_queue
    queue = build_violation_queue()
    assert isinstance(queue, list)

def test_violation_queue_entries_have_critical_violations():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_violation_queue
    critical = {"NO_PLANNED_ENTRY", "MISSING_EXIT_PLAN", "STOP_LOSS_VIOLATION", "OVERTRADE"}
    queue = build_violation_queue()
    for e in queue:
        assert any(v in critical for v in e.violation_codes)


# =========================================================================
# Section 27: Improvement suggestion queue
# =========================================================================
def test_build_improvement_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_improvement_queue
    queue = build_improvement_queue()
    assert queue is not None

def test_build_improvement_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_improvement_queue
    queue = build_improvement_queue()
    assert isinstance(queue, list)

def test_improvement_queue_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_improvement_queue
    queue = build_improvement_queue()
    for item in queue:
        assert item["paper_only"] is True

def test_improvement_queue_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_improvement_queue
    queue = build_improvement_queue()
    for item in queue:
        assert item["should_auto_apply"] is False

def test_improvement_suggestion_has_suggestion_text():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_improvement_queue
    queue = build_improvement_queue()
    for item in queue:
        assert "suggestion" in item
        assert len(item["suggestion"]) > 0


# =========================================================================
# Section 28: Human review escalation
# =========================================================================
def test_human_review_required_for_no_planned_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-028", "2317", "鴻海", "CAND-003", "THEME-EV", "SECTOR-MFGR",
        0.0, 120.0, 0, 1000, 0.0, 110.0, 0.0, 0.0
    )
    assert e.requires_human_review is True

def test_human_review_not_required_for_compliant():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    e = evaluate_journal_entry(
        "JE-029", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 900.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    )
    assert e.requires_human_review is False


# =========================================================================
# Section 29: Journal review engine
# =========================================================================
def test_run_journal_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result is not None

def test_run_journal_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.paper_only is True

def test_run_journal_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.all_passed is True

def test_run_journal_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.should_auto_apply is False

def test_run_journal_review_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.auto_apply_enabled is False

def test_run_journal_review_policy_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.journal_policy is not None

def test_run_journal_review_discipline_snapshot_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.execution_discipline_snapshot is not None

def test_run_journal_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.paper_only_safety_snapshot is True

def test_run_journal_review_has_journal_entries():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert len(result.trade_journal_snapshot) > 0

def test_run_journal_review_has_mistake_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert isinstance(result.mistake_review_queue, list)

def test_run_journal_review_has_violation_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert isinstance(result.rule_violation_queue, list)

def test_run_journal_review_has_human_review_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert isinstance(result.human_review_queue, list)

def test_run_journal_review_journal_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.journal_version == "2.0.11"

def test_run_journal_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.no_real_orders is True


# =========================================================================
# Section 30: Evaluate discipline
# =========================================================================
def test_evaluate_discipline_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert d is not None

def test_evaluate_discipline_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert isinstance(d, dict)

def test_evaluate_discipline_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert d["paper_only"] is True

def test_evaluate_discipline_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert d["should_auto_apply"] is False

def test_evaluate_discipline_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert d["auto_apply_enabled"] is False

def test_evaluate_discipline_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert d["schema_version"] == "211"

def test_evaluate_discipline_has_total_entries():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert "total_entries" in d

def test_evaluate_discipline_has_total_violations():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert "total_violations" in d


# =========================================================================
# Section 31: Grade calculations
# =========================================================================
def test_grade_discipline_A():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_discipline
    assert _grade_discipline(92.0) == "A"

def test_grade_discipline_B():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_discipline
    assert _grade_discipline(80.0) == "B"

def test_grade_discipline_C():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_discipline
    assert _grade_discipline(60.0) == "C"

def test_grade_discipline_D():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_discipline
    assert _grade_discipline(40.0) == "D"

def test_grade_plan_adherence_A():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_plan_adherence
    assert _grade_plan_adherence(9, 10) == "A"

def test_grade_plan_adherence_B():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_plan_adherence
    assert _grade_plan_adherence(8, 10) == "B"

def test_grade_plan_adherence_C():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_plan_adherence
    assert _grade_plan_adherence(6, 10) == "C"

def test_grade_plan_adherence_D():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_plan_adherence
    assert _grade_plan_adherence(4, 10) == "D"

def test_grade_plan_adherence_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import _grade_plan_adherence
    assert _grade_plan_adherence(0, 0) == "N/A"


# =========================================================================
# Section 32: Export JSON
# =========================================================================
def test_export_journal_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result is not None

def test_export_journal_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result.is_valid is True

def test_export_journal_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result.paper_only is True

def test_export_journal_json_export_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result.export_status == "complete"

def test_export_journal_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result.export_format == "json"

def test_export_journal_json_content_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert len(result.content) > 0

def test_export_journal_json_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result.should_auto_apply is False

def test_export_journal_json_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    assert result.paper_only_confirmed is True


# =========================================================================
# Section 33: Export Markdown
# =========================================================================
def test_export_journal_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert result is not None

def test_export_journal_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert result.is_valid is True

def test_export_journal_markdown_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert result.paper_only is True

def test_export_journal_markdown_content_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert len(result.content) > 0

def test_export_journal_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert result.export_format == "markdown"


# =========================================================================
# Section 34: Export CSV
# =========================================================================
def test_export_journal_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_csv
    result = export_journal_csv(run_journal_review())
    assert result is not None

def test_export_journal_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_csv
    result = export_journal_csv(run_journal_review())
    assert result.is_valid is True

def test_export_journal_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_csv
    result = export_journal_csv(run_journal_review())
    assert result.paper_only is True

def test_export_discipline_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_discipline_csv
    result = export_discipline_csv(run_journal_review())
    assert result is not None

def test_export_discipline_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_discipline_csv
    result = export_discipline_csv(run_journal_review())
    assert result.is_valid is True

def test_export_mistake_review_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_mistake_review_csv
    result = export_mistake_review_csv(run_journal_review())
    assert result is not None

def test_export_mistake_review_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_mistake_review_csv
    result = export_mistake_review_csv(run_journal_review())
    assert result.is_valid is True

def test_export_violation_queue_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_violation_queue_csv
    result = export_violation_queue_csv(run_journal_review())
    assert result is not None

def test_export_violation_queue_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_violation_queue_csv
    result = export_violation_queue_csv(run_journal_review())
    assert result.is_valid is True

def test_export_journal_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_audit_snapshot
    result = export_journal_audit_snapshot(run_journal_review())
    assert result is not None

def test_export_journal_audit_snapshot_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_audit_snapshot
    result = export_journal_audit_snapshot(run_journal_review())
    assert result.export_status == "complete"

def test_export_journal_audit_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_audit_snapshot
    result = export_journal_audit_snapshot(run_journal_review())
    assert result.paper_only is True


# =========================================================================
# Section 35: v2.0.10 exit plan integration
# =========================================================================
def test_v210_integration_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION as V210
    assert V210 == "2.0.10"

def test_v210_run_exit_plan_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result is not None

def test_v210_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION
    assert VERSION == "2.0.10"

def test_v210_schema_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "210"


# =========================================================================
# Section 36: v2.0.9 position sizing integration
# =========================================================================
def test_v209_integration_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION as V209
    assert V209 == "2.0.9"

def test_v209_run_sizing_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result is not None

def test_v209_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION
    assert VERSION == "2.0.9"


# =========================================================================
# Section 37: v2.0.8 exposure integration
# =========================================================================
def test_v208_integration_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION as V208
    assert V208 == "2.0.8"

def test_v208_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION
    assert VERSION == "2.0.8"


# =========================================================================
# Section 38: v2.0.7 market regime integration
# =========================================================================
def test_v207_integration_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION as V207
    assert V207 == "2.0.7"

def test_v207_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION
    assert VERSION == "2.0.7"


# =========================================================================
# Section 39: v2.0.6 lifecycle integration
# =========================================================================
def test_v206_integration_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION as V206
    assert V206 == "2.0.6"

def test_v206_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION
    assert VERSION == "2.0.6"


# =========================================================================
# Section 40: v2.0.5 watchlist rotation integration
# =========================================================================
def test_v205_integration_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION as V205
    assert V205 == "2.0.5"

def test_v205_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION
    assert VERSION == "2.0.5"


# =========================================================================
# Section 41: Export JSON / Markdown / CSV schema completeness
# =========================================================================
def test_export_json_contains_version():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    payload = json.loads(result.content)
    assert payload["version"] == "2.0.11"

def test_export_json_contains_paper_only():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    payload = json.loads(result.content)
    assert payload["paper_only"] is True

def test_export_json_should_auto_apply_false():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_json
    result = export_journal_json(run_journal_review())
    payload = json.loads(result.content)
    assert payload["should_auto_apply"] is False

def test_export_markdown_contains_journal():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert "Journal" in result.content or "journal" in result.content.lower()

def test_export_markdown_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_markdown
    result = export_journal_markdown(run_journal_review())
    assert "Paper Only" in result.content or "paper_only" in result.content.lower()

def test_export_journal_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_journal_csv
    result = export_journal_csv(run_journal_review())
    assert "symbol" in result.csv_content

def test_export_discipline_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review, export_discipline_csv
    result = export_discipline_csv(run_journal_review())
    assert "total" in result.csv_content or "compliant" in result.csv_content


# =========================================================================
# Section 42: CLI output
# =========================================================================
def test_cli_commands_all_strings():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    for cmd in CLI_COMMANDS_V211:
        assert isinstance(cmd, str)

def test_cli_commands_all_start_with_paper_cockpit_v211():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    for cmd in CLI_COMMANDS_V211:
        assert cmd.startswith("paper-cockpit-v211-")


# =========================================================================
# Section 43: CLI handler resolution
# =========================================================================
def test_main_importable():
    import main

def test_main_handler_review_journal_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_review_journal")

def test_main_handler_review_journal_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v211_review_journal)

def test_main_handler_evaluate_discipline_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_evaluate_discipline")

def test_main_handler_evaluate_discipline_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v211_evaluate_discipline)

def test_main_handler_build_mistake_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_build_mistake_queue")

def test_main_handler_build_violation_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_build_violation_queue")

def test_main_handler_build_improvement_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_build_improvement_queue")

def test_main_handler_export_json_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_export_json")

def test_main_handler_export_md_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_export_md")

def test_main_handler_export_csv_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_export_csv")

def test_main_handler_health_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_health")

def test_main_handler_gate_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v211_gate")

def test_no_isolated_v211_command_map():
    import main
    assert not hasattr(main, "_ISOLATED_V211_COMMAND_MAP")


# =========================================================================
# Section 44: CLI registration health
# =========================================================================
def test_cli_registry_importable():
    from cli.command_registry import PROVIDER_COMMANDS
    assert PROVIDER_COMMANDS is not None

def test_cli_registry_has_review_journal():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-review-journal" in names

def test_cli_registry_has_evaluate_discipline():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-evaluate-discipline" in names

def test_cli_registry_has_build_mistake_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-build-mistake-queue" in names

def test_cli_registry_has_build_violation_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-build-violation-queue" in names

def test_cli_registry_has_build_improvement_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-build-improvement-queue" in names

def test_cli_registry_has_export_json():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-export-json" in names

def test_cli_registry_has_export_md():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-export-md" in names

def test_cli_registry_has_export_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-export-csv" in names

def test_cli_registry_has_health():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-health" in names

def test_cli_registry_has_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v211-gate" in names


# =========================================================================
# Section 45: Replay lineage handler integrity
# =========================================================================
def test_v210_cli_handlers_still_present():
    import main
    for handler in [
        "cmd_paper_cockpit_v210_review_exit_plan",
        "cmd_paper_cockpit_v210_evaluate_stop_discipline",
        "cmd_paper_cockpit_v210_health",
        "cmd_paper_cockpit_v210_gate",
    ]:
        assert hasattr(main, handler), f"Missing v210 handler: {handler}"

def test_v209_cli_handlers_still_present():
    import main
    for handler in [
        "cmd_paper_cockpit_v209_review_sizing",
        "cmd_paper_cockpit_v209_health",
        "cmd_paper_cockpit_v209_gate",
    ]:
        assert hasattr(main, handler), f"Missing v209 handler: {handler}"

def test_v211_banner_defined():
    import main
    assert hasattr(main, "_PAPER_COCKPIT_V211_BANNER")
    assert len(main._PAPER_COCKPIT_V211_BANNER) > 0


# =========================================================================
# Section 46: GUI compatibility
# =========================================================================
def test_gui_panel_importable():
    import gui.small_capital_strategy_panel

def test_panel_version_v211_exists():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V211
    assert PANEL_VERSION_V211 == "2.0.11"

def test_panel_version_v210_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V210
    assert PANEL_VERSION_V210 == "2.0.10"

def test_get_v211_tab_names_callable():
    from gui.small_capital_strategy_panel import get_v211_tab_names
    tabs = get_v211_tab_names()
    assert isinstance(tabs, list)

def test_get_v211_tab_names_count_3():
    from gui.small_capital_strategy_panel import get_v211_tab_names
    tabs = get_v211_tab_names()
    assert len(tabs) == 3

def test_v211_tabs_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "trade_journal_v211" in tabs
    assert "execution_discipline_v211" in tabs
    assert "mistake_review_queue_v211" in tabs

def test_render_trade_journal_v211_tab():
    from gui.small_capital_strategy_panel import render_trade_journal_v211_tab
    result = render_trade_journal_v211_tab()
    assert result["tab"] == "trade_journal_v211"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_render_execution_discipline_v211_tab():
    from gui.small_capital_strategy_panel import render_execution_discipline_v211_tab
    result = render_execution_discipline_v211_tab()
    assert result["tab"] == "execution_discipline_v211"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_render_mistake_review_queue_v211_tab():
    from gui.small_capital_strategy_panel import render_mistake_review_queue_v211_tab
    result = render_mistake_review_queue_v211_tab()
    assert result["tab"] == "mistake_review_queue_v211"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False


# =========================================================================
# Section 47: render_all_tabs no error tabs
# =========================================================================
def test_render_all_tabs_no_v211_errors():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["trade_journal_v211", "execution_discipline_v211", "mistake_review_queue_v211"]:
        assert "error" not in result.get(tab, {}), f"Tab {tab} has error: {result.get(tab, {}).get('error')}"

def test_render_all_tabs_no_global_errors():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert not error_tabs, f"render_all_tabs has error tabs: {error_tabs}"

def test_render_all_tabs_v210_still_works():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["exit_plan_v210", "stop_discipline_v210", "exit_warning_queue_v210"]:
        assert "error" not in result.get(tab, {}), f"v210 tab {tab} has error"


# =========================================================================
# Section 48: Paper-only safety
# =========================================================================
def test_paper_only_guard_enabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["paper_only"] is True

def test_no_broker_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_broker"] is True

def test_no_real_order_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_production_trading_blocked_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

def test_broker_execution_disabled_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_journal_actions_are_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["journal_actions_recommendation_only"] is True

def test_no_automatic_journal_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_journal_apply"] is True

def test_no_automatic_stop_loss():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_stop_loss_execution"] is True

def test_no_automatic_take_profit():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert SAFETY_FLAGS_V211["no_automatic_take_profit_execution"] is True


# =========================================================================
# Section 49: No broker / no real order guard
# =========================================================================
def test_run_journal_review_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.no_broker is True

def test_evaluate_discipline_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    d = evaluate_discipline()
    assert d["paper_only"] is True

def test_journal_entry_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalEntry
    e = JournalEntry()
    assert e.no_real_orders is True

def test_trade_journal_policy_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    p = TradeJournalPolicy()
    assert p.no_real_orders is True

def test_journal_safety_guard_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g.no_real_orders is True

def test_journal_safety_guard_no_automatic_journal_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g.no_automatic_journal_apply is True

def test_journal_safety_guard_require_planned_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g.require_planned_entry_before_trade is True

def test_journal_safety_guard_journal_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalSafetyGuard
    g = JournalSafetyGuard()
    assert g.journal_actions_recommendation_only is True


# =========================================================================
# Section 50: Backward compatibility with v2.0.10
# =========================================================================
def test_v210_backward_compat_import():
    import paper_trading.small_capital_strategy.paper_cockpit_v210

def test_v210_backward_compat_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION
    assert VERSION == "2.0.10"

def test_v210_backward_compat_exit_actions():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert len(EXIT_ACTIONS) == 8

def test_v210_backward_compat_safety_flags():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["paper_only"] is True

def test_v210_backward_compat_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.paper_only is True
    assert result.should_auto_apply is False


# =========================================================================
# Section 51: v201 health relative-path compatibility
# =========================================================================
def test_v201_health_test_exists():
    import os
    test_path = os.path.join(
        os.path.dirname(__file__), "test_paper_cockpit_v201.py"
    )
    assert os.path.exists(test_path)


# =========================================================================
# Section 52: Health check
# =========================================================================
def test_health_check_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v211

def test_health_check_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v211 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.11"

def test_health_check_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v211 import HEALTH_RELEASE
    assert "Journal" in HEALTH_RELEASE or "Trade" in HEALTH_RELEASE

def test_health_check_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v211 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_check_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v211 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result['errors']}"

def test_health_check_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v211 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)
    assert "passed" in result
    assert "failed" in result
    assert "total" in result


# =========================================================================
# Section 53: Gate check
# =========================================================================
def test_gate_importable():
    import release.paper_cockpit_release_gate_v211

def test_gate_version():
    from release.paper_cockpit_release_gate_v211 import GATE_VERSION
    assert GATE_VERSION == "2.0.11"

def test_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v211 import BASELINE_TESTS
    assert BASELINE_TESTS == 35613

def test_gate_callable():
    from release.paper_cockpit_release_gate_v211 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_gate_all_passed():
    from release.paper_cockpit_release_gate_v211 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failed: {result['errors']}"

def test_gate_expected_panel_versions():
    from release.paper_cockpit_release_gate_v211 import EXPECTED_PANEL_VERSIONS
    assert "2.0.11" in EXPECTED_PANEL_VERSIONS
    assert "2.0.10" in EXPECTED_PANEL_VERSIONS


# =========================================================================
# Section 54: Scenarios
# =========================================================================
def test_scenarios_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    assert SCENARIOS is not None

def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_schema_version_211():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    for s in SCENARIOS:
        assert s["schema_version"] == "211"

def test_scenarios_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    for s in SCENARIOS:
        assert s["paper_only"] is True

def test_scenarios_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    for s in SCENARIOS:
        assert s["should_auto_apply"] is False

def test_scenarios_have_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    for s in SCENARIOS:
        assert "scenario_id" in s

def test_scenarios_id_prefix_sc211():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    for s in SCENARIOS:
        assert s["scenario_id"].startswith("SC211-")


# =========================================================================
# Section 55: Fixtures
# =========================================================================
def test_fixtures_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    assert FIXTURES is not None

def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_schema_version_211():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    for f in FIXTURES:
        assert f["schema_version"] == "211"

def test_fixtures_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    for f in FIXTURES:
        assert f["paper_only"] is True

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    for f in FIXTURES:
        assert "fixture_id" in f

def test_fixtures_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    for f in FIXTURES:
        assert f["should_auto_apply"] is False

def test_fixtures_id_prefix_fx211():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    for f in FIXTURES:
        assert f["fixture_id"].startswith("FX211-")


# =========================================================================
# Section 56: get_cockpit_summary_v211
# =========================================================================
def test_get_cockpit_summary_v211_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary is not None

def test_get_cockpit_summary_v211_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert isinstance(summary, dict)

def test_get_cockpit_summary_v211_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["version"] == "2.0.11"

def test_get_cockpit_summary_v211_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["paper_only"] is True

def test_get_cockpit_summary_v211_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["should_auto_apply"] is False

def test_get_cockpit_summary_v211_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["auto_apply_enabled"] is False

def test_get_cockpit_summary_v211_require_planned_entry_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["require_planned_entry_before_trade"] is True

def test_get_cockpit_summary_v211_cli_command_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["cli_command_count"] == 10

def test_get_cockpit_summary_v211_gui_tab_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    summary = get_cockpit_summary_v211()
    assert summary["gui_tab_count"] == 3
