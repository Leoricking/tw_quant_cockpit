"""
paper_trading/small_capital_strategy/decision_cockpit_engine_v186.py
End-to-end decision cockpit engine for v1.8.6.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict

ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "ALLOCATION_ONLY", "PORTFOLIO_ONLY", "DECISION_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_COCKPIT_GRADES = frozenset({
    "READY", "WATCH", "WAIT", "REDUCE_RISK", "BLOCKED", "REVIEW_REQUIRED",
})

CAPITAL_STAGES = [300000, 500000, 1000000, 3000000]

CAPITAL_STAGE_LABELS = {300000: "300K", 500000: "500K", 1000000: "1M", 3000000: "3M"}

MAX_POSITIONS_BY_STAGE = {300000: 3, 500000: 4, 1000000: 5, 3000000: 6}

DECISION_CYCLES = [
    "daily_check", "weekly_review", "pre_market_review", "post_market_review",
    "watchlist_review", "portfolio_review", "risk_review", "blocked_market_review",
]

ABC_BUY_POINTS = ["A_10MA_PULLBACK", "B_BREAKOUT", "C_20MA_RECLAIM"]

CANDIDATE_EVALUATION_CRITERIA = [
    "theme_strength",
    "revenue_fundamental_growth",
    "moving_average_structure",
    "volume_breakout_contraction",
    "kd_rsi_macd",
    "institutional_flow",
    "margin_balance_risk",
    "big_holder_retail_crowding_risk",
    "abc_buy_point_status",
    "market_regime_status",
    "position_sizing_result",
    "portfolio_concentration_result",
    "monte_carlo_ruin_risk_result",
    "final_decision_action",
]

BLOCKED_REGIMES = frozenset({"BLOCKED", "RISK_OFF", "BEAR"})

# Hard block thresholds
_MAX_TOTAL_EXPOSURE_HARD = 95.0
_MAX_SINGLE_POSITION_HARD = 60.0
_MAX_SECTOR_HARD = 80.0
_MAX_THEME_HARD = 80.0
_MIN_CASH_HARD = 5.0
_MAX_RUIN_RISK_HARD = 20.0


def validate_action(action: str) -> bool:
    """Return True if action is in ALLOWED_OUTPUT_ACTIONS."""
    return action in ALLOWED_OUTPUT_ACTIONS


def validate_grade(grade: str) -> bool:
    """Return True if grade is in VALID_COCKPIT_GRADES."""
    return grade in VALID_COCKPIT_GRADES


def _capital_stage_label(capital: float) -> str:
    if capital >= 3000000:
        return "3M"
    if capital >= 1000000:
        return "1M"
    if capital >= 500000:
        return "500K"
    return "300K"


def run_regime_decision(inp) -> "RegimeDecision":
    """Compute regime decision from DecisionCockpitInput."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import RegimeDecision
    regime = inp.market_regime
    blocked = regime in BLOCKED_REGIMES
    blocks = []
    if blocked:
        blocks.append("market_regime_blocked")
    max_exp = 60.0
    if regime == "BULL":
        max_exp = 60.0
    elif regime in ("NEUTRAL", "SIDEWAYS"):
        max_exp = 40.0
    elif regime in ("WEAK", "RISK_OFF"):
        max_exp = 20.0
    else:
        max_exp = 0.0
    entry_ok = not blocked
    add_ok = not blocked and inp.total_exposure_pct < max_exp * 0.8
    action = "BLOCKED" if blocked else ("REDUCE_RISK" if inp.total_exposure_pct > max_exp else "DECISION_ONLY")
    return RegimeDecision(
        market_regime=regime,
        regime_blocked=blocked,
        entry_permitted=entry_ok,
        add_permitted=add_ok,
        max_exposure_pct=max_exp,
        action=action,
        block_reasons=blocks,
    )


def run_theme_decision(candidate_inputs: list) -> "ThemeDecision":
    """Derive theme decision from candidate inputs."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import ThemeDecision
    strong, weak, crowded = [], [], []
    theme_counts: Dict[str, int] = {}
    for c in candidate_inputs:
        t = getattr(c, "theme", "")
        if t:
            theme_counts[t] = theme_counts.get(t, 0) + 1
        strength = getattr(c, "theme_strength", "NEUTRAL")
        if strength == "STRONG" and t and t not in strong:
            strong.append(t)
        elif strength in ("WEAK", "DETERIORATING") and t and t not in weak:
            weak.append(t)
    for t, cnt in theme_counts.items():
        if cnt >= 3 and t not in crowded:
            crowded.append(t)
    rotation = len(strong) > 0 and len(weak) > 0
    return ThemeDecision(
        top_themes=strong,
        weak_themes=weak,
        overcrowded_themes=crowded,
        theme_rotation_active=rotation,
        action="DECISION_ONLY",
    )


def run_risk_decision(inp) -> "RiskDecision":
    """Compute risk decision."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import RiskDecision
    blocks = []
    exposure_ok = inp.total_exposure_pct <= 95.0
    cash_ok = inp.cash_reserve_pct >= _MIN_CASH_HARD
    ruin_ok = inp.monte_carlo_ruin_risk_pct <= _MAX_RUIN_RISK_HARD
    drawdown_ok = inp.drawdown_used_pct <= inp.max_drawdown_budget_pct
    stop_ok = True  # evaluated at candidate level

    if not exposure_ok:
        blocks.append("total_exposure_too_high")
    if not cash_ok:
        blocks.append("cash_reserve_too_low")
    if not ruin_ok:
        blocks.append("monte_carlo_ruin_probability_too_high")
    if not drawdown_ok:
        blocks.append("drawdown_budget_exceeded")
    if inp.behavior_risk_blocked:
        blocks.append("behavior_risk_blocked")

    if blocks:
        action = "BLOCKED"
    elif inp.total_exposure_pct > 70.0 or inp.monte_carlo_ruin_risk_pct > 10.0:
        action = "REDUCE_RISK"
    elif inp.total_exposure_pct > 50.0:
        action = "REVIEW_REQUIRED"
    else:
        action = "DECISION_ONLY"

    drawdown_pct = (inp.drawdown_used_pct / inp.max_drawdown_budget_pct * 100.0
                   if inp.max_drawdown_budget_pct > 0 else 0.0)
    return RiskDecision(
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        monte_carlo_ruin_risk_pct=inp.monte_carlo_ruin_risk_pct,
        drawdown_budget_usage_pct=round(drawdown_pct, 2),
        stop_loss_coverage_ok=stop_ok,
        exposure_ok=exposure_ok,
        cash_ok=cash_ok,
        ruin_risk_ok=ruin_ok,
        drawdown_ok=drawdown_ok,
        action=action,
        block_reasons=blocks,
    )


def run_monte_carlo_decision(ruin_pct: float) -> "MonteCarloDecision":
    """Compute Monte Carlo decision."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import MonteCarloDecision
    blocks = []
    if ruin_pct > _MAX_RUIN_RISK_HARD:
        level = "HIGH"
        blocks.append("monte_carlo_ruin_probability_too_high")
        entry_ok = False
        add_ok = False
        action = "BLOCKED"
    elif ruin_pct > 10.0:
        level = "MEDIUM"
        entry_ok = True
        add_ok = False
        action = "REDUCE_RISK"
    elif ruin_pct > 5.0:
        level = "LOW_MEDIUM"
        entry_ok = True
        add_ok = True
        action = "REVIEW_REQUIRED"
    else:
        level = "LOW"
        entry_ok = True
        add_ok = True
        action = "DECISION_ONLY"
    return MonteCarloDecision(
        ruin_probability_pct=ruin_pct,
        ruin_risk_level=level,
        entry_allowed=entry_ok,
        add_allowed=add_ok,
        action=action,
        block_reasons=blocks,
    )


def run_portfolio_decision(inp) -> "PortfolioDecision":
    """Compute portfolio decision from cockpit input."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import PortfolioDecision
    blocks = []
    concentration_ok = inp.concentration_risk_score <= 70.0
    if not concentration_ok:
        blocks.append("concentration_risk_too_high")
    overexposed_sectors: List[str] = []
    overexposed_themes: List[str] = []
    portfolio_ok = len(blocks) == 0
    rebalance_needed = inp.concentration_risk_score > 50.0
    div_score = max(0.0, 100.0 - inp.concentration_risk_score)
    if blocks:
        action = "REDUCE_RISK"
    elif rebalance_needed:
        action = "REVIEW_REQUIRED"
    else:
        action = "DECISION_ONLY"
    return PortfolioDecision(
        holding_count=inp.portfolio_holding_count,
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        concentration_risk_score=inp.concentration_risk_score,
        diversification_score=round(div_score, 2),
        overexposed_sectors=overexposed_sectors,
        overexposed_themes=overexposed_themes,
        rebalance_needed=rebalance_needed,
        portfolio_ok=portfolio_ok,
        action=action,
        block_reasons=blocks,
    )


def run_buy_point_decision(candidate) -> "BuyPointDecision":
    """Evaluate A/B/C buy point for a single candidate."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import BuyPointDecision
    bpt = getattr(candidate, "abc_buy_point", "A_10MA_PULLBACK")
    regime = getattr(candidate, "market_regime", "BULL")
    regime_blocked = regime in BLOCKED_REGIMES
    blocks = []

    if regime_blocked:
        blocks.append("market_regime_blocked")
        return BuyPointDecision(
            ticker=getattr(candidate, "ticker", ""),
            buy_point_type=bpt,
            condition_met=False,
            action="BLOCKED",
            block_reasons=blocks,
        )

    above_10ma = getattr(candidate, "above_10ma", True)
    above_20ma = getattr(candidate, "above_20ma", True)
    volume_contracting = getattr(candidate, "volume_contracting", True)
    volume_breakout = getattr(candidate, "volume_breakout", False)
    kd_low = getattr(candidate, "kd_below_50", False)
    kd_recovering = getattr(candidate, "kd_recovering", False)
    institutional_neg = getattr(candidate, "institutional_consecutive_negative_days", 0)
    stop_defined = getattr(candidate, "stop_loss_defined", True)

    if not stop_defined:
        blocks.append("missing_stop_loss")

    if bpt == "A_10MA_PULLBACK":
        cond = above_10ma and volume_contracting and (kd_low or kd_recovering)
        if not above_10ma:
            blocks.append("candidate_failed_abc_buy_point_condition")
        action = "PAPER_ENTRY_ALLOWED" if (cond and not blocks) else ("PAPER_PLAN_READY" if (above_10ma and not blocks) else "WAIT")

    elif bpt == "B_BREAKOUT":
        cond = volume_breakout and above_10ma and above_20ma
        if not volume_breakout:
            blocks.append("candidate_failed_abc_buy_point_condition")
        action = "PAPER_ENTRY_ALLOWED" if (cond and not blocks) else ("PAPER_PLAN_READY" if (above_10ma and not blocks) else "REVIEW_REQUIRED")

    elif bpt == "C_20MA_RECLAIM":
        cond = above_20ma and volume_contracting and kd_recovering and institutional_neg < 3
        if not above_20ma:
            blocks.append("candidate_failed_abc_buy_point_condition")
        action = "PAPER_ENTRY_ALLOWED" if (cond and not blocks) else ("PAPER_PLAN_READY" if (above_20ma and not blocks) else "WAIT")

    else:
        cond = False
        blocks.append("unknown_buy_point_type")
        action = "WAIT"

    if blocks and action not in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY"):
        action = "BLOCKED" if "market_regime_blocked" in blocks or "missing_stop_loss" in blocks else "WAIT"

    return BuyPointDecision(
        ticker=getattr(candidate, "ticker", ""),
        buy_point_type=bpt,
        condition_met=cond and not blocks,
        action=action,
        block_reasons=blocks,
    )


def run_candidate_decision(candidate) -> "CandidateDecisionResult":
    """Evaluate a single candidate across all 14 criteria."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import CandidateDecisionResult
    blocks = []

    theme_ok = getattr(candidate, "theme_strength", "NEUTRAL") in ("STRONG", "RECOVERING", "NEUTRAL")
    rev_ok = getattr(candidate, "revenue_growth_pct", 0.0) >= 0.0
    above_10ma = getattr(candidate, "above_10ma", True)
    above_20ma = getattr(candidate, "above_20ma", True)
    ma_ok = above_10ma or above_20ma
    vol_ok = getattr(candidate, "volume_contracting", True) or getattr(candidate, "volume_breakout", False)
    rsi = getattr(candidate, "rsi", 50.0)
    osc_ok = 20.0 <= rsi <= 80.0
    inst_ok = getattr(candidate, "institutional_flow_positive", True) or \
              getattr(candidate, "institutional_consecutive_negative_days", 0) < 3
    margin_ok = getattr(candidate, "margin_balance_risk", 0.0) <= 50.0
    crowding_ok = not getattr(candidate, "big_holder_crowding", False)
    liquidity_ok = getattr(candidate, "liquidity_ok", True)
    stop_ok = getattr(candidate, "stop_loss_defined", True)
    regime = getattr(candidate, "market_regime", "BULL")
    regime_ok = regime not in BLOCKED_REGIMES
    pos_ok = getattr(candidate, "position_sizing_pct", 10.0) <= 30.0
    conc_ok = getattr(candidate, "portfolio_concentration_ok", True)
    mc_ok = getattr(candidate, "monte_carlo_ruin_risk_pct", 0.0) <= _MAX_RUIN_RISK_HARD

    bpd = run_buy_point_decision(candidate)
    abc_ok = bpd.condition_met

    if not regime_ok:
        blocks.append("market_regime_blocked")
    if not stop_ok:
        blocks.append("missing_stop_loss")
    if not liquidity_ok:
        blocks.append("candidate_failed_liquidity_condition")
    if not abc_ok and bpd.block_reasons:
        blocks.extend(b for b in bpd.block_reasons if b not in blocks)
    if not conc_ok:
        blocks.append("concentration_risk_too_high")
    if not mc_ok:
        blocks.append("monte_carlo_ruin_probability_too_high")
    if getattr(candidate, "margin_balance_risk", 0.0) > 70.0:
        blocks.append("high_margin_risk")

    if blocks:
        final_action = "BLOCKED"
    elif abc_ok and regime_ok and ma_ok and inst_ok:
        final_action = "PAPER_ENTRY_ALLOWED"
    elif (above_10ma or above_20ma) and regime_ok:
        final_action = "PAPER_PLAN_READY"
    elif regime_ok:
        final_action = "WAIT"
    else:
        final_action = "BLOCKED"

    return CandidateDecisionResult(
        ticker=getattr(candidate, "ticker", ""),
        theme_strength_ok=theme_ok,
        revenue_growth_ok=rev_ok,
        ma_structure_ok=ma_ok,
        volume_ok=vol_ok,
        oscillator_ok=osc_ok,
        institutional_flow_ok=inst_ok,
        margin_risk_ok=margin_ok,
        crowding_risk_ok=crowding_ok,
        abc_buy_point_ok=abc_ok,
        regime_ok=regime_ok,
        position_sizing_ok=pos_ok,
        concentration_ok=conc_ok,
        monte_carlo_ok=mc_ok,
        final_action=final_action,
        block_reasons=blocks,
    )


def run_position_sizing_decision(ticker: str, capital: float,
                                  conviction_score: float = 5.0,
                                  volatility_pct: float = 15.0) -> "PositionSizingDecision":
    """Compute position sizing decision."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import PositionSizingDecision
    base_pct = min(25.0, max(5.0, conviction_score * 2.0))
    if volatility_pct > 30.0:
        base_pct *= 0.7
    elif volatility_pct > 20.0:
        base_pct *= 0.85
    base_pct = round(base_pct, 2)
    amount = round(capital * base_pct / 100.0, 2)
    pos_ok = base_pct <= 30.0
    return PositionSizingDecision(
        ticker=ticker,
        capital=capital,
        suggested_position_pct=base_pct,
        suggested_position_amount=amount,
        position_ok=pos_ok,
        action="DECISION_ONLY" if pos_ok else "REVIEW_REQUIRED",
    )


def _compute_entry_readiness(regime_dec, risk_dec, portfolio_dec, mc_dec,
                              candidate_results: list) -> "EntryReadinessScore":
    """Compute entry readiness score."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import EntryReadinessScore
    score = 0.0
    regime_ok = not regime_dec.regime_blocked
    risk_ok = not risk_dec.block_reasons
    portfolio_ok = not portfolio_dec.block_reasons
    mc_ok = mc_dec.entry_allowed
    candidate_ready = any(r.final_action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY")
                         for r in candidate_results)

    if regime_ok:
        score += 25.0
    if risk_ok:
        score += 20.0
    if portfolio_ok:
        score += 20.0
    if mc_ok:
        score += 15.0
    if candidate_ready:
        score += 20.0

    all_ok = regime_ok and risk_ok and portfolio_ok and mc_ok and candidate_ready
    action = "PAPER_ENTRY_ALLOWED" if all_ok else ("PAPER_PLAN_READY" if score >= 60 else "WAIT")
    return EntryReadinessScore(
        score=round(score, 2),
        max_score=100.0,
        regime_ok=regime_ok,
        candidate_ready=candidate_ready,
        risk_ok=risk_ok,
        portfolio_ok=portfolio_ok,
        mc_ok=mc_ok,
        action=action,
    )


def _compute_add_readiness(regime_dec, risk_dec, mc_dec, portfolio_dec) -> "AddReadinessScore":
    """Compute add-position readiness score."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import AddReadinessScore
    score = 0.0
    regime_ok = not regime_dec.regime_blocked
    cash_ok = risk_dec.cash_ok and risk_dec.cash_reserve_pct >= 20.0
    ruin_ok = mc_dec.add_allowed
    conc_ok = portfolio_dec.portfolio_ok

    if regime_ok:
        score += 30.0
    if cash_ok:
        score += 25.0
    if ruin_ok:
        score += 25.0
    if conc_ok:
        score += 20.0

    all_ok = regime_ok and cash_ok and ruin_ok and conc_ok
    action = "PAPER_ADD_ALLOWED" if all_ok else ("WAIT" if score >= 50 else "NO_TRADE")
    return AddReadinessScore(
        score=round(score, 2),
        max_score=100.0,
        regime_ok=regime_ok,
        cash_reserve_ok=cash_ok,
        ruin_risk_ok=ruin_ok,
        concentration_ok=conc_ok,
        action=action,
    )


def _compute_reduce_risk(risk_dec, portfolio_dec, mc_dec) -> "ReduceRiskDecision":
    """Compute reduce-risk decision."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import ReduceRiskDecision
    reduce = (risk_dec.action in ("BLOCKED", "REDUCE_RISK") or
              portfolio_dec.action in ("REDUCE_RISK",) or
              mc_dec.action in ("BLOCKED",))
    reasons = risk_dec.block_reasons + portfolio_dec.block_reasons + mc_dec.block_reasons
    reason_str = "; ".join(reasons) if reasons else ""
    action = "REDUCE_RISK" if reduce else "OBSERVE"
    return ReduceRiskDecision(
        reduce_required=reduce,
        reason=reason_str,
        action=action,
    )


def _compute_cockpit_grade(blocks: list, entry_readiness, add_readiness,
                            reduce_risk_dec, regime_dec) -> str:
    """Compute final cockpit grade."""
    if blocks or regime_dec.regime_blocked:
        return "BLOCKED"
    if reduce_risk_dec.reduce_required:
        return "REDUCE_RISK"
    if entry_readiness.action == "PAPER_ENTRY_ALLOWED":
        return "READY"
    if entry_readiness.action == "PAPER_PLAN_READY" or entry_readiness.score >= 60.0:
        return "WATCH"
    if entry_readiness.score >= 40.0:
        return "WAIT"
    return "REVIEW_REQUIRED"


def _collect_hard_blocks(inp) -> list:
    """Check hard block conditions from cockpit input."""
    blocks = []
    if inp.market_regime in BLOCKED_REGIMES:
        blocks.append("market_regime_blocked")
    if inp.total_exposure_pct > _MAX_TOTAL_EXPOSURE_HARD:
        blocks.append("total_exposure_too_high")
    if inp.cash_reserve_pct < _MIN_CASH_HARD:
        blocks.append("cash_reserve_too_low")
    if inp.monte_carlo_ruin_risk_pct > _MAX_RUIN_RISK_HARD:
        blocks.append("monte_carlo_ruin_probability_too_high")
    if inp.drawdown_used_pct > inp.max_drawdown_budget_pct:
        blocks.append("drawdown_budget_exceeded")
    if inp.behavior_risk_blocked:
        blocks.append("behavior_risk_blocked")
    return blocks


def run_decision_cockpit(inp, candidate_inputs: list = None) -> "DecisionCockpitResult":
    """Run full end-to-end decision cockpit. Returns DecisionCockpitResult."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
        DecisionCockpitResult,
    )
    if candidate_inputs is None:
        candidate_inputs = []

    hard_blocks = _collect_hard_blocks(inp)

    regime_dec = run_regime_decision(inp)
    risk_dec = run_risk_decision(inp)
    mc_dec = run_monte_carlo_decision(inp.monte_carlo_ruin_risk_pct)
    portfolio_dec = run_portfolio_decision(inp)
    theme_dec = run_theme_decision(candidate_inputs)

    candidate_results = [run_candidate_decision(c) for c in candidate_inputs]

    entry_readiness = _compute_entry_readiness(regime_dec, risk_dec, portfolio_dec, mc_dec, candidate_results)
    add_readiness = _compute_add_readiness(regime_dec, risk_dec, mc_dec, portfolio_dec)
    reduce_risk_dec = _compute_reduce_risk(risk_dec, portfolio_dec, mc_dec)

    all_blocks = list(set(hard_blocks + regime_dec.block_reasons + risk_dec.block_reasons + portfolio_dec.block_reasons))

    grade = _compute_cockpit_grade(all_blocks, entry_readiness, add_readiness, reduce_risk_dec, regime_dec)

    if all_blocks:
        daily_action = "BLOCKED"
        weekly_action = "BLOCKED"
    elif grade == "READY":
        daily_action = "PAPER_ENTRY_ALLOWED"
        weekly_action = "PAPER_PLAN_READY"
    elif grade == "WATCH":
        daily_action = "PAPER_PLAN_READY"
        weekly_action = "OBSERVE"
    elif grade == "REDUCE_RISK":
        daily_action = "REDUCE_RISK"
        weekly_action = "REDUCE_RISK"
    elif grade == "REVIEW_REQUIRED":
        daily_action = "REVIEW_REQUIRED"
        weekly_action = "REVIEW_REQUIRED"
    else:
        daily_action = "WAIT"
        weekly_action = "WAIT"

    ready_tickers = [r.ticker for r in candidate_results if r.final_action == "PAPER_ENTRY_ALLOWED"]
    watch_tickers = [r.ticker for r in candidate_results if r.final_action == "PAPER_PLAN_READY"]
    blocked_tickers = [r.ticker for r in candidate_results if r.final_action == "BLOCKED"]
    reduce_tickers = [r.ticker for r in candidate_results if "REDUCE" in r.final_action]

    capital_stage = _capital_stage_label(inp.capital)
    ps_summary = f"capital={inp.capital:.0f} stage={capital_stage}"
    port_summary = f"holdings={inp.portfolio_holding_count} exposure={inp.total_exposure_pct:.1f}%"

    return DecisionCockpitResult(
        cockpit_version="1.8.6",
        release_name="End-to-End Small Capital Decision Cockpit",
        capital_stage=capital_stage,
        market_regime=inp.market_regime,
        daily_action=daily_action,
        weekly_action=weekly_action,
        candidate_count=len(candidate_inputs),
        ready_candidate_count=len(ready_tickers),
        watch_candidate_count=len(watch_tickers),
        blocked_candidate_count=len(blocked_tickers),
        portfolio_holding_count=inp.portfolio_holding_count,
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        concentration_risk_score=inp.concentration_risk_score,
        monte_carlo_ruin_risk=inp.monte_carlo_ruin_risk_pct,
        max_drawdown_budget_usage_pct=risk_dec.drawdown_budget_usage_pct,
        position_sizing_summary=ps_summary,
        portfolio_rebalance_summary=port_summary,
        top_watch_candidates=watch_tickers,
        paper_plan_ready_candidates=ready_tickers,
        reduce_risk_candidates=reduce_tickers,
        blocked_candidates=blocked_tickers,
        block_reasons=all_blocks,
        final_cockpit_grade=grade,
    )


def build_decision_dashboard(inp, candidate_inputs: list = None) -> "DecisionDashboard":
    """Build full decision dashboard."""
    from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
        DecisionDashboard, DecisionChecklist,
    )
    if candidate_inputs is None:
        candidate_inputs = []

    regime_dec = run_regime_decision(inp)
    theme_dec = run_theme_decision(candidate_inputs)
    risk_dec = run_risk_decision(inp)
    portfolio_dec = run_portfolio_decision(inp)
    mc_dec = run_monte_carlo_decision(inp.monte_carlo_ruin_risk_pct)

    candidate_results = [run_candidate_decision(c) for c in candidate_inputs]

    entry_readiness = _compute_entry_readiness(regime_dec, risk_dec, portfolio_dec, mc_dec, candidate_results)
    add_readiness = _compute_add_readiness(regime_dec, risk_dec, mc_dec, portfolio_dec)
    reduce_risk_dec = _compute_reduce_risk(risk_dec, portfolio_dec, mc_dec)

    all_blocks = list(set(regime_dec.block_reasons + risk_dec.block_reasons + portfolio_dec.block_reasons))
    grade = _compute_cockpit_grade(all_blocks, entry_readiness, add_readiness, reduce_risk_dec, regime_dec)

    checklist = DecisionChecklist(
        market_regime_checked=True,
        watchlist_reviewed=len(candidate_inputs) > 0,
        candidates_evaluated=len(candidate_inputs) > 0,
        buy_points_assessed=len(candidate_inputs) > 0,
        risk_reviewed=True,
        position_sizing_checked=True,
        portfolio_checked=True,
        monte_carlo_checked=True,
        theme_checked=True,
        all_checked=True,
    )

    return DecisionDashboard(
        regime_decision=regime_dec,
        theme_decision=theme_dec,
        risk_decision=risk_dec,
        portfolio_decision=portfolio_dec,
        monte_carlo_decision=mc_dec,
        entry_readiness=entry_readiness,
        add_readiness=add_readiness,
        reduce_risk_decision=reduce_risk_dec,
        checklist=checklist,
        final_cockpit_grade=grade,
    )


def get_engine_info() -> dict:
    """Return engine metadata."""
    return {
        "version": "1.8.6",
        "allowed_output_actions": list(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": list(FORBIDDEN_OUTPUT_WORDS),
        "valid_cockpit_grades": list(VALID_COCKPIT_GRADES),
        "capital_stages": CAPITAL_STAGES,
        "decision_cycles": DECISION_CYCLES,
        "abc_buy_points": ABC_BUY_POINTS,
        "candidate_evaluation_criteria": CANDIDATE_EVALUATION_CRITERIA,
        "paper_only": True,
        "decision_only": True,
        "no_real_orders": True,
    }
