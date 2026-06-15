"""
gate_enforcement.enforcement_query — EnforcementQuery v1.1.5

Query functions for gate enforcement runtime data.
Research Only. No Real Orders.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "quality_gate_enforcement")


class EnforcementQuery:
    """Query API for gate enforcement runtime data."""

    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR, audit_dir: str = ""):
        self._output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(BASE_DIR, output_dir)
        from gate_enforcement.enforcement_store import EnforcementStore
        self._store = EnforcementStore(output_dir=self._output_dir)

    def latest_runs(self, limit: int = 20) -> List[dict]:
        results = self._store.list_results()
        return results[-limit:] if results else []

    def get_run(self, run_id: str) -> dict:
        result = self._store.get_result(run_id)
        return result or {"error": f"Run {run_id} not found", "run_id": run_id}

    def get_snapshot(self, run_id: str) -> dict:
        snap = self._store.get_snapshot(run_id)
        return snap or {"error": f"Snapshot for run {run_id} not found", "run_id": run_id}

    def get_included_symbols(self, run_id: str) -> List[str]:
        result = self.get_run(run_id)
        symbols = result.get("included_symbols", "[]")
        if isinstance(symbols, list):
            return symbols
        try:
            return json.loads(symbols)
        except Exception:
            return []

    def get_excluded_symbols(self, run_id: str) -> List[str]:
        result = self.get_run(run_id)
        symbols = result.get("excluded_symbols", "[]")
        if isinstance(symbols, list):
            return symbols
        try:
            return json.loads(symbols)
        except Exception:
            return []

    def get_exclusion_reasons(self, run_id: str) -> dict:
        result = self.get_run(run_id)
        reasons = result.get("exclusion_reasons", "{}")
        if isinstance(reasons, dict):
            return reasons
        try:
            return json.loads(reasons)
        except Exception:
            return {}

    def get_reproducibility_hash(self, run_id: str) -> str:
        stored = self._store.get_hash(run_id)
        if stored:
            return stored
        result = self.get_run(run_id)
        return result.get("reproducibility_hash", "") or ""

    def verify_run(self, run_id: str) -> bool:
        from gate_enforcement.reproducibility import RunReproducibilityHasher
        hasher = RunReproducibilityHasher()
        return hasher.verify_run_hash(run_id, output_dir=self._output_dir)

    def list_overridden_runs(self) -> List[dict]:
        results = self._store.list_results()
        return [r for r in results if str(r.get("override_used", "")).lower() in ("true", "1")]

    def compare_runs(self, run_a: str, run_b: str) -> dict:
        a = self.get_run(run_a)
        b = self.get_run(run_b)

        def _get_list(d, key):
            val = d.get(key, "[]")
            if isinstance(val, list):
                return set(val)
            try:
                return set(json.loads(val))
            except Exception:
                return set()

        included_a = _get_list(a, "included_symbols")
        included_b = _get_list(b, "included_symbols")

        return {
            "run_a": run_a,
            "run_b": run_b,
            "hash_a": a.get("reproducibility_hash", ""),
            "hash_b": b.get("reproducibility_hash", ""),
            "hashes_match": a.get("reproducibility_hash") == b.get("reproducibility_hash"),
            "status_a": a.get("status", ""),
            "status_b": b.get("status", ""),
            "included_a_only": sorted(included_a - included_b),
            "included_b_only": sorted(included_b - included_a),
            "included_both": sorted(included_a & included_b),
        }

    def list_non_qualified_runs(self) -> List[dict]:
        results = self._store.list_results()
        return [
            r for r in results
            if r.get("status") in ("DEMO_ONLY", "OBSERVATIONAL_ONLY", "BLOCKED", "FAILED")
               or str(r.get("applied_level", "")).upper() in ("DEMO", "OFF")
        ]

    def audit_summary(self) -> dict:
        results = self._store.list_results()
        from collections import Counter
        statuses = Counter(r.get("status", "UNKNOWN") for r in results)
        overridden = len([r for r in results if str(r.get("override_used", "")).lower() in ("true", "1")])
        return {
            "total_runs": len(results),
            "statuses": dict(statuses),
            "overridden_runs": overridden,
            "research_only": True,
            "no_real_orders": True,
        }
