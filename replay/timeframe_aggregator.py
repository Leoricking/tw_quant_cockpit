"""
replay/timeframe_aggregator.py — TimeframeBarAggregator v1.2.5

Aggregates 1m bars to higher timeframes. Never splits daily into intraday.
Source tagged as AGGREGATED_FROM_M1. Incomplete group → PARTIAL.
OHLC: open=first, high=max, low=min, close=last. Volume/amount: sum.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Never split daily into fake intraday. Aggregated tagged AGGREGATED_FROM_M1.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
SOURCE_AGGREGATED = "AGGREGATED_FROM_M1"

# Aggregation rules
_AGGREGATION_TARGETS = {
    "M5":  {"from": "M1", "bars_needed": 5},
    "M20": {"from": "M1", "bars_needed": 20},
    "M60": {"from": "M1", "bars_needed": 60},
}

# Cannot split daily into intraday
_FORBIDDEN_SPLITS = {
    "D1": ["M60", "M20", "M5", "M1"],
}


class TimeframeBarAggregator:
    """
    Aggregates 1m bars to 5m, 20m, 60m using OHLCV rules.

    OHLC: open=first, high=max, low=min, close=last.
    Volume/amount: sum.
    Incomplete group: tagged PARTIAL.
    Source: AGGREGATED_FROM_M1.
    Never splits daily into fake intraday.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SOURCE_AGGREGATED = SOURCE_AGGREGATED

    def aggregate(
        self,
        bars: List[Dict[str, Any]],
        target_timeframe: str,
    ) -> Dict[str, Any]:
        """
        Aggregate list of bar dicts to target_timeframe.
        Returns dict: bars (list), warnings (list), source.
        """
        tf_upper = target_timeframe.upper()

        # Validate
        validation = self.validate_source_resolution(bars, target_timeframe)
        if not validation["valid"]:
            return {
                "bars": [],
                "warnings": validation["warnings"],
                "source": SOURCE_AGGREGATED,
                "status": "INVALID",
                "research_only": True,
            }

        if tf_upper not in _AGGREGATION_TARGETS:
            return {
                "bars": [],
                "warnings": [f"Cannot aggregate to {target_timeframe} — only M5/M20/M60 supported"],
                "source": SOURCE_AGGREGATED,
                "status": "INVALID",
                "research_only": True,
            }

        config    = _AGGREGATION_TARGETS[tf_upper]
        bars_need = config["bars_needed"]

        # Sort by timestamp
        sorted_bars = sorted(bars, key=lambda b: b.get("timestamp", ""))

        # Group into periods
        groups  = self._group_bars(sorted_bars, bars_need)
        result_bars = []
        warnings = []

        for group_bars in groups:
            if not group_bars:
                continue
            is_complete_group = len(group_bars) == bars_need
            agg_bar = self.build_bar(group_bars, target_timeframe, is_complete=is_complete_group)
            if not is_complete_group:
                incomplete_w = self.detect_incomplete_group(group_bars, bars_need)
                warnings.extend(incomplete_w)
            result_bars.append(agg_bar)

        return {
            "bars": result_bars,
            "warnings": warnings,
            "source": SOURCE_AGGREGATED,
            "status": "OK",
            "research_only": True,
            "no_real_orders": True,
        }

    def aggregate_until(
        self,
        bars: List[Dict[str, Any]],
        replay_timestamp: str,
        target_timeframe: str,
    ) -> Dict[str, Any]:
        """
        Aggregate bars up to and including replay_timestamp.
        Incomplete group at boundary is tagged PARTIAL.
        """
        # Filter to bars up to replay_timestamp
        filtered = [b for b in bars if b.get("timestamp", "") <= replay_timestamp]
        return self.aggregate(filtered, target_timeframe)

    def build_bar(
        self,
        source_bars: List[Dict[str, Any]],
        target_timeframe: str,
        is_complete: bool = True,
    ) -> Dict[str, Any]:
        """Build aggregated bar from source bars using OHLCV rules."""
        if not source_bars:
            return {}
        sorted_bars = sorted(source_bars, key=lambda b: b.get("timestamp", ""))
        first = sorted_bars[0]
        last  = sorted_bars[-1]

        open_price  = float(first.get("open",  0.0) or 0.0)
        high_price  = max(float(b.get("high",  0.0) or 0.0) for b in sorted_bars)
        low_price   = min(float(b.get("low",   0.0) or 0.0) for b in sorted_bars)
        close_price = float(last.get("close",  0.0) or 0.0)
        total_vol   = sum(float(b.get("volume", 0.0) or 0.0) for b in sorted_bars)
        total_amt   = sum(float(b.get("amount", 0.0) or 0.0) for b in sorted_bars)
        symbol      = first.get("symbol", "")

        return {
            "timestamp":   first.get("timestamp", ""),
            "open":        open_price,
            "high":        high_price,
            "low":         low_price,
            "close":       close_price,
            "volume":      total_vol,
            "amount":      total_amt,
            "symbol":      symbol,
            "timeframe":   target_timeframe,
            "source":      SOURCE_AGGREGATED,
            "available_at": last.get("timestamp", ""),
            "is_complete": is_complete,
            "is_partial":  not is_complete,
            "qualification": "CONFIRMED" if is_complete else "PARTIAL_OBSERVATION",
            "bar_count":   len(sorted_bars),
        }

    def validate_source_resolution(
        self, bars: List[Dict[str, Any]], target_timeframe: str
    ) -> Dict[str, Any]:
        """Validate that source bars have sufficient resolution for aggregation."""
        warnings = []
        tf_upper = target_timeframe.upper()

        # Cannot split daily into intraday
        if tf_upper in ("D1",):
            warnings.append(f"Cannot aggregate TO daily — daily is not aggregated from intraday")
            return {"valid": False, "warnings": warnings}

        if tf_upper not in _AGGREGATION_TARGETS:
            warnings.append(f"Target timeframe {target_timeframe} not supported for aggregation")
            return {"valid": False, "warnings": warnings}

        if not bars:
            warnings.append("No source bars provided")
            return {"valid": False, "warnings": warnings}

        return {"valid": True, "warnings": warnings}

    def detect_incomplete_group(
        self, group_bars: List[Dict[str, Any]], bars_needed: int
    ) -> List[str]:
        """Return warnings for incomplete aggregation group."""
        warnings = []
        actual = len(group_bars)
        if actual < bars_needed:
            ts = group_bars[0].get("timestamp", "?") if group_bars else "?"
            warnings.append(
                f"Incomplete group at {ts}: {actual}/{bars_needed} bars — tagged PARTIAL"
            )
        return warnings

    def summary(self) -> Dict[str, Any]:
        return {
            "engine": "TimeframeBarAggregator",
            "version": "v1.2.5",
            "supported_targets": list(_AGGREGATION_TARGETS.keys()),
            "source": SOURCE_AGGREGATED,
            "ohlc_rules": "open=first, high=max, low=min, close=last",
            "volume_rules": "volume=sum, amount=sum",
            "incomplete_group": "PARTIAL",
            "daily_fake_intraday": "FORBIDDEN",
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _group_bars(
        self, sorted_bars: List[Dict[str, Any]], group_size: int
    ) -> List[List[Dict[str, Any]]]:
        """Group bars into fixed-size windows based on timestamp alignment."""
        if not sorted_bars:
            return []

        groups = []
        current_group: List[Dict[str, Any]] = []
        current_group_key: Optional[str] = None

        for bar in sorted_bars:
            ts  = bar.get("timestamp", "")
            key = self._group_key(ts, group_size)

            if current_group_key is None:
                current_group_key = key

            if key != current_group_key:
                if current_group:
                    groups.append(current_group)
                current_group = []
                current_group_key = key

            current_group.append(bar)

        if current_group:
            groups.append(current_group)

        return groups

    def _group_key(self, timestamp: str, group_minutes: int) -> str:
        """Compute group key for a timestamp given group size in minutes."""
        try:
            from datetime import datetime
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    dt = datetime.strptime(timestamp[:19], fmt[:19])
                    total_min = dt.hour * 60 + dt.minute
                    group_start = (total_min // group_minutes) * group_minutes
                    return f"{dt.date().isoformat()}_{group_start:04d}"
                except ValueError:
                    continue
        except Exception:
            pass
        return timestamp[:16]
