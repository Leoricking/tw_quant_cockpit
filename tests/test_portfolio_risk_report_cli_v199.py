"""
tests/test_portfolio_risk_report_cli_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — CLI Registry Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from cli.command_registry import PROVIDER_COMMANDS, CommandSpec


def _get_prr_commands():
    return [c for c in PROVIDER_COMMANDS if getattr(c, "group", None) == "portfolio_risk_report"]


def _get_prr_command_names():
    return [c.name for c in _get_prr_commands()]


def test_provider_commands_is_list():
    assert isinstance(PROVIDER_COMMANDS, list)


def test_prr_commands_count_is_18():
    assert len(_get_prr_commands()) == 18


def test_all_prr_commands_are_command_spec():
    for cmd in _get_prr_commands():
        assert isinstance(cmd, CommandSpec)


def test_portfolio_risk_report_version_in_registry():
    assert "portfolio-risk-report-version" in _get_prr_command_names()


def test_portfolio_risk_report_run_in_registry():
    assert "portfolio-risk-report-run" in _get_prr_command_names()


def test_portfolio_risk_report_capital_profile_in_registry():
    assert "portfolio-risk-report-capital-profile" in _get_prr_command_names()


def test_portfolio_risk_report_risk_budget_in_registry():
    assert "portfolio-risk-report-risk-budget" in _get_prr_command_names()


def test_portfolio_risk_report_position_size_in_registry():
    assert "portfolio-risk-report-position-size" in _get_prr_command_names()


def test_portfolio_risk_report_entry_rule_in_registry():
    assert "portfolio-risk-report-entry-rule" in _get_prr_command_names()


def test_portfolio_risk_report_stop_distance_in_registry():
    assert "portfolio-risk-report-stop-distance" in _get_prr_command_names()


def test_portfolio_risk_report_cash_buffer_in_registry():
    assert "portfolio-risk-report-cash-buffer" in _get_prr_command_names()


def test_portfolio_risk_report_exposure_limits_in_registry():
    assert "portfolio-risk-report-exposure-limits" in _get_prr_command_names()


def test_portfolio_risk_report_no_entry_in_registry():
    assert "portfolio-risk-report-no-entry" in _get_prr_command_names()


def test_portfolio_risk_report_risk_off_in_registry():
    assert "portfolio-risk-report-risk-off" in _get_prr_command_names()


def test_portfolio_risk_report_dashboard_in_registry():
    assert "portfolio-risk-report-dashboard" in _get_prr_command_names()


def test_portfolio_risk_report_export_in_registry():
    assert "portfolio-risk-report-export" in _get_prr_command_names()


def test_portfolio_risk_report_health_in_registry():
    assert "portfolio-risk-report-health" in _get_prr_command_names()


def test_portfolio_risk_report_gate_in_registry():
    assert "portfolio-risk-report-gate" in _get_prr_command_names()


def test_portfolio_risk_report_scenarios_in_registry():
    assert "portfolio-risk-report-scenarios" in _get_prr_command_names()


def test_portfolio_risk_report_fixtures_in_registry():
    assert "portfolio-risk-report-fixtures" in _get_prr_command_names()


def test_portfolio_risk_report_safety_audit_in_registry():
    assert "portfolio-risk-report-safety-audit" in _get_prr_command_names()


def test_all_prr_commands_have_group_portfolio_risk_report():
    for cmd in _get_prr_commands():
        assert cmd.group == "portfolio_risk_report"


def test_all_prr_commands_introduced_in_1_9_9():
    for cmd in _get_prr_commands():
        assert cmd.introduced_in == "1.9.9", f"{cmd.name} introduced_in is not 1.9.9"


def test_all_prr_commands_safety_classification_RESEARCH_ONLY():
    for cmd in _get_prr_commands():
        assert cmd.safety_classification == "RESEARCH_ONLY", f"{cmd.name} classification wrong"


def test_no_duplicate_command_names_in_provider_commands():
    all_names = [c.name for c in PROVIDER_COMMANDS]
    assert len(all_names) == len(set(all_names))


def test_prr_command_names_all_strings():
    for name in _get_prr_command_names():
        assert isinstance(name, str)
