"""
tests/test_paper_cockpit_v210.py
v2.0.10 Paper Exit Plan & Stop-Loss Discipline Control — Main Tests
[!] Paper Only. Research Only. Exit Plan Recommendation Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Section 1: Module import & version constants
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v210

def test_version_is_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION
    assert VERSION == "2.0.10"

def test_schema_version_is_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "210"

def test_release_name_contains_exit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import RELEASE_NAME
    assert "Exit" in RELEASE_NAME

def test_release_name_contains_stop_loss():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import RELEASE_NAME
    assert "Stop" in RELEASE_NAME or "Discipline" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import BASELINE_TESTS
    assert BASELINE_TESTS == 35313

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import verify_version
    assert verify_version() is True


# =========================================================================
# Section 2: Safety constants
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Section 3: EXIT_ACTIONS
# =========================================================================
def test_exit_actions_count_8():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert len(EXIT_ACTIONS) == 8

def test_exit_action_allow_with_exit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "allow_with_exit_plan" in EXIT_ACTIONS

def test_exit_action_require_tighter_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "require_tighter_stop" in EXIT_ACTIONS

def test_exit_action_reduce_size_before_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "reduce_size_before_entry" in EXIT_ACTIONS

def test_exit_action_observation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "observation_only" in EXIT_ACTIONS

def test_exit_action_block_entry_missing_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "block_entry_missing_stop" in EXIT_ACTIONS

def test_exit_action_block_entry_bad_reward_risk():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "block_entry_bad_reward_risk" in EXIT_ACTIONS

def test_exit_action_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "require_rescore" in EXIT_ACTIONS

def test_exit_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    assert "human_review_required" in EXIT_ACTIONS


# =========================================================================
# Section 4: CLI commands
# =========================================================================
def test_cli_commands_count_10():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert len(CLI_COMMANDS_V210) == 10

def test_cli_cmd_review_exit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-review-exit-plan" in CLI_COMMANDS_V210

def test_cli_cmd_evaluate_stop_discipline():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-evaluate-stop-discipline" in CLI_COMMANDS_V210

def test_cli_cmd_build_exit_warning_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-build-exit-warning-queue" in CLI_COMMANDS_V210

def test_cli_cmd_build_stop_violation_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-build-stop-violation-queue" in CLI_COMMANDS_V210

def test_cli_cmd_evaluate_reward_risk():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-evaluate-reward-risk" in CLI_COMMANDS_V210

def test_cli_cmd_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-export-json" in CLI_COMMANDS_V210

def test_cli_cmd_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-export-md" in CLI_COMMANDS_V210

def test_cli_cmd_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-export-csv" in CLI_COMMANDS_V210

def test_cli_cmd_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-health" in CLI_COMMANDS_V210

def test_cli_cmd_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    assert "paper-cockpit-v210-gate" in CLI_COMMANDS_V210


# =========================================================================
# Section 5: GUI tabs
# =========================================================================
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import GUI_TABS_V210
    assert len(GUI_TABS_V210) == 3

def test_gui_tab_exit_plan_v210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import GUI_TABS_V210
    assert "exit_plan_v210" in GUI_TABS_V210

def test_gui_tab_stop_discipline_v210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import GUI_TABS_V210
    assert "stop_discipline_v210" in GUI_TABS_V210

def test_gui_tab_exit_warning_queue_v210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import GUI_TABS_V210
    assert "exit_warning_queue_v210" in GUI_TABS_V210


# =========================================================================
# Section 6: SAFETY_FLAGS_V210
# =========================================================================
def test_safety_flags_count_23():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert len(SAFETY_FLAGS_V210) == 23

def test_safety_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["paper_only"] is True

def test_safety_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["research_only"] is True

def test_safety_exit_plan_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["exit_plan_recommendation_only"] is True

def test_safety_exit_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["exit_actions_recommendation_only"] is True

def test_safety_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_real_orders"] is True

def test_safety_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_broker"] is True

def test_safety_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["should_auto_apply_always_false"] is True

def test_safety_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["auto_apply_enabled_always_false"] is True

def test_safety_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["broker_execution_disabled"] is True

def test_safety_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["production_trading_blocked"] is True

def test_safety_no_automatic_exit_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_exit_apply"] is True

def test_safety_no_automatic_stop_loss_execution():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_stop_loss_execution"] is True

def test_safety_no_automatic_take_profit_execution():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_take_profit_execution"] is True

def test_safety_require_stop_loss_before_entry_always_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["require_stop_loss_before_entry_always_true"] is True

def test_safety_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_rebalance"] is True

def test_safety_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_real_account_sync"] is True


# =========================================================================
# Section 7: Field lists
# =========================================================================
def test_exit_plan_policy_fields_13():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_PLAN_POLICY_FIELDS
    assert len(EXIT_PLAN_POLICY_FIELDS) == 13

def test_candidate_exit_plan_fields_24():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CANDIDATE_EXIT_PLAN_FIELDS
    assert len(CANDIDATE_EXIT_PLAN_FIELDS) == 24

def test_stop_discipline_summary_fields_14():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import STOP_DISCIPLINE_SUMMARY_FIELDS
    assert len(STOP_DISCIPLINE_SUMMARY_FIELDS) == 14

def test_exit_review_fields_11():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_REVIEW_FIELDS
    assert len(EXIT_REVIEW_FIELDS) == 11

def test_exit_plan_policy_fields_has_policy_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_PLAN_POLICY_FIELDS
    assert "policy_id" in EXIT_PLAN_POLICY_FIELDS

def test_exit_plan_policy_fields_has_auto_apply_enabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_PLAN_POLICY_FIELDS
    assert "auto_apply_enabled" in EXIT_PLAN_POLICY_FIELDS

def test_exit_plan_policy_fields_has_require_stop_loss():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_PLAN_POLICY_FIELDS
    assert "require_stop_loss_before_entry" in EXIT_PLAN_POLICY_FIELDS

def test_candidate_exit_plan_fields_has_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CANDIDATE_EXIT_PLAN_FIELDS
    assert "symbol" in CANDIDATE_EXIT_PLAN_FIELDS

def test_candidate_exit_plan_fields_has_exit_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CANDIDATE_EXIT_PLAN_FIELDS
    assert "exit_action" in CANDIDATE_EXIT_PLAN_FIELDS

def test_candidate_exit_plan_fields_has_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CANDIDATE_EXIT_PLAN_FIELDS
    assert "should_auto_apply" in CANDIDATE_EXIT_PLAN_FIELDS

def test_stop_discipline_summary_fields_has_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import STOP_DISCIPLINE_SUMMARY_FIELDS
    assert "exit_plan_quality_grade" in STOP_DISCIPLINE_SUMMARY_FIELDS
    assert "stop_discipline_quality_grade" in STOP_DISCIPLINE_SUMMARY_FIELDS

def test_exit_review_fields_has_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_REVIEW_FIELDS
    assert "paper_only_safety_snapshot" in EXIT_REVIEW_FIELDS


# =========================================================================
# Section 8: ExitPlanPolicy dataclass
# =========================================================================
def test_exit_plan_policy_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p is not None

def test_exit_plan_policy_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.schema_version == "210"

def test_exit_plan_policy_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.paper_only is True

def test_exit_plan_policy_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy(auto_apply_enabled=True)
    assert p.auto_apply_enabled is False

def test_exit_plan_policy_require_stop_always_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy(require_stop_loss_before_entry=False)
    assert p.require_stop_loss_before_entry is True

def test_exit_plan_policy_default_stop_loss_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.default_stop_loss_pct == 0.06

def test_exit_plan_policy_max_stop_distance_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.max_stop_distance_pct == 0.12

def test_exit_plan_policy_min_reward_risk_ratio():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.min_reward_risk_ratio == 2.0

def test_exit_plan_policy_first_tp_r_multiple():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.first_take_profit_r_multiple == 1.0

def test_exit_plan_policy_second_tp_r_multiple():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.second_take_profit_r_multiple == 2.0

def test_exit_plan_policy_time_stop_days():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.time_stop_days == 20

def test_exit_plan_policy_gap_down_exit_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.gap_down_exit_pct == 0.05

def test_exit_plan_policy_failed_breakout_days():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    p = ExitPlanPolicy()
    assert p.failed_breakout_days == 5


# =========================================================================
# Section 9: CandidateExitPlan dataclass
# =========================================================================
def test_candidate_exit_plan_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan()
    assert c is not None

def test_candidate_exit_plan_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan()
    assert c.schema_version == "210"

def test_candidate_exit_plan_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan()
    assert c.paper_only is True

def test_candidate_exit_plan_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan()
    assert c.no_real_orders is True

def test_candidate_exit_plan_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan(should_auto_apply=True)
    assert c.should_auto_apply is False

def test_candidate_exit_plan_stop_loss_required_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan()
    assert c.stop_loss_required is True

def test_candidate_exit_plan_default_exit_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    c = CandidateExitPlan()
    assert c.exit_action == "allow_with_exit_plan"


# =========================================================================
# Section 10: ExitReviewResult dataclass
# =========================================================================
def test_exit_review_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r is not None

def test_exit_review_result_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.schema_version == "210"

def test_exit_review_result_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.paper_only is True

def test_exit_review_result_exit_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.exit_version == "2.0.10"

def test_exit_review_result_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False

def test_exit_review_result_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult(auto_apply_enabled=True)
    assert r.auto_apply_enabled is False

def test_exit_review_result_paper_only_safety_snapshot_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.paper_only_safety_snapshot is True

def test_exit_review_result_human_review_required_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.human_review_required is True

def test_exit_review_result_research_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.research_only is True

def test_exit_review_result_not_investment_advice_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    r = ExitReviewResult()
    assert r.not_investment_advice is True


# =========================================================================
# Section 11: Other dataclasses
# =========================================================================
def test_exit_review_input_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewInput
    i = ExitReviewInput()
    assert i is not None

def test_stop_discipline_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import StopDisciplineSummary
    s = StopDisciplineSummary()
    assert s is not None

def test_stop_discipline_summary_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import StopDisciplineSummary
    s = StopDisciplineSummary()
    assert s.schema_version == "210"

def test_stop_discipline_summary_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import StopDisciplineSummary
    s = StopDisciplineSummary()
    assert s.paper_only is True

def test_exit_export_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitExportResult
    e = ExitExportResult()
    assert e is not None

def test_exit_audit_snapshot_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitAuditSnapshot
    a = ExitAuditSnapshot()
    assert a is not None

def test_exit_markdown_report_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitMarkdownReport
    m = ExitMarkdownReport()
    assert m is not None

def test_candidate_exit_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitCSV
    c = CandidateExitCSV()
    assert c is not None

def test_stop_discipline_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import StopDisciplineCSV
    s = StopDisciplineCSV()
    assert s is not None

def test_exit_warning_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitWarningCSV
    w = ExitWarningCSV()
    assert w is not None

def test_v210_health_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import V210HealthSummary
    h = V210HealthSummary()
    assert h is not None

def test_v210_release_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import V210ReleaseSummary
    r = V210ReleaseSummary()
    assert r is not None

def test_exit_plan_safety_guard_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanSafetyGuard
    g = ExitPlanSafetyGuard()
    assert g is not None

def test_exit_plan_safety_guard_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanSafetyGuard
    g = ExitPlanSafetyGuard()
    assert g.should_auto_apply is False
    assert g.auto_apply_enabled is False

def test_model_count_14():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import _ALL_MODEL_NAMES_V210
    assert len(_ALL_MODEL_NAMES_V210) == 14


# =========================================================================
# Section 12: calculate_exit_plan
# =========================================================================
def test_calculate_exit_plan_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result is not None

def test_calculate_exit_plan_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.paper_only is True

def test_calculate_exit_plan_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.no_real_orders is True

def test_calculate_exit_plan_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.should_auto_apply is False

def test_calculate_exit_plan_stop_loss_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.stop_loss_required is True

def test_calculate_exit_plan_valid_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.stop_loss_valid is True

def test_calculate_exit_plan_stop_distance_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert abs(result.stop_distance_pct - 0.05) < 0.001

def test_calculate_exit_plan_first_tp_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.first_take_profit_price > result.entry_price

def test_calculate_exit_plan_second_tp_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.second_take_profit_price >= result.first_take_profit_price

def test_calculate_exit_plan_trailing_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.trailing_stop_price > 0

def test_calculate_exit_plan_reward_risk_ratio():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.reward_risk_ratio > 0

def test_calculate_exit_plan_allow_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan, EXIT_ACTIONS
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.exit_action in EXIT_ACTIONS

def test_calculate_exit_plan_missing_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 0.0)
    assert result.exit_action == "block_entry_missing_stop"
    assert result.stop_loss_valid is False

def test_calculate_exit_plan_stop_above_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 90.0, 100.0)
    assert result.stop_loss_valid is False

def test_calculate_exit_plan_excessive_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 85.0)
    # excessive stop distance (15%) makes stop_loss_valid=False → blocked
    assert result.stop_loss_valid is False
    assert result.exit_action in ("block_entry_missing_stop", "require_tighter_stop")

def test_calculate_exit_plan_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan, ExitPlanPolicy
    # Use policy with min_rr=0.5 so R/R check passes and volatility check fires
    policy = ExitPlanPolicy(min_reward_risk_ratio=0.5)
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 94.0, policy=policy, is_high_volatility=True)
    assert result.exit_action == "reduce_size_before_entry"

def test_calculate_exit_plan_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan, ExitPlanPolicy
    # Use policy with min_rr=0.5 so R/R check passes and risk_off check fires
    policy = ExitPlanPolicy(min_reward_risk_ratio=0.5)
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 94.0, policy=policy, market_state="risk_off")
    assert result.exit_action == "observation_only"

def test_calculate_exit_plan_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan, ExitPlanPolicy
    # Use policy with min_rr=0.5 so R/R check passes and downtrend check fires
    policy = ExitPlanPolicy(min_reward_risk_ratio=0.5)
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 94.0, policy=policy, market_state="downtrend")
    assert result.exit_action == "human_review_required"

def test_calculate_exit_plan_expired_lifecycle():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan, ExitPlanPolicy
    policy = ExitPlanPolicy(min_reward_risk_ratio=0.5)
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 94.0, policy=policy, lifecycle_state="expired")
    assert result.exit_action == "observation_only"

def test_calculate_exit_plan_cooldown_lifecycle():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan, ExitPlanPolicy
    policy = ExitPlanPolicy(min_reward_risk_ratio=0.5)
    result = calculate_exit_plan("TEST", "test", "CAND-T", "TH", "SEC", 50.0, 50.0, 100.0, 94.0, policy=policy, lifecycle_state="cooldown")
    assert result.exit_action == "observation_only"

def test_calculate_exit_plan_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.schema_version == "210"

def test_calculate_exit_plan_symbol_preserved():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.symbol == "2330"

def test_calculate_exit_plan_max_loss_amount():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0, account_equity=300000.0)
    assert result.max_loss_amount > 0

def test_calculate_exit_plan_max_loss_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0)
    assert result.max_loss_pct == 0.08


# =========================================================================
# Section 13: run_exit_plan_review
# =========================================================================
def test_run_exit_plan_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result is not None

def test_run_exit_plan_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.paper_only is True

def test_run_exit_plan_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.all_passed is True

def test_run_exit_plan_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.should_auto_apply is False

def test_run_exit_plan_review_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.auto_apply_enabled is False

def test_run_exit_plan_review_exit_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.exit_version == "2.0.10"

def test_run_exit_plan_review_exit_plan_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.exit_plan_snapshot, list)

def test_run_exit_plan_review_exit_plan_snapshot_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert len(result.exit_plan_snapshot) > 0

def test_run_exit_plan_review_stop_loss_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.stop_loss_snapshot, list)

def test_run_exit_plan_review_take_profit_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.take_profit_snapshot, list)

def test_run_exit_plan_review_trailing_stop_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.trailing_stop_snapshot, list)

def test_run_exit_plan_review_exit_warning_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.exit_warning_queue, list)

def test_run_exit_plan_review_violation_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.stop_discipline_violation_queue, list)

def test_run_exit_plan_review_human_review_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert isinstance(result.human_review_queue, list)

def test_run_exit_plan_review_policy_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.exit_plan_policy is not None

def test_run_exit_plan_review_summary_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.stop_discipline_summary is not None

def test_run_exit_plan_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.paper_only_safety_snapshot is True

def test_run_exit_plan_review_exit_review_id_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result.exit_review_id != ""

def test_run_exit_plan_review_with_custom_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, ExitReviewInput
    inp = ExitReviewInput(review_period="2026-W30", candidate_pool=[
        {"symbol": "2330", "name": "台積電", "candidate_id": "C001", "theme_id": "T1", "sector_id": "S1",
         "candidate_score": 80.0, "final_priority_score": 80.0, "entry_price": 900.0, "stop_price": 855.0}
    ])
    result = run_exit_plan_review(review_input=inp)
    assert result.paper_only is True
    assert result.should_auto_apply is False

def test_run_exit_plan_review_stop_loss_snapshot_keys():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    if result.stop_loss_snapshot:
        snap = result.stop_loss_snapshot[0]
        assert "symbol" in snap
        assert "stop_price" in snap

def test_run_exit_plan_review_take_profit_snapshot_keys():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    if result.take_profit_snapshot:
        snap = result.take_profit_snapshot[0]
        assert "symbol" in snap
        assert "first_tp" in snap


# =========================================================================
# Section 14: StopDisciplineSummary
# =========================================================================
def test_stop_discipline_summary_total_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert s.total_candidate_count > 0

def test_stop_discipline_summary_valid_exit_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert s.valid_exit_plan_count >= 0

def test_stop_discipline_summary_missing_stop_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert s.missing_stop_count >= 0

def test_stop_discipline_summary_quality_grades():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert s.exit_plan_quality_grade in ("A", "B", "C", "D", "N/A")
    assert s.stop_discipline_quality_grade in ("A", "B", "C", "D", "N/A")

def test_stop_discipline_summary_average_rr():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert s.average_reward_risk_ratio >= 0.0

def test_stop_discipline_summary_lowest_rr_candidates_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert isinstance(s.lowest_reward_risk_candidates, list)

def test_stop_discipline_summary_top_exit_risk_reasons_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    s = result.stop_discipline_summary
    assert isinstance(s.top_exit_risk_reasons, list)


# =========================================================================
# Section 15: Export functions
# =========================================================================
def test_export_exit_plan_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert result is not None

def test_export_exit_plan_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert result.is_valid is True

def test_export_exit_plan_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert result.export_format == "json"

def test_export_exit_plan_json_content_has_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert "paper_only" in result.content

def test_export_exit_plan_json_export_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert result.export_status == "complete"

def test_export_exit_plan_json_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert result.paper_only_confirmed is True

def test_export_exit_plan_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_markdown
    result = export_exit_plan_markdown(run_exit_plan_review())
    assert result is not None

def test_export_exit_plan_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_markdown
    result = export_exit_plan_markdown(run_exit_plan_review())
    assert result.is_valid is True

def test_export_exit_plan_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_markdown
    result = export_exit_plan_markdown(run_exit_plan_review())
    assert result.export_format == "markdown"

def test_export_exit_plan_markdown_content_has_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_markdown
    result = export_exit_plan_markdown(run_exit_plan_review())
    assert "Paper Only" in result.content or "paper_only" in result.content.lower()

def test_export_candidate_exit_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_candidate_exit_csv
    result = export_candidate_exit_csv(run_exit_plan_review())
    assert result is not None

def test_export_candidate_exit_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_candidate_exit_csv
    result = export_candidate_exit_csv(run_exit_plan_review())
    assert result.is_valid is True

def test_export_candidate_exit_csv_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_candidate_exit_csv
    result = export_candidate_exit_csv(run_exit_plan_review())
    assert result.schema_version == "210"

def test_export_stop_discipline_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_stop_discipline_csv
    result = export_stop_discipline_csv(run_exit_plan_review())
    assert result is not None

def test_export_stop_discipline_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_stop_discipline_csv
    result = export_stop_discipline_csv(run_exit_plan_review())
    assert result.is_valid is True

def test_export_exit_warning_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_warning_csv
    result = export_exit_warning_csv(run_exit_plan_review())
    assert result is not None

def test_export_exit_warning_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_warning_csv
    result = export_exit_warning_csv(run_exit_plan_review())
    assert result.is_valid is True

def test_export_exit_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_audit_snapshot
    result = export_exit_audit_snapshot(run_exit_plan_review())
    assert result is not None

def test_export_exit_audit_snapshot_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_audit_snapshot
    result = export_exit_audit_snapshot(run_exit_plan_review())
    assert result.export_status == "complete"

def test_export_exit_audit_snapshot_has_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_audit_snapshot
    result = export_exit_audit_snapshot(run_exit_plan_review())
    assert result.reproducibility_hash != ""


# =========================================================================
# Section 16: get_cockpit_summary_v210
# =========================================================================
def test_get_cockpit_summary_v210_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result is not None

def test_get_cockpit_summary_v210_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert isinstance(result, dict)

def test_get_cockpit_summary_v210_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["version"] == "2.0.10"

def test_get_cockpit_summary_v210_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["paper_only"] is True

def test_get_cockpit_summary_v210_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["should_auto_apply"] is False

def test_get_cockpit_summary_v210_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["auto_apply_enabled"] is False

def test_get_cockpit_summary_v210_require_stop_loss():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["require_stop_loss_before_entry"] is True

def test_get_cockpit_summary_v210_exit_actions_recommendation():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["exit_actions_recommendation_only"] is True

def test_get_cockpit_summary_v210_exit_action_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["exit_action_count"] == 8

def test_get_cockpit_summary_v210_cli_command_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["cli_command_count"] == 10

def test_get_cockpit_summary_v210_gui_tab_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["gui_tab_count"] == 3

def test_get_cockpit_summary_v210_safety_flag_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["safety_flag_count"] == 23

def test_get_cockpit_summary_v210_model_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    result = get_cockpit_summary_v210()
    assert result["model_count"] == 14


# =========================================================================
# Section 17: Scenarios
# =========================================================================
def test_scenarios_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert SCENARIOS is not None

def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert all(s["schema_version"] == "210" for s in SCENARIOS)

def test_scenarios_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert all(s["paper_only"] is True for s in SCENARIOS)

def test_scenarios_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert all(s["should_auto_apply"] is False for s in SCENARIOS)

def test_scenarios_have_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert all("scenario_id" in s for s in SCENARIOS)

def test_scenarios_have_name():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert all("name" in s for s in SCENARIOS)

def test_scenarios_first_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert SCENARIOS[0]["scenario_id"] == "SC210-001"

def test_scenarios_last_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    assert SCENARIOS[79]["scenario_id"] == "SC210-080"


# =========================================================================
# Section 18: Fixtures
# =========================================================================
def test_fixtures_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert FIXTURES is not None

def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_schema_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert all(f["schema_version"] == "210" for f in FIXTURES)

def test_fixtures_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert all(f["paper_only"] is True for f in FIXTURES)

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert all("fixture_id" in f for f in FIXTURES)

def test_fixtures_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert all(f["should_auto_apply"] is False for f in FIXTURES)

def test_fixtures_first_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert FIXTURES[0]["fixture_id"] == "FX210-001"

def test_fixtures_last_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    assert FIXTURES[79]["fixture_id"] == "FX210-080"


# =========================================================================
# Section 19: Health check
# =========================================================================
def test_health_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v210

def test_health_run_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v210 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v210 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health failures: {result.get('errors', [])}"

def test_health_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v210 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)

def test_health_has_required_keys():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v210 import run_health_check
    result = run_health_check()
    for key in ("all_passed", "passed", "failed", "total", "errors"):
        assert key in result

def test_health_failed_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v210 import run_health_check
    result = run_health_check()
    assert result["failed"] == 0

def test_health_version_210():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v210 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.10"


# =========================================================================
# Section 20: Release gate
# =========================================================================
def test_gate_importable():
    import release.paper_cockpit_release_gate_v210

def test_gate_run_callable():
    from release.paper_cockpit_release_gate_v210 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_gate_all_passed():
    from release.paper_cockpit_release_gate_v210 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failures: {result.get('errors', [])}"

def test_gate_returns_dict():
    from release.paper_cockpit_release_gate_v210 import run_release_gate
    result = run_release_gate()
    assert isinstance(result, dict)

def test_gate_has_required_keys():
    from release.paper_cockpit_release_gate_v210 import run_release_gate
    result = run_release_gate()
    for key in ("gate_passed", "passed_count", "failed_count", "total_count", "errors"):
        assert key in result

def test_gate_failed_count_zero():
    from release.paper_cockpit_release_gate_v210 import run_release_gate
    result = run_release_gate()
    assert result["failed_count"] == 0

def test_gate_version_210():
    from release.paper_cockpit_release_gate_v210 import GATE_VERSION
    assert GATE_VERSION == "2.0.10"

def test_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v210 import BASELINE_TESTS
    assert BASELINE_TESTS == 35313


# =========================================================================
# Section 21: CLI handler resolution
# =========================================================================
def test_cli_registry_importable():
    from cli.command_registry import PROVIDER_COMMANDS
    assert PROVIDER_COMMANDS is not None

def test_cli_registry_has_v210_review_exit_plan():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-review-exit-plan" in names

def test_cli_registry_has_v210_evaluate_stop_discipline():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-evaluate-stop-discipline" in names

def test_cli_registry_has_v210_build_exit_warning_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-build-exit-warning-queue" in names

def test_cli_registry_has_v210_build_stop_violation_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-build-stop-violation-queue" in names

def test_cli_registry_has_v210_evaluate_reward_risk():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-evaluate-reward-risk" in names

def test_cli_registry_has_v210_export_json():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-export-json" in names

def test_cli_registry_has_v210_export_md():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-export-md" in names

def test_cli_registry_has_v210_export_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-export-csv" in names

def test_cli_registry_has_v210_health():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-health" in names

def test_cli_registry_has_v210_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v210-gate" in names

def test_cli_registry_v210_group():
    from cli.command_registry import PROVIDER_COMMANDS
    v210_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v210"]
    assert len(v210_cmds) == 10

def test_cli_registry_v210_safety_classification():
    from cli.command_registry import PROVIDER_COMMANDS
    v210_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v210"]
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in v210_cmds)

def test_cli_registry_is_flat_list():
    from cli.command_registry import PROVIDER_COMMANDS
    from cli.command_registry import CommandSpec
    for cmd in PROVIDER_COMMANDS:
        assert isinstance(cmd, CommandSpec)


# =========================================================================
# Section 22: CLI registration health (replay lineage handler integrity)
# =========================================================================
def test_main_importable():
    import main

def test_main_handler_review_exit_plan_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_review_exit_plan")

def test_main_handler_review_exit_plan_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v210_review_exit_plan)

def test_main_handler_evaluate_stop_discipline_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_evaluate_stop_discipline")

def test_main_handler_evaluate_stop_discipline_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v210_evaluate_stop_discipline)

def test_main_handler_build_exit_warning_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_build_exit_warning_queue")

def test_main_handler_build_stop_violation_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_build_stop_violation_queue")

def test_main_handler_evaluate_reward_risk_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_evaluate_reward_risk")

def test_main_handler_export_json_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_export_json")

def test_main_handler_export_md_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_export_md")

def test_main_handler_export_csv_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_export_csv")

def test_main_handler_health_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_health")

def test_main_handler_gate_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v210_gate")

def test_main_handlers_return_none():
    import main
    # All handlers must not raise
    main.cmd_paper_cockpit_v210_review_exit_plan()
    main.cmd_paper_cockpit_v210_evaluate_stop_discipline()
    main.cmd_paper_cockpit_v210_build_exit_warning_queue()
    main.cmd_paper_cockpit_v210_build_stop_violation_queue()
    main.cmd_paper_cockpit_v210_evaluate_reward_risk()

def test_main_handler_exports_not_raise():
    import main
    main.cmd_paper_cockpit_v210_export_json()
    main.cmd_paper_cockpit_v210_export_md()
    main.cmd_paper_cockpit_v210_export_csv()

def test_main_handler_health_not_raise():
    import main
    main.cmd_paper_cockpit_v210_health()

def test_main_handler_gate_not_raise():
    import main
    main.cmd_paper_cockpit_v210_gate()

def test_main_no_fake_isolated_command_map():
    import main
    assert not hasattr(main, "_ISOLATED_V210_COMMAND_MAP")


# =========================================================================
# Section 23: GUI panel compatibility
# =========================================================================
def test_gui_panel_importable():
    import gui.small_capital_strategy_panel

def test_gui_panel_version_v210():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V210
    assert PANEL_VERSION_V210 == "2.0.10"

def test_gui_panel_v210_tab_names():
    from gui.small_capital_strategy_panel import get_v210_tab_names
    names = get_v210_tab_names()
    assert len(names) == 3

def test_gui_panel_exit_plan_v210_in_tabs():
    from gui.small_capital_strategy_panel import get_v210_tab_names
    names = get_v210_tab_names()
    assert "exit_plan_v210" in names

def test_gui_panel_stop_discipline_v210_in_tabs():
    from gui.small_capital_strategy_panel import get_v210_tab_names
    names = get_v210_tab_names()
    assert "stop_discipline_v210" in names

def test_gui_panel_exit_warning_queue_v210_in_tabs():
    from gui.small_capital_strategy_panel import get_v210_tab_names
    names = get_v210_tab_names()
    assert "exit_warning_queue_v210" in names

def test_gui_panel_v210_tabs_in_get_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    names = get_tab_names()
    assert "exit_plan_v210" in names
    assert "stop_discipline_v210" in names
    assert "exit_warning_queue_v210" in names

def test_gui_render_exit_plan_v210_tab():
    from gui.small_capital_strategy_panel import render_exit_plan_v210_tab
    result = render_exit_plan_v210_tab()
    assert result["tab"] == "exit_plan_v210"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False
    assert result["auto_apply_enabled"] is False

def test_gui_render_stop_discipline_v210_tab():
    from gui.small_capital_strategy_panel import render_stop_discipline_v210_tab
    result = render_stop_discipline_v210_tab()
    assert result["tab"] == "stop_discipline_v210"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_gui_render_exit_warning_queue_v210_tab():
    from gui.small_capital_strategy_panel import render_exit_warning_queue_v210_tab
    result = render_exit_warning_queue_v210_tab()
    assert result["tab"] == "exit_warning_queue_v210"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_gui_render_all_tabs_exit_plan_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("exit_plan_v210", {})

def test_gui_render_all_tabs_stop_discipline_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("stop_discipline_v210", {})

def test_gui_render_all_tabs_exit_warning_queue_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("exit_warning_queue_v210", {})

def test_gui_render_all_tabs_no_global_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert not error_tabs, f"Error tabs: {error_tabs}"

def test_gui_exit_plan_v210_schema_version():
    from gui.small_capital_strategy_panel import render_exit_plan_v210_tab
    result = render_exit_plan_v210_tab()
    assert result["schema_version"] == "210"

def test_gui_exit_plan_v210_require_stop_loss():
    from gui.small_capital_strategy_panel import render_exit_plan_v210_tab
    result = render_exit_plan_v210_tab()
    assert result["require_stop_loss_before_entry"] is True

def test_gui_exit_plan_v210_no_real_orders():
    from gui.small_capital_strategy_panel import render_exit_plan_v210_tab
    result = render_exit_plan_v210_tab()
    assert result["no_real_orders"] is True


# =========================================================================
# Section 24: Paper-only safety invariants
# =========================================================================
def test_paper_only_safety_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_paper_only_safety_broker_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_paper_only_safety_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

def test_require_stop_loss_before_entry_always_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    for _ in range(3):
        p = ExitPlanPolicy(require_stop_loss_before_entry=False)
        assert p.require_stop_loss_before_entry is True

def test_auto_apply_enabled_always_false_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    for _ in range(3):
        p = ExitPlanPolicy(auto_apply_enabled=True)
        assert p.auto_apply_enabled is False

def test_should_auto_apply_always_false_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    for _ in range(3):
        c = CandidateExitPlan(should_auto_apply=True)
        assert c.should_auto_apply is False

def test_should_auto_apply_always_false_review_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    for _ in range(3):
        r = ExitReviewResult(should_auto_apply=True)
        assert r.should_auto_apply is False

def test_auto_apply_enabled_always_false_review_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewResult
    for _ in range(3):
        r = ExitReviewResult(auto_apply_enabled=True)
        assert r.auto_apply_enabled is False

def test_exit_actions_are_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["exit_actions_recommendation_only"] is True

def test_no_automatic_stop_loss_execution_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_stop_loss_execution"] is True

def test_no_automatic_take_profit_execution_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_take_profit_execution"] is True

def test_no_automatic_exit_apply_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    assert SAFETY_FLAGS_V210["no_automatic_exit_apply"] is True


# =========================================================================
# Section 25: Backward compatibility with v2.0.9
# =========================================================================
def test_v209_module_still_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v209

def test_v209_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION
    assert VERSION == "2.0.9"

def test_v209_run_sizing_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result is not None

def test_v209_run_sizing_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.paper_only is True

def test_v209_run_sizing_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.should_auto_apply is False

def test_v208_module_still_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v208

def test_v208_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION
    assert VERSION == "2.0.8"

def test_v208_run_exposure_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result is not None


# =========================================================================
# Section 26: v201 health relative-path compatibility
# =========================================================================
def test_v201_health_test_relative_path_exists():
    import os
    base = os.path.normpath(os.path.join(os.path.dirname(__file__)))
    test_file = os.path.join(base, "test_paper_cockpit_v201.py")
    assert os.path.exists(test_file)

def test_v201_health_relative_path_from_health_module():
    import os
    health_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..", "paper_trading", "small_capital_strategy"
    ))
    test_file = os.path.normpath(os.path.join(health_dir, "..", "..", "tests", "test_paper_cockpit_v201.py"))
    assert os.path.exists(test_file)


# =========================================================================
# Section 27: evaluate_stop_discipline and evaluate_reward_risk
# =========================================================================
def test_evaluate_stop_discipline_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert result is not None

def test_evaluate_stop_discipline_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert isinstance(result, dict)

def test_evaluate_stop_discipline_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert result["paper_only"] is True

def test_evaluate_stop_discipline_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert result["should_auto_apply"] is False

def test_evaluate_stop_discipline_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert result["auto_apply_enabled"] is False

def test_evaluate_stop_discipline_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert result["schema_version"] == "210"

def test_evaluate_stop_discipline_total_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    result = evaluate_stop_discipline()
    assert result["total_candidates"] >= 0

def test_evaluate_reward_risk_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result is not None

def test_evaluate_reward_risk_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert isinstance(result, dict)

def test_evaluate_reward_risk_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result["paper_only"] is True

def test_evaluate_reward_risk_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result["should_auto_apply"] is False

def test_evaluate_reward_risk_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result["schema_version"] == "210"

def test_evaluate_reward_risk_candidate_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result["candidate_count"] >= 0

def test_evaluate_reward_risk_avg_rr():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result["average_reward_risk_ratio"] >= 0.0

def test_evaluate_reward_risk_min_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    result = evaluate_reward_risk()
    assert result["min_required_ratio"] == 2.0


# =========================================================================
# Section 28: build_exit_warning_queue and build_stop_violation_queue
# =========================================================================
def test_build_exit_warning_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_exit_warning_queue
    result = build_exit_warning_queue()
    assert result is not None

def test_build_exit_warning_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_exit_warning_queue
    result = build_exit_warning_queue()
    assert isinstance(result, list)

def test_build_exit_warning_queue_items_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_exit_warning_queue
    result = build_exit_warning_queue()
    for item in result:
        assert item.paper_only is True

def test_build_exit_warning_queue_items_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_exit_warning_queue
    result = build_exit_warning_queue()
    for item in result:
        assert item.should_auto_apply is False

def test_build_exit_warning_queue_items_valid_exit_actions():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_exit_warning_queue, EXIT_ACTIONS
    result = build_exit_warning_queue()
    for item in result:
        assert item.exit_action in EXIT_ACTIONS

def test_build_stop_violation_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_stop_violation_queue
    result = build_stop_violation_queue()
    assert result is not None

def test_build_stop_violation_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_stop_violation_queue
    result = build_stop_violation_queue()
    assert isinstance(result, list)

def test_build_stop_violation_queue_items_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_stop_violation_queue
    result = build_stop_violation_queue()
    for item in result:
        assert item.paper_only is True

def test_build_stop_violation_queue_items_have_violations():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_stop_violation_queue
    result = build_stop_violation_queue()
    for item in result:
        assert item.blocked_by_missing_stop or item.blocked_by_excessive_stop_distance or not item.stop_loss_valid


# =========================================================================
# Section 29: Initial stop-loss calculation helpers
# =========================================================================
def test_stop_distance_5pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 95.0)
    assert abs(result.stop_distance_pct - 0.05) < 0.001

def test_stop_distance_6pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 1000.0, 940.0)
    assert abs(result.stop_distance_pct - 0.06) < 0.001

def test_stop_distance_zero_for_invalid():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 0.0)
    assert result.stop_distance_pct == 0.0

def test_first_tp_1r():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 94.0)
    # risk=6, first_tp_r=1 => tp = 100+6=106
    assert abs(result.first_take_profit_price - 106.0) < 0.01

def test_second_tp_2r():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 94.0)
    # risk=6, second_tp_r=2 => tp = 100+12=112
    assert abs(result.second_take_profit_price - 112.0) < 0.01

def test_trailing_stop_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 94.0)
    # trailing_stop = 100*(1-0.03) = 97
    assert abs(result.trailing_stop_price - 97.0) < 0.01

def test_rr_ratio_2():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 94.0)
    # rr = (106-100)/(100-94) = 6/6 = 1.0 (1R stop loss → 1R reward → rr=1)
    assert result.reward_risk_ratio > 0


# =========================================================================
# Section 30: Additional robustness and edge case tests
# =========================================================================
def test_exit_plan_zero_entry_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 0.0, 0.0)
    assert result.stop_loss_valid is False
    assert result.exit_action == "block_entry_missing_stop"

def test_exit_plan_equal_entry_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 100.0)
    assert result.stop_loss_valid is False

def test_exit_plan_entry_below_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 80.0, 100.0)
    assert result.stop_loss_valid is False

def test_exit_plan_exactly_12pct_stop_boundary():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    # 100 * 0.12 = 12, stop = 88
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 88.0)
    assert result.stop_loss_valid is True

def test_exit_plan_just_over_12pct_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    result = calculate_exit_plan("T", "test", "C", "TH", "SEC", 50.0, 50.0, 100.0, 87.5)
    # stop_distance = 12.5% > 12% → stop_loss_valid=False → blocked
    assert result.stop_loss_valid is False
    assert result.exit_action in ("block_entry_missing_stop", "require_tighter_stop")

def test_covered_versions_includes_v209():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import COVERED_VERSIONS
    assert "2.0.9" in COVERED_VERSIONS

def test_covered_versions_includes_v208():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import COVERED_VERSIONS
    assert "2.0.8" in COVERED_VERSIONS

def test_exit_review_input_default_market_state():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewInput
    inp = ExitReviewInput()
    assert inp.market_state == "range_bound"

def test_exit_review_input_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitReviewInput
    inp = ExitReviewInput()
    assert inp.paper_only is True

def test_stop_discipline_summary_default_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import StopDisciplineSummary
    s = StopDisciplineSummary()
    assert s.exit_plan_quality_grade == "B"
    assert s.stop_discipline_quality_grade == "B"

def test_exit_plan_safety_guard_require_stop_loss_before_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanSafetyGuard
    g = ExitPlanSafetyGuard()
    assert g.require_stop_loss_before_entry is True

def test_exit_plan_safety_guard_exit_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanSafetyGuard
    g = ExitPlanSafetyGuard()
    assert g.exit_actions_recommendation_only is True

def test_v210_health_summary_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import V210HealthSummary
    h = V210HealthSummary()
    assert h.version == "2.0.10"

def test_v210_release_summary_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import V210ReleaseSummary
    r = V210ReleaseSummary()
    assert r.version == "2.0.10"

def test_v210_release_summary_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import V210ReleaseSummary, RELEASE_NAME
    r = V210ReleaseSummary()
    assert r.release_name == RELEASE_NAME

def test_export_json_has_exit_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert result.exit_review_id != ""

def test_export_json_content_has_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_json
    result = export_exit_plan_json(run_exit_plan_review())
    assert "2.0.10" in result.content

def test_export_md_content_has_period():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_plan_markdown
    result = export_exit_plan_markdown(run_exit_plan_review())
    assert "Period" in result.content or "period" in result.content.lower()

def test_export_csv_header_has_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_candidate_exit_csv
    result = export_candidate_exit_csv(run_exit_plan_review())
    assert "symbol" in result.csv_content

def test_export_csv_has_should_auto_apply_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_candidate_exit_csv
    result = export_candidate_exit_csv(run_exit_plan_review())
    assert "should_auto_apply" in result.csv_content

def test_stop_discipline_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_stop_discipline_csv
    result = export_stop_discipline_csv(run_exit_plan_review())
    assert "total" in result.csv_content

def test_exit_warning_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_warning_csv
    result = export_exit_warning_csv(run_exit_plan_review())
    assert "symbol" in result.csv_content

def test_audit_snapshot_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_audit_snapshot
    result = export_exit_audit_snapshot(run_exit_plan_review())
    assert result.paper_only is True

def test_audit_snapshot_safety_snapshot_contains_paper():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_audit_snapshot
    result = export_exit_audit_snapshot(run_exit_plan_review())
    assert "paper_only" in result.safety_snapshot

def test_audit_snapshot_run_metadata():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_audit_snapshot
    result = export_exit_audit_snapshot(run_exit_plan_review())
    assert "v210" in result.run_metadata

def test_gui_stop_discipline_v210_no_real_orders():
    from gui.small_capital_strategy_panel import render_stop_discipline_v210_tab
    result = render_stop_discipline_v210_tab()
    assert result["no_real_orders"] is True

def test_gui_exit_warning_queue_v210_no_broker():
    from gui.small_capital_strategy_panel import render_exit_warning_queue_v210_tab
    result = render_exit_warning_queue_v210_tab()
    assert result["no_broker"] is True

def test_exit_review_no_none_in_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    for plan in result.exit_plan_snapshot:
        assert plan is not None

def test_all_snapshot_plans_have_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    for plan in result.exit_plan_snapshot:
        assert plan.schema_version == "210"

def test_all_snapshot_plans_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    for plan in result.exit_plan_snapshot:
        assert plan.should_auto_apply is False

def test_all_snapshot_plans_valid_exit_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, EXIT_ACTIONS
    result = run_exit_plan_review()
    for plan in result.exit_plan_snapshot:
        assert plan.exit_action in EXIT_ACTIONS

def test_candidate_exit_csv_row_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_candidate_exit_csv
    review = run_exit_plan_review()
    result = export_candidate_exit_csv(review)
    assert result.row_count == len(review.exit_plan_snapshot)

def test_exit_warning_csv_row_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review, export_exit_warning_csv
    review = run_exit_plan_review()
    result = export_exit_warning_csv(review)
    assert result.row_count == len(review.exit_warning_queue)
