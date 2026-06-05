"""
gui/data_coverage_adapter.py — DataCoverageAdapter for TW Quant Cockpit v0.6.2.

Bridge between GUI panel and data coverage backend.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataCoverageAdapter:
    """Adapter between GUI and data coverage backend.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/data_coverage",
        report_dir: str = "reports",
    ) -> None:
        self.output_dir = output_dir
        self.report_dir = report_dir

    def run_coverage(self, mode: str = "real"):
        """Run coverage scan. Returns (items, summary)."""
        from data_coverage.data_coverage_engine import DataCoverageEngine
        engine = DataCoverageEngine(project_root=_BASE_DIR, output_dir=self.output_dir)
        return engine.run(mode=mode)

    def generate_report(self, mode: str = "real") -> str:
        """Generate coverage report. Returns report path."""
        from reports.data_coverage_report import DataCoverageReport
        reporter = DataCoverageReport(
            project_root=_BASE_DIR,
            output_dir=self.output_dir,
            report_dir=self.report_dir,
        )
        return reporter.run(mode=mode)

    def load_latest_summary(self) -> dict:
        """Load most recent coverage summary CSV. Returns dict."""
        from data_coverage.data_coverage_store import DataCoverageStore
        store = DataCoverageStore(output_dir=self.output_dir)
        return store.load_latest_summary()

    def load_latest_items(self) -> List[dict]:
        """Load most recent coverage items CSV. Returns list of dicts."""
        from data_coverage.data_coverage_store import DataCoverageStore
        store = DataCoverageStore(output_dir=self.output_dir)
        return store.load_latest_items()

    def load_latest_report_path(self) -> Optional[str]:
        """Find the most recent coverage report markdown. Returns path or None."""
        pattern = os.path.join(_BASE_DIR, self.report_dir, "data_coverage_report_*.md")
        files = sorted(glob.glob(pattern))
        return files[-1] if files else None
