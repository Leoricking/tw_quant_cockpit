"""
gui/replay_challenge_action_panel.py — Challenge action panel v1.2.7

Buttons: View Context, View Higher/Lower Timeframe, View Strategy,
Write Thesis, Write Risk Plan, Update Checklist,
Wait, Simulate Enter, Simulate Add, Simulate Reduce, Simulate Exit, Skip,
Request Hint, Pause, Resume, Submit, Cancel.

[!] All "Simulate" buttons trigger SIMULATION DECISION ONLY — no paper/broker orders.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

ACTION_BUTTONS = [
    {"label": "View Context",           "action": "VIEW_CONTEXT",      "simulation": False},
    {"label": "View Higher Timeframe",  "action": "VIEW_TIMEFRAME",     "simulation": False},
    {"label": "View Lower Timeframe",   "action": "VIEW_TIMEFRAME",     "simulation": False},
    {"label": "View Strategy",          "action": "VIEW_STRATEGY",      "simulation": False},
    {"label": "Write Thesis",           "action": "WRITE_THESIS",       "simulation": False},
    {"label": "Write Risk Plan",        "action": "WRITE_RISK_PLAN",    "simulation": False},
    {"label": "Update Checklist",       "action": "WRITE_CHECKLIST",    "simulation": False},
    {"label": "Wait",                   "action": "DECIDE_WAIT",        "simulation": False},
    {"label": "Simulate Enter (SIMULATION DECISION ONLY)", "action": "DECIDE_ENTER", "simulation": True},
    {"label": "Simulate Add (SIMULATION DECISION ONLY)",   "action": "DECIDE_ADD",   "simulation": True},
    {"label": "Simulate Reduce (SIMULATION DECISION ONLY)","action": "DECIDE_REDUCE","simulation": True},
    {"label": "Simulate Exit (SIMULATION DECISION ONLY)",  "action": "DECIDE_EXIT",  "simulation": True},
    {"label": "Skip",                   "action": "DECIDE_SKIP",        "simulation": False},
    {"label": "Request Hint",           "action": "REQUEST_HINT",       "simulation": False},
    {"label": "Pause",                  "action": "PAUSE",              "simulation": False},
    {"label": "Resume",                 "action": "RESUME",             "simulation": False},
    {"label": "Submit",                 "action": "COMPLETE",           "simulation": False},
    {"label": "Cancel",                 "action": "CANCEL",             "simulation": False},
]

class ReplayChallengeActionPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    ALL_SIMULATION_BUTTONS_LABELED = True
    def get_buttons(self) -> List[Dict[str, Any]]:
        return ACTION_BUTTONS
    def summary(self) -> dict:
        return {"buttons": len(ACTION_BUTTONS), "simulation_labeled": True, "research_only": True, "no_real_orders": True}
