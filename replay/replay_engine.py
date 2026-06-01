"""replay/replay_engine.py — Intraday Replay Engine (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import glob
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("[IntradayReplayEngine] pandas not available — INSUFFICIENT_INTRADAY_DATA will be returned")


class IntradayReplayEngine:
    """Step-through intraday data replay engine.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    Never exposes future bars unless reveal_future=True.
    """

    read_only = True
    no_real_orders = True

    def __init__(
        self,
        standard_root: str = "data/import/intraday_standard",
        freq: str = "1min",
        replay_speed: float = 1.0,
        reveal_future: bool = False,
    ):
        self._standard_root = os.path.join(BASE_DIR, standard_root)
        self._freq = freq
        self._replay_speed = replay_speed
        self._reveal_future = reveal_future

        self._df = None
        self._current_index: int = 0
        self._symbol: Optional[str] = None
        self._date: Optional[str] = None
        self._status: str = "NOT_LOADED"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _insufficient(self, symbol: str = "") -> dict:
        return {
            "status": "INSUFFICIENT_INTRADAY_DATA",
            "symbol": symbol or self._symbol or "",
            "research_only": True,
            "no_real_orders": True,
        }

    def _not_loaded(self) -> dict:
        return {"status": "NOT_LOADED", "research_only": True, "no_real_orders": True}

    def _row_to_dict(self, index: int) -> dict:
        if self._df is None:
            return self._not_loaded()
        if len(self._df) == 0:
            return self._insufficient()
        idx = max(0, min(index, len(self._df) - 1))
        row = self._df.iloc[idx]
        result = {"bar_index": idx, "status": "OK"}
        for col in self._df.columns:
            val = row[col]
            # convert numpy types to python native
            try:
                val = val.item()
            except AttributeError:
                pass
            result[col] = val
        result["research_only"] = True
        result["no_real_orders"] = True
        return result

    def _find_csv_file(self, symbol: str, freq: str) -> Optional[str]:
        freq_dir = os.path.join(self._standard_root, freq)
        if not os.path.isdir(freq_dir):
            logger.warning("[ReplayEngine] freq dir not found: %s", freq_dir)
            return None

        # try exact match first
        exact = os.path.join(freq_dir, f"{symbol}.csv")
        if os.path.exists(exact):
            return exact

        # try glob pattern
        pattern = os.path.join(freq_dir, f"{symbol}_*.csv")
        matches = glob.glob(pattern)
        if matches:
            return sorted(matches)[-1]

        # try case-insensitive glob
        pattern2 = os.path.join(freq_dir, f"{symbol.upper()}_*.csv")
        matches2 = glob.glob(pattern2)
        if matches2:
            return sorted(matches2)[-1]

        logger.warning("[ReplayEngine] no CSV found for %s in %s", symbol, freq_dir)
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def load_intraday_data(
        self, symbol: str, date: Optional[str] = None, freq: Optional[str] = None
    ) -> dict:
        """Load intraday CSV for symbol. Returns status dict."""
        if not _PANDAS_OK:
            return self._insufficient(symbol)

        use_freq = freq or self._freq
        csv_path = self._find_csv_file(symbol, use_freq)
        if csv_path is None:
            self._status = "INSUFFICIENT_INTRADAY_DATA"
            return self._insufficient(symbol)

        try:
            df = pd.read_csv(csv_path)
        except Exception as exc:
            logger.error("[ReplayEngine] CSV read error: %s", exc)
            self._status = "INSUFFICIENT_INTRADAY_DATA"
            return self._insufficient(symbol)

        # normalise column names to lowercase
        df.columns = [c.lower().strip() for c in df.columns]

        # try to identify datetime column
        for candidate in ("datetime", "timestamp", "date_time", "time", "date"):
            if candidate in df.columns:
                df["datetime"] = pd.to_datetime(df[candidate], errors="coerce")
                break
        else:
            # attempt index as datetime
            try:
                df["datetime"] = pd.to_datetime(df.index, errors="coerce")
            except Exception:
                pass

        # filter by date if provided
        if date and "datetime" in df.columns:
            try:
                df = df[df["datetime"].dt.strftime("%Y-%m-%d") == date].copy()
            except Exception as exc:
                logger.warning("[ReplayEngine] date filter error: %s", exc)

        if len(df) == 0:
            self._status = "INSUFFICIENT_INTRADAY_DATA"
            return self._insufficient(symbol)

        df = df.reset_index(drop=True)
        self._df = df
        self._symbol = symbol
        self._date = date
        self._freq = use_freq
        self._current_index = 0
        self._status = "READY"

        return {
            "status": "READY",
            "symbol": symbol,
            "date": date,
            "freq": use_freq,
            "total_bars": len(df),
            "columns": list(df.columns),
            "research_only": True,
            "no_real_orders": True,
        }

    def prepare_replay(
        self, symbol: str, date: Optional[str] = None, freq: Optional[str] = None
    ) -> dict:
        """Load data and reset position to bar 0."""
        result = self.load_intraday_data(symbol, date=date, freq=freq)
        if result.get("status") != "READY":
            return result
        self._current_index = 0
        summary = dict(result)
        summary["current_index"] = 0
        summary["current_bar"] = self._row_to_dict(0)
        return summary

    def step_forward(self) -> dict:
        if self._df is None:
            return self._not_loaded()
        if len(self._df) == 0:
            return self._insufficient()
        self._current_index = min(self._current_index + 1, len(self._df) - 1)
        return self._row_to_dict(self._current_index)

    def step_backward(self) -> dict:
        if self._df is None:
            return self._not_loaded()
        if len(self._df) == 0:
            return self._insufficient()
        self._current_index = max(self._current_index - 1, 0)
        return self._row_to_dict(self._current_index)

    def jump_to_time(self, time_str: str) -> dict:
        """Jump to first bar at or after time_str."""
        if self._df is None:
            return self._not_loaded()
        if len(self._df) == 0:
            return self._insufficient()
        if "datetime" not in self._df.columns:
            logger.warning("[ReplayEngine] no datetime column for jump_to_time")
            return self._row_to_dict(self._current_index)
        try:
            import pandas as pd  # noqa: F811
            target = pd.to_datetime(time_str, errors="coerce")
            if pd.isna(target):
                # try time-only comparison
                mask = self._df["datetime"].astype(str).str.contains(time_str, na=False)
            else:
                mask = self._df["datetime"] >= target
            candidates = self._df[mask]
            if len(candidates) > 0:
                self._current_index = int(candidates.index[0])
        except Exception as exc:
            logger.warning("[ReplayEngine] jump_to_time error: %s", exc)
        return self._row_to_dict(self._current_index)

    def get_current_bar(self) -> dict:
        if self._df is None:
            return self._not_loaded()
        return self._row_to_dict(self._current_index)

    def get_visible_bars(self) -> list:
        """Return bars 0..current_index inclusive."""
        if self._df is None:
            return []
        if len(self._df) == 0:
            return []
        try:
            subset = self._df.iloc[: self._current_index + 1]
            records = []
            for i, (_, row) in enumerate(subset.iterrows()):
                d = {"bar_index": i}
                for col in subset.columns:
                    val = row[col]
                    try:
                        val = val.item()
                    except AttributeError:
                        pass
                    d[col] = val
                records.append(d)
            return records
        except Exception as exc:
            logger.error("[ReplayEngine] get_visible_bars error: %s", exc)
            return []

    def get_hidden_future_bars(self) -> list:
        """Return bars after current_index. Only available if reveal_future=True."""
        if not self._reveal_future:
            return []
        if self._df is None:
            return []
        try:
            subset = self._df.iloc[self._current_index + 1 :]
            records = []
            for i, (_, row) in enumerate(subset.iterrows()):
                d = {"bar_index": self._current_index + 1 + i}
                for col in subset.columns:
                    val = row[col]
                    try:
                        val = val.item()
                    except AttributeError:
                        pass
                    d[col] = val
                records.append(d)
            return records
        except Exception as exc:
            logger.error("[ReplayEngine] get_hidden_future_bars error: %s", exc)
            return []

    def reset(self) -> dict:
        self._current_index = 0
        return {
            "status": self._status,
            "current_index": 0,
            "total_bars": len(self._df) if self._df is not None else 0,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def status(self) -> str:
        return self._status

    @property
    def current_index(self) -> int:
        return self._current_index

    @property
    def total_bars(self) -> int:
        return len(self._df) if self._df is not None else 0
