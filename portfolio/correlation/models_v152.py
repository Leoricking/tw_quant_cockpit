"""
portfolio/correlation/models_v152.py — Correlation & Exposure Dataclass Models v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from portfolio.correlation.enums_v152 import (
    AlignmentMethod,
    ClusterMethod,
    ConcentrationRiskLevel,
    CorrelationMethod,
    CorrelationStatus,
    ExposureType,
    ReturnMethod,
)

RESEARCH_ONLY  = True
MODELS_VERSION = "1.5.2"

_RESULT_LABELS = [
    "RESEARCH_ONLY",
    "DESCRIPTIVE_ANALYTICS_ONLY",
    "NOT_AN_OPTIMIZATION",
    "NOT_A_REBALANCE_INSTRUCTION",
    "NOT_AN_ORDER",
    "NO_BROKER_CALL",
    "NO_LEDGER_WRITE",
]


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------

@dataclass
class CorrelationAnalysisRequest:
    """Input parameters for a correlation & exposure analysis. Research-only."""
    request_id:              str
    portfolio_id:            str
    snapshot_id:             str
    as_of:                   str
    available_from:          str
    symbols:                 List[str]
    weights:                 Dict[str, float]
    lookback_days:           int                = 120
    minimum_observations:    int                = 60
    return_method:           ReturnMethod       = ReturnMethod.SIMPLE
    correlation_method:      CorrelationMethod  = CorrelationMethod.PEARSON
    alignment_method:        AlignmentMethod    = AlignmentMethod.INNER_JOIN
    benchmark_symbol:        Optional[str]      = None
    rolling_windows:         List[int]          = field(default_factory=lambda: [20, 60, 120])
    high_correlation_threshold: float           = 0.75
    cluster_threshold:       float              = 0.75
    source_lineage_ids:      List[str]          = field(default_factory=list)
    research_only:           bool               = True
    metadata:                Dict[str, Any]     = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"


# ---------------------------------------------------------------------------
# Aligned return series
# ---------------------------------------------------------------------------

@dataclass
class AlignedReturnSeries:
    """Date-aligned return series for multiple symbols."""
    symbols:              List[str]
    dates:                List[str]
    returns_by_symbol:    Dict[str, List[float]]
    observation_count:    int
    start_date:           str
    end_date:             str
    missing_by_symbol:    Dict[str, int]          = field(default_factory=dict)
    alignment_method:     AlignmentMethod         = AlignmentMethod.INNER_JOIN
    return_method:        ReturnMethod             = ReturnMethod.SIMPLE
    status:               CorrelationStatus        = CorrelationStatus.VALID
    source_lineage_ids:   List[str]               = field(default_factory=list)
    content_hash:         str                     = ""
    metadata:             Dict[str, Any]           = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Correlation matrix
# ---------------------------------------------------------------------------

@dataclass
class CorrelationMatrixResult:
    """Full correlation matrix result with metadata."""
    matrix_id:              str
    symbols:                List[str]
    matrix:                 List[List[float]]
    observation_counts:     Dict[str, int]
    method:                 CorrelationMethod
    alignment_method:       AlignmentMethod
    lookback_days:          int
    start_date:             str
    end_date:               str
    minimum_observations:   int
    high_correlation_pairs: List[Dict[str, Any]]  = field(default_factory=list)
    invalid_pairs:          List[Dict[str, Any]]  = field(default_factory=list)
    status:                 CorrelationStatus      = CorrelationStatus.VALID
    generated_at:           str                   = ""
    content_hash:           str                   = ""
    source_lineage_ids:     List[str]             = field(default_factory=list)
    metadata:               Dict[str, Any]         = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Covariance matrix
# ---------------------------------------------------------------------------

@dataclass
class CovarianceMatrixResult:
    """Annualised covariance matrix result."""
    symbols:              List[str]
    matrix:               List[List[float]]
    annualization_factor: int                  = 252
    observation_count:    int                  = 0
    status:               CorrelationStatus    = CorrelationStatus.VALID
    source_lineage_ids:   List[str]            = field(default_factory=list)
    content_hash:         str                  = ""
    metadata:             Dict[str, Any]        = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Rolling correlation
# ---------------------------------------------------------------------------

@dataclass
class RollingCorrelationPoint:
    """Single rolling-window correlation observation for a symbol pair."""
    symbol_a:          str
    symbol_b:          str
    window:            int
    as_of:             str
    correlation:       float
    observation_count: int
    status:            CorrelationStatus = CorrelationStatus.VALID
    metadata:          Dict[str, Any]    = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Portfolio variance
# ---------------------------------------------------------------------------

@dataclass
class PortfolioVarianceResult:
    """wᵀΣw decomposition result — descriptive only."""
    portfolio_id:          str
    as_of:                 str
    weights:               Dict[str, float]
    covariance_matrix_id:  str                = ""
    daily_variance:        float              = 0.0
    daily_volatility:      float              = 0.0
    annualized_variance:   float              = 0.0
    annualized_volatility: float              = 0.0
    calculation_status:    str                = "VALID"
    assumptions:           List[str]          = field(default_factory=list)
    source_lineage_ids:    List[str]          = field(default_factory=list)
    metadata:              Dict[str, Any]     = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Risk contributions
# ---------------------------------------------------------------------------

@dataclass
class RiskContributionResult:
    """Marginal / component / percentage risk contribution for one symbol."""
    symbol:                  str
    weight:                  float
    marginal_contribution:   float           = 0.0
    component_contribution:  float           = 0.0
    percentage_contribution: float           = 0.0
    standalone_volatility:   float           = 0.0
    diversification_effect:  float           = 0.0
    status:                  str             = "VALID"
    metadata:                Dict[str, Any]  = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Beta
# ---------------------------------------------------------------------------

@dataclass
class BetaResult:
    """CAPM beta / alpha for a single asset vs a benchmark."""
    symbol:                    str
    benchmark:                 str
    beta:                      float          = 0.0
    alpha:                     float          = 0.0
    covariance_with_benchmark: float          = 0.0
    benchmark_variance:        float          = 0.0
    observation_count:         int            = 0
    start_date:                str            = ""
    end_date:                  str            = ""
    status:                    str            = "VALID"
    source_lineage_ids:        List[str]      = field(default_factory=list)
    metadata:                  Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Cluster
# ---------------------------------------------------------------------------

@dataclass
class CorrelationCluster:
    """A connected component of highly-correlated symbols."""
    cluster_id:                   str
    symbols:                      List[str]          = field(default_factory=list)
    method:                       ClusterMethod      = ClusterMethod.THRESHOLD_GRAPH
    threshold:                    float              = 0.75
    average_internal_correlation: float              = 0.0
    maximum_internal_correlation: float              = 0.0
    portfolio_weight:             float              = 0.0
    risk_contribution:            float              = 0.0
    dominant_industries:          List[str]          = field(default_factory=list)
    dominant_themes:              List[str]          = field(default_factory=list)
    warnings:                     List[str]          = field(default_factory=list)
    metadata:                     Dict[str, Any]     = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Exposure buckets
# ---------------------------------------------------------------------------

@dataclass
class ExposureBucket:
    """Aggregated weight exposure for a single industry/theme/market/asset bucket."""
    exposure_type:      ExposureType
    key:                str
    display_name:       str            = ""
    gross_weight:       float          = 0.0
    normalized_weight:  float          = 0.0
    overlapping_weight: float          = 0.0
    source:             str            = ""
    effective_from:     str            = ""
    available_from:     str            = ""
    lineage_ids:        List[str]      = field(default_factory=list)
    status:             str            = "VALID"
    metadata:           Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# ETF overlap
# ---------------------------------------------------------------------------

@dataclass
class ETFOverlapResult:
    """Direct + indirect exposure arising from an ETF holding."""
    etf_symbol:                  str
    portfolio_symbols:           List[str]      = field(default_factory=list)
    overlapping_constituents:    List[str]      = field(default_factory=list)
    direct_weight:               float          = 0.0
    indirect_weight:             float          = 0.0
    combined_effective_exposure: float          = 0.0
    holdings_as_of:              str            = ""
    holdings_available_from:     str            = ""
    lineage_ids:                 List[str]      = field(default_factory=list)
    status:                      str            = "VALID"
    metadata:                    Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Hidden concentration
# ---------------------------------------------------------------------------

@dataclass
class HiddenConcentrationResult:
    """Quantified hidden concentration metrics — descriptive only."""
    apparent_position_count:   int                         = 0
    effective_independent_bets: float                      = 0.0
    largest_cluster_weight:    float                       = 0.0
    top_cluster_weights:       List[float]                 = field(default_factory=list)
    correlated_pair_count:     int                         = 0
    industry_overlap_score:    float                       = 0.0
    theme_overlap_score:       float                       = 0.0
    ETF_overlap_score:         float                       = 0.0
    hidden_concentration_level: ConcentrationRiskLevel     = ConcentrationRiskLevel.UNKNOWN
    warnings:                  List[str]                   = field(default_factory=list)
    blockers:                  List[str]                   = field(default_factory=list)
    evidence:                  Dict[str, Any]              = field(default_factory=dict)
    metadata:                  Dict[str, Any]              = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Sizing exposure impact (hypothetical only)
# ---------------------------------------------------------------------------

@dataclass
class SizingExposureImpact:
    """
    Hypothetical impact of a proposed position on portfolio exposure.
    ALWAYS research_only=True, order_created=False, ledger_persisted=False.
    Labels: HYPOTHETICAL_ONLY, NO_LEDGER_WRITE, NO_ORDER_CREATED, NO_BROKER_CALL, NO_AUTO_APPLY.
    """
    proposal_id:               str
    portfolio_id:              str
    symbol:                    str
    before_snapshot_id:        str            = ""
    hypothetical_weight:       float          = 0.0
    before_portfolio_volatility: float        = 0.0
    after_portfolio_volatility:  float        = 0.0
    volatility_delta:          float          = 0.0
    before_cluster_weight:     float          = 0.0
    after_cluster_weight:      float          = 0.0
    cluster_weight_delta:      float          = 0.0
    before_industry_exposure:  Dict[str, float] = field(default_factory=dict)
    after_industry_exposure:   Dict[str, float] = field(default_factory=dict)
    before_theme_exposure:     Dict[str, float] = field(default_factory=dict)
    after_theme_exposure:      Dict[str, float] = field(default_factory=dict)
    binding_exposure_constraint: str          = ""
    status:                    str            = "VALID"
    research_only:             bool           = True
    order_created:             bool           = False
    ledger_persisted:          bool           = False
    metadata:                  Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True,    "research_only must always be True"
        assert self.order_created is False,   "order_created must always be False"
        assert self.ledger_persisted is False, "ledger_persisted must always be False"


# ---------------------------------------------------------------------------
# Top-level analysis result
# ---------------------------------------------------------------------------

@dataclass
class CorrelationExposureAnalysis:
    """
    Top-level result container for a full correlation & exposure analysis.
    Labels always include RESEARCH_ONLY plus the full safety set.
    """
    analysis_id:        str
    request:            CorrelationAnalysisRequest
    aligned_returns:    AlignedReturnSeries
    correlation_matrix: CorrelationMatrixResult
    covariance_matrix:  CovarianceMatrixResult
    portfolio_variance: PortfolioVarianceResult
    risk_contributions: List[RiskContributionResult]              = field(default_factory=list)
    beta_results:       List[BetaResult]                          = field(default_factory=list)
    clusters:           List[CorrelationCluster]                  = field(default_factory=list)
    industry_exposure:  List[ExposureBucket]                      = field(default_factory=list)
    theme_exposure:     List[ExposureBucket]                      = field(default_factory=list)
    market_exposure:    List[ExposureBucket]                      = field(default_factory=list)
    asset_exposure:     List[ExposureBucket]                      = field(default_factory=list)
    etf_overlaps:       List[ETFOverlapResult]                    = field(default_factory=list)
    hidden_concentration: Optional[HiddenConcentrationResult]     = None
    sizing_impact:      Optional[SizingExposureImpact]            = None
    stress_results:     List[CorrelationMatrixResult]             = field(default_factory=list)
    explanation:        Dict[str, Any]                            = field(default_factory=dict)
    lineage:            Dict[str, Any]                            = field(default_factory=dict)
    labels:             List[str]                                 = field(default_factory=lambda: list(_RESULT_LABELS))
    generated_at:       str                                       = ""
    content_hash:       str                                       = ""
    metadata:           Dict[str, Any]                            = field(default_factory=dict)
