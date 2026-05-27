"""
data/providers/twse_openapi_provider.py - TWSE / TPEx / MOPS / data.gov.tw provider skeleton.

STATUS: PLANNED — not active in v0.3.4.

This file reserves the interface for future integration with Taiwan's public
market data APIs:

    TWSE Open API      : https://openapi.twse.com.tw/
    TPEx Open API      : https://www.tpex.org.tw/openapi/
    MOPS              : https://mops.twse.com.tw/
    data.gov.tw        : https://data.gov.tw/

Implementation roadmap (v0.4):
    1. Daily OHLCV from TWSE / TPEx open API (no auth required).
    2. Monthly revenue from MOPS (public disclosure).
    3. Company fundamentals from data.gov.tw datasets.
    4. Proper announcement-date alignment to prevent revenue leakage.

Safety:
    - Real order execution is PERMANENTLY DISABLED.
    - This provider never submits orders to any exchange.
    - All methods return None until implemented.
    - Network errors must not crash the system.

TODO (v0.4):
    - Implement get_daily() with TWSE open API fetch.
    - Implement get_monthly_revenue() with MOPS scrape / API.
    - Add announcement_date column to prevent forward-look leakage.
    - Add rate-limiting and caching layer.
    - Add --provider twse CLI flag to data-check / stock-report.
"""

from __future__ import annotations

import logging
from typing import Optional

from data.providers.base_provider import BaseMarketDataProvider

logger = logging.getLogger(__name__)


class TWSEOpenAPIProvider(BaseMarketDataProvider):
    """
    Skeleton provider for TWSE / TPEx / MOPS public APIs.

    All methods return None until v0.4 implementation is complete.
    The system will not crash when this provider is selected — it degrades
    gracefully by returning None for every data request.
    """

    name = "twse_openapi"
    is_available = False
    is_planned = True

    def get_daily(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """
        TODO (v0.4): Fetch daily OHLCV from TWSE / TPEx Open API.

        Planned endpoint (TWSE):
            GET https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY
            Params: stockNo={symbol}, date={YYYYMMDD}

        Returns None until implemented.
        """
        logger.debug(
            "TWSEOpenAPIProvider.get_daily: not implemented — returning None. "
            "(symbol=%s, start=%s, end=%s)", symbol, start, end
        )
        return None

    def get_monthly_revenue(self, symbol: str, months: int = 24):
        """
        TODO (v0.4): Fetch monthly revenue from MOPS.

        Note: Must align on announcement_date (released after month end)
        to prevent forward-looking leakage in backtests.

        Returns None until implemented.
        """
        logger.debug(
            "TWSEOpenAPIProvider.get_monthly_revenue: not implemented — returning None."
        )
        return None

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """
        TODO (v0.4): Fetch institutional flows from TWSE open API.

        Returns None until implemented.
        """
        return None

    def health_check(self) -> dict:
        return {
            "ok": False,
            "provider": self.name,
            "available": False,
            "planned": True,
            "real_order": False,
            "note": (
                "PLANNED for v0.4 — TWSE / TPEx / MOPS public API. "
                "Not yet configured. System operates on CSV data in the meantime."
            ),
        }
