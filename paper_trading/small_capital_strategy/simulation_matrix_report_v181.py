"""
paper_trading/small_capital_strategy/simulation_matrix_report_v181.py
Report generation for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA  = "181"
_POLICY  = "1.8.1-simulation-scenario-matrix-stress-test"
_DISCLAIMER = "Research Only | Paper Only | Simulate Only | No Real Orders | Not Investment Advice"

REPORT_SECTIONS = [
    "version", "safety", "matrix_summary", "stress_test_summary",
    "robustness_score", "regime_performance", "theme_performance",
    "abc_performance", "mistake_impact", "equity_curve",
    "drawdown_report", "final_grade",
]


def build_matrix_report(
    matrix_result: Any,
    stress_results: Optional[List[Any]] = None,
    robustness: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Build a complete scenario matrix report dict with all sections.
    [!] Paper Only. Research Only. Simulate Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_version_v181 import get_version_info
    version_info = get_version_info()

    stress_results = stress_results or []
    stress_survived = sum(1 for r in stress_results if getattr(r, "survived", False))
    stress_count = len(stress_results)

    stress_summary: List[Dict[str, Any]] = []
    for sr in stress_results:
        stress_summary.append({
            "scenario_id": getattr(sr, "scenario_id", ""),
            "shock_type": getattr(sr, "shock_type", ""),
            "survived": getattr(sr, "survived", False),
            "total_return_pct": getattr(sr, "total_return_pct", 0.0),
            "max_drawdown_pct": getattr(sr, "max_drawdown_pct", 0.0),
            "action": getattr(sr, "action", "BLOCKED"),
            "notes": getattr(sr, "notes", ""),
        })

    # Robustness section
    robustness_section: Dict[str, Any] = {}
    if robustness is not None:
        robustness_section = {
            "score": getattr(robustness, "score", 0.0),
            "stress_survival_rate_pct": getattr(robustness, "stress_survival_rate_pct", 0.0),
            "scenario_pass_rate_pct": getattr(robustness, "scenario_pass_rate_pct", 0.0),
            "average_max_drawdown_pct": getattr(robustness, "average_max_drawdown_pct", 0.0),
            "worst_case_return_pct": getattr(robustness, "worst_case_return_pct", 0.0),
            "behavior_resilience_score": getattr(robustness, "behavior_resilience_score", 0.0),
            "final_grade": getattr(robustness, "final_grade", "FRAGILE"),
        }

    # Regime performance: group cells by market_regime
    regime_counts: Dict[str, Dict[str, Any]] = {}
    theme_counts: Dict[str, Dict[str, Any]] = {}
    abc_counts: Dict[str, Dict[str, Any]] = {}
    mistake_counts: Dict[str, Dict[str, Any]] = {}

    cells = getattr(matrix_result, "cells", [])
    for cell in cells:
        inp = getattr(cell, "input_params", {})
        regime = inp.get("market_regime", "UNKNOWN")
        theme = inp.get("theme_rank", "UNKNOWN")
        abc = inp.get("abc_signal", "UNKNOWN")
        mistake = inp.get("mistake_injection", "NONE")

        for key, counts, extra_key, extra_val in [
            (regime, regime_counts, "avg_return_pct", cell.total_return_pct),
            (theme, theme_counts, "avg_return_pct", cell.total_return_pct),
            (abc, abc_counts, "avg_expectancy_r", cell.expectancy_r),
            (mistake, mistake_counts, "avg_drawdown_pct", cell.max_drawdown_pct),
        ]:
            if key not in counts:
                counts[key] = {"count": 0, "blocked": 0, "values": []}
            counts[key]["count"] += 1
            if cell.is_blocked:
                counts[key]["blocked"] += 1
            counts[key]["values"].append(extra_val)

    def _avg(lst: List[float]) -> float:
        return round(sum(lst) / len(lst), 4) if lst else 0.0

    regime_perf = [
        {"regime": k, "scenario_count": v["count"], "blocked_count": v["blocked"],
         "avg_return_pct": _avg(v["values"])}
        for k, v in regime_counts.items()
    ]
    theme_perf = [
        {"theme": k, "scenario_count": v["count"], "blocked_count": v["blocked"],
         "avg_return_pct": _avg(v["values"])}
        for k, v in theme_counts.items()
    ]
    abc_perf = [
        {"abc_signal": k, "scenario_count": v["count"], "blocked_count": v["blocked"],
         "avg_expectancy_r": _avg(v["values"])}
        for k, v in abc_counts.items()
    ]
    mistake_impact = [
        {"mistake_type": k, "scenario_count": v["count"], "blocked_count": v["blocked"],
         "avg_drawdown_pct": _avg(v["values"])}
        for k, v in mistake_counts.items()
    ]

    # Simple equity curve approximation from cells
    eq_values = [getattr(matrix_result, "average_return_pct", 0.0)]
    eq_drawdowns = [getattr(matrix_result, "average_max_drawdown_pct", 0.0)]

    final_grade = getattr(matrix_result, "final_grade", "FRAGILE")

    return {
        "report_type": "simulation_matrix_report",
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "disclaimer": _DISCLAIMER,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "stress_test_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        # ── version ──────────────────────────────────────────────────────────
        "version": {
            "version": version_info.get("version", "1.8.1"),
            "release_name": version_info.get("release_name", ""),
            "base_release": version_info.get("base_release", ""),
            "schema_version": _SCHEMA,
            "policy_version": _POLICY,
        },
        # ── safety ───────────────────────────────────────────────────────────
        "safety": {
            "paper_only": True,
            "research_only": True,
            "simulate_only": True,
            "stress_test_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
        },
        # ── matrix_summary ───────────────────────────────────────────────────
        "matrix_summary": {
            "scenario_count": getattr(matrix_result, "scenario_count", 0),
            "pass_count": getattr(matrix_result, "pass_count", 0),
            "blocked_count": getattr(matrix_result, "blocked_count", 0),
            "average_return_pct": getattr(matrix_result, "average_return_pct", 0.0),
            "median_return_pct": getattr(matrix_result, "median_return_pct", 0.0),
            "worst_case_return_pct": getattr(matrix_result, "worst_case_return_pct", 0.0),
            "best_case_return_pct": getattr(matrix_result, "best_case_return_pct", 0.0),
            "average_max_drawdown_pct": getattr(matrix_result, "average_max_drawdown_pct", 0.0),
            "worst_max_drawdown_pct": getattr(matrix_result, "worst_max_drawdown_pct", 0.0),
            "average_win_rate_pct": getattr(matrix_result, "average_win_rate_pct", 0.0),
            "average_profit_factor": getattr(matrix_result, "average_profit_factor", 0.0),
            "average_expectancy_r": getattr(matrix_result, "average_expectancy_r", 0.0),
            "risk_of_ruin_score": getattr(matrix_result, "risk_of_ruin_score", 0.0),
            "robustness_score": getattr(matrix_result, "robustness_score", 0.0),
            "stress_survival_rate_pct": getattr(matrix_result, "stress_survival_rate_pct", 0.0),
            "blocked_reason_distribution": getattr(matrix_result, "blocked_reason_distribution", {}),
        },
        # ── stress_test_summary ──────────────────────────────────────────────
        "stress_test_summary": {
            "stress_test_count": stress_count,
            "stress_survived": stress_survived,
            "survival_rate_pct": round(stress_survived / stress_count * 100.0, 2) if stress_count > 0 else 0.0,
            "results": stress_summary,
        },
        # ── robustness_score ─────────────────────────────────────────────────
        "robustness_score": robustness_section,
        # ── regime_performance ───────────────────────────────────────────────
        "regime_performance": regime_perf,
        # ── theme_performance ────────────────────────────────────────────────
        "theme_performance": theme_perf,
        # ── abc_performance ──────────────────────────────────────────────────
        "abc_performance": abc_perf,
        # ── mistake_impact ───────────────────────────────────────────────────
        "mistake_impact": mistake_impact,
        # ── equity_curve ─────────────────────────────────────────────────────
        "equity_curve": {
            "point_count": len(eq_values),
            "first_value": eq_values[0] if eq_values else 0.0,
            "last_value": eq_values[-1] if eq_values else 0.0,
            "max_drawdown_pct": max(eq_drawdowns) if eq_drawdowns else 0.0,
        },
        # ── drawdown_report ──────────────────────────────────────────────────
        "drawdown_report": {
            "max_drawdown_pct": getattr(matrix_result, "worst_max_drawdown_pct", 0.0),
            "average_drawdown_pct": getattr(matrix_result, "average_max_drawdown_pct", 0.0),
        },
        # ── final_grade ──────────────────────────────────────────────────────
        "final_grade": final_grade,
        "sections": REPORT_SECTIONS,
    }


def build_dashboard_report(
    total_scenarios: int = 0,
    pass_count: int = 0,
    blocked_count: int = 0,
    stress_survived: int = 0,
    robustness_score: float = 0.0,
    final_grade: str = "FRAGILE",
) -> Dict[str, Any]:
    """
    Build a concise Scenario Matrix Dashboard report dict.
    [!] Paper Only. Research Only. Simulate Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import ScenarioMatrixDashboard
    dashboard = ScenarioMatrixDashboard(
        version="1.8.1",
        total_scenarios=total_scenarios,
        pass_count=pass_count,
        blocked_count=blocked_count,
        stress_tests_run=0,
        stress_survived=stress_survived,
        robustness_score=robustness_score,
        final_grade=final_grade,
        schema_version=_SCHEMA,
        paper_only=True,
        research_only=True,
        simulate_only=True,
        stress_test_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )
    return {
        "report_type": "simulation_matrix_dashboard",
        "version": dashboard.version,
        "total_scenarios": dashboard.total_scenarios,
        "pass_count": dashboard.pass_count,
        "blocked_count": dashboard.blocked_count,
        "stress_survived": dashboard.stress_survived,
        "robustness_score": dashboard.robustness_score,
        "final_grade": dashboard.final_grade,
        "disclaimer": _DISCLAIMER,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "stress_test_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "sections": REPORT_SECTIONS,
    }


def get_report_section_names() -> List[str]:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "schema": _SCHEMA,
        "policy": _POLICY,
        "disclaimer": _DISCLAIMER,
        "sections": REPORT_SECTIONS,
        "section_count": len(REPORT_SECTIONS),
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "stress_test_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


if __name__ == "__main__":
    info = get_report_info()
    print(f"[v1.8.1] Report sections: {info['section_count']}")
    assert info["section_count"] >= 10, f"Expected >=10 sections, got {info['section_count']}"
    print("[OK] simulation_matrix_report_v181 ready")
