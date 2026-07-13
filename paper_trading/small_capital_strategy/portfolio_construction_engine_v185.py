"""
paper_trading/small_capital_strategy/portfolio_construction_engine_v185.py
Portfolio construction engine for Portfolio Construction & Rebalancing Lab v1.8.5.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Portfolio Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict

ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "ALLOCATION_ONLY", "PORTFOLIO_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_FINAL_GRADES = frozenset({
    "BALANCED", "ACCEPTABLE", "CONCENTRATED", "OVEREXPOSED", "HIGH_RISK", "BLOCKED",
})

CAPITAL_STAGES = [300000, 500000, 1000000, 3000000]

MAX_POSITIONS_BY_STAGE = {
    300000: 3,
    500000: 4,
    1000000: 5,
    3000000: 6,
}

WEIGHTING_METHODS = [
    "equal_weight",
    "risk_budget_weight",
    "conviction_weight",
    "volatility_adjusted_weight",
    "position_sizing_adjusted_weight",
    "monte_carlo_ruin_risk_adjusted_weight",
    "theme_exposure_adjusted_weight",
    "market_regime_adjusted_exposure",
    "abc_staged_portfolio",
    "keep_reduce_replace_decision",
]

KEEP_REPLACE_ACTIONS = [
    "KEEP", "REDUCE", "REPLACE", "WATCH", "WAIT", "OBSERVE",
    "REDUCE_RISK", "REVIEW_REQUIRED", "NO_TRADE", "BLOCKED",
]


def validate_action(action: str) -> bool:
    """Return True if action is in ALLOWED_OUTPUT_ACTIONS."""
    return action in ALLOWED_OUTPUT_ACTIONS


def validate_grade(grade: str) -> bool:
    """Return True if grade is in VALID_FINAL_GRADES."""
    return grade in VALID_FINAL_GRADES


def _compute_sector_weights(holdings) -> Dict[str, float]:
    """Compute sector exposure weights from holdings."""
    total_value = sum(h.value for h in holdings) if holdings else 0.0
    sector_weights: Dict[str, float] = {}
    for h in holdings:
        sector = h.sector or "UNKNOWN"
        w = (h.value / total_value * 100.0) if total_value > 0 else 0.0
        sector_weights[sector] = sector_weights.get(sector, 0.0) + w
    return sector_weights


def _compute_theme_weights(holdings) -> Dict[str, float]:
    """Compute theme exposure weights from holdings."""
    total_value = sum(h.value for h in holdings) if holdings else 0.0
    theme_weights: Dict[str, float] = {}
    for h in holdings:
        theme = h.theme or "UNKNOWN"
        w = (h.value / total_value * 100.0) if total_value > 0 else 0.0
        theme_weights[theme] = theme_weights.get(theme, 0.0) + w
    return theme_weights


def _compute_equal_weights(n: int) -> List[float]:
    """Return equal weight per position as percentage."""
    if n <= 0:
        return []
    w = 100.0 / n
    return [w] * n


def _compute_conviction_weights(holdings) -> List[float]:
    """Return conviction-weighted weights."""
    scores = [max(h.conviction_score, 0.01) for h in holdings]
    total = sum(scores)
    if total <= 0:
        return _compute_equal_weights(len(holdings))
    return [(s / total) * 100.0 for s in scores]


def _compute_volatility_adjusted_weights(holdings) -> List[float]:
    """Return inverse-volatility weights."""
    inv_vols = [1.0 / max(h.volatility_pct, 0.01) for h in holdings]
    total = sum(inv_vols)
    if total <= 0:
        return _compute_equal_weights(len(holdings))
    return [(iv / total) * 100.0 for iv in inv_vols]


def _herfindahl_index(weights_pct: List[float]) -> float:
    """Compute Herfindahl index (sum of squared weight fractions)."""
    return sum((w / 100.0) ** 2 for w in weights_pct)


def _diversification_score(hhi: float, n: int) -> float:
    """Map HHI and position count to a 0–100 diversification score (higher = more diversified)."""
    if n <= 0:
        return 0.0
    min_hhi = 1.0 / n
    max_hhi = 1.0
    if max_hhi == min_hhi:
        return 100.0
    score = (1.0 - (hhi - min_hhi) / (max_hhi - min_hhi)) * 100.0
    return round(max(0.0, min(100.0, score)), 2)


def _check_hard_blocks(inp) -> list:
    """Return list of block reasons."""
    blocks = []
    if inp.market_regime == "BLOCKED":
        blocks.append("market_regime_blocked")
    if inp.max_total_exposure_pct > 95.0:
        blocks.append("total_exposure_too_high")
    if inp.max_single_position_pct > 60.0:
        blocks.append("single_position_exposure_too_high")
    if inp.max_sector_exposure_pct > 80.0:
        blocks.append("sector_exposure_too_high")
    if inp.max_theme_exposure_pct > 80.0:
        blocks.append("theme_exposure_too_high")
    if inp.min_cash_reserve_pct < 5.0:
        blocks.append("cash_reserve_too_low")
    if inp.monte_carlo_ruin_risk_pct > 20.0:
        blocks.append("monte_carlo_ruin_probability_too_high")
    if inp.max_drawdown_budget_pct <= 0:
        blocks.append("drawdown_budget_exceeded")
    return blocks


def _grade_portfolio(blocks, total_exposure_pct, max_total_exposure_pct,
                     single_max_pct, max_single_pct,
                     concentration_score, diversification_score_val,
                     overexposed_sectors, overexposed_themes,
                     correlation_risk_score) -> str:
    """Derive final portfolio grade."""
    if blocks:
        return "BLOCKED"
    if overexposed_sectors or overexposed_themes:
        return "OVEREXPOSED"
    if total_exposure_pct > max_total_exposure_pct:
        return "OVEREXPOSED"
    if single_max_pct > max_single_pct:
        return "CONCENTRATED"
    if concentration_score > 70.0 or correlation_risk_score > 70.0:
        return "CONCENTRATED"
    if diversification_score_val < 30.0 or concentration_score > 50.0:
        return "HIGH_RISK"
    if diversification_score_val < 55.0 or concentration_score > 35.0:
        return "ACCEPTABLE"
    return "BALANCED"


def _keep_or_replace_decision(holding) -> str:
    """Evaluate a holding for keep/reduce/replace."""
    if not holding.above_20ma and not holding.above_10ma:
        return "REPLACE"
    if not holding.above_10ma:
        return "REDUCE"
    if holding.unrealized_pnl_pct < -8.0:
        return "REVIEW_REQUIRED"
    return "KEEP"


def run_portfolio_construction(inp) -> "PortfolioConstructionResult":
    """Run portfolio construction engine. Returns PortfolioConstructionResult."""
    from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
        PortfolioConstructionResult,
    )

    blocks = _check_hard_blocks(inp)

    holdings = inp.holdings or []
    n = len(holdings)
    capital = inp.capital

    # Compute weights by method
    if inp.weighting_method == "conviction_weight" and holdings:
        weights = _compute_conviction_weights(holdings)
    elif inp.weighting_method == "volatility_adjusted_weight" and holdings:
        weights = _compute_volatility_adjusted_weights(holdings)
    else:
        weights = _compute_equal_weights(n) if n > 0 else []

    # Monte Carlo ruin risk adjustment
    mc_adjustment = 1.0
    if inp.monte_carlo_ruin_risk_pct > 10.0:
        mc_adjustment = 0.5
    elif inp.monte_carlo_ruin_risk_pct > 5.0:
        mc_adjustment = 0.7

    # Market regime adjustment
    if inp.market_regime in ("WEAK", "RISK_OFF"):
        mc_adjustment = min(mc_adjustment, 0.8)

    total_exposure_pct = sum(weights) * mc_adjustment if weights else 0.0
    total_exposure_pct = min(total_exposure_pct, inp.max_total_exposure_pct)
    cash_reserve_pct = max(inp.min_cash_reserve_pct, 100.0 - total_exposure_pct)
    cash_reserve_amount = capital * (cash_reserve_pct / 100.0)

    single_max_pct = max(weights) if weights else 0.0

    # Sector / theme exposure
    sector_weights = _compute_sector_weights(holdings)
    theme_weights = _compute_theme_weights(holdings)
    overexposed_sectors = [s for s, w in sector_weights.items() if w > inp.max_sector_exposure_pct]
    overexposed_themes = [t for t, w in theme_weights.items() if w > inp.max_theme_exposure_pct]

    # Correlation risk: same-theme holdings treated as correlated
    theme_exposure_max = max(theme_weights.values()) if theme_weights else 0.0
    correlation_risk_score = min(100.0, theme_exposure_max)

    # HHI / diversification
    if n == 0:
        hhi = 0.0
        div_score = 100.0
        concentration_risk_score = 0.0
    else:
        hhi = _herfindahl_index(weights) if weights else 1.0
        div_score = _diversification_score(hhi, n)
        concentration_risk_score = min(100.0, (1.0 - div_score / 100.0) * 100.0)

    # Keep/reduce/replace decisions
    keep_list, reduce_list, replace_list, watch_list = [], [], [], []
    for h in holdings:
        decision = _keep_or_replace_decision(h)
        if decision == "KEEP":
            keep_list.append(h.ticker)
        elif decision in ("REDUCE", "REDUCE_RISK"):
            reduce_list.append(h.ticker)
        elif decision == "REPLACE":
            replace_list.append(h.ticker)
        else:
            watch_list.append(h.ticker)

    # Blocked candidates (regime blocked or theme overexposed)
    blocked_candidates = []
    for c in (inp.candidates or []):
        if not c.market_regime_compatible or inp.market_regime == "BLOCKED":
            blocked_candidates.append(c.ticker)
        elif c.theme in overexposed_themes:
            blocked_candidates.append(c.ticker)

    # Rebalance actions (stub — detailed in rebalance engine)
    rebalance_actions = []
    for h in holdings:
        drift = abs(h.weight_pct - (100.0 / n if n > 0 else 0.0))
        if drift > inp.rebalance_threshold_pct:
            rebalance_actions.append(f"REBALANCE:{h.ticker}:drift={drift:.1f}%")

    grade = _grade_portfolio(
        blocks, total_exposure_pct, inp.max_total_exposure_pct,
        single_max_pct, inp.max_single_position_pct,
        concentration_risk_score, div_score,
        overexposed_sectors, overexposed_themes,
        correlation_risk_score,
    )

    if blocks:
        action = "BLOCKED"
    elif grade == "OVEREXPOSED":
        action = "REDUCE_RISK"
    elif grade in ("CONCENTRATED", "HIGH_RISK"):
        action = "REVIEW_REQUIRED"
    elif grade == "ACCEPTABLE":
        action = "PAPER_PLAN_READY"
    else:
        action = "PORTFOLIO_ONLY"

    drawdown_usage = 0.0
    if inp.max_drawdown_budget_pct > 0:
        drawdown_usage = min(100.0, (1.0 - div_score / 100.0) * 50.0)

    return PortfolioConstructionResult(
        capital=capital,
        holding_count=n,
        max_positions=inp.max_positions,
        total_exposure_pct=round(total_exposure_pct, 4),
        cash_reserve_pct=round(cash_reserve_pct, 4),
        cash_reserve_amount=round(cash_reserve_amount, 2),
        single_position_max_pct=round(single_max_pct, 4),
        concentration_risk_score=round(concentration_risk_score, 2),
        diversification_score=round(div_score, 2),
        correlation_risk_score=round(correlation_risk_score, 2),
        drawdown_budget_usage_pct=round(drawdown_usage, 2),
        monte_carlo_ruin_risk_adjustment=round(mc_adjustment, 4),
        suggested_keep_list=keep_list,
        suggested_reduce_list=reduce_list,
        suggested_replace_list=replace_list,
        suggested_watch_list=watch_list,
        blocked_candidates=blocked_candidates,
        rebalance_actions=rebalance_actions,
        final_portfolio_grade=grade,
        action=action,
    )


def run_rebalance(rebalance_input) -> "RebalancePlan":
    """Run rebalance engine. Returns RebalancePlan."""
    from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
        RebalancePlan, RebalanceAction,
    )
    holdings = rebalance_input.holdings or []
    target_weights = rebalance_input.target_weights or {}
    n = len(holdings)
    default_target = 100.0 / n if n > 0 else 0.0

    actions = []
    total_drift = 0.0
    for h in holdings:
        target = target_weights.get(h.ticker, default_target)
        drift = h.weight_pct - target
        total_drift += abs(drift)
        if abs(drift) > rebalance_input.rebalance_threshold_pct:
            act_type = "REDUCE_RISK" if drift > 0 else "PAPER_PLAN_READY"
        else:
            act_type = "OBSERVE"
        actions.append(RebalanceAction(
            ticker=h.ticker,
            current_weight_pct=h.weight_pct,
            target_weight_pct=target,
            drift_pct=round(drift, 4),
            action_type=act_type,
        ))

    rebalance_needed = total_drift > rebalance_input.rebalance_threshold_pct
    return RebalancePlan(
        actions=actions,
        total_drift_pct=round(total_drift, 4),
        rebalance_needed=rebalance_needed,
        action="REVIEW_REQUIRED" if rebalance_needed else "OBSERVE",
    )


def build_portfolio_dashboard(inp) -> "PortfolioDashboard":
    """Build full portfolio dashboard."""
    from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
        PortfolioDashboard, PortfolioProfile, PortfolioExposureReport,
        SectorExposureReport, ThemeExposureReport, CorrelationRiskReport,
        DiversificationScore, RebalanceInput,
    )

    result = run_portfolio_construction(inp)
    holdings = inp.holdings or []

    stage_label = "300K"
    if inp.capital >= 3000000:
        stage_label = "3M"
    elif inp.capital >= 1000000:
        stage_label = "1M"
    elif inp.capital >= 500000:
        stage_label = "500K"

    profile = PortfolioProfile(
        capital=inp.capital,
        capital_stage=stage_label,
        max_positions=inp.max_positions,
        max_single_position_pct=inp.max_single_position_pct,
        max_total_exposure_pct=inp.max_total_exposure_pct,
        min_cash_reserve_pct=inp.min_cash_reserve_pct,
    )
    exposure_report = PortfolioExposureReport(
        total_exposure_pct=result.total_exposure_pct,
        max_total_exposure_pct=inp.max_total_exposure_pct,
        cash_reserve_pct=result.cash_reserve_pct,
        single_position_max_pct=result.single_position_max_pct,
        exposure_ok=result.total_exposure_pct <= inp.max_total_exposure_pct,
        action=result.action,
    )
    sector_weights = _compute_sector_weights(holdings)
    sector_report = SectorExposureReport(
        sector_weights=sector_weights,
        max_sector_exposure_pct=inp.max_sector_exposure_pct,
        overexposed_sectors=[s for s, w in sector_weights.items() if w > inp.max_sector_exposure_pct],
        sector_ok=all(w <= inp.max_sector_exposure_pct for w in sector_weights.values()),
    )
    theme_weights = _compute_theme_weights(holdings)
    theme_report = ThemeExposureReport(
        theme_weights=theme_weights,
        max_theme_exposure_pct=inp.max_theme_exposure_pct,
        overexposed_themes=[t for t, w in theme_weights.items() if w > inp.max_theme_exposure_pct],
        theme_ok=all(w <= inp.max_theme_exposure_pct for w in theme_weights.values()),
    )
    correlation_report = CorrelationRiskReport(
        correlation_buckets=theme_weights,
        max_correlation_bucket_pct=inp.max_correlation_bucket_pct,
        high_correlation_pairs=[],
        correlation_risk_score=result.correlation_risk_score,
        correlation_ok=result.correlation_risk_score <= inp.max_correlation_bucket_pct,
    )
    n = len(holdings)
    weights = _compute_equal_weights(n)
    hhi = _herfindahl_index(weights) if weights else 1.0
    div_score_val = _diversification_score(hhi, n)
    div_grade = "ACCEPTABLE"
    if div_score_val >= 70:
        div_grade = "BALANCED"
    elif div_score_val < 40:
        div_grade = "CONCENTRATED"
    div_score = DiversificationScore(
        score=div_score_val,
        sector_count=len(sector_weights),
        theme_count=len(theme_weights),
        position_count=n,
        herfindahl_index=round(hhi, 6),
        grade=div_grade,
    )
    ri = RebalanceInput(
        capital=inp.capital,
        holdings=holdings,
        rebalance_threshold_pct=inp.rebalance_threshold_pct,
        market_regime=inp.market_regime,
    )
    rebalance_plan = run_rebalance(ri)

    return PortfolioDashboard(
        profile=profile,
        construction_result=result,
        exposure_report=exposure_report,
        sector_report=sector_report,
        theme_report=theme_report,
        correlation_report=correlation_report,
        diversification_score=div_score,
        rebalance_plan=rebalance_plan,
    )


def get_engine_info() -> dict:
    """Return engine metadata."""
    return {
        "version": "1.8.5",
        "allowed_output_actions": list(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": list(FORBIDDEN_OUTPUT_WORDS),
        "valid_final_grades": list(VALID_FINAL_GRADES),
        "capital_stages": CAPITAL_STAGES,
        "weighting_methods": WEIGHTING_METHODS,
        "keep_replace_actions": KEEP_REPLACE_ACTIONS,
        "paper_only": True,
        "portfolio_only": True,
        "no_real_orders": True,
    }
