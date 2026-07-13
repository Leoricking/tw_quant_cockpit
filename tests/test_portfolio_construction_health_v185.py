"""
tests/test_portfolio_construction_health_v185.py
Tests for portfolio_construction_health_v185 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_construction_health_v185 import (
    PortfolioConstructionHealthCheck, run_health_check,
)


def test_run_health_check_callable():
    result = run_health_check()
    assert result is not None

def test_health_check_all_passed():
    result = run_health_check()
    assert result.all_passed is True

def test_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"

def test_health_check_failed_zero():
    result = run_health_check()
    assert result.failed == 0

def test_health_check_total_ge_60():
    result = run_health_check()
    assert result.total >= 60

def test_health_check_paper_only():
    assert run_health_check().paper_only is True

def test_health_check_no_real_orders():
    assert run_health_check().no_real_orders is True

def test_health_check_schema_version():
    assert run_health_check().schema_version == "185"

def test_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total

def test_health_check_class_instantiable():
    hc = PortfolioConstructionHealthCheck()
    assert hc is not None

def test_health_check_class_run():
    hc = PortfolioConstructionHealthCheck()
    result = hc.run()
    assert result.all_passed is True

def test_health_check_checks_list():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    assert isinstance(hc._checks, list)

def test_health_check_checks_nonempty():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    assert len(hc._checks) >= 60

def test_health_check_all_checks_have_name():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    assert all("name" in c for c in hc._checks)

def test_health_check_all_checks_have_passed():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    assert all("passed" in c for c in hc._checks)

def test_health_check_version_check_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    version_checks = [c for c in hc._checks if "version" in c["name"]]
    assert all(c["passed"] for c in version_checks)

def test_health_check_safety_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    safety_checks = [c for c in hc._checks if "safety" in c["name"]]
    assert all(c["passed"] for c in safety_checks)

def test_health_check_model_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    model_checks = [c for c in hc._checks if "model_" in c["name"]]
    assert all(c["passed"] for c in model_checks)

def test_health_check_engine_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    engine_checks = [c for c in hc._checks if "engine_" in c["name"]]
    assert all(c["passed"] for c in engine_checks)

def test_health_check_scenario_check_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    scenario_checks = [c for c in hc._checks if "scenario" in c["name"]]
    assert all(c["passed"] for c in scenario_checks)

def test_health_check_fixture_check_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    fixture_checks = [c for c in hc._checks if "fixture" in c["name"]]
    assert all(c["passed"] for c in fixture_checks)

def test_health_check_compat_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    compat_checks = [c for c in hc._checks if "compat_" in c["name"]]
    assert all(c["passed"] for c in compat_checks)

def test_health_check_block_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    block_checks = [c for c in hc._checks if "block_" in c["name"]]
    assert all(c["passed"] for c in block_checks)

def test_health_check_forbidden_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    forbidden_checks = [c for c in hc._checks if "forbidden_" in c["name"]]
    assert all(c["passed"] for c in forbidden_checks)

def test_health_check_cli_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    cli_checks = [c for c in hc._checks if "cli_" in c["name"]]
    assert all(c["passed"] for c in cli_checks)

def test_health_check_gui_checks_pass():
    hc = PortfolioConstructionHealthCheck()
    hc.run()
    gui_checks = [c for c in hc._checks if "gui_" in c["name"]]
    assert all(c["passed"] for c in gui_checks)
