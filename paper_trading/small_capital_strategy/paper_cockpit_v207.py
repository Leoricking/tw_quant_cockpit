"""
paper_trading/small_capital_strategy/paper_cockpit_v207.py
v2.0.7 Paper Theme Rotation & Market Regime Control
[!] Paper Only. Research Only. Theme Rotation Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.7"
SCHEMA_VERSION = "207"
RELEASE_NAME = "Paper Theme Rotation & Market Regime Control"
BASELINE_TESTS = 34632
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

THEME_STATES: List[str] = [
    "emerging",
    "strengthening",
    "leading",
    "crowded",
    "overheating",
    "weakening",
    "cooling",
    "stale",
    "risk_off",
    "neutral",
]

MARKET_STATES: List[str] = [
    "strong_uptrend",
    "healthy_pullback",
    "range_bound",
    "weak_rebound",
    "downtrend",
    "high_volatility",
    "risk_off",
]

ALLOWED_RISK_MODES: List[str] = [
    "aggressive_paper",
    "normal_paper",
    "defensive_paper",
    "observation_only",
    "freeze_promotion",
]

THEME_ACTIONS: List[str] = [
    "increase_attention",
    "keep_priority",
    "reduce_priority",
    "freeze_new_candidates",
    "require_rescore",
    "downgrade_theme",
    "human_review_required",
]

PRIORITY_CHANGES: List[str] = [
    "promote_priority",
    "keep_priority",
    "reduce_priority",
    "freeze_candidate",
    "require_rescore",
    "human_review_required",
]

CLI_COMMANDS_V207: List[str] = [
    "paper-cockpit-v207-review-theme-rotation",
    "paper-cockpit-v207-evaluate-market-regime",
    "paper-cockpit-v207-rank-themes",
    "paper-cockpit-v207-detect-overheating",
    "paper-cockpit-v207-detect-weakening",
    "paper-cockpit-v207-adjust-candidate-priority",
    "paper-cockpit-v207-export-json",
    "paper-cockpit-v207-export-md",
    "paper-cockpit-v207-export-csv",
    "paper-cockpit-v207-health",
    "paper-cockpit-v207-gate",
]

GUI_TABS_V207: List[str] = [
    "theme_rotation_v207",
    "market_regime_v207",
    "candidate_priority_adjustment_v207",
]

THEME_ROTATION_REVIEW_FIELDS: List[str] = [
    "theme_rotation_review_id",
    "theme_rotation_version",
    "review_period",
    "market_regime_snapshot",
    "theme_strength_snapshot",
    "theme_momentum_snapshot",
    "theme_breadth_snapshot",
    "theme_overheat_snapshot",
    "theme_weakening_snapshot",
    "theme_rotation_action_queue",
    "candidate_priority_adjustment_snapshot",
    "paper_only_safety_snapshot",
]

THEME_STRENGTH_ITEM_FIELDS: List[str] = [
    "theme_id",
    "theme_name",
    "theme_group",
    "theme_rank",
    "previous_theme_rank",
    "theme_score",
    "momentum_score",
    "breadth_score",
    "leadership_score",
    "earnings_support_score",
    "volume_confirmation_score",
    "institutional_support_score",
    "overheating_score",
    "weakening_score",
    "concentration_risk_score",
    "candidate_count",
    "promoted_candidate_count",
    "stale_candidate_count",
    "expired_candidate_count",
    "active_candidate_count",
    "theme_state",
    "theme_action",
]

MARKET_REGIME_FIELDS: List[str] = [
    "regime_id",
    "regime_name",
    "index_trend_score",
    "breadth_score",
    "volume_score",
    "volatility_score",
    "risk_appetite_score",
    "institutional_flow_score",
    "margin_risk_score",
    "market_state",
    "allowed_risk_mode",
    "candidate_promotion_allowed",
    "aggressive_entry_allowed",
    "second_wave_entry_allowed",
    "abc_pullback_entry_allowed",
    "breakout_entry_allowed",
    "should_auto_apply",
]

CANDIDATE_PRIORITY_ADJUSTMENT_FIELDS: List[str] = [
    "symbol",
    "name",
    "candidate_id",
    "theme_id",
    "original_candidate_score",
    "theme_adjusted_score",
    "market_regime_adjusted_score",
    "lifecycle_adjusted_score",
    "final_priority_score",
    "priority_change",
    "priority_reason_codes",
    "blocked_by_market_regime",
    "blocked_by_theme_state",
    "requires_human_review",
    "should_auto_apply",
]

THEME_ROTATION_SUMMARY_FIELDS: List[str] = [
    "total_theme_count",
    "leading_theme_count",
    "strengthening_theme_count",
    "overheating_theme_count",
    "weakening_theme_count",
    "stale_theme_count",
    "risk_off_theme_count",
    "top_leading_themes",
    "top_strengthening_themes",
    "top_overheating_themes",
    "top_weakening_themes",
    "candidate_count_by_theme",
    "promotion_allowed_count",
    "promotion_blocked_count",
    "theme_rotation_quality_grade",
    "market_regime_quality_grade",
]

THEME_ROTATION_EXPORT_FORMATS: List[str] = [
    "json",
    "markdown",
    "csv",
    "audit_snapshot",
]

SAFETY_FLAGS_V207: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "theme_rotation_only": True,
    "market_regime_only": True,
    "candidate_priority_adjustment_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "should_auto_apply_theme_rotation_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
}

assert len(SAFETY_FLAGS_V207) == 20, f"Expected 20 SAFETY_FLAGS_V207, got {len(SAFETY_FLAGS_V207)}"
assert len(THEME_STATES) == 10
assert len(MARKET_STATES) == 7
assert len(ALLOWED_RISK_MODES) == 5
assert len(THEME_ACTIONS) == 7
assert len(PRIORITY_CHANGES) == 6
assert len(CLI_COMMANDS_V207) == 11
assert len(GUI_TABS_V207) == 3
assert len(THEME_ROTATION_REVIEW_FIELDS) == 12
assert len(THEME_STRENGTH_ITEM_FIELDS) == 22
assert len(MARKET_REGIME_FIELDS) == 17
assert len(CANDIDATE_PRIORITY_ADJUSTMENT_FIELDS) == 15
assert len(THEME_ROTATION_SUMMARY_FIELDS) == 16
assert len(THEME_ROTATION_EXPORT_FORMATS) == 4

COVERED_VERSIONS: List[str] = [
    "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 13 models, schema_version="207"
# ---------------------------------------------------------------------------

@dataclass
class ThemeStrengthItem:
    """Theme strength item schema. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    theme_id: str = ""
    theme_name: str = ""
    theme_group: str = ""
    theme_rank: int = 0
    previous_theme_rank: int = 0
    theme_score: float = 0.0
    momentum_score: float = 0.0
    breadth_score: float = 0.0
    leadership_score: float = 0.0
    earnings_support_score: float = 0.0
    volume_confirmation_score: float = 0.0
    institutional_support_score: float = 0.0
    overheating_score: float = 0.0
    weakening_score: float = 0.0
    concentration_risk_score: float = 0.0
    candidate_count: int = 0
    promoted_candidate_count: int = 0
    stale_candidate_count: int = 0
    expired_candidate_count: int = 0
    active_candidate_count: int = 0
    theme_state: str = "neutral"
    theme_action: str = "keep_priority"


@dataclass
class MarketRegime:
    """Market regime schema. v2.0.7. should_auto_apply is always False."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    regime_id: str = ""
    regime_name: str = ""
    index_trend_score: float = 50.0
    breadth_score: float = 50.0
    volume_score: float = 50.0
    volatility_score: float = 50.0
    risk_appetite_score: float = 50.0
    institutional_flow_score: float = 50.0
    margin_risk_score: float = 50.0
    market_state: str = "range_bound"
    allowed_risk_mode: str = "normal_paper"
    candidate_promotion_allowed: bool = True
    aggressive_entry_allowed: bool = False
    second_wave_entry_allowed: bool = True
    abc_pullback_entry_allowed: bool = True
    breakout_entry_allowed: bool = False
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class CandidatePriorityAdjustment:
    """Candidate priority adjustment schema. v2.0.7. should_auto_apply is always False."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    candidate_id: str = ""
    theme_id: str = ""
    original_candidate_score: float = 0.0
    theme_adjusted_score: float = 0.0
    market_regime_adjusted_score: float = 0.0
    lifecycle_adjusted_score: float = 0.0
    final_priority_score: float = 0.0
    priority_change: str = "keep_priority"
    priority_reason_codes: List[str] = field(default_factory=list)
    blocked_by_market_regime: bool = False
    blocked_by_theme_state: bool = False
    requires_human_review: bool = True
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ThemeRotationSummary:
    """Theme rotation summary for a rotation review. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    total_theme_count: int = 0
    leading_theme_count: int = 0
    strengthening_theme_count: int = 0
    overheating_theme_count: int = 0
    weakening_theme_count: int = 0
    stale_theme_count: int = 0
    risk_off_theme_count: int = 0
    top_leading_themes: List[str] = field(default_factory=list)
    top_strengthening_themes: List[str] = field(default_factory=list)
    top_overheating_themes: List[str] = field(default_factory=list)
    top_weakening_themes: List[str] = field(default_factory=list)
    candidate_count_by_theme: Dict[str, int] = field(default_factory=dict)
    promotion_allowed_count: int = 0
    promotion_blocked_count: int = 0
    theme_rotation_quality_grade: str = "C"
    market_regime_quality_grade: str = "C"


@dataclass
class ThemeRotationReviewInput:
    """Input for a theme rotation review run. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    review_period: str = ""
    theme_items: List[ThemeStrengthItem] = field(default_factory=list)
    market_regime: Optional[MarketRegime] = None
    lifecycle_review_ids: List[str] = field(default_factory=list)
    watchlist_rotation_ids: List[str] = field(default_factory=list)
    human_review_required: bool = True


@dataclass
class ThemeRotationReviewResult:
    """Full result of one theme rotation review run. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    research_only: bool = True
    theme_rotation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    theme_rotation_review_id: str = ""
    theme_rotation_version: str = "2.0.7"
    review_period: str = ""
    market_regime_snapshot: List[str] = field(default_factory=list)
    theme_strength_snapshot: List[str] = field(default_factory=list)
    theme_momentum_snapshot: List[str] = field(default_factory=list)
    theme_breadth_snapshot: List[str] = field(default_factory=list)
    theme_overheat_snapshot: List[str] = field(default_factory=list)
    theme_weakening_snapshot: List[str] = field(default_factory=list)
    theme_rotation_action_queue: List[ThemeStrengthItem] = field(default_factory=list)
    candidate_priority_adjustment_snapshot: List[CandidatePriorityAdjustment] = field(default_factory=list)
    theme_rotation_summary: Optional[ThemeRotationSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ThemeRotationExportResult:
    """Export result for a theme rotation review. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    theme_rotation_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True


@dataclass
class ThemeRotationAuditSnapshot:
    """Audit snapshot for a theme rotation review. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    theme_rotation_review_id: str = ""
    run_metadata: str = ""
    market_regime_snapshot: str = ""
    theme_strength_snapshot: str = ""
    overheat_snapshot: str = ""
    weakening_snapshot: str = ""
    priority_adjustment_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class ThemeRotationReport:
    """Markdown report for a theme rotation review. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    theme_rotation_review_id: str = ""
    review_period: str = ""
    report_content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class ThemeStrengthCSV:
    """CSV export of theme strength snapshot. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    theme_rotation_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class MarketRegimeCSV:
    """CSV export of market regime snapshot. v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    no_real_orders: bool = True
    theme_rotation_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V207HealthSummary:
    """Health summary for v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.7"


@dataclass
class V207ReleaseSummary:
    """Release summary for v2.0.7."""
    schema_version: str = "207"
    paper_only: bool = True
    version: str = "2.0.7"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 13
    cli_count: int = 11
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V207: List[str] = [
    "ThemeStrengthItem",
    "MarketRegime",
    "CandidatePriorityAdjustment",
    "ThemeRotationSummary",
    "ThemeRotationReviewInput",
    "ThemeRotationReviewResult",
    "ThemeRotationExportResult",
    "ThemeRotationAuditSnapshot",
    "ThemeRotationReport",
    "ThemeStrengthCSV",
    "MarketRegimeCSV",
    "V207HealthSummary",
    "V207ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V207) == 13


# ---------------------------------------------------------------------------
# Theme state classification
# ---------------------------------------------------------------------------

def classify_theme_state(
    theme_score: float,
    momentum_score: float,
    overheating_score: float,
    weakening_score: float,
    breadth_score: float,
) -> str:
    """Classify theme state from scores. Paper only."""
    if overheating_score >= 75.0:
        return "overheating"
    if weakening_score >= 70.0:
        return "weakening"
    if theme_score >= 80.0 and momentum_score >= 70.0 and overheating_score < 40.0:
        if breadth_score >= 70.0:
            return "leading"
        return "strengthening"
    if theme_score >= 70.0 and breadth_score >= 80.0 and overheating_score >= 50.0:
        return "crowded"
    if theme_score >= 55.0 and momentum_score >= 50.0:
        return "strengthening"
    if theme_score >= 40.0 and theme_score < 50.0 and momentum_score >= 35.0:
        return "emerging"
    if momentum_score < 20.0 and theme_score < 25.0 and weakening_score < 50.0:
        return "risk_off"
    if weakening_score >= 50.0 or theme_score < 30.0:
        if theme_score < 20.0:
            return "stale"
        return "cooling"
    return "neutral"


def classify_theme_action(theme_state: str) -> str:
    """Classify recommended theme action from theme state. Paper only."""
    action_map: Dict[str, str] = {
        "emerging": "increase_attention",
        "strengthening": "increase_attention",
        "leading": "keep_priority",
        "crowded": "require_rescore",
        "overheating": "freeze_new_candidates",
        "weakening": "reduce_priority",
        "cooling": "downgrade_theme",
        "stale": "downgrade_theme",
        "risk_off": "human_review_required",
        "neutral": "keep_priority",
    }
    return action_map.get(theme_state, "keep_priority")


# ---------------------------------------------------------------------------
# Market regime classification
# ---------------------------------------------------------------------------

def classify_market_state(
    index_trend_score: float,
    breadth_score: float,
    volatility_score: float,
    volume_score: float,
    risk_appetite_score: float,
) -> str:
    """Classify market state from regime scores. Paper only."""
    if volatility_score >= 80.0:
        return "high_volatility"
    if risk_appetite_score <= 20.0 and index_trend_score <= 30.0:
        return "risk_off"
    if index_trend_score >= 70.0 and breadth_score >= 65.0 and volume_score >= 60.0:
        return "strong_uptrend"
    if index_trend_score >= 55.0 and breadth_score >= 55.0 and volatility_score < 50.0:
        return "healthy_pullback"
    if index_trend_score <= 35.0 and breadth_score <= 40.0:
        return "downtrend"
    if index_trend_score >= 40.0 and index_trend_score < 55.0 and breadth_score >= 45.0 and volume_score < 50.0:
        return "range_bound"
    if index_trend_score >= 40.0 and index_trend_score < 60.0 and volume_score < 50.0:
        return "weak_rebound"
    return "range_bound"


def classify_allowed_risk_mode(market_state: str) -> str:
    """Classify allowed risk mode from market state. Paper only."""
    mode_map: Dict[str, str] = {
        "strong_uptrend": "aggressive_paper",
        "healthy_pullback": "normal_paper",
        "range_bound": "normal_paper",
        "weak_rebound": "defensive_paper",
        "downtrend": "observation_only",
        "high_volatility": "defensive_paper",
        "risk_off": "freeze_promotion",
    }
    return mode_map.get(market_state, "normal_paper")


def _regime_entry_flags(market_state: str) -> Dict[str, bool]:
    """Determine entry flags from market state. Paper only."""
    return {
        "candidate_promotion_allowed": market_state not in ("downtrend", "risk_off"),
        "aggressive_entry_allowed": market_state == "strong_uptrend",
        "second_wave_entry_allowed": market_state in ("strong_uptrend", "healthy_pullback", "range_bound"),
        "abc_pullback_entry_allowed": market_state in ("strong_uptrend", "healthy_pullback", "range_bound", "weak_rebound"),
        "breakout_entry_allowed": market_state in ("strong_uptrend", "healthy_pullback"),
    }


# ---------------------------------------------------------------------------
# Candidate priority adjustment
# ---------------------------------------------------------------------------

def _compute_priority_change(
    final_score: float,
    original_score: float,
    blocked_by_market: bool,
    blocked_by_theme: bool,
    requires_review: bool,
) -> str:
    """Compute priority change direction. Paper only."""
    if requires_review:
        return "human_review_required"
    if blocked_by_market or blocked_by_theme:
        return "freeze_candidate"
    if final_score < 20.0:
        return "require_rescore"
    if final_score >= original_score + 5.0:
        return "promote_priority"
    if final_score <= original_score - 10.0:
        return "reduce_priority"
    return "keep_priority"


def _adjust_score_for_theme(
    base_score: float,
    theme_state: str,
) -> float:
    """Apply theme state adjustment to candidate score. Paper only."""
    adjustments: Dict[str, float] = {
        "leading": 8.0,
        "strengthening": 4.0,
        "emerging": 2.0,
        "neutral": 0.0,
        "crowded": -3.0,
        "overheating": -8.0,
        "weakening": -10.0,
        "cooling": -15.0,
        "stale": -20.0,
        "risk_off": -25.0,
    }
    adj = adjustments.get(theme_state, 0.0)
    return max(0.0, min(100.0, base_score + adj))


def _adjust_score_for_regime(
    base_score: float,
    market_state: str,
) -> float:
    """Apply market regime adjustment to candidate score. Paper only."""
    adjustments: Dict[str, float] = {
        "strong_uptrend": 5.0,
        "healthy_pullback": 2.0,
        "range_bound": 0.0,
        "weak_rebound": -5.0,
        "downtrend": -15.0,
        "high_volatility": -8.0,
        "risk_off": -20.0,
    }
    adj = adjustments.get(market_state, 0.0)
    return max(0.0, min(100.0, base_score + adj))


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------

def _make_review_id(review_period: str, theme_count: int) -> str:
    raw = f"theme-rotation-{review_period}-{theme_count}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _default_market_regime() -> MarketRegime:
    return MarketRegime(
        regime_id="default-regime-v207",
        regime_name="Range Bound Default",
        index_trend_score=55.0,
        breadth_score=52.0,
        volume_score=50.0,
        volatility_score=45.0,
        risk_appetite_score=55.0,
        institutional_flow_score=50.0,
        margin_risk_score=40.0,
        market_state="range_bound",
        allowed_risk_mode="normal_paper",
        candidate_promotion_allowed=True,
        aggressive_entry_allowed=False,
        second_wave_entry_allowed=True,
        abc_pullback_entry_allowed=True,
        breakout_entry_allowed=False,
    )


def _evaluate_theme_item(item: ThemeStrengthItem) -> ThemeStrengthItem:
    """Classify theme state and action for a theme item. Paper only."""
    item.theme_state = classify_theme_state(
        item.theme_score,
        item.momentum_score,
        item.overheating_score,
        item.weakening_score,
        item.breadth_score,
    )
    item.theme_action = classify_theme_action(item.theme_state)
    return item


def _build_theme_rotation_summary(
    theme_items: List[ThemeStrengthItem],
    priority_adjustments: List[CandidatePriorityAdjustment],
    market_regime: MarketRegime,
) -> ThemeRotationSummary:
    """Build theme rotation summary from review output. Paper only."""
    total = len(theme_items)
    leading = [t for t in theme_items if t.theme_state == "leading"]
    strengthening = [t for t in theme_items if t.theme_state == "strengthening"]
    overheating = [t for t in theme_items if t.theme_state == "overheating"]
    weakening = [t for t in theme_items if t.theme_state == "weakening"]
    stale = [t for t in theme_items if t.theme_state in ("stale", "cooling")]
    risk_off = [t for t in theme_items if t.theme_state == "risk_off"]

    top_leading = [t.theme_name for t in sorted(leading, key=lambda x: x.theme_score, reverse=True)[:3]]
    top_strengthening = [t.theme_name for t in sorted(strengthening, key=lambda x: x.momentum_score, reverse=True)[:3]]
    top_overheating = [t.theme_name for t in overheating[:3]]
    top_weakening = [t.theme_name for t in weakening[:3]]

    candidate_count_by_theme = {t.theme_id: t.candidate_count for t in theme_items if t.theme_id}

    promo_allowed = sum(1 for p in priority_adjustments if not p.blocked_by_market_regime and not p.blocked_by_theme_state)
    promo_blocked = sum(1 for p in priority_adjustments if p.blocked_by_market_regime or p.blocked_by_theme_state)

    # Grade based on leading/strengthening vs total
    active_ratio = (len(leading) + len(strengthening)) / max(1, total)
    theme_grade = "A" if active_ratio >= 0.5 else "B" if active_ratio >= 0.3 else "C" if active_ratio >= 0.1 else "D"

    regime_score = (market_regime.index_trend_score + market_regime.breadth_score + market_regime.risk_appetite_score) / 3.0
    regime_grade = "A" if regime_score >= 70.0 else "B" if regime_score >= 55.0 else "C" if regime_score >= 40.0 else "D"

    return ThemeRotationSummary(
        total_theme_count=total,
        leading_theme_count=len(leading),
        strengthening_theme_count=len(strengthening),
        overheating_theme_count=len(overheating),
        weakening_theme_count=len(weakening),
        stale_theme_count=len(stale),
        risk_off_theme_count=len(risk_off),
        top_leading_themes=top_leading,
        top_strengthening_themes=top_strengthening,
        top_overheating_themes=top_overheating,
        top_weakening_themes=top_weakening,
        candidate_count_by_theme=candidate_count_by_theme,
        promotion_allowed_count=promo_allowed,
        promotion_blocked_count=promo_blocked,
        theme_rotation_quality_grade=theme_grade,
        market_regime_quality_grade=regime_grade,
    )


def evaluate_market_regime(regime: Optional[MarketRegime] = None) -> MarketRegime:
    """Evaluate and classify a market regime. Paper only."""
    if regime is None:
        regime = _default_market_regime()
    regime.market_state = classify_market_state(
        regime.index_trend_score,
        regime.breadth_score,
        regime.volatility_score,
        regime.volume_score,
        regime.risk_appetite_score,
    )
    regime.allowed_risk_mode = classify_allowed_risk_mode(regime.market_state)
    flags = _regime_entry_flags(regime.market_state)
    regime.candidate_promotion_allowed = flags["candidate_promotion_allowed"]
    regime.aggressive_entry_allowed = flags["aggressive_entry_allowed"]
    regime.second_wave_entry_allowed = flags["second_wave_entry_allowed"]
    regime.abc_pullback_entry_allowed = flags["abc_pullback_entry_allowed"]
    regime.breakout_entry_allowed = flags["breakout_entry_allowed"]
    return regime


def rank_themes(theme_items: Optional[List[ThemeStrengthItem]] = None) -> List[ThemeStrengthItem]:
    """Rank themes by theme_score descending. Paper only."""
    if theme_items is None:
        theme_items = _default_theme_items()
    for item in theme_items:
        _evaluate_theme_item(item)
    ranked = sorted(theme_items, key=lambda x: x.theme_score, reverse=True)
    for idx, item in enumerate(ranked):
        item.previous_theme_rank = item.theme_rank
        item.theme_rank = idx + 1
    return ranked


def detect_overheating(theme_items: Optional[List[ThemeStrengthItem]] = None) -> List[ThemeStrengthItem]:
    """Detect overheating themes. Paper only."""
    if theme_items is None:
        theme_items = _default_theme_items()
    for item in theme_items:
        _evaluate_theme_item(item)
    return [t for t in theme_items if t.theme_state == "overheating"]


def detect_weakening(theme_items: Optional[List[ThemeStrengthItem]] = None) -> List[ThemeStrengthItem]:
    """Detect weakening themes. Paper only."""
    if theme_items is None:
        theme_items = _default_theme_items()
    for item in theme_items:
        _evaluate_theme_item(item)
    return [t for t in theme_items if t.theme_state in ("weakening", "cooling")]


def adjust_candidate_priority(
    symbol: str,
    name: str,
    candidate_id: str,
    theme_item: ThemeStrengthItem,
    market_regime: MarketRegime,
    original_score: float = 60.0,
    lifecycle_adjusted_score: float = 60.0,
) -> CandidatePriorityAdjustment:
    """Adjust candidate priority based on theme state and market regime. Paper only."""
    theme_adj = _adjust_score_for_theme(original_score, theme_item.theme_state)
    regime_adj = _adjust_score_for_regime(theme_adj, market_regime.market_state)
    final_score = (theme_adj * 0.5 + regime_adj * 0.3 + lifecycle_adjusted_score * 0.2)
    final_score = max(0.0, min(100.0, final_score))

    blocked_by_market = not market_regime.candidate_promotion_allowed
    blocked_by_theme = theme_item.theme_state in ("overheating", "stale", "risk_off")
    requires_review = theme_item.theme_action == "human_review_required"

    reason_codes: List[str] = []
    if blocked_by_market:
        reason_codes.append(f"market_regime_blocked:{market_regime.market_state}")
    if blocked_by_theme:
        reason_codes.append(f"theme_state_blocked:{theme_item.theme_state}")
    if theme_item.theme_action in ("reduce_priority", "downgrade_theme"):
        reason_codes.append(f"theme_action:{theme_item.theme_action}")

    priority_change = _compute_priority_change(
        final_score, original_score, blocked_by_market, blocked_by_theme, requires_review,
    )

    return CandidatePriorityAdjustment(
        symbol=symbol,
        name=name,
        candidate_id=candidate_id,
        theme_id=theme_item.theme_id,
        original_candidate_score=round(original_score, 2),
        theme_adjusted_score=round(theme_adj, 2),
        market_regime_adjusted_score=round(regime_adj, 2),
        lifecycle_adjusted_score=round(lifecycle_adjusted_score, 2),
        final_priority_score=round(final_score, 2),
        priority_change=priority_change,
        priority_reason_codes=reason_codes,
        blocked_by_market_regime=blocked_by_market,
        blocked_by_theme_state=blocked_by_theme,
        requires_human_review=requires_review,
        should_auto_apply=False,
    )


def _default_theme_items() -> List[ThemeStrengthItem]:
    """Return default demo theme items. Paper only."""
    return [
        ThemeStrengthItem(
            theme_id="THEME-AI",
            theme_name="人工智慧",
            theme_group="technology",
            theme_score=85.0,
            momentum_score=80.0,
            breadth_score=75.0,
            leadership_score=82.0,
            earnings_support_score=70.0,
            volume_confirmation_score=78.0,
            institutional_support_score=80.0,
            overheating_score=30.0,
            weakening_score=10.0,
            concentration_risk_score=45.0,
            candidate_count=8,
            promoted_candidate_count=3,
            stale_candidate_count=1,
            expired_candidate_count=0,
            active_candidate_count=7,
        ),
        ThemeStrengthItem(
            theme_id="THEME-EV",
            theme_name="電動車",
            theme_group="green_energy",
            theme_score=55.0,
            momentum_score=50.0,
            breadth_score=48.0,
            leadership_score=52.0,
            earnings_support_score=45.0,
            volume_confirmation_score=50.0,
            institutional_support_score=48.0,
            overheating_score=20.0,
            weakening_score=35.0,
            concentration_risk_score=30.0,
            candidate_count=5,
            promoted_candidate_count=2,
            stale_candidate_count=2,
            expired_candidate_count=0,
            active_candidate_count=5,
        ),
        ThemeStrengthItem(
            theme_id="THEME-SEMI",
            theme_name="半導體",
            theme_group="technology",
            theme_score=90.0,
            momentum_score=85.0,
            breadth_score=80.0,
            leadership_score=88.0,
            earnings_support_score=82.0,
            volume_confirmation_score=85.0,
            institutional_support_score=90.0,
            overheating_score=55.0,
            weakening_score=5.0,
            concentration_risk_score=70.0,
            candidate_count=10,
            promoted_candidate_count=5,
            stale_candidate_count=1,
            expired_candidate_count=0,
            active_candidate_count=9,
        ),
    ]


def run_theme_rotation_review(
    review_input: Optional[ThemeRotationReviewInput] = None,
) -> ThemeRotationReviewResult:
    """Run a paper theme rotation review. Paper only."""
    if review_input is None:
        review_input = ThemeRotationReviewInput(
            review_period="2026-W29",
            theme_items=_default_theme_items(),
        )

    if review_input.market_regime is None:
        market_regime = evaluate_market_regime()
    else:
        market_regime = evaluate_market_regime(review_input.market_regime)

    review_id = _make_review_id(review_input.review_period, len(review_input.theme_items))

    # Evaluate all theme items
    for item in review_input.theme_items:
        _evaluate_theme_item(item)

    # Rank themes
    ranked_themes = sorted(review_input.theme_items, key=lambda x: x.theme_score, reverse=True)
    for idx, item in enumerate(ranked_themes):
        item.previous_theme_rank = item.theme_rank
        item.theme_rank = idx + 1

    # Build candidate priority adjustments (demo: one per theme)
    priority_adjustments: List[CandidatePriorityAdjustment] = []
    for item in ranked_themes:
        if item.candidate_count > 0:
            adj = adjust_candidate_priority(
                symbol=f"DEMO-{item.theme_id}",
                name=item.theme_name,
                candidate_id=f"CAND-{item.theme_id}-001",
                theme_item=item,
                market_regime=market_regime,
                original_score=item.theme_score,
                lifecycle_adjusted_score=item.theme_score * 0.9,
            )
            priority_adjustments.append(adj)

    summary = _build_theme_rotation_summary(ranked_themes, priority_adjustments, market_regime)

    return ThemeRotationReviewResult(
        theme_rotation_review_id=review_id,
        review_period=review_input.review_period,
        market_regime_snapshot=[market_regime.market_state, market_regime.allowed_risk_mode],
        theme_strength_snapshot=[t.theme_id for t in ranked_themes],
        theme_momentum_snapshot=[f"{t.theme_id}:{t.momentum_score}" for t in ranked_themes],
        theme_breadth_snapshot=[f"{t.theme_id}:{t.breadth_score}" for t in ranked_themes],
        theme_overheat_snapshot=[t.theme_id for t in ranked_themes if t.theme_state == "overheating"],
        theme_weakening_snapshot=[t.theme_id for t in ranked_themes if t.theme_state in ("weakening", "cooling")],
        theme_rotation_action_queue=ranked_themes,
        candidate_priority_adjustment_snapshot=priority_adjustments,
        theme_rotation_summary=summary,
        all_passed=True,
    )


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_theme_rotation_json(result: ThemeRotationReviewResult) -> ThemeRotationExportResult:
    """Export theme rotation review as JSON. Paper only."""
    rid = result.theme_rotation_review_id
    parts = [
        f'{{"theme_rotation_review_id": "{rid}", "theme_rotation_version": "{result.theme_rotation_version}",',
        f'"review_period": "{result.review_period}", "paper_only": true,',
        f'"should_auto_apply": false, "no_real_orders": true,',
        f'"market_regime_snapshot": {result.market_regime_snapshot},',
        f'"theme_count": {len(result.theme_rotation_action_queue)},',
        f'"overheat_count": {len(result.theme_overheat_snapshot)},',
        f'"weakening_count": {len(result.theme_weakening_snapshot)},',
        f'"priority_adjustment_count": {len(result.candidate_priority_adjustment_snapshot)}}}',
    ]
    return ThemeRotationExportResult(
        theme_rotation_review_id=rid,
        export_format="json",
        content="".join(str(p) for p in parts),
        is_valid=True,
        export_status="complete",
    )


def export_theme_rotation_markdown(result: ThemeRotationReviewResult) -> ThemeRotationExportResult:
    """Export theme rotation review as Markdown. Paper only."""
    rid = result.theme_rotation_review_id
    summary = result.theme_rotation_summary
    lines = [
        "# Theme Rotation Report v2.0.7",
        "",
        f"**theme_rotation_review_id**: {rid}",
        f"**theme_rotation_version**: {result.theme_rotation_version}",
        f"**review_period**: {result.review_period}",
        f"**paper_only**: True",
        f"**should_auto_apply**: False",
        f"**no_real_orders**: True",
        "",
        "## Market Regime Snapshot",
        "",
        f"- market_regime: {result.market_regime_snapshot}",
        "",
        "## Theme Rotation Summary",
        "",
    ]
    if summary:
        lines += [
            f"- Total Themes: {summary.total_theme_count}",
            f"- Leading: {summary.leading_theme_count}",
            f"- Strengthening: {summary.strengthening_theme_count}",
            f"- Overheating: {summary.overheating_theme_count}",
            f"- Weakening: {summary.weakening_theme_count}",
            f"- Stale/Cooling: {summary.stale_theme_count}",
            f"- Risk-Off: {summary.risk_off_theme_count}",
            f"- Promotion Allowed: {summary.promotion_allowed_count}",
            f"- Promotion Blocked: {summary.promotion_blocked_count}",
            f"- Theme Quality Grade: {summary.theme_rotation_quality_grade}",
            f"- Regime Quality Grade: {summary.market_regime_quality_grade}",
        ]
    lines += [
        "",
        "## Theme Action Queue",
        "",
    ]
    for item in result.theme_rotation_action_queue:
        lines.append(f"- {item.theme_name} [{item.theme_id}]: {item.theme_state} → {item.theme_action} (score={item.theme_score:.1f})")
    lines += ["", "---", "[!] Paper Only | No Real Orders | Not Investment Advice"]
    return ThemeRotationExportResult(
        theme_rotation_review_id=rid,
        export_format="markdown",
        content="\n".join(lines),
        is_valid=True,
        export_status="complete",
    )


def export_theme_strength_csv(result: ThemeRotationReviewResult) -> ThemeStrengthCSV:
    """Export theme strength snapshot as CSV. Paper only."""
    rows = ["theme_id,theme_name,theme_rank,theme_score,momentum_score,theme_state,theme_action,should_auto_apply"]
    for item in result.theme_rotation_action_queue:
        rows.append(
            f"{item.theme_id},{item.theme_name},{item.theme_rank},"
            f"{item.theme_score},{item.momentum_score},"
            f"{item.theme_state},{item.theme_action},False"
        )
    return ThemeStrengthCSV(
        theme_rotation_review_id=result.theme_rotation_review_id,
        csv_content="\n".join(rows),
        row_count=len(result.theme_rotation_action_queue),
        is_valid=True,
    )


def export_market_regime_csv(result: ThemeRotationReviewResult) -> MarketRegimeCSV:
    """Export market regime snapshot as CSV. Paper only."""
    rows = ["field,value"]
    for snap in result.market_regime_snapshot:
        rows.append(f"market_regime_snapshot,{snap}")
    rows.append(f"theme_count,{len(result.theme_rotation_action_queue)}")
    rows.append(f"overheat_count,{len(result.theme_overheat_snapshot)}")
    rows.append(f"weakening_count,{len(result.theme_weakening_snapshot)}")
    rows.append(f"should_auto_apply,False")
    return MarketRegimeCSV(
        theme_rotation_review_id=result.theme_rotation_review_id,
        csv_content="\n".join(rows),
        row_count=len(rows) - 1,
        is_valid=True,
    )


def export_candidate_priority_csv(result: ThemeRotationReviewResult) -> ThemeRotationExportResult:
    """Export candidate priority adjustments as CSV. Paper only."""
    rows = ["symbol,candidate_id,theme_id,original_score,final_priority_score,priority_change,blocked_by_market,blocked_by_theme,should_auto_apply"]
    for adj in result.candidate_priority_adjustment_snapshot:
        rows.append(
            f"{adj.symbol},{adj.candidate_id},{adj.theme_id},"
            f"{adj.original_candidate_score},{adj.final_priority_score},"
            f"{adj.priority_change},{adj.blocked_by_market_regime},"
            f"{adj.blocked_by_theme_state},False"
        )
    return ThemeRotationExportResult(
        theme_rotation_review_id=result.theme_rotation_review_id,
        export_format="csv",
        content="\n".join(rows),
        is_valid=True,
        export_status="complete",
    )


def export_theme_rotation_audit_snapshot(result: ThemeRotationReviewResult) -> ThemeRotationAuditSnapshot:
    """Build theme rotation audit snapshot. Paper only."""
    rid = result.theme_rotation_review_id
    raw = f"{rid}-{result.review_period}-{len(result.theme_rotation_action_queue)}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return ThemeRotationAuditSnapshot(
        theme_rotation_review_id=rid,
        run_metadata=f"v2.0.7-theme-rotation-{rid}",
        market_regime_snapshot=str(result.market_regime_snapshot),
        theme_strength_snapshot=str(result.theme_strength_snapshot),
        overheat_snapshot=str(result.theme_overheat_snapshot),
        weakening_snapshot=str(result.theme_weakening_snapshot),
        priority_adjustment_snapshot=str([a.symbol for a in result.candidate_priority_adjustment_snapshot]),
        safety_snapshot="paper_only=True;no_real_orders=True;should_auto_apply=False;should_auto_apply_theme_rotation=False",
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
        "should_auto_apply_theme_rotation": "False",
    }


def verify_version() -> bool:
    """Verify version constants are correct. Paper only."""
    return VERSION == "2.0.7" and SCHEMA_VERSION == "207"


def get_cockpit_summary_v207() -> Dict[str, Any]:
    """Return cockpit summary for v2.0.7. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "should_auto_apply_theme_rotation": False,
        "models_count": len(_ALL_MODEL_NAMES_V207),
        "cli_commands_count": len(CLI_COMMANDS_V207),
        "gui_tabs_count": len(GUI_TABS_V207),
        "safety_flags_count": len(SAFETY_FLAGS_V207),
        "theme_states_count": len(THEME_STATES),
        "market_states_count": len(MARKET_STATES),
        "allowed_risk_modes_count": len(ALLOWED_RISK_MODES),
        "theme_actions_count": len(THEME_ACTIONS),
        "priority_changes_count": len(PRIORITY_CHANGES),
    }
