"""
paper_trading/small_capital_strategy/paper_simulation_metrics_v180.py
Performance metrics computation for Paper Simulation & Performance Lab v1.8.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

_SCHEMA = "180"

VALID_GRADES = frozenset({"A", "B", "C", "D", "BLOCKED"})


def _grade(
    expectancy_r: float,
    win_rate_pct: float,
    max_drawdown_pct: float,
    behavior_penalty_score: float,
    is_blocked: bool,
) -> str:
    """Compute final grade from performance metrics."""
    if is_blocked or behavior_penalty_score >= 80.0:
        return "BLOCKED"
    if expectancy_r >= 1.5 and win_rate_pct >= 55.0 and max_drawdown_pct <= 15.0:
        return "A"
    if expectancy_r >= 0.8 and win_rate_pct >= 45.0 and max_drawdown_pct <= 25.0:
        return "B"
    if expectancy_r >= 0.3 and win_rate_pct >= 38.0 and max_drawdown_pct <= 35.0:
        return "C"
    if expectancy_r >= 0.0:
        return "D"
    return "D"


def _max_consecutive(results: List[bool], target: bool) -> int:
    """Count max consecutive True or False in a bool list."""
    best = 0
    cur = 0
    for r in results:
        if r == target:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def _compute_equity_curve(
    initial_capital: float,
    pnls: List[float],
) -> List[float]:
    """Return equity curve as list of portfolio values."""
    curve = [initial_capital]
    v = initial_capital
    for p in pnls:
        v += p
        curve.append(round(v, 2))
    return curve


def _compute_max_drawdown(equity_curve: List[float]) -> float:
    """Return max drawdown percentage from equity curve."""
    if len(equity_curve) < 2:
        return 0.0
    peak = equity_curve[0]
    max_dd = 0.0
    for v in equity_curve:
        if v > peak:
            peak = v
        dd = (peak - v) / peak * 100.0 if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd
    return round(max_dd, 4)


def compute_metrics(
    trades: List[Any],
    initial_capital: float = 300000.0,
    simulation_days: int = 252,
    is_blocked: bool = False,
) -> "PaperPerformanceMetrics":
    """
    Compute PaperPerformanceMetrics from a list of PaperSimulationTrade.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperPerformanceMetrics

    if not trades:
        return PaperPerformanceMetrics(
            trade_count=0,
            final_grade="BLOCKED" if is_blocked else "D",
            schema_version=_SCHEMA,
        )

    pnls = [t.pnl for t in trades]
    pnl_pcts = [t.pnl_pct for t in trades]
    r_multiples = [t.r_multiple for t in trades]
    is_win = [t.pnl > 0 for t in trades]

    trade_count = len(trades)
    wins = [p for p, w in zip(pnl_pcts, is_win) if w]
    losses = [p for p, w in zip(pnl_pcts, is_win) if not w]
    win_rate_pct = len(wins) / trade_count * 100.0 if trade_count > 0 else 0.0
    avg_win_pct = sum(wins) / len(wins) if wins else 0.0
    avg_loss_pct = sum(losses) / len(losses) if losses else 0.0

    gross_win = sum(p for p in pnls if p > 0)
    gross_loss = abs(sum(p for p in pnls if p < 0))
    profit_factor = gross_win / gross_loss if gross_loss > 0 else (float("inf") if gross_win > 0 else 0.0)

    r_wins = [r for r, w in zip(r_multiples, is_win) if w]
    r_losses = [abs(r) for r, w in zip(r_multiples, is_win) if not w]
    avg_r = sum(r_multiples) / trade_count if trade_count > 0 else 0.0
    avg_win_r = sum(r_wins) / len(r_wins) if r_wins else 0.0
    avg_loss_r = sum(r_losses) / len(r_losses) if r_losses else 1.0
    wr = win_rate_pct / 100.0
    expectancy_r = wr * avg_win_r - (1 - wr) * avg_loss_r

    equity_curve = _compute_equity_curve(initial_capital, pnls)
    final_capital = equity_curve[-1]
    total_return_pct = (final_capital - initial_capital) / initial_capital * 100.0
    ann = ((final_capital / initial_capital) ** (252.0 / max(simulation_days, 1)) - 1) * 100.0
    max_dd = _compute_max_drawdown(equity_curve)

    max_cons_losses = _max_consecutive(is_win, False)
    max_cons_wins = _max_consecutive(is_win, True)

    # Exposure and cash drag (approximation for simulation)
    exposure_pct = min(100.0, trade_count / (simulation_days / 5.0) * 100.0)
    cash_drag_pct = max(0.0, 100.0 - exposure_pct)
    turnover = trade_count * 2 / max(simulation_days / 252.0, 0.01)

    # Behavior penalty
    mistake_counts = {}
    for t in trades:
        mt = t.mistake_type if t.mistake_type else "none"
        mistake_counts[mt] = mistake_counts.get(mt, 0) + 1
    harmful_mistakes = sum(v for k, v in mistake_counts.items()
                           if k not in ("none", "", "clean"))
    behavior_penalty_score = min(100.0, harmful_mistakes * 15.0)

    # Risk of ruin (simple heuristic)
    ror_score = max(0.0, (1 - wr) ** 10 * 100.0) if wr < 0.5 else 0.0

    final_grade = _grade(expectancy_r, win_rate_pct, max_dd, behavior_penalty_score, is_blocked)

    return PaperPerformanceMetrics(
        total_return_pct=round(total_return_pct, 4),
        annualized_return_pct=round(ann, 4),
        max_drawdown_pct=round(max_dd, 4),
        win_rate_pct=round(win_rate_pct, 2),
        average_win_pct=round(avg_win_pct, 4),
        average_loss_pct=round(avg_loss_pct, 4),
        profit_factor=round(profit_factor, 4) if profit_factor != float("inf") else 9999.0,
        expectancy_r=round(expectancy_r, 4),
        average_r=round(avg_r, 4),
        max_consecutive_losses=max_cons_losses,
        max_consecutive_wins=max_cons_wins,
        trade_count=trade_count,
        exposure_pct=round(exposure_pct, 2),
        cash_drag_pct=round(cash_drag_pct, 2),
        turnover=round(turnover, 2),
        risk_of_ruin_score=round(ror_score, 2),
        behavior_penalty_score=round(behavior_penalty_score, 2),
        final_grade=final_grade,
        schema_version=_SCHEMA,
    )


def compute_equity_curve(
    trades: List[Any],
    initial_capital: float = 300000.0,
) -> "PaperEquityCurve":
    """
    Compute PaperEquityCurve from trade list.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperEquityCurve
    pnls = [t.pnl for t in trades]
    curve = _compute_equity_curve(initial_capital, pnls)
    peak = curve[0]
    drawdowns = []
    for v in curve:
        if v > peak:
            peak = v
        dd = (peak - v) / peak * 100.0 if peak > 0 else 0.0
        drawdowns.append(round(dd, 4))
    dates = [f"D{i:03d}" for i in range(len(curve))]
    return PaperEquityCurve(
        dates=dates,
        values=curve,
        drawdowns=drawdowns,
        schema_version=_SCHEMA,
    )


def compute_drawdown_report(equity_curve: "PaperEquityCurve") -> "PaperDrawdownReport":
    """
    Compute PaperDrawdownReport from PaperEquityCurve.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperDrawdownReport
    values = equity_curve.values
    if not values:
        return PaperDrawdownReport(schema_version=_SCHEMA)

    max_dd = max(equity_curve.drawdowns) if equity_curve.drawdowns else 0.0
    # Find drawdown periods
    periods: list = []
    in_dd = False
    dd_start = 0
    peak_val = values[0]
    max_dur = 0

    for i, v in enumerate(values):
        if v > peak_val:
            if in_dd:
                dur = i - dd_start
                if dur > max_dur:
                    max_dur = dur
                periods.append({"start": dd_start, "end": i, "duration_days": dur})
                in_dd = False
            peak_val = v
        elif v < peak_val and not in_dd:
            in_dd = True
            dd_start = i

    if in_dd:
        dur = len(values) - dd_start
        if dur > max_dur:
            max_dur = dur
        periods.append({"start": dd_start, "end": len(values) - 1, "duration_days": dur})

    return PaperDrawdownReport(
        max_drawdown_pct=round(max_dd, 4),
        max_drawdown_duration_days=max_dur,
        recovery_days=0,
        drawdown_periods=periods,
        schema_version=_SCHEMA,
    )


def compute_risk_report(
    inp: Any,
    metrics: "PaperPerformanceMetrics",
) -> "PaperRiskReport":
    """
    Compute PaperRiskReport from input and metrics.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperRiskReport
    risk_status = "PASS"
    if metrics.max_drawdown_pct > 25.0:
        risk_status = "WARNING"
    if metrics.final_grade == "BLOCKED":
        risk_status = "BLOCKED"
    return PaperRiskReport(
        risk_per_trade_pct=inp.risk_per_trade_pct,
        max_holdings=inp.max_holdings,
        current_exposure_pct=metrics.exposure_pct,
        risk_budget_used_pct=min(100.0, metrics.exposure_pct * inp.risk_per_trade_pct / 100.0),
        stop_loss_coverage=inp.mistake_taxonomy_effect != "no_stop_loss",
        risk_status=risk_status,
        schema_version=_SCHEMA,
    )


def compute_regime_performance(trades: List[Any]) -> List["PaperRegimePerformance"]:
    """Compute per-regime performance breakdown."""
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperRegimePerformance
    regime_data: Dict[str, list] = {}
    for t in trades:
        r = t.regime
        if r not in regime_data:
            regime_data[r] = []
        regime_data[r].append(t)
    result = []
    for regime, rtrades in regime_data.items():
        wins = [t for t in rtrades if t.pnl > 0]
        wr = len(wins) / len(rtrades) * 100.0 if rtrades else 0.0
        avg_ret = sum(t.pnl_pct for t in rtrades) / len(rtrades) if rtrades else 0.0
        result.append(PaperRegimePerformance(
            regime=regime,
            trade_count=len(rtrades),
            win_rate_pct=round(wr, 2),
            avg_return_pct=round(avg_ret, 4),
            schema_version=_SCHEMA,
        ))
    return result


def compute_theme_performance(trades: List[Any]) -> List["PaperThemePerformance"]:
    """Compute per-theme performance breakdown."""
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperThemePerformance
    theme_data: Dict[str, list] = {}
    for t in trades:
        th = t.theme or "UNKNOWN"
        if th not in theme_data:
            theme_data[th] = []
        theme_data[th].append(t)
    result = []
    for theme, ttrades in theme_data.items():
        wins = [t for t in ttrades if t.pnl > 0]
        wr = len(wins) / len(ttrades) * 100.0 if ttrades else 0.0
        avg_ret = sum(t.pnl_pct for t in ttrades) / len(ttrades) if ttrades else 0.0
        result.append(PaperThemePerformance(
            theme=theme,
            trade_count=len(ttrades),
            win_rate_pct=round(wr, 2),
            avg_return_pct=round(avg_ret, 4),
            schema_version=_SCHEMA,
        ))
    return result


def compute_abc_performance(trades: List[Any]) -> List["PaperABCPerformance"]:
    """Compute per-ABC-type performance breakdown."""
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperABCPerformance
    abc_data: Dict[str, list] = {}
    for t in trades:
        at = t.abc_type or "A"
        if at not in abc_data:
            abc_data[at] = []
        abc_data[at].append(t)
    result = []
    for abc_type, atrades in abc_data.items():
        wins = [t for t in atrades if t.pnl > 0]
        wr = len(wins) / len(atrades) * 100.0 if atrades else 0.0
        avg_ret = sum(t.pnl_pct for t in atrades) / len(atrades) if atrades else 0.0
        avg_r = sum(t.r_multiple for t in atrades) / len(atrades) if atrades else 0.0
        result.append(PaperABCPerformance(
            abc_type=abc_type,
            trade_count=len(atrades),
            win_rate_pct=round(wr, 2),
            avg_return_pct=round(avg_ret, 4),
            avg_r=round(avg_r, 4),
            schema_version=_SCHEMA,
        ))
    return result


def compute_mistake_impact(trades: List[Any]) -> List["PaperMistakeImpactReport"]:
    """Compute per-mistake-type impact report."""
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperMistakeImpactReport
    mistake_data: Dict[str, list] = {}
    for t in trades:
        mt = t.mistake_type or "none"
        if mt not in mistake_data:
            mistake_data[mt] = []
        mistake_data[mt].append(t)
    result = []
    for mtype, mtrades in mistake_data.items():
        losses = [t for t in mtrades if t.pnl < 0]
        avg_loss = sum(t.pnl_pct for t in losses) / len(losses) if losses else 0.0
        penalty_map = {
            "no_stop_loss": 50.0, "overtrading": 30.0,
            "oversized_position": 25.0, "moved_stop_loss": 20.0,
            "revenge_trade": 35.0,
        }
        penalty = penalty_map.get(mtype, 0.0)
        result.append(PaperMistakeImpactReport(
            mistake_type=mtype,
            trade_count=len(mtrades),
            avg_loss_pct=round(avg_loss, 4),
            behavior_penalty=penalty,
            schema_version=_SCHEMA,
        ))
    return result


def get_metrics_info() -> Dict[str, Any]:
    """Return metrics module metadata."""
    return {
        "schema": _SCHEMA,
        "valid_grades": sorted(VALID_GRADES),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


if __name__ == "__main__":
    print("[OK] paper_simulation_metrics_v180 ready")
