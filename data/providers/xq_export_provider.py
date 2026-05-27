"""
data/providers/xq_export_provider.py - XQ technical-analysis export provider.

Wraps the existing XQExportImporter so XQ exports appear as a standard
BaseMarketDataProvider to downstream modules.

Role in the architecture:
    Transition / fallback provider.  Once TWSE OpenAPI or another live data
    feed is wired up, this provider becomes optional.  It is kept so that
    users who already have XQ exports can continue to use them without
    changing their workflow.

Limitations:
    - get_daily() returns data only if an XQ file has been previously
      imported via 'import-xq-export' command (data lives in data/import/).
    - get_intraday(), get_ticks(), get_bidask() always return None — XQ
      batch exports do not contain tick / intraday / bid-ask data.
    - No real-time capability.
    - No order submission (read-only).
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import pandas as pd

from data.providers.base_provider import BaseMarketDataProvider
from data.providers.csv_provider import CSVProvider

logger = logging.getLogger(__name__)


class XQExportProvider(BaseMarketDataProvider):
    """
    Provider backed by XQ-exported data that was imported via import-xq-export.

    Internally delegates to CSVProvider because XQ imports land in the same
    data/import/ directory structure.  This class adds XQ-specific metadata
    and a dedicated health_check() message.
    """

    name = "xq_export"
    is_available = True
    is_planned = False

    def __init__(self):
        # XQ data lands in the same CSV directory after import-xq-export.
        self._csv = CSVProvider()

    def get_daily(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Return daily OHLCV data previously imported from XQ exports.

        Returns None if the symbol has not been imported yet.
        """
        return self._csv.get_daily(symbol, start=start, end=end)

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        return self._csv.get_institutional(symbol, start=start, end=end)

    def get_margin(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        return self._csv.get_margin(symbol, start=start, end=end)

    def get_monthly_revenue(
        self, symbol: str, months: int = 24
    ) -> Optional[pd.DataFrame]:
        return self._csv.get_monthly_revenue(symbol, months=months)

    def get_holder(self, symbol: str) -> Optional[pd.DataFrame]:
        return self._csv.get_holder(symbol)

    def get_trust_cost(self, symbol: str) -> Optional[pd.DataFrame]:
        return self._csv.get_trust_cost(symbol)

    def get_profile(self, symbol: str) -> Optional[dict]:
        return self._csv.get_profile(symbol)

    def health_check(self) -> dict:
        csv_status = self._csv.health_check()
        xq_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data", "xq_exports",
        )
        return {
            "ok": csv_status["ok"],
            "provider": self.name,
            "available": csv_status["available"],
            "planned": False,
            "real_order": False,
            "xq_exports_dir": xq_dir,
            "xq_exports_exist": os.path.isdir(xq_dir),
            "note": (
                "XQ export transition provider — delegates to CSV data/import/. "
                "Will be optional once live API feeds are wired."
            ),
        }
