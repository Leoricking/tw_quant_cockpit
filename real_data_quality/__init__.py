"""
real_data_quality/__init__.py — Real Data Quality Foundation v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] Mock fallback DISABLED. Real mode does not substitute mock data.
[!] BLOCKED status: no precise prices, no formal buy recommendations.
[!] UNAVAILABLE: returns REAL DATA UNAVAILABLE. No mock fallback.
[!] Data quality score 0-100. CRITICAL issue caps score at 49.
"""
from __future__ import annotations

# Safety constants
NO_REAL_ORDERS = True
BROKER_DISABLED = True
MOCK_FALLBACK_ENABLED = False

# Re-export key public symbols from submodules
from real_data_quality.dq_schema import (
    # DataMode constants
    DataMode,
    DATA_MODE_REAL,
    DATA_MODE_MOCK,
    DATA_MODE_UNAVAILABLE,
    # DataQualityStatus constants
    DataQualityStatus,
    DQ_STATUS_PASS,
    DQ_STATUS_DEGRADED,
    DQ_STATUS_BLOCKED,
    DQ_STATUS_UNAVAILABLE,
    # DataQualityIssueSeverity constants
    DataQualityIssueSeverity,
    SEVERITY_INFO,
    SEVERITY_WARNING,
    SEVERITY_ERROR,
    SEVERITY_CRITICAL,
    # Dataclasses
    DataQualityIssue,
    DataQualityReport,
    DataProvenanceRecord,
)
from real_data_quality.dq_validator import DataQualityValidator
from real_data_quality.dq_profiles import DataCompletenessGate, CompletenessProfile
from real_data_quality.dq_scorer import DataQualityScorer
from real_data_quality.dq_health import RealDataQualityHealth
from real_data_quality.dq_report import (
    format_quality_report_text,
    format_quality_summary_for_stock_report,
    make_blocked_output,
    make_unavailable_output,
)

__all__ = [
    # Safety
    "NO_REAL_ORDERS",
    "BROKER_DISABLED",
    "MOCK_FALLBACK_ENABLED",
    # DataMode
    "DataMode",
    "DATA_MODE_REAL",
    "DATA_MODE_MOCK",
    "DATA_MODE_UNAVAILABLE",
    # DataQualityStatus
    "DataQualityStatus",
    "DQ_STATUS_PASS",
    "DQ_STATUS_DEGRADED",
    "DQ_STATUS_BLOCKED",
    "DQ_STATUS_UNAVAILABLE",
    # DataQualityIssueSeverity
    "DataQualityIssueSeverity",
    "SEVERITY_INFO",
    "SEVERITY_WARNING",
    "SEVERITY_ERROR",
    "SEVERITY_CRITICAL",
    # Dataclasses
    "DataQualityIssue",
    "DataQualityReport",
    "DataProvenanceRecord",
    # Classes
    "DataQualityValidator",
    "DataCompletenessGate",
    "CompletenessProfile",
    "DataQualityScorer",
    "RealDataQualityHealth",
    # Report functions
    "format_quality_report_text",
    "format_quality_summary_for_stock_report",
    "make_blocked_output",
    "make_unavailable_output",
]
