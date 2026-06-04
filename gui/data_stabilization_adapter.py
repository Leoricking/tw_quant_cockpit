"""gui/data_stabilization_adapter.py — DataStabilizationAdapter v0.5.5.

Non-GUI bridge between DataStabilizationEngine / store and GUI / CLI callers.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataStabilizationAdapter:
    """Non-GUI bridge for Data / Feature Store Stabilization.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        output_dir: str = "data/backtest_results/data_stabilization",
        report_dir: str = "reports",
    ) -> None:
        self.output_dir = os.path.join(BASE_DIR, output_dir)
        self.report_dir = os.path.join(BASE_DIR, report_dir)

    # ------------------------------------------------------------------
    # Engine / Run
    # ------------------------------------------------------------------

    def run_stabilization(self, mode: str = "real") -> dict:
        """Run all data stabilization checks. Returns summary dict."""
        try:
            from data_stabilization.data_stabilization_engine import DataStabilizationEngine
            engine = DataStabilizationEngine(output_dir=os.path.relpath(self.output_dir, BASE_DIR))
            return engine.run(mode=mode)
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.run_stabilization(): %s", exc)
            return {
                "error": str(exc),
                "no_real_orders": True,
                "production_blocked": True,
            }

    def generate_report(self, mode: str = "real") -> str:
        """Generate Markdown report. Returns output path (empty on error)."""
        try:
            from reports.data_stabilization_report import DataStabilizationReport
            report = DataStabilizationReport(
                report_dir=self.report_dir,
                output_dir=self.output_dir,
                mode=mode,
            )
            return report.generate(mode=mode)
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.generate_report(): %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Store / Load
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load most recent summary CSV."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_latest_summary()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_latest_summary(): %s", exc)
            return {}

    def load_schema_status(self) -> List[dict]:
        """Load most recent schema status CSV."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_schema_status()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_schema_status(): %s", exc)
            return []

    def load_lineage(self) -> List[dict]:
        """Load most recent data lineage CSV."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_lineage()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_lineage(): %s", exc)
            return []

    def load_feature_readiness(self) -> List[dict]:
        """Load most recent feature readiness CSV."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_feature_readiness()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_feature_readiness(): %s", exc)
            return []

    def load_health(self) -> dict:
        """Load most recent feature store health CSV."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_health()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_health(): %s", exc)
            return {}

    def load_leakage_summary(self) -> List[dict]:
        """Load most recent leakage guard summary CSV."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_leakage_summary()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_leakage_summary(): %s", exc)
            return []

    def load_latest_report_path(self) -> Optional[str]:
        """Return path to most recent data stabilization Markdown report."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_latest_report_path()
        except Exception as exc:
            logger.warning("DataStabilizationAdapter.load_latest_report_path(): %s", exc)
            return None
