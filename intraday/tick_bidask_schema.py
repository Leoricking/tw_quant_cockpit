"""
intraday/tick_bidask_schema.py — Tick and BidAsk schema placeholders (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
[!] First version: schema definition and validation only. No API fetch implemented.
"""

from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("pandas not available — TickBidAskSchema will be limited")


class TickBidAskSchema:
    """
    Schema definitions and validation for tick and bid/ask data.

    In v0.3.27 no live tick or bid/ask data provider is connected.
    This class defines the expected schema and provides validation utilities
    for when data becomes available in a future version.

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] First version: schema definition and validation only. No API fetch implemented.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    tick_api_ready      : False  — tick provider not yet connected
    bidask_api_ready    : False  — bid/ask provider not yet connected
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    tick_api_ready: bool = False
    bidask_api_ready: bool = False

    TICK_REQUIRED: List[str] = [
        "symbol", "date", "time", "datetime", "price", "volume", "source",
    ]
    TICK_OPTIONAL: List[str] = [
        "amount", "side", "is_large_trade",
    ]

    BIDASK_REQUIRED: List[str] = [
        "symbol", "date", "time", "datetime",
        "bid_price_1", "bid_volume_1",
        "ask_price_1", "ask_volume_1",
        "source",
    ]
    BIDASK_OPTIONAL: List[str] = [
        "bid_price_2", "bid_price_3", "bid_price_4", "bid_price_5",
        "bid_volume_2", "bid_volume_3", "bid_volume_4", "bid_volume_5",
        "ask_price_2", "ask_price_3", "ask_price_4", "ask_price_5",
        "ask_volume_2", "ask_volume_3", "ask_volume_4", "ask_volume_5",
        "spread", "order_imbalance",
    ]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_tick(self, df) -> dict:
        """
        Validate a DataFrame against the tick schema.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        dict with keys: ok, missing_required, extra_columns, row_count, warnings
        """
        return self._validate(df, self.TICK_REQUIRED, self.TICK_OPTIONAL, "tick")

    def validate_bidask(self, df) -> dict:
        """
        Validate a DataFrame against the bid/ask schema.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        dict with keys: ok, missing_required, extra_columns, row_count, warnings
        """
        return self._validate(df, self.BIDASK_REQUIRED, self.BIDASK_OPTIONAL, "bidask")

    def _validate(
        self,
        df,
        required: List[str],
        optional: List[str],
        schema_name: str,
    ) -> dict:
        """Generic validation helper."""
        if not _PANDAS_OK:
            return {
                "ok": False,
                "missing_required": required,
                "extra_columns": [],
                "row_count": 0,
                "warnings": ["pandas not available"],
            }
        if df is None or (hasattr(df, "empty") and df.empty):
            return {
                "ok": False,
                "missing_required": required,
                "extra_columns": [],
                "row_count": 0,
                "warnings": [f"{schema_name}: DataFrame is None or empty"],
            }

        cols = list(df.columns)
        all_known = required + optional
        missing_required = [c for c in required if c not in cols]
        extra_columns = [c for c in cols if c not in all_known]
        warnings = []
        if missing_required:
            warnings.append(f"{schema_name}: Missing required columns: {missing_required}")
        if extra_columns:
            warnings.append(f"{schema_name}: Extra/unknown columns: {extra_columns}")

        return {
            "ok": len(missing_required) == 0,
            "missing_required": missing_required,
            "extra_columns": extra_columns,
            "row_count": len(df),
            "warnings": warnings,
        }

    # ------------------------------------------------------------------
    # Readiness
    # ------------------------------------------------------------------

    def get_readiness_status(self) -> dict:
        """
        Return the provider readiness status for tick and bid/ask data.

        Returns
        -------
        dict
        """
        return {
            "tick_ready": False,
            "bidask_ready": False,
            "tick_planned": True,
            "bidask_planned": True,
            "note": (
                "Tick and BidAsk providers planned for future version. "
                "Not available in v0.3.27."
            ),
        }

    # ------------------------------------------------------------------
    # Empty DataFrame factories
    # ------------------------------------------------------------------

    def create_empty_tick_df(self):
        """
        Create an empty DataFrame with all tick schema columns.

        Returns
        -------
        pd.DataFrame
        """
        if not _PANDAS_OK:
            raise RuntimeError("pandas is required to create an empty tick DataFrame")
        all_cols = self.TICK_REQUIRED + self.TICK_OPTIONAL
        return pd.DataFrame(columns=all_cols)

    def create_empty_bidask_df(self):
        """
        Create an empty DataFrame with all bid/ask schema columns.

        Returns
        -------
        pd.DataFrame
        """
        if not _PANDAS_OK:
            raise RuntimeError("pandas is required to create an empty bidask DataFrame")
        all_cols = self.BIDASK_REQUIRED + self.BIDASK_OPTIONAL
        return pd.DataFrame(columns=all_cols)
