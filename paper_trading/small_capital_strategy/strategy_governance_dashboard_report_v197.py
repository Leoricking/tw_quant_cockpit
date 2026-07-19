"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_report_v197.py
Report and export functions for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

_VERSION = "1.9.7"
_SCHEMA = "197"
_PAPER_HEADER = {
    "paper_only": True,
    "research_only": True,
    "governance_analytics_only": True,
    "dashboard_only": True,
    "quality_analytics_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "analytics_executes_decision": False,
    "dashboard_mutates_strategy": False,
    "schema_version": _SCHEMA,
}

REPORT_SECTIONS = [
    "quality_overview_report",
    "evidence_coverage_report",
    "decision_outcome_report",
    "approval_quality_report",
    "rejection_quality_report",
    "monitoring_quality_report",
    "rollback_review_frequency_report",
    "governance_violations_report",
    "consistency_summary_report",
    "trend_report",
    "scorecard_report",
    "audit_summary_report",
]


def get_report_section_names() -> List[str]:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def export_quality_overview_report(registry_source: str) -> Dict[str, Any]:
    """Export a quality overview report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "quality_overview_report",
        "total_decisions": 0,
        "average_composite_score": 0.0,
    }


def export_evidence_coverage_report(registry_source: str) -> Dict[str, Any]:
    """Export an evidence coverage report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "evidence_coverage_report",
        "decisions_with_full_evidence": 0,
        "decisions_with_gaps": 0,
    }


def export_decision_outcome_report(registry_source: str) -> Dict[str, Any]:
    """Export a decision outcome report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "decision_outcome_report",
        "approved_count": 0,
        "rejected_count": 0,
        "keep_monitoring_count": 0,
    }


def export_approval_quality_report(registry_source: str) -> Dict[str, Any]:
    """Export an approval quality report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "approval_quality_report",
        "auto_approval": False,
        "no_production_mutation": True,
    }


def export_rejection_quality_report(registry_source: str) -> Dict[str, Any]:
    """Export a rejection quality report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "rejection_quality_report",
        "total_rejected": 0,
    }


def export_monitoring_quality_report(registry_source: str) -> Dict[str, Any]:
    """Export a keep-monitoring decision quality report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "monitoring_quality_report",
        "total_keep_monitoring": 0,
    }


def export_rollback_frequency_report(registry_source: str) -> Dict[str, Any]:
    """Export a rollback review frequency report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "rollback_review_frequency_report",
        "total_rollback_reviews": 0,
        "auto_rollback": False,
        "requires_human_review": True,
    }


def export_violations_report(registry_source: str) -> Dict[str, Any]:
    """Export a governance violations report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "governance_violations_report",
        "total_violations": 0,
    }


def export_scorecard_report(registry_source: str) -> Dict[str, Any]:
    """Export a decision quality scorecard report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "scorecard_report",
        "scorecard_metrics": 12,
        "all_metrics_paper_only": True,
    }


def export_audit_summary_report(registry_source: str) -> Dict[str, Any]:
    """Export an audit summary report."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "audit_summary_report",
        "immutable": True,
        "audit_only": True,
    }


def export_full_dashboard_pack(registry_source: str) -> Dict[str, Any]:
    """Export full governance dashboard pack. Blocks on missing registry_source."""
    if not registry_source:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_registry_source"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "registry_source": registry_source,
        "section": "full_dashboard_pack",
        "sections_included": list(REPORT_SECTIONS),
        "analytics_executes_decision": False,
        "dashboard_mutates_strategy": False,
        "auto_rollback": False,
        "auto_approval": False,
        "immutable": True,
        "production_mutation_blocked": True,
        "live_activation_blocked": True,
    }
