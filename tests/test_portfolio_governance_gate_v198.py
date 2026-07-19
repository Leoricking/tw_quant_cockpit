"""
tests/test_portfolio_governance_gate_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Release Gate Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.portfolio_governance_release_gate_v198 import (
    run_release_gate, run_gate, GATE_VERSION, BASELINE_TESTS, MIN_NEW_TESTS,
)


class TestReleaseGateBasics:
    def test_returns_dict(self):
        assert isinstance(run_release_gate(), dict)

    def test_gate_passed_is_True(self):
        assert run_release_gate()["gate_passed"] is True

    def test_failed_is_0(self):
        assert run_release_gate()["failed"] == 0

    def test_passed_count_equals_total(self):
        r = run_release_gate()
        assert r["passed_count"] == r["total"]

    def test_gate_version_is_1_9_8(self):
        assert run_release_gate()["gate_version"] == "1.9.8"

    def test_baseline_tests_is_30361(self):
        assert run_release_gate()["baseline_tests"] == 30361

    def test_min_new_tests_is_400(self):
        assert run_release_gate()["min_new_tests"] == 400

    def test_paper_only_True(self):
        assert run_release_gate()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert run_release_gate()["no_real_orders"] is True

    def test_not_investment_advice_True(self):
        assert run_release_gate()["not_investment_advice"] is True

    def test_checks_is_list(self):
        assert isinstance(run_release_gate()["checks"], list)

    def test_checks_not_empty(self):
        assert len(run_release_gate()["checks"]) > 0

    def test_all_checks_pass(self):
        for c in run_release_gate()["checks"]:
            assert c["passed"] is True, f"Gate check failed: {c['name']}"


class TestGateConstants:
    def test_gate_version_constant(self):
        assert GATE_VERSION == "1.9.8"

    def test_baseline_tests_constant(self):
        assert BASELINE_TESTS == 30361

    def test_min_new_tests_constant(self):
        assert MIN_NEW_TESTS == 400


class TestRunGateAlias:
    def test_run_gate_is_callable(self):
        assert callable(run_gate)

    def test_run_gate_returns_dict(self):
        assert isinstance(run_gate(), dict)

    def test_run_gate_gate_passed_True(self):
        assert run_gate()["gate_passed"] is True

    def test_run_gate_same_result_as_run_release_gate(self):
        r1 = run_release_gate()
        r2 = run_gate()
        assert r1["gate_passed"] == r2["gate_passed"]
        assert r1["total"] == r2["total"]


class TestIndividualGateChecks:
    def _get_check(self, name):
        checks = {c["name"]: c for c in run_release_gate()["checks"]}
        return checks.get(name)

    def test_version_match_check_passes(self):
        c = self._get_check("version_match_1.9.8")
        assert c is not None
        assert c["passed"] is True

    def test_schema_version_check_passes(self):
        c = self._get_check("schema_version_match_198")
        assert c is not None
        assert c["passed"] is True

    def test_model_count_check_passes(self):
        c = self._get_check("model_count_26")
        assert c is not None
        assert c["passed"] is True

    def test_scenarios_count_check_passes(self):
        c = self._get_check("scenarios_count_75")
        assert c is not None
        assert c["passed"] is True

    def test_fixtures_count_check_passes(self):
        c = self._get_check("fixtures_count_75")
        assert c is not None
        assert c["passed"] is True

    def test_safety_all_safe_check_passes(self):
        c = self._get_check("safety_all_safe_True")
        assert c is not None
        assert c["passed"] is True

    def test_health_all_passed_check_passes(self):
        c = self._get_check("health_all_passed_True")
        assert c is not None
        assert c["passed"] is True

    def test_report_sections_count_check_passes(self):
        c = self._get_check("report_sections_count_12")
        assert c is not None
        assert c["passed"] is True

    def test_gui_tab_count_check_passes(self):
        c = self._get_check("gui_tab_count_gte_163")
        assert c is not None
        assert c["passed"] is True

    def test_cli_commands_count_check_passes(self):
        c = self._get_check("cli_commands_count_19")
        assert c is not None
        assert c["passed"] is True

    def test_baseline_tests_check_passes(self):
        c = self._get_check("baseline_tests_gte_30361")
        assert c is not None
        assert c["passed"] is True

    def test_min_new_tests_check_passes(self):
        c = self._get_check("min_new_tests_gte_400")
        assert c is not None
        assert c["passed"] is True

    def test_no_forbidden_in_allowed_check_passes(self):
        c = self._get_check("no_forbidden_in_allowed")
        assert c is not None
        assert c["passed"] is True

    def test_paper_only_flag_check_passes(self):
        c = self._get_check("version_info_paper_only_True")
        assert c is not None
        assert c["passed"] is True

    def test_analytics_executes_decision_check_passes(self):
        c = self._get_check("version_info_analytics_executes_decision_False")
        assert c is not None
        assert c["passed"] is True

    def test_dashboard_mutates_strategy_check_passes(self):
        c = self._get_check("version_info_dashboard_mutates_strategy_False")
        assert c is not None
        assert c["passed"] is True

    def test_report_triggers_rebalance_check_passes(self):
        c = self._get_check("version_info_report_triggers_rebalance_False")
        assert c is not None
        assert c["passed"] is True

    def test_engine_compute_risk_grade_check_passes(self):
        c = self._get_check("engine_compute_risk_grade_0.0_LOW")
        assert c is not None
        assert c["passed"] is True

    def test_gui_tab_portfolio_governance_check_passes(self):
        c = self._get_check("gui_tab_names_has_portfolio_governance")
        assert c is not None
        assert c["passed"] is True

    def test_gui_tab_risk_overlay_check_passes(self):
        c = self._get_check("gui_tab_names_has_risk_overlay")
        assert c is not None
        assert c["passed"] is True

    def test_gui_tab_exposure_dashboard_check_passes(self):
        c = self._get_check("gui_tab_names_has_exposure_dashboard")
        assert c is not None
        assert c["passed"] is True

    def test_assert_safe_blocks_place_real_order_check_passes(self):
        c = self._get_check("assert_safe_blocks_place_real_order")
        assert c is not None
        assert c["passed"] is True

    def test_assert_safe_blocks_broker_check_passes(self):
        c = self._get_check("assert_safe_blocks_submit_broker_order")
        assert c is not None
        assert c["passed"] is True

    def test_total_checks_gte_60(self):
        r = run_release_gate()
        assert r["total"] >= 60
