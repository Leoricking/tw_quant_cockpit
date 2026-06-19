"""
abc_validation/comparison_engine_v141.py — A/B/C comparison engine v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Requires same universe, date range, costs, slippage, execution model, benchmark,
data quality for direct comparison. Otherwise flags as "not directly rankable".
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


COMPARISON_MODES = [
    "a_vs_b", "a_vs_c", "b_vs_c", "a_vs_b_vs_c",
    "strict_vs_relaxed", "base_vs_full_filters",
    "second_wave_vs_non", "regime_specific",
    "holding_period_specific", "stop_model_specific",
]

REQUIRED_SAME_FIELDS = [
    "universe", "date_range", "cost_model", "slippage_model",
    "execution_model", "benchmark", "data_quality",
]


def _check_comparability(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check if results are directly comparable (same universe, costs, etc.)."""
    if len(results) < 2:
        return {"directly_comparable": True, "issues": []}

    issues = []
    ref = results[0]

    for i, r in enumerate(results[1:], 1):
        for field in REQUIRED_SAME_FIELDS:
            ref_val = ref.get(field)
            r_val = r.get(field)
            if ref_val is not None and r_val is not None and ref_val != r_val:
                issues.append(
                    f"results[0] vs results[{i}]: {field} differs "
                    f"({ref_val!r} vs {r_val!r})"
                )

    return {
        "directly_comparable": len(issues) == 0,
        "issues": issues,
    }


class ABCComparisonEngine:
    """
    Compares A/B/C buy point validation results.

    Supported comparisons: A vs B, A vs C, B vs C, A vs B vs C,
    strict vs relaxed, base vs full filters, second-wave vs non,
    regime-specific, holding-period-specific, stop-model-specific.
    """

    def compare(
        self,
        results: List[Dict[str, Any]],
        mode: str = "a_vs_b_vs_c",
    ) -> Dict[str, Any]:
        """Compare validation results."""
        if mode not in COMPARISON_MODES:
            raise ValueError(f"Unknown comparison mode: {mode}. Choose from {COMPARISON_MODES}")

        comparability = _check_comparability(results)

        if not comparability["directly_comparable"]:
            return {
                "mode": mode,
                "directly_rankable": False,
                "reason": "Results differ in universe/date/costs/model — cannot directly rank",
                "comparability_issues": comparability["issues"],
                "results": [self._summarize_result(r) for r in results],
                "no_real_orders": True,
            }

        summaries = [self._summarize_result(r) for r in results]

        # Build comparison table
        comparison_table = {}
        metrics_to_compare = ["win_rate", "expectancy", "drawdown", "signal_count", "trade_count"]
        for metric in metrics_to_compare:
            comparison_table[metric] = {
                s.get("buy_point_type", f"result_{i}"): s.get(metric)
                for i, s in enumerate(summaries)
            }

        return {
            "mode": mode,
            "directly_rankable": True,
            "comparison_table": comparison_table,
            "summaries": summaries,
            "note": "Comparison valid only if data quality, universe, and costs are identical.",
            "no_real_orders": True,
        }

    def _summarize_result(self, result: dict) -> dict:
        hp = result.get("holding_period_results", {})
        period5 = hp.get("period_results", {}).get(5, {}) if isinstance(hp, dict) else {}
        return {
            "buy_point_type": result.get("buy_point_type"),
            "validation_id": result.get("validation_id"),
            "signal_count": result.get("signal_count", 0),
            "trade_count": result.get("trade_count", 0),
            "win_rate": period5.get("win_rate"),
            "expectancy": period5.get("expectancy"),
            "drawdown": period5.get("max_drawdown"),
            "confidence": result.get("confidence", "INSUFFICIENT"),
            "formal_conclusion_allowed": result.get("formal_conclusion_allowed", False),
            "universe": result.get("universe"),
            "date_range": result.get("date_range"),
            "cost_model": result.get("configuration", {}).get("cost_model"),
            "slippage_model": result.get("configuration", {}).get("slippage_model"),
            "execution_model": result.get("configuration", {}).get("execution_model"),
            "benchmark": result.get("configuration", {}).get("benchmark"),
            "data_quality": result.get("quality_summary", {}).get("overall"),
        }
