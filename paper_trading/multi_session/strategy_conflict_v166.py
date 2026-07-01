"""
paper_trading/multi_session/strategy_conflict_v166.py — Strategy Conflict Detector v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No auto stock selection. No auto strategy change.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_STRATEGY_CHANGE = True
NO_AUTO_STOCK_SELECTION = True


class StrategyConflictDetector:
    """Detects cross-session strategy conflicts."""

    def detect(self, sessions: List[SessionDescriptor]) -> List[Dict[str, Any]]:
        conflicts: List[Dict[str, Any]] = []

        # Duplicate strategy detection
        strategy_sessions: Dict[str, List[str]] = {}
        for s in sessions:
            for strat in s.strategies:
                strategy_sessions.setdefault(strat, []).append(s.session_id)
        for strat, sids in strategy_sessions.items():
            if len(sids) > 1:
                conflicts.append({
                    "type": "duplicate_strategy",
                    "strategy": strat,
                    "sessions": sids,
                    "severity": "WARN",
                    "action": "warn_only",
                })

        # Incompatible horizon (placeholder detection)
        horizons: Dict[str, List[str]] = {}
        for s in sessions:
            if s.resource_requirements:
                hz = s.resource_requirements.get("horizon", "")
                if hz:
                    horizons.setdefault(hz, []).append(s.session_id)

        return conflicts
