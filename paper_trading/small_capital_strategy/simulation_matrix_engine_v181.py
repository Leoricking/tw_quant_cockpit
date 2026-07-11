"""
paper_trading/small_capital_strategy/simulation_matrix_engine_v181.py
Scenario Matrix Engine for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
Deterministic. Research-only. No real orders.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA = "181"

ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED",
    "PAPER_ADD_ALLOWED", "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED",
    "NO_TRADE", "RESEARCH_ONLY", "READ_REPORT", "SIMULATE_ONLY",
    "STRESS_TEST_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_FINAL_GRADES = frozenset({"ROBUST", "ACCEPTABLE", "FRAGILE", "DANGEROUS", "BLOCKED"})

# Block conditions for matrix cells
_BLOCK_REGIMES    = frozenset({"RISK_OFF"})
_BLOCK_THEMES     = frozenset({"EXCLUDED"})
_BLOCK_WATCHLISTS = frozenset({"EXCLUDED"})
_BLOCK_ABC        = frozenset({"BLOCKED"})
_BLOCK_BEHAVIOR   = frozenset({"BLOCKED"})
_BLOCK_RISK_DASH  = frozenset({"BLOCKED"})
_BLOCK_MISTAKES   = frozenset({"NO_STOP_LOSS"})


def _cell_action(inp: "SimulationMatrixInput") -> str:
    """Determine action for a single matrix cell input."""
    # Hard blocks
    if inp.market_regime in _BLOCK_REGIMES:        return "BLOCKED"
    if inp.theme_rank in _BLOCK_THEMES:            return "BLOCKED"
    if inp.watchlist_rank in _BLOCK_WATCHLISTS:    return "BLOCKED"
    if inp.abc_signal in _BLOCK_ABC:               return "BLOCKED"
    if inp.behavior_risk in _BLOCK_BEHAVIOR:       return "BLOCKED"
    if inp.risk_dashboard in _BLOCK_RISK_DASH:     return "BLOCKED"
    if inp.mistake_injection in _BLOCK_MISTAKES:   return "BLOCKED"

    # Downgrade conditions
    if inp.mistake_injection in ("OVERSIZED_POSITION", "OVERTRADING", "MOVED_STOP_LOSS"):
        return "REDUCE_RISK"
    if inp.mistake_injection == "REVENGE_TRADE":   return "REVIEW_REQUIRED"
    if inp.behavior_risk == "WARNING":             return "REVIEW_REQUIRED"
    if inp.risk_dashboard == "WARNING":            return "REVIEW_REQUIRED"
    if inp.behavior_risk == "WATCH":               return "WAIT"
    if inp.abc_signal == "NOT_READY":              return "WAIT"
    if inp.theme_rank in ("WEAK", "WATCH"):        return "WAIT"
    if inp.watchlist_rank in ("TRAINING",):        return "WAIT"

    # Regime conditions
    if inp.market_regime in ("BEAR", "UNKNOWN"):   return "OBSERVE"

    # Entry allowed
    if (inp.abc_signal in ("A", "B", "C")
            and inp.market_regime == "BULL"
            and inp.theme_rank in ("LEADER", "STRONG")
            and inp.watchlist_rank in ("CORE", "MAIN_THEME_SWING")):
        return "PAPER_ENTRY_ALLOWED"

    if inp.market_regime == "RANGE" and inp.abc_signal in ("A", "B", "C"):
        return "PAPER_PLAN_READY"

    return "WAIT"


def _simulate_cell_metrics(
    inp: "SimulationMatrixInput",
    action: str,
) -> Dict[str, float]:
    """Deterministically compute metrics for one matrix cell."""
    if action == "BLOCKED":
        return {"total_return_pct": 0.0, "max_drawdown_pct": 0.0,
                "win_rate_pct": 0.0, "expectancy_r": -1.0, "final_grade": "BLOCKED"}
    if action in ("OBSERVE", "WAIT", "NO_TRADE"):
        return {"total_return_pct": 0.0, "max_drawdown_pct": 0.0,
                "win_rate_pct": 0.0, "expectancy_r": 0.0, "final_grade": "FRAGILE"}
    if action == "REDUCE_RISK":
        risk_mult = 0.5
    elif action == "REVIEW_REQUIRED":
        risk_mult = 0.7
    elif action == "PAPER_PLAN_READY":
        risk_mult = 0.8
    elif action == "PAPER_ENTRY_ALLOWED":
        risk_mult = 1.0
    else:
        risk_mult = 0.6

    r = inp.single_trade_risk_pct * risk_mult
    # Regime-based win rate
    regime_wr = {"BULL": 0.62, "RANGE": 0.50, "BEAR": 0.35,
                 "RISK_OFF": 0.0, "UNKNOWN": 0.40}.get(inp.market_regime, 0.45)
    # Theme adjustment
    theme_adj = {"LEADER": 0.05, "STRONG": 0.02, "WATCH": -0.05,
                 "WEAK": -0.10, "EXCLUDED": -0.30}.get(inp.theme_rank, 0.0)
    win_rate = max(0.0, min(1.0, regime_wr + theme_adj))

    avg_win_r = 2.0 * r
    avg_loss_r = r
    expectancy_r = win_rate * avg_win_r - (1 - win_rate) * avg_loss_r

    # Simple equity simulation (20 trades)
    capital = inp.initial_capital
    trade_count = 20
    wins = int(trade_count * win_rate)
    losses = trade_count - wins
    risk_amount = capital * r / 100.0
    total_pnl = wins * risk_amount * 2.0 - losses * risk_amount
    total_return_pct = total_pnl / capital * 100.0

    # Max drawdown approximation
    max_dd = max(0.0, losses * r * 1.5 - wins * r * 0.5)
    max_dd = min(max_dd, 60.0)

    # Final grade
    if expectancy_r >= 1.2 and win_rate >= 0.55 and max_dd <= 15:
        grade = "ROBUST"
    elif expectancy_r >= 0.6 and win_rate >= 0.45 and max_dd <= 25:
        grade = "ACCEPTABLE"
    elif expectancy_r >= 0.0 and max_dd <= 40:
        grade = "FRAGILE"
    elif expectancy_r >= -0.5:
        grade = "DANGEROUS"
    else:
        grade = "BLOCKED"

    return {
        "total_return_pct": round(total_return_pct, 4),
        "max_drawdown_pct": round(max_dd, 4),
        "win_rate_pct": round(win_rate * 100.0, 2),
        "expectancy_r": round(expectancy_r, 4),
        "final_grade": grade,
    }


def run_matrix_cell(inp: "SimulationMatrixInput") -> "SimulationMatrixCell":
    """
    Run a single scenario matrix cell.
    [!] Paper Only. Research Only. Simulate Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import (
        SimulationMatrixInput, SimulationMatrixCell,
    )
    assert inp.paper_only is True
    assert inp.no_real_orders is True

    action = _cell_action(inp)
    assert action in ALLOWED_OUTPUT_ACTIONS
    for w in FORBIDDEN_OUTPUT_WORDS:
        assert w not in action

    metrics = _simulate_cell_metrics(inp, action)
    cell_id = (f"CELL181-{inp.market_regime[:2]}-{inp.theme_rank[:2]}-"
               f"{inp.watchlist_rank[:2]}-{inp.abc_signal}-{inp.mistake_injection[:3]}")

    return SimulationMatrixCell(
        cell_id=cell_id,
        input_params={
            "initial_capital": inp.initial_capital,
            "single_trade_risk_pct": inp.single_trade_risk_pct,
            "max_positions": inp.max_positions,
            "market_regime": inp.market_regime,
            "theme_rank": inp.theme_rank,
            "watchlist_rank": inp.watchlist_rank,
            "abc_signal": inp.abc_signal,
            "behavior_risk": inp.behavior_risk,
            "risk_dashboard": inp.risk_dashboard,
            "mistake_injection": inp.mistake_injection,
        },
        action=action,
        is_blocked=(action == "BLOCKED"),
        total_return_pct=metrics["total_return_pct"],
        max_drawdown_pct=metrics["max_drawdown_pct"],
        win_rate_pct=metrics["win_rate_pct"],
        expectancy_r=metrics["expectancy_r"],
        final_grade=metrics["final_grade"],
        schema_version=_SCHEMA,
        paper_only=True,
        research_only=True,
        simulate_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def run_scenario_matrix(scenarios: List["SimulationMatrixInput"]) -> "SimulationMatrixResult":
    """
    Run all matrix cells for a list of inputs; return aggregated SimulationMatrixResult.
    [!] Paper Only. Research Only. Simulate Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import SimulationMatrixResult
    cells = [run_matrix_cell(inp) for inp in scenarios]

    pass_cells = [c for c in cells if not c.is_blocked]
    blocked_cells = [c for c in cells if c.is_blocked]
    returns = [c.total_return_pct for c in pass_cells] if pass_cells else [0.0]
    drawdowns = [c.max_drawdown_pct for c in pass_cells] if pass_cells else [0.0]

    def _median(lst):
        s = sorted(lst)
        n = len(s)
        return (s[n//2] + s[(n-1)//2]) / 2.0 if n else 0.0

    avg_ret = sum(returns) / len(returns)
    avg_dd = sum(drawdowns) / len(drawdowns)
    avg_wr = (sum(c.win_rate_pct for c in pass_cells) / len(pass_cells)) if pass_cells else 0.0
    avg_exp = (sum(c.expectancy_r for c in pass_cells) / len(pass_cells)) if pass_cells else 0.0

    total = len(cells)
    pass_count = len(pass_cells)
    blocked_count = len(blocked_cells)
    survival_pct = pass_count / total * 100.0 if total > 0 else 0.0

    # Robustness score
    robustness = max(0.0, min(100.0,
        survival_pct * 0.4 +
        min(avg_exp * 20.0, 30.0) +
        max(0.0, 30.0 - avg_dd)
    ))

    # Final grade
    if robustness >= 70 and survival_pct >= 60:
        grade = "ROBUST"
    elif robustness >= 50 and survival_pct >= 40:
        grade = "ACCEPTABLE"
    elif robustness >= 25:
        grade = "FRAGILE"
    elif robustness >= 10:
        grade = "DANGEROUS"
    else:
        grade = "BLOCKED"

    blocked_reasons: Dict[str, int] = {}
    for c in blocked_cells:
        r = c.input_params.get("market_regime", "UNKNOWN")
        blocked_reasons[r] = blocked_reasons.get(r, 0) + 1

    return SimulationMatrixResult(
        scenario_count=total,
        pass_count=pass_count,
        blocked_count=blocked_count,
        average_return_pct=round(avg_ret, 4),
        median_return_pct=round(_median(returns), 4),
        worst_case_return_pct=round(min(returns), 4),
        best_case_return_pct=round(max(returns), 4),
        average_max_drawdown_pct=round(avg_dd, 4),
        worst_max_drawdown_pct=round(max(drawdowns), 4),
        average_win_rate_pct=round(avg_wr, 2),
        average_profit_factor=round(max(0.0, avg_exp + 1.0), 4),
        average_expectancy_r=round(avg_exp, 4),
        risk_of_ruin_score=round(max(0.0, blocked_count / total * 100.0) if total else 0.0, 2),
        robustness_score=round(robustness, 2),
        stress_survival_rate_pct=round(survival_pct, 2),
        blocked_reason_distribution=blocked_reasons,
        final_grade=grade,
        cells=cells,
        schema_version=_SCHEMA,
        paper_only=True,
        research_only=True,
        simulate_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def compute_robustness_score(
    matrix_result: "SimulationMatrixResult",
    stress_results: Optional[List["StressTestResult"]] = None,
) -> "RobustnessScore":
    """
    Compute RobustnessScore from matrix and optional stress test results.
    [!] Paper Only. Research Only. Simulate Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import RobustnessScore
    stress_results = stress_results or []
    survived = sum(1 for s in stress_results if s.survived)
    stress_total = len(stress_results)
    stress_survival = survived / stress_total * 100.0 if stress_total > 0 else 100.0

    scenario_pass_rate = (matrix_result.pass_count / matrix_result.scenario_count * 100.0
                          if matrix_result.scenario_count > 0 else 0.0)

    behavior_resilience = max(0.0, 100.0 - matrix_result.risk_of_ruin_score)

    score = max(0.0, min(100.0,
        matrix_result.robustness_score * 0.5 +
        stress_survival * 0.3 +
        behavior_resilience * 0.2
    ))

    if score >= 70:
        grade = "ROBUST"
    elif score >= 50:
        grade = "ACCEPTABLE"
    elif score >= 25:
        grade = "FRAGILE"
    elif score >= 10:
        grade = "DANGEROUS"
    else:
        grade = "BLOCKED"

    return RobustnessScore(
        score=round(score, 2),
        stress_survival_rate_pct=round(stress_survival, 2),
        scenario_pass_rate_pct=round(scenario_pass_rate, 2),
        average_max_drawdown_pct=matrix_result.average_max_drawdown_pct,
        worst_case_return_pct=matrix_result.worst_case_return_pct,
        behavior_resilience_score=round(behavior_resilience, 2),
        final_grade=grade,
        schema_version=_SCHEMA,
    )


def get_engine_info() -> Dict[str, Any]:
    """Return matrix engine metadata."""
    return {
        "schema": _SCHEMA,
        "allowed_output_actions": sorted(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": sorted(FORBIDDEN_OUTPUT_WORDS),
        "valid_final_grades": sorted(VALID_FINAL_GRADES),
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


def validate_action(action: str) -> bool:
    """Return True if action is in ALLOWED_OUTPUT_ACTIONS and has no forbidden words."""
    if action not in ALLOWED_OUTPUT_ACTIONS:
        return False
    return not any(w in action for w in FORBIDDEN_OUTPUT_WORDS)


if __name__ == "__main__":
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import SimulationMatrixInput
    test_inp = SimulationMatrixInput()
    cell = run_matrix_cell(test_inp)
    print(f"[v1.8.1 Matrix Engine] cell={cell.cell_id} action={cell.action} grade={cell.final_grade}")
    print("[OK] simulation_matrix_engine_v181 ready")
