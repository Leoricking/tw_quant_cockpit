"""
data/governance/bridge_tpex_v145.py — TPEx Governance Bridge v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Lightweight bridge. Does NOT rewrite TPEx provider.
"""
from __future__ import annotations

from typing import Any, Dict

from data.governance.models_v145 import HostRateLimitPolicy, SourceIdentity, SourceLineageRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExGovernanceBridge:
    """Lightweight bridge from TPEx provider to governance models."""

    def get_source_identity(self) -> SourceIdentity:
        return SourceIdentity(
            source_id="tpex_official_v141",
            provider_id="tpex_official",
            provider_name="Taipei Exchange (TPEx)",
            source_type="official_exchange",
            authority_level="PRIMARY_OFFICIAL",
            official=True,
            aggregator=False,
            market="TW",
            domain="otc_equity",
            agency="TPEx",
            host="www.tpex.org.tw",
            endpoint_family="daily",
            dataset="daily_ohlcv",
            introduced_in="1.4.1",
        )

    def map_lineage(self, tpex_response: Dict[str, Any]) -> SourceLineageRecord:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return SourceLineageRecord(
            lineage_id=str(uuid.uuid4()),
            parent_lineage_ids=[],
            root_lineage_id="",
            provider_id="tpex_official",
            source_id="tpex_official_v141",
            authority_level="PRIMARY_OFFICIAL",
            dataset="daily_ohlcv",
            endpoint=tpex_response.get("endpoint", ""),
            request_fingerprint=tpex_response.get("request_fingerprint", ""),
            fetch_run_id=tpex_response.get("fetch_run_id", ""),
            response_id=tpex_response.get("response_id", ""),
            cache_entry_id="",
            record_key=tpex_response.get("record_key", ""),
            observation_date=tpex_response.get("date"),
            reporting_period=None,
            published_at=now,
            available_from=now,
            fetched_at=now,
            normalized_at=now,
            source_content_hash=tpex_response.get("source_content_hash", ""),
            normalized_content_hash=tpex_response.get("normalized_content_hash", ""),
            schema_id="tpex_daily_v1",
            schema_version="1.0",
            parser_version="1.4.1",
            transformation_ids=[],
            quality_status="UNKNOWN",
            freshness_status="UNKNOWN",
            PIT_status="UNKNOWN",
            conflict_status="NONE",
        )

    def get_host_policy(self) -> HostRateLimitPolicy:
        return HostRateLimitPolicy(
            policy_id="tpex",
            host="www.tpex.org.tw",
            provider_id="tpex_official",
            requests_per_minute=20.0,
            minimum_interval_ms=3000,
            concurrency_limit=1,
            source="CONSERVATIVE_DEFAULT",
            confidence="LOW",
        )
