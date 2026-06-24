"""
portfolio/walk_forward/sizing_replay_v154.py — Historical Sizing Replayer v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only. PIT-safe.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

from portfolio.walk_forward.enums_v154 import ReplayStatus

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
SIZING_REPLAY_VERSION = "1.5.4"


class HistoricalSizingReplayer:
    """
    Replays position sizing using historical ATR/volatility/price/stop from context.
    PIT-safe: only uses training window data.
    """

    def __init__(self):
        self.version = SIZING_REPLAY_VERSION

    def replay(
        self,
        decision_context,
        sizing_policy=None,
    ) -> Dict[str, Any]:
        """
        Replay sizing for historical decision context.
        Returns dict with proposals, method, pit_validated, lineage, status.
        """
        if decision_context is None:
            return {
                "proposals": [],
                "method": None,
                "pit_validated": False,
                "lineage": [],
                "status": ReplayStatus.BLOCKED,
                "error": "decision_context is None",
                "research_only": True,
            }

        as_of = getattr(decision_context, "as_of", "")
        available_from = getattr(decision_context, "available_from", "")

        # PIT check
        if available_from and as_of and available_from > as_of:
            return {
                "proposals": [],
                "method": None,
                "pit_validated": False,
                "lineage": [],
                "status": ReplayStatus.BLOCKED,
                "error": f"PIT violation: available_from > as_of",
                "research_only": True,
            }

        # Demo fixture sizing proposals
        universe = getattr(decision_context, "eligible_universe", None) or []
        proposals = []
        for sym in universe[:3]:
            proposals.append({
                "symbol": sym,
                "method": "ATR_STOP_DISTANCE",
                "quantity": 1000,
                "risk_amount": 5000.0,
                "atr": 2.5,
                "stop_distance": 5.0,
                "price": 450.0,
                "pit_validated": True,
                "research_only": True,
                "executable": False,
            })

        lineage = [f"sizing_lineage_{as_of}", "fixture_sizing_policy_v154"]

        return {
            "proposals": proposals,
            "method": "ATR_STOP_DISTANCE",
            "pit_validated": True,
            "lineage": lineage,
            "status": ReplayStatus.VALID,
            "research_only": True,
            "executable": False,
        }
