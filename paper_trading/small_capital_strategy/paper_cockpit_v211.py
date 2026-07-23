"""
paper_trading/small_capital_strategy/paper_cockpit_v211.py
v2.0.11 Paper Trade Journal & Execution Discipline Review
[!] Paper Only. Research Only. Journal Review Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. No Automatic Journal Apply. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.11"
SCHEMA_VERSION = "211"
RELEASE_NAME = "Paper Trade Journal & Execution Discipline Review"
BASELINE_TESTS = 35613
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

EXECUTION_ACTIONS: List[str] = [
    "compliant",
    "monitor",
    "require_journal_note",
    "require_rescore",
    "flag_discipline_warning",
    "block_followup_action",
    "human_review_required",
]

TRADE_STATUSES: List[str] = [
    "planned_only",
    "entered",
    "reduced",
    "exited",
    "stopped_out",
    "take_profit_done",
    "invalidated",
    "cancelled",
]

VIOLATION_CODES: List[str] = [
    "ENTRY_SLIPPAGE_EXCESS",
    "SIZE_DEVIATION_EXCESS",
    "STOP_DEVIATION_EXCESS",
    "MISSING_EXIT_PLAN",
    "UNPLANNED_ADD",
    "OVERTRADE",
    "STOP_LOSS_VIOLATION",
    "NO_PLANNED_ENTRY",
]

MISTAKE_TAGS: List[str] = [
    "chasing_price",
    "position_oversized",
    "position_undersized",
    "stop_too_loose",
    "stop_moved_away",
    "unplanned_addon",
    "overtrading",
    "missing_journal_entry",
    "plan_not_followed",
]

JOURNAL_REVIEW_FIELDS: List[str] = [
    "journal_review_id",
    "journal_version",
    "review_period",
    "trade_journal_snapshot",
    "execution_discipline_snapshot",
    "plan_adherence_snapshot",
    "mistake_review_queue",
    "rule_violation_queue",
    "improvement_suggestion_queue",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

TRADE_JOURNAL_POLICY_FIELDS: List[str] = [
    "policy_id",
    "require_planned_entry_before_trade",
    "require_position_size_match",
    "require_exit_plan_match",
    "max_allowed_entry_slippage_pct",
    "max_allowed_size_deviation_pct",
    "max_allowed_stop_deviation_pct",
    "max_allowed_unplanned_add_count",
    "max_allowed_overtrade_count",
    "min_discipline_score",
    "auto_apply_enabled",
]

JOURNAL_ENTRY_FIELDS: List[str] = [
    "journal_entry_id",
    "symbol",
    "name",
    "candidate_id",
    "theme_id",
    "sector_id",
    "planned_entry_price",
    "actual_entry_price",
    "planned_position_size",
    "actual_position_size",
    "planned_stop_price",
    "actual_stop_price",
    "planned_exit_price",
    "actual_exit_price",
    "planned_exit_action",
    "actual_exit_action",
    "entry_slippage_pct",
    "size_deviation_pct",
    "stop_deviation_pct",
    "reward_risk_at_entry",
    "trade_status",
    "execution_action",
    "violation_codes",
    "mistake_tags",
    "requires_human_review",
    "should_auto_apply",
]

EXECUTION_DISCIPLINE_SUMMARY_FIELDS: List[str] = [
    "total_journal_entries",
    "compliant_entry_count",
    "entry_slippage_violation_count",
    "size_deviation_violation_count",
    "stop_deviation_violation_count",
    "missing_exit_plan_count",
    "unplanned_add_count",
    "overtrade_count",
    "stop_loss_violation_count",
    "human_review_count",
    "average_discipline_score",
    "lowest_discipline_symbols",
    "top_mistake_tags",
    "top_violation_codes",
    "discipline_quality_grade",
    "plan_adherence_grade",
]

CLI_COMMANDS_V211: List[str] = [
    "paper-cockpit-v211-review-journal",
    "paper-cockpit-v211-evaluate-discipline",
    "paper-cockpit-v211-build-mistake-queue",
    "paper-cockpit-v211-build-violation-queue",
    "paper-cockpit-v211-build-improvement-queue",
    "paper-cockpit-v211-export-json",
    "paper-cockpit-v211-export-md",
    "paper-cockpit-v211-export-csv",
    "paper-cockpit-v211-health",
    "paper-cockpit-v211-gate",
]

GUI_TABS_V211: List[str] = [
    "trade_journal_v211",
    "execution_discipline_v211",
    "mistake_review_queue_v211",
]

SAFETY_FLAGS_V211: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "journal_review_recommendation_only": True,
    "journal_actions_recommendation_only": True,
    "validation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_write": True,
    "no_real_account_sync": True,
    "no_automatic_rebalance": True,
    "no_live_strategy_activation": True,
    "no_automatic_journal_apply": True,
    "no_automatic_stop_loss_execution": True,
    "no_automatic_take_profit_execution": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "should_auto_apply_always_false": True,
    "auto_apply_enabled_always_false": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
    "require_planned_entry_before_trade_always_true": True,
    "journal_actions_paper_only": True,
}

assert len(SAFETY_FLAGS_V211) == 24, f"Expected 24 SAFETY_FLAGS_V211, got {len(SAFETY_FLAGS_V211)}"
assert len(EXECUTION_ACTIONS) == 7
assert len(TRADE_STATUSES) == 8
assert len(VIOLATION_CODES) == 8
assert len(MISTAKE_TAGS) == 9
assert len(CLI_COMMANDS_V211) == 10
assert len(GUI_TABS_V211) == 3
assert len(JOURNAL_REVIEW_FIELDS) == 11
assert len(TRADE_JOURNAL_POLICY_FIELDS) == 11
assert len(JOURNAL_ENTRY_FIELDS) == 26
assert len(EXECUTION_DISCIPLINE_SUMMARY_FIELDS) == 16

COVERED_VERSIONS: List[str] = [
    "2.0.10", "2.0.9", "2.0.8", "2.0.7", "2.0.6", "2.0.5", "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]

_ALL_MODEL_NAMES_V211: List[str] = [
    "TradeJournalPolicy",
    "JournalEntry",
    "ExecutionDisciplineSummary",
    "JournalReviewInput",
    "JournalReviewResult",
    "JournalExportResult",
    "JournalAuditSnapshot",
    "JournalMarkdownReport",
    "JournalCSV",
    "ExecutionDisciplineCSV",
    "MistakeReviewCSV",
    "ViolationQueueCSV",
    "V211HealthSummary",
    "V211ReleaseSummary",
    "JournalSafetyGuard",
]
assert len(_ALL_MODEL_NAMES_V211) == 15


# ---------------------------------------------------------------------------
# Dataclasses — 15 models, schema_version="211"
# ---------------------------------------------------------------------------

@dataclass
class TradeJournalPolicy:
    """Trade journal policy schema. v2.0.11. auto_apply_enabled is always False.
    require_planned_entry_before_trade is always True."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    policy_id: str = ""
    require_planned_entry_before_trade: bool = True   # ALWAYS True
    require_position_size_match: bool = True
    require_exit_plan_match: bool = True
    max_allowed_entry_slippage_pct: float = 0.02
    max_allowed_size_deviation_pct: float = 0.10
    max_allowed_stop_deviation_pct: float = 0.05
    max_allowed_unplanned_add_count: int = 0
    max_allowed_overtrade_count: int = 2
    min_discipline_score: float = 70.0
    auto_apply_enabled: bool = False                 # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "auto_apply_enabled", False)
        object.__setattr__(self, "require_planned_entry_before_trade", True)


@dataclass
class JournalEntry:
    """Paper trade journal entry schema. v2.0.11. should_auto_apply is always False."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_entry_id: str = ""
    symbol: str = ""
    name: str = ""
    candidate_id: str = ""
    theme_id: str = ""
    sector_id: str = ""
    planned_entry_price: float = 0.0
    actual_entry_price: float = 0.0
    planned_position_size: int = 0
    actual_position_size: int = 0
    planned_stop_price: float = 0.0
    actual_stop_price: float = 0.0
    planned_exit_price: float = 0.0
    actual_exit_price: float = 0.0
    planned_exit_action: str = "allow_with_exit_plan"
    actual_exit_action: str = "compliant"
    entry_slippage_pct: float = 0.0
    size_deviation_pct: float = 0.0
    stop_deviation_pct: float = 0.0
    reward_risk_at_entry: float = 0.0
    trade_status: str = "planned_only"
    execution_action: str = "compliant"
    violation_codes: List[str] = field(default_factory=list)
    mistake_tags: List[str] = field(default_factory=list)
    requires_human_review: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ExecutionDisciplineSummary:
    """Execution discipline summary. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    total_journal_entries: int = 0
    compliant_entry_count: int = 0
    entry_slippage_violation_count: int = 0
    size_deviation_violation_count: int = 0
    stop_deviation_violation_count: int = 0
    missing_exit_plan_count: int = 0
    unplanned_add_count: int = 0
    overtrade_count: int = 0
    stop_loss_violation_count: int = 0
    human_review_count: int = 0
    average_discipline_score: float = 0.0
    lowest_discipline_symbols: List[str] = field(default_factory=list)
    top_mistake_tags: List[str] = field(default_factory=list)
    top_violation_codes: List[str] = field(default_factory=list)
    discipline_quality_grade: str = "B"
    plan_adherence_grade: str = "B"


@dataclass
class JournalReviewInput:
    """Input for journal review. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    review_period: str = ""
    journal_entries: List[Dict[str, Any]] = field(default_factory=list)
    journal_policy: Optional[TradeJournalPolicy] = None
    market_state: str = "range_bound"


@dataclass
class JournalReviewResult:
    """Journal review result. v2.0.11. should_auto_apply is always False."""
    schema_version: str = "211"
    paper_only: bool = True
    research_only: bool = True
    journal_review_recommendation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    journal_review_id: str = ""
    journal_version: str = "2.0.11"
    review_period: str = ""
    journal_policy: Optional[TradeJournalPolicy] = None
    trade_journal_snapshot: List[JournalEntry] = field(default_factory=list)
    execution_discipline_snapshot: Optional[ExecutionDisciplineSummary] = None
    plan_adherence_snapshot: List[Dict[str, Any]] = field(default_factory=list)
    mistake_review_queue: List[JournalEntry] = field(default_factory=list)
    rule_violation_queue: List[JournalEntry] = field(default_factory=list)
    improvement_suggestion_queue: List[Dict[str, Any]] = field(default_factory=list)
    human_review_queue: List[JournalEntry] = field(default_factory=list)
    paper_only_safety_snapshot: bool = True
    all_passed: bool = True
    should_auto_apply: bool = False   # ALWAYS False
    auto_apply_enabled: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)
        object.__setattr__(self, "auto_apply_enabled", False)


@dataclass
class JournalExportResult:
    """Export result for journal review. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False


@dataclass
class JournalAuditSnapshot:
    """Audit snapshot for journal review. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    journal_review_id: str = ""
    run_metadata: str = ""
    trade_journal_snapshot: str = ""
    execution_discipline_snapshot: str = ""
    plan_adherence_snapshot: str = ""
    mistake_review_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class JournalMarkdownReport:
    """Markdown report for journal review. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_review_id: str = ""
    review_period: str = ""
    content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class JournalCSV:
    """CSV export of trade journal entries. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ExecutionDisciplineCSV:
    """CSV export of execution discipline summary. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class MistakeReviewCSV:
    """CSV export of mistake review queue. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class ViolationQueueCSV:
    """CSV export of rule violation queue. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    journal_review_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V211HealthSummary:
    """Health summary for v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.11"


@dataclass
class V211ReleaseSummary:
    """Release summary for v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    version: str = "2.0.11"
    release_name: str = RELEASE_NAME


@dataclass
class JournalSafetyGuard:
    """Safety guard snapshot for trade journal. v2.0.11."""
    schema_version: str = "211"
    paper_only: bool = True
    no_real_orders: bool = True
    no_automatic_journal_apply: bool = True
    no_automatic_stop_loss_execution: bool = True
    no_automatic_take_profit_execution: bool = True
    should_auto_apply: bool = False
    auto_apply_enabled: bool = False
    require_planned_entry_before_trade: bool = True
    journal_actions_recommendation_only: bool = True


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def _make_journal_review_id(review_period: str, entry_count: int) -> str:
    raw = f"v211-{review_period}-n{entry_count}"
    return hashlib.sha256(raw.encode()).hexdigest()[:10]


def _calc_entry_slippage_pct(planned: float, actual: float) -> float:
    if planned <= 0 or actual <= 0:
        return 0.0
    return abs(actual - planned) / planned


def _calc_size_deviation_pct(planned: int, actual: int) -> float:
    if planned <= 0 or actual <= 0:
        return 0.0
    return abs(actual - planned) / planned


def _calc_stop_deviation_pct(planned: float, actual: float) -> float:
    if planned <= 0 or actual <= 0:
        return 0.0
    return abs(actual - planned) / planned


def _calc_discipline_score(
    entry_slippage_pct: float,
    size_deviation_pct: float,
    stop_deviation_pct: float,
    has_exit_plan: bool,
    is_unplanned_add: bool,
    is_overtrade: bool,
    stop_loss_violated: bool,
    has_planned_entry: bool,
    policy: TradeJournalPolicy,
) -> float:
    """Calculate discipline score (0-100) for a single journal entry."""
    score = 100.0
    if not has_planned_entry:
        score -= 20.0
    if entry_slippage_pct > policy.max_allowed_entry_slippage_pct:
        score -= 10.0
    if size_deviation_pct > policy.max_allowed_size_deviation_pct:
        score -= 10.0
    if stop_deviation_pct > policy.max_allowed_stop_deviation_pct:
        score -= 10.0
    if not has_exit_plan:
        score -= 15.0
    if is_unplanned_add:
        score -= 5.0
    if is_overtrade:
        score -= 5.0
    if stop_loss_violated:
        score -= 15.0
    return max(0.0, score)


def _classify_execution_action(
    discipline_score: float,
    violation_codes: List[str],
    policy: TradeJournalPolicy,
) -> str:
    """Classify execution action based on discipline score and violations."""
    if "NO_PLANNED_ENTRY" in violation_codes:
        return "human_review_required"
    if discipline_score < 50.0:
        return "block_followup_action"
    if "STOP_LOSS_VIOLATION" in violation_codes or "MISSING_EXIT_PLAN" in violation_codes:
        return "flag_discipline_warning"
    if discipline_score < policy.min_discipline_score:
        return "require_rescore"
    if violation_codes:
        return "require_journal_note"
    if discipline_score < 85.0:
        return "monitor"
    return "compliant"


def _detect_violations(
    planned_entry_price: float,
    actual_entry_price: float,
    planned_position_size: int,
    actual_position_size: int,
    planned_stop_price: float,
    actual_stop_price: float,
    planned_exit_price: float,
    is_unplanned_add: bool,
    is_overtrade: bool,
    stop_loss_violated: bool,
    policy: TradeJournalPolicy,
) -> List[str]:
    """Detect and return list of violation codes."""
    codes: List[str] = []
    if planned_entry_price <= 0:
        codes.append("NO_PLANNED_ENTRY")
        return codes
    slippage = _calc_entry_slippage_pct(planned_entry_price, actual_entry_price)
    if slippage > policy.max_allowed_entry_slippage_pct:
        codes.append("ENTRY_SLIPPAGE_EXCESS")
    size_dev = _calc_size_deviation_pct(planned_position_size, actual_position_size)
    if size_dev > policy.max_allowed_size_deviation_pct:
        codes.append("SIZE_DEVIATION_EXCESS")
    stop_dev = _calc_stop_deviation_pct(planned_stop_price, actual_stop_price)
    if stop_dev > policy.max_allowed_stop_deviation_pct:
        codes.append("STOP_DEVIATION_EXCESS")
    if planned_exit_price <= 0:
        codes.append("MISSING_EXIT_PLAN")
    if is_unplanned_add:
        codes.append("UNPLANNED_ADD")
    if is_overtrade:
        codes.append("OVERTRADE")
    if stop_loss_violated:
        codes.append("STOP_LOSS_VIOLATION")
    return codes


def _detect_mistake_tags(violation_codes: List[str], entry_slippage_pct: float) -> List[str]:
    """Detect mistake tags from violation codes."""
    tags: List[str] = []
    if "ENTRY_SLIPPAGE_EXCESS" in violation_codes and entry_slippage_pct > 0.03:
        tags.append("chasing_price")
    if "SIZE_DEVIATION_EXCESS" in violation_codes:
        tags.append("position_oversized")
    if "STOP_DEVIATION_EXCESS" in violation_codes:
        tags.append("stop_too_loose")
    if "MISSING_EXIT_PLAN" in violation_codes:
        tags.append("plan_not_followed")
    if "UNPLANNED_ADD" in violation_codes:
        tags.append("unplanned_addon")
    if "OVERTRADE" in violation_codes:
        tags.append("overtrading")
    if "STOP_LOSS_VIOLATION" in violation_codes:
        tags.append("stop_moved_away")
    if "NO_PLANNED_ENTRY" in violation_codes:
        tags.append("missing_journal_entry")
    return tags


def _grade_discipline(avg_score: float) -> str:
    if avg_score >= 90.0:
        return "A"
    if avg_score >= 75.0:
        return "B"
    if avg_score >= 50.0:
        return "C"
    return "D"


def _grade_plan_adherence(compliant_count: int, total_count: int) -> str:
    if total_count == 0:
        return "N/A"
    ratio = compliant_count / total_count
    if ratio >= 0.90:
        return "A"
    if ratio >= 0.75:
        return "B"
    if ratio >= 0.50:
        return "C"
    return "D"


# ---------------------------------------------------------------------------
# Journal entry evaluation
# ---------------------------------------------------------------------------

def evaluate_journal_entry(
    journal_entry_id: str,
    symbol: str,
    name: str,
    candidate_id: str,
    theme_id: str,
    sector_id: str,
    planned_entry_price: float,
    actual_entry_price: float,
    planned_position_size: int,
    actual_position_size: int,
    planned_stop_price: float,
    actual_stop_price: float,
    planned_exit_price: float,
    actual_exit_price: float,
    planned_exit_action: str = "allow_with_exit_plan",
    trade_status: str = "entered",
    is_unplanned_add: bool = False,
    is_overtrade: bool = False,
    stop_loss_violated: bool = False,
    reward_risk_at_entry: float = 0.0,
    policy: Optional[TradeJournalPolicy] = None,
) -> JournalEntry:
    """Evaluate a paper trade journal entry. Paper only, no real orders."""
    if policy is None:
        policy = TradeJournalPolicy(policy_id="default-policy-v211")

    entry_slippage = _calc_entry_slippage_pct(planned_entry_price, actual_entry_price)
    size_dev = _calc_size_deviation_pct(planned_position_size, actual_position_size)
    stop_dev = _calc_stop_deviation_pct(planned_stop_price, actual_stop_price)
    has_exit_plan = planned_exit_price > 0
    has_planned_entry = planned_entry_price > 0

    violation_codes = _detect_violations(
        planned_entry_price=planned_entry_price,
        actual_entry_price=actual_entry_price,
        planned_position_size=planned_position_size,
        actual_position_size=actual_position_size,
        planned_stop_price=planned_stop_price,
        actual_stop_price=actual_stop_price,
        planned_exit_price=planned_exit_price,
        is_unplanned_add=is_unplanned_add,
        is_overtrade=is_overtrade,
        stop_loss_violated=stop_loss_violated,
        policy=policy,
    )

    discipline_score = _calc_discipline_score(
        entry_slippage_pct=entry_slippage,
        size_deviation_pct=size_dev,
        stop_deviation_pct=stop_dev,
        has_exit_plan=has_exit_plan,
        is_unplanned_add=is_unplanned_add,
        is_overtrade=is_overtrade,
        stop_loss_violated=stop_loss_violated,
        has_planned_entry=has_planned_entry,
        policy=policy,
    )

    execution_action = _classify_execution_action(
        discipline_score=discipline_score,
        violation_codes=violation_codes,
        policy=policy,
    )

    mistake_tags = _detect_mistake_tags(violation_codes, entry_slippage)
    requires_review = execution_action == "human_review_required"

    return JournalEntry(
        schema_version="211",
        paper_only=True,
        no_real_orders=True,
        journal_entry_id=journal_entry_id,
        symbol=symbol,
        name=name,
        candidate_id=candidate_id,
        theme_id=theme_id,
        sector_id=sector_id,
        planned_entry_price=planned_entry_price,
        actual_entry_price=actual_entry_price,
        planned_position_size=planned_position_size,
        actual_position_size=actual_position_size,
        planned_stop_price=planned_stop_price,
        actual_stop_price=actual_stop_price,
        planned_exit_price=planned_exit_price,
        actual_exit_price=actual_exit_price,
        planned_exit_action=planned_exit_action,
        actual_exit_action=execution_action,
        entry_slippage_pct=entry_slippage,
        size_deviation_pct=size_dev,
        stop_deviation_pct=stop_dev,
        reward_risk_at_entry=reward_risk_at_entry,
        trade_status=trade_status,
        execution_action=execution_action,
        violation_codes=violation_codes,
        mistake_tags=mistake_tags,
        requires_human_review=requires_review,
        should_auto_apply=False,
    )


# ---------------------------------------------------------------------------
# Journal review engine
# ---------------------------------------------------------------------------

def _default_journal_policy() -> TradeJournalPolicy:
    return TradeJournalPolicy(policy_id="default-policy-v211")


def _default_journal_entry_pool() -> List[Dict[str, Any]]:
    """Return default demo journal entry pool. Paper only."""
    return [
        {
            "journal_entry_id": "JE-2330-001", "symbol": "2330", "name": "台積電",
            "candidate_id": "CAND-2330", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH",
            "planned_entry_price": 900.0, "actual_entry_price": 901.0,
            "planned_position_size": 1000, "actual_position_size": 1000,
            "planned_stop_price": 855.0, "actual_stop_price": 855.0,
            "planned_exit_price": 945.0, "actual_exit_price": 0.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "entered",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 2.0,
        },
        {
            "journal_entry_id": "JE-2454-001", "symbol": "2454", "name": "聯發科",
            "candidate_id": "CAND-2454", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH",
            "planned_entry_price": 1000.0, "actual_entry_price": 1035.0,
            "planned_position_size": 500, "actual_position_size": 600,
            "planned_stop_price": 940.0, "actual_stop_price": 940.0,
            "planned_exit_price": 1080.0, "actual_exit_price": 0.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "entered",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 1.3,
        },
        {
            "journal_entry_id": "JE-2382-001", "symbol": "2382", "name": "廣達",
            "candidate_id": "CAND-2382", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH",
            "planned_entry_price": 300.0, "actual_entry_price": 300.0,
            "planned_position_size": 2000, "actual_position_size": 2000,
            "planned_stop_price": 282.0, "actual_stop_price": 282.0,
            "planned_exit_price": 318.0, "actual_exit_price": 315.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "exited",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 2.0,
        },
        {
            "journal_entry_id": "JE-2308-001", "symbol": "2308", "name": "台達電",
            "candidate_id": "CAND-2308", "theme_id": "THEME-EV", "sector_id": "SECTOR-ELEC",
            "planned_entry_price": 400.0, "actual_entry_price": 400.0,
            "planned_position_size": 1000, "actual_position_size": 1000,
            "planned_stop_price": 372.0, "actual_stop_price": 365.0,
            "planned_exit_price": 428.0, "actual_exit_price": 0.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "entered",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 2.0,
        },
        {
            "journal_entry_id": "JE-2317-001", "symbol": "2317", "name": "鴻海",
            "candidate_id": "CAND-2317", "theme_id": "THEME-EV", "sector_id": "SECTOR-MFGR",
            "planned_entry_price": 0.0, "actual_entry_price": 120.0,
            "planned_position_size": 0, "actual_position_size": 1000,
            "planned_stop_price": 0.0, "actual_stop_price": 110.0,
            "planned_exit_price": 0.0, "actual_exit_price": 0.0,
            "planned_exit_action": "", "trade_status": "entered",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 0.0,
        },
        {
            "journal_entry_id": "JE-3711-001", "symbol": "3711", "name": "日月光",
            "candidate_id": "CAND-3711", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH",
            "planned_entry_price": 150.0, "actual_entry_price": 150.0,
            "planned_position_size": 2000, "actual_position_size": 2000,
            "planned_stop_price": 141.0, "actual_stop_price": 141.0,
            "planned_exit_price": 159.0, "actual_exit_price": 157.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "take_profit_done",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 2.0,
        },
        {
            "journal_entry_id": "JE-2303-001", "symbol": "2303", "name": "聯電",
            "candidate_id": "CAND-2303", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH",
            "planned_entry_price": 55.0, "actual_entry_price": 55.0,
            "planned_position_size": 3000, "actual_position_size": 3000,
            "planned_stop_price": 51.0, "actual_stop_price": 51.0,
            "planned_exit_price": 59.0, "actual_exit_price": 48.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "stopped_out",
            "is_unplanned_add": False, "is_overtrade": False, "stop_loss_violated": True,
            "reward_risk_at_entry": 1.5,
        },
        {
            "journal_entry_id": "JE-6669-001", "symbol": "6669", "name": "緯穎",
            "candidate_id": "CAND-6669", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH",
            "planned_entry_price": 2000.0, "actual_entry_price": 2000.0,
            "planned_position_size": 300, "actual_position_size": 500,
            "planned_stop_price": 1880.0, "actual_stop_price": 1880.0,
            "planned_exit_price": 2120.0, "actual_exit_price": 0.0,
            "planned_exit_action": "allow_with_exit_plan", "trade_status": "entered",
            "is_unplanned_add": True, "is_overtrade": False, "stop_loss_violated": False,
            "reward_risk_at_entry": 2.0,
        },
    ]


def build_mistake_review_queue(
    journal_entries: Optional[List[JournalEntry]] = None,
) -> List[JournalEntry]:
    """Build mistake review queue — entries with discipline violations. Paper only."""
    if journal_entries is None:
        pool = _default_journal_entry_pool()
        policy = _default_journal_policy()
        journal_entries = [
            evaluate_journal_entry(
                journal_entry_id=e["journal_entry_id"],
                symbol=e["symbol"], name=e["name"],
                candidate_id=e["candidate_id"], theme_id=e["theme_id"],
                sector_id=e["sector_id"],
                planned_entry_price=e["planned_entry_price"],
                actual_entry_price=e["actual_entry_price"],
                planned_position_size=e["planned_position_size"],
                actual_position_size=e["actual_position_size"],
                planned_stop_price=e["planned_stop_price"],
                actual_stop_price=e["actual_stop_price"],
                planned_exit_price=e["planned_exit_price"],
                actual_exit_price=e["actual_exit_price"],
                planned_exit_action=e.get("planned_exit_action", ""),
                trade_status=e.get("trade_status", "entered"),
                is_unplanned_add=e.get("is_unplanned_add", False),
                is_overtrade=e.get("is_overtrade", False),
                stop_loss_violated=e.get("stop_loss_violated", False),
                reward_risk_at_entry=e.get("reward_risk_at_entry", 0.0),
                policy=policy,
            )
            for e in pool
        ]
    return [e for e in journal_entries if e.violation_codes or e.mistake_tags]


def build_violation_queue(
    journal_entries: Optional[List[JournalEntry]] = None,
) -> List[JournalEntry]:
    """Build rule violation queue — entries with critical violations. Paper only."""
    if journal_entries is None:
        pool = _default_journal_entry_pool()
        policy = _default_journal_policy()
        journal_entries = [
            evaluate_journal_entry(
                journal_entry_id=e["journal_entry_id"],
                symbol=e["symbol"], name=e["name"],
                candidate_id=e["candidate_id"], theme_id=e["theme_id"],
                sector_id=e["sector_id"],
                planned_entry_price=e["planned_entry_price"],
                actual_entry_price=e["actual_entry_price"],
                planned_position_size=e["planned_position_size"],
                actual_position_size=e["actual_position_size"],
                planned_stop_price=e["planned_stop_price"],
                actual_stop_price=e["actual_stop_price"],
                planned_exit_price=e["planned_exit_price"],
                actual_exit_price=e["actual_exit_price"],
                planned_exit_action=e.get("planned_exit_action", ""),
                trade_status=e.get("trade_status", "entered"),
                is_unplanned_add=e.get("is_unplanned_add", False),
                is_overtrade=e.get("is_overtrade", False),
                stop_loss_violated=e.get("stop_loss_violated", False),
                reward_risk_at_entry=e.get("reward_risk_at_entry", 0.0),
                policy=policy,
            )
            for e in pool
        ]
    critical = {"NO_PLANNED_ENTRY", "MISSING_EXIT_PLAN", "STOP_LOSS_VIOLATION", "OVERTRADE"}
    return [
        e for e in journal_entries
        if any(v in critical for v in e.violation_codes)
    ]


def build_improvement_queue(
    journal_entries: Optional[List[JournalEntry]] = None,
) -> List[Dict[str, Any]]:
    """Build improvement suggestion queue. Paper only."""
    if journal_entries is None:
        pool = _default_journal_entry_pool()
        policy = _default_journal_policy()
        journal_entries = [
            evaluate_journal_entry(
                journal_entry_id=e["journal_entry_id"],
                symbol=e["symbol"], name=e["name"],
                candidate_id=e["candidate_id"], theme_id=e["theme_id"],
                sector_id=e["sector_id"],
                planned_entry_price=e["planned_entry_price"],
                actual_entry_price=e["actual_entry_price"],
                planned_position_size=e["planned_position_size"],
                actual_position_size=e["actual_position_size"],
                planned_stop_price=e["planned_stop_price"],
                actual_stop_price=e["actual_stop_price"],
                planned_exit_price=e["planned_exit_price"],
                actual_exit_price=e["actual_exit_price"],
                planned_exit_action=e.get("planned_exit_action", ""),
                trade_status=e.get("trade_status", "entered"),
                is_unplanned_add=e.get("is_unplanned_add", False),
                is_overtrade=e.get("is_overtrade", False),
                stop_loss_violated=e.get("stop_loss_violated", False),
                reward_risk_at_entry=e.get("reward_risk_at_entry", 0.0),
                policy=policy,
            )
            for e in pool
        ]
    suggestions = []
    for e in journal_entries:
        if e.violation_codes:
            sugg: Dict[str, Any] = {
                "symbol": e.symbol,
                "journal_entry_id": e.journal_entry_id,
                "violation_codes": list(e.violation_codes),
                "mistake_tags": list(e.mistake_tags),
                "suggestion": _make_suggestion(e.violation_codes),
                "paper_only": True,
                "should_auto_apply": False,
            }
            suggestions.append(sugg)
    return suggestions


def _make_suggestion(violation_codes: List[str]) -> str:
    if "NO_PLANNED_ENTRY" in violation_codes:
        return "先建立計畫再進場，不得無計畫交易"
    if "MISSING_EXIT_PLAN" in violation_codes:
        return "進場前必須設定出場計畫與停損"
    if "STOP_LOSS_VIOLATION" in violation_codes:
        return "停損必須確實執行，不得隨意移動停損"
    if "ENTRY_SLIPPAGE_EXCESS" in violation_codes:
        return "避免追高，嚴守進場價格紀律"
    if "SIZE_DEVIATION_EXCESS" in violation_codes:
        return "部位大小必須符合原始計畫，避免超量"
    if "UNPLANNED_ADD" in violation_codes:
        return "不得無計畫加碼，加碼需事先納入計畫"
    if "OVERTRADE" in violation_codes:
        return "減少過度交易頻率，保持交易紀律"
    return "遵守交易計畫，確實填寫交易日誌"


def evaluate_discipline(
    journal_entries: Optional[List[JournalEntry]] = None,
) -> Dict[str, Any]:
    """Evaluate execution discipline across journal entries. Paper only."""
    if journal_entries is None:
        pool = _default_journal_entry_pool()
        policy = _default_journal_policy()
        journal_entries = [
            evaluate_journal_entry(
                journal_entry_id=e["journal_entry_id"],
                symbol=e["symbol"], name=e["name"],
                candidate_id=e["candidate_id"], theme_id=e["theme_id"],
                sector_id=e["sector_id"],
                planned_entry_price=e["planned_entry_price"],
                actual_entry_price=e["actual_entry_price"],
                planned_position_size=e["planned_position_size"],
                actual_position_size=e["actual_position_size"],
                planned_stop_price=e["planned_stop_price"],
                actual_stop_price=e["actual_stop_price"],
                planned_exit_price=e["planned_exit_price"],
                actual_exit_price=e["actual_exit_price"],
                planned_exit_action=e.get("planned_exit_action", ""),
                trade_status=e.get("trade_status", "entered"),
                is_unplanned_add=e.get("is_unplanned_add", False),
                is_overtrade=e.get("is_overtrade", False),
                stop_loss_violated=e.get("stop_loss_violated", False),
                reward_risk_at_entry=e.get("reward_risk_at_entry", 0.0),
                policy=policy,
            )
            for e in pool
        ]
    n = len(journal_entries)
    compliant = sum(1 for e in journal_entries if e.execution_action == "compliant")
    slippage_violations = sum(1 for e in journal_entries if "ENTRY_SLIPPAGE_EXCESS" in e.violation_codes)
    size_violations = sum(1 for e in journal_entries if "SIZE_DEVIATION_EXCESS" in e.violation_codes)
    stop_dev_violations = sum(1 for e in journal_entries if "STOP_DEVIATION_EXCESS" in e.violation_codes)
    missing_exit = sum(1 for e in journal_entries if "MISSING_EXIT_PLAN" in e.violation_codes)
    unplanned_add = sum(1 for e in journal_entries if "UNPLANNED_ADD" in e.violation_codes)
    overtrade = sum(1 for e in journal_entries if "OVERTRADE" in e.violation_codes)
    sl_violation = sum(1 for e in journal_entries if "STOP_LOSS_VIOLATION" in e.violation_codes)
    human_review = sum(1 for e in journal_entries if e.requires_human_review)
    return {
        "total_entries": n,
        "compliant_count": compliant,
        "slippage_violation_count": slippage_violations,
        "size_violation_count": size_violations,
        "stop_deviation_violation_count": stop_dev_violations,
        "missing_exit_plan_count": missing_exit,
        "unplanned_add_count": unplanned_add,
        "overtrade_count": overtrade,
        "stop_loss_violation_count": sl_violation,
        "human_review_count": human_review,
        "total_violations": slippage_violations + size_violations + stop_dev_violations + missing_exit + unplanned_add + overtrade + sl_violation,
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "schema_version": "211",
    }


def _build_execution_discipline_summary(
    journal_entries: List[JournalEntry],
    policy: TradeJournalPolicy,
) -> ExecutionDisciplineSummary:
    n = len(journal_entries)
    compliant = sum(1 for e in journal_entries if e.execution_action == "compliant")
    slippage_v = sum(1 for e in journal_entries if "ENTRY_SLIPPAGE_EXCESS" in e.violation_codes)
    size_v = sum(1 for e in journal_entries if "SIZE_DEVIATION_EXCESS" in e.violation_codes)
    stop_dev_v = sum(1 for e in journal_entries if "STOP_DEVIATION_EXCESS" in e.violation_codes)
    missing_exit = sum(1 for e in journal_entries if "MISSING_EXIT_PLAN" in e.violation_codes)
    unplanned_add = sum(1 for e in journal_entries if "UNPLANNED_ADD" in e.violation_codes)
    overtrade = sum(1 for e in journal_entries if "OVERTRADE" in e.violation_codes)
    sl_v = sum(1 for e in journal_entries if "STOP_LOSS_VIOLATION" in e.violation_codes)
    human_rv = sum(1 for e in journal_entries if e.requires_human_review)

    # Average discipline score (estimate from execution_action)
    action_scores = {
        "compliant": 95.0, "monitor": 82.0, "require_journal_note": 72.0,
        "require_rescore": 62.0, "flag_discipline_warning": 52.0,
        "block_followup_action": 35.0, "human_review_required": 20.0,
    }
    scores = [action_scores.get(e.execution_action, 70.0) for e in journal_entries]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    worst_symbols = [
        e.symbol for e in journal_entries
        if e.execution_action in ("block_followup_action", "human_review_required", "flag_discipline_warning")
    ][:3]

    all_tags: List[str] = []
    for e in journal_entries:
        all_tags.extend(e.mistake_tags)
    tag_counts: Dict[str, int] = {}
    for t in all_tags:
        tag_counts[t] = tag_counts.get(t, 0) + 1
    top_tags = sorted(tag_counts, key=lambda x: tag_counts[x], reverse=True)[:3]

    all_codes: List[str] = []
    for e in journal_entries:
        all_codes.extend(e.violation_codes)
    code_counts: Dict[str, int] = {}
    for c in all_codes:
        code_counts[c] = code_counts.get(c, 0) + 1
    top_codes = sorted(code_counts, key=lambda x: code_counts[x], reverse=True)[:3]

    return ExecutionDisciplineSummary(
        total_journal_entries=n,
        compliant_entry_count=compliant,
        entry_slippage_violation_count=slippage_v,
        size_deviation_violation_count=size_v,
        stop_deviation_violation_count=stop_dev_v,
        missing_exit_plan_count=missing_exit,
        unplanned_add_count=unplanned_add,
        overtrade_count=overtrade,
        stop_loss_violation_count=sl_v,
        human_review_count=human_rv,
        average_discipline_score=avg_score,
        lowest_discipline_symbols=worst_symbols,
        top_mistake_tags=top_tags,
        top_violation_codes=top_codes,
        discipline_quality_grade=_grade_discipline(avg_score),
        plan_adherence_grade=_grade_plan_adherence(compliant, n),
    )


def run_journal_review(
    review_input: Optional[JournalReviewInput] = None,
) -> JournalReviewResult:
    """Run a paper trade journal review. Paper only, no real orders."""
    if review_input is None:
        review_input = JournalReviewInput(
            review_period="2026-W29",
            journal_entries=_default_journal_entry_pool(),
        )

    policy = review_input.journal_policy or _default_journal_policy()
    raw_entries = review_input.journal_entries

    review_id = _make_journal_review_id(review_input.review_period, len(raw_entries))

    journal_entries: List[JournalEntry] = []
    for e in raw_entries:
        entry = evaluate_journal_entry(
            journal_entry_id=e.get("journal_entry_id", ""),
            symbol=e.get("symbol", ""),
            name=e.get("name", ""),
            candidate_id=e.get("candidate_id", ""),
            theme_id=e.get("theme_id", ""),
            sector_id=e.get("sector_id", ""),
            planned_entry_price=e.get("planned_entry_price", 0.0),
            actual_entry_price=e.get("actual_entry_price", 0.0),
            planned_position_size=e.get("planned_position_size", 0),
            actual_position_size=e.get("actual_position_size", 0),
            planned_stop_price=e.get("planned_stop_price", 0.0),
            actual_stop_price=e.get("actual_stop_price", 0.0),
            planned_exit_price=e.get("planned_exit_price", 0.0),
            actual_exit_price=e.get("actual_exit_price", 0.0),
            planned_exit_action=e.get("planned_exit_action", ""),
            trade_status=e.get("trade_status", "entered"),
            is_unplanned_add=e.get("is_unplanned_add", False),
            is_overtrade=e.get("is_overtrade", False),
            stop_loss_violated=e.get("stop_loss_violated", False),
            reward_risk_at_entry=e.get("reward_risk_at_entry", 0.0),
            policy=policy,
        )
        journal_entries.append(entry)

    discipline_summary = _build_execution_discipline_summary(journal_entries, policy)

    mistake_queue = [e for e in journal_entries if e.violation_codes or e.mistake_tags]
    critical_codes = {"NO_PLANNED_ENTRY", "MISSING_EXIT_PLAN", "STOP_LOSS_VIOLATION", "OVERTRADE"}
    violation_queue = [
        e for e in journal_entries if any(v in critical_codes for v in e.violation_codes)
    ]
    human_queue = [e for e in journal_entries if e.requires_human_review]

    plan_adherence = [
        {
            "symbol": e.symbol,
            "compliant": e.execution_action == "compliant",
            "entry_match": e.entry_slippage_pct <= policy.max_allowed_entry_slippage_pct,
            "size_match": e.size_deviation_pct <= policy.max_allowed_size_deviation_pct,
            "stop_match": e.stop_deviation_pct <= policy.max_allowed_stop_deviation_pct,
        }
        for e in journal_entries
    ]

    improvement_suggestions = build_improvement_queue(journal_entries)

    return JournalReviewResult(
        journal_review_id=review_id,
        journal_version="2.0.11",
        review_period=review_input.review_period,
        journal_policy=policy,
        trade_journal_snapshot=journal_entries,
        execution_discipline_snapshot=discipline_summary,
        plan_adherence_snapshot=plan_adherence,
        mistake_review_queue=mistake_queue,
        rule_violation_queue=violation_queue,
        improvement_suggestion_queue=improvement_suggestions,
        human_review_queue=human_queue,
        paper_only_safety_snapshot=True,
        all_passed=True,
        should_auto_apply=False,
        auto_apply_enabled=False,
    )


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_journal_json(result: JournalReviewResult) -> JournalExportResult:
    """Export journal review as JSON. Paper only."""
    import json as _json
    payload = {
        "version": "2.0.11",
        "schema_version": "211",
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "journal_review_id": result.journal_review_id,
        "journal_version": result.journal_version,
        "review_period": result.review_period,
        "entry_count": len(result.trade_journal_snapshot),
        "mistake_count": len(result.mistake_review_queue),
        "violation_count": len(result.rule_violation_queue),
        "human_review_count": len(result.human_review_queue),
    }
    content = _json.dumps(payload, ensure_ascii=False, indent=2)
    return JournalExportResult(
        journal_review_id=result.journal_review_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
    )


def export_journal_markdown(result: JournalReviewResult) -> JournalExportResult:
    """Export journal review as Markdown. Paper only."""
    lines = [
        "# Paper Trade Journal Review v2.0.11",
        "",
        f"**Period:** {result.review_period}",
        f"**Journal Review ID:** {result.journal_review_id}",
        f"**Paper Only:** True",
        f"**No Real Orders:** True",
        f"**Should Auto Apply:** False",
        "",
        f"## Journal Entries: {len(result.trade_journal_snapshot)}",
        f"## Mistakes: {len(result.mistake_review_queue)}",
        f"## Violations: {len(result.rule_violation_queue)}",
        f"## Human Review: {len(result.human_review_queue)}",
        "",
        "*[!] Paper Only. Not Investment Advice. Journal Actions Are Recommendation Only.*",
    ]
    content = "\n".join(lines)
    return JournalExportResult(
        journal_review_id=result.journal_review_id,
        export_format="markdown",
        content=content,
        is_valid=True,
        export_status="complete",
        paper_only_confirmed=True,
    )


def export_journal_csv(result: JournalReviewResult) -> JournalCSV:
    """Export journal entries as CSV. Paper only."""
    header = "symbol,planned_entry,actual_entry,slippage_pct,planned_size,actual_size,size_dev_pct,trade_status,execution_action,violation_codes,should_auto_apply"
    rows = [header]
    for e in result.trade_journal_snapshot:
        vcodes = "|".join(e.violation_codes)
        rows.append(
            f"{e.symbol},{e.planned_entry_price},{e.actual_entry_price},{e.entry_slippage_pct:.4f},"
            f"{e.planned_position_size},{e.actual_position_size},{e.size_deviation_pct:.4f},"
            f"{e.trade_status},{e.execution_action},{vcodes},{e.should_auto_apply}"
        )
    csv_content = "\n".join(rows)
    return JournalCSV(
        journal_review_id=result.journal_review_id,
        csv_content=csv_content,
        row_count=len(result.trade_journal_snapshot),
        is_valid=True,
    )


def export_discipline_csv(result: JournalReviewResult) -> ExecutionDisciplineCSV:
    """Export execution discipline summary as CSV. Paper only."""
    s = result.execution_discipline_snapshot
    if s is None:
        s = ExecutionDisciplineSummary()
    header = "total,compliant,slippage_v,size_v,stop_dev_v,missing_exit,unplanned_add,overtrade,sl_violation,human_review,avg_score,discipline_grade,adherence_grade"
    row = (
        f"{s.total_journal_entries},{s.compliant_entry_count},"
        f"{s.entry_slippage_violation_count},{s.size_deviation_violation_count},"
        f"{s.stop_deviation_violation_count},{s.missing_exit_plan_count},"
        f"{s.unplanned_add_count},{s.overtrade_count},{s.stop_loss_violation_count},"
        f"{s.human_review_count},{s.average_discipline_score:.2f},"
        f"{s.discipline_quality_grade},{s.plan_adherence_grade}"
    )
    csv_content = header + "\n" + row
    return ExecutionDisciplineCSV(
        journal_review_id=result.journal_review_id,
        csv_content=csv_content,
        row_count=1,
        is_valid=True,
    )


def export_mistake_review_csv(result: JournalReviewResult) -> MistakeReviewCSV:
    """Export mistake review queue as CSV. Paper only."""
    header = "symbol,execution_action,violation_codes,mistake_tags,requires_human_review"
    rows = [header]
    for e in result.mistake_review_queue:
        vcodes = "|".join(e.violation_codes)
        mtags = "|".join(e.mistake_tags)
        rows.append(
            f"{e.symbol},{e.execution_action},{vcodes},{mtags},{e.requires_human_review}"
        )
    csv_content = "\n".join(rows)
    return MistakeReviewCSV(
        journal_review_id=result.journal_review_id,
        csv_content=csv_content,
        row_count=len(result.mistake_review_queue),
        is_valid=True,
    )


def export_violation_queue_csv(result: JournalReviewResult) -> ViolationQueueCSV:
    """Export violation queue as CSV. Paper only."""
    header = "symbol,execution_action,violation_codes,requires_human_review"
    rows = [header]
    for e in result.rule_violation_queue:
        vcodes = "|".join(e.violation_codes)
        rows.append(
            f"{e.symbol},{e.execution_action},{vcodes},{e.requires_human_review}"
        )
    csv_content = "\n".join(rows)
    return ViolationQueueCSV(
        journal_review_id=result.journal_review_id,
        csv_content=csv_content,
        row_count=len(result.rule_violation_queue),
        is_valid=True,
    )


def export_journal_audit_snapshot(result: JournalReviewResult) -> JournalAuditSnapshot:
    """Export journal audit snapshot. Paper only."""
    hash_val = hashlib.sha256(
        f"{result.journal_review_id}-{result.review_period}-{len(result.trade_journal_snapshot)}".encode()
    ).hexdigest()[:16]
    return JournalAuditSnapshot(
        journal_review_id=result.journal_review_id,
        run_metadata="v211-paper-only-journal-audit",
        trade_journal_snapshot=f"entries={len(result.trade_journal_snapshot)}",
        execution_discipline_snapshot=f"discipline_checked=True",
        plan_adherence_snapshot=f"plan_adherence_entries={len(result.plan_adherence_snapshot)}",
        mistake_review_snapshot=f"mistakes={len(result.mistake_review_queue)}",
        safety_snapshot="paper_only=True,no_real_orders=True,should_auto_apply=False",
        reproducibility_hash=hash_val,
        export_status="complete",
    )


# ---------------------------------------------------------------------------
# Version / summary
# ---------------------------------------------------------------------------

def verify_version() -> bool:
    """Verify v2.0.11 version constants are correct."""
    return VERSION == "2.0.11" and SCHEMA_VERSION == "211"


def get_cockpit_summary_v211() -> Dict[str, Any]:
    """Return v2.0.11 cockpit summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "require_planned_entry_before_trade": True,
        "journal_actions_recommendation_only": True,
        "execution_action_count": len(EXECUTION_ACTIONS),
        "trade_status_count": len(TRADE_STATUSES),
        "cli_command_count": len(CLI_COMMANDS_V211),
        "gui_tab_count": len(GUI_TABS_V211),
        "safety_flag_count": len(SAFETY_FLAGS_V211),
        "model_count": len(_ALL_MODEL_NAMES_V211),
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }
