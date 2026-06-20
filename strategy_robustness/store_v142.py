"""
strategy_robustness/store_v142.py — Persistence store for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
Data saved to data/strategy_robustness/ (runtime, NOT committed).
"""
from __future__ import annotations

import json
import os
import tempfile
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

SCHEMA_VERSION = "1.4.2"
STORE_FILES = [
    "robustness_runs.json",
    "robustness_results.json",
    "parameter_sensitivity_results.json",
    "cost_stress_results.json",
    "bootstrap_results.json",
    "monte_carlo_results.json",
    "decay_results.json",
    "comparison_results.json",
]


class StrategyRobustnessStore:
    """
    Atomic-write, versioned store for strategy robustness results.
    Never overwrites old results; never saves credentials.
    Graceful on corruption; forward-compatible with unknown fields.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(base_dir, "data", "strategy_robustness")
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_path(self, filename: str) -> str:
        return os.path.join(self.data_dir, filename)

    def _load_json(self, filename: str) -> list:
        path = self._get_path(filename)
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                if isinstance(data, dict) and "items" in data:
                    return data["items"]
                return []
        except Exception as exc:
            logger.warning("Store load error for %s: %s", filename, exc)
            return []

    def _save_json(self, filename: str, data: list) -> None:
        """Atomic write."""
        path = self._get_path(filename)
        payload = {"schema_version": SCHEMA_VERSION, "items": data}
        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.data_dir, suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, path)
        except Exception as exc:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            raise exc

    def save_run(self, run_dict: dict) -> None:
        """Append a robustness run (never overwrites existing)."""
        items = self._load_json("robustness_runs.json")
        # Avoid duplicate by robustness_id
        existing_ids = {item.get("robustness_id") for item in items}
        if run_dict.get("robustness_id") not in existing_ids:
            items.append(run_dict)
            self._save_json("robustness_runs.json", items)

    def save_result(self, result_dict: dict) -> None:
        """Append a full robustness result."""
        items = self._load_json("robustness_results.json")
        existing_ids = {item.get("robustness_id") for item in items}
        if result_dict.get("robustness_id") not in existing_ids:
            items.append(result_dict)
            self._save_json("robustness_results.json", items)

    def save_comparison(self, comparison_dict: dict) -> None:
        """Append a comparison result."""
        items = self._load_json("comparison_results.json")
        items.append(comparison_dict)
        self._save_json("comparison_results.json", items)

    def list_runs(self) -> list:
        return self._load_json("robustness_runs.json")

    def get_run(self, robustness_id: str) -> Optional[dict]:
        items = self._load_json("robustness_results.json")
        for item in items:
            if item.get("robustness_id") == robustness_id:
                return item
        # Fallback to runs index
        runs = self._load_json("robustness_runs.json")
        for r in runs:
            if r.get("robustness_id") == robustness_id:
                return r
        return None

    def list_by_rule(self, rule_id: str) -> list:
        items = self._load_json("robustness_results.json")
        return [i for i in items if i.get("rule_id") == rule_id]

    def list_by_status(self, status: str) -> list:
        items = self._load_json("robustness_results.json")
        return [i for i in items if i.get("robustness_status") == status]

    def list_robust(self) -> list:
        return self.list_by_status("ROBUST")

    def list_fragile(self) -> list:
        return self.list_by_status("FRAGILE")

    def list_decaying(self) -> list:
        items = self._load_json("robustness_results.json")
        from strategy_robustness.models_v142 import DecayStatus
        return [
            i for i in items
            if i.get("decay", {}).get("decay_status") in (
                DecayStatus.POSSIBLE_DECAY, DecayStatus.SIGNIFICANT_DECAY
            )
        ]

    def list_regime_dependent(self) -> list:
        items = self._load_json("robustness_results.json")
        return [i for i in items if i.get("robustness_status") == "REGIME_DEPENDENT"
                or i.get("regime_robustness", {}).get("regime_dependency_score", 0.0) >= 0.6]

    def list_parameter_sensitive(self) -> list:
        items = self._load_json("robustness_results.json")
        return [i for i in items if i.get("robustness_status") == "PARAMETER_SENSITIVE"]

    def list_cost_sensitive(self) -> list:
        items = self._load_json("robustness_results.json")
        return [i for i in items if i.get("cost_stress", {}).get("status") == "COST_SENSITIVE"]

    def summarize(self) -> dict:
        items = self._load_json("robustness_results.json")
        runs = self._load_json("robustness_runs.json")
        return {
            "schema_version": SCHEMA_VERSION,
            "total_results": len(items),
            "total_runs": len(runs),
            "robust_count": sum(1 for i in items if i.get("robustness_status") == "ROBUST"),
            "fragile_count": sum(1 for i in items if i.get("robustness_status") == "FRAGILE"),
            "blocked_count": sum(1 for i in items if i.get("robustness_status") == "BLOCKED"),
        }
