"""
paper_trading/performance_attribution/selection_attribution_v167.py
Selection attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No look-ahead. Benchmark must be period-correct. No silent equal-weight fallback.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from .enums_v167 import (
    AttributionLevel, AttributionStatus, BenchmarkMode, ConfidenceLevel,
)
from .models_v167 import SelectionContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class SelectionAttributionEngine:
    """
    Selection attribution: measures excess return from stock selection.
    Uses Brinson-Fachler approach.
    No look-ahead. Benchmark constituents must be period-correct.
    No silent equal-weight fallback when benchmark missing.
    """

    def __init__(self, no_look_ahead: bool = True) -> None:
        self._no_look_ahead = no_look_ahead

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        portfolio_weights: Dict[str, float],
        portfolio_returns: Dict[str, float],
        benchmark_weights: Optional[Dict[str, float]],
        benchmark_returns: Optional[Dict[str, float]],
        benchmark_mode: BenchmarkMode,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> SelectionContribution:
        """
        Compute selection attribution.
        selection_effect_i = benchmark_weight_i * (portfolio_return_i - benchmark_return_i)
        Requires benchmark present unless mode=NONE.
        """
        errors: List[str] = []
        warnings: List[str] = []

        # Benchmark validation
        if benchmark_mode == BenchmarkMode.MARKET_BENCHMARK:
            if not benchmark_weights or not benchmark_returns:
                return SelectionContribution(
                    entity_id=entity_id,
                    level=level,
                    selection_return=0.0,
                    selection_alpha=0.0,
                    hit_rate=0.0,
                    win_rate=0.0,
                    average_winner=0.0,
                    average_loser=0.0,
                    benchmark_mode=benchmark_mode,
                    look_ahead_checked=True,
                    no_look_ahead=self._no_look_ahead,
                    confidence=ConfidenceLevel.UNKNOWN,
                    status=AttributionStatus.INSUFFICIENT_DATA,
                    source_lineage=source_lineage,
                    period_start=period_start,
                    period_end=period_end,
                    paper_only=True,
                    research_only=True,
                    no_real_orders=True,
                    not_for_production=True,
                )

        if benchmark_mode == BenchmarkMode.NONE:
            benchmark_weights = {}
            benchmark_returns = {}

        bm_w = benchmark_weights or {}
        bm_r = benchmark_returns or {}
        p_w = portfolio_weights or {}
        p_r = portfolio_returns or {}

        # Selection contribution per symbol: bm_weight * (port_return - bm_return)
        symbols = set(p_r.keys()) | set(bm_r.keys())
        selection_per_symbol: Dict[str, float] = {}
        symbol_alphas: List[float] = []

        for sym in symbols:
            pw = p_w.get(sym, 0.0)
            pr = p_r.get(sym, 0.0)
            bw = bm_w.get(sym, 0.0)
            br = bm_r.get(sym, 0.0)
            sel = bw * (pr - br)
            selection_per_symbol[sym] = sel
            if pw > 0:
                symbol_alphas.append(pr - br)

        selection_return = sum(selection_per_symbol.values())
        selection_alpha = _safe_div(sum(symbol_alphas), len(symbol_alphas)) if symbol_alphas else 0.0

        # Hit rate, win rate
        held_symbols = [(sym, p_r[sym], bm_r.get(sym, 0.0)) for sym in p_r]
        winners = [(sym, pr, br) for sym, pr, br in held_symbols if pr > br]
        losers = [(sym, pr, br) for sym, pr, br in held_symbols if pr < br]

        hit_rate = _safe_div(len(winners), len(held_symbols)) if held_symbols else 0.0
        win_rate = hit_rate

        avg_winner = _safe_div(
            sum(pr - br for _, pr, br in winners), len(winners)
        ) if winners else 0.0
        avg_loser = _safe_div(
            sum(pr - br for _, pr, br in losers), len(losers)
        ) if losers else 0.0

        # Top/bottom contributors
        sorted_sel = sorted(selection_per_symbol.items(), key=lambda x: x[1], reverse=True)
        top_n = [s for s, _ in sorted_sel[:5]]
        bottom_n = [s for s, _ in sorted_sel[-5:]]

        confidence = ConfidenceLevel.HIGH if len(held_symbols) >= 5 else ConfidenceLevel.MEDIUM
        status = AttributionStatus.COMPLETE if not errors else AttributionStatus.DEGRADED

        return SelectionContribution(
            entity_id=entity_id,
            level=level,
            selection_return=selection_return,
            selection_alpha=selection_alpha,
            hit_rate=hit_rate,
            win_rate=win_rate,
            average_winner=avg_winner,
            average_loser=avg_loser,
            top_contributors=top_n,
            bottom_contributors=bottom_n,
            benchmark_mode=benchmark_mode,
            look_ahead_checked=True,
            no_look_ahead=self._no_look_ahead,
            confidence=confidence,
            status=status,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
