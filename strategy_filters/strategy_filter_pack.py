"""
strategy_filters/strategy_filter_pack.py — Strategy Filter Pack (v0.5.1.1).

Unified manager for all strategy filters.

[!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from strategy_filters.financial_turnaround_filter import FinancialTurnaroundFilter

logger = logging.getLogger(__name__)


class StrategyFilterPack:
    """
    Unified manager for all strategy filters.

    Instantiates and runs every filter in the pack; returns a combined result
    dict keyed by filter name.

    Safety invariants
    -----------------
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    No BUY / SELL / ORDER output is ever generated.
    """

    VERSION = "v0.5.1.1"

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self, mode: str = "real") -> None:
        self.mode = mode
        self._financial_turnaround = FinancialTurnaroundFilter(mode=mode)

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def run_all(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run every filter in the pack for a given stock_data dict.

        Returns
        -------
        dict with keys:
            symbol, filters, aggregate_score, suggested_action,
            research_only, no_real_orders, production_blocked
        """
        symbol  = str(stock_data.get("symbol", "UNKNOWN"))
        results: Dict[str, Any] = {}

        # --- Financial Turnaround ---
        try:
            ft_result = self._financial_turnaround.evaluate(stock_data)
            results["financial_turnaround"] = ft_result
        except Exception as exc:
            logger.warning("StrategyFilterPack.run_all: financial_turnaround failed: %s", exc)
            results["financial_turnaround"] = {
                "error":  str(exc),
                "score":  0,
                "labels": [],
            }

        # Aggregate score: currently only one filter; future-proofed for more
        scores = [v.get("score", 0) for v in results.values() if isinstance(v, dict)]
        agg_score = scores[0] if len(scores) == 1 else (sum(scores) / len(scores) if scores else 0)

        # Aggregate action: pick from financial_turnaround result
        agg_action = results.get("financial_turnaround", {}).get("suggested_action", "WATCH")

        # v0.9.0.1 crash reversal integration
        crash_reversal_fields = {
            "crash_cause":                        None,
            "stabilization_score":                None,
            "relative_strength_after_crash":      None,
            "sakata_dip_buy_eligibility":         None,
            "ma_profit_discipline":               None,
            "high_risk_industry_guard":           None,
        }
        try:
            from strategy_filters.crash_reversal_strategy_pack import CrashReversalStrategyPack
            _crsp = CrashReversalStrategyPack()
            _cr_result = _crsp.evaluate_market(stock_data)
            crash_reversal_fields["crash_cause"]                   = _cr_result.get("crash_cause")
            crash_reversal_fields["stabilization_score"]           = _cr_result.get("stabilization_score")
            crash_reversal_fields["relative_strength_after_crash"] = _cr_result.get("relative_strength_after_crash")
            crash_reversal_fields["sakata_dip_buy_eligibility"]    = _cr_result.get("sakata_dip_buy_eligibility")
            crash_reversal_fields["ma_profit_discipline"]          = _cr_result.get("ma_profit_discipline")
            crash_reversal_fields["high_risk_industry_guard"]      = _cr_result.get("high_risk_industry_guard")
        except (ImportError, Exception) as _cr_exc:
            logger.debug("StrategyFilterPack: crash_reversal_strategy_pack unavailable: %s", _cr_exc)
            crash_reversal_fields = {k: "INSUFFICIENT_DATA" for k in crash_reversal_fields}

        return {
            "symbol":            symbol,
            "filters":           results,
            "aggregate_score":   round(agg_score, 1),
            "suggested_action":  agg_action,
            "research_only":     True,
            "no_real_orders":    True,
            "production_blocked": True,
            "pack_version":      self.VERSION,
            **crash_reversal_fields,
        }

    def run_financial_turnaround(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run only the Financial Turnaround & Trend Discipline filter.

        Returns the raw FinancialTurnaroundFilter.evaluate() result.
        """
        return self._financial_turnaround.evaluate(stock_data)

    # ------------------------------------------------------------------
    # Batch run
    # ------------------------------------------------------------------

    def run_all_batch(self, stocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run all filters for a list of stock_data dicts.

        Parameters
        ----------
        stocks : list of stock_data dicts

        Returns
        -------
        list of run_all() results, sorted by aggregate_score descending
        """
        results = []
        for sd in stocks:
            try:
                res = self.run_all(sd)
                results.append(res)
            except Exception as exc:
                sym = sd.get("symbol", "?")
                logger.warning("StrategyFilterPack.run_all_batch: %s failed: %s", sym, exc)
                results.append({
                    "symbol":           sym,
                    "filters":          {},
                    "aggregate_score":  0,
                    "suggested_action": "WATCH",
                    "error":            str(exc),
                })

        results.sort(key=lambda r: r.get("aggregate_score", 0), reverse=True)
        return results

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_summary(self, pack_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Summarize a list of run_all() results.

        Returns counts by suggested_action and top candidates.
        """
        action_counts: Dict[str, int] = {}
        strong_candidates = []
        watch_candidates  = []

        for r in pack_results:
            action = r.get("suggested_action", "WATCH")
            action_counts[action] = action_counts.get(action, 0) + 1
            score  = r.get("aggregate_score", 0)
            if score >= 80:
                strong_candidates.append({"symbol": r.get("symbol"), "score": score, "action": action})
            elif score >= 65:
                watch_candidates.append({"symbol": r.get("symbol"), "score": score, "action": action})

        return {
            "total_stocks":         len(pack_results),
            "action_counts":        action_counts,
            "strong_candidates":    strong_candidates,
            "watch_candidates":     watch_candidates,
            "research_only":        True,
            "no_real_orders":       True,
            "production_blocked":   True,
        }
