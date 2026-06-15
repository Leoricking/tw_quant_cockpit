"""
replay/point_in_time_context.py — PointInTimeReplayContextBuilder v1.2.0

Builds market snapshot using ONLY data available at replay_date.

Indicator rules:
- Only data with date <= replay_date
- min_periods set reasonably
- NO backward fill for future values
- NO center=True in rolling
- NO future window

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    import pandas as pd
    import numpy as np
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("[PointInTimeContextBuilder] pandas/numpy not available")


class PointInTimeReplayContextBuilder:
    """
    Builds market snapshot using ONLY data available at replay_date.

    Indicator rules:
    - Only data with date <= replay_date
    - min_periods set reasonably
    - NO backward fill for future values
    - NO center=True in rolling
    - NO future window
    """

    def __init__(self, data_source, firewall, repo_root=None):
        self.data_source = data_source
        self.firewall = firewall
        self.repo_root = repo_root

    def build(self, symbol: str, replay_date: str, session_config) -> Any:
        """Returns ReplayMarketSnapshot."""
        from replay.replay_schema import ReplayMarketSnapshot

        available_sections = []
        unavailable_sections = []
        timing_warnings = []
        future_blocked_count = 0

        # Price context
        price_data = {}
        indicator_data = {}
        try:
            price_ctx = self.build_price_context(symbol, replay_date)
            if price_ctx:
                price_data = price_ctx
                available_sections.append("price")
                # Build indicators
                price_df = self.data_source.load_price_history(symbol, replay_date)
                if price_df is not None and not price_df.empty:
                    indicator_data = self.build_indicator_context(price_df, replay_date)
                    if indicator_data:
                        available_sections.append("indicators")
            else:
                unavailable_sections.append("price")
        except Exception as exc:
            logger.warning("[PIT] Price/indicator error for %s: %s", symbol, exc)
            unavailable_sections.append("price")

        # Chips context
        chips_data = {}
        try:
            chips_ctx = self.build_chips_context(symbol, replay_date)
            if chips_ctx:
                chips_data = chips_ctx
                available_sections.append("chips")
            else:
                unavailable_sections.append("chips")
        except Exception as exc:
            logger.warning("[PIT] Chips error for %s: %s", symbol, exc)
            unavailable_sections.append("chips")

        # Fundamental context
        fundamental_data = {}
        try:
            fund_ctx = self.build_fundamental_context(symbol, replay_date)
            if fund_ctx:
                fundamental_data = fund_ctx
                available_sections.append("fundamental")
                if fund_ctx.get("timing_warning"):
                    timing_warnings.append("FUNDAMENTAL_TIMING_APPROXIMATE")
            else:
                unavailable_sections.append("fundamental")
        except Exception as exc:
            logger.warning("[PIT] Fundamental error for %s: %s", symbol, exc)
            unavailable_sections.append("fundamental")

        # Quality gate context
        quality_gate = {}
        try:
            qg_ctx = self.build_quality_gate_context(symbol, replay_date)
            if qg_ctx:
                quality_gate = qg_ctx
                available_sections.append("quality_gate")
            else:
                unavailable_sections.append("quality_gate")
        except Exception as exc:
            logger.warning("[PIT] Quality gate error for %s: %s", symbol, exc)
            unavailable_sections.append("quality_gate")

        # Strategy knowledge context
        strategy_knowledge = {}
        if getattr(session_config, "include_strategy_knowledge", True):
            try:
                sk_ctx = self.build_strategy_knowledge_context(symbol, replay_date)
                if sk_ctx:
                    strategy_knowledge = sk_ctx
                    available_sections.append("strategy_knowledge")
                else:
                    unavailable_sections.append("strategy_knowledge")
            except Exception as exc:
                logger.warning("[PIT] Strategy knowledge error for %s: %s", symbol, exc)
                unavailable_sections.append("strategy_knowledge")

        # Sanitize: remove forbidden fields
        price_data, b1, w1 = self.firewall.sanitize_context(price_data, replay_date)
        indicator_data, b2, w2 = self.firewall.sanitize_context(indicator_data, replay_date)
        future_blocked_count = b1 + b2
        timing_warnings.extend(w1)
        timing_warnings.extend(w2)

        snapshot = ReplayMarketSnapshot(
            session_id=getattr(session_config, "session_id", ""),
            symbol=symbol,
            replay_date=replay_date,
            price_data=price_data,
            indicator_data=indicator_data,
            chips_data=chips_data,
            fundamental_data=fundamental_data,
            quality_gate=quality_gate,
            freshness={},
            strategy_knowledge=strategy_knowledge,
            available_sections=available_sections,
            unavailable_sections=unavailable_sections,
            timing_warnings=timing_warnings,
            source_metadata=self.data_source.source_status(symbol),
            point_in_time_verified=False,
            future_data_blocked_count=future_blocked_count,
        )

        verified, issues = self.verify_point_in_time(snapshot)
        snapshot.point_in_time_verified = verified
        if not verified:
            snapshot.timing_warnings.extend(issues)

        return snapshot

    def build_price_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Returns dict with OHLCV for replay_date and recent history."""
        if not _PANDAS_OK:
            return None
        df = self.data_source.load_price_history(symbol, replay_date)
        if df is None or df.empty:
            return None
        try:
            date_col = "date"
            # Find the row for replay_date
            row = df[df[date_col] == replay_date]
            if row.empty:
                # Use last available
                row = df.tail(1)

            latest = row.iloc[-1].to_dict()
            recent = df.tail(20).to_dict("records")
            return {
                "current": latest,
                "recent_history": recent,
                "date": replay_date,
                "available_days": len(df),
            }
        except Exception as exc:
            logger.warning("[PIT] build_price_context error: %s", exc)
            return None

    def build_indicator_context(self, price_df, replay_date: str) -> Dict[str, Any]:
        """
        Computes point-in-time indicators.
        All rolling: only past data, no center=True, no backward fill for future.
        """
        if not _PANDAS_OK or price_df is None or price_df.empty:
            return {}
        try:
            df = price_df.copy()

            # Ensure numeric close/high/low/volume
            for col in ["close", "open", "high", "low", "volume"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            if "close" not in df.columns or len(df) < 2:
                return {}

            close = df["close"]
            result = {}

            # Moving averages (no center=True)
            for n in [5, 10, 20, 60]:
                col = f"MA{n}"
                ma = close.rolling(window=n, min_periods=1).mean()
                val = ma.iloc[-1] if not ma.empty else None
                result[col] = round(float(val), 4) if val is not None and not (hasattr(val, '__float__') and val != val) else None

            # Volume MA5
            if "volume" in df.columns:
                vol = df["volume"]
                vol_ma5 = vol.rolling(window=5, min_periods=1).mean()
                result["volume_ma5"] = round(float(vol_ma5.iloc[-1]), 2) if not vol_ma5.empty else None

            # KD stochastic
            try:
                k_series, d_series = self._compute_kd(df)
                result["KD_K"] = round(float(k_series.iloc[-1]), 4) if not k_series.empty else None
                result["KD_D"] = round(float(d_series.iloc[-1]), 4) if not d_series.empty else None
            except Exception:
                result["KD_K"] = None
                result["KD_D"] = None

            # MACD
            try:
                macd_dict = self._compute_macd(df)
                result.update(macd_dict)
            except Exception:
                result["MACD"] = None
                result["MACD_signal"] = None
                result["MACD_hist"] = None

            # RSI
            try:
                rsi = self._compute_rsi(df)
                result["RSI"] = round(float(rsi.iloc[-1]), 4) if not rsi.empty else None
            except Exception:
                result["RSI"] = None

            # ATR
            try:
                atr = self._compute_atr(df)
                result["ATR"] = round(float(atr.iloc[-1]), 4) if not atr.empty else None
            except Exception:
                result["ATR"] = None

            # Rolling high/low (20-day)
            if "high" in df.columns and "low" in df.columns:
                result["rolling_high"] = round(float(df["high"].rolling(window=20, min_periods=1).max().iloc[-1]), 4)
                result["rolling_low"] = round(float(df["low"].rolling(window=20, min_periods=1).min().iloc[-1]), 4)

            result["replay_date"] = replay_date
            result["pit_verified"] = True
            return result
        except Exception as exc:
            logger.warning("[PIT] build_indicator_context error: %s", exc)
            return {"error": str(exc)}

    def build_chips_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Returns dict or None."""
        return self.data_source.load_chips_history(symbol, replay_date)

    def build_fundamental_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Returns dict with timing_warning if announcement_date unknown."""
        result = self.data_source.load_fundamental_history(symbol, replay_date)
        if result and result.get("timing_approximate"):
            result["timing_warning"] = "FUNDAMENTAL_TIMING_APPROXIMATE"
        return result

    def build_quality_gate_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Returns quality gate status dict."""
        return self.data_source.load_quality_context(symbol, replay_date)

    def build_strategy_knowledge_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Returns strategy knowledge dict using only data available at replay_date."""
        return self.data_source.load_strategy_context(symbol, replay_date)

    def verify_point_in_time(self, snapshot) -> Tuple[bool, List[str]]:
        """Runs firewall verification on snapshot. Returns (verified, issues)."""
        return self.firewall.verify_snapshot(snapshot)

    def limitations(self, symbol: str, replay_date: str) -> List[str]:
        """Returns list of known limitations for this symbol/date combo."""
        return self.data_source.data_limitations(symbol, replay_date)

    # ------------------------------------------------------------------
    # Indicator computations
    # ------------------------------------------------------------------

    def _compute_kd(self, df, n: int = 9, m1: int = 3, m2: int = 3):
        """Stochastic KD. Returns Series K, D using only past data."""
        if "high" not in df.columns or "low" not in df.columns or "close" not in df.columns:
            empty = pd.Series(dtype=float)
            return empty, empty

        high = df["high"].rolling(window=n, min_periods=1).max()
        low = df["low"].rolling(window=n, min_periods=1).min()
        diff = high - low
        diff = diff.replace(0, float("nan"))
        rsv = ((df["close"] - low) / diff * 100).fillna(50)

        # K = EWM of RSV, D = EWM of K
        # Use span=(2*m1-1) for ewm
        k = rsv.ewm(com=(m1 - 1), adjust=False).mean()
        d = k.ewm(com=(m2 - 1), adjust=False).mean()
        return k, d

    def _compute_macd(self, df, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, Any]:
        """MACD. No center, no future. Returns dict with macd, signal, hist."""
        close = df["close"]
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        hist = macd_line - signal_line

        def _safe_val(s):
            if s.empty:
                return None
            v = s.iloc[-1]
            if v != v:  # NaN check
                return None
            return round(float(v), 6)

        return {
            "MACD": _safe_val(macd_line),
            "MACD_signal": _safe_val(signal_line),
            "MACD_hist": _safe_val(hist),
        }

    def _compute_rsi(self, df, period: int = 14) -> "pd.Series":
        """RSI. No center, no future."""
        close = df["close"]
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        avg_gain = gain.ewm(com=(period - 1), adjust=False).mean()
        avg_loss = loss.ewm(com=(period - 1), adjust=False).mean()
        rs = avg_gain / avg_loss.replace(0, float("nan"))
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)

    def _compute_atr(self, df, period: int = 14) -> "pd.Series":
        """ATR. No center, no future."""
        if "high" not in df.columns or "low" not in df.columns or "close" not in df.columns:
            return pd.Series(dtype=float)
        high = df["high"]
        low = df["low"]
        close = df["close"]
        prev_close = close.shift(1)
        tr = pd.concat([
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ], axis=1).max(axis=1)
        atr = tr.ewm(com=(period - 1), adjust=False).mean()
        return atr
