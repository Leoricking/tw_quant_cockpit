"""
data/tick_bidask_interface.py - Future tick / bid-ask provider interface.

v0.3.9 status: PLANNED / NOT CONFIGURED.

This module defines the standard schema for tick and bid-ask data that
will be populated in a future phase when a real-time or historical tick
data source is available (e.g., broker API or third-party vendor).

Current behaviour:
    - All methods return None / empty DataFrame.
    - provider-status shows PLANNED / NOT CONFIGURED.
    - No real tick or bid-ask data is fabricated.

Standard tick columns:
    symbol, datetime, price, volume, side, source

Standard bidask columns:
    symbol, datetime, bid_price_1, bid_size_1, ask_price_1, ask_size_1,
    bid_total_size, ask_total_size, source
"""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# Provider status constants
TICK_PROVIDER_STATUS = "PLANNED"
BIDASK_PROVIDER_STATUS = "NOT CONFIGURED"

# Standard column schemas
TICK_COLUMNS = ["symbol", "datetime", "price", "volume", "side", "source"]
BIDASK_COLUMNS = [
    "symbol",
    "datetime",
    "bid_price_1",
    "bid_size_1",
    "ask_price_1",
    "ask_size_1",
    "bid_total_size",
    "ask_total_size",
    "source",
]


def empty_tick_df() -> pd.DataFrame:
    """Return an empty DataFrame with standard tick columns."""
    return pd.DataFrame(columns=TICK_COLUMNS)


def empty_bidask_df() -> pd.DataFrame:
    """Return an empty DataFrame with standard bid-ask columns."""
    return pd.DataFrame(columns=BIDASK_COLUMNS)


class TickBidaskInterface:
    """
    Future tick / bid-ask provider interface.

    All methods return None or empty DataFrames — no real data is
    fabricated.  Use provider_status() to display current availability.
    """

    name: str = "tick_bidask"
    is_available: bool = False
    is_planned: bool = True

    def get_ticks(
        self,
        symbol: str,
        date: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Return tick-by-tick data for one trading date.

        Not yet implemented.  Returns None with a debug log.
        """
        logger.debug(
            "TickBidaskInterface.get_ticks: PLANNED — symbol=%s date=%s",
            symbol,
            date,
        )
        return None

    def get_bidask(
        self,
        symbol: str,
    ) -> Optional[pd.DataFrame]:
        """
        Return latest bid-ask snapshot.

        Not yet implemented.  Returns None with a debug log.
        """
        logger.debug(
            "TickBidaskInterface.get_bidask: NOT CONFIGURED — symbol=%s",
            symbol,
        )
        return None

    def provider_status(self) -> dict:
        """Return provider status dict."""
        return {
            "tick_provider": TICK_PROVIDER_STATUS,
            "bidask_provider": BIDASK_PROVIDER_STATUS,
            "is_available": False,
            "is_planned": True,
            "note": (
                "Tick and bid-ask data are future interfaces. "
                "No real data is available or fabricated in v0.3.9."
            ),
        }

    def health_check(self) -> dict:
        """Return health check dict compatible with BaseMarketDataProvider."""
        return {
            "ok": False,
            "provider": self.name,
            "available": False,
            "planned": True,
            "real_order": False,
            "tick_status": TICK_PROVIDER_STATUS,
            "bidask_status": BIDASK_PROVIDER_STATUS,
            "note": "Tick/BidAsk — PLANNED / NOT CONFIGURED",
        }
