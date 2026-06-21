"""
data/stable/schema_version_registry_v149.py — Schema Version Registry v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Tracks schema versions for each provider; drift detection baseline.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

_SCHEMA_REGISTRY_VERSION = "1.4.9"

_SCHEMA_ENTRIES: List[Dict[str, Any]] = [
    {
        "provider_id":      "twse_official",
        "schema_id":        "twse_daily_price_v1",
        "version":          "1",
        "fields":           ["date", "stock_id", "open", "high", "low", "close", "volume",
                             "fetched_at", "source_hash"],
        "pit_fields":       ["fetched_at", "available_from"],
        "drift_baseline":   "1.4.0",
        "stable_since":     "1.4.9",
        "breaking_changes": [],
    },
    {
        "provider_id":      "tpex_official",
        "schema_id":        "tpex_daily_price_v1",
        "version":          "1",
        "fields":           ["date", "stock_id", "open", "high", "low", "close", "volume",
                             "fetched_at", "source_hash"],
        "pit_fields":       ["fetched_at", "available_from"],
        "drift_baseline":   "1.4.1",
        "stable_since":     "1.4.9",
        "breaking_changes": [],
    },
    {
        "provider_id":      "mops_official",
        "schema_id":        "mops_fundamental_v1",
        "version":          "1",
        "fields":           ["report_date", "stock_id", "revenue", "gross_profit",
                             "operating_income", "net_income", "fetched_at", "revision_seq"],
        "pit_fields":       ["report_date", "fetched_at", "revision_seq"],
        "drift_baseline":   "1.4.2",
        "stable_since":     "1.4.9",
        "breaking_changes": [],
    },
    {
        "provider_id":      "data_gov_tw_official",
        "schema_id":        "data_gov_tw_dataset_v1",
        "version":          "1",
        "fields":           ["dataset_id", "resource_id", "record_date", "value",
                             "fetched_at", "license", "source_hash"],
        "pit_fields":       ["record_date", "fetched_at"],
        "drift_baseline":   "1.4.3",
        "stable_since":     "1.4.9",
        "breaking_changes": [],
    },
    {
        "provider_id":      "finmind_aggregator",
        "schema_id":        "finmind_price_v1",
        "version":          "1",
        "fields":           ["date", "stock_id", "open", "high", "low", "close", "volume",
                             "fetched_at", "source_hash", "normalized_hash"],
        "pit_fields":       ["fetched_at"],
        "drift_baseline":   "1.4.4",
        "stable_since":     "1.4.9",
        "breaking_changes": [],
    },
    {
        "provider_id":      "ptt_stock",
        "schema_id":        "ptt_article_v1",
        "version":          "1",
        "fields":           ["article_id", "board", "title", "posted_at", "fetched_at",
                             "author_hash", "sentiment_label", "source_hash"],
        "pit_fields":       ["posted_at", "fetched_at"],
        "drift_baseline":   "1.4.7",
        "stable_since":     "1.4.9",
        "breaking_changes": [],
    },
]


class SchemaVersionRegistry:
    """
    Tracks and validates schema versions for all stable providers.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _SCHEMA_REGISTRY_VERSION

    def get_all(self) -> List[Dict[str, Any]]:
        return list(_SCHEMA_ENTRIES)

    def get_by_provider(self, provider_id: str) -> Dict[str, Any]:
        for e in _SCHEMA_ENTRIES:
            if e["provider_id"] == provider_id:
                return dict(e)
        raise KeyError(f"Unknown provider schema: {provider_id}")

    def validate(self) -> Dict[str, Any]:
        total = len(_SCHEMA_ENTRIES)
        drift_detected = [e["schema_id"] for e in _SCHEMA_ENTRIES if e["breaking_changes"]]
        missing_pit = [e["schema_id"] for e in _SCHEMA_ENTRIES if not e["pit_fields"]]
        ok = total == 6 and not drift_detected and not missing_pit
        return {
            "registry_version": self.VERSION,
            "total_schemas": total,
            "drift_detected": drift_detected,
            "missing_pit_fields": missing_pit,
            "valid": ok,
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def get_summary(self) -> Dict[str, Any]:
        result = self.validate()
        items = [(f"schema_{e['schema_id']}",
                  "PASS" if not e["breaking_changes"] else "FAIL",
                  f"version={e['version']} pit_fields={len(e['pit_fields'])}")
                 for e in _SCHEMA_ENTRIES]
        result["items"] = items
        return result
