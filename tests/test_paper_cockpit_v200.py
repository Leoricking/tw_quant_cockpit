"""
tests/test_paper_cockpit_v200.py
v2.0.0 Paper Cockpit Unified Entry & Strategy Decision Console — Main Tests
[!] Paper Only. Research Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS, MIN_NEW_TESTS,
    SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS, HARD_BLOCK_CONDITIONS,
    NO_ENTRY_CONDITIONS, ABC_DECISION_TYPES, CLI_COMMANDS, GUI_TABS, COVERED_VERSIONS,
    _ALL_MODEL_NAMES,
    PaperCockpitInput, PaperCockpitResult, PaperCockpitWatchlist, PaperCockpitCandidate,
    PaperCockpitSignalScore, PaperCockpitThemeScore, PaperCockpitFundamentalScore,
    PaperCockpitTechnicalScore, PaperCockpitInstitutionalScore, PaperCockpitMarginScore,
    PaperCockpitEntryCheck, PaperCockpitABCDecision, PaperCockpitPortfolioRiskCheck,
    PaperCockpitPositionSizingCheck, PaperCockpitNoEntryCondition, PaperCockpitDecisionTicket,
    PaperCockpitHumanReviewRequest, PaperCockpitDashboard, PaperCockpitReport,
    PaperCockpitAuditTrail, PaperCockpitValidationResult, PaperCockpitHealthSummary,
    PaperCockpitReleaseSummary,
    score_watchlist, score_candidate, classify_abc, check_portfolio_risk,
    check_position_sizing, evaluate_no_entry, generate_decision_ticket,
    generate_human_review_request, build_dashboard, build_report, build_audit_trail,
    validate_cockpit, run_cockpit, get_cockpit_summary, get_version_info, verify_version,
)


# ---------------------------------------------------------------------------
# Version and constants
# ---------------------------------------------------------------------------

def test_version_is_200():
    assert VERSION == "2.0.0"

def test_schema_version_is_200():
    assert SCHEMA_VERSION == "200"

def test_release_name_correct():
    assert "Cockpit" in RELEASE_NAME or "Console" in RELEASE_NAME

def test_baseline_tests_31925():
    assert BASELINE_TESTS == 31925

def test_min_new_tests_500():
    assert MIN_NEW_TESTS == 500

# ---------------------------------------------------------------------------
# SAFETY_FLAGS
# ---------------------------------------------------------------------------

def test_safety_flags_count_30():
    assert len(SAFETY_FLAGS) == 30

def test_safety_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_research_only():
    assert SAFETY_FLAGS["research_only"] is True

def test_safety_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True

def test_safety_validation_only():
    assert SAFETY_FLAGS["validation_only"] is True

def test_safety_unified_paper_cockpit_only():
    assert SAFETY_FLAGS["unified_paper_cockpit_only"] is True

def test_safety_decision_console_only():
    assert SAFETY_FLAGS["decision_console_only"] is True

def test_safety_dashboard_only():
    assert SAFETY_FLAGS["dashboard_only"] is True

def test_safety_report_only():
    assert SAFETY_FLAGS["report_only"] is True

def test_safety_audit_only():
    assert SAFETY_FLAGS["audit_only"] is True

def test_safety_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True

def test_safety_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_safety_no_production_db_write():
    assert SAFETY_FLAGS["no_production_db_write"] is True

def test_safety_no_production_strategy_mutation():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True

def test_safety_no_automatic_rollback():
    assert SAFETY_FLAGS["no_automatic_rollback"] is True

def test_safety_no_live_strategy_activation():
    assert SAFETY_FLAGS["no_live_strategy_activation"] is True

def test_safety_no_real_portfolio_rebalancing():
    assert SAFETY_FLAGS["no_real_portfolio_rebalancing"] is True

def test_safety_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_human_review_required():
    assert SAFETY_FLAGS["human_review_required"] is True

def test_safety_cockpit_executes_order_false():
    assert SAFETY_FLAGS["cockpit_executes_order"] is False

def test_safety_cockpit_mutates_strategy_false():
    assert SAFETY_FLAGS["cockpit_mutates_strategy"] is False

def test_safety_cockpit_rebalances_real_portfolio_false():
    assert SAFETY_FLAGS["cockpit_rebalances_real_portfolio"] is False

def test_safety_export_triggers_real_order_false():
    assert SAFETY_FLAGS["export_triggers_real_order"] is False

def test_safety_ticket_triggers_broker_false():
    assert SAFETY_FLAGS["ticket_triggers_broker"] is False

def test_safety_dashboard_writes_production_db_false():
    assert SAFETY_FLAGS["dashboard_writes_production_db"] is False

def test_safety_report_activates_live_strategy_false():
    assert SAFETY_FLAGS["report_activates_live_strategy"] is False

def test_safety_audit_activates_live_strategy_false():
    assert SAFETY_FLAGS["audit_activates_live_strategy"] is False

# ---------------------------------------------------------------------------
# FORBIDDEN_ACTIONS
# ---------------------------------------------------------------------------

def test_forbidden_actions_count_10():
    assert len(FORBIDDEN_ACTIONS) == 10

def test_forbidden_buy():
    assert "BUY" in FORBIDDEN_ACTIONS

def test_forbidden_sell():
    assert "SELL" in FORBIDDEN_ACTIONS

def test_forbidden_order():
    assert "ORDER" in FORBIDDEN_ACTIONS

def test_forbidden_execute():
    assert "EXECUTE" in FORBIDDEN_ACTIONS

def test_forbidden_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_ACTIONS

def test_forbidden_auto_trade():
    assert "AUTO_TRADE" in FORBIDDEN_ACTIONS

def test_forbidden_real_trade():
    assert "REAL_TRADE" in FORBIDDEN_ACTIONS

def test_forbidden_live_trade():
    assert "LIVE_TRADE" in FORBIDDEN_ACTIONS

def test_forbidden_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_ACTIONS

def test_forbidden_rebalance_real_portfolio():
    assert "REBALANCE_REAL_PORTFOLIO" in FORBIDDEN_ACTIONS

# ---------------------------------------------------------------------------
# ALLOWED_ACTIONS
# ---------------------------------------------------------------------------

def test_allowed_actions_count_9():
    assert len(ALLOWED_ACTIONS) == 9

def test_allowed_paper_watch_only():
    assert "PAPER_WATCH_ONLY" in ALLOWED_ACTIONS

def test_allowed_paper_allow_normal_size():
    assert "PAPER_ALLOW_NORMAL_SIZE" in ALLOWED_ACTIONS

def test_allowed_paper_allow_reduced_size():
    assert "PAPER_ALLOW_REDUCED_SIZE" in ALLOWED_ACTIONS

def test_allowed_paper_test_position_only():
    assert "PAPER_TEST_POSITION_ONLY" in ALLOWED_ACTIONS

def test_allowed_paper_block_new_entry():
    assert "PAPER_BLOCK_NEW_ENTRY" in ALLOWED_ACTIONS

def test_allowed_paper_keep_cash():
    assert "PAPER_KEEP_CASH" in ALLOWED_ACTIONS

def test_allowed_paper_require_human_review():
    assert "PAPER_REQUIRE_HUMAN_REVIEW" in ALLOWED_ACTIONS

def test_allowed_paper_risk_off_mode():
    assert "PAPER_RISK_OFF_MODE" in ALLOWED_ACTIONS

def test_allowed_paper_no_change():
    assert "PAPER_NO_CHANGE" in ALLOWED_ACTIONS

# ---------------------------------------------------------------------------
# HARD_BLOCK_CONDITIONS
# ---------------------------------------------------------------------------

def test_hard_block_conditions_count_22():
    assert len(HARD_BLOCK_CONDITIONS) == 22

def test_hard_block_real_order_requested():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_broker_requested():
    assert "broker_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_margin_or_leverage():
    assert "margin_or_leverage_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_missing_watchlist():
    assert "missing_watchlist" in HARD_BLOCK_CONDITIONS

def test_hard_block_malformed_cockpit_input():
    assert "malformed_cockpit_input" in HARD_BLOCK_CONDITIONS

# ---------------------------------------------------------------------------
# NO_ENTRY_CONDITIONS
# ---------------------------------------------------------------------------

def test_no_entry_conditions_count_8():
    assert len(NO_ENTRY_CONDITIONS) == 8

def test_no_entry_portfolio_risk_exceeded():
    assert "portfolio_risk_exceeded" in NO_ENTRY_CONDITIONS

def test_no_entry_theme_exposure_exceeded():
    assert "theme_exposure_exceeded" in NO_ENTRY_CONDITIONS

def test_no_entry_cash_buffer_too_low():
    assert "cash_buffer_too_low" in NO_ENTRY_CONDITIONS

def test_no_entry_stop_distance_too_wide():
    assert "stop_distance_too_wide" in NO_ENTRY_CONDITIONS

# ---------------------------------------------------------------------------
# ABC_DECISION_TYPES
# ---------------------------------------------------------------------------

def test_abc_types_count_4():
    assert len(ABC_DECISION_TYPES) == 4

def test_abc_a_pullback():
    assert "A_PULLBACK_10MA" in ABC_DECISION_TYPES

def test_abc_b_breakout():
    assert "B_BREAKOUT_BASE" in ABC_DECISION_TYPES

def test_abc_c_reclaim():
    assert "C_RECLAIM_20MA" in ABC_DECISION_TYPES

def test_abc_no_entry():
    assert "NO_ENTRY" in ABC_DECISION_TYPES

# ---------------------------------------------------------------------------
# CLI_COMMANDS / GUI_TABS
# ---------------------------------------------------------------------------

def test_cli_commands_count_17():
    assert len(CLI_COMMANDS) == 17

def test_cli_paper_cockpit_version():
    assert "paper-cockpit-version" in CLI_COMMANDS

def test_cli_paper_cockpit_run():
    assert "paper-cockpit-run" in CLI_COMMANDS

def test_cli_paper_cockpit_health():
    assert "paper-cockpit-health" in CLI_COMMANDS

def test_cli_paper_cockpit_gate():
    assert "paper-cockpit-gate" in CLI_COMMANDS

def test_cli_paper_cockpit_safety_audit():
    assert "paper-cockpit-safety-audit" in CLI_COMMANDS

def test_gui_tabs_count_3():
    assert len(GUI_TABS) == 3

def test_gui_tab_paper_cockpit():
    assert "paper_cockpit" in GUI_TABS

def test_gui_tab_strategy_decision_console():
    assert "strategy_decision_console" in GUI_TABS

def test_gui_tab_decision_ticket():
    assert "decision_ticket" in GUI_TABS

# ---------------------------------------------------------------------------
# COVERED_VERSIONS
# ---------------------------------------------------------------------------

def test_covered_versions_count_29():
    assert len(COVERED_VERSIONS) == 29

def test_covered_versions_includes_v170():
    assert "1.7.0" in COVERED_VERSIONS

def test_covered_versions_includes_v1910():
    assert "1.9.10" in COVERED_VERSIONS

def test_covered_versions_includes_v180():
    assert "1.8.0" in COVERED_VERSIONS

def test_covered_versions_includes_v190():
    assert "1.9.0" in COVERED_VERSIONS

# ---------------------------------------------------------------------------
# Models: all 23
# ---------------------------------------------------------------------------

def test_model_count_23():
    assert len(_ALL_MODEL_NAMES) == 23

def test_model_PaperCockpitInput_instantiates():
    m = PaperCockpitInput()
    assert m.schema_version == "200"
    assert m.paper_only is True
    assert m.no_real_orders is True

def test_model_PaperCockpitResult_instantiates():
    m = PaperCockpitResult()
    assert m.schema_version == "200"
    assert m.paper_only is True
    assert m.cockpit_executes_order is False

def test_model_PaperCockpitWatchlist_instantiates():
    m = PaperCockpitWatchlist()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitCandidate_instantiates():
    m = PaperCockpitCandidate()
    assert m.schema_version == "200"
    assert m.requires_human_review is True

def test_model_PaperCockpitSignalScore_instantiates():
    m = PaperCockpitSignalScore()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitThemeScore_instantiates():
    m = PaperCockpitThemeScore()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitFundamentalScore_instantiates():
    m = PaperCockpitFundamentalScore()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitTechnicalScore_instantiates():
    m = PaperCockpitTechnicalScore()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitInstitutionalScore_instantiates():
    m = PaperCockpitInstitutionalScore()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitMarginScore_instantiates():
    m = PaperCockpitMarginScore()
    assert m.schema_version == "200"
    assert m.no_margin is True

def test_model_PaperCockpitEntryCheck_instantiates():
    m = PaperCockpitEntryCheck()
    assert m.schema_version == "200"
    assert m.no_real_orders is True

def test_model_PaperCockpitABCDecision_instantiates():
    m = PaperCockpitABCDecision()
    assert m.schema_version == "200"
    assert m.cockpit_executes_order is False
    assert m.cockpit_mutates_strategy is False

def test_model_PaperCockpitPortfolioRiskCheck_instantiates():
    m = PaperCockpitPortfolioRiskCheck()
    assert m.schema_version == "200"
    assert m.no_real_portfolio_rebalancing is True

def test_model_PaperCockpitPositionSizingCheck_instantiates():
    m = PaperCockpitPositionSizingCheck()
    assert m.schema_version == "200"
    assert m.sizing_executes_order is False

def test_model_PaperCockpitNoEntryCondition_instantiates():
    m = PaperCockpitNoEntryCondition()
    assert m.schema_version == "200"
    assert m.cockpit_executes_order is False

def test_model_PaperCockpitDecisionTicket_instantiates():
    m = PaperCockpitDecisionTicket()
    assert m.schema_version == "200"
    assert m.ticket_triggers_broker is False
    assert m.ticket_executes_order is False

def test_model_PaperCockpitHumanReviewRequest_instantiates():
    m = PaperCockpitHumanReviewRequest()
    assert m.schema_version == "200"
    assert m.auto_approval_blocked is True
    assert m.cockpit_auto_approves is False

def test_model_PaperCockpitDashboard_instantiates():
    m = PaperCockpitDashboard()
    assert m.schema_version == "200"
    assert m.dashboard_writes_production_db is False
    assert m.dashboard_places_real_order is False

def test_model_PaperCockpitReport_instantiates():
    m = PaperCockpitReport()
    assert m.schema_version == "200"
    assert m.report_triggers_real_order is False
    assert m.report_activates_live_strategy is False

def test_model_PaperCockpitAuditTrail_instantiates():
    m = PaperCockpitAuditTrail()
    assert m.schema_version == "200"
    assert m.audit_triggers_order is False
    assert m.audit_activates_live_strategy is False

def test_model_PaperCockpitValidationResult_instantiates():
    m = PaperCockpitValidationResult()
    assert m.schema_version == "200"
    assert m.paper_only is True

def test_model_PaperCockpitHealthSummary_instantiates():
    m = PaperCockpitHealthSummary()
    assert m.schema_version == "200"
    assert m.version == "2.0.0"

def test_model_PaperCockpitReleaseSummary_instantiates():
    m = PaperCockpitReleaseSummary()
    assert m.schema_version == "200"
    assert m.version == "2.0.0"
    assert m.models_count == 23
    assert m.cli_count == 17
    assert m.gui_tabs_count == 3
    assert m.scenarios_count == 80
    assert m.fixtures_count == 80

# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------

def test_score_watchlist_valid():
    result = score_watchlist(["2330", "2454"])
    assert result.is_valid is True
    assert result.count == 2
    assert result.paper_only is True

def test_score_watchlist_empty_invalid():
    result = score_watchlist([])
    assert result.is_valid is False

def test_score_watchlist_30_valid():
    symbols = [f"{2300 + i}" for i in range(30)]
    result = score_watchlist(symbols)
    assert result.is_valid is True
    assert result.count == 30

def test_score_watchlist_31_invalid():
    symbols = [f"{2300 + i}" for i in range(31)]
    result = score_watchlist(symbols)
    assert result.is_valid is False

def test_score_candidate_default():
    result = score_candidate("2330")
    assert result.symbol == "2330"
    assert result.paper_only is True
    assert result.schema_version == "200"
    assert isinstance(result.total_score, float)

def test_score_candidate_grade_a():
    result = score_candidate("2330",
        theme_score=90.0, fundamental_score=90.0, technical_score=90.0,
        institutional_score=90.0, margin_score=90.0)
    assert result.grade == "A"
    assert result.is_tradable is True

def test_score_candidate_grade_f():
    result = score_candidate("2330",
        theme_score=10.0, fundamental_score=10.0, technical_score=10.0,
        institutional_score=10.0, margin_score=10.0)
    assert result.grade == "F"
    assert result.is_tradable is False

def test_score_candidate_grade_b():
    result = score_candidate("2330",
        theme_score=75.0, fundamental_score=72.0, technical_score=70.0,
        institutional_score=71.0, margin_score=73.0)
    assert result.grade == "B"

def test_score_candidate_total_is_avg():
    result = score_candidate("2330",
        theme_score=100.0, fundamental_score=0.0, technical_score=0.0,
        institutional_score=0.0, margin_score=0.0)
    assert abs(result.total_score - 20.0) < 0.01

def test_classify_abc_a_pullback():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, ma10_support=True, volume_contraction=True,
                           continuous_institutional_selling=False)
    assert result.abc_type == "A_PULLBACK_10MA"
    assert result.paper_only is True
    assert result.cockpit_executes_order is False

def test_classify_abc_b_breakout():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, base_breakout=True, volume_expansion_ratio=2.0,
                           margin_financing_exploding=False)
    assert result.abc_type == "B_BREAKOUT_BASE"

def test_classify_abc_c_reclaim():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, ma20_reclaim=True, momentum_repair=True,
                           ma20_failed_again=False)
    assert result.abc_type == "C_RECLAIM_20MA"

def test_classify_abc_no_entry_default():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig)
    assert result.abc_type == "NO_ENTRY"
    assert result.paper_size_pct == 0.0

def test_classify_abc_a_blocked_by_institutional_selling():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, ma10_support=True, volume_contraction=True,
                           continuous_institutional_selling=True)
    assert result.abc_type == "NO_ENTRY"

def test_classify_abc_b_blocked_by_margin_explosion():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, base_breakout=True, volume_expansion_ratio=2.0,
                           margin_financing_exploding=True)
    assert result.abc_type == "NO_ENTRY"

def test_classify_abc_b_blocked_by_insufficient_volume():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, base_breakout=True, volume_expansion_ratio=1.4)
    assert result.abc_type == "NO_ENTRY"

def test_classify_abc_c_blocked_by_ma20_failed():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, ma20_reclaim=True, momentum_repair=True,
                           ma20_failed_again=True)
    assert result.abc_type == "NO_ENTRY"

def test_classify_abc_b_extended_reduced_size():
    sig = score_candidate("2330")
    result = classify_abc("2330", sig, base_breakout=True, volume_expansion_ratio=3.5,
                           margin_financing_exploding=False)
    assert result.abc_type == "B_BREAKOUT_BASE"
    assert result.paper_size_pct == 0.6

def test_check_portfolio_risk_default_ok():
    result = check_portfolio_risk()
    assert result.overall_ok is True
    assert result.paper_only is True
    assert result.no_real_portfolio_rebalancing is True

def test_check_portfolio_risk_exceeded():
    result = check_portfolio_risk(portfolio_risk_pct=70.0)
    assert result.overall_ok is False
    assert result.portfolio_risk_ok is False
    assert result.recommendation == "PAPER_BLOCK_NEW_ENTRY"

def test_check_portfolio_risk_theme_exceeded():
    result = check_portfolio_risk(theme_exposure_pct=40.0)
    assert result.theme_exposure_ok is False
    assert result.overall_ok is False

def test_check_portfolio_risk_cash_buffer_low():
    result = check_portfolio_risk(cash_buffer_pct=10.0)
    assert result.cash_buffer_ok is False
    assert result.recommendation == "PAPER_KEEP_CASH"

def test_check_portfolio_risk_block_reason_set():
    result = check_portfolio_risk(portfolio_risk_pct=70.0)
    assert len(result.block_reason) > 0

def test_check_position_sizing_default_ok():
    result = check_position_sizing()
    assert result.sizing_ok is True
    assert result.sizing_executes_order is False
    assert result.sizing_mutates_strategy is False

def test_check_position_sizing_zero_stop_blocked():
    result = check_position_sizing(stop_distance_pct=0.0)
    assert result.sizing_ok is False
    assert "zero" in result.block_reason

def test_check_position_sizing_wide_stop_blocked():
    result = check_position_sizing(stop_distance_pct=0.20)
    assert result.sizing_ok is False
    assert "wide" in result.block_reason

def test_check_position_sizing_max_loss_4500():
    result = check_position_sizing(stop_distance_pct=0.08)
    assert result.max_loss_per_trade_twd == 4500.0

def test_check_position_sizing_min_loss_2400():
    result = check_position_sizing(stop_distance_pct=0.08)
    assert result.min_loss_per_trade_twd == 2400.0

def test_evaluate_no_entry_from_abc_no_entry():
    abc = PaperCockpitABCDecision(abc_type="NO_ENTRY", block_reason="no_abc_condition_met")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    result = evaluate_no_entry(abc, risk, sizing)
    assert result.condition_triggered is True
    assert result.cockpit_executes_order is False

def test_evaluate_no_entry_from_portfolio_risk():
    abc = PaperCockpitABCDecision(abc_type="A_PULLBACK_10MA")
    risk = check_portfolio_risk(portfolio_risk_pct=70.0)
    sizing = check_position_sizing()
    result = evaluate_no_entry(abc, risk, sizing)
    assert result.condition_triggered is True

def test_evaluate_no_entry_not_triggered_all_pass():
    abc = PaperCockpitABCDecision(abc_type="A_PULLBACK_10MA")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    result = evaluate_no_entry(abc, risk, sizing)
    assert result.condition_triggered is False
    assert result.recommendation == "PAPER_ALLOW_NORMAL_SIZE"

def test_generate_decision_ticket_paper_only():
    abc = PaperCockpitABCDecision(abc_type="A_PULLBACK_10MA")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    no_entry = evaluate_no_entry(abc, risk, sizing)
    ticket = generate_decision_ticket("2330", abc, risk, sizing, no_entry)
    assert ticket.paper_only is True
    assert ticket.no_broker is True
    assert ticket.ticket_triggers_broker is False
    assert ticket.ticket_executes_order is False
    assert ticket.ticket_mutates_strategy is False
    assert ticket.requires_human_review is True

def test_generate_decision_ticket_blocked_when_no_entry():
    abc = PaperCockpitABCDecision(abc_type="NO_ENTRY", block_reason="no_abc")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    no_entry = evaluate_no_entry(abc, risk, sizing)
    ticket = generate_decision_ticket("2330", abc, risk, sizing, no_entry)
    assert ticket.is_blocked is True

def test_generate_decision_ticket_not_blocked_when_all_pass():
    abc = PaperCockpitABCDecision(abc_type="A_PULLBACK_10MA")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    no_entry = evaluate_no_entry(abc, risk, sizing)
    ticket = generate_decision_ticket("2330", abc, risk, sizing, no_entry)
    assert ticket.is_blocked is False

def test_generate_human_review_request_always_blocks_auto():
    abc = PaperCockpitABCDecision(abc_type="A_PULLBACK_10MA")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    no_entry = evaluate_no_entry(abc, risk, sizing)
    ticket = generate_decision_ticket("2330", abc, risk, sizing, no_entry)
    review = generate_human_review_request(ticket)
    assert review.auto_approval_blocked is True
    assert review.cockpit_auto_approves is False
    assert review.human_review_required is True

def test_generate_human_review_high_urgency_for_a_type():
    abc = PaperCockpitABCDecision(abc_type="A_PULLBACK_10MA")
    risk = check_portfolio_risk()
    sizing = check_position_sizing()
    no_entry = evaluate_no_entry(abc, risk, sizing)
    ticket = generate_decision_ticket("2330", abc, risk, sizing, no_entry)
    review = generate_human_review_request(ticket)
    assert review.urgency == "HIGH"

def test_build_dashboard_paper_only():
    inp = PaperCockpitInput(market_regime="BULL", watchlist=["2330"])
    risk = check_portfolio_risk()
    dashboard = build_dashboard(inp, [], risk)
    assert dashboard.paper_only is True
    assert dashboard.dashboard_only is True
    assert dashboard.dashboard_writes_production_db is False
    assert dashboard.dashboard_places_real_order is False

def test_build_dashboard_regime():
    inp = PaperCockpitInput(market_regime="BEAR", watchlist=["2330"])
    risk = check_portfolio_risk()
    dashboard = build_dashboard(inp, [], risk)
    assert dashboard.regime == "BEAR"

def test_build_report_paper_only():
    inp = PaperCockpitInput(market_regime="BULL")
    report = build_report(inp, [], [])
    assert report.paper_only is True
    assert report.report_only is True
    assert report.report_triggers_real_order is False
    assert report.report_activates_live_strategy is False

def test_build_audit_trail_paper_only():
    trail = build_audit_trail("run-001", ["entry1", "entry2"])
    assert trail.paper_only is True
    assert trail.audit_only is True
    assert trail.audit_triggers_order is False
    assert trail.audit_activates_live_strategy is False
    assert len(trail.entries) == 2

def test_validate_cockpit_default_valid():
    result = validate_cockpit(PaperCockpitInput())
    assert result.is_valid is True
    assert result.safety_flags_ok is True
    assert result.errors == []

def test_validate_cockpit_fails_paper_only_false():
    inp = PaperCockpitInput(paper_only=False)
    result = validate_cockpit(inp)
    assert result.is_valid is False
    assert len(result.errors) > 0

def test_validate_cockpit_fails_wrong_schema():
    inp = PaperCockpitInput(schema_version="100")
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_run_cockpit_default():
    result = run_cockpit()
    assert result.paper_only is True
    assert result.cockpit_executes_order is False
    assert result.cockpit_mutates_strategy is False
    assert result.cockpit_rebalances_real_portfolio is False
    assert result.human_review_required is True

def test_run_cockpit_with_watchlist():
    inp = PaperCockpitInput(watchlist=["2330", "2454"])
    result = run_cockpit(inp)
    assert result.all_passed is True
    assert result.dashboard is not None
    assert result.report is not None
    assert result.audit_trail is not None

def test_run_cockpit_all_passed():
    result = run_cockpit(PaperCockpitInput(watchlist=["2330"]))
    assert result.all_passed is True

def test_run_cockpit_is_deterministic():
    inp = PaperCockpitInput(watchlist=["2330"])
    r1 = run_cockpit(inp)
    r2 = run_cockpit(inp)
    assert r1.regime == r2.regime
    assert r1.paper_only == r2.paper_only

def test_get_cockpit_summary_all_fields():
    s = get_cockpit_summary()
    assert s["version"] == "2.0.0"
    assert s["schema_version"] == "200"
    assert s["models"] == 23
    assert s["cli_commands"] == 17
    assert s["gui_tabs"] == 3
    assert s["paper_only"] is True
    assert s["no_real_orders"] is True

def test_get_version_info():
    info = get_version_info()
    assert info["version"] == "2.0.0"
    assert info["schema_version"] == "200"
    assert info["paper_only"] is True

def test_verify_version_returns_true():
    assert verify_version() is True

def test_covered_versions_no_duplicates():
    assert len(COVERED_VERSIONS) == len(set(COVERED_VERSIONS))

def test_run_cockpit_no_forbidden_action_in_summary():
    result = run_cockpit()
    summary = get_cockpit_summary()
    for forbidden in FORBIDDEN_ACTIONS:
        assert forbidden not in str(summary), f"Forbidden action '{forbidden}' found in summary"
