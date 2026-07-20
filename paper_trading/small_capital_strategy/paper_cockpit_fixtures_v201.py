"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v201.py
v2.0.1 Paper Cockpit — 80 Fixtures (PC201-F001 through PC201-F080)
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


def _f(n: int, category: str, title: str, **data) -> Dict[str, Any]:
    d = dict(_BASE)
    d["id"] = f"PC201-F{n:03d}"
    d["fixture_id"] = d["id"]
    d["category"] = category
    d["title"] = title
    d.update(data)
    return d


FIXTURES: List[Dict[str, Any]] = [
    # --- DailyWorkflowInput fixtures (F001-F010) ---
    _f(1, "daily_workflow_input", "Default DailyWorkflowInput",
       capital_twd=300000.0, market_regime="BULL", candidates=[], risk_budget_remaining_pct=100.0),
    _f(2, "daily_workflow_input", "DailyWorkflowInput with 3 candidates",
       capital_twd=300000.0, market_regime="BULL", candidates=["2330", "2454", "2317"], risk_budget_remaining_pct=80.0),
    _f(3, "daily_workflow_input", "DailyWorkflowInput bear regime",
       capital_twd=300000.0, market_regime="BEAR", candidates=["2330"], risk_budget_remaining_pct=50.0),
    _f(4, "daily_workflow_input", "DailyWorkflowInput risk budget critical",
       capital_twd=300000.0, market_regime="BULL", candidates=["2330"], risk_budget_remaining_pct=5.0),
    _f(5, "daily_workflow_input", "DailyWorkflowInput no candidates",
       capital_twd=300000.0, market_regime="BULL", candidates=[], risk_budget_remaining_pct=100.0),
    _f(6, "daily_workflow_input", "DailyWorkflowInput with theme",
       capital_twd=300000.0, market_regime="BULL", candidates=["2330"], theme="AI", risk_budget_remaining_pct=70.0),
    _f(7, "daily_workflow_input", "DailyWorkflowInput schema_version=201",
       schema_version="201", capital_twd=300000.0),
    _f(8, "daily_workflow_input", "DailyWorkflowInput paper_only=True",
       paper_only=True, no_real_orders=True, capital_twd=300000.0),
    _f(9, "daily_workflow_input", "DailyWorkflowInput with run_date",
       capital_twd=300000.0, market_regime="BULL", run_date="2026-07-20"),
    _f(10, "daily_workflow_input", "DailyWorkflowInput human_review_required=True",
       capital_twd=300000.0, human_review_required=True),

    # --- CandidateRankEntry fixtures (F011-F020) ---
    _f(11, "candidate_rank", "Rank 1 candidate with high score",
       symbol="2330", name="台積電", rank=1, total_score=90.0, abc_type="A_PULLBACK_10MA", final_action="PAPER_BUY_PLAN"),
    _f(12, "candidate_rank", "Rank 2 candidate with medium score",
       symbol="2454", name="聯發科", rank=2, total_score=72.0, abc_type="B_BREAKOUT_BASE", final_action="PAPER_BUY_PLAN"),
    _f(13, "candidate_rank", "Rank 3 candidate with low score",
       symbol="2317", name="鴻海", rank=3, total_score=55.0, abc_type="NO_ENTRY", final_action="NO_ENTRY"),
    _f(14, "candidate_rank", "Candidate with NO_ENTRY action",
       symbol="2308", name="台達電", rank=4, total_score=40.0, abc_type="NO_ENTRY", final_action="NO_ENTRY"),
    _f(15, "candidate_rank", "Candidate with WAIT action",
       symbol="2412", name="中華電", rank=5, total_score=60.0, abc_type="NO_ENTRY", final_action="WAIT"),
    _f(16, "candidate_rank", "Candidate with WATCH action",
       symbol="2882", name="國泰金", rank=6, total_score=65.0, abc_type="NO_ENTRY", final_action="WATCH"),
    _f(17, "candidate_rank", "Candidate with PAPER_ADD_PLAN",
       symbol="2303", name="聯電", rank=1, total_score=85.0, abc_type="A_PULLBACK_10MA", final_action="PAPER_ADD_PLAN", has_position=True),
    _f(18, "candidate_rank", "Candidate entry_allowed=True",
       symbol="2330", rank=1, total_score=90.0, final_action="PAPER_BUY_PLAN", entry_allowed=True),
    _f(19, "candidate_rank", "Candidate entry_allowed=False",
       symbol="2317", rank=3, total_score=40.0, final_action="NO_ENTRY", entry_allowed=False, block_reason="trend_broken"),
    _f(20, "candidate_rank", "CandidateRankEntry schema_version=201",
       schema_version="201", symbol="2330", rank=1, final_action="PAPER_BUY_PLAN"),

    # --- NoEntryReasonDetail fixtures (F021-F033) ---
    _f(21, "no_entry_reason", "trend_broken detail",
       reason_code="trend_broken", severity="HIGH", is_valid_reason=True),
    _f(22, "no_entry_reason", "below_20ma detail",
       reason_code="below_20ma", severity="MEDIUM", is_valid_reason=True),
    _f(23, "no_entry_reason", "below_60ma detail",
       reason_code="below_60ma", severity="HIGH", is_valid_reason=True),
    _f(24, "no_entry_reason", "volume_overheated detail",
       reason_code="volume_overheated", severity="MEDIUM", is_valid_reason=True),
    _f(25, "no_entry_reason", "volume_dry_up_failed detail",
       reason_code="volume_dry_up_failed", severity="MEDIUM", is_valid_reason=True),
    _f(26, "no_entry_reason", "institutional_selling detail",
       reason_code="institutional_selling", severity="HIGH", is_valid_reason=True),
    _f(27, "no_entry_reason", "margin_overheated detail",
       reason_code="margin_overheated", severity="HIGH", is_valid_reason=True),
    _f(28, "no_entry_reason", "market_risk_high detail",
       reason_code="market_risk_high", severity="HIGH", is_valid_reason=True),
    _f(29, "no_entry_reason", "risk_budget_exceeded detail",
       reason_code="risk_budget_exceeded", severity="HIGH", is_valid_reason=True),
    _f(30, "no_entry_reason", "position_size_too_large detail",
       reason_code="position_size_too_large", severity="MEDIUM", is_valid_reason=True),
    _f(31, "no_entry_reason", "stop_loss_too_wide detail",
       reason_code="stop_loss_too_wide", severity="MEDIUM", is_valid_reason=True),
    _f(32, "no_entry_reason", "missing_required_signal detail",
       reason_code="missing_required_signal", severity="HIGH", is_valid_reason=True),
    _f(33, "no_entry_reason", "human_review_required detail",
       reason_code="human_review_required", severity="INFO", recommendation="PAPER_REQUIRE_HUMAN_REVIEW", is_valid_reason=True),

    # --- EnhancedDecisionTicket fixtures (F034-F045) ---
    _f(34, "enhanced_ticket", "Full ticket all 21 fields",
       symbol="2330", name="台積電", setup_type="A_PULLBACK_10MA",
       theme_score=85.0, fundamental_score=90.0, technical_score=88.0,
       volume_score=80.0, chip_score=82.0, margin_score=78.0,
       entry_price_plan=920.0, add_price_plan=950.0, reduce_price_plan=1100.0, exit_price_plan=1242.0,
       stop_loss_price=874.0, invalid_conditions=[], risk_amount=4500.0,
       max_position_size=45000.0, position_size_reason="risk/stop", no_entry_reasons=[],
       final_action="PAPER_BUY_PLAN"),
    _f(35, "enhanced_ticket", "Ticket with NO_ENTRY action",
       symbol="2317", name="鴻海", setup_type="NO_ENTRY",
       no_entry_reasons=["trend_broken"], invalid_conditions=["trend_broken"],
       final_action="NO_ENTRY"),
    _f(36, "enhanced_ticket", "Ticket schema_version=201",
       schema_version="201", symbol="2330", final_action="PAPER_BUY_PLAN"),
    _f(37, "enhanced_ticket", "Ticket paper_only=True",
       paper_only=True, no_real_orders=True, symbol="2330"),
    _f(38, "enhanced_ticket", "Ticket ticket_triggers_broker=False",
       ticket_triggers_broker=False, symbol="2330"),
    _f(39, "enhanced_ticket", "Ticket ticket_executes_order=False",
       ticket_executes_order=False, symbol="2330"),
    _f(40, "enhanced_ticket", "Ticket human_review_required=True",
       human_review_required=True, symbol="2330"),
    _f(41, "enhanced_ticket", "Ticket total_score = mean of 6 sub-scores",
       theme_score=80.0, fundamental_score=80.0, technical_score=80.0,
       volume_score=80.0, chip_score=80.0, margin_score=80.0, expected_total=80.0),
    _f(42, "enhanced_ticket", "Ticket with multiple no_entry_reasons",
       symbol="2317", no_entry_reasons=["trend_broken", "below_20ma"], final_action="NO_ENTRY"),
    _f(43, "enhanced_ticket", "Ticket PAPER_ADD_PLAN for existing position",
       symbol="2330", final_action="PAPER_ADD_PLAN", has_position=True),
    _f(44, "enhanced_ticket", "Ticket PAPER_REDUCE_PLAN",
       symbol="2330", final_action="PAPER_REDUCE_PLAN", position_profit_pct=0.30),
    _f(45, "enhanced_ticket", "Ticket PAPER_EXIT_PLAN",
       symbol="2330", final_action="PAPER_EXIT_PLAN", position_profit_pct=-0.10),

    # --- RiskBudgetStatus fixtures (F046-F052) ---
    _f(46, "risk_budget_status", "NORMAL status 100% remaining",
       portfolio_risk_pct=0.0, risk_budget_remaining_pct=100.0, expected_status="NORMAL"),
    _f(47, "risk_budget_status", "CAUTION status 35% remaining",
       portfolio_risk_pct=30.0, risk_budget_remaining_pct=35.0, expected_status="CAUTION"),
    _f(48, "risk_budget_status", "WARNING status 15% remaining",
       portfolio_risk_pct=50.0, risk_budget_remaining_pct=15.0, expected_status="WARNING"),
    _f(49, "risk_budget_status", "CRITICAL status 5% remaining",
       portfolio_risk_pct=70.0, risk_budget_remaining_pct=5.0, expected_status="CRITICAL"),
    _f(50, "risk_budget_status", "risk_budget_ok=True when >= 10%",
       risk_budget_remaining_pct=10.0, expected_ok=True),
    _f(51, "risk_budget_status", "risk_budget_ok=False when < 10%",
       risk_budget_remaining_pct=9.0, expected_ok=False),
    _f(52, "risk_budget_status", "risk_budget_used_pct = 100 - remaining",
       risk_budget_remaining_pct=70.0, expected_used_pct=30.0),

    # --- CLIDisplayRow fixtures (F053-F058) ---
    _f(53, "cli_display_row", "Row for PAPER_BUY_PLAN candidate",
       symbol="2330", setup_type="A_PULLBACK_10MA", suggested_paper_action="PAPER_BUY_PLAN", entry_allowed=True),
    _f(54, "cli_display_row", "Row for NO_ENTRY candidate",
       symbol="2317", setup_type="NO_ENTRY", suggested_paper_action="NO_ENTRY", entry_allowed=False, blocked_reason="trend_broken"),
    _f(55, "cli_display_row", "Row human_review_flag=True",
       symbol="2330", human_review_flag=True),
    _f(56, "cli_display_row", "Row paper_only=True",
       symbol="2330", paper_only=True),
    _f(57, "cli_display_row", "Row for WATCH action",
       symbol="2330", suggested_paper_action="WATCH", entry_allowed=False),
    _f(58, "cli_display_row", "Row for WAIT action",
       symbol="2412", suggested_paper_action="WAIT", entry_allowed=False),

    # --- CLIDisplayOutput fixtures (F059-F064) ---
    _f(59, "cli_display_output", "Full CLI display output structure",
       total_candidates=3, paper_buy_plan_count=1, no_entry_count=2),
    _f(60, "cli_display_output", "Action counts sum to total",
       total_candidates=5, watch_count=1, wait_count=1, paper_buy_plan_count=1, no_entry_count=2),
    _f(61, "cli_display_output", "CLIDisplayOutput paper_only=True",
       paper_only=True, no_real_orders=True),
    _f(62, "cli_display_output", "CLIDisplayOutput human_review_required=True",
       human_review_required=True),
    _f(63, "cli_display_output", "CLIDisplayOutput schema_version=201",
       schema_version="201"),
    _f(64, "cli_display_output", "Empty display output with no candidates",
       total_candidates=0, top_candidates=[]),

    # --- DailyWorkflowCandidateResult fixtures (F065-F070) ---
    _f(65, "candidate_result", "Candidate result PAPER_BUY_PLAN",
       symbol="2330", abc_type="A_PULLBACK_10MA", final_action="PAPER_BUY_PLAN", risk_overlay_status="CLEAR"),
    _f(66, "candidate_result", "Candidate result NO_ENTRY blocked",
       symbol="2317", abc_type="NO_ENTRY", final_action="NO_ENTRY", risk_overlay_status="BLOCKED"),
    _f(67, "candidate_result", "Candidate result human_review_requirement=True",
       symbol="2330", human_review_requirement=True),
    _f(68, "candidate_result", "Candidate result with watchlist_summary",
       symbol="2330", watchlist_summary="2330 watchlist rank #1, regime=BULL"),
    _f(69, "candidate_result", "Candidate result with position_sizing_suggestion",
       symbol="2330", position_sizing_suggestion="Max 45,000 TWD (8.0% stop)", final_action="PAPER_BUY_PLAN"),
    _f(70, "candidate_result", "Candidate result schema_version=201",
       schema_version="201", symbol="2330"),

    # --- DailyWorkflowResult fixtures (F071-F075) ---
    _f(71, "workflow_result", "Full workflow result structure",
       version="2.0.1", market_regime="BULL", all_passed=True),
    _f(72, "workflow_result", "Workflow result paper_only=True",
       paper_only=True, no_real_orders=True, no_broker=True),
    _f(73, "workflow_result", "Workflow result cockpit_executes_order=False",
       cockpit_executes_order=False),
    _f(74, "workflow_result", "Workflow result human_review_required=True",
       human_review_required=True),
    _f(75, "workflow_result", "Workflow result schema_version=201",
       schema_version="201"),

    # --- Safety Fixtures (F076-F078) ---
    _f(76, "safety", "NO_REAL_ORDERS module constant",
       constant="NO_REAL_ORDERS", expected_value=True),
    _f(77, "safety", "BROKER_EXECUTION_ENABLED module constant",
       constant="BROKER_EXECUTION_ENABLED", expected_value=False),
    _f(78, "safety", "PRODUCTION_TRADING_BLOCKED module constant",
       constant="PRODUCTION_TRADING_BLOCKED", expected_value=True),

    # --- V201 Health/Release fixtures (F079-F080) ---
    _f(79, "health", "V201HealthSummary structure",
       version="2.0.1", no_entry_reasons_count=13, daily_final_actions_count=7, enhanced_ticket_fields_count=22),
    _f(80, "release", "V201ReleaseSummary structure",
       version="2.0.1", release_name="Paper Cockpit Usability & Daily Workflow Hardening",
       models_count=12, cli_count=10, gui_tabs_count=3, scenarios_count=80, fixtures_count=80),
]

assert len(FIXTURES) == 80, f"Expected 80 fixtures, got {len(FIXTURES)}"
assert all(f["schema_version"] == "201" for f in FIXTURES), "All fixtures must have schema_version=201"
assert all(f["paper_only"] is True for f in FIXTURES), "All fixtures must have paper_only=True"
assert all("fixture_id" in f for f in FIXTURES), "All fixtures must have fixture_id"
assert len({f["id"] for f in FIXTURES}) == 80, "Fixture IDs must be unique"
