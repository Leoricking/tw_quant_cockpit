"""
paper_trading/small_capital_strategy/strategy_registry_version_v196.py
Version metadata for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.6"
RELEASE_NAME = "Paper Strategy Decision Registry & Governance Lab"
BASE_RELEASE = "v1.9.5-paper-strategy-review-alert-human-approval-lab"
SCHEMA_VERSION = "196"
POLICY_VERSION = "1.9.6-small-capital-strategy-paper-strategy-decision-registry-governance-lab"

INCLUDED_RELEASES = [
    "Small Capital Strategy v1.7.0",
    "Watchlist Strategy Layer v1.7.1",
    "A/B/C Buy Point Execution Plan v1.7.2",
    "Market Regime Position Control v1.7.3",
    "Small Account Trade Journal v1.7.5",
    "Mistake Taxonomy Review Dashboard v1.7.6",
    "Theme Rotation Scanner v1.7.7",
    "Small Capital Strategy Integration v1.7.8",
    "Small Capital Strategy Stable Rollup v1.7.9",
    "Paper Simulation & Performance Lab v1.8.0",
    "Simulation Scenario Matrix & Stress Test Lab v1.8.1",
    "Parameter Optimization & Walk-Forward Validation Lab v1.8.2",
    "Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3",
    "Position Sizing & Capital Allocation Lab v1.8.4",
    "Portfolio Construction & Rebalancing Lab v1.8.5",
    "End-to-End Small Capital Decision Cockpit v1.8.6",
    "Decision Report Export & Evidence Pack v1.8.7",
    "Paper Decision Workflow Runner v1.8.8",
    "Paper Decision Journal & Review Loop v1.8.9",
    "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0",
    "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1",
    "Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2",
    "Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3",
    "Paper Strategy Monitoring & Drift Detection Lab v1.9.4",
    "Paper Strategy Review Alert & Human Approval Lab v1.9.5",
    "Paper Strategy Decision Registry & Governance Lab v1.9.6",
]

DECISION_SOURCES = [
    "TUNING_PROPOSAL",
    "SANDBOX_VALIDATION",
    "SHADOW_COMPARISON",
    "PROMOTION_PACKAGE",
    "ROLLBACK_PLAN",
    "MONITORING_ALERT",
    "DRIFT_DETECTION",
    "HUMAN_APPROVAL_REQUEST",
    "ROLLBACK_REVIEW_TICKET",
    "MANUAL_REVIEW_NOTE",
]

DECISION_TYPES = [
    "APPROVE_FOR_PAPER_ONLY",
    "REJECT_CANDIDATE",
    "KEEP_MONITORING",
    "KEEP_SHADOW_ONLY",
    "OPEN_ROLLBACK_REVIEW",
    "SUSPEND_CANDIDATE_RULE",
    "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_LONGER_MONITORING",
    "ESCALATE_TO_MANUAL_REVIEW",
    "NO_CHANGE",
]

DECISION_STATES = [
    "DRAFT",
    "PENDING_REVIEW",
    "RECORDED",
    "APPROVED_FOR_PAPER_ONLY",
    "REJECTED",
    "KEEP_MONITORING",
    "KEEP_SHADOW_ONLY",
    "ROLLBACK_REVIEW_REQUIRED",
    "SUSPENDED_FOR_PAPER",
    "NEED_MORE_EVIDENCE",
    "INVALID",
    "ARCHIVED",
]

GOVERNANCE_CHECKS = [
    "decision_id_present",
    "source_present",
    "lineage_present",
    "evidence_present",
    "rationale_present",
    "checklist_present",
    "owner_present",
    "paper_only_flags_present",
    "no_broker_flags_present",
    "no_real_order_flags_present",
    "no_production_mutation_flags_present",
    "no_automatic_rollback_flags_present",
    "no_live_activation_flags_present",
    "not_investment_advice_present",
    "export_path_safe",
    "forbidden_action_words_absent",
    "duplicate_decision_id_absent",
    "immutable_record_policy_present",
    "audit_trail_present",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_or_leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_decision_id",
    "missing_decision_source",
    "missing_decision_lineage",
    "missing_decision_evidence",
    "missing_decision_rationale",
    "missing_governance_checklist",
    "duplicate_decision_id",
    "malformed_registry_input",
    "unsafe_export_path",
    "forbidden_action_words",
]

FORBIDDEN_REGISTRY_ACTIONS = [
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
]

ALLOWED_REGISTRY_ACTIONS = [
    "REGISTRY_VERSION",
    "REGISTER_DECISION",
    "REGISTRY_RECORD",
    "REGISTRY_LIST",
    "REGISTRY_LINEAGE",
    "GOVERNANCE_CHECK",
    "REGISTRY_QUEUE",
    "REGISTRY_VALIDATE",
    "REGISTRY_REPORT",
    "REGISTRY_DASHBOARD",
    "REGISTRY_EXPORT",
    "EVIDENCE_PACK",
    "AUDIT_TRAIL",
    "HEALTH_CHECK",
    "RELEASE_GATE",
    "REGISTRY_SCENARIOS",
    "REGISTRY_FIXTURES",
    "SAFETY_AUDIT",
]

MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 18
MIN_HEALTH_CHECKS = 60

KNOWN_RELEASE_NAMES = list(INCLUDED_RELEASES)


def get_version_info() -> dict:
    """Return version metadata dict."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "governance_only": True,
        "registry_only": True,
        "decision_record_only": True,
        "review_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "no_production_strategy_mutation": True,
        "no_automatic_rollback": True,
        "no_live_strategy_activation": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "decision_sources": DECISION_SOURCES,
        "decision_types": DECISION_TYPES,
        "decision_states": DECISION_STATES,
        "governance_checks": GOVERNANCE_CHECKS,
        "hard_block_conditions": HARD_BLOCK_CONDITIONS,
        "forbidden_registry_actions": FORBIDDEN_REGISTRY_ACTIONS,
        "allowed_registry_actions": ALLOWED_REGISTRY_ACTIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.9.6'."""
    return VERSION == "1.9.6"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_decision_sources() -> list:
    """Return list of decision sources."""
    return list(DECISION_SOURCES)


def get_decision_types() -> list:
    """Return list of decision types."""
    return list(DECISION_TYPES)


def get_decision_states() -> list:
    """Return list of decision states."""
    return list(DECISION_STATES)


def get_governance_checks() -> list:
    """Return list of governance check names."""
    return list(GOVERNANCE_CHECKS)


def get_hard_block_conditions() -> list:
    """Return list of hard block conditions."""
    return list(HARD_BLOCK_CONDITIONS)


def get_forbidden_registry_actions() -> list:
    """Return list of forbidden registry actions."""
    return list(FORBIDDEN_REGISTRY_ACTIONS)


def get_allowed_registry_actions() -> list:
    """Return list of allowed registry actions."""
    return list(ALLOWED_REGISTRY_ACTIONS)
