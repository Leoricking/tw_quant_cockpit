"""
paper_trading/small_capital_strategy/decision_performance_engine_v190.py
Core analytics engine for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


_SCHEMA = "190"
_SAFE_DEFAULTS = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "review_only": True, "performance_review_only": True,
    "strategy_improvement_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "not_investment_advice": True, "demo_only": True,
    "not_for_production": True, "production_trading_blocked": True,
}


def validate_performance_action(action: str) -> Dict[str, Any]:
    """Validate that an action is allowed for performance review."""
    from paper_trading.small_capital_strategy.decision_performance_safety_v190 import (
        is_forbidden_action, is_allowed_action,
    )
    if is_forbidden_action(action):
        return {"valid": False, "blocked": True, "reason": f"forbidden:{action.upper()}",
                **_SAFE_DEFAULTS, "schema_version": _SCHEMA}
    if is_allowed_action(action):
        return {"valid": True, "blocked": False, "reason": "allowed",
                **_SAFE_DEFAULTS, "schema_version": _SCHEMA}
    return {"valid": False, "blocked": False, "reason": f"unknown:{action.upper()}",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA}


def validate_setup_type(setup_type: str) -> bool:
    """Return True if setup_type is a known setup type."""
    from paper_trading.small_capital_strategy.decision_performance_version_v190 import SETUP_TYPES
    return setup_type in SETUP_TYPES


def validate_improvement_suggestion(suggestion: str) -> bool:
    """Return True if suggestion is a known improvement suggestion type."""
    from paper_trading.small_capital_strategy.decision_performance_version_v190 import IMPROVEMENT_SUGGESTIONS
    return suggestion in IMPROVEMENT_SUGGESTIONS


def validate_quality_grade(grade: str) -> bool:
    """Return True if grade is a known quality grade."""
    from paper_trading.small_capital_strategy.decision_performance_version_v190 import QUALITY_GRADES
    return grade in QUALITY_GRADES


def validate_performance_dimension(dimension: str) -> bool:
    """Return True if dimension is a known performance dimension."""
    from paper_trading.small_capital_strategy.decision_performance_version_v190 import PERFORMANCE_DIMENSIONS
    return dimension in PERFORMANCE_DIMENSIONS


def _compute_win_rate(wins: int, total: int) -> float:
    """Compute win rate as a float in [0.0, 1.0]."""
    if total <= 0:
        return 0.0
    return round(wins / total, 4)


def _compute_expectancy(win_rate: float, avg_win_r: float, avg_loss_r: float) -> float:
    """Compute expectancy in R: (win_rate * avg_win_r) - (loss_rate * abs(avg_loss_r))."""
    loss_rate = 1.0 - win_rate
    return round((win_rate * avg_win_r) - (loss_rate * abs(avg_loss_r)), 4)


def _compute_profit_factor(total_gain_r: float, total_loss_r: float) -> float:
    """Compute profit factor: total_gain / abs(total_loss)."""
    if total_loss_r == 0.0:
        return 0.0
    return round(total_gain_r / abs(total_loss_r), 4)


def _grade_from_score(score: float) -> str:
    """Map a score in [0, 1] to a quality grade."""
    if score >= 0.90:
        return "EXCELLENT"
    if score >= 0.75:
        return "GOOD"
    if score >= 0.55:
        return "ACCEPTABLE"
    if score >= 0.35:
        return "REVIEW_REQUIRED"
    if score >= 0.15:
        return "POOR"
    return "INVALID"


def _suggest_improvement(win_rate: float, expectancy: float, mistake_rate: float) -> str:
    """Suggest an improvement action based on performance metrics."""
    if expectancy < -0.5:
        return "BLOCK_SETUP"
    if mistake_rate > 0.4:
        return "REQUIRE_RISK_REVIEW"
    if win_rate < 0.3:
        return "TIGHTEN_RULE"
    if expectancy > 0.5 and win_rate > 0.6:
        return "KEEP_RULE"
    if expectancy > 0.2:
        return "NO_CHANGE"
    return "REVIEW_MANUALLY"


def run_performance_review(
    review_id: str,
    journal_entry_ids: List[str],
    period_label: str = "review_period",
) -> Dict[str, Any]:
    """
    Run a paper performance review given journal entry IDs.
    Returns blocked if journal_entry_ids is empty.
    """
    from paper_trading.small_capital_strategy.decision_performance_models_v190 import PerformanceReviewResult
    if not journal_entry_ids:
        r = PerformanceReviewResult(
            review_id=review_id,
            period_label=period_label,
            blocked=True,
            block_reason="performance_review_without_journal_entries",
        )
        return {
            "review_id": review_id, "blocked": True,
            "block_reason": "performance_review_without_journal_entries",
            "total_decisions": 0, "reviewed_count": 0,
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    total = len(journal_entry_ids)
    reviewed = total
    r = PerformanceReviewResult(
        review_id=review_id,
        period_label=period_label,
        total_decisions=total,
        reviewed_count=reviewed,
        blocked=False,
        quality_grade="ACCEPTABLE",
    )
    return {
        "review_id": review_id, "blocked": False,
        "total_decisions": total, "reviewed_count": reviewed,
        "quality_grade": "ACCEPTABLE",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_strategy_summary(
    decisions: List[Dict[str, Any]],
    period_label: str = "summary_period",
) -> Dict[str, Any]:
    """Build a strategy performance summary from a list of decision dicts."""
    total = len(decisions)
    plan_ready = sum(1 for d in decisions if d.get("state") == "PAPER_PLAN_READY")
    entry_allowed = sum(1 for d in decisions if d.get("state") == "PAPER_ENTRY_ALLOWED")
    reduce_risk = sum(1 for d in decisions if d.get("state") == "REDUCE_RISK")
    blocked = sum(1 for d in decisions if d.get("state") == "BLOCKED")
    no_trade = sum(1 for d in decisions if d.get("state") == "NO_TRADE")
    wins = sum(1 for d in decisions if d.get("outcome") == "WIN")
    losses = sum(1 for d in decisions if d.get("outcome") == "LOSS")
    mistakes = sum(1 for d in decisions if d.get("has_mistake", False))
    win_rate = _compute_win_rate(wins, wins + losses) if (wins + losses) > 0 else 0.0
    mistake_rate = _compute_win_rate(mistakes, total) if total > 0 else 0.0
    return {
        "total_paper_decisions": total,
        "reviewed_decision_count": total,
        "paper_plan_ready_count": plan_ready,
        "paper_entry_allowed_count": entry_allowed,
        "reduce_risk_count": reduce_risk,
        "blocked_count": blocked,
        "no_trade_count": no_trade,
        "win_rate": win_rate,
        "loss_rate": round(1.0 - win_rate, 4),
        "mistake_rate": mistake_rate,
        "period_label": period_label,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_setup_summary(
    setup_type: str,
    decisions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build a setup performance summary for a specific setup type."""
    relevant = [d for d in decisions if d.get("setup_type") == setup_type]
    count = len(relevant)
    wins = sum(1 for d in relevant if d.get("outcome") == "WIN")
    losses = sum(1 for d in relevant if d.get("outcome") == "LOSS")
    win_rate = _compute_win_rate(wins, wins + losses) if (wins + losses) > 0 else 0.0
    r_values = [d.get("r_multiple", 0.0) for d in relevant]
    win_r = [r for r in r_values if r > 0]
    loss_r = [r for r in r_values if r < 0]
    avg_gain = round(sum(win_r) / len(win_r), 4) if win_r else 0.0
    avg_loss = round(sum(loss_r) / len(loss_r), 4) if loss_r else 0.0
    expectancy = _compute_expectancy(win_rate, avg_gain, avg_loss)
    suggestion = _suggest_improvement(win_rate, expectancy, 0.0)
    grade = _grade_from_score(max(0.0, min(1.0, 0.5 + expectancy * 0.3)))
    return {
        "setup_type": setup_type,
        "occurrence_count": count,
        "win_count": wins,
        "loss_count": losses,
        "win_rate": win_rate,
        "average_gain_r": avg_gain,
        "average_loss_r": avg_loss,
        "expectancy_r": expectancy,
        "quality_grade": grade,
        "improvement_suggestion": suggestion,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_mistake_summary(
    decisions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Build a list of mistake performance summaries from decisions."""
    from collections import Counter
    tags: List[str] = []
    for d in decisions:
        tags.extend(d.get("mistake_tags", []))
    total = len(decisions)
    counter = Counter(tags)
    result = []
    for tag, count in counter.most_common():
        freq = round(count / total, 4) if total > 0 else 0.0
        result.append({
            "mistake_tag": tag,
            "occurrence_count": count,
            "frequency_pct": round(freq * 100, 2),
            "average_impact_r": -0.5,
            "improvement_suggestion": "REVIEW_MANUALLY",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        })
    return result


def build_r_multiple_summary(
    r_values: List[float],
) -> Dict[str, Any]:
    """Build R-multiple summary from a list of R-multiple values."""
    if not r_values:
        return {
            "total_trades": 0, "average_gain_r": 0.0, "average_loss_r": 0.0,
            "expectancy_r": 0.0, "profit_factor": 0.0, "largest_win_r": 0.0,
            "largest_loss_r": 0.0, "r_multiple_healthy": False,
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    wins = [r for r in r_values if r > 0]
    losses = [r for r in r_values if r < 0]
    avg_win = round(sum(wins) / len(wins), 4) if wins else 0.0
    avg_loss = round(sum(losses) / len(losses), 4) if losses else 0.0
    win_rate = _compute_win_rate(len(wins), len(r_values))
    expectancy = _compute_expectancy(win_rate, avg_win, avg_loss)
    profit_factor = _compute_profit_factor(sum(wins), abs(sum(losses)))
    return {
        "total_trades": len(r_values),
        "average_gain_r": avg_win,
        "average_loss_r": avg_loss,
        "expectancy_r": expectancy,
        "profit_factor": profit_factor,
        "largest_win_r": max(wins) if wins else 0.0,
        "largest_loss_r": min(losses) if losses else 0.0,
        "r_multiple_healthy": expectancy > 0.1,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_drawdown_summary(
    r_values: List[float],
    drawdown_budget_r: float = 6.0,
) -> Dict[str, Any]:
    """Build drawdown review summary from R-multiple sequence."""
    if not r_values:
        return {
            "max_drawdown_r": 0.0, "drawdown_budget_r": drawdown_budget_r,
            "drawdown_budget_usage_pct": 0.0, "drawdown_within_budget": True,
            "consecutive_loss_count": 0, "drawdown_blocked": False,
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    peak = 0.0
    equity = 0.0
    max_dd = 0.0
    cons_loss = 0
    max_cons = 0
    for r in r_values:
        equity += r
        if equity > peak:
            peak = equity
        dd = peak - equity
        if dd > max_dd:
            max_dd = dd
        if r < 0:
            cons_loss += 1
            max_cons = max(max_cons, cons_loss)
        else:
            cons_loss = 0
    usage_pct = round((max_dd / drawdown_budget_r) * 100, 2) if drawdown_budget_r > 0 else 0.0
    return {
        "max_drawdown_r": round(max_dd, 4),
        "drawdown_budget_r": drawdown_budget_r,
        "drawdown_budget_usage_pct": usage_pct,
        "drawdown_within_budget": max_dd <= drawdown_budget_r,
        "consecutive_loss_count": max_cons,
        "drawdown_blocked": max_dd > drawdown_budget_r,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_expectancy_summary(
    win_rate: float,
    avg_win_r: float,
    avg_loss_r: float,
) -> Dict[str, Any]:
    """Build expectancy summary."""
    expectancy = _compute_expectancy(win_rate, avg_win_r, avg_loss_r)
    edge = round(min(1.0, max(0.0, 0.5 + expectancy * 0.4)), 4)
    suggestion = _suggest_improvement(win_rate, expectancy, 0.0)
    return {
        "expectancy_r": expectancy,
        "expectancy_positive": expectancy > 0,
        "win_rate": win_rate,
        "average_win_r": avg_win_r,
        "average_loss_r": avg_loss_r,
        "edge_score": edge,
        "suggestion": suggestion,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_improvement_suggestion(
    suggestion_id: str,
    suggestion_type: str,
    rule_target: str,
    rationale: str,
    evidence_refs: Optional[List[str]] = None,
    priority: str = "LOW",
) -> Dict[str, Any]:
    """Build a strategy improvement suggestion dict."""
    if evidence_refs is None:
        evidence_refs = []
    if not evidence_refs:
        return {
            "suggestion_id": suggestion_id,
            "blocked": True,
            "block_reason": "improvement_suggestion_without_evidence",
            **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
        }
    return {
        "suggestion_id": suggestion_id,
        "suggestion_type": suggestion_type,
        "rule_target": rule_target,
        "rationale": rationale,
        "evidence_refs": evidence_refs,
        "priority": priority,
        "blocked": False,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_dashboard(
    dashboard_id: str,
    period_label: str,
    strategy_summary: Optional[Dict] = None,
    r_multiple: Optional[Dict] = None,
    drawdown: Optional[Dict] = None,
    expectancy: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Build a performance review dashboard dict."""
    grade_scores = []
    if r_multiple:
        grade_scores.append(0.7 if r_multiple.get("r_multiple_healthy") else 0.3)
    if drawdown:
        grade_scores.append(0.8 if drawdown.get("drawdown_within_budget") else 0.2)
    if expectancy:
        grade_scores.append(0.9 if expectancy.get("expectancy_positive") else 0.3)
    overall_score = sum(grade_scores) / len(grade_scores) if grade_scores else 0.5
    overall_grade = _grade_from_score(overall_score)
    return {
        "dashboard_id": dashboard_id,
        "period_label": period_label,
        "strategy_summary": strategy_summary or {},
        "r_multiple": r_multiple or {},
        "drawdown": drawdown or {},
        "expectancy": expectancy or {},
        "overall_grade": overall_grade,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_evidence_pack(
    pack_id: str,
    review_id: str,
    evidence_items: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Build a performance review evidence pack."""
    items = evidence_items or []
    return {
        "pack_id": pack_id,
        "review_id": review_id,
        "evidence_items": items,
        "evidence_count": len(items),
        "all_evidence_present": len(items) > 0,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_audit_trail(
    trail_id: str,
    review_id: str,
    steps: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Build a performance review audit trail."""
    step_list = steps or []
    return {
        "trail_id": trail_id,
        "review_id": review_id,
        "steps": step_list,
        "audit_complete": len(step_list) > 0,
        "deterministic_timestamp_policy": "date_label_only_no_wall_clock",
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def build_export_manifest(
    manifest_id: str,
    period_label: str,
    export_path: str = "reports/",
    sections: Optional[List[str]] = None,
    export_format: str = "json",
) -> Dict[str, Any]:
    """Build a performance review export manifest. Redirects unsafe paths."""
    from paper_trading.small_capital_strategy.decision_performance_safety_v190 import is_safe_output_path
    safe_path = is_safe_output_path(export_path)
    final_path = export_path if safe_path else "reports/"
    return {
        "manifest_id": manifest_id,
        "export_path": final_path,
        "period_label": period_label,
        "sections": sections or ["strategy_summary", "r_multiple", "drawdown", "expectancy"],
        "export_format": export_format,
        "safe_path": safe_path,
        **_SAFE_DEFAULTS, "schema_version": _SCHEMA,
    }


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "engine": "decision_performance_engine_v190",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        "functions": [
            "run_performance_review", "build_strategy_summary", "build_setup_summary",
            "build_mistake_summary", "build_r_multiple_summary", "build_drawdown_summary",
            "build_expectancy_summary", "build_improvement_suggestion",
            "build_dashboard", "build_evidence_pack", "build_audit_trail",
            "build_export_manifest", "validate_performance_action",
            "validate_setup_type", "validate_improvement_suggestion",
            "validate_quality_grade", "validate_performance_dimension",
        ],
        **_SAFE_DEFAULTS,
    }
