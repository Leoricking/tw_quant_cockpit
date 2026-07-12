"""
paper_trading/small_capital_strategy/monte_carlo_bootstrap_v183.py
Bootstrap resampling engine for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import random as _random

BOOTSTRAP_TYPES = [
    "WITH_REPLACEMENT",
    "BLOCK_BOOTSTRAP",
    "CIRCULAR_BOOTSTRAP",
    "STATIONARY_BOOTSTRAP",
    "REGIME_BOOTSTRAP",
]


def run_bootstrap(mc_input, config, sample_count: int = 500):
    """Run bootstrap resampling on Monte Carlo input. Returns BootstrapResult."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
        BootstrapSample, BootstrapResult,
    )
    rng = _random.Random(config.random_seed + 7777)
    samples = []
    win_rate = mc_input.win_rate_pct / 100.0

    for i in range(sample_count):
        n = mc_input.trade_count_per_trial
        wins = sum(1 for _ in range(n) if rng.random() < win_rate)
        losses = n - wins
        sample_win_rate = wins / n * 100.0
        avg_return = wins * mc_input.avg_win_pct / n - losses * mc_input.avg_loss_pct / n
        max_dd = round(max(0.0, (1.0 - sample_win_rate / 100.0) * mc_input.avg_loss_pct * 3.0), 2)
        samples.append(BootstrapSample(
            sample_id=i,
            sample_size=n,
            resampled_return_pct=round(avg_return, 2),
            resampled_max_drawdown_pct=max_dd,
            resampled_win_rate_pct=round(sample_win_rate, 2),
            with_replacement=True,
        ))

    returns = sorted(s.resampled_return_pct for s in samples)
    drawdowns = sorted(s.resampled_max_drawdown_pct for s in samples)
    n_s = len(returns)
    mean_ret = round(sum(returns) / n_s, 2)
    mean_dd = round(sum(drawdowns) / n_s, 2)
    p5_idx = max(0, int(n_s * 0.05))
    p95_idx = min(n_s - 1, int(n_s * 0.95))
    ci_lower = round(returns[p5_idx], 2)
    ci_upper = round(returns[p95_idx], 2)
    worst_5pct_dd = round(sum(drawdowns[int(n_s * 0.95):]) / max(1, n_s - int(n_s * 0.95)), 2)

    bootstrap_passed = mean_ret > 0.0 and worst_5pct_dd < mc_input.max_drawdown_limit_pct

    # Variance
    variance = sum((r - mean_ret) ** 2 for r in returns) / n_s
    std_ret = round(variance ** 0.5, 2)

    return BootstrapResult(
        sample_count=sample_count,
        mean_return_pct=mean_ret,
        std_return_pct=std_ret,
        ci_lower_5pct=ci_lower,
        ci_upper_95pct=ci_upper,
        mean_max_drawdown_pct=mean_dd,
        worst_5pct_drawdown_pct=worst_5pct_dd,
        bootstrap_passed=bootstrap_passed,
        samples=samples,
    )


def get_bootstrap_info() -> dict:
    """Return bootstrap metadata dict."""
    return {
        "version": "1.8.3",
        "bootstrap_types": BOOTSTRAP_TYPES,
        "count": len(BOOTSTRAP_TYPES),
        "paper_only": True,
        "monte_carlo_only": True,
        "schema_version": "183",
    }
