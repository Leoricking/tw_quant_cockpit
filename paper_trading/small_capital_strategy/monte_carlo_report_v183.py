"""
paper_trading/small_capital_strategy/monte_carlo_report_v183.py
Report builder for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

REPORT_SECTIONS = [
    "version", "safety", "monte_carlo_engine", "bootstrap_sampling",
    "risk_of_ruin", "drawdown_distribution", "return_distribution",
    "sequence_risk", "tail_risk", "slippage_cost_shock",
    "robustness_probability", "summary",
]


def build_monte_carlo_report(dashboard):
    """Build full Monte Carlo report from dashboard."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import MonteCarloReport
    sections = [
        {"section": "version", "version": "1.8.3", "paper_only": True, "monte_carlo_only": True},
        {"section": "safety", "all_safe": True, "paper_only": True, "monte_carlo_only": True},
        {"section": "monte_carlo_engine", "trial_count": dashboard.trial_count, "paper_only": True},
        {"section": "bootstrap_sampling", "sample_count": dashboard.trial_count, "paper_only": True},
        {"section": "risk_of_ruin", "ruin_probability_pct": dashboard.ruin_probability_pct, "paper_only": True},
        {"section": "drawdown_distribution", "worst_5pct": dashboard.worst_5pct_max_drawdown_pct, "paper_only": True},
        {"section": "return_distribution", "median_return_pct": dashboard.median_return_pct, "paper_only": True},
        {"section": "sequence_risk", "sequence_risk_score": dashboard.sequence_risk_score, "paper_only": True},
        {"section": "tail_risk", "tail_risk_score": dashboard.tail_risk_score, "paper_only": True},
        {"section": "slippage_cost_shock", "cost_sensitivity_score": dashboard.cost_sensitivity_score, "paper_only": True},
        {"section": "robustness_probability", "robustness_probability_pct": dashboard.robustness_probability_pct, "paper_only": True},
        {"section": "summary", "final_grade": dashboard.final_grade, "all_audits_pass": dashboard.final_grade not in ("BLOCKED", "RUIN_RISK"), "paper_only": True},
    ]
    return MonteCarloReport(
        sections=sections,
        all_audits_pass=dashboard.final_grade not in ("BLOCKED", "RUIN_RISK"),
    )


def build_dashboard_from_result(mc_result):
    """Build MonteCarloDashboard from MonteCarloResult."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import MonteCarloDashboard
    return MonteCarloDashboard(
        trial_count=mc_result.trial_count,
        survival_rate_pct=mc_result.survival_rate_pct,
        ruin_probability_pct=mc_result.ruin_probability_pct,
        median_return_pct=mc_result.median_return_pct,
        average_return_pct=mc_result.average_return_pct,
        worst_5pct_return_pct=mc_result.worst_5pct_return_pct,
        best_5pct_return_pct=mc_result.best_5pct_return_pct,
        median_max_drawdown_pct=mc_result.median_max_drawdown_pct,
        average_max_drawdown_pct=mc_result.average_max_drawdown_pct,
        worst_5pct_max_drawdown_pct=mc_result.worst_5pct_max_drawdown_pct,
        risk_of_ruin_score=mc_result.risk_of_ruin_score,
        sequence_risk_score=mc_result.sequence_risk_score,
        tail_risk_score=mc_result.tail_risk_score,
        robustness_probability_pct=mc_result.robustness_probability_pct,
        cost_sensitivity_score=mc_result.cost_sensitivity_score,
        slippage_sensitivity_score=mc_result.slippage_sensitivity_score,
        final_grade=mc_result.final_grade,
    )


def get_report_info() -> dict:
    """Return report metadata dict."""
    return {
        "version": "1.8.3",
        "sections": REPORT_SECTIONS,
        "count": len(REPORT_SECTIONS),
        "paper_only": True,
        "monte_carlo_only": True,
        "schema_version": "183",
    }
