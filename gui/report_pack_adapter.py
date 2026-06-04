"""gui/report_pack_adapter.py — ReportPackAdapter for TW Quant Cockpit v0.5.4.

Non-GUI bridge for Report Pack Consolidation. No PySide6 dependency.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReportPackAdapter:
    """Non-GUI adapter for the Report Pack Consolidation feature.

    Safe for use from CLI or non-GUI contexts.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        output_dir: str = "data/backtest_results/report_pack",
        report_dir: str = "reports",
    ) -> None:
        self.output_dir = os.path.join(BASE_DIR, output_dir)
        self.report_dir = os.path.join(BASE_DIR, report_dir)

        self._registry       = None
        self._collector      = None
        self._builder        = None
        self._health_checker = None
        self._link_registry  = None
        self._store          = None

        try:
            from report_pack.report_registry import ReportRegistry
            self._registry = ReportRegistry()
        except Exception as exc:
            logger.warning("ReportPackAdapter: registry unavailable: %s", exc)

        try:
            from report_pack.report_collector import ReportCollector
            self._collector = ReportCollector()
        except Exception as exc:
            logger.warning("ReportPackAdapter: collector unavailable: %s", exc)

        try:
            from report_pack.report_health_checker import ReportHealthChecker
            self._health_checker = ReportHealthChecker()
        except Exception as exc:
            logger.warning("ReportPackAdapter: health_checker unavailable: %s", exc)

        try:
            from report_pack.report_link_registry import ReportLinkRegistry
            self._link_registry = ReportLinkRegistry()
        except Exception as exc:
            logger.warning("ReportPackAdapter: link_registry unavailable: %s", exc)

        try:
            from report_pack.report_pack_store import ReportPackStore
            self._store = ReportPackStore(output_dir=output_dir)
        except Exception as exc:
            logger.warning("ReportPackAdapter: store unavailable: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_pack(
        self,
        pack_type: str = "daily",
        report_date: Optional[str] = None,
        generate_missing: bool = False,
    ) -> dict:
        """Build a report pack and return its dict. generate_missing=False by default."""
        try:
            from report_pack.report_pack_builder import ReportPackBuilder
            builder = ReportPackBuilder(
                pack_type=pack_type,
                report_date=report_date,
                generate_missing=generate_missing,
            )
            pack = builder.build()
            pack_dict = pack.to_dict()

            # Persist to store
            if self._store:
                self._store.save_pack_summary(pack_dict)
                self._store.save_pack_items(
                    [i.to_dict() for i in pack.items], pack_type=pack_type
                )

            return pack_dict
        except Exception as exc:
            logger.warning("ReportPackAdapter.build_pack() failed: %s", exc)
            return {
                "pack_type":       pack_type,
                "status":          "FAILED",
                "error":           str(exc),
                "no_real_orders":  True,
            }

    def get_health(self, pack_type: str = "daily") -> dict:
        """Return health check dict for the most recent pack build."""
        try:
            if self._store is None or self._health_checker is None:
                return {"health_label": "UNKNOWN", "error": "Store or health checker unavailable"}

            # Build a fresh pack to get current state
            from report_pack.report_pack_builder import ReportPackBuilder
            builder = ReportPackBuilder(pack_type=pack_type)
            pack = builder.build()
            health = self._health_checker.check_pack(pack)

            if self._store:
                self._store.save_health_report(health)
            return health
        except Exception as exc:
            logger.warning("ReportPackAdapter.get_health() failed: %s", exc)
            return {"health_label": "UNKNOWN", "error": str(exc)}

    def get_links(self) -> list:
        """Return full link index."""
        try:
            if self._link_registry:
                return self._link_registry.build_link_index()
        except Exception as exc:
            logger.warning("ReportPackAdapter.get_links() failed: %s", exc)
        return []

    def generate_report(self, pack_type: str = "daily", mode: str = "real") -> str:
        """Generate the consolidation report. Returns path."""
        try:
            from reports.report_pack_consolidation_report import ReportPackConsolidationReport
            rpt = ReportPackConsolidationReport(
                report_dir=self.report_dir,
                output_dir=self.output_dir,
                mode=mode,
            )
            return rpt.generate(pack_type=pack_type, mode=mode)
        except Exception as exc:
            logger.warning("ReportPackAdapter.generate_report() failed: %s", exc)
            return ""

    def load_latest_summary(self) -> dict:
        try:
            if self._store:
                return self._store.load_latest_summary()
        except Exception as exc:
            logger.warning("ReportPackAdapter.load_latest_summary() failed: %s", exc)
        return {}

    def load_latest_items(self, pack_type: str = "") -> list:
        try:
            if self._store:
                return self._store.load_latest_items(pack_type)
        except Exception as exc:
            logger.warning("ReportPackAdapter.load_latest_items() failed: %s", exc)
        return []

    def load_latest_report_path(self) -> Optional[str]:
        try:
            if self._store:
                return self._store.load_latest_report_path()
        except Exception as exc:
            logger.warning("ReportPackAdapter.load_latest_report_path() failed: %s", exc)
        return None

    def list_pack_types(self) -> List[str]:
        try:
            if self._registry:
                return self._registry.list_pack_types()
        except Exception as exc:
            logger.warning("ReportPackAdapter.list_pack_types() failed: %s", exc)
        return ["daily", "weekly", "full", "custom"]

    def get_registry_info(self, pack_type: str) -> dict:
        """Return registry metadata for a pack type."""
        try:
            if self._registry:
                return {
                    "pack_type":     pack_type,
                    "report_types":  self._registry.get_report_types(pack_type),
                    "meta":          self._registry.get_pack_meta(pack_type),
                }
        except Exception as exc:
            logger.warning("ReportPackAdapter.get_registry_info() failed: %s", exc)
        return {"pack_type": pack_type, "report_types": [], "meta": {}}
