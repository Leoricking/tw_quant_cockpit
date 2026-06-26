"""
paper_trading/analytics/models_v164.py — Operational Analytics Data Models v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import (
    ReviewStatus, ReviewScope, MetricQuality, AttributionType,
    RootCauseCategory, ActionItemStatus, AnomalySeverity,
    MistakeCategory, ReproducibilityStatus, LessonStatus, ScorecardDimension,
)

# Safety invariants
NO_REAL_ORDERS: bool = True
NO_BROKER: bool = True
PAPER_ONLY: bool = True
RESEARCH_ONLY: bool = True
AUTO_STRATEGY_CHANGE_ENABLED: bool = False
AUTO_DEPLOYMENT_ENABLED: bool = False


@dataclass
class OperationalAnalyticsRequest:
    """Request for operational analytics computation."""
    session_id: str
    scope: ReviewScope
    as_of: datetime
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    baseline_id: Optional[str] = None
    benchmark_id: Optional[str] = None
    metric_policy_version: str = "1.6.4"
    attribution_policy_version: str = "1.6.4"
    review_policy_version: str = "1.6.4"
    cost_policy_version: str = "1.6.4"

    def validate(self) -> None:
        if not self.session_id:
            raise ValueError("session_id required")
        if self.window_start and self.window_start > self.as_of:
            raise ValueError("window_start must not be after as_of (PIT violation)")
        if self.window_end and self.window_end > self.as_of:
            raise ValueError("window_end must not be after as_of (PIT violation)")


@dataclass
class AttributionRecord:
    """Single attribution record linking PnL to a source."""
    attribution_id: str
    analytics_id: str
    attribution_type: AttributionType
    entity_id: str
    metric_name: str
    gross_value: Decimal
    net_value: Decimal
    contribution: Decimal
    confidence: Decimal
    quality: MetricQuality
    evidence_refs: List[str] = field(default_factory=list)
    policy_version: str = "1.6.4"


@dataclass
class AnomalyRecord:
    """Detected anomaly from deterministic rule."""
    anomaly_id: str
    rule_id: str
    rule_version: str
    metric: str
    observed: Any
    expected: Any
    threshold: Any
    severity: AnomalySeverity
    evidence: List[str] = field(default_factory=list)
    as_of: Optional[datetime] = None


@dataclass
class OperationalAnalyticsResult:
    """Result of an operational analytics run."""
    analytics_id: str
    session_id: str
    scope: ReviewScope
    as_of: datetime
    metrics: Dict[str, Any] = field(default_factory=dict)
    attributions: List[AttributionRecord] = field(default_factory=list)
    anomalies: List[AnomalyRecord] = field(default_factory=list)
    incidents: List[Dict[str, Any]] = field(default_factory=list)
    alerts: List[Dict[str, Any]] = field(default_factory=list)
    recovery_events: List[Dict[str, Any]] = field(default_factory=list)
    data_quality: MetricQuality = MetricQuality.UNKNOWN
    lineage: Dict[str, Any] = field(default_factory=dict)
    reproducibility_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    metric_policy_version: str = "1.6.4"
    attribution_policy_version: str = "1.6.4"
    paper_only: bool = True
    research_only: bool = True


@dataclass
class MistakeRecord:
    """A classified mistake from post-session review."""
    mistake_id: str
    category: MistakeCategory
    severity: AnomalySeverity
    evidence: List[str] = field(default_factory=list)
    affected_metric: Optional[str] = None
    root_cause: Optional[str] = None
    lesson: Optional[str] = None
    recommended_action: Optional[str] = None


@dataclass
class RootCauseRecord:
    """Root cause analysis result."""
    rca_id: str
    problem: str
    candidate_causes: List[str] = field(default_factory=list)
    excluded_causes: List[str] = field(default_factory=list)
    root_cause_category: RootCauseCategory = RootCauseCategory.UNKNOWN
    confidence: Decimal = Decimal("0.0")
    evidence_refs: List[str] = field(default_factory=list)
    causal_label: str = "ASSOCIATED"  # CAUSAL or ASSOCIATED or UNKNOWN


@dataclass
class LessonRecord:
    """A versioned lesson from review."""
    lesson_id: str
    title: str
    category: str
    description: str
    evidence_refs: List[str] = field(default_factory=list)
    applicable_scope: Optional[ReviewScope] = None
    created_from_review: Optional[str] = None
    version: str = "1.6.4"
    status: LessonStatus = LessonStatus.PROPOSED


@dataclass
class ActionItemHistoryEntry:
    """Single history entry for an action item."""
    from_status: Optional[ActionItemStatus]
    to_status: ActionItemStatus
    actor: str
    reason: str
    timestamp: datetime


@dataclass
class ActionItem:
    """An action item from review."""
    action_item_id: str
    review_id: str
    category: str
    title: str
    description: str
    owner: str
    status: ActionItemStatus
    priority: str
    due_date: Optional[datetime] = None
    evidence_refs: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    history: List[ActionItemHistoryEntry] = field(default_factory=list)

    def transition(self, to_status: ActionItemStatus, actor: str, reason: str, at: datetime) -> None:
        from paper_trading.analytics.enums_v164 import VALID_ACTION_ITEM_TRANSITIONS
        allowed = VALID_ACTION_ITEM_TRANSITIONS.get(self.status, set())
        if to_status not in allowed:
            raise ValueError(
                f"Invalid action item transition {self.status} → {to_status}. "
                f"Allowed: {allowed}"
            )
        if not actor:
            raise ValueError("actor required for action item transition")
        if not reason:
            raise ValueError("reason required for action item transition")
        entry = ActionItemHistoryEntry(
            from_status=self.status,
            to_status=to_status,
            actor=actor,
            reason=reason,
            timestamp=at,
        )
        self.history.append(entry)
        self.status = to_status
        self.updated_at = at


@dataclass
class ReviewScorecard:
    """Post-session review scorecard."""
    session_id: str
    data_quality_score: Decimal = Decimal("0")
    signal_quality_score: Decimal = Decimal("0")
    strategy_quality_score: Decimal = Decimal("0")
    execution_quality_score: Decimal = Decimal("0")
    operational_quality_score: Decimal = Decimal("0")
    risk_discipline_score: Decimal = Decimal("0")
    recovery_quality_score: Decimal = Decimal("0")
    overall_score: Decimal = Decimal("0")
    blocking_failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    weight_version: str = "1.6.4"
    quality: MetricQuality = MetricQuality.UNKNOWN
    score_ceiling: Optional[Decimal] = None

    def compute_overall(self) -> Decimal:
        from paper_trading.analytics.enums_v164 import SCORECARD_WEIGHTS, ScorecardDimension
        weights = SCORECARD_WEIGHTS
        scores = {
            ScorecardDimension.DATA_QUALITY:        self.data_quality_score,
            ScorecardDimension.SIGNAL_QUALITY:      self.signal_quality_score,
            ScorecardDimension.STRATEGY_QUALITY:    self.strategy_quality_score,
            ScorecardDimension.EXECUTION_QUALITY:   self.execution_quality_score,
            ScorecardDimension.OPERATIONAL_QUALITY: self.operational_quality_score,
            ScorecardDimension.RISK_DISCIPLINE:     self.risk_discipline_score,
            ScorecardDimension.RECOVERY_QUALITY:    self.recovery_quality_score,
        }
        total_weight = sum(weights.values())
        weighted_sum = sum(
            scores[dim] * Decimal(str(weights[dim]))
            for dim in weights
        )
        overall = weighted_sum / Decimal(str(total_weight))
        if self.score_ceiling is not None:
            overall = min(overall, self.score_ceiling)
        self.overall_score = overall.quantize(Decimal("0.01"))
        return self.overall_score


@dataclass
class SessionReview:
    """Post-session review record."""
    review_id: str
    session_id: str
    status: ReviewStatus
    review_scope: ReviewScope
    summary: str = ""
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    root_causes: List[RootCauseRecord] = field(default_factory=list)
    mistakes: List[MistakeRecord] = field(default_factory=list)
    lessons: List[LessonRecord] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    reviewer: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    version: str = "1.6.4"
    evidence_refs: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True

    def transition(self, to_status: ReviewStatus, actor: str, reason: str, at: datetime) -> None:
        from paper_trading.analytics.enums_v164 import VALID_REVIEW_TRANSITIONS
        allowed = VALID_REVIEW_TRANSITIONS.get(self.status, set())
        if to_status not in allowed:
            raise ValueError(
                f"Invalid review transition {self.status} → {to_status}. Allowed: {allowed}"
            )
        if not actor:
            raise ValueError("actor required for review transition")
        if not reason:
            raise ValueError("reason required for review transition")
        if to_status == ReviewStatus.COMPLETED and not self.evidence_refs:
            raise ValueError("evidence required to complete review")
        self.status = to_status
        self.updated_at = at
        if to_status == ReviewStatus.COMPLETED:
            self.completed_at = at


@dataclass
class AnalyticsSnapshot:
    """Immutable analytics snapshot for reproducibility."""
    snapshot_id: str
    analytics_id: str
    session_id: str
    input_hash: str
    output_hash: str
    reproducibility_hash: str
    code_version: str
    release_version: str
    metric_policy_version: str
    attribution_policy_version: str
    as_of: datetime
    created_at: datetime
    paper_only: bool = True
    research_only: bool = True


@dataclass
class AnalyticsLineage:
    """Lineage record for an analytics result."""
    lineage_id: str
    analytics_id: str
    source_session_ids: List[str] = field(default_factory=list)
    source_event_ids: List[str] = field(default_factory=list)
    metric_policy_version: str = "1.6.4"
    attribution_policy_version: str = "1.6.4"
    review_policy_version: str = "1.6.4"
    as_of: Optional[datetime] = None
    code_version: str = "1.6.4"
    release_version: str = "1.6.4"


__all__ = [
    "OperationalAnalyticsRequest", "AttributionRecord", "AnomalyRecord",
    "OperationalAnalyticsResult", "MistakeRecord", "RootCauseRecord",
    "LessonRecord", "ActionItemHistoryEntry", "ActionItem",
    "ReviewScorecard", "SessionReview", "AnalyticsSnapshot", "AnalyticsLineage",
    "NO_REAL_ORDERS", "NO_BROKER", "PAPER_ONLY", "RESEARCH_ONLY",
    "AUTO_STRATEGY_CHANGE_ENABLED", "AUTO_DEPLOYMENT_ENABLED",
]
