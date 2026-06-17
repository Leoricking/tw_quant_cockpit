"""
gui/replay_strategy_knowledge_adapter.py — Qt adapter for Strategy Knowledge Replay v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyKnowledgeGuiAdapter:
    """
    Bridges the strategy replay backend to the GUI panel.
    [!] Research Only. No Real Orders.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = repo_root

    def get_current_snapshot(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest strategy snapshot for a session."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            q = StrategyReplayQuery(repo_root=self.repo_root)
            return q.latest_snapshot(session_id)
        except Exception as exc:
            logger.warning("get_current_snapshot error: %s", exc)
            return None

    def get_agreement(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest agreement result for a session."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            q = StrategyReplayQuery(repo_root=self.repo_root)
            agreements = q.agreements(session_id)
            if agreements:
                return sorted(agreements, key=lambda a: a.get("created_at", ""), reverse=True)[0]
            return None
        except Exception as exc:
            logger.warning("get_agreement error: %s", exc)
            return None

    def get_conflicts(self, session_id: str):
        """Get conflicts for a session."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            q = StrategyReplayQuery(repo_root=self.repo_root)
            return q.conflicts(session_id)
        except Exception as exc:
            logger.warning("get_conflicts error: %s", exc)
            return []

    def get_pending_reviews(self, session_id: str):
        """Get pending rule reviews for a session."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            q = StrategyReplayQuery(repo_root=self.repo_root)
            return q.pending_reviews(session_id)
        except Exception as exc:
            logger.warning("get_pending_reviews error: %s", exc)
            return []
