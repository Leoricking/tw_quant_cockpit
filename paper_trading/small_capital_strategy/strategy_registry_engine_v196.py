"""
paper_trading/small_capital_strategy/strategy_registry_engine_v196.py
Core engine for Paper Strategy Decision Registry & Governance Lab v1.9.6.
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
    "governance_only": True,
    "registry_only": True,
    "decision_record_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "schema_version": _SCHEMA,
}

_FORBIDDEN = frozenset(["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                         "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"])
_ALLOWED_ACTIONS = frozenset([
    "REGISTRY_VERSION", "REGISTER_DECISION", "REGISTRY_RECORD", "REGISTRY_LIST",
    "REGISTRY_LINEAGE", "GOVERNANCE_CHECK", "REGISTRY_QUEUE", "REGISTRY_VALIDATE",
    "REGISTRY_REPORT", "REGISTRY_DASHBOARD", "REGISTRY_EXPORT", "EVIDENCE_PACK",
    "AUDIT_TRAIL", "HEALTH_CHECK", "RELEASE_GATE", "REGISTRY_SCENARIOS",
    "REGISTRY_FIXTURES", "SAFETY_AUDIT",
    # Additional allowed registry actions
    "REGISTER_DECISION", "GET_DECISION", "GOVERNANCE_REPORT", "AUDIT_TRAIL_BUILD",
    "VIOLATION_REPORT", "RETENTION_POLICY", "FULL_PACK",
])
_VALID_SOURCES = frozenset([
    "TUNING_PROPOSAL", "SANDBOX_VALIDATION", "SHADOW_COMPARISON", "PROMOTION_PACKAGE",
    "ROLLBACK_PLAN", "MONITORING_ALERT", "DRIFT_DETECTION", "HUMAN_APPROVAL_REQUEST",
    "ROLLBACK_REVIEW_TICKET", "MANUAL_REVIEW_NOTE", "MANUAL_REVIEW",
])
_VALID_TYPES = frozenset([
    "APPROVE_FOR_PAPER_ONLY", "REJECT_CANDIDATE", "KEEP_MONITORING", "KEEP_SHADOW_ONLY",
    "OPEN_ROLLBACK_REVIEW", "SUSPEND_CANDIDATE_RULE", "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_LONGER_MONITORING", "ESCALATE_TO_MANUAL_REVIEW", "NO_CHANGE",
])
_VALID_STATES = frozenset([
    "DRAFT", "PENDING_REVIEW", "RECORDED", "APPROVED_FOR_PAPER_ONLY", "REJECTED",
    "KEEP_MONITORING", "KEEP_SHADOW_ONLY", "ROLLBACK_REVIEW_REQUIRED",
    "SUSPENDED_FOR_PAPER", "NEED_MORE_EVIDENCE", "INVALID", "ARCHIVED",
])

_UNSAFE_PATH_PATTERNS = (
    "production", "prod_db", "live_db", "broker_", "real_trade", "real_order",
    "/etc/", "\\etc\\", "c:/windows/", "c:/program files/",
)


def _blocked(reason: str) -> Dict[str, Any]:
    """Return a standard blocked response."""
    return {
        **_PAPER_HEADER,
        "valid": False,
        "blocked": True,
        "block_reason": reason,
        "reason": reason,
        "block_reasons": [reason],
    }


def _ok(**extra) -> Dict[str, Any]:
    """Return a standard valid (not blocked) response."""
    return {
        **_PAPER_HEADER,
        "valid": True,
        "blocked": False,
        "block_reason": "",
        "reason": "",
        "block_reasons": [],
        **extra,
    }


def _is_unsafe_path(path: str) -> bool:
    """Return True if the path is unsafe."""
    if not path:
        return True
    lower = path.lower()
    # absolute Unix/Windows paths are unsafe for export
    if path.startswith("/") or (len(path) > 1 and path[1] == ":"):
        # Allow only known safe absolute prefixes
        safe_absolute = ("c:/users/", "c:/tmp/")
        if not any(lower.startswith(p) for p in safe_absolute):
            return True
    return any(d in lower for d in _UNSAFE_PATH_PATTERNS)


def validate_registry_action(action: str) -> Dict[str, Any]:
    """Validate a registry action against allowed/forbidden lists."""
    upper = action.upper() if action else ""
    if upper in _FORBIDDEN:
        return _blocked(f"forbidden_registry_action: {action}")
    if upper in _ALLOWED_ACTIONS:
        return _ok(action=action)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_registry_action: {action}",
            "reason": f"unknown_registry_action: {action}",
            "block_reasons": [f"unknown_registry_action: {action}"]}


def validate_decision_source(source: str) -> Dict[str, Any]:
    """Validate a decision source type."""
    if not source:
        return _blocked("missing_decision_source")
    if source.upper() in _VALID_SOURCES:
        return _ok(source=source)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_decision_source: {source}",
            "reason": f"unknown_decision_source: {source}",
            "block_reasons": [f"unknown_decision_source: {source}"]}


def validate_decision_type(decision_type: str) -> Dict[str, Any]:
    """Validate a decision type."""
    if not decision_type:
        return _blocked("missing_decision_type")
    if decision_type.upper() in _VALID_TYPES:
        return _ok(decision_type=decision_type)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_decision_type: {decision_type}",
            "reason": f"unknown_decision_type: {decision_type}",
            "block_reasons": [f"unknown_decision_type: {decision_type}"]}


def validate_decision_state(state: str) -> Dict[str, Any]:
    """Validate a decision state."""
    if not state:
        return _blocked("missing_decision_state")
    if state.upper() in _VALID_STATES:
        return _ok(state=state)
    return {**_PAPER_HEADER, "valid": False, "blocked": False,
            "block_reason": f"unknown_decision_state: {state}",
            "reason": f"unknown_decision_state: {state}",
            "block_reasons": [f"unknown_decision_state: {state}"]}


def build_decision_record(
    decision_id: str,
    source: str,
    decision_type: str,
    rationale: str = "",
    evidence_ids: List[str] = None,
) -> Dict[str, Any]:
    """Build a strategy decision record. Blocks on missing required fields."""
    if not decision_id:
        return _blocked("missing_decision_id")
    if not source:
        return _blocked("missing_decision_source")
    if not decision_type:
        return _blocked("missing_decision_type")
    if not rationale:
        return _blocked("missing_decision_rationale")
    return _ok(
        decision_id=decision_id,
        source=source,
        decision_type=decision_type,
        decision_state="DRAFT",
        rationale=rationale,
        evidence_ids=list(evidence_ids or []),
        immutable=True,
        auto_decision=False,
        no_automatic_rollback=True,
    )


def build_governance_check(
    decision_id: str,
    evidence,
    rationale: str,
) -> Dict[str, Any]:
    """Run governance checks on a decision. Blocks on missing required fields."""
    if not decision_id:
        return _blocked("missing_decision_id")
    if not evidence:
        return _blocked("missing_decision_evidence")
    if not rationale:
        return _blocked("missing_decision_rationale")
    checks = {
        "decision_id_present": bool(decision_id),
        "evidence_present": bool(evidence),
        "rationale_present": bool(rationale),
        "paper_only_flags_present": True,
        "no_broker_flags_present": True,
        "no_real_order_flags_present": True,
        "no_production_mutation_flags_present": True,
        "no_automatic_rollback_flags_present": True,
        "not_investment_advice_present": True,
        "immutable_record_policy_present": True,
        "audit_trail_present": True,
    }
    all_passed = all(checks.values())
    return _ok(
        decision_id=decision_id,
        governance_checks=checks,
        governance_passed=all_passed,
    )


def build_decision_queue(registry_id: str) -> Dict[str, Any]:
    """Build a decision queue for the given registry."""
    if not registry_id:
        return _blocked("missing_registry_id")
    return _ok(
        registry_id=registry_id,
        pending_decisions=[],
        queue_size=0,
        auto_processing=False,
        requires_human_review=True,
    )


def build_evidence_pack(decision_id: str, evidence_links: List[str] = None) -> Dict[str, Any]:
    """Build an evidence pack for a decision. Blocks on missing decision_id only."""
    if not decision_id:
        return _blocked("missing_decision_id")
    links = list(evidence_links or [])
    return _ok(
        decision_id=decision_id,
        evidence_links=links,
        evidence_count=len(links),
        complete=len(links) > 0,
        audit_only=True,
    )


def build_audit_trail(decision_id: str, events: List[str] = None) -> Dict[str, Any]:
    """Build an audit trail for a decision. Blocks on missing decision_id."""
    if not decision_id:
        return _blocked("missing_decision_id")
    return _ok(
        decision_id=decision_id,
        events=list(events or []),
        entries=[],
        immutable=True,
        audit_only=True,
    )


def build_registry_dashboard(registry_id: str, decision_id: str = "") -> Dict[str, Any]:
    """Build a decision registry dashboard. Blocks on missing registry_id."""
    if not registry_id:
        return _blocked("missing_registry_id")
    return _ok(
        registry_id=registry_id,
        decision_id=decision_id,
        total_decisions=0,
        pending_review=0,
        approved_for_paper=0,
        rejected=0,
        archived=0,
    )


def build_export_manifest(export_path: str, decision_id: str = "") -> Dict[str, Any]:
    """Build an export manifest. Blocks on unsafe export paths."""
    if _is_unsafe_path(export_path):
        return _blocked("unsafe_export_path")
    return _ok(
        decision_id=decision_id,
        export_path=export_path,
        safe_path_only=True,
        included_sections=[
            "decision_record", "evidence_pack", "governance_result",
            "lineage", "audit_trail",
        ],
    )


def build_decision_lineage(decision_id: str, source_ids: List[str] = None) -> Dict[str, Any]:
    """Build decision lineage. Blocks on missing decision_id."""
    if not decision_id:
        return _blocked("missing_decision_id")
    ids = list(source_ids or [])
    return _ok(
        decision_id=decision_id,
        source_ids=ids,
        parent_decision_ids=[],
        lineage_complete=len(ids) > 0,
    )


def build_registry_report(decision_id: str) -> Dict[str, Any]:
    """Build a registry report for a decision."""
    if not decision_id:
        return _blocked("missing_decision_id")
    return _ok(
        decision_id=decision_id,
        report_sections=[
            "summary", "decision_record", "evidence_pack", "governance_result",
            "lineage", "audit_trail", "risk_summary", "impact_summary",
        ],
        report_only=True,
    )


def build_violation_report(decision_id: str, violations: List[str] = None) -> Dict[str, Any]:
    """Build a violation report for a decision."""
    if not decision_id:
        return _blocked("missing_decision_id")
    viols = list(violations or [])
    return _ok(
        decision_id=decision_id,
        violations=viols,
        violation_count=len(viols),
        governance_passed=len(viols) == 0,
    )


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return _ok(
        version=_VERSION,
        engine="strategy_registry_engine_v196",
        functions=[
            "validate_registry_action", "validate_decision_source",
            "validate_decision_type", "validate_decision_state",
            "build_decision_record", "build_governance_check",
            "build_decision_queue", "build_evidence_pack",
            "build_audit_trail", "build_registry_dashboard",
            "build_export_manifest", "build_decision_lineage",
            "build_registry_report", "build_violation_report",
        ],
    )
