"""
tests/test_failure_validation_gui_report_v165.py — GUI Panel & Report tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import os
import pytest

# Force headless mode for panel tests
os.environ["FAILURE_INJECTION_PANEL_HEADLESS"] = "1"

from gui.failure_injection_recovery_panel import (
    HEADLESS_SAFE,
    PAPER_ONLY as GUI_PAPER_ONLY,
    PRODUCTION_CHAOS_ENABLED as GUI_PC,
    REAL_FAILURE_INJECTION_ENABLED as GUI_RFI,
    RESEARCH_ONLY as GUI_RESEARCH_ONLY,
    TAB_NAMES,
    FailureInjectionRecoveryPanel,
    FailureInjectionRecoveryPanelState,
    get_panel_state,
    tab_count,
    tab_names,
)
from paper_trading.failure_validation.report_v165 import (
    EXTERNAL_PUBLISH_ENABLED,
    PAPER_ONLY as REPORT_PAPER_ONLY,
    RESEARCH_ONLY as REPORT_RESEARCH_ONLY,
    FailureInjectionReport,
    ReportStore,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestGuiReportSafetyFlags:
    def test_gui_real_failure_injection_disabled(self):
        assert GUI_RFI is False

    def test_gui_production_chaos_disabled(self):
        assert GUI_PC is False

    def test_gui_paper_only(self):
        assert GUI_PAPER_ONLY is True

    def test_gui_research_only(self):
        assert GUI_RESEARCH_ONLY is True

    def test_headless_safe_true(self):
        assert HEADLESS_SAFE is True

    def test_external_publish_disabled(self):
        assert EXTERNAL_PUBLISH_ENABLED is False

    def test_report_paper_only(self):
        assert REPORT_PAPER_ONLY is True

    def test_report_research_only(self):
        assert REPORT_RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# TAB_NAMES
# ---------------------------------------------------------------------------

class TestTabNames:
    def test_tab_count_is_16(self):
        assert len(TAB_NAMES) == 16

    def test_tab_names_function_returns_16(self):
        assert len(tab_names()) == 16

    def test_tab_count_function_returns_16(self):
        assert tab_count() == 16

    def test_overview_tab_present(self):
        assert "Overview" in TAB_NAMES

    def test_scenarios_tab_present(self):
        assert "Scenarios" in TAB_NAMES

    def test_injection_results_tab_present(self):
        assert "Injection Results" in TAB_NAMES

    def test_detection_tab_present(self):
        assert "Detection" in TAB_NAMES

    def test_recovery_plans_tab_present(self):
        assert "Recovery Plans" in TAB_NAMES

    def test_scorecard_tab_present(self):
        assert "Scorecard" in TAB_NAMES

    def test_rto_rpo_tab_present(self):
        assert "RTO/RPO" in TAB_NAMES

    def test_reports_tab_present(self):
        assert "Reports" in TAB_NAMES

    def test_tab_names_returns_copy(self):
        t1 = tab_names()
        t2 = tab_names()
        assert t1 == t2
        t1.clear()
        assert tab_count() == 16  # original unaffected


# ---------------------------------------------------------------------------
# FailureInjectionRecoveryPanelState
# ---------------------------------------------------------------------------

class TestPanelState:
    def test_initial_active_tab_is_overview(self):
        state = FailureInjectionRecoveryPanelState()
        assert state.active_tab == "Overview"

    def test_set_valid_tab_returns_true(self):
        state = FailureInjectionRecoveryPanelState()
        assert state.set_tab("Scenarios") is True
        assert state.active_tab == "Scenarios"

    def test_set_invalid_tab_returns_false(self):
        state = FailureInjectionRecoveryPanelState()
        assert state.set_tab("NonExistentTab") is False
        assert state.active_tab == "Overview"  # unchanged

    def test_add_injection_result(self):
        state = FailureInjectionRecoveryPanelState()
        state.add_injection_result({"status": "INJECTED", "result_id": "r1"})
        assert len(state.injection_results) == 1

    def test_add_recovery_validation(self):
        state = FailureInjectionRecoveryPanelState()
        state.add_recovery_validation({"final_state": "RECOVERED"})
        assert len(state.recovery_validations) == 1

    def test_add_scorecard(self):
        state = FailureInjectionRecoveryPanelState()
        state.add_scorecard({"total_score": 85})
        assert len(state.scorecards) == 1

    def test_add_alert(self):
        state = FailureInjectionRecoveryPanelState()
        state.add_alert({"alert_id": "a1", "title": "Stale data"})
        assert len(state.alerts) == 1

    def test_add_incident(self):
        state = FailureInjectionRecoveryPanelState()
        state.add_incident({"incident_id": "i1", "status": "OPEN"})
        assert len(state.incidents) == 1

    def test_summary_has_required_keys(self):
        state = FailureInjectionRecoveryPanelState()
        s = state.summary()
        assert "active_tab" in s
        assert "tabs" in s
        assert "tab_count" in s
        assert "paper_only" in s
        assert "research_only" in s
        assert "real_failure_injection_enabled" in s

    def test_summary_paper_only_true(self):
        state = FailureInjectionRecoveryPanelState()
        assert state.summary()["paper_only"] is True

    def test_summary_real_injection_false(self):
        state = FailureInjectionRecoveryPanelState()
        assert state.summary()["real_failure_injection_enabled"] is False

    def test_summary_tab_count_16(self):
        state = FailureInjectionRecoveryPanelState()
        assert state.summary()["tab_count"] == 16


# ---------------------------------------------------------------------------
# get_panel_state and FailureInjectionRecoveryPanel
# ---------------------------------------------------------------------------

class TestPanelInstantiation:
    def test_get_panel_state_returns_state(self):
        state = get_panel_state()
        assert isinstance(state, FailureInjectionRecoveryPanelState)

    def test_panel_instantiates_in_headless(self):
        panel = FailureInjectionRecoveryPanel()
        assert panel is not None

    def test_panel_headless_true(self):
        panel = FailureInjectionRecoveryPanel()
        assert panel._headless is True

    def test_panel_has_state(self):
        panel = FailureInjectionRecoveryPanel()
        assert isinstance(panel._state, FailureInjectionRecoveryPanelState)


# ---------------------------------------------------------------------------
# FailureInjectionReport
# ---------------------------------------------------------------------------

class TestFailureInjectionReport:
    def test_report_instantiates(self):
        r = FailureInjectionReport(run_id="run_1", scenario_name="md_timeout_001")
        assert r is not None

    def test_report_has_run_id(self):
        r = FailureInjectionReport(run_id="run_42")
        assert r.run_id == "run_42"

    def test_report_has_scenario_name(self):
        r = FailureInjectionReport(scenario_name="md_stale_001")
        assert r.scenario_name == "md_stale_001"

    def test_report_initial_sections_empty(self):
        r = FailureInjectionReport()
        assert r.sections == []

    def test_add_section(self):
        r = FailureInjectionReport()
        r.add_section("Detection", {"detected": True})
        assert len(r.sections) == 1

    def test_add_multiple_sections(self):
        r = FailureInjectionReport()
        r.add_section("Detection", {"detected": True})
        r.add_section("Containment", {"contained": True})
        r.add_section("Recovery", {"recovered": True})
        assert len(r.sections) == 3

    def test_summary_has_required_keys(self):
        r = FailureInjectionReport(run_id="r1", scenario_name="s1")
        s = r.summary()
        assert "run_id" in s
        assert "scenario_name" in s
        assert "sections" in s
        assert "paper_only" in s
        assert "research_only" in s

    def test_summary_sections_count(self):
        r = FailureInjectionReport()
        r.add_section("X", {})
        r.add_section("Y", {})
        assert r.summary()["sections"] == 2

    def test_as_dict_has_sections_detail(self):
        r = FailureInjectionReport()
        r.add_section("X", {"key": "val"})
        d = r.as_dict()
        assert "sections_detail" in d
        assert len(d["sections_detail"]) == 1


# ---------------------------------------------------------------------------
# ReportStore
# ---------------------------------------------------------------------------

class TestReportStore:
    def test_empty_store(self):
        store = ReportStore()
        assert store.count() == 0

    def test_store_report(self):
        store = ReportStore()
        r = FailureInjectionReport(run_id="r1")
        store.store(r)
        assert store.count() == 1

    def test_all_returns_all(self):
        store = ReportStore()
        store.store(FailureInjectionReport(run_id="r1"))
        store.store(FailureInjectionReport(run_id="r2"))
        assert len(store.all()) == 2

    def test_all_returns_copy(self):
        store = ReportStore()
        store.store(FailureInjectionReport(run_id="r1"))
        a1 = store.all()
        a1.clear()
        assert store.count() == 1  # original unaffected
