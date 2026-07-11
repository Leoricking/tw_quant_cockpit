"""
tests/test_optimization_sensitivity_v182.py
Tests for parameter sensitivity analysis v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_sensitivity_v182 import (
    compute_sensitivity, _PARAMETER_NAMES,
)
from paper_trading.small_capital_strategy.optimization_models_v182 import (
    ParameterSearchResult, ParameterSensitivityReport,
)


# --- _PARAMETER_NAMES ---
def test_parameter_names_count_12():
    assert len(_PARAMETER_NAMES) == 12

def test_parameter_names_is_list():
    assert isinstance(_PARAMETER_NAMES, list)

def test_parameter_names_initial_capital():
    assert "initial_capital" in _PARAMETER_NAMES

def test_parameter_names_stop_loss():
    assert "stop_loss_pct" in _PARAMETER_NAMES

def test_parameter_names_take_profit():
    assert "take_profit_pct" in _PARAMETER_NAMES

def test_parameter_names_risk_pct():
    assert "single_trade_risk_pct" in _PARAMETER_NAMES

def test_parameter_names_all_strings():
    assert all(isinstance(n, str) for n in _PARAMETER_NAMES)


# --- compute_sensitivity ---
def test_sensitivity_returns_model():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert isinstance(report, ParameterSensitivityReport)

def test_sensitivity_scores_12_keys():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert len(report.sensitivity_scores) == 12

def test_sensitivity_most_sensitive_stop_loss():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert report.most_sensitive_parameter == "stop_loss_pct"

def test_sensitivity_least_sensitive_initial_capital():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert report.least_sensitive_parameter == "initial_capital"

def test_sensitivity_high_list():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert isinstance(report.high_sensitivity_parameters, list)
    assert len(report.high_sensitivity_parameters) > 0

def test_sensitivity_low_list():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert isinstance(report.low_sensitivity_parameters, list)
    assert len(report.low_sensitivity_parameters) > 0

def test_sensitivity_overall_gt_0():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert report.overall_sensitivity > 0

def test_sensitivity_paper_only():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert report.paper_only is True

def test_sensitivity_validation_only():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert report.validation_only is True

def test_sensitivity_schema_version():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert report.schema_version == "182"

def test_sensitivity_stop_loss_high():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert "stop_loss_pct" in report.high_sensitivity_parameters

def test_sensitivity_take_profit_high():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert "take_profit_pct" in report.high_sensitivity_parameters

def test_sensitivity_risk_pct_high():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert "single_trade_risk_pct" in report.high_sensitivity_parameters

def test_sensitivity_initial_capital_low():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert "initial_capital" in report.low_sensitivity_parameters

def test_sensitivity_scores_all_positive():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    for v in report.sensitivity_scores.values():
        assert v > 0

def test_sensitivity_scores_keys_match_params():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    for name in _PARAMETER_NAMES:
        assert name in report.sensitivity_scores

def test_sensitivity_overall_range():
    result = ParameterSearchResult()
    report = compute_sensitivity(result)
    assert 0 <= report.overall_sensitivity <= 100.0
