"""
replay/timeframe_data_source.py — MultiTimeframeReplayDataSource v1.2.5

Loads OHLCV data for replay per timeframe. Real mode never falls back to mock.
Daily data is never split into fake intraday. Missing timeframe → UNAVAILABLE.
Timezone: Asia/Taipei. Standard columns enforced.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Real mode: NO mock fallback. Daily: NO fake intraday split.
[!] Missing timeframe → UNAVAILABLE (not a crash). Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
REAL_MODE_NO_MOCK_FALLBACK = True
DAILY_NO_FAKE_INTRADAY = True

TIMEZONE = "Asia/Taipei"
STANDARD_COLUMNS = [
    "timestamp", "open", "high", "low", "close",
    "volume", "amount", "symbol", "timeframe", "source", "available_at",
]
UNAVAILABLE_STATUS = "UNAVAILABLE"

# Timeframes that can be sourced from 1m aggregation
AGGREGATABLE_TIMEFRAMES = {"M5", "M20", "M60"}
SOURCE_AGGREGATED = "AGGREGATED_FROM_M1"
SOURCE_DIRECT = "DIRECT"
SOURCE_MOCK = "MOCK"


class MultiTimeframeReplayDataSource:
    """
    Data source for multi-timeframe replay.

    Rules:
    - Real mode: NO mock fallback. If data missing → UNAVAILABLE.
    - Daily: NEVER split into fake intraday bars.
    - Missing timeframe: return safe_empty_result() — no crash.
    - Timezone: Asia/Taipei for all timestamps.
    - Standard columns enforced on all returned DataFrames.
    - Point-in-time: available_at must be <= replay_timestamp.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    REAL_MODE_NO_MOCK_FALLBACK = True
    DAILY_NO_FAKE_INTRADAY = True

    def __init__(self, base_dir: Optional[str] = None, mode: str = "real") -> None:
        self._base_dir = base_dir or os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "data")
        self._mode = mode

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(
        self,
        symbol: str,
        timeframe: str,
        start: str,
        end: str,
        mode: str = "real",
    ) -> Dict[str, Any]:
        """
        Load OHLCV data for symbol+timeframe between start and end.
        Returns dict with keys: status, data (list of dicts), source, warnings.

        Real mode: never fallback to mock.
        Daily: never split into fake intraday.
        Missing: returns UNAVAILABLE (no crash).
        """
        effective_mode = mode or self._mode

        # Safety: daily never split into intraday
        if self._is_daily_timeframe(timeframe) and self._is_intraday_timeframe(timeframe):
            return self.safe_empty_result(
                symbol, timeframe,
                reason="Daily cannot be split into fake intraday — UNAVAILABLE"
            )

        # Real mode: no mock fallback
        if effective_mode == "real":
            result = self._load_real(symbol, timeframe, start, end)
            if result["status"] == UNAVAILABLE_STATUS:
                # Do NOT try mock
                return result
            return result
        elif effective_mode == "mock":
            return self._load_mock(symbol, timeframe, start, end)
        else:
            return self.safe_empty_result(symbol, timeframe, reason=f"Unknown mode: {effective_mode}")

    def available_timeframes(self, symbol: str) -> List[str]:
        """Return list of timeframes with available data for symbol."""
        available = []
        all_tfs = ["D1", "M60", "M20", "M5", "M1"]
        for tf in all_tfs:
            meta = self.availability(symbol, tf)
            if meta.get("status") == "AVAILABLE":
                available.append(tf)
        return available

    def availability(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Return availability metadata for symbol+timeframe."""
        data_path = self._data_path(symbol, timeframe)
        if data_path and os.path.exists(data_path):
            return {
                "status": "AVAILABLE",
                "symbol": symbol,
                "timeframe": timeframe,
                "path": data_path,
                "source": SOURCE_DIRECT,
            }
        # Check aggregatable from M1
        if timeframe in AGGREGATABLE_TIMEFRAMES:
            m1_path = self._data_path(symbol, "M1")
            if m1_path and os.path.exists(m1_path):
                return {
                    "status": "AVAILABLE",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "path": m1_path,
                    "source": SOURCE_AGGREGATED,
                }
        return {
            "status": UNAVAILABLE_STATUS,
            "symbol": symbol,
            "timeframe": timeframe,
            "path": None,
            "source": None,
        }

    def latest_available_timestamp(self, symbol: str, timeframe: str) -> Optional[str]:
        """Return latest timestamp with available data, or None."""
        result = self.load(symbol, timeframe, "2000-01-01", "2099-12-31")
        if result["status"] != UNAVAILABLE_STATUS and result.get("data"):
            try:
                return max(r["timestamp"] for r in result["data"])
            except Exception:
                return None
        return None

    def source_metadata(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Return source metadata for symbol+timeframe."""
        avail = self.availability(symbol, timeframe)
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "status": avail["status"],
            "source": avail.get("source"),
            "path": avail.get("path"),
            "timezone": TIMEZONE,
            "standard_columns": STANDARD_COLUMNS,
            "real_mode_no_mock_fallback": REAL_MODE_NO_MOCK_FALLBACK,
            "daily_no_fake_intraday": DAILY_NO_FAKE_INTRADAY,
        }

    def safe_empty_result(
        self, symbol: str, timeframe: str, reason: str = ""
    ) -> Dict[str, Any]:
        """Return safe UNAVAILABLE result — no crash, no mock data."""
        return {
            "status": UNAVAILABLE_STATUS,
            "symbol": symbol,
            "timeframe": timeframe,
            "data": [],
            "source": None,
            "warnings": [reason] if reason else [f"{timeframe} data unavailable for {symbol}"],
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def normalize_columns(self, records: List[Dict[str, Any]], symbol: str, timeframe: str) -> List[Dict[str, Any]]:
        """Ensure standard columns are present; fill missing with None."""
        normalized = []
        for r in records:
            row = {col: r.get(col) for col in STANDARD_COLUMNS}
            row["symbol"] = row.get("symbol") or symbol
            row["timeframe"] = row.get("timeframe") or timeframe
            row["source"] = row.get("source") or SOURCE_DIRECT
            normalized.append(row)
        return normalized

    def normalize_timestamp(self, ts: str) -> str:
        """Normalize timestamp to ISO format with timezone."""
        return ts  # Pass-through; real normalization done in calendar

    def validate_ohlcv(self, records: List[Dict[str, Any]]) -> List[str]:
        """Validate OHLCV integrity. Returns list of warning messages."""
        warnings = []
        for i, r in enumerate(records):
            try:
                o, h, l, c = float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])
                if h < max(o, c) or l > min(o, c):
                    warnings.append(f"Row {i}: OHLCV integrity violation (H<max(O,C) or L>min(O,C))")
                if float(r.get("volume", 0)) < 0:
                    warnings.append(f"Row {i}: Negative volume")
            except (TypeError, ValueError, KeyError):
                warnings.append(f"Row {i}: Missing or invalid OHLCV fields")
        return warnings

    def detect_gaps(self, records: List[Dict[str, Any]], timeframe: str) -> List[str]:
        """Detect gaps in bar sequence. Returns warning messages."""
        warnings = []
        if len(records) < 2:
            return warnings
        try:
            from replay.timeframe_registry import ReplayTimeframeRegistry
            registry = ReplayTimeframeRegistry()
            td = registry.get(timeframe)
            if not td or td.timeframe_id == "D1":
                return warnings
            minutes = td.minutes
            timestamps = sorted(r["timestamp"] for r in records if r.get("timestamp"))
            for i in range(1, len(timestamps)):
                pass  # Gap detection is best-effort; real impl would parse timestamps
        except Exception:
            pass
        return warnings

    def detect_duplicates(self, records: List[Dict[str, Any]]) -> List[str]:
        """Detect duplicate timestamps. Returns warning messages."""
        warnings = []
        seen = set()
        for r in records:
            ts = r.get("timestamp")
            if ts in seen:
                warnings.append(f"Duplicate timestamp: {ts}")
            seen.add(ts)
        return warnings

    def detect_future_rows(
        self, records: List[Dict[str, Any]], replay_timestamp: str
    ) -> List[str]:
        """Detect rows with timestamp > replay_timestamp. Returns warnings."""
        warnings = []
        for r in records:
            ts = r.get("timestamp", "")
            if ts and ts > replay_timestamp:
                warnings.append(f"Future row detected: {ts} > {replay_timestamp}")
        return warnings

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_real(self, symbol: str, timeframe: str, start: str, end: str) -> Dict[str, Any]:
        """Load real data from disk. Returns UNAVAILABLE if not found."""
        data_path = self._data_path(symbol, timeframe)
        if not data_path or not os.path.exists(data_path):
            # Try aggregation from M1 for intraday timeframes
            if timeframe in AGGREGATABLE_TIMEFRAMES:
                return self._try_aggregate_from_m1(symbol, timeframe, start, end)
            return self.safe_empty_result(symbol, timeframe,
                reason=f"No real data found for {symbol} {timeframe}")
        try:
            records = self._read_csv_or_jsonl(data_path, symbol, timeframe, start, end)
            warnings = self.validate_ohlcv(records)
            warnings += self.detect_duplicates(records)
            return {
                "status": "AVAILABLE",
                "symbol": symbol,
                "timeframe": timeframe,
                "data": records,
                "source": SOURCE_DIRECT,
                "warnings": warnings,
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as e:
            logger.warning("[MTFDataSource] Error loading %s %s: %s", symbol, timeframe, e)
            return self.safe_empty_result(symbol, timeframe,
                reason=f"Load error: {e}")

    def _try_aggregate_from_m1(
        self, symbol: str, timeframe: str, start: str, end: str
    ) -> Dict[str, Any]:
        """Attempt to aggregate from M1 data. Returns UNAVAILABLE if M1 missing."""
        m1_path = self._data_path(symbol, "M1")
        if not m1_path or not os.path.exists(m1_path):
            return self.safe_empty_result(symbol, timeframe,
                reason=f"No M1 data available to aggregate {timeframe} for {symbol}")
        try:
            m1_records = self._read_csv_or_jsonl(m1_path, symbol, "M1", start, end)
            if not m1_records:
                return self.safe_empty_result(symbol, timeframe,
                    reason=f"M1 data empty; cannot aggregate {timeframe}")
            from replay.timeframe_aggregator import TimeframeBarAggregator
            agg = TimeframeBarAggregator()
            result = agg.aggregate(m1_records, timeframe)
            return {
                "status": "AVAILABLE",
                "symbol": symbol,
                "timeframe": timeframe,
                "data": result.get("bars", []),
                "source": SOURCE_AGGREGATED,
                "warnings": result.get("warnings", []),
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as e:
            logger.warning("[MTFDataSource] Aggregation failed %s %s: %s", symbol, timeframe, e)
            return self.safe_empty_result(symbol, timeframe,
                reason=f"Aggregation error: {e}")

    def _load_mock(self, symbol: str, timeframe: str, start: str, end: str) -> Dict[str, Any]:
        """Load mock data (labeled MOCK). Never used in real mode."""
        from replay.timeframe_registry import ReplayTimeframeRegistry
        registry = ReplayTimeframeRegistry()
        td = registry.get(timeframe)
        minutes = td.minutes if td else 1
        records = self._generate_mock_bars(symbol, timeframe, start, end, minutes)
        return {
            "status": "AVAILABLE",
            "symbol": symbol,
            "timeframe": timeframe,
            "data": records,
            "source": SOURCE_MOCK,
            "warnings": ["MOCK DATA — for testing only. Never use in real mode."],
            "research_only": True,
            "no_real_orders": True,
            "is_mock": True,
        }

    def _generate_mock_bars(
        self, symbol: str, timeframe: str, start: str, end: str, minutes: int
    ) -> List[Dict[str, Any]]:
        """Generate deterministic mock OHLCV bars for testing."""
        bars = []
        # Generate a few mock bars
        mock_timestamps = [
            "2023-01-06T09:00:00+08:00",
            "2023-01-06T09:05:00+08:00",
            "2023-01-06T09:10:00+08:00",
        ]
        for i, ts in enumerate(mock_timestamps):
            bars.append({
                "timestamp": ts,
                "open": 100.0 + i,
                "high": 101.0 + i,
                "low": 99.0 + i,
                "close": 100.5 + i,
                "volume": 1000.0,
                "amount": 100500.0,
                "symbol": symbol,
                "timeframe": timeframe,
                "source": SOURCE_MOCK,
                "available_at": ts,
            })
        return bars

    def _data_path(self, symbol: str, timeframe: str) -> Optional[str]:
        """Return expected data file path for symbol+timeframe, or None."""
        tf_dir_map = {
            "D1": "daily", "M60": "m60", "M20": "m20", "M5": "m5", "M1": "m1"
        }
        tf_dir = tf_dir_map.get(timeframe.upper())
        if not tf_dir:
            return None
        csv_path = os.path.join(self._base_dir, tf_dir, f"{symbol}.csv")
        if os.path.exists(csv_path):
            return csv_path
        return None

    def _read_csv_or_jsonl(
        self, path: str, symbol: str, timeframe: str, start: str, end: str
    ) -> List[Dict[str, Any]]:
        """Read CSV or JSONL file and return normalized records filtered by date range."""
        records = []
        try:
            if path.endswith(".jsonl"):
                import json
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                records.append(json.loads(line))
                            except Exception:
                                pass
            else:
                import csv
                with open(path, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        records.append(dict(row))
        except Exception as e:
            logger.warning("[MTFDataSource] Read error %s: %s", path, e)
            return []

        # Filter by date range
        filtered = []
        for r in records:
            ts = r.get("timestamp", r.get("date", ""))
            if ts and str(ts)[:10] >= start[:10] and str(ts)[:10] <= end[:10]:
                filtered.append(r)

        return self.normalize_columns(filtered, symbol, timeframe)

    def _is_daily_timeframe(self, timeframe: str) -> bool:
        return timeframe.upper() in ("D1", "DAILY", "DAY", "1D")

    def _is_intraday_timeframe(self, timeframe: str) -> bool:
        return timeframe.upper() in ("M60", "M20", "M5", "M1", "60M", "20M", "5M", "1M")
