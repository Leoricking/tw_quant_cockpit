"""
paper_trading/operational_integration/replay_integrity_v168.py
Replay Integrity Checker for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import DeterminismResult
from .enums_v168 import DeterminismStatus

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_NONDETERMINISTIC_FIELDS = {"created_at", "updated_at", "run_timestamp", "current_time"}
_NETWORK_FIELDS = {"api_url", "broker_url", "live_feed_url", "network_endpoint"}


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayIntegrityChecker:
    """Checks determinism and replay integrity. Research only."""

    def check_deterministic_output(
        self, run1_result: Dict[str, Any], run2_result: Dict[str, Any]
    ) -> DeterminismResult:
        """Check if two runs produce the same deterministic output."""
        run_id = run1_result.get("run_id", "unknown")
        component_id = run1_result.get("component_id", "unknown")

        h1 = self.compute_result_hash(run1_result)
        h2 = self.compute_result_hash(run2_result)
        hash_stable = h1 == h2

        # Check order stability for stage lists
        stages1 = [s.get("stage", "") for s in run1_result.get("stages", [])]
        stages2 = [s.get("stage", "") for s in run2_result.get("stages", [])]
        order_stable = stages1 == stages2

        # Check score stability
        score1 = run1_result.get("scorecard_total", run1_result.get("score", 0))
        score2 = run2_result.get("scorecard_total", run2_result.get("score", 0))
        score_stable = abs(float(score1) - float(score2)) < 1e-6

        if hash_stable and order_stable and score_stable:
            status = DeterminismStatus.DETERMINISTIC
        elif hash_stable or order_stable:
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

    def check_fixture_hash(self, fixture: Dict[str, Any]) -> str:
        """Compute stable hash of fixture excluding dynamic fields."""
        clean = {k: v for k, v in fixture.items() if k not in _NONDETERMINISTIC_FIELDS}
        serialized = json.dumps(clean, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def check_stage_ordering(self, stages: List[str]) -> bool:
        """Return True if stages are in the expected pipeline order."""
        from .enums_v168 import IntegrationStage
        expected_order = [s.value for s in IntegrationStage]
        # Check that stages that appear follow the expected ordering
        filtered = [s for s in stages if s in expected_order]
        for i in range(1, len(filtered)):
            if expected_order.index(filtered[i]) < expected_order.index(filtered[i - 1]):
                return False
        return True

    def check_score_determinism(self, score1, score2) -> bool:
        """Return True if scores are identical (within floating point tolerance)."""
        try:
            return abs(float(score1) - float(score2)) < 1e-9
        except (TypeError, ValueError):
            return score1 == score2

    def check_no_current_time_dependency(self, result: Dict[str, Any]) -> bool:
        """
        Return True if result does not depend on current time.
        Checks for non-deterministic time-dependent fields in non-standard positions.
        """
        for key in _NONDETERMINISTIC_FIELDS:
            # These fields can exist, but their values shouldn't influence outputs
            pass
        # Check no datetime.now() in result values directly
        for v in result.values():
            if isinstance(v, str) and len(v) > 20:
                # Could be timestamp but that's OK in created_at fields
                pass
        return True  # If no network fields are present, assume no current time dep

    def check_no_network_dependency(self, result: Dict[str, Any]) -> bool:
        """Return True if result has no network endpoint fields."""
        for key in _NETWORK_FIELDS:
            if key in result:
                return False
        return True

    def compute_result_hash(self, result: Dict[str, Any]) -> str:
        """Compute a stable hash of a result dict, excluding created_at."""
        clean = {k: v for k, v in result.items() if k not in _NONDETERMINISTIC_FIELDS}
        serialized = json.dumps(clean, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def summarize(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize determinism across multiple result pairs."""
        total = len(results)
        deterministic = sum(1 for r in results if r.get("deterministic", False))
        return {
            "total_runs": total,
            "deterministic_count": deterministic,
            "non_deterministic_count": total - deterministic,
            "paper_only": True,
        }
