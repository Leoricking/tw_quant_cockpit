"""
paper_trading/operational_integration/determinism_checker_v168.py
Determinism Checker for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from .models_v168 import DeterminismResult
from .enums_v168 import DeterminismStatus

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_EXCLUDE_FIELDS = {
    "created_at", "updated_at", "run_timestamp", "timestamp",
    "started_at", "completed_at", "processed_at", "generated_at",
}


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _strip_timestamps(obj: Any) -> Any:
    """Recursively strip timestamp fields from dicts and lists."""
    if isinstance(obj, dict):
        return {k: _strip_timestamps(v) for k, v in obj.items() if k not in _EXCLUDE_FIELDS}
    if isinstance(obj, list):
        return [_strip_timestamps(item) for item in obj]
    return obj


def _stable_hash(obj: Any) -> str:
    serialized = json.dumps(obj, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()


class DeterminismChecker:
    """Validates determinism of integration outputs. Research only."""

    def check_run(self, run1: Dict[str, Any], run2: Dict[str, Any]) -> DeterminismResult:
        """Check if two run results are deterministic."""
        run_id = run1.get("run_id", "unknown")
        component_id = run1.get("component_id", "unknown")

        clean1 = _strip_timestamps(run1)
        clean2 = _strip_timestamps(run2)

        h1 = _stable_hash(clean1)
        h2 = _stable_hash(clean2)
        hash_stable = h1 == h2

        stages1 = [s.get("stage", "") for s in run1.get("stages", [])]
        stages2 = [s.get("stage", "") for s in run2.get("stages", [])]
        order_stable = stages1 == stages2

        score1 = run1.get("scorecard_total", 0)
        score2 = run2.get("scorecard_total", 0)
        score_stable = self.check_score_stability(score1, score2)

        if hash_stable and order_stable and score_stable:
            status = DeterminismStatus.DETERMINISTIC
        elif hash_stable or (order_stable and score_stable):
            status = DeterminismStatus.PARTIAL
        else:
            status = DeterminismStatus.NON_DETERMINISTIC

        return DeterminismResult(
            run_id=run_id,
            component_id=component_id,
            status=status,
            hash_stable=hash_stable,
            order_stable=order_stable,
            score_stable=score_stable,
        )

    def check_hash_stability(self, h1: str, h2: str) -> bool:
        """Return True if hashes are equal."""
        return h1 == h2

    def check_order_stability(self, list1: List[Any], list2: List[Any]) -> bool:
        """Return True if lists have same order."""
        return list(list1) == list(list2)

    def check_score_stability(self, s1, s2) -> bool:
        """Return True if scores differ by less than 1e-9."""
        try:
            return abs(float(s1) - float(s2)) < 1e-9
        except (TypeError, ValueError):
            return s1 == s2

    def check_snapshot_stability(self, snap1: Any, snap2: Any) -> bool:
        """Return True if two snapshots have the same component hash."""
        if snap1 is None or snap2 is None:
            return snap1 == snap2
        c1 = getattr(snap1, "components", snap1)
        c2 = getattr(snap2, "components", snap2)
        return _stable_hash(c1) == _stable_hash(c2)

    def check_report_stability(self, r1: Dict[str, Any], r2: Dict[str, Any]) -> bool:
        """Return True if two report dicts are the same (excluding timestamps)."""
        c1 = {k: v for k, v in r1.items() if k not in _EXCLUDE_FIELDS}
        c2 = {k: v for k, v in r2.items() if k not in _EXCLUDE_FIELDS}
        return _stable_hash(c1) == _stable_hash(c2)

    def summarize(self, results: List[DeterminismResult]) -> Dict[str, Any]:
        """Return summary of determinism check results."""
        total = len(results)
        det = sum(1 for r in results if r.status == DeterminismStatus.DETERMINISTIC)
        non_det = sum(1 for r in results if r.status == DeterminismStatus.NON_DETERMINISTIC)
        partial = sum(1 for r in results if r.status == DeterminismStatus.PARTIAL)
        return {
            "total": total,
            "deterministic": det,
            "non_deterministic": non_det,
            "partial": partial,
            "all_deterministic": non_det == 0 and partial == 0 and total > 0,
            "paper_only": True,
        }
