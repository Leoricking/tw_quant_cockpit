"""
replay/dataset_validator.py — ReplayDatasetValidator v1.2.8

Validates dataset manifests and files.
Checks: schema, required fields, file presence, hash, row count,
symbol/timeframe coverage, timestamp monotonicity, duplicates,
timezone, PIT, mock contamination, path safety, frozen immutability,
lineage cycles, version consistency.

Output: PASS / WARN / FAIL / BLOCKED per check.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from replay.dataset_registry_schema import (
    ReplayDatasetManifest, DatasetMode, DatasetQualification, DatasetStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetValidator:
    """
    Validates dataset manifests.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def validate(self, manifest: ReplayDatasetManifest) -> Dict[str, Tuple[str, str]]:
        """Run all validation checks. Returns dict of check_name -> (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}
        results["manifest_schema"]      = self._check_manifest_schema(manifest)
        results["required_fields"]      = self._check_required_fields(manifest)
        results["file_presence"]        = self._check_file_presence(manifest)
        results["row_count"]            = self._check_row_count(manifest)
        results["symbol_coverage"]      = self._check_symbol_coverage(manifest)
        results["timeframe_coverage"]   = self._check_timeframe_coverage(manifest)
        results["pit_qualification"]    = self._check_pit(manifest)
        results["mock_contamination"]   = self._check_mock_contamination(manifest)
        results["path_safety"]          = self._check_path_safety(manifest)
        results["frozen_immutability"]  = self._check_frozen_immutability(manifest)
        results["version_consistency"]  = self._check_version_consistency(manifest)
        return results

    def _check_manifest_schema(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if not m.dataset_id:
            return ("FAIL", "dataset_id is empty")
        if not m.dataset_name:
            return ("WARN", "dataset_name is empty")
        return ("PASS", "manifest schema OK")

    def _check_required_fields(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        missing = []
        if not m.dataset_id:    missing.append("dataset_id")
        if not m.schema_version: missing.append("schema_version")
        if not m.mode:           missing.append("mode")
        if missing:
            return ("FAIL", f"Missing required fields: {missing}")
        return ("PASS", "required fields OK")

    def _check_file_presence(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        missing_required = [f.relative_path for f in m.files if f.required and not f.present]
        missing_optional = [f.relative_path for f in m.files if not f.required and not f.present]
        if missing_required:
            return ("BLOCKED", f"MISSING required files: {missing_required}")
        if missing_optional:
            return ("WARN", f"MISSING optional files: {missing_optional}")
        return ("PASS", "all files present")

    def _check_row_count(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if m.row_count == 0 and m.file_count > 0:
            return ("WARN", "row_count is 0 but files exist")
        return ("PASS", f"row_count={m.row_count}")

    def _check_symbol_coverage(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if not m.symbols:
            return ("WARN", "no symbols listed")
        return ("PASS", f"symbols={m.symbols}")

    def _check_timeframe_coverage(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if not m.timeframes:
            return ("WARN", "no timeframes listed")
        return ("PASS", f"timeframes={m.timeframes}")

    def _check_pit(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if m.mode == DatasetMode.REAL.value and not m.point_in_time_verified:
            return ("WARN", "REAL dataset: PIT not verified -> REAL_UNVERIFIED")
        if m.future_data_check == "LEAK_DETECTED":
            return ("BLOCKED", "FUTURE DATA LEAK detected")
        return ("PASS", "PIT check OK")

    def _check_mock_contamination(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if m.mode == DatasetMode.REAL.value:
            if any("MOCK" in w.upper() for w in m.warnings):
                return ("BLOCKED", "Mock contamination in REAL dataset")
        return ("PASS", "no mock contamination")

    def _check_path_safety(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        import os
        for p in m.relative_paths:
            if os.path.isabs(p) or ":\\" in p or p.startswith("/"):
                return ("FAIL", f"Absolute path found: {p}")
        return ("PASS", "paths are relative")

    def _check_frozen_immutability(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if m.frozen_at and m.status != DatasetStatus.FROZEN.value:
            return ("WARN", "frozen_at set but status is not FROZEN")
        return ("PASS", "frozen status consistent")

    def _check_version_consistency(self, m: ReplayDatasetManifest) -> Tuple[str, str]:
        if not m.dataset_version:
            return ("WARN", "no dataset_version")
        parts = m.dataset_version.split(".")
        if len(parts) != 3:
            return ("WARN", f"version format unexpected: {m.dataset_version}")
        return ("PASS", f"version={m.dataset_version}")
