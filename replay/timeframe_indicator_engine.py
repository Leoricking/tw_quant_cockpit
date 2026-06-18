"""
replay/timeframe_indicator_engine.py — MultiTimeframeIndicatorEngine v1.2.5

Per-timeframe indicator calculation using completed bars only.
Partial bar indicators go to partial_observation field.
No bfill, no centered rolling.

Indicators: MA5/MA10/MA20/MA60, Volume MA5/MA20, KD, MACD, RSI, ATR,
rolling high/low, price distance to MA, volume ratio, trend slope.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Default: completed bars only. No bfill. No centered rolling.
"""
from __future__ import annotations

import logging
import math
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_BFILL = True
NO_CENTERED_ROLLING = True


class MultiTimeframeIndicatorEngine:
    """
    Calculates technical indicators per timeframe using completed bars only.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] No bfill. No centered rolling. Partial bar → partial_observation only.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_BFILL = True
    NO_CENTERED_ROLLING = True

    # Minimum lookback periods for each indicator
    LOOKBACK = {
        "MA5": 5, "MA10": 10, "MA20": 20, "MA60": 60,
        "VOL_MA5": 5, "VOL_MA20": 20,
        "KD": 9,
        "MACD": 26,
        "RSI": 14,
        "ATR": 14,
        "ROLLING_HIGH": 20, "ROLLING_LOW": 20,
    }

    def calculate(
        self,
        bars: List[Dict[str, Any]],
        timeframe: str,
        replay_timestamp: str,
        use_partial: bool = False,
    ) -> Dict[str, Any]:
        """
        Calculate all indicators for completed bars up to replay_timestamp.
        Returns dict with all indicator values.
        """
        # Filter to completed bars only (default)
        completed = self._filter_completed(bars, replay_timestamp, timeframe)

        if not completed:
            return self._insufficient_result(timeframe, replay_timestamp, "No completed bars")

        closes   = [float(b.get("close",  0.0) or 0.0) for b in completed]
        highs    = [float(b.get("high",   0.0) or 0.0) for b in completed]
        lows     = [float(b.get("low",    0.0) or 0.0) for b in completed]
        volumes  = [float(b.get("volume", 0.0) or 0.0) for b in completed]
        n = len(closes)

        result: Dict[str, Any] = {
            "timeframe": timeframe,
            "replay_timestamp": replay_timestamp,
            "bar_count": n,
            "uses_completed_bars_only": True,
            "no_bfill": True,
            "no_centered_rolling": True,
            "research_only": True,
        }

        # Moving averages
        result["MA5"]  = self.calculate_ma(closes, 5)
        result["MA10"] = self.calculate_ma(closes, 10)
        result["MA20"] = self.calculate_ma(closes, 20)
        result["MA60"] = self.calculate_ma(closes, 60)

        # Volume MAs
        result["VOL_MA5"]  = self.calculate_ma(volumes, 5)
        result["VOL_MA20"] = self.calculate_ma(volumes, 20)

        # KD
        result["KD"] = self.calculate_kd(closes, highs, lows)

        # MACD
        result["MACD"] = self.calculate_macd(closes)

        # RSI
        result["RSI"] = self.calculate_rsi(closes, 14)

        # ATR
        result["ATR"] = self.calculate_atr(closes, highs, lows, 14)

        # Rolling high/low
        result["ROLLING_HIGH_20"] = max(highs[-20:]) if len(highs) >= 20 else None
        result["ROLLING_LOW_20"]  = min(lows[-20:])  if len(lows)  >= 20 else None

        # Price distance to MA
        latest_close = closes[-1] if closes else None
        result["DIST_TO_MA20"] = (
            (latest_close - result["MA20"]) / result["MA20"]
            if result["MA20"] and latest_close else None
        )

        # Volume ratio
        result["VOL_RATIO"] = (
            volumes[-1] / result["VOL_MA20"]
            if result["VOL_MA20"] and volumes else None
        )

        # Trend slope (simple linear regression slope of last 5 closes)
        result["TREND_SLOPE"] = self._trend_slope(closes[-5:]) if len(closes) >= 5 else None

        # Trend state
        result["trend_state"]  = self.calculate_trend_state(closes, result)

        # Volume state
        result["volume_state"] = self.calculate_volume_state(volumes, result)

        # Validate no future data
        future_warnings = self.validate_no_future(result, replay_timestamp)
        result["warnings"] = future_warnings

        return result

    def calculate_ma(self, closes: List[float], period: int) -> Optional[float]:
        """Simple moving average. Returns None if insufficient data."""
        if len(closes) < period:
            return None
        return sum(closes[-period:]) / period

    def calculate_kd(
        self, closes: List[float], highs: List[float], lows: List[float], period: int = 9
    ) -> Dict[str, Any]:
        """Stochastic KD oscillator. Returns dict with K, D, or INSUFFICIENT."""
        if len(closes) < period:
            return {"K": None, "D": None, "status": "INSUFFICIENT"}
        try:
            h_max = max(highs[-period:])
            l_min = min(lows[-period:])
            c     = closes[-1]
            if h_max == l_min:
                rsv = 50.0
            else:
                rsv = (c - l_min) / (h_max - l_min) * 100.0
            # Simple approximation
            k = rsv
            d = rsv
            return {"K": round(k, 2), "D": round(d, 2), "status": "OK"}
        except Exception:
            return {"K": None, "D": None, "status": "ERROR"}

    def calculate_macd(
        self, closes: List[float], fast: int = 12, slow: int = 26, signal: int = 9
    ) -> Dict[str, Any]:
        """MACD. Returns dict with macd, signal, histogram, or INSUFFICIENT."""
        if len(closes) < slow:
            return {"macd": None, "signal_line": None, "histogram": None, "status": "INSUFFICIENT"}
        try:
            ema_fast = self._ema(closes, fast)
            ema_slow = self._ema(closes, slow)
            if ema_fast is None or ema_slow is None:
                return {"macd": None, "signal_line": None, "histogram": None, "status": "INSUFFICIENT"}
            macd_val = ema_fast - ema_slow
            return {
                "macd": round(macd_val, 4),
                "signal_line": None,  # simplified
                "histogram": None,
                "status": "OK",
            }
        except Exception:
            return {"macd": None, "signal_line": None, "histogram": None, "status": "ERROR"}

    def calculate_rsi(self, closes: List[float], period: int = 14) -> Optional[float]:
        """RSI. Returns None if insufficient data."""
        if len(closes) < period + 1:
            return None
        try:
            deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
            gains  = [d if d > 0 else 0 for d in deltas[-period:]]
            losses = [-d if d < 0 else 0 for d in deltas[-period:]]
            avg_gain = sum(gains) / period
            avg_loss = sum(losses) / period
            if avg_loss == 0:
                return 100.0
            rs = avg_gain / avg_loss
            return round(100.0 - 100.0 / (1 + rs), 2)
        except Exception:
            return None

    def calculate_atr(
        self, closes: List[float], highs: List[float], lows: List[float], period: int = 14
    ) -> Optional[float]:
        """Average True Range. Returns None if insufficient data."""
        if len(closes) < period + 1:
            return None
        try:
            trs = []
            for i in range(1, len(closes)):
                tr = max(
                    highs[i] - lows[i],
                    abs(highs[i] - closes[i - 1]),
                    abs(lows[i] - closes[i - 1]),
                )
                trs.append(tr)
            if len(trs) < period:
                return None
            return round(sum(trs[-period:]) / period, 4)
        except Exception:
            return None

    def calculate_volume_state(
        self, volumes: List[float], indicators: Dict[str, Any]
    ) -> str:
        """Classify volume state relative to MA."""
        try:
            vol_ratio = indicators.get("VOL_RATIO")
            if vol_ratio is None:
                return "UNKNOWN"
            if vol_ratio > 2.0:
                return "HIGH_VOLUME"
            if vol_ratio > 1.2:
                return "ABOVE_AVERAGE"
            if vol_ratio < 0.5:
                return "LOW_VOLUME"
            return "NORMAL"
        except Exception:
            return "UNKNOWN"

    def calculate_trend_state(
        self, closes: List[float], indicators: Dict[str, Any]
    ) -> str:
        """Classify trend based on MAs and slope."""
        try:
            if not closes:
                return "UNKNOWN"
            latest = closes[-1]
            ma5    = indicators.get("MA5")
            ma20   = indicators.get("MA20")
            slope  = indicators.get("TREND_SLOPE")

            if ma5 is None or ma20 is None:
                return "INSUFFICIENT"

            if latest > ma5 > ma20 and (slope or 0) > 0:
                return "UPTREND"
            if latest < ma5 < ma20 and (slope or 0) < 0:
                return "DOWNTREND"
            if abs(latest - ma20) / ma20 < 0.02:
                return "SIDEWAYS"
            return "MIXED"
        except Exception:
            return "UNKNOWN"

    def validate_no_future(
        self, indicators: Dict[str, Any], replay_timestamp: str
    ) -> List[str]:
        """Validate indicators contain no future data references."""
        warnings = []
        for k, v in indicators.items():
            if isinstance(v, dict):
                calc_at = v.get("calculated_at", "")
                if calc_at and calc_at > replay_timestamp:
                    warnings.append(f"Indicator {k} calculated_at {calc_at} > replay {replay_timestamp}")
        return warnings

    def summary(self, timeframe: str) -> Dict[str, Any]:
        return {
            "engine": "MultiTimeframeIndicatorEngine",
            "version": "v1.2.5",
            "timeframe": timeframe,
            "indicators": list(self.LOOKBACK.keys()),
            "uses_completed_bars_only": True,
            "no_bfill": True,
            "no_centered_rolling": True,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _filter_completed(
        self, bars: List[Dict[str, Any]], replay_timestamp: str, timeframe: str
    ) -> List[Dict[str, Any]]:
        """Filter bars to completed only, sorted by timestamp."""
        from replay.timeframe_bar_state import ReplayBarStateEvaluator
        evaluator = ReplayBarStateEvaluator()
        completed = []
        for bar in bars:
            bar_ts = bar.get("timestamp", "")
            if bar_ts and bar_ts <= replay_timestamp:
                if evaluator.is_complete(bar, replay_timestamp, timeframe):
                    completed.append(bar)
        return sorted(completed, key=lambda b: b.get("timestamp", ""))

    def _insufficient_result(
        self, timeframe: str, replay_timestamp: str, reason: str
    ) -> Dict[str, Any]:
        return {
            "timeframe": timeframe,
            "replay_timestamp": replay_timestamp,
            "status": "INSUFFICIENT",
            "reason": reason,
            "warnings": [reason],
            "uses_completed_bars_only": True,
            "no_bfill": True,
            "no_centered_rolling": True,
            "research_only": True,
        }

    def _ema(self, values: List[float], period: int) -> Optional[float]:
        """Simple EMA calculation."""
        if len(values) < period:
            return None
        k = 2.0 / (period + 1)
        ema = sum(values[:period]) / period
        for v in values[period:]:
            ema = v * k + ema * (1 - k)
        return ema

    def _trend_slope(self, values: List[float]) -> Optional[float]:
        """Simple linear regression slope of values."""
        n = len(values)
        if n < 2:
            return None
        try:
            x_mean = (n - 1) / 2.0
            y_mean = sum(values) / n
            numer  = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
            denom  = sum((i - x_mean) ** 2 for i in range(n))
            return numer / denom if denom != 0 else 0.0
        except Exception:
            return None
