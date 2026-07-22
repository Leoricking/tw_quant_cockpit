"""
paper_trading/small_capital_strategy/paper_cockpit_v210.py
v2.0.10 Paper Exit Plan & Stop-Loss Discipline Control
[!] Paper Only. Research Only. Exit Plan Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. No Automatic Exit Apply. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.10"
SCHEMA_VERSION = "210"
RELEASE_NAME = "Paper Exit Plan & Stop-Loss Discipline Control"
BASELINE_TESTS = 35313
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

EXIT_ACTIONS: List[str] = [
    "allow_with_exit_plan",
    "require_tighter_stop",
    "reduce_size_before_entry",
    "observation_only",
    "block_entry_missing_stop",
    "block_entry_bad_reward_risk",
    "require_rescore",
    "human_review_required",
]

EXIT_REVIEW_FIELDS: List[str] = [
    "exit_review_id",
    "exit_version",
    "review_period",
    "exit_plan_snapshot",
    "stop_loss_snapshot",
    "take_profit_snapshot",
    "trailing_stop_snapshot",
    "exit_warning_queue",
    "stop_discipline_violation_queue",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

EXIT_PLAN_POLICY_FIELDS: List[str] = [
    "policy_id",
    "default_stop_loss_pct",
    "max_allowed_loss_pct",
    "max_stop_distance_pct",
    "min_reward_risk_ratio",
    "first_take_profit_r_multiple",
    "second_take_profit_r_multiple",
    "trailing_stop_ma",
    "time_stop_days",
    "gap_down_exit_pct",
    "failed_breakout_days",
    "require_stop_loss_before_entry",
    "auto_apply_enabled",
]

CANDIDATE_EXIT_PLAN_FIELDS: List[str] = [
    "symbol",
    "name",
    "candidate_id",
    "theme_id",
    "sector_id",
    "candidate_score",
    "final_priority_score",
    "entry_price",
    "stop_price",
    "stop_distance_pct",
    "max_loss_amount",
    "max_loss_pct",
    "first_take_profit_price",
    "second_take_profit_price",
    "trailing_stop_price",
    "reward_risk_ratio",
    "exit_action",
    "stop_loss_required",
    "stop_loss_valid",
    "blocked_by_missing_stop",
    "blocked_by_excessive_stop_distance",
    "blocked_by_bad_reward_risk",
    "requires_human_review",
    "should_auto_apply",
]

STOP_DISCIPLINE_SUMMARY_FIELDS: List[str] = [
    "total_candidate_count",
    "valid_exit_plan_count",
    "missing_stop_count",
    "excessive_stop_distance_count",
    "bad_reward_risk_count",
    "blocked_entry_count",
    "require_tighter_stop_count",
    "reduce_size_before_entry_count",
    "human_review_count",
    "average_reward_risk_ratio",
    "lowest_reward_risk_candidates",
    "top_exit_risk_reasons",
    "exit_plan_quality_grade",
    "stop_discipline_quality_grade",
]

CLI_COMMANDS_V210: List[str] = [
    "paper-cockpit-v210-review-exit-plan",
    "paper-cockpit-v210-evaluate-stop-discipline",
    "paper-cockpit-v210-build-exit-warning-queue",
    "paper-cockpit-v210-build-stop-violation-queue",
    "paper-cockpit-v210-evaluate-reward-risk",
    "paper-cockpit-v210-export-json",
    "paper-cockpit-v210-export-md",
    "paper-cockpit-v210-export-csv",
    "paper-cockpit-v210-health",
    "paper-cockpit-v210-gate",
]

GUI_TABS_V210: List[str] = [
    "exit_plan_v210",
    "stop_discipline_v210",
    "exit_warning_queue_v210",
]

SAFETY_FLAGS_V210: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "exit_plan_recommendation_only": True,
    "exit_actions_recommendation_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_exit_apply": True,
    "no_automatic_stop_loss_execution": True,
    "no_automatic_take_profit_execution": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "require_stop_loss_before_entry_always_true": True,
}

assert len(SAFETY_FLAGS_V210) == 23, f"Expected 23 SAFETY_FLAGS_V210, got {len(SAFETY_FLAGS_V210)}"
assert len(EXIT_ACTIONS) == 8
assert len(CLI_COMMANDS_V210) == 10
assert len(GUI_TABS_V210) == 3
assert len(EXIT_REVIEW_FIELDS) == 11
assert len(EXIT_PLAN_POLICY_FIELDS) == 13
assert len(CANDIDATE_EXIT_PLAN_FIELDS) == 24
assert len(STOP_DISCIPLINE_SUMMARY_FIELDS) == 14

COVERED_VERSIONS: List[str] = [
    "2.0.9", "2.0.8", "2.0.7", "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]

_ALL_MODEL_NAMES_V210: List[str] = [
    "ExitPlanPolicy",
    "CandidateExitPlan",
    "ExitReviewResult",
    "ExitReviewInput",
    "StopDisciplineSummary",
    "ExitExportResult",
    "ExitAuditSnapshot",
    "ExitMarkdownReport",
    "CandidateExitCSV",
    "StopDisciplineCSV",
    "ExitWarningCSV",
    "V210HealthSummary",
    "V210ReleaseSummary",
    "ExitPlanSafetyGuard",
]
assert len(_ALL_MODEL_NAMES_V210) == 14


# ---------------------------------------------------------------------------
# Dataclasses — 14 models, schema_version="210"
# ---------------------------------------------------------------------------

@dataclass
class ExitPlanPolicy:
    """Exit plan policy schema. v2.0.10. auto_apply_enabled is always False.
    require_stop_loss_before_entry is always True."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    default_stop_loss_pct: float = 0.06
    max_allowed_loss_pct: float = 0.08
    max_stop_distance_pct: float = 0.12
    min_reward_risk_ratio: float = 2.0
    first_take_profit_r_multiple: float = 1.0
    second_take_profit_r_multiple: float = 2.0
    trailing_stop_ma: int = 20
    time_stop_days: int = 20
    gap_down_exit_pct: float = 0.05
    failed_breakout_days: int = 5
    require_stop_loss_before_entry: bool = True   # ALWAYS True
    auto_apply_enabled: bool = False              # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)
        object.__setattr__(self, "require_stop_loss_before_entry", True)


@dataclass
class CandidateExitPlan:
    """Candidate exit plan schema. v2.0.10. should_auto_apply is always False."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    candidate_id: str = ""
    theme_id: str = ""
    sector_id: str = ""
    candidate_score: float = 0.0
    final_priority_score: float = 0.0
    entry_price: float = 0.0
    stop_price: float = 0.0
    stop_distance_pct: float = 0.0
    max_loss_amount: float = 0.0
    max_loss_pct: float = 0.0
    first_take_profit_price: float = 0.0
    second_take_profit_price: float = 0.0
    trailing_stop_price: float = 0.0
    reward_risk_ratio: float = 0.0
    exit_action: str = "allow_with_exit_plan"
    stop_loss_required: bool = True
    stop_loss_valid: bool = False
    blocked_by_missing_stop: bool = False
    blocked_by_excessive_stop_distance: bool = False
    blocked_by_bad_reward_risk: bool = False
    requires_human_review: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ExitReviewInput:
    """Input for exit plan review. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    review_period: str = ""
    candidate_pool: List[Dict[str, Any]] = field(default_factory=list)
    exit_plan_policy: Optional[ExitPlanPolicy] = None
    market_state: str = "range_bound"


@dataclass
class StopDisciplineSummary:
    """Stop discipline summary. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    total_candidate_count: int = 0
    valid_exit_plan_count: int = 0
    missing_stop_count: int = 0
    excessive_stop_distance_count: int = 0
    bad_reward_risk_count: int = 0
    blocked_entry_count: int = 0
    require_tighter_stop_count: int = 0
    reduce_size_before_entry_count: int = 0
    human_review_count: int = 0
    average_reward_risk_ratio: float = 0.0
    lowest_reward_risk_candidates: List[str] = field(default_factory=list)
    top_exit_risk_reasons: List[str] = field(default_factory=list)
    exit_plan_quality_grade: str = "B"
    stop_discipline_quality_grade: str = "B"


@dataclass
class ExitReviewResult:
    """Exit plan review result. v2.0.10. should_auto_apply is always False."""
    schema_version: str = "210"
    paper_only: bool = True
    research_only: bool = True
    exit_plan_recommendation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    exit_review_id: str = ""
    exit_version: str = "2.0.10"
    review_period: str = ""
    exit_plan_policy: Optional[ExitPlanPolicy] = None
    exit_plan_snapshot: List[CandidateExitPlan] = field(default_factory=list)
    stop_loss_snapshot: List[Dict[str, Any]] = field(default_factory=list)
    take_profit_snapshot: List[Dict[str, Any]] = field(default_factory=list)
    trailing_stop_snapshot: List[Dict[str, Any]] = field(default_factory=list)
    exit_warning_queue: List[CandidateExitPlan] = field(default_factory=list)
    stop_discipline_violation_queue: List[CandidateExitPlan] = field(default_factory=list)
    human_review_queue: List[CandidateExitPlan] = field(default_factory=list)
    stop_discipline_summary: Optional[StopDisciplineSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = True
    should_auto_apply: bool = False   # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class ExitExportResult:
    """Export result for exit plan review. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    exit_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class ExitAuditSnapshot:
    """Audit snapshot for exit plan review. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    exit_review_id: str = ""
    run_metadata: str = ""
    exit_plan_snapshot: str = ""
    stop_loss_snapshot: str = ""
    take_profit_snapshot: str = ""
    exit_warning_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class ExitMarkdownReport:
    """Markdown report for exit plan review. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    exit_review_id: str = ""
    review_period: str = ""
    content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class CandidateExitCSV:
    """CSV export of candidate exit plans. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    exit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class StopDisciplineCSV:
    """CSV export of stop discipline summary. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    exit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ExitWarningCSV:
    """CSV export of exit warning queue. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    exit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V210HealthSummary:
    """Health summary for v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.10"


@dataclass
class V210ReleaseSummary:
    """Release summary for v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    version: str = "2.0.10"
    release_name: str = RELEASE_NAME


@dataclass
class ExitPlanSafetyGuard:
    """Safety guard snapshot for exit plan. v2.0.10."""
    schema_version: str = "210"
    paper_only: bool = True
    no_real_orders: bool = True
    no_automatic_exit_apply: bool = True
    no_automatic_stop_loss_execution: bool = True
    no_automatic_take_profit_execution: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False
    require_stop_loss_before_entry: bool = True
    exit_actions_recommendation_only: bool = True


# ---------------------------------------------------------------------------
# Sizing helpers
# ---------------------------------------------------------------------------

def _make_exit_review_id(review_period: str, candidate_count: int) -> str:
    raw = f"v210-{review_period}-n{candidate_count}"
    return hashlib.sha256(raw.encode()).hexdigest()[:10]


def _calc_stop_distance_pct(entry_price: float, stop_price: float) -> float:
    if entry_price <= 0 or stop_price <= 0 or stop_price >= entry_price:
        return 0.0
    return (entry_price - stop_price) / entry_price


def _calc_reward_risk_ratio(
    entry_price: float,
    stop_price: float,
    first_tp_price: float,
) -> float:
    """R/R = (first_tp - entry) / (entry - stop). Returns 0 if invalid."""
    if entry_price <= 0 or stop_price <= 0 or stop_price >= entry_price:
        return 0.0
    risk = entry_price - stop_price
    reward = first_tp_price - entry_price
    if risk <= 0:
        return 0.0
    return reward / risk


def _calc_first_tp_price(
    entry_price: float,
    stop_price: float,
    r_multiple: float,
) -> float:
    if entry_price <= 0 or stop_price <= 0 or stop_price >= entry_price:
        return entry_price
    risk = entry_price - stop_price
    return entry_price + risk * r_multiple


def _calc_trailing_stop_price(
    entry_price: float,
    stop_price: float,
    trail_pct: float = 0.03,
) -> float:
    if entry_price <= 0:
        return stop_price
    return entry_price * (1.0 - trail_pct)


def _classify_exit_action(
    stop_distance_pct: float,
    reward_risk_ratio: float,
    stop_loss_valid: bool,
    policy: ExitPlanPolicy,
    is_high_volatility: bool = False,
    market_state: str = "range_bound",
    lifecycle_state: str = "active",
) -> str:
    """Classify exit action based on stop discipline validation."""
    # Missing stop — block entry
    if not stop_loss_valid or stop_distance_pct <= 0.0:
        return "block_entry_missing_stop"
    # Excessive stop distance — require tighter stop
    if stop_distance_pct > policy.max_stop_distance_pct:
        return "require_tighter_stop"
    # Bad reward/risk — block entry
    if reward_risk_ratio < policy.min_reward_risk_ratio and reward_risk_ratio > 0.0:
        return "block_entry_bad_reward_risk"
    # No valid R/R ratio (first TP not set correctly)
    if reward_risk_ratio <= 0.0:
        return "block_entry_bad_reward_risk"
    # Risk-off market — observation only
    if market_state == "risk_off":
        return "observation_only"
    # Expired/cooldown lifecycle
    if lifecycle_state in ("expired", "cooldown"):
        return "observation_only"
    # High volatility — reduce size before entry
    if is_high_volatility:
        return "reduce_size_before_entry"
    # Require human review for downtrend
    if market_state == "downtrend":
        return "human_review_required"
    # All checks pass — allow with exit plan
    return "allow_with_exit_plan"


def _calc_max_loss(
    entry_price: float,
    stop_price: float,
    account_equity: float,
    max_loss_pct: float,
) -> float:
    """Max loss amount = account_equity * max_loss_pct."""
    return account_equity * max_loss_pct


def _grade_exit_plan(valid_count: int, total_count: int) -> str:
    if total_count == 0:
        return "N/A"
    ratio = valid_count / total_count
    if ratio >= 0.90:
        return "A"
    if ratio >= 0.75:
        return "B"
    if ratio >= 0.50:
        return "C"
    return "D"


def _grade_stop_discipline(violation_count: int, total_count: int) -> str:
    if total_count == 0:
        return "N/A"
    ratio = violation_count / total_count
    if ratio == 0.0:
        return "A"
    if ratio <= 0.10:
        return "B"
    if ratio <= 0.25:
        return "C"
    return "D"


# ---------------------------------------------------------------------------
# Main exit plan calculation
# ---------------------------------------------------------------------------

def calculate_exit_plan(
    symbol: str,
    name: str,
    candidate_id: str,
    theme_id: str,
    sector_id: str,
    candidate_score: float,
    final_priority_score: float,
    entry_price: float,
    stop_price: float,
    policy: Optional[ExitPlanPolicy] = None,
    is_high_volatility: bool = False,
    is_low_liquidity: bool = False,
    market_state: str = "range_bound",
    lifecycle_state: str = "active",
    account_equity: float = 300000.0,
) -> CandidateExitPlan:
    """Calculate paper-only exit plan for a candidate. Paper only, no real orders."""
    if policy is None:
        policy = ExitPlanPolicy(policy_id="default-policy-v210")

    # Stop distance
    stop_distance_pct = _calc_stop_distance_pct(entry_price, stop_price)
    stop_loss_valid = (
        stop_price > 0
        and entry_price > 0
        and stop_price < entry_price
        and stop_distance_pct <= policy.max_stop_distance_pct
    )

    # Take-profit targets
    first_tp = _calc_first_tp_price(entry_price, stop_price, policy.first_take_profit_r_multiple)
    second_tp = _calc_first_tp_price(entry_price, stop_price, policy.second_take_profit_r_multiple)
    trailing_stop = _calc_trailing_stop_price(entry_price, stop_price)

    # Reward/risk
    rr_ratio = _calc_reward_risk_ratio(entry_price, stop_price, first_tp)

    # Max loss
    max_loss_amt = _calc_max_loss(entry_price, stop_price, account_equity, policy.max_allowed_loss_pct)
    max_loss_pct = policy.max_allowed_loss_pct

    # Classify exit action
    exit_action = _classify_exit_action(
        stop_distance_pct=stop_distance_pct,
        reward_risk_ratio=rr_ratio,
        stop_loss_valid=stop_loss_valid,
        policy=policy,
        is_high_volatility=is_high_volatility,
        market_state=market_state,
        lifecycle_state=lifecycle_state,
    )

    blocked_missing = exit_action == "block_entry_missing_stop"
    blocked_excess = exit_action == "require_tighter_stop"
    blocked_rr = exit_action == "block_entry_bad_reward_risk"
    requires_review = exit_action in ("human_review_required", "require_rescore")

    return CandidateExitPlan(
        schema_version="210",
        paper_only=True,
        no_real_orders=True,
        symbol=symbol,
        name=name,
        candidate_id=candidate_id,
        theme_id=theme_id,
        sector_id=sector_id,
        candidate_score=candidate_score,
        final_priority_score=final_priority_score,
        entry_price=entry_price,
        stop_price=stop_price,
        stop_distance_pct=stop_distance_pct,
        max_loss_amount=max_loss_amt,
        max_loss_pct=max_loss_pct,
        first_take_profit_price=first_tp,
        second_take_profit_price=second_tp,
        trailing_stop_price=trailing_stop,
        reward_risk_ratio=rr_ratio,
        exit_action=exit_action,
        stop_loss_required=True,
        stop_loss_valid=stop_loss_valid,
        blocked_by_missing_stop=blocked_missing,
        blocked_by_excessive_stop_distance=blocked_excess,
        blocked_by_bad_reward_risk=blocked_rr,
        requires_human_review=requires_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Exit plan review engine
# ---------------------------------------------------------------------------

def _default_exit_plan_policy() -> ExitPlanPolicy:
    return ExitPlanPolicy(policy_id="default-policy-v210")


def _default_exit_candidate_pool() -> List[Dict[str, Any]]:
    """Return default demo candidate pool for exit planning. Paper only."""
    return [
        {"symbol": "2330", "name": "台積電", "candidate_id": "CAND-2330", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "candidate_score": 82.0, "final_priority_score": 80.0, "entry_price": 900.0, "stop_price": 855.0, "is_high_volatility": False, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "active"},
        {"symbol": "2454", "name": "聯發科", "candidate_id": "CAND-2454", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "candidate_score": 76.0, "final_priority_score": 75.0, "entry_price": 1000.0, "stop_price": 940.0, "is_high_volatility": False, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "active"},
        {"symbol": "2382", "name": "廣達", "candidate_id": "CAND-2382", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "candidate_score": 70.0, "final_priority_score": 68.0, "entry_price": 300.0, "stop_price": 282.0, "is_high_volatility": False, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "active"},
        {"symbol": "2308", "name": "台達電", "candidate_id": "CAND-2308", "theme_id": "THEME-EV", "sector_id": "SECTOR-ELEC", "candidate_score": 65.0, "final_priority_score": 62.0, "entry_price": 400.0, "stop_price": 372.0, "is_high_volatility": True, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "active"},
        {"symbol": "2317", "name": "鴻海", "candidate_id": "CAND-2317", "theme_id": "THEME-EV", "sector_id": "SECTOR-MFGR", "candidate_score": 60.0, "final_priority_score": 58.0, "entry_price": 120.0, "stop_price": 112.0, "is_high_volatility": False, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "aging"},
        {"symbol": "3711", "name": "日月光", "candidate_id": "CAND-3711", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "candidate_score": 72.0, "final_priority_score": 72.0, "entry_price": 150.0, "stop_price": 141.0, "is_high_volatility": False, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "active"},
        {"symbol": "2303", "name": "聯電", "candidate_id": "CAND-2303", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "candidate_score": 65.0, "final_priority_score": 65.0, "entry_price": 55.0, "stop_price": 51.0, "is_high_volatility": False, "is_low_liquidity": True, "market_state": "range_bound", "lifecycle_state": "active"},
        {"symbol": "6669", "name": "緯穎", "candidate_id": "CAND-6669", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "candidate_score": 71.0, "final_priority_score": 70.0, "entry_price": 2000.0, "stop_price": 1880.0, "is_high_volatility": True, "is_low_liquidity": False, "market_state": "range_bound", "lifecycle_state": "active"},
    ]


def build_exit_warning_queue(
    exit_plans: Optional[List[CandidateExitPlan]] = None,
) -> List[CandidateExitPlan]:
    """Build exit warning queue — candidates with bad R/R or excessive stop distance. Paper only."""
    if exit_plans is None:
        pool = _default_exit_candidate_pool()
        policy = _default_exit_plan_policy()
        exit_plans = [
            calculate_exit_plan(
                symbol=c["symbol"], name=c["name"], candidate_id=c["candidate_id"],
                theme_id=c["theme_id"], sector_id=c["sector_id"],
                candidate_score=c["candidate_score"], final_priority_score=c["final_priority_score"],
                entry_price=c["entry_price"], stop_price=c["stop_price"],
                policy=policy,
                is_high_volatility=c.get("is_high_volatility", False),
                is_low_liquidity=c.get("is_low_liquidity", False),
                market_state=c.get("market_state", "range_bound"),
                lifecycle_state=c.get("lifecycle_state", "active"),
            )
            for c in pool
        ]
    return [
        p for p in exit_plans
        if p.exit_action in (
            "require_tighter_stop",
            "block_entry_bad_reward_risk",
            "block_entry_missing_stop",
            "human_review_required",
        )
    ]


def build_stop_violation_queue(
    exit_plans: Optional[List[CandidateExitPlan]] = None,
) -> List[CandidateExitPlan]:
    """Build stop discipline violation queue. Paper only."""
    if exit_plans is None:
        pool = _default_exit_candidate_pool()
        policy = _default_exit_plan_policy()
        exit_plans = [
            calculate_exit_plan(
                symbol=c["symbol"], name=c["name"], candidate_id=c["candidate_id"],
                theme_id=c["theme_id"], sector_id=c["sector_id"],
                candidate_score=c["candidate_score"], final_priority_score=c["final_priority_score"],
                entry_price=c["entry_price"], stop_price=c["stop_price"],
                policy=policy,
                is_high_volatility=c.get("is_high_volatility", False),
                is_low_liquidity=c.get("is_low_liquidity", False),
                market_state=c.get("market_state", "range_bound"),
                lifecycle_state=c.get("lifecycle_state", "active"),
            )
            for c in pool
        ]
    return [
        p for p in exit_plans
        if p.blocked_by_missing_stop
        or p.blocked_by_excessive_stop_distance
        or not p.stop_loss_valid
    ]


def evaluate_stop_discipline(
    exit_plans: Optional[List[CandidateExitPlan]] = None,
) -> Dict[str, Any]:
    """Evaluate stop discipline across candidates. Paper only."""
    if exit_plans is None:
        pool = _default_exit_candidate_pool()
        policy = _default_exit_plan_policy()
        exit_plans = [
            calculate_exit_plan(
                symbol=c["symbol"], name=c["name"], candidate_id=c["candidate_id"],
                theme_id=c["theme_id"], sector_id=c["sector_id"],
                candidate_score=c["candidate_score"], final_priority_score=c["final_priority_score"],
                entry_price=c["entry_price"], stop_price=c["stop_price"],
                policy=policy,
            )
            for c in pool
        ]
    n = len(exit_plans)
    missing = sum(1 for p in exit_plans if p.blocked_by_missing_stop)
    excess = sum(1 for p in exit_plans if p.blocked_by_excessive_stop_distance)
    bad_rr = sum(1 for p in exit_plans if p.blocked_by_bad_reward_risk)
    return {
        "total_candidates": n,
        "missing_stop_count": missing,
        "excessive_stop_count": excess,
        "bad_reward_risk_count": bad_rr,
        "total_violations": missing + excess + bad_rr,
        "stop_discipline_pass_rate": (n - missing) / max(n, 1),
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "schema_version": "210",
    }


def evaluate_reward_risk(
    exit_plans: Optional[List[CandidateExitPlan]] = None,
) -> Dict[str, Any]:
    """Evaluate reward/risk ratios across candidates. Paper only."""
    if exit_plans is None:
        pool = _default_exit_candidate_pool()
        policy = _default_exit_plan_policy()
        exit_plans = [
            calculate_exit_plan(
                symbol=c["symbol"], name=c["name"], candidate_id=c["candidate_id"],
                theme_id=c["theme_id"], sector_id=c["sector_id"],
                candidate_score=c["candidate_score"], final_priority_score=c["final_priority_score"],
                entry_price=c["entry_price"], stop_price=c["stop_price"],
                policy=policy,
            )
            for c in pool
        ]
    ratios = [p.reward_risk_ratio for p in exit_plans if p.reward_risk_ratio > 0]
    avg_rr = sum(ratios) / len(ratios) if ratios else 0.0
    return {
        "candidate_count": len(exit_plans),
        "average_reward_risk_ratio": round(avg_rr, 4),
        "min_required_ratio": 2.0,
        "passing_rr_count": sum(1 for r in ratios if r >= 2.0),
        "failing_rr_count": sum(1 for r in ratios if r < 2.0),
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "schema_version": "210",
    }


def _build_stop_discipline_summary(
    exit_plans: List[CandidateExitPlan],
) -> StopDisciplineSummary:
    n = len(exit_plans)
    valid = sum(1 for p in exit_plans if p.stop_loss_valid and p.exit_action == "allow_with_exit_plan")
    missing = sum(1 for p in exit_plans if p.blocked_by_missing_stop)
    excess = sum(1 for p in exit_plans if p.blocked_by_excessive_stop_distance)
    bad_rr = sum(1 for p in exit_plans if p.blocked_by_bad_reward_risk)
    blocked = sum(1 for p in exit_plans if p.exit_action in ("block_entry_missing_stop", "block_entry_bad_reward_risk"))
    tighter = sum(1 for p in exit_plans if p.exit_action == "require_tighter_stop")
    reduce = sum(1 for p in exit_plans if p.exit_action == "reduce_size_before_entry")
    human = sum(1 for p in exit_plans if p.requires_human_review)
    ratios = [p.reward_risk_ratio for p in exit_plans if p.reward_risk_ratio > 0]
    avg_rr = round(sum(ratios) / len(ratios), 4) if ratios else 0.0
    worst = sorted(
        [p.symbol for p in exit_plans if p.reward_risk_ratio > 0 and p.reward_risk_ratio < 2.0],
    )[:3]
    return StopDisciplineSummary(
        total_candidate_count=n,
        valid_exit_plan_count=valid,
        missing_stop_count=missing,
        excessive_stop_distance_count=excess,
        bad_reward_risk_count=bad_rr,
        blocked_entry_count=blocked,
        require_tighter_stop_count=tighter,
        reduce_size_before_entry_count=reduce,
        human_review_count=human,
        average_reward_risk_ratio=avg_rr,
        lowest_reward_risk_candidates=worst,
        top_exit_risk_reasons=[],
        exit_plan_quality_grade=_grade_exit_plan(valid, n),
        stop_discipline_quality_grade=_grade_stop_discipline(missing + excess, n),
    )


def run_exit_plan_review(
    review_input: Optional[ExitReviewInput] = None,
) -> ExitReviewResult:
    """Run a paper exit plan review. Paper only, no real orders."""
    if review_input is None:
        review_input = ExitReviewInput(
            review_period="2026-W29",
            candidate_pool=_default_exit_candidate_pool(),
        )

    policy = review_input.exit_plan_policy or _default_exit_plan_policy()
    candidates = review_input.candidate_pool
    market_state = review_input.market_state

    review_id = _make_exit_review_id(review_input.review_period, len(candidates))

    exit_plans: List[CandidateExitPlan] = []
    for c in candidates:
        plan = calculate_exit_plan(
            symbol=c.get("symbol", ""),
            name=c.get("name", ""),
            candidate_id=c.get("candidate_id", ""),
            theme_id=c.get("theme_id", ""),
            sector_id=c.get("sector_id", ""),
            candidate_score=c.get("candidate_score", 50.0),
            final_priority_score=c.get("final_priority_score", 50.0),
            entry_price=c.get("entry_price", 0.0),
            stop_price=c.get("stop_price", 0.0),
            policy=policy,
            is_high_volatility=c.get("is_high_volatility", False),
            is_low_liquidity=c.get("is_low_liquidity", False),
            market_state=c.get("market_state", market_state),
            lifecycle_state=c.get("lifecycle_state", "active"),
        )
        exit_plans.append(plan)

    warning_queue = [
        p for p in exit_plans
        if p.exit_action in (
            "require_tighter_stop", "block_entry_bad_reward_risk",
            "block_entry_missing_stop",
        )
    ]
    violation_queue = [
        p for p in exit_plans
        if p.blocked_by_missing_stop or p.blocked_by_excessive_stop_distance
    ]
    human_queue = [p for p in exit_plans if p.requires_human_review]

    sl_snapshot = [
        {"symbol": p.symbol, "stop_price": p.stop_price, "stop_distance_pct": p.stop_distance_pct, "stop_loss_valid": p.stop_loss_valid}
        for p in exit_plans
    ]
    tp_snapshot = [
        {"symbol": p.symbol, "first_tp": p.first_take_profit_price, "second_tp": p.second_take_profit_price, "reward_risk_ratio": p.reward_risk_ratio}
        for p in exit_plans
    ]
    trail_snapshot = [
        {"symbol": p.symbol, "trailing_stop": p.trailing_stop_price}
        for p in exit_plans
    ]

    summary = _build_stop_discipline_summary(exit_plans)

    return ExitReviewResult(
        exit_review_id=review_id,
        exit_version="2.0.10",
        review_period=review_input.review_period,
        exit_plan_policy=policy,
        exit_plan_snapshot=exit_plans,
        stop_loss_snapshot=sl_snapshot,
        take_profit_snapshot=tp_snapshot,
        trailing_stop_snapshot=trail_snapshot,
        exit_warning_queue=warning_queue,
        stop_discipline_violation_queue=violation_queue,
        human_review_queue=human_queue,
        stop_discipline_summary=summary,
        paper_only_safety_snapshot=True,
        all_passed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_exit_plan_json(result: ExitReviewResult) -> ExitExportResult:
    """Export exit plan review as JSON. Paper only."""
    import json as _json
    payload = {
        "version": "2.0.10",
        "schema_version": "210",
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "exit_review_id": result.exit_review_id,
        "exit_version": result.exit_version,
        "review_period": result.review_period,
        "candidate_count": len(result.exit_plan_snapshot),
        "warning_count": len(result.exit_warning_queue),
        "violation_count": len(result.stop_discipline_violation_queue),
        "human_review_count": len(result.human_review_queue),
    }
    content = _json.dumps(payload, ensure_ascii=False, indent=2)
    return ExitExportResult(
        exit_review_id=result.exit_review_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
    )


def export_exit_plan_markdown(result: ExitReviewResult) -> ExitExportResult:
    """Export exit plan review as Markdown. Paper only."""
    lines = [
        f"# Paper Exit Plan Review v2.0.10",
        f"",
        f"**Period:** {result.review_period}",
        f"**Exit Review ID:** {result.exit_review_id}",
        f"**Paper Only:** True",
        f"**No Real Orders:** True",
        f"**Should Auto Apply:** False",
        f"",
        f"## Candidates: {len(result.exit_plan_snapshot)}",
        f"## Warnings: {len(result.exit_warning_queue)}",
        f"## Violations: {len(result.stop_discipline_violation_queue)}",
        f"## Human Review: {len(result.human_review_queue)}",
        f"",
        f"*[!] Paper Only. Not Investment Advice. Exit Actions Are Recommendation Only.*",
    ]
    content = "\n".join(lines)
    return ExitExportResult(
        exit_review_id=result.exit_review_id,
        export_format="markdown",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
    )


def export_candidate_exit_csv(result: ExitReviewResult) -> CandidateExitCSV:
    """Export candidate exit plans as CSV. Paper only."""
    header = "symbol,entry_price,stop_price,stop_distance_pct,first_tp,rr_ratio,exit_action,stop_loss_valid,should_auto_apply"
    rows = [header]
    for p in result.exit_plan_snapshot:
        rows.append(
            f"{p.symbol},{p.entry_price},{p.stop_price},{p.stop_distance_pct:.4f},"
            f"{p.first_take_profit_price},{p.reward_risk_ratio:.2f},"
            f"{p.exit_action},{p.stop_loss_valid},{p.should_auto_apply}"
        )
    csv_content = "\n".join(rows)
    return CandidateExitCSV(
        exit_review_id=result.exit_review_id,
        csv_content=csv_content,
        row_count=len(result.exit_plan_snapshot),
        is_valid=True,
    )


def export_stop_discipline_csv(result: ExitReviewResult) -> StopDisciplineCSV:
    """Export stop discipline summary as CSV. Paper only."""
    s = result.stop_discipline_summary
    if s is None:
        s = StopDisciplineSummary()
    header = "total,valid_exit_plans,missing_stop,excessive_stop,bad_rr,blocked,quality_grade,discipline_grade"
    row = (
        f"{s.total_candidate_count},{s.valid_exit_plan_count},"
        f"{s.missing_stop_count},{s.excessive_stop_distance_count},"
        f"{s.bad_reward_risk_count},{s.blocked_entry_count},"
        f"{s.exit_plan_quality_grade},{s.stop_discipline_quality_grade}"
    )
    csv_content = header + "\n" + row
    return StopDisciplineCSV(
        exit_review_id=result.exit_review_id,
        csv_content=csv_content,
        row_count=1,
        is_valid=True,
    )


def export_exit_warning_csv(result: ExitReviewResult) -> ExitWarningCSV:
    """Export exit warning queue as CSV. Paper only."""
    header = "symbol,exit_action,blocked_by_missing_stop,blocked_by_bad_rr,requires_human_review"
    rows = [header]
    for p in result.exit_warning_queue:
        rows.append(
            f"{p.symbol},{p.exit_action},{p.blocked_by_missing_stop},"
            f"{p.blocked_by_bad_reward_risk},{p.requires_human_review}"
        )
    csv_content = "\n".join(rows)
    return ExitWarningCSV(
        exit_review_id=result.exit_review_id,
        csv_content=csv_content,
        row_count=len(result.exit_warning_queue),
        is_valid=True,
    )


def export_exit_audit_snapshot(result: ExitReviewResult) -> ExitAuditSnapshot:
    """Export exit plan audit snapshot. Paper only."""
    hash_val = hashlib.sha256(
        f"{result.exit_review_id}-{result.review_period}-{len(result.exit_plan_snapshot)}".encode()
    ).hexdigest()[:16]
    return ExitAuditSnapshot(
        exit_review_id=result.exit_review_id,
        run_metadata=f"v210-paper-only-exit-audit",
        exit_plan_snapshot=f"candidates={len(result.exit_plan_snapshot)}",
        stop_loss_snapshot=f"sl_entries={len(result.stop_loss_snapshot)}",
        take_profit_snapshot=f"tp_entries={len(result.take_profit_snapshot)}",
        exit_warning_snapshot=f"warnings={len(result.exit_warning_queue)}",
        safety_snapshot="paper_only=True,no_real_orders=True,should_auto_apply=False",
        reproducibility_hash=hash_val,
        export_status="complete",
    )


# ---------------------------------------------------------------------------
# Version / summary
# ---------------------------------------------------------------------------

def verify_version() -> bool:
    """Verify v2.0.10 version constants are correct."""
    return VERSION == "2.0.10" and SCHEMA_VERSION == "210"


def get_cockpit_summary_v210() -> Dict[str, Any]:
    """Return v2.0.10 cockpit summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "require_stop_loss_before_entry": True,
        "exit_actions_recommendation_only": True,
        "exit_action_count": len(EXIT_ACTIONS),
        "cli_command_count": len(CLI_COMMANDS_V210),
        "gui_tab_count": len(GUI_TABS_V210),
        "safety_flag_count": len(SAFETY_FLAGS_V210),
        "model_count": len(_ALL_MODEL_NAMES_V210),
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }
