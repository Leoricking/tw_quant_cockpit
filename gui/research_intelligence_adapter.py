"""
gui/research_intelligence_adapter.py — ResearchIntelligenceAdapter v0.7.0.

Bridge between GUI panel and research intelligence backend.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchIntelligenceAdapter:
    """Adapter between GUI and research intelligence backend.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    [!] Production Trading: BLOCKED. Not investment advice.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        output_dir: str = "data/backtest_results/research_intelligence",
        report_dir: str = "reports",
    ) -> None:
        self.output_dir = (
            os.path.join(_BASE_DIR, output_dir)
            if not os.path.isabs(output_dir) else output_dir
        )
        self.report_dir = report_dir

    def run_intelligence(self, mode: str = "real", period: str = "daily") -> dict:
        """Run full research intelligence pipeline. Returns result dict."""
        from research_intelligence.research_intelligence_engine import ResearchIntelligenceEngine
        engine = ResearchIntelligenceEngine(project_root=_BASE_DIR, output_dir=self.output_dir)
        return engine.run(mode=mode, period=period)

    def generate_report(self, mode: str = "real") -> str:
        """Generate Markdown research intelligence report. Returns report path."""
        result = self.run_intelligence(mode=mode)
        from reports.research_intelligence_report import ResearchIntelligenceReport
        reporter = ResearchIntelligenceReport()
        content = reporter.generate(
            summary=result.get("summary", {}),
            signals=result.get("signals", []),
            recommendations=result.get("recommendations", []),
            priority_board={"rows": result.get("priority_board", [])},
            daily_plan=result.get("daily_plan", []),
            weekly_plan=result.get("weekly_plan", []),
            mode=mode,
        )
        return reporter.save(content, report_dir=self.report_dir)

    def load_latest_summary(self) -> dict:
        """Load most recent research intelligence summary. Returns dict."""
        from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
        store = ResearchIntelligenceStore(output_dir=self.output_dir)
        return store.load_latest_summary()

    def load_latest_signals(self) -> List[dict]:
        """Load most recent signals CSV. Returns list of dicts."""
        from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
        store = ResearchIntelligenceStore(output_dir=self.output_dir)
        result = store.load_latest_signals()
        return result.get("signals", [])

    def load_latest_recommendations(self) -> List[dict]:
        """Load most recent recommendations CSV. Returns list of dicts."""
        from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
        store = ResearchIntelligenceStore(output_dir=self.output_dir)
        result = store.load_latest_recommendations()
        return result.get("recommendations", [])

    def load_latest_priority_board(self) -> dict:
        """Load most recent priority board. Returns {P0:[..], P1:[..], P2:[..], P3:[..]}."""
        from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
        store = ResearchIntelligenceStore(output_dir=self.output_dir)
        result = store.load_latest_priority_board()
        return result.get("board", {"P0": [], "P1": [], "P2": [], "P3": []})

    def load_latest_daily_plan(self) -> List[dict]:
        """Load most recent daily plan. Returns list of dicts."""
        from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
        store = ResearchIntelligenceStore(output_dir=self.output_dir)
        result = store.load_latest_daily_plan()
        return result.get("daily_plan", [])

    def load_latest_weekly_plan(self) -> List[dict]:
        """Load most recent weekly plan. Returns list of dicts."""
        from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
        store = ResearchIntelligenceStore(output_dir=self.output_dir)
        result = store.load_latest_weekly_plan()
        return result.get("weekly_plan", [])

    def load_latest_report_path(self) -> Optional[str]:
        """Find most recent research intelligence report markdown. Returns path or None."""
        pattern = os.path.join(_BASE_DIR, self.report_dir, "research_intelligence_report_*.md")
        files = sorted(glob.glob(pattern))
        return files[-1] if files else None
