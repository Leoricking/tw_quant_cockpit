"""
portfolio/risk_controls/models_v153.py — Drawdown & Risk Controls Models v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from portfolio.risk_controls.enums_v153 import (
    AttributionType,
    DrawdownEpisodeStatus,
    DrawdownStatus,
    RiskActionType,
    RiskControlStatus,
    RiskControlType,
    StressScenarioType,
)

RESEARCH_ONLY  = True
MODELS_VERSION = "1.5.3"

_RESULT_LABELS = [
    "RESEARCH_ONLY",
    "DESCRIPTIVE_ANALYTICS_ONLY",
    "NOT_AN_AUTOMATED_CONTROL",
    "NOT_A_STOP_ORDER",
    "NOT_AN_ORDER",
    "NO_BROKER_CALL",
    "NO_LEDGER_WRITE",
]


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------

@dataclass
class DrawdownAnalysisRequest:
    """Input parameters for drawdown & risk controls analysis. Research-only."""
    request_id:           str
    portfolio_id:         str
    as_of:                str
    available_from:       str
    lookback_days:        int              = 252
    source_lineage_ids:   List[str]        = field(default_factory=list)
    research_only:        bool             = True
    metadata:             Dict[str, Any]  = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"


# ---------------------------------------------------------------------------
# Equity curve
# ---------------------------------------------------------------------------

@dataclass
class EquityCurvePoint:
    """A single point on the portfolio equity curve."""
    date:          str
    portfolio_value: float
    cash_flow:     float  = 0.0
    adjusted_value: float = 0.0
    metadata:      Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Underwater curve
# ---------------------------------------------------------------------------

@dataclass
class UnderwaterPoint:
    """A single point on the underwater (drawdown) curve."""
    date:             str
    drawdown_pct:     float
    portfolio_value:  float
    high_water_mark:  float
    status:           DrawdownStatus = DrawdownStatus.UNKNOWN
    metadata:         Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Drawdown episode
# ---------------------------------------------------------------------------

@dataclass
class DrawdownEpisode:
    """A contiguous drawdown episode from peak to recovery."""
    episode_id:        str
    start_date:        str
    trough_date:       str
    end_date:          Optional[str]        = None
    peak_value:        float                = 0.0
    trough_value:      float                = 0.0
    max_drawdown_pct:  float                = 0.0
    duration_days:     int                  = 0
    recovery_days:     Optional[int]        = None
    status:            DrawdownEpisodeStatus = DrawdownEpisodeStatus.OPEN
    metadata:          Dict[str, Any]       = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Drawdown summary
# ---------------------------------------------------------------------------

@dataclass
class DrawdownSummary:
    """Aggregated drawdown statistics for the full history."""
    portfolio_id:          str
    as_of:                 str
    max_drawdown_pct:      float             = 0.0
    max_drawdown_start:    str               = ""
    max_drawdown_trough:   str               = ""
    max_drawdown_end:      Optional[str]     = None
    current_drawdown_pct:  float             = 0.0
    current_drawdown_status: DrawdownStatus  = DrawdownStatus.UNKNOWN
    high_water_mark:       float             = 0.0
    high_water_mark_date:  str               = ""
    average_drawdown_pct:  float             = 0.0
    drawdown_episodes:     List[DrawdownEpisode] = field(default_factory=list)
    research_only:         bool              = True
    labels:                List[str]         = field(default_factory=lambda: list(_RESULT_LABELS))
    metadata:              Dict[str, Any]    = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"


# ---------------------------------------------------------------------------
# Drawdown attribution
# ---------------------------------------------------------------------------

@dataclass
class DrawdownAttribution:
    """Attribution of drawdown to a single dimension (position/industry/theme/cluster)."""
    attribution_id:     str
    attribution_type:   AttributionType
    key:                str
    drawdown_contribution_pct: float      = 0.0
    weight:             float             = 0.0
    pnl_contribution:   float             = 0.0
    research_only:      bool              = True
    metadata:           Dict[str, Any]    = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"


# ---------------------------------------------------------------------------
# Risk control policy
# ---------------------------------------------------------------------------

@dataclass
class RiskControlPolicy:
    """A single risk control policy definition. Research-only."""
    policy_id:          str
    control_type:       RiskControlType
    name:               str
    description:        str                = ""
    warn_threshold:     float              = 0.0
    breach_threshold:   float              = 0.0
    enabled:            bool               = True
    research_only:      bool               = True
    executable:         bool               = False
    order_created:      bool               = False
    auto_applied:       bool               = False
    metadata:           Dict[str, Any]     = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"
        assert self.executable is False, "executable must always be False"
        assert self.order_created is False, "order_created must always be False"
        assert self.auto_applied is False, "auto_applied must always be False"


# ---------------------------------------------------------------------------
# Risk control check
# ---------------------------------------------------------------------------

@dataclass
class RiskControlCheck:
    """Result of evaluating one risk control."""
    check_id:           str
    policy_id:          str
    control_type:       RiskControlType
    status:             RiskControlStatus  = RiskControlStatus.UNKNOWN
    current_value:      float              = 0.0
    warn_threshold:     float              = 0.0
    breach_threshold:   float              = 0.0
    recommended_action: RiskActionType     = RiskActionType.NO_ACTION
    detail:             str                = ""
    research_only:      bool               = True
    executable:         bool               = False
    order_created:      bool               = False
    ledger_persisted:   bool               = False
    auto_applied:       bool               = False
    metadata:           Dict[str, Any]     = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"
        assert self.executable is False, "executable must always be False"
        assert self.order_created is False, "order_created must always be False"
        assert self.ledger_persisted is False, "ledger_persisted must always be False"
        assert self.auto_applied is False, "auto_applied must always be False"


# ---------------------------------------------------------------------------
# Risk control evaluation
# ---------------------------------------------------------------------------

@dataclass
class RiskControlEvaluation:
    """Full evaluation result across all risk controls."""
    evaluation_id:      str
    portfolio_id:       str
    as_of:              str
    checks:             List[RiskControlCheck] = field(default_factory=list)
    overall_status:     RiskControlStatus      = RiskControlStatus.UNKNOWN
    breach_count:       int                    = 0
    warn_count:         int                    = 0
    pass_count:         int                    = 0
    research_only:      bool                   = True
    executable:         bool                   = False
    order_created:      bool                   = False
    ledger_persisted:   bool                   = False
    auto_applied:       bool                   = False
    labels:             List[str]              = field(default_factory=lambda: list(_RESULT_LABELS))
    generated_at:       str                    = ""
    metadata:           Dict[str, Any]         = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"
        assert self.executable is False, "executable must always be False"
        assert self.order_created is False, "order_created must always be False"
        assert self.ledger_persisted is False, "ledger_persisted must always be False"
        assert self.auto_applied is False, "auto_applied must always be False"


# ---------------------------------------------------------------------------
# Sizing risk impact
# ---------------------------------------------------------------------------

@dataclass
class SizingRiskImpact:
    """Hypothetical impact of a sizing proposal on risk controls. Research-only."""
    proposal_id:            str
    portfolio_id:           str
    symbol:                 str
    before_drawdown_pct:    float            = 0.0
    after_drawdown_pct:     float            = 0.0
    before_volatility:      float            = 0.0
    after_volatility:       float            = 0.0
    control_breaches_added: List[str]        = field(default_factory=list)
    control_breaches_removed: List[str]      = field(default_factory=list)
    risk_budget_consumed_pct: float          = 0.0
    binding_constraint:     str              = ""
    status:                 str              = "VALID"
    research_only:          bool             = True
    executable:             bool             = False
    order_created:          bool             = False
    ledger_persisted:       bool             = False
    auto_applied:           bool             = False
    metadata:               Dict[str, Any]   = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"
        assert self.executable is False, "executable must always be False"
        assert self.order_created is False, "order_created must always be False"
        assert self.ledger_persisted is False, "ledger_persisted must always be False"
        assert self.auto_applied is False, "auto_applied must always be False"


# ---------------------------------------------------------------------------
# Stress result
# ---------------------------------------------------------------------------

@dataclass
class DrawdownStressResult:
    """Result of a drawdown stress scenario. Research-only."""
    scenario_id:            str
    scenario_type:          StressScenarioType
    portfolio_id:           str
    shock_magnitude:        float            = 0.0
    projected_drawdown_pct: float            = 0.0
    projected_loss:         float            = 0.0
    risk_controls_breached: List[str]        = field(default_factory=list)
    description:            str              = ""
    research_only:          bool             = True
    executable:             bool             = False
    order_created:          bool             = False
    metadata:               Dict[str, Any]   = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"
        assert self.executable is False, "executable must always be False"
        assert self.order_created is False, "order_created must always be False"
