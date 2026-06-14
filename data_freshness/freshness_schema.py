"""
data_freshness/freshness_schema.py — Freshness schema dataclasses for v1.1.3.
[!] Research Only. No Real Orders.
[!] future_date does not count as fresh.
[!] mock data not used for formal freshness conclusions.
"""
from __future__ import annotations
from dataclasses import dataclass, field as dc_field
from datetime import datetime
from typing import Any, Dict, List, Optional

# Dataset constants
DATASET_DAILY_PRICE      = "DAILY_PRICE"
DATASET_VOLUME           = "VOLUME"
DATASET_CHIPS            = "CHIPS"
DATASET_REVENUE          = "REVENUE"
DATASET_FUNDAMENTALS     = "FUNDAMENTALS"
DATASET_MARGIN           = "MARGIN"
DATASET_SHORT_INTEREST   = "SHORT_INTEREST"
DATASET_CORPORATE_ACTION = "CORPORATE_ACTION"
DATASET_UNKNOWN          = "UNKNOWN"

ALL_DATASETS = [
    DATASET_DAILY_PRICE, DATASET_VOLUME, DATASET_CHIPS,
    DATASET_REVENUE, DATASET_FUNDAMENTALS, DATASET_MARGIN,
    DATASET_SHORT_INTEREST, DATASET_CORPORATE_ACTION, DATASET_UNKNOWN,
]

# Status constants
STATUS_FRESH           = "FRESH"
STATUS_ACCEPTABLE      = "ACCEPTABLE"
STATUS_DELAYED         = "DELAYED"
STATUS_STALE           = "STALE"
STATUS_INTERRUPTED     = "INTERRUPTED"
STATUS_MISSING         = "MISSING"
STATUS_FUTURE_DATE     = "FUTURE_DATE"
STATUS_DATE_REGRESSION = "DATE_REGRESSION"
STATUS_UNKNOWN         = "UNKNOWN"

ALL_STATUSES = [
    STATUS_FRESH, STATUS_ACCEPTABLE, STATUS_DELAYED, STATUS_STALE,
    STATUS_INTERRUPTED, STATUS_MISSING, STATUS_FUTURE_DATE,
    STATUS_DATE_REGRESSION, STATUS_UNKNOWN,
]

# Severity constants
SEVERITY_INFO     = "INFO"
SEVERITY_LOW      = "LOW"
SEVERITY_MEDIUM   = "MEDIUM"
SEVERITY_HIGH     = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"

# Source status constants
SOURCE_STATUS_HEALTHY     = "HEALTHY"
SOURCE_STATUS_DEGRADED    = "DEGRADED"
SOURCE_STATUS_INTERRUPTED = "INTERRUPTED"
SOURCE_STATUS_UNKNOWN     = "UNKNOWN"

# Alert type constants
ALERT_DATA_DELAY             = "DATA_DELAY"
ALERT_DATA_STALE             = "DATA_STALE"
ALERT_SOURCE_INTERRUPTION    = "SOURCE_INTERRUPTION"
ALERT_DATA_MISSING           = "DATA_MISSING"
ALERT_FUTURE_DATE            = "FUTURE_DATE"
ALERT_DATE_REGRESSION        = "DATE_REGRESSION"
ALERT_PARTIAL_UPDATE         = "PARTIAL_UPDATE"
ALERT_COVERAGE_NOT_REFRESHED = "COVERAGE_NOT_REFRESHED"
ALERT_SLA_VIOLATION          = "SLA_VIOLATION"

# Alert status constants
ALERT_STATUS_OPEN         = "OPEN"
ALERT_STATUS_ACKNOWLEDGED = "ACKNOWLEDGED"
ALERT_STATUS_RESOLVED     = "RESOLVED"
ALERT_STATUS_SUPPRESSED   = "SUPPRESSED"
ALERT_STATUS_BLOCKED      = "BLOCKED"


@dataclass
class DatasetFreshnessRecord:
    record_id:                str
    symbol:                   str
    tier:                     str
    dataset:                  str
    source:                   str
    expected_latest_date:     Optional[str]
    actual_latest_date:       Optional[str]
    previous_latest_date:     Optional[str]
    calendar_age_days:        Optional[int]
    trading_day_lag:          Optional[int]
    row_count:                int
    latest_row_valid:         bool
    future_date_detected:     bool
    date_regression_detected: bool
    status:                   str
    severity:                 str
    sla_name:                 str
    sla_limit:                Optional[int]
    detected_at:              str
    reason:                   str
    research_only:            bool = True
    no_real_orders:           bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "symbol": self.symbol,
            "tier": self.tier,
            "dataset": self.dataset,
            "source": self.source,
            "expected_latest_date": self.expected_latest_date,
            "actual_latest_date": self.actual_latest_date,
            "previous_latest_date": self.previous_latest_date,
            "calendar_age_days": self.calendar_age_days,
            "trading_day_lag": self.trading_day_lag,
            "row_count": self.row_count,
            "latest_row_valid": self.latest_row_valid,
            "future_date_detected": self.future_date_detected,
            "date_regression_detected": self.date_regression_detected,
            "status": self.status,
            "severity": self.severity,
            "sla_name": self.sla_name,
            "sla_limit": self.sla_limit,
            "detected_at": self.detected_at,
            "reason": self.reason,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DatasetFreshnessRecord":
        return cls(
            record_id=d.get("record_id", ""),
            symbol=d.get("symbol", ""),
            tier=d.get("tier", ""),
            dataset=d.get("dataset", DATASET_UNKNOWN),
            source=d.get("source", "UNKNOWN"),
            expected_latest_date=d.get("expected_latest_date"),
            actual_latest_date=d.get("actual_latest_date"),
            previous_latest_date=d.get("previous_latest_date"),
            calendar_age_days=d.get("calendar_age_days"),
            trading_day_lag=d.get("trading_day_lag"),
            row_count=d.get("row_count", 0),
            latest_row_valid=d.get("latest_row_valid", True),
            future_date_detected=d.get("future_date_detected", False),
            date_regression_detected=d.get("date_regression_detected", False),
            status=d.get("status", STATUS_UNKNOWN),
            severity=d.get("severity", SEVERITY_INFO),
            sla_name=d.get("sla_name", ""),
            sla_limit=d.get("sla_limit"),
            detected_at=d.get("detected_at", ""),
            reason=d.get("reason", ""),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class SourceFreshnessStatus:
    source_id:               str
    source_name:             str
    dataset:                 str
    symbols_expected:        int
    symbols_fresh:           int
    symbols_delayed:         int
    symbols_stale:           int
    symbols_missing:         int
    latest_seen_at:          Optional[str]
    interruption_suspected:  bool
    interruption_started_at: Optional[str]
    status:                  str
    severity:                str
    reason:                  str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "dataset": self.dataset,
            "symbols_expected": self.symbols_expected,
            "symbols_fresh": self.symbols_fresh,
            "symbols_delayed": self.symbols_delayed,
            "symbols_stale": self.symbols_stale,
            "symbols_missing": self.symbols_missing,
            "latest_seen_at": self.latest_seen_at,
            "interruption_suspected": self.interruption_suspected,
            "interruption_started_at": self.interruption_started_at,
            "status": self.status,
            "severity": self.severity,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SourceFreshnessStatus":
        return cls(
            source_id=d.get("source_id", ""),
            source_name=d.get("source_name", ""),
            dataset=d.get("dataset", DATASET_UNKNOWN),
            symbols_expected=d.get("symbols_expected", 0),
            symbols_fresh=d.get("symbols_fresh", 0),
            symbols_delayed=d.get("symbols_delayed", 0),
            symbols_stale=d.get("symbols_stale", 0),
            symbols_missing=d.get("symbols_missing", 0),
            latest_seen_at=d.get("latest_seen_at"),
            interruption_suspected=d.get("interruption_suspected", False),
            interruption_started_at=d.get("interruption_started_at"),
            status=d.get("status", SOURCE_STATUS_UNKNOWN),
            severity=d.get("severity", SEVERITY_INFO),
            reason=d.get("reason", ""),
        )


@dataclass
class FreshnessAlert:
    alert_id:          str
    symbol:            str
    dataset:           str
    source:            str
    alert_type:        str
    severity:          str
    status:            str
    message:           str
    first_detected_at: str
    last_detected_at:  str
    occurrence_count:  int
    repair_issue_id:   Optional[str]
    acknowledged:      bool
    research_only:     bool = True
    no_real_orders:    bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "symbol": self.symbol,
            "dataset": self.dataset,
            "source": self.source,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "status": self.status,
            "message": self.message,
            "first_detected_at": self.first_detected_at,
            "last_detected_at": self.last_detected_at,
            "occurrence_count": self.occurrence_count,
            "repair_issue_id": self.repair_issue_id,
            "acknowledged": self.acknowledged,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FreshnessAlert":
        return cls(
            alert_id=d.get("alert_id", ""),
            symbol=d.get("symbol", ""),
            dataset=d.get("dataset", DATASET_UNKNOWN),
            source=d.get("source", "UNKNOWN"),
            alert_type=d.get("alert_type", ALERT_DATA_MISSING),
            severity=d.get("severity", SEVERITY_INFO),
            status=d.get("status", ALERT_STATUS_OPEN),
            message=d.get("message", ""),
            first_detected_at=d.get("first_detected_at", ""),
            last_detected_at=d.get("last_detected_at", ""),
            occurrence_count=d.get("occurrence_count", 1),
            repair_issue_id=d.get("repair_issue_id"),
            acknowledged=d.get("acknowledged", False),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class FreshnessSummary:
    generated_at:     str
    tier:             str
    symbols:          List[str]          = dc_field(default_factory=list)
    datasets:         List[str]          = dc_field(default_factory=list)
    fresh_count:      int                = 0
    acceptable_count: int                = 0
    delayed_count:    int                = 0
    stale_count:      int                = 0
    interrupted_count: int               = 0
    missing_count:    int                = 0
    critical_count:   int                = 0
    source_health:    Dict[str, Any]     = dc_field(default_factory=dict)
    overall_status:   str                = STATUS_UNKNOWN
    confidence:       str                = "LOW"
    research_only:    bool               = True
    no_real_orders:   bool               = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "tier": self.tier,
            "symbols": self.symbols,
            "datasets": self.datasets,
            "fresh_count": self.fresh_count,
            "acceptable_count": self.acceptable_count,
            "delayed_count": self.delayed_count,
            "stale_count": self.stale_count,
            "interrupted_count": self.interrupted_count,
            "missing_count": self.missing_count,
            "critical_count": self.critical_count,
            "source_health": self.source_health,
            "overall_status": self.overall_status,
            "confidence": self.confidence,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FreshnessSummary":
        obj = cls(
            generated_at=d.get("generated_at", ""),
            tier=d.get("tier", ""),
        )
        obj.symbols = d.get("symbols", [])
        obj.datasets = d.get("datasets", [])
        obj.fresh_count = d.get("fresh_count", 0)
        obj.acceptable_count = d.get("acceptable_count", 0)
        obj.delayed_count = d.get("delayed_count", 0)
        obj.stale_count = d.get("stale_count", 0)
        obj.interrupted_count = d.get("interrupted_count", 0)
        obj.missing_count = d.get("missing_count", 0)
        obj.critical_count = d.get("critical_count", 0)
        obj.source_health = d.get("source_health", {})
        obj.overall_status = d.get("overall_status", STATUS_UNKNOWN)
        obj.confidence = d.get("confidence", "LOW")
        obj.research_only = d.get("research_only", True)
        obj.no_real_orders = d.get("no_real_orders", True)
        return obj
