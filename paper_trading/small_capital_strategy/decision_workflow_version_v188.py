"""
paper_trading/small_capital_strategy/decision_workflow_version_v188.py
Version metadata for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only.
[!] Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.8.8"
RELEASE_NAME = "Paper Decision Workflow Runner"
BASE_RELEASE = "v1.8.7-decision-report-export-evidence-pack"
SCHEMA_VERSION = "188"
POLICY_VERSION = "1.8.8-small-capital-strategy-paper-decision-workflow-runner"

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
]

WORKFLOW_TYPES = [
    "daily_workflow",
    "weekly_workflow",
    "pre_market_workflow",
    "post_market_workflow",
    "watchlist_workflow",
    "candidate_review_workflow",
    "risk_review_workflow",
    "portfolio_review_workflow",
    "blocked_market_workflow",
    "report_generation_workflow",
    "evidence_pack_workflow",
    "audit_trail_workflow",
]

WORKFLOW_STEPS = [
    "load_config",
    "validate_safety_flags",
    "load_watchlist",
    "load_candidates",
    "validate_candidates",
    "evaluate_market_regime",
    "evaluate_theme_rotation",
    "evaluate_abc_buy_points",
    "evaluate_position_sizing",
    "evaluate_portfolio_exposure",
    "evaluate_monte_carlo_risk",
    "evaluate_block_reasons",
    "run_decision_cockpit",
    "generate_decision_report",
    "generate_evidence_pack",
    "generate_audit_trail",
    "generate_dashboard_payload",
    "export_manifest",
    "final_validation",
    "final_workflow_grade",
]

FINAL_WORKFLOW_GRADES = [
    "COMPLETE",
    "REVIEW_REQUIRED",
    "PARTIAL",
    "BLOCKED",
    "INVALID",
]

ALLOWED_WORKFLOW_ACTIONS = [
    "OBSERVE",
    "WAIT",
    "PAPER_PLAN_READY",
    "PAPER_ENTRY_ALLOWED",
    "PAPER_ADD_ALLOWED",
    "REDUCE_RISK",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "NO_TRADE",
    "RESEARCH_ONLY",
    "READ_REPORT",
    "SIMULATE_ONLY",
    "STRESS_TEST_ONLY",
    "VALIDATION_ONLY",
    "ALLOCATION_ONLY",
    "PORTFOLIO_ONLY",
    "DECISION_ONLY",
    "REPORT_ONLY",
    "AUDIT_ONLY",
    "WORKFLOW_ONLY",
]

FORBIDDEN_WORKFLOW_ACTIONS = [
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

MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 21
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
        "decision_only": True,
        "workflow_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "workflow_types": WORKFLOW_TYPES,
        "workflow_steps": WORKFLOW_STEPS,
        "final_workflow_grades": FINAL_WORKFLOW_GRADES,
        "allowed_workflow_actions": ALLOWED_WORKFLOW_ACTIONS,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.8.8'."""
    return VERSION == "1.8.8"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version."""
    return VERSION >= min_version


def get_workflow_types() -> list:
    """Return list of supported workflow types."""
    return list(WORKFLOW_TYPES)


def get_workflow_steps() -> list:
    """Return list of workflow steps."""
    return list(WORKFLOW_STEPS)


def get_final_workflow_grades() -> list:
    """Return list of final workflow grades."""
    return list(FINAL_WORKFLOW_GRADES)


def get_allowed_workflow_actions() -> list:
    """Return list of allowed workflow actions."""
    return list(ALLOWED_WORKFLOW_ACTIONS)


def get_forbidden_workflow_actions() -> list:
    """Return list of forbidden workflow actions."""
    return list(FORBIDDEN_WORKFLOW_ACTIONS)
