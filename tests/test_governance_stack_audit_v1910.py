"""
tests/test_governance_stack_audit_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit — Audit Tests
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS, MIN_NEW_TESTS,
    COVERED_VERSIONS, COVERED_MODULES, CLI_COMMANDS, GUI_TABS,
    FORBIDDEN_ACTIONS, ALLOWED_AUDIT_ACTIONS, SAFETY_FLAGS, _ALL_MODEL_NAMES,
    verify_version, get_version_info, get_governance_stack_summary,
    run_safety_audit, assert_audit_safe, is_safe_export_path,
    audit_covered_modules, audit_cli_commands, audit_gui_tabs,
    audit_health_checks, audit_release_gates, audit_fixture_schemas,
    audit_scenario_schemas, audit_safety_flags, audit_backward_compatibility,
    run_full_governance_stack_audit,
    PaperGovernanceStackAuditInput, PaperGovernanceStackAuditResult,
    PaperGovernanceStackModule, PaperGovernanceStackVersion,
    PaperGovernanceStackCompatibilityResult,
    PaperGovernanceStackCliAuditResult, PaperGovernanceStackGuiAuditResult,
    PaperGovernanceStackHealthAuditResult, PaperGovernanceStackGateAuditResult,
    PaperGovernanceStackFixtureAuditResult, PaperGovernanceStackScenarioAuditResult,
    PaperGovernanceStackSafetyAuditResult, PaperGovernanceStackReleaseSummary,
    PaperGovernanceStackAuditReport, PaperGovernanceStackRecommendation,
)
import pytest


# --- Version constants ---

def test_version_is_1910():
    assert VERSION == "1.9.10"

def test_schema_version_is_1910():
    assert SCHEMA_VERSION == "1910"

def test_release_name_contains_governance():
    assert "Governance" in RELEASE_NAME or "Consolidation" in RELEASE_NAME

def test_baseline_tests_31469():
    assert BASELINE_TESTS == 31469

def test_min_new_tests_300():
    assert MIN_NEW_TESTS == 300

def test_covered_versions_count_6():
    assert len(COVERED_VERSIONS) == 6

def test_covered_modules_count_6():
    assert len(COVERED_MODULES) == 6

def test_v194_in_covered():
    assert "1.9.4" in COVERED_VERSIONS

def test_v195_in_covered():
    assert "1.9.5" in COVERED_VERSIONS

def test_v196_in_covered():
    assert "1.9.6" in COVERED_VERSIONS

def test_v197_in_covered():
    assert "1.9.7" in COVERED_VERSIONS

def test_v198_in_covered():
    assert "1.9.8" in COVERED_VERSIONS

def test_v199_in_covered():
    assert "1.9.9" in COVERED_VERSIONS

def test_cli_commands_count_14():
    assert len(CLI_COMMANDS) == 14

def test_governance_stack_version_in_cli():
    assert "governance-stack-version" in CLI_COMMANDS

def test_governance_stack_audit_in_cli():
    assert "governance-stack-audit" in CLI_COMMANDS

def test_governance_stack_health_in_cli():
    assert "governance-stack-health" in CLI_COMMANDS

def test_governance_stack_gate_in_cli():
    assert "governance-stack-gate" in CLI_COMMANDS

def test_governance_stack_compatibility_in_cli():
    assert "governance-stack-compatibility" in CLI_COMMANDS

def test_governance_stack_report_in_cli():
    assert "governance-stack-report" in CLI_COMMANDS

def test_gui_tabs_count_3():
    assert len(GUI_TABS) == 3

def test_governance_stack_audit_tab_in_gui():
    assert "governance_stack_audit" in GUI_TABS

def test_release_audit_tab_in_gui():
    assert "release_audit" in GUI_TABS

def test_compatibility_summary_tab_in_gui():
    assert "compatibility_summary" in GUI_TABS

def test_model_count_15():
    assert len(_ALL_MODEL_NAMES) == 15

def test_safety_flags_count_29():
    assert len(SAFETY_FLAGS) == 29

def test_forbidden_actions_count_15():
    assert len(FORBIDDEN_ACTIONS) == 15

def test_allowed_audit_actions_count_15():
    assert len(ALLOWED_AUDIT_ACTIONS) == 15

def test_all_model_names_are_strings():
    assert all(isinstance(n, str) for n in _ALL_MODEL_NAMES)


# --- Safety flags ---

def test_safety_paper_only_true():
    assert SAFETY_FLAGS.get("paper_only") is True

def test_safety_research_only_true():
    assert SAFETY_FLAGS.get("research_only") is True

def test_safety_simulate_only_true():
    assert SAFETY_FLAGS.get("simulate_only") is True

def test_safety_consolidation_only_true():
    assert SAFETY_FLAGS.get("consolidation_only") is True

def test_safety_release_audit_only_true():
    assert SAFETY_FLAGS.get("release_audit_only") is True

def test_safety_no_real_orders_true():
    assert SAFETY_FLAGS.get("no_real_orders") is True

def test_safety_no_broker_true():
    assert SAFETY_FLAGS.get("no_broker") is True

def test_safety_no_margin_true():
    assert SAFETY_FLAGS.get("no_margin") is True

def test_safety_no_leverage_true():
    assert SAFETY_FLAGS.get("no_leverage") is True

def test_safety_production_trading_blocked_true():
    assert SAFETY_FLAGS.get("production_trading_blocked") is True

def test_safety_audit_executes_order_false():
    assert SAFETY_FLAGS.get("audit_executes_order") is False

def test_safety_audit_mutates_strategy_false():
    assert SAFETY_FLAGS.get("audit_mutates_strategy") is False

def test_safety_audit_rebalances_real_false():
    assert SAFETY_FLAGS.get("audit_rebalances_real_portfolio") is False

def test_safety_dashboard_mutates_strategy_false():
    assert SAFETY_FLAGS.get("dashboard_mutates_strategy") is False

def test_safety_dashboard_places_real_order_false():
    assert SAFETY_FLAGS.get("dashboard_places_real_order") is False

def test_safety_export_triggers_real_order_false():
    assert SAFETY_FLAGS.get("export_triggers_real_order") is False

def test_safety_compatibility_check_executes_order_false():
    assert SAFETY_FLAGS.get("compatibility_check_executes_order") is False


# --- Forbidden / allowed actions ---

def test_buy_in_forbidden():
    assert "BUY" in FORBIDDEN_ACTIONS

def test_sell_in_forbidden():
    assert "SELL" in FORBIDDEN_ACTIONS

def test_live_activate_in_forbidden():
    assert "LIVE_ACTIVATE" in FORBIDDEN_ACTIONS

def test_broker_connect_in_forbidden():
    assert "BROKER_CONNECT" in FORBIDDEN_ACTIONS

def test_production_write_in_forbidden():
    assert "PRODUCTION_WRITE" in FORBIDDEN_ACTIONS

def test_paper_audit_in_allowed():
    assert "PAPER_AUDIT" in ALLOWED_AUDIT_ACTIONS

def test_paper_consolidate_in_allowed():
    assert "PAPER_CONSOLIDATE" in ALLOWED_AUDIT_ACTIONS

def test_paper_release_audit_in_allowed():
    assert "PAPER_RELEASE_AUDIT" in ALLOWED_AUDIT_ACTIONS

def test_no_overlap_forbidden_allowed():
    for action in FORBIDDEN_ACTIONS:
        assert action not in ALLOWED_AUDIT_ACTIONS

def test_no_overlap_allowed_forbidden():
    for action in ALLOWED_AUDIT_ACTIONS:
        assert action not in FORBIDDEN_ACTIONS


# --- verify_version ---

def test_verify_version_returns_true():
    assert verify_version() is True


# --- get_version_info ---

def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)

def test_version_info_version_1910():
    assert get_version_info()["version"] == "1.9.10"

def test_version_info_schema_1910():
    assert get_version_info()["schema_version"] == "1910"

def test_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_version_info_consolidation_only():
    assert get_version_info()["consolidation_only"] is True

def test_version_info_release_audit_only():
    assert get_version_info()["release_audit_only"] is True

def test_version_info_production_blocked():
    assert get_version_info()["production_trading_blocked"] is True


# --- get_governance_stack_summary ---

def test_get_governance_stack_summary_returns_dict():
    assert isinstance(get_governance_stack_summary(), dict)

def test_governance_stack_summary_version():
    assert get_governance_stack_summary()["version"] == "1.9.10"

def test_governance_stack_summary_paper_only():
    assert get_governance_stack_summary()["paper_only"] is True

def test_governance_stack_summary_consolidation_only():
    assert get_governance_stack_summary()["consolidation_only"] is True

def test_governance_stack_summary_model_count():
    assert get_governance_stack_summary()["model_count"] == 15


# --- run_safety_audit ---

def test_run_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)

def test_run_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True

def test_run_safety_audit_errors_empty():
    assert run_safety_audit()["errors"] == []

def test_run_safety_audit_flags_count():
    assert run_safety_audit()["safety_flags_count"] == 29

def test_run_safety_audit_forbidden_count():
    assert run_safety_audit()["forbidden_actions_count"] == 15

def test_run_safety_audit_allowed_count():
    assert run_safety_audit()["allowed_actions_count"] == 15

def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True


# --- assert_audit_safe ---

def test_assert_audit_safe_buy_raises():
    with pytest.raises(ValueError):
        assert_audit_safe("BUY")

def test_assert_audit_safe_live_activate_raises():
    with pytest.raises(ValueError):
        assert_audit_safe("LIVE_ACTIVATE")

def test_assert_audit_safe_production_write_raises():
    with pytest.raises(ValueError):
        assert_audit_safe("PRODUCTION_WRITE")

def test_assert_audit_safe_paper_audit_ok():
    result = assert_audit_safe("PAPER_AUDIT")
    assert result is None


# --- is_safe_export_path ---

def test_is_safe_export_path_paper_path_ok():
    assert is_safe_export_path("C:/Users/paper/report.json") is True

def test_is_safe_export_path_production_blocked():
    assert is_safe_export_path("C:/production/audit") is False

def test_is_safe_export_path_live_blocked():
    assert is_safe_export_path("/live/audit") is False

def test_is_safe_export_path_empty_blocked():
    assert is_safe_export_path("") is False

def test_is_safe_export_path_broker_blocked():
    assert is_safe_export_path("C:/broker/data") is False


# --- audit_covered_modules ---

def test_audit_covered_modules_returns_dict():
    assert isinstance(audit_covered_modules(), dict)

def test_audit_covered_modules_paper_only():
    assert audit_covered_modules()["paper_only"] is True

def test_audit_covered_modules_total_6():
    assert audit_covered_modules()["total"] == 6

def test_audit_covered_modules_results_is_dict():
    assert isinstance(audit_covered_modules()["results"], dict)


# --- audit_safety_flags ---

def test_audit_safety_flags_returns_dict():
    assert isinstance(audit_safety_flags(), dict)

def test_audit_safety_flags_all_consistent():
    assert audit_safety_flags()["all_consistent"] is True

def test_audit_safety_flags_errors_empty():
    assert audit_safety_flags()["errors"] == []

def test_audit_safety_flags_count():
    assert audit_safety_flags()["safety_flags_count"] == 29

def test_audit_safety_flags_forbidden_count():
    assert audit_safety_flags()["forbidden_actions_count"] == 15

def test_audit_safety_flags_allowed_count():
    assert audit_safety_flags()["allowed_actions_count"] == 15


# --- audit_cli_commands ---

def test_audit_cli_commands_returns_dict():
    assert isinstance(audit_cli_commands(), dict)

def test_audit_cli_commands_paper_only():
    assert audit_cli_commands()["paper_only"] is True

def test_audit_cli_commands_executes_order_false():
    assert audit_cli_commands()["audit_executes_order"] is False


# --- audit_gui_tabs ---

def test_audit_gui_tabs_returns_dict():
    assert isinstance(audit_gui_tabs(), dict)

def test_audit_gui_tabs_paper_only():
    assert audit_gui_tabs()["paper_only"] is True

def test_audit_gui_tabs_dashboard_mutates_false():
    assert audit_gui_tabs()["dashboard_mutates_strategy"] is False


# --- audit_backward_compatibility ---

def test_audit_backward_compatibility_returns_dict():
    assert isinstance(audit_backward_compatibility(), dict)

def test_audit_backward_compatibility_paper_only():
    assert audit_backward_compatibility()["paper_only"] is True


# --- run_full_governance_stack_audit ---

def test_run_full_governance_stack_audit_returns_dict():
    assert isinstance(run_full_governance_stack_audit(), dict)

def test_run_full_audit_paper_only():
    assert run_full_governance_stack_audit()["paper_only"] is True

def test_run_full_audit_no_real_orders():
    assert run_full_governance_stack_audit()["no_real_orders"] is True

def test_run_full_audit_consolidation_only():
    assert run_full_governance_stack_audit()["consolidation_only"] is True

def test_run_full_audit_release_audit_only():
    assert run_full_governance_stack_audit()["release_audit_only"] is True

def test_run_full_audit_executes_order_false():
    assert run_full_governance_stack_audit()["audit_executes_order"] is False

def test_run_full_audit_mutates_strategy_false():
    assert run_full_governance_stack_audit()["audit_mutates_strategy"] is False

def test_run_full_audit_has_checks():
    result = run_full_governance_stack_audit()
    assert "checks" in result
    assert isinstance(result["checks"], list)
    assert len(result["checks"]) > 0

def test_run_full_audit_has_status():
    assert "status" in run_full_governance_stack_audit()

def test_run_full_audit_has_all_passed_field():
    result = run_full_governance_stack_audit()
    assert "all_passed" in result
    assert isinstance(result["all_passed"], bool)


# --- Models ---

def test_audit_input_schema_version():
    assert PaperGovernanceStackAuditInput().schema_version == "1910"

def test_audit_input_paper_only():
    assert PaperGovernanceStackAuditInput().paper_only is True

def test_audit_input_consolidation_only():
    assert PaperGovernanceStackAuditInput().consolidation_only is True

def test_audit_input_release_audit_only():
    assert PaperGovernanceStackAuditInput().release_audit_only is True

def test_audit_input_executes_order_false():
    assert PaperGovernanceStackAuditInput().audit_executes_order is False

def test_audit_result_schema_version():
    assert PaperGovernanceStackAuditResult().schema_version == "1910"

def test_audit_result_executes_order_false():
    assert PaperGovernanceStackAuditResult().audit_executes_order is False

def test_audit_result_mutates_strategy_false():
    assert PaperGovernanceStackAuditResult().audit_mutates_strategy is False

def test_audit_result_rebalances_false():
    assert PaperGovernanceStackAuditResult().audit_rebalances_real_portfolio is False

def test_stack_module_schema_version():
    assert PaperGovernanceStackModule().schema_version == "1910"

def test_stack_module_paper_only():
    assert PaperGovernanceStackModule().paper_only is True

def test_stack_version_schema_version():
    assert PaperGovernanceStackVersion().schema_version == "1910"

def test_stack_version_consolidation_only():
    assert PaperGovernanceStackVersion().consolidation_only is True

def test_compat_result_schema_version():
    assert PaperGovernanceStackCompatibilityResult().schema_version == "1910"

def test_compat_result_executes_order_false():
    assert PaperGovernanceStackCompatibilityResult().compatibility_check_executes_order is False

def test_cli_audit_result_schema_version():
    assert PaperGovernanceStackCliAuditResult().schema_version == "1910"

def test_cli_audit_result_executes_order_false():
    assert PaperGovernanceStackCliAuditResult().audit_executes_order is False

def test_gui_audit_result_schema_version():
    assert PaperGovernanceStackGuiAuditResult().schema_version == "1910"

def test_gui_audit_result_mutates_false():
    assert PaperGovernanceStackGuiAuditResult().dashboard_mutates_strategy is False

def test_gui_audit_result_places_real_order_false():
    assert PaperGovernanceStackGuiAuditResult().dashboard_places_real_order is False

def test_health_audit_result_schema_version():
    assert PaperGovernanceStackHealthAuditResult().schema_version == "1910"

def test_gate_audit_result_schema_version():
    assert PaperGovernanceStackGateAuditResult().schema_version == "1910"

def test_fixture_audit_result_schema_version():
    assert PaperGovernanceStackFixtureAuditResult().schema_version == "1910"

def test_scenario_audit_result_schema_version():
    assert PaperGovernanceStackScenarioAuditResult().schema_version == "1910"

def test_safety_audit_result_schema_version():
    assert PaperGovernanceStackSafetyAuditResult().schema_version == "1910"

def test_safety_audit_result_executes_order_false():
    assert PaperGovernanceStackSafetyAuditResult().audit_executes_order is False

def test_release_summary_schema_version():
    assert PaperGovernanceStackReleaseSummary().schema_version == "1910"

def test_release_summary_consolidation_only():
    assert PaperGovernanceStackReleaseSummary().consolidation_only is True

def test_release_summary_release_audit_only():
    assert PaperGovernanceStackReleaseSummary().release_audit_only is True

def test_audit_report_schema_version():
    assert PaperGovernanceStackAuditReport().schema_version == "1910"

def test_audit_report_executes_order_false():
    assert PaperGovernanceStackAuditReport().audit_executes_order is False

def test_audit_report_mutates_strategy_false():
    assert PaperGovernanceStackAuditReport().audit_mutates_strategy is False

def test_audit_report_rebalances_false():
    assert PaperGovernanceStackAuditReport().audit_rebalances_real_portfolio is False

def test_audit_report_triggers_real_order_false():
    assert PaperGovernanceStackAuditReport().report_triggers_real_order is False

def test_recommendation_schema_version():
    assert PaperGovernanceStackRecommendation().schema_version == "1910"

def test_recommendation_executes_order_false():
    assert PaperGovernanceStackRecommendation().recommendation_executes_order is False

def test_recommendation_mutates_strategy_false():
    assert PaperGovernanceStackRecommendation().recommendation_mutates_strategy is False
