"""
paper_trading/small_capital_strategy/optimization_engine_v182.py
Parameter optimization engine for v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import math  # noqa: F401

ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_FINAL_GRADES = frozenset({"ROBUST", "ACCEPTABLE", "UNSTABLE", "OVERFITTED", "BLOCKED"})


def validate_action(action: str) -> bool:
    """Return True if action is in ALLOWED_OUTPUT_ACTIONS."""
    return action in ALLOWED_OUTPUT_ACTIONS


def validate_grade(grade: str) -> bool:
    """Return True if grade is in VALID_FINAL_GRADES."""
    return grade in VALID_FINAL_GRADES


def _simulate_parameter_set(ps):
    """Deterministic simulation of a parameter set performance."""
    if ps.behavior_risk_limit == "BLOCKED" or ps.risk_dashboard_limit == "BLOCKED":
        ps.is_blocked = True
        ps.block_reason = "behavior_risk or risk_dashboard BLOCKED"
        return ps
    if ps.stop_loss_pct <= 0:
        ps.is_blocked = True
        ps.block_reason = "missing stop loss"
        return ps

    risk_score = ps.single_trade_risk_pct / ps.max_positions
    threshold_avg = (ps.theme_score_threshold + ps.watchlist_score_threshold + ps.abc_score_threshold) / 3.0
    selectivity = threshold_avg / 100.0

    base_return = (ps.take_profit_pct * 0.4) - (ps.stop_loss_pct * 0.15)
    adjusted_return = base_return * selectivity * (1.0 - risk_score * 0.1)

    ps.in_sample_return_pct = round(adjusted_return * 1.2, 2)
    ps.out_of_sample_return_pct = round(adjusted_return * 0.85, 2)
    ps.max_drawdown_pct = round(ps.stop_loss_pct * 0.6 * ps.max_positions * 0.3, 2)
    ps.win_rate_pct = round(45.0 + selectivity * 20.0, 1)
    ps.profit_factor = round(1.0 + (ps.take_profit_pct / ps.stop_loss_pct) * selectivity * 0.5, 2)
    ps.expectancy_r = round(
        (ps.win_rate_pct / 100.0) * (ps.take_profit_pct / ps.stop_loss_pct) - (1 - ps.win_rate_pct / 100.0), 2
    )

    if ps.max_drawdown_pct > ps.max_drawdown_limit_pct:
        ps.is_blocked = True
        ps.block_reason = "max_drawdown exceeds limit"

    return ps


def run_parameter_search(grid, config):
    """Run grid search over parameter grid."""
    from paper_trading.small_capital_strategy.optimization_models_v182 import (
        ParameterSet, ParameterSearchResult,
    )
    sets = []
    idx = 0
    for cap in grid.initial_capital_values:
        for risk in grid.single_trade_risk_pct_values:
            for pos in grid.max_positions_values:
                for sl in grid.stop_loss_pct_values:
                    for tp in grid.take_profit_pct_values[:2]:
                        idx += 1
                        ps = ParameterSet(
                            parameter_set_id=f"PS182-{idx:04d}",
                            initial_capital=cap, single_trade_risk_pct=risk,
                            max_positions=pos, stop_loss_pct=sl, take_profit_pct=tp,
                            trailing_stop_pct=8.0, max_drawdown_limit_pct=12.0,
                            theme_score_threshold=65.0, watchlist_score_threshold=65.0,
                            abc_score_threshold=65.0, behavior_risk_limit="PASS",
                            risk_dashboard_limit="PASS",
                        )
                        ps = _simulate_parameter_set(ps)
                        sets.append(ps)

    valid = [s for s in sets if not s.is_blocked]
    blocked = [s for s in sets if s.is_blocked]
    best = max(valid, key=lambda s: s.out_of_sample_return_pct, default=None)

    return ParameterSearchResult(
        total_parameter_sets=len(sets),
        valid_parameter_sets=len(valid),
        blocked_parameter_sets=len(blocked),
        best_in_sample_return_pct=best.in_sample_return_pct if best else 0.0,
        best_out_of_sample_return_pct=best.out_of_sample_return_pct if best else 0.0,
        average_out_of_sample_return_pct=round(sum(s.out_of_sample_return_pct for s in valid) / len(valid), 2) if valid else 0.0,
        best_parameter_set_id=best.parameter_set_id if best else "",
        parameter_sets=sets,
        search_mode="GRID_SEARCH",
    )


def rank_parameter_sets(result):
    """Rank valid parameter sets by composite score. Returns list of ParameterRanking."""
    from paper_trading.small_capital_strategy.optimization_models_v182 import ParameterRanking
    valid = [s for s in result.parameter_sets if not s.is_blocked]
    rankings = []
    for i, ps in enumerate(sorted(valid, key=lambda s: s.out_of_sample_return_pct, reverse=True)):
        stability = round(min(100.0, ps.win_rate_pct * 0.8 + ps.profit_factor * 5.0), 1)
        robustness = round(
            min(100.0, (ps.out_of_sample_return_pct / ps.in_sample_return_pct) * 100.0)
            if ps.in_sample_return_pct > 0 else 50.0, 1
        )
        overfitting = round(max(0.0, 100.0 - robustness), 1)

        if overfitting >= 70.0:
            grade = "OVERFITTED"
        elif robustness >= 80.0 and stability >= 70.0:
            grade = "ROBUST"
        elif robustness >= 60.0:
            grade = "ACCEPTABLE"
        else:
            grade = "UNSTABLE"

        rankings.append(ParameterRanking(
            rank=i + 1,
            parameter_set_id=ps.parameter_set_id,
            composite_score=round(robustness * 0.5 + stability * 0.3 + (100.0 - overfitting) * 0.2, 1),
            out_of_sample_return_pct=ps.out_of_sample_return_pct,
            stability_score=stability,
            robustness_score=robustness,
            overfitting_risk_score=overfitting,
            final_grade=grade,
        ))
    return rankings


def compute_stability_score(ps):
    """Compute stability score for a parameter set."""
    from paper_trading.small_capital_strategy.optimization_models_v182 import StabilityScore
    regime_consistency = round(min(100.0, ps.win_rate_pct * 0.9), 1)
    param_sensitivity = round(max(0.0, 100.0 - ps.single_trade_risk_pct * 10.0), 1)
    wf_consistency = round(min(100.0, ps.profit_factor * 25.0), 1)
    dd_consistency = round(max(0.0, 100.0 - ps.max_drawdown_pct * 3.0), 1)
    score = round((regime_consistency + param_sensitivity + wf_consistency + dd_consistency) / 4.0, 1)
    is_stable = score >= 60.0
    if score >= 75.0:
        grade = "STABLE"
    elif score >= 60.0:
        grade = "ACCEPTABLE"
    elif score >= 40.0:
        grade = "UNSTABLE"
    else:
        grade = "BLOCKED"
    return StabilityScore(
        score=score, regime_consistency=regime_consistency,
        parameter_sensitivity=param_sensitivity,
        walk_forward_consistency=wf_consistency,
        drawdown_consistency=dd_consistency,
        is_stable=is_stable, stability_grade=grade,
    )


def get_engine_info() -> dict:
    """Return engine metadata dict."""
    return {
        "version": "1.8.2",
        "allowed_output_actions": sorted(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": sorted(FORBIDDEN_OUTPUT_WORDS),
        "valid_final_grades": sorted(VALID_FINAL_GRADES),
        "paper_only": True,
        "validation_only": True,
        "no_real_orders": True,
        "schema_version": "182",
    }
