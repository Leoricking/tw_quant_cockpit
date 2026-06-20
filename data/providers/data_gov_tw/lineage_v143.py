"""
data/providers/data_gov_tw/lineage_v143.py — Source lineage tracking v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Every record must preserve platform, provider_agency, authoritative_level,
    original resource URL identifier, catalog dataset ID.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class DataGovTwLineageService:
    """
    Builds and validates source lineage records for data.gov.tw data.

    Every record must carry:
    - platform = "data.gov.tw"
    - provider_agency
    - authoritative_level
    - original_resource_url identifier (not necessarily the full URL for privacy)
    - catalog_dataset_id
    """

    def build_lineage(
        self,
        dataset_id: str,
        resource_id: str,
        provider_agency: str,
        authoritative_level: str,
        download_url_identifier: str,
        content_hash: Optional[str] = None,
        source_timestamp: Optional[str] = None,
        fetched_at: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Build a lineage record for a fetched resource."""
        return {
            "platform": "data.gov.tw",
            "catalog_dataset_id": dataset_id,
            "resource_id": resource_id,
            "provider_agency": provider_agency,
            "authoritative_level": authoritative_level,
            "original_resource_url_identifier": download_url_identifier,
            "content_hash": content_hash,
            "source_timestamp": source_timestamp,
            "fetched_at": fetched_at or _now_iso(),
            "extra": extra or {},
        }

    def validate_lineage(self, lineage: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that required lineage fields are present."""
        required = [
            "platform",
            "catalog_dataset_id",
            "resource_id",
            "provider_agency",
            "authoritative_level",
        ]
        missing = [f for f in required if not lineage.get(f)]
        complete = len(missing) == 0
        return {
            "complete": complete,
            "missing_fields": missing,
            "platform": lineage.get("platform"),
            "provider_agency": lineage.get("provider_agency"),
            "authoritative_level": lineage.get("authoritative_level"),
        }
