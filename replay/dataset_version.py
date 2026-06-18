"""
replay/dataset_version.py — ReplayDatasetVersionManager v1.2.8

Manages dataset versions. Version scheme: MAJOR.MINOR.PATCH.
- patch: metadata / safe correction
- minor: new symbols / timeframes / fields
- major: schema incompatible change

Frozen versions are immutable and cannot be modified in place.
Modifying a frozen version requires creating a new version.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from replay.dataset_registry_schema import (
    ReplayDatasetVersionRecord, DatasetQualification,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _bump_version(version: str, bump: str) -> str:
    """Bump a MAJOR.MINOR.PATCH version string."""
    try:
        parts = [int(x) for x in version.split(".")]
        while len(parts) < 3:
            parts.append(0)
        major, minor, patch = parts[0], parts[1], parts[2]
        if bump == "major":
            return f"{major + 1}.0.0"
        elif bump == "minor":
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
    except Exception:
        return "1.0.0"


class ReplayDatasetVersionManager:
    """
    Manages dataset version records.

    Rules:
    - Initial version: 1.0.0
    - patch: metadata / safe correction
    - minor: new symbols / timeframes / fields
    - major: schema incompatible change
    - Frozen versions cannot be modified in place
    - Modifying a frozen version requires a new version
    - No auto-upgrade; version bump requires explicit reason

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self):
        self._records: Dict[str, List[ReplayDatasetVersionRecord]] = {}

    def create_initial_version(
        self,
        dataset_id: str,
        fingerprint: str = "",
        manifest_hash: str = "",
        qualification: str = DatasetQualification.MOCK_DEMO_ONLY.value,
    ) -> ReplayDatasetVersionRecord:
        """Create the initial 1.0.0 version record."""
        rec = ReplayDatasetVersionRecord(
            dataset_id=dataset_id,
            version="1.0.0",
            version_reason="initial",
            created_at=_now_utc(),
            fingerprint=fingerprint,
            manifest_hash=manifest_hash,
            qualification=qualification,
        )
        self._records.setdefault(dataset_id, []).append(rec)
        return rec

    def create_next_version(
        self,
        dataset_id: str,
        current_version: str,
        reason: str,
        change_type: str = "patch",
        fingerprint: str = "",
        manifest_hash: str = "",
        qualification: str = DatasetQualification.MOCK_DEMO_ONLY.value,
    ) -> ReplayDatasetVersionRecord:
        """Create the next version. change_type: patch / minor / major."""
        existing = self.list_versions(dataset_id)
        current = next((r for r in existing if r.version == current_version), None)
        if current and current.frozen:
            new_version = _bump_version(current_version, change_type)
        else:
            new_version = _bump_version(current_version, change_type)
        rec = ReplayDatasetVersionRecord(
            dataset_id=dataset_id,
            version=new_version,
            parent_version=current_version,
            version_reason=reason,
            created_at=_now_utc(),
            fingerprint=fingerprint,
            manifest_hash=manifest_hash,
            qualification=qualification,
        )
        self._records.setdefault(dataset_id, []).append(rec)
        return rec

    def list_versions(self, dataset_id: str) -> List[ReplayDatasetVersionRecord]:
        return self._records.get(dataset_id, [])

    def get_version(self, dataset_id: str, version: str) -> Optional[ReplayDatasetVersionRecord]:
        for r in self.list_versions(dataset_id):
            if r.version == version:
                return r
        return None

    def compare_versions(self, dataset_id: str, v1: str, v2: str) -> Dict[str, Any]:
        r1 = self.get_version(dataset_id, v1)
        r2 = self.get_version(dataset_id, v2)
        return {
            "v1": v1, "v2": v2,
            "v1_fingerprint": r1.fingerprint if r1 else "NOT_FOUND",
            "v2_fingerprint": r2.fingerprint if r2 else "NOT_FOUND",
            "fingerprint_match": (r1.fingerprint == r2.fingerprint) if (r1 and r2) else False,
            "v1_frozen": r1.frozen if r1 else None,
            "v2_frozen": r2.frozen if r2 else None,
        }

    def freeze_version(self, dataset_id: str, version: str) -> Optional[ReplayDatasetVersionRecord]:
        """Mark a version as frozen and immutable."""
        rec = self.get_version(dataset_id, version)
        if rec:
            rec.frozen    = True
            rec.immutable = True
            import datetime as _dt
            rec.warnings.append(f"frozen_at={_dt.datetime.now(_dt.timezone.utc).isoformat()}")
        return rec

    def archive_version(self, dataset_id: str, version: str) -> None:
        rec = self.get_version(dataset_id, version)
        if rec:
            rec.warnings.append("ARCHIVED")

    def restore_version(self, dataset_id: str, version: str) -> None:
        rec = self.get_version(dataset_id, version)
        if rec:
            rec.warnings = [w for w in rec.warnings if w != "ARCHIVED"]

    def verify_immutable(self, dataset_id: str, version: str, current_fingerprint: str) -> bool:
        """Return True if frozen version fingerprint still matches."""
        rec = self.get_version(dataset_id, version)
        if not rec:
            return False
        if not rec.frozen:
            return True  # not frozen, no constraint
        return rec.fingerprint == current_fingerprint

    def summary(self, dataset_id: str) -> str:
        versions = self.list_versions(dataset_id)
        if not versions:
            return f"Dataset {dataset_id}: no versions registered."
        lines = [f"Dataset {dataset_id}: {len(versions)} version(s)"]
        for r in versions:
            frozen_marker = " [FROZEN]" if r.frozen else ""
            lines.append(f"  v{r.version}{frozen_marker} | {r.version_reason} | {r.created_at[:10]}")
        return "\n".join(lines)
