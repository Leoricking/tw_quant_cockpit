"""
portfolio/correlation/enums_v152.py — Correlation & Exposure Enums v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import enum

RESEARCH_ONLY = True
ENUMS_VERSION = "1.5.2"


class CorrelationMethod(str, enum.Enum):
    """Method used to compute the correlation matrix."""
    PEARSON  = "PEARSON"
    SPEARMAN = "SPEARMAN"


class ReturnMethod(str, enum.Enum):
    """How returns are computed from prices."""
    SIMPLE = "SIMPLE"
    LOG    = "LOG"


class AlignmentMethod(str, enum.Enum):
    """How multi-symbol return series are date-aligned."""
    INNER_JOIN         = "INNER_JOIN"
    PAIRWISE_COMPLETE  = "PAIRWISE_COMPLETE"


class CorrelationStatus(str, enum.Enum):
    """Quality/completeness status of a correlation result."""
    VALID               = "VALID"
    PARTIAL             = "PARTIAL"
    INSUFFICIENT_SAMPLE = "INSUFFICIENT_SAMPLE"
    STALE               = "STALE"
    BLOCKED             = "BLOCKED"
    UNKNOWN             = "UNKNOWN"


class ExposureType(str, enum.Enum):
    """Category of an exposure bucket."""
    SYMBOL        = "SYMBOL"
    INDUSTRY      = "INDUSTRY"
    THEME         = "THEME"
    MARKET        = "MARKET"
    ASSET_CLASS   = "ASSET_CLASS"
    BENCHMARK     = "BENCHMARK"
    ETF_COMPONENT = "ETF_COMPONENT"


class ConcentrationRiskLevel(str, enum.Enum):
    """Risk level assigned to a hidden-concentration result."""
    LOW      = "LOW"
    MODERATE = "MODERATE"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN  = "UNKNOWN"


class ClusterMethod(str, enum.Enum):
    """Algorithm used to build correlation clusters."""
    THRESHOLD_GRAPH = "THRESHOLD_GRAPH"
    HIERARCHICAL    = "HIERARCHICAL"


class RiskContributionType(str, enum.Enum):
    """Which risk-contribution decomposition is used."""
    MARGINAL   = "MARGINAL"
    COMPONENT  = "COMPONENT"
    PERCENTAGE = "PERCENTAGE"
