"""
strategy_robustness/query_v142.py — Query service for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import os
from typing import List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class StrategyRobustnessQueryService:
    """
    Read-only query service for strategy robustness results.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def __init__(self, base_dir: str = None):
        from strategy_robustness.store_v142 import StrategyRobustnessStore
        self._store = StrategyRobustnessStore(base_dir=base_dir)

    def list_runs(self) -> list:
        return self._store.list_runs()

    def get_result(self, robustness_id: str) -> Optional[dict]:
        return self._store.get_run(robustness_id)

    def list_by_rule(self, rule_id: str) -> list:
        return self._store.list_by_rule(rule_id)

    def list_by_status(self, status: str) -> list:
        return self._store.list_by_status(status)

    def list_robust(self) -> list:
        return self._store.list_robust()

    def list_fragile(self) -> list:
        return self._store.list_fragile()

    def list_decaying(self) -> list:
        return self._store.list_decaying()

    def list_regime_dependent(self) -> list:
        return self._store.list_regime_dependent()

    def list_parameter_sensitive(self) -> list:
        return self._store.list_parameter_sensitive()

    def list_cost_sensitive(self) -> list:
        return self._store.list_cost_sensitive()

    def compare_rules(self, ids: list) -> dict:
        from strategy_robustness.comparison_v142 import StrategyKnowledgeRobustnessComparison
        results = [self._store.get_run(rid) for rid in ids if self._store.get_run(rid)]
        comp = StrategyKnowledgeRobustnessComparison()
        return comp.compare_rules(results)

    def summarize(self) -> dict:
        return self._store.summarize()
