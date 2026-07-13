"""
tests/test_decision_cockpit_health_v186.py
Tests for decision_cockpit_health_v186 module.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_cockpit_health_v186 import (
    DecisionCockpitHealthCheck, run_health_check,
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

def test_health_check_decision_only():
    assert run_health_check().decision_only is True

def test_health_check_no_real_orders():
    assert run_health_check().no_real_orders is True

def test_health_check_schema_version():
    assert run_health_check().schema_version == "186"

def test_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total

def test_health_check_class_instantiable():
    hc = DecisionCockpitHealthCheck()
    assert hc is not None

def test_health_check_class_run():
    hc = DecisionCockpitHealthCheck()
    result = hc.run()
    assert result.all_passed is True

def test_health_check_checks_list():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    assert isinstance(hc._checks, list)

def test_health_check_checks_nonempty():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    assert len(hc._checks) > 0

def test_health_check_no_failed_checks():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    failed = [c for c in hc._checks if not c["passed"]]
    assert failed == [], f"Failed checks: {[c['name'] for c in failed]}"

def test_health_check_version_check_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    v_check = next((c for c in hc._checks if c["name"] == "version_is_186"), None)
    assert v_check is not None
    assert v_check["passed"] is True

def test_health_check_safety_check_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    s_check = next((c for c in hc._checks if c["name"] == "safety_all_safe"), None)
    assert s_check is not None
    assert s_check["passed"] is True

def test_health_check_model_count_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    m_check = next((c for c in hc._checks if c["name"] == "model_count_22"), None)
    assert m_check is not None
    assert m_check["passed"] is True

def test_health_check_engine_actions_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    e_check = next((c for c in hc._checks if c["name"] == "engine_allowed_actions_17"), None)
    assert e_check is not None
    assert e_check["passed"] is True

def test_health_check_gui_panel_version_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    g_check = next((c for c in hc._checks if c["name"] == "gui_panel_version_186"), None)
    assert g_check is not None
    assert g_check["passed"] is True

def test_health_check_scenarios_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    s_check = next((c for c in hc._checks if c["name"] == "scenarios_ge_75"), None)
    assert s_check is not None
    assert s_check["passed"] is True

def test_health_check_fixtures_passes():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    f_check = next((c for c in hc._checks if c["name"] == "fixtures_ge_75"), None)
    assert f_check is not None
    assert f_check["passed"] is True

def test_health_check_forbidden_buy():
    hc = DecisionCockpitHealthCheck()
    hc.run()
    b_check = next((c for c in hc._checks if c["name"] == "forbidden_BUY"), None)
    assert b_check is not None
    assert b_check["passed"] is True
