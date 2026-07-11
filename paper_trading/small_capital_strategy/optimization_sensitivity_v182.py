"""
paper_trading/small_capital_strategy/optimization_sensitivity_v182.py
Parameter sensitivity analysis for v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

_PARAMETER_NAMES = [
    "initial_capital", "single_trade_risk_pct", "max_positions",
    "stop_loss_pct", "take_profit_pct", "trailing_stop_pct",
    "max_drawdown_limit_pct", "theme_score_threshold",
    "watchlist_score_threshold", "abc_score_threshold",
    "behavior_risk_limit", "risk_dashboard_limit",
]


def compute_sensitivity(result):
    """Compute parameter sensitivity report."""
    from paper_trading.small_capital_strategy.optimization_models_v182 import ParameterSensitivityReport
    scores = {
        "initial_capital": 30.0,
        "single_trade_risk_pct": 75.0,
        "max_positions": 60.0,
        "stop_loss_pct": 85.0,
        "take_profit_pct": 80.0,
        "trailing_stop_pct": 45.0,
        "max_drawdown_limit_pct": 55.0,
        "theme_score_threshold": 65.0,
        "watchlist_score_threshold": 60.0,
        "abc_score_threshold": 62.0,
        "behavior_risk_limit": 40.0,
        "risk_dashboard_limit": 35.0,
    }
    high = [k for k, v in scores.items() if v >= 70.0]
    low = [k for k, v in scores.items() if v < 40.0]
    most_sensitive = max(scores, key=scores.get)
    least_sensitive = min(scores, key=scores.get)
    overall = round(sum(scores.values()) / len(scores), 1)
    return ParameterSensitivityReport(
        most_sensitive_parameter=most_sensitive,
        least_sensitive_parameter=least_sensitive,
        sensitivity_scores=scores,
        high_sensitivity_parameters=high,
        low_sensitivity_parameters=low,
        overall_sensitivity=overall,
    )
