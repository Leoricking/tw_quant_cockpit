"""
paper_trading/small_capital_strategy/paper_simulation_scenarios_v180.py
70 paper simulation scenarios for Paper Simulation & Performance Lab v1.8.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List, Optional

_SCHEMA  = "180"
_POLICY  = "1.8.0-paper-simulation-performance-lab"

_SAFETY = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_SCENARIOS: List[Dict[str, Any]] = [
    # ── PAPER_ENTRY_ALLOWED (10) ─────────────────────────────────────────────
    {
        "id": "SC180-001", "name": "BULL + LEADER + CORE + A → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-002", "name": "BULL + LEADER + CORE + B → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-003", "name": "BULL + LEADER + CORE + C → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-004", "name": "BULL + STRONG + MAIN_THEME_SWING + A → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 3,
        **_SAFETY,
    },
    {
        "id": "SC180-005", "name": "BULL + LEADER + CORE + A + risk_0.8 → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 5,
        **_SAFETY,
    },
    {
        "id": "SC180-006", "name": "BULL + STRONG + CORE + B → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-007", "name": "BULL + LEADER + MAIN_THEME_SWING + C → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.5, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-008", "name": "BULL + STRONG + MAIN_THEME_SWING + B → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-009", "name": "BULL + LEADER + CORE + A + max5 → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 5,
        **_SAFETY,
    },
    {
        "id": "SC180-010", "name": "BULL + STRONG + CORE + C + risk_1.5 → PAPER_ENTRY_ALLOWED",
        "category": "entry_allowed", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.5, "max_holdings": 3,
        **_SAFETY,
    },
    # ── BLOCKED (10) ─────────────────────────────────────────────────────────
    {
        "id": "SC180-011", "name": "RISK_OFF regime → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-012", "name": "integrated_decision=BLOCKED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "BLOCKED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-013", "name": "watchlist=EXCLUDED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "EXCLUDED",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-014", "name": "theme=EXCLUDED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "EXCLUDED", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-015", "name": "risk_dashboard=BLOCKED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "BLOCKED", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-016", "name": "abc=BLOCKED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "BLOCKED", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-017", "name": "mistake=no_stop_loss → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "no_stop_loss",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-018", "name": "RISK_OFF + EXCLUDED theme → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "RISK_OFF", "theme_rank": "EXCLUDED", "watchlist_rank": "EXCLUDED",
        "abc_buy_point": "BLOCKED", "mistake_taxonomy_effect": "no_stop_loss",
        "risk_dashboard_status": "BLOCKED", "integrated_decision": "BLOCKED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-019", "name": "BEAR + EXCLUDED + no_stop_loss → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BEAR", "theme_rank": "EXCLUDED", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "no_stop_loss",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-020", "name": "BULL + watchlist=EXCLUDED + risk=BLOCKED → BLOCKED",
        "category": "blocked", "expected_action": "BLOCKED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "EXCLUDED",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "BLOCKED", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── OBSERVE (8) ──────────────────────────────────────────────────────────
    {
        "id": "SC180-021", "name": "BEAR regime → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-022", "name": "UNKNOWN regime → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-023", "name": "BEAR + STRONG + CORE + A → OBSERVE (regime overrides)",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-024", "name": "BEAR + LEADER + CORE + B → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-025", "name": "UNKNOWN + WEAK + CORE → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "WEAK", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-026", "name": "BEAR + WATCH + TRAINING → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "WATCH", "watchlist_rank": "TRAINING",
        "abc_buy_point": "NOT_READY", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-027", "name": "UNKNOWN + CORE + B → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "UNKNOWN", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-028", "name": "BEAR + LEADER + MAIN_THEME_SWING + C → OBSERVE",
        "category": "observe", "expected_action": "OBSERVE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "OBSERVE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── WAIT (8) ──────────────────────────────────────────────────────────────
    {
        "id": "SC180-029", "name": "abc=NOT_READY → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "NOT_READY", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-030", "name": "RANGE + WEAK theme → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "RANGE", "theme_rank": "WEAK", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-031", "name": "BULL + WATCH theme → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "WATCH", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-032", "name": "BULL + TRAINING watchlist → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "TRAINING",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-033", "name": "RANGE + SECOND_WAVE + NOT_READY → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "SECOND_WAVE",
        "abc_buy_point": "NOT_READY", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-034", "name": "BULL + WEAK + SECOND_WAVE → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "WEAK", "watchlist_rank": "SECOND_WAVE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-035", "name": "integrated=WAIT → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-036", "name": "RANGE + LEADER + TRAINING → WAIT",
        "category": "wait", "expected_action": "WAIT",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "TRAINING",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "WAIT",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── PAPER_PLAN_READY (7) ──────────────────────────────────────────────────
    {
        "id": "SC180-037", "name": "integrated=PAPER_PLAN_READY → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-038", "name": "RANGE + LEADER + CORE + A → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-039", "name": "RANGE + STRONG + MAIN_THEME_SWING + B → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-040", "name": "RANGE + LEADER + CORE + C → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 3,
        **_SAFETY,
    },
    {
        "id": "SC180-041", "name": "RANGE + STRONG + CORE + A → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.5, "max_holdings": 5,
        **_SAFETY,
    },
    {
        "id": "SC180-042", "name": "RANGE + LEADER + SECOND_WAVE + A → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "SECOND_WAVE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-043", "name": "BULL + LEADER + CORE + A + PAPER_PLAN_READY decision → PAPER_PLAN_READY",
        "category": "plan_ready", "expected_action": "PAPER_PLAN_READY",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_PLAN_READY",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── REDUCE_RISK (6) ──────────────────────────────────────────────────────
    {
        "id": "SC180-044", "name": "oversized_position mistake → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "oversized_position",
        "risk_dashboard_status": "PASS", "integrated_decision": "REDUCE_RISK",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-045", "name": "overtrading mistake → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "overtrading",
        "risk_dashboard_status": "PASS", "integrated_decision": "REDUCE_RISK",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-046", "name": "moved_stop_loss mistake → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "moved_stop_loss",
        "risk_dashboard_status": "PASS", "integrated_decision": "REDUCE_RISK",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-047", "name": "integrated=REDUCE_RISK → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "REDUCE_RISK",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-048", "name": "RANGE + oversized_position → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "oversized_position",
        "risk_dashboard_status": "PASS", "integrated_decision": "REDUCE_RISK",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-049", "name": "BULL + overtrading + WARNING → REDUCE_RISK",
        "category": "reduce_risk", "expected_action": "REDUCE_RISK",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "overtrading",
        "risk_dashboard_status": "WARNING", "integrated_decision": "REDUCE_RISK",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── REVIEW_REQUIRED (6) ──────────────────────────────────────────────────
    {
        "id": "SC180-050", "name": "revenge_trade mistake → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "revenge_trade",
        "risk_dashboard_status": "PASS", "integrated_decision": "REVIEW_REQUIRED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-051", "name": "risk_dashboard=WARNING → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "WARNING", "integrated_decision": "REVIEW_REQUIRED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-052", "name": "integrated=REVIEW_REQUIRED → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "RANGE", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "REVIEW_REQUIRED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-053", "name": "revenge_trade + WARNING → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "revenge_trade",
        "risk_dashboard_status": "WARNING", "integrated_decision": "REVIEW_REQUIRED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-054", "name": "RANGE + WARNING + LEADER → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "WARNING", "integrated_decision": "REVIEW_REQUIRED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-055", "name": "BULL + revenge_trade + CORE → REVIEW_REQUIRED",
        "category": "review_required", "expected_action": "REVIEW_REQUIRED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "revenge_trade",
        "risk_dashboard_status": "PASS", "integrated_decision": "REVIEW_REQUIRED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── NO_TRADE (7) ──────────────────────────────────────────────────────────
    {
        "id": "SC180-056", "name": "integrated=NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-057", "name": "RANGE + LEADER + CORE + NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "RANGE", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-058", "name": "BEAR + LEADER + CORE + NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "BEAR", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-059", "name": "BULL + STRONG + TRAINING + NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "TRAINING",
        "abc_buy_point": "NOT_READY", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-060", "name": "RANGE + WATCH + SECOND_WAVE + NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "RANGE", "theme_rank": "WATCH", "watchlist_rank": "SECOND_WAVE",
        "abc_buy_point": "NOT_READY", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-061", "name": "UNKNOWN + LEADER + CORE + NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "UNKNOWN", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-062", "name": "BULL + WEAK + TRAINING + NO_TRADE → NO_TRADE",
        "category": "no_trade", "expected_action": "NO_TRADE",
        "market_regime": "BULL", "theme_rank": "WEAK", "watchlist_rank": "TRAINING",
        "abc_buy_point": "NOT_READY", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "NO_TRADE",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    # ── PAPER_ADD_ALLOWED (7) ────────────────────────────────────────────────
    {
        "id": "SC180-063", "name": "integrated=PAPER_ADD_ALLOWED → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-064", "name": "BULL + LEADER + CORE + C + ADD → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 5,
        **_SAFETY,
    },
    {
        "id": "SC180-065", "name": "BULL + STRONG + MAIN_THEME_SWING + B + ADD → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "B", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-066", "name": "BULL + LEADER + CORE + A + ADD + risk_1.0 → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
    {
        "id": "SC180-067", "name": "BULL + STRONG + CORE + A + ADD + 3holdings → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 0.8, "max_holdings": 3,
        **_SAFETY,
    },
    {
        "id": "SC180-068", "name": "BULL + LEADER + MAIN_THEME_SWING + C + ADD → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 5,
        **_SAFETY,
    },
    {
        "id": "SC180-069", "name": "BULL + STRONG + MAIN_THEME_SWING + C + ADD + risk_1.5 → PAPER_ADD_ALLOWED",
        "category": "add_allowed", "expected_action": "PAPER_ADD_ALLOWED",
        "market_regime": "BULL", "theme_rank": "STRONG", "watchlist_rank": "MAIN_THEME_SWING",
        "abc_buy_point": "C", "mistake_taxonomy_effect": "none",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ADD_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.5, "max_holdings": 4,
        **_SAFETY,
    },
    # ── Additional / edge cases (1) ───────────────────────────────────────────
    {
        "id": "SC180-070", "name": "BULL + LEADER + CORE + A + clean → PAPER_ENTRY_ALLOWED (benchmark)",
        "category": "benchmark", "expected_action": "PAPER_ENTRY_ALLOWED",
        "market_regime": "BULL", "theme_rank": "LEADER", "watchlist_rank": "CORE",
        "abc_buy_point": "A", "mistake_taxonomy_effect": "clean",
        "risk_dashboard_status": "PASS", "integrated_decision": "PAPER_ENTRY_ALLOWED",
        "initial_capital": 300000.0, "risk_per_trade_pct": 1.0, "max_holdings": 4,
        **_SAFETY,
    },
]


def get_scenario_count() -> int:
    """Return number of scenarios."""
    return len(_SCENARIOS)


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios."""
    return list(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Return scenario by ID or None."""
    for s in _SCENARIOS:
        if s.get("id") == scenario_id:
            return s
    return None


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return all scenarios with given category."""
    return [s for s in _SCENARIOS if s.get("category") == category]


def get_scenario_categories() -> List[str]:
    """Return sorted list of unique scenario categories."""
    return sorted(set(s["category"] for s in _SCENARIOS))


def get_scenario_ids() -> List[str]:
    """Return all scenario IDs."""
    return [s["id"] for s in _SCENARIOS]


def get_scenarios_info() -> Dict[str, Any]:
    """Return scenario registry metadata."""
    return {
        "schema": _SCHEMA,
        "policy": _POLICY,
        "count": len(_SCENARIOS),
        "categories": get_scenario_categories(),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


if __name__ == "__main__":
    print(f"[v1.8.0] Scenarios: {get_scenario_count()}")
    for cat in get_scenario_categories():
        n = len(get_scenarios_by_category(cat))
        print(f"  {cat}: {n}")
    print("[OK] paper_simulation_scenarios_v180 ready")
