"""
data/providers/finmind/query_v144.py — FinMind query service v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All results include provider, authority, dataset, records, quality, freshness,
    pit_class, conflict_status, quota_evidence, provenance, warnings.
[!] SECONDARY_AGGREGATOR. Cannot override primary source.
"""
from __future__ import annotations

import datetime
import logging
from typing import Any, Callable, Dict, List, Optional

from data.providers.finmind.auth_v144 import FinMindAuthManager
from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
from data.providers.finmind.capabilities_v144 import get_capabilities
from data.providers.finmind.client_v144 import FinMindClient
from data.providers.finmind.conflict_detection_v144 import FinMindConflictDetector
from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
from data.providers.finmind.normalizer_v144 import FinMindNormalizer
from data.providers.finmind.parser_v144 import FinMindParser
from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
from data.providers.finmind.quota_v144 import FinMindQuotaManager
from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
from data.providers.finmind.schema_registry_v144 import FinMindSchemaRegistry

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class FinMindQueryService:
    """
    Main query service for FinMind v1.4.4.
    Composes all subsystems. Injectable transport for offline tests.
    All results annotated with SECONDARY_AGGREGATOR authority.
    """

    PROVIDER_ID = "finmind"
    AUTHORITY = "SECONDARY_AGGREGATOR"
    API_VERSION = "v4"

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._auth = FinMindAuthManager()
        self._quota = FinMindQuotaManager(authenticated=self._auth.authenticated_mode)
        self._client = FinMindClient(transport=transport)
        self._parser = FinMindParser()
        self._normalizer = FinMindNormalizer()
        self._schema_registry = FinMindSchemaRegistry()
        self._schema_drift = FinMindSchemaDriftDetector()
        self._allowlist = FinMindDatasetAllowlist()
        self._error_classifier = FinMindErrorClassifier()
        self._pit_guard = FinMindPITGuard()
        self._conflict_detector = FinMindConflictDetector()
        self._cache_policy = FinMindCachePolicy()
        self._last_fetch_status: Optional[Dict[str, Any]] = None
        self._conflicts: List[Dict[str, Any]] = []

    def get_dataset_capabilities(self) -> List[Dict[str, Any]]:
        """Return all FinMind capabilities."""
        return get_capabilities()

    def get_dataset_schema(self, dataset: str) -> Optional[Dict[str, Any]]:
        """Return schema for a dataset."""
        return self._schema_registry.get_schema(dataset)

    def get_records(
        self,
        dataset: str,
        data_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch and normalize records for any supported dataset."""
        if not self._allowlist.is_allowed(dataset):
            return self._blocked_result(dataset, "Dataset not in allowlist or not approved")

        if self._quota.is_exhausted():
            return self._blocked_result(dataset, "Quota exhausted")

        raw = self._client.fetch(
            dataset=dataset,
            data_id=data_id,
            start_date=start_date,
            end_date=end_date,
            token=self._auth.get_token_for_request(),
        )
        self._quota.record_request()
        self._quota.update_from_response(raw.get("headers", {}))

        parsed = self._parser.parse_response(raw)
        self._last_fetch_status = {
            "dataset": dataset,
            "data_id": data_id,
            "error_code": parsed.get("error_code"),
            "is_success": parsed.get("is_success"),
            "fetched_at": _now_iso(),
        }

        if not parsed["is_success"]:
            if parsed.get("is_quota_exceeded"):
                self._quota.record_quota_error("QUOTA_EXCEEDED from API")
            return self._error_result(dataset, parsed)

        records = parsed["data"]
        pit_class = self._pit_guard.classify_pit(dataset)

        # Schema drift detection
        if records:
            actual_fields = list(records[0].keys())
            drift_result = self._schema_drift.detect_drift(dataset, actual_fields)
            if drift_result.get("blocked"):
                return self._blocked_result(dataset, f"Schema drift blocked: {drift_result.get('status')}")
        else:
            drift_result = {"status": "NO_CHANGE", "blocked": False}

        return {
            "provider": self.PROVIDER_ID,
            "authority": self.AUTHORITY,
            "dataset": dataset,
            "data_id": data_id,
            "records": records,
            "record_count": len(records),
            "quality": "SECONDARY",
            "freshness": "DAILY",
            "pit_class": pit_class.value,
            "conflict_status": "NOT_CHECKED",
            "quota_evidence": self._quota.get_status().status.value,
            "provenance": {
                "source": self.PROVIDER_ID,
                "api_version": self.API_VERSION,
                "authority": self.AUTHORITY,
            },
            "warnings": [],
            "schema_drift": drift_result.get("status"),
            "fetched_at": _now_iso(),
            "no_real_orders": True,
        }

    def get_price(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch and normalize price data for a symbol."""
        result = self.get_records("TaiwanStockPrice", symbol, start_date, end_date)
        if result.get("records"):
            result["records"] = self._normalizer.normalize_price(result["records"])
        return result

    def get_institutional(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch and normalize institutional flow data."""
        result = self.get_records("TaiwanStockInstitutionalInvestorsBuySell", symbol, start_date, end_date)
        if result.get("records"):
            result["records"] = self._normalizer.normalize_institutional_narrow(result["records"])
        return result

    def get_margin(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch and normalize margin/short sale data."""
        result = self.get_records("TaiwanStockMarginPurchaseShortSale", symbol, start_date, end_date)
        if result.get("records"):
            result["records"] = self._normalizer.normalize_margin(result["records"])
        return result

    def get_records_as_of(
        self,
        dataset: str,
        data_id: str,
        as_of: str,
    ) -> Dict[str, Any]:
        """Fetch records and filter by as-of date with PIT guard."""
        result = self.get_records(dataset, data_id, end_date=as_of)
        if not result.get("records"):
            return result
        pit_class_str = result.get("pit_class", "UNKNOWN")
        from data.providers.finmind.models_v144 import FinMindPITClass
        try:
            pit_class = FinMindPITClass(pit_class_str)
        except ValueError:
            pit_class = FinMindPITClass.UNKNOWN
        filtered = [
            r for r in result["records"]
            if self._pit_guard.validate_as_of(r, as_of, pit_class)
        ]
        result["records"] = filtered
        result["record_count"] = len(filtered)
        result["pit_guard_applied"] = True
        return result

    def get_quota_status(self) -> Dict[str, Any]:
        """Return current quota status."""
        state = self._quota.get_status()
        return {
            "status": state.status.value,
            "quota_limit": state.quota_limit,
            "quota_used": state.quota_used,
            "quota_remaining": state.quota_remaining,
            "plan_unknown": state.plan_unknown,
            "last_checked_at": state.last_checked_at,
            "last_quota_error": state.last_quota_error,
        }

    def get_last_fetch_status(self) -> Optional[Dict[str, Any]]:
        """Return status of the most recent fetch."""
        return self._last_fetch_status

    def get_schema_drift_status(self, dataset: str) -> Dict[str, Any]:
        """Return latest schema drift status for a dataset."""
        return self._schema_drift.detect_drift(dataset, [])

    def compare_with_primary(
        self,
        dataset: str,
        symbol: str,
        primary_records: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Compare FinMind data with primary source. Primary always wins."""
        result = self.get_records(dataset, symbol)
        finmind_records = result.get("records", [])
        if dataset == "TaiwanStockPrice":
            conflicts = self._conflict_detector.compare_price(primary_records, finmind_records)
        elif "Institutional" in dataset:
            conflicts = self._conflict_detector.compare_institutional(primary_records, finmind_records)
        elif "Margin" in dataset:
            conflicts = self._conflict_detector.compare_margin(primary_records, finmind_records)
        else:
            conflicts = []
        self._conflicts.extend(conflicts)
        return {
            "dataset": dataset,
            "symbol": symbol,
            "conflicts": conflicts,
            "primary_wins": True,
            "finmind_preserved_as_secondary": True,
        }

    def get_conflicts(self) -> List[Dict[str, Any]]:
        """Return all recorded conflicts from comparisons."""
        return list(self._conflicts)

    def get_provider_lineage(self) -> Dict[str, Any]:
        """Return provider lineage information."""
        return {
            "provider": self.PROVIDER_ID,
            "authority": self.AUTHORITY,
            "api_version": self.API_VERSION,
            "official": False,
            "aggregator": True,
            "can_override_primary_provider": False,
            "token_mode": "authenticated" if self._auth.authenticated_mode else "anonymous",
            "token_fingerprint": self._auth.token_fingerprint,
        }

    def summarize_coverage(self) -> Dict[str, Any]:
        """Return coverage summary for all supported datasets."""
        supported = self._allowlist.get_supported()
        return {
            "provider": self.PROVIDER_ID,
            "authority": self.AUTHORITY,
            "supported_datasets": [d.get("dataset") for d in supported],
            "total_supported": len(supported),
            "allowlist_summary": self._allowlist.summary(),
        }

    def _blocked_result(self, dataset: str, reason: str) -> Dict[str, Any]:
        return {
            "provider": self.PROVIDER_ID,
            "authority": self.AUTHORITY,
            "dataset": dataset,
            "records": [],
            "record_count": 0,
            "quality": "BLOCKED",
            "freshness": "UNKNOWN",
            "pit_class": "UNKNOWN",
            "conflict_status": "NOT_CHECKED",
            "quota_evidence": "UNKNOWN",
            "provenance": {"source": self.PROVIDER_ID},
            "warnings": [reason],
            "blocked": True,
            "no_real_orders": True,
        }

    def _error_result(self, dataset: str, parsed: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": self.PROVIDER_ID,
            "authority": self.AUTHORITY,
            "dataset": dataset,
            "records": [],
            "record_count": 0,
            "quality": "ERROR",
            "freshness": "UNKNOWN",
            "pit_class": "UNKNOWN",
            "conflict_status": "NOT_CHECKED",
            "quota_evidence": self._quota.get_status().status.value,
            "provenance": {"source": self.PROVIDER_ID},
            "warnings": [parsed.get("error_code", "UNKNOWN_ERROR")],
            "error_code": parsed.get("error_code"),
            "no_real_orders": True,
        }
