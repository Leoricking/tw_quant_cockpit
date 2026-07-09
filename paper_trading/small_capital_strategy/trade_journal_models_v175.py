"""
paper_trading/small_capital_strategy/trade_journal_models_v175.py
Dataclass models for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, TradeOutcome, EntryQuality, ExitQuality,
    ABCPattern, MistakeCategory, ReviewStatus, JournalEntryStatus,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"
_LINEAGE = "paper_trading.small_capital_strategy.trade_journal_models_v175"


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@dataclass
class TradeJournalEntry:
    """Single trade journal entry."""
    symbol: str = ""
    direction: TradeDirection = TradeDirection.LONG
    entry_date: str = ""
    entry_price: float = 0.0
    exit_date: str = ""
    exit_price: float = 0.0
    position_size_twd: float = 0.0
    stop_loss_price: float = 0.0
    stop_loss_pct: float = 0.0
    outcome: TradeOutcome = TradeOutcome.OPEN
    status: JournalEntryStatus = JournalEntryStatus.OPEN
    abc_pattern: ABCPattern = ABCPattern.UNKNOWN
    market_regime: str = "UNKNOWN"
    watchlist_tier: int = 0
    notes: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class TradeDecisionSnapshot:
    """Snapshot of the decision state at trade entry time."""
    symbol: str = ""
    decision_date: str = ""
    market_regime: str = "UNKNOWN"
    abc_pattern: ABCPattern = ABCPattern.UNKNOWN
    watchlist_tier: int = 0
    entry_trigger: str = ""
    risk_per_trade_twd: float = 3000.0
    position_size_twd: float = 0.0
    cash_pct_before: float = 100.0
    stop_loss_pct: float = 0.0
    rationale: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class EntryReviewResult:
    """Result of reviewing a trade entry."""
    symbol: str = ""
    entry_date: str = ""
    entry_quality: EntryQuality = EntryQuality.UNKNOWN
    entry_score: float = 0.0
    trigger_met: bool = False
    regime_aligned: bool = False
    watchlist_confirmed: bool = False
    stop_loss_set: bool = False
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class ExitReviewResult:
    """Result of reviewing a trade exit."""
    symbol: str = ""
    exit_date: str = ""
    exit_quality: ExitQuality = ExitQuality.UNKNOWN
    exit_score: float = 0.0
    target_reached: bool = False
    stop_triggered: bool = False
    panic_exit: bool = False
    held_too_long: bool = False
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCExecutionReview:
    """Review of ABC buy-point execution quality."""
    symbol: str = ""
    abc_pattern: ABCPattern = ABCPattern.UNKNOWN
    execution_score: float = 0.0
    a_point_valid: bool = False
    b_breakout_clean: bool = False
    c_reclaim_confirmed: bool = False
    position_sized_correctly: bool = False
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class WatchlistConversionReview:
    """Review of watchlist candidate conversion to actual trade."""
    symbol: str = ""
    watchlist_tier: int = 0
    converted_to_trade: bool = False
    conversion_score: float = 0.0
    tier1_count: int = 0
    tier2_count: int = 0
    conversion_rate_pct: float = 0.0
    exclusion_reason: str = ""
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class RiskViolationReview:
    """Review of risk management violations."""
    symbol: str = ""
    violation_date: str = ""
    violation_type: str = ""
    severity: str = "LOW"
    oversize_detected: bool = False
    no_stop_loss_detected: bool = False
    regime_mismatch_detected: bool = False
    abc_plan_violated: bool = False
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class RegimeOutcomeReview:
    """Review of outcomes grouped by market regime."""
    regime: str = "UNKNOWN"
    period_start: str = ""
    period_end: str = ""
    trade_count: int = 0
    win_count: int = 0
    loss_count: int = 0
    win_rate_pct: float = 0.0
    avg_return_pct: float = 0.0
    regime_alignment_score: float = 0.0
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class MistakeTaxonomyResult:
    """Result of classifying trading mistakes."""
    symbol: str = ""
    trade_date: str = ""
    mistake_categories: List[MistakeCategory] = field(default_factory=list)
    primary_mistake: MistakeCategory = MistakeCategory.NONE
    severity_score: float = 0.0
    corrective_action: str = ""
    notes: str = ""
    review_status: ReviewStatus = ReviewStatus.PENDING
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class ReviewScorecard:
    """Comprehensive review scorecard. No A+."""
    total_score: float = 0.0
    entry_score: float = 0.0
    exit_score: float = 0.0
    abc_score: float = 0.0
    watchlist_score: float = 0.0
    risk_compliance_score: float = 0.0
    regime_alignment_score: float = 0.0
    mistake_rate_pct: float = 0.0
    win_rate_pct: float = 0.0
    grade: str = "F"
    weights_sum: int = 100
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class TradeJournalDashboard:
    """Aggregated trade journal dashboard."""
    entries_count: int = 0
    open_count: int = 0
    closed_count: int = 0
    win_count: int = 0
    loss_count: int = 0
    win_rate_pct: float = 0.0
    avg_return_pct: float = 0.0
    total_pnl_twd: float = 0.0
    scorecard: ReviewScorecard = field(default_factory=ReviewScorecard)
    violations_count: int = 0
    regime_reviews: List[RegimeOutcomeReview] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class TradeJournalReport:
    """Full trade journal report."""
    sections: Dict[str, Any] = field(default_factory=dict)
    report_format: str = "JSON"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class TradeJournalHealthSummary:
    """Health summary for the trade journal system."""
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    status: str = "FAIL"
    checks: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
