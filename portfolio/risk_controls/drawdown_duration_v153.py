"""
portfolio/risk_controls/drawdown_duration_v153.py — Drawdown Duration Calculations v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.risk_controls.models_v153 import DrawdownEpisode

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownDurationAnalyzer:
    """Analyzes duration statistics for drawdown episodes."""

    RESEARCH_ONLY = True

    def analyze(self, episodes: List[DrawdownEpisode]) -> Dict[str, Any]:
        """Compute duration statistics across episodes."""
        if not episodes:
            return {
                "episode_count": 0,
                "avg_duration_days": 0.0,
                "max_duration_days": 0,
                "min_duration_days": 0,
                "total_days_in_drawdown": 0,
            }

        durations = [ep.duration_days for ep in episodes]
        return {
            "episode_count": len(episodes),
            "avg_duration_days": sum(durations) / len(durations),
            "max_duration_days": max(durations),
            "min_duration_days": min(durations),
            "total_days_in_drawdown": sum(durations),
        }
