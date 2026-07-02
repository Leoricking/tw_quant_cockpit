"""
tests/test_paper_attribution_scenarios_v167.py
Tests for paper attribution scenario registry v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.scenario_registry_v167 import (
    ScenarioRegistry,
    _SCENARIOS,
    _BY_ID,
    _BY_CATEGORY,
    STATUS_PASS, STATUS_FAIL, STATUS_BLOCKED, STATUS_DEGRADED,
    STATUS_INSUFFICIENT, STATUS_EMPTY,
    CAT_RETURN, CAT_PNL, CAT_SELECTION, CAT_ALLOCATION, CAT_TIMING,
    CAT_EXECUTION, CAT_COST, CAT_SLIPPAGE, CAT_TURNOVER, CAT_EXPOSURE,
    CAT_RISK, CAT_DRAWDOWN, CAT_REGIME, CAT_BENCHMARK, CAT_FACTOR,
    CAT_STRATEGY, CAT_SESSION, CAT_SYMBOL, CAT_SECTOR, CAT_PORTFOLIO,
    CAT_RECON, CAT_SCORE, CAT_SAFETY, CAT_REGRESSION, CAT_INTEGRATION,
)


class TestScenarioCount:
    def test_at_least_80_scenarios(self):
        assert len(_SCENARIOS) >= 80

    def test_unique_ids(self):
        ids = [s["id"] for s in _SCENARIOS]
        assert len(ids) == len(set(ids)), "Duplicate scenario IDs found"


class TestScenarioSchema:
    def test_all_have_id(self):
        for s in _SCENARIOS:
            assert s.get("id"), f"Missing id in {s}"

    def test_all_have_category(self):
        for s in _SCENARIOS:
            assert s.get("category"), f"Missing category in {s}"

    def test_all_have_name(self):
        for s in _SCENARIOS:
            assert s.get("name"), f"Missing name in {s}"

    def test_all_have_description(self):
        for s in _SCENARIOS:
            assert s.get("description"), f"Missing description in {s}"

    def test_all_have_expected_status(self):
        for s in _SCENARIOS:
            assert "expected_status" in s, f"Missing expected_status in {s['id']}"

    def test_all_have_paper_only(self):
        for s in _SCENARIOS:
            assert s.get("paper_only") is True, f"{s['id']} missing paper_only=True"

    def test_all_expected_statuses_valid(self):
        valid = {STATUS_PASS, STATUS_FAIL, STATUS_BLOCKED,
                 STATUS_DEGRADED, STATUS_INSUFFICIENT, STATUS_EMPTY}
        for s in _SCENARIOS:
            assert s["expected_status"] in valid, \
                f"{s['id']}: unknown status {s['expected_status']!r}"


class TestScenarioCategories:
    def test_return_decomposition_exists(self):
        assert CAT_RETURN in _BY_CATEGORY

    def test_pnl_attribution_exists(self):
        assert CAT_PNL in _BY_CATEGORY

    def test_selection_attribution_exists(self):
        assert CAT_SELECTION in _BY_CATEGORY

    def test_allocation_attribution_exists(self):
        assert CAT_ALLOCATION in _BY_CATEGORY

    def test_timing_attribution_exists(self):
        assert CAT_TIMING in _BY_CATEGORY

    def test_execution_attribution_exists(self):
        assert CAT_EXECUTION in _BY_CATEGORY

    def test_cost_attribution_exists(self):
        assert CAT_COST in _BY_CATEGORY

    def test_risk_attribution_exists(self):
        assert CAT_RISK in _BY_CATEGORY

    def test_drawdown_attribution_exists(self):
        assert CAT_DRAWDOWN in _BY_CATEGORY

    def test_regime_attribution_exists(self):
        assert CAT_REGIME in _BY_CATEGORY

    def test_reconciliation_exists(self):
        assert CAT_RECON in _BY_CATEGORY

    def test_scorecard_exists(self):
        assert CAT_SCORE in _BY_CATEGORY

    def test_safety_exists(self):
        assert CAT_SAFETY in _BY_CATEGORY

    def test_regression_exists(self):
        assert CAT_REGRESSION in _BY_CATEGORY

    def test_integration_exists(self):
        assert CAT_INTEGRATION in _BY_CATEGORY


class TestScenaryRegistryAPI:
    def setup_method(self):
        self.reg = ScenarioRegistry()

    def test_get_existing_by_id(self):
        s = self.reg.get("RD-001")
        assert s is not None
        assert s["id"] == "RD-001"

    def test_get_nonexistent_returns_none(self):
        assert self.reg.get("FAKE-999") is None

    def test_get_by_category_return_decomp(self):
        cats = self.reg.get_by_category(CAT_RETURN)
        assert len(cats) >= 5

    def test_get_by_category_nonexistent_empty(self):
        cats = self.reg.get_by_category("nonexistent_cat")
        assert cats == []

    def test_list_ids_sorted(self):
        ids = self.reg.list_ids()
        assert ids == sorted(ids)

    def test_list_ids_complete(self):
        ids = self.reg.list_ids()
        assert len(ids) >= 80

    def test_list_categories_sorted(self):
        cats = self.reg.list_categories()
        assert cats == sorted(cats)

    def test_count_at_least_80(self):
        assert self.reg.count() >= 80

    def test_count_by_status_pass(self):
        pass_count = self.reg.count_by_status(STATUS_PASS)
        assert pass_count >= 30

    def test_count_by_status_blocked(self):
        blocked_count = self.reg.count_by_status(STATUS_BLOCKED)
        assert blocked_count >= 1

    def test_find_by_name(self):
        s = self.reg.find_by_name("reconciled_within_tolerance")
        assert s is not None

    def test_find_by_name_nonexistent(self):
        s = self.reg.find_by_name("nonexistent_scenario_name_xyz")
        assert s is None

    def test_all_scenarios_returns_list(self):
        all_s = self.reg.all_scenarios()
        assert isinstance(all_s, list)
        assert len(all_s) >= 80

    def test_summarize_returns_dict(self):
        s = self.reg.summarize()
        assert isinstance(s, dict)

    def test_summarize_total_correct(self):
        s = self.reg.summarize()
        assert s["total"] >= 80

    def test_summarize_paper_only(self):
        s = self.reg.summarize()
        assert s["paper_only"] is True


class TestSpecificScenarios:
    def setup_method(self):
        self.reg = ScenarioRegistry()

    def test_rd_001_return_decomp(self):
        s = self.reg.get("RD-001")
        assert s["category"] == CAT_RETURN

    def test_se_003_no_benchmark_insufficient(self):
        s = self.reg.get("SE-003")
        assert s["expected_status"] == STATUS_INSUFFICIENT

    def test_ex_003_not_simulated_blocked(self):
        s = self.reg.get("EX-003")
        assert s["expected_status"] == STATUS_BLOCKED

    def test_sf_001_forbidden_field_blocked(self):
        s = self.reg.get("SF-001")
        assert s["expected_status"] == STATUS_BLOCKED

    def test_sf_002_missing_marker_fails(self):
        s = self.reg.get("SF-002")
        assert s["expected_status"] == STATUS_FAIL

    def test_rc_004_large_residual_fails(self):
        s = self.reg.get("RC-004")
        assert s["expected_status"] == STATUS_FAIL

    def test_rc_005_residual_never_zeroed(self):
        s = self.reg.get("RC-005")
        assert s["expected_status"] == STATUS_PASS

    def test_qs_002_real_markers_blocked(self):
        s = self.reg.get("QS-002")
        assert s["expected_status"] == STATUS_BLOCKED

    def test_rg_003_unknown_regime_not_forced(self):
        s = self.reg.get("RG-003")
        assert s["expected_status"] == STATUS_PASS

    def test_bm_002_missing_benchmark_empty(self):
        s = self.reg.get("BM-002")
        assert s["expected_status"] == STATUS_EMPTY
