"""
paper_trading/small_capital_strategy/strategy_review_scenarios_v195.py
Scenarios for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
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


def _sc(n: int, name: str, stype: str, outcome: str, **kw) -> Dict[str, Any]:
    sid = f"SP195-{n:03d}"
    d = {**_SF, "scenario_id": sid, "name": name, "scenario_type": stype,
         "expected_outcome": outcome, "auto_approval": False,
         "auto_rollback": False}
    d.update(kw)
    return d


_SCENARIOS: List[Dict[str, Any]] = [
    # 1-10: Core review workflow scenarios
    _sc(1, "Complete Review Alert Package", "complete_review",
        "Full review alert package built successfully",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(2, "Healthy Alert Keep Monitoring", "healthy_review",
        "Healthy monitoring; continue monitoring recommended",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(3, "Critical Drift Opens Rollback Review", "rollback_review_ticket",
        "Critical drift triggers rollback review ticket; no auto-rollback",
        drift_detected=True, blocked=False, review_severity="CRITICAL"),
    _sc(4, "Missing Evidence Requires More Evidence", "missing_evidence_review",
        "Missing review evidence triggers NEED_MORE_EVIDENCE state",
        drift_detected=False, blocked=True, review_severity="MEDIUM"),
    _sc(5, "Manual Approval Required", "manual_approval_required",
        "Alert severity HIGH triggers manual approval request",
        drift_detected=True, blocked=False, review_severity="HIGH"),
    _sc(6, "Approved For Paper Only", "approved_for_paper_only",
        "Human reviewer approves candidate for paper-only continuation",
        drift_detected=False, blocked=False, review_severity="LOW"),
    _sc(7, "Rejected Candidate", "rejected_candidate",
        "Human reviewer rejects candidate rule; no live activation",
        drift_detected=True, blocked=False, review_severity="HIGH"),
    _sc(8, "Keep Shadow Only", "keep_shadow_only",
        "Alert triggers keep-shadow-only decision; no promotion",
        drift_detected=True, blocked=False, review_severity="MEDIUM"),
    _sc(9, "Suspend Candidate Rule", "suspend_candidate_rule",
        "Alert triggers suspension of candidate rule from paper queue",
        drift_detected=True, blocked=False, review_severity="HIGH"),
    _sc(10, "Rollback Review Ticket Generated", "rollback_review_ticket",
        "Rollback review ticket generated; requires human sign-off",
        drift_detected=True, blocked=False, review_severity="CRITICAL"),
    # 11-19: Safety block scenarios
    _sc(11, "Malformed Review Input Blocked", "safety_block",
        "Malformed input blocked at safety gate",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(12, "Missing Monitoring Alert Source Blocked", "safety_block",
        "Missing monitoring alert source causes safety block",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(13, "Missing Human Approval Checklist Blocked", "safety_block",
        "Missing checklist causes safety block",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(14, "Missing Decision Rationale Blocked", "safety_block",
        "Missing decision rationale causes safety block",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(15, "Unsafe Export Path Blocked", "safety_block",
        "Unsafe export path blocked by safety layer",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(16, "Production Mutation Blocked", "safety_block",
        "Production strategy mutation attempt blocked",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(17, "Automatic Rollback Blocked", "safety_block",
        "Automatic rollback attempt blocked; only review ticket allowed",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(18, "Live Activation Blocked", "safety_block",
        "Live strategy activation attempt blocked",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(19, "Broker Request Blocked", "safety_block",
        "Broker order request blocked at safety gate",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    # 20: Complete review evidence pack
    _sc(20, "Complete Review Evidence Pack", "complete_review",
        "Full evidence pack assembled; no auto-approval",
        drift_detected=False, blocked=False, review_severity="INFO"),
    # 21-30: Win rate drift review scenarios
    _sc(21, "Win Rate Drift Low Severity", "drift_review",
        "Win rate drift detected at LOW severity; keep monitoring",
        drift_detected=True, blocked=False, review_severity="LOW",
        alert_category="WIN_RATE_DRIFT_REVIEW"),
    _sc(22, "Win Rate Drift Medium Severity", "drift_review",
        "Win rate drift at MEDIUM severity triggers review alert",
        drift_detected=True, blocked=False, review_severity="MEDIUM",
        alert_category="WIN_RATE_DRIFT_REVIEW"),
    _sc(23, "Win Rate Drift High Severity", "drift_review",
        "Win rate drift HIGH triggers manual approval request",
        drift_detected=True, blocked=False, review_severity="HIGH",
        alert_category="WIN_RATE_DRIFT_REVIEW"),
    _sc(24, "Expectancy Drift Review", "drift_review",
        "Expectancy drift triggers review alert",
        drift_detected=True, blocked=False, review_severity="MEDIUM",
        alert_category="EXPECTANCY_DRIFT_REVIEW"),
    _sc(25, "Profit Factor Drift Review", "drift_review",
        "Profit factor drift triggers evidence review",
        drift_detected=True, blocked=False, review_severity="MEDIUM",
        alert_category="PROFIT_FACTOR_DRIFT_REVIEW"),
    _sc(26, "Drawdown Review Alert", "drift_review",
        "Drawdown breach triggers human review",
        drift_detected=True, blocked=False, review_severity="HIGH",
        alert_category="DRAWDOWN_REVIEW"),
    _sc(27, "Signal Collapse Review", "drift_review",
        "Signal collapse triggers urgent review",
        drift_detected=True, blocked=False, review_severity="HIGH",
        alert_category="SIGNAL_COLLAPSE_REVIEW"),
    _sc(28, "Guardrail False Positive Review", "drift_review",
        "Guardrail false positive review alert generated",
        drift_detected=False, blocked=False, review_severity="LOW",
        alert_category="GUARDRAIL_FALSE_POSITIVE_REVIEW"),
    _sc(29, "Opportunity Loss Review", "drift_review",
        "Opportunity loss alert triggers paper-only review",
        drift_detected=True, blocked=False, review_severity="LOW",
        alert_category="OPPORTUNITY_LOSS_REVIEW"),
    _sc(30, "Evidence Missing Review", "missing_evidence_review",
        "Evidence gap triggers evidence-missing review alert",
        drift_detected=False, blocked=True, review_severity="MEDIUM",
        alert_category="EVIDENCE_MISSING_REVIEW"),
    # 31-40: Market regime and rollback scenarios
    _sc(31, "Market Regime Mismatch Review", "drift_review",
        "Market regime mismatch triggers keep-shadow-only recommendation",
        drift_detected=True, blocked=False, review_severity="HIGH",
        alert_category="MARKET_REGIME_MISMATCH_REVIEW"),
    _sc(32, "Rollback Trigger Review Critical", "rollback_review_ticket",
        "Rollback trigger review at CRITICAL level; ticket opened",
        drift_detected=True, blocked=False, review_severity="CRITICAL",
        alert_category="ROLLBACK_TRIGGER_REVIEW"),
    _sc(33, "Safety Flag Review Info", "safety_review",
        "Safety flag review at INFO level passes audit",
        drift_detected=False, blocked=False, review_severity="INFO",
        alert_category="SAFETY_FLAG_REVIEW"),
    _sc(34, "Manual Approval Required Critical", "manual_approval_required",
        "CRITICAL alert requires immediate manual approval",
        drift_detected=True, blocked=False, review_severity="CRITICAL",
        alert_category="MANUAL_APPROVAL_REQUIRED"),
    _sc(35, "Package Suspension Review", "package_suspension_review",
        "Package suspension review triggered by multiple HIGH alerts",
        drift_detected=True, blocked=False, review_severity="HIGH",
        alert_category="PACKAGE_SUSPENSION_REVIEW"),
    _sc(36, "Continue Monitoring Review Info", "healthy_review",
        "Continue monitoring review; all checks pass at INFO",
        drift_detected=False, blocked=False, review_severity="INFO",
        alert_category="CONTINUE_MONITORING_REVIEW"),
    _sc(37, "Rollback Review Ticket No Auto Rollback", "rollback_review_ticket",
        "Ticket created; auto-rollback confirmed False",
        drift_detected=True, blocked=False, review_severity="HIGH"),
    _sc(38, "Escalation To Manual Review", "escalated_review",
        "Alert escalated to manual review due to repeated drift",
        drift_detected=True, blocked=False, review_severity="CRITICAL",
        escalated=True),
    _sc(39, "Require More Evidence Decision", "missing_evidence_review",
        "Review paused; more evidence required before decision",
        drift_detected=False, blocked=False, review_severity="MEDIUM"),
    _sc(40, "Require Longer Monitoring Decision", "healthy_review",
        "Decision deferred; require longer monitoring window",
        drift_detected=False, blocked=False, review_severity="LOW"),
    # 41-50: Decision state scenarios
    _sc(41, "Draft Decision State", "decision_state_review",
        "Review in DRAFT state; not yet submitted",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(42, "Pending Review State", "decision_state_review",
        "Review in PENDING_REVIEW state awaiting human action",
        drift_detected=False, blocked=False, review_severity="LOW"),
    _sc(43, "Approved For Paper Only State", "approved_for_paper_only",
        "Decision reaches APPROVED_FOR_PAPER_ONLY; no live activation",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(44, "Keep Monitoring State", "healthy_review",
        "Decision reaches KEEP_MONITORING; continue observation",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(45, "Keep Shadow Only State", "keep_shadow_only",
        "Decision KEEP_SHADOW_ONLY; no paper promotion",
        drift_detected=True, blocked=False, review_severity="MEDIUM"),
    _sc(46, "Rejected Decision State", "rejected_candidate",
        "Decision REJECTED; candidate removed from queue",
        drift_detected=True, blocked=False, review_severity="HIGH"),
    _sc(47, "Rollback Review Required State", "rollback_review_ticket",
        "Decision reaches ROLLBACK_REVIEW_REQUIRED; ticket opened",
        drift_detected=True, blocked=False, review_severity="CRITICAL"),
    _sc(48, "Suspended For Paper State", "suspend_candidate_rule",
        "Decision SUSPENDED_FOR_PAPER; rule suspended from paper queue",
        drift_detected=True, blocked=False, review_severity="HIGH"),
    _sc(49, "Need More Evidence State", "missing_evidence_review",
        "Decision NEED_MORE_EVIDENCE; review paused",
        drift_detected=False, blocked=False, review_severity="MEDIUM"),
    _sc(50, "Invalid Decision State", "safety_block",
        "Invalid input triggers INVALID decision state",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    # 51-60: Queue and SLA scenarios
    _sc(51, "Empty Review Queue", "healthy_review",
        "Review queue is empty; no pending alerts",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(52, "Review Queue With One Pending", "decision_state_review",
        "Review queue has one pending item; SLA active",
        drift_detected=False, blocked=False, review_severity="LOW"),
    _sc(53, "Review Queue Multiple Critical", "escalated_review",
        "Multiple CRITICAL alerts in queue trigger escalation",
        drift_detected=True, blocked=False, review_severity="CRITICAL",
        escalated=True),
    _sc(54, "SLA Within Deadline", "healthy_review",
        "Review completed within SLA deadline",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(55, "SLA Breach Escalation", "escalated_review",
        "SLA breach triggers escalation to manual review",
        drift_detected=False, blocked=False, review_severity="HIGH",
        escalated=True),
    _sc(56, "Escalation Rule Trigger High", "escalated_review",
        "HIGH severity triggers escalation rule",
        drift_detected=True, blocked=False, review_severity="HIGH",
        escalated=True),
    _sc(57, "Escalation Rule Trigger Critical", "escalated_review",
        "CRITICAL severity triggers immediate escalation",
        drift_detected=True, blocked=False, review_severity="CRITICAL",
        escalated=True),
    _sc(58, "No Auto Escalation For Low", "healthy_review",
        "LOW severity does not trigger auto-escalation; manual only",
        drift_detected=False, blocked=False, review_severity="LOW"),
    _sc(59, "Review Evidence Link Valid", "complete_review",
        "Review evidence link points to valid paper-only source",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(60, "Review Finding Documented", "complete_review",
        "Review finding documented in audit trail",
        drift_detected=False, blocked=False, review_severity="INFO"),
    # 61-75: Additional safety and edge case scenarios
    _sc(61, "Real Order Request Blocked At Review Gate", "safety_block",
        "Real order request detected in review input; blocked immediately",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(62, "Margin Request Blocked At Review Gate", "safety_block",
        "Margin request blocked before review begins",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(63, "Leverage Request Blocked At Review Gate", "safety_block",
        "Leverage request blocked before review begins",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(64, "Production DB Write Blocked", "safety_block",
        "Production DB write attempt blocked by review safety gate",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(65, "Missing Drift Detection Source Blocked", "safety_block",
        "Missing drift detection source causes block at review gate",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(66, "Forbidden Word In Input Blocked", "safety_block",
        "Forbidden word BUY in review input; blocked immediately",
        drift_detected=False, blocked=True, review_severity="CRITICAL"),
    _sc(67, "Approval Checklist Complete", "approved_for_paper_only",
        "Approval checklist fully completed; decision recorded as paper-only",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(68, "Approval Checklist Incomplete Blocked", "safety_block",
        "Incomplete checklist blocks approval decision",
        drift_detected=False, blocked=True, review_severity="HIGH"),
    _sc(69, "Decision Rationale Required", "missing_evidence_review",
        "Decision rationale must be provided before state transition",
        drift_detected=False, blocked=True, review_severity="MEDIUM"),
    _sc(70, "Full Evidence Pack Before Approval", "complete_review",
        "Full evidence pack assembled before any approval decision",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(71, "Audit Trail Covers All Events", "complete_review",
        "Audit trail captures all review events for traceability",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(72, "Dashboard Shows Zero Auto Approvals", "healthy_review",
        "Dashboard confirms zero automatic approvals; all manual",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(73, "Export Manifest Paper Only", "complete_review",
        "Export manifest marks all sections as paper-only",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(74, "Review Queue Summary No Live Decisions", "healthy_review",
        "Queue summary shows no live-strategy decisions pending",
        drift_detected=False, blocked=False, review_severity="INFO"),
    _sc(75, "Full Review Alert Human Approval Cycle", "complete_review",
        "Full cycle: alert → checklist → human decision → evidence → audit",
        drift_detected=False, blocked=False, review_severity="MEDIUM"),
]

assert len(_SCENARIOS) == 75, f"Expected 75 scenarios, got {len(_SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    return list(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    for s in _SCENARIOS:
        if s["scenario_id"] == scenario_id:
            return s
    return {}


def get_scenario_ids() -> List[str]:
    return [s["scenario_id"] for s in _SCENARIOS]


def get_scenarios_by_type(scenario_type: str) -> List[Dict[str, Any]]:
    return [s for s in _SCENARIOS if s["scenario_type"] == scenario_type]


def get_blocked_scenarios() -> List[Dict[str, Any]]:
    return [s for s in _SCENARIOS if s.get("blocked") is True]


def get_escalated_scenarios() -> List[Dict[str, Any]]:
    return [s for s in _SCENARIOS if s.get("escalated") is True]


def get_drift_scenarios() -> List[Dict[str, Any]]:
    return [s for s in _SCENARIOS if s.get("drift_detected") is True]
