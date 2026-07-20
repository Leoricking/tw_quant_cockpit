"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v201.py
v2.0.1 Paper Cockpit — 80 Scenarios (PC201-001 through PC201-080)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_BASE = {
    "schema_version": "201",
    "paper_only": True,
    "no_real_orders": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "version": "2.0.1",
}


def _s(n: int, category: str, title: str, description: str, **extra) -> Dict[str, Any]:
    d = dict(_BASE)
    d["id"] = f"PC201-{n:03d}"
    d["scenario_id"] = d["id"]
    d["category"] = category
    d["title"] = title
    d["description"] = description
    d.update(extra)
    return d


SCENARIOS: List[Dict[str, Any]] = [
    # --- Daily Workflow (001-010) ---
    _s(1, "daily_workflow", "Full daily workflow run — bull regime", "Run complete daily workflow with 3 candidates in bull market", final_actions=["PAPER_BUY_PLAN", "WATCH", "NO_ENTRY"]),
    _s(2, "daily_workflow", "Full daily workflow run — bear regime", "Run complete daily workflow in bear market, all NO_ENTRY", final_actions=["NO_ENTRY", "NO_ENTRY", "NO_ENTRY"]),
    _s(3, "daily_workflow", "Empty candidate list", "Run daily workflow with no candidates, returns empty result", candidates=[]),
    _s(4, "daily_workflow", "Single candidate PAPER_BUY_PLAN", "Single candidate passes all checks => PAPER_BUY_PLAN", final_action="PAPER_BUY_PLAN"),
    _s(5, "daily_workflow", "Single candidate WAIT", "Single candidate with no ABC signal, no position => WAIT", final_action="WAIT"),
    _s(6, "daily_workflow", "Single candidate WATCH", "Single candidate with position, no add signal => WATCH", final_action="WATCH"),
    _s(7, "daily_workflow", "Single candidate PAPER_ADD_PLAN", "Candidate with existing position, valid ABC => PAPER_ADD_PLAN", final_action="PAPER_ADD_PLAN"),
    _s(8, "daily_workflow", "Single candidate PAPER_REDUCE_PLAN", "Candidate with 25%+ profit position => PAPER_REDUCE_PLAN", final_action="PAPER_REDUCE_PLAN"),
    _s(9, "daily_workflow", "Single candidate PAPER_EXIT_PLAN", "Candidate with -8% loss => PAPER_EXIT_PLAN", final_action="PAPER_EXIT_PLAN"),
    _s(10, "daily_workflow", "Multi-candidate ranking", "5 candidates ranked by total_score descending", candidate_count=5),

    # --- Final Actions (011-017) ---
    _s(11, "final_action", "WATCH action classification", "Classify WATCH: position exists, no add signal", expected_action="WATCH"),
    _s(12, "final_action", "WAIT action classification", "Classify WAIT: no position, no ABC signal", expected_action="WAIT"),
    _s(13, "final_action", "PAPER_BUY_PLAN action classification", "Classify PAPER_BUY_PLAN: valid ABC, no position", expected_action="PAPER_BUY_PLAN"),
    _s(14, "final_action", "PAPER_ADD_PLAN action classification", "Classify PAPER_ADD_PLAN: valid ABC, has position", expected_action="PAPER_ADD_PLAN"),
    _s(15, "final_action", "PAPER_REDUCE_PLAN action classification", "Classify PAPER_REDUCE_PLAN: position profit >= 25%", expected_action="PAPER_REDUCE_PLAN"),
    _s(16, "final_action", "PAPER_EXIT_PLAN action classification", "Classify PAPER_EXIT_PLAN: position loss <= -8%", expected_action="PAPER_EXIT_PLAN"),
    _s(17, "final_action", "NO_ENTRY action classification", "Classify NO_ENTRY: blocking no-entry reasons present", expected_action="NO_ENTRY"),

    # --- No-Entry Reasons (018-030) ---
    _s(18, "no_entry_reason", "trend_broken reason", "Evaluate trend_broken no-entry reason", reason_code="trend_broken"),
    _s(19, "no_entry_reason", "below_20ma reason", "Evaluate below_20ma no-entry reason", reason_code="below_20ma"),
    _s(20, "no_entry_reason", "below_60ma reason", "Evaluate below_60ma no-entry reason", reason_code="below_60ma"),
    _s(21, "no_entry_reason", "volume_overheated reason", "Evaluate volume_overheated no-entry reason", reason_code="volume_overheated"),
    _s(22, "no_entry_reason", "volume_dry_up_failed reason", "Evaluate volume_dry_up_failed no-entry reason", reason_code="volume_dry_up_failed"),
    _s(23, "no_entry_reason", "institutional_selling reason", "Evaluate institutional_selling no-entry reason", reason_code="institutional_selling"),
    _s(24, "no_entry_reason", "margin_overheated reason", "Evaluate margin_overheated no-entry reason", reason_code="margin_overheated"),
    _s(25, "no_entry_reason", "market_risk_high reason", "Evaluate market_risk_high no-entry reason", reason_code="market_risk_high"),
    _s(26, "no_entry_reason", "risk_budget_exceeded reason", "Evaluate risk_budget_exceeded no-entry reason", reason_code="risk_budget_exceeded"),
    _s(27, "no_entry_reason", "position_size_too_large reason", "Evaluate position_size_too_large no-entry reason", reason_code="position_size_too_large"),
    _s(28, "no_entry_reason", "stop_loss_too_wide reason", "Evaluate stop_loss_too_wide no-entry reason", reason_code="stop_loss_too_wide"),
    _s(29, "no_entry_reason", "missing_required_signal reason", "Evaluate missing_required_signal no-entry reason", reason_code="missing_required_signal"),
    _s(30, "no_entry_reason", "human_review_required reason", "human_review_required is always appended", reason_code="human_review_required"),

    # --- Enhanced Decision Ticket (031-040) ---
    _s(31, "decision_ticket", "Build ticket with all 21 fields", "EnhancedDecisionTicket must have all 21 required fields", field_count=21),
    _s(32, "decision_ticket", "Ticket schema_version is 201", "Ticket schema_version must equal '201'", expected_schema="201"),
    _s(33, "decision_ticket", "Ticket paper_only=True", "Ticket paper_only flag must be True", paper_only=True),
    _s(34, "decision_ticket", "Ticket no_broker=True", "Ticket no_broker flag must be True"),
    _s(35, "decision_ticket", "Ticket final_action PAPER_BUY_PLAN", "Ticket with PAPER_BUY_PLAN final_action", final_action="PAPER_BUY_PLAN"),
    _s(36, "decision_ticket", "Ticket final_action NO_ENTRY", "Ticket with NO_ENTRY and populated no_entry_reasons", final_action="NO_ENTRY"),
    _s(37, "decision_ticket", "Ticket total_score computed from 6 scores", "total_score = mean of 6 sub-scores", sub_scores=6),
    _s(38, "decision_ticket", "Ticket invalid_conditions list", "invalid_conditions is a list of blocking reason codes"),
    _s(39, "decision_ticket", "Ticket position_size_reason string", "position_size_reason is non-empty string"),
    _s(40, "decision_ticket", "Ticket ticket_triggers_broker=False", "Ticket never triggers broker", ticket_triggers_broker=False),

    # --- Risk Budget (041-047) ---
    _s(41, "risk_budget", "Risk budget NORMAL status", "100% remaining => NORMAL status", expected_status="NORMAL"),
    _s(42, "risk_budget", "Risk budget CAUTION status", "35% remaining => CAUTION status", expected_status="CAUTION"),
    _s(43, "risk_budget", "Risk budget WARNING status", "15% remaining => WARNING status", expected_status="WARNING"),
    _s(44, "risk_budget", "Risk budget CRITICAL status", "5% remaining => CRITICAL status", expected_status="CRITICAL"),
    _s(45, "risk_budget", "Risk budget blocks new entry", "0% remaining => NO_ENTRY final action", blocks_entry=True),
    _s(46, "risk_budget", "Risk budget risk_budget_ok=False when <10%", "risk_budget_ok is False when remaining < 10%"),
    _s(47, "risk_budget", "Risk budget used_pct = 100 - remaining", "risk_budget_used_pct = 100 - remaining"),

    # --- CLI Display (048-055) ---
    _s(48, "cli_display", "CLI display top candidates list", "CLIDisplayOutput contains top_candidates rows"),
    _s(49, "cli_display", "CLI display row fields", "CLIDisplayRow has all required display fields"),
    _s(50, "cli_display", "CLI display entry_allowed=True for PAPER_BUY_PLAN", "Row with PAPER_BUY_PLAN has entry_allowed=True"),
    _s(51, "cli_display", "CLI display entry_allowed=False for NO_ENTRY", "Row with NO_ENTRY has entry_allowed=False"),
    _s(52, "cli_display", "CLI display blocked_reason non-empty for blocked candidates", "Blocked candidate has non-empty blocked_reason"),
    _s(53, "cli_display", "CLI display human_review_flag=True always", "human_review_flag is always True"),
    _s(54, "cli_display", "CLI display action counts sum to total", "Sum of action counts equals total_candidates"),
    _s(55, "cli_display", "CLI display paper_only=True", "CLIDisplayOutput paper_only=True"),

    # --- Candidate Ranking (056-060) ---
    _s(56, "candidate_ranking", "Candidates ranked by total_score descending", "Rank 1 has highest total_score"),
    _s(57, "candidate_ranking", "Rank numbers are sequential starting at 1", "Ranks go 1, 2, 3..."),
    _s(58, "candidate_ranking", "CandidateRankEntry schema_version=201", "CandidateRankEntry schema_version='201'"),
    _s(59, "candidate_ranking", "CandidateRankEntry final_action is valid", "final_action is in DAILY_FINAL_ACTIONS"),
    _s(60, "candidate_ranking", "Empty candidate list => empty ranking", "Empty input => empty ranking list"),

    # --- Safety Guards (061-068) ---
    _s(61, "safety", "NO_REAL_ORDERS=True", "Module constant NO_REAL_ORDERS must be True"),
    _s(62, "safety", "BROKER_EXECUTION_ENABLED=False", "Module constant BROKER_EXECUTION_ENABLED must be False"),
    _s(63, "safety", "PRODUCTION_TRADING_BLOCKED=True", "Module constant PRODUCTION_TRADING_BLOCKED must be True"),
    _s(64, "safety", "SAFETY_FLAGS paper_only=True", "SAFETY_FLAGS['paper_only'] is True"),
    _s(65, "safety", "SAFETY_FLAGS cockpit_executes_order=False", "SAFETY_FLAGS['cockpit_executes_order'] is False"),
    _s(66, "safety", "SAFETY_FLAGS broker_execution_enabled=False", "SAFETY_FLAGS['broker_execution_enabled'] is False"),
    _s(67, "safety", "FORBIDDEN_ACTIONS contains BUY SELL ORDER", "All core forbidden words present"),
    _s(68, "safety", "PAPER_BUY_PLAN is ALLOWED (contains PLAN)", "PAPER_BUY_PLAN is not in FORBIDDEN_ACTIONS"),

    # --- Backward Compatibility (069-073) ---
    _s(69, "backward_compat", "v2.0.0 module still importable", "paper_cockpit_v200 can be imported alongside v2.0.1"),
    _s(70, "backward_compat", "v2.0.0 VERSION still 2.0.0", "v2.0.0 module VERSION unchanged"),
    _s(71, "backward_compat", "v2.0.0 SCHEMA_VERSION still 200", "v2.0.0 module SCHEMA_VERSION unchanged"),
    _s(72, "backward_compat", "v2.0.0 models still instantiate", "All v2.0.0 dataclasses still work"),
    _s(73, "backward_compat", "COVERED_VERSIONS includes 2.0.0", "v2.0.1 COVERED_VERSIONS includes 2.0.0"),

    # --- GUI Tabs (074-077) ---
    _s(74, "gui", "PANEL_VERSION is 2.0.1", "GUI panel PANEL_VERSION must be '2.0.1'"),
    _s(75, "gui", "daily_workflow_v201 tab present", "New tab daily_workflow_v201 in panel tabs"),
    _s(76, "gui", "no_entry_reason_detail tab present", "New tab no_entry_reason_detail in panel tabs"),
    _s(77, "gui", "decision_ticket_v201 tab present", "New tab decision_ticket_v201 in panel tabs"),

    # --- Health & Gate (078-080) ---
    _s(78, "health", "Health check all_passed=True", "run_health_check returns all_passed=True"),
    _s(79, "gate", "Release gate gate_passed=True", "run_release_gate returns gate_passed=True"),
    _s(80, "integration", "End-to-end daily workflow integration", "Full workflow from input to CLI display output"),
]

assert len(SCENARIOS) == 80, f"Expected 80 scenarios, got {len(SCENARIOS)}"
assert all(s["schema_version"] == "201" for s in SCENARIOS), "All scenarios must have schema_version=201"
assert all(s["paper_only"] is True for s in SCENARIOS), "All scenarios must have paper_only=True"
assert all(s["no_real_orders"] is True for s in SCENARIOS), "All scenarios must have no_real_orders=True"
assert len({s["id"] for s in SCENARIOS}) == 80, "Scenario IDs must be unique"
