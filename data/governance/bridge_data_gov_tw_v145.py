"""
data/governance/bridge_data_gov_tw_v145.py — data.gov.tw Governance Bridge v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Lightweight bridge. Does NOT rewrite data.gov.tw provider.
"""
from __future__ import annotations

from typing import Any, Dict

from data.governance.models_v145 import HostRateLimitPolicy, SourceIdentity, SourceLineageRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataGovTwGovernanceBridge:
    """Lightweight bridge from data.gov.tw provider to governance models."""

    def get_source_identity(self) -> SourceIdentity:
        return SourceIdentity(
            source_id="data_gov_tw_official_v143",
            provider_id="data_gov_tw_official",
            provider_name="data.gov.tw Open Data Platform",
            source_type="government_open_data",
            authority_level="PRIMARY_DOMAIN_OFFICIAL",
            official=True,
            aggregator=False,
            market="TW",
            domain="government_data",
            agency="NIAS/Executive Yuan",
            host="data.gov.tw",
            endpoint_family="catalog",
            dataset="open_data_catalog",
            introduced_in="1.4.3",
        )

    def map_lineage(self, response: Dict[str, Any]) -> SourceLineageRecord:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return SourceLineageRecord(
            lineage_id=str(uuid.uuid4()),
            parent_lineage_ids=[],
            root_lineage_id="",
            provider_id="data_gov_tw_official",
            source_id="data_gov_tw_official_v143",
            authority_level="PRIMARY_DOMAIN_OFFICIAL",
            dataset=response.get("dataset", "open_data"),
            endpoint=response.get("endpoint", ""),
            request_fingerprint=response.get("request_fingerprint", ""),
            fetch_run_id=response.get("fetch_run_id", ""),
            response_id=response.get("response_id", ""),
            cache_entry_id="",
            record_key=response.get("record_key", ""),
            observation_date=response.get("date"),
            reporting_period=None,
            published_at=now,
            available_from=now,
            fetched_at=now,
            normalized_at=now,
            source_content_hash=response.get("source_content_hash", ""),
            normalized_content_hash=response.get("normalized_content_hash", ""),
            schema_id="data_gov_tw_v1",
            schema_version="1.0",
            parser_version="1.4.3",
            transformation_ids=[],
            quality_status="UNKNOWN",
            freshness_status="UNKNOWN",
            PIT_status="UNKNOWN",
            conflict_status="NONE",
        )

    def get_host_policy(self) -> HostRateLimitPolicy:
        return HostRateLimitPolicy(
            policy_id="data_gov_tw_catalog",
            host="data.gov.tw",
            provider_id="data_gov_tw_official",
            requests_per_minute=30.0,
            minimum_interval_ms=2000,
            concurrency_limit=1,
            source="CONSERVATIVE_DEFAULT",
            confidence="LOW",
        )
