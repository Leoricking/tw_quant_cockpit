"""
data_coverage/data_coverage_scanner.py — DataCoverageScanner for TW Quant Cockpit v0.6.2.

Scans the filesystem for actual files matching registry patterns and classifies
each item with a coverage status.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

from data_coverage.data_coverage_schema import (
    DataCoverageItem,
    STATUS_READY, STATUS_MISSING_REQUIRED, STATUS_MISSING_OPTIONAL,
    STATUS_ENV_LIMITED, STATUS_NOT_GENERATED, STATUS_FAILED, STATUS_UNKNOWN,
)
from data_coverage.data_coverage_registry import DataCoverageRegistry

logger = logging.getLogger(__name__)


class DataCoverageScanner:
    """Scans filesystem for actual files matching registry patterns.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        registry: Optional[DataCoverageRegistry] = None,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/data_coverage",
    ) -> None:
        self.registry    = registry or DataCoverageRegistry()
        self.project_root = os.path.abspath(project_root)
        self.output_dir  = output_dir
        self._finmind_token_present: Optional[bool] = None

    def _check_finmind_token(self) -> bool:
        """Check if FINMIND_TOKEN is present in environment. Never logs the value."""
        if self._finmind_token_present is None:
            self._finmind_token_present = bool(
                os.environ.get("FINMIND_TOKEN", "").strip()
            )
        return self._finmind_token_present

    def scan(self, mode: str = "real") -> List[DataCoverageItem]:
        """Scan all registry items and return DataCoverageItem list."""
        items: List[DataCoverageItem] = []
        for item_def in self.registry.list_items():
            try:
                item = self.scan_item(item_def)
                items.append(item)
            except Exception as exc:
                logger.warning("Scanner error for %s: %s", item_def.get("item_id", "?"), exc)
                items.append(DataCoverageItem(
                    item_id=item_def.get("item_id", "unknown"),
                    domain=item_def.get("domain", "unknown"),
                    dataset_name=item_def.get("dataset_name", "unknown"),
                    status=STATUS_FAILED,
                    required=item_def.get("required", True),
                    missing_reason=str(exc),
                    suggested_command=item_def.get("suggested_command", ""),
                ))
        return items

    def scan_item(self, item_def: dict) -> DataCoverageItem:
        """Scan a single registry item and return a DataCoverageItem."""
        item_id          = item_def.get("item_id", "unknown")
        domain           = item_def.get("domain", "unknown")
        dataset_name     = item_def.get("dataset_name", "unknown")
        required         = item_def.get("required", True)
        env_limited      = item_def.get("environment_limited", False)
        not_generated    = item_def.get("not_generated", False)
        patterns         = item_def.get("expected_patterns", [])
        suggested_cmd    = item_def.get("suggested_command", "")
        source_module    = item_def.get("owner_module", "")

        matches = self.match_patterns(patterns)
        status  = self.classify_status(item_def, matches)

        actual_path = matches[-1] if matches else ""
        last_updated = ""
        if actual_path and os.path.exists(actual_path):
            try:
                mtime = os.path.getmtime(actual_path)
                last_updated = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass

        missing_reason = ""
        if status == STATUS_ENV_LIMITED:
            missing_reason = "Environment token not set (FINMIND_TOKEN)"
        elif status == STATUS_NOT_GENERATED:
            missing_reason = "Not yet generated (optional / on-demand)"
        elif status == STATUS_MISSING_REQUIRED:
            missing_reason = f"Required dataset not found. Run: {suggested_cmd}"
        elif status == STATUS_MISSING_OPTIONAL:
            missing_reason = "Optional dataset not found"

        return DataCoverageItem(
            item_id=item_id,
            domain=domain,
            dataset_name=dataset_name,
            source_module=source_module,
            actual_path=actual_path,
            status=status,
            required=required,
            environment_limited=env_limited,
            not_generated=not_generated,
            last_updated=last_updated,
            missing_reason=missing_reason,
            suggested_command=suggested_cmd,
        )

    def match_patterns(self, patterns: List[str]) -> List[str]:
        """Glob-match each pattern relative to project_root. Returns list of paths."""
        matched: List[str] = []
        for pattern in patterns:
            full_pattern = os.path.join(self.project_root, pattern)
            try:
                hits = glob.glob(full_pattern, recursive=True)
                # Filter to files with size > 0
                for h in sorted(hits):
                    try:
                        if os.path.isfile(h) and os.path.getsize(h) > 0:
                            matched.append(h)
                    except Exception:
                        pass
            except Exception as exc:
                logger.debug("Pattern match error '%s': %s", pattern, exc)
        return matched

    def classify_status(self, item_def: dict, matches: List[str]) -> str:
        """Apply classification rules and return a status string."""
        try:
            env_limited   = item_def.get("environment_limited", False)
            not_generated = item_def.get("not_generated", False)
            required      = item_def.get("required", True)

            # Special case: FinMind token
            if env_limited and item_def.get("item_id") == "finmind_provider_token":
                if self._check_finmind_token():
                    return STATUS_READY
                return STATUS_ENV_LIMITED

            # General env-limited: check for token presence only as a proxy
            if env_limited and not matches:
                return STATUS_ENV_LIMITED

            # Not-generated items: always NOT_GENERATED regardless of files
            if not_generated:
                return STATUS_NOT_GENERATED

            # Files found with size > 0
            if matches:
                return STATUS_READY

            # No files found
            if not required:
                return STATUS_MISSING_OPTIONAL

            return STATUS_MISSING_REQUIRED

        except Exception as exc:
            logger.warning("classify_status error: %s", exc)
            return STATUS_FAILED
