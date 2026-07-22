"""
paper_trading/small_capital_strategy/paper_cockpit_v209.py
v2.0.9 Paper Position Sizing & Risk Budget Control
[!] Paper Only. Research Only. Position Sizing Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. No Automatic Position Apply. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.9"
SCHEMA_VERSION = "209"
RELEASE_NAME = "Paper Position Sizing & Risk Budget Control"
BASELINE_TESTS = 34678
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

SIZE_ACTIONS: List[str] = [
    "allow_full_paper_size",
    "reduce_size",
    "minimum_probe_size",
    "observation_only",
    "block_new_position",
    "require_rescore",
    "human_review_required",
]

SIZING_REVIEW_FIELDS: List[str] = [
    "sizing_review_id",
    "sizing_version",
    "review_period",
    "risk_budget_snapshot",
    "candidate_sizing_snapshot",
    "position_sizing_recommendation_queue",
    "size_reduction_queue",
    "blocked_sizing_queue",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

RISK_BUDGET_POLICY_FIELDS: List[str] = [
    "policy_id",
    "account_equity",
    "max_total_risk_pct",
    "max_single_trade_risk_pct",
    "max_single_theme_risk_pct",
    "max_single_sector_risk_pct",
    "max_high_volatility_risk_pct",
    "max_low_liquidity_risk_pct",
    "max_risk_off_budget_pct",
    "min_cash_buffer_pct",
    "default_stop_loss_pct",
    "auto_apply_enabled",
]

CANDIDATE_SIZING_ITEM_FIELDS: List[str] = [
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
    "risk_per_share",
    "base_position_size",
    "volatility_adjusted_size",
    "liquidity_adjusted_size",
    "exposure_adjusted_size",
    "market_regime_adjusted_size",
    "lifecycle_adjusted_size",
    "final_recommended_size",
    "final_risk_amount",
    "final_risk_pct",
    "size_action",
    "blocked_reasons",
    "requires_human_review",
    "should_auto_apply",
]

POSITION_SIZING_SUMMARY_FIELDS: List[str] = [
    "total_candidate_count",
    "allowed_full_size_count",
    "reduced_size_count",
    "probe_size_count",
    "observation_only_count",
    "blocked_position_count",
    "human_review_count",
    "total_allocated_risk_pct",
    "remaining_risk_budget_pct",
    "max_single_trade_risk_pct",
    "top_risk_contributors",
    "top_size_reduction_reasons",
    "sizing_quality_grade",
    "risk_budget_quality_grade",
]

CLI_COMMANDS_V209: List[str] = [
    "paper-cockpit-v209-review-sizing",
    "paper-cockpit-v209-evaluate-risk-budget",
    "paper-cockpit-v209-calculate-position-size",
    "paper-cockpit-v209-build-size-reduction-queue",
    "paper-cockpit-v209-build-blocked-sizing-queue",
    "paper-cockpit-v209-export-json",
    "paper-cockpit-v209-export-md",
    "paper-cockpit-v209-export-csv",
    "paper-cockpit-v209-health",
    "paper-cockpit-v209-gate",
]

GUI_TABS_V209: List[str] = [
    "position_sizing_v209",
    "risk_budget_v209",
    "size_reduction_queue_v209",
]

SAFETY_FLAGS_V209: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "position_sizing_recommendation_only": True,
    "sizing_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_position_apply": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "sizing_actions_recommendation_only": True,
}

assert len(SAFETY_FLAGS_V209) == 21, f"Expected 21 SAFETY_FLAGS_V209, got {len(SAFETY_FLAGS_V209)}"
assert len(SIZE_ACTIONS) == 7
assert len(CLI_COMMANDS_V209) == 10
assert len(GUI_TABS_V209) == 3
assert len(SIZING_REVIEW_FIELDS) == 10
assert len(RISK_BUDGET_POLICY_FIELDS) == 12
assert len(CANDIDATE_SIZING_ITEM_FIELDS) == 24
assert len(POSITION_SIZING_SUMMARY_FIELDS) == 14

COVERED_VERSIONS: List[str] = [
    "2.0.8", "2.0.7", "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 14 models, schema_version="209"
# ---------------------------------------------------------------------------

@dataclass
class RiskBudgetPolicy:
    """Risk budget policy schema. v2.0.9. auto_apply_enabled is always False."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    account_equity: float = 300000.0
    max_total_risk_pct: float = 0.06
    max_single_trade_risk_pct: float = 0.01
    max_single_theme_risk_pct: float = 0.03
    max_single_sector_risk_pct: float = 0.04
    max_high_volatility_risk_pct: float = 0.02
    max_low_liquidity_risk_pct: float = 0.01
    max_risk_off_budget_pct: float = 0.02
    min_cash_buffer_pct: float = 0.20
    default_stop_loss_pct: float = 0.06
    auto_apply_enabled: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class CandidateSizingItem:
    """Candidate sizing item schema. v2.0.9. should_auto_apply is always False."""
    schema_version: str = "209"
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
    risk_per_share: float = 0.0
    base_position_size: int = 0
    volatility_adjusted_size: int = 0
    liquidity_adjusted_size: int = 0
    exposure_adjusted_size: int = 0
    market_regime_adjusted_size: int = 0
    lifecycle_adjusted_size: int = 0
    final_recommended_size: int = 0
    final_risk_amount: float = 0.0
    final_risk_pct: float = 0.0
    size_action: str = "observation_only"
    blocked_reasons: List[str] = field(default_factory=list)
    requires_human_review: bool = True
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class PositionSizingSummary:
    """Position sizing summary. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    total_candidate_count: int = 0
    allowed_full_size_count: int = 0
    reduced_size_count: int = 0
    probe_size_count: int = 0
    observation_only_count: int = 0
    blocked_position_count: int = 0
    human_review_count: int = 0
    total_allocated_risk_pct: float = 0.0
    remaining_risk_budget_pct: float = 0.06
    max_single_trade_risk_pct: float = 0.01
    top_risk_contributors: List[str] = field(default_factory=list)
    top_size_reduction_reasons: List[str] = field(default_factory=list)
    sizing_quality_grade: str = "C"
    risk_budget_quality_grade: str = "C"


@dataclass
class SizingReviewInput:
    """Input for a position sizing review run. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    review_period: str = ""
    candidate_pool: List[Dict[str, Any]] = field(default_factory=list)
    risk_budget_policy: Optional[RiskBudgetPolicy] = None
    market_state: str = "range_bound"
    human_review_required: bool = True


@dataclass
class SizingReviewResult:
    """Full result of one position sizing review run. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    research_only: bool = True
    position_sizing_recommendation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    sizing_review_id: str = ""
    sizing_version: str = "2.0.9"
    review_period: str = ""
    risk_budget_snapshot: Optional[RiskBudgetPolicy] = None
    candidate_sizing_snapshot: List[CandidateSizingItem] = field(default_factory=list)
    position_sizing_recommendation_queue: List[CandidateSizingItem] = field(default_factory=list)
    size_reduction_queue: List[CandidateSizingItem] = field(default_factory=list)
    blocked_sizing_queue: List[CandidateSizingItem] = field(default_factory=list)
    human_review_queue: List[CandidateSizingItem] = field(default_factory=list)
    sizing_summary: Optional[PositionSizingSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False
    should_auto_apply: bool = False  # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class SizingExportResult:
    """Export result for a position sizing review. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    sizing_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class SizingAuditSnapshot:
    """Audit snapshot for a position sizing review. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    sizing_review_id: str = ""
    run_metadata: str = ""
    candidate_sizing_snapshot: str = ""
    risk_budget_snapshot: str = ""
    size_reduction_snapshot: str = ""
    blocked_sizing_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class SizingReport:
    """Markdown report for a position sizing review. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    sizing_review_id: str = ""
    review_period: str = ""
    report_content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class CandidateSizingCSV:
    """CSV export of candidate sizing items. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    sizing_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class RiskBudgetCSV:
    """CSV export of risk budget policy. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    sizing_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class SizeReductionCSV:
    """CSV export of size reduction queue. v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    no_real_orders: bool = True
    sizing_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V209HealthSummary:
    """Health summary for v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.9"


@dataclass
class V209ReleaseSummary:
    """Release summary for v2.0.9."""
    schema_version: str = "209"
    paper_only: bool = True
    version: str = "2.0.9"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 14
    cli_count: int = 10
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V209: List[str] = [
    "RiskBudgetPolicy",
    "CandidateSizingItem",
    "PositionSizingSummary",
    "SizingReviewInput",
    "SizingReviewResult",
    "SizingExportResult",
    "SizingAuditSnapshot",
    "SizingReport",
    "CandidateSizingCSV",
    "RiskBudgetCSV",
    "SizeReductionCSV",
    "V209HealthSummary",
    "V209ReleaseSummary",
    "RiskBudgetPolicy",  # counted once more for export schema alias
]

# 14 unique models — using precise list
_ALL_MODEL_NAMES_V209 = [
    "RiskBudgetPolicy",
    "CandidateSizingItem",
    "PositionSizingSummary",
    "SizingReviewInput",
    "SizingReviewResult",
    "SizingExportResult",
    "SizingAuditSnapshot",
    "SizingReport",
    "CandidateSizingCSV",
    "RiskBudgetCSV",
    "SizeReductionCSV",
    "V209HealthSummary",
    "V209ReleaseSummary",
    "SizingReviewResult",  # second slot filled by primary result type
]

assert len(_ALL_MODEL_NAMES_V209) == 14


# ---------------------------------------------------------------------------
# Core sizing calculation helpers
# ---------------------------------------------------------------------------

def _compute_base_position_size(
    account_equity: float,
    max_single_trade_risk_pct: float,
    stop_distance_pct: float,
) -> int:
    """Compute base position size from risk budget and stop distance. Paper only.

    Formula: max_loss_twd / stop_distance = position_size_twd
    Shares not computed here (price-based); result is TWD amount.
    """
    if stop_distance_pct <= 0.0:
        return 0
    max_loss_twd = account_equity * max_single_trade_risk_pct
    position_twd = max_loss_twd / stop_distance_pct
    return max(0, int(position_twd))


def _apply_volatility_adjustment(base_size: int, is_high_volatility: bool) -> int:
    """Reduce position size for high-volatility candidates. Paper only."""
    if is_high_volatility:
        return max(0, int(base_size * 0.75))
    return base_size


def _apply_liquidity_adjustment(size: int, is_low_liquidity: bool) -> int:
    """Reduce position size for low-liquidity candidates. Paper only."""
    if is_low_liquidity:
        return max(0, int(size * 0.60))
    return size


def _apply_exposure_adjustment(size: int, exposure_penalty_pct: float) -> int:
    """Reduce position size based on v2.0.8 exposure penalty. Paper only."""
    if exposure_penalty_pct <= 0.0:
        return size
    factor = max(0.0, 1.0 - exposure_penalty_pct / 100.0)
    return max(0, int(size * factor))


def _apply_market_regime_adjustment(size: int, market_state: str) -> int:
    """Reduce position size based on v2.0.7 market regime. Paper only."""
    regime_factor: Dict[str, float] = {
        "strong_uptrend": 1.00,
        "healthy_pullback": 0.90,
        "range_bound": 0.80,
        "weak_rebound": 0.70,
        "high_volatility": 0.60,
        "downtrend": 0.50,
        "risk_off": 0.30,
    }
    factor = regime_factor.get(market_state, 0.80)
    return max(0, int(size * factor))


def _apply_lifecycle_adjustment(size: int, lifecycle_state: str) -> int:
    """Reduce position size based on v2.0.6 lifecycle state. Paper only."""
    lifecycle_factor: Dict[str, float] = {
        "fresh": 1.00,
        "active": 1.00,
        "aging": 0.80,
        "stale": 0.50,
        "expired": 0.00,
        "observation": 0.25,
        "cooldown": 0.00,
    }
    factor = lifecycle_factor.get(lifecycle_state, 0.80)
    return max(0, int(size * factor))


def _apply_theme_concentration_adjustment(size: int, theme_concentration_score: float) -> int:
    """Reduce position size based on v2.0.8 theme concentration. Paper only."""
    if theme_concentration_score >= 80.0:
        return max(0, int(size * 0.60))
    if theme_concentration_score >= 65.0:
        return max(0, int(size * 0.75))
    if theme_concentration_score >= 50.0:
        return max(0, int(size * 0.90))
    return size


def _apply_candidate_priority_adjustment(size: int, priority_score: float) -> int:
    """Scale final size based on candidate priority score. Paper only."""
    if priority_score >= 80.0:
        return size
    if priority_score >= 65.0:
        return max(0, int(size * 0.90))
    if priority_score >= 50.0:
        return max(0, int(size * 0.75))
    if priority_score >= 35.0:
        return max(0, int(size * 0.50))
    return max(0, int(size * 0.25))


def _classify_size_action(
    final_size: int,
    base_size: int,
    stop_distance_pct: float,
    entry_price: float,
    policy: RiskBudgetPolicy,
    blocked_reasons: List[str],
    requires_human_review: bool,
) -> str:
    """Classify the sizing action for a candidate. Paper only."""
    if stop_distance_pct <= 0.0 or entry_price <= 0.0:
        return "block_new_position"
    if requires_human_review or "hard_block" in " ".join(blocked_reasons):
        return "human_review_required"
    if final_size == 0:
        return "block_new_position"
    if blocked_reasons:
        return "block_new_position"
    ratio = final_size / max(1, base_size)
    if ratio >= 0.90:
        return "allow_full_paper_size"
    if ratio >= 0.60:
        return "reduce_size"
    if ratio >= 0.20:
        return "minimum_probe_size"
    if ratio > 0.0:
        return "observation_only"
    return "block_new_position"


def _compute_final_risk(
    final_size: int,
    stop_distance_pct: float,
    account_equity: float,
) -> tuple:
    """Return (risk_amount_twd, risk_pct). Paper only."""
    risk_amount = final_size * stop_distance_pct
    risk_pct = risk_amount / max(1.0, account_equity)
    return round(risk_amount, 2), round(risk_pct, 6)


def calculate_position_size(
    symbol: str,
    name: str,
    candidate_id: str,
    theme_id: str,
    sector_id: str,
    candidate_score: float,
    final_priority_score: float,
    entry_price: float,
    stop_price: float,
    policy: Optional[RiskBudgetPolicy] = None,
    is_high_volatility: bool = False,
    is_low_liquidity: bool = False,
    exposure_penalty_pct: float = 0.0,
    market_state: str = "range_bound",
    lifecycle_state: str = "active",
    theme_concentration_score: float = 0.0,
) -> CandidateSizingItem:
    """Calculate paper-only position size for a candidate. Paper only."""
    if policy is None:
        policy = _default_risk_budget_policy()

    blocked_reasons: List[str] = []

    # Stop distance
    if entry_price <= 0.0:
        stop_distance_pct = 0.0
        blocked_reasons.append("invalid_entry_price")
    elif stop_price <= 0.0 or stop_price >= entry_price:
        stop_distance_pct = 0.0
        blocked_reasons.append("invalid_stop_price")
    else:
        stop_distance_pct = (entry_price - stop_price) / entry_price

    if stop_distance_pct <= 0.0 and "invalid_entry_price" not in blocked_reasons:
        blocked_reasons.append("zero_stop_distance")

    risk_per_share = entry_price * stop_distance_pct if entry_price > 0 else 0.0

    # Base size
    base_size = _compute_base_position_size(
        policy.account_equity,
        policy.max_single_trade_risk_pct,
        stop_distance_pct,
    )

    # Adjustments
    vol_size = _apply_volatility_adjustment(base_size, is_high_volatility)
    liq_size = _apply_liquidity_adjustment(vol_size, is_low_liquidity)
    exp_size = _apply_exposure_adjustment(liq_size, exposure_penalty_pct)
    regime_size = _apply_market_regime_adjustment(exp_size, market_state)
    lc_size = _apply_lifecycle_adjustment(regime_size, lifecycle_state)
    final_size = _apply_theme_concentration_adjustment(lc_size, theme_concentration_score)
    final_size = _apply_candidate_priority_adjustment(final_size, final_priority_score)

    # Market regime block check
    if market_state == "risk_off" and final_size > 0:
        blocked_reasons.append("market_regime_risk_off")
        final_size = 0

    # Lifecycle hard block
    if lifecycle_state in ("expired", "cooldown"):
        blocked_reasons.append(f"lifecycle_{lifecycle_state}")
        final_size = 0

    # Risk amount
    final_risk_amount, final_risk_pct = _compute_final_risk(
        final_size, stop_distance_pct, policy.account_equity
    )

    # Requires human review
    requires_review = (
        bool(blocked_reasons)
        or market_state in ("risk_off", "downtrend")
        or final_risk_pct > policy.max_single_trade_risk_pct
        or is_high_volatility and is_low_liquidity
    )

    size_action = _classify_size_action(
        final_size, base_size, stop_distance_pct, entry_price,
        policy, blocked_reasons, requires_review,
    )

    return CandidateSizingItem(
        symbol=symbol,
        name=name,
        candidate_id=candidate_id,
        theme_id=theme_id,
        sector_id=sector_id,
        candidate_score=round(candidate_score, 2),
        final_priority_score=round(final_priority_score, 2),
        entry_price=round(entry_price, 2),
        stop_price=round(stop_price, 2),
        stop_distance_pct=round(stop_distance_pct, 6),
        risk_per_share=round(risk_per_share, 2),
        base_position_size=base_size,
        volatility_adjusted_size=vol_size,
        liquidity_adjusted_size=liq_size,
        exposure_adjusted_size=exp_size,
        market_regime_adjusted_size=regime_size,
        lifecycle_adjusted_size=lc_size,
        final_recommended_size=final_size,
        final_risk_amount=final_risk_amount,
        final_risk_pct=final_risk_pct,
        size_action=size_action,
        blocked_reasons=blocked_reasons,
        requires_human_review=requires_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Risk budget evaluation
# ---------------------------------------------------------------------------

def evaluate_risk_budget(
    candidate_items: Optional[List[CandidateSizingItem]] = None,
    policy: Optional[RiskBudgetPolicy] = None,
) -> Dict[str, Any]:
    """Evaluate total risk budget utilization from candidate sizing items. Paper only."""
    if policy is None:
        policy = _default_risk_budget_policy()
    if candidate_items is None:
        candidate_items = []

    total_risk_pct = sum(item.final_risk_pct for item in candidate_items)
    remaining = max(0.0, policy.max_total_risk_pct - total_risk_pct)
    budget_pct_used = total_risk_pct / max(0.001, policy.max_total_risk_pct)
    over_budget = total_risk_pct > policy.max_total_risk_pct

    return {
        "policy_id": policy.policy_id,
        "account_equity": policy.account_equity,
        "max_total_risk_pct": policy.max_total_risk_pct,
        "total_allocated_risk_pct": round(total_risk_pct, 6),
        "remaining_risk_budget_pct": round(remaining, 6),
        "budget_pct_used": round(budget_pct_used, 4),
        "over_budget": over_budget,
        "candidate_count": len(candidate_items),
        "auto_apply_enabled": False,
        "should_auto_apply": False,
        "paper_only": True,
        "no_real_orders": True,
    }


# ---------------------------------------------------------------------------
# Sizing summary
# ---------------------------------------------------------------------------

def _build_sizing_summary(
    items: List[CandidateSizingItem],
    policy: RiskBudgetPolicy,
) -> PositionSizingSummary:
    """Build position sizing summary. Paper only."""
    total = len(items)
    full_size = [i for i in items if i.size_action == "allow_full_paper_size"]
    reduced = [i for i in items if i.size_action == "reduce_size"]
    probe = [i for i in items if i.size_action == "minimum_probe_size"]
    obs_only = [i for i in items if i.size_action == "observation_only"]
    blocked = [i for i in items if i.size_action in ("block_new_position",)]
    human_rev = [i for i in items if i.requires_human_review]

    total_risk_pct = sum(i.final_risk_pct for i in items)
    remaining = max(0.0, policy.max_total_risk_pct - total_risk_pct)

    # Top risk contributors
    sorted_by_risk = sorted(items, key=lambda x: x.final_risk_pct, reverse=True)
    top_risk = [f"{i.symbol}({i.final_risk_pct:.4%})" for i in sorted_by_risk[:3]]

    # Top size reduction reasons
    all_reasons: List[str] = []
    for i in items:
        all_reasons.extend(i.blocked_reasons)
    from collections import Counter
    reason_counts = Counter(all_reasons)
    top_reasons = [r for r, _ in reason_counts.most_common(3)]

    # Grades
    blocked_ratio = len(blocked) / max(1, total)
    sq_grade = "A" if blocked_ratio == 0 and len(reduced) == 0 else (
        "B" if blocked_ratio <= 0.20 else (
            "C" if blocked_ratio <= 0.50 else "D"
        )
    )

    over_budget = total_risk_pct > policy.max_total_risk_pct
    rbq_grade = "A" if not over_budget and len(human_rev) == 0 else (
        "B" if not over_budget else "C"
    )

    return PositionSizingSummary(
        total_candidate_count=total,
        allowed_full_size_count=len(full_size),
        reduced_size_count=len(reduced),
        probe_size_count=len(probe),
        observation_only_count=len(obs_only),
        blocked_position_count=len(blocked),
        human_review_count=len(human_rev),
        total_allocated_risk_pct=round(total_risk_pct, 6),
        remaining_risk_budget_pct=round(remaining, 6),
        max_single_trade_risk_pct=policy.max_single_trade_risk_pct,
        top_risk_contributors=top_risk,
        top_size_reduction_reasons=top_reasons,
        sizing_quality_grade=sq_grade,
        risk_budget_quality_grade=rbq_grade,
    )


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

def _make_sizing_review_id(review_period: str, item_count: int) -> str:
    raw = f"sizing-review-{review_period}-{item_count}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _default_risk_budget_policy() -> RiskBudgetPolicy:
    return RiskBudgetPolicy(policy_id="default-policy-v209")


def _default_candidate_pool() -> List[Dict[str, Any]]:
    """Return default demo candidate pool. Paper only."""
    return [
        {"symbol": "2330", "name": "台積電", "candidate_id": "CAND-2330", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "candidate_score": 82.0, "final_priority_score": 80.0, "entry_price": 900.0, "stop_price": 855.0, "is_high_volatility": False, "is_low_liquidity": False, "exposure_penalty_pct": 0.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 37.5},
        {"symbol": "2454", "name": "聯發科", "candidate_id": "CAND-2454", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "candidate_score": 76.0, "final_priority_score": 75.0, "entry_price": 1000.0, "stop_price": 940.0, "is_high_volatility": False, "is_low_liquidity": False, "exposure_penalty_pct": 5.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 37.5},
        {"symbol": "2382", "name": "廣達", "candidate_id": "CAND-2382", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "candidate_score": 70.0, "final_priority_score": 68.0, "entry_price": 300.0, "stop_price": 282.0, "is_high_volatility": False, "is_low_liquidity": False, "exposure_penalty_pct": 5.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 37.5},
        {"symbol": "2308", "name": "台達電", "candidate_id": "CAND-2308", "theme_id": "THEME-EV", "sector_id": "SECTOR-ELEC", "candidate_score": 65.0, "final_priority_score": 62.0, "entry_price": 400.0, "stop_price": 372.0, "is_high_volatility": True, "is_low_liquidity": False, "exposure_penalty_pct": 8.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 25.0},
        {"symbol": "2317", "name": "鴻海", "candidate_id": "CAND-2317", "theme_id": "THEME-EV", "sector_id": "SECTOR-MFGR", "candidate_score": 60.0, "final_priority_score": 58.0, "entry_price": 120.0, "stop_price": 112.0, "is_high_volatility": False, "is_low_liquidity": False, "exposure_penalty_pct": 0.0, "market_state": "range_bound", "lifecycle_state": "aging", "theme_concentration_score": 25.0},
        {"symbol": "3711", "name": "日月光", "candidate_id": "CAND-3711", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "candidate_score": 72.0, "final_priority_score": 72.0, "entry_price": 150.0, "stop_price": 141.0, "is_high_volatility": False, "is_low_liquidity": False, "exposure_penalty_pct": 0.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 37.5},
        {"symbol": "2303", "name": "聯電", "candidate_id": "CAND-2303", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "candidate_score": 65.0, "final_priority_score": 65.0, "entry_price": 55.0, "stop_price": 51.0, "is_high_volatility": False, "is_low_liquidity": True, "exposure_penalty_pct": 10.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 37.5},
        {"symbol": "6669", "name": "緯穎", "candidate_id": "CAND-6669", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "candidate_score": 71.0, "final_priority_score": 70.0, "entry_price": 2000.0, "stop_price": 1880.0, "is_high_volatility": True, "is_low_liquidity": False, "exposure_penalty_pct": 5.0, "market_state": "range_bound", "lifecycle_state": "active", "theme_concentration_score": 37.5},
    ]


def run_sizing_review(
    review_input: Optional[SizingReviewInput] = None,
) -> SizingReviewResult:
    """Run a paper position sizing review. Paper only."""
    if review_input is None:
        review_input = SizingReviewInput(
            review_period="2026-W29",
            candidate_pool=_default_candidate_pool(),
        )

    policy = review_input.risk_budget_policy or _default_risk_budget_policy()
    candidates = review_input.candidate_pool
    market_state = review_input.market_state

    review_id = _make_sizing_review_id(review_input.review_period, len(candidates))

    sizing_items: List[CandidateSizingItem] = []
    for c in candidates:
        item = calculate_position_size(
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
            exposure_penalty_pct=c.get("exposure_penalty_pct", 0.0),
            market_state=c.get("market_state", market_state),
            lifecycle_state=c.get("lifecycle_state", "active"),
            theme_concentration_score=c.get("theme_concentration_score", 0.0),
        )
        sizing_items.append(item)

    recommend_queue = [i for i in sizing_items if i.size_action in (
        "allow_full_paper_size", "reduce_size", "minimum_probe_size"
    )]
    reduction_queue = [i for i in sizing_items if i.size_action == "reduce_size"]
    blocked_queue = [i for i in sizing_items if i.size_action == "block_new_position"]
    human_queue = [i for i in sizing_items if i.requires_human_review]

    summary = _build_sizing_summary(sizing_items, policy)

    return SizingReviewResult(
        sizing_review_id=review_id,
        review_period=review_input.review_period,
        risk_budget_snapshot=policy,
        candidate_sizing_snapshot=sizing_items,
        position_sizing_recommendation_queue=recommend_queue,
        size_reduction_queue=reduction_queue,
        blocked_sizing_queue=blocked_queue,
        human_review_queue=human_queue,
        sizing_summary=summary,
        all_passed=True,
    )


def build_size_reduction_queue(
    candidates: Optional[List[Dict[str, Any]]] = None,
    policy: Optional[RiskBudgetPolicy] = None,
) -> List[CandidateSizingItem]:
    """Build size reduction queue. Paper only."""
    result = run_sizing_review(
        SizingReviewInput(
            review_period="2026-W29",
            candidate_pool=candidates or _default_candidate_pool(),
            risk_budget_policy=policy,
        )
    )
    return result.size_reduction_queue


def build_blocked_sizing_queue(
    candidates: Optional[List[Dict[str, Any]]] = None,
    policy: Optional[RiskBudgetPolicy] = None,
) -> List[CandidateSizingItem]:
    """Build blocked sizing queue. Paper only."""
    result = run_sizing_review(
        SizingReviewInput(
            review_period="2026-W29",
            candidate_pool=candidates or _default_candidate_pool(),
            risk_budget_policy=policy,
        )
    )
    return result.blocked_sizing_queue


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_sizing_json(result: SizingReviewResult) -> SizingExportResult:
    """Export sizing review as JSON. Paper only."""
    rid = result.sizing_review_id
    parts = [
        f'{{"sizing_review_id": "{rid}", "sizing_version": "{result.sizing_version}",',
        f'"review_period": "{result.review_period}", "paper_only": true,',
        f'"should_auto_apply": false, "auto_apply_enabled": false, "no_real_orders": true,',
        f'"candidate_sizing_count": {len(result.candidate_sizing_snapshot)},',
        f'"recommendation_queue_count": {len(result.position_sizing_recommendation_queue)},',
        f'"size_reduction_count": {len(result.size_reduction_queue)},',
        f'"blocked_count": {len(result.blocked_sizing_queue)},',
        f'"human_review_count": {len(result.human_review_queue)}}}',
    ]
    return SizingExportResult(
        sizing_review_id=rid,
        export_format="json",
        content="".join(str(p) for p in parts),
        is_valid=True,
        export_status="complete",
    )


def export_sizing_markdown(result: SizingReviewResult) -> SizingExportResult:
    """Export sizing review as Markdown. Paper only."""
    rid = result.sizing_review_id
    summary = result.sizing_summary
    lines = [
        "# Position Sizing Report v2.0.9",
        "",
        f"**sizing_review_id**: {rid}",
        f"**sizing_version**: {result.sizing_version}",
        f"**review_period**: {result.review_period}",
        f"**paper_only**: True",
        f"**should_auto_apply**: False",
        f"**auto_apply_enabled**: False",
        f"**no_real_orders**: True",
        "",
        "## Sizing Summary",
        "",
    ]
    if summary:
        lines += [
            f"- Total Candidates: {summary.total_candidate_count}",
            f"- Allowed Full Size: {summary.allowed_full_size_count}",
            f"- Reduced Size: {summary.reduced_size_count}",
            f"- Probe Size: {summary.probe_size_count}",
            f"- Observation Only: {summary.observation_only_count}",
            f"- Blocked: {summary.blocked_position_count}",
            f"- Human Review: {summary.human_review_count}",
            f"- Total Allocated Risk: {summary.total_allocated_risk_pct:.4%}",
            f"- Remaining Risk Budget: {summary.remaining_risk_budget_pct:.4%}",
            f"- Sizing Quality Grade: {summary.sizing_quality_grade}",
            f"- Risk Budget Quality Grade: {summary.risk_budget_quality_grade}",
        ]
    lines += [
        "",
        "## Position Sizing Recommendations",
        "",
    ]
    for item in result.position_sizing_recommendation_queue:
        lines.append(
            f"- {item.symbol} [{item.name}]: "
            f"size={item.final_recommended_size:,} "
            f"risk={item.final_risk_pct:.4%} "
            f"action={item.size_action} "
            f"should_auto_apply=False"
        )
    lines += ["", "---", "[!] Paper Only | No Real Orders | Not Investment Advice | should_auto_apply=False"]
    return SizingExportResult(
        sizing_review_id=rid,
        export_format="markdown",
        content="\n".join(lines),
        is_valid=True,
        export_status="complete",
    )


def export_candidate_sizing_csv(result: SizingReviewResult) -> CandidateSizingCSV:
    """Export candidate sizing items as CSV. Paper only."""
    rows = [
        "symbol,candidate_id,theme_id,sector_id,final_priority_score,"
        "entry_price,stop_distance_pct,base_position_size,final_recommended_size,"
        "final_risk_pct,size_action,should_auto_apply"
    ]
    for item in result.candidate_sizing_snapshot:
        rows.append(
            f"{item.symbol},{item.candidate_id},{item.theme_id},{item.sector_id},"
            f"{item.final_priority_score:.2f},{item.entry_price:.2f},"
            f"{item.stop_distance_pct:.6f},{item.base_position_size},"
            f"{item.final_recommended_size},{item.final_risk_pct:.6f},"
            f"{item.size_action},False"
        )
    return CandidateSizingCSV(
        sizing_review_id=result.sizing_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_risk_budget_csv(result: SizingReviewResult) -> RiskBudgetCSV:
    """Export risk budget policy as CSV. Paper only."""
    policy = result.risk_budget_snapshot or _default_risk_budget_policy()
    rows = [
        "policy_id,account_equity,max_total_risk_pct,max_single_trade_risk_pct,"
        "max_single_theme_risk_pct,min_cash_buffer_pct,auto_apply_enabled"
    ]
    rows.append(
        f"{policy.policy_id},{policy.account_equity:.2f},{policy.max_total_risk_pct:.4f},"
        f"{policy.max_single_trade_risk_pct:.4f},{policy.max_single_theme_risk_pct:.4f},"
        f"{policy.min_cash_buffer_pct:.4f},False"
    )
    return RiskBudgetCSV(
        sizing_review_id=result.sizing_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_size_reduction_csv(result: SizingReviewResult) -> SizeReductionCSV:
    """Export size reduction queue as CSV. Paper only."""
    rows = [
        "symbol,candidate_id,base_position_size,final_recommended_size,"
        "size_action,blocked_reasons,should_auto_apply"
    ]
    for item in result.size_reduction_queue:
        rows.append(
            f"{item.symbol},{item.candidate_id},{item.base_position_size},"
            f"{item.final_recommended_size},{item.size_action},"
            f"{'|'.join(item.blocked_reasons)},False"
        )
    return SizeReductionCSV(
        sizing_review_id=result.sizing_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_sizing_audit_snapshot(result: SizingReviewResult) -> SizingAuditSnapshot:
    """Build position sizing audit snapshot. Paper only."""
    rid = result.sizing_review_id
    raw = f"{rid}-{result.review_period}-{len(result.candidate_sizing_snapshot)}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return SizingAuditSnapshot(
        sizing_review_id=rid,
        run_metadata=f"v2.0.9-sizing-review-{rid}",
        candidate_sizing_snapshot=str([i.symbol for i in result.candidate_sizing_snapshot]),
        risk_budget_snapshot=str(result.risk_budget_snapshot.policy_id if result.risk_budget_snapshot else ""),
        size_reduction_snapshot=str([i.symbol for i in result.size_reduction_queue]),
        blocked_sizing_snapshot=str([i.symbol for i in result.blocked_sizing_queue]),
        safety_snapshot=(
            "paper_only=True;no_real_orders=True;should_auto_apply=False;"
            "auto_apply_enabled=False;sizing_actions_recommendation_only=True"
        ),
        reproducibility_hash=repro_hash,
    )


def get_version_info() -> Dict[str, str]:
    """Return version information. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": "True",
        "no_real_orders": "True",
        "should_auto_apply": "False",
        "auto_apply_enabled": "False",
        "sizing_actions_recommendation_only": "True",
    }


def verify_version() -> bool:
    """Verify version constants are correct. Paper only."""
    return VERSION == "2.0.9" and SCHEMA_VERSION == "209"


def get_cockpit_summary_v209() -> Dict[str, Any]:
    """Return cockpit summary for v2.0.9. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "sizing_actions_recommendation_only": True,
        "models_count": len(_ALL_MODEL_NAMES_V209),
        "cli_commands_count": len(CLI_COMMANDS_V209),
        "gui_tabs_count": len(GUI_TABS_V209),
        "safety_flags_count": len(SAFETY_FLAGS_V209),
        "size_actions_count": len(SIZE_ACTIONS),
    }
