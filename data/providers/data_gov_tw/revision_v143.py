"""
data/providers/data_gov_tw/revision_v143.py — Revision tracking service v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Detects: metadata change, URL change, format change, schema change,
    update frequency change, license change, agency change, removed, restored,
    content hash change, historical value revision.
[!] Never silently overwrites old revisions.
[!] Never back-fills old as_of timestamps.
[!] Dataset revision and record revision are separate.
"""
from __future__ import annotations

import datetime
import hashlib
import uuid
from typing import Any, Dict, List, Optional

from data.providers.data_gov_tw.models_v143 import DataGovTwDatasetRevision

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _hash_dict(d: Dict[str, Any]) -> str:
    import json
    payload = json.dumps(d, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


class DataGovTwRevisionService:
    """
    Detects and tracks revisions in data.gov.tw datasets and resources.

    Rules:
    - No silent overwrite of old revisions
    - Old revision hash is preserved (immutable)
    - No back-fill of past as_of timestamps
    - Dataset revision and record revision are separate
    """

    def detect_metadata_revision(
        self,
        old_dataset: Dict[str, Any],
        new_dataset: Dict[str, Any],
    ) -> Optional[DataGovTwDatasetRevision]:
        """Detect metadata-level revision between two dataset snapshots."""
        changed_fields: List[str] = []
        flags: Dict[str, bool] = {
            "metadata_changed": False,
            "schema_changed": False,
            "resource_changed": False,
            "update_frequency_changed": False,
            "license_changed": False,
        }

        _TRACKED_FIELDS = [
            "title", "description", "provider_agency", "agency_code",
            "update_frequency", "license_name", "license_url",
            "metadata_updated_at", "status", "download_url",
        ]

        for field in _TRACKED_FIELDS:
            old_val = old_dataset.get(field)
            new_val = new_dataset.get(field)
            if old_val != new_val:
                changed_fields.append(field)
                flags["metadata_changed"] = True
                if field == "update_frequency":
                    flags["update_frequency_changed"] = True
                if field in ("license_name", "license_url"):
                    flags["license_changed"] = True

        if not changed_fields:
            return None

        old_hash = _hash_dict({f: old_dataset.get(f) for f in _TRACKED_FIELDS})
        new_hash = _hash_dict({f: new_dataset.get(f) for f in _TRACKED_FIELDS})

        severity = "WARNING" if flags.get("license_changed") or flags.get("update_frequency_changed") else "INFO"

        return DataGovTwDatasetRevision(
            revision_id=str(uuid.uuid4()),
            dataset_id=new_dataset.get("dataset_id", ""),
            detected_at=_now_iso(),
            old_content_hash=old_hash,
            new_content_hash=new_hash,
            metadata_changed=flags["metadata_changed"],
            schema_changed=flags["schema_changed"],
            update_frequency_changed=flags["update_frequency_changed"],
            license_changed=flags["license_changed"],
            changed_fields=changed_fields,
            severity=severity,
            review_required=flags.get("license_changed", False),
            provenance={"source": "metadata_diff"},
        )

    def detect_content_revision(
        self,
        dataset_id: str,
        resource_id: str,
        old_hash: str,
        new_hash: str,
    ) -> Optional[DataGovTwDatasetRevision]:
        """Detect content-level revision (data values changed)."""
        if old_hash == new_hash:
            return None
        return DataGovTwDatasetRevision(
            revision_id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            resource_id=resource_id,
            detected_at=_now_iso(),
            old_content_hash=old_hash,
            new_content_hash=new_hash,
            resource_changed=True,
            changed_fields=["content_hash"],
            severity="INFO",
            review_required=False,
            provenance={"source": "content_diff"},
        )

    def detect_schema_revision(
        self,
        dataset_id: str,
        old_schema_hash: str,
        new_schema_hash: str,
    ) -> Optional[DataGovTwDatasetRevision]:
        """Detect schema contract revision."""
        if old_schema_hash == new_schema_hash:
            return None
        return DataGovTwDatasetRevision(
            revision_id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            detected_at=_now_iso(),
            old_content_hash=old_schema_hash,
            new_content_hash=new_schema_hash,
            schema_changed=True,
            changed_fields=["schema_contract"],
            severity="WARNING",
            review_required=True,
            provenance={"source": "schema_diff"},
        )
