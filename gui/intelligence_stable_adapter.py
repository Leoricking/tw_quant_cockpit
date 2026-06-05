"""
gui/intelligence_stable_adapter.py — IntelligenceStableAdapter v0.8.0

Bridge between GUI and intelligence_stable package.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/intelligence_stable"
_DEFAULT_REPORT_DIR = "reports"


class IntelligenceStableAdapter:
    """
    GUI adapter for intelligence_stable package.

    All methods catch exceptions and return safe defaults.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = _DEFAULT_OUTPUT_DIR,
        report_dir: str = _DEFAULT_REPORT_DIR,
    ) -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(_BASE_DIR, output_dir)
        if not os.path.isabs(report_dir):
            report_dir = os.path.join(_BASE_DIR, report_dir)
        self._output_dir = output_dir
        self._report_dir = report_dir

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def run_validation(self, mode: str = "real") -> dict:
        """Run full intelligence stable validation. Returns result dict."""
        try:
            from intelligence_stable.intelligence_stable_engine import IntelligenceStableEngine
            engine = IntelligenceStableEngine(
                project_root=_BASE_DIR,
                output_dir=self._output_dir,
            )
            result = engine.run(mode=mode)
            summary = result.get("summary")
            caps    = result.get("capabilities", [])
            checks  = result.get("checks", [])
            manifest = result.get("manifest", {})
            summary_dict = summary.to_dict() if summary else {}
            return {
                "ok":           True,
                "summary":      summary_dict,
                "capabilities": [c.to_dict() for c in caps],
                "checks":       [c.to_dict() for c in checks],
                "manifest":     manifest,
                "no_real_orders":    True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.run_validation: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "summary": {},
                "capabilities": [],
                "checks": [],
                "manifest": {},
                "no_real_orders": True,
                "production_blocked": True,
            }

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """Generate intelligence stable report. Returns dict with path."""
        try:
            from reports.intelligence_stable_report import IntelligenceStableReportBuilder
            builder = IntelligenceStableReportBuilder()
            path = builder.build(
                mode=mode,
                output_dir=self._report_dir,
                stable_output_dir=self._output_dir,
            )
            return {"ok": True, "path": path}
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.generate_report: %s", exc)
            return {"ok": False, "error": str(exc), "path": ""}

    # ------------------------------------------------------------------
    # Manifest
    # ------------------------------------------------------------------

    def build_manifest(self) -> dict:
        """Build release manifest. Returns dict."""
        try:
            from intelligence_stable.intelligence_release_manifest import IntelligenceReleaseManifestBuilder
            builder = IntelligenceReleaseManifestBuilder(
                project_root=_BASE_DIR,
                output_dir=self._output_dir,
            )
            return builder.build_manifest()
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.build_manifest: %s", exc)
            return {"error": str(exc)}

    # ------------------------------------------------------------------
    # Load latest
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load latest summary from store. Returns dict or empty dict."""
        try:
            from intelligence_stable.intelligence_stable_store import IntelligenceStableStore
            store = IntelligenceStableStore(output_dir=self._output_dir)
            summary = store.load_latest_summary()
            return summary or {}
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.load_latest_summary: %s", exc)
            return {}

    def load_capabilities(self) -> list:
        """Load capabilities from store. Returns list of dicts."""
        try:
            from intelligence_stable.intelligence_stable_store import IntelligenceStableStore
            store = IntelligenceStableStore(output_dir=self._output_dir)
            return store.load_capabilities()
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.load_capabilities: %s", exc)
            return []

    def load_checks(self) -> list:
        """Load latest checks from store. Returns list of dicts."""
        try:
            from intelligence_stable.intelligence_stable_store import IntelligenceStableStore
            store = IntelligenceStableStore(output_dir=self._output_dir)
            return store.load_latest_checks()
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.load_checks: %s", exc)
            return []

    def load_latest_report_path(self) -> str:
        """Return path to latest intelligence stable report Markdown file."""
        try:
            pattern = os.path.join(self._report_dir, "intelligence_stable_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else ""
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.load_latest_report_path: %s", exc)
            return ""

    def load_latest_manifest_path(self) -> str:
        """Return path to latest release manifest JSON file."""
        try:
            pattern = os.path.join(self._output_dir, "intelligence_release_manifest_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else ""
        except Exception as exc:
            logger.warning("IntelligenceStableAdapter.load_latest_manifest_path: %s", exc)
            return ""
