"""
paper_trading/small_capital_strategy/paper_cockpit_v205.py
v2.0.5 Paper Watchlist Rotation & Candidate Promotion Queue
[!] Paper Only. Research Only. Rotation Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.5"
SCHEMA_VERSION = "205"
RELEASE_NAME = "Paper Watchlist Rotation & Candidate Promotion Queue"
BASELINE_TESTS = 33984
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

WATCHLIST_STATUSES: List[str] = [
    "active_watchlist",
    "promoted_candidate",
    "second_wave_candidate",
    "abc_pullback_candidate",
    "breakout_candidate",
    "quarantined_no_entry",
    "downgraded",
    "removed",
    "human_review_required",
]

ROTATION_DECISION_TYPES: List[str] = [
    "keep",
    "promote",
    "demote",
    "remove",
    "quarantine",
    "human_review",
]

CLI_COMMANDS_V205: List[str] = [
    "paper-cockpit-v205-rotate-watchlist",
    "paper-cockpit-v205-promote-candidates",
    "paper-cockpit-v205-demote-candidates",
    "paper-cockpit-v205-build-human-review-queue",
    "paper-cockpit-v205-build-quarantine-queue",
    "paper-cockpit-v205-export-json",
    "paper-cockpit-v205-export-md",
    "paper-cockpit-v205-export-csv",
    "paper-cockpit-v205-health",
    "paper-cockpit-v205-gate",
]

GUI_TABS_V205: List[str] = [
    "watchlist_rotation_v205",
    "promotion_queue_v205",
    "human_review_queue_v205",
]

ROTATION_RESULT_FIELDS: List[str] = [
    "rotation_id",
    "rotation_version",
    "rotation_period",
    "input_watchlist_snapshot",
    "review_pack_snapshot",
    "simulation_ranking_snapshot",
    "promotion_queue",
    "demotion_queue",
    "remove_queue",
    "keep_queue",
    "human_review_queue",
    "paper_only_safety_snapshot",
]

WATCHLIST_ITEM_FIELDS: List[str] = [
    "symbol",
    "name",
    "theme_tags",
    "current_status",
    "previous_status",
    "score",
    "trend_quality",
    "volume_quality",
    "chip_quality",
    "risk_quality",
    "no_entry_reasons",
    "promotion_reasons",
    "demotion_reasons",
    "human_review_reasons",
    "next_review_action",
]

PROMOTION_DECISION_FIELDS: List[str] = [
    "decision_id",
    "symbol",
    "from_status",
    "to_status",
    "promotion_score",
    "risk_score",
    "theme_score",
    "technical_score",
    "liquidity_score",
    "chip_score",
    "reason_codes",
    "blocked_reasons",
    "requires_human_review",
    "should_auto_apply",
]

QUEUE_SUMMARY_FIELDS: List[str] = [
    "total_watchlist_count",
    "keep_count",
    "promote_count",
    "demote_count",
    "remove_count",
    "quarantine_count",
    "human_review_count",
    "avg_promotion_score",
    "avg_risk_score",
    "top_promotion_candidates",
    "top_demoted_symbols",
    "top_quarantine_reasons",
    "weekly_rotation_grade",
]

ROTATION_EXPORT_FORMATS: List[str] = [
    "json",
    "markdown",
    "csv",
    "audit_snapshot",
]

SAFETY_FLAGS_V205: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "rotation_only": True,
    "validation_only": True,
    "watchlist_rotation_only": True,
    "candidate_promotion_queue_only": True,
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
    "paper_only_data_only": True,
    "broker_execution_disabled": True,
    "production_trading_blocked": True,
}

assert len(SAFETY_FLAGS_V205) == 20, f"Expected 20 SAFETY_FLAGS_V205, got {len(SAFETY_FLAGS_V205)}"
assert len(WATCHLIST_STATUSES) == 9
assert len(ROTATION_DECISION_TYPES) == 6
assert len(CLI_COMMANDS_V205) == 10
assert len(GUI_TABS_V205) == 3
assert len(ROTATION_RESULT_FIELDS) == 12
assert len(WATCHLIST_ITEM_FIELDS) == 15
assert len(PROMOTION_DECISION_FIELDS) == 14
assert len(QUEUE_SUMMARY_FIELDS) == 13
assert len(ROTATION_EXPORT_FORMATS) == 4

COVERED_VERSIONS: List[str] = [
    "2.0.4", "2.0.3", "2.0.2", "2.0.1", "2.0.0",
    "1.9.10", "1.9.9", "1.9.8", "1.9.7", "1.9.6",
    "1.9.5", "1.9.4", "1.9.3", "1.9.2", "1.9.0",
    "1.8.9", "1.8.8", "1.8.4", "1.8.3", "1.8.2",
    "1.8.1", "1.8.0", "1.7.9", "1.7.8", "1.7.7",
    "1.7.6", "1.7.5", "1.7.3", "1.7.2", "1.7.1",
    "1.7.0",
]


# ---------------------------------------------------------------------------
# Dataclasses — 12 models, schema_version="205"
# ---------------------------------------------------------------------------

@dataclass
class WatchlistItem:
    """Watchlist item schema. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    theme_tags: List[str] = field(default_factory=list)
    current_status: str = "active_watchlist"
    previous_status: str = "active_watchlist"
    score: float = 0.0
    trend_quality: float = 0.0
    volume_quality: float = 0.0
    chip_quality: float = 0.0
    risk_quality: float = 0.0
    no_entry_reasons: List[str] = field(default_factory=list)
    promotion_reasons: List[str] = field(default_factory=list)
    demotion_reasons: List[str] = field(default_factory=list)
    human_review_reasons: List[str] = field(default_factory=list)
    next_review_action: str = "keep"


@dataclass
class PromotionDecision:
    """Promotion decision schema. v2.0.5. should_auto_apply is always False."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    decision_id: str = ""
    symbol: str = ""
    from_status: str = "active_watchlist"
    to_status: str = "promoted_candidate"
    promotion_score: float = 0.0
    risk_score: float = 0.0
    theme_score: float = 0.0
    technical_score: float = 0.0
    liquidity_score: float = 0.0
    chip_score: float = 0.0
    reason_codes: List[str] = field(default_factory=list)
    blocked_reasons: List[str] = field(default_factory=list)
    requires_human_review: bool = True
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        # Enforce safety invariant: should_auto_apply must always be False
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class QueueSummary:
    """Queue summary for a watchlist rotation. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    total_watchlist_count: int = 0
    keep_count: int = 0
    promote_count: int = 0
    demote_count: int = 0
    remove_count: int = 0
    quarantine_count: int = 0
    human_review_count: int = 0
    avg_promotion_score: float = 0.0
    avg_risk_score: float = 0.0
    top_promotion_candidates: List[str] = field(default_factory=list)
    top_demoted_symbols: List[str] = field(default_factory=list)
    top_quarantine_reasons: List[str] = field(default_factory=list)
    weekly_rotation_grade: str = "C"


@dataclass
class WatchlistRotationInput:
    """Input for a watchlist rotation run. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    rotation_period: str = ""
    watchlist_items: List[WatchlistItem] = field(default_factory=list)
    review_pack_ids: List[str] = field(default_factory=list)
    simulation_ranking_ids: List[str] = field(default_factory=list)
    risk_budget_pct: float = 20.0
    strategy_profile_id: str = ""
    human_review_required: bool = True


@dataclass
class WatchlistRotationResult:
    """Full result of one watchlist rotation run. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    research_only: bool = True
    rotation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    rotation_id: str = ""
    rotation_version: str = "2.0.5"
    rotation_period: str = ""
    input_watchlist_snapshot: List[str] = field(default_factory=list)
    review_pack_snapshot: List[str] = field(default_factory=list)
    simulation_ranking_snapshot: List[str] = field(default_factory=list)
    promotion_queue: List[PromotionDecision] = field(default_factory=list)
    demotion_queue: List[PromotionDecision] = field(default_factory=list)
    remove_queue: List[PromotionDecision] = field(default_factory=list)
    keep_queue: List[WatchlistItem] = field(default_factory=list)
    human_review_queue: List[WatchlistItem] = field(default_factory=list)
    quarantine_queue: List[WatchlistItem] = field(default_factory=list)
    queue_summary: Optional[QueueSummary] = None
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class RotationExportResult:
    """Export result for a watchlist rotation. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    rotation_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True


@dataclass
class RotationAuditSnapshot:
    """Audit snapshot for a watchlist rotation. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    rotation_id: str = ""
    run_metadata: str = ""
    input_snapshot: str = ""
    promotion_snapshot: str = ""
    demotion_snapshot: str = ""
    quarantine_snapshot: str = ""
    human_review_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class WatchlistRotationReport:
    """Markdown report for a watchlist rotation. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    rotation_id: str = ""
    rotation_period: str = ""
    report_content: str = ""
    section_count: int = 0
    is_valid: bool = False


@dataclass
class PromotionQueueCSV:
    """CSV export of the promotion queue. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    rotation_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


@dataclass
class V205HealthSummary:
    """Health summary for v2.0.5. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.5"


@dataclass
class V205ReleaseSummary:
    """Release summary for v2.0.5. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    version: str = "2.0.5"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 12
    cli_count: int = 10
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V205: List[str] = [
    "WatchlistItem",
    "PromotionDecision",
    "QueueSummary",
    "WatchlistRotationInput",
    "WatchlistRotationResult",
    "RotationExportResult",
    "RotationAuditSnapshot",
    "WatchlistRotationReport",
    "PromotionQueueCSV",
    "V205HealthSummary",
    "V205ReleaseSummary",
    "DemotionQueueCSV",
]

assert len(_ALL_MODEL_NAMES_V205) == 12


@dataclass
class DemotionQueueCSV:
    """CSV export of the demotion queue. v2.0.5."""
    schema_version: str = "205"
    paper_only: bool = True
    no_real_orders: bool = True
    rotation_id: str = ""
    csv_content: str = ""
    row_count: int = 0
    is_valid: bool = False


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------

def _make_rotation_id(rotation_period: str, item_count: int) -> str:
    raw = f"rotation-{rotation_period}-{item_count}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _score_item(item: WatchlistItem, risk_budget_pct: float) -> float:
    """Score a watchlist item for promotion eligibility. Paper only."""
    base = (item.trend_quality + item.volume_quality + item.chip_quality + item.risk_quality) / 4.0
    # Penalty when risk_quality is weak (below 50) or risk budget is very tight
    risk_quality_penalty = max(0.0, (50.0 - item.risk_quality) * 0.4) if item.risk_quality < 50.0 else 0.0
    budget_penalty = max(0.0, (10.0 - risk_budget_pct) * 0.5) if risk_budget_pct < 10.0 else 0.0
    no_entry_penalty = len(item.no_entry_reasons) * 5.0
    promotion_bonus = len(item.promotion_reasons) * 3.0
    return max(0.0, min(100.0, base + promotion_bonus - risk_quality_penalty - budget_penalty - no_entry_penalty))


def _classify_item(item: WatchlistItem, promotion_score: float) -> str:
    """Classify rotation decision for a watchlist item. Paper only."""
    if item.no_entry_reasons and len(item.no_entry_reasons) >= 3:
        return "quarantine"
    if item.human_review_reasons:
        return "human_review"
    if promotion_score >= 75.0 and not item.no_entry_reasons:
        return "promote"
    if promotion_score < 30.0 or item.demotion_reasons:
        return "demote" if promotion_score >= 15.0 else "remove"
    return "keep"


def _build_promotion_decision(
    item: WatchlistItem,
    decision_type: str,
    rotation_id: str,
    simulation_ranking_ids: List[str],
) -> PromotionDecision:
    """Build a promotion decision for a watchlist item. Paper only."""
    decision_id = f"DEC-{rotation_id}-{item.symbol}"
    to_status_map = {
        "promote": "promoted_candidate",
        "demote": "downgraded",
        "remove": "removed",
        "quarantine": "quarantined_no_entry",
        "human_review": "human_review_required",
        "keep": item.current_status,
    }
    to_status = to_status_map.get(decision_type, item.current_status)

    sim_score = float(abs(hash(item.symbol + rotation_id)) % 40 + 50) if simulation_ranking_ids else 50.0
    theme_score = float(len(item.theme_tags) * 10 + 40) if item.theme_tags else 40.0
    liquidity_score = item.volume_quality
    chip_score = item.chip_quality
    risk_score = item.risk_quality

    reason_codes = list(item.promotion_reasons) if decision_type == "promote" else list(item.demotion_reasons)
    blocked = list(item.no_entry_reasons)

    return PromotionDecision(
        decision_id=decision_id,
        symbol=item.symbol,
        from_status=item.current_status,
        to_status=to_status,
        promotion_score=_score_item(item, 20.0),
        risk_score=round(risk_score, 2),
        theme_score=round(theme_score, 2),
        technical_score=round(item.trend_quality, 2),
        liquidity_score=round(liquidity_score, 2),
        chip_score=round(chip_score, 2),
        reason_codes=reason_codes,
        blocked_reasons=blocked,
        requires_human_review=bool(item.human_review_reasons),
        should_auto_apply=False,
    )


def _build_queue_summary(
    promotion_queue: List[PromotionDecision],
    demotion_queue: List[PromotionDecision],
    remove_queue: List[PromotionDecision],
    keep_queue: List[WatchlistItem],
    human_review_queue: List[WatchlistItem],
    quarantine_queue: List[WatchlistItem],
) -> QueueSummary:
    """Build queue summary from rotation output. Paper only."""
    total = (
        len(promotion_queue) + len(demotion_queue) + len(remove_queue)
        + len(keep_queue) + len(human_review_queue) + len(quarantine_queue)
    )
    promo_scores = [d.promotion_score for d in promotion_queue] if promotion_queue else [0.0]
    risk_scores = [d.risk_score for d in promotion_queue] if promotion_queue else [0.0]
    avg_promo = sum(promo_scores) / max(1, len(promo_scores))
    avg_risk = sum(risk_scores) / max(1, len(risk_scores))

    top_promo = [d.symbol for d in sorted(promotion_queue, key=lambda x: x.promotion_score, reverse=True)[:3]]
    top_demoted = [d.symbol for d in demotion_queue[:3]]
    top_quarantine_reasons: List[str] = []
    for item in quarantine_queue:
        top_quarantine_reasons.extend(item.no_entry_reasons[:2])
    top_quarantine_reasons = list(dict.fromkeys(top_quarantine_reasons))[:3]

    avg_score = (avg_promo * 0.6 + avg_risk * 0.4)
    grade = "A" if avg_score >= 80 else "B" if avg_score >= 65 else "C" if avg_score >= 50 else "D"

    return QueueSummary(
        total_watchlist_count=total,
        keep_count=len(keep_queue),
        promote_count=len(promotion_queue),
        demote_count=len(demotion_queue),
        remove_count=len(remove_queue),
        quarantine_count=len(quarantine_queue),
        human_review_count=len(human_review_queue),
        avg_promotion_score=round(avg_promo, 2),
        avg_risk_score=round(avg_risk, 2),
        top_promotion_candidates=top_promo,
        top_demoted_symbols=top_demoted,
        top_quarantine_reasons=top_quarantine_reasons,
        weekly_rotation_grade=grade,
    )


def run_watchlist_rotation(
    rotation_input: Optional[WatchlistRotationInput] = None,
) -> WatchlistRotationResult:
    """Run a paper watchlist rotation. Paper only."""
    if rotation_input is None:
        rotation_input = WatchlistRotationInput(
            rotation_period="2026-W29",
            watchlist_items=[
                WatchlistItem(
                    symbol="2330",
                    name="台積電",
                    theme_tags=["semiconductor", "ai"],
                    current_status="active_watchlist",
                    score=78.0,
                    trend_quality=80.0,
                    volume_quality=75.0,
                    chip_quality=82.0,
                    risk_quality=70.0,
                    promotion_reasons=["strong_trend", "volume_confirmation"],
                ),
                WatchlistItem(
                    symbol="2317",
                    name="鴻海",
                    theme_tags=["ev", "ai_server"],
                    current_status="active_watchlist",
                    score=55.0,
                    trend_quality=55.0,
                    volume_quality=50.0,
                    chip_quality=58.0,
                    risk_quality=52.0,
                ),
            ],
        )

    rotation_id = _make_rotation_id(rotation_input.rotation_period, len(rotation_input.watchlist_items))

    promotion_queue: List[PromotionDecision] = []
    demotion_queue: List[PromotionDecision] = []
    remove_queue: List[PromotionDecision] = []
    keep_queue: List[WatchlistItem] = []
    human_review_queue: List[WatchlistItem] = []
    quarantine_queue: List[WatchlistItem] = []

    for item in rotation_input.watchlist_items:
        promo_score = _score_item(item, rotation_input.risk_budget_pct)
        decision_type = _classify_item(item, promo_score)

        if decision_type == "promote":
            dec = _build_promotion_decision(item, decision_type, rotation_id, rotation_input.simulation_ranking_ids)
            promotion_queue.append(dec)
        elif decision_type == "demote":
            dec = _build_promotion_decision(item, decision_type, rotation_id, rotation_input.simulation_ranking_ids)
            demotion_queue.append(dec)
        elif decision_type == "remove":
            dec = _build_promotion_decision(item, decision_type, rotation_id, rotation_input.simulation_ranking_ids)
            remove_queue.append(dec)
        elif decision_type == "quarantine":
            quarantine_queue.append(item)
        elif decision_type == "human_review":
            human_review_queue.append(item)
        else:
            keep_queue.append(item)

    summary = _build_queue_summary(
        promotion_queue, demotion_queue, remove_queue,
        keep_queue, human_review_queue, quarantine_queue,
    )

    return WatchlistRotationResult(
        rotation_id=rotation_id,
        rotation_period=rotation_input.rotation_period,
        input_watchlist_snapshot=[item.symbol for item in rotation_input.watchlist_items],
        review_pack_snapshot=list(rotation_input.review_pack_ids),
        simulation_ranking_snapshot=list(rotation_input.simulation_ranking_ids),
        promotion_queue=promotion_queue,
        demotion_queue=demotion_queue,
        remove_queue=remove_queue,
        keep_queue=keep_queue,
        human_review_queue=human_review_queue,
        quarantine_queue=quarantine_queue,
        queue_summary=summary,
        all_passed=True,
    )


def build_promotion_queue(
    rotation_input: Optional[WatchlistRotationInput] = None,
) -> List[PromotionDecision]:
    """Build only the promotion queue. Paper only."""
    result = run_watchlist_rotation(rotation_input)
    return result.promotion_queue


def build_demotion_queue(
    rotation_input: Optional[WatchlistRotationInput] = None,
) -> List[PromotionDecision]:
    """Build only the demotion queue. Paper only."""
    result = run_watchlist_rotation(rotation_input)
    return result.demotion_queue


def build_human_review_queue(
    rotation_input: Optional[WatchlistRotationInput] = None,
) -> List[WatchlistItem]:
    """Build only the human review queue. Paper only."""
    result = run_watchlist_rotation(rotation_input)
    return result.human_review_queue


def build_quarantine_queue(
    rotation_input: Optional[WatchlistRotationInput] = None,
) -> List[WatchlistItem]:
    """Build only the quarantine queue. Paper only."""
    result = run_watchlist_rotation(rotation_input)
    return result.quarantine_queue


def export_rotation_json(result: WatchlistRotationResult) -> RotationExportResult:
    """Export watchlist rotation as JSON. Paper only."""
    rotation_id = result.rotation_id
    content_parts = [
        f'{{"rotation_id": "{rotation_id}", "rotation_version": "{result.rotation_version}",',
        f'"rotation_period": "{result.rotation_period}", "paper_only": true,',
        f'"should_auto_apply": false, "no_real_orders": true,',
        f'"promote_count": {len(result.promotion_queue)},',
        f'"demote_count": {len(result.demotion_queue)},',
        f'"remove_count": {len(result.remove_queue)},',
        f'"keep_count": {len(result.keep_queue)},',
        f'"human_review_count": {len(result.human_review_queue)},',
        f'"quarantine_count": {len(result.quarantine_queue)}}}',
    ]
    content = "".join(content_parts)
    return RotationExportResult(
        rotation_id=rotation_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
    )


def export_rotation_markdown(result: WatchlistRotationResult) -> RotationExportResult:
    """Export watchlist rotation as Markdown. Paper only."""
    rotation_id = result.rotation_id
    lines = [
        f"# Watchlist Rotation Report v2.0.5",
        f"",
        f"**rotation_id**: {rotation_id}",
        f"**rotation_version**: {result.rotation_version}",
        f"**rotation_period**: {result.rotation_period}",
        f"**paper_only**: True",
        f"**should_auto_apply**: False",
        f"**no_real_orders**: True",
        f"",
        f"## Queue Summary",
        f"",
        f"- Promote: {len(result.promotion_queue)}",
        f"- Demote: {len(result.demotion_queue)}",
        f"- Remove: {len(result.remove_queue)}",
        f"- Keep: {len(result.keep_queue)}",
        f"- Human Review: {len(result.human_review_queue)}",
        f"- Quarantine: {len(result.quarantine_queue)}",
        f"",
        f"## Promotion Queue",
        f"",
    ]
    for dec in result.promotion_queue:
        lines.append(f"- {dec.symbol}: {dec.from_status} → {dec.to_status} (score={dec.promotion_score:.1f})")
    lines.append("")
    lines.append(f"---")
    lines.append(f"[!] Paper Only | No Real Orders | Not Investment Advice")
    content = "\n".join(lines)
    return RotationExportResult(
        rotation_id=rotation_id,
        export_format="markdown",
        content=content,
        is_valid=True,
        export_status="complete",
    )


def export_promotion_queue_csv(result: WatchlistRotationResult) -> PromotionQueueCSV:
    """Export promotion queue as CSV. Paper only."""
    rows = ["symbol,from_status,to_status,promotion_score,risk_score,should_auto_apply"]
    for dec in result.promotion_queue:
        rows.append(f"{dec.symbol},{dec.from_status},{dec.to_status},{dec.promotion_score},{dec.risk_score},False")
    csv_content = "\n".join(rows)
    return PromotionQueueCSV(
        rotation_id=result.rotation_id,
        csv_content=csv_content,
        row_count=len(result.promotion_queue),
        is_valid=True,
    )


def export_demotion_queue_csv(result: WatchlistRotationResult) -> DemotionQueueCSV:
    """Export demotion queue as CSV. Paper only."""
    rows = ["symbol,from_status,to_status,promotion_score,risk_score,should_auto_apply"]
    for dec in result.demotion_queue:
        rows.append(f"{dec.symbol},{dec.from_status},{dec.to_status},{dec.promotion_score},{dec.risk_score},False")
    csv_content = "\n".join(rows)
    return DemotionQueueCSV(
        rotation_id=result.rotation_id,
        csv_content=csv_content,
        row_count=len(result.demotion_queue),
        is_valid=True,
    )


def export_rotation_audit_snapshot(result: WatchlistRotationResult) -> RotationAuditSnapshot:
    """Build rotation audit snapshot. Paper only."""
    rotation_id = result.rotation_id
    raw = f"{rotation_id}-{result.rotation_period}-{len(result.promotion_queue)}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return RotationAuditSnapshot(
        rotation_id=rotation_id,
        run_metadata=f"v2.0.5-rotation-{rotation_id}",
        input_snapshot=str(result.input_watchlist_snapshot),
        promotion_snapshot=str([d.symbol for d in result.promotion_queue]),
        demotion_snapshot=str([d.symbol for d in result.demotion_queue]),
        quarantine_snapshot=str([item.symbol for item in result.quarantine_queue]),
        human_review_snapshot=str([item.symbol for item in result.human_review_queue]),
        safety_snapshot="paper_only=True;no_real_orders=True;should_auto_apply=False",
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
    }


def verify_version() -> bool:
    """Verify version constants are correct. Paper only."""
    return VERSION == "2.0.5" and SCHEMA_VERSION == "205"


def get_cockpit_summary_v205() -> Dict[str, Any]:
    """Return cockpit summary for v2.0.5. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "models_count": len(_ALL_MODEL_NAMES_V205),
        "cli_commands_count": len(CLI_COMMANDS_V205),
        "gui_tabs_count": len(GUI_TABS_V205),
        "safety_flags_count": len(SAFETY_FLAGS_V205),
        "watchlist_statuses_count": len(WATCHLIST_STATUSES),
    }
