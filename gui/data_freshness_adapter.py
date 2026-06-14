"""
gui/data_freshness_adapter.py — GUI adapter for Data Freshness Monitor v1.1.3.
[!] Research Only. No Real Orders. No Auto Download. No Auto Repair.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
AUTO_DOWNLOAD_DISABLED = True
AUTO_REPAIR_DISABLED = True


class DataFreshnessAdapter:
    """
    Bridges DataFreshnessEngine to the GUI panel.
    [!] All methods are read-only. No data modification.
    [!] No broker. No real orders. No automatic download.
    """

    def __init__(self):
        self._engine = None
        self._store = None
        self._query = None

    def _get_engine(self):
        if self._engine is None:
            from data_freshness.freshness_engine import DataFreshnessEngine
            self._engine = DataFreshnessEngine()
        return self._engine

    def _get_store(self):
        if self._store is None:
            from data_freshness.freshness_store import FreshnessStore
            self._store = FreshnessStore()
        return self._store

    def _get_query(self):
        if self._query is None:
            from data_freshness.freshness_query import FreshnessQuery
            self._query = FreshnessQuery(store=self._get_store())
        return self._query

    def run_scan(self, tier=None, symbols=None, mode="real") -> Dict:
        """Run freshness scan. Does NOT download data or execute repairs."""
        try:
            return self._get_engine().run(tier=tier, symbols=symbols, mode=mode)
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.run_scan error: {e}")
            return {"records": [], "alerts": [], "source_health": [], "summary": None}

    def get_latest_summary(self) -> Optional[Dict]:
        try:
            summary = self._get_query().latest_summary()
            return summary.to_dict() if summary else None
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.get_latest_summary error: {e}")
            return None

    def get_stale_list(self) -> List[Dict]:
        try:
            return [r.to_dict() for r in self._get_query().list_stale()]
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.get_stale_list error: {e}")
            return []

    def get_open_alerts(self) -> List[Dict]:
        try:
            return [a.to_dict() for a in self._get_query().list_open_alerts()]
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.get_open_alerts error: {e}")
            return []

    def get_source_interruptions(self) -> List[Dict]:
        try:
            return [s.to_dict() for s in self._get_query().list_source_interruptions()]
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.get_source_interruptions error: {e}")
            return []

    def create_repair_handoff(self, alerts=None) -> List[Dict]:
        """
        Creates repair handoff tasks from alerts.
        [!] Does NOT execute repair. Tasks only.
        [!] No real orders. No broker.
        """
        try:
            if alerts is None:
                raw_alerts = self._get_query().list_open_alerts()
            else:
                raw_alerts = alerts
            return self._get_engine().create_repair_handoff(raw_alerts)
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.create_repair_handoff error: {e}")
            return []

    def build_report(self, tier=None, mode="real") -> Optional[str]:
        """Build Markdown freshness report. Returns path or None."""
        try:
            result = self.run_scan(tier=tier, mode=mode)
            from reports.data_freshness_report import DataFreshnessReportBuilder
            builder = DataFreshnessReportBuilder()
            return builder.build(
                result.get("records", []),
                result.get("alerts", []),
                result.get("source_health", []),
                result.get("summary"),
            )
        except Exception as e:
            logger.warning(f"DataFreshnessAdapter.build_report error: {e}")
            return None

    def get_safe_cli_commands(self) -> List[Dict]:
        """Return safe read-only CLI commands for Local Assistant routing."""
        return [
            {"cmd": "python main.py freshness-health", "label": "Freshness health check", "safe": True},
            {"cmd": "python main.py freshness-summary --tier research30", "label": "Freshness summary", "safe": True},
            {"cmd": "python main.py freshness-stale", "label": "List stale symbols", "safe": True},
            {"cmd": "python main.py freshness-source-health", "label": "Source health status", "safe": True},
            {"cmd": "python main.py coverage-repair-source-required", "label": "Coverage repair source required", "safe": True},
        ]
