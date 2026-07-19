"""
tests/test_paper_cockpit_safety_v200.py
v2.0.0 Paper Cockpit — Safety Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
    SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS, HARD_BLOCK_CONDITIONS,
    NO_ENTRY_CONDITIONS, ABC_DECISION_TYPES, CLI_COMMANDS, GUI_TABS, COVERED_VERSIONS,
    _ALL_MODEL_NAMES,
    PaperCockpitInput, PaperCockpitResult, PaperCockpitABCDecision,
    PaperCockpitDecisionTicket, PaperCockpitPortfolioRiskCheck, PaperCockpitPositionSizingCheck,
    PaperCockpitDashboard, PaperCockpitReport, PaperCockpitAuditTrail,
    PaperCockpitHumanReviewRequest, PaperCockpitNoEntryCondition,
    run_cockpit, validate_cockpit, get_cockpit_summary, verify_version,
    check_portfolio_risk, check_position_sizing, evaluate_no_entry,
    generate_decision_ticket, generate_human_review_request,
)


# ---------------------------------------------------------------------------
# Safety: no forbidden action words in output
# ---------------------------------------------------------------------------

def test_forbidden_not_in_cockpit_summary():
    summary = get_cockpit_summary()
    summary_str = str(summary)
    for fa in FORBIDDEN_ACTIONS:
        assert fa not in summary_str, f"Forbidden '{fa}' found in summary"

def test_forbidden_not_in_run_cockpit_result():
    result = run_cockpit()
    result_str = str(result.regime) + str(result.version)
    for fa in ["BUY", "SELL", "ORDER", "EXECUTE"]:
        assert fa not in result_str

def test_allowed_actions_are_paper_only():
    for action in ALLOWED_ACTIONS:
        assert action.startswith("PAPER_"), f"Action '{action}' is not paper-only"

def test_forbidden_buy_not_in_allowed():
    assert "BUY" not in ALLOWED_ACTIONS

def test_forbidden_sell_not_in_allowed():
    assert "SELL" not in ALLOWED_ACTIONS

def test_forbidden_order_not_in_allowed():
    assert "ORDER" not in ALLOWED_ACTIONS

def test_forbidden_execute_not_in_allowed():
    assert "EXECUTE" not in ALLOWED_ACTIONS

def test_forbidden_auto_trade_not_in_allowed():
    assert "AUTO_TRADE" not in ALLOWED_ACTIONS

def test_forbidden_real_trade_not_in_allowed():
    assert "REAL_TRADE" not in ALLOWED_ACTIONS

def test_forbidden_live_trade_not_in_allowed():
    assert "LIVE_TRADE" not in ALLOWED_ACTIONS

def test_forbidden_broker_order_not_in_allowed():
    assert "BROKER_ORDER" not in ALLOWED_ACTIONS

# ---------------------------------------------------------------------------
# Safety: no order execution
# ---------------------------------------------------------------------------

def test_run_cockpit_no_execution():
    result = run_cockpit()
    assert result.cockpit_executes_order is False

def test_run_cockpit_no_mutation():
    result = run_cockpit()
    assert result.cockpit_mutates_strategy is False

def test_run_cockpit_no_rebalancing():
    result = run_cockpit()
    assert result.cockpit_rebalances_real_portfolio is False

def test_abc_decision_no_execution():
    abc = PaperCockpitABCDecision()
    assert abc.cockpit_executes_order is False
    assert abc.cockpit_mutates_strategy is False

def test_decision_ticket_no_broker():
    ticket = PaperCockpitDecisionTicket()
    assert ticket.ticket_triggers_broker is False
    assert ticket.ticket_executes_order is False
    assert ticket.ticket_mutates_strategy is False

def test_dashboard_no_production_writes():
    dashboard = PaperCockpitDashboard()
    assert dashboard.dashboard_writes_production_db is False
    assert dashboard.dashboard_places_real_order is False

def test_report_no_order_trigger():
    report = PaperCockpitReport()
    assert report.report_triggers_real_order is False
    assert report.report_activates_live_strategy is False

def test_audit_trail_no_activation():
    trail = PaperCockpitAuditTrail()
    assert trail.audit_triggers_order is False
    assert trail.audit_activates_live_strategy is False

def test_no_entry_condition_no_execution():
    cond = PaperCockpitNoEntryCondition()
    assert cond.cockpit_executes_order is False

def test_human_review_no_auto_approval():
    review = PaperCockpitHumanReviewRequest()
    assert review.auto_approval_blocked is True
    assert review.cockpit_auto_approves is False

def test_position_sizing_no_execution():
    sizing = PaperCockpitPositionSizingCheck()
    assert sizing.sizing_executes_order is False
    assert sizing.sizing_mutates_strategy is False

def test_portfolio_risk_no_rebalancing():
    risk = PaperCockpitPortfolioRiskCheck()
    assert risk.no_real_portfolio_rebalancing is True

# ---------------------------------------------------------------------------
# Safety: all models have paper_only=True
# ---------------------------------------------------------------------------

def test_cockpit_input_paper_only():
    assert PaperCockpitInput().paper_only is True

def test_cockpit_result_paper_only():
    assert PaperCockpitResult().paper_only is True

def test_abc_decision_paper_only():
    assert PaperCockpitABCDecision().paper_only is True

def test_decision_ticket_paper_only():
    assert PaperCockpitDecisionTicket().paper_only is True

def test_portfolio_risk_paper_only():
    assert PaperCockpitPortfolioRiskCheck().paper_only is True

def test_dashboard_paper_only():
    assert PaperCockpitDashboard().paper_only is True

def test_report_paper_only():
    assert PaperCockpitReport().paper_only is True

def test_audit_trail_paper_only():
    assert PaperCockpitAuditTrail().paper_only is True

def test_human_review_paper_only():
    assert PaperCockpitHumanReviewRequest().paper_only is True

# ---------------------------------------------------------------------------
# Safety: all models have no_real_orders or equivalent
# ---------------------------------------------------------------------------

def test_cockpit_input_no_real_orders():
    assert PaperCockpitInput().no_real_orders is True

def test_cockpit_result_no_real_orders():
    assert PaperCockpitResult().no_real_orders is True

def test_decision_ticket_no_real_orders():
    assert PaperCockpitDecisionTicket().no_real_orders is True

def test_report_no_real_orders():
    assert PaperCockpitReport().no_real_orders is True

def test_audit_trail_no_real_orders():
    assert PaperCockpitAuditTrail().no_real_orders is True

# ---------------------------------------------------------------------------
# Safety: hard block conditions coverage
# ---------------------------------------------------------------------------

def test_hard_block_real_order_listed():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_broker_listed():
    assert "broker_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_margin_listed():
    assert "margin_or_leverage_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_production_db_listed():
    assert "production_db_write_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_strategy_mutation_listed():
    assert "production_strategy_mutation_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_automatic_rollback_listed():
    assert "automatic_rollback_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_live_activation_listed():
    assert "live_strategy_activation_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_rebalancing_listed():
    assert "real_portfolio_rebalancing_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_missing_watchlist():
    assert "missing_watchlist" in HARD_BLOCK_CONDITIONS

def test_hard_block_malformed_input():
    assert "malformed_cockpit_input" in HARD_BLOCK_CONDITIONS

def test_hard_block_unsafe_export():
    assert "unsafe_export_path" in HARD_BLOCK_CONDITIONS

def test_hard_block_executes_order():
    assert "cockpit_tries_to_execute_order" in HARD_BLOCK_CONDITIONS

def test_hard_block_mutates_strategy():
    assert "cockpit_tries_to_mutate_strategy" in HARD_BLOCK_CONDITIONS

def test_hard_block_rebalances_portfolio():
    assert "cockpit_tries_to_rebalance_real_portfolio" in HARD_BLOCK_CONDITIONS

# ---------------------------------------------------------------------------
# Safety: validation enforces paper flags
# ---------------------------------------------------------------------------

def test_validation_rejects_paper_only_false():
    inp = PaperCockpitInput(paper_only=False)
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_validation_rejects_no_real_orders_false():
    inp = PaperCockpitInput(no_real_orders=False)
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_validation_rejects_no_broker_false():
    inp = PaperCockpitInput(no_broker=False)
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_validation_rejects_not_investment_advice_false():
    inp = PaperCockpitInput(not_investment_advice=False)
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_validation_rejects_human_review_false():
    inp = PaperCockpitInput(human_review_required=False)
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_validation_rejects_wrong_schema_version():
    inp = PaperCockpitInput(schema_version="100")
    result = validate_cockpit(inp)
    assert result.is_valid is False

def test_validation_passes_all_defaults():
    result = validate_cockpit(PaperCockpitInput())
    assert result.is_valid is True

# ---------------------------------------------------------------------------
# Safety: verify_version covers all invariants
# ---------------------------------------------------------------------------

def test_verify_version_passes():
    assert verify_version() is True

def test_verify_version_is_bool():
    assert isinstance(verify_version(), bool)

def test_safety_flags_all_safety_true():
    positive_flags = [
        "paper_only", "research_only", "simulate_only", "validation_only",
        "unified_paper_cockpit_only", "decision_console_only", "dashboard_only",
        "report_only", "audit_only", "no_real_orders", "no_broker", "no_margin",
        "no_leverage", "no_production_db_write", "no_production_strategy_mutation",
        "no_automatic_rollback", "no_live_strategy_activation", "no_real_portfolio_rebalancing",
        "not_investment_advice", "human_review_required", "deterministic_paper_workflow",
        "backward_compatible_v170_to_v1910",
    ]
    for flag in positive_flags:
        assert SAFETY_FLAGS.get(flag) is True, f"Safety flag '{flag}' should be True"

def test_safety_flags_all_block_false():
    block_flags = [
        "cockpit_executes_order", "cockpit_mutates_strategy", "cockpit_rebalances_real_portfolio",
        "export_triggers_real_order", "ticket_triggers_broker", "dashboard_writes_production_db",
        "report_activates_live_strategy", "audit_activates_live_strategy",
    ]
    for flag in block_flags:
        assert SAFETY_FLAGS.get(flag) is False, f"Safety flag '{flag}' should be False"
