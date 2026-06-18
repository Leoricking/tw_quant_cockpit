"""
gui/replay_challenge_context_panel.py — Challenge context panel v1.2.7

Shows point-in-time context per difficulty. No future data. Hidden symbol/date don't leak via tooltip.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeContextPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    HIDDEN_SYMBOL_LEAKS_VIA_TOOLTIP = False
    HIDDEN_DATE_LEAKS_VIA_TOOLTIP = False
    def get_context(self, session_data: Dict[str, Any], difficulty: str = "INTERMEDIATE", hide_symbol: bool = False, hide_date: bool = False) -> Dict[str, Any]:
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        guard = ReplayChallengeHiddenDataGuard()
        ctx = dict(session_data)
        ctx = guard.sanitize_active_payload(ctx)
        ctx = guard.hide_future(ctx)
        ctx = guard.hide_outcome(ctx)
        if hide_symbol:
            ctx = guard.hide_identity(ctx, hide_symbol=True)
        if hide_date:
            ctx = guard.hide_identity(ctx, hide_date=True)
        ctx["future_data_hidden"] = True
        ctx["point_in_time_verified"] = True
        ctx["research_only"] = True
        return ctx
