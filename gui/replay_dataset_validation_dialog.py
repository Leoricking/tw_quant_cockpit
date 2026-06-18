"""
gui/replay_dataset_validation_dialog.py — Dataset Validation dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetValidationDialog:
    """
    Runs and displays dataset validation results (PASS/WARN/FAIL/BLOCKED).

    Checks: manifest_schema, required_fields, file_presence, row_count,
    symbol/timeframe coverage, pit_qualification, mock_contamination,
    path_safety, frozen_immutability, version_consistency.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    CHECK_COLUMNS = ["check", "status", "detail"]

    def __init__(self, dataset_id: Optional[str] = None) -> None:
        self._dataset_id = dataset_id

    def run_validation(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_registry import ReplayDatasetRegistry
            from replay.dataset_validator import ReplayDatasetValidator
            reg = ReplayDatasetRegistry()
            d   = reg.get_dataset(dataset_id)
            if d is None:
                return {"error": f"Dataset {dataset_id!r} not found"}
            results = ReplayDatasetValidator().validate(d)
            passed  = sum(1 for v in results.values() if v[0] == "PASS")
            failed  = sum(1 for v in results.values() if v[0] == "FAIL")
            warned  = sum(1 for v in results.values() if v[0] == "WARN")
            blocked = sum(1 for v in results.values() if v[0] == "BLOCKED")
            return {
                "dataset_id": dataset_id,
                "results":    results,
                "passed":     passed,
                "failed":     failed,
                "warned":     warned,
                "blocked":    blocked,
                "ok":         failed == 0 and blocked == 0,
            }
        except Exception as exc:
            logger.warning("run_validation failed: %s", exc)
            return {"error": str(exc), "dataset_id": dataset_id}

    def run_integrity(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_registry import ReplayDatasetRegistry
            from replay.dataset_integrity import ReplayDatasetIntegrityChecker
            reg = ReplayDatasetRegistry()
            d   = reg.get_dataset(dataset_id)
            if d is None:
                return {"error": f"Dataset {dataset_id!r} not found"}
            return ReplayDatasetIntegrityChecker().check(d)
        except Exception as exc:
            logger.warning("run_integrity failed: %s", exc)
            return {"error": str(exc), "dataset_id": dataset_id}
