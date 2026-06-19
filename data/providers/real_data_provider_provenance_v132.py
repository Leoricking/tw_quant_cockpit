"""
data/providers/real_data_provider_provenance_v132.py — Extended provenance for v1.3.2.
Extends DataProvenanceRecord from v1.3.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Never records credentials. Never stores complete API response in git.
[!] fallback_from is NEVER mock.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from data.providers.real_data_provider_models import (
    CacheStatus,
    ProviderType,
    _now_iso,
)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False

_MOCK_FALLBACK_FORBIDDEN = {"mock", "test_fixture"}


@dataclass
class ProviderProvenanceRecord:
    """
    Extended provenance record for v1.3.2 provider operations.

    [!] Never records credentials (no passwords, tokens, secrets).
    [!] fallback_from must NEVER be mock or test_fixture.
    [!] source_reference is file path or 'local_db' only — no API credentials.
    """
    provider_id: str = ""
    provider_name: str = ""
    provider_type: str = ProviderType.UNKNOWN
    capability: str = ""
    request_id: str = ""
    source_type: str = ""
    source_reference: str = ""  # file path or "local_db" — NO credentials
    fetched_at: str = field(default_factory=_now_iso)
    source_timestamp: str = ""
    market_timestamp: str = ""
    normalized_at: str = field(default_factory=_now_iso)
    schema_version: str = "1.3.2"
    cache_status: str = CacheStatus.MISS
    attempt_count: int = 1
    fallback_from: Optional[str] = None  # NEVER mock
    raw_field_availability: Dict[str, bool] = field(default_factory=dict)
    transformations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    content_hash: str = ""  # SHA256 of record_count + first key fields
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.fallback_from is not None:
            lowered = self.fallback_from.lower().strip()
            assert lowered not in _MOCK_FALLBACK_FORBIDDEN, (
                f"fallback_from must NEVER be mock or test_fixture. Got: '{self.fallback_from}'"
            )

    def to_dict(self) -> dict:
        return {
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "provider_type": self.provider_type,
            "capability": self.capability,
            "request_id": self.request_id,
            "source_type": self.source_type,
            "source_reference": self.source_reference,
            "fetched_at": self.fetched_at,
            "source_timestamp": self.source_timestamp,
            "market_timestamp": self.market_timestamp,
            "normalized_at": self.normalized_at,
            "schema_version": self.schema_version,
            "cache_status": self.cache_status,
            "attempt_count": self.attempt_count,
            "fallback_from": self.fallback_from,
            "raw_field_availability": dict(self.raw_field_availability),
            "transformations": list(self.transformations),
            "warnings": list(self.warnings),
            "content_hash": self.content_hash,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ProviderProvenanceRecord":
        """Forward-compatible: ignores unknown keys."""
        return cls(
            provider_id=d.get("provider_id", ""),
            provider_name=d.get("provider_name", ""),
            provider_type=d.get("provider_type", ProviderType.UNKNOWN),
            capability=d.get("capability", ""),
            request_id=d.get("request_id", ""),
            source_type=d.get("source_type", ""),
            source_reference=d.get("source_reference", ""),
            fetched_at=d.get("fetched_at", _now_iso()),
            source_timestamp=d.get("source_timestamp", ""),
            market_timestamp=d.get("market_timestamp", ""),
            normalized_at=d.get("normalized_at", _now_iso()),
            schema_version=d.get("schema_version", "1.3.2"),
            cache_status=d.get("cache_status", CacheStatus.MISS),
            attempt_count=d.get("attempt_count", 1),
            fallback_from=d.get("fallback_from", None),
            raw_field_availability=dict(d.get("raw_field_availability", {})),
            transformations=list(d.get("transformations", [])),
            warnings=list(d.get("warnings", [])),
            content_hash=d.get("content_hash", ""),
            metadata=dict(d.get("metadata", {})),
        )

    def to_data_provenance_record(self):
        """
        Convert to v1.3.0 DataProvenanceRecord for backward compatibility.
        Returns a dict if the import is unavailable.
        """
        try:
            from real_data_quality.dq_schema import DataProvenanceRecord, DataMode
            return DataProvenanceRecord(
                provider=self.provider_id,
                source_type=self.source_type,
                fetched_at=self.fetched_at,
                market_timestamp=self.market_timestamp,
                normalized_at=self.normalized_at,
                symbol="",
                market="",
                data_mode=DataMode.REAL,
                schema_version=self.schema_version,
                raw_field_availability=dict(self.raw_field_availability),
                transformation_notes="; ".join(self.transformations),
            )
        except (ImportError, TypeError):
            # Fallback: return dict representation compatible with v1.3.0 schema
            return self.to_dict()
