"""
gui/strategy_lab_adapter.py — StrategyLabAdapter v0.9.0

GUI bridge between StrategyLabPanel and backend strategy_lab package.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/strategy_lab"
_DEFAULT_REPORT_DIR = "reports"


class StrategyLabAdapter:
    """GUI ↔ backend bridge for Strategy Lab Stable.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Read-only. Does not modify any module status or weights.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = _DEFAULT_OUTPUT_DIR,
        report_dir: str = _DEFAULT_REPORT_DIR,
    ) -> None:
        if os.path.isabs(output_dir):
            self._out_dir = output_dir
        else:
            self._out_dir = os.path.join(BASE_DIR, output_dir)
        if os.path.isabs(report_dir):
            self._rep_dir = report_dir
        else:
            self._rep_dir = os.path.join(BASE_DIR, report_dir)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def run_validation(self, mode: str = "real") -> dict:
        """Run full Strategy Lab validation pipeline."""
        try:
            from strategy_lab.strategy_lab_engine import StrategyLabEngine
            engine = StrategyLabEngine(project_root=BASE_DIR, output_dir=self._out_dir)
            return engine.run(mode=mode)
        except Exception as exc:
            logger.warning("StrategyLabAdapter.run_validation: %s", exc)
            return {"error": str(exc), "no_real_orders": True, "production_blocked": True}

    def generate_report(self, mode: str = "real") -> str:
        """Generate Markdown report. Returns path."""
        try:
            from reports.strategy_lab_stable_report import StrategyLabStableReportBuilder
            builder = StrategyLabStableReportBuilder()
            return builder.build(mode=mode, output_dir=self._rep_dir,
                                 lab_output_dir=self._out_dir)
        except Exception as exc:
            logger.warning("StrategyLabAdapter.generate_report: %s", exc)
            return ""

    def build_manifest(self) -> dict:
        """Build release manifest."""
        try:
            from strategy_lab.strategy_lab_release_manifest import StrategyLabReleaseManifestBuilder
            builder = StrategyLabReleaseManifestBuilder(output_dir=self._out_dir)
            return builder.build_manifest()
        except Exception as exc:
            logger.warning("StrategyLabAdapter.build_manifest: %s", exc)
            return {"error": str(exc)}

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_summary(self):
        """Load latest StrategyLabSummary or None."""
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            store = StrategyLabStore(output_dir=self._out_dir)
            return store.load_latest_summary()
        except Exception as exc:
            logger.warning("StrategyLabAdapter.load_latest_summary: %s", exc)
            return None

    def load_capabilities(self) -> list:
        """Load capabilities as list of dicts."""
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            from strategy_lab.strategy_lab_schema import StrategyLabCapability
            store = StrategyLabStore(output_dir=self._out_dir)
            raws  = store.load_capabilities()
            return [StrategyLabCapability.from_dict(d) for d in raws]
        except Exception as exc:
            logger.warning("StrategyLabAdapter.load_capabilities: %s", exc)
            return []

    def load_checks(self) -> list:
        """Load latest checks as list of dicts."""
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            from strategy_lab.strategy_lab_schema import StrategyLabCheck
            store = StrategyLabStore(output_dir=self._out_dir)
            raws  = store.load_latest_checks()
            return [StrategyLabCheck.from_dict(d) for d in raws]
        except Exception as exc:
            logger.warning("StrategyLabAdapter.load_checks: %s", exc)
            return []

    def load_latest_report_path(self) -> str:
        """Return path to latest strategy_lab report, or ''."""
        pattern = os.path.join(self._rep_dir, "strategy_lab_stable_report_*.md")
        files   = sorted(glob.glob(pattern))
        return files[-1] if files else ""

    def load_latest_manifest_path(self) -> str:
        """Return path to latest manifest JSON, or ''."""
        pattern = os.path.join(self._out_dir, "strategy_lab_release_manifest_*.json")
        files   = sorted(glob.glob(pattern))
        return files[-1] if files else ""
