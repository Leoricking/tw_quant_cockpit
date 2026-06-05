"""research_intelligence/research_intelligence_engine.py — ResearchIntelligenceEngine v0.7.0.

Master engine: collect signals → build recommendations → build priority board → save outputs.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
[!] No broker connection. No order submission. No auto-trading.
[!] No modification of rule weights, strategy weights, or ML features.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from research_intelligence.research_intelligence_schema import (
    ResearchSignal, ResearchRecommendation, ResearchIntelligenceSummary,
    PRI_P0, PRI_P1, SEV_CRITICAL, SEV_HIGH,
    CAT_DATA_GAP, CAT_REPLAY_MISTAKE, CAT_RULE_REVIEW, CAT_REPORT_GAP, CAT_SYSTEM_RISK,
)
from research_intelligence.signal_aggregator import ResearchSignalAggregator
from research_intelligence.recommendation_engine import ResearchRecommendationEngine
from research_intelligence.priority_planner import ResearchPriorityPlanner
from research_intelligence.research_intelligence_store import ResearchIntelligenceStore

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchIntelligenceEngine:
    """Master research intelligence engine.

    Runs the full pipeline:
      collect signals → build recommendations → build plans → build priority board →
      save outputs → return summary.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    [!] Does NOT: place orders, connect broker, modify weights, auto-trade.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/research_intelligence",
    ) -> None:
        root = os.path.abspath(project_root) if project_root != "." else BASE_DIR
        self._root       = root
        self._output_dir = os.path.join(root, output_dir) if not os.path.isabs(output_dir) else output_dir
        os.makedirs(self._output_dir, exist_ok=True)

        self._aggregator    = ResearchSignalAggregator(project_root=root, output_dir=self._output_dir)
        self._rec_engine    = ResearchRecommendationEngine()
        self._planner       = ResearchPriorityPlanner()
        self._store         = ResearchIntelligenceStore(output_dir=self._output_dir)

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

    def run(self, mode: str = "real", period: str = "daily") -> dict:
        """Run the full research intelligence pipeline.

        Returns a dict with summary, signals, recommendations, priority_board,
        daily_plan, weekly_plan.
        """
        logger.info("[ResearchIntelligenceEngine] run mode=%s period=%s", mode, period)

        # 1. Collect signals
        signals = self._aggregator.collect_all(mode=mode)

        # 2. Build recommendations
        recommendations = self._rec_engine.build_recommendations(signals, mode=mode)

        # 3. Build plans
        daily_plan  = self._rec_engine.build_daily_plan(recommendations)
        weekly_plan = self._rec_engine.build_weekly_plan(recommendations)

        # 4. Build priority board
        priority_board = self._planner.build_priority_board(signals, recommendations)

        # 5. Build summary
        summary = self.build_summary(signals, recommendations, priority_board)

        # 6. Save outputs
        try:
            self._store.save_summary(summary)
            self._store.save_signals(signals)
            self._store.save_recommendations(recommendations)
            self._store.save_priority_board(priority_board)
            self._store.save_daily_plan(daily_plan)
            self._store.save_weekly_plan(weekly_plan)
        except Exception as exc:
            logger.error("[ResearchIntelligenceEngine] save error: %s", exc)

        return {
            "ok":              True,
            "summary":         summary.to_dict(),
            "signals":         [s.to_dict() for s in signals],
            "recommendations": [r.to_dict() for r in recommendations],
            "priority_board":  self._planner.board_to_rows(priority_board),
            "daily_plan":      [r.to_dict() for r in daily_plan],
            "weekly_plan":     [r.to_dict() for r in weekly_plan],
            "no_real_orders":  True,
            "production_blocked": True,
            "research_only":   True,
        }

    # ------------------------------------------------------------------
    # Summary builder
    # ------------------------------------------------------------------

    def build_summary(
        self,
        signals: List[ResearchSignal],
        recommendations: List[ResearchRecommendation],
        priority_board: Dict[str, list],
    ) -> ResearchIntelligenceSummary:
        high = sum(1 for s in signals if s.severity in (SEV_CRITICAL, SEV_HIGH))
        med  = sum(1 for s in signals if s.severity == "MEDIUM")
        low  = sum(1 for s in signals if s.severity in ("LOW", "INFO"))

        data_gaps    = sum(1 for s in signals if s.category == CAT_DATA_GAP)
        replay_issues= sum(1 for s in signals if s.category == CAT_REPLAY_MISTAKE)
        rule_reviews = sum(1 for s in signals if s.category == CAT_RULE_REVIEW)
        report_gaps  = sum(1 for s in signals if s.category == CAT_REPORT_GAP)
        sys_risk     = sum(1 for s in signals if s.category == CAT_SYSTEM_RISK)

        p0_items = priority_board.get(PRI_P0, [])
        p1_items = priority_board.get(PRI_P1, [])
        top = p0_items[0].get("title", "") if p0_items else (
            p1_items[0].get("title", "") if p1_items else ""
        )
        top_p0 = p0_items[0].get("title", "") if p0_items else ""
        top_p1 = p1_items[0].get("title", "") if p1_items else ""

        overall = "ATTENTION_NEEDED" if p0_items or sys_risk > 0 else (
            "REVIEW" if high > 0 else "OK"
        )

        # today_focus: P0/P1 most important item, or fallback message
        if top_p0:
            today_focus = f"P0: {top_p0[:100]}"
        elif top_p1:
            today_focus = f"P1: {top_p1[:100]}"
        elif recommendations:
            today_focus = f"Review: {recommendations[0].title[:100]}"
        else:
            today_focus = "No critical issues — continue optional reports and replay practice"

        # Safe commands = recommendations with non-BLOCKED_FOR_TRADING command_safety
        safe_cmds = sum(
            1 for r in recommendations
            if getattr(r, "command_safety", "") != "BLOCKED_FOR_TRADING"
        )
        blocked_trading = 0  # by design — forbidden action guard ensures this
        optional_count  = sum(1 for r in recommendations if getattr(r, "optional", False))

        return ResearchIntelligenceSummary(
            generated_at=datetime.now().isoformat(),
            mode="real",
            total_signals=len(signals),
            high_priority_count=high,
            medium_priority_count=med,
            low_priority_count=low,
            data_gap_count=data_gaps,
            replay_issue_count=replay_issues,
            rule_review_count=rule_reviews,
            report_gap_count=report_gaps,
            system_risk_count=sys_risk,
            recommendations_count=len(recommendations),
            top_priority=top[:200] if top else "",
            overall_status=overall,
            today_focus=today_focus,
            top_p0_title=top_p0[:200] if top_p0 else "",
            top_p1_title=top_p1[:200] if top_p1 else "",
            safe_command_count=safe_cmds,
            blocked_trading_action_count=blocked_trading,
            optional_recommendation_count=optional_count,
        )
