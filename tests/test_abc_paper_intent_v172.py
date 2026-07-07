"""tests/test_abc_paper_intent_v172.py — Paper order intent tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_paper_order_intent_v172 import (
    build_paper_order_intent, get_paper_intent_actions,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCPaperOrderIntentType, ABCExecutionBlockReason,
    ABCRiskPermission,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCEntryPricePlan, ABCStopLossExecutionPlan, ABCTakeProfitExecutionPlan,
    ABCPositionSizingBridgeResult,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCEntryMode, ABCStopLossMode, ABCTakeProfitMode,
)


def _make_entry_ready():
    return ABCEntryPricePlan(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        entry_mode=ABCEntryMode.MA10_RECLAIM,
        status=ABCExecutionStatus.READY, entry_price=100.0,
    )


def _make_sl():
    return ABCStopLossExecutionPlan(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        stop_loss_mode=ABCStopLossMode.MA10_BREAK_REF,
        stop_loss_price=93.0, stop_loss_pct_from_entry=0.07,
    )


def _make_tp():
    return ABCTakeProfitExecutionPlan(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        take_profit_mode=ABCTakeProfitMode.SWING_25_40_PCT,
        take_profit_references=[125.0, 140.0],
    )


def _make_ps():
    return ABCPositionSizingBridgeResult(
        symbol="2330", capital_twd=300_000.0, max_holdings=4,
        position_amount=30_000.0, quantity_estimate=1000,
        max_loss_amount=2_100.0, risk_pct=0.007,
        training_cap_applied=False,
        risk_permission=ABCRiskPermission.ALLOWED,
        block_reasons=[],
    )


def test_ready_entry_produces_paper_buy():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.action == ABCPaperOrderIntentType.PAPER_BUY


def test_real_order_requested_blocked():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
        real_order_requested=True,
    )
    assert intent.action == ABCPaperOrderIntentType.PAPER_BLOCK


def test_real_order_block_reason():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
        real_order_requested=True,
    )
    assert ABCExecutionBlockReason.REAL_ORDER_REQUESTED in intent.block_reasons


def test_broker_requested_blocked():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
        broker_execution_requested=True,
    )
    assert intent.action == ABCPaperOrderIntentType.PAPER_BLOCK


def test_block_reasons_cause_paper_block():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(),
        [ABCExecutionBlockReason.BELOW_20MA],
    )
    assert intent.action == ABCPaperOrderIntentType.PAPER_BLOCK


def test_no_block_real_order_is_false():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.real_order_requested is False


def test_broker_execution_disabled():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.broker_execution_requested is False


def test_intent_id_nonempty():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert len(intent.intent_id) > 0


def test_get_paper_intent_actions_nonempty():
    actions = get_paper_intent_actions()
    assert len(actions) > 0


def test_paper_only_flag():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.paper_only is True


def test_not_investment_advice():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.not_investment_advice is True


def test_no_real_orders_flag():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.no_real_orders is True


def test_reference_price_from_entry():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.reference_price == 100.0


def test_stop_loss_price_stored():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.stop_loss_price == 93.0


def test_quantity_from_position_sizing():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.quantity_estimate == 1000


def test_broker_requested_block_reason():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
        broker_execution_requested=True,
    )
    assert ABCExecutionBlockReason.BROKER_REQUESTED in intent.block_reasons


def test_take_profit_references_stored():
    intent = build_paper_order_intent(
        "2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK,
        _make_entry_ready(), _make_sl(), _make_tp(), _make_ps(), [],
    )
    assert intent.take_profit_references == [125.0, 140.0]


def test_paper_intent_actions_include_buy():
    actions = get_paper_intent_actions()
    assert "PAPER_BUY" in actions


def test_paper_intent_actions_include_block():
    actions = get_paper_intent_actions()
    assert "PAPER_BLOCK" in actions
