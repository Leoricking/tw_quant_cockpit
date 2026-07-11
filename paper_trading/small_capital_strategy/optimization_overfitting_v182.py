"""
paper_trading/small_capital_strategy/optimization_overfitting_v182.py
Overfitting risk detection for v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


def compute_overfitting_risk(ps) -> float:
    """Compute overfitting risk score 0-100. Higher = more overfitted."""
    if ps.in_sample_return_pct <= 0:
        return 80.0
    ratio = ps.out_of_sample_return_pct / ps.in_sample_return_pct if ps.in_sample_return_pct > 0 else 0.0
    degradation = max(0.0, 1.0 - ratio)
    return round(min(100.0, degradation * 100.0 * 1.5), 1)


def build_overfitting_risk_report(ps):
    """Build overfitting risk report for a parameter set."""
    from paper_trading.small_capital_strategy.optimization_models_v182 import OverfittingRiskReport
    score = compute_overfitting_risk(ps)
    detected = score >= 70.0
    if score >= 85.0:
        level = "CRITICAL"
    elif score >= 70.0:
        level = "HIGH"
    elif score >= 50.0:
        level = "MEDIUM"
    else:
        level = "LOW"
    degradation = round(max(0.0, ps.in_sample_return_pct - ps.out_of_sample_return_pct), 2)
    recommendations = []
    if detected:
        recommendations.append("Reduce parameter count")
    if score >= 50.0:
        recommendations.append("Use walk-forward validation")
    if degradation > 5.0:
        recommendations.append("Check regime dependency")
    return OverfittingRiskReport(
        overfitting_risk_score=score,
        in_sample_return_pct=ps.in_sample_return_pct,
        out_of_sample_return_pct=ps.out_of_sample_return_pct,
        degradation_pct=degradation,
        parameter_count_used=12,
        overfitting_detected=detected,
        overfitting_risk_level=level,
        recommendations=recommendations,
    )
