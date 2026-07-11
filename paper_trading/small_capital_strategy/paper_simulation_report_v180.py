"""
paper_trading/small_capital_strategy/paper_simulation_report_v180.py
Report generation for Paper Simulation & Performance Lab v1.8.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA  = "180"
_POLICY  = "1.8.0-paper-simulation-performance-lab"
_DISCLAIMER = "Research Only | Paper Only | No Real Orders | Not Investment Advice"

REPORT_SECTIONS = [
    "version",
    "safety",
    "simulation_summary",
    "performance_metrics",
    "equity_curve",
    "drawdown_report",
    "risk_report",
    "regime_performance",
    "theme_performance",
    "abc_performance",
    "mistake_impact",
]


def build_simulation_report(
    result: Any,
    metrics: Any,
    equity_curve: Any,
    drawdown_report: Any,
    risk_report: Any,
    regime_performance: Optional[List[Any]] = None,
    theme_performance: Optional[List[Any]] = None,
    abc_performance: Optional[List[Any]] = None,
    mistake_impact: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """
    Build a complete paper simulation report dict.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_version_v180 import get_version_info
    version_info = get_version_info()

    regime_perf_list = []
    if regime_performance:
        for rp in regime_performance:
            regime_perf_list.append({
                "regime": rp.regime,
                "trade_count": rp.trade_count,
                "win_rate_pct": rp.win_rate_pct,
                "avg_return_pct": rp.avg_return_pct,
            })

    theme_perf_list = []
    if theme_performance:
        for tp in theme_performance:
            theme_perf_list.append({
                "theme": tp.theme,
                "trade_count": tp.trade_count,
                "win_rate_pct": tp.win_rate_pct,
                "avg_return_pct": tp.avg_return_pct,
            })

    abc_perf_list = []
    if abc_performance:
        for ap in abc_performance:
            abc_perf_list.append({
                "abc_type": ap.abc_type,
                "trade_count": ap.trade_count,
                "win_rate_pct": ap.win_rate_pct,
                "avg_return_pct": ap.avg_return_pct,
                "avg_r": ap.avg_r,
            })

    mistake_list = []
    if mistake_impact:
        for mi in mistake_impact:
            mistake_list.append({
                "mistake_type": mi.mistake_type,
                "trade_count": mi.trade_count,
                "avg_loss_pct": mi.avg_loss_pct,
                "behavior_penalty": mi.behavior_penalty,
            })

    return {
        "report_type": "paper_simulation_report",
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "disclaimer": _DISCLAIMER,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "version_info": {
            "version": version_info["version"],
            "release_name": version_info["release_name"],
        },
        "simulation_summary": {
            "scenario_id": result.scenario_id,
            "trade_count": result.trade_count,
            "final_capital": result.final_capital,
            "total_return_pct": result.total_return_pct,
        },
        "performance_metrics": {
            "total_return_pct": metrics.total_return_pct,
            "annualized_return_pct": metrics.annualized_return_pct,
            "max_drawdown_pct": metrics.max_drawdown_pct,
            "win_rate_pct": metrics.win_rate_pct,
            "average_win_pct": metrics.average_win_pct,
            "average_loss_pct": metrics.average_loss_pct,
            "profit_factor": metrics.profit_factor,
            "expectancy_r": metrics.expectancy_r,
            "average_r": metrics.average_r,
            "max_consecutive_losses": metrics.max_consecutive_losses,
            "max_consecutive_wins": metrics.max_consecutive_wins,
            "trade_count": metrics.trade_count,
            "exposure_pct": metrics.exposure_pct,
            "cash_drag_pct": metrics.cash_drag_pct,
            "turnover": metrics.turnover,
            "risk_of_ruin_score": metrics.risk_of_ruin_score,
            "behavior_penalty_score": metrics.behavior_penalty_score,
            "final_grade": metrics.final_grade,
        },
        "equity_curve": {
            "point_count": len(equity_curve.values),
            "first_value": equity_curve.values[0] if equity_curve.values else None,
            "last_value": equity_curve.values[-1] if equity_curve.values else None,
            "max_drawdown_pct": max(equity_curve.drawdowns) if equity_curve.drawdowns else 0.0,
        },
        "drawdown_report": {
            "max_drawdown_pct": drawdown_report.max_drawdown_pct,
            "max_drawdown_duration_days": drawdown_report.max_drawdown_duration_days,
            "recovery_days": drawdown_report.recovery_days,
            "period_count": len(drawdown_report.drawdown_periods),
        },
        "risk_report": {
            "risk_per_trade_pct": risk_report.risk_per_trade_pct,
            "max_holdings": risk_report.max_holdings,
            "current_exposure_pct": risk_report.current_exposure_pct,
            "risk_budget_used_pct": risk_report.risk_budget_used_pct,
            "stop_loss_coverage": risk_report.stop_loss_coverage,
            "risk_status": risk_report.risk_status,
        },
        "regime_performance": regime_perf_list,
        "theme_performance": theme_perf_list,
        "abc_performance": abc_perf_list,
        "mistake_impact": mistake_list,
        "sections": REPORT_SECTIONS,
    }


def build_dashboard_report(
    scenario_count: int = 0,
    total_trades: int = 0,
    final_grade: str = "B",
    metrics: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Build a Paper Simulation Dashboard report dict.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperSimulationDashboard
    dashboard = PaperSimulationDashboard(
        version="1.8.0",
        scenario_count=scenario_count,
        total_trades=total_trades,
        final_grade=final_grade,
        metrics=metrics,
        schema_version=_SCHEMA,
    )
    return {
        "report_type": "paper_simulation_dashboard",
        "version": dashboard.version,
        "scenario_count": dashboard.scenario_count,
        "total_trades": dashboard.total_trades,
        "final_grade": dashboard.final_grade,
        "disclaimer": _DISCLAIMER,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


def get_report_section_names() -> List[str]:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "schema": _SCHEMA,
        "policy": _POLICY,
        "sections": REPORT_SECTIONS,
        "section_count": len(REPORT_SECTIONS),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


if __name__ == "__main__":
    print(f"[v1.8.0] Report sections: {len(REPORT_SECTIONS)}")
    print("[OK] paper_simulation_report_v180 ready")
