"""
backtest/execution_model.py — Execution model for hardened backtest (v0.3.26).

Resolves entry/exit prices and applies stop-loss, take-profit, trailing stop,
and time stop logic for backtesting purposes.

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
    logger.warning("pandas/numpy not available — ExecutionModel will operate in degraded mode")


class ExecutionModel:
    """
    Execution model for hardened backtesting.

    Resolves entry/exit prices and applies stop-loss, take-profit,
    trailing stop, and time stop logic.

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    VALID_ENTRY_MODELS = ("signal_close", "next_open", "next_close", "vwap_proxy")
    VALID_EXIT_MODELS = ("fixed_holding_days", "combined")

    def __init__(
        self,
        entry_model: str = "next_open",
        exit_model: str = "combined",
        allow_same_day_entry: bool = False,
        max_holding_days: int = 20,
        stop_loss_pct: float | None = None,
        take_profit_pct: float | None = None,
        trailing_stop_pct: float | None = None,
        time_stop_days: int | None = None,
    ) -> None:
        if entry_model not in self.VALID_ENTRY_MODELS:
            logger.warning("Unknown entry_model '%s', defaulting to 'next_open'", entry_model)
            entry_model = "next_open"
        if exit_model not in self.VALID_EXIT_MODELS:
            logger.warning("Unknown exit_model '%s', defaulting to 'combined'", exit_model)
            exit_model = "combined"

        self.entry_model = entry_model
        self.exit_model = exit_model
        self.allow_same_day_entry = allow_same_day_entry
        self.max_holding_days = max_holding_days
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.trailing_stop_pct = trailing_stop_pct
        self.time_stop_days = time_stop_days

    # ------------------------------------------------------------------
    # Entry resolution
    # ------------------------------------------------------------------

    def resolve_entry_price(
        self,
        price_df,
        signal_date: str,
        symbol: str | None = None,
    ) -> dict:
        """
        Resolve the entry price based on entry_model.

        Returns a dict with keys:
            price, date, status, assumption
        """
        assumption = (
            f"entry_model={self.entry_model}; "
            f"allow_same_day_entry={self.allow_same_day_entry}"
        )
        empty = {
            "price": None,
            "date": None,
            "status": "MISSING_ENTRY_PRICE",
            "assumption": assumption,
        }

        if not _PANDAS_AVAILABLE:
            logger.warning("pandas unavailable — cannot resolve entry price")
            return empty

        try:
            df = self._normalize_df(price_df)
            if df is None or df.empty:
                return {**empty, "status": "MISSING_ENTRY_PRICE"}

            # Locate signal date
            if signal_date not in df.index:
                return {**empty, "status": "SIGNAL_DATE_NOT_FOUND"}

            signal_loc = df.index.get_loc(signal_date)

            if self.entry_model == "signal_close":
                row = df.iloc[signal_loc]
                price = self._safe_get(row, "close")
                if price is None:
                    return {**empty, "status": "MISSING_ENTRY_PRICE"}
                return {
                    "price": float(price),
                    "date": str(df.index[signal_loc]),
                    "status": "OK",
                    "assumption": assumption,
                }

            # All other models need next trading day
            next_loc = signal_loc + 1
            if next_loc >= len(df):
                return {**empty, "status": "MISSING_ENTRY_PRICE"}

            next_row = df.iloc[next_loc]
            next_date = str(df.index[next_loc])

            if self.entry_model == "next_open":
                price = self._safe_get(next_row, "open")
                if price is None:
                    price = self._safe_get(next_row, "close")
                    assumption += "; open missing, fallback to next_close"
            elif self.entry_model == "next_close":
                price = self._safe_get(next_row, "close")
            elif self.entry_model == "vwap_proxy":
                h = self._safe_get(next_row, "high")
                l = self._safe_get(next_row, "low")
                c = self._safe_get(next_row, "close")
                if h is not None and l is not None and c is not None:
                    price = (h + l + c) / 3.0
                    assumption += "; vwap_proxy=(high+low+close)/3"
                else:
                    price = c
                    assumption += "; vwap_proxy fallback to close"
            else:
                price = self._safe_get(next_row, "close")

            if price is None:
                return {**empty, "status": "MISSING_ENTRY_PRICE"}

            return {
                "price": float(price),
                "date": next_date,
                "status": "OK",
                "assumption": assumption,
            }

        except Exception as exc:
            logger.error("resolve_entry_price error: %s", exc)
            return {**empty, "status": "MISSING_ENTRY_PRICE"}

    # ------------------------------------------------------------------
    # Exit resolution
    # ------------------------------------------------------------------

    def resolve_exit_price(
        self,
        price_df,
        entry_date: str,
        entry_price: float,
        symbol: str | None = None,
    ) -> dict:
        """
        Resolve exit price based on exit_model and stop rules.

        Returns a dict with keys:
            price, exit_date, exit_reason, status, assumption
        """
        assumption = (
            f"exit_model={self.exit_model}; "
            f"max_holding_days={self.max_holding_days}; "
            f"stop_loss_pct={self.stop_loss_pct}; "
            f"take_profit_pct={self.take_profit_pct}; "
            f"trailing_stop_pct={self.trailing_stop_pct}; "
            f"time_stop_days={self.time_stop_days}"
        )
        empty = {
            "price": None,
            "exit_date": None,
            "exit_reason": "INSUFFICIENT_DATA",
            "status": "INSUFFICIENT_DATA",
            "assumption": assumption,
        }

        if not _PANDAS_AVAILABLE:
            return empty

        try:
            df = self._normalize_df(price_df)
            if df is None or df.empty:
                return empty

            if entry_date not in df.index:
                return empty

            entry_loc = df.index.get_loc(entry_date)
            holding_df = df.iloc[entry_loc + 1 : entry_loc + 1 + self.max_holding_days]

            if holding_df.empty:
                return empty

            if self.exit_model == "fixed_holding_days":
                last_row = holding_df.iloc[-1]
                price = self._safe_get(last_row, "close")
                if price is None:
                    return empty
                return {
                    "price": float(price),
                    "exit_date": str(holding_df.index[-1]),
                    "exit_reason": "max_holding_days",
                    "status": "OK",
                    "assumption": assumption,
                }

            # combined: check all stops in order
            candidates = []

            sl = self.apply_stop_loss(holding_df, entry_price)
            if sl and sl["triggered"]:
                candidates.append(
                    (sl["trigger_date"], sl["trigger_price"], "stop_loss")
                )

            tp = self.apply_take_profit(holding_df, entry_price)
            if tp and tp["triggered"]:
                candidates.append(
                    (tp["trigger_date"], tp["trigger_price"], "take_profit")
                )

            ts = self.apply_trailing_stop(holding_df, entry_price)
            if ts and ts["triggered"]:
                candidates.append(
                    (ts["trigger_date"], ts["trigger_price"], "trailing_stop")
                )

            ti = self.apply_time_stop(holding_df, entry_date)
            if ti and ti["triggered"]:
                candidates.append(
                    (ti["trigger_date"], ti["trigger_price"], "time_stop")
                )

            if candidates:
                # Pick the earliest trigger
                candidates.sort(key=lambda x: x[0])
                exit_date, exit_price, reason = candidates[0]
                if exit_price is None:
                    return empty
                return {
                    "price": float(exit_price),
                    "exit_date": exit_date,
                    "exit_reason": reason,
                    "status": "OK",
                    "assumption": assumption,
                }

            # Fallback: end of holding period
            last_row = holding_df.iloc[-1]
            price = self._safe_get(last_row, "close")
            if price is None:
                return empty
            return {
                "price": float(price),
                "exit_date": str(holding_df.index[-1]),
                "exit_reason": "max_holding_days",
                "status": "OK",
                "assumption": assumption,
            }

        except Exception as exc:
            logger.error("resolve_exit_price error: %s", exc)
            return empty

    # ------------------------------------------------------------------
    # Stop rules
    # ------------------------------------------------------------------

    def apply_stop_loss(self, holding_df, entry_price: float) -> dict | None:
        """Apply stop-loss rule to holding period DataFrame."""
        if self.stop_loss_pct is None:
            return None
        if not _PANDAS_AVAILABLE:
            return None

        try:
            stop_level = entry_price * (1.0 - self.stop_loss_pct)
            has_low = "low" in holding_df.columns
            has_high = "high" in holding_df.columns
            model = "intraday" if has_low else "close_only"

            for date_idx, row in holding_df.iterrows():
                check_col = "low" if has_low else "close"
                val = self._safe_get(row, check_col)
                if val is not None and val < stop_level:
                    # Exit at stop level (or open if gapped below)
                    exit_price = stop_level
                    if has_low:
                        low_val = self._safe_get(row, "low")
                        if low_val is not None and low_val < stop_level:
                            exit_price = stop_level
                    else:
                        close_val = self._safe_get(row, "close")
                        if close_val is not None:
                            exit_price = close_val
                    return {
                        "triggered": True,
                        "trigger_date": str(date_idx),
                        "trigger_price": float(exit_price),
                        "model": model,
                    }
            return {"triggered": False, "trigger_date": None, "trigger_price": None, "model": model}
        except Exception as exc:
            logger.error("apply_stop_loss error: %s", exc)
            return None

    def apply_take_profit(self, holding_df, entry_price: float) -> dict | None:
        """Apply take-profit rule to holding period DataFrame."""
        if self.take_profit_pct is None:
            return None
        if not _PANDAS_AVAILABLE:
            return None

        try:
            tp_level = entry_price * (1.0 + self.take_profit_pct)
            has_high = "high" in holding_df.columns
            model = "intraday" if has_high else "close_only"

            for date_idx, row in holding_df.iterrows():
                check_col = "high" if has_high else "close"
                val = self._safe_get(row, check_col)
                if val is not None and val >= tp_level:
                    exit_price = tp_level
                    return {
                        "triggered": True,
                        "trigger_date": str(date_idx),
                        "trigger_price": float(exit_price),
                        "model": model,
                    }
            return {"triggered": False, "trigger_date": None, "trigger_price": None, "model": model}
        except Exception as exc:
            logger.error("apply_take_profit error: %s", exc)
            return None

    def apply_trailing_stop(self, holding_df, entry_price: float) -> dict | None:
        """Apply trailing stop rule to holding period DataFrame."""
        if self.trailing_stop_pct is None:
            return None
        if not _PANDAS_AVAILABLE:
            return None

        try:
            has_high = "high" in holding_df.columns
            has_low = "low" in holding_df.columns
            peak = entry_price

            for date_idx, row in holding_df.iterrows():
                # Update peak
                if has_high:
                    h = self._safe_get(row, "high")
                    if h is not None and h > peak:
                        peak = h
                else:
                    c = self._safe_get(row, "close")
                    if c is not None and c > peak:
                        peak = c

                # Check trigger
                trail_level = peak * (1.0 - self.trailing_stop_pct)
                check_val = self._safe_get(row, "low") if has_low else self._safe_get(row, "close")
                if check_val is None:
                    check_val = self._safe_get(row, "close")

                if check_val is not None and check_val < trail_level:
                    exit_price = trail_level
                    return {
                        "triggered": True,
                        "trigger_date": str(date_idx),
                        "trigger_price": float(exit_price),
                        "model": "trailing_stop",
                    }
            return {"triggered": False, "trigger_date": None, "trigger_price": None, "model": "trailing_stop"}
        except Exception as exc:
            logger.error("apply_trailing_stop error: %s", exc)
            return None

    def apply_time_stop(self, holding_df, entry_date: str) -> dict | None:
        """Apply time-based stop rule."""
        if self.time_stop_days is None:
            return None
        if not _PANDAS_AVAILABLE:
            return None

        try:
            if len(holding_df) >= self.time_stop_days:
                exit_row = holding_df.iloc[self.time_stop_days - 1]
                exit_date = str(holding_df.index[self.time_stop_days - 1])
                exit_price = self._safe_get(exit_row, "close")
                if exit_price is None:
                    return {"triggered": False, "trigger_date": None, "trigger_price": None, "model": "time_stop"}
                return {
                    "triggered": True,
                    "trigger_date": exit_date,
                    "trigger_price": float(exit_price),
                    "model": "time_stop",
                }
            return {"triggered": False, "trigger_date": None, "trigger_price": None, "model": "time_stop"}
        except Exception as exc:
            logger.error("apply_time_stop error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def build_assumption_dict(self) -> dict:
        """Return all model parameters as a dictionary for reporting."""
        return {
            "entry_model": self.entry_model,
            "exit_model": self.exit_model,
            "allow_same_day_entry": self.allow_same_day_entry,
            "max_holding_days": self.max_holding_days,
            "stop_loss_pct": self.stop_loss_pct,
            "take_profit_pct": self.take_profit_pct,
            "trailing_stop_pct": self.trailing_stop_pct,
            "time_stop_days": self.time_stop_days,
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    def _normalize_df(self, price_df):
        """Normalize DataFrame to have DatetimeIndex and lowercase columns."""
        if not _PANDAS_AVAILABLE:
            return None
        if price_df is None:
            return None
        try:
            df = price_df.copy()
            df.columns = [c.lower() for c in df.columns]
            if "date" in df.columns:
                df = df.set_index("date")
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index, errors="coerce")
                df = df[~df.index.isna()]
                df = df.sort_index()
            df.index = df.index.strftime("%Y-%m-%d")
            return df
        except Exception as exc:
            logger.error("_normalize_df error: %s", exc)
            return None

    @staticmethod
    def _safe_get(row, col: str):
        """Safely get a value from a row; return None if missing or NaN."""
        try:
            val = row[col]
            if _PANDAS_AVAILABLE and pd.isna(val):
                return None
            return float(val) if val is not None else None
        except (KeyError, TypeError, ValueError):
            return None
