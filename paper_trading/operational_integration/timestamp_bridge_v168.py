"""
paper_trading/operational_integration/timestamp_bridge_v168.py
Timestamp Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_TZ_OFFSETS = {
    "Asia/Taipei": "+08:00",
    "UTC": "+00:00",
    "US/Eastern": "-05:00",
    "US/Pacific": "-08:00",
}


def _parse_ts(ts: str) -> Optional[datetime]:
    """Parse ISO8601 timestamp, return datetime or None."""
    try:
        cleaned = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    except Exception:
        return None


class TimestampBridge:
    """Validates and normalizes timestamps across integration. Research only."""

    def normalize(self, ts: str, source_tz: str, target_tz: str) -> str:
        """
        Normalize timestamp from source_tz to target_tz.
        Returns ISO8601 string in target timezone offset.
        """
        dt = _parse_ts(ts)
        if dt is None:
            return ts
        # If naive, attach source_tz offset
        if dt.tzinfo is None:
            offset_str = _TZ_OFFSETS.get(source_tz, "+00:00")
            sign = 1 if offset_str[0] == "+" else -1
            h, m = map(int, offset_str[1:].split(":"))
            offset = timezone(timedelta(hours=sign * h, minutes=sign * m))
            dt = dt.replace(tzinfo=offset)
        # Convert to target tz offset
        target_offset_str = _TZ_OFFSETS.get(target_tz, "+00:00")
        sign = 1 if target_offset_str[0] == "+" else -1
        h, m = map(int, target_offset_str[1:].split(":"))
        target_tz_obj = timezone(timedelta(hours=sign * h, minutes=sign * m))
        dt_target = dt.astimezone(target_tz_obj)
        return dt_target.isoformat()

    def check_future(self, ts: str) -> bool:
        """Return True if ts is in the future relative to now."""
        dt = _parse_ts(ts)
        if dt is None:
            return False
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt > now

    def check_reversed(self, ts1: str, ts2: str) -> bool:
        """Return True if ts1 > ts2 (reversed ordering)."""
        d1 = _parse_ts(ts1)
        d2 = _parse_ts(ts2)
        if d1 is None or d2 is None:
            return False
        if d1.tzinfo is None:
            d1 = d1.replace(tzinfo=timezone.utc)
        if d2.tzinfo is None:
            d2 = d2.replace(tzinfo=timezone.utc)
        return d1 > d2

    def check_stale(self, ts: str, max_age_seconds: float) -> bool:
        """Return True if ts is older than max_age_seconds from now."""
        dt = _parse_ts(ts)
        if dt is None:
            return True
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age = (now - dt).total_seconds()
        return age > max_age_seconds

    def check_timezone_mismatch(self, ts1: str, tz1: str, ts2: str, tz2: str) -> bool:
        """Return True if the timestamps have mismatched timezone conventions."""
        d1 = _parse_ts(ts1)
        d2 = _parse_ts(ts2)
        # If both are naive and in different tz contexts, it's a mismatch
        if d1 is None or d2 is None:
            return True
        naive1 = d1.tzinfo is None
        naive2 = d2.tzinfo is None
        if naive1 != naive2:
            return True
        return tz1 != tz2

    def check_naive(self, ts: str) -> bool:
        """Return True if ts has no timezone information."""
        dt = _parse_ts(ts)
        if dt is None:
            return True
        return dt.tzinfo is None

    def check_out_of_order(self, timestamps: List[str]) -> List[Dict[str, Any]]:
        """Return list of out-of-order entries."""
        if len(timestamps) < 2:
            return []
        issues = []
        dts = []
        for ts in timestamps:
            dt = _parse_ts(ts)
            if dt is not None and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dts.append(dt)

        for i in range(1, len(dts)):
            if dts[i - 1] is not None and dts[i] is not None:
                if dts[i] < dts[i - 1]:
                    issues.append({
                        "index": i,
                        "ts": timestamps[i],
                        "prev_ts": timestamps[i - 1],
                        "issue": "out_of_order",
                    })
        return issues

    def check_period_boundary(self, period_start: str, period_end: str, event_ts: str) -> bool:
        """Return True if event_ts falls within [period_start, period_end]."""
        start = _parse_ts(period_start)
        end = _parse_ts(period_end)
        event = _parse_ts(event_ts)
        if start is None or end is None or event is None:
            return False
        # Make all aware
        for ts in [start, end, event]:
            pass
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        if event.tzinfo is None:
            event = event.replace(tzinfo=timezone.utc)
        return start <= event <= end

    def audit_timestamps(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run all checks on a list of timestamp records."""
        issues = []
        future_count = 0
        naive_count = 0
        stale_count = 0
        out_of_order_count = 0
        all_ts = []

        for rec in records:
            ts = rec.get("timestamp") or rec.get("event_timestamp", "")
            if not ts:
                continue
            all_ts.append(ts)
            if self.check_future(ts):
                future_count += 1
                issues.append({"ts": ts, "issue": "future"})
            if self.check_naive(ts):
                naive_count += 1
                issues.append({"ts": ts, "issue": "naive"})
            if self.check_stale(ts, 86400 * 365):
                stale_count += 1

        oo = self.check_out_of_order(all_ts)
        out_of_order_count = len(oo)
        issues.extend(oo)

        return {
            "total_checked": len(records),
            "future_count": future_count,
            "naive_count": naive_count,
            "stale_count": stale_count,
            "out_of_order_count": out_of_order_count,
            "issue_count": len(issues),
            "issues": issues,
            "paper_only": True,
        }
