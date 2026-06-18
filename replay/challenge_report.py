"""
replay/challenge_report.py — Challenge report generator v1.2.7

Outputs to:
  reports/replay_challenge_attempt_{attempt_id}.md
  reports/replay_challenge_summary_YYYY-MM-DD.md
  reports/replay_challenge_progress_YYYY-MM-DD.md

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class ReplayChallengeReportGenerator:
    """
    Generate challenge reports as Markdown files.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None) -> None:
        self._root = Path(repo_root or os.getcwd())
        self._reports_dir = self._root / "reports"
        self._reports_dir.mkdir(exist_ok=True)

    def generate_attempt_report(
        self,
        attempt_id: str,
        attempt: Dict[str, Any],
        score: Optional[Dict[str, Any]] = None,
        review: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate attempt report to reports/replay_challenge_attempt_{id}.md"""
        path = self._reports_dir / f"replay_challenge_attempt_{attempt_id}.md"
        score_obj = score.get("score") if score else None
        process_score = float(getattr(score_obj, "process_score", 0.0)) if score_obj else 0.0
        total_score = float(getattr(score_obj, "total_score", 0.0)) if score_obj else 0.0

        lines = [
            f"# Replay Challenge Attempt Report",
            f"",
            f"**Attempt ID:** {attempt_id}",
            f"**Challenge ID:** {attempt.get('challenge_id', '')}",
            f"**Status:** {attempt.get('status', '')}",
            f"**Mode:** {attempt.get('mode', 'mock')}",
            f"",
            f"## Challenge Overview",
            f"",
            f"- Type: {attempt.get('challenge_type', 'N/A')}",
            f"- Difficulty: {attempt.get('difficulty', 'N/A')}",
            f"- Started At: {attempt.get('started_at', 'N/A')}",
            f"- Finished At: {attempt.get('finished_at', 'N/A')}",
            f"",
            f"## Attempt Timeline",
            f"",
            f"- Active Elapsed: {attempt.get('active_elapsed_seconds', 0.0):.1f}s",
            f"- Paused Elapsed: {attempt.get('paused_elapsed_seconds', 0.0):.1f}s",
            f"- Actions Taken: {len(attempt.get('actions', []))}",
            f"- Hints Used: {attempt.get('hints_used', 0)}",
            f"",
            f"## Decision",
            f"",
            f"- Final Decision: {attempt.get('final_decision', 'N/A')}",
            f"",
            f"## Process Score",
            f"",
            f"- Process Score: {process_score:.1f}/100",
            f"- Total Score: {total_score:.1f}/100",
            f"- Classification: {getattr(score_obj, 'classification', 'PROCESS_ONLY') if score_obj else 'PROCESS_ONLY'}",
            f"",
            f"## Outcome Review",
            f"",
            f"- Outcome: {review.get('outcome', 'NOT_REVEALED') if review else 'NOT_REVEALED'}",
            f"",
            f"## Limitations",
            f"",
            f"- This is a training simulation only.",
            f"- Scores do not represent investment ability.",
            f"- No real orders were placed.",
            f"",
            f"## Safety Declaration",
            f"",
            f"> [!] Challenge Training Only. Simulation Only. No Real Orders.",
            f"> Not Investment Advice. Process weight >= Outcome weight.",
            f"> No Public Leaderboard. No Network Submission.",
        ]
        content = "\n".join(lines)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as exc:
            logger.warning("Could not write attempt report: %s", exc)
        return str(path)

    def generate_summary_report(self, summary: Dict[str, Any]) -> str:
        """Generate summary report."""
        date = _now_date()
        path = self._reports_dir / f"replay_challenge_summary_{date}.md"
        lines = [
            f"# Replay Challenge Summary Report — {date}",
            f"",
            f"**Total Attempts:** {summary.get('total_attempts', 0)}",
            f"**Completed:** {summary.get('completed', 0)}",
            f"**Avg Process Score:** {summary.get('avg_process_score', 0.0):.1f}",
            f"**Personal Best:** {summary.get('personal_best', 0.0):.1f}",
            f"",
            f"---",
            f"*[!] Challenge Training Only. Simulation Only. No Real Orders.*",
            f"*[!] Not Investment Advice. No Public Leaderboard.*",
        ]
        content = "\n".join(lines)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as exc:
            logger.warning("Could not write summary report: %s", exc)
        return str(path)

    def generate_progress_report(self, progress: Dict[str, Any]) -> str:
        """Generate progress report."""
        date = _now_date()
        path = self._reports_dir / f"replay_challenge_progress_{date}.md"
        lines = [
            f"# Replay Challenge Progress Report — {date}",
            f"",
            f"**Challenges Attempted:** {progress.get('challenges_attempted', 0)}",
            f"**Challenges Completed:** {progress.get('challenges_completed', 0)}",
            f"**Avg Process Score:** {progress.get('avg_process_score', 0.0):.1f}",
            f"**Personal Best:** {progress.get('personal_best', 0.0):.1f}",
            f"",
            f"---",
            f"*[!] Challenge Training Only. Simulation Only. No Real Orders.*",
        ]
        content = "\n".join(lines)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as exc:
            logger.warning("Could not write progress report: %s", exc)
        return str(path)
