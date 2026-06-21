"""
data/integration/storage_migration_v148.py — Storage Migration Hardening v1.4.8.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Migrations must be additive, idempotent, non-destructive.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .models_v148 import MigrationRecord, MigrationStatus

logger = logging.getLogger(__name__)

MIGRATION_REGISTRY: List[MigrationRecord] = [
    MigrationRecord(
        migration_id="m001_provider_foundation",
        from_version="1.0.0", to_version="1.4.0",
        additive=True, destructive=False, reversible=True, idempotent=True,
        status=MigrationStatus.APPLIED,
    ),
    MigrationRecord(
        migration_id="m002_source_governance",
        from_version="1.4.0", to_version="1.4.5",
        additive=True, destructive=False, reversible=True, idempotent=True,
        status=MigrationStatus.APPLIED,
    ),
    MigrationRecord(
        migration_id="m003_provider_quality",
        from_version="1.4.5", to_version="1.4.6",
        additive=True, destructive=False, reversible=True, idempotent=True,
        status=MigrationStatus.APPLIED,
    ),
    MigrationRecord(
        migration_id="m004_forum_intelligence",
        from_version="1.4.6", to_version="1.4.7",
        additive=True, destructive=False, reversible=True, idempotent=True,
        status=MigrationStatus.APPLIED,
    ),
    MigrationRecord(
        migration_id="m005_integration_hardening",
        from_version="1.4.7", to_version="1.4.8",
        additive=True, destructive=False, reversible=True, idempotent=True,
        status=MigrationStatus.APPLIED,
    ),
]


class StorageMigrationHardeningService:
    """Validates and manages storage migrations."""

    VERSION = "1.4.8"
    AUTO_DESTRUCTIVE_ALLOWED = False
    AUTO_SCHEMA_REBUILD_ALLOWED = False

    def validate_all(self) -> List[Dict[str, Any]]:
        results = []
        seen_ids: set = set()
        for m in MIGRATION_REGISTRY:
            result = self._validate_migration(m, seen_ids)
            seen_ids.add(m.migration_id)
            results.append(result)
        return results

    def _validate_migration(self, m: MigrationRecord, seen_ids: set) -> Dict[str, Any]:
        errors = []
        if m.migration_id in seen_ids:
            errors.append(f"Duplicate migration_id: {m.migration_id}")
        if m.destructive:
            errors.append(f"Destructive migration not allowed: {m.migration_id}")
        if not m.idempotent:
            errors.append(f"Non-idempotent migration: {m.migration_id}")
        if m.status == MigrationStatus.PARTIAL:
            errors.append(f"Partial migration detected: {m.migration_id}")
        status = "PASS" if not errors else "FAIL"
        return {
            "migration_id": m.migration_id,
            "from_version": m.from_version,
            "to_version":   m.to_version,
            "additive":     m.additive,
            "destructive":  m.destructive,
            "idempotent":   m.idempotent,
            "status":       status,
            "errors":       errors,
        }

    def check_old_data_readable(self, version_tag: str) -> bool:
        """Check that data from a previous version is still readable."""
        # Structural: additive-only migrations preserve old columns/tables
        for m in MIGRATION_REGISTRY:
            if m.from_version == version_tag or m.to_version == version_tag:
                return m.additive and not m.destructive
        return True  # no migration needed → data unchanged

    def get_summary(self) -> Dict[str, Any]:
        results = self.validate_all()
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        return {
            "version": self.VERSION,
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "all_valid": failed == 0,
            "migrations": results,
        }
