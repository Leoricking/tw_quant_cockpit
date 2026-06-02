"""
gui/research_review_dashboard_adapter.py — GUI Bridge for Research Review Dashboard (v0.4.7).

Bridges the GUI panel to the research review aggregation logic.

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchReviewDashboardAdapter:
    """
    GUI bridge for the Research Review Dashboard.

    All methods are safe to call from a QThread. No broker calls.
    No auto-weight changes. No order submission.

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
        output_dir: str = "data/backtest_results/research_review",
        report_dir: str = "reports",
    ):
        self._output_dir = os.path.join(BASE_DIR, output_dir)
        self._report_dir = os.path.join(BASE_DIR, report_dir)

    # ------------------------------------------------------------------
    # Run review
    # ------------------------------------------------------------------

    def run_review(self, mode: str = "real", period: str = "daily") -> dict:
        """
        Run full research review aggregation and persist results.

        Returns dashboard summary dict. Never raises.
        """
        try:
            from review.review_aggregator import ResearchReviewAggregator
            from review.review_scorecard import ResearchReviewScorecard
            from review.review_action_planner import ReviewActionPlanner
            from review.review_store import ResearchReviewStore

            agg = ResearchReviewAggregator()
            summary = agg.run(mode=mode, period=period)
            items   = agg.get_review_items()

            scorecard   = ResearchReviewScorecard().calculate(summary)
            action_plan = ReviewActionPlanner().build_action_plan(items, scorecard)

            store = ResearchReviewStore(output_dir=self._output_dir)
            store.save_summary(summary)
            store.save_review_items(items)
            store.save_scorecard(scorecard)
            store.save_action_plan(action_plan)

            summary["_scorecard"]   = scorecard
            summary["_action_plan"] = action_plan
            summary["_items"]       = [i.to_dict() for i in items]
            return summary

        except Exception as exc:
            logger.error("[adapter] run_review failed: %s", exc, exc_info=True)
            return {
                "error": str(exc),
                "open_items": 0,
                "critical_items": 0,
                "warning_items": 0,
                "action_items_count": 0,
                "safety_status": "PRODUCTION_BLOCKED",
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
            }

    def generate_report(self, mode: str = "real", period: str = "daily") -> str:
        """
        Run review and generate Markdown report.

        Returns report file path. Never raises.
        """
        try:
            from review.review_aggregator import ResearchReviewAggregator
            from review.review_scorecard import ResearchReviewScorecard
            from review.review_action_planner import ReviewActionPlanner
            from reports.research_review_dashboard_report import ResearchReviewDashboardReport

            agg = ResearchReviewAggregator()
            summary = agg.run(mode=mode, period=period)
            items   = agg.get_review_items()

            scorecard   = ResearchReviewScorecard().calculate(summary)
            action_plan = ReviewActionPlanner().build_action_plan(items, scorecard)

            reporter = ResearchReviewDashboardReport(report_dir=self._report_dir)
            path = reporter.generate(
                summary=summary,
                scorecard=scorecard,
                review_items=items,
                action_plan=action_plan,
                mode=mode,
                period=period,
            )
            return path

        except Exception as exc:
            logger.error("[adapter] generate_report failed: %s", exc, exc_info=True)
            return ""

    # ------------------------------------------------------------------
    # Load persisted results
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> Optional[dict]:
        """Load latest dashboard summary from CSV."""
        try:
            from review.review_store import ResearchReviewStore
            return ResearchReviewStore(output_dir=self._output_dir).load_latest_summary()
        except Exception as exc:
            logger.warning("[adapter] load_latest_summary failed: %s", exc)
            return None

    def load_latest_items(self) -> List[dict]:
        """Load latest review items from CSV."""
        try:
            from review.review_store import ResearchReviewStore
            return ResearchReviewStore(output_dir=self._output_dir).load_latest_items()
        except Exception as exc:
            logger.warning("[adapter] load_latest_items failed: %s", exc)
            return []

    def load_latest_scorecard(self) -> Optional[dict]:
        """Load latest scorecard from CSV."""
        try:
            from review.review_store import ResearchReviewStore
            return ResearchReviewStore(output_dir=self._output_dir).load_latest_scorecard()
        except Exception as exc:
            logger.warning("[adapter] load_latest_scorecard failed: %s", exc)
            return None

    def load_latest_action_plan(self) -> List[dict]:
        """Load latest action plan from CSV."""
        try:
            from review.review_store import ResearchReviewStore
            return ResearchReviewStore(output_dir=self._output_dir).load_latest_action_plan()
        except Exception as exc:
            logger.warning("[adapter] load_latest_action_plan failed: %s", exc)
            return []

    def load_latest_report_path(self) -> str:
        """Find the most recent research review dashboard report file."""
        try:
            reports = [
                f for f in os.listdir(self._report_dir)
                if f.startswith("research_review_dashboard_report_") and f.endswith(".md")
            ]
            if not reports:
                return ""
            reports.sort(reverse=True)
            return os.path.join(self._report_dir, reports[0])
        except Exception as exc:
            logger.warning("[adapter] load_latest_report_path failed: %s", exc)
            return ""
