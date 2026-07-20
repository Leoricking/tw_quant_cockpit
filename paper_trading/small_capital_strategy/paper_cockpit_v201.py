"""
paper_trading/small_capital_strategy/paper_cockpit_v201.py
v2.0.1 Paper Cockpit Usability & Daily Workflow Hardening
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
[!] Daily Workflow Hardening. No-Entry Reason Strengthening. Enhanced Decision Ticket.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

VERSION = "2.0.1"
SCHEMA_VERSION = "201"
RELEASE_NAME = "Paper Cockpit Usability & Daily Workflow Hardening"
BASELINE_TESTS = 32425
MIN_NEW_TESTS = 300

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

NO_ENTRY_REASONS: List[str] = [
    "trend_broken",
    "below_20ma",
    "below_60ma",
    "volume_overheated",
    "volume_dry_up_failed",
    "institutional_selling",
    "margin_overheated",
    "market_risk_high",
    "risk_budget_exceeded",
    "position_size_too_large",
    "stop_loss_too_wide",
    "missing_required_signal",
    "human_review_required",
]

assert len(NO_ENTRY_REASONS) == 13, f"Expected 13 NO_ENTRY_REASONS, got {len(NO_ENTRY_REASONS)}"

DAILY_FINAL_ACTIONS: List[str] = [
    "WATCH",
    "WAIT",
    "PAPER_BUY_PLAN",
    "PAPER_ADD_PLAN",
    "PAPER_REDUCE_PLAN",
    "PAPER_EXIT_PLAN",
    "NO_ENTRY",
]

assert len(DAILY_FINAL_ACTIONS) == 7, f"Expected 7 DAILY_FINAL_ACTIONS, got {len(DAILY_FINAL_ACTIONS)}"

CLI_COMMANDS_V201: List[str] = [
    "paper-cockpit-daily-workflow",
    "paper-cockpit-no-entry-reason",
    "paper-cockpit-final-action",
    "paper-cockpit-candidate-rank",
    "paper-cockpit-risk-budget-status",
    "paper-cockpit-cli-display",
    "paper-cockpit-version-201",
    "paper-cockpit-health-201",
    "paper-cockpit-gate-201",
    "paper-cockpit-safety-audit-201",
]

assert len(CLI_COMMANDS_V201) == 10, f"Expected 10 CLI_COMMANDS_V201, got {len(CLI_COMMANDS_V201)}"

GUI_TABS_V201: List[str] = [
    "daily_workflow_v201",
    "no_entry_reason_detail",
    "decision_ticket_v201",
]

assert len(GUI_TABS_V201) == 3, f"Expected 3 GUI_TABS_V201, got {len(GUI_TABS_V201)}"

ENHANCED_TICKET_FIELDS: List[str] = [
    "symbol",
    "name",
    "setup_type",
    "theme_score",
    "fundamental_score",
    "technical_score",
    "volume_score",
    "chip_score",
    "margin_score",
    "total_score",
    "entry_price_plan",
    "add_price_plan",
    "reduce_price_plan",
    "exit_price_plan",
    "stop_loss_price",
    "invalid_conditions",
    "risk_amount",
    "max_position_size",
    "position_size_reason",
    "no_entry_reasons",
    "human_review_required",
    "final_action",
]

assert len(ENHANCED_TICKET_FIELDS) == 22, f"Expected 22 ENHANCED_TICKET_FIELDS, got {len(ENHANCED_TICKET_FIELDS)}"

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
]

assert len(FORBIDDEN_ACTIONS) == 9, f"Expected 9 FORBIDDEN_ACTIONS, got {len(FORBIDDEN_ACTIONS)}"

SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "daily_workflow_hardening": True,
    "no_entry_reason_strengthening": True,
    "enhanced_decision_ticket": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "production_trading_blocked": True,
    "broker_execution_enabled": False,
    "cockpit_executes_order": False,
    "cockpit_mutates_strategy": False,
    "cockpit_rebalances_real_portfolio": False,
    "no_automatic_rebalance": True,
    "no_real_account_sync": True,
}

assert len(SAFETY_FLAGS) == 20, f"Expected 20 SAFETY_FLAGS, got {len(SAFETY_FLAGS)}"

COVERED_VERSIONS: List[str] = [
    "1.7.0", "1.7.1", "1.7.2", "1.7.3", "1.7.5", "1.7.6",
    "1.7.7", "1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2",
    "1.8.3", "1.8.4", "1.8.6", "1.8.7", "1.8.8", "1.8.9",
    "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5",
    "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0",
]

assert len(COVERED_VERSIONS) == 30, f"Expected 30 COVERED_VERSIONS, got {len(COVERED_VERSIONS)}"


# ---------------------------------------------------------------------------
# Dataclasses — 12 new models, schema_version="201"
# ---------------------------------------------------------------------------

@dataclass
class DailyWorkflowInput:
    """Daily workflow input with schema_version='201'. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    capital_twd: float = 300000.0
    market_regime: str = "BULL"
    candidates: List[str] = field(default_factory=list)
    watchlist: List[str] = field(default_factory=list)
    portfolio_risk_pct: float = 0.0
    risk_budget_remaining_pct: float = 100.0
    theme: str = ""
    run_date: str = ""


@dataclass
class CandidateRankEntry:
    """Ranked candidate with final_action field. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    rank: int = 0
    total_score: float = 0.0
    abc_type: str = "NO_ENTRY"
    final_action: str = "NO_ENTRY"
    entry_allowed: bool = False
    block_reason: str = ""
    human_review_required: bool = True


@dataclass
class NoEntryReasonDetail:
    """Structured no-entry reason with reason_code from NO_ENTRY_REASONS. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    reason_code: str = ""
    reason_label: str = ""
    detail: str = ""
    severity: str = "HIGH"
    recommendation: str = "PAPER_BLOCK_NEW_ENTRY"
    is_valid_reason: bool = False

    def __post_init__(self) -> None:
        self.is_valid_reason = self.reason_code in NO_ENTRY_REASONS


@dataclass
class EnhancedDecisionTicket:
    """Enhanced decision ticket with all 21 required fields. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    # 21 required fields
    symbol: str = ""
    name: str = ""
    setup_type: str = "NO_ENTRY"
    theme_score: float = 0.0
    fundamental_score: float = 0.0
    technical_score: float = 0.0
    volume_score: float = 0.0
    chip_score: float = 0.0
    margin_score: float = 0.0
    total_score: float = 0.0
    entry_price_plan: float = 0.0
    add_price_plan: float = 0.0
    reduce_price_plan: float = 0.0
    exit_price_plan: float = 0.0
    stop_loss_price: float = 0.0
    invalid_conditions: List[str] = field(default_factory=list)
    risk_amount: float = 0.0
    max_position_size: float = 0.0
    position_size_reason: str = ""
    no_entry_reasons: List[str] = field(default_factory=list)
    human_review_required: bool = True
    final_action: str = "NO_ENTRY"
    # safety
    ticket_triggers_broker: bool = False
    ticket_executes_order: bool = False


@dataclass
class RiskBudgetStatus:
    """Risk budget usage display. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    portfolio_risk_pct: float = 0.0
    risk_budget_remaining_pct: float = 100.0
    risk_budget_used_pct: float = 0.0
    risk_budget_ok: bool = True
    status_label: str = "NORMAL"
    recommendation: str = "PAPER_ALLOW_NORMAL_SIZE"
    human_review_required: bool = True


@dataclass
class CLIDisplayRow:
    """One row for CLI display. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    symbol: str = ""
    name: str = ""
    setup_type: str = ""
    abc_status: str = ""
    entry_allowed: bool = False
    blocked_reason: str = ""
    risk_budget_used_pct: float = 0.0
    suggested_paper_action: str = "NO_ENTRY"
    human_review_flag: bool = True


@dataclass
class CLIDisplayOutput:
    """Full CLI display output. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    top_candidates: List[CLIDisplayRow] = field(default_factory=list)
    total_candidates: int = 0
    watch_count: int = 0
    wait_count: int = 0
    paper_buy_plan_count: int = 0
    paper_add_plan_count: int = 0
    paper_reduce_plan_count: int = 0
    paper_exit_plan_count: int = 0
    no_entry_count: int = 0
    human_review_required: bool = True


@dataclass
class DailyWorkflowCandidateResult:
    """Per-candidate daily workflow output. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    watchlist_summary: str = ""
    candidate_rank: int = 0
    abc_type: str = "NO_ENTRY"
    no_entry_reasons: List[NoEntryReasonDetail] = field(default_factory=list)
    risk_overlay_status: str = "BLOCKED"
    position_sizing_suggestion: str = ""
    paper_decision_ticket: Optional[EnhancedDecisionTicket] = None
    human_review_requirement: bool = True
    final_action: str = "NO_ENTRY"


@dataclass
class DailyWorkflowSummary:
    """Aggregate daily workflow summary. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    no_real_orders: bool = True
    total_candidates: int = 0
    watch_count: int = 0
    wait_count: int = 0
    paper_buy_plan_count: int = 0
    paper_add_plan_count: int = 0
    paper_reduce_plan_count: int = 0
    paper_exit_plan_count: int = 0
    no_entry_count: int = 0
    human_review_count: int = 0
    all_passed_safety: bool = True


@dataclass
class DailyWorkflowResult:
    """Full daily workflow run result. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    cockpit_executes_order: bool = False
    version: str = "2.0.1"
    market_regime: str = "BULL"
    candidate_results: List[DailyWorkflowCandidateResult] = field(default_factory=list)
    candidate_ranking: List[CandidateRankEntry] = field(default_factory=list)
    summary: Optional[DailyWorkflowSummary] = None
    cli_display: Optional[CLIDisplayOutput] = None
    all_passed: bool = False


@dataclass
class V201HealthSummary:
    """Health summary for v2.0.1. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.1"
    no_entry_reasons_count: int = 13
    enhanced_ticket_fields_count: int = 22
    daily_final_actions_count: int = 7


@dataclass
class V201ReleaseSummary:
    """Release summary for v2.0.1. v2.0.1."""
    schema_version: str = "201"
    paper_only: bool = True
    version: str = "2.0.1"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 12
    cli_count: int = 10
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    no_entry_reasons_count: int = 13
    daily_final_actions_count: int = 7
    enhanced_ticket_fields_count: int = 22
    all_sealed: bool = False


_ALL_MODEL_NAMES_V201: List[str] = [
    "DailyWorkflowInput",
    "CandidateRankEntry",
    "NoEntryReasonDetail",
    "EnhancedDecisionTicket",
    "RiskBudgetStatus",
    "CLIDisplayRow",
    "CLIDisplayOutput",
    "DailyWorkflowCandidateResult",
    "DailyWorkflowSummary",
    "DailyWorkflowResult",
    "V201HealthSummary",
    "V201ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V201) == 12, f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V201)}"


# ---------------------------------------------------------------------------
# Core engine functions
# ---------------------------------------------------------------------------

def _check_forbidden_words(text: str) -> bool:
    """Return True if text contains forbidden action words."""
    upper = text.upper()
    for fa in FORBIDDEN_ACTIONS:
        if fa in upper:
            return True
    return False


def evaluate_no_entry_reasons(
    technical_data: Optional[Dict[str, Any]] = None,
    risk_data: Optional[Dict[str, Any]] = None,
) -> List[NoEntryReasonDetail]:
    """Evaluate and return list of NoEntryReasonDetail for a candidate."""
    if technical_data is None:
        technical_data = {}
    if risk_data is None:
        risk_data = {}

    reasons: List[NoEntryReasonDetail] = []

    # trend checks
    if technical_data.get("trend_broken", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="trend_broken",
            reason_label="Trend Broken",
            detail="Price trend has broken below key support",
            severity="HIGH",
        ))
    if technical_data.get("below_20ma", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="below_20ma",
            reason_label="Below 20MA",
            detail="Price is below the 20-day moving average",
            severity="MEDIUM",
        ))
    if technical_data.get("below_60ma", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="below_60ma",
            reason_label="Below 60MA",
            detail="Price is below the 60-day moving average",
            severity="HIGH",
        ))
    # volume checks
    if technical_data.get("volume_overheated", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="volume_overheated",
            reason_label="Volume Overheated",
            detail="Trading volume is excessively elevated indicating potential distribution",
            severity="MEDIUM",
        ))
    if technical_data.get("volume_dry_up_failed", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="volume_dry_up_failed",
            reason_label="Volume Dry-Up Failed",
            detail="Expected volume contraction did not materialize",
            severity="MEDIUM",
        ))
    # chip checks
    if technical_data.get("institutional_selling", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="institutional_selling",
            reason_label="Institutional Selling",
            detail="Continuous institutional net selling detected",
            severity="HIGH",
        ))
    if technical_data.get("margin_overheated", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="margin_overheated",
            reason_label="Margin Overheated",
            detail="Margin financing ratio is excessively high",
            severity="HIGH",
        ))
    # risk checks
    if risk_data.get("market_risk_high", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="market_risk_high",
            reason_label="Market Risk High",
            detail="Overall market risk level is elevated",
            severity="HIGH",
        ))
    if risk_data.get("risk_budget_exceeded", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="risk_budget_exceeded",
            reason_label="Risk Budget Exceeded",
            detail="Portfolio risk budget has been exhausted",
            severity="HIGH",
        ))
    if risk_data.get("position_size_too_large", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="position_size_too_large",
            reason_label="Position Size Too Large",
            detail="Suggested position size exceeds maximum allowed",
            severity="MEDIUM",
        ))
    if risk_data.get("stop_loss_too_wide", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="stop_loss_too_wide",
            reason_label="Stop Loss Too Wide",
            detail="Required stop distance exceeds policy limit",
            severity="MEDIUM",
        ))
    # signal checks
    if technical_data.get("missing_required_signal", False):
        reasons.append(NoEntryReasonDetail(
            reason_code="missing_required_signal",
            reason_label="Missing Required Signal",
            detail="One or more required entry signals are absent",
            severity="HIGH",
        ))
    # always last: human review
    reasons.append(NoEntryReasonDetail(
        reason_code="human_review_required",
        reason_label="Human Review Required",
        detail="All paper decisions require human review before action",
        severity="INFO",
        recommendation="PAPER_REQUIRE_HUMAN_REVIEW",
    ))

    return reasons


def classify_final_action(
    candidate: str,
    abc_type: str,
    no_entry_reasons: List[str],
    risk_ok: bool,
    sizing_ok: bool,
    has_position: bool = False,
    position_profit_pct: float = 0.0,
) -> str:
    """Classify the final daily action from DAILY_FINAL_ACTIONS. Returns one of 7 actions."""
    # Blocking no-entry reasons (excluding human_review_required which is always present)
    blocking_reasons = [r for r in no_entry_reasons if r != "human_review_required"]

    if blocking_reasons:
        return "NO_ENTRY"

    if not risk_ok or not sizing_ok:
        return "NO_ENTRY"

    if abc_type == "NO_ENTRY":
        # Has position — decide reduce or exit or watch
        if has_position:
            if position_profit_pct >= 0.25:
                return "PAPER_REDUCE_PLAN"
            elif position_profit_pct <= -0.08:
                return "PAPER_EXIT_PLAN"
            else:
                return "WATCH"
        return "WAIT"

    # Valid ABC entry
    if abc_type in ("A_PULLBACK_10MA", "B_BREAKOUT_BASE", "C_RECLAIM_20MA"):
        if has_position:
            return "PAPER_ADD_PLAN"
        return "PAPER_BUY_PLAN"

    return "WAIT"


def get_risk_budget_status(
    portfolio_risk_pct: float = 0.0,
    risk_budget_remaining_pct: float = 100.0,
) -> RiskBudgetStatus:
    """Return RiskBudgetStatus for display. Paper only."""
    risk_budget_used_pct = 100.0 - risk_budget_remaining_pct
    risk_budget_ok = risk_budget_remaining_pct >= 10.0

    if risk_budget_remaining_pct >= 50.0:
        status_label = "NORMAL"
        recommendation = "PAPER_ALLOW_NORMAL_SIZE"
    elif risk_budget_remaining_pct >= 20.0:
        status_label = "CAUTION"
        recommendation = "PAPER_ALLOW_REDUCED_SIZE"
    elif risk_budget_remaining_pct >= 10.0:
        status_label = "WARNING"
        recommendation = "PAPER_TEST_POSITION_ONLY"
    else:
        status_label = "CRITICAL"
        recommendation = "PAPER_BLOCK_NEW_ENTRY"

    return RiskBudgetStatus(
        portfolio_risk_pct=portfolio_risk_pct,
        risk_budget_remaining_pct=risk_budget_remaining_pct,
        risk_budget_used_pct=risk_budget_used_pct,
        risk_budget_ok=risk_budget_ok,
        status_label=status_label,
        recommendation=recommendation,
    )


def build_enhanced_ticket(
    symbol: str = "",
    name: str = "",
    setup_type: str = "NO_ENTRY",
    theme_score: float = 0.0,
    fundamental_score: float = 0.0,
    technical_score: float = 0.0,
    volume_score: float = 0.0,
    chip_score: float = 0.0,
    margin_score: float = 0.0,
    entry_price_plan: float = 0.0,
    add_price_plan: float = 0.0,
    reduce_price_plan: float = 0.0,
    exit_price_plan: float = 0.0,
    stop_loss_price: float = 0.0,
    invalid_conditions: Optional[List[str]] = None,
    risk_amount: float = 0.0,
    max_position_size: float = 0.0,
    position_size_reason: str = "",
    no_entry_reasons: Optional[List[str]] = None,
    human_review_required: bool = True,
    final_action: str = "NO_ENTRY",
) -> EnhancedDecisionTicket:
    """Build an EnhancedDecisionTicket with all 21 required fields. Paper only."""
    if invalid_conditions is None:
        invalid_conditions = []
    if no_entry_reasons is None:
        no_entry_reasons = []
    scores = [theme_score, fundamental_score, technical_score, volume_score, chip_score, margin_score]
    total_score = sum(scores) / len(scores) if scores else 0.0

    return EnhancedDecisionTicket(
        symbol=symbol,
        name=name,
        setup_type=setup_type,
        theme_score=theme_score,
        fundamental_score=fundamental_score,
        technical_score=technical_score,
        volume_score=volume_score,
        chip_score=chip_score,
        margin_score=margin_score,
        total_score=total_score,
        entry_price_plan=entry_price_plan,
        add_price_plan=add_price_plan,
        reduce_price_plan=reduce_price_plan,
        exit_price_plan=exit_price_plan,
        stop_loss_price=stop_loss_price,
        invalid_conditions=list(invalid_conditions),
        risk_amount=risk_amount,
        max_position_size=max_position_size,
        position_size_reason=position_size_reason,
        no_entry_reasons=list(no_entry_reasons),
        human_review_required=human_review_required,
        final_action=final_action,
    )


def build_candidate_ranking(
    candidates: List[Dict[str, Any]],
) -> List[CandidateRankEntry]:
    """Build sorted ranked candidate list. Paper only."""
    ranked = sorted(candidates, key=lambda c: c.get("total_score", 0.0), reverse=True)
    result = []
    for i, c in enumerate(ranked, start=1):
        result.append(CandidateRankEntry(
            symbol=c.get("symbol", ""),
            name=c.get("name", ""),
            rank=i,
            total_score=c.get("total_score", 0.0),
            abc_type=c.get("abc_type", "NO_ENTRY"),
            final_action=c.get("final_action", "NO_ENTRY"),
            entry_allowed=c.get("entry_allowed", False),
            block_reason=c.get("block_reason", ""),
        ))
    return result


def build_cli_display(workflow_result: DailyWorkflowResult) -> CLIDisplayOutput:
    """Build CLIDisplayOutput from a DailyWorkflowResult. Paper only."""
    rows = []
    action_counts: Dict[str, int] = {a: 0 for a in DAILY_FINAL_ACTIONS}

    for candidate_result in workflow_result.candidate_results:
        action = candidate_result.final_action
        if action in action_counts:
            action_counts[action] += 1

        blocked_reason = ""
        if candidate_result.no_entry_reasons:
            blocking = [r.reason_code for r in candidate_result.no_entry_reasons
                        if r.reason_code != "human_review_required"]
            if blocking:
                blocked_reason = blocking[0]

        risk_pct = 0.0
        if candidate_result.paper_decision_ticket:
            risk_pct = (candidate_result.paper_decision_ticket.risk_amount / 300000.0) * 100.0

        rows.append(CLIDisplayRow(
            symbol=candidate_result.symbol,
            name=candidate_result.name,
            setup_type=candidate_result.abc_type,
            abc_status=candidate_result.abc_type,
            entry_allowed=(action in ("PAPER_BUY_PLAN", "PAPER_ADD_PLAN")),
            blocked_reason=blocked_reason,
            risk_budget_used_pct=risk_pct,
            suggested_paper_action=action,
            human_review_flag=candidate_result.human_review_requirement,
        ))

    return CLIDisplayOutput(
        top_candidates=rows,
        total_candidates=len(rows),
        watch_count=action_counts.get("WATCH", 0),
        wait_count=action_counts.get("WAIT", 0),
        paper_buy_plan_count=action_counts.get("PAPER_BUY_PLAN", 0),
        paper_add_plan_count=action_counts.get("PAPER_ADD_PLAN", 0),
        paper_reduce_plan_count=action_counts.get("PAPER_REDUCE_PLAN", 0),
        paper_exit_plan_count=action_counts.get("PAPER_EXIT_PLAN", 0),
        no_entry_count=action_counts.get("NO_ENTRY", 0),
    )


def _process_single_candidate(
    symbol: str,
    rank: int,
    workflow_input: DailyWorkflowInput,
    candidate_data: Optional[Dict[str, Any]] = None,
) -> DailyWorkflowCandidateResult:
    """Process a single candidate through the daily workflow. Paper only."""
    if candidate_data is None:
        candidate_data = {}

    name = candidate_data.get("name", symbol)
    technical_data = candidate_data.get("technical_data", {})
    risk_data = candidate_data.get("risk_data", {})

    # Evaluate no-entry reasons
    no_entry_reasons = evaluate_no_entry_reasons(technical_data, risk_data)

    # Determine ABC type
    abc_type = candidate_data.get("abc_type", "NO_ENTRY")

    # Risk check
    risk_ok = workflow_input.risk_budget_remaining_pct >= 10.0
    if not risk_ok:
        risk_data = dict(risk_data)
        risk_data["risk_budget_exceeded"] = True

    # Sizing check
    stop_dist = candidate_data.get("stop_distance_pct", 0.08)
    sizing_ok = 0.0 < stop_dist <= 0.15

    # Classify final action
    blocking_reason_codes = [r.reason_code for r in no_entry_reasons if r.reason_code != "human_review_required"]
    final_action = classify_final_action(
        candidate=symbol,
        abc_type=abc_type,
        no_entry_reasons=blocking_reason_codes,
        risk_ok=risk_ok,
        sizing_ok=sizing_ok,
        has_position=candidate_data.get("has_position", False),
        position_profit_pct=candidate_data.get("position_profit_pct", 0.0),
    )

    # Build enhanced ticket
    entry_price = candidate_data.get("entry_price", 0.0)
    stop_loss_price = entry_price * (1.0 - stop_dist) if entry_price > 0 else 0.0
    risk_amount = candidate_data.get("risk_amount", 4500.0)
    max_pos = risk_amount / stop_dist if stop_dist > 0 else 0.0

    ticket = build_enhanced_ticket(
        symbol=symbol,
        name=name,
        setup_type=abc_type,
        theme_score=candidate_data.get("theme_score", 0.0),
        fundamental_score=candidate_data.get("fundamental_score", 0.0),
        technical_score=candidate_data.get("technical_score", 0.0),
        volume_score=candidate_data.get("volume_score", 0.0),
        chip_score=candidate_data.get("chip_score", 0.0),
        margin_score=candidate_data.get("margin_score", 0.0),
        entry_price_plan=entry_price,
        add_price_plan=candidate_data.get("add_price", 0.0),
        reduce_price_plan=entry_price * 1.20 if entry_price > 0 else 0.0,
        exit_price_plan=entry_price * 1.35 if entry_price > 0 else 0.0,
        stop_loss_price=stop_loss_price,
        invalid_conditions=blocking_reason_codes,
        risk_amount=risk_amount,
        max_position_size=round(min(max_pos, workflow_input.capital_twd * 0.15), 0),
        position_size_reason=f"risk_amount/{stop_dist:.2%} capped at 15% capital",
        no_entry_reasons=blocking_reason_codes,
        human_review_required=True,
        final_action=final_action,
    )

    # Risk overlay status
    if not risk_ok:
        risk_overlay_status = "BLOCKED_RISK_BUDGET"
    elif blocking_reason_codes:
        risk_overlay_status = "BLOCKED"
    else:
        risk_overlay_status = "CLEAR"

    # Position sizing suggestion
    if final_action in ("PAPER_BUY_PLAN", "PAPER_ADD_PLAN"):
        pos_suggestion = f"Max {ticket.max_position_size:,.0f} TWD ({stop_dist:.1%} stop)"
    else:
        pos_suggestion = "No position suggested"

    watchlist_summary = f"{symbol} watchlist rank #{rank}, regime={workflow_input.market_regime}"

    return DailyWorkflowCandidateResult(
        symbol=symbol,
        name=name,
        watchlist_summary=watchlist_summary,
        candidate_rank=rank,
        abc_type=abc_type,
        no_entry_reasons=no_entry_reasons,
        risk_overlay_status=risk_overlay_status,
        position_sizing_suggestion=pos_suggestion,
        paper_decision_ticket=ticket,
        human_review_requirement=True,
        final_action=final_action,
    )


def run_daily_workflow(
    workflow_input: Optional[DailyWorkflowInput] = None,
    candidate_data_map: Optional[Dict[str, Dict[str, Any]]] = None,
) -> DailyWorkflowResult:
    """Main entry point for the daily workflow. Paper only."""
    if workflow_input is None:
        workflow_input = DailyWorkflowInput()
    if candidate_data_map is None:
        candidate_data_map = {}

    candidates = workflow_input.candidates or workflow_input.watchlist
    candidate_results = []

    for rank, symbol in enumerate(candidates, start=1):
        cdata = candidate_data_map.get(symbol, {})
        result = _process_single_candidate(symbol, rank, workflow_input, cdata)
        candidate_results.append(result)

    # Build candidate ranking data
    ranking_data = []
    for cr in candidate_results:
        ticket = cr.paper_decision_ticket
        total_score = ticket.total_score if ticket else 0.0
        ranking_data.append({
            "symbol": cr.symbol,
            "name": cr.name,
            "total_score": total_score,
            "abc_type": cr.abc_type,
            "final_action": cr.final_action,
            "entry_allowed": cr.final_action in ("PAPER_BUY_PLAN", "PAPER_ADD_PLAN"),
            "block_reason": "; ".join(
                r.reason_code for r in cr.no_entry_reasons
                if r.reason_code != "human_review_required"
            ),
        })

    candidate_ranking = build_candidate_ranking(ranking_data)

    # Build summary
    action_counts: Dict[str, int] = {a: 0 for a in DAILY_FINAL_ACTIONS}
    human_review_count = 0
    for cr in candidate_results:
        if cr.final_action in action_counts:
            action_counts[cr.final_action] += 1
        if cr.human_review_requirement:
            human_review_count += 1

    summary = DailyWorkflowSummary(
        total_candidates=len(candidate_results),
        watch_count=action_counts.get("WATCH", 0),
        wait_count=action_counts.get("WAIT", 0),
        paper_buy_plan_count=action_counts.get("PAPER_BUY_PLAN", 0),
        paper_add_plan_count=action_counts.get("PAPER_ADD_PLAN", 0),
        paper_reduce_plan_count=action_counts.get("PAPER_REDUCE_PLAN", 0),
        paper_exit_plan_count=action_counts.get("PAPER_EXIT_PLAN", 0),
        no_entry_count=action_counts.get("NO_ENTRY", 0),
        human_review_count=human_review_count,
        all_passed_safety=True,
    )

    workflow_result = DailyWorkflowResult(
        market_regime=workflow_input.market_regime,
        candidate_results=candidate_results,
        candidate_ranking=candidate_ranking,
        summary=summary,
        all_passed=True,
    )

    # Build CLI display
    workflow_result.cli_display = build_cli_display(workflow_result)

    return workflow_result


def get_version_info() -> Dict[str, Any]:
    """Return version info dict. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "no_entry_reasons_count": len(NO_ENTRY_REASONS),
        "daily_final_actions_count": len(DAILY_FINAL_ACTIONS),
        "cli_commands_count": len(CLI_COMMANDS_V201),
        "gui_tabs_count": len(GUI_TABS_V201),
        "covered_versions_count": len(COVERED_VERSIONS),
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def verify_version() -> bool:
    """Verify this is v2.0.1. Returns True if correct."""
    return VERSION == "2.0.1" and SCHEMA_VERSION == "201"


def get_cockpit_summary_v201() -> Dict[str, Any]:
    """Return cockpit summary dict. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "paper_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
        "no_entry_reasons": NO_ENTRY_REASONS,
        "daily_final_actions": DAILY_FINAL_ACTIONS,
        "cli_commands": CLI_COMMANDS_V201,
        "gui_tabs": GUI_TABS_V201,
        "human_review_required": True,
        "covered_versions": COVERED_VERSIONS,
    }
