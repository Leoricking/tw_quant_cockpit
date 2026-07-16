"""
paper_trading/small_capital_strategy/decision_journal_report_v189.py
Report export for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
    DailyReviewSummary, WeeklyReviewSummary, MonthlyReviewSummary,
    JournalDashboard, JournalExportManifest, JournalEvidencePack, JournalAuditTrail,
    DecisionJournalBook,
)


def export_daily_review_as_json(summary: DailyReviewSummary) -> str:
    """Export a DailyReviewSummary as a JSON string."""
    data = {
        "date_label": summary.date_label,
        "source_workflow_id": summary.source_workflow_id,
        "total_decisions": summary.total_decisions,
        "paper_plan_count": summary.paper_plan_count,
        "paper_entry_count": summary.paper_entry_count,
        "reduce_risk_count": summary.reduce_risk_count,
        "blocked_count": summary.blocked_count,
        "no_trade_count": summary.no_trade_count,
        "average_quality_score": summary.average_quality_score,
        "grade": summary.grade,
        "findings": summary.findings,
        "action_items": summary.action_items,
        "mistake_tags": summary.mistake_tags,
        "market_regime": summary.market_regime,
        "total_exposure_pct": summary.total_exposure_pct,
        "cash_reserve_pct": summary.cash_reserve_pct,
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_weekly_review_as_json(summary: WeeklyReviewSummary) -> str:
    """Export a WeeklyReviewSummary as a JSON string."""
    data = {
        "week_label": summary.week_label,
        "total_decisions": summary.total_decisions,
        "paper_plan_count": summary.paper_plan_count,
        "paper_entry_count": summary.paper_entry_count,
        "reduce_risk_count": summary.reduce_risk_count,
        "blocked_count": summary.blocked_count,
        "no_trade_count": summary.no_trade_count,
        "average_quality_score": summary.average_quality_score,
        "weekly_grade": summary.weekly_grade,
        "recurring_mistakes": summary.recurring_mistakes,
        "top_findings": summary.top_findings,
        "top_action_items": summary.top_action_items,
        "risk_budget_exceeded": summary.risk_budget_exceeded,
        "over_concentration_detected": summary.over_concentration_detected,
        "low_cash_reserve_detected": summary.low_cash_reserve_detected,
        "daily_summary_count": len(summary.daily_summaries),
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_weekly_review_as_markdown(summary: WeeklyReviewSummary) -> str:
    """Export a WeeklyReviewSummary as a Markdown string."""
    lines = [
        "# Paper Decision Journal — Weekly Review Report v1.8.9",
        "",
        f"**Week:** {summary.week_label or 'N/A'}",
        f"**Grade:** {summary.weekly_grade}",
        f"**Average Quality Score:** {summary.average_quality_score:.3f}",
        f"**Total Decisions:** {summary.total_decisions}",
        "",
        "## Summary",
        f"- Paper Plan Ready: {summary.paper_plan_count}",
        f"- Paper Entry Allowed: {summary.paper_entry_count}",
        f"- Reduce Risk: {summary.reduce_risk_count}",
        f"- Blocked: {summary.blocked_count}",
        f"- No Trade: {summary.no_trade_count}",
        "",
        "## Recurring Mistakes",
    ]
    if summary.recurring_mistakes:
        for m in summary.recurring_mistakes:
            lines.append(f"- {m}")
    else:
        lines.append("- None detected")
    lines += [
        "",
        "## Top Findings",
    ]
    if summary.top_findings:
        for f in summary.top_findings:
            lines.append(f"- {f}")
    else:
        lines.append("- No findings")
    lines += [
        "",
        "## Action Items",
    ]
    if summary.top_action_items:
        for a in summary.top_action_items:
            lines.append(f"- [ ] {a}")
    else:
        lines.append("- No action items")
    lines += [
        "",
        "---",
        "[!] Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.",
        f"Schema: 189  |  Version: 1.8.9",
    ]
    return "\n".join(lines)


def export_dashboard_as_json(dashboard: JournalDashboard) -> str:
    """Export a JournalDashboard as a JSON string."""
    data = {
        "dashboard_id": dashboard.dashboard_id,
        "period_label": dashboard.period_label,
        "total_entries": dashboard.total_entries,
        "open_decisions": dashboard.open_decisions,
        "reviewed_decisions": dashboard.reviewed_decisions,
        "average_quality_score": dashboard.average_quality_score,
        "overall_grade": dashboard.overall_grade,
        "top_mistakes": dashboard.top_mistakes,
        "key_findings": dashboard.key_findings,
        "action_items_open": dashboard.action_items_open,
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_manifest_as_json(manifest: JournalExportManifest) -> str:
    """Export a JournalExportManifest as a JSON string."""
    data = {
        "manifest_id": manifest.manifest_id,
        "export_date_label": manifest.export_date_label,
        "export_path": manifest.export_path,
        "included_periods": manifest.included_periods,
        "entry_count": manifest.entry_count,
        "review_count": manifest.review_count,
        "evidence_count": manifest.evidence_count,
        "audit_trail_count": manifest.audit_trail_count,
        "format": manifest.format,
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_audit_trail_as_json(trail: JournalAuditTrail) -> str:
    """Export a JournalAuditTrail as a JSON string."""
    data = {
        "trail_id": trail.trail_id,
        "period_label": trail.period_label,
        "event_count": trail.event_count,
        "entry_ids": trail.entry_ids,
        "review_ids": trail.review_ids,
        "is_complete": trail.is_complete,
        "events": trail.audit_events,
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_evidence_pack_as_json(pack: JournalEvidencePack) -> str:
    """Export a JournalEvidencePack as a JSON string."""
    data = {
        "pack_id": pack.pack_id,
        "period_label": pack.period_label,
        "evidence_count": pack.evidence_count,
        "workflow_ids": pack.workflow_ids,
        "entry_ids": pack.entry_ids,
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_console_summary(summary: DailyReviewSummary) -> str:
    """Export a human-readable console summary of a DailyReviewSummary."""
    lines = [
        "=== Paper Decision Journal Daily Review v1.8.9 ===",
        f"Date:        {summary.date_label or 'N/A'}",
        f"Grade:       {summary.grade}",
        f"Avg Score:   {summary.average_quality_score:.3f}",
        f"Decisions:   {summary.total_decisions}",
        f"  Plan:      {summary.paper_plan_count}",
        f"  Entry:     {summary.paper_entry_count}",
        f"  Risk Down: {summary.reduce_risk_count}",
        f"  Blocked:   {summary.blocked_count}",
        f"  No Trade:  {summary.no_trade_count}",
        f"Mistakes:    {', '.join(summary.mistake_tags) or 'None'}",
        f"Findings:    {len(summary.findings)}",
        f"Actions:     {len(summary.action_items)}",
        "=================================================",
        "[!] Paper Only. Journal Only. No Real Orders. Not Investment Advice.",
    ]
    return "\n".join(lines)


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "version": "1.8.9",
        "release_name": "Paper Decision Journal & Review Loop",
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
        "supported_exports": [
            "daily_review_json",
            "weekly_review_json",
            "weekly_review_markdown",
            "dashboard_json",
            "manifest_json",
            "audit_trail_json",
            "evidence_pack_json",
            "console_summary",
        ],
    }
