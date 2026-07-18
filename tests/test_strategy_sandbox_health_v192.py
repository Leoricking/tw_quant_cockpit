"""tests/test_strategy_sandbox_health_v192.py
Tests for strategy sandbox health check v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_health_v192 import (
    StrategySandboxHealthCheck, run_health_check,
)
from paper_trading.small_capital_strategy.strategy_sandbox_models_v192 import (
    SandboxHealthSummary,
)


# ── run_health_check ──────────────────────────────────────────────────────────

def test_run_health_check_returns_sandbox_health_summary():
    result = run_health_check()
    assert isinstance(result, SandboxHealthSummary)

def test_run_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"

def test_run_health_check_failed_zero():
    result = run_health_check()
    assert result.failed == 0

def test_run_health_check_passed_ge_60():
    result = run_health_check()
    assert result.passed >= 60

def test_run_health_check_total_ge_60():
    result = run_health_check()
    assert result.total >= 60

def test_run_health_check_all_passed_true():
    result = run_health_check()
    assert result.all_passed is True

def test_run_health_check_paper_only():
    result = run_health_check()
    assert result.paper_only is True

def test_run_health_check_sandbox_only():
    result = run_health_check()
    assert result.sandbox_only is True

def test_run_health_check_shadow_only():
    result = run_health_check()
    assert result.shadow_only is True

def test_run_health_check_no_real_orders():
    result = run_health_check()
    assert result.no_real_orders is True

def test_run_health_check_schema_192():
    result = run_health_check()
    assert result.schema_version == "192"

def test_run_health_check_checks_is_list():
    result = run_health_check()
    assert isinstance(result.checks, list)

def test_run_health_check_checks_not_empty():
    result = run_health_check()
    assert len(result.checks) > 0

def test_all_checks_have_name_key():
    result = run_health_check()
    assert all("name" in c for c in result.checks)

def test_all_checks_have_passed_key():
    result = run_health_check()
    assert all("passed" in c for c in result.checks)

def test_all_checks_passed_true():
    result = run_health_check()
    assert all(c["passed"] is True for c in result.checks)

def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total

def test_run_health_check_not_investment_advice():
    result = run_health_check()
    assert result.not_investment_advice is True

def test_run_health_check_production_trading_blocked():
    result = run_health_check()
    assert result.production_trading_blocked is True

def test_run_health_check_no_broker():
    result = run_health_check()
    assert result.no_broker is True


# ── StrategySandboxHealthCheck class ─────────────────────────────────────────

def test_strategy_sandbox_health_check_instantiation():
    checker = StrategySandboxHealthCheck()
    assert checker is not None

def test_strategy_sandbox_health_check_run_method():
    checker = StrategySandboxHealthCheck()
    result = checker.run()
    assert isinstance(result, SandboxHealthSummary)

def test_strategy_sandbox_health_check_run_all_passed():
    checker = StrategySandboxHealthCheck()
    result = checker.run()
    assert result.all_passed is True

def test_strategy_sandbox_health_check_run_status_pass():
    checker = StrategySandboxHealthCheck()
    result = checker.run()
    assert result.status == "PASS"
