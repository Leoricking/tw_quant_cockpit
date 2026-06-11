"""
gui/data_report_hygiene_adapter.py — DataReportHygieneAdapter for v1.0.2.

Adapter for the Data & Report Hygiene panel. Review-only.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DataReportHygieneAdapter:
    """Adapter for Data & Report Hygiene data in the GUI.

    [!] Research Only. No Real Orders. Review Only.
    """

    no_real_orders     = True
    production_blocked = True
    review_only        = True
    data_cleanup_review_only = True
    archive_suggestions_only = True

    def __init__(self, output_dir: str = "data/backtest_results/maintenance") -> None:
        self._output_dir = output_dir

    def load_summary(self) -> Optional[Dict[str, Any]]:
        """Load the latest hygiene summary from the store."""
        try:
            from maintenance.data_report_hygiene_store import DataReportHygieneStore
            store   = DataReportHygieneStore(output_dir=self._output_dir)
            summary = store.load_latest_summary()
            if summary is None:
                return None
            return summary.to_dict()
        except Exception as exc:
            logger.warning("DataReportHygieneAdapter.load_summary error: %s", exc)
            return None

    def load_safe_commands(self) -> List[str]:
        """Return list of safe CLI commands for this module.

        These commands do not trigger any real orders or broker actions.
        """
        return [
            "data-report-hygiene --mode real",
            "data-report-hygiene-summary",
            "data-report-hygiene-inventory",
            "data-report-hygiene-reports",
            "data-report-hygiene-gitignore",
            "data-report-hygiene-tracked",
            "data-report-hygiene-stale",
            "data-report-hygiene-large-files",
            "data-report-hygiene-report --mode real",
        ]
