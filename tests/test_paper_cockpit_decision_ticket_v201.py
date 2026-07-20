"""
tests/test_paper_cockpit_decision_ticket_v201.py
v2.0.1 Paper Cockpit — Decision Ticket Tests (40+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
    EnhancedDecisionTicket, ENHANCED_TICKET_FIELDS, DAILY_FINAL_ACTIONS,
    build_enhanced_ticket,
)


# --- ENHANCED_TICKET_FIELDS list tests ---

def test_enhanced_ticket_fields_count():
    assert len(ENHANCED_TICKET_FIELDS) == 22

def test_enhanced_ticket_fields_contains_symbol():
    assert "symbol" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_name():
    assert "name" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_setup_type():
    assert "setup_type" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_theme_score():
    assert "theme_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_fundamental_score():
    assert "fundamental_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_technical_score():
    assert "technical_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_volume_score():
    assert "volume_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_chip_score():
    assert "chip_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_margin_score():
    assert "margin_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_total_score():
    assert "total_score" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_entry_price_plan():
    assert "entry_price_plan" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_add_price_plan():
    assert "add_price_plan" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_reduce_price_plan():
    assert "reduce_price_plan" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_exit_price_plan():
    assert "exit_price_plan" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_stop_loss_price():
    assert "stop_loss_price" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_invalid_conditions():
    assert "invalid_conditions" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_risk_amount():
    assert "risk_amount" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_max_position_size():
    assert "max_position_size" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_position_size_reason():
    assert "position_size_reason" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_no_entry_reasons():
    assert "no_entry_reasons" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_human_review_required():
    assert "human_review_required" in ENHANCED_TICKET_FIELDS

def test_enhanced_ticket_fields_contains_final_action():
    assert "final_action" in ENHANCED_TICKET_FIELDS


# --- EnhancedDecisionTicket dataclass tests ---

def test_enhanced_ticket_default_schema_version():
    t = EnhancedDecisionTicket()
    assert t.schema_version == "201"

def test_enhanced_ticket_default_paper_only():
    t = EnhancedDecisionTicket()
    assert t.paper_only is True

def test_enhanced_ticket_default_no_real_orders():
    t = EnhancedDecisionTicket()
    assert t.no_real_orders is True

def test_enhanced_ticket_default_no_broker():
    t = EnhancedDecisionTicket()
    assert t.no_broker is True

def test_enhanced_ticket_default_not_investment_advice():
    t = EnhancedDecisionTicket()
    assert t.not_investment_advice is True

def test_enhanced_ticket_default_human_review_required():
    t = EnhancedDecisionTicket()
    assert t.human_review_required is True

def test_enhanced_ticket_default_ticket_triggers_broker_false():
    t = EnhancedDecisionTicket()
    assert t.ticket_triggers_broker is False

def test_enhanced_ticket_default_ticket_executes_order_false():
    t = EnhancedDecisionTicket()
    assert t.ticket_executes_order is False

def test_enhanced_ticket_default_final_action():
    t = EnhancedDecisionTicket()
    assert t.final_action == "NO_ENTRY"

def test_enhanced_ticket_default_invalid_conditions_empty_list():
    t = EnhancedDecisionTicket()
    assert t.invalid_conditions == []

def test_enhanced_ticket_default_no_entry_reasons_empty_list():
    t = EnhancedDecisionTicket()
    assert t.no_entry_reasons == []

def test_enhanced_ticket_custom_fields():
    t = EnhancedDecisionTicket(
        symbol="2330",
        name="台積電",
        setup_type="A_PULLBACK_10MA",
        theme_score=85.0,
        final_action="PAPER_BUY_PLAN",
    )
    assert t.symbol == "2330"
    assert t.name == "台積電"
    assert t.setup_type == "A_PULLBACK_10MA"
    assert t.theme_score == 85.0
    assert t.final_action == "PAPER_BUY_PLAN"


# --- build_enhanced_ticket function tests ---

def test_build_enhanced_ticket_default():
    t = build_enhanced_ticket()
    assert isinstance(t, EnhancedDecisionTicket)

def test_build_enhanced_ticket_schema_version():
    t = build_enhanced_ticket("2330")
    assert t.schema_version == "201"

def test_build_enhanced_ticket_paper_only():
    t = build_enhanced_ticket("2330")
    assert t.paper_only is True

def test_build_enhanced_ticket_symbol():
    t = build_enhanced_ticket("2330")
    assert t.symbol == "2330"

def test_build_enhanced_ticket_name():
    t = build_enhanced_ticket("2330", name="台積電")
    assert t.name == "台積電"

def test_build_enhanced_ticket_total_score_computed():
    t = build_enhanced_ticket(
        "2330",
        theme_score=80.0, fundamental_score=80.0, technical_score=80.0,
        volume_score=80.0, chip_score=80.0, margin_score=80.0,
    )
    assert t.total_score == 80.0

def test_build_enhanced_ticket_total_score_average():
    t = build_enhanced_ticket(
        "2330",
        theme_score=60.0, fundamental_score=80.0, technical_score=100.0,
        volume_score=60.0, chip_score=80.0, margin_score=80.0,
    )
    expected = (60.0 + 80.0 + 100.0 + 60.0 + 80.0 + 80.0) / 6.0
    assert abs(t.total_score - expected) < 0.001

def test_build_enhanced_ticket_no_entry_reasons():
    t = build_enhanced_ticket("2330", no_entry_reasons=["trend_broken"])
    assert "trend_broken" in t.no_entry_reasons

def test_build_enhanced_ticket_invalid_conditions():
    t = build_enhanced_ticket("2330", invalid_conditions=["trend_broken"])
    assert "trend_broken" in t.invalid_conditions

def test_build_enhanced_ticket_final_action_paper_buy_plan():
    t = build_enhanced_ticket("2330", final_action="PAPER_BUY_PLAN")
    assert t.final_action == "PAPER_BUY_PLAN"

def test_build_enhanced_ticket_final_action_in_daily_final_actions():
    for action in DAILY_FINAL_ACTIONS:
        t = build_enhanced_ticket("2330", final_action=action)
        assert t.final_action == action

def test_build_enhanced_ticket_human_review_required():
    t = build_enhanced_ticket("2330")
    assert t.human_review_required is True

def test_build_enhanced_ticket_ticket_triggers_broker_false():
    t = build_enhanced_ticket("2330")
    assert t.ticket_triggers_broker is False

def test_build_enhanced_ticket_ticket_executes_order_false():
    t = build_enhanced_ticket("2330")
    assert t.ticket_executes_order is False

def test_build_enhanced_ticket_prices():
    t = build_enhanced_ticket(
        "2330",
        entry_price_plan=920.0,
        add_price_plan=950.0,
        reduce_price_plan=1100.0,
        exit_price_plan=1242.0,
        stop_loss_price=874.0,
    )
    assert t.entry_price_plan == 920.0
    assert t.add_price_plan == 950.0
    assert t.reduce_price_plan == 1100.0
    assert t.exit_price_plan == 1242.0
    assert t.stop_loss_price == 874.0

def test_build_enhanced_ticket_risk_sizing():
    t = build_enhanced_ticket("2330", risk_amount=4500.0, max_position_size=45000.0)
    assert t.risk_amount == 4500.0
    assert t.max_position_size == 45000.0

def test_build_enhanced_ticket_position_size_reason():
    t = build_enhanced_ticket("2330", position_size_reason="test reason")
    assert t.position_size_reason == "test reason"
