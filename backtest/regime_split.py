"""
backtest/regime_split.py — Market regime classification for hardened backtest (v0.3.26).

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    import numpy as np
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False
    logger.warning("pandas/numpy not available — MarketRegimeSplitter will operate in degraded mode")

REGIME_PROXY = "proxy"


class MarketRegimeSplitter:
    """
    Market regime classifier for hardened backtesting.

    Classifies market days into:
    - bull: close > MA60 AND MA20 > MA60
    - bear: close < MA60 AND MA20 < MA60
    - sideways: between bull and bear conditions
    - high_volatility: rolling 20-day return std > volatility_threshold (checked first)
    - unknown: insufficient data

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    REGIMES = ("bull", "bear", "sideways", "high_volatility", "unknown")

    def __init__(
        self,
        ma_short: int = 20,
        ma_long: int = 60,
        volatility_window: int = 20,
        volatility_threshold: float = 0.02,
    ) -> None:
        self.ma_short = ma_short
        self.ma_long = ma_long
        self.volatility_window = volatility_window
        self.volatility_threshold = volatility_threshold

    # ------------------------------------------------------------------
    # Regime classification
    # ------------------------------------------------------------------

    def classify_regime(self, market_df) -> "pd.DataFrame | None":
        """
        Classify market regime for each date.

        Args:
            market_df: DataFrame with 'close' column and date index or 'date' column

        Returns:
            DataFrame with columns: date, regime, ma_short, ma_long, rolling_vol, is_proxy
        """
        if not _PANDAS_AVAILABLE:
            logger.warning("classify_regime: pandas unavailable")
            return None

        fallback_cols = ["date", "regime", f"ma_{self.ma_short}", f"ma_{self.ma_long}", "rolling_vol", "is_proxy"]

        try:
            if market_df is None or (hasattr(market_df, "empty") and market_df.empty):
                logger.warning("classify_regime: no market data, returning proxy regime")
                return self._build_proxy_regime(None)

            df = market_df.copy()
            df.columns = [c.lower() for c in df.columns]

            if "date" in df.columns:
                df = df.set_index("date")
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index, errors="coerce")
                df = df[~df.index.isna()]
            df = df.sort_index()

            if "close" not in df.columns:
                logger.warning("classify_regime: 'close' column missing")
                return self._build_proxy_regime(None)

            # Compute indicators
            df[f"ma_{self.ma_short}"] = df["close"].rolling(self.ma_short, min_periods=1).mean()
            df[f"ma_{self.ma_long}"] = df["close"].rolling(self.ma_long, min_periods=1).mean()
            df["daily_return"] = df["close"].pct_change()
            df["rolling_vol"] = df["daily_return"].rolling(self.volatility_window, min_periods=1).std()

            ma_s = f"ma_{self.ma_short}"
            ma_l = f"ma_{self.ma_long}"

            def _classify_row(row) -> str:
                try:
                    rv = row.get("rolling_vol", 0) or 0
                    c = row.get("close", None)
                    ms = row.get(ma_s, None)
                    ml = row.get(ma_l, None)

                    if rv > self.volatility_threshold:
                        return "high_volatility"
                    if c is None or ms is None or ml is None:
                        return "unknown"
                    if pd.isna(c) or pd.isna(ms) or pd.isna(ml):
                        return "unknown"
                    if c > ml and ms > ml:
                        return "bull"
                    if c < ml and ms < ml:
                        return "bear"
                    return "sideways"
                except Exception:
                    return "unknown"

            df["regime"] = df.apply(_classify_row, axis=1)
            df["is_proxy"] = False
            df.index = df.index.strftime("%Y-%m-%d")
            df = df.reset_index().rename(columns={"index": "date"})

            keep_cols = ["date", "regime", ma_s, ma_l, "rolling_vol", "is_proxy"]
            result_cols = [c for c in keep_cols if c in df.columns]
            return df[result_cols]

        except Exception as exc:
            logger.error("classify_regime error: %s", exc)
            return self._build_proxy_regime(None)

    # ------------------------------------------------------------------
    # Assign regime to trades
    # ------------------------------------------------------------------

    def assign_regime_to_trades(self, trades_df, market_df) -> "pd.DataFrame":
        """
        Join regime classification onto trades by entry_date.

        Returns trades_df with 'regime' column added.
        """
        if not _PANDAS_AVAILABLE:
            logger.warning("assign_regime_to_trades: pandas unavailable")
            return trades_df

        try:
            regime_df = self.classify_regime(market_df)

            if trades_df is None or (hasattr(trades_df, "empty") and trades_df.empty):
                return trades_df

            df = trades_df.copy()

            if regime_df is None or (hasattr(regime_df, "empty") and regime_df.empty):
                df["regime"] = "unknown"
                return df

            regime_map = dict(zip(regime_df["date"].astype(str), regime_df["regime"]))

            if "entry_date" in df.columns:
                df["regime"] = df["entry_date"].astype(str).map(regime_map).fillna("unknown")
            else:
                df["regime"] = "unknown"

            return df

        except Exception as exc:
            logger.error("assign_regime_to_trades error: %s", exc)
            if trades_df is not None:
                try:
                    trades_df["regime"] = "unknown"
                    return trades_df
                except Exception:
                    pass
            return trades_df

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def get_regime_summary(self, regime_df) -> dict:
        """
        Return a summary of regime day counts.

        Returns:
            bull_days, bear_days, sideways_days, high_volatility_days, unknown_days, proxy_used
        """
        result = {
            "bull_days": 0,
            "bear_days": 0,
            "sideways_days": 0,
            "high_volatility_days": 0,
            "unknown_days": 0,
            "proxy_used": False,
        }

        if not _PANDAS_AVAILABLE or regime_df is None:
            return result

        try:
            if hasattr(regime_df, "empty") and regime_df.empty:
                return result

            if "regime" in regime_df.columns:
                counts = regime_df["regime"].value_counts().to_dict()
                result["bull_days"] = int(counts.get("bull", 0))
                result["bear_days"] = int(counts.get("bear", 0))
                result["sideways_days"] = int(counts.get("sideways", 0))
                result["high_volatility_days"] = int(counts.get("high_volatility", 0))
                result["unknown_days"] = int(counts.get("unknown", 0))

            if "is_proxy" in regime_df.columns:
                result["proxy_used"] = bool(regime_df["is_proxy"].any())

            return result

        except Exception as exc:
            logger.error("get_regime_summary error: %s", exc)
            return result

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def build_assumption_dict(self) -> dict:
        """Return all model parameters as a dictionary for reporting."""
        return {
            "ma_short": self.ma_short,
            "ma_long": self.ma_long,
            "volatility_window": self.volatility_window,
            "volatility_threshold": self.volatility_threshold,
            "regime_rules": {
                "high_volatility": f"rolling_vol > {self.volatility_threshold} (checked first)",
                "bull": f"close > MA{self.ma_long} AND MA{self.ma_short} > MA{self.ma_long}",
                "bear": f"close < MA{self.ma_long} AND MA{self.ma_short} < MA{self.ma_long}",
                "sideways": "else",
            },
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_proxy_regime(self, dates) -> "pd.DataFrame | None":
        """Build a proxy regime DataFrame when market data is unavailable."""
        if not _PANDAS_AVAILABLE:
            return None
        try:
            if dates:
                data = [{"date": str(d), "regime": "unknown", "is_proxy": True} for d in dates]
            else:
                data = []
            df = pd.DataFrame(data)
            if df.empty:
                return df
            ma_s_col = f"ma_{self.ma_short}"
            ma_l_col = f"ma_{self.ma_long}"
            df[ma_s_col] = None
            df[ma_l_col] = None
            df["rolling_vol"] = None
            return df
        except Exception as exc:
            logger.error("_build_proxy_regime error: %s", exc)
            return None
