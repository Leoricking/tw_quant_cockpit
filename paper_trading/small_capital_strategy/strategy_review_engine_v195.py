"""
paper_trading/small_capital_strategy/strategy_review_engine_v195.py
Engine functions for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any, List

from paper_trading.small_capital_strategy.strategy_review_safety_v195 import (
    FORBIDDEN_REVIEW_ACTIONS, ALLOWED_REVIEW_ACTIONS,
    HARD_BLOCK_CONDITIONS, is_forbidden_action, is_allowed_action,
    is_safe_output_path, has_forbidden_words,
)
from paper_trading.small_capital_strategy.strategy_review_version_v195 import (
    REVIEW_ALERT_CATEGORIES, REVIEW_DECISION_STATES, REVIEW_SEVERITIES,
    REVIEW_RECOMMENDATIONS, VERSION, SCHEMA_VERSION,
)

_SAFE = {
    "paper_only": True,
    "research_only": True,
    "review_only": True,
    "human_approval_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "auto_rollback": False,
    "auto_approval": False,
    "schema_version": SCHEMA_VERSION,
}


def validate_review_action(action: str) -> Dict[str, Any]:
    """Validate a review action."""
    if is_forbidden_action(action):
        return {**_SAFE, "valid": False, "blocked": True,
                "reason": f"forbidden:{action.upper()}"}
    if is_allowed_action(action):
        return {**_SAFE, "valid": True, "blocked": False, "reason": "allowed"}
    return {**_SAFE, "valid": False, "blocked": False,
            "reason": f"unknown:{action.upper()}"}


def validate_review_decision_state(state: str) -> Dict[str, Any]:
    """Validate a review decision state string."""
    is_known = state in REVIEW_DECISION_STATES
    return {
        **_SAFE,
        "valid": is_known,
        "blocked": not is_known,
        "state": state,
        "reason": "valid_state" if is_known else f"unknown_state:{state}",
    }


def validate_review_alert_category(category: str) -> Dict[str, Any]:
    """Validate a review alert category string."""
    is_known = category in REVIEW_ALERT_CATEGORIES
    return {
        **_SAFE,
        "valid": is_known,
        "blocked": not is_known,
        "category": category,
        "reason": "valid_category" if is_known else f"unknown_category:{category}",
    }


def validate_review_severity(severity: str) -> Dict[str, Any]:
    """Validate a review severity string."""
    is_known = severity in REVIEW_SEVERITIES
    return {
        **_SAFE,
        "valid": is_known,
        "blocked": not is_known,
        "severity": severity,
        "reason": "valid_severity" if is_known else f"unknown_severity:{severity}",
    }


def build_review_alert(review_id: str, category: str, severity: str = "INFO") -> Dict[str, Any]:
    """Build a review alert. Blocked if review_id is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    if not category:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_category"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "alert_category": category,
        "alert_severity": severity,
        "requires_human_review": True,
        "auto_approval": False,
    }


def build_human_approval_request(review_id: str, alert_id: str,
                                  checklist_id: str) -> Dict[str, Any]:
    """Build a human approval request. Blocked if any required arg is empty."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    if not alert_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_alert_id"}
    if not checklist_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_checklist_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "alert_id": alert_id,
        "checklist_id": checklist_id,
        "auto_approval": False,
        "requires_manual_review": True,
    }


def build_rollback_review_ticket(review_id: str, trigger_id: str) -> Dict[str, Any]:
    """Build a rollback review ticket. Never auto-rollback."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "trigger_id": trigger_id,
        "auto_rollback": False,
        "requires_manual_review": True,
        "no_automatic_rollback": True,
    }


def build_review_evidence_pack(review_id: str, evidence_links: List[str] = None) -> Dict[str, Any]:
    """Build a review evidence pack."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "evidence_links": list(evidence_links or []),
        "audit_only": True,
    }


def build_review_dashboard(dashboard_id: str, review_id: str) -> Dict[str, Any]:
    """Build a review dashboard. Blocked if dashboard_id is empty."""
    if not dashboard_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_dashboard_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "dashboard_id": dashboard_id,
        "review_id": review_id,
        "alert_count": 0,
        "pending_approvals": 0,
    }


def build_review_export_manifest(review_id: str) -> Dict[str, Any]:
    """Build a review export manifest."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "review_id": review_id,
        "export_sections": [
            "review_alerts", "approval_checklist", "review_decisions",
            "rollback_tickets", "evidence_pack", "audit_trail",
        ],
    }


def build_review_audit_trail(audit_id: str, review_id: str) -> Dict[str, Any]:
    """Build a review audit trail. Blocked if audit_id is empty."""
    if not audit_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_audit_id"}
    return {
        **_SAFE,
        "valid": True,
        "blocked": False,
        "audit_id": audit_id,
        "review_id": review_id,
        "audit_only": True,
    }


def build_review_recommendation(review_id: str, recommendation: str) -> Dict[str, Any]:
    """Build a review recommendation."""
    if not review_id:
        return {**_SAFE, "valid": False, "blocked": True,
                "block_reason": "missing_review_id"}
    from paper_trading.small_capital_strategy.strategy_review_version_v195 import REVIEW_RECOMMENDATIONS
    is_known = recommendation in REVIEW_RECOMMENDATIONS
    return {
        **_SAFE,
        "valid": is_known,
        "blocked": not is_known,
        "review_id": review_id,
        "recommendation": recommendation,
        "no_production_strategy_mutation": True,
        "no_automatic_rollback": True,
        "auto_execution": False,
    }


def get_engine_info() -> Dict[str, Any]:
    """Return engine metadata."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "paper_only": True,
        "review_only": True,
        "human_approval_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "auto_approval": False,
        "auto_rollback": False,
    }
