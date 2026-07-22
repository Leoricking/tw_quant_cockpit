"""
paper_trading/small_capital_strategy/paper_cockpit_v208.py
v2.0.8 Paper Portfolio Exposure & Theme Concentration Risk Control
[!] Paper Only. Research Only. Exposure Analysis Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.8"
SCHEMA_VERSION = "208"
RELEASE_NAME = "Paper Portfolio Exposure & Theme Concentration Risk Control"
BASELINE_TESTS = 35005
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

EXPOSURE_TYPES: List[str] = [
    "theme",
    "sector",
    "style",
    "volatility",
    "liquidity",
    "market_regime",
    "candidate_pool",
    "promotion_queue",
    "watchlist",
]

WARNING_LEVELS: List[str] = [
    "none",
    "low",
    "medium",
    "high",
    "critical",
]

EXPOSURE_ACTIONS: List[str] = [
    "allow",
    "monitor",
    "reduce_priority",
    "freeze_new_candidates",
    "require_rescore",
    "block_promotion",
    "human_review_required",
]

CLI_COMMANDS_V208: List[str] = [
    "paper-cockpit-v208-review-exposure",
    "paper-cockpit-v208-evaluate-concentration",
    "paper-cockpit-v208-build-warning-queue",
    "paper-cockpit-v208-build-risk-cap-queue",
    "paper-cockpit-v208-adjust-candidate-exposure",
    "paper-cockpit-v208-export-json",
    "paper-cockpit-v208-export-md",
    "paper-cockpit-v208-export-csv",
    "paper-cockpit-v208-health",
    "paper-cockpit-v208-gate",
]

GUI_TABS_V208: List[str] = [
    "portfolio_exposure_v208",
    "theme_concentration_v208",
    "exposure_warning_queue_v208",
]

EXPOSURE_REVIEW_FIELDS: List[str] = [
    "exposure_review_id",
    "exposure_version",
    "review_period",
    "portfolio_exposure_snapshot",
    "theme_concentration_snapshot",
    "sector_concentration_snapshot",
    "style_concentration_snapshot",
    "volatility_exposure_snapshot",
    "market_regime_exposure_snapshot",
    "candidate_pool_exposure_snapshot",
    "promotion_queue_exposure_snapshot",
    "exposure_warning_queue",
    "risk_cap_recommendation_queue",
    "paper_only_safety_snapshot",
]

EXPOSURE_ITEM_FIELDS: List[str] = [
    "exposure_id",
    "exposure_type",
    "exposure_group",
    "exposure_name",
    "exposure_weight",
    "exposure_score",
    "concentration_score",
    "risk_score",
    "over_limit",
    "warning_level",
    "affected_symbols",
    "affected_candidate_count",
    "affected_watchlist_count",
    "affected_promotion_count",
    "cap_limit",
    "current_usage",
    "remaining_capacity",
    "exposure_action",
]

RISK_CAP_POLICY_FIELDS: List[str] = [
    "policy_id",
    "max_single_theme_weight",
    "max_single_sector_weight",
    "max_single_style_weight",
    "max_high_volatility_weight",
    "max_low_liquidity_weight",
    "max_risk_off_exposure",
    "max_overheating_theme_exposure",
    "max_promotion_queue_single_theme_weight",
    "require_human_review_above_warning_level",
    "auto_apply_enabled",
]

CANDIDATE_EXPOSURE_ADJUSTMENT_FIELDS: List[str] = [
    "symbol",
    "name",
    "candidate_id",
    "theme_id",
    "sector_id",
    "original_priority_score",
    "theme_concentration_penalty",
    "sector_concentration_penalty",
    "style_concentration_penalty",
    "market_regime_penalty",
    "liquidity_penalty",
    "volatility_penalty",
    "final_exposure_adjusted_score",
    "blocked_by_exposure_cap",
    "exposure_reason_codes",
    "requires_human_review",
    "should_auto_apply",
]

EXPOSURE_SUMMARY_FIELDS: List[str] = [
    "total_exposure_groups",
    "over_limit_group_count",
    "high_warning_count",
    "critical_warning_count",
    "blocked_promotion_count",
    "reduced_priority_count",
    "human_review_count",
    "top_concentrated_themes",
    "top_concentrated_sectors",
    "top_risk_sources",
    "exposure_quality_grade",
    "diversification_grade",
    "risk_cap_quality_grade",
]

EXPOSURE_EXPORT_FORMATS: List[str] = [
    "json",
    "markdown",
    "csv",
    "audit_snapshot",
]

SAFETY_FLAGS_V208: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "exposure_analysis_only": True,
    "concentration_risk_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_rebalance_from_exposure": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "exposure_actions_recommendation_only": True,
}

assert len(SAFETY_FLAGS_V208) == 21, f"Expected 21 SAFETY_FLAGS_V208, got {len(SAFETY_FLAGS_V208)}"
assert len(EXPOSURE_TYPES) == 9
assert len(WARNING_LEVELS) == 5
assert len(EXPOSURE_ACTIONS) == 7
assert len(CLI_COMMANDS_V208) == 10
assert len(GUI_TABS_V208) == 3
assert len(EXPOSURE_REVIEW_FIELDS) == 14
assert len(EXPOSURE_ITEM_FIELDS) == 18
assert len(RISK_CAP_POLICY_FIELDS) == 11
assert len(CANDIDATE_EXPOSURE_ADJUSTMENT_FIELDS) == 17
assert len(EXPOSURE_SUMMARY_FIELDS) == 13
assert len(EXPOSURE_EXPORT_FORMATS) == 4

COVERED_VERSIONS: List[str] = [
    "2.0.7", "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 14 models, schema_version="208"
# ---------------------------------------------------------------------------

@dataclass
class ExposureItem:
    """Exposure item schema for portfolio exposure engine. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    exposure_id: str = ""
    exposure_type: str = "theme"
    exposure_group: str = ""
    exposure_name: str = ""
    exposure_weight: float = 0.0
    exposure_score: float = 0.0
    concentration_score: float = 0.0
    risk_score: float = 0.0
    over_limit: bool = False
    warning_level: str = "none"
    affected_symbols: List[str] = field(default_factory=list)
    affected_candidate_count: int = 0
    affected_watchlist_count: int = 0
    affected_promotion_count: int = 0
    cap_limit: float = 0.40
    current_usage: float = 0.0
    remaining_capacity: float = 1.0
    exposure_action: str = "allow"


@dataclass
class PortfolioRiskCapPolicy:
    """Portfolio risk cap policy schema. v2.0.8. auto_apply_enabled is always False."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    max_single_theme_weight: float = 0.40
    max_single_sector_weight: float = 0.45
    max_single_style_weight: float = 0.50
    max_high_volatility_weight: float = 0.30
    max_low_liquidity_weight: float = 0.20
    max_risk_off_exposure: float = 0.10
    max_overheating_theme_exposure: float = 0.25
    max_promotion_queue_single_theme_weight: float = 0.35
    require_human_review_above_warning_level: str = "high"
    auto_apply_enabled: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class CandidateExposureAdjustment:
    """Candidate exposure adjustment schema. v2.0.8. should_auto_apply is always False."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    candidate_id: str = ""
    theme_id: str = ""
    sector_id: str = ""
    original_priority_score: float = 0.0
    theme_concentration_penalty: float = 0.0
    sector_concentration_penalty: float = 0.0
    style_concentration_penalty: float = 0.0
    market_regime_penalty: float = 0.0
    liquidity_penalty: float = 0.0
    volatility_penalty: float = 0.0
    final_exposure_adjusted_score: float = 0.0
    blocked_by_exposure_cap: bool = False
    exposure_reason_codes: List[str] = field(default_factory=list)
    requires_human_review: bool = True
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ExposureSummary:
    """Portfolio exposure summary. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    total_exposure_groups: int = 0
    over_limit_group_count: int = 0
    high_warning_count: int = 0
    critical_warning_count: int = 0
    blocked_promotion_count: int = 0
    reduced_priority_count: int = 0
    human_review_count: int = 0
    top_concentrated_themes: List[str] = field(default_factory=list)
    top_concentrated_sectors: List[str] = field(default_factory=list)
    top_risk_sources: List[str] = field(default_factory=list)
    exposure_quality_grade: str = "C"
    diversification_grade: str = "C"
    risk_cap_quality_grade: str = "C"


@dataclass
class ExposureReviewInput:
    """Input for a portfolio exposure review run. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    review_period: str = ""
    candidate_pool: List[Dict[str, Any]] = field(default_factory=list)
    watchlist: List[Dict[str, Any]] = field(default_factory=list)
    promotion_queue: List[Dict[str, Any]] = field(default_factory=list)
    risk_cap_policy: Optional[PortfolioRiskCapPolicy] = None
    human_review_required: bool = True


@dataclass
class ExposureReviewResult:
    """Full result of one portfolio exposure review run. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    research_only: bool = True
    exposure_analysis_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    exposure_review_id: str = ""
    exposure_version: str = "2.0.8"
    review_period: str = ""
    portfolio_exposure_snapshot: List[ExposureItem] = field(default_factory=list)
    theme_concentration_snapshot: List[ExposureItem] = field(default_factory=list)
    sector_concentration_snapshot: List[ExposureItem] = field(default_factory=list)
    style_concentration_snapshot: List[ExposureItem] = field(default_factory=list)
    volatility_exposure_snapshot: List[ExposureItem] = field(default_factory=list)
    market_regime_exposure_snapshot: List[ExposureItem] = field(default_factory=list)
    candidate_pool_exposure_snapshot: List[ExposureItem] = field(default_factory=list)
    promotion_queue_exposure_snapshot: List[ExposureItem] = field(default_factory=list)
    exposure_warning_queue: List[ExposureItem] = field(default_factory=list)
    risk_cap_recommendation_queue: List[ExposureItem] = field(default_factory=list)
    candidate_exposure_adjustments: List[CandidateExposureAdjustment] = field(default_factory=list)
    exposure_summary: Optional[ExposureSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False
    should_auto_apply: bool = False  # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class ExposureExportResult:
    """Export result for a portfolio exposure review. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    exposure_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class ExposureAuditSnapshot:
    """Audit snapshot for a portfolio exposure review. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    exposure_review_id: str = ""
    run_metadata: str = ""
    portfolio_exposure_snapshot: str = ""
    theme_concentration_snapshot: str = ""
    warning_queue_snapshot: str = ""
    risk_cap_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class ExposureReport:
    """Markdown report for a portfolio exposure review. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    exposure_review_id: str = ""
    review_period: str = ""
    report_content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class ExposureItemCSV:
    """CSV export of exposure items. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    exposure_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class RiskCapCSV:
    """CSV export of risk cap recommendations. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    exposure_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class CandidateExposureCSV:
    """CSV export of candidate exposure adjustments. v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    no_real_orders: bool = True
    exposure_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V208HealthSummary:
    """Health summary for v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.8"


@dataclass
class V208ReleaseSummary:
    """Release summary for v2.0.8."""
    schema_version: str = "208"
    paper_only: bool = True
    version: str = "2.0.8"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 14
    cli_count: int = 10
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V208: List[str] = [
    "ExposureItem",
    "PortfolioRiskCapPolicy",
    "CandidateExposureAdjustment",
    "ExposureSummary",
    "ExposureReviewInput",
    "ExposureReviewResult",
    "ExposureExportResult",
    "ExposureAuditSnapshot",
    "ExposureReport",
    "ExposureItemCSV",
    "RiskCapCSV",
    "CandidateExposureCSV",
    "V208HealthSummary",
    "V208ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V208) == 14


# ---------------------------------------------------------------------------
# Warning level classification
# ---------------------------------------------------------------------------

def classify_warning_level(
    concentration_score: float,
    cap_limit: float,
    current_usage: float,
) -> str:
    """Classify warning level from concentration and cap usage. Paper only."""
    ratio = current_usage / max(0.001, cap_limit)
    if ratio >= 1.30 or concentration_score >= 90.0:
        return "critical"
    if ratio >= 1.10 or concentration_score >= 75.0:
        return "high"
    if ratio >= 0.90 or concentration_score >= 60.0:
        return "medium"
    if ratio >= 0.70 or concentration_score >= 45.0:
        return "low"
    return "none"


def classify_exposure_action(
    warning_level: str,
    exposure_type: str,
    over_limit: bool,
    policy: Optional[PortfolioRiskCapPolicy] = None,
) -> str:
    """Classify exposure action from warning level. Paper only."""
    review_threshold = "high"
    if policy is not None:
        review_threshold = policy.require_human_review_above_warning_level
    if warning_level == "critical":
        return "human_review_required"
    if warning_level == "high":
        if review_threshold in ("high", "medium", "low"):
            return "human_review_required"
        return "block_promotion"
    if warning_level == "medium":
        if exposure_type in ("theme", "sector"):
            return "reduce_priority"
        return "freeze_new_candidates"
    if warning_level == "low":
        return "monitor"
    return "allow"


def compute_concentration_score(
    group_weight: float,
    total_weight: float,
) -> float:
    """Compute concentration score 0-100 from group/total weight ratio. Paper only."""
    if total_weight <= 0.0:
        return 0.0
    ratio = group_weight / total_weight
    return min(100.0, ratio * 100.0)


def compute_risk_score(
    concentration_score: float,
    warning_level: str,
    exposure_type: str,
) -> float:
    """Compute composite risk score 0-100. Paper only."""
    level_weight: Dict[str, float] = {
        "none": 0.0, "low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0,
    }
    type_weight: Dict[str, float] = {
        "theme": 1.0, "sector": 0.9, "style": 0.7,
        "volatility": 0.8, "liquidity": 0.8, "market_regime": 1.0,
        "candidate_pool": 0.6, "promotion_queue": 0.7, "watchlist": 0.5,
    }
    lw = level_weight.get(warning_level, 0.0)
    tw = type_weight.get(exposure_type, 0.7)
    return min(100.0, concentration_score * lw * tw)


# ---------------------------------------------------------------------------
# Concentration scoring per type
# ---------------------------------------------------------------------------

def score_theme_concentration(
    theme_id: str,
    theme_name: str,
    candidate_count: int,
    total_candidates: int,
    watchlist_count: int,
    total_watchlist: int,
    promotion_count: int,
    total_promotion: int,
    cap_limit: float = 0.40,
) -> ExposureItem:
    """Score theme concentration for a single theme. Paper only."""
    total_weight = max(1, total_candidates)
    current_usage = candidate_count / total_weight
    concentration_score = compute_concentration_score(candidate_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "theme", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "theme")
    eid = hashlib.md5(f"theme-{theme_id}".encode()).hexdigest()[:10]
    return ExposureItem(
        exposure_id=eid,
        exposure_type="theme",
        exposure_group=theme_id,
        exposure_name=theme_name,
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_symbols=[],
        affected_candidate_count=candidate_count,
        affected_watchlist_count=watchlist_count,
        affected_promotion_count=promotion_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_sector_concentration(
    sector_id: str,
    sector_name: str,
    candidate_count: int,
    total_candidates: int,
    cap_limit: float = 0.45,
) -> ExposureItem:
    """Score sector concentration for a single sector. Paper only."""
    current_usage = candidate_count / max(1, total_candidates)
    concentration_score = compute_concentration_score(candidate_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "sector", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "sector")
    eid = hashlib.md5(f"sector-{sector_id}".encode()).hexdigest()[:10]
    return ExposureItem(
        exposure_id=eid,
        exposure_type="sector",
        exposure_group=sector_id,
        exposure_name=sector_name,
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_candidate_count=candidate_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_style_concentration(
    style_id: str,
    style_name: str,
    candidate_count: int,
    total_candidates: int,
    cap_limit: float = 0.50,
) -> ExposureItem:
    """Score style concentration. Paper only."""
    current_usage = candidate_count / max(1, total_candidates)
    concentration_score = compute_concentration_score(candidate_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "style", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "style")
    eid = hashlib.md5(f"style-{style_id}".encode()).hexdigest()[:10]
    return ExposureItem(
        exposure_id=eid,
        exposure_type="style",
        exposure_group=style_id,
        exposure_name=style_name,
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_candidate_count=candidate_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_volatility_exposure(
    high_volatility_count: int,
    total_candidates: int,
    cap_limit: float = 0.30,
) -> ExposureItem:
    """Score high-volatility exposure. Paper only."""
    current_usage = high_volatility_count / max(1, total_candidates)
    concentration_score = compute_concentration_score(high_volatility_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "volatility", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "volatility")
    return ExposureItem(
        exposure_id="volatility-high",
        exposure_type="volatility",
        exposure_group="high_volatility",
        exposure_name="High Volatility Exposure",
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_candidate_count=high_volatility_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_liquidity_exposure(
    low_liquidity_count: int,
    total_candidates: int,
    cap_limit: float = 0.20,
) -> ExposureItem:
    """Score low-liquidity exposure. Paper only."""
    current_usage = low_liquidity_count / max(1, total_candidates)
    concentration_score = compute_concentration_score(low_liquidity_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "liquidity", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "liquidity")
    return ExposureItem(
        exposure_id="liquidity-low",
        exposure_type="liquidity",
        exposure_group="low_liquidity",
        exposure_name="Low Liquidity Exposure",
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_candidate_count=low_liquidity_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_market_regime_exposure(
    risk_off_count: int,
    total_candidates: int,
    overheating_count: int = 0,
    cap_limit: float = 0.10,
) -> ExposureItem:
    """Score market regime (risk-off) exposure. Paper only."""
    current_usage = risk_off_count / max(1, total_candidates)
    concentration_score = compute_concentration_score(risk_off_count + overheating_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "market_regime", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "market_regime")
    return ExposureItem(
        exposure_id="market-regime-risk-off",
        exposure_type="market_regime",
        exposure_group="risk_off_overheating",
        exposure_name="Market Regime Risk-Off / Overheating Exposure",
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_candidate_count=risk_off_count + overheating_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_candidate_pool_exposure(
    dominant_theme_count: int,
    total_candidates: int,
    cap_limit: float = 0.40,
) -> ExposureItem:
    """Score candidate pool concentration (single theme dominance). Paper only."""
    current_usage = dominant_theme_count / max(1, total_candidates)
    concentration_score = compute_concentration_score(dominant_theme_count, total_candidates)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "candidate_pool", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "candidate_pool")
    return ExposureItem(
        exposure_id="candidate-pool-dominant",
        exposure_type="candidate_pool",
        exposure_group="dominant_theme",
        exposure_name="Candidate Pool Dominant Theme Exposure",
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_candidate_count=dominant_theme_count,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


def score_promotion_queue_exposure(
    dominant_theme_in_queue: int,
    total_in_queue: int,
    cap_limit: float = 0.35,
) -> ExposureItem:
    """Score promotion queue single-theme concentration. Paper only."""
    current_usage = dominant_theme_in_queue / max(1, total_in_queue)
    concentration_score = compute_concentration_score(dominant_theme_in_queue, total_in_queue)
    over_limit = current_usage > cap_limit
    warning_level = classify_warning_level(concentration_score, cap_limit, current_usage)
    exposure_action = classify_exposure_action(warning_level, "promotion_queue", over_limit)
    risk_score = compute_risk_score(concentration_score, warning_level, "promotion_queue")
    return ExposureItem(
        exposure_id="promotion-queue-dominant",
        exposure_type="promotion_queue",
        exposure_group="dominant_theme",
        exposure_name="Promotion Queue Dominant Theme Exposure",
        exposure_weight=current_usage,
        exposure_score=concentration_score,
        concentration_score=concentration_score,
        risk_score=risk_score,
        over_limit=over_limit,
        warning_level=warning_level,
        affected_promotion_count=dominant_theme_in_queue,
        cap_limit=cap_limit,
        current_usage=current_usage,
        remaining_capacity=max(0.0, cap_limit - current_usage),
        exposure_action=exposure_action,
    )


# ---------------------------------------------------------------------------
# Candidate exposure adjustment
# ---------------------------------------------------------------------------

def _compute_theme_concentration_penalty(concentration_score: float) -> float:
    """Compute theme concentration penalty for candidate. Paper only."""
    if concentration_score >= 80.0:
        return 15.0
    if concentration_score >= 65.0:
        return 10.0
    if concentration_score >= 50.0:
        return 5.0
    return 0.0


def _compute_sector_concentration_penalty(concentration_score: float) -> float:
    """Compute sector concentration penalty. Paper only."""
    if concentration_score >= 80.0:
        return 12.0
    if concentration_score >= 65.0:
        return 8.0
    if concentration_score >= 50.0:
        return 4.0
    return 0.0


def _compute_style_concentration_penalty(concentration_score: float) -> float:
    """Compute style concentration penalty. Paper only."""
    if concentration_score >= 80.0:
        return 8.0
    if concentration_score >= 65.0:
        return 5.0
    return 0.0


def _compute_market_regime_penalty(market_state: str) -> float:
    """Compute market regime penalty. Paper only."""
    penalty_map: Dict[str, float] = {
        "risk_off": 20.0, "downtrend": 15.0, "high_volatility": 10.0,
        "weak_rebound": 5.0, "range_bound": 0.0,
        "healthy_pullback": 0.0, "strong_uptrend": 0.0,
    }
    return penalty_map.get(market_state, 0.0)


def _compute_liquidity_penalty(is_low_liquidity: bool) -> float:
    """Compute liquidity penalty. Paper only."""
    return 10.0 if is_low_liquidity else 0.0


def _compute_volatility_penalty(is_high_volatility: bool) -> float:
    """Compute volatility penalty. Paper only."""
    return 8.0 if is_high_volatility else 0.0


def adjust_candidate_exposure(
    symbol: str,
    name: str,
    candidate_id: str,
    theme_id: str,
    sector_id: str,
    original_priority_score: float,
    theme_concentration_score: float = 0.0,
    sector_concentration_score: float = 0.0,
    style_concentration_score: float = 0.0,
    market_state: str = "range_bound",
    is_low_liquidity: bool = False,
    is_high_volatility: bool = False,
    blocked_by_exposure_cap: bool = False,
    policy: Optional[PortfolioRiskCapPolicy] = None,
) -> CandidateExposureAdjustment:
    """Adjust candidate priority based on portfolio exposure. Paper only."""
    tp = _compute_theme_concentration_penalty(theme_concentration_score)
    sp = _compute_sector_concentration_penalty(sector_concentration_score)
    stp = _compute_style_concentration_penalty(style_concentration_score)
    mrp = _compute_market_regime_penalty(market_state)
    lp = _compute_liquidity_penalty(is_low_liquidity)
    vp = _compute_volatility_penalty(is_high_volatility)

    total_penalty = tp + sp + stp + mrp + lp + vp
    final_score = max(0.0, min(100.0, original_priority_score - total_penalty))

    reason_codes: List[str] = []
    if tp > 0:
        reason_codes.append(f"theme_concentration_penalty:{tp:.1f}")
    if sp > 0:
        reason_codes.append(f"sector_concentration_penalty:{sp:.1f}")
    if stp > 0:
        reason_codes.append(f"style_concentration_penalty:{stp:.1f}")
    if mrp > 0:
        reason_codes.append(f"market_regime_penalty:{market_state}:{mrp:.1f}")
    if lp > 0:
        reason_codes.append("liquidity_penalty:low_liquidity")
    if vp > 0:
        reason_codes.append("volatility_penalty:high_volatility")
    if blocked_by_exposure_cap:
        reason_codes.append("blocked_by_exposure_cap")

    review_threshold = "high"
    if policy is not None:
        review_threshold = policy.require_human_review_above_warning_level

    requires_review = (
        blocked_by_exposure_cap
        or market_state in ("risk_off",)
        or total_penalty >= 20.0
    )

    return CandidateExposureAdjustment(
        symbol=symbol,
        name=name,
        candidate_id=candidate_id,
        theme_id=theme_id,
        sector_id=sector_id,
        original_priority_score=round(original_priority_score, 2),
        theme_concentration_penalty=round(tp, 2),
        sector_concentration_penalty=round(sp, 2),
        style_concentration_penalty=round(stp, 2),
        market_regime_penalty=round(mrp, 2),
        liquidity_penalty=round(lp, 2),
        volatility_penalty=round(vp, 2),
        final_exposure_adjusted_score=round(final_score, 2),
        blocked_by_exposure_cap=blocked_by_exposure_cap,
        exposure_reason_codes=reason_codes,
        requires_human_review=requires_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Exposure summary
# ---------------------------------------------------------------------------

def _build_exposure_summary(
    all_items: List[ExposureItem],
    candidate_adjustments: List[CandidateExposureAdjustment],
) -> ExposureSummary:
    """Build exposure summary from review output. Paper only."""
    total = len(all_items)
    over_limit = [i for i in all_items if i.over_limit]
    high_warning = [i for i in all_items if i.warning_level == "high"]
    critical_warning = [i for i in all_items if i.warning_level == "critical"]
    blocked = [i for i in all_items if i.exposure_action == "block_promotion"]
    reduced = [i for i in all_items if i.exposure_action == "reduce_priority"]
    human_review = [i for i in all_items if i.exposure_action == "human_review_required"]

    theme_items = sorted(
        [i for i in all_items if i.exposure_type == "theme"],
        key=lambda x: x.concentration_score, reverse=True,
    )
    top_themes = [i.exposure_name for i in theme_items[:3]]

    sector_items = sorted(
        [i for i in all_items if i.exposure_type == "sector"],
        key=lambda x: x.concentration_score, reverse=True,
    )
    top_sectors = [i.exposure_name for i in sector_items[:3]]

    risk_sources = sorted(
        [i for i in all_items if i.warning_level in ("high", "critical")],
        key=lambda x: x.risk_score, reverse=True,
    )
    top_risks = [i.exposure_name for i in risk_sources[:3]]

    over_ratio = len(over_limit) / max(1, total)
    if over_ratio == 0:
        eq_grade = "A"
    elif over_ratio <= 0.10:
        eq_grade = "B"
    elif over_ratio <= 0.25:
        eq_grade = "C"
    else:
        eq_grade = "D"

    div_grade = "A" if total >= 5 and len(over_limit) == 0 else (
        "B" if total >= 3 and len(critical_warning) == 0 else (
            "C" if total >= 2 else "D"
        )
    )

    blocked_adj = [a for a in candidate_adjustments if a.blocked_by_exposure_cap]
    rq_grade = "A" if not blocked_adj and not critical_warning else (
        "B" if not critical_warning else "C"
    )

    return ExposureSummary(
        total_exposure_groups=total,
        over_limit_group_count=len(over_limit),
        high_warning_count=len(high_warning),
        critical_warning_count=len(critical_warning),
        blocked_promotion_count=len(blocked),
        reduced_priority_count=len(reduced),
        human_review_count=len(human_review),
        top_concentrated_themes=top_themes,
        top_concentrated_sectors=top_sectors,
        top_risk_sources=top_risks,
        exposure_quality_grade=eq_grade,
        diversification_grade=div_grade,
        risk_cap_quality_grade=rq_grade,
    )


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

def _make_review_id(review_period: str, item_count: int) -> str:
    raw = f"exposure-review-{review_period}-{item_count}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _default_candidate_pool() -> List[Dict[str, Any]]:
    """Return default demo candidate pool. Paper only."""
    return [
        {"symbol": "2330", "name": "台積電", "candidate_id": "CAND-2330", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "style_id": "STYLE-GROWTH", "priority_score": 80.0, "is_high_volatility": False, "is_low_liquidity": False},
        {"symbol": "2454", "name": "聯發科", "candidate_id": "CAND-2454", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "style_id": "STYLE-GROWTH", "priority_score": 75.0, "is_high_volatility": False, "is_low_liquidity": False},
        {"symbol": "2382", "name": "廣達", "candidate_id": "CAND-2382", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "style_id": "STYLE-GROWTH", "priority_score": 68.0, "is_high_volatility": False, "is_low_liquidity": False},
        {"symbol": "2308", "name": "台達電", "candidate_id": "CAND-2308", "theme_id": "THEME-EV", "sector_id": "SECTOR-ELEC", "style_id": "STYLE-VALUE", "priority_score": 62.0, "is_high_volatility": True, "is_low_liquidity": False},
        {"symbol": "2317", "name": "鴻海", "candidate_id": "CAND-2317", "theme_id": "THEME-EV", "sector_id": "SECTOR-MFGR", "style_id": "STYLE-VALUE", "priority_score": 58.0, "is_high_volatility": False, "is_low_liquidity": False},
        {"symbol": "3711", "name": "日月光", "candidate_id": "CAND-3711", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "style_id": "STYLE-GROWTH", "priority_score": 72.0, "is_high_volatility": False, "is_low_liquidity": False},
        {"symbol": "2303", "name": "聯電", "candidate_id": "CAND-2303", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "style_id": "STYLE-GROWTH", "priority_score": 65.0, "is_high_volatility": False, "is_low_liquidity": True},
        {"symbol": "6669", "name": "緯穎", "candidate_id": "CAND-6669", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "style_id": "STYLE-GROWTH", "priority_score": 70.0, "is_high_volatility": True, "is_low_liquidity": False},
    ]


def _build_theme_concentration(
    candidates: List[Dict[str, Any]],
    policy: PortfolioRiskCapPolicy,
) -> List[ExposureItem]:
    """Build theme concentration exposure items from candidates. Paper only."""
    from collections import Counter
    theme_counts: Counter = Counter(c.get("theme_id", "") for c in candidates)
    total = len(candidates)
    items = []
    theme_names = {
        "THEME-SEMI": "半導體", "THEME-AI": "人工智慧", "THEME-EV": "電動車",
        "THEME-CLOUD": "雲端運算", "THEME-ROBOT": "機器人", "THEME-SOLAR": "太陽能",
        "THEME-BIOTECH": "生技", "THEME-FIN": "金融",
    }
    for theme_id, count in theme_counts.items():
        w_count = sum(1 for c in candidates if c.get("theme_id") == theme_id and "watchlist_id" in c)
        p_count = sum(1 for c in candidates if c.get("theme_id") == theme_id and "promotion_id" in c)
        item = score_theme_concentration(
            theme_id=theme_id,
            theme_name=theme_names.get(theme_id, theme_id),
            candidate_count=count,
            total_candidates=total,
            watchlist_count=w_count,
            total_watchlist=total,
            promotion_count=p_count,
            total_promotion=total,
            cap_limit=policy.max_single_theme_weight,
        )
        items.append(item)
    return sorted(items, key=lambda x: x.concentration_score, reverse=True)


def _build_sector_concentration(
    candidates: List[Dict[str, Any]],
    policy: PortfolioRiskCapPolicy,
) -> List[ExposureItem]:
    """Build sector concentration exposure items. Paper only."""
    from collections import Counter
    sector_counts: Counter = Counter(c.get("sector_id", "") for c in candidates)
    total = len(candidates)
    sector_names = {
        "SECTOR-TECH": "科技業", "SECTOR-ELEC": "電子零組件",
        "SECTOR-MFGR": "製造業", "SECTOR-FIN": "金融業",
        "SECTOR-CHEM": "化工業", "SECTOR-BLDG": "營建業",
    }
    items = []
    for sector_id, count in sector_counts.items():
        item = score_sector_concentration(
            sector_id=sector_id,
            sector_name=sector_names.get(sector_id, sector_id),
            candidate_count=count,
            total_candidates=total,
            cap_limit=policy.max_single_sector_weight,
        )
        items.append(item)
    return sorted(items, key=lambda x: x.concentration_score, reverse=True)


def _build_style_concentration(
    candidates: List[Dict[str, Any]],
    policy: PortfolioRiskCapPolicy,
) -> List[ExposureItem]:
    """Build style concentration exposure items. Paper only."""
    from collections import Counter
    style_counts: Counter = Counter(c.get("style_id", "") for c in candidates)
    total = len(candidates)
    style_names = {
        "STYLE-GROWTH": "成長型", "STYLE-VALUE": "價值型",
        "STYLE-MOMENTUM": "動能型", "STYLE-INCOME": "收益型",
    }
    items = []
    for style_id, count in style_counts.items():
        item = score_style_concentration(
            style_id=style_id,
            style_name=style_names.get(style_id, style_id),
            candidate_count=count,
            total_candidates=total,
            cap_limit=policy.max_single_style_weight,
        )
        items.append(item)
    return sorted(items, key=lambda x: x.concentration_score, reverse=True)


def _build_candidate_exposure_adjustments(
    candidates: List[Dict[str, Any]],
    theme_items: List[ExposureItem],
    sector_items: List[ExposureItem],
    style_items: List[ExposureItem],
    market_state: str,
    policy: PortfolioRiskCapPolicy,
) -> List[CandidateExposureAdjustment]:
    """Build candidate exposure adjustments. Paper only."""
    theme_scores = {i.exposure_group: i.concentration_score for i in theme_items}
    sector_scores = {i.exposure_group: i.concentration_score for i in sector_items}
    style_scores = {i.exposure_group: i.concentration_score for i in style_items}
    over_limit_themes = {i.exposure_group for i in theme_items if i.over_limit}

    adjustments = []
    for c in candidates:
        tid = c.get("theme_id", "")
        sid = c.get("sector_id", "")
        stid = c.get("style_id", "")
        blocked = tid in over_limit_themes
        adj = adjust_candidate_exposure(
            symbol=c.get("symbol", ""),
            name=c.get("name", ""),
            candidate_id=c.get("candidate_id", ""),
            theme_id=tid,
            sector_id=sid,
            original_priority_score=c.get("priority_score", 50.0),
            theme_concentration_score=theme_scores.get(tid, 0.0),
            sector_concentration_score=sector_scores.get(sid, 0.0),
            style_concentration_score=style_scores.get(stid, 0.0),
            market_state=market_state,
            is_low_liquidity=c.get("is_low_liquidity", False),
            is_high_volatility=c.get("is_high_volatility", False),
            blocked_by_exposure_cap=blocked,
            policy=policy,
        )
        adjustments.append(adj)
    return adjustments


def _default_risk_cap_policy() -> PortfolioRiskCapPolicy:
    return PortfolioRiskCapPolicy(
        policy_id="default-policy-v208",
    )


def run_exposure_review(
    review_input: Optional[ExposureReviewInput] = None,
    market_state: str = "range_bound",
) -> ExposureReviewResult:
    """Run a paper portfolio exposure review. Paper only."""
    if review_input is None:
        review_input = ExposureReviewInput(
            review_period="2026-W29",
            candidate_pool=_default_candidate_pool(),
        )

    policy = review_input.risk_cap_policy or _default_risk_cap_policy()
    candidates = review_input.candidate_pool
    total = len(candidates)

    review_id = _make_review_id(review_input.review_period, total)

    theme_items = _build_theme_concentration(candidates, policy)
    sector_items = _build_sector_concentration(candidates, policy)
    style_items = _build_style_concentration(candidates, policy)

    high_vol_count = sum(1 for c in candidates if c.get("is_high_volatility", False))
    low_liq_count = sum(1 for c in candidates if c.get("is_low_liquidity", False))
    risk_off_count = sum(1 for c in candidates if c.get("theme_state", "") == "risk_off")
    overheating_count = sum(1 for c in candidates if c.get("theme_state", "") == "overheating")

    volatility_item = score_volatility_exposure(
        high_vol_count, total, cap_limit=policy.max_high_volatility_weight
    )
    liquidity_item = score_liquidity_exposure(
        low_liq_count, total, cap_limit=policy.max_low_liquidity_weight
    )
    regime_item = score_market_regime_exposure(
        risk_off_count, total, overheating_count, cap_limit=policy.max_risk_off_exposure
    )
    pool_item = score_candidate_pool_exposure(
        max((c for c in [sum(1 for x in candidates if x.get("theme_id") == ti.exposure_group) for ti in theme_items[:1]]), default=0),
        total,
        cap_limit=policy.max_single_theme_weight,
    )

    promotion = review_input.promotion_queue or []
    promo_counts = {}
    for p in promotion:
        tid = p.get("theme_id", "")
        promo_counts[tid] = promo_counts.get(tid, 0) + 1
    dominant_promo = max(promo_counts.values(), default=0)
    promo_item = score_promotion_queue_exposure(
        dominant_promo, max(1, len(promotion)),
        cap_limit=policy.max_promotion_queue_single_theme_weight,
    )

    portfolio_snapshot = theme_items + sector_items + style_items
    all_items = portfolio_snapshot + [volatility_item, liquidity_item, regime_item, pool_item, promo_item]

    warning_queue = [i for i in all_items if i.warning_level in ("medium", "high", "critical")]
    risk_cap_queue = [i for i in all_items if i.over_limit]

    candidate_adjustments = _build_candidate_exposure_adjustments(
        candidates, theme_items, sector_items, style_items, market_state, policy
    )

    summary = _build_exposure_summary(all_items, candidate_adjustments)

    return ExposureReviewResult(
        exposure_review_id=review_id,
        review_period=review_input.review_period,
        portfolio_exposure_snapshot=portfolio_snapshot,
        theme_concentration_snapshot=theme_items,
        sector_concentration_snapshot=sector_items,
        style_concentration_snapshot=style_items,
        volatility_exposure_snapshot=[volatility_item],
        market_regime_exposure_snapshot=[regime_item],
        candidate_pool_exposure_snapshot=[pool_item],
        promotion_queue_exposure_snapshot=[promo_item],
        exposure_warning_queue=warning_queue,
        risk_cap_recommendation_queue=risk_cap_queue,
        candidate_exposure_adjustments=candidate_adjustments,
        exposure_summary=summary,
        all_passed=True,
    )


def evaluate_concentration(
    candidates: Optional[List[Dict[str, Any]]] = None,
    policy: Optional[PortfolioRiskCapPolicy] = None,
) -> List[ExposureItem]:
    """Evaluate concentration across theme/sector/style. Paper only."""
    if candidates is None:
        candidates = _default_candidate_pool()
    if policy is None:
        policy = _default_risk_cap_policy()
    theme_items = _build_theme_concentration(candidates, policy)
    sector_items = _build_sector_concentration(candidates, policy)
    style_items = _build_style_concentration(candidates, policy)
    return theme_items + sector_items + style_items


def build_warning_queue(
    candidates: Optional[List[Dict[str, Any]]] = None,
) -> List[ExposureItem]:
    """Build exposure warning queue. Paper only."""
    result = run_exposure_review(
        ExposureReviewInput(review_period="2026-W29", candidate_pool=candidates or _default_candidate_pool())
    )
    return result.exposure_warning_queue


def build_risk_cap_queue(
    candidates: Optional[List[Dict[str, Any]]] = None,
    policy: Optional[PortfolioRiskCapPolicy] = None,
) -> List[ExposureItem]:
    """Build risk cap recommendation queue. Paper only."""
    result = run_exposure_review(
        ExposureReviewInput(
            review_period="2026-W29",
            candidate_pool=candidates or _default_candidate_pool(),
            risk_cap_policy=policy,
        )
    )
    return result.risk_cap_recommendation_queue


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_exposure_json(result: ExposureReviewResult) -> ExposureExportResult:
    """Export exposure review as JSON. Paper only."""
    rid = result.exposure_review_id
    parts = [
        f'{{"exposure_review_id": "{rid}", "exposure_version": "{result.exposure_version}",',
        f'"review_period": "{result.review_period}", "paper_only": true,',
        f'"should_auto_apply": false, "auto_apply_enabled": false, "no_real_orders": true,',
        f'"portfolio_exposure_count": {len(result.portfolio_exposure_snapshot)},',
        f'"theme_concentration_count": {len(result.theme_concentration_snapshot)},',
        f'"sector_concentration_count": {len(result.sector_concentration_snapshot)},',
        f'"exposure_warning_count": {len(result.exposure_warning_queue)},',
        f'"risk_cap_count": {len(result.risk_cap_recommendation_queue)},',
        f'"candidate_adjustment_count": {len(result.candidate_exposure_adjustments)}}}',
    ]
    return ExposureExportResult(
        exposure_review_id=rid,
        export_format="json",
        content="".join(str(p) for p in parts),
        is_valid=True,
        export_status="complete",
    )


def export_exposure_markdown(result: ExposureReviewResult) -> ExposureExportResult:
    """Export exposure review as Markdown. Paper only."""
    rid = result.exposure_review_id
    summary = result.exposure_summary
    lines = [
        "# Portfolio Exposure Report v2.0.8",
        "",
        f"**exposure_review_id**: {rid}",
        f"**exposure_version**: {result.exposure_version}",
        f"**review_period**: {result.review_period}",
        f"**paper_only**: True",
        f"**should_auto_apply**: False",
        f"**auto_apply_enabled**: False",
        f"**no_real_orders**: True",
        "",
        "## Exposure Summary",
        "",
    ]
    if summary:
        lines += [
            f"- Total Exposure Groups: {summary.total_exposure_groups}",
            f"- Over Limit Groups: {summary.over_limit_group_count}",
            f"- High Warning Count: {summary.high_warning_count}",
            f"- Critical Warning Count: {summary.critical_warning_count}",
            f"- Blocked Promotion Count: {summary.blocked_promotion_count}",
            f"- Human Review Count: {summary.human_review_count}",
            f"- Exposure Quality Grade: {summary.exposure_quality_grade}",
            f"- Diversification Grade: {summary.diversification_grade}",
            f"- Risk Cap Quality Grade: {summary.risk_cap_quality_grade}",
        ]
    lines += [
        "",
        "## Theme Concentration",
        "",
    ]
    for item in result.theme_concentration_snapshot:
        lines.append(
            f"- {item.exposure_name} [{item.exposure_group}]: "
            f"concentration={item.concentration_score:.1f}% "
            f"warning={item.warning_level} action={item.exposure_action}"
        )
    lines += [
        "",
        "## Exposure Warning Queue",
        "",
    ]
    for item in result.exposure_warning_queue:
        lines.append(
            f"- [{item.warning_level.upper()}] {item.exposure_name}: "
            f"usage={item.current_usage:.1%} cap={item.cap_limit:.1%} → {item.exposure_action}"
        )
    lines += ["", "---", "[!] Paper Only | No Real Orders | Not Investment Advice"]
    return ExposureExportResult(
        exposure_review_id=rid,
        export_format="markdown",
        content="\n".join(lines),
        is_valid=True,
        export_status="complete",
    )


def export_exposure_item_csv(result: ExposureReviewResult) -> ExposureItemCSV:
    """Export exposure items as CSV. Paper only."""
    rows = [
        "exposure_id,exposure_type,exposure_name,concentration_score,warning_level,"
        "over_limit,current_usage,cap_limit,exposure_action,should_auto_apply"
    ]
    all_items = (
        result.portfolio_exposure_snapshot
        + result.volatility_exposure_snapshot
        + result.market_regime_exposure_snapshot
        + result.candidate_pool_exposure_snapshot
        + result.promotion_queue_exposure_snapshot
    )
    for item in all_items:
        rows.append(
            f"{item.exposure_id},{item.exposure_type},{item.exposure_name},"
            f"{item.concentration_score:.2f},{item.warning_level},"
            f"{item.over_limit},{item.current_usage:.4f},{item.cap_limit:.4f},"
            f"{item.exposure_action},False"
        )
    return ExposureItemCSV(
        exposure_review_id=result.exposure_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_risk_cap_csv(result: ExposureReviewResult) -> RiskCapCSV:
    """Export risk cap recommendations as CSV. Paper only."""
    rows = [
        "exposure_id,exposure_type,exposure_name,current_usage,cap_limit,"
        "over_limit,warning_level,exposure_action,auto_apply_enabled"
    ]
    for item in result.risk_cap_recommendation_queue:
        rows.append(
            f"{item.exposure_id},{item.exposure_type},{item.exposure_name},"
            f"{item.current_usage:.4f},{item.cap_limit:.4f},"
            f"{item.over_limit},{item.warning_level},{item.exposure_action},False"
        )
    return RiskCapCSV(
        exposure_review_id=result.exposure_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_candidate_exposure_csv(result: ExposureReviewResult) -> CandidateExposureCSV:
    """Export candidate exposure adjustments as CSV. Paper only."""
    rows = [
        "symbol,candidate_id,theme_id,sector_id,original_score,"
        "theme_penalty,sector_penalty,final_score,blocked,should_auto_apply"
    ]
    for adj in result.candidate_exposure_adjustments:
        rows.append(
            f"{adj.symbol},{adj.candidate_id},{adj.theme_id},{adj.sector_id},"
            f"{adj.original_priority_score:.2f},{adj.theme_concentration_penalty:.2f},"
            f"{adj.sector_concentration_penalty:.2f},{adj.final_exposure_adjusted_score:.2f},"
            f"{adj.blocked_by_exposure_cap},False"
        )
    return CandidateExposureCSV(
        exposure_review_id=result.exposure_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_exposure_audit_snapshot(result: ExposureReviewResult) -> ExposureAuditSnapshot:
    """Build portfolio exposure audit snapshot. Paper only."""
    rid = result.exposure_review_id
    raw = f"{rid}-{result.review_period}-{len(result.portfolio_exposure_snapshot)}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return ExposureAuditSnapshot(
        exposure_review_id=rid,
        run_metadata=f"v2.0.8-exposure-review-{rid}",
        portfolio_exposure_snapshot=str([i.exposure_id for i in result.portfolio_exposure_snapshot]),
        theme_concentration_snapshot=str([i.exposure_name for i in result.theme_concentration_snapshot]),
        warning_queue_snapshot=str([i.warning_level for i in result.exposure_warning_queue]),
        risk_cap_snapshot=str([i.exposure_id for i in result.risk_cap_recommendation_queue]),
        safety_snapshot=(
            "paper_only=True;no_real_orders=True;should_auto_apply=False;"
            "auto_apply_enabled=False;exposure_actions_recommendation_only=True"
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
        "exposure_actions_recommendation_only": "True",
    }


def verify_version() -> bool:
    """Verify version constants are correct. Paper only."""
    return VERSION == "2.0.8" and SCHEMA_VERSION == "208"


def get_cockpit_summary_v208() -> Dict[str, Any]:
    """Return cockpit summary for v2.0.8. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "exposure_actions_recommendation_only": True,
        "models_count": len(_ALL_MODEL_NAMES_V208),
        "cli_commands_count": len(CLI_COMMANDS_V208),
        "gui_tabs_count": len(GUI_TABS_V208),
        "safety_flags_count": len(SAFETY_FLAGS_V208),
        "exposure_types_count": len(EXPOSURE_TYPES),
        "warning_levels_count": len(WARNING_LEVELS),
        "exposure_actions_count": len(EXPOSURE_ACTIONS),
    }
