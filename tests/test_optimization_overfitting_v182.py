"""
tests/test_optimization_overfitting_v182.py
Tests for overfitting risk detection v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_overfitting_v182 import (
    compute_overfitting_risk, build_overfitting_risk_report,
)
from paper_trading.small_capital_strategy.optimization_models_v182 import (
    ParameterSet, OverfittingRiskReport,
)


# --- compute_overfitting_risk ---
def test_overfitting_risk_returns_float():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    assert isinstance(compute_overfitting_risk(ps), float)

def test_overfitting_risk_range():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    score = compute_overfitting_risk(ps)
    assert 0 <= score <= 100.0

def test_overfitting_risk_high_degradation():
    ps = ParameterSet(in_sample_return_pct=20.0, out_of_sample_return_pct=2.0)
    score = compute_overfitting_risk(ps)
    assert score >= 70.0

def test_overfitting_risk_low_degradation():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=9.0)
    score = compute_overfitting_risk(ps)
    assert score < 50.0

def test_overfitting_risk_zero_in_sample():
    ps = ParameterSet(in_sample_return_pct=0.0, out_of_sample_return_pct=0.0)
    score = compute_overfitting_risk(ps)
    assert score == 80.0

def test_overfitting_risk_negative_in_sample():
    ps = ParameterSet(in_sample_return_pct=-5.0, out_of_sample_return_pct=-3.0)
    score = compute_overfitting_risk(ps)
    assert score == 80.0

def test_overfitting_risk_equal_returns():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=10.0)
    score = compute_overfitting_risk(ps)
    assert score == 0.0

def test_overfitting_risk_max_100():
    ps = ParameterSet(in_sample_return_pct=100.0, out_of_sample_return_pct=0.0)
    score = compute_overfitting_risk(ps)
    assert score <= 100.0


# --- build_overfitting_risk_report ---
def test_report_returns_model():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert isinstance(report, OverfittingRiskReport)

def test_report_paper_only():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.paper_only is True

def test_report_validation_only():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.validation_only is True

def test_report_schema_version():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.schema_version == "182"

def test_report_risk_level_low():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=9.0)
    report = build_overfitting_risk_report(ps)
    assert report.overfitting_risk_level == "LOW"

def test_report_risk_level_high():
    ps = ParameterSet(in_sample_return_pct=20.0, out_of_sample_return_pct=2.0)
    report = build_overfitting_risk_report(ps)
    assert report.overfitting_risk_level in ("HIGH", "CRITICAL")

def test_report_detected_when_high():
    ps = ParameterSet(in_sample_return_pct=20.0, out_of_sample_return_pct=2.0)
    report = build_overfitting_risk_report(ps)
    assert report.overfitting_detected is True

def test_report_not_detected_when_low():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=9.0)
    report = build_overfitting_risk_report(ps)
    assert report.overfitting_detected is False

def test_report_recommendations_list():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert isinstance(report.recommendations, list)

def test_report_recommendations_when_high():
    ps = ParameterSet(in_sample_return_pct=20.0, out_of_sample_return_pct=2.0)
    report = build_overfitting_risk_report(ps)
    assert len(report.recommendations) > 0

def test_report_parameter_count_12():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.parameter_count_used == 12

def test_report_degradation_ge_0():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.degradation_pct >= 0.0

def test_report_in_sample_matches():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.in_sample_return_pct == 10.0

def test_report_out_sample_matches():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.out_of_sample_return_pct == 7.0

def test_report_risk_level_valid():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    report = build_overfitting_risk_report(ps)
    assert report.overfitting_risk_level in ("LOW", "MEDIUM", "HIGH", "CRITICAL")

def test_report_score_matches_compute():
    ps = ParameterSet(in_sample_return_pct=10.0, out_of_sample_return_pct=7.0)
    score = compute_overfitting_risk(ps)
    report = build_overfitting_risk_report(ps)
    assert report.overfitting_risk_score == score
