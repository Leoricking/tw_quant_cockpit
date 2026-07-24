"""
paper_trading/small_capital_strategy/paper_cockpit_v214.py
v2.0.14 Paper Pullback Reaction & Crash Rebound Confirmation
[!] Paper Only. Research Only. Pullback Reaction Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. No Automatic Pullback Action. Not Investment Advice.
核心句：不猜底、不追反彈、站回均線才是確認，急跌靠近季線只是觀察。
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.14"
SCHEMA_VERSION = "214"
RELEASE_NAME = "Paper Pullback Reaction & Crash Rebound Confirmation"
BASELINE_TESTS = 36989
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

# ---------------------------------------------------------------------------
# Reaction state values
# ---------------------------------------------------------------------------
REACTION_STATES: List[str] = [
    "no_pullback",
    "observation_rebound",
    "short_term_rebound_confirmed",
    "rebound_failed",
    "defensive_wait_second_confirmation",
    "human_review_required",
]

# ---------------------------------------------------------------------------
# Recommended action values
# ---------------------------------------------------------------------------
RECOMMENDED_ACTIONS: List[str] = [
    "observation_only",
    "wait_for_ma_reclaim",
    "short_term_rebound_confirmed",
    "defensive_mode",
    "rebound_failed_reduce_risk",
    "human_review_required",
]

CLI_COMMANDS_V214: List[str] = [
    "paper-cockpit-v214-review-pullback-reaction",
    "paper-cockpit-v214-detect-pullback-event",
    "paper-cockpit-v214-evaluate-rebound-confirmation",
    "paper-cockpit-v214-build-rebound-watch-queue",
    "paper-cockpit-v214-build-rebound-failure-queue",
    "paper-cockpit-v214-export-json",
    "paper-cockpit-v214-export-md",
    "paper-cockpit-v214-export-csv",
    "paper-cockpit-v214-health",
    "paper-cockpit-v214-gate",
]

GUI_TABS_V214: List[str] = [
    "pullback_reaction_v214",
    "rebound_confirmation_v214",
    "rebound_failure_queue_v214",
]

SAFETY_FLAGS_V214: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "pullback_reaction_recommendation_only": True,
    "rebound_recommendation_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_pullback_action": True,
    "no_automatic_stop_loss_execution": True,
    "no_automatic_take_profit_execution": True,
    "no_automatic_rebound_action": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "require_ma_reclaim_for_confirmation_always_true": True,
    "pullback_actions_recommendation_only": True,
}

assert len(SAFETY_FLAGS_V214) == 25, f"Expected 25 SAFETY_FLAGS_V214, got {len(SAFETY_FLAGS_V214)}"
assert len(REACTION_STATES) == 6
assert len(RECOMMENDED_ACTIONS) == 6
assert len(CLI_COMMANDS_V214) == 10
assert len(GUI_TABS_V214) == 3

PULLBACK_REVIEW_FIELDS: List[str] = [
    "pullback_review_id",
    "pullback_version",
    "review_period",
    "index_snapshot",
    "pullback_event_snapshot",
    "ma_reclaim_snapshot",
    "rebound_confirmation_snapshot",
    "tsmc_confirmation_snapshot",
    "futures_adr_confirmation_snapshot",
    "margin_stress_snapshot",
    "rebound_failure_snapshot",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

PULLBACK_POLICY_FIELDS: List[str] = [
    "policy_id",
    "observation_window_days",
    "seasonal_ma_period",
    "reclaim_fast_ma_period",
    "reclaim_slow_ma_period",
    "require_index_near_ma60",
    "require_reclaim_ma5_or_ma10_for_confirmation",
    "require_tsmc_confirmation",
    "require_futures_or_adr_confirmation",
    "require_margin_not_stressed",
    "failure_if_breaks_pullback_low",
    "auto_apply_enabled",
]

PULLBACK_EVENT_FIELDS: List[str] = [
    "index_symbol",
    "index_name",
    "current_index_level",
    "previous_close",
    "pullback_start_level",
    "pullback_low_level",
    "pullback_low_date",
    "pullback_pct",
    "days_since_pullback_low",
    "ma5",
    "ma10",
    "ma20",
    "ma60",
    "near_ma60",
    "reclaimed_ma5",
    "reclaimed_ma10",
    "broke_pullback_low",
    "reaction_state",
    "requires_human_review",
    "should_auto_apply",
]

CONFIRMATION_SIGNAL_FIELDS: List[str] = [
    "tsmc_spot_confirmed",
    "tsmc_adr_confirmed",
    "futures_night_session_stable",
    "foreign_futures_short_not_increasing",
    "margin_stress_controlled",
    "volume_confirmation",
    "ma_reclaim_confirmation",
    "confirmation_score",
    "failed_confirmation_reasons",
    "should_auto_apply",
]

PULLBACK_SUMMARY_FIELDS: List[str] = [
    "reaction_state",
    "index_level",
    "pullback_pct",
    "days_since_pullback_low",
    "near_ma60",
    "reclaimed_ma5",
    "reclaimed_ma10",
    "broke_pullback_low",
    "confirmation_score",
    "rebound_quality_grade",
    "failure_risk_grade",
    "recommended_action",
    "human_review_count",
]

_ALL_MODEL_NAMES_V214: List[str] = [
    "PullbackPolicy",
    "PullbackEvent",
    "ConfirmationSignal",
    "PullbackSummary",
    "PullbackReviewInput",
    "PullbackReviewResult",
    "PullbackExportResult",
    "PullbackAuditSnapshot",
    "PullbackMarkdownReport",
    "ReboundWatchQueueCSV",
    "ReboundFailureQueueCSV",
    "PullbackReactionCSV",
    "V214HealthSummary",
    "V214ReleaseSummary",
    "PullbackSafetyGuard",
    "PullbackSummaryCSV",
]
assert len(_ALL_MODEL_NAMES_V214) == 16

COVERED_VERSIONS: List[str] = [
    "2.0.13", "2.0.12", "2.0.11", "2.0.10", "2.0.9", "2.0.8", "2.0.7",
    "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 16 models, schema_version="214"
# ---------------------------------------------------------------------------

@dataclass
class PullbackPolicy:
    """Pullback policy schema. v2.0.14.
    auto_apply_enabled is always False.
    require_reclaim_ma5_or_ma10_for_confirmation is always True."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    observation_window_days: int = 3
    seasonal_ma_period: int = 60
    reclaim_fast_ma_period: int = 5
    reclaim_slow_ma_period: int = 10
    require_index_near_ma60: bool = True         # ALWAYS True
    require_reclaim_ma5_or_ma10_for_confirmation: bool = True  # ALWAYS True
    require_tsmc_confirmation: bool = True
    require_futures_or_adr_confirmation: bool = True
    require_margin_not_stressed: bool = True
    failure_if_breaks_pullback_low: bool = True
    auto_apply_enabled: bool = False              # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)
        object.__setattr__(self, "require_reclaim_ma5_or_ma10_for_confirmation", True)
        object.__setattr__(self, "require_index_near_ma60", True)


@dataclass
class PullbackEvent:
    """Pullback event schema. v2.0.14. should_auto_apply is always False."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    index_symbol: str = "TWSE"
    index_name: str = "台灣加權指數"
    current_index_level: float = 0.0
    previous_close: float = 0.0
    pullback_start_level: float = 0.0
    pullback_low_level: float = 0.0
    pullback_low_date: str = ""
    pullback_pct: float = 0.0
    days_since_pullback_low: int = 0
    ma5: float = 0.0
    ma10: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0
    near_ma60: bool = False
    reclaimed_ma5: bool = False
    reclaimed_ma10: bool = False
    broke_pullback_low: bool = False
    reaction_state: str = "no_pullback"
    requires_human_review: bool = False
    should_auto_apply: bool = False   # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ConfirmationSignal:
    """Confirmation signal schema. v2.0.14. should_auto_apply is always False."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    tsmc_spot_confirmed: bool = False
    tsmc_adr_confirmed: bool = False
    futures_night_session_stable: bool = False
    foreign_futures_short_not_increasing: bool = False
    margin_stress_controlled: bool = True
    volume_confirmation: bool = False
    ma_reclaim_confirmation: bool = False
    confirmation_score: float = 0.0
    failed_confirmation_reasons: List[str] = field(default_factory=list)
    should_auto_apply: bool = False   # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class PullbackSummary:
    """Pullback summary. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    reaction_state: str = "no_pullback"
    index_level: float = 0.0
    pullback_pct: float = 0.0
    days_since_pullback_low: int = 0
    near_ma60: bool = False
    reclaimed_ma5: bool = False
    reclaimed_ma10: bool = False
    broke_pullback_low: bool = False
    confirmation_score: float = 0.0
    rebound_quality_grade: str = "B"
    failure_risk_grade: str = "B"
    recommended_action: str = "observation_only"
    human_review_count: int = 0


@dataclass
class PullbackReviewInput:
    """Input for pullback reaction review. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    review_period: str = ""
    index_level: float = 43_000.0
    previous_close: float = 44_500.0
    pullback_start_level: float = 45_000.0
    pullback_low_level: float = 42_500.0
    pullback_low_date: str = "2026-07-18"
    days_since_pullback_low: int = 2
    ma5: float = 43_200.0
    ma10: float = 43_800.0
    ma20: float = 44_200.0
    ma60: float = 42_800.0
    tsmc_spot_up: bool = True
    tsmc_adr_positive: bool = True
    futures_night_stable: bool = True
    foreign_futures_short_increasing: bool = False
    margin_stress: bool = False
    volume_expansion: bool = True
    policy: Optional[PullbackPolicy] = None


@dataclass
class PullbackReviewResult:
    """Pullback reaction review result. v2.0.14. should_auto_apply is always False."""
    schema_version: str = "214"
    paper_only: bool = True
    research_only: bool = True
    pullback_reaction_recommendation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    pullback_review_id: str = ""
    pullback_version: str = "2.0.14"
    review_period: str = ""
    policy: Optional[PullbackPolicy] = None
    index_snapshot: Optional[PullbackEvent] = None
    pullback_event_snapshot: Dict[str, Any] = field(default_factory=dict)
    ma_reclaim_snapshot: Dict[str, Any] = field(default_factory=dict)
    rebound_confirmation_snapshot: Optional[ConfirmationSignal] = None
    tsmc_confirmation_snapshot: Dict[str, Any] = field(default_factory=dict)
    futures_adr_confirmation_snapshot: Dict[str, Any] = field(default_factory=dict)
    margin_stress_snapshot: Dict[str, Any] = field(default_factory=dict)
    rebound_failure_snapshot: Dict[str, Any] = field(default_factory=dict)
    human_review_queue: List[str] = field(default_factory=list)
    pullback_summary: Optional[PullbackSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = True
    should_auto_apply: bool = False   # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class PullbackExportResult:
    """Export result for pullback reaction review. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    pullback_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class PullbackAuditSnapshot:
    """Audit snapshot for pullback reaction review. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    pullback_review_id: str = ""
    run_metadata: str = ""
    pullback_event_snapshot: str = ""
    reaction_state: str = ""
    confirmation_snapshot: str = ""
    failure_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class PullbackMarkdownReport:
    """Markdown report for pullback reaction review. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    pullback_review_id: str = ""
    review_period: str = ""
    content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class ReboundWatchQueueCSV:
    """CSV export of rebound watch queue. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    pullback_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ReboundFailureQueueCSV:
    """CSV export of rebound failure queue. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    pullback_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class PullbackReactionCSV:
    """CSV export of pullback reaction summary. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    pullback_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V214HealthSummary:
    """Health summary for v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.14"


@dataclass
class V214ReleaseSummary:
    """Release summary for v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    version: str = "2.0.14"
    release_name: str = RELEASE_NAME


@dataclass
class PullbackSafetyGuard:
    """Safety guard snapshot for pullback reaction. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    no_automatic_pullback_action: bool = True
    no_automatic_stop_loss_execution: bool = True
    no_automatic_take_profit_execution: bool = True
    no_automatic_rebalance: bool = True
    no_automatic_rebound_action: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False
    require_reclaim_ma5_or_ma10_for_confirmation: bool = True
    pullback_actions_recommendation_only: bool = True
    rebound_actions_recommendation_only: bool = True


@dataclass
class PullbackSummaryCSV:
    """CSV export of pullback summary. v2.0.14."""
    schema_version: str = "214"
    paper_only: bool = True
    no_real_orders: bool = True
    pullback_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


# ---------------------------------------------------------------------------
# ID helper
# ---------------------------------------------------------------------------

def _make_pullback_review_id(review_period: str, index_level: float) -> str:
    raw = f"v214-{review_period}-idx{int(index_level)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:10]


# ---------------------------------------------------------------------------
# Pullback detection helpers
# ---------------------------------------------------------------------------

def _calc_pullback_pct(start_level: float, low_level: float) -> float:
    """Calculate pullback percentage from high to low. Paper only."""
    if start_level <= 0:
        return 0.0
    return round((low_level - start_level) / start_level, 4)


def _is_near_ma60(index_level: float, ma60: float, tolerance_pct: float = 0.03) -> bool:
    """True if index is within tolerance_pct of MA60. Paper only."""
    if ma60 <= 0:
        return False
    diff_pct = abs(index_level - ma60) / ma60
    return diff_pct <= tolerance_pct


def _detect_reaction_state(
    pullback_event: "PullbackEvent",
    confirmation: "ConfirmationSignal",
    policy: "PullbackPolicy",
) -> str:
    """Classify pullback reaction state. Paper only."""
    # No meaningful pullback
    if pullback_event.pullback_pct > -0.03:
        return "no_pullback"

    # Rebound failure takes priority
    if pullback_event.broke_pullback_low:
        return "rebound_failed"

    # Short-term rebound confirmed: must reclaim MA5 or MA10
    if policy.require_reclaim_ma5_or_ma10_for_confirmation:
        if (pullback_event.reclaimed_ma5 or pullback_event.reclaimed_ma10) and confirmation.confirmation_score >= 0.6:
            return "short_term_rebound_confirmed"

    # Defensive: very low confirmation score, need second confirmation (checked before observation)
    if confirmation.confirmation_score < 0.4:
        return "defensive_wait_second_confirmation"

    # Observation rebound: near MA60 within observation window with some signals
    if (
        pullback_event.near_ma60
        and pullback_event.days_since_pullback_low <= policy.observation_window_days
        and not pullback_event.broke_pullback_low
    ):
        return "observation_rebound"

    # Human review for ambiguous cases
    if pullback_event.requires_human_review:
        return "human_review_required"

    return "observation_rebound"


def _calc_confirmation_score(
    tsmc_spot: bool,
    tsmc_adr: bool,
    futures_stable: bool,
    foreign_short_not_increasing: bool,
    margin_controlled: bool,
    volume_confirmed: bool,
    ma_reclaim: bool,
) -> float:
    """Calculate confirmation score 0.0-1.0. Paper only."""
    weights = [
        (tsmc_spot, 0.20),
        (tsmc_adr, 0.15),
        (futures_stable, 0.15),
        (foreign_short_not_increasing, 0.15),
        (margin_controlled, 0.15),
        (volume_confirmed, 0.10),
        (ma_reclaim, 0.10),
    ]
    score = sum(w for ok, w in weights if ok)
    return round(score, 4)


def _classify_rebound_quality_grade(
    reaction_state: str,
    confirmation_score: float,
    reclaimed_ma5: bool,
    reclaimed_ma10: bool,
) -> str:
    if reaction_state == "short_term_rebound_confirmed" and confirmation_score >= 0.8:
        return "A"
    if reaction_state == "short_term_rebound_confirmed" and confirmation_score >= 0.6:
        return "B"
    if reaction_state == "observation_rebound" and (reclaimed_ma5 or reclaimed_ma10):
        return "B"
    return "C"


def _classify_failure_risk_grade(
    broke_pullback_low: bool,
    confirmation_score: float,
    reaction_state: str,
) -> str:
    if broke_pullback_low or reaction_state == "rebound_failed":
        return "C"
    if confirmation_score < 0.4 or reaction_state == "defensive_wait_second_confirmation":
        return "C"
    if confirmation_score < 0.6:
        return "B"
    return "A"


def _classify_recommended_action(reaction_state: str) -> str:
    mapping = {
        "no_pullback": "observation_only",
        "observation_rebound": "wait_for_ma_reclaim",
        "short_term_rebound_confirmed": "short_term_rebound_confirmed",
        "rebound_failed": "rebound_failed_reduce_risk",
        "defensive_wait_second_confirmation": "defensive_mode",
        "human_review_required": "human_review_required",
    }
    return mapping.get(reaction_state, "observation_only")


# ---------------------------------------------------------------------------
# Pullback event builder
# ---------------------------------------------------------------------------

def detect_pullback_event(
    index_level: float,
    previous_close: float = 0.0,
    pullback_start_level: float = 0.0,
    pullback_low_level: float = 0.0,
    pullback_low_date: str = "",
    days_since_pullback_low: int = 0,
    ma5: float = 0.0,
    ma10: float = 0.0,
    ma20: float = 0.0,
    ma60: float = 0.0,
    policy: Optional[PullbackPolicy] = None,
) -> PullbackEvent:
    """Detect and classify pullback event. Paper only, no real orders."""
    if policy is None:
        policy = PullbackPolicy(policy_id="default-policy-v214")

    pullback_pct = _calc_pullback_pct(pullback_start_level, pullback_low_level)
    near_ma60 = _is_near_ma60(pullback_low_level if pullback_low_level > 0 else index_level, ma60)
    reclaimed_ma5 = index_level >= ma5 if ma5 > 0 else False
    reclaimed_ma10 = index_level >= ma10 if ma10 > 0 else False
    broke_pullback_low = (
        index_level < pullback_low_level if pullback_low_level > 0 else False
    )

    requires_human_review = (
        pullback_pct < -0.10
        or days_since_pullback_low > policy.observation_window_days
        or (not near_ma60 and pullback_pct < -0.05)
    )

    return PullbackEvent(
        schema_version="214",
        paper_only=True,
        no_real_orders=True,
        index_symbol="TWSE",
        index_name="台灣加權指數",
        current_index_level=round(index_level, 2),
        previous_close=round(previous_close, 2),
        pullback_start_level=round(pullback_start_level, 2),
        pullback_low_level=round(pullback_low_level, 2),
        pullback_low_date=pullback_low_date,
        pullback_pct=pullback_pct,
        days_since_pullback_low=days_since_pullback_low,
        ma5=round(ma5, 2),
        ma10=round(ma10, 2),
        ma20=round(ma20, 2),
        ma60=round(ma60, 2),
        near_ma60=near_ma60,
        reclaimed_ma5=reclaimed_ma5,
        reclaimed_ma10=reclaimed_ma10,
        broke_pullback_low=broke_pullback_low,
        reaction_state="no_pullback",  # updated after confirmation
        requires_human_review=requires_human_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Confirmation signal builder
# ---------------------------------------------------------------------------

def evaluate_rebound_confirmation(
    tsmc_spot_up: bool = True,
    tsmc_adr_positive: bool = True,
    futures_night_stable: bool = True,
    foreign_futures_short_increasing: bool = False,
    margin_stress: bool = False,
    volume_expansion: bool = True,
    ma_reclaim: bool = False,
) -> ConfirmationSignal:
    """Evaluate rebound confirmation signals. Paper only, no real orders."""
    foreign_ok = not foreign_futures_short_increasing
    margin_ok = not margin_stress

    score = _calc_confirmation_score(
        tsmc_spot=tsmc_spot_up,
        tsmc_adr=tsmc_adr_positive,
        futures_stable=futures_night_stable,
        foreign_short_not_increasing=foreign_ok,
        margin_controlled=margin_ok,
        volume_confirmed=volume_expansion,
        ma_reclaim=ma_reclaim,
    )

    failed_reasons: List[str] = []
    if not tsmc_spot_up:
        failed_reasons.append("tsmc_spot_not_confirmed")
    if not tsmc_adr_positive:
        failed_reasons.append("tsmc_adr_not_confirmed")
    if not futures_night_stable:
        failed_reasons.append("futures_night_session_unstable")
    if foreign_futures_short_increasing:
        failed_reasons.append("foreign_futures_short_increasing")
    if margin_stress:
        failed_reasons.append("margin_stress_detected")
    if not volume_expansion:
        failed_reasons.append("volume_not_confirmed")
    if not ma_reclaim:
        failed_reasons.append("ma_reclaim_not_confirmed")

    return ConfirmationSignal(
        schema_version="214",
        paper_only=True,
        no_real_orders=True,
        tsmc_spot_confirmed=tsmc_spot_up,
        tsmc_adr_confirmed=tsmc_adr_positive,
        futures_night_session_stable=futures_night_stable,
        foreign_futures_short_not_increasing=foreign_ok,
        margin_stress_controlled=margin_ok,
        volume_confirmation=volume_expansion,
        ma_reclaim_confirmation=ma_reclaim,
        confirmation_score=score,
        failed_confirmation_reasons=failed_reasons,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Queue builders
# ---------------------------------------------------------------------------

def build_rebound_watch_queue(
    reaction_state: str,
    candidate_symbols: Optional[List[str]] = None,
) -> List[str]:
    """Build rebound watch queue for observation states. Paper only."""
    if candidate_symbols is None:
        candidate_symbols = _default_candidate_symbols()
    if reaction_state in ("observation_rebound", "defensive_wait_second_confirmation"):
        return list(candidate_symbols)
    return []


def build_rebound_failure_queue(
    reaction_state: str,
    candidate_symbols: Optional[List[str]] = None,
) -> List[str]:
    """Build rebound failure queue for failed/defensive states. Paper only."""
    if candidate_symbols is None:
        candidate_symbols = _default_candidate_symbols()
    if reaction_state in ("rebound_failed",):
        return list(candidate_symbols)
    if reaction_state == "defensive_wait_second_confirmation":
        return [s for s in candidate_symbols if s in _default_core_symbols()]
    return []


def build_human_review_queue(
    reaction_state: str,
    confirmation: ConfirmationSignal,
) -> List[str]:
    """Build human review queue. Paper only."""
    items = []
    if reaction_state == "human_review_required":
        items.append(f"reaction_alert:{reaction_state}")
    if reaction_state == "rebound_failed":
        items.append("rebound_failure_alert:reduce_risk_now")
    if confirmation.failed_confirmation_reasons:
        for reason in confirmation.failed_confirmation_reasons[:3]:
            items.append(f"confirmation_fail:{reason}")
    return items


# ---------------------------------------------------------------------------
# Default demo data
# ---------------------------------------------------------------------------

def _default_policy() -> PullbackPolicy:
    return PullbackPolicy(policy_id="default-policy-v214")


def _default_candidate_symbols() -> List[str]:
    return ["2330", "2454", "2382", "2308", "6669", "2317", "3711", "2303"]


def _default_core_symbols() -> List[str]:
    return ["2330", "2454", "0050", "0056"]


def _default_review_input() -> PullbackReviewInput:
    return PullbackReviewInput(
        review_period="2026-W29",
        index_level=43_000.0,
        previous_close=44_500.0,
        pullback_start_level=45_000.0,
        pullback_low_level=42_500.0,
        pullback_low_date="2026-07-18",
        days_since_pullback_low=2,
        ma5=43_200.0,
        ma10=43_800.0,
        ma20=44_200.0,
        ma60=42_800.0,
        tsmc_spot_up=True,
        tsmc_adr_positive=True,
        futures_night_stable=True,
        foreign_futures_short_increasing=False,
        margin_stress=False,
        volume_expansion=True,
        policy=_default_policy(),
    )


# ---------------------------------------------------------------------------
# Summary builder
# ---------------------------------------------------------------------------

def _build_pullback_summary(
    pullback_event: PullbackEvent,
    confirmation: ConfirmationSignal,
    human_review_queue: List[str],
) -> PullbackSummary:
    reaction_state = pullback_event.reaction_state
    rebound_grade = _classify_rebound_quality_grade(
        reaction_state,
        confirmation.confirmation_score,
        pullback_event.reclaimed_ma5,
        pullback_event.reclaimed_ma10,
    )
    failure_grade = _classify_failure_risk_grade(
        pullback_event.broke_pullback_low,
        confirmation.confirmation_score,
        reaction_state,
    )
    recommended_action = _classify_recommended_action(reaction_state)

    return PullbackSummary(
        schema_version="214",
        paper_only=True,
        no_real_orders=True,
        reaction_state=reaction_state,
        index_level=round(pullback_event.current_index_level, 2),
        pullback_pct=pullback_event.pullback_pct,
        days_since_pullback_low=pullback_event.days_since_pullback_low,
        near_ma60=pullback_event.near_ma60,
        reclaimed_ma5=pullback_event.reclaimed_ma5,
        reclaimed_ma10=pullback_event.reclaimed_ma10,
        broke_pullback_low=pullback_event.broke_pullback_low,
        confirmation_score=confirmation.confirmation_score,
        rebound_quality_grade=rebound_grade,
        failure_risk_grade=failure_grade,
        recommended_action=recommended_action,
        human_review_count=len(human_review_queue),
    )


# ---------------------------------------------------------------------------
# Main review engine
# ---------------------------------------------------------------------------

def run_pullback_reaction_review(
    review_input: Optional[PullbackReviewInput] = None,
) -> PullbackReviewResult:
    """Run a paper pullback reaction review. Paper only, no real orders."""
    if review_input is None:
        review_input = _default_review_input()

    policy = review_input.policy or _default_policy()
    review_id = _make_pullback_review_id(review_input.review_period, review_input.index_level)

    pullback_event = detect_pullback_event(
        index_level=review_input.index_level,
        previous_close=review_input.previous_close,
        pullback_start_level=review_input.pullback_start_level,
        pullback_low_level=review_input.pullback_low_level,
        pullback_low_date=review_input.pullback_low_date,
        days_since_pullback_low=review_input.days_since_pullback_low,
        ma5=review_input.ma5,
        ma10=review_input.ma10,
        ma20=review_input.ma20,
        ma60=review_input.ma60,
        policy=policy,
    )

    ma_reclaim = pullback_event.reclaimed_ma5 or pullback_event.reclaimed_ma10

    confirmation = evaluate_rebound_confirmation(
        tsmc_spot_up=review_input.tsmc_spot_up,
        tsmc_adr_positive=review_input.tsmc_adr_positive,
        futures_night_stable=review_input.futures_night_stable,
        foreign_futures_short_increasing=review_input.foreign_futures_short_increasing,
        margin_stress=review_input.margin_stress,
        volume_expansion=review_input.volume_expansion,
        ma_reclaim=ma_reclaim,
    )

    reaction_state = _detect_reaction_state(pullback_event, confirmation, policy)
    object.__setattr__(pullback_event, "reaction_state", reaction_state)

    human_queue = build_human_review_queue(reaction_state, confirmation)
    watch_queue = build_rebound_watch_queue(reaction_state)
    failure_queue = build_rebound_failure_queue(reaction_state)

    pullback_event_snapshot = {
        "pullback_pct": pullback_event.pullback_pct,
        "pullback_low_level": pullback_event.pullback_low_level,
        "pullback_low_date": pullback_event.pullback_low_date,
        "days_since_pullback_low": pullback_event.days_since_pullback_low,
        "near_ma60": pullback_event.near_ma60,
    }

    ma_reclaim_snapshot = {
        "ma5": pullback_event.ma5,
        "ma10": pullback_event.ma10,
        "ma20": pullback_event.ma20,
        "ma60": pullback_event.ma60,
        "reclaimed_ma5": pullback_event.reclaimed_ma5,
        "reclaimed_ma10": pullback_event.reclaimed_ma10,
        "require_reclaim_ma5_or_ma10_for_confirmation": True,
    }

    tsmc_snapshot = {
        "tsmc_spot_confirmed": confirmation.tsmc_spot_confirmed,
        "tsmc_adr_confirmed": confirmation.tsmc_adr_confirmed,
        "paper_only": True,
        "should_auto_apply": False,
    }

    futures_adr_snapshot = {
        "futures_night_session_stable": confirmation.futures_night_session_stable,
        "foreign_futures_short_not_increasing": confirmation.foreign_futures_short_not_increasing,
        "should_auto_apply": False,
    }

    margin_stress_snapshot = {
        "margin_stress_controlled": confirmation.margin_stress_controlled,
        "should_auto_apply": False,
    }

    rebound_failure_snapshot = {
        "broke_pullback_low": pullback_event.broke_pullback_low,
        "reaction_state": reaction_state,
        "failure_queue_count": len(failure_queue),
        "should_auto_apply": False,
    }

    summary = _build_pullback_summary(pullback_event, confirmation, human_queue)

    return PullbackReviewResult(
        pullback_review_id=review_id,
        pullback_version="2.0.14",
        review_period=review_input.review_period,
        policy=policy,
        index_snapshot=pullback_event,
        pullback_event_snapshot=pullback_event_snapshot,
        ma_reclaim_snapshot=ma_reclaim_snapshot,
        rebound_confirmation_snapshot=confirmation,
        tsmc_confirmation_snapshot=tsmc_snapshot,
        futures_adr_confirmation_snapshot=futures_adr_snapshot,
        margin_stress_snapshot=margin_stress_snapshot,
        rebound_failure_snapshot=rebound_failure_snapshot,
        human_review_queue=human_queue,
        pullback_summary=summary,
        paper_only_safety_snapshot=True,
        all_passed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_pullback_json(result: PullbackReviewResult) -> PullbackExportResult:
    """Export pullback reaction review as JSON. Paper only."""
    import json as _json
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    summ = result.pullback_summary
    payload = {
        "version": "2.0.14",
        "schema_version": "214",
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "pullback_review_id": result.pullback_review_id,
        "pullback_version": result.pullback_version,
        "review_period": result.review_period,
        "reaction_state": evt.reaction_state if evt else "",
        "pullback_pct": evt.pullback_pct if evt else 0.0,
        "days_since_pullback_low": evt.days_since_pullback_low if evt else 0,
        "near_ma60": evt.near_ma60 if evt else False,
        "reclaimed_ma5": evt.reclaimed_ma5 if evt else False,
        "reclaimed_ma10": evt.reclaimed_ma10 if evt else False,
        "broke_pullback_low": evt.broke_pullback_low if evt else False,
        "confirmation_score": conf.confirmation_score if conf else 0.0,
        "recommended_action": summ.recommended_action if summ else "",
        "human_review_count": len(result.human_review_queue),
        "require_reclaim_ma5_or_ma10_for_confirmation": True,
        "pullback_actions_recommendation_only": True,
    }
    content = _json.dumps(payload, ensure_ascii=False, indent=2)
    return PullbackExportResult(
        pullback_review_id=result.pullback_review_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


def export_pullback_markdown(result: PullbackReviewResult) -> PullbackExportResult:
    """Export pullback reaction review as Markdown. Paper only."""
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    summ = result.pullback_summary
    lines = [
        "# Paper Pullback Reaction Review v2.0.14",
        "",
        f"**Period:** {result.review_period}",
        f"**Pullback Review ID:** {result.pullback_review_id}",
        f"**Paper Only:** True",
        f"**No Real Orders:** True",
        f"**Should Auto Apply:** False",
        f"**核心句：不猜底、不追反彈、站回均線才是確認，急跌靠近季線只是觀察。**",
        "",
        f"## Reaction State: {evt.reaction_state if evt else 'N/A'}",
        f"## Pullback Pct: {evt.pullback_pct:.2%}" if evt else "## Pullback Pct: N/A",
        f"## Days Since Pullback Low: {evt.days_since_pullback_low if evt else 0}",
        f"## Near MA60: {evt.near_ma60 if evt else False}",
        f"## Reclaimed MA5: {evt.reclaimed_ma5 if evt else False}",
        f"## Reclaimed MA10: {evt.reclaimed_ma10 if evt else False}",
        f"## Broke Pullback Low: {evt.broke_pullback_low if evt else False}",
        f"## Confirmation Score: {conf.confirmation_score:.2f}" if conf else "## Confirmation Score: N/A",
        f"## Recommended Action: {summ.recommended_action if summ else 'N/A'}",
        f"## Human Review Count: {len(result.human_review_queue)}",
        "",
        "*[!] Paper Only. Not Investment Advice. Pullback Actions Are Recommendation Only.*",
    ]
    content = "\n".join(lines)
    return PullbackExportResult(
        pullback_review_id=result.pullback_review_id,
        export_format="markdown",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


def export_pullback_csv(result: PullbackReviewResult) -> PullbackSummaryCSV:
    """Export pullback summary as CSV. Paper only."""
    header = "reaction_state,pullback_pct,days_since_pullback_low,near_ma60,reclaimed_ma5,reclaimed_ma10,broke_pullback_low,confirmation_score,recommended_action,human_review_count,should_auto_apply"
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    summ = result.pullback_summary
    rows = [header]
    rows.append(
        f"{evt.reaction_state if evt else ''},"
        f"{evt.pullback_pct if evt else 0.0},"
        f"{evt.days_since_pullback_low if evt else 0},"
        f"{evt.near_ma60 if evt else False},"
        f"{evt.reclaimed_ma5 if evt else False},"
        f"{evt.reclaimed_ma10 if evt else False},"
        f"{evt.broke_pullback_low if evt else False},"
        f"{conf.confirmation_score if conf else 0.0},"
        f"{summ.recommended_action if summ else ''},"
        f"{len(result.human_review_queue)},"
        f"False"
    )
    csv_content = "\n".join(rows)
    return PullbackSummaryCSV(
        pullback_review_id=result.pullback_review_id,
        csv_content=csv_content,
        row_count=1,
        is_valid=True,
    )


def export_rebound_watch_queue_csv(result: PullbackReviewResult) -> ReboundWatchQueueCSV:
    """Export rebound watch queue as CSV. Paper only."""
    evt = result.index_snapshot
    reaction_state = evt.reaction_state if evt else "no_pullback"
    watch_queue = build_rebound_watch_queue(reaction_state)
    header = "symbol,reaction_state,watch_reason,should_auto_apply"
    rows = [header]
    for sym in watch_queue:
        rows.append(f"{sym},{reaction_state},pullback_observation,False")
    csv_content = "\n".join(rows)
    return ReboundWatchQueueCSV(
        pullback_review_id=result.pullback_review_id,
        csv_content=csv_content,
        row_count=len(watch_queue),
        is_valid=True,
    )


def export_rebound_failure_queue_csv(result: PullbackReviewResult) -> ReboundFailureQueueCSV:
    """Export rebound failure queue as CSV. Paper only."""
    evt = result.index_snapshot
    reaction_state = evt.reaction_state if evt else "no_pullback"
    failure_queue = build_rebound_failure_queue(reaction_state)
    header = "symbol,reaction_state,failure_reason,should_auto_apply"
    rows = [header]
    for sym in failure_queue:
        rows.append(f"{sym},{reaction_state},rebound_failure_detected,False")
    csv_content = "\n".join(rows)
    return ReboundFailureQueueCSV(
        pullback_review_id=result.pullback_review_id,
        csv_content=csv_content,
        row_count=len(failure_queue),
        is_valid=True,
    )


def export_pullback_audit_snapshot(result: PullbackReviewResult) -> PullbackAuditSnapshot:
    """Export pullback audit snapshot. Paper only."""
    hash_val = hashlib.sha256(
        f"{result.pullback_review_id}-{result.review_period}".encode()
    ).hexdigest()[:16]
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    return PullbackAuditSnapshot(
        pullback_review_id=result.pullback_review_id,
        run_metadata="v214-paper-only-pullback-reaction-audit",
        pullback_event_snapshot=f"pullback_pct={evt.pullback_pct if evt else 0},reaction_state={evt.reaction_state if evt else ''}",
        reaction_state=evt.reaction_state if evt else "",
        confirmation_snapshot=f"score={conf.confirmation_score if conf else 0},tsmc_spot={conf.tsmc_spot_confirmed if conf else False}",
        failure_snapshot=f"broke_pullback_low={evt.broke_pullback_low if evt else False}",
        safety_snapshot="paper_only=True,no_real_orders=True,should_auto_apply=False,auto_apply_enabled=False,require_reclaim_ma5_or_ma10_for_confirmation=True",
        reproducibility_hash=hash_val,
        export_status="complete",
    )


# ---------------------------------------------------------------------------
# Version / summary
# ---------------------------------------------------------------------------

def verify_version() -> bool:
    """Verify v2.0.14 version constants are correct."""
    return VERSION == "2.0.14" and SCHEMA_VERSION == "214"


def get_cockpit_summary_v214() -> Dict[str, Any]:
    """Return v2.0.14 cockpit summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "require_reclaim_ma5_or_ma10_for_confirmation": True,
        "pullback_actions_recommendation_only": True,
        "rebound_actions_recommendation_only": True,
        "no_automatic_pullback_action": True,
        "no_automatic_rebound_action": True,
        "reaction_state_count": len(REACTION_STATES),
        "recommended_action_count": len(RECOMMENDED_ACTIONS),
        "cli_command_count": len(CLI_COMMANDS_V214),
        "gui_tab_count": len(GUI_TABS_V214),
        "safety_flag_count": len(SAFETY_FLAGS_V214),
        "model_count": len(_ALL_MODEL_NAMES_V214),
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }
