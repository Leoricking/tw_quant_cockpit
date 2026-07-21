"""
paper_trading/small_capital_strategy/paper_cockpit_v206.py
v2.0.6 Paper Candidate Lifecycle & Setup Aging Control
[!] Paper Only. Research Only. Lifecycle Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.6"
SCHEMA_VERSION = "206"
RELEASE_NAME = "Paper Candidate Lifecycle & Setup Aging Control"
BASELINE_TESTS = 34332
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

LIFECYCLE_STATES: List[str] = [
    "newly_promoted",
    "active_candidate",
    "waiting_buy_point",
    "second_wave_waiting",
    "abc_pullback_waiting",
    "breakout_waiting",
    "cooling_down",
    "stale_setup",
    "expired_candidate",
    "rescore_required",
    "downgraded_to_watchlist",
    "removed_from_pool",
    "human_review_required",
]

AGING_BUCKETS: List[str] = [
    "fresh",
    "normal",
    "aging",
    "stale",
    "expired",
]

ACTION_TYPES: List[str] = [
    "keep_active",
    "keep_waiting",
    "move_to_cooldown",
    "mark_stale",
    "require_rescore",
    "downgrade_to_watchlist",
    "remove_from_candidate_pool",
    "require_human_review",
]

CLI_COMMANDS_V206: List[str] = [
    "paper-cockpit-v206-review-lifecycle",
    "paper-cockpit-v206-evaluate-aging",
    "paper-cockpit-v206-build-stale-queue",
    "paper-cockpit-v206-build-expired-queue",
    "paper-cockpit-v206-build-rescore-queue",
    "paper-cockpit-v206-build-cooldown-queue",
    "paper-cockpit-v206-export-json",
    "paper-cockpit-v206-export-md",
    "paper-cockpit-v206-export-csv",
    "paper-cockpit-v206-health",
    "paper-cockpit-v206-gate",
]

GUI_TABS_V206: List[str] = [
    "candidate_lifecycle_v206",
    "setup_aging_v206",
    "stale_candidate_queue_v206",
]

LIFECYCLE_REVIEW_FIELDS: List[str] = [
    "lifecycle_review_id",
    "lifecycle_version",
    "review_period",
    "input_candidate_snapshot",
    "watchlist_rotation_snapshot",
    "setup_aging_snapshot",
    "lifecycle_action_queue",
    "cooldown_queue",
    "stale_setup_queue",
    "expired_candidate_queue",
    "rescore_queue",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

LIFECYCLE_ITEM_FIELDS: List[str] = [
    "symbol",
    "name",
    "candidate_id",
    "current_lifecycle_state",
    "previous_lifecycle_state",
    "days_in_candidate_pool",
    "days_since_last_signal",
    "days_since_last_score_update",
    "setup_type",
    "setup_age_bucket",
    "signal_age_bucket",
    "theme_age_bucket",
    "stale_reasons",
    "refresh_reasons",
    "downgrade_reasons",
    "remove_reasons",
    "human_review_reasons",
    "next_lifecycle_action",
]

AGING_POLICY_FIELDS: List[str] = [
    "policy_id",
    "max_days_active_candidate",
    "max_days_waiting_buy_point",
    "max_days_without_signal_refresh",
    "max_days_without_score_update",
    "stale_score_threshold",
    "remove_score_threshold",
    "cooldown_days",
    "require_human_review_before_remove",
    "auto_apply_enabled",
]

LIFECYCLE_ACTION_FIELDS: List[str] = [
    "action_id",
    "symbol",
    "from_state",
    "to_state",
    "action_type",
    "action_reason_codes",
    "age_score",
    "current_score",
    "risk_score",
    "setup_quality_score",
    "confidence_score",
    "requires_human_review",
    "should_auto_apply",
]

LIFECYCLE_SUMMARY_FIELDS: List[str] = [
    "total_candidate_count",
    "active_count",
    "waiting_count",
    "cooling_down_count",
    "stale_count",
    "expired_count",
    "rescore_required_count",
    "downgrade_count",
    "remove_count",
    "human_review_count",
    "avg_days_in_candidate_pool",
    "avg_days_since_last_signal",
    "top_stale_reasons",
    "top_remove_reasons",
    "lifecycle_quality_grade",
]

LIFECYCLE_EXPORT_FORMATS: List[str] = [
    "json",
    "markdown",
    "csv",
    "audit_snapshot",
]

SAFETY_FLAGS_V206: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "lifecycle_only": True,
    "validation_only": True,
    "candidate_lifecycle_only": True,
    "setup_aging_control_only": True,
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
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
}

assert len(SAFETY_FLAGS_V206) == 20, f"Expected 20 SAFETY_FLAGS_V206, got {len(SAFETY_FLAGS_V206)}"
assert len(LIFECYCLE_STATES) == 13
assert len(AGING_BUCKETS) == 5
assert len(ACTION_TYPES) == 8
assert len(CLI_COMMANDS_V206) == 11
assert len(GUI_TABS_V206) == 3
assert len(LIFECYCLE_REVIEW_FIELDS) == 13
assert len(LIFECYCLE_ITEM_FIELDS) == 18
assert len(AGING_POLICY_FIELDS) == 10
assert len(LIFECYCLE_ACTION_FIELDS) == 13
assert len(LIFECYCLE_SUMMARY_FIELDS) == 15
assert len(LIFECYCLE_EXPORT_FORMATS) == 4

COVERED_VERSIONS: List[str] = [
    "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 13 models, schema_version="206"
# ---------------------------------------------------------------------------

@dataclass
class CandidateLifecycleItem:
    """Candidate lifecycle item schema. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    candidate_id: str = ""
    current_lifecycle_state: str = "active_candidate"
    previous_lifecycle_state: str = "newly_promoted"
    days_in_candidate_pool: int = 0
    days_since_last_signal: int = 0
    days_since_last_score_update: int = 0
    setup_type: str = ""
    setup_age_bucket: str = "fresh"
    signal_age_bucket: str = "fresh"
    theme_age_bucket: str = "fresh"
    stale_reasons: List[str] = field(default_factory=list)
    refresh_reasons: List[str] = field(default_factory=list)
    downgrade_reasons: List[str] = field(default_factory=list)
    remove_reasons: List[str] = field(default_factory=list)
    human_review_reasons: List[str] = field(default_factory=list)
    next_lifecycle_action: str = "keep_active"


@dataclass
class SetupAgingPolicy:
    """Setup aging policy schema. v2.0.6. auto_apply_enabled is always False."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = "default_aging_policy_v206"
    max_days_active_candidate: int = 60
    max_days_waiting_buy_point: int = 30
    max_days_without_signal_refresh: int = 14
    max_days_without_score_update: int = 21
    stale_score_threshold: float = 40.0
    remove_score_threshold: float = 20.0
    cooldown_days: int = 14
    require_human_review_before_remove: bool = True
    auto_apply_enabled: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class LifecycleAction:
    """Lifecycle action schema. v2.0.6. should_auto_apply is always False."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    action_id: str = ""
    symbol: str = ""
    from_state: str = "active_candidate"
    to_state: str = "active_candidate"
    action_type: str = "keep_active"
    action_reason_codes: List[str] = field(default_factory=list)
    age_score: float = 0.0
    current_score: float = 0.0
    risk_score: float = 0.0
    setup_quality_score: float = 0.0
    confidence_score: float = 0.0
    requires_human_review: bool = True
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class LifecycleSummary:
    """Lifecycle summary for a lifecycle review. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    total_candidate_count: int = 0
    active_count: int = 0
    waiting_count: int = 0
    cooling_down_count: int = 0
    stale_count: int = 0
    expired_count: int = 0
    rescore_required_count: int = 0
    downgrade_count: int = 0
    remove_count: int = 0
    human_review_count: int = 0
    avg_days_in_candidate_pool: float = 0.0
    avg_days_since_last_signal: float = 0.0
    top_stale_reasons: List[str] = field(default_factory=list)
    top_remove_reasons: List[str] = field(default_factory=list)
    lifecycle_quality_grade: str = "C"


@dataclass
class LifecycleReviewInput:
    """Input for a lifecycle review run. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    review_period: str = ""
    candidate_items: List[CandidateLifecycleItem] = field(default_factory=list)
    watchlist_rotation_ids: List[str] = field(default_factory=list)
    aging_policy: Optional[SetupAgingPolicy] = None
    human_review_required: bool = True


@dataclass
class LifecycleReviewResult:
    """Full result of one lifecycle review run. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    research_only: bool = True
    lifecycle_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    lifecycle_review_id: str = ""
    lifecycle_version: str = "2.0.6"
    review_period: str = ""
    input_candidate_snapshot: List[str] = field(default_factory=list)
    watchlist_rotation_snapshot: List[str] = field(default_factory=list)
    setup_aging_snapshot: List[str] = field(default_factory=list)
    lifecycle_action_queue: List[LifecycleAction] = field(default_factory=list)
    cooldown_queue: List[CandidateLifecycleItem] = field(default_factory=list)
    stale_setup_queue: List[CandidateLifecycleItem] = field(default_factory=list)
    expired_candidate_queue: List[CandidateLifecycleItem] = field(default_factory=list)
    rescore_queue: List[CandidateLifecycleItem] = field(default_factory=list)
    human_review_queue: List[CandidateLifecycleItem] = field(default_factory=list)
    lifecycle_summary: Optional[LifecycleSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class LifecycleExportResult:
    """Export result for a lifecycle review. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    lifecycle_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True


@dataclass
class LifecycleAuditSnapshot:
    """Audit snapshot for a lifecycle review. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    lifecycle_review_id: str = ""
    run_metadata: str = ""
    input_snapshot: str = ""
    cooldown_snapshot: str = ""
    stale_snapshot: str = ""
    expired_snapshot: str = ""
    rescore_snapshot: str = ""
    human_review_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class LifecycleReport:
    """Markdown report for a lifecycle review. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    lifecycle_review_id: str = ""
    review_period: str = ""
    report_content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class StaleSetupCSV:
    """CSV export of the stale setup queue. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    lifecycle_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ExpiredCandidateCSV:
    """CSV export of the expired candidate queue. v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    no_real_orders: bool = True
    lifecycle_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V206HealthSummary:
    """Health summary for v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.6"


@dataclass
class V206ReleaseSummary:
    """Release summary for v2.0.6."""
    schema_version: str = "206"
    paper_only: bool = True
    version: str = "2.0.6"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 13
    cli_count: int = 11
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V206: List[str] = [
    "CandidateLifecycleItem",
    "SetupAgingPolicy",
    "LifecycleAction",
    "LifecycleSummary",
    "LifecycleReviewInput",
    "LifecycleReviewResult",
    "LifecycleExportResult",
    "LifecycleAuditSnapshot",
    "LifecycleReport",
    "StaleSetupCSV",
    "ExpiredCandidateCSV",
    "V206HealthSummary",
    "V206ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V206) == 13


# ---------------------------------------------------------------------------
# Aging bucket classification
# ---------------------------------------------------------------------------

def classify_aging_bucket(days: int, fresh_max: int = 5, normal_max: int = 14, aging_max: int = 30, stale_max: int = 60) -> str:
    """Classify days into an aging bucket. Paper only."""
    if days <= fresh_max:
        return "fresh"
    if days <= normal_max:
        return "normal"
    if days <= aging_max:
        return "aging"
    if days <= stale_max:
        return "stale"
    return "expired"


def classify_setup_age_bucket(item: CandidateLifecycleItem, policy: SetupAgingPolicy) -> str:
    """Classify setup age bucket for a candidate item. Paper only."""
    return classify_aging_bucket(
        item.days_in_candidate_pool,
        fresh_max=5,
        normal_max=14,
        aging_max=policy.max_days_waiting_buy_point // 2,
        stale_max=policy.max_days_waiting_buy_point,
    )


def classify_signal_age_bucket(item: CandidateLifecycleItem, policy: SetupAgingPolicy) -> str:
    """Classify signal age bucket for a candidate item. Paper only."""
    return classify_aging_bucket(
        item.days_since_last_signal,
        fresh_max=3,
        normal_max=7,
        aging_max=policy.max_days_without_signal_refresh // 2,
        stale_max=policy.max_days_without_signal_refresh,
    )


def classify_theme_age_bucket(item: CandidateLifecycleItem, policy: SetupAgingPolicy) -> str:
    """Classify theme age bucket for a candidate item. Paper only."""
    return classify_aging_bucket(
        item.days_since_last_score_update,
        fresh_max=3,
        normal_max=7,
        aging_max=policy.max_days_without_score_update // 2,
        stale_max=policy.max_days_without_score_update,
    )


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------

def _make_review_id(review_period: str, item_count: int) -> str:
    raw = f"lifecycle-{review_period}-{item_count}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _default_policy() -> SetupAgingPolicy:
    return SetupAgingPolicy()


def _evaluate_item_lifecycle(
    item: CandidateLifecycleItem,
    policy: SetupAgingPolicy,
) -> LifecycleAction:
    """Evaluate lifecycle action for one candidate item. Paper only."""
    action_id = f"LC-{item.symbol}-{item.days_in_candidate_pool}"

    # Update age buckets
    item.setup_age_bucket = classify_setup_age_bucket(item, policy)
    item.signal_age_bucket = classify_signal_age_bucket(item, policy)
    item.theme_age_bucket = classify_theme_age_bucket(item, policy)

    # Determine action type
    age_score = max(0.0, 100.0 - (item.days_in_candidate_pool * 1.5))
    reason_codes: List[str] = []
    requires_human_review = bool(item.human_review_reasons)

    if item.current_lifecycle_state == "expired_candidate" or item.days_in_candidate_pool > policy.max_days_active_candidate:
        action_type = "remove_from_candidate_pool"
        to_state = "removed_from_pool"
        reason_codes.append("max_days_exceeded")
        if policy.require_human_review_before_remove:
            action_type = "require_human_review"
            to_state = "human_review_required"
            requires_human_review = True
    elif item.setup_age_bucket == "expired" or item.signal_age_bucket == "expired":
        action_type = "remove_from_candidate_pool"
        to_state = "removed_from_pool"
        reason_codes.append("signal_expired")
        if policy.require_human_review_before_remove:
            action_type = "require_human_review"
            to_state = "human_review_required"
            requires_human_review = True
    elif item.current_lifecycle_state in ("stale_setup",) or item.setup_age_bucket == "stale":
        action_type = "require_rescore"
        to_state = "rescore_required"
        reason_codes.append("stale_setup_detected")
    elif item.human_review_reasons:
        action_type = "require_human_review"
        to_state = "human_review_required"
        requires_human_review = True
    elif item.current_lifecycle_state == "cooling_down":
        action_type = "move_to_cooldown"
        to_state = "cooling_down"
        reason_codes.append("in_cooldown")
    elif item.setup_age_bucket == "aging" or item.signal_age_bucket == "aging":
        action_type = "mark_stale"
        to_state = "stale_setup"
        reason_codes.append("aging_detected")
    elif item.downgrade_reasons:
        action_type = "downgrade_to_watchlist"
        to_state = "downgraded_to_watchlist"
        reason_codes.extend(item.downgrade_reasons[:2])
    elif item.current_lifecycle_state in ("waiting_buy_point", "second_wave_waiting",
                                           "abc_pullback_waiting", "breakout_waiting"):
        action_type = "keep_waiting"
        to_state = item.current_lifecycle_state
        reason_codes.append("waiting_for_entry")
    else:
        action_type = "keep_active"
        to_state = item.current_lifecycle_state
        reason_codes.append("candidate_active")

    item.next_lifecycle_action = action_type

    return LifecycleAction(
        action_id=action_id,
        symbol=item.symbol,
        from_state=item.current_lifecycle_state,
        to_state=to_state,
        action_type=action_type,
        action_reason_codes=reason_codes,
        age_score=round(age_score, 2),
        current_score=round(max(0.0, 100.0 - len(item.stale_reasons) * 10.0), 2),
        risk_score=round(50.0 + len(item.downgrade_reasons) * (-5.0), 2),
        setup_quality_score=round(max(0.0, 80.0 - item.days_in_candidate_pool * 0.5), 2),
        confidence_score=round(max(0.0, 100.0 - item.days_since_last_signal * 3.0), 2),
        requires_human_review=requires_human_review,
        should_auto_apply=False,
    )


def _build_lifecycle_summary(
    action_queue: List[LifecycleAction],
    cooldown_queue: List[CandidateLifecycleItem],
    stale_queue: List[CandidateLifecycleItem],
    expired_queue: List[CandidateLifecycleItem],
    rescore_queue: List[CandidateLifecycleItem],
    human_review_queue: List[CandidateLifecycleItem],
    all_items: List[CandidateLifecycleItem],
) -> LifecycleSummary:
    """Build lifecycle summary from review output. Paper only."""
    active_states = {"newly_promoted", "active_candidate"}
    waiting_states = {"waiting_buy_point", "second_wave_waiting", "abc_pullback_waiting", "breakout_waiting"}

    active_count = sum(1 for it in all_items if it.current_lifecycle_state in active_states)
    waiting_count = sum(1 for it in all_items if it.current_lifecycle_state in waiting_states)
    cooling_down_count = sum(1 for it in all_items if it.current_lifecycle_state == "cooling_down")
    stale_count = len(stale_queue)
    expired_count = len(expired_queue)
    rescore_count = len(rescore_queue)
    downgrade_count = sum(1 for a in action_queue if a.action_type == "downgrade_to_watchlist")
    remove_count = sum(1 for a in action_queue if a.action_type == "remove_from_candidate_pool")
    hr_count = len(human_review_queue)

    total = len(all_items)
    avg_days_pool = sum(it.days_in_candidate_pool for it in all_items) / max(1, total)
    avg_days_signal = sum(it.days_since_last_signal for it in all_items) / max(1, total)

    all_stale_reasons: List[str] = []
    for it in stale_queue:
        all_stale_reasons.extend(it.stale_reasons[:2])
    top_stale = list(dict.fromkeys(all_stale_reasons))[:3]

    all_remove_reasons: List[str] = []
    for it in expired_queue:
        all_remove_reasons.extend(it.remove_reasons[:2])
    top_remove = list(dict.fromkeys(all_remove_reasons))[:3]

    avg_age = avg_days_pool
    grade = "A" if avg_age <= 10 else "B" if avg_age <= 20 else "C" if avg_age <= 35 else "D"

    return LifecycleSummary(
        total_candidate_count=total,
        active_count=active_count,
        waiting_count=waiting_count,
        cooling_down_count=cooling_down_count,
        stale_count=stale_count,
        expired_count=expired_count,
        rescore_required_count=rescore_count,
        downgrade_count=downgrade_count,
        remove_count=remove_count,
        human_review_count=hr_count,
        avg_days_in_candidate_pool=round(avg_days_pool, 2),
        avg_days_since_last_signal=round(avg_days_signal, 2),
        top_stale_reasons=top_stale,
        top_remove_reasons=top_remove,
        lifecycle_quality_grade=grade,
    )


def run_lifecycle_review(
    review_input: Optional[LifecycleReviewInput] = None,
) -> LifecycleReviewResult:
    """Run a paper candidate lifecycle review. Paper only."""
    if review_input is None:
        review_input = LifecycleReviewInput(
            review_period="2026-W29",
            candidate_items=[
                CandidateLifecycleItem(
                    symbol="2330",
                    name="台積電",
                    candidate_id="CAND-2330-001",
                    current_lifecycle_state="active_candidate",
                    previous_lifecycle_state="newly_promoted",
                    days_in_candidate_pool=5,
                    days_since_last_signal=2,
                    days_since_last_score_update=3,
                    setup_type="breakout",
                ),
                CandidateLifecycleItem(
                    symbol="2317",
                    name="鴻海",
                    candidate_id="CAND-2317-001",
                    current_lifecycle_state="waiting_buy_point",
                    previous_lifecycle_state="active_candidate",
                    days_in_candidate_pool=25,
                    days_since_last_signal=10,
                    days_since_last_score_update=15,
                    setup_type="abc_pullback",
                    stale_reasons=["no_recent_volume_signal"],
                ),
            ],
        )

    if review_input.aging_policy is None:
        policy = _default_policy()
    else:
        policy = review_input.aging_policy

    review_id = _make_review_id(review_input.review_period, len(review_input.candidate_items))

    action_queue: List[LifecycleAction] = []
    cooldown_queue: List[CandidateLifecycleItem] = []
    stale_setup_queue: List[CandidateLifecycleItem] = []
    expired_candidate_queue: List[CandidateLifecycleItem] = []
    rescore_queue: List[CandidateLifecycleItem] = []
    human_review_queue: List[CandidateLifecycleItem] = []

    for item in review_input.candidate_items:
        action = _evaluate_item_lifecycle(item, policy)
        action_queue.append(action)

        atype = action.action_type
        if atype == "move_to_cooldown":
            cooldown_queue.append(item)
        elif atype == "mark_stale":
            stale_setup_queue.append(item)
        elif atype == "remove_from_candidate_pool":
            expired_candidate_queue.append(item)
        elif atype == "require_rescore":
            rescore_queue.append(item)
        elif atype == "require_human_review":
            human_review_queue.append(item)

    summary = _build_lifecycle_summary(
        action_queue, cooldown_queue, stale_setup_queue,
        expired_candidate_queue, rescore_queue, human_review_queue,
        review_input.candidate_items,
    )

    return LifecycleReviewResult(
        lifecycle_review_id=review_id,
        review_period=review_input.review_period,
        input_candidate_snapshot=[it.symbol for it in review_input.candidate_items],
        watchlist_rotation_snapshot=list(review_input.watchlist_rotation_ids),
        setup_aging_snapshot=[it.setup_age_bucket for it in review_input.candidate_items],
        lifecycle_action_queue=action_queue,
        cooldown_queue=cooldown_queue,
        stale_setup_queue=stale_setup_queue,
        expired_candidate_queue=expired_candidate_queue,
        rescore_queue=rescore_queue,
        human_review_queue=human_review_queue,
        lifecycle_summary=summary,
        all_passed=True,
    )


def build_stale_queue(
    review_input: Optional[LifecycleReviewInput] = None,
) -> List[CandidateLifecycleItem]:
    """Build only the stale setup queue. Paper only."""
    return run_lifecycle_review(review_input).stale_setup_queue


def build_expired_queue(
    review_input: Optional[LifecycleReviewInput] = None,
) -> List[CandidateLifecycleItem]:
    """Build only the expired candidate queue. Paper only."""
    return run_lifecycle_review(review_input).expired_candidate_queue


def build_rescore_queue(
    review_input: Optional[LifecycleReviewInput] = None,
) -> List[CandidateLifecycleItem]:
    """Build only the rescore queue. Paper only."""
    return run_lifecycle_review(review_input).rescore_queue


def build_cooldown_queue(
    review_input: Optional[LifecycleReviewInput] = None,
) -> List[CandidateLifecycleItem]:
    """Build only the cooldown queue. Paper only."""
    return run_lifecycle_review(review_input).cooldown_queue


def build_human_review_queue(
    review_input: Optional[LifecycleReviewInput] = None,
) -> List[CandidateLifecycleItem]:
    """Build only the human review queue. Paper only."""
    return run_lifecycle_review(review_input).human_review_queue


def evaluate_aging(
    review_input: Optional[LifecycleReviewInput] = None,
) -> List[LifecycleAction]:
    """Evaluate aging for all candidate items. Paper only."""
    return run_lifecycle_review(review_input).lifecycle_action_queue


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_lifecycle_json(result: LifecycleReviewResult) -> LifecycleExportResult:
    """Export lifecycle review as JSON. Paper only."""
    rid = result.lifecycle_review_id
    parts = [
        f'{{"lifecycle_review_id": "{rid}", "lifecycle_version": "{result.lifecycle_version}",',
        f'"review_period": "{result.review_period}", "paper_only": true,',
        f'"should_auto_apply": false, "no_real_orders": true,',
        f'"action_queue_count": {len(result.lifecycle_action_queue)},',
        f'"cooldown_count": {len(result.cooldown_queue)},',
        f'"stale_count": {len(result.stale_setup_queue)},',
        f'"expired_count": {len(result.expired_candidate_queue)},',
        f'"rescore_count": {len(result.rescore_queue)},',
        f'"human_review_count": {len(result.human_review_queue)}}}',
    ]
    return LifecycleExportResult(
        lifecycle_review_id=rid,
        export_format="json",
        content="".join(parts),
        is_valid=True,
        export_status="complete",
    )


def export_lifecycle_markdown(result: LifecycleReviewResult) -> LifecycleExportResult:
    """Export lifecycle review as Markdown. Paper only."""
    rid = result.lifecycle_review_id
    lines = [
        f"# Candidate Lifecycle Report v2.0.6",
        f"",
        f"**lifecycle_review_id**: {rid}",
        f"**lifecycle_version**: {result.lifecycle_version}",
        f"**review_period**: {result.review_period}",
        f"**paper_only**: True",
        f"**should_auto_apply**: False",
        f"**no_real_orders**: True",
        f"",
        f"## Lifecycle Summary",
        f"",
        f"- Action Queue: {len(result.lifecycle_action_queue)}",
        f"- Cooldown: {len(result.cooldown_queue)}",
        f"- Stale Setup: {len(result.stale_setup_queue)}",
        f"- Expired: {len(result.expired_candidate_queue)}",
        f"- Rescore Required: {len(result.rescore_queue)}",
        f"- Human Review: {len(result.human_review_queue)}",
        f"",
        f"## Lifecycle Action Queue",
        f"",
    ]
    for act in result.lifecycle_action_queue:
        lines.append(f"- {act.symbol}: {act.from_state} → {act.to_state} ({act.action_type})")
    lines.append("")
    lines.append(f"---")
    lines.append(f"[!] Paper Only | No Real Orders | Not Investment Advice")
    return LifecycleExportResult(
        lifecycle_review_id=rid,
        export_format="markdown",
        content="\n".join(lines),
        is_valid=True,
        export_status="complete",
    )


def export_stale_setup_csv(result: LifecycleReviewResult) -> StaleSetupCSV:
    """Export stale setup queue as CSV. Paper only."""
    rows = ["symbol,current_lifecycle_state,days_in_candidate_pool,setup_age_bucket,should_auto_apply"]
    for it in result.stale_setup_queue:
        rows.append(f"{it.symbol},{it.current_lifecycle_state},{it.days_in_candidate_pool},{it.setup_age_bucket},False")
    return StaleSetupCSV(
        lifecycle_review_id=result.lifecycle_review_id,
        csv_content="\n".join(rows),
        row_count=len(result.stale_setup_queue),
        is_valid=True,
    )


def export_expired_candidate_csv(result: LifecycleReviewResult) -> ExpiredCandidateCSV:
    """Export expired candidate queue as CSV. Paper only."""
    rows = ["symbol,current_lifecycle_state,days_in_candidate_pool,signal_age_bucket,should_auto_apply"]
    for it in result.expired_candidate_queue:
        rows.append(f"{it.symbol},{it.current_lifecycle_state},{it.days_in_candidate_pool},{it.signal_age_bucket},False")
    return ExpiredCandidateCSV(
        lifecycle_review_id=result.lifecycle_review_id,
        csv_content="\n".join(rows),
        row_count=len(result.expired_candidate_queue),
        is_valid=True,
    )


def export_lifecycle_action_csv(result: LifecycleReviewResult) -> LifecycleExportResult:
    """Export lifecycle action queue as CSV. Paper only."""
    rows = ["symbol,from_state,to_state,action_type,age_score,should_auto_apply"]
    for act in result.lifecycle_action_queue:
        rows.append(f"{act.symbol},{act.from_state},{act.to_state},{act.action_type},{act.age_score},False")
    return LifecycleExportResult(
        lifecycle_review_id=result.lifecycle_review_id,
        export_format="csv",
        content="\n".join(rows),
        is_valid=True,
        export_status="complete",
    )


def export_lifecycle_audit_snapshot(result: LifecycleReviewResult) -> LifecycleAuditSnapshot:
    """Build lifecycle audit snapshot. Paper only."""
    rid = result.lifecycle_review_id
    raw = f"{rid}-{result.review_period}-{len(result.lifecycle_action_queue)}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return LifecycleAuditSnapshot(
        lifecycle_review_id=rid,
        run_metadata=f"v2.0.6-lifecycle-{rid}",
        input_snapshot=str(result.input_candidate_snapshot),
        cooldown_snapshot=str([it.symbol for it in result.cooldown_queue]),
        stale_snapshot=str([it.symbol for it in result.stale_setup_queue]),
        expired_snapshot=str([it.symbol for it in result.expired_candidate_queue]),
        rescore_snapshot=str([it.symbol for it in result.rescore_queue]),
        human_review_snapshot=str([it.symbol for it in result.human_review_queue]),
        safety_snapshot="paper_only=True;no_real_orders=True;should_auto_apply=False;auto_apply_enabled=False",
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
    }


def verify_version() -> bool:
    """Verify version constants are correct. Paper only."""
    return VERSION == "2.0.6" and SCHEMA_VERSION == "206"


def get_cockpit_summary_v206() -> Dict[str, Any]:
    """Return cockpit summary for v2.0.6. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "models_count": len(_ALL_MODEL_NAMES_V206),
        "cli_commands_count": len(CLI_COMMANDS_V206),
        "gui_tabs_count": len(GUI_TABS_V206),
        "safety_flags_count": len(SAFETY_FLAGS_V206),
        "lifecycle_states_count": len(LIFECYCLE_STATES),
        "aging_buckets_count": len(AGING_BUCKETS),
        "action_types_count": len(ACTION_TYPES),
    }
