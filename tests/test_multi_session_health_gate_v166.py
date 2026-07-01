"""
test_multi_session_health_gate_v166.py — Health Check, Release Gate, and GUI Panel tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestMultiSessionCoordinationHealthCheck:
    def test_run_returns_dict(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert isinstance(result, dict)

    def test_run_has_total_key(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert "total" in result

    def test_run_has_passed_key(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert "passed" in result

    def test_run_has_failed_key(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert "failed" in result

    def test_run_has_status_key(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert "status" in result

    def test_run_has_checks_key(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert "checks" in result

    def test_total_gte_60(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert result["total"] >= 60

    def test_failed_is_zero(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert result["failed"] == 0

    def test_status_is_pass(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert result["status"] == "PASS"

    def test_passed_equals_total(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert result["passed"] == result["total"]

    def test_checks_is_dict(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert isinstance(result["checks"], dict)

    def test_checks_non_empty(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert len(result["checks"]) > 0

    def test_check_version_is_166(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert CHECK_VERSION == "1.6.6"

    def test_all_checks_pass(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        checks = result["checks"]
        # Each check value is a (status, message) tuple
        failing = [k for k, v in checks.items() if v[0] != "PASS"]
        assert failing == []

    def test_version_in_result(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert "version" in result

    def test_version_value_is_166(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert result["version"] == "1.6.6"

    def test_total_is_int(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert isinstance(result["total"], int)

    def test_failed_is_int(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        hc = MultiSessionCoordinationHealthCheck()
        result = hc.run()
        assert isinstance(result["failed"], int)


class TestMultiSessionCoordinationReleaseGate:
    def test_run_returns_dict(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert isinstance(result, dict)

    def test_run_total_is_50(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert result["total"] == 50

    def test_run_passed_is_50(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert result["passed"] == 50

    def test_run_failed_is_zero(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert result["failed"] == 0

    def test_run_status_is_pass(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert result["status"] == "PASS"

    def test_gate_checks_key_present(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert "gate_checks" in result

    def test_gate_checks_all_true(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        gate_checks = result["gate_checks"]
        failing = [k for k, v in gate_checks.items() if v is not True]
        assert failing == []

    def test_failures_is_empty_list(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert result["failures"] == []

    def test_gate_version_is_166(self):
        from release.multi_session_coordination_release_gate_v166 import GATE_VERSION
        assert GATE_VERSION == "1.6.6"

    def test_gate_version_in_result(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert result.get("version") == "1.6.6"

    def test_gate_checks_is_dict(self):
        from release.multi_session_coordination_release_gate_v166 import MultiSessionCoordinationReleaseGate
        g = MultiSessionCoordinationReleaseGate()
        result = g.run()
        assert isinstance(result["gate_checks"], dict)


class TestGUIPanelBasic:
    def test_panel_tabs_count_is_26(self):
        from gui.multi_session_coordination_panel import PANEL_TABS
        assert len(PANEL_TABS) == 26

    def test_panel_version_is_166(self):
        from gui.multi_session_coordination_panel import PANEL_VERSION
        assert PANEL_VERSION == "1.6.6"

    def test_panel_tabs_is_list(self):
        from gui.multi_session_coordination_panel import PANEL_TABS
        assert isinstance(PANEL_TABS, list)

    def test_panel_instantiation(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel
        p = MultiSessionCoordinationPanel()
        assert p is not None

    def test_render_tab_returns_dict(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel, PANEL_TABS
        p = MultiSessionCoordinationPanel()
        result = p.render_tab(PANEL_TABS[0])
        assert isinstance(result, dict)

    def test_render_all_returns_dict(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel
        p = MultiSessionCoordinationPanel()
        result = p.render_all()
        assert isinstance(result, dict)

    def test_render_all_has_tabs_key(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel
        p = MultiSessionCoordinationPanel()
        result = p.render_all()
        assert "tabs" in result

    def test_render_text_summary_returns_string(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel
        p = MultiSessionCoordinationPanel()
        result = p.render_text_summary()
        assert isinstance(result, str)

    def test_panel_tabs_has_overview(self):
        from gui.multi_session_coordination_panel import PANEL_TABS
        assert "overview" in PANEL_TABS

    def test_panel_tabs_has_sessions(self):
        from gui.multi_session_coordination_panel import PANEL_TABS
        assert "sessions" in PANEL_TABS

    def test_panel_tabs_has_lifecycle(self):
        from gui.multi_session_coordination_panel import PANEL_TABS
        assert "lifecycle" in PANEL_TABS

    def test_render_tab_each_valid(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel, PANEL_TABS
        p = MultiSessionCoordinationPanel()
        for tab in PANEL_TABS:
            result = p.render_tab(tab)
            assert isinstance(result, dict), f"render_tab({tab!r}) did not return dict"
