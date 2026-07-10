"""
paper_trading/small_capital_strategy/mistake_taxonomy_models_v176.py
Data models for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity, BehaviorRiskLevel,
)

_SCHEMA  = "176"
_POLICY  = "1.7.6-mistake-taxonomy-weekly-review"
_LINEAGE = "paper_trading.small_capital_strategy.mistake_taxonomy_models_v176"


@dataclass
class MistakeTaxonomyRule:
    """Definition of a taxonomy rule mapping category to severity and description."""
    rule_id:     str = ""
    category:    MistakeCategory = MistakeCategory.UNKNOWN
    severity:    MistakeSeverity = MistakeSeverity.INFO
    description: str = ""
    example:     str = ""
    corrective_action: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class MistakeEvent:
    """Single mistake occurrence linked to a trade."""
    event_id:   str = ""
    symbol:     str = ""
    trade_date: str = ""
    category:   MistakeCategory = MistakeCategory.UNKNOWN
    severity:   MistakeSeverity = MistakeSeverity.INFO
    cost_twd:   float = 0.0
    description: str = ""
    week_label:  str = ""
    month_label: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class MistakeCostSummary:
    """Aggregate cost summary across multiple mistake events."""
    total_cost_twd:  float = 0.0
    event_count:     int   = 0
    by_category:     Dict[str, float] = field(default_factory=dict)
    worst_category:  Optional[MistakeCategory] = None
    worst_cost_twd:  float = 0.0
    avg_cost_twd:    float = 0.0
    schema_version:  str = _SCHEMA
    policy_version:  str = _POLICY
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class RepeatedMistakePattern:
    """Pattern of a mistake category that repeats within a review period."""
    category:     MistakeCategory = MistakeCategory.UNKNOWN
    count:        int   = 0
    dates:        List[str] = field(default_factory=list)
    total_cost_twd: float = 0.0
    severity_escalation: MistakeSeverity = MistakeSeverity.INFO
    risk_flag:    str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class WeeklyReviewInput:
    """Input data bundle for a weekly review."""
    week_start:   str = ""
    week_end:     str = ""
    events:       List[MistakeEvent] = field(default_factory=list)
    total_trades: int = 0
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class WeeklyReviewResult:
    """Result of a weekly mistake review analysis."""
    week_start:         str = ""
    week_end:           str = ""
    total_events:       int = 0
    top_mistakes:       List[MistakeCategory] = field(default_factory=list)
    cost_summary:       Optional[MistakeCostSummary] = None
    repeat_patterns:    List[RepeatedMistakePattern] = field(default_factory=list)
    behavior_score:     float = 0.0
    risk_level:         BehaviorRiskLevel = BehaviorRiskLevel.PASS
    actions:            List[str] = field(default_factory=list)
    summary:            str = ""
    schema_version:     str = _SCHEMA
    policy_version:     str = _POLICY
    source_lineage:     str = _LINEAGE
    paper_only:         bool = True
    research_only:      bool = True
    no_real_orders:     bool = True
    no_broker:          bool = True
    not_investment_advice: bool = True


@dataclass
class MonthlyReviewResult:
    """Monthly rollup of weekly reviews."""
    month_label:        str = ""
    weekly_results:     List[WeeklyReviewResult] = field(default_factory=list)
    total_events:       int = 0
    total_cost_twd:     float = 0.0
    behavior_trend:     str = "STABLE"
    worst_week:         str = ""
    top_mistakes:       List[MistakeCategory] = field(default_factory=list)
    avg_behavior_score: float = 0.0
    schema_version:     str = _SCHEMA
    policy_version:     str = _POLICY
    source_lineage:     str = _LINEAGE
    paper_only:         bool = True
    research_only:      bool = True
    no_real_orders:     bool = True
    no_broker:          bool = True
    not_investment_advice: bool = True


@dataclass
class BehaviorRiskScore:
    """Behavior risk score for a review period (0-100, higher = more risk)."""
    score:       float = 0.0
    level:       BehaviorRiskLevel = BehaviorRiskLevel.PASS
    factors:     Dict[str, float] = field(default_factory=dict)
    description: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class ImprovementAction:
    """A specific improvement action derived from mistake analysis."""
    action_id:   str = ""
    category:    MistakeCategory = MistakeCategory.UNKNOWN
    priority:    int = 3
    description: str = ""
    rationale:   str = ""
    deadline:    str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class ReviewDashboard:
    """Comprehensive weekly/monthly review dashboard."""
    weekly_result:   Optional[WeeklyReviewResult]  = None
    monthly_result:  Optional[MonthlyReviewResult] = None
    behavior_score:  Optional[BehaviorRiskScore]   = None
    top_actions:     List[ImprovementAction] = field(default_factory=list)
    entries_count:   int = 0
    events_count:    int = 0
    schema_version:  str = _SCHEMA
    policy_version:  str = _POLICY
    source_lineage:  str = _LINEAGE
    paper_only:      bool = True
    research_only:   bool = True
    no_real_orders:  bool = True
    no_broker:       bool = True
    not_investment_advice: bool = True


@dataclass
class ReviewHealthSummary:
    """Health check summary for the review system."""
    all_passed:     bool = True
    passed:         int  = 0
    failed:         int  = 0
    total:          int  = 0
    status:         str  = "PASS"
    checks:         List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    paper_only:     bool = True
    research_only:  bool = True
    no_real_orders: bool = True
    no_broker:      bool = True
    not_investment_advice: bool = True
