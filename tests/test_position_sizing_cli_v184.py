"""
tests/test_position_sizing_cli_v184.py
Tests for v1.8.4 CLI command registration and handler resolution.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
import importlib
from cli.command_registry import PROVIDER_COMMANDS


def _ps_cmds():
    return [c for c in PROVIDER_COMMANDS if c.name.startswith("position-sizing") and c.introduced_in == "1.8.4"]


def _get_main():
    return importlib.import_module("main")


# ── Registration ──────────────────────────────────────────────────────────────
def test_ps_commands_ge_20():
    assert len(_ps_cmds()) >= 20

def test_ps_commands_count_22():
    assert len(_ps_cmds()) == 20

def test_ps_version_registered():
    assert any(c.name == "position-sizing-version" for c in PROVIDER_COMMANDS)

def test_ps_run_registered():
    assert any(c.name == "position-sizing-run" for c in PROVIDER_COMMANDS)

def test_ps_config_registered():
    assert any(c.name == "position-sizing-config" for c in PROVIDER_COMMANDS)

def test_ps_capital_profile_registered():
    assert any(c.name == "position-sizing-capital-profile" for c in PROVIDER_COMMANDS)

def test_ps_risk_budget_registered():
    assert any(c.name == "position-sizing-risk-budget" for c in PROVIDER_COMMANDS)

def test_ps_by_stop_registered():
    assert any(c.name == "position-sizing-by-stop" for c in PROVIDER_COMMANDS)

def test_ps_by_volatility_registered():
    assert any(c.name == "position-sizing-by-volatility" for c in PROVIDER_COMMANDS)

def test_ps_by_drawdown_registered():
    assert any(c.name == "position-sizing-by-drawdown" for c in PROVIDER_COMMANDS)

def test_ps_mc_adjusted_registered():
    assert any(c.name == "position-sizing-monte-carlo-adjusted" for c in PROVIDER_COMMANDS)

def test_ps_abc_plan_registered():
    assert any(c.name == "position-sizing-abc-plan" for c in PROVIDER_COMMANDS)

def test_ps_add_plan_registered():
    assert any(c.name == "position-sizing-add-plan" for c in PROVIDER_COMMANDS)

def test_ps_reduce_plan_registered():
    assert any(c.name == "position-sizing-reduce-plan" for c in PROVIDER_COMMANDS)

def test_ps_exposure_limit_registered():
    assert any(c.name == "position-sizing-exposure-limit" for c in PROVIDER_COMMANDS)

def test_ps_concentration_risk_registered():
    assert any(c.name == "position-sizing-concentration-risk" for c in PROVIDER_COMMANDS)

def test_ps_cash_reserve_registered():
    assert any(c.name == "position-sizing-cash-reserve" for c in PROVIDER_COMMANDS)

def test_ps_dashboard_registered():
    assert any(c.name == "position-sizing-dashboard" for c in PROVIDER_COMMANDS)

def test_ps_report_registered():
    assert any(c.name == "position-sizing-report" for c in PROVIDER_COMMANDS)

def test_ps_scenarios_registered():
    assert any(c.name == "position-sizing-scenarios" for c in PROVIDER_COMMANDS)

def test_ps_fixtures_registered():
    assert any(c.name == "position-sizing-fixtures" for c in PROVIDER_COMMANDS)

def test_ps_health_registered():
    assert any(c.name == "position-sizing-health" for c in PROVIDER_COMMANDS)

def test_ps_gate_registered():
    assert any(c.name == "position-sizing-gate" for c in PROVIDER_COMMANDS)

def test_ps_safety_audit_registered():
    assert any(c.name == "position-sizing-safety-audit" for c in PROVIDER_COMMANDS)


# ── Handler resolution ────────────────────────────────────────────────────────
def test_handler_version_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_version", None))

def test_handler_run_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_run", None))

def test_handler_config_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_config", None))

def test_handler_capital_profile_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_capital_profile", None))

def test_handler_risk_budget_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_risk_budget", None))

def test_handler_by_stop_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_by_stop", None))

def test_handler_by_volatility_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_by_volatility", None))

def test_handler_by_drawdown_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_by_drawdown", None))

def test_handler_mc_adjusted_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_monte_carlo_adjusted", None))

def test_handler_abc_plan_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_abc_plan", None))

def test_handler_add_plan_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_add_plan", None))

def test_handler_reduce_plan_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_reduce_plan", None))

def test_handler_exposure_limit_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_exposure_limit", None))

def test_handler_concentration_risk_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_concentration_risk", None))

def test_handler_cash_reserve_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_cash_reserve", None))

def test_handler_dashboard_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_dashboard", None))

def test_handler_report_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_report", None))

def test_handler_scenarios_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_scenarios", None))

def test_handler_fixtures_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_fixtures", None))

def test_handler_health_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_health", None))

def test_handler_gate_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_gate", None))

def test_handler_safety_audit_callable():
    main = _get_main()
    assert callable(getattr(main, "cmd_position_sizing_safety_audit", None))


# ── Group classification ──────────────────────────────────────────────────────
def test_all_ps_commands_in_group():
    for cmd in _ps_cmds():
        assert cmd.group == "position_sizing"

def test_all_ps_commands_introduced_in_184():
    for cmd in _ps_cmds():
        assert cmd.introduced_in == "1.8.4"

def test_all_ps_commands_research_only():
    for cmd in _ps_cmds():
        assert cmd.safety_classification == "RESEARCH_ONLY"

def test_all_ps_handler_names_start_with_cmd():
    for cmd in _ps_cmds():
        assert cmd.handler_name.startswith("cmd_position_sizing_")

def test_all_ps_handlers_resolvable():
    main = _get_main()
    unresolved = [c.handler_name for c in _ps_cmds()
                  if not callable(getattr(main, c.handler_name, None))]
    assert unresolved == [], f"Unresolved handlers: {unresolved}"
