"""
data/governance/bridge_twse_v145.py — TWSE Governance Bridge v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Lightweight bridge. Does NOT rewrite TWSE provider.
[!] Maps TWSE data to governance models only.
"""
from __future__ import annotations

from typing import Any, Dict

from data.governance.models_v145 import HostRateLimitPolicy, SourceIdentity, SourceLineageRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSEGovernanceBridge:
    """
    Lightweight bridge from TWSE provider to governance models.
    [!] Does NOT rewrite the TWSE provider.
    """

    def get_source_identity(self) -> SourceIdentity:
        return SourceIdentity(
            source_id="twse_official_v140",
            provider_id="twse_official",
            provider_name="Taiwan Stock Exchange (TWSE)",
            source_type="official_exchange",
            authority_level="PRIMARY_OFFICIAL",
            official=True,
            aggregator=False,
            market="TW",
            domain="equity",
            agency="TWSE",
            host="www.twse.com.tw",
            endpoint_family="daily",
            dataset="daily_ohlcv",
            introduced_in="1.4.0",
        )

    def map_lineage(self, twse_response: Dict[str, Any]) -> SourceLineageRecord:
        """Basic mapping of TWSE response to SourceLineageRecord."""
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return SourceLineageRecord(
            lineage_id=str(uuid.uuid4()),
            parent_lineage_ids=[],
            root_lineage_id="",
            provider_id="twse_official",
            source_id="twse_official_v140",
            authority_level="PRIMARY_OFFICIAL",
            dataset="daily_ohlcv",
            endpoint=twse_response.get("endpoint", ""),
            request_fingerprint=twse_response.get("request_fingerprint", ""),
            fetch_run_id=twse_response.get("fetch_run_id", ""),
            response_id=twse_response.get("response_id", ""),
            cache_entry_id="",
            record_key=twse_response.get("record_key", ""),
            observation_date=twse_response.get("date"),
            reporting_period=None,
            published_at=now,
            available_from=now,
            fetched_at=now,
            normalized_at=now,
            source_content_hash=twse_response.get("source_content_hash", ""),
            normalized_content_hash=twse_response.get("normalized_content_hash", ""),
            schema_id="twse_daily_v1",
            schema_version="1.0",
            parser_version="1.4.0",
            transformation_ids=[],
            quality_status="UNKNOWN",
            freshness_status="UNKNOWN",
            PIT_status="UNKNOWN",
            conflict_status="NONE",
        )

    def get_host_policy(self) -> HostRateLimitPolicy:
        return HostRateLimitPolicy(
            policy_id="twse_legacy",
            host="www.twse.com.tw",
            provider_id="twse_official",
            requests_per_minute=20.0,
            minimum_interval_ms=3000,
            concurrency_limit=1,
            source="CONSERVATIVE_DEFAULT",
            confidence="LOW",
        )
