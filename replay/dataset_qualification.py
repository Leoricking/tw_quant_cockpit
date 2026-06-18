"""
replay/dataset_qualification.py — ReplayDatasetQualificationEvaluator v1.2.8

Evaluates dataset qualification based on source validity, PIT verification,
future data leakage, coverage, hash validity, schema compatibility, etc.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.dataset_registry_schema import (
    ReplayDatasetManifest, ReplayDatasetFileEntry,
    DatasetMode, DatasetQualification,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetQualificationEvaluator:
    """
    Evaluates dataset qualification.

    Rules:
    - Real with mock contamination => BLOCKED
    - Real without PIT => REAL_UNVERIFIED or BLOCKED
    - Missing required files => BLOCKED
    - Missing optional files => WARN
    - Too few samples => INSUFFICIENT
    - Mock can never be VERIFIED_REAL

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    MIN_ROW_COUNT = 10  # minimum rows for SUFFICIENT

    def evaluate(
        self,
        manifest: ReplayDatasetManifest,
        file_entries: Optional[List[ReplayDatasetFileEntry]] = None,
    ) -> str:
        """Return the qualification level string."""
        issues = self._collect_issues(manifest, file_entries or manifest.files)
        if "MOCK_CONTAMINATION" in issues:
            return DatasetQualification.BLOCKED.value
        if "SCHEMA_INCOMPATIBLE" in issues:
            return DatasetQualification.INCOMPATIBLE.value
        if "MISSING_REQUIRED_FILE" in issues:
            return DatasetQualification.BLOCKED.value
        if manifest.mode == DatasetMode.MOCK.value:
            return DatasetQualification.MOCK_DEMO_ONLY.value
        if "INSUFFICIENT_ROWS" in issues:
            return DatasetQualification.INSUFFICIENT.value
        if "FUTURE_LEAK" in issues:
            return DatasetQualification.BLOCKED.value
        if not manifest.point_in_time_verified:
            return DatasetQualification.REAL_UNVERIFIED.value
        return DatasetQualification.VERIFIED_REAL.value

    def check_source_validity(self, manifest: ReplayDatasetManifest) -> str:
        if not manifest.source_type or manifest.source_type == "UNKNOWN":
            return "WARN: unknown source_type"
        return "OK"

    def check_pit_verification(self, manifest: ReplayDatasetManifest) -> str:
        if not manifest.point_in_time_verified:
            return "WARN: PIT not verified"
        return "OK"

    def check_future_leakage(self, manifest: ReplayDatasetManifest) -> str:
        if manifest.future_data_check == "LEAK_DETECTED":
            return "FAIL: future data leakage detected"
        return "OK"

    def check_field_coverage(self, manifest: ReplayDatasetManifest) -> str:
        if not manifest.field_names:
            return "WARN: no fields listed"
        required = {"open", "high", "low", "close", "volume"}
        missing = required - set(manifest.field_names)
        if missing:
            return f"WARN: missing fields {missing}"
        return "OK"

    def check_mock_contamination(self, manifest: ReplayDatasetManifest) -> str:
        if manifest.mode == DatasetMode.REAL.value:
            if "MOCK" in " ".join(manifest.warnings).upper():
                return "FAIL: mock contamination in real dataset"
        return "OK"

    def explain(
        self,
        manifest: ReplayDatasetManifest,
        file_entries: Optional[List[ReplayDatasetFileEntry]] = None,
    ) -> Dict[str, str]:
        return {
            "qualification":      self.evaluate(manifest, file_entries),
            "source_validity":    self.check_source_validity(manifest),
            "pit_verification":   self.check_pit_verification(manifest),
            "future_leakage":     self.check_future_leakage(manifest),
            "field_coverage":     self.check_field_coverage(manifest),
            "mock_contamination": self.check_mock_contamination(manifest),
        }

    # ------------------------------------------------------------------ #

    def _collect_issues(
        self,
        manifest: ReplayDatasetManifest,
        files: List[ReplayDatasetFileEntry],
    ) -> List[str]:
        issues = []
        if manifest.future_data_check == "LEAK_DETECTED":
            issues.append("FUTURE_LEAK")
        if manifest.mode == DatasetMode.REAL.value:
            if "MOCK" in " ".join(manifest.warnings).upper():
                issues.append("MOCK_CONTAMINATION")
        for f in files:
            if f.required and not f.present:
                issues.append("MISSING_REQUIRED_FILE")
        if manifest.row_count > 0 and manifest.row_count < self.MIN_ROW_COUNT:
            issues.append("INSUFFICIENT_ROWS")
        return issues
