"""
paper_trading/small_capital_strategy/paper_cockpit_v212.py
v2.0.12 Paper Profit Taking & ETF Rebalancing Control
[!] Paper Only. Research Only. Profit Taking Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. No Automatic Profit Taking. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.12"
SCHEMA_VERSION = "212"
RELEASE_NAME = "Paper Profit Taking & ETF Rebalancing Control"
BASELINE_TESTS = 36361
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

PROFIT_ACTIONS: List[str] = [
    "hold_with_plan",
    "take_first_third",
    "take_second_third",
    "protect_runner",
    "tighten_trailing_stop",
    "reduce_on_pressure",
    "observation_only",
    "block_new_add",
    "human_review_required",
]

ASSET_TYPES: List[str] = [
    "stock",
    "etf",
    "leveraged_etf",
    "theme_basket",
    "watchlist_candidate",
]

REBALANCE_ACTIONS: List[str] = [
    "within_band_hold",
    "trim_to_target_band",
    "add_back_to_target_band",
    "reduce_leveraged_exposure",
    "observation_only",
    "human_review_required",
]

PROFIT_REVIEW_FIELDS: List[str] = [
    "profit_review_id",
    "profit_version",
    "review_period",
    "profit_taking_snapshot",
    "one_third_profit_plan_snapshot",
    "trailing_profit_snapshot",
    "profit_giveback_snapshot",
    "profit_warning_queue",
    "giveback_review_queue",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

PROFIT_TAKING_POLICY_FIELDS: List[str] = [
    "policy_id",
    "first_take_profit_pct",
    "first_take_profit_fraction",
    "second_take_profit_pct",
    "second_take_profit_fraction",
    "runner_fraction",
    "trailing_stop_from_high_pct",
    "strong_trend_ma_exit",
    "max_profit_giveback_pct",
    "weak_rebound_pressure_exit_enabled",
    "require_profit_plan_before_entry",
    "auto_apply_enabled",
]

CANDIDATE_PROFIT_PLAN_FIELDS: List[str] = [
    "plan_id",
    "symbol",
    "name",
    "candidate_id",
    "theme_id",
    "sector_id",
    "asset_type",
    "entry_price",
    "current_price",
    "unrealized_return_pct",
    "unrealized_profit_amount",
    "first_take_profit_price",
    "second_take_profit_price",
    "trailing_stop_price",
    "high_watermark_price",
    "giveback_from_high_pct",
    "first_take_profit_triggered",
    "second_take_profit_triggered",
    "runner_active",
    "profit_action",
    "blocked_by_missing_profit_plan",
    "requires_human_review",
    "should_auto_apply",
    "paper_only",
    "no_real_orders",
    "schema_version",
]

ETF_REBALANCING_ITEM_FIELDS: List[str] = [
    "etf_symbol",
    "etf_name",
    "target_allocation_pct",
    "current_allocation_pct",
    "upper_rebalance_band_pct",
    "lower_rebalance_band_pct",
    "overweight_pct",
    "underweight_pct",
    "rebalance_action",
    "recommended_trim_pct",
    "recommended_add_pct",
    "is_leveraged_etf",
    "leveraged_etf_warning",
    "requires_human_review",
    "should_auto_apply",
]

PROFIT_TAKING_SUMMARY_FIELDS: List[str] = [
    "total_position_count",
    "stock_profit_plan_count",
    "etf_rebalance_plan_count",
    "first_take_profit_count",
    "second_take_profit_count",
    "runner_protection_count",
    "giveback_warning_count",
    "pressure_zone_reduce_count",
    "leveraged_etf_warning_count",
    "human_review_count",
    "average_unrealized_return_pct",
    "top_unrealized_profit_symbols",
    "top_giveback_risk_symbols",
    "profit_taking_quality_grade",
    "rebalancing_quality_grade",
]

CLI_COMMANDS_V212: List[str] = [
    "paper-cockpit-v212-review-profit-taking",
    "paper-cockpit-v212-evaluate-giveback-risk",
    "paper-cockpit-v212-build-profit-warning-queue",
    "paper-cockpit-v212-build-giveback-review-queue",
    "paper-cockpit-v212-review-etf-rebalancing",
    "paper-cockpit-v212-export-json",
    "paper-cockpit-v212-export-md",
    "paper-cockpit-v212-export-csv",
    "paper-cockpit-v212-health",
    "paper-cockpit-v212-gate",
]

GUI_TABS_V212: List[str] = [
    "profit_taking_v212",
    "etf_rebalancing_v212",
    "giveback_review_queue_v212",
]

SAFETY_FLAGS_V212: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "profit_taking_recommendation_only": True,
    "etf_rebalance_recommendation_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_profit_taking_action": True,
    "no_automatic_stop_loss_execution": True,
    "no_automatic_take_profit_execution": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "require_profit_plan_before_entry_always_true": True,
    "profit_actions_recommendation_only": True,
    "etf_rebalance_actions_recommendation_only": True,
}

assert len(SAFETY_FLAGS_V212) == 25, f"Expected 25 SAFETY_FLAGS_V212, got {len(SAFETY_FLAGS_V212)}"
assert len(PROFIT_ACTIONS) == 9
assert len(ASSET_TYPES) == 5
assert len(REBALANCE_ACTIONS) == 6
assert len(CLI_COMMANDS_V212) == 10
assert len(GUI_TABS_V212) == 3
assert len(PROFIT_REVIEW_FIELDS) == 11
assert len(PROFIT_TAKING_POLICY_FIELDS) == 12
assert len(CANDIDATE_PROFIT_PLAN_FIELDS) == 26
assert len(ETF_REBALANCING_ITEM_FIELDS) == 15
assert len(PROFIT_TAKING_SUMMARY_FIELDS) == 15

COVERED_VERSIONS: List[str] = [
    "2.0.11", "2.0.10", "2.0.9", "2.0.8", "2.0.7", "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]

_ALL_MODEL_NAMES_V212: List[str] = [
    "ProfitTakingPolicy",
    "CandidateProfitPlan",
    "ETFRebalancingItem",
    "ProfitTakingSummary",
    "ProfitReviewInput",
    "ProfitReviewResult",
    "ProfitTakingExportResult",
    "ProfitTakingAuditSnapshot",
    "ProfitTakingMarkdownReport",
    "CandidateProfitPlanCSV",
    "ETFRebalancingCSV",
    "ProfitWarningQueueCSV",
    "GivebackReviewQueueCSV",
    "V212HealthSummary",
    "V212ReleaseSummary",
    "ProfitSafetyGuard",
]
assert len(_ALL_MODEL_NAMES_V212) == 16


# ---------------------------------------------------------------------------
# Dataclasses — 16 models, schema_version="212"
# ---------------------------------------------------------------------------

@dataclass
class ProfitTakingPolicy:
    """Profit taking policy schema. v2.0.12.
    auto_apply_enabled is always False.
    require_profit_plan_before_entry is always True."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    first_take_profit_pct: float = 0.20          # +20% triggers first 1/3 take
    first_take_profit_fraction: float = 1 / 3
    second_take_profit_pct: float = 0.40         # +40% triggers second 1/3 take
    second_take_profit_fraction: float = 1 / 3
    runner_fraction: float = 1 / 3
    trailing_stop_from_high_pct: float = 0.12    # trailing stop 12% from high
    strong_trend_ma_exit: str = "20ma_break"
    max_profit_giveback_pct: float = 0.15        # giveback > 15% of high triggers warning
    weak_rebound_pressure_exit_enabled: bool = True
    require_profit_plan_before_entry: bool = True  # ALWAYS True
    auto_apply_enabled: bool = False              # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)
        object.__setattr__(self, "require_profit_plan_before_entry", True)


@dataclass
class CandidateProfitPlan:
    """Candidate profit plan schema. v2.0.12. should_auto_apply is always False."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    plan_id: str = ""
    symbol: str = ""
    name: str = ""
    candidate_id: str = ""
    theme_id: str = ""
    sector_id: str = ""
    asset_type: str = "stock"
    entry_price: float = 0.0
    current_price: float = 0.0
    unrealized_return_pct: float = 0.0
    unrealized_profit_amount: float = 0.0
    first_take_profit_price: float = 0.0
    second_take_profit_price: float = 0.0
    trailing_stop_price: float = 0.0
    high_watermark_price: float = 0.0
    giveback_from_high_pct: float = 0.0
    first_take_profit_triggered: bool = False
    second_take_profit_triggered: bool = False
    runner_active: bool = False
    profit_action: str = "hold_with_plan"
    blocked_by_missing_profit_plan: bool = False
    requires_human_review: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ETFRebalancingItem:
    """ETF rebalancing item schema. v2.0.12. should_auto_apply is always False."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    etf_symbol: str = ""
    etf_name: str = ""
    target_allocation_pct: float = 0.0
    current_allocation_pct: float = 0.0
    upper_rebalance_band_pct: float = 0.0
    lower_rebalance_band_pct: float = 0.0
    overweight_pct: float = 0.0
    underweight_pct: float = 0.0
    rebalance_action: str = "within_band_hold"
    recommended_trim_pct: float = 0.0
    recommended_add_pct: float = 0.0
    is_leveraged_etf: bool = False
    leveraged_etf_warning: str = ""
    requires_human_review: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ProfitTakingSummary:
    """Profit taking summary. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    total_position_count: int = 0
    stock_profit_plan_count: int = 0
    etf_rebalance_plan_count: int = 0
    first_take_profit_count: int = 0
    second_take_profit_count: int = 0
    runner_protection_count: int = 0
    giveback_warning_count: int = 0
    pressure_zone_reduce_count: int = 0
    leveraged_etf_warning_count: int = 0
    human_review_count: int = 0
    average_unrealized_return_pct: float = 0.0
    top_unrealized_profit_symbols: List[str] = field(default_factory=list)
    top_giveback_risk_symbols: List[str] = field(default_factory=list)
    profit_taking_quality_grade: str = "B"
    rebalancing_quality_grade: str = "B"


@dataclass
class ProfitReviewInput:
    """Input for profit taking review. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    review_period: str = ""
    candidate_plans: List[Dict[str, Any]] = field(default_factory=list)
    etf_items: List[Dict[str, Any]] = field(default_factory=list)
    profit_policy: Optional[ProfitTakingPolicy] = None
    market_state: str = "range_bound"


@dataclass
class ProfitReviewResult:
    """Profit taking review result. v2.0.12. should_auto_apply is always False."""
    schema_version: str = "212"
    paper_only: bool = True
    research_only: bool = True
    profit_taking_recommendation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    profit_review_id: str = ""
    profit_version: str = "2.0.12"
    review_period: str = ""
    profit_policy: Optional[ProfitTakingPolicy] = None
    profit_taking_snapshot: List[CandidateProfitPlan] = field(default_factory=list)
    one_third_profit_plan_snapshot: List[CandidateProfitPlan] = field(default_factory=list)
    trailing_profit_snapshot: List[CandidateProfitPlan] = field(default_factory=list)
    profit_giveback_snapshot: List[CandidateProfitPlan] = field(default_factory=list)
    etf_rebalancing_snapshot: List[ETFRebalancingItem] = field(default_factory=list)
    profit_taking_summary: Optional[ProfitTakingSummary] = None
    profit_warning_queue: List[CandidateProfitPlan] = field(default_factory=list)
    giveback_review_queue: List[CandidateProfitPlan] = field(default_factory=list)
    human_review_queue: List[CandidateProfitPlan] = field(default_factory=list)
    paper_only_safety_snapshot: bool = True
    all_passed: bool = True
    should_auto_apply: bool = False   # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class ProfitTakingExportResult:
    """Export result for profit taking review. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    profit_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class ProfitTakingAuditSnapshot:
    """Audit snapshot for profit taking review. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    profit_review_id: str = ""
    run_metadata: str = ""
    profit_taking_snapshot: str = ""
    etf_rebalancing_snapshot: str = ""
    giveback_snapshot: str = ""
    profit_warning_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class ProfitTakingMarkdownReport:
    """Markdown report for profit taking review. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    profit_review_id: str = ""
    review_period: str = ""
    content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class CandidateProfitPlanCSV:
    """CSV export of candidate profit plans. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    profit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ETFRebalancingCSV:
    """CSV export of ETF rebalancing items. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    profit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ProfitWarningQueueCSV:
    """CSV export of profit warning queue. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    profit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class GivebackReviewQueueCSV:
    """CSV export of giveback review queue. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    profit_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V212HealthSummary:
    """Health summary for v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.12"


@dataclass
class V212ReleaseSummary:
    """Release summary for v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    version: str = "2.0.12"
    release_name: str = RELEASE_NAME


@dataclass
class ProfitSafetyGuard:
    """Safety guard snapshot for profit taking. v2.0.12."""
    schema_version: str = "212"
    paper_only: bool = True
    no_real_orders: bool = True
    no_automatic_profit_taking_action: bool = True
    no_automatic_stop_loss_execution: bool = True
    no_automatic_take_profit_execution: bool = True
    no_automatic_rebalance: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False
    require_profit_plan_before_entry: bool = True
    profit_actions_recommendation_only: bool = True
    etf_rebalance_actions_recommendation_only: bool = True


# ---------------------------------------------------------------------------
# ID helper
# ---------------------------------------------------------------------------

def _make_profit_review_id(review_period: str, plan_count: int) -> str:
    raw = f"v212-{review_period}-n{plan_count}"
    return hashlib.sha256(raw.encode()).hexdigest()[:10]


# ---------------------------------------------------------------------------
# Profit taking calculation helpers
# ---------------------------------------------------------------------------

def _calc_unrealized_return_pct(entry_price: float, current_price: float) -> float:
    if entry_price <= 0:
        return 0.0
    return (current_price - entry_price) / entry_price


def _calc_giveback_from_high(high_watermark_price: float, current_price: float) -> float:
    if high_watermark_price <= 0 or current_price >= high_watermark_price:
        return 0.0
    return (high_watermark_price - current_price) / high_watermark_price


def _calc_trailing_stop_price(high_watermark_price: float, trailing_stop_from_high_pct: float) -> float:
    if high_watermark_price <= 0:
        return 0.0
    return high_watermark_price * (1.0 - trailing_stop_from_high_pct)


def _classify_profit_action(
    unrealized_return_pct: float,
    giveback_from_high_pct: float,
    first_take_profit_triggered: bool,
    second_take_profit_triggered: bool,
    runner_active: bool,
    asset_type: str,
    blocked_by_missing_profit_plan: bool,
    current_price: float,
    trailing_stop_price: float,
    policy: ProfitTakingPolicy,
    has_pressure_signal: bool = False,
    has_blowoff_signal: bool = False,
) -> str:
    """Classify profit action for a stock position. Paper only, no real orders."""
    if blocked_by_missing_profit_plan:
        return "block_new_add"

    # ETF uses rebalancing, not individual profit taking
    if asset_type in ("etf", "leveraged_etf"):
        return "observation_only"

    if unrealized_return_pct < 0:
        return "hold_with_plan"

    # Runner stage: trailing stop management takes priority over giveback escalation
    if second_take_profit_triggered:
        if current_price > 0 and trailing_stop_price > 0 and current_price <= trailing_stop_price:
            return "tighten_trailing_stop"
        if has_blowoff_signal or has_pressure_signal:
            return "reduce_on_pressure"
        # Giveback exceeds max in runner stage — escalate
        if giveback_from_high_pct > policy.max_profit_giveback_pct:
            return "human_review_required"
        return "protect_runner"

    # Giveback exceeds max — escalate
    if giveback_from_high_pct > policy.max_profit_giveback_pct:
        return "human_review_required"

    # Second take-profit threshold
    if first_take_profit_triggered and unrealized_return_pct >= policy.second_take_profit_pct:
        return "take_second_third"

    # First take-profit threshold
    if not first_take_profit_triggered and unrealized_return_pct >= policy.first_take_profit_pct:
        return "take_first_third"

    # Pressure zone before first take-profit
    if has_pressure_signal or has_blowoff_signal:
        return "reduce_on_pressure"

    return "hold_with_plan"


# ---------------------------------------------------------------------------
# ETF rebalancing helpers
# ---------------------------------------------------------------------------

def _classify_rebalance_action(
    current_allocation_pct: float,
    target_allocation_pct: float,
    upper_rebalance_band_pct: float,
    lower_rebalance_band_pct: float,
    is_leveraged_etf: bool,
) -> str:
    """Classify ETF rebalance action. Paper only, no real orders."""
    if is_leveraged_etf and current_allocation_pct > target_allocation_pct:
        return "reduce_leveraged_exposure"
    if current_allocation_pct > upper_rebalance_band_pct:
        return "trim_to_target_band"
    if current_allocation_pct < lower_rebalance_band_pct:
        return "add_back_to_target_band"
    return "within_band_hold"


# ---------------------------------------------------------------------------
# Evaluate single profit plan
# ---------------------------------------------------------------------------

def evaluate_profit_taking_plan(
    plan_id: str,
    symbol: str,
    name: str,
    candidate_id: str,
    theme_id: str,
    sector_id: str,
    asset_type: str,
    entry_price: float,
    current_price: float,
    position_size: int = 1000,
    high_watermark_price: float = 0.0,
    first_take_profit_triggered: bool = False,
    second_take_profit_triggered: bool = False,
    has_profit_plan: bool = True,
    has_pressure_signal: bool = False,
    has_blowoff_signal: bool = False,
    policy: Optional[ProfitTakingPolicy] = None,
) -> CandidateProfitPlan:
    """Evaluate a paper profit taking plan. Paper only, no real orders."""
    if policy is None:
        policy = ProfitTakingPolicy(policy_id="default-policy-v212")

    if high_watermark_price <= 0:
        high_watermark_price = current_price

    unrealized_return_pct = _calc_unrealized_return_pct(entry_price, current_price)
    unrealized_profit_amount = (current_price - entry_price) * position_size if entry_price > 0 else 0.0

    first_tp_price = entry_price * (1.0 + policy.first_take_profit_pct) if entry_price > 0 else 0.0
    second_tp_price = entry_price * (1.0 + policy.second_take_profit_pct) if entry_price > 0 else 0.0
    trailing_stop_price = _calc_trailing_stop_price(high_watermark_price, policy.trailing_stop_from_high_pct)
    giveback_from_high_pct = _calc_giveback_from_high(high_watermark_price, current_price)

    runner_active = first_take_profit_triggered and second_take_profit_triggered
    blocked_by_missing_profit_plan = not has_profit_plan and policy.require_profit_plan_before_entry

    profit_action = _classify_profit_action(
        unrealized_return_pct=unrealized_return_pct,
        giveback_from_high_pct=giveback_from_high_pct,
        first_take_profit_triggered=first_take_profit_triggered,
        second_take_profit_triggered=second_take_profit_triggered,
        runner_active=runner_active,
        asset_type=asset_type,
        blocked_by_missing_profit_plan=blocked_by_missing_profit_plan,
        current_price=current_price,
        trailing_stop_price=trailing_stop_price,
        policy=policy,
        has_pressure_signal=has_pressure_signal,
        has_blowoff_signal=has_blowoff_signal,
    )

    requires_human_review = profit_action == "human_review_required"

    return CandidateProfitPlan(
        schema_version="212",
        paper_only=True,
        no_real_orders=True,
        plan_id=plan_id,
        symbol=symbol,
        name=name,
        candidate_id=candidate_id,
        theme_id=theme_id,
        sector_id=sector_id,
        asset_type=asset_type,
        entry_price=entry_price,
        current_price=current_price,
        unrealized_return_pct=round(unrealized_return_pct, 4),
        unrealized_profit_amount=round(unrealized_profit_amount, 2),
        first_take_profit_price=round(first_tp_price, 2),
        second_take_profit_price=round(second_tp_price, 2),
        trailing_stop_price=round(trailing_stop_price, 2),
        high_watermark_price=round(high_watermark_price, 2),
        giveback_from_high_pct=round(giveback_from_high_pct, 4),
        first_take_profit_triggered=first_take_profit_triggered,
        second_take_profit_triggered=second_take_profit_triggered,
        runner_active=runner_active,
        profit_action=profit_action,
        blocked_by_missing_profit_plan=blocked_by_missing_profit_plan,
        requires_human_review=requires_human_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Evaluate ETF rebalancing
# ---------------------------------------------------------------------------

def evaluate_etf_rebalancing(
    etf_symbol: str,
    etf_name: str,
    target_allocation_pct: float,
    current_allocation_pct: float,
    upper_rebalance_band_pct: float = 0.0,
    lower_rebalance_band_pct: float = 0.0,
    is_leveraged_etf: bool = False,
    policy: Optional[ProfitTakingPolicy] = None,
) -> ETFRebalancingItem:
    """Evaluate ETF rebalancing. Paper only, no real orders."""
    if policy is None:
        policy = ProfitTakingPolicy(policy_id="default-policy-v212")

    if upper_rebalance_band_pct <= 0:
        upper_rebalance_band_pct = target_allocation_pct + 0.10
    if lower_rebalance_band_pct <= 0:
        lower_rebalance_band_pct = target_allocation_pct - 0.05

    overweight_pct = max(0.0, current_allocation_pct - upper_rebalance_band_pct)
    underweight_pct = max(0.0, lower_rebalance_band_pct - current_allocation_pct)

    rebalance_action = _classify_rebalance_action(
        current_allocation_pct=current_allocation_pct,
        target_allocation_pct=target_allocation_pct,
        upper_rebalance_band_pct=upper_rebalance_band_pct,
        lower_rebalance_band_pct=lower_rebalance_band_pct,
        is_leveraged_etf=is_leveraged_etf,
    )

    recommended_trim_pct = max(0.0, current_allocation_pct - target_allocation_pct) if rebalance_action in ("trim_to_target_band", "reduce_leveraged_exposure") else 0.0
    recommended_add_pct = max(0.0, target_allocation_pct - current_allocation_pct) if rebalance_action == "add_back_to_target_band" else 0.0

    leveraged_etf_warning = ""
    if is_leveraged_etf:
        leveraged_etf_warning = "[!] 槓桿ETF僅限短線小部位，不得長期滿倉，不得融資。建議修剪至目標配置。"

    requires_human_review = (rebalance_action == "human_review_required") or (is_leveraged_etf and overweight_pct > 0.05)

    return ETFRebalancingItem(
        schema_version="212",
        paper_only=True,
        no_real_orders=True,
        etf_symbol=etf_symbol,
        etf_name=etf_name,
        target_allocation_pct=round(target_allocation_pct, 4),
        current_allocation_pct=round(current_allocation_pct, 4),
        upper_rebalance_band_pct=round(upper_rebalance_band_pct, 4),
        lower_rebalance_band_pct=round(lower_rebalance_band_pct, 4),
        overweight_pct=round(overweight_pct, 4),
        underweight_pct=round(underweight_pct, 4),
        rebalance_action=rebalance_action,
        recommended_trim_pct=round(recommended_trim_pct, 4),
        recommended_add_pct=round(recommended_add_pct, 4),
        is_leveraged_etf=is_leveraged_etf,
        leveraged_etf_warning=leveraged_etf_warning,
        requires_human_review=requires_human_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Default demo data
# ---------------------------------------------------------------------------

def _default_profit_policy() -> ProfitTakingPolicy:
    return ProfitTakingPolicy(policy_id="default-policy-v212")


def _default_candidate_pool() -> List[Dict[str, Any]]:
    """Return default demo candidate pool. Paper only."""
    return [
        {
            "plan_id": "PP-2330-001", "symbol": "2330", "name": "台積電",
            "candidate_id": "CAND-2330", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH",
            "asset_type": "stock",
            "entry_price": 700.0, "current_price": 855.0, "position_size": 1000,
            "high_watermark_price": 870.0,
            "first_take_profit_triggered": True, "second_take_profit_triggered": False,
            "has_profit_plan": True, "has_pressure_signal": False, "has_blowoff_signal": False,
        },
        {
            "plan_id": "PP-2454-001", "symbol": "2454", "name": "聯發科",
            "candidate_id": "CAND-2454", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH",
            "asset_type": "stock",
            "entry_price": 800.0, "current_price": 1130.0, "position_size": 500,
            "high_watermark_price": 1200.0,
            "first_take_profit_triggered": True, "second_take_profit_triggered": True,
            "has_profit_plan": True, "has_pressure_signal": False, "has_blowoff_signal": True,
        },
        {
            "plan_id": "PP-2382-001", "symbol": "2382", "name": "廣達",
            "candidate_id": "CAND-2382", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH",
            "asset_type": "stock",
            "entry_price": 200.0, "current_price": 245.0, "position_size": 2000,
            "high_watermark_price": 260.0,
            "first_take_profit_triggered": False, "second_take_profit_triggered": False,
            "has_profit_plan": True, "has_pressure_signal": True, "has_blowoff_signal": False,
        },
        {
            "plan_id": "PP-2308-001", "symbol": "2308", "name": "台達電",
            "candidate_id": "CAND-2308", "theme_id": "THEME-EV", "sector_id": "SECTOR-ELEC",
            "asset_type": "stock",
            "entry_price": 350.0, "current_price": 420.0, "position_size": 1000,
            "high_watermark_price": 430.0,
            "first_take_profit_triggered": False, "second_take_profit_triggered": False,
            "has_profit_plan": True, "has_pressure_signal": False, "has_blowoff_signal": False,
        },
        {
            "plan_id": "PP-6669-001", "symbol": "6669", "name": "緯穎",
            "candidate_id": "CAND-6669", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH",
            "asset_type": "stock",
            "entry_price": 1500.0, "current_price": 1720.0, "position_size": 300,
            "high_watermark_price": 1800.0,
            "first_take_profit_triggered": True, "second_take_profit_triggered": True,
            "has_profit_plan": True, "has_pressure_signal": False, "has_blowoff_signal": False,
        },
        {
            "plan_id": "PP-2317-001", "symbol": "2317", "name": "鴻海",
            "candidate_id": "CAND-2317", "theme_id": "THEME-EV", "sector_id": "SECTOR-MFGR",
            "asset_type": "stock",
            "entry_price": 100.0, "current_price": 115.0, "position_size": 2000,
            "high_watermark_price": 115.0,
            "first_take_profit_triggered": False, "second_take_profit_triggered": False,
            "has_profit_plan": False, "has_pressure_signal": False, "has_blowoff_signal": False,
        },
        {
            "plan_id": "PP-3711-001", "symbol": "3711", "name": "日月光",
            "candidate_id": "CAND-3711", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH",
            "asset_type": "stock",
            "entry_price": 130.0, "current_price": 145.0, "position_size": 2000,
            "high_watermark_price": 155.0,
            "first_take_profit_triggered": False, "second_take_profit_triggered": False,
            "has_profit_plan": True, "has_pressure_signal": False, "has_blowoff_signal": False,
        },
        {
            "plan_id": "PP-2303-001", "symbol": "2303", "name": "聯電",
            "candidate_id": "CAND-2303", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH",
            "asset_type": "stock",
            "entry_price": 50.0, "current_price": 43.0, "position_size": 3000,
            "high_watermark_price": 58.0,
            "first_take_profit_triggered": False, "second_take_profit_triggered": False,
            "has_profit_plan": True, "has_pressure_signal": False, "has_blowoff_signal": False,
        },
    ]


def _default_etf_pool() -> List[Dict[str, Any]]:
    """Return default demo ETF pool. Paper only."""
    return [
        {
            "etf_symbol": "0050", "etf_name": "元大台灣50",
            "target_allocation_pct": 0.40, "current_allocation_pct": 0.51,
            "upper_rebalance_band_pct": 0.50, "lower_rebalance_band_pct": 0.35,
            "is_leveraged_etf": False,
        },
        {
            "etf_symbol": "0056", "etf_name": "元大高股息",
            "target_allocation_pct": 0.20, "current_allocation_pct": 0.18,
            "upper_rebalance_band_pct": 0.25, "lower_rebalance_band_pct": 0.15,
            "is_leveraged_etf": False,
        },
        {
            "etf_symbol": "00631L", "etf_name": "元大台灣50正2",
            "target_allocation_pct": 0.05, "current_allocation_pct": 0.09,
            "upper_rebalance_band_pct": 0.08, "lower_rebalance_band_pct": 0.02,
            "is_leveraged_etf": True,
        },
    ]


# ---------------------------------------------------------------------------
# Queue builders
# ---------------------------------------------------------------------------

def detect_giveback_risk(
    plans: Optional[List[CandidateProfitPlan]] = None,
    policy: Optional[ProfitTakingPolicy] = None,
) -> List[CandidateProfitPlan]:
    """Detect positions with significant profit giveback. Paper only."""
    if policy is None:
        policy = _default_profit_policy()
    if plans is None:
        pool = _default_candidate_pool()
        plans = [
            evaluate_profit_taking_plan(
                plan_id=p["plan_id"], symbol=p["symbol"], name=p["name"],
                candidate_id=p["candidate_id"], theme_id=p["theme_id"],
                sector_id=p["sector_id"], asset_type=p["asset_type"],
                entry_price=p["entry_price"], current_price=p["current_price"],
                position_size=p.get("position_size", 1000),
                high_watermark_price=p.get("high_watermark_price", 0.0),
                first_take_profit_triggered=p.get("first_take_profit_triggered", False),
                second_take_profit_triggered=p.get("second_take_profit_triggered", False),
                has_profit_plan=p.get("has_profit_plan", True),
                has_pressure_signal=p.get("has_pressure_signal", False),
                has_blowoff_signal=p.get("has_blowoff_signal", False),
                policy=policy,
            )
            for p in pool
        ]
    return [p for p in plans if p.giveback_from_high_pct > policy.max_profit_giveback_pct]


def build_profit_warning_queue(
    plans: Optional[List[CandidateProfitPlan]] = None,
    policy: Optional[ProfitTakingPolicy] = None,
) -> List[CandidateProfitPlan]:
    """Build profit warning queue. Paper only."""
    if policy is None:
        policy = _default_profit_policy()
    if plans is None:
        pool = _default_candidate_pool()
        plans = [
            evaluate_profit_taking_plan(
                plan_id=p["plan_id"], symbol=p["symbol"], name=p["name"],
                candidate_id=p["candidate_id"], theme_id=p["theme_id"],
                sector_id=p["sector_id"], asset_type=p["asset_type"],
                entry_price=p["entry_price"], current_price=p["current_price"],
                position_size=p.get("position_size", 1000),
                high_watermark_price=p.get("high_watermark_price", 0.0),
                first_take_profit_triggered=p.get("first_take_profit_triggered", False),
                second_take_profit_triggered=p.get("second_take_profit_triggered", False),
                has_profit_plan=p.get("has_profit_plan", True),
                has_pressure_signal=p.get("has_pressure_signal", False),
                has_blowoff_signal=p.get("has_blowoff_signal", False),
                policy=policy,
            )
            for p in pool
        ]
    warning_actions = {"tighten_trailing_stop", "reduce_on_pressure", "human_review_required", "block_new_add"}
    return [p for p in plans if p.profit_action in warning_actions or p.giveback_from_high_pct > policy.max_profit_giveback_pct]


def build_giveback_review_queue(
    plans: Optional[List[CandidateProfitPlan]] = None,
    policy: Optional[ProfitTakingPolicy] = None,
) -> List[CandidateProfitPlan]:
    """Build giveback review queue. Paper only."""
    if policy is None:
        policy = _default_profit_policy()
    if plans is None:
        pool = _default_candidate_pool()
        plans = [
            evaluate_profit_taking_plan(
                plan_id=p["plan_id"], symbol=p["symbol"], name=p["name"],
                candidate_id=p["candidate_id"], theme_id=p["theme_id"],
                sector_id=p["sector_id"], asset_type=p["asset_type"],
                entry_price=p["entry_price"], current_price=p["current_price"],
                position_size=p.get("position_size", 1000),
                high_watermark_price=p.get("high_watermark_price", 0.0),
                first_take_profit_triggered=p.get("first_take_profit_triggered", False),
                second_take_profit_triggered=p.get("second_take_profit_triggered", False),
                has_profit_plan=p.get("has_profit_plan", True),
                has_pressure_signal=p.get("has_pressure_signal", False),
                has_blowoff_signal=p.get("has_blowoff_signal", False),
                policy=policy,
            )
            for p in pool
        ]
    return [p for p in plans if p.giveback_from_high_pct > 0.05]


# ---------------------------------------------------------------------------
# Summary builder
# ---------------------------------------------------------------------------

def _build_profit_taking_summary(
    plans: List[CandidateProfitPlan],
    etf_items: List[ETFRebalancingItem],
) -> ProfitTakingSummary:
    stock_plans = [p for p in plans if p.asset_type == "stock"]
    first_tp = sum(1 for p in plans if p.profit_action == "take_first_third")
    second_tp = sum(1 for p in plans if p.profit_action == "take_second_third")
    runner_prot = sum(1 for p in plans if p.profit_action == "protect_runner")
    giveback_warn = sum(1 for p in plans if p.giveback_from_high_pct > 0.05)
    pressure_reduce = sum(1 for p in plans if p.profit_action == "reduce_on_pressure")
    lev_warn = sum(1 for e in etf_items if e.is_leveraged_etf and e.leveraged_etf_warning)
    human_rv = sum(1 for p in plans if p.requires_human_review)

    returns = [p.unrealized_return_pct for p in plans if p.unrealized_return_pct > 0]
    avg_return = round(sum(returns) / len(returns), 4) if returns else 0.0

    top_profit = sorted(plans, key=lambda p: p.unrealized_return_pct, reverse=True)[:3]
    top_giveback = sorted(plans, key=lambda p: p.giveback_from_high_pct, reverse=True)[:3]

    profit_grade = "A" if first_tp + second_tp + runner_prot > 0 else "B"
    rebalance_grade = "A" if any(e.rebalance_action in ("trim_to_target_band", "add_back_to_target_band") for e in etf_items) else "B"

    return ProfitTakingSummary(
        total_position_count=len(plans),
        stock_profit_plan_count=len(stock_plans),
        etf_rebalance_plan_count=len(etf_items),
        first_take_profit_count=first_tp,
        second_take_profit_count=second_tp,
        runner_protection_count=runner_prot,
        giveback_warning_count=giveback_warn,
        pressure_zone_reduce_count=pressure_reduce,
        leveraged_etf_warning_count=lev_warn,
        human_review_count=human_rv,
        average_unrealized_return_pct=avg_return,
        top_unrealized_profit_symbols=[p.symbol for p in top_profit],
        top_giveback_risk_symbols=[p.symbol for p in top_giveback if p.giveback_from_high_pct > 0],
        profit_taking_quality_grade=profit_grade,
        rebalancing_quality_grade=rebalance_grade,
    )


# ---------------------------------------------------------------------------
# Main review engine
# ---------------------------------------------------------------------------

def run_profit_taking_review(
    review_input: Optional[ProfitReviewInput] = None,
) -> ProfitReviewResult:
    """Run a paper profit taking review. Paper only, no real orders."""
    if review_input is None:
        review_input = ProfitReviewInput(
            review_period="2026-W29",
            candidate_plans=_default_candidate_pool(),
            etf_items=_default_etf_pool(),
        )

    policy = review_input.profit_policy or _default_profit_policy()
    review_id = _make_profit_review_id(review_input.review_period, len(review_input.candidate_plans))

    plans: List[CandidateProfitPlan] = []
    for p in review_input.candidate_plans:
        plan = evaluate_profit_taking_plan(
            plan_id=p.get("plan_id", ""),
            symbol=p.get("symbol", ""),
            name=p.get("name", ""),
            candidate_id=p.get("candidate_id", ""),
            theme_id=p.get("theme_id", ""),
            sector_id=p.get("sector_id", ""),
            asset_type=p.get("asset_type", "stock"),
            entry_price=p.get("entry_price", 0.0),
            current_price=p.get("current_price", 0.0),
            position_size=p.get("position_size", 1000),
            high_watermark_price=p.get("high_watermark_price", 0.0),
            first_take_profit_triggered=p.get("first_take_profit_triggered", False),
            second_take_profit_triggered=p.get("second_take_profit_triggered", False),
            has_profit_plan=p.get("has_profit_plan", True),
            has_pressure_signal=p.get("has_pressure_signal", False),
            has_blowoff_signal=p.get("has_blowoff_signal", False),
            policy=policy,
        )
        plans.append(plan)

    etf_items: List[ETFRebalancingItem] = []
    for e in review_input.etf_items:
        item = evaluate_etf_rebalancing(
            etf_symbol=e.get("etf_symbol", ""),
            etf_name=e.get("etf_name", ""),
            target_allocation_pct=e.get("target_allocation_pct", 0.0),
            current_allocation_pct=e.get("current_allocation_pct", 0.0),
            upper_rebalance_band_pct=e.get("upper_rebalance_band_pct", 0.0),
            lower_rebalance_band_pct=e.get("lower_rebalance_band_pct", 0.0),
            is_leveraged_etf=e.get("is_leveraged_etf", False),
            policy=policy,
        )
        etf_items.append(item)

    one_third_plans = [p for p in plans if p.profit_action in ("take_first_third", "take_second_third")]
    trailing_plans = [p for p in plans if p.profit_action in ("protect_runner", "tighten_trailing_stop")]
    giveback_plans = [p for p in plans if p.giveback_from_high_pct > 0.05]

    warning_actions = {"tighten_trailing_stop", "reduce_on_pressure", "human_review_required", "block_new_add"}
    profit_warning = [p for p in plans if p.profit_action in warning_actions or p.giveback_from_high_pct > policy.max_profit_giveback_pct]
    giveback_queue = [p for p in plans if p.giveback_from_high_pct > 0.05]
    human_queue = [p for p in plans if p.requires_human_review]

    summary = _build_profit_taking_summary(plans, etf_items)

    return ProfitReviewResult(
        profit_review_id=review_id,
        profit_version="2.0.12",
        review_period=review_input.review_period,
        profit_policy=policy,
        profit_taking_snapshot=plans,
        one_third_profit_plan_snapshot=one_third_plans,
        trailing_profit_snapshot=trailing_plans,
        profit_giveback_snapshot=giveback_plans,
        etf_rebalancing_snapshot=etf_items,
        profit_taking_summary=summary,
        profit_warning_queue=profit_warning,
        giveback_review_queue=giveback_queue,
        human_review_queue=human_queue,
        paper_only_safety_snapshot=True,
        all_passed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_profit_taking_json(result: ProfitReviewResult) -> ProfitTakingExportResult:
    """Export profit taking review as JSON. Paper only."""
    import json as _json
    payload = {
        "version": "2.0.12",
        "schema_version": "212",
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "profit_review_id": result.profit_review_id,
        "profit_version": result.profit_version,
        "review_period": result.review_period,
        "position_count": len(result.profit_taking_snapshot),
        "first_take_profit_count": len(result.one_third_profit_plan_snapshot),
        "trailing_plan_count": len(result.trailing_profit_snapshot),
        "giveback_count": len(result.profit_giveback_snapshot),
        "etf_rebalancing_count": len(result.etf_rebalancing_snapshot),
        "profit_warning_count": len(result.profit_warning_queue),
        "human_review_count": len(result.human_review_queue),
    }
    content = _json.dumps(payload, ensure_ascii=False, indent=2)
    return ProfitTakingExportResult(
        profit_review_id=result.profit_review_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
    )


def export_profit_taking_markdown(result: ProfitReviewResult) -> ProfitTakingExportResult:
    """Export profit taking review as Markdown. Paper only."""
    lines = [
        "# Paper Profit Taking Review v2.0.12",
        "",
        f"**Period:** {result.review_period}",
        f"**Profit Review ID:** {result.profit_review_id}",
        f"**Paper Only:** True",
        f"**No Real Orders:** True",
        f"**Should Auto Apply:** False",
        "",
        f"## Positions: {len(result.profit_taking_snapshot)}",
        f"## First Take-Profit Actions: {len(result.one_third_profit_plan_snapshot)}",
        f"## Trailing Plans: {len(result.trailing_profit_snapshot)}",
        f"## Giveback Alerts: {len(result.profit_giveback_snapshot)}",
        f"## ETF Rebalancing: {len(result.etf_rebalancing_snapshot)}",
        f"## Profit Warnings: {len(result.profit_warning_queue)}",
        f"## Human Review: {len(result.human_review_queue)}",
        "",
        "*[!] Paper Only. Not Investment Advice. Profit Taking Actions Are Recommendation Only.*",
    ]
    content = "\n".join(lines)
    return ProfitTakingExportResult(
        profit_review_id=result.profit_review_id,
        export_format="markdown",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
    )


def export_candidate_profit_plan_csv(result: ProfitReviewResult) -> CandidateProfitPlanCSV:
    """Export candidate profit plans as CSV. Paper only."""
    header = "symbol,asset_type,entry_price,current_price,unrealized_return_pct,first_tp_price,second_tp_price,trailing_stop_price,high_watermark,giveback_pct,profit_action,should_auto_apply"
    rows = [header]
    for p in result.profit_taking_snapshot:
        rows.append(
            f"{p.symbol},{p.asset_type},{p.entry_price},{p.current_price},{p.unrealized_return_pct:.4f},"
            f"{p.first_take_profit_price},{p.second_take_profit_price},{p.trailing_stop_price},"
            f"{p.high_watermark_price},{p.giveback_from_high_pct:.4f},{p.profit_action},{p.should_auto_apply}"
        )
    csv_content = "\n".join(rows)
    return CandidateProfitPlanCSV(
        profit_review_id=result.profit_review_id,
        csv_content=csv_content,
        row_count=len(result.profit_taking_snapshot),
        is_valid=True,
    )


def export_etf_rebalancing_csv(result: ProfitReviewResult) -> ETFRebalancingCSV:
    """Export ETF rebalancing items as CSV. Paper only."""
    header = "etf_symbol,etf_name,target_pct,current_pct,upper_band,lower_band,overweight,underweight,rebalance_action,trim_pct,add_pct,is_leveraged,should_auto_apply"
    rows = [header]
    for e in result.etf_rebalancing_snapshot:
        rows.append(
            f"{e.etf_symbol},{e.etf_name},{e.target_allocation_pct:.4f},{e.current_allocation_pct:.4f},"
            f"{e.upper_rebalance_band_pct:.4f},{e.lower_rebalance_band_pct:.4f},"
            f"{e.overweight_pct:.4f},{e.underweight_pct:.4f},{e.rebalance_action},"
            f"{e.recommended_trim_pct:.4f},{e.recommended_add_pct:.4f},{e.is_leveraged_etf},{e.should_auto_apply}"
        )
    csv_content = "\n".join(rows)
    return ETFRebalancingCSV(
        profit_review_id=result.profit_review_id,
        csv_content=csv_content,
        row_count=len(result.etf_rebalancing_snapshot),
        is_valid=True,
    )


def export_profit_warning_queue_csv(result: ProfitReviewResult) -> ProfitWarningQueueCSV:
    """Export profit warning queue as CSV. Paper only."""
    header = "symbol,profit_action,giveback_from_high_pct,requires_human_review,should_auto_apply"
    rows = [header]
    for p in result.profit_warning_queue:
        rows.append(
            f"{p.symbol},{p.profit_action},{p.giveback_from_high_pct:.4f},{p.requires_human_review},{p.should_auto_apply}"
        )
    csv_content = "\n".join(rows)
    return ProfitWarningQueueCSV(
        profit_review_id=result.profit_review_id,
        csv_content=csv_content,
        row_count=len(result.profit_warning_queue),
        is_valid=True,
    )


def export_giveback_review_queue_csv(result: ProfitReviewResult) -> GivebackReviewQueueCSV:
    """Export giveback review queue as CSV. Paper only."""
    header = "symbol,high_watermark_price,current_price,giveback_from_high_pct,profit_action,should_auto_apply"
    rows = [header]
    for p in result.giveback_review_queue:
        rows.append(
            f"{p.symbol},{p.high_watermark_price},{p.current_price},{p.giveback_from_high_pct:.4f},{p.profit_action},{p.should_auto_apply}"
        )
    csv_content = "\n".join(rows)
    return GivebackReviewQueueCSV(
        profit_review_id=result.profit_review_id,
        csv_content=csv_content,
        row_count=len(result.giveback_review_queue),
        is_valid=True,
    )


def export_profit_taking_audit_snapshot(result: ProfitReviewResult) -> ProfitTakingAuditSnapshot:
    """Export profit taking audit snapshot. Paper only."""
    hash_val = hashlib.sha256(
        f"{result.profit_review_id}-{result.review_period}-{len(result.profit_taking_snapshot)}".encode()
    ).hexdigest()[:16]
    return ProfitTakingAuditSnapshot(
        profit_review_id=result.profit_review_id,
        run_metadata="v212-paper-only-profit-taking-audit",
        profit_taking_snapshot=f"positions={len(result.profit_taking_snapshot)}",
        etf_rebalancing_snapshot=f"etf_items={len(result.etf_rebalancing_snapshot)}",
        giveback_snapshot=f"giveback_alerts={len(result.profit_giveback_snapshot)}",
        profit_warning_snapshot=f"warnings={len(result.profit_warning_queue)}",
        safety_snapshot="paper_only=True,no_real_orders=True,should_auto_apply=False,auto_apply_enabled=False",
        reproducibility_hash=hash_val,
        export_status="complete",
    )


# ---------------------------------------------------------------------------
# ETF rebalancing review (standalone)
# ---------------------------------------------------------------------------

def run_etf_rebalancing_review(
    etf_items: Optional[List[Dict[str, Any]]] = None,
    policy: Optional[ProfitTakingPolicy] = None,
) -> List[ETFRebalancingItem]:
    """Run ETF rebalancing review. Paper only, no real orders."""
    if policy is None:
        policy = _default_profit_policy()
    if etf_items is None:
        etf_items = _default_etf_pool()
    return [
        evaluate_etf_rebalancing(
            etf_symbol=e.get("etf_symbol", ""),
            etf_name=e.get("etf_name", ""),
            target_allocation_pct=e.get("target_allocation_pct", 0.0),
            current_allocation_pct=e.get("current_allocation_pct", 0.0),
            upper_rebalance_band_pct=e.get("upper_rebalance_band_pct", 0.0),
            lower_rebalance_band_pct=e.get("lower_rebalance_band_pct", 0.0),
            is_leveraged_etf=e.get("is_leveraged_etf", False),
            policy=policy,
        )
        for e in etf_items
    ]


def evaluate_giveback_risk(
    plans: Optional[List[CandidateProfitPlan]] = None,
    policy: Optional[ProfitTakingPolicy] = None,
) -> Dict[str, Any]:
    """Evaluate giveback risk across plans. Paper only."""
    if policy is None:
        policy = _default_profit_policy()
    giveback_list = detect_giveback_risk(plans=plans, policy=policy)
    return {
        "giveback_risk_count": len(giveback_list),
        "giveback_symbols": [p.symbol for p in giveback_list],
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "schema_version": "212",
    }


# ---------------------------------------------------------------------------
# Version / summary
# ---------------------------------------------------------------------------

def verify_version() -> bool:
    """Verify v2.0.12 version constants are correct."""
    return VERSION == "2.0.12" and SCHEMA_VERSION == "212"


def export_profit_taking_csv(result: ProfitReviewResult) -> CandidateProfitPlanCSV:
    """Export profit taking entries as CSV. Alias for export_candidate_profit_plan_csv. Paper only."""
    return export_candidate_profit_plan_csv(result)


def get_cockpit_summary_v212() -> Dict[str, Any]:
    """Return v2.0.12 cockpit summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "require_profit_plan_before_entry": True,
        "profit_actions_recommendation_only": True,
        "etf_rebalance_actions_recommendation_only": True,
        "profit_action_count": len(PROFIT_ACTIONS),
        "asset_type_count": len(ASSET_TYPES),
        "rebalance_action_count": len(REBALANCE_ACTIONS),
        "cli_command_count": len(CLI_COMMANDS_V212),
        "gui_tab_count": len(GUI_TABS_V212),
        "safety_flag_count": len(SAFETY_FLAGS_V212),
        "model_count": len(_ALL_MODEL_NAMES_V212),
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }
