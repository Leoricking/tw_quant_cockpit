"""
tests/test_integrated_strategy_gate_v178.py
Release gate tests for Small Capital Strategy Integration v1.7.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


class TestReleaseGateImport:
    def test_release_gate_importable(self):
        from release.small_capital_strategy_integration_release_gate_v178 import run_release_gate
        assert callable(run_release_gate)

    def test_gate_version_constant(self):
        from release.small_capital_strategy_integration_release_gate_v178 import GATE_VERSION
        assert GATE_VERSION == "1.7.8"

    def test_min_checks_constant(self):
        from release.small_capital_strategy_integration_release_gate_v178 import MIN_CHECKS
        assert MIN_CHECKS >= 70

    def test_gate_class_importable(self):
        from release.small_capital_strategy_integration_release_gate_v178 import (
            SmallCapitalStrategyIntegrationReleaseGate,
        )
        assert SmallCapitalStrategyIntegrationReleaseGate is not None

    def test_run_gate_alias(self):
        from release.small_capital_strategy_integration_release_gate_v178 import run_gate
        assert callable(run_gate)


class TestReleaseGateResult:
    @pytest.fixture(scope="class")
    def gate_result(self):
        from release.small_capital_strategy_integration_release_gate_v178 import run_release_gate
        return run_release_gate()

    def test_gate_passed(self, gate_result):
        assert gate_result["gate_passed"] is True

    def test_failed_zero(self, gate_result):
        assert gate_result["failed"] == 0

    def test_total_ge_70(self, gate_result):
        assert gate_result["total"] >= 70

    def test_passed_ge_70(self, gate_result):
        assert gate_result["passed"] >= 70

    def test_passed_equals_total(self, gate_result):
        assert gate_result["passed"] == gate_result["total"]

    def test_gate_version_in_result(self, gate_result):
        assert gate_result["gate_version"] == "1.7.8"

    def test_checks_is_list(self, gate_result):
        assert isinstance(gate_result["checks"], list)

    def test_all_checks_passed(self, gate_result):
        failed = [c for c in gate_result["checks"] if not c.get("passed")]
        assert failed == [], f"Failed checks: {[c['name'] for c in failed]}"

    def test_checks_have_name(self, gate_result):
        for c in gate_result["checks"]:
            assert "name" in c and c["name"]

    def test_checks_have_passed_key(self, gate_result):
        for c in gate_result["checks"]:
            assert "passed" in c

    def test_no_error_in_passed_checks(self, gate_result):
        for c in gate_result["checks"]:
            if c.get("passed"):
                assert c.get("error") is None

    def test_gate_is_deterministic(self):
        from release.small_capital_strategy_integration_release_gate_v178 import run_release_gate
        r1 = run_release_gate()
        r2 = run_release_gate()
        assert r1["gate_passed"] == r2["gate_passed"]
        assert r1["total"] == r2["total"]
        assert r1["failed"] == r2["failed"]


class TestSpecificGateChecks:
    @pytest.fixture(scope="class")
    def checks_by_name(self):
        from release.small_capital_strategy_integration_release_gate_v178 import run_release_gate
        result = run_release_gate()
        return {c["name"]: c for c in result["checks"]}

    def _assert_passed(self, checks_by_name, name):
        assert name in checks_by_name, f"Check '{name}' not found"
        assert checks_by_name[name]["passed"], f"Check '{name}' failed: {checks_by_name[name].get('error')}"

    def test_health_all_passed(self, checks_by_name):
        self._assert_passed(checks_by_name, "health_all_passed")

    def test_health_status_pass(self, checks_by_name):
        self._assert_passed(checks_by_name, "health_status_pass")

    def test_health_failed_zero(self, checks_by_name):
        self._assert_passed(checks_by_name, "health_failed_zero")

    def test_gate_version_1_7_8(self, checks_by_name):
        self._assert_passed(checks_by_name, "gate_version_1_7_8")

    def test_gate_release_name(self, checks_by_name):
        self._assert_passed(checks_by_name, "gate_release_name")

    def test_safety_no_real_order(self, checks_by_name):
        self._assert_passed(checks_by_name, "safety_no_real_order")

    def test_safety_no_broker_exec(self, checks_by_name):
        self._assert_passed(checks_by_name, "safety_no_broker_exec")

    def test_safety_paper_only(self, checks_by_name):
        self._assert_passed(checks_by_name, "safety_paper_only")

    def test_safety_no_margin(self, checks_by_name):
        self._assert_passed(checks_by_name, "safety_no_margin")

    def test_model_count_14(self, checks_by_name):
        self._assert_passed(checks_by_name, "model_count_14")

    def test_model_input_paper_only(self, checks_by_name):
        self._assert_passed(checks_by_name, "model_input_paper_only")

    def test_broker_exec_disabled(self, checks_by_name):
        self._assert_passed(checks_by_name, "broker_exec_disabled")

    def test_scenarios_ge_70(self, checks_by_name):
        self._assert_passed(checks_by_name, "scenarios_ge_70")

    def test_fixtures_ge_70(self, checks_by_name):
        self._assert_passed(checks_by_name, "fixtures_ge_70")

    def test_fixtures_registry_valid(self, checks_by_name):
        self._assert_passed(checks_by_name, "fixtures_registry_valid")

    def test_gui_panel_version_178(self, checks_by_name):
        self._assert_passed(checks_by_name, "gui_panel_version_178")

    def test_cli_is_cmds_ge_17(self, checks_by_name):
        self._assert_passed(checks_by_name, "cli_is_cmds_ge_17")

    def test_no_broker_flag(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_broker_flag")

    def test_no_real_orders_flag(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_real_orders_flag")

    def test_no_margin_flag(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_margin_flag")

    def test_no_production_writes(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_production_writes")

    def test_compat_v177(self, checks_by_name):
        self._assert_passed(checks_by_name, "compat_v177")

    def test_compat_v176(self, checks_by_name):
        self._assert_passed(checks_by_name, "compat_v176")

    def test_compat_v175(self, checks_by_name):
        self._assert_passed(checks_by_name, "compat_v175")

    def test_compat_v174(self, checks_by_name):
        self._assert_passed(checks_by_name, "compat_v174")

    def test_compat_v173(self, checks_by_name):
        self._assert_passed(checks_by_name, "compat_v173")

    def test_compat_v172(self, checks_by_name):
        self._assert_passed(checks_by_name, "compat_v172")

    def test_no_stubs(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_stubs")

    def test_no_live_broker(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_live_broker")

    def test_no_real_account(self, checks_by_name):
        self._assert_passed(checks_by_name, "no_real_account")
