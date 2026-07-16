"""
paper_trading/small_capital_strategy/decision_journal_engine_v189.py
Core engine for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Any

from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
    DecisionJournalEntry, DecisionJournalBook, DecisionReviewInput, DecisionReviewResult,
    DecisionOutcomeSnapshot, PaperDecisionLifecycle, PaperDecisionEvidenceLink,
    DecisionMistakeTag, DecisionQualityScore, DailyReviewSummary, WeeklyReviewSummary,
    MonthlyReviewSummary, ReviewChecklist, ReviewFinding, ReviewActionItem,
    ReviewBlockReason, JournalExportManifest, JournalEvidencePack, JournalAuditTrail,
    JournalDashboard, JournalValidationResult,
)
from paper_trading.small_capital_strategy.decision_journal_version_v189 import (
    JOURNAL_ENTRY_STATES, REVIEW_DIMENSIONS, MISTAKE_TAGS, QUALITY_GRADES,
    FORBIDDEN_JOURNAL_ACTIONS, ALLOWED_JOURNAL_ACTIONS, HARD_BLOCK_CONDITIONS,
)
from paper_trading.small_capital_strategy.decision_journal_safety_v189 import (
    is_forbidden_action, is_allowed_action, is_safe_output_path,
    run_safety_audit, validate_journal_entry_safe,
)


def validate_journal_action(action: str) -> bool:
    """Return True if action is an allowed journal action."""
    return action in ALLOWED_JOURNAL_ACTIONS


def validate_journal_state(state: str) -> bool:
    """Return True if state is a valid journal entry state."""
    return state in JOURNAL_ENTRY_STATES


def validate_quality_grade(grade: str) -> bool:
    """Return True if grade is a valid quality grade."""
    return grade in QUALITY_GRADES


def validate_mistake_tag(tag: str) -> bool:
    """Return True if tag is a valid mistake tag."""
    return tag in MISTAKE_TAGS


def validate_review_dimension(dimension: str) -> bool:
    """Return True if dimension is a valid review dimension."""
    return dimension in REVIEW_DIMENSIONS


def create_journal_entry(
    entry_id: str = "",
    date_label: str = "",
    state: str = "OBSERVE",
    symbol: str = "",
    rationale: str = "",
    evidence_refs: Optional[List[str]] = None,
    workflow_id: str = "",
    market_regime: str = "BULL",
    **kwargs,
) -> DecisionJournalEntry:
    """Create a new paper-only journal entry."""
    entry = DecisionJournalEntry(
        entry_id=entry_id or f"JE-{date_label}-{symbol or 'GENERAL'}",
        date_label=date_label,
        state=state if state in JOURNAL_ENTRY_STATES else "OBSERVE",
        symbol=symbol,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        workflow_id=workflow_id,
        market_regime=market_regime,
    )
    return entry


def validate_journal_entry(entry: DecisionJournalEntry) -> JournalValidationResult:
    """Validate a journal entry. Returns JournalValidationResult."""
    errors: List[str] = []
    warnings: List[str] = []
    blocked = False
    block_reason = ""

    if not entry.paper_only:
        errors.append("missing_paper_only_flag")
        blocked = True
        block_reason = "missing_paper_only_flags"
    if not entry.no_real_orders:
        errors.append("missing_no_real_orders_flag")
        blocked = True
        block_reason = "missing_paper_only_flags"
    if not entry.no_broker:
        errors.append("missing_no_broker_flag")
        blocked = True
        block_reason = "missing_no_broker_flags"
    if not entry.not_investment_advice:
        errors.append("missing_not_investment_advice_flag")
        blocked = True
        block_reason = "missing_not_investment_advice_flags"
    if not entry.journal_only:
        errors.append("missing_journal_only_flag")
        blocked = True
        block_reason = "malformed_journal_entry"
    if entry.state not in JOURNAL_ENTRY_STATES:
        errors.append(f"invalid_state: {entry.state}")
        blocked = True
        block_reason = "malformed_journal_entry"
    if entry.state in ("PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED") and not entry.evidence_refs:
        warnings.append("paper_decision_without_evidence")
    if not entry.date_label:
        warnings.append("missing_date_label")
    if entry.deterministic_timestamp_policy != "date_label_only_no_wall_clock":
        warnings.append("non_deterministic_timestamp_policy")

    return JournalValidationResult(
        is_valid=len(errors) == 0,
        entry_id=entry.entry_id,
        errors=errors,
        warnings=warnings,
        blocked=blocked,
        block_reason=block_reason,
    )


def create_journal_book(
    book_id: str = "",
    period_label: str = "",
    entries: Optional[List[DecisionJournalEntry]] = None,
) -> DecisionJournalBook:
    """Create a DecisionJournalBook from a list of entries."""
    entries = entries or []
    book = DecisionJournalBook(
        book_id=book_id or f"JB-{period_label}",
        period_label=period_label,
        entries=list(entries),
        entry_count=len(entries),
        open_decisions=sum(1 for e in entries if e.state in ("OBSERVE", "WAIT", "REVIEW_REQUIRED")),
        blocked_decisions=sum(1 for e in entries if e.state == "BLOCKED"),
        paper_plan_count=sum(1 for e in entries if e.state == "PAPER_PLAN_READY"),
        paper_entry_count=sum(1 for e in entries if e.state == "PAPER_ENTRY_ALLOWED"),
        reduce_risk_count=sum(1 for e in entries if e.state == "REDUCE_RISK"),
        no_trade_count=sum(1 for e in entries if e.state == "NO_TRADE"),
    )
    return book


def _score_dimension(entry: DecisionJournalEntry, dimension: str) -> float:
    """Score a single review dimension for a journal entry. Returns 0.0-1.0."""
    if dimension == "market_regime_alignment":
        return 1.0 if entry.market_regime in ("BULL", "WATCH") else 0.5
    if dimension == "evidence_completeness":
        return 1.0 if entry.evidence_refs else 0.3
    if dimension == "execution_discipline":
        return 1.0 if entry.state in ALLOWED_JOURNAL_ACTIONS else 0.0
    if dimension == "blocked_condition_respect":
        return 0.0 if entry.state in ("PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED") and not entry.evidence_refs else 1.0
    if dimension == "risk_budget_usage":
        return 1.0 if entry.risk_budget_usage_pct <= 80.0 else 0.3
    if dimension == "position_sizing_quality":
        return 1.0 if 0.0 < entry.planned_size_pct <= 25.0 else 0.5
    if dimension == "stop_loss_quality":
        return 1.0 if entry.stop_loss_pct > 0.0 else 0.2
    if dimension == "take_profit_quality":
        return 1.0 if entry.take_profit_pct > 0.0 else 0.4
    if dimension == "journal_completeness":
        return 1.0 if entry.rationale else 0.2
    if dimension == "audit_traceability":
        return 1.0 if entry.workflow_id else 0.3
    return 0.7


def _grade_from_score(score: float) -> str:
    """Convert numeric score (0-1) to quality grade."""
    if score >= 0.9:
        return "EXCELLENT"
    if score >= 0.75:
        return "GOOD"
    if score >= 0.6:
        return "ACCEPTABLE"
    if score >= 0.4:
        return "REVIEW_REQUIRED"
    if score > 0.0:
        return "POOR"
    return "INVALID"


def _detect_mistakes(entry: DecisionJournalEntry, review_input: DecisionReviewInput) -> List[str]:
    """Detect mistake tags for a journal entry."""
    tags: List[str] = []
    if entry.planned_size_pct > 25.0:
        tags.append("OVERSIZE_POSITION")
    if entry.state in ("PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED") and not entry.evidence_refs:
        tags.append("MISSING_EVIDENCE")
    if entry.state == "BLOCKED" and entry.block_reason == "":
        tags.append("IGNORE_BLOCK_REASON")
    if review_input.total_exposure_pct > 80.0:
        tags.append("OVER_CONCENTRATION")
    if review_input.cash_reserve_pct < 10.0:
        tags.append("LOW_CASH_RESERVE")
    if entry.market_regime in ("BEAR", "BLOCKED", "RISK_OFF") and entry.state in ("PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED"):
        tags.append("IGNORE_MARKET_REGIME")
    if entry.stop_loss_pct == 0.0 and entry.state in ("PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED"):
        tags.append("NO_CLEAR_STOP")
    if entry.take_profit_pct == 0.0 and entry.state in ("PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED"):
        tags.append("NO_CLEAR_TAKE_PROFIT")
    if not entry.rationale:
        tags.append("MISSING_EVIDENCE")
    if not tags:
        tags.append("NO_MISTAKE_FOUND")
    return list(dict.fromkeys(tags))


def run_review(review_input: DecisionReviewInput) -> DecisionReviewResult:
    """Run a decision review for a journal book. Returns DecisionReviewResult."""
    if not review_input.source_workflow_id:
        return DecisionReviewResult(
            review_type=review_input.review_type,
            date_label=review_input.date_label,
            source_workflow_id="",
            review_grade="INVALID",
            blocked=True,
            block_reason="review_without_source_workflow_id",
            findings=["Review blocked: missing source_workflow_id"],
        )

    entries = []
    if review_input.journal_book:
        entries = review_input.journal_book.entries

    all_dim_scores: Dict[str, float] = {}
    all_mistakes: List[str] = []
    all_findings: List[str] = []
    all_actions: List[str] = []

    for dim in REVIEW_DIMENSIONS:
        if entries:
            scores = [_score_dimension(e, dim) for e in entries]
            all_dim_scores[dim] = sum(scores) / len(scores)
        else:
            all_dim_scores[dim] = 0.8

    for entry in entries:
        tags = _detect_mistakes(entry, review_input)
        all_mistakes.extend(tags)

    all_mistakes = list(dict.fromkeys(all_mistakes)) if all_mistakes else ["NO_MISTAKE_FOUND"]

    avg_score = sum(all_dim_scores.values()) / len(all_dim_scores) if all_dim_scores else 0.8
    grade = _grade_from_score(avg_score)

    if review_input.total_exposure_pct > 80.0:
        all_findings.append("OVER_CONCENTRATION: total exposure exceeds 80%")
        all_actions.append("Reduce position sizes to bring total exposure below 80%")
    if review_input.cash_reserve_pct < 10.0:
        all_findings.append("LOW_CASH_RESERVE: cash reserve below 10%")
        all_actions.append("Rebuild cash reserve to at least 20%")
    if review_input.risk_budget_usage_pct > 90.0:
        all_findings.append("RISK_BUDGET_EXCEEDED: risk budget usage above 90%")
        all_actions.append("Reduce risk exposure before adding new positions")
    if not entries:
        all_findings.append("EMPTY_JOURNAL: no entries found for review period")

    return DecisionReviewResult(
        review_type=review_input.review_type,
        date_label=review_input.date_label,
        source_workflow_id=review_input.source_workflow_id,
        review_grade=grade,
        dimension_scores=all_dim_scores,
        findings=all_findings,
        action_items=all_actions,
        mistake_tags=all_mistakes,
        quality_score=round(avg_score, 3),
        blocked=False,
        block_reason="",
    )


def build_daily_review(review_input: DecisionReviewInput) -> DailyReviewSummary:
    """Build a DailyReviewSummary from a review input."""
    result = run_review(review_input)
    book = review_input.journal_book or DecisionJournalBook()
    return DailyReviewSummary(
        date_label=review_input.date_label,
        source_workflow_id=review_input.source_workflow_id,
        total_decisions=book.entry_count,
        paper_plan_count=book.paper_plan_count,
        paper_entry_count=book.paper_entry_count,
        reduce_risk_count=book.reduce_risk_count,
        blocked_count=book.blocked_decisions,
        no_trade_count=book.no_trade_count,
        average_quality_score=result.quality_score,
        grade=result.review_grade,
        findings=result.findings,
        action_items=result.action_items,
        mistake_tags=result.mistake_tags,
        market_regime=review_input.market_regime,
        total_exposure_pct=review_input.total_exposure_pct,
        cash_reserve_pct=review_input.cash_reserve_pct,
    )


def build_weekly_review(daily_summaries: List[DailyReviewSummary]) -> WeeklyReviewSummary:
    """Build a WeeklyReviewSummary from a list of DailyReviewSummary."""
    total = sum(d.total_decisions for d in daily_summaries)
    plans = sum(d.paper_plan_count for d in daily_summaries)
    entries = sum(d.paper_entry_count for d in daily_summaries)
    reduces = sum(d.reduce_risk_count for d in daily_summaries)
    blocked = sum(d.blocked_count for d in daily_summaries)
    no_trade = sum(d.no_trade_count for d in daily_summaries)
    avg_q = sum(d.average_quality_score for d in daily_summaries) / len(daily_summaries) if daily_summaries else 0.0
    all_mistakes: List[str] = []
    all_findings: List[str] = []
    all_actions: List[str] = []
    for d in daily_summaries:
        all_mistakes.extend(d.mistake_tags)
        all_findings.extend(d.findings)
        all_actions.extend(d.action_items)
    from collections import Counter
    mistake_counts = Counter(all_mistakes)
    recurring = [t for t, c in mistake_counts.items() if c > 1 and t != "NO_MISTAKE_FOUND"]
    grade = _grade_from_score(avg_q)
    return WeeklyReviewSummary(
        daily_summaries=list(daily_summaries),
        total_decisions=total,
        paper_plan_count=plans,
        paper_entry_count=entries,
        reduce_risk_count=reduces,
        blocked_count=blocked,
        no_trade_count=no_trade,
        average_quality_score=round(avg_q, 3),
        weekly_grade=grade,
        recurring_mistakes=recurring,
        top_findings=list(dict.fromkeys(all_findings))[:5],
        top_action_items=list(dict.fromkeys(all_actions))[:5],
        risk_budget_exceeded=any("RISK_BUDGET" in f for f in all_findings),
        over_concentration_detected=any("OVER_CONCENTRATION" in f for f in all_findings),
        low_cash_reserve_detected=any("LOW_CASH_RESERVE" in f for f in all_findings),
    )


def build_monthly_review(weekly_summaries: List[WeeklyReviewSummary], month_label: str = "") -> MonthlyReviewSummary:
    """Build a MonthlyReviewSummary from a list of WeeklyReviewSummary."""
    total = sum(w.total_decisions for w in weekly_summaries)
    avg_q = sum(w.average_quality_score for w in weekly_summaries) / len(weekly_summaries) if weekly_summaries else 0.0
    all_mistakes: List[str] = []
    for w in weekly_summaries:
        all_mistakes.extend(w.recurring_mistakes)
    from collections import Counter
    mc = Counter(all_mistakes)
    top_mistakes = [t for t, _ in mc.most_common(5)]
    grade = _grade_from_score(avg_q)
    consistency = round(1.0 - (max(w.average_quality_score for w in weekly_summaries) - min(w.average_quality_score for w in weekly_summaries) if len(weekly_summaries) > 1 else 0.0), 3)
    return MonthlyReviewSummary(
        month_label=month_label,
        weekly_summaries=list(weekly_summaries),
        total_decisions=total,
        average_quality_score=round(avg_q, 3),
        monthly_grade=grade,
        top_mistake_tags=top_mistakes,
        improvement_areas=[f"Reduce {t}" for t in top_mistakes[:3]],
        consistency_score=max(0.0, consistency),
    )


def build_quality_score(entry: DecisionJournalEntry, review_input: DecisionReviewInput) -> DecisionQualityScore:
    """Compute quality score for a single journal entry."""
    dim_scores: Dict[str, float] = {}
    for dim in REVIEW_DIMENSIONS:
        dim_scores[dim] = _score_dimension(entry, dim)
    avg = sum(dim_scores.values()) / len(dim_scores)
    grade = _grade_from_score(avg)
    mistakes = _detect_mistakes(entry, review_input)
    strengths = [d for d, s in dim_scores.items() if s >= 0.8]
    weaknesses = [d for d, s in dim_scores.items() if s < 0.5]
    return DecisionQualityScore(
        entry_id=entry.entry_id,
        date_label=entry.date_label,
        grade=grade,
        score=round(avg, 3),
        dimension_scores=dim_scores,
        mistake_tags=mistakes,
        strengths=strengths,
        weaknesses=weaknesses,
    )


def build_evidence_link(
    entry: DecisionJournalEntry,
    workflow_id: str,
    evidence_type: str = "workflow_result",
    evidence_summary: str = "",
) -> PaperDecisionEvidenceLink:
    """Build a PaperDecisionEvidenceLink from a journal entry and workflow id."""
    return PaperDecisionEvidenceLink(
        link_id=f"EL-{entry.entry_id}-{workflow_id}",
        entry_id=entry.entry_id,
        workflow_id=workflow_id,
        evidence_type=evidence_type,
        evidence_ref=f"workflow/{workflow_id}",
        evidence_summary=evidence_summary or f"Evidence from workflow {workflow_id}",
        evidence_date_label=entry.date_label,
    )


def build_audit_trail(
    period_label: str,
    entries: List[DecisionJournalEntry],
    review_results: Optional[List[DecisionReviewResult]] = None,
) -> JournalAuditTrail:
    """Build a JournalAuditTrail from journal entries and review results."""
    review_results = review_results or []
    events: List[Dict[str, Any]] = []
    for entry in entries:
        events.append({
            "event_type": "journal_entry",
            "entry_id": entry.entry_id,
            "date_label": entry.date_label,
            "state": entry.state,
            "symbol": entry.symbol,
        })
    for r in review_results:
        events.append({
            "event_type": "review",
            "date_label": r.date_label,
            "review_type": r.review_type,
            "grade": r.review_grade,
            "source_workflow_id": r.source_workflow_id,
        })
    return JournalAuditTrail(
        trail_id=f"AT-{period_label}",
        period_label=period_label,
        audit_events=events,
        event_count=len(events),
        entry_ids=[e.entry_id for e in entries],
        review_ids=[r.source_workflow_id for r in review_results],
        is_complete=True,
    )


def build_evidence_pack(
    period_label: str,
    entries: List[DecisionJournalEntry],
    workflow_ids: Optional[List[str]] = None,
) -> JournalEvidencePack:
    """Build a JournalEvidencePack for a period."""
    workflow_ids = workflow_ids or []
    links = [build_evidence_link(e, e.workflow_id or "no-workflow") for e in entries if e.workflow_id]
    return JournalEvidencePack(
        pack_id=f"EP-{period_label}",
        period_label=period_label,
        evidence_links=links,
        workflow_ids=list(dict.fromkeys(workflow_ids + [e.workflow_id for e in entries if e.workflow_id])),
        entry_ids=[e.entry_id for e in entries],
        evidence_count=len(links),
    )


def build_export_manifest(
    period_label: str,
    export_path: str,
    entries: List[DecisionJournalEntry],
    review_count: int = 0,
    evidence_count: int = 0,
    audit_count: int = 0,
) -> JournalExportManifest:
    """Build a JournalExportManifest for an export operation."""
    if not is_safe_output_path(export_path):
        export_path = "reports/"
    return JournalExportManifest(
        manifest_id=f"EM-{period_label}",
        export_date_label=period_label,
        export_path=export_path,
        included_periods=[period_label],
        entry_count=len(entries),
        review_count=review_count,
        evidence_count=evidence_count,
        audit_trail_count=audit_count,
        format="json",
    )


def build_dashboard(
    period_label: str,
    book: DecisionJournalBook,
    weekly_review: Optional[WeeklyReviewSummary] = None,
) -> JournalDashboard:
    """Build a JournalDashboard payload."""
    grade = "ACCEPTABLE"
    top_mistakes: List[str] = []
    key_findings: List[str] = []
    avg_score = 0.0
    open_actions = 0
    if weekly_review:
        grade = weekly_review.weekly_grade
        top_mistakes = weekly_review.recurring_mistakes[:3]
        key_findings = weekly_review.top_findings[:3]
        avg_score = weekly_review.average_quality_score
        open_actions = len(weekly_review.top_action_items)
    return JournalDashboard(
        dashboard_id=f"DB-{period_label}",
        period_label=period_label,
        total_entries=book.entry_count,
        open_decisions=book.open_decisions,
        reviewed_decisions=book.entry_count - book.open_decisions,
        average_quality_score=avg_score,
        overall_grade=grade,
        top_mistakes=top_mistakes,
        key_findings=key_findings,
        action_items_open=open_actions,
    )


def build_review_checklist(review_input: DecisionReviewInput) -> ReviewChecklist:
    """Build a ReviewChecklist for a review session."""
    items = [
        {"item": "Verify paper_only flags", "required": True},
        {"item": "Verify no_broker flags", "required": True},
        {"item": "Check source_workflow_id present", "required": True},
        {"item": "Review all journal entries", "required": True},
        {"item": "Score all 20 review dimensions", "required": True},
        {"item": "Tag mistakes", "required": True},
        {"item": "Create action items for findings", "required": True},
        {"item": "Verify no forbidden words in output", "required": True},
        {"item": "Confirm audit trail complete", "required": True},
        {"item": "Check export path is safe", "required": True},
    ]
    return ReviewChecklist(
        checklist_id=f"CL-{review_input.date_label}",
        review_type=review_input.review_type,
        date_label=review_input.date_label,
        items=items,
        completed_count=len(items),
        total_count=len(items),
        all_complete=True,
    )


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata dict."""
    return {
        "version": "1.8.9",
        "release_name": "Paper Decision Journal & Review Loop",
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "journal_entry_states_count": 16,
        "review_dimensions_count": 20,
        "mistake_tags_count": 18,
        "quality_grades_count": 6,
    }
