"""
paper_trading/small_capital_strategy/paper_simulation_engine_v180.py
Paper Simulation Engine for Paper Simulation & Performance Lab v1.8.0.
Deterministic. Research-only. No real orders.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA = "180"
_POLICY = "1.8.0-paper-simulation-performance-lab"

# ---------------------------------------------------------------------------
# Allowed output action literals — no forbidden words
# ---------------------------------------------------------------------------
ALLOWED_OUTPUT_ACTIONS = frozenset({
    "OBSERVE",
    "WAIT",
    "PAPER_PLAN_READY",
    "PAPER_ENTRY_ALLOWED",
    "PAPER_ADD_ALLOWED",
    "REDUCE_RISK",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "NO_TRADE",
    "RESEARCH_ONLY",
    "READ_REPORT",
    "SIMULATE_ONLY",
})

FORBIDDEN_OUTPUT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

# Hard-block conditions
_HARD_BLOCK_INTEGRATED = frozenset({"BLOCKED"})
_HARD_BLOCK_WATCHLIST  = frozenset({"EXCLUDED"})
_HARD_BLOCK_THEME      = frozenset({"EXCLUDED"})
_HARD_BLOCK_REGIME     = frozenset({"RISK_OFF"})
_HARD_BLOCK_RISK_DASH  = frozenset({"BLOCKED"})
_HARD_BLOCK_ABC        = frozenset({"BLOCKED"})
_HARD_BLOCK_MISTAKES   = frozenset({"no_stop_loss"})

_REDUCE_RISK_MISTAKES  = frozenset({"oversized_position", "overtrading", "moved_stop_loss"})
_REVIEW_MISTAKES       = frozenset({"revenge_trade"})

_ABC_READY             = frozenset({"A", "B", "C"})


def _determine_action(
    market_regime: str,
    theme_rank: str,
    watchlist_rank: str,
    abc_buy_point: str,
    mistake_taxonomy_effect: str,
    risk_dashboard_status: str,
    integrated_decision: str,
) -> str:
    """Core decision engine. Returns one of ALLOWED_OUTPUT_ACTIONS."""
    # 1. Hard-block checks (highest priority)
    if integrated_decision in _HARD_BLOCK_INTEGRATED:
        return "BLOCKED"
    if watchlist_rank in _HARD_BLOCK_WATCHLIST:
        return "BLOCKED"
    if theme_rank in _HARD_BLOCK_THEME:
        return "BLOCKED"
    if risk_dashboard_status in _HARD_BLOCK_RISK_DASH:
        return "BLOCKED"
    if abc_buy_point in _HARD_BLOCK_ABC:
        return "BLOCKED"
    if mistake_taxonomy_effect in _HARD_BLOCK_MISTAKES:
        return "BLOCKED"
    if market_regime in _HARD_BLOCK_REGIME:
        return "BLOCKED"

    # 2. Integrated decision pass-through for explicit states
    if integrated_decision == "PAPER_ADD_ALLOWED":
        return "PAPER_ADD_ALLOWED"
    if integrated_decision == "REDUCE_RISK":
        return "REDUCE_RISK"
    if integrated_decision == "REVIEW_REQUIRED":
        return "REVIEW_REQUIRED"
    if integrated_decision == "NO_TRADE":
        return "NO_TRADE"
    if integrated_decision == "OBSERVE":
        return "OBSERVE"
    if integrated_decision == "WAIT":
        return "WAIT"

    # 3. Mistake effect downgrades
    if mistake_taxonomy_effect in _REDUCE_RISK_MISTAKES:
        return "REDUCE_RISK"
    if mistake_taxonomy_effect in _REVIEW_MISTAKES:
        return "REVIEW_REQUIRED"

    # 4. Risk dashboard warning
    if risk_dashboard_status == "WARNING":
        return "REVIEW_REQUIRED"

    # 5. ABC not ready / not in tradeable set
    if abc_buy_point == "NOT_READY":
        return "WAIT"

    # 6. Market regime conditions
    if market_regime == "BEAR":
        return "OBSERVE"
    if market_regime == "UNKNOWN":
        return "OBSERVE"

    # 7. Theme / watchlist rank checks
    if theme_rank in ("WEAK", "WATCH"):
        return "WAIT"
    if watchlist_rank in ("TRAINING",):
        return "WAIT"
    if watchlist_rank in ("SECOND_WAVE",):
        if market_regime == "RANGE":
            return "WAIT"

    # 8. PAPER_ENTRY_ALLOWED conditions
    if (
        abc_buy_point in _ABC_READY
        and market_regime in ("BULL",)
        and theme_rank in ("LEADER", "STRONG")
        and watchlist_rank in ("CORE", "MAIN_THEME_SWING")
        and integrated_decision in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY")
    ):
        return "PAPER_ENTRY_ALLOWED"

    # 9. PAPER_PLAN_READY
    if integrated_decision == "PAPER_PLAN_READY":
        return "PAPER_PLAN_READY"
    if abc_buy_point in _ABC_READY and market_regime == "RANGE":
        return "PAPER_PLAN_READY"

    # 10. Default safe fallback
    return "WAIT"


def run_paper_simulation(inp: "PaperSimulationInput") -> "PaperSimulationResult":
    """
    Run a single-scenario paper simulation.
    Returns PaperSimulationResult with simulated trades.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
        PaperSimulationInput, PaperSimulationResult, PaperSimulationTrade,
    )
    assert inp.paper_only is True,       "paper_only must be True"
    assert inp.no_real_orders is True,   "no_real_orders must be True"
    assert inp.research_only is True,    "research_only must be True"

    action = _determine_action(
        market_regime=inp.market_regime,
        theme_rank=inp.theme_rank,
        watchlist_rank=inp.watchlist_rank,
        abc_buy_point=inp.abc_buy_point,
        mistake_taxonomy_effect=inp.mistake_taxonomy_effect,
        risk_dashboard_status=inp.risk_dashboard_status,
        integrated_decision=inp.integrated_decision,
    )

    assert action in ALLOWED_OUTPUT_ACTIONS, f"Forbidden action: {action}"
    for w in FORBIDDEN_OUTPUT_WORDS:
        assert w not in action, f"Forbidden word in action: {action}"

    # Simulate a small set of paper trades based on action
    trades: List[PaperSimulationTrade] = []
    capital = inp.initial_capital

    if action in ("PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED", "PAPER_PLAN_READY"):
        # Generate deterministic paper trades
        trade_count = 5 if action == "PAPER_ENTRY_ALLOWED" else 2
        risk_pct = inp.risk_per_trade_pct / 100.0
        win_trades = int(trade_count * 0.6)

        for i in range(trade_count):
            is_win = i < win_trades
            trade_risk_amount = capital * risk_pct
            entry = 100.0 + i * 5.0
            stop = entry * (1 - risk_pct * 2)
            if is_win:
                exit_p = entry * (1 + risk_pct * 3)
                pnl = trade_risk_amount * 2.0
                r_mult = 2.0
            else:
                exit_p = stop
                pnl = -trade_risk_amount
                r_mult = -1.0
            pnl_pct = pnl / capital * 100.0
            capital += pnl
            trades.append(PaperSimulationTrade(
                trade_id=f"PT180-{i+1:03d}",
                symbol=f"SIM{i+1:04d}",
                entry_price=round(entry, 2),
                exit_price=round(exit_p, 2),
                stop_loss=round(stop, 2),
                position_size=round(trade_risk_amount / (entry - stop) if entry != stop else 1.0, 2),
                pnl=round(pnl, 2),
                pnl_pct=round(pnl_pct, 4),
                r_multiple=r_mult,
                abc_type=inp.abc_buy_point if inp.abc_buy_point in ("A", "B", "C") else "A",
                theme=inp.theme_rank,
                regime=inp.market_regime,
                mistake_type=inp.mistake_taxonomy_effect,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                no_broker=True,
                not_investment_advice=True,
            ))
    elif action == "REDUCE_RISK":
        # Half-size trade
        risk_pct = inp.risk_per_trade_pct / 200.0
        trade_risk_amount = capital * risk_pct
        entry = 100.0
        stop = entry * 0.98
        exit_p = entry * 0.99  # small loss
        pnl = -trade_risk_amount * 0.5
        pnl_pct = pnl / capital * 100.0
        capital += pnl
        trades.append(PaperSimulationTrade(
            trade_id="PT180-R001",
            symbol="SIM_REDUCE",
            entry_price=entry,
            exit_price=exit_p,
            stop_loss=stop,
            position_size=round(trade_risk_amount / (entry - stop), 2),
            pnl=round(pnl, 2),
            pnl_pct=round(pnl_pct, 4),
            r_multiple=-0.5,
            abc_type="A",
            theme=inp.theme_rank,
            regime=inp.market_regime,
            mistake_type=inp.mistake_taxonomy_effect,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            no_broker=True,
            not_investment_advice=True,
        ))

    final_capital = capital
    total_return_pct = (final_capital - inp.initial_capital) / inp.initial_capital * 100.0

    return PaperSimulationResult(
        scenario_id=f"SIM180-{action}",
        total_return_pct=round(total_return_pct, 4),
        final_capital=round(final_capital, 2),
        trade_count=len(trades),
        trades=trades,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        no_broker=True,
        not_investment_advice=True,
    )


def get_action_for_input(inp: "PaperSimulationInput") -> str:
    """
    Return the paper simulation action for given input without running full simulation.
    [!] Paper Only. Research Only. No Real Orders.
    """
    return _determine_action(
        market_regime=inp.market_regime,
        theme_rank=inp.theme_rank,
        watchlist_rank=inp.watchlist_rank,
        abc_buy_point=inp.abc_buy_point,
        mistake_taxonomy_effect=inp.mistake_taxonomy_effect,
        risk_dashboard_status=inp.risk_dashboard_status,
        integrated_decision=inp.integrated_decision,
    )


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "schema": _SCHEMA,
        "policy": _POLICY,
        "allowed_output_actions": sorted(ALLOWED_OUTPUT_ACTIONS),
        "forbidden_output_words": sorted(FORBIDDEN_OUTPUT_WORDS),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


def validate_action(action: str) -> bool:
    """Return True if action is allowed and contains no forbidden words."""
    if action not in ALLOWED_OUTPUT_ACTIONS:
        return False
    for w in FORBIDDEN_OUTPUT_WORDS:
        if w in action:
            return False
    return True


if __name__ == "__main__":
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperSimulationInput
    test_input = PaperSimulationInput()
    result = run_paper_simulation(test_input)
    print(f"[v1.8.0 Paper Simulation Engine] action={result.scenario_id} trades={result.trade_count} return={result.total_return_pct:.2f}%")
    print("[OK] paper_simulation_engine_v180 ready")
