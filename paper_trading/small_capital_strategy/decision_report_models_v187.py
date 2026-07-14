"""
paper_trading/small_capital_strategy/decision_report_models_v187.py
Data models for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
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


# ── 1. DecisionReportInput ────────────────────────────────────────────────────

@dataclass
class DecisionReportInput:
    """Input to the decision report generator, wrapping cockpit result."""
    report_type: str = "daily_decision_report"
    report_version: str = "1.8.7"
    release_name: str = "Decision Report Export & Evidence Pack"
    generated_at_policy: str = "deterministic_utc_date_only"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    final_cockpit_grade: str = "WAIT"
    daily_action: str = "DECISION_ONLY"
    weekly_action: str = "DECISION_ONLY"
    candidate_count: int = 0
    ready_candidate_count: int = 0
    watch_candidate_count: int = 0
    blocked_candidate_count: int = 0
    reduce_risk_candidate_count: int = 0
    portfolio_holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    theme_exposure_summary: Dict[str, float] = field(default_factory=dict)
    sector_exposure_summary: Dict[str, float] = field(default_factory=dict)
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    max_drawdown_budget_usage_pct: float = 0.0
    position_sizing_summary: str = ""
    portfolio_rebalance_summary: str = ""
    top_watch_candidates: List[str] = field(default_factory=list)
    paper_plan_ready_candidates: List[str] = field(default_factory=list)
    reduce_risk_candidates: List[str] = field(default_factory=list)
    blocked_candidates: List[str] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
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
    schema_version: str = "187"


# ── 2. DecisionReportResult ───────────────────────────────────────────────────

@dataclass
class DecisionReportResult:
    """Output from the decision report generator."""
    report_version: str = "1.8.7"
    release_name: str = "Decision Report Export & Evidence Pack"
    report_type: str = "daily_decision_report"
    generated_at_policy: str = "deterministic_utc_date_only"
    deterministic_timestamp_policy: str = "date_label_only_no_wall_clock"
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    final_cockpit_grade: str = "WAIT"
    daily_action: str = "DECISION_ONLY"
    weekly_action: str = "DECISION_ONLY"
    candidate_count: int = 0
    ready_candidate_count: int = 0
    watch_candidate_count: int = 0
    blocked_candidate_count: int = 0
    reduce_risk_candidate_count: int = 0
    portfolio_holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    theme_exposure_summary: Dict[str, float] = field(default_factory=dict)
    sector_exposure_summary: Dict[str, float] = field(default_factory=dict)
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    max_drawdown_budget_usage_pct: float = 0.0
    position_sizing_summary: str = ""
    portfolio_rebalance_summary: str = ""
    top_watch_candidates: List[str] = field(default_factory=list)
    paper_plan_ready_candidates: List[str] = field(default_factory=list)
    reduce_risk_candidates: List[str] = field(default_factory=list)
    blocked_candidates: List[str] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    evidence_items: List[str] = field(default_factory=list)
    audit_trail: List[str] = field(default_factory=list)
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
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
    schema_version: str = "187"


# ── 3. DailyDecisionReport ────────────────────────────────────────────────────

@dataclass
class DailyDecisionReport:
    """Daily decision report output."""
    report_version: str = "1.8.7"
    report_type: str = "daily_decision_report"
    date_label: str = ""
    market_regime: str = "BULL"
    daily_action: str = "DECISION_ONLY"
    final_cockpit_grade: str = "WAIT"
    candidate_count: int = 0
    ready_candidate_count: int = 0
    blocked_candidate_count: int = 0
    paper_plan_ready_candidates: List[str] = field(default_factory=list)
    blocked_candidates: List[str] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 4. WeeklyDecisionReport ───────────────────────────────────────────────────

@dataclass
class WeeklyDecisionReport:
    """Weekly decision report output."""
    report_version: str = "1.8.7"
    report_type: str = "weekly_decision_report"
    week_label: str = ""
    market_regime: str = "BULL"
    weekly_action: str = "DECISION_ONLY"
    final_cockpit_grade: str = "WAIT"
    portfolio_holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    max_drawdown_budget_usage_pct: float = 0.0
    reduce_risk_candidates: List[str] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    portfolio_rebalance_summary: str = ""
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 5. CandidateEvidenceItem ──────────────────────────────────────────────────

@dataclass
class CandidateEvidenceItem:
    """Evidence item for a single candidate decision."""
    ticker: str = ""
    decision_action: str = "WAIT"
    block_reason: str = ""
    abc_buy_point_status: str = ""
    market_regime_status: str = ""
    risk_status: str = ""
    position_sizing_status: str = ""
    portfolio_exposure_status: str = ""
    monte_carlo_risk_status: str = ""
    theme_sector_concentration: str = ""
    cash_reserve_status: str = ""
    stop_loss_presence: bool = True
    final_decision_grade: str = "WAIT"
    evidence_source: str = "decision_cockpit_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 6. CandidateEvidencePack ──────────────────────────────────────────────────

@dataclass
class CandidateEvidencePack:
    """Evidence pack for all candidates in a report."""
    report_version: str = "1.8.7"
    report_type: str = "evidence_pack"
    candidate_count: int = 0
    evidence_items: List[CandidateEvidenceItem] = field(default_factory=list)
    ready_count: int = 0
    blocked_count: int = 0
    reduce_risk_count: int = 0
    watch_count: int = 0
    audit_complete: bool = True
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 7. BlockReasonEvidence ────────────────────────────────────────────────────

@dataclass
class BlockReasonEvidence:
    """Evidence for a block reason."""
    block_code: str = ""
    block_description: str = ""
    severity: str = "HIGH"
    affected_tickers: List[str] = field(default_factory=list)
    evidence_source: str = ""
    triggered_at: str = ""
    resolution_guidance: str = ""
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 8. BuyPointEvidence ───────────────────────────────────────────────────────

@dataclass
class BuyPointEvidence:
    """Evidence for A/B/C buy point evaluation."""
    ticker: str = ""
    buy_point_type: str = "A_10MA_PULLBACK"
    condition_met: bool = False
    action: str = "WAIT"
    above_10ma: bool = False
    above_20ma: bool = False
    volume_breakout: bool = False
    volume_contracting: bool = True
    kd_below_50: bool = False
    kd_recovering: bool = False
    stop_loss_defined: bool = True
    block_reasons: List[str] = field(default_factory=list)
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 9. RiskEvidence ───────────────────────────────────────────────────────────

@dataclass
class RiskEvidence:
    """Evidence for risk decision."""
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk_pct: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    exposure_ok: bool = True
    cash_ok: bool = True
    ruin_risk_ok: bool = True
    drawdown_ok: bool = True
    stop_loss_coverage_ok: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 10. PositionSizingEvidence ────────────────────────────────────────────────

@dataclass
class PositionSizingEvidence:
    """Evidence for position sizing decision."""
    ticker: str = ""
    capital: float = 300000.0
    suggested_position_pct: float = 10.0
    suggested_position_amount: float = 30000.0
    position_ok: bool = True
    action: str = "DECISION_ONLY"
    conviction_score: float = 5.0
    volatility_pct: float = 15.0
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 11. PortfolioEvidence ─────────────────────────────────────────────────────

@dataclass
class PortfolioEvidence:
    """Evidence for portfolio decision."""
    holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    overexposed_sectors: List[str] = field(default_factory=list)
    overexposed_themes: List[str] = field(default_factory=list)
    rebalance_needed: bool = False
    portfolio_ok: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 12. MonteCarloEvidence ────────────────────────────────────────────────────

@dataclass
class MonteCarloEvidence:
    """Evidence for Monte Carlo risk decision."""
    ruin_probability_pct: float = 0.0
    ruin_risk_level: str = "LOW"
    entry_allowed: bool = True
    add_allowed: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 13. ThemeEvidence ─────────────────────────────────────────────────────────

@dataclass
class ThemeEvidence:
    """Evidence for theme/sector concentration."""
    top_themes: List[str] = field(default_factory=list)
    weak_themes: List[str] = field(default_factory=list)
    overcrowded_themes: List[str] = field(default_factory=list)
    theme_rotation_active: bool = False
    theme_exposure_summary: Dict[str, float] = field(default_factory=dict)
    sector_exposure_summary: Dict[str, float] = field(default_factory=dict)
    concentration_blocked: bool = False
    action: str = "DECISION_ONLY"
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 14. MarketRegimeEvidence ──────────────────────────────────────────────────

@dataclass
class MarketRegimeEvidence:
    """Evidence for market regime decision."""
    market_regime: str = "BULL"
    regime_blocked: bool = False
    entry_permitted: bool = True
    add_permitted: bool = True
    max_exposure_pct: float = 60.0
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    evidence_source: str = "decision_cockpit_engine_v186"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 15. WatchlistReport ───────────────────────────────────────────────────────

@dataclass
class WatchlistReport:
    """Watchlist report output."""
    report_version: str = "1.8.7"
    report_type: str = "watchlist_report"
    candidate_count: int = 0
    top_watch_candidates: List[str] = field(default_factory=list)
    paper_plan_ready_candidates: List[str] = field(default_factory=list)
    watch_candidate_count: int = 0
    ready_candidate_count: int = 0
    market_regime: str = "BULL"
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 16. BlockedCandidateReport ────────────────────────────────────────────────

@dataclass
class BlockedCandidateReport:
    """Blocked candidates report output."""
    report_version: str = "1.8.7"
    report_type: str = "blocked_candidates_report"
    blocked_candidate_count: int = 0
    blocked_candidates: List[str] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    block_reason_evidence: List[BlockReasonEvidence] = field(default_factory=list)
    market_regime: str = "BULL"
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 17. ReduceRiskReport ──────────────────────────────────────────────────────

@dataclass
class ReduceRiskReport:
    """Reduce risk report output."""
    report_version: str = "1.8.7"
    report_type: str = "reduce_risk_report"
    reduce_risk_candidate_count: int = 0
    reduce_risk_candidates: List[str] = field(default_factory=list)
    risk_evidence: Optional[RiskEvidence] = None
    portfolio_evidence: Optional[PortfolioEvidence] = None
    monte_carlo_evidence: Optional[MonteCarloEvidence] = None
    reduce_required: bool = False
    reason: str = ""
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 18. PaperPlanReadyReport ──────────────────────────────────────────────────

@dataclass
class PaperPlanReadyReport:
    """Paper plan ready report output."""
    report_version: str = "1.8.7"
    report_type: str = "paper_plan_ready_report"
    ready_candidate_count: int = 0
    paper_plan_ready_candidates: List[str] = field(default_factory=list)
    evidence_items: List[CandidateEvidenceItem] = field(default_factory=list)
    market_regime: str = "BULL"
    capital_stage: str = "300K"
    final_cockpit_grade: str = "WATCH"
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 19. DecisionAuditTrail ────────────────────────────────────────────────────

@dataclass
class DecisionAuditTrail:
    """Audit trail for a single decision report."""
    report_version: str = "1.8.7"
    report_type: str = "audit_trail"
    date_label: str = ""
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    final_cockpit_grade: str = "WAIT"
    daily_action: str = "DECISION_ONLY"
    weekly_action: str = "DECISION_ONLY"
    audit_entries: List[Dict[str, Any]] = field(default_factory=list)
    decision_evidence_count: int = 0
    block_reasons: List[str] = field(default_factory=list)
    audit_complete: bool = True
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 20. ReportExportManifest ──────────────────────────────────────────────────

@dataclass
class ReportExportManifest:
    """Manifest tracking all report exports."""
    report_version: str = "1.8.7"
    report_type: str = "export_manifest"
    exports: List[Dict[str, Any]] = field(default_factory=list)
    export_count: int = 0
    json_exports: int = 0
    markdown_exports: int = 0
    csv_exports: int = 0
    console_exports: int = 0
    dashboard_exports: int = 0
    all_exports_safe: bool = True
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "187"


# ── 21. ReportValidationResult ────────────────────────────────────────────────

@dataclass
class ReportValidationResult:
    """Result of validating a decision report."""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    has_audit_trail: bool = True
    has_evidence_pack: bool = True
    has_paper_only_flags: bool = True
    has_no_broker_flags: bool = True
    has_not_investment_advice_flags: bool = True
    has_deterministic_timestamp: bool = True
    has_safe_output_path: bool = True
    no_forbidden_actions: bool = True
    consistent_candidate_counts: bool = True
    all_blocks_have_reasons: bool = True
    all_entries_have_evidence: bool = True
    final_report_grade: str = "COMPLETE"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── 22. ReportHealthSummary ───────────────────────────────────────────────────

@dataclass
class ReportHealthSummary:
    """Health summary for decision report system."""
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    paper_only: bool = True
    research_only: bool = True
    report_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "187"


# ── Model registry ────────────────────────────────────────────────────────────

_ALL_MODELS = [
    "DecisionReportInput",
    "DecisionReportResult",
    "DailyDecisionReport",
    "WeeklyDecisionReport",
    "CandidateEvidenceItem",
    "CandidateEvidencePack",
    "BlockReasonEvidence",
    "BuyPointEvidence",
    "RiskEvidence",
    "PositionSizingEvidence",
    "PortfolioEvidence",
    "MonteCarloEvidence",
    "ThemeEvidence",
    "MarketRegimeEvidence",
    "WatchlistReport",
    "BlockedCandidateReport",
    "ReduceRiskReport",
    "PaperPlanReadyReport",
    "DecisionAuditTrail",
    "ReportExportManifest",
    "ReportValidationResult",
    "ReportHealthSummary",
]


def get_all_model_names() -> list:
    """Return list of all model names (22 total)."""
    return list(_ALL_MODELS)
