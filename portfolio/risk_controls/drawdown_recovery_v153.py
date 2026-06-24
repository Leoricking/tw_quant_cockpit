"""
portfolio/risk_controls/drawdown_recovery_v153.py — Drawdown Recovery Analysis v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from portfolio.risk_controls.enums_v153 import DrawdownEpisodeStatus
from portfolio.risk_controls.models_v153 import DrawdownEpisode

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownRecoveryAnalyzer:
    """Analyzes recovery duration statistics for drawdown episodes."""

    RESEARCH_ONLY = True

    def analyze(self, episodes: List[DrawdownEpisode]) -> Dict[str, Any]:
        """Compute recovery duration stats for closed episodes."""
        closed = [ep for ep in episodes if ep.status == DrawdownEpisodeStatus.CLOSED
                  and ep.recovery_days is not None]
        open_eps = [ep for ep in episodes if ep.status == DrawdownEpisodeStatus.OPEN]

        if not closed:
            return {
                "closed_episode_count": 0,
                "open_episode_count": len(open_eps),
                "avg_recovery_days": None,
                "max_recovery_days": None,
                "min_recovery_days": None,
            }

        recovery_days = [ep.recovery_days for ep in closed]
        return {
            "closed_episode_count": len(closed),
            "open_episode_count": len(open_eps),
            "avg_recovery_days": sum(recovery_days) / len(recovery_days),
            "max_recovery_days": max(recovery_days),
            "min_recovery_days": min(recovery_days),
        }
