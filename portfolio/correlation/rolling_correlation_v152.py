"""
portfolio/correlation/rolling_correlation_v152.py — Rolling Correlation Service v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional

from portfolio.correlation.enums_v152 import CorrelationStatus, ReturnMethod
from portfolio.correlation.models_v152 import RollingCorrelationPoint

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"

RISING_CORRELATION_WARNING = "RISING_CORRELATION_WARNING"


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _pearson(xs: List[float], ys: List[float]) -> Optional[float]:
    """Returns Pearson correlation or None if series is constant."""
    n = len(xs)
    if n < 2:
        return None
    mx = _mean(xs)
    my = _mean(ys)
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den_x = sum((x - mx) ** 2 for x in xs)
    den_y = sum((y - my) ** 2 for y in ys)
    if den_x == 0.0 or den_y == 0.0:
        return None
    r = num / math.sqrt(den_x * den_y)
    return max(-1.0, min(1.0, r))


class RollingCorrelationService:
    """
    Computes rolling correlation between a pair of symbols.
    No future leakage — only dates <= as_of are used.
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        prices_by_symbol: Dict[str, Dict[str, float]],
        symbol_a: str,
        symbol_b: str,
        window: int = 60,
        as_of: Optional[str] = None,
        return_method: ReturnMethod = ReturnMethod.SIMPLE,
    ) -> List[RollingCorrelationPoint]:
        """
        Calculate rolling correlations for a symbol pair.

        Returns a list of RollingCorrelationPoint sorted ascending by date.
        Only windows with exactly `window` complete observations are included.
        """
        if symbol_a not in prices_by_symbol or symbol_b not in prices_by_symbol:
            return []

        prices_a = prices_by_symbol[symbol_a]
        prices_b = prices_by_symbol[symbol_b]

        # Intersect dates, filter to <= as_of
        dates_a = set(prices_a.keys())
        dates_b = set(prices_b.keys())
        common = sorted(dates_a & dates_b)
        if as_of is not None:
            common = [d for d in common if d <= as_of]

        if len(common) < 2:
            return []

        # Compute returns on common dates
        returns_a: List[float] = []
        returns_b: List[float] = []
        return_dates: List[str] = []

        for i in range(1, len(common)):
            pa_prev = prices_a[common[i - 1]]
            pa_curr = prices_a[common[i]]
            pb_prev = prices_b[common[i - 1]]
            pb_curr = prices_b[common[i]]
            if pa_prev == 0 or pb_prev == 0:
                continue
            if return_method == ReturnMethod.LOG:
                ra = math.log(pa_curr / pa_prev)
                rb = math.log(pb_curr / pb_prev)
            else:
                ra = (pa_curr / pa_prev) - 1.0
                rb = (pb_curr / pb_prev) - 1.0
            returns_a.append(ra)
            returns_b.append(rb)
            return_dates.append(common[i])

        n_returns = len(returns_a)
        if n_returns < window:
            return []

        points: List[RollingCorrelationPoint] = []

        # Compute correlations for all windows of size `window`
        # Also keep a 120-window result for RISING_CORRELATION_WARNING check
        corr_map: Dict[str, float] = {}  # date → 60-day corr
        corr_120_map: Dict[str, float] = {}

        for end_idx in range(window - 1, n_returns):
            start_idx = end_idx - window + 1
            xs = returns_a[start_idx:end_idx + 1]
            ys = returns_b[start_idx:end_idx + 1]
            r = _pearson(xs, ys)
            date = return_dates[end_idx]
            if r is not None:
                corr_map[date] = r

        # 120-window for warning check
        if window == 60:
            for end_idx in range(120 - 1, n_returns):
                start_idx = end_idx - 120 + 1
                xs = returns_a[start_idx:end_idx + 1]
                ys = returns_b[start_idx:end_idx + 1]
                r120 = _pearson(xs, ys)
                date = return_dates[end_idx]
                if r120 is not None:
                    corr_120_map[date] = r120

        for date in sorted(corr_map.keys()):
            r = corr_map[date]
            metadata: dict = {}

            # RISING_CORRELATION_WARNING
            if window == 60 and r > 0.8 and date in corr_120_map:
                r120 = corr_120_map[date]
                if r > r120:
                    metadata["warning"] = RISING_CORRELATION_WARNING
                    metadata["corr_60"] = r
                    metadata["corr_120"] = r120

            points.append(RollingCorrelationPoint(
                symbol_a=symbol_a,
                symbol_b=symbol_b,
                window=window,
                as_of=date,
                correlation=r,
                observation_count=window,
                status=CorrelationStatus.VALID,
                metadata=metadata,
            ))

        return points
