"""
strategy_robustness/repair_integration_v142.py — Repair integration for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No auto repair. No auto refresh. No auto download. No mock fallback.
"""
from __future__ import annotations

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

REPAIR_ISSUES = [
    "industry_metadata_missing",
    "stale_source_result",
    "insufficient_symbols",
    "insufficient_trades",
    "data_gaps",
    "source_conflict",
    "corporate_action_unknown",
    "benchmark_missing",
    "missing_oos_period",
]


class RobustnessRepairIntegration:
    """
    Identifies repair needs from robustness analysis.
    Uses CoverageRepairQueue dedup. No auto repair/refresh/download. No mock fallback.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def __init__(self, create_repair_tasks: bool = False, base_dir: str = None):
        self.create_repair_tasks = create_repair_tasks
        self.base_dir = base_dir

    def identify_repair_needs(self, robustness_result: dict) -> list:
        """
        Identify repair needs from a robustness result.

        Parameters
        ----------
        robustness_result : dict

        Returns
        -------
        list of repair need dicts
        """
        repair_needs = []

        # industry_metadata_missing
        industry = robustness_result.get("industry_robustness", {})
        if industry.get("no_industry_count", 0) > 0:
            repair_needs.append({
                "issue": "industry_metadata_missing",
                "count": industry.get("no_industry_count"),
                "action_required": "PROVIDE_INDUSTRY_MAP",
                "priority": "MEDIUM",
                "auto_repair": False,
            })

        # insufficient_symbols
        cross = robustness_result.get("cross_sectional", {})
        if cross.get("symbols_total", 0) < 5:
            repair_needs.append({
                "issue": "insufficient_symbols",
                "symbols_found": cross.get("symbols_total", 0),
                "minimum_required": 5,
                "action_required": "EXPAND_SYMBOL_COVERAGE",
                "priority": "HIGH",
                "auto_repair": False,
            })

        # insufficient_trades
        if robustness_result.get("trade_count", 0) < 30:
            repair_needs.append({
                "issue": "insufficient_trades",
                "trade_count": robustness_result.get("trade_count", 0),
                "minimum_required": 30,
                "action_required": "EXTEND_DATE_RANGE_OR_UNIVERSE",
                "priority": "HIGH",
                "auto_repair": False,
            })

        # missing_oos_period
        bootstrap = robustness_result.get("bootstrap", {})
        if bootstrap.get("status") == "INSUFFICIENT":
            repair_needs.append({
                "issue": "missing_oos_period",
                "action_required": "ADD_OUT_OF_SAMPLE_PERIOD",
                "priority": "HIGH",
                "auto_repair": False,
            })

        return repair_needs

    def create_repair_candidates(self, repair_needs: list) -> list:
        """
        Preview repair candidates (never executes). Returns list of candidate dicts.
        Requires create_repair_tasks=True to attempt queue insertion.
        """
        if not self.create_repair_tasks:
            return [{**need, "status": "PREVIEW_ONLY", "queued": False} for need in repair_needs]

        candidates = []
        try:
            from coverage_repair.queue_v133 import CoverageRepairQueue
            queue = CoverageRepairQueue(base_dir=self.base_dir)
            for need in repair_needs:
                try:
                    task_id = queue.add_task({
                        "source": "strategy_robustness_v142",
                        "issue": need.get("issue"),
                        "priority": need.get("priority", "MEDIUM"),
                        "action_required": need.get("action_required", "REVIEW"),
                        "auto_repair": False,
                        "no_mock_fallback": True,
                    })
                    candidates.append({**need, "status": "QUEUED", "task_id": task_id})
                except Exception as exc:
                    candidates.append({**need, "status": "QUEUE_ERROR", "error": str(exc)})
        except ImportError:
            candidates = [{**need, "status": "PREVIEW_ONLY", "queued": False} for need in repair_needs]

        return candidates
