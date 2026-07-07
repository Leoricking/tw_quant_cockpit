"""tests/test_abc_models_v172.py — Dataclass model tests for v1.7.2."""
import pytest
from dataclasses import fields
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCNormalizedSignal, ABCConditionCheck,
    ABCEntryPricePlan, ABCAddPricePlan, ABCStopLossExecutionPlan,
    ABCTakeProfitExecutionPlan, ABCInvalidationPlan,
    ABCPositionSizingBridgeResult, ABCWatchlistBridgeResult,
    ABCMarketRegimeBridgeResult, ABCForbiddenRuleBridgeResult,
    ABCPaperOrderIntent, ABCExecutionPlan, ABCExecutionScorecard,
    ABCExecutionReport, ABCExecutionHealthSummary,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCPaperOrderIntentType,
)

_REQUIRED_FIELDS = ["schema_version", "policy_version", "source_lineage", "created_at",
                    "paper_only", "research_only", "no_real_orders", "not_investment_advice"]

def _field_names(cls):
    return [f.name for f in fields(cls)]


def test_signal_input_has_required_fields():
    for f in _REQUIRED_FIELDS:
        assert f in _field_names(ABCSignalInput), f"Missing {f} in ABCSignalInput"


def test_normalized_signal_has_required_fields():
    for f in _REQUIRED_FIELDS:
        assert f in _field_names(ABCNormalizedSignal)


def test_condition_check_has_required_fields():
    for f in _REQUIRED_FIELDS:
        assert f in _field_names(ABCConditionCheck)


def test_entry_plan_has_required_fields():
    for f in _REQUIRED_FIELDS:
        assert f in _field_names(ABCEntryPricePlan)


def test_stop_loss_plan_has_required_fields():
    for f in _REQUIRED_FIELDS:
        assert f in _field_names(ABCStopLossExecutionPlan)


def test_paper_intent_has_required_fields():
    for f in ["paper_only", "no_real_orders", "not_investment_advice"]:
        assert f in _field_names(ABCPaperOrderIntent)


def test_paper_intent_broker_enabled_false():
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCPaperOrderIntentType
    intent = ABCPaperOrderIntent(
        intent_id="test", symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        tier="MAIN_THEME", action=ABCPaperOrderIntentType.PAPER_BUY,
        reference_price=100.0, quantity_estimate=1000, position_size_amount=50000.0,
        max_loss_amount=3000.0, stop_loss_price=95.0,
    )
    assert intent.broker_execution_enabled is False
    assert intent.paper_only is True
    assert intent.no_real_orders is True


def test_execution_plan_has_schema_version():
    assert "schema_version" in _field_names(ABCExecutionPlan)


def test_execution_plan_default_paper_only():
    plan = ABCExecutionPlan(
        symbol="TEST", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        tier="MAIN_THEME", status=ABCExecutionStatus.BLOCKED,
    )
    assert plan.paper_only is True
    assert plan.no_real_orders is True
    assert plan.not_investment_advice is True


def test_execution_report_has_required_fields():
    for f in _REQUIRED_FIELDS:
        assert f in _field_names(ABCExecutionReport)


def test_health_summary_has_schema_version():
    assert "schema_version" in _field_names(ABCExecutionHealthSummary)


def test_scorecard_weights_sum_field():
    assert "weights_sum" in _field_names(ABCExecutionScorecard)


def test_position_sizing_has_training_cap_field():
    assert "training_cap_applied" in _field_names(ABCPositionSizingBridgeResult)


def test_watchlist_bridge_has_training_cap():
    assert "training_cap" in _field_names(ABCWatchlistBridgeResult)
