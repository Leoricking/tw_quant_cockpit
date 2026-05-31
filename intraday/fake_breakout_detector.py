"""
intraday/fake_breakout_detector.py — Fake breakout detector (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

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
    logger.warning("pandas not available — FakeBreakoutDetector will be limited")

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False


def _empty_result(reason: str = "NO_DATA") -> dict:
    """Return a fully-keyed dict with all breakout feature values set to None."""
    return {
        "status": reason,
        "intraday_high_break": None,
        "intraday_low_break": None,
        "breakout_volume_confirmed": None,
        "breakout_failed": None,
        "fake_breakout_risk": None,
        "fake_breakout_score": None,
        "chase_risk_score": None,
        "breakout_quality": None,
    }


class FakeBreakoutDetector:
    """
    Detects fake breakouts from the opening range using intraday 1-minute bar data.

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        breakout_window: int = 30,
        fail_window: int = 15,
        min_breakout_pct: float = 0.005,
    ):
        self.breakout_window = breakout_window
        self.fail_window = fail_window
        self.min_breakout_pct = min_breakout_pct

    def detect(self, df) -> dict:
        """
        Detect fake breakout patterns from a standard 1min DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Must have columns: open, high, low, close, volume

        Returns
        -------
        dict with all breakout feature keys; None values where data is insufficient
        """
        if not _PANDAS_OK:
            return _empty_result("NO_PANDAS")

        if df is None or (hasattr(df, "empty") and df.empty):
            return _empty_result("NO_DATA")

        try:
            df = df.copy()
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            # Sort by datetime / time
            if "datetime" in df.columns:
                df["_sort_dt"] = pd.to_datetime(df["datetime"], errors="coerce")
                df = df.sort_values("_sort_dt").reset_index(drop=True)
            elif "time" in df.columns:
                df = df.sort_values("time").reset_index(drop=True)

            if len(df) < 2:
                return _empty_result("INSUFFICIENT_DATA")

            total_bars = len(df)
            opening_bars_count = min(15, total_bars)
            opening_bars = df.iloc[:opening_bars_count]
            post_opening = df.iloc[opening_bars_count:].reset_index(drop=True)

            # Reference levels from opening bars
            reference_high: Optional[float] = None
            reference_low: Optional[float] = None
            if "high" in opening_bars.columns:
                h_vals = opening_bars["high"].dropna()
                if len(h_vals) > 0:
                    reference_high = float(h_vals.max())
            if "low" in opening_bars.columns:
                l_vals = opening_bars["low"].dropna()
                if len(l_vals) > 0:
                    reference_low = float(l_vals.min())

            if reference_high is None or reference_low is None:
                return _empty_result("NO_REFERENCE_LEVEL")

            mean_volume: Optional[float] = None
            if "volume" in df.columns:
                all_vol = df["volume"].dropna()
                if len(all_vol) > 0:
                    mean_volume = float(all_vol.mean())

            # Detect breakouts in post-opening period
            intraday_high_break = False
            intraday_low_break = False
            breakout_bar_idx: Optional[int] = None
            breakout_direction: Optional[str] = None  # "up" or "down"
            breakout_volume: Optional[float] = None

            if not post_opening.empty and "close" in post_opening.columns:
                for i, row in post_opening.iterrows():
                    close_val = row.get("close")
                    if pd.isna(close_val):
                        continue
                    close_val = float(close_val)

                    if close_val > reference_high * (1 + self.min_breakout_pct):
                        intraday_high_break = True
                        if breakout_bar_idx is None:
                            breakout_bar_idx = i
                            breakout_direction = "up"
                            breakout_volume = (
                                float(row.get("volume", 0))
                                if not pd.isna(row.get("volume", float("nan")))
                                else None
                            )

                    if close_val < reference_low * (1 - self.min_breakout_pct):
                        intraday_low_break = True
                        if breakout_bar_idx is None:
                            breakout_bar_idx = i
                            breakout_direction = "down"
                            breakout_volume = (
                                float(row.get("volume", 0))
                                if not pd.isna(row.get("volume", float("nan")))
                                else None
                            )

            # Volume confirmation
            breakout_volume_confirmed = False
            if (breakout_volume is not None and mean_volume is not None
                    and mean_volume > 0):
                breakout_volume_confirmed = bool(breakout_volume > mean_volume * 1.5)

            # Breakout failed: broke out but fell back within opening range in fail_window bars
            breakout_failed = False
            if (breakout_bar_idx is not None and not post_opening.empty
                    and "close" in post_opening.columns):
                look_start = breakout_bar_idx
                look_end = min(look_start + self.fail_window, len(post_opening))
                window_bars = post_opening.iloc[look_start:look_end]

                for _, row in window_bars.iterrows():
                    close_val = row.get("close")
                    if pd.isna(close_val):
                        continue
                    close_val = float(close_val)
                    if breakout_direction == "up" and close_val <= reference_high:
                        breakout_failed = True
                        break
                    elif breakout_direction == "down" and close_val >= reference_low:
                        breakout_failed = True
                        break

            # Classify fake breakout risk
            any_breakout = intraday_high_break or intraday_low_break
            if not any_breakout:
                fake_breakout_risk = "NONE"
            elif breakout_failed and not breakout_volume_confirmed:
                fake_breakout_risk = "HIGH"
            elif breakout_failed or (intraday_high_break and not breakout_volume_confirmed):
                fake_breakout_risk = "MEDIUM"
            elif any_breakout and breakout_volume_confirmed:
                fake_breakout_risk = "LOW"
            else:
                fake_breakout_risk = "MEDIUM"

            # Fake breakout score (0–100, higher = more risk)
            fake_breakout_score = 0.0
            if fake_breakout_risk == "HIGH":
                fake_breakout_score = 85.0
            elif fake_breakout_risk == "MEDIUM":
                fake_breakout_score = 55.0
            elif fake_breakout_risk == "LOW":
                fake_breakout_score = 20.0
            else:
                fake_breakout_score = 0.0

            # Adjust for volume confirmation
            if breakout_volume_confirmed and fake_breakout_score > 0:
                fake_breakout_score = max(0.0, fake_breakout_score - 15.0)
            if not breakout_volume_confirmed and any_breakout:
                fake_breakout_score = min(100.0, fake_breakout_score + 10.0)

            # Chase risk score (0–100)
            chase_risk_score = 0.0
            if not any_breakout:
                chase_risk_score = 10.0
            elif fake_breakout_risk == "HIGH":
                chase_risk_score = 90.0
            elif fake_breakout_risk == "MEDIUM":
                chase_risk_score = 65.0
            elif fake_breakout_risk == "LOW":
                chase_risk_score = 30.0
            if breakout_failed:
                chase_risk_score = min(100.0, chase_risk_score + 15.0)

            # Breakout quality
            if not any_breakout:
                breakout_quality = "NONE"
            elif breakout_failed:
                breakout_quality = "FAILED"
            elif breakout_volume_confirmed:
                breakout_quality = "STRONG"
            else:
                breakout_quality = "WEAK"

            return {
                "status": "OK",
                "intraday_high_break": intraday_high_break,
                "intraday_low_break": intraday_low_break,
                "breakout_volume_confirmed": breakout_volume_confirmed,
                "breakout_failed": breakout_failed,
                "fake_breakout_risk": fake_breakout_risk,
                "fake_breakout_score": round(fake_breakout_score, 2),
                "chase_risk_score": round(chase_risk_score, 2),
                "breakout_quality": breakout_quality,
                # v0.3.28: governance rule_id reference (metadata only)
                "feature_rule_id": "INTRADAY.BREAKOUT.FAKE_BREAKOUT_RISK.V1",
            }

        except Exception as exc:
            logger.exception("FakeBreakoutDetector.detect error: %s", exc)
            result = _empty_result("ERROR")
            result["warning"] = str(exc)
            return result
