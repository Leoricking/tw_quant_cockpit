"""
data/governance/bridge_mops_v145.py — MOPS Governance Bridge v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Lightweight bridge. Does NOT rewrite MOPS provider.
"""
from __future__ import annotations

from typing import Any, Dict

from data.governance.models_v145 import HostRateLimitPolicy, SourceIdentity, SourceLineageRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class MOPSGovernanceBridge:
    """Lightweight bridge from MOPS provider to governance models."""

    def get_source_identity(self) -> SourceIdentity:
        return SourceIdentity(
            source_id="mops_official_v142",
            provider_id="mops_official",
            provider_name="Market Observation Post System (MOPS)",
            source_type="official_disclosure",
            authority_level="PRIMARY_OFFICIAL",
            official=True,
            aggregator=False,
            market="TW",
            domain="corporate_disclosure",
            agency="MOPS/TWSE",
            host="mops.twse.com.tw",
            endpoint_family="disclosure",
            dataset="material_info",
            introduced_in="1.4.2",
        )

    def map_lineage(self, mops_response: Dict[str, Any]) -> SourceLineageRecord:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return SourceLineageRecord(
            lineage_id=str(uuid.uuid4()),
            parent_lineage_ids=[],
            root_lineage_id="",
            provider_id="mops_official",
            source_id="mops_official_v142",
            authority_level="PRIMARY_OFFICIAL",
            dataset=mops_response.get("dataset", "disclosure"),
            endpoint=mops_response.get("endpoint", ""),
            request_fingerprint=mops_response.get("request_fingerprint", ""),
            fetch_run_id=mops_response.get("fetch_run_id", ""),
            response_id=mops_response.get("response_id", ""),
            cache_entry_id="",
            record_key=mops_response.get("record_key", ""),
            observation_date=mops_response.get("date"),
            reporting_period=mops_response.get("reporting_period"),
            published_at=now,
            available_from=now,
            fetched_at=now,
            normalized_at=now,
            source_content_hash=mops_response.get("source_content_hash", ""),
            normalized_content_hash=mops_response.get("normalized_content_hash", ""),
            schema_id="mops_disclosure_v1",
            schema_version="1.0",
            parser_version="1.4.2",
            transformation_ids=[],
            quality_status="UNKNOWN",
            freshness_status="UNKNOWN",
            PIT_status="UNKNOWN",
            conflict_status="NONE",
        )

    def get_host_policy(self) -> HostRateLimitPolicy:
        return HostRateLimitPolicy(
            policy_id="mops",
            host="mops.twse.com.tw",
            provider_id="mops_official",
            requests_per_minute=15.0,
            minimum_interval_ms=4000,
            concurrency_limit=1,
            source="CONSERVATIVE_DEFAULT",
            confidence="LOW",
        )
