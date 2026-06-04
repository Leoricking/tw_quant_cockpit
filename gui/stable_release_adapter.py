"""gui/stable_release_adapter.py — StableReleaseAdapter for v0.6.0 Stable Release panel.

GUI adapter bridge — wraps all stable_release modules. Returns dicts for GUI consumption.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No BUY/SELL/ORDER outputs. No broker connection.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_REPORT_DIR = os.path.join(BASE_DIR, "reports")
_MANIFEST_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "stable_release")


class StableReleaseAdapter:
    """Bridges GUI panel to all stable_release modules.

    All methods are wrapped in try/except — never crash. Lazy imports.
    Returns dicts (not objects) for GUI consumption.
    No real orders. No broker connection.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self) -> None:
        self._last_checklist_result: Optional[dict] = None
        self._last_capability_summary: Optional[dict] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_checklist(self, mode: str = "real") -> dict:
        """Run v0.6.0 stable release checklist. Returns result dict."""
        try:
            from stable_release.stable_release_checklist_v060 import StableReleaseChecklistV060
            result = StableReleaseChecklistV060().run(mode=mode)
            self._last_checklist_result = result
            return result
        except Exception as exc:
            logger.error("[StableReleaseAdapter] run_checklist error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "overall_status": "ERROR",
                "checks": [],
                "total_checks": 0,
                "pass_count": 0,
                "warning_count": 0,
                "fail_count": 0,
                "no_real_orders": True,
                "production_blocked": True,
            }

    def build_capability_matrix(self) -> dict:
        """Build and return capability matrix summary."""
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            matrix.build()
            caps = matrix.list_capabilities()
            by_status: dict[str, int] = {}
            by_category: dict[str, int] = {}
            for c in caps:
                by_status[c.status] = by_status.get(c.status, 0) + 1
                by_category[c.category] = by_category.get(c.category, 0) + 1
            result = {
                "ok":                 True,
                "total":              len(caps),
                "stable_count":       by_status.get("STABLE", 0),
                "usable_count":       by_status.get("USABLE", 0),
                "partial_count":      by_status.get("PARTIAL", 0),
                "experimental_count": by_status.get("EXPERIMENTAL", 0),
                "blocked_count":      by_status.get("BLOCKED", 0),
                "by_status":          by_status,
                "by_category":        by_category,
                "capabilities":       [c.to_dict() for c in caps],
                "no_real_orders":     True,
                "production_blocked": True,
            }
            self._last_capability_summary = result
            return result
        except Exception as exc:
            logger.error("[StableReleaseAdapter] build_capability_matrix error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "total": 0,
                "capabilities": [],
                "no_real_orders": True,
                "production_blocked": True,
            }

    def build_manifest(self, version: str = "v0.6.0") -> dict:
        """Build release manifest JSON and Markdown."""
        try:
            from stable_release.release_manifest_builder import ReleaseManifestBuilder
            result = ReleaseManifestBuilder().build_manifest(version=version)
            return result
        except Exception as exc:
            logger.error("[StableReleaseAdapter] build_manifest error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "no_real_orders": True,
                "production_blocked": True,
            }

    def generate_report(self, mode: str = "real") -> dict:
        """Generate v0.6.0 stable release Markdown report."""
        try:
            from reports.stable_release_v060_report import StableReleaseV060Report
            result = StableReleaseV060Report().run(mode=mode)
            return result
        except Exception as exc:
            logger.error("[StableReleaseAdapter] generate_report error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "report_path": "",
                "status": "ERROR",
                "no_real_orders": True,
                "production_blocked": True,
            }

    def load_latest_summary(self) -> dict:
        """Return last cached capability summary or reload it."""
        if self._last_capability_summary:
            return self._last_capability_summary
        return self.build_capability_matrix()

    def load_latest_manifest_path(self) -> str:
        """Return path to most recent release manifest JSON, or empty string."""
        try:
            import glob
            pattern = os.path.join(_MANIFEST_DIR, "release_manifest_*.json")
            files = glob.glob(pattern)
            if files:
                return max(files, key=os.path.getmtime)
        except Exception as exc:
            logger.warning("[StableReleaseAdapter] manifest path error: %s", exc)
        return ""

    def load_latest_report_path(self) -> str:
        """Return path to most recent stable release report, or empty string."""
        try:
            import glob
            pattern = os.path.join(_REPORT_DIR, "stable_release_v0.6.0_report_*.md")
            files = glob.glob(pattern)
            if files:
                return max(files, key=os.path.getmtime)
        except Exception as exc:
            logger.warning("[StableReleaseAdapter] report path error: %s", exc)
        return ""

    def load_limitations(self) -> list:
        """Return list of known limitations."""
        try:
            from stable_release.known_limitations import _LIMITATIONS
            return list(_LIMITATIONS)
        except Exception as exc:
            logger.warning("[StableReleaseAdapter] limitations error: %s", exc)
            return []
