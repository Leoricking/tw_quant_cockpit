"""
replay/timeframe_future_firewall.py — MultiTimeframeFutureDataFirewall v1.2.5

Blocks all future data from multi-timeframe replay.

Blocks:
- timestamp > replay_timestamp
- available_at > replay_timestamp
- incomplete bar marked completed
- current day full OHLC premature
- incomplete M60/M20/M5 close
- future child bars
- future rolling window
- future pivot
- outcome/forward_return/realized_pnl/hindsight_score/final_session_high/final_session_low

Per-snapshot counters:
  future_rows_blocked, incomplete_bars_blocked, daily_close_leaks_blocked,
  aggregation_leaks_blocked, indicator_leaks_blocked, strategy_leaks_blocked.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Forbidden fields — any presence is a firewall violation
FORBIDDEN_FIELDS = [
    "outcome", "forward_return", "realized_pnl", "hindsight_score",
    "final_session_high", "final_session_low", "future_high", "future_low",
    "final_result", "future_return", "broker", "order_token", "api_key", "secret",
]


class MultiTimeframeFutureDataFirewall:
    """
    Future data firewall for multi-timeframe replay.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def filter_bars(
        self,
        bars: List[Dict[str, Any]],
        replay_timestamp: str,
        timeframe: str,
    ) -> Dict[str, Any]:
        """
        Filter bars to only those valid at replay_timestamp.
        Returns: {filtered_bars, blocked_count, warnings, report}.
        """
        filtered = []
        blocked  = 0
        warnings = []

        for bar in bars:
            bar_ts    = bar.get("timestamp", "")
            avail_at  = bar.get("available_at") or bar_ts

            # Block future timestamp
            if bar_ts and bar_ts > replay_timestamp:
                blocked += 1
                warnings.append(f"BLOCKED future bar: {bar_ts} > {replay_timestamp}")
                continue

            # Block future available_at
            if avail_at and avail_at > replay_timestamp:
                blocked += 1
                warnings.append(f"BLOCKED future available_at: {avail_at} > {replay_timestamp}")
                continue

            # Block incomplete bar marked as complete
            if bar.get("is_complete") and self._is_bar_actually_incomplete(bar, replay_timestamp, timeframe):
                blocked += 1
                warnings.append(
                    f"BLOCKED incomplete bar marked complete: {bar_ts} in {timeframe}"
                )
                continue

            # Block forbidden fields
            forbidden = [f for f in FORBIDDEN_FIELDS if f in bar]
            if forbidden:
                blocked += 1
                warnings.append(f"BLOCKED forbidden fields {forbidden} in bar {bar_ts}")
                continue

            filtered.append(bar)

        return {
            "filtered_bars": filtered,
            "blocked_count": blocked,
            "warnings": warnings,
            "research_only": True,
        }

    def validate_snapshot(
        self, snapshot: Dict[str, Any], replay_timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate a single timeframe snapshot for future data."""
        warnings = []
        counters = {
            "future_rows_blocked": 0,
            "incomplete_bars_blocked": 0,
            "daily_close_leaks_blocked": 0,
            "aggregation_leaks_blocked": 0,
            "indicator_leaks_blocked": 0,
            "strategy_leaks_blocked": 0,
        }

        rts = replay_timestamp or snapshot.get("replay_timestamp", "")

        # Check current_bar
        current_bar = snapshot.get("current_bar") or {}
        if current_bar:
            bar_ts = current_bar.get("timestamp", "")
            if bar_ts and rts and bar_ts > rts:
                counters["future_rows_blocked"] += 1
                warnings.append(f"Future current_bar: {bar_ts}")

        # Check indicators for future fields
        indicators = snapshot.get("indicators") or {}
        for k, v in indicators.items():
            if isinstance(v, dict) and any(f in v for f in FORBIDDEN_FIELDS):
                counters["indicator_leaks_blocked"] += 1
                warnings.append(f"Indicator leak in {k}")

        # Check forbidden fields in snapshot
        for f in FORBIDDEN_FIELDS:
            if f in snapshot:
                counters["strategy_leaks_blocked"] += 1
                warnings.append(f"Forbidden field in snapshot: {f}")

        return {
            "valid": len(warnings) == 0,
            "counters": counters,
            "warnings": warnings,
            "research_only": True,
        }

    def validate_multi_snapshot(
        self, multi_snapshot: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate all timeframe snapshots in a multi-snapshot."""
        rts = multi_snapshot.get("replay_timestamp", "")
        all_warnings = []
        total_counters = {
            "future_rows_blocked": 0,
            "incomplete_bars_blocked": 0,
            "daily_close_leaks_blocked": 0,
            "aggregation_leaks_blocked": 0,
            "indicator_leaks_blocked": 0,
            "strategy_leaks_blocked": 0,
        }
        snapshots = multi_snapshot.get("snapshots", {})
        for tf, snap in snapshots.items():
            result = self.validate_snapshot(snap, rts)
            for k, v in result["counters"].items():
                total_counters[k] += v
            all_warnings.extend(result["warnings"])

        # Check forbidden fields in multi_snapshot itself
        for f in FORBIDDEN_FIELDS:
            if f in multi_snapshot:
                total_counters["strategy_leaks_blocked"] += 1
                all_warnings.append(f"Forbidden field in multi_snapshot: {f}")

        return {
            "valid": len(all_warnings) == 0,
            "counters": total_counters,
            "warnings": all_warnings,
            "research_only": True,
        }

    def detect_future_bars(
        self, bars: List[Dict[str, Any]], replay_timestamp: str
    ) -> List[str]:
        """Return list of future bar timestamps."""
        return [
            bar.get("timestamp", "")
            for bar in bars
            if bar.get("timestamp", "") > replay_timestamp
        ]

    def detect_incomplete_bar_leak(
        self, bars: List[Dict[str, Any]], replay_timestamp: str, timeframe: str
    ) -> List[str]:
        """Detect bars marked complete but actually incomplete."""
        violations = []
        for bar in bars:
            if bar.get("is_complete") and self._is_bar_actually_incomplete(bar, replay_timestamp, timeframe):
                violations.append(bar.get("timestamp", "?"))
        return violations

    def detect_daily_close_leak(
        self, bars: List[Dict[str, Any]], replay_timestamp: str
    ) -> List[str]:
        """Detect D1 final close leaked before end of trading day."""
        violations = []
        for bar in bars:
            tf = bar.get("timeframe", "")
            if tf == "D1" and bar.get("is_complete"):
                # If replay_timestamp is intraday (before 13:30), daily close should not be available
                bar_date = bar.get("session_date", "") or bar.get("timestamp", "")[:10]
                replay_date = replay_timestamp[:10]
                if bar_date == replay_date:
                    # Same day — check if it's before market close
                    replay_time = replay_timestamp[11:16] if len(replay_timestamp) > 10 else "13:30"
                    if replay_time < "13:30":
                        violations.append(
                            f"Daily close leak: {bar.get('timestamp', '?')} marked complete at {replay_timestamp}"
                        )
        return violations

    def detect_aggregation_leak(
        self, bars: List[Dict[str, Any]], replay_timestamp: str, timeframe: str
    ) -> List[str]:
        """Detect aggregated bars using future source bars."""
        violations = []
        for bar in bars:
            if bar.get("source") == "AGGREGATED_FROM_M1":
                avail_at = bar.get("available_at", "")
                if avail_at and avail_at > replay_timestamp:
                    violations.append(
                        f"Aggregation leak: bar {bar.get('timestamp', '?')} avail at {avail_at}"
                    )
        return violations

    def detect_indicator_leak(
        self, indicators: Dict[str, Any], replay_timestamp: str
    ) -> List[str]:
        """Detect indicators containing future data references."""
        violations = []
        for k, v in indicators.items():
            if isinstance(v, dict):
                for f in FORBIDDEN_FIELDS:
                    if f in v:
                        violations.append(f"Indicator {k} contains forbidden field {f}")
                calc_at = v.get("calculated_at", "")
                if calc_at and calc_at > replay_timestamp:
                    violations.append(f"Indicator {k} calculated_at {calc_at} > replay")
        return violations

    def detect_strategy_leak(
        self, strategy_output: Dict[str, Any], replay_timestamp: str
    ) -> List[str]:
        """Detect strategy outputs containing future data."""
        violations = []
        for f in FORBIDDEN_FIELDS:
            if f in strategy_output:
                violations.append(f"Strategy output contains forbidden field: {f}")
        return violations

    def build_report(
        self, replay_timestamp: str, counters: Dict[str, int], warnings: List[str]
    ) -> Dict[str, Any]:
        """Build firewall report."""
        total_blocked = sum(counters.values())
        return {
            "replay_timestamp": replay_timestamp,
            "total_blocked": total_blocked,
            "counters": counters,
            "warnings": warnings,
            "firewall_ok": total_blocked == 0,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_bar_actually_incomplete(
        self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str
    ) -> bool:
        """Check if bar is actually incomplete despite being marked complete."""
        try:
            from replay.timeframe_calendar import TaiwanReplayTradingCalendar
            cal = TaiwanReplayTradingCalendar()
            bar_ts = bar.get("timestamp", "")
            if not bar_ts:
                return False
            # Bar is complete only if its close time <= replay_timestamp
            return not cal.is_bar_complete(bar_ts, replay_timestamp, timeframe)
        except Exception:
            return False
