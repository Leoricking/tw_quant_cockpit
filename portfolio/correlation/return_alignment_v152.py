"""
portfolio/correlation/return_alignment_v152.py — Return Alignment Service v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List, Optional

from portfolio.correlation.enums_v152 import (
    AlignmentMethod,
    CorrelationStatus,
    ReturnMethod,
)
from portfolio.correlation.models_v152 import AlignedReturnSeries

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class ReturnAlignmentService:
    """
    Aligns price series across symbols and computes returns.

    Rules:
    - Does NOT forward-fill.
    - Does NOT treat missing dates as 0.
    - Inner join: only dates present in ALL symbols.
    - Pairwise complete: used only for pairwise diagnostics (not bulk alignment).
    - Raises ValueError on duplicate dates within a single symbol's price series.
    - Blocks if any date > as_of (future-data guard).
    """

    RESEARCH_ONLY = True

    def align(
        self,
        prices_by_symbol: Dict[str, Dict[str, float]],
        as_of: str,
        method: AlignmentMethod = AlignmentMethod.INNER_JOIN,
        return_method: ReturnMethod = ReturnMethod.SIMPLE,
        minimum_observations: int = 60,
    ) -> AlignedReturnSeries:
        """
        Align price series and compute returns.

        Args:
            prices_by_symbol: {symbol: {date_str: price}}
            as_of: ISO date string — no data beyond this date is used
            method: alignment method
            return_method: SIMPLE or LOG
            minimum_observations: minimum required observations

        Returns:
            AlignedReturnSeries
        """
        if not prices_by_symbol:
            return AlignedReturnSeries(
                symbols=[],
                dates=[],
                returns_by_symbol={},
                observation_count=0,
                start_date="",
                end_date="",
                status=CorrelationStatus.INSUFFICIENT_SAMPLE,
            )

        symbols = sorted(prices_by_symbol.keys())

        # Validate: check for duplicate dates and future data
        blocked = False
        for sym, price_map in prices_by_symbol.items():
            dates_for_sym = list(price_map.keys())
            if len(dates_for_sym) != len(set(dates_for_sym)):
                raise ValueError(f"Duplicate dates detected for symbol {sym}")
            for d in dates_for_sym:
                if d > as_of:
                    blocked = True

        # Gather sorted date sets per symbol (filtered to <= as_of)
        dates_by_symbol: Dict[str, List[str]] = {}
        for sym in symbols:
            price_map = prices_by_symbol[sym]
            valid_dates = sorted(d for d in price_map if d <= as_of)
            dates_by_symbol[sym] = valid_dates

        # Inner join: intersection of all symbols' date sets
        if method == AlignmentMethod.INNER_JOIN:
            common_dates_set = set(dates_by_symbol[symbols[0]])
            for sym in symbols[1:]:
                common_dates_set &= set(dates_by_symbol[sym])
            common_dates = sorted(common_dates_set)
        else:
            # PAIRWISE_COMPLETE: use union for bulk alignment (pairwise handled separately)
            all_dates_set: set = set()
            for sym in symbols:
                all_dates_set |= set(dates_by_symbol[sym])
            common_dates = sorted(all_dates_set)

        # missing_by_symbol: count per-symbol how many common dates they lack prices for
        missing_by_symbol: Dict[str, int] = {}
        for sym in symbols:
            sym_date_set = set(dates_by_symbol[sym])
            missing_by_symbol[sym] = sum(1 for d in common_dates if d not in sym_date_set)

        # Compute returns for each symbol over common_dates
        returns_by_symbol: Dict[str, List[float]] = {}
        for sym in symbols:
            price_map = prices_by_symbol[sym]
            sym_returns: List[float] = []
            for i in range(1, len(common_dates)):
                d_prev = common_dates[i - 1]
                d_curr = common_dates[i]
                p_prev = price_map.get(d_prev)
                p_curr = price_map.get(d_curr)
                if p_prev is None or p_curr is None or p_prev == 0:
                    continue  # skip missing
                if return_method == ReturnMethod.LOG:
                    sym_returns.append(math.log(p_curr / p_prev))
                else:
                    sym_returns.append((p_curr / p_prev) - 1.0)
            returns_by_symbol[sym] = sym_returns

        # observation_count: minimum across all symbols
        obs_counts = [len(v) for v in returns_by_symbol.values()]
        observation_count = min(obs_counts) if obs_counts else 0

        # Determine date range (returns start from index 1)
        return_dates = common_dates[1:] if len(common_dates) > 1 else []
        start_date = return_dates[0] if return_dates else ""
        end_date   = return_dates[-1] if return_dates else ""

        # Status
        if blocked:
            status = CorrelationStatus.BLOCKED
        elif observation_count < minimum_observations:
            status = CorrelationStatus.INSUFFICIENT_SAMPLE
        else:
            status = CorrelationStatus.VALID

        # Content hash
        content_hash = _compute_hash({
            "symbols": symbols,
            "return_dates": return_dates,
            "returns_by_symbol": {k: v for k, v in sorted(returns_by_symbol.items())},
        })

        return AlignedReturnSeries(
            symbols=symbols,
            dates=return_dates,
            returns_by_symbol=returns_by_symbol,
            observation_count=observation_count,
            start_date=start_date,
            end_date=end_date,
            missing_by_symbol=missing_by_symbol,
            alignment_method=method,
            return_method=return_method,
            status=status,
            content_hash=content_hash,
        )


def _compute_hash(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]
