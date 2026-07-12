"""
paper_trading/small_capital_strategy/monte_carlo_engine_v183.py
Monte Carlo engine for Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import random as _random

ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "MONTE_CARLO_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_FINAL_GRADES = frozenset({
    "ROBUST", "ACCEPTABLE", "FRAGILE", "HIGH_RISK", "RUIN_RISK", "BLOCKED",
})

VALID_TRIAL_COUNTS = frozenset({100, 500, 1000, 5000})


def validate_action(action: str) -> bool:
    """Return True if action is in ALLOWED_OUTPUT_ACTIONS."""
    return action in ALLOWED_OUTPUT_ACTIONS


def validate_grade(grade: str) -> bool:
    """Return True if grade is in VALID_FINAL_GRADES."""
    return grade in VALID_FINAL_GRADES


def _grade_from_scores(ruin_prob: float, survival_rate: float, worst_dd: float) -> str:
    """Derive final grade from ruin probability, survival rate, worst 5% drawdown."""
    if ruin_prob > 20.0 or survival_rate < 50.0:
        return "RUIN_RISK"
    if ruin_prob > 10.0 or worst_dd > 40.0:
        return "HIGH_RISK"
    if ruin_prob > 5.0 or worst_dd > 30.0:
        return "FRAGILE"
    if ruin_prob > 2.0 or worst_dd > 20.0:
        return "ACCEPTABLE"
    return "ROBUST"


def _simulate_trial(mc_input, trial_id: int, seed: int):
    """Simulate a single Monte Carlo trial deterministically."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import MonteCarloTrial
    rng = _random.Random(seed + trial_id)

    capital = mc_input.initial_capital
    capital_floor = mc_input.initial_capital * (mc_input.capital_floor_pct / 100.0)
    max_dd_pct = 0.0
    peak_capital = capital
    consecutive_losses = 0
    max_consecutive_losses = 0
    wins = 0
    losses = 0
    ruined = False
    ruin_reason = ""

    trades = list(range(mc_input.trade_count_per_trial))
    rng.shuffle(trades)

    for _ in trades:
        # Apply slippage and cost
        effective_slippage = mc_input.slippage_pct
        effective_cost = mc_input.transaction_cost_pct

        # Determine outcome
        roll = rng.random()
        if roll < (mc_input.win_rate_pct / 100.0):
            gain_pct = mc_input.avg_win_pct * (0.8 + rng.random() * 0.4)
            trade_return = capital * mc_input.single_trade_risk_pct / 100.0 * (gain_pct / mc_input.stop_loss_pct)
            trade_return -= capital * (effective_slippage + effective_cost) / 100.0
            capital += trade_return
            wins += 1
            consecutive_losses = 0
        else:
            loss_pct = mc_input.avg_loss_pct * (0.8 + rng.random() * 0.4)
            trade_loss = capital * mc_input.single_trade_risk_pct / 100.0 * (loss_pct / mc_input.stop_loss_pct)
            trade_loss += capital * (effective_slippage + effective_cost) / 100.0
            capital -= trade_loss
            losses += 1
            consecutive_losses += 1
            if consecutive_losses > max_consecutive_losses:
                max_consecutive_losses = consecutive_losses

        if capital > peak_capital:
            peak_capital = capital
        current_dd = (peak_capital - capital) / peak_capital * 100.0 if peak_capital > 0 else 0.0
        if current_dd > max_dd_pct:
            max_dd_pct = current_dd

        # Ruin checks
        if capital <= capital_floor:
            ruined = True
            ruin_reason = "capital_floor_breached"
            break
        if max_dd_pct >= mc_input.max_drawdown_limit_pct:
            ruined = True
            ruin_reason = "max_drawdown_exceeded"
            break
        if consecutive_losses >= mc_input.losing_streak_threshold and capital <= capital_floor * 1.1:
            ruined = True
            ruin_reason = "losing_streak_at_floor"
            break

    terminal_return = (capital - mc_input.initial_capital) / mc_input.initial_capital * 100.0

    return MonteCarloTrial(
        trial_id=trial_id,
        seed_used=seed + trial_id,
        terminal_equity=round(capital, 2),
        terminal_return_pct=round(terminal_return, 2),
        max_drawdown_pct=round(max_dd_pct, 2),
        max_consecutive_losses=max_consecutive_losses,
        trade_count=wins + losses,
        win_count=wins,
        loss_count=losses,
        ruined=ruined,
        ruin_reason=ruin_reason,
    )


def run_monte_carlo(mc_input, config):
    """Run Monte Carlo simulation. Returns MonteCarloResult."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import MonteCarloResult

    trial_count = config.trial_count
    seed = config.random_seed
    trials = [_simulate_trial(mc_input, i, seed) for i in range(trial_count)]

    ruined_trials = [t for t in trials if t.ruined]
    surviving_trials = [t for t in trials if not t.ruined]
    ruin_count = len(ruined_trials)
    ruin_prob = ruin_count / trial_count * 100.0
    survival_rate = 100.0 - ruin_prob

    returns = sorted(t.terminal_return_pct for t in trials)
    drawdowns = sorted(t.max_drawdown_pct for t in trials)
    n = len(returns)
    p5_idx = max(0, int(n * 0.05) - 1)
    p95_idx = min(n - 1, int(n * 0.95))

    median_ret = returns[n // 2]
    avg_ret = round(sum(returns) / n, 2)
    worst_5pct_ret = round(sum(returns[:max(1, int(n * 0.05))]) / max(1, int(n * 0.05)), 2)
    best_5pct_ret = round(sum(returns[int(n * 0.95):]) / max(1, n - int(n * 0.95)), 2)

    median_dd = drawdowns[n // 2]
    avg_dd = round(sum(drawdowns) / n, 2)
    worst_5pct_dd = round(sum(drawdowns[int(n * 0.95):]) / max(1, n - int(n * 0.95)), 2)

    # Consecutive loss distribution
    max_cl_dist = {}
    for t in trials:
        k = str(t.max_consecutive_losses)
        max_cl_dist[k] = max_cl_dist.get(k, 0) + 1

    # Scores
    ror_score = round(min(100.0, ruin_prob * 5.0), 1)
    seq_risk_score = round(min(100.0, sum(t.max_consecutive_losses for t in trials) / n * 5.0), 1)
    tail_risk_score = round(min(100.0, abs(worst_5pct_ret) * 2.0), 1)
    rob_prob = round(max(0.0, survival_rate - ror_score * 0.3), 1)

    # Sensitivity scores (simplified: compare baseline vs shocked)
    cost_sensitivity = round(min(100.0, abs(avg_ret) * 0.5 + 10.0), 1) if avg_ret < 0 else round(max(0.0, 100.0 - avg_ret * 2.0), 1)
    slippage_sensitivity = round(min(100.0, abs(worst_5pct_ret) * 0.5), 1)

    grade = _grade_from_scores(ruin_prob, survival_rate, worst_5pct_dd)

    return MonteCarloResult(
        trial_count=trial_count,
        survival_rate_pct=round(survival_rate, 2),
        ruin_probability_pct=round(ruin_prob, 2),
        median_return_pct=round(median_ret, 2),
        average_return_pct=avg_ret,
        worst_5pct_return_pct=worst_5pct_ret,
        best_5pct_return_pct=best_5pct_ret,
        median_max_drawdown_pct=round(median_dd, 2),
        average_max_drawdown_pct=avg_dd,
        worst_5pct_max_drawdown_pct=worst_5pct_dd,
        max_consecutive_loss_distribution=max_cl_dist,
        risk_of_ruin_score=ror_score,
        sequence_risk_score=seq_risk_score,
        tail_risk_score=tail_risk_score,
        robustness_probability_pct=rob_prob,
        cost_sensitivity_score=cost_sensitivity,
        slippage_sensitivity_score=slippage_sensitivity,
        final_grade=grade,
        trials=trials,
    )


def get_engine_info() -> dict:
    """Return engine metadata dict."""
    return {
        "version": "1.8.3",
        "allowed_output_actions": sorted(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": sorted(FORBIDDEN_OUTPUT_WORDS),
        "valid_final_grades": sorted(VALID_FINAL_GRADES),
        "valid_trial_counts": sorted(VALID_TRIAL_COUNTS),
        "paper_only": True,
        "monte_carlo_only": True,
        "no_real_orders": True,
        "schema_version": "183",
    }
