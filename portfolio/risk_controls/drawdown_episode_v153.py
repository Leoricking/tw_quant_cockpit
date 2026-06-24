"""
portfolio/risk_controls/drawdown_episode_v153.py — Drawdown Episode Detection v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import uuid
from typing import List

from portfolio.risk_controls.enums_v153 import DrawdownEpisodeStatus
from portfolio.risk_controls.models_v153 import DrawdownEpisode, UnderwaterPoint

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownEpisodeDetector:
    """Detects contiguous drawdown episodes from the underwater curve."""

    RESEARCH_ONLY = True

    def detect(
        self,
        underwater_curve: List[UnderwaterPoint],
        min_drawdown_pct: float = -0.01,
    ) -> List[DrawdownEpisode]:
        """
        Detect all drawdown episodes.
        An episode starts when dd_pct < min_drawdown_pct and ends when dd_pct >= 0.
        """
        episodes: List[DrawdownEpisode] = []
        if not underwater_curve:
            return episodes

        in_episode = False
        episode_start: str = ""
        episode_peak_value: float = 0.0
        episode_trough_pct: float = 0.0
        episode_trough_date: str = ""
        episode_trough_value: float = 0.0

        for pt in underwater_curve:
            if not in_episode:
                if pt.drawdown_pct < min_drawdown_pct:
                    in_episode = True
                    episode_start = pt.date
                    episode_peak_value = pt.high_water_mark
                    episode_trough_pct = pt.drawdown_pct
                    episode_trough_date = pt.date
                    episode_trough_value = pt.portfolio_value
            else:
                if pt.drawdown_pct < episode_trough_pct:
                    episode_trough_pct = pt.drawdown_pct
                    episode_trough_date = pt.date
                    episode_trough_value = pt.portfolio_value

                if pt.drawdown_pct >= 0.0:
                    # Episode closed
                    ep = self._build_episode(
                        episode_start, episode_trough_date,
                        episode_peak_value, episode_trough_value, episode_trough_pct,
                        end_date=pt.date, status=DrawdownEpisodeStatus.CLOSED,
                    )
                    episodes.append(ep)
                    in_episode = False

        # Handle open episode
        if in_episode and underwater_curve:
            last = underwater_curve[-1]
            ep = self._build_episode(
                episode_start, episode_trough_date,
                episode_peak_value, episode_trough_value, episode_trough_pct,
                end_date=None, status=DrawdownEpisodeStatus.OPEN,
            )
            episodes.append(ep)

        return episodes

    def _build_episode(
        self,
        start_date: str,
        trough_date: str,
        peak_value: float,
        trough_value: float,
        max_drawdown_pct: float,
        end_date=None,
        status=DrawdownEpisodeStatus.OPEN,
    ) -> DrawdownEpisode:
        episode_id = f"EP_{start_date}_{uuid.uuid4().hex[:6]}"
        duration = self._date_diff_days(start_date, end_date or trough_date)
        recovery = (
            self._date_diff_days(trough_date, end_date)
            if end_date and status == DrawdownEpisodeStatus.CLOSED
            else None
        )
        return DrawdownEpisode(
            episode_id=episode_id,
            start_date=start_date,
            trough_date=trough_date,
            end_date=end_date,
            peak_value=peak_value,
            trough_value=trough_value,
            max_drawdown_pct=max_drawdown_pct,
            duration_days=duration,
            recovery_days=recovery,
            status=status,
        )

    @staticmethod
    def _date_diff_days(d1: str, d2: str) -> int:
        from datetime import date
        try:
            a = date.fromisoformat(d1)
            b = date.fromisoformat(d2)
            return abs((b - a).days)
        except Exception:
            return 0
