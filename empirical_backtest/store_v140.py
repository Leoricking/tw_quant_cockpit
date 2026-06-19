"""
empirical_backtest/store_v140.py — Empirical Backtest Store for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import json
import os
from typing import Optional, List
from .models_v140 import BacktestResult, StrategyRuleSnapshot, BacktestStatus

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_VERSION = "1.4.0"


class EmpiricalBacktestStore:
    """Persistent store for empirical backtest results."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            self._storage_dir = os.path.join(BASE_DIR, "data", "empirical_backtest")
        else:
            self._storage_dir = os.path.abspath(storage_dir)

    def _ensure_dir(self) -> None:
        os.makedirs(self._storage_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._storage_dir, filename)

    def _load(self, filename: str) -> dict:
        path = self._path(filename)
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save(self, filename: str, data: dict) -> None:
        self._ensure_dir()
        path = self._path(filename)
        tmp_path = path + ".tmp"
        data["schema_version"] = SCHEMA_VERSION
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)

    def save_result(self, result: BacktestResult) -> None:
        """Append-only: save a backtest result by backtest_id."""
        data = self._load("backtest_results.json")
        backtest_id = result.backtest_id
        if backtest_id not in data:
            data[backtest_id] = result.to_dict()
        self._save("backtest_results.json", data)

    def get_result(self, backtest_id: str) -> Optional[dict]:
        data = self._load("backtest_results.json")
        return data.get(backtest_id)

    def save_run(self, run_info: dict) -> None:
        """Append-only: save run metadata."""
        data = self._load("backtest_runs.json")
        run_id = run_info.get("backtest_id", str(len(data)))
        if run_id not in data:
            data[run_id] = run_info
        self._save("backtest_runs.json", data)

    def save_snapshot(self, snapshot: StrategyRuleSnapshot) -> None:
        """Append-only: save a rule snapshot."""
        data = self._load("strategy_rule_snapshots.json")
        sid = snapshot.snapshot_id
        if sid not in data:
            data[sid] = snapshot.to_dict()
        self._save("strategy_rule_snapshots.json", data)


class EmpiricalBacktestQueryService:
    """Query interface for empirical backtest store."""

    def __init__(self, store: EmpiricalBacktestStore):
        self._store = store

    def list_runs(self) -> list:
        data = self._store._load("backtest_runs.json")
        return [v for k, v in data.items() if k != "schema_version"]

    def get_run(self, backtest_id: str) -> Optional[dict]:
        data = self._store._load("backtest_runs.json")
        return data.get(backtest_id)

    def get_result(self, backtest_id: str) -> Optional[dict]:
        return self._store.get_result(backtest_id)

    def list_by_rule(self, rule_id: str) -> list:
        data = self._store._load("backtest_results.json")
        return [
            v for k, v in data.items()
            if k != "schema_version" and v.get("strategy_snapshot_id", "").endswith(rule_id)
        ]

    def list_by_symbol(self, symbol: str) -> list:
        data = self._store._load("backtest_results.json")
        return [
            v for k, v in data.items()
            if k != "schema_version" and symbol in v.get("symbols_requested", [])
        ]

    def list_by_universe(self, universe_id: str) -> list:
        data = self._store._load("backtest_results.json")
        return [
            v for k, v in data.items()
            if k != "schema_version" and v.get("configuration", {}).get("universe_id") == universe_id
        ]

    def list_passed(self) -> list:
        data = self._store._load("backtest_results.json")
        return [v for k, v in data.items() if k != "schema_version" and v.get("status") == BacktestStatus.PASS]

    def list_blocked(self) -> list:
        data = self._store._load("backtest_results.json")
        return [v for k, v in data.items() if k != "schema_version" and v.get("status") == BacktestStatus.BLOCKED]

    def list_insufficient(self) -> list:
        data = self._store._load("backtest_results.json")
        return [
            v for k, v in data.items()
            if k != "schema_version" and v.get("status") == BacktestStatus.INSUFFICIENT_DATA
        ]

    def compare_runs(self, backtest_id_a: str, backtest_id_b: str) -> dict:
        result_a = self._store.get_result(backtest_id_a)
        result_b = self._store.get_result(backtest_id_b)
        return {
            "backtest_id_a": backtest_id_a,
            "backtest_id_b": backtest_id_b,
            "result_a": result_a,
            "result_b": result_b,
            "comparable": result_a is not None and result_b is not None,
        }

    def summarize(self) -> dict:
        data = self._store._load("backtest_results.json")
        results = [v for k, v in data.items() if k != "schema_version"]
        status_counts: dict = {}
        for r in results:
            s = r.get("status", "UNKNOWN")
            status_counts[s] = status_counts.get(s, 0) + 1
        return {
            "total_runs": len(results),
            "by_status": status_counts,
            "schema_version": SCHEMA_VERSION,
        }
