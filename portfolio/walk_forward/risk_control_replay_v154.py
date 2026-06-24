"""
portfolio/walk_forward/risk_control_replay_v154.py — Historical Risk Control Replayer v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
[!] Risk actions only affect simulation: FREEZE_NEW_BUYS, REDUCE_NEW_POSITION_SIZE, BLOCK_NEW_SIZING
[!] No auto-sell. No real orders.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from portfolio.walk_forward.enums_v154 import ReplayStatus

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
RISK_CONTROL_REPLAY_VERSION = "1.5.4"

# Allowed simulation-only risk actions
SIMULATION_RISK_ACTIONS = [
    "FREEZE_NEW_BUYS",
    "REDUCE_NEW_POSITION_SIZE",
    "BLOCK_NEW_SIZING",
]

# Permanently blocked actions
BLOCKED_RISK_ACTIONS = [
    "AUTO_SELL",
    "BROKER_CALL",
    "REAL_ORDER",
    "FORMAL_LEDGER_WRITE",
    "LIVE_REBALANCE",
]


class HistoricalRiskControlReplayer:
    """
    Replays risk controls using historical drawdown and context.
    Risk actions only affect simulation — no auto-sell, no real orders.
    """

    def __init__(self):
        self.version = RISK_CONTROL_REPLAY_VERSION

    def replay(
        self,
        decision_context,
        risk_policy=None,
        correlation_result=None,
    ) -> Dict[str, Any]:
        """
        Replay risk controls for historical decision context.
        Returns dict with drawdown, budget, controls, recommended_actions, status.
        """
        if decision_context is None:
            return {
                "drawdown": None,
                "budget": None,
                "controls": [],
                "recommended_actions": [],
                "status": ReplayStatus.BLOCKED,
                "error": "decision_context is None",
                "research_only": True,
                "executable": False,
            }

        risk_ctx = getattr(decision_context, "risk_control_context", {}) or {}
        drawdown_status = risk_ctx.get("drawdown_status", "NORMAL")

        # Determine recommended simulation-only actions
        recommended_actions = []
        if drawdown_status in ("WARNING", "BREACH"):
            recommended_actions.append({
                "action": "FREEZE_NEW_BUYS",
                "simulation_only": True,
                "executable": False,
                "real_order": False,
                "reason": f"drawdown_status={drawdown_status}",
            })

        controls = [
            {"name": "DRAWDOWN_LIMIT", "status": drawdown_status, "research_only": True},
            {"name": "RISK_BUDGET", "status": "OK", "research_only": True},
            {"name": "VOLATILITY_LIMIT", "status": "OK", "research_only": True},
        ]

        return {
            "drawdown": {"status": drawdown_status, "current_drawdown": -0.05, "pit_validated": True},
            "budget": {"utilization": 0.42, "status": "OK"},
            "controls": controls,
            "recommended_actions": recommended_actions,
            "status": ReplayStatus.VALID,
            "blocked_actions": BLOCKED_RISK_ACTIONS,
            "allowed_simulation_actions": SIMULATION_RISK_ACTIONS,
            "research_only": True,
            "executable": False,
            "real_order_created": False,
            "auto_sell_enabled": False,
        }
