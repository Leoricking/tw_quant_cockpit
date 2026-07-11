"""
paper_trading/small_capital_strategy/simulation_stress_engine_v181.py
Stress Test Engine for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
10 stress test types. Deterministic. Research-only.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA = "181"

# Stress test type registry
STRESS_TEST_TYPES = [
    "MARKET_CRASH",
    "THEME_COLLAPSE",
    "LIQUIDITY_SHRINK",
    "VOLATILITY_SPIKE",
    "LOSING_STREAK_3",
    "LOSING_STREAK_5",
    "LOSING_STREAK_8",
    "GAP_DOWN_STOP_LOSS",
    "OVERTRADING_INJECTION",
    "NO_STOP_LOSS_INJECTION",
    "OVERSIZED_POSITION_INJECTION",
    "RISK_OFF_REGIME_SHIFT",
]


def _run_market_crash(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Market crash: -25% sudden drawdown."""
    crash_loss = initial_capital * 0.25
    final = initial_capital - crash_loss
    return {
        "survived": final > initial_capital * 0.5,
        "total_return_pct": round(-25.0, 4),
        "max_drawdown_pct": round(25.0, 4),
        "final_capital": round(final, 2),
        "action": "OBSERVE",
        "notes": "Market crash: -25% shock applied",
    }


def _run_theme_collapse(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Theme collapse: theme drops to EXCLUDED, all positions closed."""
    close_loss = initial_capital * risk_pct / 100.0 * 3  # 3 open positions
    final = initial_capital - close_loss
    return {
        "survived": final > initial_capital * 0.6,
        "total_return_pct": round(-close_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(close_loss / initial_capital * 100, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "BLOCKED",
        "notes": "Theme collapsed to EXCLUDED; positions forced closed",
    }


def _run_liquidity_shrink(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Liquidity shrink: position sizes halved, slippage increased."""
    slippage_loss = initial_capital * 0.015
    final = initial_capital - slippage_loss
    return {
        "survived": True,
        "total_return_pct": round(-slippage_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(1.5, 4),
        "final_capital": round(final, 2),
        "action": "REDUCE_RISK",
        "notes": "Liquidity shrink: position sizes halved, 1.5% slippage loss",
    }


def _run_volatility_spike(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Volatility spike: stops triggered early, wider spreads."""
    vol_loss = initial_capital * risk_pct / 100.0 * 1.5 * 2
    final = initial_capital - vol_loss
    return {
        "survived": final > initial_capital * 0.7,
        "total_return_pct": round(-vol_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(vol_loss / initial_capital * 100, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "REDUCE_RISK",
        "notes": "Volatility spike: stops triggered early on 2 positions",
    }


def _run_losing_streak(
    initial_capital: float, risk_pct: float, streak_length: int
) -> Dict[str, Any]:
    """Consecutive losing streak of N trades."""
    loss_per = initial_capital * risk_pct / 100.0
    total_loss = loss_per * streak_length
    final = initial_capital - total_loss
    dd = total_loss / initial_capital * 100.0
    return {
        "survived": final > initial_capital * 0.5,
        "total_return_pct": round(-dd, 4),
        "max_drawdown_pct": round(dd, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "REVIEW_REQUIRED",
        "notes": f"Losing streak of {streak_length} consecutive losses",
    }


def _run_gap_down_stop_loss(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Gap-down: price gaps below stop loss, worse fill."""
    gap_loss = initial_capital * risk_pct / 100.0 * 2.5
    final = initial_capital - gap_loss
    return {
        "survived": final > initial_capital * 0.6,
        "total_return_pct": round(-gap_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(gap_loss / initial_capital * 100, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "REVIEW_REQUIRED",
        "notes": "Gap-down: stop loss filled at -2.5R instead of -1R",
    }


def _run_overtrading_injection(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Overtrading injection: 3x normal trade frequency, lower win rate."""
    extra_loss = initial_capital * risk_pct / 100.0 * 4
    final = initial_capital - extra_loss
    return {
        "survived": final > initial_capital * 0.7,
        "total_return_pct": round(-extra_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(extra_loss / initial_capital * 100, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "REDUCE_RISK",
        "notes": "Overtrading: 3x frequency, 4R extra loss from churn",
    }


def _run_no_stop_loss_injection(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Missing stop loss: catastrophic loss on one trade."""
    catastrophic_loss = initial_capital * 0.12
    final = initial_capital - catastrophic_loss
    return {
        "survived": False,
        "total_return_pct": round(-12.0, 4),
        "max_drawdown_pct": round(12.0, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "BLOCKED",
        "notes": "Missing stop loss: -12% single trade catastrophic loss",
    }


def _run_oversized_position_injection(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Oversized position: 3x normal size on a losing trade."""
    oversized_loss = initial_capital * risk_pct / 100.0 * 3
    final = initial_capital - oversized_loss
    return {
        "survived": final > initial_capital * 0.7,
        "total_return_pct": round(-oversized_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(oversized_loss / initial_capital * 100, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "REDUCE_RISK",
        "notes": "Oversized position: 3x normal size, 3R loss",
    }


def _run_risk_off_regime_shift(
    initial_capital: float, risk_pct: float
) -> Dict[str, Any]:
    """Sudden shift to RISK_OFF regime: all paper plans blocked."""
    transition_loss = initial_capital * 0.08
    final = initial_capital - transition_loss
    return {
        "survived": True,
        "total_return_pct": round(-transition_loss / initial_capital * 100, 4),
        "max_drawdown_pct": round(8.0, 4),
        "final_capital": round(max(final, 0.0), 2),
        "action": "BLOCKED",
        "notes": "RISK_OFF shift: all positions reduced, -8% transition loss",
    }


def run_stress_test(
    shock_type: str,
    initial_capital: float = 300000.0,
    risk_pct: float = 1.0,
    scenario_id: str = "",
) -> "StressTestResult":
    """
    Run a single stress test by shock type.
    [!] Paper Only. Research Only. Simulate Only. Stress Test Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import StressTestResult

    _handlers = {
        "MARKET_CRASH":                  lambda: _run_market_crash(initial_capital, risk_pct),
        "THEME_COLLAPSE":                lambda: _run_theme_collapse(initial_capital, risk_pct),
        "LIQUIDITY_SHRINK":              lambda: _run_liquidity_shrink(initial_capital, risk_pct),
        "VOLATILITY_SPIKE":              lambda: _run_volatility_spike(initial_capital, risk_pct),
        "LOSING_STREAK_3":               lambda: _run_losing_streak(initial_capital, risk_pct, 3),
        "LOSING_STREAK_5":               lambda: _run_losing_streak(initial_capital, risk_pct, 5),
        "LOSING_STREAK_8":               lambda: _run_losing_streak(initial_capital, risk_pct, 8),
        "GAP_DOWN_STOP_LOSS":            lambda: _run_gap_down_stop_loss(initial_capital, risk_pct),
        "OVERTRADING_INJECTION":         lambda: _run_overtrading_injection(initial_capital, risk_pct),
        "NO_STOP_LOSS_INJECTION":        lambda: _run_no_stop_loss_injection(initial_capital, risk_pct),
        "OVERSIZED_POSITION_INJECTION":  lambda: _run_oversized_position_injection(initial_capital, risk_pct),
        "RISK_OFF_REGIME_SHIFT":         lambda: _run_risk_off_regime_shift(initial_capital, risk_pct),
    }

    handler = _handlers.get(shock_type)
    if handler is None:
        metrics = {"survived": False, "total_return_pct": 0.0, "max_drawdown_pct": 0.0,
                   "final_capital": initial_capital, "action": "BLOCKED",
                   "notes": f"Unknown shock type: {shock_type}"}
    else:
        metrics = handler()

    sid = scenario_id or f"STRESS181-{shock_type[:6]}"
    return StressTestResult(
        scenario_id=sid,
        shock_type=shock_type,
        survived=metrics["survived"],
        total_return_pct=metrics["total_return_pct"],
        max_drawdown_pct=metrics["max_drawdown_pct"],
        final_capital=metrics["final_capital"],
        action=metrics["action"],
        notes=metrics["notes"],
        schema_version=_SCHEMA,
        paper_only=True,
        research_only=True,
        simulate_only=True,
        stress_test_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def run_all_stress_tests(
    initial_capital: float = 300000.0,
    risk_pct: float = 1.0,
) -> List["StressTestResult"]:
    """
    Run all registered stress tests.
    [!] Paper Only. Research Only. Simulate Only. Stress Test Only. No Real Orders.
    """
    return [
        run_stress_test(st, initial_capital, risk_pct,
                        scenario_id=f"STRESS181-{i+1:03d}-{st[:8]}")
        for i, st in enumerate(STRESS_TEST_TYPES)
    ]


def get_stress_engine_info() -> Dict[str, Any]:
    """Return stress test engine metadata."""
    return {
        "schema": _SCHEMA,
        "stress_test_types": STRESS_TEST_TYPES,
        "stress_test_count": len(STRESS_TEST_TYPES),
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "stress_test_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


if __name__ == "__main__":
    results = run_all_stress_tests()
    survived = sum(1 for r in results if r.survived)
    print(f"[v1.8.1 Stress Engine] {len(results)} tests, {survived} survived")
    print("[OK] simulation_stress_engine_v181 ready")
