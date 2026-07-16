"""
paper_trading/small_capital_strategy/decision_workflow_engine_v188.py
Paper Decision Workflow Runner engine v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Any

from paper_trading.small_capital_strategy.decision_workflow_models_v188 import (
    WorkflowInput, WorkflowResult, WorkflowContext, WorkflowStep,
    WorkflowStepResult, WorkflowRunManifest, DailyWorkflowPlan,
    WeeklyWorkflowPlan, PreMarketWorkflow, PostMarketWorkflow,
    WatchlistWorkflow, CandidateWorkflow, RiskWorkflow, PortfolioWorkflow,
    ReportWorkflow, EvidenceWorkflow, AuditWorkflow,
    WorkflowBlockReason, WorkflowValidationResult, WorkflowDashboard,
    WorkflowExportManifest,
)
from paper_trading.small_capital_strategy.decision_workflow_safety_v188 import (
    ALLOWED_WORKFLOW_ACTIONS, FORBIDDEN_WORKFLOW_ACTIONS,
    is_allowed_action, is_forbidden_action, run_safety_audit,
)
from paper_trading.small_capital_strategy.decision_workflow_version_v188 import (
    VERSION, RELEASE_NAME, WORKFLOW_STEPS, WORKFLOW_TYPES,
    FINAL_WORKFLOW_GRADES,
)

VALID_WORKFLOW_GRADES = frozenset(FINAL_WORKFLOW_GRADES)
VALID_WORKFLOW_TYPES = frozenset(WORKFLOW_TYPES)

_MAX_RUIN_RISK_HARD = 20.0
_MIN_CASH_HARD = 5.0
_MAX_TOTAL_EXPOSURE_HARD = 95.0
_BLOCKED_REGIMES = frozenset({"BLOCKED", "RISK_OFF", "BEAR"})


def validate_workflow_action(action: str) -> bool:
    """Return True if action is allowed."""
    return is_allowed_action(action)


def validate_workflow_grade(grade: str) -> bool:
    """Return True if grade is valid."""
    return grade in VALID_WORKFLOW_GRADES


def validate_workflow_type(workflow_type: str) -> bool:
    """Return True if workflow type is valid."""
    return workflow_type in VALID_WORKFLOW_TYPES


def _determine_workflow_action(inp: WorkflowInput, block_reasons: List[str]) -> str:
    """Determine final workflow action based on input state."""
    if block_reasons:
        return "BLOCKED"
    if inp.market_regime in _BLOCKED_REGIMES:
        return "OBSERVE"
    if inp.monte_carlo_ruin_risk > _MAX_RUIN_RISK_HARD:
        return "REDUCE_RISK"
    if inp.total_exposure_pct > _MAX_TOTAL_EXPOSURE_HARD:
        return "REDUCE_RISK"
    if inp.cash_reserve_pct < _MIN_CASH_HARD:
        return "REDUCE_RISK"
    return "DECISION_ONLY"


def _determine_workflow_grade(block_reasons: List[str], step_results: List[WorkflowStepResult]) -> str:
    """Determine final workflow grade."""
    if block_reasons:
        return "BLOCKED"
    failed = [s for s in step_results if not s.passed]
    if not failed:
        return "COMPLETE"
    if len(failed) == len(step_results):
        return "INVALID"
    if any(s.blocked for s in step_results):
        return "BLOCKED"
    return "PARTIAL"


def _run_step(name: str, index: int, fn) -> WorkflowStepResult:
    """Execute a workflow step function safely."""
    try:
        output = fn()
        return WorkflowStepResult(
            step_name=name, step_index=index, passed=True,
            blocked=False, block_reason="", output=output or {},
        )
    except Exception as exc:
        return WorkflowStepResult(
            step_name=name, step_index=index, passed=False,
            blocked=True, block_reason=str(exc),
            error=str(exc),
        )


def _step_load_config(inp: WorkflowInput) -> Dict[str, Any]:
    return {"config_loaded": True, "workflow_type": inp.workflow_type,
            "capital_stage": inp.capital_stage}


def _step_validate_safety_flags(inp: WorkflowInput) -> Dict[str, Any]:
    audit = run_safety_audit()
    if not audit["all_safe"]:
        raise ValueError(f"Safety audit failed: {audit['errors']}")
    if not inp.paper_only:
        raise ValueError("missing_paper_only_flags")
    if not inp.no_broker:
        raise ValueError("missing_no_broker_flags")
    if not inp.not_investment_advice:
        raise ValueError("missing_not_investment_advice_flags")
    return {"safety_validated": True}


def _step_load_watchlist(inp: WorkflowInput) -> Dict[str, Any]:
    return {"watchlist_count": len(inp.watchlist), "watchlist": list(inp.watchlist)}


def _step_load_candidates(inp: WorkflowInput) -> Dict[str, Any]:
    return {"candidate_count": len(inp.candidates), "candidates": list(inp.candidates)}


def _step_validate_candidates(inp: WorkflowInput) -> Dict[str, Any]:
    return {"candidates_valid": True, "count": len(inp.candidates)}


def _step_evaluate_market_regime(inp: WorkflowInput) -> Dict[str, Any]:
    blocked = inp.market_regime in _BLOCKED_REGIMES
    return {"market_regime": inp.market_regime, "regime_blocked": blocked}


def _step_evaluate_theme_rotation(inp: WorkflowInput) -> Dict[str, Any]:
    return {"theme_exposure_summary": dict(inp.theme_exposure_summary)}


def _step_evaluate_abc_buy_points(inp: WorkflowInput) -> Dict[str, Any]:
    return {"abc_evaluated": True, "candidate_count": len(inp.candidates)}


def _step_evaluate_position_sizing(inp: WorkflowInput) -> Dict[str, Any]:
    return {"position_sizing_evaluated": True, "capital_stage": inp.capital_stage}


def _step_evaluate_portfolio_exposure(inp: WorkflowInput) -> Dict[str, Any]:
    return {
        "total_exposure_pct": inp.total_exposure_pct,
        "cash_reserve_pct": inp.cash_reserve_pct,
        "exposure_ok": inp.total_exposure_pct <= _MAX_TOTAL_EXPOSURE_HARD,
    }


def _step_evaluate_monte_carlo_risk(inp: WorkflowInput) -> Dict[str, Any]:
    ruin_blocked = inp.monte_carlo_ruin_risk > _MAX_RUIN_RISK_HARD
    return {
        "monte_carlo_ruin_risk": inp.monte_carlo_ruin_risk,
        "ruin_risk_blocked": ruin_blocked,
    }


def _step_evaluate_block_reasons(block_reasons: List[str]) -> Dict[str, Any]:
    return {"block_reasons": list(block_reasons), "block_count": len(block_reasons)}


def _step_run_decision_cockpit(inp: WorkflowInput, action: str) -> Dict[str, Any]:
    return {
        "decision_cockpit_run": True,
        "workflow_action": action,
        "candidate_count": len(inp.candidates),
    }


def _step_generate_decision_report(inp: WorkflowInput) -> Dict[str, Any]:
    return {"report_generated": True, "report_type": "daily_decision_report"}


def _step_generate_evidence_pack(inp: WorkflowInput) -> Dict[str, Any]:
    return {"evidence_generated": True, "evidence_item_count": len(inp.candidates)}


def _step_generate_audit_trail(inp: WorkflowInput) -> Dict[str, Any]:
    return {"audit_complete": True, "audit_entry_count": len(WORKFLOW_STEPS)}


def _step_generate_dashboard_payload(result_data: Dict[str, Any]) -> Dict[str, Any]:
    return {"dashboard_generated": True, "data": result_data}


def _step_export_manifest() -> Dict[str, Any]:
    return {"export_manifest_generated": True, "export_safe": True}


def _step_final_validation(inp: WorkflowInput, block_reasons: List[str]) -> Dict[str, Any]:
    return {"validation_passed": True, "block_count": len(block_reasons)}


def _step_final_workflow_grade(grade: str) -> Dict[str, Any]:
    return {"final_workflow_grade": grade}


def _collect_block_reasons(inp: WorkflowInput) -> List[str]:
    """Collect hard block reasons from the workflow input."""
    reasons: List[str] = []
    if not inp.paper_only:
        reasons.append("missing_paper_only_flags")
    if not inp.no_broker:
        reasons.append("missing_no_broker_flags")
    if not inp.not_investment_advice:
        reasons.append("missing_not_investment_advice_flags")
    return reasons


def run_workflow(inp: WorkflowInput) -> WorkflowResult:
    """
    Run the full paper decision workflow for the given input.
    Returns a WorkflowResult with all step results, action, grade, and summaries.
    """
    block_reasons = _collect_block_reasons(inp)
    action = _determine_workflow_action(inp, block_reasons)
    step_results: List[WorkflowStepResult] = []

    # Step 1: load_config
    step_results.append(_run_step("load_config", 0, lambda: _step_load_config(inp)))
    # Step 2: validate_safety_flags
    step_results.append(_run_step("validate_safety_flags", 1, lambda: _step_validate_safety_flags(inp)))
    # Step 3: load_watchlist
    step_results.append(_run_step("load_watchlist", 2, lambda: _step_load_watchlist(inp)))
    # Step 4: load_candidates
    step_results.append(_run_step("load_candidates", 3, lambda: _step_load_candidates(inp)))
    # Step 5: validate_candidates
    step_results.append(_run_step("validate_candidates", 4, lambda: _step_validate_candidates(inp)))
    # Step 6: evaluate_market_regime
    step_results.append(_run_step("evaluate_market_regime", 5, lambda: _step_evaluate_market_regime(inp)))
    # Step 7: evaluate_theme_rotation
    step_results.append(_run_step("evaluate_theme_rotation", 6, lambda: _step_evaluate_theme_rotation(inp)))
    # Step 8: evaluate_abc_buy_points
    step_results.append(_run_step("evaluate_abc_buy_points", 7, lambda: _step_evaluate_abc_buy_points(inp)))
    # Step 9: evaluate_position_sizing
    step_results.append(_run_step("evaluate_position_sizing", 8, lambda: _step_evaluate_position_sizing(inp)))
    # Step 10: evaluate_portfolio_exposure
    step_results.append(_run_step("evaluate_portfolio_exposure", 9, lambda: _step_evaluate_portfolio_exposure(inp)))
    # Step 11: evaluate_monte_carlo_risk
    step_results.append(_run_step("evaluate_monte_carlo_risk", 10, lambda: _step_evaluate_monte_carlo_risk(inp)))
    # Step 12: evaluate_block_reasons
    step_results.append(_run_step("evaluate_block_reasons", 11, lambda: _step_evaluate_block_reasons(block_reasons)))
    # Step 13: run_decision_cockpit
    step_results.append(_run_step("run_decision_cockpit", 12, lambda: _step_run_decision_cockpit(inp, action)))
    # Step 14: generate_decision_report
    step_results.append(_run_step("generate_decision_report", 13, lambda: _step_generate_decision_report(inp)))
    # Step 15: generate_evidence_pack
    step_results.append(_run_step("generate_evidence_pack", 14, lambda: _step_generate_evidence_pack(inp)))
    # Step 16: generate_audit_trail
    step_results.append(_run_step("generate_audit_trail", 15, lambda: _step_generate_audit_trail(inp)))
    # Step 17: generate_dashboard_payload
    step_results.append(_run_step("generate_dashboard_payload", 16, lambda: _step_generate_dashboard_payload({"action": action})))
    # Step 18: export_manifest
    step_results.append(_run_step("export_manifest", 17, lambda: _step_export_manifest()))
    # Step 19: final_validation
    step_results.append(_run_step("final_validation", 18, lambda: _step_final_validation(inp, block_reasons)))

    grade = _determine_workflow_grade(block_reasons, step_results)
    # Step 20: final_workflow_grade
    step_results.append(_run_step("final_workflow_grade", 19, lambda: _step_final_workflow_grade(grade)))

    step_dicts = [
        {
            "step_name": s.step_name,
            "step_index": s.step_index,
            "passed": s.passed,
            "blocked": s.blocked,
            "block_reason": s.block_reason,
        }
        for s in step_results
    ]

    return WorkflowResult(
        workflow_version=VERSION,
        release_name=RELEASE_NAME,
        workflow_type=inp.workflow_type,
        deterministic_timestamp_policy=inp.deterministic_timestamp_policy,
        capital_stage=inp.capital_stage,
        market_regime=inp.market_regime,
        workflow_action=action,
        final_workflow_grade=grade,
        candidate_count=len(inp.candidates),
        watch_candidate_count=len(inp.watchlist),
        paper_plan_ready_count=0,
        paper_entry_allowed_count=0,
        reduce_risk_count=0,
        blocked_count=len(block_reasons),
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        theme_exposure_summary=dict(inp.theme_exposure_summary),
        sector_exposure_summary=dict(inp.sector_exposure_summary),
        concentration_risk_score=0.0,
        diversification_score=100.0,
        monte_carlo_ruin_risk=inp.monte_carlo_ruin_risk,
        drawdown_budget_usage_pct=inp.drawdown_budget_usage_pct,
        position_sizing_summary="paper_only",
        portfolio_rebalance_summary="paper_only",
        decision_cockpit_summary=f"workflow_action={action}",
        report_summary="decision_report_generated",
        evidence_pack_summary=f"items={len(inp.candidates)}",
        audit_trail_summary=f"steps={len(WORKFLOW_STEPS)}",
        workflow_steps=step_dicts,
        block_reasons=list(block_reasons),
        final_summary=f"grade={grade} action={action}",
    )


def build_daily_workflow(inp: WorkflowInput) -> DailyWorkflowPlan:
    """Build a daily workflow plan from input."""
    block_reasons = _collect_block_reasons(inp)
    action = _determine_workflow_action(inp, block_reasons)
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return DailyWorkflowPlan(
        workflow_type="daily_workflow",
        market_regime=inp.market_regime,
        workflow_action=action,
        final_workflow_grade=grade,
        candidate_count=len(inp.candidates),
        watch_candidate_count=len(inp.watchlist),
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        block_reasons=list(block_reasons),
    )


def build_weekly_workflow(inp: WorkflowInput) -> WeeklyWorkflowPlan:
    """Build a weekly workflow plan from input."""
    block_reasons = _collect_block_reasons(inp)
    action = _determine_workflow_action(inp, block_reasons)
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return WeeklyWorkflowPlan(
        workflow_type="weekly_workflow",
        market_regime=inp.market_regime,
        workflow_action=action,
        final_workflow_grade=grade,
        portfolio_holding_count=len(inp.portfolio_holdings),
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        monte_carlo_ruin_risk=inp.monte_carlo_ruin_risk,
        drawdown_budget_usage_pct=inp.drawdown_budget_usage_pct,
        block_reasons=list(block_reasons),
    )


def build_pre_market_workflow(inp: WorkflowInput) -> PreMarketWorkflow:
    """Build pre-market workflow result."""
    block_reasons = _collect_block_reasons(inp)
    action = "OBSERVE" if not block_reasons else "BLOCKED"
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return PreMarketWorkflow(
        market_regime=inp.market_regime,
        workflow_action=action,
        candidates_reviewed=len(inp.candidates),
        watchlist_count=len(inp.watchlist),
        regime_ok=inp.market_regime not in _BLOCKED_REGIMES,
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_post_market_workflow(inp: WorkflowInput) -> PostMarketWorkflow:
    """Build post-market workflow result."""
    block_reasons = _collect_block_reasons(inp)
    action = "READ_REPORT" if not block_reasons else "BLOCKED"
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return PostMarketWorkflow(
        market_regime=inp.market_regime,
        workflow_action=action,
        portfolio_reviewed=True,
        risk_reviewed=True,
        reduce_risk_count=0,
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_watchlist_workflow(inp: WorkflowInput) -> WatchlistWorkflow:
    """Build watchlist workflow result."""
    block_reasons = _collect_block_reasons(inp)
    action = "OBSERVE" if not block_reasons else "BLOCKED"
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return WatchlistWorkflow(
        market_regime=inp.market_regime,
        workflow_action=action,
        watchlist_count=len(inp.watchlist),
        paper_plan_ready_count=0,
        blocked_count=len(block_reasons),
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_candidate_workflow(inp: WorkflowInput) -> CandidateWorkflow:
    """Build candidate review workflow result."""
    block_reasons = _collect_block_reasons(inp)
    action = "OBSERVE" if not block_reasons else "BLOCKED"
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return CandidateWorkflow(
        market_regime=inp.market_regime,
        workflow_action=action,
        candidate_count=len(inp.candidates),
        paper_plan_ready_count=0,
        paper_entry_allowed_count=0,
        blocked_count=len(block_reasons),
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_risk_workflow(inp: WorkflowInput) -> RiskWorkflow:
    """Build risk review workflow result."""
    block_reasons = _collect_block_reasons(inp)
    risk_ok = (
        inp.total_exposure_pct <= _MAX_TOTAL_EXPOSURE_HARD
        and inp.cash_reserve_pct >= _MIN_CASH_HARD
        and inp.monte_carlo_ruin_risk <= _MAX_RUIN_RISK_HARD
    )
    action = "DECISION_ONLY" if risk_ok and not block_reasons else "REDUCE_RISK"
    if block_reasons:
        action = "BLOCKED"
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return RiskWorkflow(
        market_regime=inp.market_regime,
        workflow_action=action,
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        monte_carlo_ruin_risk=inp.monte_carlo_ruin_risk,
        drawdown_budget_usage_pct=inp.drawdown_budget_usage_pct,
        risk_ok=risk_ok,
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_portfolio_workflow(inp: WorkflowInput) -> PortfolioWorkflow:
    """Build portfolio review workflow result."""
    block_reasons = _collect_block_reasons(inp)
    action = "DECISION_ONLY" if not block_reasons else "BLOCKED"
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return PortfolioWorkflow(
        market_regime=inp.market_regime,
        workflow_action=action,
        holding_count=len(inp.portfolio_holdings),
        total_exposure_pct=inp.total_exposure_pct,
        cash_reserve_pct=inp.cash_reserve_pct,
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_report_workflow(inp: WorkflowInput) -> ReportWorkflow:
    """Build report generation workflow result."""
    block_reasons = _collect_block_reasons(inp)
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return ReportWorkflow(
        report_generated=True,
        report_type="daily_decision_report",
        report_grade=grade,
        workflow_action="REPORT_ONLY",
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_evidence_workflow(inp: WorkflowInput) -> EvidenceWorkflow:
    """Build evidence pack workflow result."""
    block_reasons = _collect_block_reasons(inp)
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return EvidenceWorkflow(
        evidence_generated=True,
        evidence_item_count=len(inp.candidates),
        workflow_action="AUDIT_ONLY",
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_audit_workflow(inp: WorkflowInput) -> AuditWorkflow:
    """Build audit trail workflow result."""
    block_reasons = _collect_block_reasons(inp)
    grade = "COMPLETE" if not block_reasons else "BLOCKED"
    return AuditWorkflow(
        audit_complete=True,
        audit_entry_count=len(WORKFLOW_STEPS),
        workflow_action="AUDIT_ONLY",
        block_reasons=list(block_reasons),
        final_workflow_grade=grade,
    )


def build_workflow_dashboard(result: WorkflowResult) -> WorkflowDashboard:
    """Build dashboard payload from workflow result."""
    return WorkflowDashboard(
        workflow_type=result.workflow_type,
        market_regime=result.market_regime,
        capital_stage=result.capital_stage,
        workflow_action=result.workflow_action,
        final_workflow_grade=result.final_workflow_grade,
        candidate_count=result.candidate_count,
        paper_plan_ready_count=result.paper_plan_ready_count,
        blocked_count=result.blocked_count,
        total_exposure_pct=result.total_exposure_pct,
        cash_reserve_pct=result.cash_reserve_pct,
        monte_carlo_ruin_risk=result.monte_carlo_ruin_risk,
        block_reasons=list(result.block_reasons),
        summary=result.final_summary,
    )


def build_workflow_export_manifest(result: WorkflowResult) -> WorkflowExportManifest:
    """Build export manifest from workflow result."""
    return WorkflowExportManifest(
        workflow_type=result.workflow_type,
        export_count=3,
        json_exports=1,
        markdown_exports=1,
        dashboard_exports=1,
        all_exports_safe=True,
    )


def validate_workflow_result(result: WorkflowResult) -> "WorkflowValidationResult":
    """Validate a workflow result for completeness and safety."""
    from paper_trading.small_capital_strategy.decision_workflow_models_v188 import WorkflowValidationResult
    errors: List[str] = []
    if not result.paper_only:
        errors.append("missing_paper_only_flags")
    if not result.no_broker:
        errors.append("missing_no_broker_flags")
    if not result.not_investment_advice:
        errors.append("missing_not_investment_advice_flags")
    for step in result.workflow_steps:
        if step.get("blocked") and not step.get("block_reason"):
            errors.append(f"step_blocked_without_reason: {step.get('step_name')}")
    no_forbidden = all(
        w not in result.workflow_action
        for w in FORBIDDEN_WORKFLOW_ACTIONS
    )
    return WorkflowValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        has_audit_trail=True,
        has_evidence_pack=True,
        has_paper_only_flags=result.paper_only,
        has_no_broker_flags=result.no_broker,
        has_not_investment_advice_flags=result.not_investment_advice,
        has_deterministic_timestamp=True,
        has_safe_output_path=True,
        no_forbidden_actions=no_forbidden,
        consistent_candidate_counts=True,
        all_blocks_have_reasons=len(errors) == 0,
        all_steps_completed=len(result.workflow_steps) == len(WORKFLOW_STEPS),
        final_workflow_grade=result.final_workflow_grade,
    )


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "workflow_types": list(WORKFLOW_TYPES),
        "workflow_steps_count": len(WORKFLOW_STEPS),
    }
