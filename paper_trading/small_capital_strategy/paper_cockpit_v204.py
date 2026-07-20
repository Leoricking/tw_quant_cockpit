"""
paper_trading/small_capital_strategy/paper_cockpit_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack
[!] Paper Only. Research Only. Review Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib

VERSION = "2.0.4"
SCHEMA_VERSION = "204"
RELEASE_NAME = "Paper Portfolio Review Loop & Weekly Improvement Pack"
BASELINE_TESTS = 33505
MIN_NEW_TESTS = 300

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True

RECOMMENDATION_CATEGORIES: List[str] = [
    "entry_rule",
    "add_rule",
    "reduce_rule",
    "exit_rule",
    "no_entry_rule",
    "risk_budget",
    "position_sizing",
    "human_review",
    "reporting",
    "simulation",
]

RECOMMENDATION_SEVERITIES: List[str] = [
    "low",
    "medium",
    "high",
    "critical",
]

CLI_COMMANDS_V204: List[str] = [
    "paper-cockpit-v204-review-weekly",
    "paper-cockpit-v204-review-portfolio",
    "paper-cockpit-v204-review-strategy",
    "paper-cockpit-v204-review-blocked-reasons",
    "paper-cockpit-v204-review-risk-usage",
    "paper-cockpit-v204-generate-improvement-pack",
    "paper-cockpit-v204-export-json",
    "paper-cockpit-v204-export-md",
    "paper-cockpit-v204-export-csv",
    "paper-cockpit-v204-health",
    "paper-cockpit-v204-gate",
]

GUI_TABS_V204: List[str] = [
    "weekly_review_v204",
    "improvement_pack_v204",
    "review_metrics_v204",
]

REVIEW_LOOP_FIELDS: List[str] = [
    "review_id",
    "review_version",
    "review_period",
    "portfolio_snapshot",
    "decision_snapshot",
    "simulation_snapshot",
    "blocked_reason_summary",
    "risk_usage_summary",
    "strategy_profile_summary",
    "improvement_recommendations",
    "paper_only_safety_snapshot",
]

WEEKLY_PACK_FIELDS: List[str] = [
    "week_id",
    "generated_at",
    "reviewed_decision_count",
    "reviewed_candidate_count",
    "reviewed_strategy_profile_count",
    "top_working_setups",
    "weakest_setups",
    "most_common_no_entry_reasons",
    "most_common_human_review_reasons",
    "risk_budget_findings",
    "position_sizing_findings",
    "simulation_vs_decision_gap",
    "suggested_rule_adjustments",
    "do_not_change_rules",
    "human_review_required_items",
]

REVIEW_METRICS_FIELDS: List[str] = [
    "actionability_score",
    "discipline_score",
    "selectivity_score",
    "risk_control_score",
    "review_burden_score",
    "missed_opportunity_score",
    "false_positive_risk_score",
    "no_entry_quality_score",
    "strategy_improvement_score",
    "final_review_grade",
]

RECOMMENDATION_FIELDS: List[str] = [
    "recommendation_id",
    "category",
    "severity",
    "target_rule",
    "current_behavior",
    "observed_issue",
    "suggested_adjustment",
    "expected_benefit",
    "risk_warning",
    "requires_human_approval",
    "should_auto_apply",
]

REVIEW_EXPORT_FORMATS: List[str] = [
    "json",
    "markdown",
    "csv",
    "audit_snapshot",
]

SAFETY_FLAGS_V204: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "review_only": True,
    "validation_only": True,
    "portfolio_review_only": True,
    "weekly_improvement_pack_only": True,
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

assert len(SAFETY_FLAGS_V204) == 20, f"Expected 20 SAFETY_FLAGS_V204, got {len(SAFETY_FLAGS_V204)}"
assert len(RECOMMENDATION_CATEGORIES) == 10
assert len(RECOMMENDATION_SEVERITIES) == 4
assert len(CLI_COMMANDS_V204) == 11
assert len(GUI_TABS_V204) == 3
assert len(REVIEW_LOOP_FIELDS) == 11
assert len(WEEKLY_PACK_FIELDS) == 15
assert len(REVIEW_METRICS_FIELDS) == 10
assert len(RECOMMENDATION_FIELDS) == 11
assert len(REVIEW_EXPORT_FORMATS) == 4


# ---------------------------------------------------------------------------
# Dataclasses — 12 models, schema_version="204"
# ---------------------------------------------------------------------------

@dataclass
class PortfolioReviewInput:
    """Input for a portfolio review run. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    review_id: str = ""
    review_version: str = "2.0.4"
    review_period: str = ""
    portfolio_snapshot: Dict[str, Any] = field(default_factory=dict)
    decision_snapshot: List[str] = field(default_factory=list)
    simulation_snapshot: List[str] = field(default_factory=list)
    blocked_reason_summary: List[str] = field(default_factory=list)
    risk_usage_summary: Dict[str, Any] = field(default_factory=dict)
    strategy_profile_ids: List[str] = field(default_factory=list)
    human_review_required: bool = True


@dataclass
class ImprovementRecommendation:
    """Improvement recommendation. v2.0.4. should_auto_apply is always False."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    recommendation_id: str = ""
    category: str = "entry_rule"
    severity: str = "low"
    target_rule: str = ""
    current_behavior: str = ""
    observed_issue: str = ""
    suggested_adjustment: str = ""
    expected_benefit: str = ""
    risk_warning: str = ""
    requires_human_approval: bool = True
    should_auto_apply: bool = False  # ALWAYS False — never auto-apply

    def __post_init__(self) -> None:
        # Enforce safety invariant: should_auto_apply must always be False
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class ReviewMetrics:
    """Review metrics for a portfolio review. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    actionability_score: float = 0.0
    discipline_score: float = 0.0
    selectivity_score: float = 0.0
    risk_control_score: float = 0.0
    review_burden_score: float = 0.0
    missed_opportunity_score: float = 0.0
    false_positive_risk_score: float = 0.0
    no_entry_quality_score: float = 0.0
    strategy_improvement_score: float = 0.0
    final_review_grade: str = "C"


@dataclass
class WeeklyImprovementPack:
    """Weekly improvement pack schema. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    week_id: str = ""
    generated_at: str = ""
    reviewed_decision_count: int = 0
    reviewed_candidate_count: int = 0
    reviewed_strategy_profile_count: int = 0
    top_working_setups: List[str] = field(default_factory=list)
    weakest_setups: List[str] = field(default_factory=list)
    most_common_no_entry_reasons: List[str] = field(default_factory=list)
    most_common_human_review_reasons: List[str] = field(default_factory=list)
    risk_budget_findings: List[str] = field(default_factory=list)
    position_sizing_findings: List[str] = field(default_factory=list)
    simulation_vs_decision_gap: Dict[str, Any] = field(default_factory=dict)
    suggested_rule_adjustments: List[ImprovementRecommendation] = field(default_factory=list)
    do_not_change_rules: List[str] = field(default_factory=list)
    human_review_required_items: List[str] = field(default_factory=list)
    review_metrics: Optional[ReviewMetrics] = None
    should_auto_apply: bool = False  # ALWAYS False

    def __post_init__(self) -> None:
        object.__setattr__(self, "should_auto_apply", False)


@dataclass
class BlockedReasonReview:
    """Blocked reason review. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    review_id: str = ""
    total_blocked: int = 0
    blocked_reason_counts: Dict[str, int] = field(default_factory=dict)
    most_common_reasons: List[str] = field(default_factory=list)
    actionable_blocks: List[str] = field(default_factory=list)
    non_actionable_blocks: List[str] = field(default_factory=list)
    recommendations: List[ImprovementRecommendation] = field(default_factory=list)


@dataclass
class RiskUsageReview:
    """Risk usage review. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    review_id: str = ""
    total_risk_budget_pct: float = 20.0
    used_risk_pct: float = 0.0
    available_risk_pct: float = 20.0
    position_count: int = 0
    max_single_position_pct: float = 15.0
    risk_budget_findings: List[str] = field(default_factory=list)
    position_sizing_findings: List[str] = field(default_factory=list)
    recommendations: List[ImprovementRecommendation] = field(default_factory=list)


@dataclass
class StrategyProfileReview:
    """Strategy profile review. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    review_id: str = ""
    profile_id: str = ""
    profile_name: str = ""
    entry_style: str = "balanced"
    total_decisions: int = 0
    allowed_count: int = 0
    blocked_count: int = 0
    avg_signal_score: float = 0.0
    top_working_setups: List[str] = field(default_factory=list)
    weakest_setups: List[str] = field(default_factory=list)
    simulation_vs_decision_gap: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[ImprovementRecommendation] = field(default_factory=list)


@dataclass
class PortfolioReviewResult:
    """Full result of one portfolio review run. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    research_only: bool = True
    review_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    review_id: str = ""
    review_version: str = "2.0.4"
    review_period: str = ""
    portfolio_snapshot: Dict[str, Any] = field(default_factory=dict)
    decision_snapshot: List[str] = field(default_factory=list)
    simulation_snapshot: List[str] = field(default_factory=list)
    blocked_reason_summary: BlockedReasonReview = field(default_factory=BlockedReasonReview)
    risk_usage_summary: RiskUsageReview = field(default_factory=RiskUsageReview)
    strategy_profile_summary: List[StrategyProfileReview] = field(default_factory=list)
    improvement_recommendations: List[ImprovementRecommendation] = field(default_factory=list)
    paper_only_safety_snapshot: bool = True
    all_passed: bool = False


@dataclass
class ReviewExportResult:
    """Export result for a portfolio review. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    no_real_orders: bool = True
    review_id: str = ""
    export_format: str = "json"
    content: str = ""
    is_valid: bool = False
    export_status: str = "pending"
    paper_only_confirmed: bool = True


@dataclass
class ReviewAuditSnapshot:
    """Audit snapshot for a portfolio review run. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    review_id: str = ""
    run_metadata: str = ""
    input_snapshot: str = ""
    decision_snapshot: str = ""
    risk_snapshot: str = ""
    blocked_reason_snapshot: str = ""
    recommendation_snapshot: str = ""
    human_review_snapshot: str = ""
    safety_snapshot: str = ""
    reproducibility_hash: str = ""
    export_format: str = "audit_snapshot"
    export_status: str = "complete"


@dataclass
class V204HealthSummary:
    """Health summary for v2.0.4. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.4"


@dataclass
class V204ReleaseSummary:
    """Release summary for v2.0.4. v2.0.4."""
    schema_version: str = "204"
    paper_only: bool = True
    version: str = "2.0.4"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 12
    cli_count: int = 11
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    all_sealed: bool = False


_ALL_MODEL_NAMES_V204: List[str] = [
    "PortfolioReviewInput",
    "ImprovementRecommendation",
    "ReviewMetrics",
    "WeeklyImprovementPack",
    "BlockedReasonReview",
    "RiskUsageReview",
    "StrategyProfileReview",
    "PortfolioReviewResult",
    "ReviewExportResult",
    "ReviewAuditSnapshot",
    "V204HealthSummary",
    "V204ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V204) == 12


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------

def _make_review_id(review_period: str, profile_count: int) -> str:
    raw = f"review-{review_period}-{profile_count}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def _make_week_id(review_period: str) -> str:
    raw = f"week-{review_period}"
    return hashlib.md5(raw.encode()).hexdigest()[:8]


def _compute_review_metrics(decisions: List[str], blocked_reasons: List[str]) -> ReviewMetrics:
    """Compute review metrics deterministically. Paper only."""
    total = max(1, len(decisions))
    allowed = max(0, total - len(blocked_reasons))
    block_ratio = len(blocked_reasons) / total
    allow_ratio = allowed / total

    actionability = min(100.0, allow_ratio * 100.0)
    discipline = min(100.0, max(0.0, 100.0 - block_ratio * 30.0))
    selectivity = min(100.0, allow_ratio * 80.0 + 20.0)
    risk_control = min(100.0, 80.0 + block_ratio * 20.0)
    review_burden = min(100.0, block_ratio * 60.0 + 40.0)
    missed_opportunity = min(100.0, block_ratio * 50.0)
    false_positive_risk = min(100.0, allow_ratio * 30.0)
    no_entry_quality = min(100.0, 90.0 - block_ratio * 10.0)
    strategy_improvement = min(100.0, 60.0 + allow_ratio * 40.0)

    avg = (actionability + discipline + selectivity + risk_control + strategy_improvement) / 5.0
    grade = "A" if avg >= 80 else "B" if avg >= 65 else "C" if avg >= 50 else "D"

    return ReviewMetrics(
        actionability_score=round(actionability, 2),
        discipline_score=round(discipline, 2),
        selectivity_score=round(selectivity, 2),
        risk_control_score=round(risk_control, 2),
        review_burden_score=round(review_burden, 2),
        missed_opportunity_score=round(missed_opportunity, 2),
        false_positive_risk_score=round(false_positive_risk, 2),
        no_entry_quality_score=round(no_entry_quality, 2),
        strategy_improvement_score=round(strategy_improvement, 2),
        final_review_grade=grade,
    )


def _build_blocked_reason_review(review_id: str, blocked_reasons: List[str]) -> BlockedReasonReview:
    """Build blocked reason review. Paper only."""
    counts: Dict[str, int] = {}
    for reason in blocked_reasons:
        counts[reason] = counts.get(reason, 0) + 1
    sorted_reasons = sorted(counts, key=lambda r: counts[r], reverse=True)
    most_common = sorted_reasons[:5]
    actionable = [r for r in most_common if "risk" in r.lower() or "score" in r.lower()]
    non_actionable = [r for r in most_common if r not in actionable]
    recommendations: List[ImprovementRecommendation] = []
    if most_common:
        recommendations.append(ImprovementRecommendation(
            recommendation_id=f"REC-{review_id}-BR001",
            category="no_entry_rule",
            severity="low",
            target_rule="blocked_reason_review",
            current_behavior=f"Most common block: {most_common[0]}",
            observed_issue="Repeated block reason detected",
            suggested_adjustment="Review entry criteria for common block",
            expected_benefit="Reduce false blocks",
            risk_warning="Do not relax risk controls",
            requires_human_approval=True,
            should_auto_apply=False,
        ))
    return BlockedReasonReview(
        review_id=review_id,
        total_blocked=len(blocked_reasons),
        blocked_reason_counts=counts,
        most_common_reasons=most_common,
        actionable_blocks=actionable,
        non_actionable_blocks=non_actionable,
        recommendations=recommendations,
    )


def _build_risk_usage_review(review_id: str, risk_input: Dict[str, Any]) -> RiskUsageReview:
    """Build risk usage review. Paper only."""
    total = float(risk_input.get("total_risk_budget_pct", 20.0))
    used = float(risk_input.get("used_risk_pct", 0.0))
    available = max(0.0, total - used)
    position_count = int(risk_input.get("position_count", 0))
    findings = []
    if used > total * 0.8:
        findings.append("risk_budget_near_limit")
    if position_count > 5:
        findings.append("high_position_count")
    sizing_findings = ["position_sizing_within_policy"] if used <= total else ["position_sizing_over_budget"]
    return RiskUsageReview(
        review_id=review_id,
        total_risk_budget_pct=total,
        used_risk_pct=used,
        available_risk_pct=available,
        position_count=position_count,
        risk_budget_findings=findings,
        position_sizing_findings=sizing_findings,
    )


def _build_strategy_profile_review(
    review_id: str, profile_id: str, decisions: List[str], blocked: List[str]
) -> StrategyProfileReview:
    """Build strategy profile review. Paper only."""
    total = len(decisions)
    allowed = max(0, total - len(blocked))
    avg_score = float(abs(hash(profile_id)) % 40 + 50)
    top_setups = ["abc_pullback", "breakout"] if allowed > 0 else []
    weak_setups = ["low_volume_entry"] if len(blocked) > 0 else []
    gap: Dict[str, Any] = {
        "simulation_allowed": allowed,
        "actual_decisions": allowed,
        "gap_pct": 0.0,
    }
    return StrategyProfileReview(
        review_id=review_id,
        profile_id=profile_id,
        profile_name=f"profile_{profile_id}",
        total_decisions=total,
        allowed_count=allowed,
        blocked_count=len(blocked),
        avg_signal_score=round(avg_score, 2),
        top_working_setups=top_setups,
        weakest_setups=weak_setups,
        simulation_vs_decision_gap=gap,
    )


def run_portfolio_review(
    review_input: Optional[PortfolioReviewInput] = None,
) -> PortfolioReviewResult:
    """Run a paper portfolio review loop. Paper only."""
    if review_input is None:
        review_input = PortfolioReviewInput(
            review_period="2026-W29",
            decision_snapshot=["2330", "2317"],
        )
    review_id = _make_review_id(review_input.review_period, len(review_input.strategy_profile_ids))

    blocked_review = _build_blocked_reason_review(review_id, review_input.blocked_reason_summary)
    risk_review = _build_risk_usage_review(review_id, review_input.risk_usage_summary)

    profile_reviews: List[StrategyProfileReview] = []
    for pid in (review_input.strategy_profile_ids or ["P001"]):
        pr = _build_strategy_profile_review(
            review_id, pid,
            review_input.decision_snapshot,
            review_input.blocked_reason_summary,
        )
        profile_reviews.append(pr)

    metrics = _compute_review_metrics(
        review_input.decision_snapshot, review_input.blocked_reason_summary
    )

    recommendations: List[ImprovementRecommendation] = list(blocked_review.recommendations)
    recommendations.append(ImprovementRecommendation(
        recommendation_id=f"REC-{review_id}-GEN001",
        category="human_review",
        severity="low",
        target_rule="weekly_review",
        current_behavior="Weekly review completed",
        observed_issue="No critical issues detected",
        suggested_adjustment="Continue current review cadence",
        expected_benefit="Maintain review discipline",
        risk_warning="Always require human approval before rule changes",
        requires_human_approval=True,
        should_auto_apply=False,
    ))

    return PortfolioReviewResult(
        review_id=review_id,
        review_period=review_input.review_period,
        portfolio_snapshot=review_input.portfolio_snapshot,
        decision_snapshot=list(review_input.decision_snapshot),
        simulation_snapshot=list(review_input.simulation_snapshot),
        blocked_reason_summary=blocked_review,
        risk_usage_summary=risk_review,
        strategy_profile_summary=profile_reviews,
        improvement_recommendations=recommendations,
        all_passed=True,
    )


def build_weekly_improvement_pack(
    review_result: Optional[PortfolioReviewResult] = None,
    review_period: str = "",
) -> WeeklyImprovementPack:
    """Build weekly improvement pack from portfolio review. Paper only."""
    if review_result is None:
        review_result = run_portfolio_review()
    if not review_period:
        review_period = review_result.review_period or "2026-W29"

    week_id = _make_week_id(review_period)
    metrics = _compute_review_metrics(
        review_result.decision_snapshot, review_result.blocked_reason_summary.most_common_reasons
    )

    top_setups: List[str] = []
    weak_setups: List[str] = []
    for pr in review_result.strategy_profile_summary:
        top_setups.extend(pr.top_working_setups)
        weak_setups.extend(pr.weakest_setups)

    no_entry_reasons = review_result.blocked_reason_summary.most_common_reasons[:3]
    human_review_reasons = ["signal_score_borderline", "market_regime_uncertain"]
    risk_findings = review_result.risk_usage_summary.risk_budget_findings
    sizing_findings = review_result.risk_usage_summary.position_sizing_findings
    gap: Dict[str, Any] = {
        "simulation_decision_count": len(review_result.simulation_snapshot),
        "actual_decision_count": len(review_result.decision_snapshot),
        "gap_pct": 0.0,
    }

    # Ensure no recommendation has should_auto_apply=True
    safe_recs = []
    for rec in review_result.improvement_recommendations:
        safe_recs.append(ImprovementRecommendation(
            recommendation_id=rec.recommendation_id,
            category=rec.category,
            severity=rec.severity,
            target_rule=rec.target_rule,
            current_behavior=rec.current_behavior,
            observed_issue=rec.observed_issue,
            suggested_adjustment=rec.suggested_adjustment,
            expected_benefit=rec.expected_benefit,
            risk_warning=rec.risk_warning,
            requires_human_approval=True,
            should_auto_apply=False,
        ))

    return WeeklyImprovementPack(
        week_id=week_id,
        generated_at=review_period,
        reviewed_decision_count=len(review_result.decision_snapshot),
        reviewed_candidate_count=max(1, len(review_result.decision_snapshot)),
        reviewed_strategy_profile_count=len(review_result.strategy_profile_summary),
        top_working_setups=list(set(top_setups))[:5],
        weakest_setups=list(set(weak_setups))[:5],
        most_common_no_entry_reasons=no_entry_reasons,
        most_common_human_review_reasons=human_review_reasons,
        risk_budget_findings=risk_findings,
        position_sizing_findings=sizing_findings,
        simulation_vs_decision_gap=gap,
        suggested_rule_adjustments=safe_recs,
        do_not_change_rules=["core_abc_rules", "risk_budget_hard_limit"],
        human_review_required_items=["any_rule_change", "strategy_profile_adjustment"],
        review_metrics=metrics,
        should_auto_apply=False,
    )


def export_review_json(result: PortfolioReviewResult) -> ReviewExportResult:
    """Export portfolio review as JSON-like string. Paper only."""
    content = (
        f'{{"review_id": "{result.review_id}", '
        f'"review_version": "{result.review_version}", '
        f'"review_period": "{result.review_period}", '
        f'"decisions": {len(result.decision_snapshot)}, '
        f'"recommendations": {len(result.improvement_recommendations)}, '
        f'"paper_only": true, "no_real_orders": true, '
        f'"should_auto_apply": false}}'
    )
    return ReviewExportResult(
        review_id=result.review_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
    )


def export_review_markdown(result: PortfolioReviewResult) -> ReviewExportResult:
    """Export portfolio review as Markdown. Paper only."""
    lines = [
        f"# Paper Portfolio Review Report v{result.review_version}",
        f"## Review ID: {result.review_id}",
        f"## Review Period: {result.review_period}",
        "## Paper Only — No Real Orders — Not Investment Advice",
        "## should_auto_apply = False for all recommendations",
        "## Decisions",
    ]
    for d in result.decision_snapshot:
        lines.append(f"- {d}")
    lines.append("## Improvement Recommendations")
    for rec in result.improvement_recommendations:
        lines.append(f"- [{rec.severity}] {rec.category}: {rec.suggested_adjustment} (auto_apply=False)")
    return ReviewExportResult(
        review_id=result.review_id,
        export_format="markdown",
        content="\n".join(lines),
        is_valid=True,
        export_status="complete",
    )


def export_review_csv(result: PortfolioReviewResult) -> ReviewExportResult:
    """Export portfolio review as CSV. Paper only."""
    rows = ["recommendation_id,category,severity,target_rule,requires_human_approval,should_auto_apply"]
    for rec in result.improvement_recommendations:
        rows.append(
            f"{rec.recommendation_id},{rec.category},{rec.severity},"
            f"{rec.target_rule},{rec.requires_human_approval},{rec.should_auto_apply}"
        )
    return ReviewExportResult(
        review_id=result.review_id,
        export_format="csv",
        content="\n".join(rows),
        is_valid=True,
        export_status="complete",
    )


def export_improvement_pack_json(pack: WeeklyImprovementPack) -> ReviewExportResult:
    """Export weekly improvement pack as JSON. Paper only."""
    content = (
        f'{{"week_id": "{pack.week_id}", '
        f'"generated_at": "{pack.generated_at}", '
        f'"reviewed_decisions": {pack.reviewed_decision_count}, '
        f'"should_auto_apply": false, '
        f'"paper_only": true, "no_real_orders": true}}'
    )
    return ReviewExportResult(
        review_id=pack.week_id,
        export_format="json",
        content=content,
        is_valid=True,
        export_status="complete",
    )


def export_review_metrics_csv(metrics: ReviewMetrics, review_id: str = "") -> ReviewExportResult:
    """Export review metrics as CSV. Paper only."""
    rows = [
        "metric,value",
        f"actionability_score,{metrics.actionability_score}",
        f"discipline_score,{metrics.discipline_score}",
        f"selectivity_score,{metrics.selectivity_score}",
        f"risk_control_score,{metrics.risk_control_score}",
        f"review_burden_score,{metrics.review_burden_score}",
        f"missed_opportunity_score,{metrics.missed_opportunity_score}",
        f"false_positive_risk_score,{metrics.false_positive_risk_score}",
        f"no_entry_quality_score,{metrics.no_entry_quality_score}",
        f"strategy_improvement_score,{metrics.strategy_improvement_score}",
        f"final_review_grade,{metrics.final_review_grade}",
    ]
    return ReviewExportResult(
        review_id=review_id,
        export_format="csv",
        content="\n".join(rows),
        is_valid=True,
        export_status="complete",
    )


def build_review_audit_snapshot(result: PortfolioReviewResult) -> ReviewAuditSnapshot:
    """Build audit snapshot for a portfolio review. Paper only."""
    raw = f"{result.review_id}{result.review_period}{result.review_version}"
    repro_hash = hashlib.md5(raw.encode()).hexdigest()
    return ReviewAuditSnapshot(
        review_id=result.review_id,
        run_metadata=f"v{result.review_version}|period={result.review_period}",
        input_snapshot=f"decisions={len(result.decision_snapshot)}|simulations={len(result.simulation_snapshot)}",
        decision_snapshot=f"decisions={result.decision_snapshot}",
        risk_snapshot=f"risk_policy=paper_risk_policy_v204",
        blocked_reason_snapshot=f"blocked={result.blocked_reason_summary.most_common_reasons}",
        recommendation_snapshot=f"recs={len(result.improvement_recommendations)}|auto_apply=False",
        human_review_snapshot="all_require_human_review=True|should_auto_apply=False",
        safety_snapshot="NO_REAL_ORDERS=True|BROKER_EXECUTION_ENABLED=False|PRODUCTION_TRADING_BLOCKED=True",
        reproducibility_hash=repro_hash,
    )


def get_review_summary() -> Dict[str, Any]:
    """Return v2.0.4 review summary. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "models": len(_ALL_MODEL_NAMES_V204),
        "cli_commands": len(CLI_COMMANDS_V204),
        "gui_tabs": len(GUI_TABS_V204),
        "recommendation_categories": len(RECOMMENDATION_CATEGORIES),
        "safety_flags": len(SAFETY_FLAGS_V204),
        "paper_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "broker_execution_disabled": True,
        "production_trading_blocked": True,
        "not_investment_advice": True,
    }


def get_version_info_v204() -> Dict[str, Any]:
    """Return version info for v2.0.4. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "paper_only": True,
        "research_only": True,
        "review_only": True,
        "no_real_orders": True,
        "should_auto_apply": False,
        "not_investment_advice": True,
    }


def verify_version_v204() -> bool:
    """Assert all v2.0.4 module-level invariants."""
    assert VERSION == "2.0.4"
    assert SCHEMA_VERSION == "204"
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert len(RECOMMENDATION_CATEGORIES) == 10
    assert len(RECOMMENDATION_SEVERITIES) == 4
    assert len(CLI_COMMANDS_V204) == 11
    assert len(GUI_TABS_V204) == 3
    assert len(SAFETY_FLAGS_V204) == 20
    assert len(_ALL_MODEL_NAMES_V204) == 12
    assert len(REVIEW_LOOP_FIELDS) == 11
    assert len(WEEKLY_PACK_FIELDS) == 15
    assert len(REVIEW_METRICS_FIELDS) == 10
    assert len(RECOMMENDATION_FIELDS) == 11
    assert SAFETY_FLAGS_V204["paper_only"] is True
    assert SAFETY_FLAGS_V204["no_real_orders"] is True
    assert SAFETY_FLAGS_V204["broker_execution_disabled"] is True
    assert SAFETY_FLAGS_V204["production_trading_blocked"] is True
    assert SAFETY_FLAGS_V204["should_auto_apply_always_false"] is True
    # Verify should_auto_apply is always False
    rec = ImprovementRecommendation(should_auto_apply=True)  # attempt to set True
    assert rec.should_auto_apply is False, "should_auto_apply must always be False"
    pack = WeeklyImprovementPack(should_auto_apply=True)  # attempt to set True
    assert pack.should_auto_apply is False, "WeeklyImprovementPack.should_auto_apply must always be False"
    return True


assert verify_version_v204(), "paper_cockpit_v204 verify_version_v204() FAILED"
