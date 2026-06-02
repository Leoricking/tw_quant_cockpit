"""
gui/research_assistant_adapter.py — ResearchAssistantAdapter (v0.4.8).

GUI bridge for Research Assistant / Coach panel.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchAssistantAdapter:
    """
    GUI bridge for ResearchAssistantPanel.
    Provides run_coach(), generate_report(), and load_* methods.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/research_coach",
        report_dir: str = "reports",
    ):
        self._output_dir = (
            os.path.join(BASE_DIR, output_dir)
            if not os.path.isabs(output_dir)
            else output_dir
        )
        self._report_dir = (
            os.path.join(BASE_DIR, report_dir)
            if not os.path.isabs(report_dir)
            else report_dir
        )

    def run_coach(self, mode: str = "real", period: str = "daily") -> dict:
        """
        Run the Research Assistant Coach and save results.
        Returns session summary dict.
        Does NOT execute any trading commands.
        """
        try:
            from coach.research_assistant_engine import ResearchAssistantEngine
            from coach.coach_store import ResearchCoachStore
            engine = ResearchAssistantEngine()
            summary = engine.run(mode=mode, period=period)
            store = ResearchCoachStore(output_dir=self._output_dir)
            store.save_all(summary)
            return summary
        except Exception as exc:
            logger.error("[ResearchAssistantAdapter] run_coach failed: %s", exc)
            return {"error": str(exc), "coaching_only": True, "no_real_orders": True}

    def generate_report(self, mode: str = "real", period: str = "daily") -> str:
        """
        Generate Research Assistant report.
        Returns report file path.
        """
        try:
            from coach.research_assistant_engine import ResearchAssistantEngine
            from reports.research_assistant_report import ResearchAssistantReport
            engine = ResearchAssistantEngine()
            summary = engine.run(mode=mode, period=period)
            reporter = ResearchAssistantReport(report_dir=self._report_dir)
            path = reporter.generate(session_summary=summary, mode=mode, period=period)
            return path
        except Exception as exc:
            logger.error("[ResearchAssistantAdapter] generate_report failed: %s", exc)
            return ""

    def load_latest_summary(self) -> Optional[dict]:
        """Load latest coach summary from persisted CSV."""
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore(output_dir=self._output_dir)
            return store.load_latest_summary()
        except Exception as exc:
            logger.warning("[ResearchAssistantAdapter] load_latest_summary failed: %s", exc)
            return None

    def load_daily_checklist(self) -> List[dict]:
        """Load daily checklist from persisted CSV."""
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore(output_dir=self._output_dir)
            return store.load_daily_checklist()
        except Exception as exc:
            logger.warning("[ResearchAssistantAdapter] load_daily_checklist failed: %s", exc)
            return []

    def load_replay_training_plan(self) -> List[dict]:
        """Load replay training plan from persisted CSV."""
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore(output_dir=self._output_dir)
            return store.load_replay_training_plan()
        except Exception as exc:
            logger.warning("[ResearchAssistantAdapter] load_replay_training_plan failed: %s", exc)
            return []

    def load_rule_review_queue(self) -> List[dict]:
        """Load rule review queue from persisted CSV."""
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore(output_dir=self._output_dir)
            return store.load_rule_review_queue()
        except Exception as exc:
            logger.warning("[ResearchAssistantAdapter] load_rule_review_queue failed: %s", exc)
            return []

    def load_data_repair_plan(self) -> List[dict]:
        """Load data repair plan from persisted CSV."""
        try:
            from coach.coach_store import ResearchCoachStore
            store = ResearchCoachStore(output_dir=self._output_dir)
            return store.load_data_repair_plan()
        except Exception as exc:
            logger.warning("[ResearchAssistantAdapter] load_data_repair_plan failed: %s", exc)
            return []

    def load_latest_report_path(self) -> str:
        """Return path of the latest research assistant report file, or empty string."""
        try:
            import glob
            pattern = os.path.join(self._report_dir, "research_assistant_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else ""
        except Exception as exc:
            logger.warning("[ResearchAssistantAdapter] load_latest_report_path failed: %s", exc)
            return ""
