"""
real_data_quality/dq_schema.py — Formal models for Real Data Quality Foundation v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] Mock fallback DISABLED. Real mode does not substitute mock data.
[!] BLOCKED: no precise prices. UNAVAILABLE: no mock fallback.
"""
from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Dict, List

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_DISABLED = True
MOCK_FALLBACK_ENABLED = False  # ALWAYS FALSE


# ---------------------------------------------------------------------------
# DataMode constants (string constants, not Enum — matches existing project style)
# ---------------------------------------------------------------------------
class DataMode:
    """Data mode constants. MOCK always displayed with DEMO_ONLY label."""
    REAL = "REAL"
    MOCK = "MOCK"               # Always displayed with DEMO_ONLY label
    UNAVAILABLE = "UNAVAILABLE"


# Module-level aliases for easy import
DATA_MODE_REAL = DataMode.REAL
DATA_MODE_MOCK = DataMode.MOCK
DATA_MODE_UNAVAILABLE = DataMode.UNAVAILABLE


# ---------------------------------------------------------------------------
# DataQualityStatus constants
# ---------------------------------------------------------------------------
class DataQualityStatus:
    """Quality gate status constants."""
    PASS = "PASS"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"


DQ_STATUS_PASS = DataQualityStatus.PASS
DQ_STATUS_DEGRADED = DataQualityStatus.DEGRADED
DQ_STATUS_BLOCKED = DataQualityStatus.BLOCKED
DQ_STATUS_UNAVAILABLE = DataQualityStatus.UNAVAILABLE


# ---------------------------------------------------------------------------
# DataQualityIssueSeverity constants
# ---------------------------------------------------------------------------
class DataQualityIssueSeverity:
    """Issue severity constants."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


SEVERITY_INFO = DataQualityIssueSeverity.INFO
SEVERITY_WARNING = DataQualityIssueSeverity.WARNING
SEVERITY_ERROR = DataQualityIssueSeverity.ERROR
SEVERITY_CRITICAL = DataQualityIssueSeverity.CRITICAL


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# DataQualityIssue dataclass
# ---------------------------------------------------------------------------
@dataclass
class DataQualityIssue:
    """Describes a single data quality issue detected during validation."""

    code: str
    severity: str                # One of DataQualityIssueSeverity constants
    field: str
    message: str
    source: str
    observed_at: str             # ISO timestamp
    expected_rule: str
    actual_value: str
    blocks_analysis: bool

    def __post_init__(self):
        if not self.observed_at:
            self.observed_at = _now_iso()

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "severity": self.severity,
            "field": self.field,
            "message": self.message,
            "source": self.source,
            "observed_at": self.observed_at,
            "expected_rule": self.expected_rule,
            "actual_value": self.actual_value,
            "blocks_analysis": self.blocks_analysis,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DataQualityIssue":
        return cls(
            code=d.get("code", ""),
            severity=d.get("severity", DataQualityIssueSeverity.INFO),
            field=d.get("field", ""),
            message=d.get("message", ""),
            source=d.get("source", ""),
            observed_at=d.get("observed_at", ""),
            expected_rule=d.get("expected_rule", ""),
            actual_value=d.get("actual_value", ""),
            blocks_analysis=bool(d.get("blocks_analysis", False)),
        )


# ---------------------------------------------------------------------------
# DataQualityReport dataclass
# ---------------------------------------------------------------------------
@dataclass
class DataQualityReport:
    """Full data quality report for a symbol at a point in time."""

    symbol: str
    market: str
    data_mode: str                          # DataMode constant
    status: str                             # DataQualityStatus constant
    score: int                              # 0-100
    checked_at: str                         # ISO timestamp
    source_names: List[str] = dc_field(default_factory=list)
    latest_market_timestamp: str = ""
    missing_fields: List[str] = dc_field(default_factory=list)
    stale_fields: List[str] = dc_field(default_factory=list)
    invalid_fields: List[str] = dc_field(default_factory=list)
    inconsistent_fields: List[str] = dc_field(default_factory=list)
    issues: List[DataQualityIssue] = dc_field(default_factory=list)
    blocking_reasons: List[str] = dc_field(default_factory=list)
    warnings: List[str] = dc_field(default_factory=list)
    can_generate_analysis: bool = False
    can_generate_precise_prices: bool = False
    can_run_backtest: bool = False
    metadata: dict = dc_field(default_factory=dict)

    # Safety constants — always enforced
    NO_REAL_ORDERS: bool = dc_field(default=True, repr=False)
    MOCK_FALLBACK_ENABLED: bool = dc_field(default=False, repr=False)

    def __post_init__(self):
        if not self.checked_at:
            self.checked_at = _now_iso()
        # Enforce safety — never allow mock fallback
        object.__setattr__(self, "NO_REAL_ORDERS", True)
        object.__setattr__(self, "MOCK_FALLBACK_ENABLED", False)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "market": self.market,
            "data_mode": self.data_mode,
            "status": self.status,
            "score": self.score,
            "checked_at": self.checked_at,
            "source_names": list(self.source_names),
            "latest_market_timestamp": self.latest_market_timestamp,
            "missing_fields": list(self.missing_fields),
            "stale_fields": list(self.stale_fields),
            "invalid_fields": list(self.invalid_fields),
            "inconsistent_fields": list(self.inconsistent_fields),
            "issues": [iss.to_dict() for iss in self.issues],
            "blocking_reasons": list(self.blocking_reasons),
            "warnings": list(self.warnings),
            "can_generate_analysis": self.can_generate_analysis,
            "can_generate_precise_prices": self.can_generate_precise_prices,
            "can_run_backtest": self.can_run_backtest,
            "metadata": dict(self.metadata),
            "NO_REAL_ORDERS": True,
            "MOCK_FALLBACK_ENABLED": False,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DataQualityReport":
        raw_issues = d.get("issues", [])
        issues = []
        for iss in raw_issues:
            if isinstance(iss, dict):
                issues.append(DataQualityIssue.from_dict(iss))
            elif isinstance(iss, DataQualityIssue):
                issues.append(iss)
        return cls(
            symbol=d.get("symbol", ""),
            market=d.get("market", ""),
            data_mode=d.get("data_mode", DataMode.UNAVAILABLE),
            status=d.get("status", DataQualityStatus.UNAVAILABLE),
            score=int(d.get("score", 0)),
            checked_at=d.get("checked_at", ""),
            source_names=list(d.get("source_names", [])),
            latest_market_timestamp=d.get("latest_market_timestamp", ""),
            missing_fields=list(d.get("missing_fields", [])),
            stale_fields=list(d.get("stale_fields", [])),
            invalid_fields=list(d.get("invalid_fields", [])),
            inconsistent_fields=list(d.get("inconsistent_fields", [])),
            issues=issues,
            blocking_reasons=list(d.get("blocking_reasons", [])),
            warnings=list(d.get("warnings", [])),
            can_generate_analysis=bool(d.get("can_generate_analysis", False)),
            can_generate_precise_prices=bool(d.get("can_generate_precise_prices", False)),
            can_run_backtest=bool(d.get("can_run_backtest", False)),
            metadata=dict(d.get("metadata", {})),
        )


# ---------------------------------------------------------------------------
# DataProvenanceRecord dataclass
# ---------------------------------------------------------------------------
@dataclass
class DataProvenanceRecord:
    """Tracks provenance (origin and transformation) of a data fetch."""

    provider: str
    source_type: str             # "api", "csv", "db", etc.
    fetched_at: str
    market_timestamp: str
    normalized_at: str
    symbol: str
    market: str
    data_mode: str               # DataMode constant
    schema_version: str
    raw_field_availability: Dict[str, bool] = dc_field(default_factory=dict)
    transformation_notes: str = ""

    def __post_init__(self):
        if not self.fetched_at:
            self.fetched_at = _now_iso()
        if not self.normalized_at:
            self.normalized_at = _now_iso()

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "source_type": self.source_type,
            "fetched_at": self.fetched_at,
            "market_timestamp": self.market_timestamp,
            "normalized_at": self.normalized_at,
            "symbol": self.symbol,
            "market": self.market,
            "data_mode": self.data_mode,
            "schema_version": self.schema_version,
            "raw_field_availability": dict(self.raw_field_availability),
            "transformation_notes": self.transformation_notes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DataProvenanceRecord":
        return cls(
            provider=d.get("provider", ""),
            source_type=d.get("source_type", ""),
            fetched_at=d.get("fetched_at", ""),
            market_timestamp=d.get("market_timestamp", ""),
            normalized_at=d.get("normalized_at", ""),
            symbol=d.get("symbol", ""),
            market=d.get("market", ""),
            data_mode=d.get("data_mode", DataMode.UNAVAILABLE),
            schema_version=d.get("schema_version", "1.3.0"),
            raw_field_availability=dict(d.get("raw_field_availability", {})),
            transformation_notes=d.get("transformation_notes", ""),
        )
