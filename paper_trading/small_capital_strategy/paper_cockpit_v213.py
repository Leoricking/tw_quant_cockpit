"""
paper_trading/small_capital_strategy/paper_cockpit_v213.py
v2.0.13 Paper Market Box Range & Index Regime Control
[!] Paper Only. Research Only. Market Box Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. No Automatic Market Action. Not Investment Advice.
核心句：有現金就不怕震盪，最怕滿倉又融資。
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.13"
SCHEMA_VERSION = "213"
RELEASE_NAME = "Paper Market Box Range & Index Regime Control"
BASELINE_TESTS = 36689
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

# ---------------------------------------------------------------------------
# Box zone boundaries (TWI index points)
# ---------------------------------------------------------------------------
UPPER_ZONE_MIN: int = 45_000
UPPER_ZONE_MAX: int = 47_000
NEUTRAL_ZONE_MIN: int = 42_000
NEUTRAL_ZONE_MAX: int = 45_000
LOWER_ZONE_MIN: int = 40_000
LOWER_ZONE_MAX: int = 42_000
EXTREME_RISK_ZONE_MIN: int = 38_000
EXTREME_RISK_ZONE_MAX: int = 40_000
BELOW_BOX_THRESHOLD: int = 38_000
ABOVE_BOX_THRESHOLD: int = 47_000

ZONE_NAMES: List[str] = [
    "upper_zone",
    "neutral_zone",
    "lower_zone",
    "extreme_risk_zone",
    "below_box",
    "above_box",
]

EXPOSURE_ACTIONS: List[str] = [
    "hold_current_exposure",
    "reduce_exposure_near_upper_box",
    "normal_selective_exposure",
    "core_only_low_zone",
    "defensive_extreme_risk",
    "below_box_defense",
    "overheating_above_box",
    "human_review_required",
]

CLI_COMMANDS_V213: List[str] = [
    "paper-cockpit-v213-review-market-box",
    "paper-cockpit-v213-classify-index-zone",
    "paper-cockpit-v213-build-exposure-control",
    "paper-cockpit-v213-build-chase-risk-queue",
    "paper-cockpit-v213-build-defensive-review-queue",
    "paper-cockpit-v213-export-json",
    "paper-cockpit-v213-export-md",
    "paper-cockpit-v213-export-csv",
    "paper-cockpit-v213-health",
    "paper-cockpit-v213-gate",
]

GUI_TABS_V213: List[str] = [
    "market_box_v213",
    "exposure_control_v213",
    "defensive_review_queue_v213",
]

SAFETY_FLAGS_V213: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "market_box_recommendation_only": True,
    "exposure_recommendation_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_market_action": True,
    "no_automatic_stop_loss_execution": True,
    "no_automatic_take_profit_execution": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "require_box_check_before_entry_always_true": True,
    "market_box_actions_recommendation_only": True,
    "exposure_actions_recommendation_only": True,
}

assert len(SAFETY_FLAGS_V213) == 25, f"Expected 25 SAFETY_FLAGS_V213, got {len(SAFETY_FLAGS_V213)}"
assert len(ZONE_NAMES) == 6
assert len(EXPOSURE_ACTIONS) == 8
assert len(CLI_COMMANDS_V213) == 10
assert len(GUI_TABS_V213) == 3

MARKET_BOX_REVIEW_FIELDS: List[str] = [
    "market_box_review_id",
    "market_box_version",
    "review_period",
    "index_snapshot",
    "box_range_snapshot",
    "zone_classification",
    "exposure_control_snapshot",
    "chase_risk_snapshot",
    "low_zone_core_only_snapshot",
    "defensive_mode_snapshot",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

MARKET_BOX_POLICY_FIELDS: List[str] = [
    "policy_id",
    "upper_zone_min",
    "upper_zone_max",
    "neutral_zone_min",
    "neutral_zone_max",
    "lower_zone_min",
    "lower_zone_max",
    "extreme_risk_zone_min",
    "extreme_risk_zone_max",
    "below_box_threshold",
    "above_box_threshold",
    "upper_zone_max_exposure_pct",
    "neutral_zone_max_exposure_pct",
    "lower_zone_max_exposure_pct",
    "extreme_risk_zone_max_exposure_pct",
    "below_box_max_exposure_pct",
    "require_box_check_before_entry",
    "auto_apply_enabled",
]

INDEX_SNAPSHOT_FIELDS: List[str] = [
    "index_symbol",
    "index_name",
    "current_index_level",
    "previous_close",
    "index_return_pct",
    "volume_ratio",
    "ma5",
    "ma10",
    "ma20",
    "ma60",
    "above_ma5",
    "above_ma10",
    "above_ma20",
    "above_ma60",
    "near_upper_zone",
    "near_lower_zone",
    "zone_name",
    "box_position_pct",
    "box_break_status",
    "requires_human_review",
    "should_auto_apply",
]

EXPOSURE_RECOMMENDATION_FIELDS: List[str] = [
    "current_exposure_pct",
    "recommended_max_exposure_pct",
    "recommended_cash_buffer_pct",
    "exposure_action",
    "chase_high_allowed",
    "add_position_allowed",
    "core_only_allowed",
    "short_term_momentum_allowed",
    "leveraged_etf_allowed",
    "reduce_short_term_exposure",
    "reduce_leveraged_exposure",
    "block_new_add_reason",
    "human_review_reason",
    "should_auto_apply",
]

MARKET_BOX_SUMMARY_FIELDS: List[str] = [
    "current_zone",
    "index_level",
    "box_position_pct",
    "recommended_max_exposure_pct",
    "recommended_cash_buffer_pct",
    "chase_high_block_count",
    "core_only_candidate_count",
    "defensive_candidate_count",
    "human_review_count",
    "leveraged_etf_warning_count",
    "short_term_reduction_count",
    "market_box_quality_grade",
    "exposure_control_quality_grade",
    "risk_temperature_grade",
]

_ALL_MODEL_NAMES_V213: List[str] = [
    "MarketBoxPolicy",
    "IndexSnapshot",
    "ExposureRecommendation",
    "MarketBoxSummary",
    "MarketBoxReviewInput",
    "MarketBoxReviewResult",
    "MarketBoxExportResult",
    "MarketBoxAuditSnapshot",
    "MarketBoxMarkdownReport",
    "ChaseRiskQueueCSV",
    "DefensiveReviewQueueCSV",
    "ExposureRecommendationCSV",
    "V213HealthSummary",
    "V213ReleaseSummary",
    "MarketBoxSafetyGuard",
    "MarketBoxSummaryCSV",
]
assert len(_ALL_MODEL_NAMES_V213) == 16

COVERED_VERSIONS: List[str] = [
    "2.0.12", "2.0.11", "2.0.10", "2.0.9", "2.0.8", "2.0.7",
    "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 16 models, schema_version="213"
# ---------------------------------------------------------------------------

@dataclass
class MarketBoxPolicy:
    """Market box policy schema. v2.0.13.
    auto_apply_enabled is always False.
    require_box_check_before_entry is always True."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    upper_zone_min: int = UPPER_ZONE_MIN
    upper_zone_max: int = UPPER_ZONE_MAX
    neutral_zone_min: int = NEUTRAL_ZONE_MIN
    neutral_zone_max: int = NEUTRAL_ZONE_MAX
    lower_zone_min: int = LOWER_ZONE_MIN
    lower_zone_max: int = LOWER_ZONE_MAX
    extreme_risk_zone_min: int = EXTREME_RISK_ZONE_MIN
    extreme_risk_zone_max: int = EXTREME_RISK_ZONE_MAX
    below_box_threshold: int = BELOW_BOX_THRESHOLD
    above_box_threshold: int = ABOVE_BOX_THRESHOLD
    upper_zone_max_exposure_pct: float = 0.50
    neutral_zone_max_exposure_pct: float = 0.70
    lower_zone_max_exposure_pct: float = 0.40
    extreme_risk_zone_max_exposure_pct: float = 0.20
    below_box_max_exposure_pct: float = 0.10
    require_box_check_before_entry: bool = True   # ALWAYS True
    auto_apply_enabled: bool = False               # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)
        object.__setattr__(self, "require_box_check_before_entry", True)


@dataclass
class IndexSnapshot:
    """Index snapshot schema. v2.0.13. should_auto_apply is always False."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    index_symbol: str = "TWSE"
    index_name: str = "台灣加權指數"
    current_index_level: float = 0.0
    previous_close: float = 0.0
    index_return_pct: float = 0.0
    volume_ratio: float = 1.0
    ma5: float = 0.0
    ma10: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0
    above_ma5: bool = False
    above_ma10: bool = False
    above_ma20: bool = False
    above_ma60: bool = False
    near_upper_zone: bool = False
    near_lower_zone: bool = False
    zone_name: str = "neutral_zone"
    box_position_pct: float = 0.0
    box_break_status: str = "within_box"
    requires_human_review: bool = False
    should_auto_apply: bool = False   # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ExposureRecommendation:
    """Exposure recommendation schema. v2.0.13. should_auto_apply is always False."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    current_exposure_pct: float = 0.0
    recommended_max_exposure_pct: float = 0.70
    recommended_cash_buffer_pct: float = 0.30
    exposure_action: str = "normal_selective_exposure"
    chase_high_allowed: bool = False
    add_position_allowed: bool = True
    core_only_allowed: bool = False
    short_term_momentum_allowed: bool = True
    leveraged_etf_allowed: bool = False
    reduce_short_term_exposure: bool = False
    reduce_leveraged_exposure: bool = True
    block_new_add_reason: str = ""
    human_review_reason: str = ""
    should_auto_apply: bool = False   # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class MarketBoxSummary:
    """Market box summary. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    current_zone: str = "neutral_zone"
    index_level: float = 0.0
    box_position_pct: float = 0.0
    recommended_max_exposure_pct: float = 0.70
    recommended_cash_buffer_pct: float = 0.30
    chase_high_block_count: int = 0
    core_only_candidate_count: int = 0
    defensive_candidate_count: int = 0
    human_review_count: int = 0
    leveraged_etf_warning_count: int = 0
    short_term_reduction_count: int = 0
    market_box_quality_grade: str = "B"
    exposure_control_quality_grade: str = "B"
    risk_temperature_grade: str = "B"


@dataclass
class MarketBoxReviewInput:
    """Input for market box review. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    review_period: str = ""
    index_level: float = 43_000.0
    previous_close: float = 42_800.0
    volume_ratio: float = 1.0
    ma5: float = 42_500.0
    ma10: float = 42_200.0
    ma20: float = 41_800.0
    ma60: float = 40_500.0
    current_exposure_pct: float = 0.60
    policy: Optional[MarketBoxPolicy] = None


@dataclass
class MarketBoxReviewResult:
    """Market box review result. v2.0.13. should_auto_apply is always False."""
    schema_version: str = "213"
    paper_only: bool = True
    research_only: bool = True
    market_box_recommendation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    market_box_review_id: str = ""
    market_box_version: str = "2.0.13"
    review_period: str = ""
    policy: Optional[MarketBoxPolicy] = None
    index_snapshot: Optional[IndexSnapshot] = None
    box_range_snapshot: Dict[str, Any] = field(default_factory=dict)
    zone_classification: str = "neutral_zone"
    exposure_control_snapshot: Optional[ExposureRecommendation] = None
    chase_risk_snapshot: List[str] = field(default_factory=list)
    low_zone_core_only_snapshot: List[str] = field(default_factory=list)
    defensive_mode_snapshot: List[str] = field(default_factory=list)
    human_review_queue: List[str] = field(default_factory=list)
    market_box_summary: Optional[MarketBoxSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = True
    should_auto_apply: bool = False   # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class MarketBoxExportResult:
    """Export result for market box review. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    market_box_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class MarketBoxAuditSnapshot:
    """Audit snapshot for market box review. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    market_box_review_id: str = ""
    run_metadata: str = ""
    index_snapshot: str = ""
    zone_classification: str = ""
    exposure_snapshot: str = ""
    defensive_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class MarketBoxMarkdownReport:
    """Markdown report for market box review. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    market_box_review_id: str = ""
    review_period: str = ""
    content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class ChaseRiskQueueCSV:
    """CSV export of chase-high blocker queue. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    market_box_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class DefensiveReviewQueueCSV:
    """CSV export of defensive review queue. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    market_box_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ExposureRecommendationCSV:
    """CSV export of exposure recommendation. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    market_box_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V213HealthSummary:
    """Health summary for v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.13"


@dataclass
class V213ReleaseSummary:
    """Release summary for v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    version: str = "2.0.13"
    release_name: str = RELEASE_NAME


@dataclass
class MarketBoxSafetyGuard:
    """Safety guard snapshot for market box. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    no_automatic_market_action: bool = True
    no_automatic_stop_loss_execution: bool = True
    no_automatic_take_profit_execution: bool = True
    no_automatic_rebalance: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False
    require_box_check_before_entry: bool = True
    market_box_actions_recommendation_only: bool = True
    exposure_actions_recommendation_only: bool = True


@dataclass
class MarketBoxSummaryCSV:
    """CSV export of market box summary. v2.0.13."""
    schema_version: str = "213"
    paper_only: bool = True
    no_real_orders: bool = True
    market_box_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


# ---------------------------------------------------------------------------
# ID helper
# ---------------------------------------------------------------------------

def _make_market_box_review_id(review_period: str, index_level: float) -> str:
    raw = f"v213-{review_period}-idx{int(index_level)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:10]


# ---------------------------------------------------------------------------
# Zone classification helpers
# ---------------------------------------------------------------------------

def classify_zone(index_level: float, policy: Optional[MarketBoxPolicy] = None) -> str:
    """Classify TWI index into market box zone. Paper only."""
    if policy is None:
        policy = MarketBoxPolicy(policy_id="default-policy-v213")
    if index_level >= policy.above_box_threshold:
        return "above_box"
    if index_level >= policy.upper_zone_min:
        return "upper_zone"
    if index_level >= policy.neutral_zone_min:
        return "neutral_zone"
    if index_level >= policy.lower_zone_min:
        return "lower_zone"
    if index_level >= policy.extreme_risk_zone_min:
        return "extreme_risk_zone"
    return "below_box"


def _calc_box_position_pct(index_level: float, policy: MarketBoxPolicy) -> float:
    """Calculate box position percentage within full box range. Paper only."""
    box_low = float(policy.below_box_threshold)
    box_high = float(policy.above_box_threshold)
    if box_high <= box_low:
        return 0.0
    pct = (index_level - box_low) / (box_high - box_low)
    return round(max(0.0, min(1.0, pct)), 4)


def _calc_index_return_pct(current_level: float, previous_close: float) -> float:
    if previous_close <= 0:
        return 0.0
    return round((current_level - previous_close) / previous_close, 4)


def _classify_box_break_status(index_level: float, policy: MarketBoxPolicy) -> str:
    if index_level > policy.above_box_threshold:
        return "above_box_break"
    if index_level < policy.below_box_threshold:
        return "below_box_break"
    return "within_box"


# ---------------------------------------------------------------------------
# Index snapshot builder
# ---------------------------------------------------------------------------

def build_index_snapshot(
    index_level: float,
    previous_close: float = 0.0,
    volume_ratio: float = 1.0,
    ma5: float = 0.0,
    ma10: float = 0.0,
    ma20: float = 0.0,
    ma60: float = 0.0,
    policy: Optional[MarketBoxPolicy] = None,
) -> IndexSnapshot:
    """Build index snapshot for TWI. Paper only, no real orders."""
    if policy is None:
        policy = MarketBoxPolicy(policy_id="default-policy-v213")

    zone = classify_zone(index_level, policy)
    box_position_pct = _calc_box_position_pct(index_level, policy)
    index_return_pct = _calc_index_return_pct(index_level, previous_close)
    box_break_status = _classify_box_break_status(index_level, policy)

    near_upper_zone = index_level >= policy.upper_zone_min
    near_lower_zone = index_level <= policy.lower_zone_max

    above_ma5 = index_level >= ma5 if ma5 > 0 else False
    above_ma10 = index_level >= ma10 if ma10 > 0 else False
    above_ma20 = index_level >= ma20 if ma20 > 0 else False
    above_ma60 = index_level >= ma60 if ma60 > 0 else False

    requires_human_review = zone in ("below_box", "above_box", "extreme_risk_zone")

    return IndexSnapshot(
        schema_version="213",
        paper_only=True,
        no_real_orders=True,
        index_symbol="TWSE",
        index_name="台灣加權指數",
        current_index_level=round(index_level, 2),
        previous_close=round(previous_close, 2),
        index_return_pct=index_return_pct,
        volume_ratio=round(volume_ratio, 2),
        ma5=round(ma5, 2),
        ma10=round(ma10, 2),
        ma20=round(ma20, 2),
        ma60=round(ma60, 2),
        above_ma5=above_ma5,
        above_ma10=above_ma10,
        above_ma20=above_ma20,
        above_ma60=above_ma60,
        near_upper_zone=near_upper_zone,
        near_lower_zone=near_lower_zone,
        zone_name=zone,
        box_position_pct=box_position_pct,
        box_break_status=box_break_status,
        requires_human_review=requires_human_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Exposure recommendation helpers
# ---------------------------------------------------------------------------

def _classify_exposure_action(zone: str) -> str:
    if zone == "above_box":
        return "overheating_above_box"
    if zone == "upper_zone":
        return "reduce_exposure_near_upper_box"
    if zone == "neutral_zone":
        return "normal_selective_exposure"
    if zone == "lower_zone":
        return "core_only_low_zone"
    if zone == "extreme_risk_zone":
        return "defensive_extreme_risk"
    if zone == "below_box":
        return "below_box_defense"
    return "human_review_required"


def build_exposure_recommendation(
    zone: str,
    current_exposure_pct: float = 0.60,
    policy: Optional[MarketBoxPolicy] = None,
) -> ExposureRecommendation:
    """Build exposure recommendation based on zone. Paper only, no real orders."""
    if policy is None:
        policy = MarketBoxPolicy(policy_id="default-policy-v213")

    exposure_action = _classify_exposure_action(zone)

    # Zone-specific exposure limits
    zone_max_map = {
        "above_box": policy.upper_zone_max_exposure_pct,  # treat as upper limit
        "upper_zone": policy.upper_zone_max_exposure_pct,
        "neutral_zone": policy.neutral_zone_max_exposure_pct,
        "lower_zone": policy.lower_zone_max_exposure_pct,
        "extreme_risk_zone": policy.extreme_risk_zone_max_exposure_pct,
        "below_box": policy.below_box_max_exposure_pct,
    }
    recommended_max = zone_max_map.get(zone, policy.neutral_zone_max_exposure_pct)
    recommended_cash = round(1.0 - recommended_max, 4)

    # Zone-specific rules
    chase_high_allowed = False  # never allowed — universal rule
    add_position_allowed = zone in ("neutral_zone",)
    core_only_allowed = zone in ("lower_zone", "extreme_risk_zone", "below_box")
    short_term_momentum_allowed = zone in ("neutral_zone",)
    leveraged_etf_allowed = False  # always restricted in this system
    reduce_short_term_exposure = zone in ("upper_zone", "above_box")
    reduce_leveraged_exposure = True  # always True

    block_new_add_reason = ""
    human_review_reason = ""

    if zone == "upper_zone":
        block_new_add_reason = "靠近上緣 45,000-47,000：禁止新增高追型進場，分批降碼"
    elif zone == "above_box":
        block_new_add_reason = "已超過箱型上緣 47,000：過熱警示，不得追高"
        human_review_reason = "指數超過箱型上緣，需人工審核"
    elif zone == "extreme_risk_zone":
        block_new_add_reason = "極端風險區 38,000-40,000：只允許 core-only，先防守"
        human_review_reason = "指數進入極端風險區，等待第二次確認"
    elif zone == "below_box":
        block_new_add_reason = "跌破 38,000：防守模式，新增進場全部進 human review"
        human_review_reason = "指數跌破箱型下緣，強制人工審核所有進場"

    return ExposureRecommendation(
        schema_version="213",
        paper_only=True,
        no_real_orders=True,
        current_exposure_pct=round(current_exposure_pct, 4),
        recommended_max_exposure_pct=round(recommended_max, 4),
        recommended_cash_buffer_pct=round(recommended_cash, 4),
        exposure_action=exposure_action,
        chase_high_allowed=chase_high_allowed,
        add_position_allowed=add_position_allowed,
        core_only_allowed=core_only_allowed,
        short_term_momentum_allowed=short_term_momentum_allowed,
        leveraged_etf_allowed=leveraged_etf_allowed,
        reduce_short_term_exposure=reduce_short_term_exposure,
        reduce_leveraged_exposure=reduce_leveraged_exposure,
        block_new_add_reason=block_new_add_reason,
        human_review_reason=human_review_reason,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Queue builders
# ---------------------------------------------------------------------------

def build_chase_risk_queue(
    zone: str,
    candidate_symbols: Optional[List[str]] = None,
) -> List[str]:
    """Build chase-high blocker queue. Paper only."""
    if candidate_symbols is None:
        candidate_symbols = _default_candidate_symbols()
    # In upper_zone or above_box, all candidates are blocked from chase-high
    if zone in ("upper_zone", "above_box"):
        return list(candidate_symbols)
    return []


def build_defensive_review_queue(
    zone: str,
    candidate_symbols: Optional[List[str]] = None,
) -> List[str]:
    """Build defensive review queue. Paper only."""
    if candidate_symbols is None:
        candidate_symbols = _default_candidate_symbols()
    if zone in ("extreme_risk_zone", "below_box"):
        return list(candidate_symbols)
    if zone in ("lower_zone",):
        # Only core stocks allowed in lower zone
        return [s for s in candidate_symbols if s in _default_core_symbols()]
    return []


def build_human_review_queue(zone: str, exposure_rec: ExposureRecommendation) -> List[str]:
    """Build human review queue based on zone and exposure. Paper only."""
    items = []
    if zone in ("below_box", "extreme_risk_zone", "above_box"):
        items.append(f"zone_alert:{zone}")
    if exposure_rec.human_review_reason:
        items.append(f"exposure_alert:{exposure_rec.human_review_reason}")
    return items


# ---------------------------------------------------------------------------
# Default demo data
# ---------------------------------------------------------------------------

def _default_policy() -> MarketBoxPolicy:
    return MarketBoxPolicy(policy_id="default-policy-v213")


def _default_candidate_symbols() -> List[str]:
    return ["2330", "2454", "2382", "2308", "6669", "2317", "3711", "2303"]


def _default_core_symbols() -> List[str]:
    return ["2330", "2454", "0050", "0056"]


def _default_review_input() -> MarketBoxReviewInput:
    return MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=43_500.0,
        previous_close=43_200.0,
        volume_ratio=1.05,
        ma5=43_000.0,
        ma10=42_500.0,
        ma20=42_000.0,
        ma60=40_800.0,
        current_exposure_pct=0.62,
        policy=_default_policy(),
    )


# ---------------------------------------------------------------------------
# Summary builder
# ---------------------------------------------------------------------------

def _build_market_box_summary(
    zone: str,
    index_level: float,
    box_position_pct: float,
    exposure_rec: ExposureRecommendation,
    chase_risk_queue: List[str],
    core_only_candidates: List[str],
    defensive_queue: List[str],
    human_review_queue: List[str],
) -> MarketBoxSummary:
    lev_warn_count = 1 if zone in ("upper_zone", "above_box", "extreme_risk_zone", "below_box") else 0
    short_reduce = len(chase_risk_queue) if exposure_rec.reduce_short_term_exposure else 0

    market_grade = "A" if zone == "neutral_zone" else ("B" if zone in ("lower_zone",) else "C")
    exposure_grade = "A" if len(human_review_queue) == 0 else ("B" if len(human_review_queue) <= 2 else "C")
    risk_grade = "A" if zone in ("neutral_zone", "upper_zone") else ("B" if zone in ("lower_zone",) else "C")

    return MarketBoxSummary(
        schema_version="213",
        paper_only=True,
        no_real_orders=True,
        current_zone=zone,
        index_level=round(index_level, 2),
        box_position_pct=round(box_position_pct, 4),
        recommended_max_exposure_pct=exposure_rec.recommended_max_exposure_pct,
        recommended_cash_buffer_pct=exposure_rec.recommended_cash_buffer_pct,
        chase_high_block_count=len(chase_risk_queue),
        core_only_candidate_count=len(core_only_candidates),
        defensive_candidate_count=len(defensive_queue),
        human_review_count=len(human_review_queue),
        leveraged_etf_warning_count=lev_warn_count,
        short_term_reduction_count=short_reduce,
        market_box_quality_grade=market_grade,
        exposure_control_quality_grade=exposure_grade,
        risk_temperature_grade=risk_grade,
    )


# ---------------------------------------------------------------------------
# Main review engine
# ---------------------------------------------------------------------------

def run_market_box_review(
    review_input: Optional[MarketBoxReviewInput] = None,
) -> MarketBoxReviewResult:
    """Run a paper market box review. Paper only, no real orders."""
    if review_input is None:
        review_input = _default_review_input()

    policy = review_input.policy or _default_policy()
    review_id = _make_market_box_review_id(review_input.review_period, review_input.index_level)

    index_snap = build_index_snapshot(
        index_level=review_input.index_level,
        previous_close=review_input.previous_close,
        volume_ratio=review_input.volume_ratio,
        ma5=review_input.ma5,
        ma10=review_input.ma10,
        ma20=review_input.ma20,
        ma60=review_input.ma60,
        policy=policy,
    )

    zone = index_snap.zone_name

    exposure_rec = build_exposure_recommendation(
        zone=zone,
        current_exposure_pct=review_input.current_exposure_pct,
        policy=policy,
    )

    candidates = _default_candidate_symbols()
    chase_queue = build_chase_risk_queue(zone, candidates)
    core_only_candidates = _default_core_symbols() if zone in ("lower_zone", "extreme_risk_zone", "below_box") else []
    defensive_queue = build_defensive_review_queue(zone, candidates)
    human_queue = build_human_review_queue(zone, exposure_rec)

    box_range_snapshot = {
        "above_box_threshold": policy.above_box_threshold,
        "upper_zone_min": policy.upper_zone_min,
        "upper_zone_max": policy.upper_zone_max,
        "neutral_zone_min": policy.neutral_zone_min,
        "neutral_zone_max": policy.neutral_zone_max,
        "lower_zone_min": policy.lower_zone_min,
        "lower_zone_max": policy.lower_zone_max,
        "extreme_risk_zone_min": policy.extreme_risk_zone_min,
        "extreme_risk_zone_max": policy.extreme_risk_zone_max,
        "below_box_threshold": policy.below_box_threshold,
    }

    summary = _build_market_box_summary(
        zone=zone,
        index_level=review_input.index_level,
        box_position_pct=index_snap.box_position_pct,
        exposure_rec=exposure_rec,
        chase_risk_queue=chase_queue,
        core_only_candidates=core_only_candidates,
        defensive_queue=defensive_queue,
        human_review_queue=human_queue,
    )

    return MarketBoxReviewResult(
        market_box_review_id=review_id,
        market_box_version="2.0.13",
        review_period=review_input.review_period,
        policy=policy,
        index_snapshot=index_snap,
        box_range_snapshot=box_range_snapshot,
        zone_classification=zone,
        exposure_control_snapshot=exposure_rec,
        chase_risk_snapshot=chase_queue,
        low_zone_core_only_snapshot=core_only_candidates,
        defensive_mode_snapshot=defensive_queue,
        human_review_queue=human_queue,
        market_box_summary=summary,
        paper_only_safety_snapshot=True,
        all_passed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


def classify_index_zone(
    index_level: float,
    policy: Optional[MarketBoxPolicy] = None,
) -> Dict[str, Any]:
    """Classify index level into zone. Paper only."""
    if policy is None:
        policy = _default_policy()
    zone = classify_zone(index_level, policy)
    box_position_pct = _calc_box_position_pct(index_level, policy)
    return {
        "index_level": index_level,
        "zone_name": zone,
        "box_position_pct": box_position_pct,
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "schema_version": "213",
    }


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_market_box_json(result: MarketBoxReviewResult) -> MarketBoxExportResult:
    """Export market box review as JSON. Paper only."""
    import json as _json
    payload = {
        "version": "2.0.13",
        "schema_version": "213",
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "market_box_review_id": result.market_box_review_id,
        "market_box_version": result.market_box_version,
        "review_period": result.review_period,
        "zone_classification": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "recommended_max_exposure_pct": result.exposure_control_snapshot.recommended_max_exposure_pct if result.exposure_control_snapshot else 0.0,
        "recommended_cash_buffer_pct": result.exposure_control_snapshot.recommended_cash_buffer_pct if result.exposure_control_snapshot else 0.0,
        "chase_high_block_count": len(result.chase_risk_snapshot),
        "defensive_count": len(result.defensive_mode_snapshot),
        "human_review_count": len(result.human_review_queue),
        "chase_high_allowed": False,
        "require_box_check_before_entry": True,
    }
    content = _json.dumps(payload, ensure_ascii=False, indent=2)
    return MarketBoxExportResult(
        market_box_review_id=result.market_box_review_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


def export_market_box_markdown(result: MarketBoxReviewResult) -> MarketBoxExportResult:
    """Export market box review as Markdown. Paper only."""
    exp_rec = result.exposure_control_snapshot
    lines = [
        "# Paper Market Box Review v2.0.13",
        "",
        f"**Period:** {result.review_period}",
        f"**Market Box Review ID:** {result.market_box_review_id}",
        f"**Paper Only:** True",
        f"**No Real Orders:** True",
        f"**Should Auto Apply:** False",
        f"**核心句：有現金就不怕震盪，最怕滿倉又融資。**",
        "",
        f"## Zone Classification: {result.zone_classification}",
        f"## Exposure Action: {exp_rec.exposure_action if exp_rec else 'N/A'}",
        f"## Recommended Max Exposure: {exp_rec.recommended_max_exposure_pct:.0%}" if exp_rec else "## Recommended Max Exposure: N/A",
        f"## Cash Buffer: {exp_rec.recommended_cash_buffer_pct:.0%}" if exp_rec else "## Cash Buffer: N/A",
        f"## Chase-High Blocked: {len(result.chase_risk_snapshot)}",
        f"## Defensive Queue: {len(result.defensive_mode_snapshot)}",
        f"## Human Review: {len(result.human_review_queue)}",
        "",
        "*[!] Paper Only. Not Investment Advice. Market Box Actions Are Recommendation Only.*",
    ]
    content = "\n".join(lines)
    return MarketBoxExportResult(
        market_box_review_id=result.market_box_review_id,
        export_format="markdown",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


def export_market_box_csv(result: MarketBoxReviewResult) -> MarketBoxSummaryCSV:
    """Export market box summary as CSV. Paper only."""
    header = "zone_classification,index_level,box_position_pct,recommended_max_exposure_pct,recommended_cash_buffer_pct,chase_high_block_count,defensive_count,human_review_count,should_auto_apply"
    snap = result.index_snapshot
    exp_rec = result.exposure_control_snapshot
    rows = [header]
    rows.append(
        f"{result.zone_classification},"
        f"{snap.current_index_level if snap else 0.0},"
        f"{snap.box_position_pct if snap else 0.0},"
        f"{exp_rec.recommended_max_exposure_pct if exp_rec else 0.0},"
        f"{exp_rec.recommended_cash_buffer_pct if exp_rec else 0.0},"
        f"{len(result.chase_risk_snapshot)},"
        f"{len(result.defensive_mode_snapshot)},"
        f"{len(result.human_review_queue)},"
        f"False"
    )
    csv_content = "\n".join(rows)
    return MarketBoxSummaryCSV(
        market_box_review_id=result.market_box_review_id,
        csv_content=csv_content,
        row_count=1,
        is_valid=True,
    )


def export_chase_risk_queue_csv(result: MarketBoxReviewResult) -> ChaseRiskQueueCSV:
    """Export chase-high blocker queue as CSV. Paper only."""
    header = "symbol,zone_classification,chase_high_allowed,should_auto_apply"
    rows = [header]
    for sym in result.chase_risk_snapshot:
        rows.append(f"{sym},{result.zone_classification},False,False")
    csv_content = "\n".join(rows)
    return ChaseRiskQueueCSV(
        market_box_review_id=result.market_box_review_id,
        csv_content=csv_content,
        row_count=len(result.chase_risk_snapshot),
        is_valid=True,
    )


def export_defensive_review_queue_csv(result: MarketBoxReviewResult) -> DefensiveReviewQueueCSV:
    """Export defensive review queue as CSV. Paper only."""
    header = "symbol,zone_classification,core_only_allowed,should_auto_apply"
    rows = [header]
    for sym in result.defensive_mode_snapshot:
        rows.append(f"{sym},{result.zone_classification},True,False")
    csv_content = "\n".join(rows)
    return DefensiveReviewQueueCSV(
        market_box_review_id=result.market_box_review_id,
        csv_content=csv_content,
        row_count=len(result.defensive_mode_snapshot),
        is_valid=True,
    )


def export_exposure_recommendation_csv(result: MarketBoxReviewResult) -> ExposureRecommendationCSV:
    """Export exposure recommendation as CSV. Paper only."""
    exp_rec = result.exposure_control_snapshot
    header = "zone,exposure_action,current_exposure_pct,recommended_max_exposure_pct,recommended_cash_buffer_pct,chase_high_allowed,add_position_allowed,core_only_allowed,should_auto_apply"
    rows = [header]
    if exp_rec:
        rows.append(
            f"{result.zone_classification},{exp_rec.exposure_action},"
            f"{exp_rec.current_exposure_pct:.4f},{exp_rec.recommended_max_exposure_pct:.4f},"
            f"{exp_rec.recommended_cash_buffer_pct:.4f},{exp_rec.chase_high_allowed},"
            f"{exp_rec.add_position_allowed},{exp_rec.core_only_allowed},False"
        )
    csv_content = "\n".join(rows)
    return ExposureRecommendationCSV(
        market_box_review_id=result.market_box_review_id,
        csv_content=csv_content,
        row_count=max(0, len(rows) - 1),
        is_valid=True,
    )


def export_market_box_audit_snapshot(result: MarketBoxReviewResult) -> MarketBoxAuditSnapshot:
    """Export market box audit snapshot. Paper only."""
    hash_val = hashlib.sha256(
        f"{result.market_box_review_id}-{result.review_period}-{result.zone_classification}".encode()
    ).hexdigest()[:16]
    snap = result.index_snapshot
    exp_rec = result.exposure_control_snapshot
    return MarketBoxAuditSnapshot(
        market_box_review_id=result.market_box_review_id,
        run_metadata="v213-paper-only-market-box-audit",
        index_snapshot=f"index_level={snap.current_index_level if snap else 0},zone={result.zone_classification}",
        zone_classification=result.zone_classification,
        exposure_snapshot=f"exposure_action={exp_rec.exposure_action if exp_rec else ''},max={exp_rec.recommended_max_exposure_pct if exp_rec else 0}",
        defensive_snapshot=f"defensive_count={len(result.defensive_mode_snapshot)}",
        safety_snapshot="paper_only=True,no_real_orders=True,should_auto_apply=False,auto_apply_enabled=False,require_box_check_before_entry=True",
        reproducibility_hash=hash_val,
        export_status="complete",
    )


# ---------------------------------------------------------------------------
# Version / summary
# ---------------------------------------------------------------------------

def verify_version() -> bool:
    """Verify v2.0.13 version constants are correct."""
    return VERSION == "2.0.13" and SCHEMA_VERSION == "213"


def get_cockpit_summary_v213() -> Dict[str, Any]:
    """Return v2.0.13 cockpit summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "require_box_check_before_entry": True,
        "market_box_actions_recommendation_only": True,
        "exposure_actions_recommendation_only": True,
        "chase_high_always_blocked": True,
        "zone_name_count": len(ZONE_NAMES),
        "exposure_action_count": len(EXPOSURE_ACTIONS),
        "cli_command_count": len(CLI_COMMANDS_V213),
        "gui_tab_count": len(GUI_TABS_V213),
        "safety_flag_count": len(SAFETY_FLAGS_V213),
        "model_count": len(_ALL_MODEL_NAMES_V213),
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }
