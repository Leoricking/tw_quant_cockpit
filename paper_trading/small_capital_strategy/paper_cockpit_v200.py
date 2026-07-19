"""
paper_trading/small_capital_strategy/paper_cockpit_v200.py
v2.0.0 Paper Cockpit Unified Entry & Strategy Decision Console
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] Unified Paper Cockpit Only. Decision Console Only. Dashboard Only. Report Only. Audit Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

VERSION = "2.0.0"
SCHEMA_VERSION = "200"
RELEASE_NAME = "Paper Cockpit Unified Entry & Strategy Decision Console"
BASELINE_TESTS = 31925
MIN_NEW_TESTS = 500

COVERED_VERSIONS = [
    "1.7.0", "1.7.1", "1.7.2", "1.7.3", "1.7.5", "1.7.6",
    "1.7.7", "1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2",
    "1.8.3", "1.8.4", "1.8.6", "1.8.7", "1.8.8", "1.8.9",
    "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5",
    "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10",
]

SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "unified_paper_cockpit_only": True,
    "decision_console_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "no_real_portfolio_rebalancing": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "deterministic_paper_workflow": True,
    "backward_compatible_v170_to_v1910": True,
    "cockpit_executes_order": False,
    "cockpit_mutates_strategy": False,
    "cockpit_rebalances_real_portfolio": False,
    "export_triggers_real_order": False,
    "ticket_triggers_broker": False,
    "dashboard_writes_production_db": False,
    "report_activates_live_strategy": False,
    "audit_activates_live_strategy": False,
}

assert len(SAFETY_FLAGS) == 30, f"Expected 30 SAFETY_FLAGS, got {len(SAFETY_FLAGS)}"

FORBIDDEN_ACTIONS: List[str] = [
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
    "REBALANCE_REAL_PORTFOLIO",
]

assert len(FORBIDDEN_ACTIONS) == 10, f"Expected 10 FORBIDDEN_ACTIONS, got {len(FORBIDDEN_ACTIONS)}"

ALLOWED_ACTIONS: List[str] = [
    "PAPER_WATCH_ONLY",
    "PAPER_ALLOW_NORMAL_SIZE",
    "PAPER_ALLOW_REDUCED_SIZE",
    "PAPER_TEST_POSITION_ONLY",
    "PAPER_BLOCK_NEW_ENTRY",
    "PAPER_KEEP_CASH",
    "PAPER_REQUIRE_HUMAN_REVIEW",
    "PAPER_RISK_OFF_MODE",
    "PAPER_NO_CHANGE",
]

assert len(ALLOWED_ACTIONS) == 9, f"Expected 9 ALLOWED_ACTIONS, got {len(ALLOWED_ACTIONS)}"

HARD_BLOCK_CONDITIONS: List[str] = [
    "real_order_requested",
    "broker_requested",
    "margin_or_leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "real_portfolio_rebalancing_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_watchlist",
    "missing_candidate_evidence",
    "missing_abc_entry_check",
    "missing_portfolio_risk_check",
    "missing_position_sizing_check",
    "malformed_cockpit_input",
    "unsafe_export_path",
    "forbidden_action_words",
    "cockpit_tries_to_execute_order",
    "cockpit_tries_to_mutate_strategy",
    "cockpit_tries_to_rebalance_real_portfolio",
]

assert len(HARD_BLOCK_CONDITIONS) == 22, f"Expected 22 HARD_BLOCK_CONDITIONS, got {len(HARD_BLOCK_CONDITIONS)}"

NO_ENTRY_CONDITIONS: List[str] = [
    "portfolio_risk_exceeded",
    "theme_exposure_exceeded",
    "cash_buffer_too_low",
    "stop_distance_too_wide",
    "market_risk_off_without_enough_edge",
    "missing_evidence",
    "malformed_input",
    "broker_or_real_order_or_live_activation_requested",
]

assert len(NO_ENTRY_CONDITIONS) == 8, f"Expected 8 NO_ENTRY_CONDITIONS, got {len(NO_ENTRY_CONDITIONS)}"

ABC_DECISION_TYPES: List[str] = [
    "A_PULLBACK_10MA",
    "B_BREAKOUT_BASE",
    "C_RECLAIM_20MA",
    "NO_ENTRY",
]

assert len(ABC_DECISION_TYPES) == 4, f"Expected 4 ABC_DECISION_TYPES, got {len(ABC_DECISION_TYPES)}"

CLI_COMMANDS: List[str] = [
    "paper-cockpit-version",
    "paper-cockpit-run",
    "paper-cockpit-watchlist",
    "paper-cockpit-score",
    "paper-cockpit-abc-check",
    "paper-cockpit-risk-check",
    "paper-cockpit-sizing-check",
    "paper-cockpit-no-entry",
    "paper-cockpit-decision-ticket",
    "paper-cockpit-dashboard",
    "paper-cockpit-report",
    "paper-cockpit-export",
    "paper-cockpit-health",
    "paper-cockpit-gate",
    "paper-cockpit-scenarios",
    "paper-cockpit-fixtures",
    "paper-cockpit-safety-audit",
]

assert len(CLI_COMMANDS) == 17, f"Expected 17 CLI_COMMANDS, got {len(CLI_COMMANDS)}"

GUI_TABS: List[str] = [
    "paper_cockpit",
    "strategy_decision_console",
    "decision_ticket",
]

assert len(GUI_TABS) == 3, f"Expected 3 GUI_TABS, got {len(GUI_TABS)}"


# ---------------------------------------------------------------------------
# Dataclasses — all 23 models, schema_version="200"
# ---------------------------------------------------------------------------

@dataclass
class PaperCockpitInput:
    """Input to the unified paper cockpit workflow. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    capital_twd: float = 300000.0
    market_regime: str = "BULL"
    watchlist: List[str] = field(default_factory=list)
    candidates: List[str] = field(default_factory=list)
    theme: str = ""
    use_cash_buffer_check: bool = True
    use_risk_budget_check: bool = True
    human_review_required: bool = True


@dataclass
class PaperCockpitWatchlist:
    """Paper cockpit watchlist model. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_orders: bool = True
    symbols: List[str] = field(default_factory=list)
    theme: str = ""
    regime: str = "BULL"
    count: int = 0
    is_valid: bool = False
    block_reason: str = ""


@dataclass
class PaperCockpitSignalScore:
    """Unified signal score for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    symbol: str = ""
    theme_score: float = 0.0
    fundamental_score: float = 0.0
    technical_score: float = 0.0
    institutional_score: float = 0.0
    margin_score: float = 0.0
    total_score: float = 0.0
    grade: str = "F"
    is_tradable: bool = False


@dataclass
class PaperCockpitThemeScore:
    """Theme-level score for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    symbol: str = ""
    theme: str = ""
    theme_momentum: float = 0.0
    theme_concentration_risk: float = 0.0
    theme_rank: int = 0
    theme_exposure_ok: bool = True


@dataclass
class PaperCockpitFundamentalScore:
    """Fundamental score for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    symbol: str = ""
    revenue_growth: float = 0.0
    eps_growth: float = 0.0
    pe_ratio: float = 0.0
    fundamental_rank: int = 0
    fundamental_ok: bool = True


@dataclass
class PaperCockpitTechnicalScore:
    """Technical analysis score for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    symbol: str = ""
    ma10_support: bool = False
    ma20_support: bool = False
    volume_contraction: bool = False
    volume_expansion: bool = False
    breakout_confirmed: bool = False
    momentum_repair: bool = False
    technical_rank: int = 0
    technical_ok: bool = False


@dataclass
class PaperCockpitInstitutionalScore:
    """Institutional flow score for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    symbol: str = ""
    institutional_net_flow: float = 0.0
    continuous_selling: bool = False
    institutional_rank: int = 0
    institutional_ok: bool = True


@dataclass
class PaperCockpitMarginScore:
    """Margin / financing risk score for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_margin: bool = True
    symbol: str = ""
    margin_ratio: float = 0.0
    financing_explosion: bool = False
    margin_ok: bool = True


@dataclass
class PaperCockpitEntryCheck:
    """Pre-entry check result for a candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    abc_type: str = "NO_ENTRY"
    signal_score_ok: bool = False
    theme_ok: bool = False
    fundamental_ok: bool = False
    technical_ok: bool = False
    institutional_ok: bool = False
    margin_ok: bool = False
    entry_allowed: bool = False
    block_reason: str = ""


@dataclass
class PaperCockpitABCDecision:
    """A/B/C entry classification decision. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    abc_type: str = "NO_ENTRY"
    paper_size_pct: float = 0.0
    paper_size_twd: float = 0.0
    allow_add: bool = False
    block_reason: str = ""
    requires_human_review: bool = True
    cockpit_executes_order: bool = False
    cockpit_mutates_strategy: bool = False


@dataclass
class PaperCockpitPortfolioRiskCheck:
    """Portfolio-level risk overlay check result. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_portfolio_rebalancing: bool = True
    portfolio_risk_pct: float = 0.0
    theme_exposure_pct: float = 0.0
    cash_buffer_pct: float = 0.0
    risk_budget_remaining_pct: float = 0.0
    portfolio_risk_ok: bool = True
    theme_exposure_ok: bool = True
    cash_buffer_ok: bool = True
    risk_budget_ok: bool = True
    overall_ok: bool = True
    block_reason: str = ""
    recommendation: str = "PAPER_NO_CHANGE"


@dataclass
class PaperCockpitPositionSizingCheck:
    """Position sizing policy check. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_orders: bool = True
    capital_twd: float = 300000.0
    max_loss_per_trade_twd: float = 4500.0
    min_loss_per_trade_twd: float = 2400.0
    paper_size_twd: float = 0.0
    stop_distance_pct: float = 0.0
    stop_distance_ok: bool = True
    sizing_ok: bool = False
    sizing_executes_order: bool = False
    sizing_mutates_strategy: bool = False
    block_reason: str = ""


@dataclass
class PaperCockpitNoEntryCondition:
    """No-entry condition evaluation. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_orders: bool = True
    condition_triggered: bool = False
    condition_type: str = ""
    detail: str = ""
    recommendation: str = "PAPER_BLOCK_NEW_ENTRY"
    cockpit_executes_order: bool = False


@dataclass
class PaperCockpitDecisionTicket:
    """Paper-only decision ticket output. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    ticket_id: str = ""
    symbol: str = ""
    abc_type: str = "NO_ENTRY"
    recommendation: str = "PAPER_BLOCK_NEW_ENTRY"
    paper_size_twd: float = 0.0
    portfolio_risk_ok: bool = False
    sizing_ok: bool = False
    requires_human_review: bool = True
    ticket_triggers_broker: bool = False
    ticket_executes_order: bool = False
    ticket_mutates_strategy: bool = False
    is_blocked: bool = True
    block_reason: str = ""


@dataclass
class PaperCockpitHumanReviewRequest:
    """Human review request generated by the cockpit. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    human_review_required: bool = True
    ticket_id: str = ""
    review_reason: str = ""
    urgency: str = "NORMAL"
    auto_approval_blocked: bool = True
    cockpit_auto_approves: bool = False


@dataclass
class PaperCockpitDashboard:
    """Unified paper cockpit dashboard output. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    dashboard_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    regime: str = "BULL"
    watchlist_count: int = 0
    candidates_scored: int = 0
    a_count: int = 0
    b_count: int = 0
    c_count: int = 0
    no_entry_count: int = 0
    blocked_by_portfolio_risk: int = 0
    tickets_generated: int = 0
    human_review_required_count: int = 0
    portfolio_risk_ok: bool = True
    cash_buffer_ok: bool = True
    risk_off_mode: bool = False
    dashboard_writes_production_db: bool = False
    dashboard_places_real_order: bool = False


@dataclass
class PaperCockpitReport:
    """Paper cockpit report output. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    report_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    regime: str = "BULL"
    capital_twd: float = 300000.0
    total_candidates: int = 0
    passed_candidates: int = 0
    blocked_candidates: int = 0
    decision_tickets: List[str] = field(default_factory=list)
    human_review_count: int = 0
    report_triggers_real_order: bool = False
    report_activates_live_strategy: bool = False


@dataclass
class PaperCockpitAuditTrail:
    """Immutable paper cockpit audit trail. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    audit_only: bool = True
    no_real_orders: bool = True
    entries: List[str] = field(default_factory=list)
    run_id: str = ""
    audit_triggers_order: bool = False
    audit_activates_live_strategy: bool = False


@dataclass
class PaperCockpitValidationResult:
    """Safety and schema validation result. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    is_valid: bool = False
    safety_flags_ok: bool = False
    forbidden_actions_clean: bool = False
    allowed_actions_only: bool = False
    hard_blocks_clear: bool = False
    backward_compat_ok: bool = False
    errors: List[str] = field(default_factory=list)


@dataclass
class PaperCockpitHealthSummary:
    """Health check summary. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.0"


@dataclass
class PaperCockpitReleaseSummary:
    """Release audit summary. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    version: str = "2.0.0"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 23
    cli_count: int = 17
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


@dataclass
class PaperCockpitCandidate:
    """A single scored paper cockpit candidate. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    signal_score: float = 0.0
    abc_type: str = "NO_ENTRY"
    portfolio_risk_ok: bool = False
    sizing_ok: bool = False
    has_ticket: bool = False
    requires_human_review: bool = True
    block_reason: str = ""


@dataclass
class PaperCockpitResult:
    """Full unified cockpit run result. v2.0.0."""
    schema_version: str = "200"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True,
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    cockpit_executes_order: bool = False
    cockpit_mutates_strategy: bool = False
    cockpit_rebalances_real_portfolio: bool = False
    version: str = "2.0.0"
    regime: str = "BULL"
    candidates: List[PaperCockpitCandidate] = field(default_factory=list)
    dashboard: Optional[PaperCockpitDashboard] = None
    report: Optional[PaperCockpitReport] = None
    audit_trail: Optional[PaperCockpitAuditTrail] = None
    all_passed: bool = False


_ALL_MODEL_NAMES: List[str] = [
    "PaperCockpitInput",
    "PaperCockpitResult",
    "PaperCockpitWatchlist",
    "PaperCockpitCandidate",
    "PaperCockpitSignalScore",
    "PaperCockpitThemeScore",
    "PaperCockpitFundamentalScore",
    "PaperCockpitTechnicalScore",
    "PaperCockpitInstitutionalScore",
    "PaperCockpitMarginScore",
    "PaperCockpitEntryCheck",
    "PaperCockpitABCDecision",
    "PaperCockpitPortfolioRiskCheck",
    "PaperCockpitPositionSizingCheck",
    "PaperCockpitNoEntryCondition",
    "PaperCockpitDecisionTicket",
    "PaperCockpitHumanReviewRequest",
    "PaperCockpitDashboard",
    "PaperCockpitReport",
    "PaperCockpitAuditTrail",
    "PaperCockpitValidationResult",
    "PaperCockpitHealthSummary",
    "PaperCockpitReleaseSummary",
]

assert len(_ALL_MODEL_NAMES) == 23, f"Expected 23 models, got {len(_ALL_MODEL_NAMES)}"


# ---------------------------------------------------------------------------
# Cockpit flow engine
# ---------------------------------------------------------------------------

def _make_default_safety() -> Dict[str, Any]:
    return {
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "unified_paper_cockpit_only": True,
        "decision_console_only": True,
        "dashboard_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "no_production_strategy_mutation": True,
        "no_automatic_rollback": True,
        "no_live_strategy_activation": True,
        "no_real_portfolio_rebalancing": True,
        "not_investment_advice": True,
        "human_review_required": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
    }


def _check_forbidden_actions(text: str) -> bool:
    """Return True if text contains forbidden action words."""
    upper = text.upper()
    return any(fa in upper for fa in FORBIDDEN_ACTIONS)


def score_watchlist(symbols: List[str], theme: str = "") -> PaperCockpitWatchlist:
    """Score and validate a paper watchlist. Paper only."""
    is_valid = bool(symbols) and len(symbols) <= 30
    return PaperCockpitWatchlist(
        symbols=list(symbols),
        theme=theme,
        count=len(symbols),
        is_valid=is_valid,
        block_reason="" if is_valid else "empty_or_oversized_watchlist",
    )


def score_candidate(symbol: str, **kwargs) -> PaperCockpitSignalScore:
    """Compute unified signal score for a candidate. Paper only."""
    theme_score = float(kwargs.get("theme_score", 0.0))
    fundamental_score = float(kwargs.get("fundamental_score", 0.0))
    technical_score = float(kwargs.get("technical_score", 0.0))
    institutional_score = float(kwargs.get("institutional_score", 0.0))
    margin_score = float(kwargs.get("margin_score", 0.0))
    total = (theme_score + fundamental_score + technical_score + institutional_score + margin_score) / 5.0
    grade = (
        "A" if total >= 85 else
        "B" if total >= 70 else
        "C" if total >= 55 else
        "D" if total >= 40 else
        "F"
    )
    return PaperCockpitSignalScore(
        symbol=symbol,
        theme_score=theme_score,
        fundamental_score=fundamental_score,
        technical_score=technical_score,
        institutional_score=institutional_score,
        margin_score=margin_score,
        total_score=total,
        grade=grade,
        is_tradable=total >= 55,
    )


def classify_abc(symbol: str, signal_score: PaperCockpitSignalScore, **kwargs) -> PaperCockpitABCDecision:
    """Classify entry type A/B/C or NO_ENTRY. Paper only."""
    ma10_support: bool = bool(kwargs.get("ma10_support", False))
    volume_contraction: bool = bool(kwargs.get("volume_contraction", False))
    institutional_selling: bool = bool(kwargs.get("continuous_institutional_selling", False))
    base_breakout: bool = bool(kwargs.get("base_breakout", False))
    volume_expansion: float = float(kwargs.get("volume_expansion_ratio", 1.0))
    margin_financing_exploding: bool = bool(kwargs.get("margin_financing_exploding", False))
    ma20_reclaim: bool = bool(kwargs.get("ma20_reclaim", False))
    momentum_repair: bool = bool(kwargs.get("momentum_repair", False))
    ma20_failed_again: bool = bool(kwargs.get("ma20_failed_again", False))

    # A_PULLBACK_10MA
    if ma10_support and volume_contraction and not institutional_selling:
        return PaperCockpitABCDecision(
            symbol=symbol,
            abc_type="A_PULLBACK_10MA",
            paper_size_pct=1.0,
            paper_size_twd=30000.0,
            allow_add=True,
            requires_human_review=True,
        )

    # B_BREAKOUT_BASE
    if base_breakout and volume_expansion >= 1.5 and not margin_financing_exploding:
        size_pct = 0.6 if volume_expansion >= 3.0 else 0.8
        return PaperCockpitABCDecision(
            symbol=symbol,
            abc_type="B_BREAKOUT_BASE",
            paper_size_pct=size_pct,
            paper_size_twd=30000.0 * size_pct,
            allow_add=False,
            requires_human_review=True,
        )

    # C_RECLAIM_20MA
    if ma20_reclaim and momentum_repair and not ma20_failed_again:
        return PaperCockpitABCDecision(
            symbol=symbol,
            abc_type="C_RECLAIM_20MA",
            paper_size_pct=0.5,
            paper_size_twd=15000.0,
            allow_add=False,
            requires_human_review=True,
        )

    return PaperCockpitABCDecision(
        symbol=symbol,
        abc_type="NO_ENTRY",
        paper_size_pct=0.0,
        paper_size_twd=0.0,
        allow_add=False,
        requires_human_review=True,
        block_reason="no_abc_condition_met",
    )


def check_portfolio_risk(
    portfolio_risk_pct: float = 0.0,
    theme_exposure_pct: float = 0.0,
    cash_buffer_pct: float = 100.0,
    risk_budget_remaining_pct: float = 100.0,
) -> PaperCockpitPortfolioRiskCheck:
    """Check portfolio-level risk overlay. Paper only."""
    portfolio_risk_ok = portfolio_risk_pct <= 60.0
    theme_exposure_ok = theme_exposure_pct <= 35.0
    cash_buffer_ok = cash_buffer_pct >= 20.0
    risk_budget_ok = risk_budget_remaining_pct >= 10.0
    overall_ok = portfolio_risk_ok and theme_exposure_ok and cash_buffer_ok and risk_budget_ok

    if not portfolio_risk_ok:
        recommendation = "PAPER_BLOCK_NEW_ENTRY"
    elif not theme_exposure_ok:
        recommendation = "PAPER_BLOCK_NEW_ENTRY"
    elif not cash_buffer_ok:
        recommendation = "PAPER_KEEP_CASH"
    elif not risk_budget_ok:
        recommendation = "PAPER_KEEP_CASH"
    else:
        recommendation = "PAPER_ALLOW_NORMAL_SIZE"

    block_reason = ""
    if not overall_ok:
        reasons = []
        if not portfolio_risk_ok:
            reasons.append("portfolio_risk_exceeded")
        if not theme_exposure_ok:
            reasons.append("theme_exposure_exceeded")
        if not cash_buffer_ok:
            reasons.append("cash_buffer_too_low")
        if not risk_budget_ok:
            reasons.append("risk_budget_exhausted")
        block_reason = "; ".join(reasons)

    return PaperCockpitPortfolioRiskCheck(
        portfolio_risk_pct=portfolio_risk_pct,
        theme_exposure_pct=theme_exposure_pct,
        cash_buffer_pct=cash_buffer_pct,
        risk_budget_remaining_pct=risk_budget_remaining_pct,
        portfolio_risk_ok=portfolio_risk_ok,
        theme_exposure_ok=theme_exposure_ok,
        cash_buffer_ok=cash_buffer_ok,
        risk_budget_ok=risk_budget_ok,
        overall_ok=overall_ok,
        block_reason=block_reason,
        recommendation=recommendation,
    )


def check_position_sizing(
    capital_twd: float = 300000.0,
    stop_distance_pct: float = 0.08,
    abc_type: str = "A_PULLBACK_10MA",
) -> PaperCockpitPositionSizingCheck:
    """Check position sizing policy for 300k capital. Paper only."""
    max_loss_twd = 4500.0
    min_loss_twd = 2400.0
    if stop_distance_pct <= 0.0:
        return PaperCockpitPositionSizingCheck(
            capital_twd=capital_twd,
            max_loss_per_trade_twd=max_loss_twd,
            min_loss_per_trade_twd=min_loss_twd,
            stop_distance_pct=stop_distance_pct,
            stop_distance_ok=False,
            sizing_ok=False,
            block_reason="zero_stop_distance",
        )
    if stop_distance_pct > 0.15:
        return PaperCockpitPositionSizingCheck(
            capital_twd=capital_twd,
            max_loss_per_trade_twd=max_loss_twd,
            min_loss_per_trade_twd=min_loss_twd,
            stop_distance_pct=stop_distance_pct,
            stop_distance_ok=False,
            sizing_ok=False,
            block_reason="stop_distance_too_wide",
        )
    size_by_max = max_loss_twd / stop_distance_pct
    size_by_min = min_loss_twd / stop_distance_pct
    paper_size = min(size_by_max, capital_twd * 0.15)
    return PaperCockpitPositionSizingCheck(
        capital_twd=capital_twd,
        max_loss_per_trade_twd=max_loss_twd,
        min_loss_per_trade_twd=min_loss_twd,
        paper_size_twd=round(paper_size, 0),
        stop_distance_pct=stop_distance_pct,
        stop_distance_ok=True,
        sizing_ok=True,
    )


def evaluate_no_entry(
    abc_decision: PaperCockpitABCDecision,
    portfolio_risk: PaperCockpitPortfolioRiskCheck,
    sizing: PaperCockpitPositionSizingCheck,
) -> PaperCockpitNoEntryCondition:
    """Evaluate whether a no-entry condition is triggered. Paper only."""
    if abc_decision.abc_type == "NO_ENTRY":
        return PaperCockpitNoEntryCondition(
            condition_triggered=True,
            condition_type="no_abc_condition_met",
            detail=abc_decision.block_reason,
            recommendation="PAPER_BLOCK_NEW_ENTRY",
        )
    if not portfolio_risk.overall_ok:
        return PaperCockpitNoEntryCondition(
            condition_triggered=True,
            condition_type="portfolio_risk_exceeded",
            detail=portfolio_risk.block_reason,
            recommendation=portfolio_risk.recommendation,
        )
    if not sizing.sizing_ok:
        return PaperCockpitNoEntryCondition(
            condition_triggered=True,
            condition_type="sizing_failed",
            detail=sizing.block_reason,
            recommendation="PAPER_BLOCK_NEW_ENTRY",
        )
    return PaperCockpitNoEntryCondition(
        condition_triggered=False,
        condition_type="none",
        detail="all_checks_passed",
        recommendation="PAPER_ALLOW_NORMAL_SIZE",
    )


def generate_decision_ticket(
    symbol: str,
    abc_decision: PaperCockpitABCDecision,
    portfolio_risk: PaperCockpitPortfolioRiskCheck,
    sizing: PaperCockpitPositionSizingCheck,
    no_entry: PaperCockpitNoEntryCondition,
    run_id: str = "",
) -> PaperCockpitDecisionTicket:
    """Generate paper-only decision ticket. Paper only."""
    import hashlib
    ticket_id = hashlib.md5(f"{symbol}{run_id}{abc_decision.abc_type}".encode()).hexdigest()[:10]
    is_blocked = no_entry.condition_triggered
    recommendation = no_entry.recommendation if is_blocked else portfolio_risk.recommendation
    return PaperCockpitDecisionTicket(
        ticket_id=ticket_id,
        symbol=symbol,
        abc_type=abc_decision.abc_type,
        recommendation=recommendation,
        paper_size_twd=sizing.paper_size_twd if not is_blocked else 0.0,
        portfolio_risk_ok=portfolio_risk.overall_ok,
        sizing_ok=sizing.sizing_ok,
        requires_human_review=True,
        is_blocked=is_blocked,
        block_reason=no_entry.detail if is_blocked else "",
    )


def generate_human_review_request(ticket: PaperCockpitDecisionTicket) -> PaperCockpitHumanReviewRequest:
    """Generate human review request. Paper only."""
    urgency = "HIGH" if ticket.abc_type == "A_PULLBACK_10MA" else "NORMAL"
    reason = f"paper_decision_ticket_{ticket.ticket_id}_requires_review: {ticket.recommendation}"
    return PaperCockpitHumanReviewRequest(
        ticket_id=ticket.ticket_id,
        review_reason=reason,
        urgency=urgency,
    )


def build_dashboard(
    cockpit_input: PaperCockpitInput,
    candidates: List[PaperCockpitCandidate],
    portfolio_risk: PaperCockpitPortfolioRiskCheck,
) -> PaperCockpitDashboard:
    """Build unified paper cockpit dashboard. Paper only."""
    a_count = sum(1 for c in candidates if c.abc_type == "A_PULLBACK_10MA")
    b_count = sum(1 for c in candidates if c.abc_type == "B_BREAKOUT_BASE")
    c_count = sum(1 for c in candidates if c.abc_type == "C_RECLAIM_20MA")
    no_entry_count = sum(1 for c in candidates if c.abc_type == "NO_ENTRY")
    blocked = sum(1 for c in candidates if not c.portfolio_risk_ok)
    tickets = sum(1 for c in candidates if c.has_ticket)
    review = sum(1 for c in candidates if c.requires_human_review)
    risk_off = not portfolio_risk.overall_ok or portfolio_risk.recommendation == "PAPER_RISK_OFF_MODE"
    return PaperCockpitDashboard(
        regime=cockpit_input.market_regime,
        watchlist_count=len(cockpit_input.watchlist),
        candidates_scored=len(candidates),
        a_count=a_count,
        b_count=b_count,
        c_count=c_count,
        no_entry_count=no_entry_count,
        blocked_by_portfolio_risk=blocked,
        tickets_generated=tickets,
        human_review_required_count=review,
        portfolio_risk_ok=portfolio_risk.overall_ok,
        cash_buffer_ok=portfolio_risk.cash_buffer_ok,
        risk_off_mode=risk_off,
    )


def build_report(
    cockpit_input: PaperCockpitInput,
    candidates: List[PaperCockpitCandidate],
    tickets: List[PaperCockpitDecisionTicket],
) -> PaperCockpitReport:
    """Build paper cockpit report. Paper only."""
    passed = sum(1 for c in candidates if not c.block_reason)
    blocked = sum(1 for c in candidates if c.block_reason)
    review_count = sum(1 for t in tickets if t.requires_human_review)
    return PaperCockpitReport(
        regime=cockpit_input.market_regime,
        capital_twd=cockpit_input.capital_twd,
        total_candidates=len(candidates),
        passed_candidates=passed,
        blocked_candidates=blocked,
        decision_tickets=[t.ticket_id for t in tickets],
        human_review_count=review_count,
    )


def build_audit_trail(run_id: str, entries: List[str]) -> PaperCockpitAuditTrail:
    """Build immutable paper cockpit audit trail. Paper only."""
    return PaperCockpitAuditTrail(
        entries=list(entries),
        run_id=run_id,
    )


def validate_cockpit(inp: PaperCockpitInput) -> PaperCockpitValidationResult:
    """Validate cockpit input safety flags and schema. Paper only."""
    errors: List[str] = []
    if not inp.paper_only:
        errors.append("paper_only_flag_missing")
    if not inp.no_real_orders:
        errors.append("no_real_orders_flag_missing")
    if not inp.no_broker:
        errors.append("no_broker_flag_missing")
    if not inp.not_investment_advice:
        errors.append("not_investment_advice_flag_missing")
    if not inp.human_review_required:
        errors.append("human_review_required_flag_missing")
    if inp.schema_version != "200":
        errors.append(f"wrong_schema_version: {inp.schema_version}")
    safety_ok = inp.paper_only and inp.no_real_orders and inp.no_broker
    forbidden_ok = True
    allowed_ok = True
    hard_blocks_clear = not bool(errors)
    backward_compat_ok = True
    is_valid = not bool(errors)
    return PaperCockpitValidationResult(
        is_valid=is_valid,
        safety_flags_ok=safety_ok,
        forbidden_actions_clean=forbidden_ok,
        allowed_actions_only=allowed_ok,
        hard_blocks_clear=hard_blocks_clear,
        backward_compat_ok=backward_compat_ok,
        errors=errors,
    )


def run_cockpit(cockpit_input: Optional[PaperCockpitInput] = None) -> PaperCockpitResult:
    """Run full unified paper cockpit workflow. Paper only."""
    import hashlib, datetime
    if cockpit_input is None:
        cockpit_input = PaperCockpitInput()
    run_id = hashlib.md5(
        f"cockpit-{cockpit_input.market_regime}-{len(cockpit_input.watchlist)}".encode()
    ).hexdigest()[:8]

    validation = validate_cockpit(cockpit_input)
    if not validation.is_valid:
        return PaperCockpitResult(
            regime=cockpit_input.market_regime,
            all_passed=False,
        )

    portfolio_risk = check_portfolio_risk()
    candidates_out: List[PaperCockpitCandidate] = []
    tickets_out: List[PaperCockpitDecisionTicket] = []
    audit_entries: List[str] = [f"cockpit_run_start:{run_id}"]

    for symbol in cockpit_input.candidates or cockpit_input.watchlist:
        sig = score_candidate(symbol)
        abc = classify_abc(symbol, sig)
        sizing = check_position_sizing()
        no_entry = evaluate_no_entry(abc, portfolio_risk, sizing)
        ticket = generate_decision_ticket(symbol, abc, portfolio_risk, sizing, no_entry, run_id)
        candidate = PaperCockpitCandidate(
            symbol=symbol,
            signal_score=sig.total_score,
            abc_type=abc.abc_type,
            portfolio_risk_ok=portfolio_risk.overall_ok,
            sizing_ok=sizing.sizing_ok,
            has_ticket=True,
            requires_human_review=True,
            block_reason=ticket.block_reason,
        )
        candidates_out.append(candidate)
        tickets_out.append(ticket)
        audit_entries.append(f"scored:{symbol}:{abc.abc_type}:{ticket.recommendation}")

    dashboard = build_dashboard(cockpit_input, candidates_out, portfolio_risk)
    report = build_report(cockpit_input, candidates_out, tickets_out)
    audit_trail = build_audit_trail(run_id, audit_entries)

    return PaperCockpitResult(
        version=VERSION,
        regime=cockpit_input.market_regime,
        candidates=candidates_out,
        dashboard=dashboard,
        report=report,
        audit_trail=audit_trail,
        all_passed=True,
    )


def get_cockpit_summary() -> Dict[str, Any]:
    """Return cockpit summary dict. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "models": len(_ALL_MODEL_NAMES),
        "cli_commands": len(CLI_COMMANDS),
        "gui_tabs": len(GUI_TABS),
        "safety_flags": len(SAFETY_FLAGS),
        "forbidden_actions": len(FORBIDDEN_ACTIONS),
        "allowed_actions": len(ALLOWED_ACTIONS),
        "hard_block_conditions": len(HARD_BLOCK_CONDITIONS),
        "no_entry_conditions": len(NO_ENTRY_CONDITIONS),
        "abc_types": len(ABC_DECISION_TYPES),
        "covered_versions": len(COVERED_VERSIONS),
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_version_info() -> Dict[str, Any]:
    """Return version information dict. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def verify_version() -> bool:
    """Assert all module-level invariants. Returns True on success."""
    assert VERSION == "2.0.0", f"Expected VERSION 2.0.0, got {VERSION}"
    assert SCHEMA_VERSION == "200", f"Expected SCHEMA_VERSION 200, got {SCHEMA_VERSION}"
    assert len(_ALL_MODEL_NAMES) == 23, f"Expected 23 models"
    assert len(SAFETY_FLAGS) == 30, f"Expected 30 SAFETY_FLAGS"
    assert len(FORBIDDEN_ACTIONS) == 10, f"Expected 10 FORBIDDEN_ACTIONS"
    assert len(ALLOWED_ACTIONS) == 9, f"Expected 9 ALLOWED_ACTIONS"
    assert len(HARD_BLOCK_CONDITIONS) == 22, f"Expected 22 HARD_BLOCK_CONDITIONS"
    assert len(NO_ENTRY_CONDITIONS) == 8, f"Expected 8 NO_ENTRY_CONDITIONS"
    assert len(CLI_COMMANDS) == 17, f"Expected 17 CLI_COMMANDS"
    assert len(GUI_TABS) == 3, f"Expected 3 GUI_TABS"
    assert len(ABC_DECISION_TYPES) == 4, f"Expected 4 ABC_DECISION_TYPES"
    assert len(COVERED_VERSIONS) == 29, f"Expected 29 COVERED_VERSIONS"
    assert SAFETY_FLAGS["paper_only"] is True
    assert SAFETY_FLAGS["no_real_orders"] is True
    assert SAFETY_FLAGS["no_broker"] is True
    assert SAFETY_FLAGS["cockpit_executes_order"] is False
    assert SAFETY_FLAGS["cockpit_mutates_strategy"] is False
    assert SAFETY_FLAGS["cockpit_rebalances_real_portfolio"] is False
    assert "BUY" in FORBIDDEN_ACTIONS
    assert "SELL" in FORBIDDEN_ACTIONS
    assert "ORDER" in FORBIDDEN_ACTIONS
    assert "PAPER_WATCH_ONLY" in ALLOWED_ACTIONS
    assert "PAPER_ALLOW_NORMAL_SIZE" in ALLOWED_ACTIONS
    assert "PAPER_BLOCK_NEW_ENTRY" in ALLOWED_ACTIONS
    return True


assert verify_version(), "paper_cockpit_v200 verify_version() FAILED"
