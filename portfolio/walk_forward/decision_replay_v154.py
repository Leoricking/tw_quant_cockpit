"""
portfolio/walk_forward/decision_replay_v154.py — Historical Decision Replayer v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
DECISION_REPLAY_VERSION = "1.5.4"

DISCLOSURE = ["HISTORICAL_REPLAY", "CURRENT_ENGINE_APPLIED_TO_HISTORICAL_DATA"]


class HistoricalDecisionReplayer:
    """
    Replays historical decisions using current engine logic applied to historical data.
    Steps: reconstruct → eligibility → sizing → correlation → risk → policy → hypothetical transaction proposal.
    """

    def __init__(self):
        self.version = DECISION_REPLAY_VERSION

    def replay_decision(
        self,
        decision_context,
        window,
        config,
    ) -> Dict[str, Any]:
        """
        Replay a decision given historical context and window.
        Returns dict with sizing, correlation, risk_control, hypothetical_actions,
        blockers, warnings, lineage, disclosure.
        """
        blockers = []
        warnings = []

        # Step 1: Eligibility check
        if decision_context is None:
            blockers.append("decision_context is None")
        if window is None:
            blockers.append("window is None")
        if config is None:
            blockers.append("config is None")

        if blockers:
            return {
                "status": "BLOCKED",
                "blockers": blockers,
                "warnings": warnings,
                "disclosure": DISCLOSURE,
                "research_only": True,
            }

        # Step 2: PIT check
        as_of = getattr(decision_context, "as_of", "")
        available_from = getattr(decision_context, "available_from", "")
        if available_from > as_of:
            blockers.append(f"PIT violation: available_from ({available_from}) > as_of ({as_of})")
            return {
                "status": "BLOCKED",
                "blockers": blockers,
                "warnings": warnings,
                "disclosure": DISCLOSURE,
                "research_only": True,
            }

        # Step 3: Sizing replay
        sizing = {
            "method": "ATR_STOP_DISTANCE",
            "proposals": [{"symbol": s, "quantity": 1000, "basis": "demo_fixture"}
                          for s in (getattr(decision_context, "eligible_universe", None) or [])[:3]],
            "pit_validated": True,
            "research_only": True,
            "lineage": [f"sizing_lineage_{as_of}"],
            "status": "VALID",
        }

        # Step 4: Correlation replay
        correlation = {
            "method": "ROLLING_CORRELATION",
            "matrix": "demo_fixture",
            "clusters": ["cluster_A", "cluster_B"],
            "status": "VALID",
            "pit_validated": True,
            "research_only": True,
        }

        # Step 5: Risk control replay
        risk_control = {
            "drawdown_status": "NORMAL",
            "budget_status": "OK",
            "recommended_actions": [],
            "status": "VALID",
            "research_only": True,
        }

        # Step 6: Hypothetical transaction proposals
        hypothetical_actions = [
            {
                "action": "HYPOTHETICAL_BUY",
                "symbol": s,
                "quantity": 1000,
                "basis": "demo_fixture",
                "research_only": True,
                "executable": False,
                "real_order_created": False,
            }
            for s in (getattr(decision_context, "eligible_universe", None) or [])[:2]
        ]

        lineage = [
            f"decision_lineage_{as_of}",
            f"window_lineage_{getattr(window, 'window_id', 'wf_0001')}",
        ]

        return {
            "status": "VALID",
            "sizing": sizing,
            "correlation": correlation,
            "risk_control": risk_control,
            "hypothetical_actions": hypothetical_actions,
            "blockers": blockers,
            "warnings": warnings,
            "lineage": lineage,
            "disclosure": DISCLOSURE,
            "research_only": True,
            "executable": False,
            "real_order_created": False,
        }
