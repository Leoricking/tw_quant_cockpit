"""
abc_validation/store_v141.py — Validation store for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Atomic writes, versioned schema, corruption-tolerant, old schema loading,
forward-compatible unknown fields.
"""
from __future__ import annotations

import json
import os
import tempfile
from typing import Any, Dict, List, Optional

SCHEMA_VERSION = "1.4.1"
STORE_DIR = "data/abc_validation"


def _store_path(base_dir: str, filename: str) -> str:
    return os.path.join(base_dir, STORE_DIR, filename)


def _atomic_write(path: str, data: Any) -> None:
    """Write JSON atomically (write to temp then rename)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
        raise


def _safe_load(path: str) -> Any:
    """Load JSON tolerantly — returns empty list on corruption/missing."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


class ABCValidationStore:
    """
    Persistence layer for A/B/C validation results.

    Files:
    - abc_rule_snapshots.json
    - abc_validation_runs.json
    - abc_validation_results.json
    - abc_comparison_results.json
    - abc_ablation_results.json
    - abc_walk_forward_results.json
    """

    def __init__(self, base_dir: str = ""):
        self.base_dir = base_dir or os.getcwd()
        self._store_dir = os.path.join(self.base_dir, STORE_DIR)

    def _path(self, filename: str) -> str:
        return os.path.join(self._store_dir, filename)

    def _load(self, filename: str) -> list:
        return _safe_load(self._path(filename))

    def _save(self, filename: str, data: Any) -> None:
        _atomic_write(self._path(filename), data)

    # ── Snapshots ────────────────────────────────────────────────────────────

    def save_snapshot(self, snapshot: dict) -> None:
        snaps = self._load("abc_rule_snapshots.json")
        # Deduplicate by snapshot_id
        existing_ids = {s.get("snapshot_id") for s in snaps}
        if snapshot.get("snapshot_id") not in existing_ids:
            snaps.append(snapshot)
            self._save("abc_rule_snapshots.json", snaps)

    def list_snapshots(self) -> list:
        return self._load("abc_rule_snapshots.json")

    # ── Validation Runs ──────────────────────────────────────────────────────

    def save_run(self, run: dict) -> None:
        runs = self._load("abc_validation_runs.json")
        runs.append(run)
        self._save("abc_validation_runs.json", runs)

    def list_runs(self) -> list:
        return self._load("abc_validation_runs.json")

    def get_run(self, run_id: str) -> Optional[dict]:
        runs = self.list_runs()
        for r in runs:
            if r.get("validation_id") == run_id or r.get("run_id") == run_id:
                return r
        return None

    # ── Validation Results ───────────────────────────────────────────────────

    def save_result(self, result: dict) -> None:
        results = self._load("abc_validation_results.json")
        results.append(result)
        self._save("abc_validation_results.json", results)

    def list_results(self) -> list:
        return self._load("abc_validation_results.json")

    def list_by_buy_point_type(self, buy_point_type: str) -> list:
        return [r for r in self.list_results() if r.get("buy_point_type") == buy_point_type]

    def list_by_symbol(self, symbol: str) -> list:
        return [r for r in self.list_results() if symbol in r.get("symbols_tested", [])]

    def list_by_universe(self, universe: str) -> list:
        return [r for r in self.list_results() if r.get("universe") == universe]

    def list_passed(self) -> list:
        return [r for r in self.list_results() if r.get("confidence") in ("HIGH", "MEDIUM")]

    def list_blocked(self) -> list:
        return [r for r in self.list_results() if r.get("confidence") == "BLOCKED"]

    def list_insufficient(self) -> list:
        return [r for r in self.list_results() if r.get("confidence") == "INSUFFICIENT"]

    # ── Comparison Results ───────────────────────────────────────────────────

    def save_comparison(self, comparison: dict) -> None:
        comparisons = self._load("abc_comparison_results.json")
        comparisons.append(comparison)
        self._save("abc_comparison_results.json", comparisons)

    def compare_abc(self) -> list:
        return self._load("abc_comparison_results.json")

    # ── Ablation Results ─────────────────────────────────────────────────────

    def save_ablation(self, ablation: dict) -> None:
        ablations = self._load("abc_ablation_results.json")
        ablations.append(ablation)
        self._save("abc_ablation_results.json", ablations)

    def list_ablation_results(self) -> list:
        return self._load("abc_ablation_results.json")

    # ── Walk-Forward Results ─────────────────────────────────────────────────

    def save_walk_forward(self, wf: dict) -> None:
        wfs = self._load("abc_walk_forward_results.json")
        wfs.append(wf)
        self._save("abc_walk_forward_results.json", wfs)

    def list_walk_forward_results(self) -> list:
        return self._load("abc_walk_forward_results.json")

    # ── Summary ──────────────────────────────────────────────────────────────

    def summarize(self) -> dict:
        results = self.list_results()
        return {
            "schema_version": SCHEMA_VERSION,
            "total_validation_results": len(results),
            "passed": len(self.list_passed()),
            "blocked": len(self.list_blocked()),
            "insufficient": len(self.list_insufficient()),
            "by_type": {
                "A": len(self.list_by_buy_point_type("A")),
                "B": len(self.list_by_buy_point_type("B")),
                "C": len(self.list_by_buy_point_type("C")),
            },
            "comparisons": len(self.compare_abc()),
            "ablation_runs": len(self.list_ablation_results()),
            "walk_forward_runs": len(self.list_walk_forward_results()),
            "no_real_orders": True,
        }
