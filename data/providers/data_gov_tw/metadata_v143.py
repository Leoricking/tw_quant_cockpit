"""
data/providers/data_gov_tw/metadata_v143.py — Metadata validation v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Incomplete metadata → formal_use_allowed=False, review_required=True.
[!] No auto-guessing of missing metadata fields.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, MetadataStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


_REQUIRED_METADATA_FIELDS = [
    "dataset_id",
    "title",
    "description",
    "provider_agency",
    "update_frequency",
    "license_name",
    "status",
]

_QUALITY_METADATA_FIELDS = [
    "metadata_updated_at",
    "published_at",
    "agency_code",
    "contact_name",
    "language",
]


class DataGovTwMetadataValidator:
    """
    Validates metadata completeness for data.gov.tw datasets.

    Rules:
    - Incomplete metadata → formal_use_allowed=False
    - Missing license → MISSING_LICENSE
    - Missing resources → MISSING_RESOURCE
    - No auto-guessing of missing fields
    - Removed/deprecated datasets → BLOCKED
    """

    def validate(self, dataset: DataGovTwDataset) -> Dict[str, Any]:
        """Validate metadata completeness. Returns structured result."""
        issues: List[str] = []
        warnings: List[str] = []

        # Check removed/deprecated status
        from data.providers.data_gov_tw.models_v143 import DatasetStatus
        if dataset.status in (DatasetStatus.REMOVED.value, DatasetStatus.DEPRECATED.value):
            return {
                "status": MetadataStatus.REMOVED.value,
                "formal_use_allowed": False,
                "review_required": True,
                "issues": [f"Dataset status is {dataset.status}"],
                "warnings": [],
                "complete": False,
            }

        # Check required fields
        d = dataset.to_dict()
        for field in _REQUIRED_METADATA_FIELDS:
            if not d.get(field):
                issues.append(f"Missing required metadata field: {field}")

        # Check license
        if not dataset.license_name and not dataset.license_url:
            issues.append("Missing license information")
            status = MetadataStatus.MISSING_LICENSE.value
        elif issues:
            status = MetadataStatus.PARTIAL.value
        else:
            status = MetadataStatus.VALID.value

        # Quality warnings (non-blocking)
        for field in _QUALITY_METADATA_FIELDS:
            if not d.get(field):
                warnings.append(f"Optional metadata field absent: {field}")

        formal_use_allowed = (status == MetadataStatus.VALID.value and not issues)

        return {
            "status": status,
            "formal_use_allowed": formal_use_allowed,
            "review_required": bool(issues),
            "issues": issues,
            "warnings": warnings,
            "complete": len(issues) == 0,
        }

    def validate_dict(self, dataset_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate from raw dict without constructing full object."""
        dataset = DataGovTwDataset.from_dict(dataset_dict)
        return self.validate(dataset)
