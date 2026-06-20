"""
data/providers/data_gov_tw/catalog_v143.py — Dataset catalog service v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Catalog manages metadata only. No auto-ingest from search.
[!] No auto-add to allowlist from search results.
[!] Catalog refresh is dry-run by default.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DataGovTwResource

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
DATA_GOV_TW_AUTO_DISCOVERY_ENABLED = False
DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False


class DataGovTwCatalogService:
    """
    Manages dataset catalog metadata from data.gov.tw.

    Rules:
    - Catalog manages metadata only.
    - Search results do NOT trigger auto-ingest.
    - Dataset title containing '股票' does NOT auto-add to allowlist.
    - Refresh is dry-run by default.
    - Has max_pages, max_records, request budget.
    - Supports incremental metadata updates.
    """

    def __init__(
        self,
        client=None,
        allowlist=None,
    ) -> None:
        self._client = client
        self._allowlist = allowlist
        self._datasets: Dict[str, DataGovTwDataset] = {}
        self._resources: Dict[str, List[DataGovTwResource]] = {}

    def list_datasets(
        self,
        category: Optional[str] = None,
        agency: Optional[str] = None,
        limit: int = 100,
    ) -> List[DataGovTwDataset]:
        """List cached datasets, optionally filtered."""
        result = list(self._datasets.values())
        if category:
            result = [d for d in result if d.category == category]
        if agency:
            result = [d for d in result if d.provider_agency == agency]
        return result[:limit]

    def search_datasets(
        self,
        keyword: str,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Search catalog metadata by keyword.
        NEVER auto-ingests results.
        NEVER auto-adds to allowlist.
        """
        matches = [
            d for d in self._datasets.values()
            if keyword.lower() in (d.title or "").lower()
            or keyword.lower() in (d.description or "").lower()
        ]
        return {
            "keyword": keyword,
            "results": [d.to_dict() for d in matches[:limit]],
            "total_found": len(matches),
            "auto_ingest": False,
            "auto_allowlist": False,
            "message": "Search results for metadata inspection only. No auto-ingest.",
        }

    def get_dataset(self, dataset_id: str) -> Optional[DataGovTwDataset]:
        return self._datasets.get(dataset_id)

    def get_dataset_metadata(self, dataset_id: str) -> Dict[str, Any]:
        ds = self._datasets.get(dataset_id)
        if ds is None:
            return {"dataset_id": dataset_id, "found": False, "error": "Dataset not in local catalog"}
        result = ds.to_dict()
        result["found"] = True
        if self._allowlist:
            result["allowlist"] = self._allowlist.check_allowlist_result(dataset_id)
        return result

    def list_resources(self, dataset_id: str) -> List[DataGovTwResource]:
        return self._resources.get(dataset_id, [])

    def get_resource(self, dataset_id: str, resource_id: str) -> Optional[DataGovTwResource]:
        for r in self._resources.get(dataset_id, []):
            if r.resource_id == resource_id:
                return r
        return None

    def load_from_fixture(self, datasets: List[Dict[str, Any]]) -> int:
        """Load datasets from fixture data (for offline testing)."""
        count = 0
        for d in datasets:
            ds = DataGovTwDataset.from_dict(d)
            self._datasets[ds.dataset_id] = ds
            count += 1
        return count

    def load_resources_from_fixture(
        self, dataset_id: str, resources: List[Dict[str, Any]]
    ) -> int:
        result = []
        for r in resources:
            res = DataGovTwResource.from_dict(r)
            result.append(res)
        self._resources[dataset_id] = result
        return len(result)

    def refresh_catalog_metadata(
        self,
        dry_run: bool = True,
        max_pages: int = 5,
        max_records: int = 500,
        request_budget: int = 20,
    ) -> Dict[str, Any]:
        """
        Refresh catalog metadata from data.gov.tw API.
        Dry-run by default. Does not download resources.
        """
        if self._client is None:
            return {
                "status": "SKIPPED",
                "dry_run": dry_run,
                "reason": "No HTTP client configured — offline mode",
                "records_fetched": 0,
                "auto_download": False,
            }
        return {
            "status": "DRY_RUN" if dry_run else "NOT_IMPLEMENTED",
            "dry_run": dry_run,
            "max_pages": max_pages,
            "max_records": max_records,
            "request_budget": request_budget,
            "records_fetched": 0,
            "auto_download": False,
            "message": "Catalog refresh requires explicit --execute flag.",
        }

    def compare_catalog_versions(
        self, old_snapshot: Dict[str, Any], new_snapshot: Dict[str, Any]
    ) -> Dict[str, Any]:
        old_ids = set(old_snapshot.get("dataset_ids", []))
        new_ids = set(new_snapshot.get("dataset_ids", []))
        added = sorted(new_ids - old_ids)
        removed = sorted(old_ids - new_ids)
        return {
            "added": added,
            "removed": removed,
            "added_count": len(added),
            "removed_count": len(removed),
        }

    def list_removed_datasets(self) -> List[str]:
        from data.providers.data_gov_tw.models_v143 import DatasetStatus
        return [
            d.dataset_id for d in self._datasets.values()
            if d.status == DatasetStatus.REMOVED.value
        ]

    def list_changed_datasets(self) -> List[str]:
        return []  # Populated by revision service in real operation
