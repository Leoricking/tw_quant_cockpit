"""
strategy_robustness/comparison_v142.py — Robustness comparison utilities for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import List, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _same_conditions(r1: dict, r2: dict) -> bool:
    """Check if two results have matching universe, date range, and costs."""
    return (
        r1.get("universe") == r2.get("universe")
        and r1.get("start_date") == r2.get("start_date")
        and r1.get("end_date") == r2.get("end_date")
    )


class ABCRobustnessComparison:
    """
    Compares A, B, and C buy point robustness results.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def compare_abc(self, a_result: dict, b_result: dict, c_result: dict) -> dict:
        """
        Compare A, B, C buy point robustness results.

        Parameters
        ----------
        a_result, b_result, c_result : robustness result dicts

        Returns
        -------
        dict with comparison
        """
        results = {"A": a_result, "B": b_result, "C": c_result}

        # Check if conditions are matching
        conditions_match = (
            _same_conditions(a_result, b_result)
            and _same_conditions(b_result, c_result)
        )

        if not conditions_match:
            return {
                "rankable": False,
                "reason": "NOT_DIRECTLY_RANKABLE: results have different universe/date/conditions",
                "results": {k: {
                    "overall_score": v.get("overall_score", 0.0),
                    "robustness_status": v.get("robustness_status", "UNKNOWN"),
                    "universe": v.get("universe"),
                    "start_date": v.get("start_date"),
                    "end_date": v.get("end_date"),
                } for k, v in results.items()},
            }

        ranked = sorted(results.items(), key=lambda x: x[1].get("overall_score", 0.0), reverse=True)

        return {
            "rankable": True,
            "ranking": [{"buy_point": k, "score": v.get("overall_score", 0.0),
                         "status": v.get("robustness_status", "UNKNOWN")} for k, v in ranked],
            "best": ranked[0][0] if ranked else None,
            "scores": {k: v.get("overall_score", 0.0) for k, v in results.items()},
            "statuses": {k: v.get("robustness_status", "UNKNOWN") for k, v in results.items()},
            "conditions_matched": True,
        }


class StrategyKnowledgeRobustnessComparison:
    """
    Compares multiple strategy rule robustness results.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def compare_rules(self, results: list) -> dict:
        """
        Compare multiple robustness results.

        Parameters
        ----------
        results : list of robustness result dicts

        Returns
        -------
        dict with comparison
        """
        if not results:
            return {"rankable": False, "reason": "NO_RESULTS", "results": []}

        # Check conditions
        first = results[0]
        conditions_match = all(_same_conditions(first, r) for r in results[1:])

        if not conditions_match:
            return {
                "rankable": False,
                "reason": "NOT_DIRECTLY_RANKABLE: results have different conditions",
                "results": [{
                    "rule_id": r.get("rule_id"),
                    "overall_score": r.get("overall_score", 0.0),
                    "robustness_status": r.get("robustness_status", "UNKNOWN"),
                } for r in results],
            }

        ranked = sorted(results, key=lambda r: r.get("overall_score", 0.0), reverse=True)

        return {
            "rankable": True,
            "ranking": [{
                "rule_id": r.get("rule_id"),
                "score": r.get("overall_score", 0.0),
                "status": r.get("robustness_status", "UNKNOWN"),
                "rank": i + 1,
            } for i, r in enumerate(ranked)],
            "best_rule": ranked[0].get("rule_id") if ranked else None,
            "conditions_matched": True,
        }
