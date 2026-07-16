"""
paper_trading/small_capital_strategy/decision_journal_models_v189.py
Data models for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


_SAFETY_DEFAULTS = dict(
    paper_only=True,
    research_only=True,
    simulate_only=True,
    validation_only=True,
    decision_only=True,
    journal_only=True,
    review_only=True,
    report_only=True,
    audit_only=True,
    no_real_orders=True,
    no_broker=True,
    no_margin=True,
    no_leverage=True,
    not_investment_advice=True,
    demo_only=True,
    not_for_production=True,
    production_trading_blocked=True,
)


# ── 1. DecisionJournalEntry ───────────────────────────────────────────────────

@dataclass
class DecisionJournalEntry:
    """Single decision journal entry for a paper decision event."""
    entry_id: str = ""
    date_label: str = ""
    state: str = "OBSERVE"
    symbol: str = ""
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    workflow_id: str = ""
    market_regime: str = ""
    theme: str = ""
    abc_point: str = ""
    planned_size_pct: float = 0.0
    stop_loss_pct: float = 0.0
    take_profit_pct: float = 0.0
    risk_budget_usage_pct: float = 0.0
    block_reason: str = ""
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 2. DecisionJournalBook ────────────────────────────────────────────────────

@dataclass
class DecisionJournalBook:
    """Collection of decision journal entries for a period."""
    book_id: str = ""
    period_label: str = ""
    entries: List[DecisionJournalEntry] = field(default_factory=list)
    entry_count: int = 0
    open_decisions: int = 0
    blocked_decisions: int = 0
    paper_plan_count: int = 0
    paper_entry_count: int = 0
    reduce_risk_count: int = 0
    no_trade_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 3. DecisionReviewInput ────────────────────────────────────────────────────

@dataclass
class DecisionReviewInput:
    """Input to the decision review engine."""
    review_type: str = "daily_review"
    date_label: str = ""
    source_workflow_id: str = ""
    journal_book: Optional[DecisionJournalBook] = None
    market_regime: str = "BULL"
    theme_exposure: Dict[str, float] = field(default_factory=dict)
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    risk_budget_usage_pct: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    monte_carlo_ruin_risk: float = 0.0
    config: Dict[str, Any] = field(default_factory=dict)
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 4. DecisionReviewResult ───────────────────────────────────────────────────

@dataclass
class DecisionReviewResult:
    """Output of the decision review engine."""
    review_type: str = "daily_review"
    date_label: str = ""
    source_workflow_id: str = ""
    review_grade: str = "ACCEPTABLE"
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    mistake_tags: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    blocked: bool = False
    block_reason: str = ""
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 5. DecisionOutcomeSnapshot ────────────────────────────────────────────────

@dataclass
class DecisionOutcomeSnapshot:
    """Snapshot of decision outcome for post-review tracking."""
    snapshot_id: str = ""
    entry_id: str = ""
    date_label: str = ""
    symbol: str = ""
    initial_state: str = "OBSERVE"
    outcome_state: str = "OBSERVE"
    risk_context: str = ""
    pnl_simulation: float = 0.0
    max_drawdown_simulation: float = 0.0
    held_days: int = 0
    stop_triggered: bool = False
    take_profit_triggered: bool = False
    review_grade: str = "ACCEPTABLE"
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 6. PaperDecisionLifecycle ─────────────────────────────────────────────────

@dataclass
class PaperDecisionLifecycle:
    """Tracks full lifecycle of a single paper decision from creation to review."""
    lifecycle_id: str = ""
    entry_id: str = ""
    symbol: str = ""
    created_label: str = ""
    reviewed_label: str = ""
    lifecycle_states: List[str] = field(default_factory=list)
    current_state: str = "OBSERVE"
    is_closed: bool = False
    close_reason: str = ""
    outcome: Optional[DecisionOutcomeSnapshot] = None
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 7. PaperDecisionEvidenceLink ──────────────────────────────────────────────

@dataclass
class PaperDecisionEvidenceLink:
    """Links a journal entry to its workflow evidence source."""
    link_id: str = ""
    entry_id: str = ""
    workflow_id: str = ""
    evidence_type: str = ""
    evidence_ref: str = ""
    evidence_summary: str = ""
    evidence_date_label: str = ""
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 8. DecisionMistakeTag ─────────────────────────────────────────────────────

@dataclass
class DecisionMistakeTag:
    """A tagged mistake identified during post-trade review."""
    tag: str = "NO_MISTAKE_FOUND"
    entry_id: str = ""
    date_label: str = ""
    description: str = ""
    severity: str = "LOW"
    recurrence_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 9. DecisionQualityScore ───────────────────────────────────────────────────

@dataclass
class DecisionQualityScore:
    """Computed quality score for a reviewed paper decision."""
    entry_id: str = ""
    date_label: str = ""
    grade: str = "ACCEPTABLE"
    score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    mistake_tags: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 10. DailyReviewSummary ────────────────────────────────────────────────────

@dataclass
class DailyReviewSummary:
    """Summary of a daily paper decision review session."""
    date_label: str = ""
    source_workflow_id: str = ""
    total_decisions: int = 0
    paper_plan_count: int = 0
    paper_entry_count: int = 0
    reduce_risk_count: int = 0
    blocked_count: int = 0
    no_trade_count: int = 0
    average_quality_score: float = 0.0
    grade: str = "ACCEPTABLE"
    findings: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    mistake_tags: List[str] = field(default_factory=list)
    market_regime: str = "BULL"
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 11. WeeklyReviewSummary ───────────────────────────────────────────────────

@dataclass
class WeeklyReviewSummary:
    """Summary of a weekly paper decision review session."""
    week_label: str = ""
    daily_summaries: List[DailyReviewSummary] = field(default_factory=list)
    total_decisions: int = 0
    paper_plan_count: int = 0
    paper_entry_count: int = 0
    reduce_risk_count: int = 0
    blocked_count: int = 0
    no_trade_count: int = 0
    average_quality_score: float = 0.0
    weekly_grade: str = "ACCEPTABLE"
    recurring_mistakes: List[str] = field(default_factory=list)
    top_findings: List[str] = field(default_factory=list)
    top_action_items: List[str] = field(default_factory=list)
    risk_budget_exceeded: bool = False
    over_concentration_detected: bool = False
    low_cash_reserve_detected: bool = False
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 12. MonthlyReviewSummary ──────────────────────────────────────────────────

@dataclass
class MonthlyReviewSummary:
    """Summary of a monthly paper decision review session."""
    month_label: str = ""
    weekly_summaries: List[WeeklyReviewSummary] = field(default_factory=list)
    total_decisions: int = 0
    average_quality_score: float = 0.0
    monthly_grade: str = "ACCEPTABLE"
    top_mistake_tags: List[str] = field(default_factory=list)
    improvement_areas: List[str] = field(default_factory=list)
    consistency_score: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 13. ReviewChecklist ───────────────────────────────────────────────────────

@dataclass
class ReviewChecklist:
    """Structured checklist for paper decision review."""
    checklist_id: str = ""
    review_type: str = "daily_review"
    date_label: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    completed_count: int = 0
    total_count: int = 0
    all_complete: bool = False
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 14. ReviewFinding ─────────────────────────────────────────────────────────

@dataclass
class ReviewFinding:
    """A single finding from a paper decision review."""
    finding_id: str = ""
    entry_id: str = ""
    date_label: str = ""
    dimension: str = ""
    severity: str = "LOW"
    description: str = ""
    evidence_ref: str = ""
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 15. ReviewActionItem ──────────────────────────────────────────────────────

@dataclass
class ReviewActionItem:
    """An action item generated from a paper decision review."""
    action_id: str = ""
    finding_id: str = ""
    date_label: str = ""
    description: str = ""
    priority: str = "MEDIUM"
    is_complete: bool = False
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 16. ReviewBlockReason ─────────────────────────────────────────────────────

@dataclass
class ReviewBlockReason:
    """A reason why a review was blocked."""
    block_id: str = ""
    entry_id: str = ""
    block_condition: str = ""
    description: str = ""
    date_label: str = ""
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 17. JournalExportManifest ─────────────────────────────────────────────────

@dataclass
class JournalExportManifest:
    """Manifest for journal export bundle."""
    manifest_id: str = ""
    export_date_label: str = ""
    export_path: str = ""
    included_periods: List[str] = field(default_factory=list)
    entry_count: int = 0
    review_count: int = 0
    evidence_count: int = 0
    audit_trail_count: int = 0
    format: str = "json"
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 18. JournalEvidencePack ───────────────────────────────────────────────────

@dataclass
class JournalEvidencePack:
    """Evidence pack for all journal entries in a period."""
    pack_id: str = ""
    period_label: str = ""
    evidence_links: List[PaperDecisionEvidenceLink] = field(default_factory=list)
    workflow_ids: List[str] = field(default_factory=list)
    entry_ids: List[str] = field(default_factory=list)
    evidence_count: int = 0
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 19. JournalAuditTrail ─────────────────────────────────────────────────────

@dataclass
class JournalAuditTrail:
    """Complete audit trail for all journal decisions and reviews."""
    trail_id: str = ""
    period_label: str = ""
    audit_events: List[Dict[str, Any]] = field(default_factory=list)
    event_count: int = 0
    entry_ids: List[str] = field(default_factory=list)
    review_ids: List[str] = field(default_factory=list)
    is_complete: bool = True
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 20. JournalHealthSummary ──────────────────────────────────────────────────

@dataclass
class JournalHealthSummary:
    """Health check summary for the decision journal system."""
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 21. JournalDashboard ──────────────────────────────────────────────────────

@dataclass
class JournalDashboard:
    """Dashboard payload for the decision journal UI."""
    dashboard_id: str = ""
    period_label: str = ""
    total_entries: int = 0
    open_decisions: int = 0
    reviewed_decisions: int = 0
    average_quality_score: float = 0.0
    overall_grade: str = "ACCEPTABLE"
    top_mistakes: List[str] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)
    action_items_open: int = 0
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    review_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


# ── 22. JournalValidationResult ───────────────────────────────────────────────

@dataclass
class JournalValidationResult:
    """Result of validating a journal entry or journal book."""
    is_valid: bool = True
    entry_id: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    blocked: bool = False
    block_reason: str = ""
    paper_only: bool = True
    research_only: bool = True
    journal_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "189"


_ALL_MODEL_NAMES = [
    "DecisionJournalEntry",
    "DecisionJournalBook",
    "DecisionReviewInput",
    "DecisionReviewResult",
    "DecisionOutcomeSnapshot",
    "PaperDecisionLifecycle",
    "PaperDecisionEvidenceLink",
    "DecisionMistakeTag",
    "DecisionQualityScore",
    "DailyReviewSummary",
    "WeeklyReviewSummary",
    "MonthlyReviewSummary",
    "ReviewChecklist",
    "ReviewFinding",
    "ReviewActionItem",
    "ReviewBlockReason",
    "JournalExportManifest",
    "JournalEvidencePack",
    "JournalAuditTrail",
    "JournalHealthSummary",
    "JournalDashboard",
    "JournalValidationResult",
]


def get_all_model_names() -> List[str]:
    """Return list of all 22 model names."""
    return list(_ALL_MODEL_NAMES)
