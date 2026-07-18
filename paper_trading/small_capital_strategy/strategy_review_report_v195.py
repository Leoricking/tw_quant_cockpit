"""
paper_trading/small_capital_strategy/strategy_review_report_v195.py
Report functions for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any, List

_SAFE = {
    "paper_only": True,
    "research_only": True,
    "review_only": True,
    "human_approval_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "auto_approval": False,
    "auto_rollback": False,
    "schema_version": "195",
}


def export_review_summary(review_id: str) -> Dict[str, Any]:
    """Export review summary. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "review_summary",
        "requires_manual_review": True,
    }


def export_review_alert_report(review_id: str) -> Dict[str, Any]:
    """Export review alert report. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "review_alerts",
        "alert_count": 0,
    }


def export_human_approval_report(review_id: str) -> Dict[str, Any]:
    """Export human approval report. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "human_approval",
        "auto_approval": False,
        "requires_manual_review": True,
    }


def export_rollback_review_report(review_id: str) -> Dict[str, Any]:
    """Export rollback review report. Never triggers auto-rollback."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "rollback_review",
        "auto_rollback": False,
        "requires_manual_review": True,
    }


def export_review_evidence_pack(review_id: str) -> Dict[str, Any]:
    """Export review evidence pack. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "evidence_pack",
    }


def export_review_audit_trail(review_id: str) -> Dict[str, Any]:
    """Export review audit trail. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "audit_trail",
    }


def export_full_review_pack(review_id: str) -> Dict[str, Any]:
    """Export full review pack. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "full_review_pack",
        "auto_approval": False,
        "auto_rollback": False,
    }


def export_review_dashboard(review_id: str) -> Dict[str, Any]:
    """Export review dashboard data. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "review_dashboard",
    }


def export_approval_checklist(review_id: str) -> Dict[str, Any]:
    """Export approval checklist. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "approval_checklist",
        "auto_approval": False,
        "requires_manual_review": True,
    }


def export_review_findings(review_id: str) -> Dict[str, Any]:
    """Export review findings. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "section": "review_findings",
        "finding_count": 0,
    }


def get_report_section_names() -> List[str]:
    """Return list of available report section names."""
    return [
        "review_summary",
        "review_alerts",
        "human_approval",
        "rollback_review",
        "evidence_pack",
        "audit_trail",
        "full_review_pack",
        "review_dashboard",
        "approval_checklist",
        "review_findings",
    ]
