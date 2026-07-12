"""
paper_trading/small_capital_strategy/position_sizing_engine_v184.py
Position sizing engine for Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "ALLOCATION_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_FINAL_GRADES = frozenset({
    "SAFE", "ACCEPTABLE", "CAUTION", "HIGH_RISK", "BLOCKED",
})

CAPITAL_STAGES = [300000, 500000, 1000000, 3000000]

ABC_SIZING_RULES = {
    "A_10MA_PULLBACK":  {"initial_pct": 40.0, "add1_pct": 30.0, "add2_pct": 30.0},
    "B_BREAKOUT":       {"initial_pct": 50.0, "add1_pct": 25.0, "add2_pct": 25.0},
    "C_20MA_RECLAIM":   {"initial_pct": 30.0, "add1_pct": 30.0, "add2_pct": 40.0},
}

SIZING_METHODS = [
    "fixed_risk",
    "volatility_adjusted",
    "stop_distance",
    "drawdown_aware",
    "monte_carlo_ruin_adjusted",
    "concentration_risk_adjusted",
    "capital_stage_adjusted",
    "abc_buy_point_staged",
    "add_position",
    "reduce_risk",
]


def validate_action(action: str) -> bool:
    """Return True if action is in ALLOWED_OUTPUT_ACTIONS."""
    return action in ALLOWED_OUTPUT_ACTIONS


def validate_grade(grade: str) -> bool:
    """Return True if grade is in VALID_FINAL_GRADES."""
    return grade in VALID_FINAL_GRADES


def _check_hard_blocks(ps_input) -> list:
    """Return list of block reasons. Empty list means no blocks."""
    blocks = []
    if not ps_input.has_stop_loss:
        blocks.append("missing_stop_loss")
    if ps_input.stop_loss_distance_pct <= 0:
        blocks.append("stop_loss_distance_pct_zero_or_negative")
    if ps_input.per_trade_risk_pct > 5.0:
        blocks.append("per_trade_risk_pct_too_high")
    if ps_input.max_single_position_pct > 50.0:
        blocks.append("single_position_exposure_too_high")
    if ps_input.max_total_equity_exposure_pct > 95.0:
        blocks.append("total_exposure_too_high")
    if ps_input.cash_reserve_pct < 5.0:
        blocks.append("cash_reserve_too_low")
    if ps_input.max_drawdown_budget_pct <= 0 or ps_input.current_drawdown_pct >= ps_input.max_drawdown_budget_pct:
        blocks.append("drawdown_budget_exceeded")
    if ps_input.ruin_risk_pct > 20.0:
        blocks.append("monte_carlo_ruin_probability_too_high")
    if ps_input.market_regime == "BLOCKED":
        blocks.append("market_regime_blocked")
    return blocks


def _grade_from_metrics(blocks: list, concentration_score: float,
                        drawdown_usage: float, ruin_risk_pct: float) -> str:
    """Derive final position grade."""
    if blocks:
        return "BLOCKED"
    if ruin_risk_pct > 10.0 or drawdown_usage > 85.0 or concentration_score > 80.0:
        return "HIGH_RISK"
    if ruin_risk_pct > 5.0 or drawdown_usage > 60.0 or concentration_score > 60.0:
        return "CAUTION"
    if ruin_risk_pct > 2.0 or drawdown_usage > 40.0 or concentration_score > 40.0:
        return "ACCEPTABLE"
    return "SAFE"


def run_position_sizing(ps_input) -> "PositionSizingResult":
    """Run position sizing engine. Returns PositionSizingResult."""
    from paper_trading.small_capital_strategy.position_sizing_models_v184 import PositionSizingResult

    blocks = _check_hard_blocks(ps_input)

    capital = ps_input.capital
    per_trade_risk_pct = ps_input.per_trade_risk_pct
    stop_loss_pct = ps_input.stop_loss_distance_pct

    per_trade_risk_amount = capital * (per_trade_risk_pct / 100.0)
    max_loss_allowed = per_trade_risk_amount

    # Fixed risk sizing: position_value = risk_amount / stop_loss_pct
    if stop_loss_pct > 0:
        suggested_position_value = per_trade_risk_amount / (stop_loss_pct / 100.0)
    else:
        suggested_position_value = 0.0

    # Cap by single position limit
    max_single_value = capital * (ps_input.max_single_position_pct / 100.0)
    suggested_position_value = min(suggested_position_value, max_single_value)

    # Ruin risk adjustment
    ruin_risk_adjustment = 1.0
    if ps_input.ruin_risk_pct > 10.0:
        ruin_risk_adjustment = 0.5
    elif ps_input.ruin_risk_pct > 5.0:
        ruin_risk_adjustment = 0.7

    # Volatility adjustment
    if ps_input.volatility_pct > 30.0:
        ruin_risk_adjustment = min(ruin_risk_adjustment, 0.7)

    # Regime adjustment
    if ps_input.market_regime in ("WEAK", "RISK_OFF"):
        ruin_risk_adjustment = min(ruin_risk_adjustment, 0.8)

    suggested_position_value *= ruin_risk_adjustment

    # ABC buy point staged sizing
    abc_rules = ABC_SIZING_RULES.get(ps_input.abc_buy_point,
                                     ABC_SIZING_RULES["A_10MA_PULLBACK"])
    initial_entry_value = suggested_position_value * (abc_rules["initial_pct"] / 100.0)
    add_position_value = suggested_position_value * (abc_rules["add1_pct"] / 100.0)

    suggested_position_pct = (suggested_position_value / capital * 100.0) if capital > 0 else 0.0
    max_shares_estimate = suggested_position_value / 100.0  # assume price = 100

    cash_after_entry = capital - initial_entry_value
    cash_reserve_pct = ps_input.cash_reserve_pct
    total_exposure_pct = ps_input.current_exposure_pct + suggested_position_pct

    concentration_risk_score = min(100.0, suggested_position_pct * 2.0)

    drawdown_budget_usage_pct = 0.0
    if ps_input.max_drawdown_budget_pct > 0:
        drawdown_budget_usage_pct = (ps_input.current_drawdown_pct
                                     / ps_input.max_drawdown_budget_pct) * 100.0

    final_grade = _grade_from_metrics(blocks, concentration_risk_score,
                                      drawdown_budget_usage_pct, ps_input.ruin_risk_pct)

    if blocks:
        action = "BLOCKED"
    elif final_grade == "HIGH_RISK":
        action = "REVIEW_REQUIRED"
    elif final_grade == "CAUTION":
        action = "PAPER_PLAN_READY"
    else:
        action = "PAPER_ENTRY_ALLOWED"

    return PositionSizingResult(
        capital=capital,
        per_trade_risk_amount=round(per_trade_risk_amount, 2),
        max_loss_allowed=round(max_loss_allowed, 2),
        stop_loss_distance_pct=stop_loss_pct,
        suggested_position_value=round(suggested_position_value, 2),
        suggested_position_pct=round(suggested_position_pct, 4),
        max_shares_estimate=round(max_shares_estimate, 2),
        initial_entry_value=round(initial_entry_value, 2),
        add_position_value=round(add_position_value, 2),
        reduce_position_trigger="REDUCE_RISK",
        stop_loss_trigger="REVIEW_REQUIRED",
        cash_after_entry=round(cash_after_entry, 2),
        cash_reserve_pct=cash_reserve_pct,
        total_exposure_pct=round(total_exposure_pct, 4),
        concentration_risk_score=round(concentration_risk_score, 2),
        drawdown_budget_usage_pct=round(drawdown_budget_usage_pct, 2),
        ruin_risk_adjustment=round(ruin_risk_adjustment, 4),
        final_position_grade=final_grade,
        action=action,
    )


def build_position_sizing_dashboard(ps_input) -> "PositionSizingDashboard":
    """Build full position sizing dashboard."""
    from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
        PositionSizingDashboard, CapitalProfile, RiskBudget,
        DrawdownBudget, ConcentrationRiskReport, ExposureLimitReport, CashReservePlan,
        CapitalStagePlan,
    )
    result = run_position_sizing(ps_input)
    capital = ps_input.capital

    stage_label = "300K"
    if capital >= 3000000:
        stage_label = "3M"
    elif capital >= 1000000:
        stage_label = "1M"
    elif capital >= 500000:
        stage_label = "500K"

    capital_profile = CapitalProfile(capital=capital, capital_stage=stage_label)
    risk_budget = RiskBudget(
        per_trade_risk_pct=ps_input.per_trade_risk_pct,
        max_single_position_pct=ps_input.max_single_position_pct,
        max_total_equity_exposure_pct=ps_input.max_total_equity_exposure_pct,
        cash_reserve_pct=ps_input.cash_reserve_pct,
        max_concurrent_positions=ps_input.max_concurrent_positions,
        max_drawdown_budget_pct=ps_input.max_drawdown_budget_pct,
        stop_loss_distance_pct=ps_input.stop_loss_distance_pct,
    )
    drawdown_budget = DrawdownBudget(
        max_drawdown_budget_pct=ps_input.max_drawdown_budget_pct,
        current_drawdown_pct=ps_input.current_drawdown_pct,
        remaining_drawdown_pct=max(0.0, ps_input.max_drawdown_budget_pct
                                   - ps_input.current_drawdown_pct),
        drawdown_budget_usage_pct=result.drawdown_budget_usage_pct,
        budget_exhausted=result.drawdown_budget_usage_pct >= 100.0,
    )
    concentration_report = ConcentrationRiskReport(
        single_position_pct=result.suggested_position_pct,
        max_allowed_single_pct=ps_input.max_single_position_pct,
        concentration_risk_score=result.concentration_risk_score,
        risk_level=result.final_position_grade,
    )
    exposure_report = ExposureLimitReport(
        total_exposure_pct=result.total_exposure_pct,
        max_total_exposure_pct=ps_input.max_total_equity_exposure_pct,
        cash_reserve_pct=ps_input.cash_reserve_pct,
        cash_reserve_amount=capital * (ps_input.cash_reserve_pct / 100.0),
        exposure_ok=result.total_exposure_pct <= ps_input.max_total_equity_exposure_pct,
        cash_reserve_ok=True,
        action=result.action,
    )
    cash_reserve_plan = CashReservePlan(
        capital=capital,
        cash_reserve_pct=ps_input.cash_reserve_pct,
        cash_reserve_amount=capital * (ps_input.cash_reserve_pct / 100.0),
        deployable_capital=capital * ((100.0 - ps_input.cash_reserve_pct) / 100.0),
    )
    capital_stage_plan = CapitalStagePlan(
        capital=capital,
        stage_label=stage_label,
        max_per_trade_risk_amount=result.per_trade_risk_amount,
        max_position_value=capital * (ps_input.max_single_position_pct / 100.0),
        suggested_max_positions=ps_input.max_concurrent_positions,
        recommended_risk_pct=ps_input.per_trade_risk_pct,
    )
    return PositionSizingDashboard(
        capital_profile=capital_profile,
        risk_budget=risk_budget,
        sizing_result=result,
        drawdown_budget=drawdown_budget,
        concentration_report=concentration_report,
        exposure_report=exposure_report,
        cash_reserve_plan=cash_reserve_plan,
        capital_stage_plan=capital_stage_plan,
    )


def get_engine_info() -> dict:
    """Return engine metadata."""
    return {
        "version": "1.8.4",
        "allowed_output_actions": list(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": list(FORBIDDEN_OUTPUT_WORDS),
        "valid_final_grades": list(VALID_FINAL_GRADES),
        "capital_stages": CAPITAL_STAGES,
        "sizing_methods": SIZING_METHODS,
        "abc_sizing_rules": ABC_SIZING_RULES,
        "paper_only": True,
        "allocation_only": True,
        "no_real_orders": True,
    }
