"""
paper_trading/small_capital_strategy/strategy_registry_report_v196.py
Report and export functions for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

_VERSION = "1.9.6"
_SCHEMA = "196"
_PAPER_HEADER = {
    "paper_only": True,
    "research_only": True,
    "governance_only": True,
    "registry_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "schema_version": _SCHEMA,
}

REPORT_SECTIONS = [
    "decision_record",
    "governance_report",
    "lineage_report",
    "evidence_pack_report",
    "audit_trail_report",
    "dashboard_report",
    "registry_summary",
    "violation_report",
    "retention_policy_report",
    "full_registry_pack",
]


def get_report_section_names() -> List[str]:
    """Return list of report section names."""
    return list(REPORT_SECTIONS)


def export_decision_record_report(decision_id: str) -> Dict[str, Any]:
    """Export a decision record report."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "decision_record",
        "decision_state": "DRAFT",
        "auto_decision": False,
        "immutable": True,
        "no_production_mutation": True,
    }


def export_governance_report(decision_id: str) -> Dict[str, Any]:
    """Export a governance report for a decision."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "governance_report",
        "governance_passed": False,
        "governance_check_count": 19,
        "auto_approval": False,
    }


def export_lineage_report(decision_id: str) -> Dict[str, Any]:
    """Export a lineage report for a decision."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "lineage_report",
        "parent_decisions": [],
        "source_references": [],
        "lineage_complete": False,
    }


def export_evidence_pack_report(decision_id: str) -> Dict[str, Any]:
    """Export an evidence pack report for a decision."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "evidence_pack_report",
        "evidence_count": 0,
        "complete": False,
    }


def export_audit_trail_report(decision_id: str) -> Dict[str, Any]:
    """Export an audit trail report for a decision."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "audit_trail_report",
        "entry_count": 0,
        "immutable": True,
    }


def export_dashboard_report(decision_id: str) -> Dict[str, Any]:
    """Export a dashboard report for a decision registry."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "dashboard_report",
        "total_decisions": 0,
        "pending_review": 0,
        "auto_decision": False,
    }


def export_registry_summary(decision_id: str) -> Dict[str, Any]:
    """Export a registry summary."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "registry_summary",
        "version": _VERSION,
        "schema_version": _SCHEMA,
    }


def export_violation_report(decision_id: str) -> Dict[str, Any]:
    """Export a violation report for a decision."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "violation_report",
        "violations": [],
        "violation_count": 0,
        "governance_passed": True,
    }


def export_retention_policy_report(decision_id: str) -> Dict[str, Any]:
    """Export a retention policy report."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "retention_policy_report",
        "retention_days": 3650,
        "immutable_after_record": True,
        "auto_deletion": False,
    }


def export_full_registry_pack(decision_id: str) -> Dict[str, Any]:
    """Export a full registry pack for a decision. Blocks on missing decision_id."""
    if not decision_id:
        return {**_PAPER_HEADER, "valid": False, "blocked": True,
                "block_reason": "missing_decision_id"}
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "decision_id": decision_id,
        "section": "full_registry_pack",
        "sections_included": list(REPORT_SECTIONS),
        "auto_decision": False,
        "auto_rollback": False,
        "auto_approval": False,
        "immutable": True,
        "production_mutation_blocked": True,
        "live_activation_blocked": True,
    }
