"""
Metrics Aggregator v1.6.3 — Decimal-safe, PIT-safe, deterministic.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
import statistics
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import AggregationType
from paper_trading.operations.models_v163 import SessionMetric

UNKNOWN = "UNKNOWN"


def _to_decimal(v: float) -> Decimal:
    return Decimal(str(v))


def aggregate(
    observations: List[SessionMetric],
    agg_type:     AggregationType,
    *,
    window_start:     Optional[datetime] = None,
    window_end:       Optional[datetime] = None,
    minimum_samples:  int = 1,
    available_from:   Optional[datetime] = None,
    pit:              Optional[datetime] = None,
) -> Tuple[Optional[float], str]:
    """
    Returns (value, status) where status is 'ok', 'UNKNOWN', 'insufficient'.

    Rules:
    - Empty window → UNKNOWN (not 0)
    - Insufficient samples → UNKNOWN
    - No future data (PIT filter)
    - missing data not filled with 0
    - Decimal-safe arithmetic
    """
    cutoff = pit or window_end
    if cutoff and cutoff.tzinfo is None:
        cutoff = cutoff.replace(tzinfo=timezone.utc)

    filtered = [o for o in observations if o.observed_at is not None]

    if window_start:
        ws = window_start if window_start.tzinfo else window_start.replace(tzinfo=timezone.utc)
        filtered = [o for o in filtered if o.observed_at >= ws]

    if cutoff:
        filtered = [o for o in filtered if o.observed_at <= cutoff]

    if available_from:
        af = available_from if available_from.tzinfo else available_from.replace(tzinfo=timezone.utc)
        if cutoff and cutoff < af:
            return None, UNKNOWN

    if not filtered:
        return None, UNKNOWN

    if len(filtered) < minimum_samples:
        return None, "insufficient"

    values = [o.value for o in filtered]
    dec_vals = [_to_decimal(v) for v in values]

    if agg_type == AggregationType.SUM:
        return float(sum(dec_vals)), "ok"
    elif agg_type == AggregationType.COUNT:
        return float(len(filtered)), "ok"
    elif agg_type == AggregationType.MIN:
        return float(min(dec_vals)), "ok"
    elif agg_type == AggregationType.MAX:
        return float(max(dec_vals)), "ok"
    elif agg_type == AggregationType.AVG:
        avg = sum(dec_vals) / Decimal(len(dec_vals))
        return float(avg.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)), "ok"
    elif agg_type == AggregationType.LAST:
        sorted_obs = sorted(filtered, key=lambda o: o.observed_at)
        return float(_to_decimal(sorted_obs[-1].value)), "ok"
    elif agg_type == AggregationType.RATE:
        if len(filtered) < 2:
            return None, UNKNOWN
        sorted_obs = sorted(filtered, key=lambda o: o.observed_at)
        delta_t = (sorted_obs[-1].observed_at - sorted_obs[0].observed_at).total_seconds()
        if delta_t <= 0:
            return None, UNKNOWN
        delta_v = float(_to_decimal(sorted_obs[-1].value) - _to_decimal(sorted_obs[0].value))
        return float(Decimal(str(delta_v / delta_t)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)), "ok"
    elif agg_type == AggregationType.RATIO:
        total = sum(dec_vals)
        if total == 0:
            return None, UNKNOWN
        return float((dec_vals[0] / total).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)), "ok"
    elif agg_type == AggregationType.P50:
        return float(statistics.median(values)), "ok"
    elif agg_type == AggregationType.P95:
        if len(values) < 2:
            return None, UNKNOWN
        s = sorted(values)
        idx = int(len(s) * 0.95)
        return float(s[min(idx, len(s) - 1)]), "ok"
    elif agg_type == AggregationType.P99:
        if len(values) < 2:
            return None, UNKNOWN
        s = sorted(values)
        idx = int(len(s) * 0.99)
        return float(s[min(idx, len(s) - 1)]), "ok"

    return None, UNKNOWN


__all__ = ["aggregate", "UNKNOWN"]
