"""
data/providers/data_gov_tw/models_v143.py — data.gov.tw Provider domain models v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] DATA_GOV_TW_REALTIME_AVAILABLE = False.
[!] DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False.
[!] DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False.
[!] Cannot override TWSE/TPEx/MOPS as primary providers.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DataGovTwCapability(str, Enum):
    DATASET_CATALOG = "DATASET_CATALOG"
    DATASET_METADATA = "DATASET_METADATA"
    DATASET_RESOURCE = "DATASET_RESOURCE"
    JSON_RESOURCE = "JSON_RESOURCE"
    CSV_RESOURCE = "CSV_RESOURCE"
    XML_RESOURCE = "XML_RESOURCE"
    ZIP_RESOURCE = "ZIP_RESOURCE"
    OAS_API_RESOURCE = "OAS_API_RESOURCE"
    LICENSE_VALIDATION = "LICENSE_VALIDATION"
    SCHEMA_CONTRACT = "SCHEMA_CONTRACT"
    DATASET_REVISION = "DATASET_REVISION"
    SOURCE_LINEAGE = "SOURCE_LINEAGE"
    UPDATE_FREQUENCY = "UPDATE_FREQUENCY"
    MACRO_DATA = "MACRO_DATA"
    INDUSTRY_DATA = "INDUSTRY_DATA"
    TRADE_DATA = "TRADE_DATA"
    ENERGY_DATA = "ENERGY_DATA"
    POLICY_DATA = "POLICY_DATA"
    CORPORATE_REGISTRY_SUPPLEMENT = "CORPORATE_REGISTRY_SUPPLEMENT"


class DatasetStatus(str, Enum):
    APPROVED = "APPROVED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    PLANNED = "PLANNED"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
    REMOVED = "REMOVED"
    BLOCKED = "BLOCKED"


class MetadataStatus(str, Enum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    OUTDATED = "OUTDATED"
    MISSING_LICENSE = "MISSING_LICENSE"
    MISSING_SCHEMA = "MISSING_SCHEMA"
    MISSING_RESOURCE = "MISSING_RESOURCE"
    REMOVED = "REMOVED"
    BLOCKED = "BLOCKED"


class LicenseStatus(str, Enum):
    APPROVED = "APPROVED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    RESTRICTED = "RESTRICTED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class QualityStatus(str, Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class FreshnessStatus(str, Enum):
    FRESH = "FRESH"
    NEAR_STALE = "NEAR_STALE"
    STALE = "STALE"
    DELAYED = "DELAYED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class AuthoritativeLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY_OFFICIAL = "SECONDARY_OFFICIAL"
    SUPPLEMENTARY = "SUPPLEMENTARY"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    UNKNOWN = "UNKNOWN"


class UpdateFrequency(str, Enum):
    REAL_TIME_METADATA_ONLY = "REAL_TIME_METADATA_ONLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"
    IRREGULAR = "IRREGULAR"
    UNSCHEDULED = "UNSCHEDULED"
    UNKNOWN = "UNKNOWN"


class FetchStatus(str, Enum):
    SUCCESS = "SUCCESS"
    RATE_LIMITED = "RATE_LIMITED"
    BLOCKED = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    MALFORMED = "MALFORMED"
    TIMEOUT = "TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"
    SCHEMA_CHANGED = "SCHEMA_CHANGED"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    NOT_ALLOWLISTED = "NOT_ALLOWLISTED"
    LICENSE_BLOCKED = "LICENSE_BLOCKED"
    DRY_RUN = "DRY_RUN"


def _safe_str(v: Any) -> Optional[str]:
    return str(v) if v is not None else None


def _safe_dict(v: Any) -> Dict[str, Any]:
    if isinstance(v, dict):
        return v
    return {}


def _safe_list(v: Any) -> List[Any]:
    if isinstance(v, list):
        return v
    return []


# ---------------------------------------------------------------------------
# DataGovTwDataset
# ---------------------------------------------------------------------------

@dataclass
class DataGovTwDataset:
    """Metadata for a single data.gov.tw dataset."""
    dataset_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    research_domain: Optional[str] = None
    provider_agency: Optional[str] = None
    agency_code: Optional[str] = None
    dataset_type: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    language: Optional[str] = None
    published_at: Optional[str] = None
    metadata_updated_at: Optional[str] = None
    update_frequency: Optional[str] = None
    temporal_coverage_start: Optional[str] = None
    temporal_coverage_end: Optional[str] = None
    spatial_coverage: Optional[str] = None
    license_name: Optional[str] = None
    license_url: Optional[str] = None
    pricing_policy: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    status: str = DatasetStatus.PLANNED.value
    official: bool = True
    allowlisted: bool = False
    approved: bool = False
    authoritative_level: str = AuthoritativeLevel.UNKNOWN.value
    metadata_source: Optional[str] = None
    fetched_at: Optional[str] = None
    content_hash: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "research_domain": self.research_domain,
            "provider_agency": self.provider_agency,
            "agency_code": self.agency_code,
            "dataset_type": self.dataset_type,
            "keywords": list(self.keywords),
            "language": self.language,
            "published_at": self.published_at,
            "metadata_updated_at": self.metadata_updated_at,
            "update_frequency": self.update_frequency,
            "temporal_coverage_start": self.temporal_coverage_start,
            "temporal_coverage_end": self.temporal_coverage_end,
            "spatial_coverage": self.spatial_coverage,
            "license_name": self.license_name,
            "license_url": self.license_url,
            "pricing_policy": self.pricing_policy,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "status": self.status,
            "official": self.official,
            "allowlisted": self.allowlisted,
            "approved": self.approved,
            "authoritative_level": self.authoritative_level,
            "metadata_source": self.metadata_source,
            "fetched_at": self.fetched_at,
            "content_hash": self.content_hash,
            "provenance": dict(self.provenance),
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataGovTwDataset":
        return cls(
            dataset_id=d.get("dataset_id", ""),
            title=d.get("title"),
            description=d.get("description"),
            category=d.get("category"),
            research_domain=d.get("research_domain"),
            provider_agency=d.get("provider_agency"),
            agency_code=d.get("agency_code"),
            dataset_type=d.get("dataset_type"),
            keywords=_safe_list(d.get("keywords")),
            language=d.get("language"),
            published_at=d.get("published_at"),
            metadata_updated_at=d.get("metadata_updated_at"),
            update_frequency=d.get("update_frequency"),
            temporal_coverage_start=d.get("temporal_coverage_start"),
            temporal_coverage_end=d.get("temporal_coverage_end"),
            spatial_coverage=d.get("spatial_coverage"),
            license_name=d.get("license_name"),
            license_url=d.get("license_url"),
            pricing_policy=d.get("pricing_policy"),
            contact_name=d.get("contact_name"),
            contact_email=d.get("contact_email"),
            status=d.get("status", DatasetStatus.PLANNED.value),
            official=bool(d.get("official", True)),
            allowlisted=bool(d.get("allowlisted", False)),
            approved=bool(d.get("approved", False)),
            authoritative_level=d.get("authoritative_level", AuthoritativeLevel.UNKNOWN.value),
            metadata_source=d.get("metadata_source"),
            fetched_at=d.get("fetched_at"),
            content_hash=d.get("content_hash"),
            provenance=_safe_dict(d.get("provenance")),
            warnings=_safe_list(d.get("warnings")),
            metadata=_safe_dict(d.get("metadata")),
        )


# ---------------------------------------------------------------------------
# DataGovTwResource
# ---------------------------------------------------------------------------

@dataclass
class DataGovTwResource:
    """A single downloadable resource within a data.gov.tw dataset."""
    resource_id: str
    dataset_id: str
    title: Optional[str] = None
    format: Optional[str] = None
    media_type: Optional[str] = None
    download_url: Optional[str] = None
    api_doc_url: Optional[str] = None
    schema_url: Optional[str] = None
    encoding: Optional[str] = None
    compression: Optional[str] = None
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None
    last_modified: Optional[str] = None
    source_timestamp: Optional[str] = None
    fetched_at: Optional[str] = None
    enabled: bool = True
    parse_status: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "dataset_id": self.dataset_id,
            "title": self.title,
            "format": self.format,
            "media_type": self.media_type,
            "download_url": self.download_url,
            "api_doc_url": self.api_doc_url,
            "schema_url": self.schema_url,
            "encoding": self.encoding,
            "compression": self.compression,
            "size_bytes": self.size_bytes,
            "checksum": self.checksum,
            "last_modified": self.last_modified,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "enabled": self.enabled,
            "parse_status": self.parse_status,
            "provenance": dict(self.provenance),
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataGovTwResource":
        return cls(
            resource_id=d.get("resource_id", ""),
            dataset_id=d.get("dataset_id", ""),
            title=d.get("title"),
            format=d.get("format"),
            media_type=d.get("media_type"),
            download_url=d.get("download_url"),
            api_doc_url=d.get("api_doc_url"),
            schema_url=d.get("schema_url"),
            encoding=d.get("encoding"),
            compression=d.get("compression"),
            size_bytes=d.get("size_bytes"),
            checksum=d.get("checksum"),
            last_modified=d.get("last_modified"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at"),
            enabled=bool(d.get("enabled", True)),
            parse_status=d.get("parse_status"),
            provenance=_safe_dict(d.get("provenance")),
            warnings=_safe_list(d.get("warnings")),
            metadata=_safe_dict(d.get("metadata")),
        )


# ---------------------------------------------------------------------------
# DataGovTwSchemaContract
# ---------------------------------------------------------------------------

@dataclass
class DataGovTwSchemaContract:
    """Schema contract defining expected structure for a dataset resource."""
    schema_id: str
    dataset_id: str
    version: str = "1.0"
    expected_format: Optional[str] = None
    required_fields: List[str] = field(default_factory=list)
    optional_fields: List[str] = field(default_factory=list)
    field_types: Dict[str, str] = field(default_factory=dict)
    aliases: Dict[str, str] = field(default_factory=dict)
    primary_key: List[str] = field(default_factory=list)
    date_fields: List[str] = field(default_factory=list)
    timestamp_fields: List[str] = field(default_factory=list)
    unit_fields: Dict[str, str] = field(default_factory=dict)
    currency_fields: List[str] = field(default_factory=list)
    allowed_values: Dict[str, List[Any]] = field(default_factory=dict)
    missing_value_tokens: List[str] = field(default_factory=list)
    normalization_rules: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    point_in_time_rules: Dict[str, Any] = field(default_factory=dict)
    authoritative_fields: List[str] = field(default_factory=list)
    contract_hash: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def compute_hash(self) -> str:
        """Compute a deterministic hash of this contract's key fields."""
        payload = json.dumps({
            "schema_id": self.schema_id,
            "dataset_id": self.dataset_id,
            "version": self.version,
            "required_fields": sorted(self.required_fields),
            "field_types": dict(sorted(self.field_types.items())),
            "primary_key": sorted(self.primary_key),
        }, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "dataset_id": self.dataset_id,
            "version": self.version,
            "expected_format": self.expected_format,
            "required_fields": list(self.required_fields),
            "optional_fields": list(self.optional_fields),
            "field_types": dict(self.field_types),
            "aliases": dict(self.aliases),
            "primary_key": list(self.primary_key),
            "date_fields": list(self.date_fields),
            "timestamp_fields": list(self.timestamp_fields),
            "unit_fields": dict(self.unit_fields),
            "currency_fields": list(self.currency_fields),
            "allowed_values": {k: list(v) for k, v in self.allowed_values.items()},
            "missing_value_tokens": list(self.missing_value_tokens),
            "normalization_rules": dict(self.normalization_rules),
            "validation_rules": dict(self.validation_rules),
            "point_in_time_rules": dict(self.point_in_time_rules),
            "authoritative_fields": list(self.authoritative_fields),
            "contract_hash": self.contract_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataGovTwSchemaContract":
        return cls(
            schema_id=d.get("schema_id", ""),
            dataset_id=d.get("dataset_id", ""),
            version=d.get("version", "1.0"),
            expected_format=d.get("expected_format"),
            required_fields=_safe_list(d.get("required_fields")),
            optional_fields=_safe_list(d.get("optional_fields")),
            field_types=_safe_dict(d.get("field_types")),
            aliases=_safe_dict(d.get("aliases")),
            primary_key=_safe_list(d.get("primary_key")),
            date_fields=_safe_list(d.get("date_fields")),
            timestamp_fields=_safe_list(d.get("timestamp_fields")),
            unit_fields=_safe_dict(d.get("unit_fields")),
            currency_fields=_safe_list(d.get("currency_fields")),
            allowed_values=_safe_dict(d.get("allowed_values")),
            missing_value_tokens=_safe_list(d.get("missing_value_tokens")),
            normalization_rules=_safe_dict(d.get("normalization_rules")),
            validation_rules=_safe_dict(d.get("validation_rules")),
            point_in_time_rules=_safe_dict(d.get("point_in_time_rules")),
            authoritative_fields=_safe_list(d.get("authoritative_fields")),
            contract_hash=d.get("contract_hash"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            metadata=_safe_dict(d.get("metadata")),
        )


# ---------------------------------------------------------------------------
# DataGovTwDatasetRevision
# ---------------------------------------------------------------------------

@dataclass
class DataGovTwDatasetRevision:
    """Tracks changes detected in a dataset or resource."""
    revision_id: str
    dataset_id: str
    resource_id: Optional[str] = None
    detected_at: Optional[str] = None
    source_updated_at: Optional[str] = None
    old_content_hash: Optional[str] = None
    new_content_hash: Optional[str] = None
    metadata_changed: bool = False
    schema_changed: bool = False
    resource_changed: bool = False
    update_frequency_changed: bool = False
    license_changed: bool = False
    changed_fields: List[str] = field(default_factory=list)
    severity: str = "INFO"
    review_required: bool = False
    supersedes_revision_id: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "revision_id": self.revision_id,
            "dataset_id": self.dataset_id,
            "resource_id": self.resource_id,
            "detected_at": self.detected_at,
            "source_updated_at": self.source_updated_at,
            "old_content_hash": self.old_content_hash,
            "new_content_hash": self.new_content_hash,
            "metadata_changed": self.metadata_changed,
            "schema_changed": self.schema_changed,
            "resource_changed": self.resource_changed,
            "update_frequency_changed": self.update_frequency_changed,
            "license_changed": self.license_changed,
            "changed_fields": list(self.changed_fields),
            "severity": self.severity,
            "review_required": self.review_required,
            "supersedes_revision_id": self.supersedes_revision_id,
            "provenance": dict(self.provenance),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataGovTwDatasetRevision":
        return cls(
            revision_id=d.get("revision_id", ""),
            dataset_id=d.get("dataset_id", ""),
            resource_id=d.get("resource_id"),
            detected_at=d.get("detected_at"),
            source_updated_at=d.get("source_updated_at"),
            old_content_hash=d.get("old_content_hash"),
            new_content_hash=d.get("new_content_hash"),
            metadata_changed=bool(d.get("metadata_changed", False)),
            schema_changed=bool(d.get("schema_changed", False)),
            resource_changed=bool(d.get("resource_changed", False)),
            update_frequency_changed=bool(d.get("update_frequency_changed", False)),
            license_changed=bool(d.get("license_changed", False)),
            changed_fields=_safe_list(d.get("changed_fields")),
            severity=d.get("severity", "INFO"),
            review_required=bool(d.get("review_required", False)),
            supersedes_revision_id=d.get("supersedes_revision_id"),
            provenance=_safe_dict(d.get("provenance")),
            metadata=_safe_dict(d.get("metadata")),
        )


# ---------------------------------------------------------------------------
# DataGovTwRecord
# ---------------------------------------------------------------------------

@dataclass
class DataGovTwRecord:
    """A single normalized data record from a data.gov.tw dataset."""
    dataset_id: str
    resource_id: str
    record_id: Optional[str] = None
    schema_id: Optional[str] = None
    reporting_period: Optional[str] = None
    observation_date: Optional[str] = None
    published_at: Optional[str] = None
    available_from: Optional[str] = None
    values: Dict[str, Any] = field(default_factory=dict)
    unit: Optional[str] = None
    currency: Optional[str] = None
    source_timestamp: Optional[str] = None
    fetched_at: Optional[str] = None
    revision_id: Optional[str] = None
    content_hash: Optional[str] = None
    quality_status: str = QualityStatus.REVIEW_REQUIRED.value
    freshness_status: str = FreshnessStatus.UNKNOWN.value
    formal_use_allowed: bool = False
    provenance: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "resource_id": self.resource_id,
            "record_id": self.record_id,
            "schema_id": self.schema_id,
            "reporting_period": self.reporting_period,
            "observation_date": self.observation_date,
            "published_at": self.published_at,
            "available_from": self.available_from,
            "values": dict(self.values),
            "unit": self.unit,
            "currency": self.currency,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "revision_id": self.revision_id,
            "content_hash": self.content_hash,
            "quality_status": self.quality_status,
            "freshness_status": self.freshness_status,
            "formal_use_allowed": self.formal_use_allowed,
            "provenance": dict(self.provenance),
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataGovTwRecord":
        return cls(
            dataset_id=d.get("dataset_id", ""),
            resource_id=d.get("resource_id", ""),
            record_id=d.get("record_id"),
            schema_id=d.get("schema_id"),
            reporting_period=d.get("reporting_period"),
            observation_date=d.get("observation_date"),
            published_at=d.get("published_at"),
            available_from=d.get("available_from"),
            values=_safe_dict(d.get("values")),
            unit=d.get("unit"),
            currency=d.get("currency"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at"),
            revision_id=d.get("revision_id"),
            content_hash=d.get("content_hash"),
            quality_status=d.get("quality_status", QualityStatus.REVIEW_REQUIRED.value),
            freshness_status=d.get("freshness_status", FreshnessStatus.UNKNOWN.value),
            formal_use_allowed=bool(d.get("formal_use_allowed", False)),
            provenance=_safe_dict(d.get("provenance")),
            warnings=_safe_list(d.get("warnings")),
            metadata=_safe_dict(d.get("metadata")),
        )


# ---------------------------------------------------------------------------
# DataGovTwFetchRun
# ---------------------------------------------------------------------------

@dataclass
class DataGovTwFetchRun:
    """Audit record for a single fetch operation."""
    run_id: str
    dataset_id: str
    resource_id: Optional[str] = None
    mode: str = "real"
    dry_run: bool = True
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    records_received: Optional[int] = None
    records_valid: Optional[int] = None
    records_rejected: Optional[int] = None
    cache_hit: bool = False
    rate_limited: bool = False
    blocked: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    database_updated: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "dataset_id": self.dataset_id,
            "resource_id": self.resource_id,
            "mode": self.mode,
            "dry_run": self.dry_run,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "records_received": self.records_received,
            "records_valid": self.records_valid,
            "records_rejected": self.records_rejected,
            "cache_hit": self.cache_hit,
            "rate_limited": self.rate_limited,
            "blocked": self.blocked,
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "database_updated": self.database_updated,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataGovTwFetchRun":
        return cls(
            run_id=d.get("run_id", ""),
            dataset_id=d.get("dataset_id", ""),
            resource_id=d.get("resource_id"),
            mode=d.get("mode", "real"),
            dry_run=bool(d.get("dry_run", True)),
            started_at=d.get("started_at"),
            finished_at=d.get("finished_at"),
            records_received=d.get("records_received"),
            records_valid=d.get("records_valid"),
            records_rejected=d.get("records_rejected"),
            cache_hit=bool(d.get("cache_hit", False)),
            rate_limited=bool(d.get("rate_limited", False)),
            blocked=bool(d.get("blocked", False)),
            warnings=_safe_list(d.get("warnings")),
            errors=_safe_list(d.get("errors")),
            database_updated=bool(d.get("database_updated", False)),
            metadata=_safe_dict(d.get("metadata")),
        )


# ---------------------------------------------------------------------------
# GovernmentObservation
# ---------------------------------------------------------------------------

@dataclass
class GovernmentObservation:
    """
    Standardized research observation from government open data.
    Applies to macro, trade, industry, energy, labor, price index domains.
    NOT for all datasets — domain-specific schema used when contract doesn't fit.
    """
    domain: str
    indicator_code: str
    indicator_name: Optional[str] = None
    observation_date: Optional[str] = None
    reporting_period: Optional[str] = None
    value: Optional[Any] = None
    unit: Optional[str] = None
    currency: Optional[str] = None
    geography: Optional[str] = None
    industry_code: Optional[str] = None
    category: Optional[str] = None
    published_at: Optional[str] = None
    available_from: Optional[str] = None
    revision: Optional[str] = None
    dataset_id: Optional[str] = None
    resource_id: Optional[str] = None
    provider_agency: Optional[str] = None
    authoritative_level: str = AuthoritativeLevel.SECONDARY_OFFICIAL.value
    quality_status: str = QualityStatus.REVIEW_REQUIRED.value
    freshness_status: str = FreshnessStatus.UNKNOWN.value
    formal_use_allowed: bool = False
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "indicator_code": self.indicator_code,
            "indicator_name": self.indicator_name,
            "observation_date": self.observation_date,
            "reporting_period": self.reporting_period,
            "value": self.value,
            "unit": self.unit,
            "currency": self.currency,
            "geography": self.geography,
            "industry_code": self.industry_code,
            "category": self.category,
            "published_at": self.published_at,
            "available_from": self.available_from,
            "revision": self.revision,
            "dataset_id": self.dataset_id,
            "resource_id": self.resource_id,
            "provider_agency": self.provider_agency,
            "authoritative_level": self.authoritative_level,
            "quality_status": self.quality_status,
            "freshness_status": self.freshness_status,
            "formal_use_allowed": self.formal_use_allowed,
            "provenance": dict(self.provenance),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GovernmentObservation":
        return cls(
            domain=d.get("domain", ""),
            indicator_code=d.get("indicator_code", ""),
            indicator_name=d.get("indicator_name"),
            observation_date=d.get("observation_date"),
            reporting_period=d.get("reporting_period"),
            value=d.get("value"),
            unit=d.get("unit"),
            currency=d.get("currency"),
            geography=d.get("geography"),
            industry_code=d.get("industry_code"),
            category=d.get("category"),
            published_at=d.get("published_at"),
            available_from=d.get("available_from"),
            revision=d.get("revision"),
            dataset_id=d.get("dataset_id"),
            resource_id=d.get("resource_id"),
            provider_agency=d.get("provider_agency"),
            authoritative_level=d.get("authoritative_level", AuthoritativeLevel.SECONDARY_OFFICIAL.value),
            quality_status=d.get("quality_status", QualityStatus.REVIEW_REQUIRED.value),
            freshness_status=d.get("freshness_status", FreshnessStatus.UNKNOWN.value),
            formal_use_allowed=bool(d.get("formal_use_allowed", False)),
            provenance=_safe_dict(d.get("provenance")),
            metadata=_safe_dict(d.get("metadata")),
        )
