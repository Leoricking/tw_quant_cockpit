"""
tests/test_risk_dashboard_cli_v174.py
Tests for CLI command registration of risk dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, CommandSpec


_RISK_DASHBOARD_NAMES = [
    "risk-dashboard-version",
    "risk-dashboard-summary",
    "risk-dashboard-single-trade",
    "risk-dashboard-exposure",
    "risk-dashboard-cash",
    "risk-dashboard-drawdown",
    "risk-dashboard-losing-streak",
    "risk-dashboard-concentration",
    "risk-dashboard-theme-exposure",
    "risk-dashboard-position-count",
    "risk-dashboard-stop-loss",
    "risk-dashboard-budget-usage",
    "risk-dashboard-scorecard",
    "risk-dashboard-report",
    "risk-dashboard-fixtures",
    "risk-dashboard-scenarios",
    "risk-dashboard-health",
    "risk-dashboard-gate",
    "risk-dashboard-safety-audit",
]

_all_names = [c.name for c in PROVIDER_COMMANDS]


class TestCommandRegistration:
    def test_total_commands_ge_700(self):
        assert len(PROVIDER_COMMANDS) >= 700

    def test_19_risk_dashboard_commands_registered(self):
        rd_cmds = [c for c in PROVIDER_COMMANDS if c.name in set(_RISK_DASHBOARD_NAMES)]
        assert len(rd_cmds) == 19

    def test_risk_dashboard_version_present(self):
        assert "risk-dashboard-version" in _all_names

    def test_risk_dashboard_summary_present(self):
        assert "risk-dashboard-summary" in _all_names

    def test_risk_dashboard_single_trade_present(self):
        assert "risk-dashboard-single-trade" in _all_names

    def test_risk_dashboard_exposure_present(self):
        assert "risk-dashboard-exposure" in _all_names

    def test_risk_dashboard_cash_present(self):
        assert "risk-dashboard-cash" in _all_names

    def test_risk_dashboard_drawdown_present(self):
        assert "risk-dashboard-drawdown" in _all_names

    def test_risk_dashboard_losing_streak_present(self):
        assert "risk-dashboard-losing-streak" in _all_names

    def test_risk_dashboard_concentration_present(self):
        assert "risk-dashboard-concentration" in _all_names

    def test_risk_dashboard_health_present(self):
        assert "risk-dashboard-health" in _all_names

    def test_risk_dashboard_gate_present(self):
        assert "risk-dashboard-gate" in _all_names

    def test_risk_dashboard_safety_audit_present(self):
        assert "risk-dashboard-safety-audit" in _all_names

    def test_risk_dashboard_scorecard_present(self):
        assert "risk-dashboard-scorecard" in _all_names

    def test_risk_dashboard_report_present(self):
        assert "risk-dashboard-report" in _all_names

    def test_risk_dashboard_fixtures_present(self):
        assert "risk-dashboard-fixtures" in _all_names

    def test_risk_dashboard_scenarios_present(self):
        assert "risk-dashboard-scenarios" in _all_names


class TestCommandSpec:
    def _get(self, name):
        for c in PROVIDER_COMMANDS:
            if c.name == name:
                return c
        return None

    def test_version_introduced_174(self):
        c = self._get("risk-dashboard-version")
        assert c is not None
        assert c.introduced_in == "1.7.4"

    def test_all_research_only(self):
        for name in _RISK_DASHBOARD_NAMES:
            c = self._get(name)
            assert c is not None, f"Command {name} not found"
            assert c.safety_classification == "RESEARCH_ONLY"

    def test_all_in_small_capital_group(self):
        for name in _RISK_DASHBOARD_NAMES:
            c = self._get(name)
            assert c is not None, f"Command {name} not found"
            assert c.group == "small_capital_strategy"

    def test_all_have_handler_names(self):
        for name in _RISK_DASHBOARD_NAMES:
            c = self._get(name)
            assert c is not None
            assert c.handler_name.startswith("cmd_risk_dashboard_")

    def test_all_commands_have_help(self):
        for name in _RISK_DASHBOARD_NAMES:
            c = self._get(name)
            assert c is not None
            assert len(c.help) > 0
