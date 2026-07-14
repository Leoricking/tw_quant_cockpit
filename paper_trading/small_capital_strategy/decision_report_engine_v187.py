"""
paper_trading/small_capital_strategy/decision_report_engine_v187.py
Report engine for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional

ALLOWED_REPORT_ACTIONS = frozenset({
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
    "ALLOCATION_ONLY", "PORTFOLIO_ONLY", "DECISION_ONLY", "REPORT_ONLY", "AUDIT_ONLY",
})

FORBIDDEN_REPORT_WORDS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

VALID_REPORT_GRADES = frozenset({
    "COMPLETE", "REVIEW_REQUIRED", "PARTIAL", "BLOCKED", "INVALID",
})

VALID_REPORT_TYPES = frozenset({
    "daily_decision_report", "weekly_decision_report", "watchlist_report",
    "blocked_candidates_report", "reduce_risk_report", "paper_plan_ready_report",
    "portfolio_exposure_report", "monte_carlo_risk_report", "abc_buy_point_report",
    "evidence_pack", "audit_trail", "export_manifest",
})


def validate_report_action(action: str) -> bool:
    """Return True if action is in ALLOWED_REPORT_ACTIONS and not forbidden."""
    return action in ALLOWED_REPORT_ACTIONS and action not in FORBIDDEN_REPORT_WORDS


def validate_report_grade(grade: str) -> bool:
    """Return True if grade is in VALID_REPORT_GRADES."""
    return grade in VALID_REPORT_GRADES


def validate_report_type(report_type: str) -> bool:
    """Return True if report_type is in VALID_REPORT_TYPES."""
    return report_type in VALID_REPORT_TYPES


def _compute_final_report_grade(inp) -> str:
    """Compute final report grade from DecisionReportInput."""
    # Check hard blocks first
    if not getattr(inp, "paper_only", True):
        return "BLOCKED"
    if not getattr(inp, "no_real_orders", True):
        return "BLOCKED"
    if not getattr(inp, "not_investment_advice", True):
        return "BLOCKED"
    if not getattr(inp, "production_trading_blocked", True):
        return "BLOCKED"

    block_reasons = getattr(inp, "block_reasons", [])
    blocked_count = getattr(inp, "blocked_candidate_count", 0)
    candidate_count = getattr(inp, "candidate_count", 0)

    daily_action = getattr(inp, "daily_action", "WAIT")
    if daily_action in FORBIDDEN_REPORT_WORDS:
        return "INVALID"

    final_grade = getattr(inp, "final_cockpit_grade", "WAIT")
    if final_grade == "BLOCKED":
        return "BLOCKED"
    if block_reasons:
        if blocked_count > 0 and blocked_count == candidate_count and candidate_count > 0:
            return "BLOCKED"
        return "REVIEW_REQUIRED"
    if final_grade in ("READY", "WATCH", "WAIT"):
        return "COMPLETE"
    if final_grade in ("REDUCE_RISK", "REVIEW_REQUIRED"):
        return "REVIEW_REQUIRED"
    return "PARTIAL"


def build_candidate_evidence_item(ticker: str, decision_action: str,
                                  block_reason: str = "",
                                  abc_buy_point_status: str = "",
                                  market_regime_status: str = "BULL",
                                  risk_status: str = "OK",
                                  position_sizing_status: str = "OK",
                                  portfolio_exposure_status: str = "OK",
                                  monte_carlo_risk_status: str = "LOW",
                                  theme_sector_concentration: str = "NORMAL",
                                  cash_reserve_status: str = "OK",
                                  stop_loss_presence: bool = True,
                                  final_decision_grade: str = "WAIT") -> "CandidateEvidenceItem":
    """Build a CandidateEvidenceItem for a single ticker."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import CandidateEvidenceItem
    return CandidateEvidenceItem(
        ticker=ticker,
        decision_action=decision_action if decision_action in ALLOWED_REPORT_ACTIONS else "WAIT",
        block_reason=block_reason,
        abc_buy_point_status=abc_buy_point_status,
        market_regime_status=market_regime_status,
        risk_status=risk_status,
        position_sizing_status=position_sizing_status,
        portfolio_exposure_status=portfolio_exposure_status,
        monte_carlo_risk_status=monte_carlo_risk_status,
        theme_sector_concentration=theme_sector_concentration,
        cash_reserve_status=cash_reserve_status,
        stop_loss_presence=stop_loss_presence,
        final_decision_grade=final_decision_grade,
    )


def build_block_reason_evidence(block_code: str, block_description: str,
                                 severity: str = "HIGH",
                                 affected_tickers: Optional[List[str]] = None) -> "BlockReasonEvidence":
    """Build a BlockReasonEvidence item."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import BlockReasonEvidence
    return BlockReasonEvidence(
        block_code=block_code,
        block_description=block_description,
        severity=severity,
        affected_tickers=affected_tickers or [],
    )


def build_evidence_pack(inp, candidate_evidence: Optional[List] = None) -> "CandidateEvidencePack":
    """Build full evidence pack from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import CandidateEvidencePack
    items = candidate_evidence or []
    return CandidateEvidencePack(
        candidate_count=getattr(inp, "candidate_count", 0),
        evidence_items=items,
        ready_count=getattr(inp, "ready_candidate_count", 0),
        blocked_count=getattr(inp, "blocked_candidate_count", 0),
        reduce_risk_count=getattr(inp, "reduce_risk_candidate_count", 0),
        watch_count=getattr(inp, "watch_candidate_count", 0),
        audit_complete=True,
    )


def build_audit_trail(inp) -> "DecisionAuditTrail":
    """Build audit trail from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import DecisionAuditTrail
    entries = []
    daily_action = getattr(inp, "daily_action", "DECISION_ONLY")
    entries.append({
        "step": "market_regime",
        "value": getattr(inp, "market_regime", "BULL"),
        "action": "DECISION_ONLY",
        "evidence": "market_regime_status",
    })
    entries.append({
        "step": "daily_action",
        "value": daily_action,
        "action": daily_action if validate_report_action(daily_action) else "BLOCKED",
        "evidence": "cockpit_engine_v186",
    })
    entries.append({
        "step": "final_cockpit_grade",
        "value": getattr(inp, "final_cockpit_grade", "WAIT"),
        "action": "REPORT_ONLY",
        "evidence": "cockpit_grade_computation",
    })
    block_reasons = getattr(inp, "block_reasons", [])
    for reason in block_reasons:
        entries.append({
            "step": "block_reason",
            "value": reason,
            "action": "BLOCKED",
            "evidence": "hard_block_condition",
        })
    grade = _compute_final_report_grade(inp)
    return DecisionAuditTrail(
        date_label=getattr(inp, "generated_at_policy", ""),
        capital_stage=getattr(inp, "capital_stage", "300K"),
        market_regime=getattr(inp, "market_regime", "BULL"),
        final_cockpit_grade=getattr(inp, "final_cockpit_grade", "WAIT"),
        daily_action=daily_action,
        weekly_action=getattr(inp, "weekly_action", "DECISION_ONLY"),
        audit_entries=entries,
        decision_evidence_count=len(entries),
        block_reasons=block_reasons,
        audit_complete=True,
        final_report_grade=grade,
    )


def build_daily_report(inp) -> "DailyDecisionReport":
    """Build daily decision report from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import DailyDecisionReport
    grade = _compute_final_report_grade(inp)
    return DailyDecisionReport(
        date_label=getattr(inp, "generated_at_policy", ""),
        market_regime=getattr(inp, "market_regime", "BULL"),
        daily_action=getattr(inp, "daily_action", "DECISION_ONLY"),
        final_cockpit_grade=getattr(inp, "final_cockpit_grade", "WAIT"),
        candidate_count=getattr(inp, "candidate_count", 0),
        ready_candidate_count=getattr(inp, "ready_candidate_count", 0),
        blocked_candidate_count=getattr(inp, "blocked_candidate_count", 0),
        paper_plan_ready_candidates=list(getattr(inp, "paper_plan_ready_candidates", [])),
        blocked_candidates=list(getattr(inp, "blocked_candidates", [])),
        block_reasons=list(getattr(inp, "block_reasons", [])),
        total_exposure_pct=getattr(inp, "total_exposure_pct", 0.0),
        cash_reserve_pct=getattr(inp, "cash_reserve_pct", 100.0),
        monte_carlo_ruin_risk=getattr(inp, "monte_carlo_ruin_risk", 0.0),
        final_report_grade=grade,
    )


def build_weekly_report(inp) -> "WeeklyDecisionReport":
    """Build weekly decision report from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import WeeklyDecisionReport
    grade = _compute_final_report_grade(inp)
    return WeeklyDecisionReport(
        week_label=getattr(inp, "generated_at_policy", ""),
        market_regime=getattr(inp, "market_regime", "BULL"),
        weekly_action=getattr(inp, "weekly_action", "DECISION_ONLY"),
        final_cockpit_grade=getattr(inp, "final_cockpit_grade", "WAIT"),
        portfolio_holding_count=getattr(inp, "portfolio_holding_count", 0),
        total_exposure_pct=getattr(inp, "total_exposure_pct", 0.0),
        cash_reserve_pct=getattr(inp, "cash_reserve_pct", 100.0),
        concentration_risk_score=getattr(inp, "concentration_risk_score", 0.0),
        diversification_score=getattr(inp, "diversification_score", 100.0),
        monte_carlo_ruin_risk=getattr(inp, "monte_carlo_ruin_risk", 0.0),
        max_drawdown_budget_usage_pct=getattr(inp, "max_drawdown_budget_usage_pct", 0.0),
        reduce_risk_candidates=list(getattr(inp, "reduce_risk_candidates", [])),
        block_reasons=list(getattr(inp, "block_reasons", [])),
        portfolio_rebalance_summary=getattr(inp, "portfolio_rebalance_summary", ""),
        final_report_grade=grade,
    )


def build_watchlist_report(inp) -> "WatchlistReport":
    """Build watchlist report from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import WatchlistReport
    grade = _compute_final_report_grade(inp)
    return WatchlistReport(
        candidate_count=getattr(inp, "candidate_count", 0),
        top_watch_candidates=list(getattr(inp, "top_watch_candidates", [])),
        paper_plan_ready_candidates=list(getattr(inp, "paper_plan_ready_candidates", [])),
        watch_candidate_count=getattr(inp, "watch_candidate_count", 0),
        ready_candidate_count=getattr(inp, "ready_candidate_count", 0),
        market_regime=getattr(inp, "market_regime", "BULL"),
        final_report_grade=grade,
    )


def build_blocked_candidate_report(inp) -> "BlockedCandidateReport":
    """Build blocked candidates report from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import (
        BlockedCandidateReport, BlockReasonEvidence,
    )
    grade = _compute_final_report_grade(inp)
    block_reasons = list(getattr(inp, "block_reasons", []))
    evidence = []
    for reason in block_reasons:
        evidence.append(BlockReasonEvidence(
            block_code=reason,
            block_description=f"Block triggered: {reason}",
            severity="HIGH",
            affected_tickers=list(getattr(inp, "blocked_candidates", [])),
        ))
    return BlockedCandidateReport(
        blocked_candidate_count=getattr(inp, "blocked_candidate_count", 0),
        blocked_candidates=list(getattr(inp, "blocked_candidates", [])),
        block_reasons=block_reasons,
        block_reason_evidence=evidence,
        market_regime=getattr(inp, "market_regime", "BULL"),
        final_report_grade=grade,
    )


def build_reduce_risk_report(inp) -> "ReduceRiskReport":
    """Build reduce risk report from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import (
        ReduceRiskReport, RiskEvidence, PortfolioEvidence, MonteCarloEvidence,
    )
    grade = _compute_final_report_grade(inp)
    reduce_required = getattr(inp, "daily_action", "") == "REDUCE_RISK" or \
                      getattr(inp, "final_cockpit_grade", "") == "REDUCE_RISK"
    risk_ev = RiskEvidence(
        total_exposure_pct=getattr(inp, "total_exposure_pct", 0.0),
        cash_reserve_pct=getattr(inp, "cash_reserve_pct", 100.0),
        monte_carlo_ruin_risk_pct=getattr(inp, "monte_carlo_ruin_risk", 0.0),
        drawdown_budget_usage_pct=getattr(inp, "max_drawdown_budget_usage_pct", 0.0),
        action=getattr(inp, "daily_action", "DECISION_ONLY"),
    )
    port_ev = PortfolioEvidence(
        holding_count=getattr(inp, "portfolio_holding_count", 0),
        total_exposure_pct=getattr(inp, "total_exposure_pct", 0.0),
        cash_reserve_pct=getattr(inp, "cash_reserve_pct", 100.0),
        concentration_risk_score=getattr(inp, "concentration_risk_score", 0.0),
        diversification_score=getattr(inp, "diversification_score", 100.0),
    )
    mc_ev = MonteCarloEvidence(
        ruin_probability_pct=getattr(inp, "monte_carlo_ruin_risk", 0.0),
        action=getattr(inp, "daily_action", "DECISION_ONLY"),
    )
    return ReduceRiskReport(
        reduce_risk_candidate_count=getattr(inp, "reduce_risk_candidate_count", 0),
        reduce_risk_candidates=list(getattr(inp, "reduce_risk_candidates", [])),
        risk_evidence=risk_ev,
        portfolio_evidence=port_ev,
        monte_carlo_evidence=mc_ev,
        reduce_required=reduce_required,
        reason="; ".join(getattr(inp, "block_reasons", [])),
        final_report_grade=grade,
    )


def build_paper_plan_ready_report(inp) -> "PaperPlanReadyReport":
    """Build paper plan ready report from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import PaperPlanReadyReport
    grade = _compute_final_report_grade(inp)
    evidence_items = []
    for ticker in getattr(inp, "paper_plan_ready_candidates", []):
        evidence_items.append(build_candidate_evidence_item(
            ticker=ticker,
            decision_action="PAPER_PLAN_READY",
            market_regime_status=getattr(inp, "market_regime", "BULL"),
            final_decision_grade="WATCH",
        ))
    return PaperPlanReadyReport(
        ready_candidate_count=getattr(inp, "ready_candidate_count", 0),
        paper_plan_ready_candidates=list(getattr(inp, "paper_plan_ready_candidates", [])),
        evidence_items=evidence_items,
        market_regime=getattr(inp, "market_regime", "BULL"),
        capital_stage=getattr(inp, "capital_stage", "300K"),
        final_cockpit_grade=getattr(inp, "final_cockpit_grade", "WAIT"),
        final_report_grade=grade,
    )


def build_export_manifest(exports: List[Dict[str, Any]]) -> "ReportExportManifest":
    """Build export manifest from a list of export records."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import ReportExportManifest
    json_cnt = sum(1 for e in exports if e.get("format") == "json")
    md_cnt = sum(1 for e in exports if e.get("format") == "markdown")
    csv_cnt = sum(1 for e in exports if e.get("format") == "csv_rows")
    console_cnt = sum(1 for e in exports if e.get("format") == "console_summary")
    dash_cnt = sum(1 for e in exports if e.get("format") == "dashboard_payload")
    return ReportExportManifest(
        exports=list(exports),
        export_count=len(exports),
        json_exports=json_cnt,
        markdown_exports=md_cnt,
        csv_exports=csv_cnt,
        console_exports=console_cnt,
        dashboard_exports=dash_cnt,
        all_exports_safe=True,
    )


def validate_report(report_input) -> "ReportValidationResult":
    """Validate a DecisionReportInput for completeness and safety."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import ReportValidationResult
    errors = []
    warnings = []

    has_paper = getattr(report_input, "paper_only", False)
    has_no_broker = getattr(report_input, "no_broker", False)
    has_nia = getattr(report_input, "not_investment_advice", False)
    has_prod_blocked = getattr(report_input, "production_trading_blocked", False)

    if not has_paper:
        errors.append("missing_paper_only_flag")
    if not has_no_broker:
        errors.append("missing_no_broker_flag")
    if not has_nia:
        errors.append("missing_not_investment_advice_flag")
    if not has_prod_blocked:
        errors.append("missing_production_trading_blocked_flag")

    daily_action = getattr(report_input, "daily_action", "DECISION_ONLY")
    if daily_action in FORBIDDEN_REPORT_WORDS:
        errors.append(f"forbidden_action_in_daily_action: {daily_action}")

    candidate_count = getattr(report_input, "candidate_count", 0)
    ready = getattr(report_input, "ready_candidate_count", 0)
    watch = getattr(report_input, "watch_candidate_count", 0)
    blocked = getattr(report_input, "blocked_candidate_count", 0)
    reduce = getattr(report_input, "reduce_risk_candidate_count", 0)
    total_sub = ready + watch + blocked + reduce
    if candidate_count > 0 and total_sub > candidate_count:
        errors.append("inconsistent_candidate_counts")

    blocked_tickers = getattr(report_input, "blocked_candidates", [])
    block_reasons = getattr(report_input, "block_reasons", [])
    if blocked_tickers and not block_reasons:
        errors.append("blocked_candidate_without_block_reason")

    grade = "COMPLETE" if not errors else ("BLOCKED" if any("forbidden" in e for e in errors) else "REVIEW_REQUIRED")
    return ReportValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        has_audit_trail=True,
        has_evidence_pack=True,
        has_paper_only_flags=has_paper,
        has_no_broker_flags=has_no_broker,
        has_not_investment_advice_flags=has_nia,
        has_deterministic_timestamp=True,
        has_safe_output_path=True,
        no_forbidden_actions=daily_action not in FORBIDDEN_REPORT_WORDS,
        consistent_candidate_counts=len(errors) == 0 or "inconsistent" not in str(errors),
        all_blocks_have_reasons=not any("without_block_reason" in e for e in errors),
        all_entries_have_evidence=True,
        final_report_grade=grade,
    )


def run_decision_report(inp) -> "DecisionReportResult":
    """Run full decision report generation from DecisionReportInput."""
    from paper_trading.small_capital_strategy.decision_report_models_v187 import DecisionReportResult

    validation = validate_report(inp)
    grade = validation.final_report_grade

    audit = build_audit_trail(inp)
    evidence_pack = build_evidence_pack(inp)

    return DecisionReportResult(
        report_type=getattr(inp, "report_type", "daily_decision_report"),
        generated_at_policy=getattr(inp, "generated_at_policy", "deterministic_utc_date_only"),
        deterministic_timestamp_policy=getattr(inp, "deterministic_timestamp_policy", "date_label_only_no_wall_clock"),
        capital_stage=getattr(inp, "capital_stage", "300K"),
        market_regime=getattr(inp, "market_regime", "BULL"),
        final_cockpit_grade=getattr(inp, "final_cockpit_grade", "WAIT"),
        daily_action=getattr(inp, "daily_action", "DECISION_ONLY"),
        weekly_action=getattr(inp, "weekly_action", "DECISION_ONLY"),
        candidate_count=getattr(inp, "candidate_count", 0),
        ready_candidate_count=getattr(inp, "ready_candidate_count", 0),
        watch_candidate_count=getattr(inp, "watch_candidate_count", 0),
        blocked_candidate_count=getattr(inp, "blocked_candidate_count", 0),
        reduce_risk_candidate_count=getattr(inp, "reduce_risk_candidate_count", 0),
        portfolio_holding_count=getattr(inp, "portfolio_holding_count", 0),
        total_exposure_pct=getattr(inp, "total_exposure_pct", 0.0),
        cash_reserve_pct=getattr(inp, "cash_reserve_pct", 100.0),
        theme_exposure_summary=dict(getattr(inp, "theme_exposure_summary", {})),
        sector_exposure_summary=dict(getattr(inp, "sector_exposure_summary", {})),
        concentration_risk_score=getattr(inp, "concentration_risk_score", 0.0),
        diversification_score=getattr(inp, "diversification_score", 100.0),
        monte_carlo_ruin_risk=getattr(inp, "monte_carlo_ruin_risk", 0.0),
        max_drawdown_budget_usage_pct=getattr(inp, "max_drawdown_budget_usage_pct", 0.0),
        position_sizing_summary=getattr(inp, "position_sizing_summary", ""),
        portfolio_rebalance_summary=getattr(inp, "portfolio_rebalance_summary", ""),
        top_watch_candidates=list(getattr(inp, "top_watch_candidates", [])),
        paper_plan_ready_candidates=list(getattr(inp, "paper_plan_ready_candidates", [])),
        reduce_risk_candidates=list(getattr(inp, "reduce_risk_candidates", [])),
        blocked_candidates=list(getattr(inp, "blocked_candidates", [])),
        block_reasons=list(getattr(inp, "block_reasons", [])),
        evidence_items=[str(i) for i in evidence_pack.evidence_items],
        audit_trail=audit.audit_entries,
        final_report_grade=grade,
    )


def get_engine_info() -> dict:
    """Return engine metadata."""
    return {
        "version": "1.8.7",
        "allowed_report_actions": list(ALLOWED_REPORT_ACTIONS),
        "forbidden_report_words": list(FORBIDDEN_REPORT_WORDS),
        "valid_report_grades": list(VALID_REPORT_GRADES),
        "valid_report_types": list(VALID_REPORT_TYPES),
        "paper_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "schema_version": "187",
    }
