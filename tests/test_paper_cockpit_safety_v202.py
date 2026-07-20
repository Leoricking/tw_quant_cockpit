"""
tests/test_paper_cockpit_safety_v202.py
v2.0.2 Paper Cockpit — Safety Tests (25+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# Module-level safety constants
# ---------------------------------------------------------------------------

def test_no_real_orders_is_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True


def test_broker_execution_enabled_is_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False


def test_production_trading_blocked_is_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# ---------------------------------------------------------------------------
# SAFETY_FLAGS_V202 tests
# ---------------------------------------------------------------------------

def test_safety_flags_v202_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert isinstance(SAFETY_FLAGS_V202, dict)


def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["paper_only"] is True


def test_safety_flags_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["research_only"] is True


def test_safety_flags_simulate_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["simulate_only"] is True


def test_safety_flags_validation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["validation_only"] is True


def test_safety_flags_report_export_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["report_export_only"] is True


def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_real_orders"] is True


def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_broker"] is True


def test_safety_flags_no_margin():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_margin"] is True


def test_safety_flags_no_leverage():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_leverage"] is True


def test_safety_flags_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["not_investment_advice"] is True


def test_safety_flags_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["human_review_required"] is True


def test_safety_flags_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["production_trading_blocked"] is True


def test_safety_flags_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["broker_execution_enabled"] is False


def test_safety_flags_cockpit_executes_order_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["cockpit_executes_order"] is False


def test_safety_flags_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_automatic_rebalance"] is True


def test_safety_flags_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_real_account_sync"] is True


def test_safety_flags_export_is_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["export_is_paper_only"] is True


def test_safety_flags_no_sensitive_data():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_sensitive_data"] is True


def test_safety_flags_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert len(SAFETY_FLAGS_V202) == 20


# ---------------------------------------------------------------------------
# Export output safety fields
# ---------------------------------------------------------------------------

def test_json_export_paper_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.paper_only is True
    assert result.no_real_orders is True


def test_markdown_export_paper_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.paper_only is True
    assert result.no_real_orders is True


def test_csv_export_paper_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.paper_only is True
    assert result.no_real_orders is True


def test_audit_pack_safety_snapshot_has_all_guards():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    ss = result.safety_snapshot
    assert ss["NO_REAL_ORDERS"] is True
    assert ss["BROKER_EXECUTION_ENABLED"] is False
    assert ss["PRODUCTION_TRADING_BLOCKED"] is True
    assert ss["paper_only_guard_enabled"] is True
    assert ss["no_real_account_sync"] is True
    assert ss["no_automatic_rebalance"] is True


def test_export_status_summary_safety():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.paper_only_guard_enabled is True
    assert result.broker_execution_disabled is True
    assert result.production_trading_blocked is True
