"""
strategy_robustness/monte_carlo_v142.py — Monte Carlo trade-order analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import random
import statistics
from typing import List

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

MAX_MC_ITERATIONS = 10000


def _simulate_equity(trades_shuffled: list, initial: float = 1.0) -> tuple:
    """Simulate equity curve from shuffled trades. Returns (terminal, max_drawdown, max_consec_loss)."""
    equity = initial
    peak = initial
    max_dd = 0.0
    consec_loss = 0
    max_consec_loss = 0

    for t in trades_shuffled:
        ret = t.get("return_pct", 0.0)
        cost = t.get("cost", 0.0)
        net = ret - cost
        equity *= (1 + net)
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd
        if net < 0:
            consec_loss += 1
            max_consec_loss = max(max_consec_loss, consec_loss)
        else:
            consec_loss = 0

    return equity, max_dd, max_consec_loss


class MonteCarloTradeOrderAnalyzer:
    """
    Monte Carlo simulation by randomly shuffling trade order.
    Original trades are not modified.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Run Monte Carlo simulation on trade ordering.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with Monte Carlo simulation results
        """
        n_iter = min(getattr(config, "monte_carlo_iterations", 1000), MAX_MC_ITERATIONS)
        seed = getattr(config, "random_seed", 42)

        if not trades or len(trades) < 3:
            return {
                "status": "INSUFFICIENT",
                "trade_count": len(trades) if trades else 0,
                "iterations": 0,
                "seed": seed,
                "warnings": ["INSUFFICIENT_TRADES_FOR_MONTE_CARLO"],
            }

        rng = random.Random(seed)
        original_trades = list(trades)  # Do not modify original

        terminal_capitals = []
        max_drawdowns = []
        max_consec_losses = []

        for _ in range(n_iter):
            shuffled = list(original_trades)
            rng.shuffle(shuffled)
            terminal, max_dd, consec = _simulate_equity(shuffled)
            terminal_capitals.append(terminal)
            max_drawdowns.append(max_dd)
            max_consec_losses.append(consec)

        terminal_capitals.sort()
        max_drawdowns.sort()
        max_consec_losses.sort()

        n_sims = len(terminal_capitals)
        median_terminal = statistics.median(terminal_capitals)
        p5_terminal = terminal_capitals[int(n_sims * 0.05)]
        p95_terminal = terminal_capitals[int(n_sims * 0.95)]
        median_max_dd = statistics.median(max_drawdowns)
        worst_dd = max(max_drawdowns)

        # Max consecutive loss distribution
        consec_dist: dict = {}
        for v in max_consec_losses:
            consec_dist[str(v)] = consec_dist.get(str(v), 0) + 1

        # Ruin probability (equity < 0.5 of initial)
        ruin_count = sum(1 for c in terminal_capitals if c < 0.5)
        ruin_probability = ruin_count / n_sims

        status = "PASS" if p5_terminal >= 1.0 else ("MARGINAL" if median_terminal >= 1.0 else "FAIL")

        return {
            "status": status,
            "trade_count": len(original_trades),
            "iterations": n_iter,
            "seed": seed,
            "median_terminal_capital": round(median_terminal, 6),
            "p5_terminal_capital": round(p5_terminal, 6),
            "p95_terminal_capital": round(p95_terminal, 6),
            "median_max_drawdown": round(median_max_dd, 4),
            "worst_simulated_drawdown": round(worst_dd, 4),
            "max_consecutive_loss_distribution": consec_dist,
            "ruin_probability_approximation": round(ruin_probability, 4),
            "warnings": [] if p5_terminal >= 1.0 else ["TAIL_RISK_RUIN"],
        }
