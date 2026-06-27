"""
paper_trading/failure_validation/store_v165.py — Research-only local append-only store v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] Local in-memory only. No production DB. No external write. Append-only.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

PRODUCTION_DB_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True
LOCAL_ONLY = True
APPEND_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class FailureInjectionStore:
    """
    Local in-memory append-only store for failure injection records.
    Research/paper only. No production DB writes.
    """

    def __init__(self) -> None:
        assert not PRODUCTION_DB_ENABLED, "Production DB must never be enabled"
        self._injection_results: List[Dict[str, Any]] = []
        self._recovery_validations: List[Dict[str, Any]] = []
        self._scorecards: List[Dict[str, Any]] = []
        self._baseline_snapshots: List[Dict[str, Any]] = []

    def append_injection_result(self, record: Dict[str, Any]) -> None:
        record["_stored_at"] = _utcnow().isoformat()
        self._injection_results.append(record)

    def append_recovery_validation(self, record: Dict[str, Any]) -> None:
        record["_stored_at"] = _utcnow().isoformat()
        self._recovery_validations.append(record)

    def append_scorecard(self, record: Dict[str, Any]) -> None:
        record["_stored_at"] = _utcnow().isoformat()
        self._scorecards.append(record)

    def append_baseline_snapshot(self, record: Dict[str, Any]) -> None:
        record["_stored_at"] = _utcnow().isoformat()
        self._baseline_snapshots.append(record)

    def query_injection_results(self, limit: int = 100) -> List[Dict[str, Any]]:
        return list(self._injection_results[-limit:])

    def query_recovery_validations(self, limit: int = 100) -> List[Dict[str, Any]]:
        return list(self._recovery_validations[-limit:])

    def query_scorecards(self, limit: int = 100) -> List[Dict[str, Any]]:
        return list(self._scorecards[-limit:])

    def injection_result_count(self) -> int:
        return len(self._injection_results)

    def recovery_validation_count(self) -> int:
        return len(self._recovery_validations)

    def scorecard_count(self) -> int:
        return len(self._scorecards)

    def summary(self) -> Dict[str, Any]:
        return {
            "production_db_enabled": PRODUCTION_DB_ENABLED,
            "paper_only": PAPER_ONLY,
            "research_only": RESEARCH_ONLY,
            "local_only": LOCAL_ONLY,
            "append_only": APPEND_ONLY,
            "injection_results": self.injection_result_count(),
            "recovery_validations": self.recovery_validation_count(),
            "scorecards": self.scorecard_count(),
            "baseline_snapshots": len(self._baseline_snapshots),
        }
