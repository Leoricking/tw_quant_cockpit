"""
paper_trading/small_capital_strategy/strategy_review_fixtures_v195.py
Fixtures for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional

_SF = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, monitoring_review_only=True, human_approval_only=True,
    rollback_review_only=True, review_only=True, report_only=True,
    audit_only=True, no_real_orders=True, no_broker=True, no_margin=True,
    no_leverage=True, no_production_strategy_mutation=True,
    no_automatic_rollback=True, no_live_strategy_activation=True,
    not_investment_advice=True, demo_only=True, not_for_production=True,
    production_trading_blocked=True, schema_version="195",
)

_CATS = [
    "WIN_RATE_DRIFT_REVIEW", "EXPECTANCY_DRIFT_REVIEW", "PROFIT_FACTOR_DRIFT_REVIEW",
    "DRAWDOWN_REVIEW", "SIGNAL_COLLAPSE_REVIEW", "GUARDRAIL_FALSE_POSITIVE_REVIEW",
    "OPPORTUNITY_LOSS_REVIEW", "EVIDENCE_MISSING_REVIEW", "MARKET_REGIME_MISMATCH_REVIEW",
    "ROLLBACK_TRIGGER_REVIEW", "SAFETY_FLAG_REVIEW", "MANUAL_APPROVAL_REQUIRED",
    "PACKAGE_SUSPENSION_REVIEW", "CONTINUE_MONITORING_REVIEW",
]
_SEVS = ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
_STATS = ["HEALTHY", "PENDING_REVIEW", "REVIEW_REQUIRED", "BLOCKED", "ESCALATED"]


def _fx(n: int, rs: str, rv: str, rc: str,
        drift: bool = False, blocked: bool = False,
        escalated: bool = False) -> Dict[str, Any]:
    return {
        **_SF,
        "fixture_id": f"SMF195-{n:03d}",
        "review_status": rs,
        "review_severity": rv,
        "review_category": rc,
        "drift_detected": drift,
        "blocked": blocked,
        "escalated": escalated,
        "auto_approval": False,
        "auto_rollback": False,
        "requires_human_review": True,
    }


_FIXTURES: List[Dict[str, Any]] = [
    # 1-15: HEALTHY / INFO / NONE
    _fx(1,  "HEALTHY",        "NONE",     "CONTINUE_MONITORING_REVIEW"),
    _fx(2,  "HEALTHY",        "INFO",     "CONTINUE_MONITORING_REVIEW"),
    _fx(3,  "HEALTHY",        "NONE",     "CONTINUE_MONITORING_REVIEW"),
    _fx(4,  "HEALTHY",        "INFO",     "SAFETY_FLAG_REVIEW"),
    _fx(5,  "HEALTHY",        "NONE",     "CONTINUE_MONITORING_REVIEW"),
    _fx(6,  "HEALTHY",        "INFO",     "CONTINUE_MONITORING_REVIEW"),
    _fx(7,  "HEALTHY",        "NONE",     "GUARDRAIL_FALSE_POSITIVE_REVIEW"),
    _fx(8,  "HEALTHY",        "INFO",     "OPPORTUNITY_LOSS_REVIEW"),
    _fx(9,  "HEALTHY",        "NONE",     "CONTINUE_MONITORING_REVIEW"),
    _fx(10, "HEALTHY",        "INFO",     "CONTINUE_MONITORING_REVIEW"),
    _fx(11, "HEALTHY",        "NONE",     "SAFETY_FLAG_REVIEW"),
    _fx(12, "HEALTHY",        "INFO",     "CONTINUE_MONITORING_REVIEW"),
    _fx(13, "HEALTHY",        "NONE",     "CONTINUE_MONITORING_REVIEW"),
    _fx(14, "HEALTHY",        "INFO",     "OPPORTUNITY_LOSS_REVIEW"),
    _fx(15, "HEALTHY",        "NONE",     "CONTINUE_MONITORING_REVIEW"),
    # 16-30: PENDING_REVIEW / LOW-MEDIUM drift
    _fx(16, "PENDING_REVIEW", "LOW",      "WIN_RATE_DRIFT_REVIEW",      drift=True),
    _fx(17, "PENDING_REVIEW", "LOW",      "EXPECTANCY_DRIFT_REVIEW",    drift=True),
    _fx(18, "PENDING_REVIEW", "MEDIUM",   "PROFIT_FACTOR_DRIFT_REVIEW", drift=True),
    _fx(19, "PENDING_REVIEW", "LOW",      "DRAWDOWN_REVIEW",            drift=False),
    _fx(20, "PENDING_REVIEW", "MEDIUM",   "WIN_RATE_DRIFT_REVIEW",      drift=True),
    _fx(21, "PENDING_REVIEW", "LOW",      "EXPECTANCY_DRIFT_REVIEW",    drift=True),
    _fx(22, "PENDING_REVIEW", "MEDIUM",   "PROFIT_FACTOR_DRIFT_REVIEW", drift=True),
    _fx(23, "PENDING_REVIEW", "LOW",      "SIGNAL_COLLAPSE_REVIEW",     drift=False),
    _fx(24, "PENDING_REVIEW", "MEDIUM",   "GUARDRAIL_FALSE_POSITIVE_REVIEW", drift=False),
    _fx(25, "PENDING_REVIEW", "LOW",      "OPPORTUNITY_LOSS_REVIEW",    drift=True),
    _fx(26, "PENDING_REVIEW", "MEDIUM",   "EVIDENCE_MISSING_REVIEW",    drift=False),
    _fx(27, "PENDING_REVIEW", "LOW",      "MARKET_REGIME_MISMATCH_REVIEW", drift=True),
    _fx(28, "PENDING_REVIEW", "MEDIUM",   "ROLLBACK_TRIGGER_REVIEW",    drift=True),
    _fx(29, "PENDING_REVIEW", "LOW",      "SAFETY_FLAG_REVIEW",         drift=False),
    _fx(30, "PENDING_REVIEW", "MEDIUM",   "CONTINUE_MONITORING_REVIEW", drift=False),
    # 31-45: REVIEW_REQUIRED / HIGH drift
    _fx(31, "REVIEW_REQUIRED","HIGH",     "WIN_RATE_DRIFT_REVIEW",      drift=True),
    _fx(32, "REVIEW_REQUIRED","HIGH",     "EXPECTANCY_DRIFT_REVIEW",    drift=True),
    _fx(33, "REVIEW_REQUIRED","HIGH",     "PROFIT_FACTOR_DRIFT_REVIEW", drift=True),
    _fx(34, "REVIEW_REQUIRED","HIGH",     "DRAWDOWN_REVIEW",            drift=True),
    _fx(35, "REVIEW_REQUIRED","HIGH",     "SIGNAL_COLLAPSE_REVIEW",     drift=True),
    _fx(36, "REVIEW_REQUIRED","HIGH",     "MARKET_REGIME_MISMATCH_REVIEW", drift=True),
    _fx(37, "REVIEW_REQUIRED","HIGH",     "ROLLBACK_TRIGGER_REVIEW",    drift=True),
    _fx(38, "REVIEW_REQUIRED","HIGH",     "MANUAL_APPROVAL_REQUIRED",   drift=True),
    _fx(39, "REVIEW_REQUIRED","HIGH",     "PACKAGE_SUSPENSION_REVIEW",  drift=True),
    _fx(40, "REVIEW_REQUIRED","MEDIUM",   "EVIDENCE_MISSING_REVIEW",    drift=False),
    _fx(41, "REVIEW_REQUIRED","HIGH",     "WIN_RATE_DRIFT_REVIEW",      drift=True),
    _fx(42, "REVIEW_REQUIRED","HIGH",     "EXPECTANCY_DRIFT_REVIEW",    drift=True),
    _fx(43, "REVIEW_REQUIRED","MEDIUM",   "GUARDRAIL_FALSE_POSITIVE_REVIEW", drift=False),
    _fx(44, "REVIEW_REQUIRED","HIGH",     "ROLLBACK_TRIGGER_REVIEW",    drift=True),
    _fx(45, "REVIEW_REQUIRED","HIGH",     "MANUAL_APPROVAL_REQUIRED",   drift=True),
    # 46-60: BLOCKED / CRITICAL (safety blocks)
    _fx(46, "BLOCKED",        "CRITICAL", "SAFETY_FLAG_REVIEW",         blocked=True),
    _fx(47, "BLOCKED",        "CRITICAL", "MANUAL_APPROVAL_REQUIRED",   blocked=True),
    _fx(48, "BLOCKED",        "CRITICAL", "ROLLBACK_TRIGGER_REVIEW",    blocked=True),
    _fx(49, "BLOCKED",        "CRITICAL", "EVIDENCE_MISSING_REVIEW",    blocked=True),
    _fx(50, "BLOCKED",        "CRITICAL", "SAFETY_FLAG_REVIEW",         blocked=True),
    _fx(51, "BLOCKED",        "CRITICAL", "MANUAL_APPROVAL_REQUIRED",   blocked=True),
    _fx(52, "BLOCKED",        "CRITICAL", "WIN_RATE_DRIFT_REVIEW",      blocked=True, drift=True),
    _fx(53, "BLOCKED",        "CRITICAL", "DRAWDOWN_REVIEW",            blocked=True, drift=True),
    _fx(54, "BLOCKED",        "CRITICAL", "SIGNAL_COLLAPSE_REVIEW",     blocked=True, drift=True),
    _fx(55, "BLOCKED",        "CRITICAL", "SAFETY_FLAG_REVIEW",         blocked=True),
    _fx(56, "BLOCKED",        "CRITICAL", "EVIDENCE_MISSING_REVIEW",    blocked=True),
    _fx(57, "BLOCKED",        "CRITICAL", "PACKAGE_SUSPENSION_REVIEW",  blocked=True),
    _fx(58, "BLOCKED",        "CRITICAL", "ROLLBACK_TRIGGER_REVIEW",    blocked=True, drift=True),
    _fx(59, "BLOCKED",        "CRITICAL", "SAFETY_FLAG_REVIEW",         blocked=True),
    _fx(60, "BLOCKED",        "CRITICAL", "MANUAL_APPROVAL_REQUIRED",   blocked=True),
    # 61-75: ESCALATED / CRITICAL drift
    _fx(61, "ESCALATED",      "CRITICAL", "WIN_RATE_DRIFT_REVIEW",      drift=True,  escalated=True),
    _fx(62, "ESCALATED",      "CRITICAL", "EXPECTANCY_DRIFT_REVIEW",    drift=True,  escalated=True),
    _fx(63, "ESCALATED",      "CRITICAL", "PROFIT_FACTOR_DRIFT_REVIEW", drift=True,  escalated=True),
    _fx(64, "ESCALATED",      "CRITICAL", "DRAWDOWN_REVIEW",            drift=True,  escalated=True),
    _fx(65, "ESCALATED",      "CRITICAL", "SIGNAL_COLLAPSE_REVIEW",     drift=True,  escalated=True),
    _fx(66, "ESCALATED",      "HIGH",     "MARKET_REGIME_MISMATCH_REVIEW", drift=True, escalated=True),
    _fx(67, "ESCALATED",      "CRITICAL", "ROLLBACK_TRIGGER_REVIEW",    drift=True,  escalated=True),
    _fx(68, "ESCALATED",      "CRITICAL", "MANUAL_APPROVAL_REQUIRED",   drift=True,  escalated=True),
    _fx(69, "ESCALATED",      "HIGH",     "PACKAGE_SUSPENSION_REVIEW",  drift=True,  escalated=True),
    _fx(70, "ESCALATED",      "CRITICAL", "WIN_RATE_DRIFT_REVIEW",      drift=True,  escalated=True),
    _fx(71, "ESCALATED",      "HIGH",     "EXPECTANCY_DRIFT_REVIEW",    drift=True,  escalated=True),
    _fx(72, "ESCALATED",      "CRITICAL", "DRAWDOWN_REVIEW",            drift=True,  escalated=True),
    _fx(73, "ESCALATED",      "HIGH",     "ROLLBACK_TRIGGER_REVIEW",    drift=True,  escalated=True),
    _fx(74, "ESCALATED",      "CRITICAL", "MANUAL_APPROVAL_REQUIRED",   drift=True,  escalated=True),
    _fx(75, "ESCALATED",      "HIGH",     "PACKAGE_SUSPENSION_REVIEW",  drift=True,  escalated=True),
]

assert len(_FIXTURES) == 75, f"Expected 75 fixtures, got {len(_FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    return list(_FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Optional[Dict[str, Any]]:
    for f in _FIXTURES:
        if f["fixture_id"] == fixture_id:
            return f
    return None


def get_fixture_ids() -> List[str]:
    return [f["fixture_id"] for f in _FIXTURES]


def get_fixtures_by_status(review_status: str) -> List[Dict[str, Any]]:
    return [f for f in _FIXTURES if f["review_status"] == review_status]


def get_fixtures_by_severity(review_severity: str) -> List[Dict[str, Any]]:
    return [f for f in _FIXTURES if f["review_severity"] == review_severity]


def get_blocked_fixtures() -> List[Dict[str, Any]]:
    return [f for f in _FIXTURES if f.get("blocked") is True]


def get_escalated_fixtures() -> List[Dict[str, Any]]:
    return [f for f in _FIXTURES if f.get("escalated") is True]


def get_drift_fixtures() -> List[Dict[str, Any]]:
    return [f for f in _FIXTURES if f.get("drift_detected") is True]
