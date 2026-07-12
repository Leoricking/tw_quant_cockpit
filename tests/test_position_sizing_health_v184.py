"""
tests/test_position_sizing_health_v184.py
Tests for position_sizing_health_v184 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.position_sizing_health_v184 import (
    run_health_check, PositionSizingHealthCheck,
)


def test_run_health_check_callable():
    result = run_health_check()
    assert result is not None

def test_health_all_passed():
    assert run_health_check().all_passed is True

def test_health_status_pass():
    assert run_health_check().status == "PASS"

def test_health_failed_zero():
    assert run_health_check().failed == 0

def test_health_total_ge_60():
    assert run_health_check().total >= 60

def test_health_paper_only():
    assert run_health_check().paper_only is True

def test_health_no_real_orders():
    assert run_health_check().no_real_orders is True

def test_health_passed_ge_60():
    assert run_health_check().passed >= 60

def test_health_check_class_run():
    hc = PositionSizingHealthCheck()
    result = hc.run()
    assert result.all_passed is True

def test_health_check_class_checks_not_empty():
    hc = PositionSizingHealthCheck()
    hc.run()
    assert len(hc._checks) > 0

def test_health_check_no_failed_checks():
    hc = PositionSizingHealthCheck()
    hc.run()
    failed = [c for c in hc._checks if not c["passed"]]
    assert len(failed) == 0, f"Failed health checks: {[c['name'] for c in failed]}"

def test_health_check_version_check_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    v_checks = [c for c in hc._checks if c["name"] == "version_is_184"]
    assert len(v_checks) == 1
    assert v_checks[0]["passed"] is True

def test_health_check_safety_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    s_checks = [c for c in hc._checks if c["name"] == "safety_all_safe"]
    assert len(s_checks) == 1
    assert s_checks[0]["passed"] is True

def test_health_check_model_count_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    m_checks = [c for c in hc._checks if c["name"] == "model_count_19"]
    assert len(m_checks) == 1
    assert m_checks[0]["passed"] is True

def test_health_check_engine_actions_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    checks = [c for c in hc._checks if c["name"] == "engine_allowed_actions_15"]
    assert len(checks) == 1
    assert checks[0]["passed"] is True

def test_health_check_scenarios_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    checks = [c for c in hc._checks if c["name"] == "scenarios_ge_75"]
    assert len(checks) == 1
    assert checks[0]["passed"] is True

def test_health_check_cli_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    checks = [c for c in hc._checks if c["name"] == "cli_ps_cmds_ge_20"]
    assert len(checks) == 1
    assert checks[0]["passed"] is True

def test_health_check_gui_version_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    checks = [c for c in hc._checks if c["name"] == "gui_panel_version_184"]
    assert len(checks) == 1
    assert checks[0]["passed"] is True

def test_health_check_blocked_no_stop_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    checks = [c for c in hc._checks if c["name"] == "block_no_stop_loss"]
    assert len(checks) == 1
    assert checks[0]["passed"] is True

def test_health_check_compat_v183_passes():
    hc = PositionSizingHealthCheck()
    hc.run()
    checks = [c for c in hc._checks if c["name"] == "compat_v183"]
    assert len(checks) == 1
    assert checks[0]["passed"] is True
