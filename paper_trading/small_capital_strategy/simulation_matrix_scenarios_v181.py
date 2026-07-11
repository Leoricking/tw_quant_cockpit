"""
paper_trading/small_capital_strategy/simulation_matrix_scenarios_v181.py
75 simulation matrix scenarios for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA  = "181"
_POLICY  = "1.8.1-simulation-scenario-matrix-stress-test"

_SAFETY = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "stress_test_only": True, "no_real_orders": True, "no_broker": True,
    "not_investment_advice": True, "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}

_SCENARIOS: List[Dict[str, Any]] = [
    # ── SM181-001 to SM181-010: entry_allowed (BULL + LEADER/STRONG + CORE/MAIN + A/B/C) ──
    {
        "id": "SM181-001", "name": "BULL + LEADER + CORE + A → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-002", "name": "BULL + LEADER + CORE + B → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-003", "name": "BULL + LEADER + CORE + C → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-004", "name": "BULL + STRONG + MAIN_THEME_SWING + A → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-005", "name": "BULL + LEADER + CORE + A + risk_0.8 → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-006", "name": "BULL + STRONG + CORE + B → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-007", "name": "BULL + LEADER + MAIN_THEME_SWING + C → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-008", "name": "BULL + LEADER + CORE + B + capital_500k → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-009", "name": "BULL + STRONG + MAIN_THEME_SWING + B + capital_1m → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-010", "name": "BULL + LEADER + CORE + A + max5 + risk_1.5 → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },

    # ── SM181-011 to SM181-020: blocked ──────────────────────────────────────
    {
        "id": "SM181-011", "name": "RISK_OFF regime → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-012", "name": "EXCLUDED theme_rank → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "EXCLUDED", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-013", "name": "EXCLUDED watchlist_rank → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "EXCLUDED",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-014", "name": "BLOCKED abc_signal → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "BLOCKED", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-015", "name": "BLOCKED behavior_risk → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "BLOCKED", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-016", "name": "BLOCKED risk_dashboard → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-017", "name": "NO_STOP_LOSS mistake_injection → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NO_STOP_LOSS",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-018", "name": "RISK_OFF + EXCLUDED theme → double BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "EXCLUDED", "watchlist_rank": "EXCLUDED",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NO_STOP_LOSS",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-019", "name": "RISK_OFF + NO_STOP_LOSS + EXCLUDED watchlist → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "LEADER", "watchlist_rank": "EXCLUDED",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NO_STOP_LOSS",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.5, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-020", "name": "BULL + EXCLUDED + BLOCKED abc + risk BLOCKED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "EXCLUDED", "watchlist_rank": "CORE",
        "abc_signal": "BLOCKED", "behavior_risk": "PASS", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },

    # ── SM181-021 to SM181-028: observe ──────────────────────────────────────
    {
        "id": "SM181-021", "name": "BEAR + LEADER + CORE + A → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-022", "name": "UNKNOWN regime + LEADER + CORE + B → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-023", "name": "BEAR + STRONG + MAIN_THEME_SWING + C → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-024", "name": "UNKNOWN + STRONG + CORE + A → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-025", "name": "BEAR + LEADER + MAIN_THEME_SWING + B → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-026", "name": "BEAR + STRONG + SECOND_WAVE + A → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "STRONG", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-027", "name": "UNKNOWN + LEADER + SECOND_WAVE + C → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "LEADER", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-028", "name": "BEAR + LEADER + CORE + A + capital_1m → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },

    # ── SM181-029 to SM181-036: wait ─────────────────────────────────────────
    {
        "id": "SM181-029", "name": "BULL + LEADER + CORE + NOT_READY → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "NOT_READY", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-030", "name": "BULL + WEAK theme + CORE + A → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "WEAK", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-031", "name": "BULL + LEADER + TRAINING watchlist + A → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "TRAINING",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-032", "name": "BULL + WATCH theme + CORE + B → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "WATCH", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-033", "name": "BULL + LEADER + CORE + NOT_READY + WATCH behavior → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "NOT_READY", "behavior_risk": "WATCH", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-034", "name": "RANGE + WEAK theme + TRAINING + NOT_READY → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "RANGE", "theme_rank": "WEAK", "watchlist_rank": "TRAINING",
        "abc_signal": "NOT_READY", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-035", "name": "BULL + WEAK + TRAINING + B → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "WEAK", "watchlist_rank": "TRAINING",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-036", "name": "BULL + LEADER + TRAINING + NOT_READY + capital_1m → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "TRAINING",
        "abc_signal": "NOT_READY", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },

    # ── SM181-037 to SM181-043: plan_ready ───────────────────────────────────
    {
        "id": "SM181-037", "name": "RANGE + LEADER + CORE + A → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-038", "name": "RANGE + STRONG + CORE + B → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-039", "name": "RANGE + LEADER + MAIN_THEME_SWING + C → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-040", "name": "RANGE + STRONG + MAIN_THEME_SWING + A → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-041", "name": "RANGE + LEADER + SECOND_WAVE + B → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-042", "name": "RANGE + STRONG + CORE + C + capital_1m → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-043", "name": "RANGE + LEADER + CORE + A + max3 + risk_0.8 → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },

    # ── SM181-044 to SM181-049: reduce_risk ──────────────────────────────────
    {
        "id": "SM181-044", "name": "BULL + LEADER + CORE + A + OVERSIZED_POSITION → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "OVERSIZED_POSITION",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-045", "name": "BULL + LEADER + CORE + B + OVERTRADING → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "OVERTRADING",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-046", "name": "BULL + STRONG + CORE + A + MOVED_STOP_LOSS → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "MOVED_STOP_LOSS",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-047", "name": "RANGE + LEADER + CORE + C + OVERSIZED_POSITION → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "OVERSIZED_POSITION",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-048", "name": "BULL + STRONG + MAIN_THEME_SWING + B + MOVED_STOP_LOSS → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "MOVED_STOP_LOSS",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-049", "name": "BULL + LEADER + SECOND_WAVE + A + OVERTRADING + capital_1m → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "OVERTRADING",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },

    # ── SM181-050 to SM181-055: review_required ───────────────────────────────
    {
        "id": "SM181-050", "name": "BULL + LEADER + CORE + A + REVENGE_TRADE → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "REVENGE_TRADE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-051", "name": "BULL + LEADER + CORE + B + behavior WARNING → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "WARNING", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-052", "name": "BULL + STRONG + CORE + A + risk_dashboard WARNING → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "WARNING",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-053", "name": "RANGE + LEADER + MAIN_THEME_SWING + C + REVENGE_TRADE → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "REVENGE_TRADE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-054", "name": "BULL + STRONG + CORE + B + WARNING behavior + capital_1m → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "B", "behavior_risk": "WARNING", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-055", "name": "BULL + LEADER + CORE + A + risk WARNING + REVENGE_TRADE → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "WARNING",
        "mistake_injection": "REVENGE_TRADE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },

    # ── SM181-056 to SM181-062: stress ───────────────────────────────────────
    {
        "id": "SM181-056", "name": "STRESS: Market crash -25% shock → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "BEAR", "theme_rank": "EXCLUDED", "watchlist_rank": "EXCLUDED",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-057", "name": "STRESS: Theme collapse LEADER→EXCLUDED → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "BULL", "theme_rank": "EXCLUDED", "watchlist_rank": "CORE",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NO_STOP_LOSS",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-058", "name": "STRESS: Losing streak 8 trades → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "BEAR", "theme_rank": "WEAK", "watchlist_rank": "TRAINING",
        "abc_signal": "NOT_READY", "behavior_risk": "WARNING", "risk_dashboard": "WARNING",
        "mistake_injection": "REVENGE_TRADE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-059", "name": "STRESS: Volatility spike + oversized position → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "RISK_OFF", "theme_rank": "EXCLUDED", "watchlist_rank": "EXCLUDED",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "OVERSIZED_POSITION",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-060", "name": "STRESS: Gap-down stop + NO_STOP_LOSS + RISK_OFF → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "RISK_OFF", "theme_rank": "WEAK", "watchlist_rank": "TRAINING",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NO_STOP_LOSS",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-061", "name": "STRESS: Liquidity shrink + OVERTRADING → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "BEAR", "theme_rank": "WEAK", "watchlist_rank": "EXCLUDED",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "OVERTRADING",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-062", "name": "STRESS: Combined MOVED_STOP_LOSS + BEAR + EXCLUDED → STRESS_TEST_ONLY",
        "category": "stress", "expected_action": "STRESS_TEST_ONLY",
        "market_regime": "BEAR", "theme_rank": "EXCLUDED", "watchlist_rank": "EXCLUDED",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "MOVED_STOP_LOSS",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },

    # ── SM181-063 to SM181-069: robustness ───────────────────────────────────
    {
        "id": "SM181-063", "name": "ROBUSTNESS: BULL + LEADER + CORE + A + all PASS → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-064", "name": "ROBUSTNESS: RANGE + STRONG + SECOND_WAVE + B → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-065", "name": "ROBUSTNESS: BULL + LEADER + MAIN_THEME_SWING + C + OVERTRADING → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "WARNING",
        "mistake_injection": "OVERTRADING",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-066", "name": "ROBUSTNESS: BEAR + STRONG + CORE + A + WATCH behavior → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "BEAR", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "WATCH", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-067", "name": "ROBUSTNESS: RANGE + LEADER + TRAINING + B + MOVED_STOP_LOSS → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "TRAINING",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "MOVED_STOP_LOSS",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-068", "name": "ROBUSTNESS: BULL + WATCH + SECOND_WAVE + NOT_READY + capital_1m → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "BULL", "theme_rank": "WATCH", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "NOT_READY", "behavior_risk": "WATCH", "risk_dashboard": "WARNING",
        "mistake_injection": "NONE",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-069", "name": "ROBUSTNESS: UNKNOWN + STRONG + MAIN_THEME_SWING + C + OVERSIZED → SIMULATE_ONLY",
        "category": "robustness", "expected_action": "SIMULATE_ONLY",
        "market_regime": "UNKNOWN", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "C", "behavior_risk": "WARNING", "risk_dashboard": "PASS",
        "mistake_injection": "OVERSIZED_POSITION",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },

    # ── SM181-070 to SM181-075: regime_shift ─────────────────────────────────
    {
        "id": "SM181-070", "name": "REGIME_SHIFT: BULL→RISK_OFF mid-run → BLOCKED",
        "category": "regime_shift", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-071", "name": "REGIME_SHIFT: BULL→BEAR mid-run → OBSERVE",
        "category": "regime_shift", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "A", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-072", "name": "REGIME_SHIFT: RANGE→RISK_OFF → BLOCKED",
        "category": "regime_shift", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
    {
        "id": "SM181-073", "name": "REGIME_SHIFT: BULL→UNKNOWN → OBSERVE",
        "category": "regime_shift", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_signal": "C", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 300000.0, "single_trade_risk_pct": 0.8, "max_positions": 3,
        **_SAFETY,
    },
    {
        "id": "SM181-074", "name": "REGIME_SHIFT: BULL→RISK_OFF + EXCLUDED theme → BLOCKED",
        "category": "regime_shift", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "EXCLUDED", "watchlist_rank": "EXCLUDED",
        "abc_signal": "BLOCKED", "behavior_risk": "BLOCKED", "risk_dashboard": "BLOCKED",
        "mistake_injection": "NO_STOP_LOSS",
        "initial_capital": 1000000.0, "single_trade_risk_pct": 1.5, "max_positions": 5,
        **_SAFETY,
    },
    {
        "id": "SM181-075", "name": "REGIME_SHIFT: RANGE→BEAR + WEAK theme → OBSERVE",
        "category": "regime_shift", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "STRONG", "watchlist_rank": "SECOND_WAVE",
        "abc_signal": "B", "behavior_risk": "PASS", "risk_dashboard": "PASS",
        "mistake_injection": "NONE",
        "initial_capital": 500000.0, "single_trade_risk_pct": 1.0, "max_positions": 4,
        **_SAFETY,
    },
]


# ── Helper functions ──────────────────────────────────────────────────────────

def get_scenario_count() -> int:
    """Return total number of scenarios defined."""
    return len(_SCENARIOS)


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return a copy of the full scenario list."""
    return list(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Return the scenario dict with matching id, or None."""
    for s in _SCENARIOS:
        if s["id"] == scenario_id:
            return dict(s)
    return None


def get_scenarios_by_category(cat: str) -> List[Dict[str, Any]]:
    """Return all scenarios whose category matches cat."""
    return [dict(s) for s in _SCENARIOS if s["category"] == cat]


def get_scenario_categories() -> List[str]:
    """Return sorted list of unique category values present."""
    seen: List[str] = []
    for s in _SCENARIOS:
        c = s["category"]
        if c not in seen:
            seen.append(c)
    return sorted(seen)


def get_scenario_ids() -> List[str]:
    """Return list of all scenario id strings."""
    return [s["id"] for s in _SCENARIOS]


def get_scenarios_info() -> Dict[str, Any]:
    """Return metadata dict about the scenario collection."""
    return {
        "schema": _SCHEMA,
        "policy": _POLICY,
        "count": get_scenario_count(),
        "categories": get_scenario_categories(),
        "ids": get_scenario_ids(),
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "stress_test_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


if __name__ == "__main__":
    info = get_scenarios_info()
    print(f"[v1.8.1 Scenarios] count={info['count']} categories={info['categories']}")
    assert info["count"] >= 75, f"Expected >=75 scenarios, got {info['count']}"
    print("[OK] simulation_matrix_scenarios_v181 ready")
