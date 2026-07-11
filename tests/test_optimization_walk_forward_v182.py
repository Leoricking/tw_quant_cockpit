"""
tests/test_optimization_walk_forward_v182.py
Tests for walk-forward validation engine v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_walk_forward_v182 import (
    WALK_FORWARD_TYPES, run_walk_forward, run_all_walk_forward_types,
    get_walk_forward_info,
)
from paper_trading.small_capital_strategy.optimization_models_v182 import (
    ParameterSet, WalkForwardConfig, WalkForwardResult,
)


# --- WALK_FORWARD_TYPES ---
def test_wf_types_count_10():
    assert len(WALK_FORWARD_TYPES) == 10

def test_wf_types_is_list():
    assert isinstance(WALK_FORWARD_TYPES, list)

def test_wf_types_rolling():
    assert "ROLLING" in WALK_FORWARD_TYPES

def test_wf_types_expanding():
    assert "EXPANDING" in WALK_FORWARD_TYPES

def test_wf_types_regime_based():
    assert "REGIME_BASED" in WALK_FORWARD_TYPES

def test_wf_types_theme_cycle():
    assert "THEME_CYCLE" in WALK_FORWARD_TYPES

def test_wf_types_bullish():
    assert "BULLISH" in WALK_FORWARD_TYPES

def test_wf_types_range():
    assert "RANGE" in WALK_FORWARD_TYPES

def test_wf_types_bearish():
    assert "BEARISH" in WALK_FORWARD_TYPES

def test_wf_types_risk_off():
    assert "RISK_OFF" in WALK_FORWARD_TYPES

def test_wf_types_param_stability():
    assert "PARAMETER_STABILITY" in WALK_FORWARD_TYPES

def test_wf_types_overfitting_check():
    assert "OVERFITTING_CHECK" in WALK_FORWARD_TYPES

def test_wf_types_all_strings():
    assert all(isinstance(t, str) for t in WALK_FORWARD_TYPES)


# --- run_walk_forward ---
def test_run_wf_returns_result():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert isinstance(result, WalkForwardResult)

def test_run_wf_total_windows():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig(num_windows=5)
    result = run_walk_forward(ps, config)
    assert result.total_windows == 5

def test_run_wf_windows_list():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert isinstance(result.windows, list)
    assert len(result.windows) == 5

def test_run_wf_pass_rate_range():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert 0 <= result.pass_rate_pct <= 100.0

def test_run_wf_paper_only():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert result.paper_only is True

def test_run_wf_validation_only():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert result.validation_only is True

def test_run_wf_no_real_orders():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert result.no_real_orders is True

def test_run_wf_type_matches_config():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig(walk_forward_type="EXPANDING")
    result = run_walk_forward(ps, config)
    assert result.walk_forward_type == "EXPANDING"

def test_run_wf_passed_plus_failed_eq_total():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert result.passed_windows + result.failed_windows == result.total_windows

def test_run_wf_degradation_ge_0():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    assert result.degradation_pct >= 0.0

def test_run_wf_window_ids():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    for w in result.windows:
        assert w.window_id.startswith("WFW-")

def test_run_wf_window_paper_only():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig()
    result = run_walk_forward(ps, config)
    for w in result.windows:
        assert w.paper_only is True


# --- run_all_walk_forward_types ---
def test_all_wf_returns_dict():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    assert isinstance(results, dict)

def test_all_wf_10_keys():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    assert len(results) == 10

def test_all_wf_contains_rolling():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    assert "ROLLING" in results

def test_all_wf_contains_expanding():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    assert "EXPANDING" in results

def test_all_wf_contains_regime_based():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    assert "REGIME_BASED" in results

def test_all_wf_contains_all_types():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    for wf_type in WALK_FORWARD_TYPES:
        assert wf_type in results

def test_all_wf_values_are_results():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    results = run_all_walk_forward_types(ps)
    for v in results.values():
        assert isinstance(v, WalkForwardResult)


# --- get_walk_forward_info ---
def test_wf_info_returns_dict():
    assert isinstance(get_walk_forward_info(), dict)

def test_wf_info_version():
    assert get_walk_forward_info()["version"] == "1.8.2"

def test_wf_info_count_10():
    assert get_walk_forward_info()["count"] == 10

def test_wf_info_paper_only():
    assert get_walk_forward_info()["paper_only"] is True

def test_wf_info_validation_only():
    assert get_walk_forward_info()["validation_only"] is True

def test_wf_info_schema_version():
    assert get_walk_forward_info()["schema_version"] == "182"

def test_wf_info_types_list():
    info = get_walk_forward_info()
    assert isinstance(info["walk_forward_types"], list)
    assert len(info["walk_forward_types"]) == 10


# --- Parametrized type tests ---
@pytest.mark.parametrize("wf_type", WALK_FORWARD_TYPES)
def test_run_wf_each_type(wf_type):
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    config = WalkForwardConfig(walk_forward_type=wf_type)
    result = run_walk_forward(ps, config)
    assert result.walk_forward_type == wf_type
    assert result.total_windows == 5
