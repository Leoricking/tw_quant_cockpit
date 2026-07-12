"""
paper_trading/small_capital_strategy/monte_carlo_risk_of_ruin_v183.py
Risk-of-Ruin calculator for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import random as _random

CAPITAL_FLOOR_OPTIONS = [50, 60, 70]
MAX_DRAWDOWN_LIMIT_OPTIONS = [10, 15, 20, 25]
LOSING_STREAK_THRESHOLD_OPTIONS = [3, 5, 8, 10]


def _compute_ror_probability(win_rate: float, avg_win: float, avg_loss: float,
                              capital_floor_pct: float, trade_count: int, seed: int) -> float:
    """Estimate ruin probability via simulation."""
    rng = _random.Random(seed)
    ruin_count = 0
    sim_count = 500
    floor_frac = capital_floor_pct / 100.0

    for _ in range(sim_count):
        equity = 1.0
        peak = 1.0
        for _ in range(trade_count):
            if rng.random() < win_rate:
                equity *= (1.0 + avg_win / 100.0)
            else:
                equity *= (1.0 - avg_loss / 100.0)
            if equity > peak:
                peak = equity
            if equity <= floor_frac:
                ruin_count += 1
                break

    return round(ruin_count / sim_count * 100.0, 2)


def run_risk_of_ruin(ror_input, seed: int = 42):
    """Compute Risk-of-Ruin result. Returns RiskOfRuinResult."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import RiskOfRuinResult
    rng = _random.Random(seed + 9999)
    win_rate = ror_input.win_rate_pct / 100.0

    ruin_prob = _compute_ror_probability(
        win_rate=win_rate,
        avg_win=ror_input.avg_win_pct,
        avg_loss=ror_input.avg_loss_pct,
        capital_floor_pct=ror_input.capital_floor_pct,
        trade_count=100,
        seed=seed,
    )
    survival_prob = round(100.0 - ruin_prob, 2)

    # Simulate terminal equities
    equities = []
    drawdowns = []
    for i in range(500):
        rng2 = _random.Random(seed + i)
        equity = ror_input.initial_capital
        peak = equity
        max_dd = 0.0
        for _ in range(100):
            if rng2.random() < win_rate:
                equity *= (1.0 + ror_input.avg_win_pct / 100.0 * ror_input.single_trade_risk_pct / 100.0 * 10.0)
            else:
                equity *= (1.0 - ror_input.avg_loss_pct / 100.0 * ror_input.single_trade_risk_pct / 100.0 * 10.0)
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd
        equities.append(equity)
        drawdowns.append(max_dd)

    equities.sort()
    drawdowns.sort()
    n = len(equities)
    p5_eq = round(sum(equities[:max(1, int(n * 0.05))]) / max(1, int(n * 0.05)), 2)
    p95_eq = round(sum(equities[int(n * 0.95):]) / max(1, n - int(n * 0.95)), 2)
    median_eq = round(equities[n // 2], 2)
    expected_dd = round(sum(drawdowns) / n, 2)
    worst_5pct_dd = round(sum(drawdowns[int(n * 0.95):]) / max(1, n - int(n * 0.95)), 2)

    ror_score = round(min(100.0, ruin_prob * 5.0), 1)

    return RiskOfRuinResult(
        capital_floor_pct=ror_input.capital_floor_pct,
        max_drawdown_limit_pct=ror_input.max_drawdown_limit_pct,
        losing_streak_threshold=ror_input.losing_streak_threshold,
        ruin_probability_pct=ruin_prob,
        survival_probability_pct=survival_prob,
        expected_max_drawdown_pct=expected_dd,
        worst_5pct_drawdown_pct=worst_5pct_dd,
        median_terminal_equity=median_eq,
        worst_5pct_terminal_equity=p5_eq,
        best_5pct_terminal_equity=p95_eq,
        risk_of_ruin_score=ror_score,
        is_ruined=ruin_prob > 20.0,
    )


def run_risk_of_ruin_matrix(ror_input, seed: int = 42) -> list:
    """Run RoR for all capital floor / drawdown limit combinations."""
    results = []
    for floor_pct in CAPITAL_FLOOR_OPTIONS:
        for dd_limit in MAX_DRAWDOWN_LIMIT_OPTIONS:
            inp = type(ror_input)(
                initial_capital=ror_input.initial_capital,
                capital_floor_pct=float(floor_pct),
                max_drawdown_limit_pct=float(dd_limit),
                losing_streak_threshold=ror_input.losing_streak_threshold,
                single_trade_risk_pct=ror_input.single_trade_risk_pct,
                win_rate_pct=ror_input.win_rate_pct,
                avg_win_pct=ror_input.avg_win_pct,
                avg_loss_pct=ror_input.avg_loss_pct,
            )
            results.append(run_risk_of_ruin(inp, seed=seed))
    return results


def get_ror_info() -> dict:
    """Return RoR metadata dict."""
    return {
        "version": "1.8.3",
        "capital_floor_options": CAPITAL_FLOOR_OPTIONS,
        "max_drawdown_limit_options": MAX_DRAWDOWN_LIMIT_OPTIONS,
        "losing_streak_threshold_options": LOSING_STREAK_THRESHOLD_OPTIONS,
        "paper_only": True,
        "monte_carlo_only": True,
        "schema_version": "183",
    }
