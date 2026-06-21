"""
data/governance/bridge_finmind_v145.py — FinMind Governance Bridge v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Lightweight bridge. Does NOT rewrite FinMind provider.
[!] SECONDARY_AGGREGATOR. Cannot override primary source.
"""
from __future__ import annotations

from typing import Any, Dict

from data.governance.models_v145 import HostRateLimitPolicy, SourceIdentity, SourceLineageRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_CAN_OVERRIDE_PRIMARY = False


class FinMindGovernanceBridge:
    """
    Lightweight bridge from FinMind adapter to governance models.
    [!] SECONDARY_AGGREGATOR — cannot override primary sources.
    """

    def get_source_identity(self) -> SourceIdentity:
        return SourceIdentity(
            source_id="finmind_v144",
            provider_id="finmind",
            provider_name="FinMind (財報狗)",
            source_type="secondary_aggregator",
            authority_level="SECONDARY_AGGREGATOR",
            official=False,
            aggregator=True,
            market="TW",
            domain="multi_domain",
            agency="FinMind",
            host="api.finmindtrade.com",
            endpoint_family="v4",
            dataset="taiwan_stock_price",
            introduced_in="1.4.4",
        )

    def map_lineage(self, finmind_response: Dict[str, Any]) -> SourceLineageRecord:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return SourceLineageRecord(
            lineage_id=str(uuid.uuid4()),
            parent_lineage_ids=[],
            root_lineage_id="",
            provider_id="finmind",
            source_id="finmind_v144",
            authority_level="SECONDARY_AGGREGATOR",
            dataset=finmind_response.get("dataset", "taiwan_stock_price"),
            endpoint=finmind_response.get("endpoint", "/v4/data"),
            request_fingerprint=finmind_response.get("request_fingerprint", ""),
            fetch_run_id=finmind_response.get("fetch_run_id", ""),
            response_id=finmind_response.get("response_id", ""),
            cache_entry_id="",
            record_key=finmind_response.get("record_key", ""),
            observation_date=finmind_response.get("date"),
            reporting_period=None,
            published_at=now,
            available_from=now,
            fetched_at=now,
            normalized_at=now,
            source_content_hash=finmind_response.get("source_content_hash", ""),
            normalized_content_hash=finmind_response.get("normalized_content_hash", ""),
            schema_id="finmind_v4",
            schema_version="4.0",
            parser_version="1.4.4",
            transformation_ids=[],
            quality_status="UNKNOWN",
            freshness_status="UNKNOWN",
            PIT_status="UNKNOWN",
            conflict_status="NONE",
            formal_use_allowed=False,  # SECONDARY_AGGREGATOR
        )

    def get_host_policy(self) -> HostRateLimitPolicy:
        return HostRateLimitPolicy(
            policy_id="finmind",
            host="api.finmindtrade.com",
            provider_id="finmind",
            requests_per_minute=10.0,
            minimum_interval_ms=6000,
            concurrency_limit=1,
            source="CONSERVATIVE_DEFAULT",
            confidence="LOW",
        )
