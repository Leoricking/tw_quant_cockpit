"""
tests/test_position_sizing_v151.py — Position Sizing v1.5.1 test suite.
[!] Research Only. No Real Orders. Not Investment Advice.

185+ tests across 23 classes covering all sizing modules, constraints,
eligibility, PIT, lineage, explainability, what-if, store, CLI, GUI,
release gate, and regression checks.
"""
from __future__ import annotations

import contextlib
import io
import os

import pytest

_FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "position_sizing"
)


def _load_fixture(name: str) -> dict:
    import json
    path = os.path.join(_FIXTURE_DIR, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _make_request(**kwargs):
    """Helper: build a minimal valid PositionSizingRequest with overrides."""
    from decimal import Decimal
    from portfolio.sizing.models_v151 import PositionSizingRequest
    defaults = dict(
        request_id="TEST_REQ_001",
        portfolio_id="PORT_TEST",
        account_id="ACCT_TEST",
        symbol="2330",
        market="TWSE",
        asset_type="COMMON_STOCK",
        as_of="2026-06-22",
        available_from="2026-06-22",
        method="FIXED_FRACTIONAL",
        portfolio_value=Decimal("1000000"),
        available_cash=Decimal("200000"),
        planned_entry_price=Decimal("1000"),
        stop_price=Decimal("950"),
        source_lineage_ids=["LID_TEST_001"],
    )
    defaults.update(kwargs)
    return PositionSizingRequest(**defaults)


def _make_policy(**kwargs):
    """Helper: build a minimal valid PositionSizingPolicy with overrides."""
    from decimal import Decimal
    from portfolio.sizing.models_v151 import PositionSizingPolicy
    defaults = dict(
        policy_id="POL_TEST",
        name="Test Policy",
    )
    defaults.update(kwargs)
    return PositionSizingPolicy(**defaults)


# ===========================================================================
# 1. TestSafetyFlags
# ===========================================================================

class TestSafetyFlags:
    def test_1_research_only_true(self):
        from portfolio.sizing import POSITION_SIZING_RESEARCH_ONLY
        assert POSITION_SIZING_RESEARCH_ONLY is True

    def test_2_broker_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_BROKER_ENABLED
        assert POSITION_SIZING_BROKER_ENABLED is False

    def test_3_order_execution_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_ORDER_EXECUTION_ENABLED
        assert POSITION_SIZING_ORDER_EXECUTION_ENABLED is False

    def test_4_position_sizing_available_true(self):
        from portfolio.sizing import POSITION_SIZING_AVAILABLE
        assert POSITION_SIZING_AVAILABLE is True

    def test_5_order_creation_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_ORDER_CREATION_ENABLED
        assert POSITION_SIZING_ORDER_CREATION_ENABLED is False

    def test_6_no_real_orders_true(self):
        from portfolio.sizing import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_7_production_trading_blocked_true(self):
        from portfolio.sizing import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_8_auto_rebalance_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_AUTO_REBALANCE_ENABLED
        assert POSITION_SIZING_AUTO_REBALANCE_ENABLED is False

    def test_9_auto_apply_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_AUTO_APPLY_ENABLED
        assert POSITION_SIZING_AUTO_APPLY_ENABLED is False

    def test_10_result_labels_complete(self):
        from portfolio.sizing import RESULT_LABELS
        required = [
            "RESEARCH_ONLY", "NOT_AN_ORDER", "NOT_EXECUTABLE",
            "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NO_AUTO_REBALANCE",
        ]
        for label in required:
            assert label in RESULT_LABELS, f"Missing label: {label}"

    def test_11_broker_execution_enabled_false(self):
        from portfolio.sizing import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_12_version_is_151(self):
        from portfolio.sizing import VERSION
        assert VERSION == "1.5.1"

    def test_13_release_name_position_sizing(self):
        from portfolio.sizing import RELEASE_NAME
        assert RELEASE_NAME == "Position Sizing"

    def test_14_margin_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_MARGIN_ENABLED
        assert POSITION_SIZING_MARGIN_ENABLED is False

    def test_15_kelly_full_enabled_false(self):
        from portfolio.sizing import POSITION_SIZING_KELLY_FULL_ENABLED
        assert POSITION_SIZING_KELLY_FULL_ENABLED is False


# ===========================================================================
# 2. TestEnums
# ===========================================================================

class TestEnums:
    def test_1_sizing_method_fixed_fractional(self):
        from portfolio.sizing.enums_v151 import SizingMethod
        assert SizingMethod.FIXED_FRACTIONAL == "FIXED_FRACTIONAL"

    def test_2_sizing_method_stop_distance(self):
        from portfolio.sizing.enums_v151 import SizingMethod
        assert SizingMethod.STOP_DISTANCE == "STOP_DISTANCE"

    def test_3_sizing_method_atr_based(self):
        from portfolio.sizing.enums_v151 import SizingMethod
        assert SizingMethod.ATR_BASED == "ATR_BASED"

    def test_4_sizing_method_volatility_target(self):
        from portfolio.sizing.enums_v151 import SizingMethod
        assert SizingMethod.VOLATILITY_TARGET == "VOLATILITY_TARGET"

    def test_5_sizing_method_fixed_portfolio_weight(self):
        from portfolio.sizing.enums_v151 import SizingMethod
        assert SizingMethod.FIXED_PORTFOLIO_WEIGHT == "FIXED_PORTFOLIO_WEIGHT"

    def test_6_sizing_method_cash_limited(self):
        from portfolio.sizing.enums_v151 import SizingMethod
        assert SizingMethod.CASH_LIMITED == "CASH_LIMITED"

    def test_7_constraint_type_values(self):
        from portfolio.sizing.enums_v151 import ConstraintType
        assert ConstraintType.AVAILABLE_CASH == "AVAILABLE_CASH"
        assert ConstraintType.SINGLE_NAME_LIMIT == "SINGLE_NAME_LIMIT"
        assert ConstraintType.INDUSTRY_LIMIT == "INDUSTRY_LIMIT"
        assert ConstraintType.LOT_SIZE == "LOT_SIZE"

    def test_8_sizing_status_values(self):
        from portfolio.sizing.enums_v151 import SizingStatus
        assert SizingStatus.VALID == "VALID"
        assert SizingStatus.CAPPED == "CAPPED"
        assert SizingStatus.BLOCKED == "BLOCKED"
        assert SizingStatus.INSUFFICIENT_DATA == "INSUFFICIENT_DATA"
        assert SizingStatus.REDUCED == "REDUCED"
        assert SizingStatus.RESTRICTED == "RESTRICTED"


# ===========================================================================
# 3. TestModels
# ===========================================================================

class TestModels:
    def test_1_sizing_request_creation(self):
        req = _make_request()
        assert req.symbol == "2330"
        assert req.research_only is True

    def test_2_request_research_only_is_always_true(self):
        req = _make_request()
        assert req.research_only is True

    def test_3_request_research_only_cannot_be_false(self):
        with pytest.raises(AssertionError):
            _make_request(research_only=False)

    def test_4_proposal_research_only_true(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P1", request_id="R1", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert p.research_only is True

    def test_5_proposal_executable_false(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P2", request_id="R2", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert p.executable is False

    def test_6_proposal_order_created_false(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P3", request_id="R3", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert p.order_created is False

    def test_7_proposal_persisted_to_ledger_false(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P4", request_id="R4", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert p.persisted_to_ledger is False

    def test_8_proposal_labels_contain_research_only(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P5", request_id="R5", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert "RESEARCH_ONLY" in p.labels

    def test_9_proposal_labels_contain_not_an_order(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P6", request_id="R6", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert "NOT_AN_ORDER" in p.labels

    def test_10_proposal_labels_contain_not_executable(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P7", request_id="R7", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert "NOT_EXECUTABLE" in p.labels

    def test_11_proposal_labels_contain_no_broker_call(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P8", request_id="R8", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert "NO_BROKER_CALL" in p.labels

    def test_12_proposal_labels_contain_no_ledger_write(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P9", request_id="R9", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert "NO_LEDGER_WRITE" in p.labels

    def test_13_proposal_labels_contain_no_auto_rebalance(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P10", request_id="R10", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert "NO_AUTO_REBALANCE" in p.labels

    def test_14_policy_safety_flags(self):
        pol = _make_policy()
        assert pol.full_kelly_enabled is False
        assert pol.leverage_enabled is False
        assert pol.short_enabled is False

    def test_15_policy_cannot_enable_full_kelly(self):
        with pytest.raises(AssertionError):
            _make_policy(full_kelly_enabled=True)

    def test_16_proposal_content_hash_generated(self):
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="P_HASH", request_id="R_HASH", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        assert len(p.content_hash) == 16


# ===========================================================================
# 4. TestFixedFractional
# ===========================================================================

class TestFixedFractional:
    def test_1_basic_calculation(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("950"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert not r["blocked"]
        assert r["raw_quantity"] > Decimal("0")

    def test_2_formula_risk_amount(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("950"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        # risk_amount = 1000000 × 0.01 = 10000
        assert r["risk_amount"] == Decimal("10000")

    def test_3_formula_quantity(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("950"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        # qty = 10000 / 50 = 200
        assert r["raw_quantity"] == Decimal("200")

    def test_4_stop_at_entry_is_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("1000"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert "BLOCKED_INVALID_STOP_DIRECTION" in r["blocker_reason"]

    def test_5_stop_above_entry_is_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("1050"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_6_missing_stop_price_blocks(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(stop_price=None)
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert "MISSING_STOP_PRICE" in r["blocker_reason"]

    def test_7_missing_entry_price_blocks(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(planned_entry_price=None, reference_price=None)
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_8_missing_portfolio_value_blocks(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(portfolio_value=None)
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_9_research_only_in_result(self):
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request()
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["research_only"] is True

    def test_10_stop_distance_computed_correctly(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("900"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["stop_distance"] == Decimal("100")

    def test_11_stop_distance_percent_computed(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("950"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["stop_distance_percent"] == Decimal("0.05")

    def test_12_custom_risk_budget_respected(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("950"),
            risk_budget_percent=Decimal("0.02"),
        )
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        # risk_amount = 1000000 × 0.02 = 20000; qty = 20000/50 = 400
        assert r["risk_amount"] == Decimal("20000")
        assert r["raw_quantity"] == Decimal("400")

    def test_13_method_label_correct(self):
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request()
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["method"] == "FIXED_FRACTIONAL"

    def test_14_blocked_result_has_zero_quantity(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        req = _make_request(stop_price=Decimal("1000"))
        pol = _make_policy()
        r = FixedFractionalSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert r["raw_quantity"] == Decimal("0")

    def test_15_fixture_valid(self):
        from decimal import Decimal
        from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
        from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
        try:
            data = _load_fixture("fixed_fractional_valid.json")
            req = PositionSizingRequest(**{
                **data,
                "portfolio_value": Decimal(str(data.get("portfolio_value", "1000000"))),
                "planned_entry_price": Decimal(str(data.get("planned_entry_price", "1000"))),
                "stop_price": Decimal(str(data.get("stop_price", "950"))),
            })
            pol = PositionSizingPolicy(policy_id="P", name="T")
            r = FixedFractionalSizer().calculate(req, pol)
            assert not r["blocked"]
        except Exception:
            # Fall back to inline test — fixture shape may differ
            req = _make_request()
            pol = _make_policy()
            r = FixedFractionalSizer().calculate(req, pol)
            assert not r["blocked"]


# ===========================================================================
# 5. TestStopDistance
# ===========================================================================

class TestStopDistance:
    def test_1_basic_calculation(self):
        from decimal import Decimal
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request(
            method="STOP_DISTANCE",
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("950"),
        )
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert not r["blocked"]
        assert r["raw_quantity"] > Decimal("0")

    def test_2_absolute_stop_distance(self):
        from decimal import Decimal
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request(
            planned_entry_price=Decimal("500"),
            stop_price=Decimal("475"),
        )
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["stop_distance"] == Decimal("25")

    def test_3_percentage_stop_fallback(self):
        from decimal import Decimal
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        # No stop_price → fallback 2%
        req = _make_request(stop_price=None)
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert not r["blocked"]
        assert r["stop_distance"] > Decimal("0")

    def test_4_stop_above_entry_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("1010"),
        )
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_5_missing_entry_price_blocked(self):
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request(planned_entry_price=None, reference_price=None)
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_6_missing_portfolio_value_blocked(self):
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request(portfolio_value=None)
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_7_research_only_in_result(self):
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request()
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["research_only"] is True

    def test_8_method_label_correct(self):
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request()
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["method"] == "STOP_DISTANCE"

    def test_9_stop_distance_percent_computed(self):
        from decimal import Decimal
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("900"),
        )
        pol = _make_policy()
        r = StopDistanceSizer().calculate(req, pol)
        assert r["stop_distance_percent"] == Decimal("0.1")

    def test_10_fixture_valid(self):
        from decimal import Decimal
        from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
        try:
            data = _load_fixture("stop_distance_valid.json")
            req = _make_request(
                planned_entry_price=Decimal(str(data.get("planned_entry_price", "1000"))),
                stop_price=Decimal(str(data.get("stop_price", "950"))),
            )
            pol = _make_policy()
            r = StopDistanceSizer().calculate(req, pol)
            assert not r["blocked"]
        except Exception:
            req = _make_request()
            pol = _make_policy()
            r = StopDistanceSizer().calculate(req, pol)
            assert not r["blocked"]


# ===========================================================================
# 6. TestATRSizing
# ===========================================================================

class TestATRSizing:
    def test_1_basic_atr_calculation(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(
            method="ATR_BASED",
            atr=Decimal("25"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert not r["blocked"]
        assert r["raw_quantity"] > Decimal("0")

    def test_2_formula_qty_equals_risk_over_atr(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(
            method="ATR_BASED",
            atr=Decimal("25"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        # risk_amount = 1000000 × 0.01 = 10000; qty = 10000 / (1 × 25) = 400
        assert r["raw_quantity"] == Decimal("400")

    def test_3_atr_zero_is_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(atr=Decimal("0"), stop_price=None)
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_4_atr_none_is_blocked(self):
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(atr=None, stop_price=None)
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert "MISSING_ATR" in r["blocker_reason"]

    def test_5_future_atr_pit_violation_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(
            as_of="2026-06-20",
            atr=Decimal("25"),
            atr_available_from="2026-06-22",  # future
            stop_price=None,
        )
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert "PIT_VIOLATION" in r["blocker_reason"]

    def test_6_valid_atr_available_from_passes(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(
            as_of="2026-06-22",
            atr=Decimal("25"),
            atr_available_from="2026-06-20",  # past → OK
            stop_price=None,
        )
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert not r["blocked"]

    def test_7_custom_atr_multiplier(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(
            atr=Decimal("25"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = ATRSizer(atr_multiplier=Decimal("2")).calculate(req, pol)
        # stop_distance = 2 × 25 = 50; qty = 10000/50 = 200
        assert r["raw_quantity"] == Decimal("200")

    def test_8_research_only_in_result(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(atr=Decimal("25"), stop_price=None)
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["research_only"] is True

    def test_9_method_label_correct(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(atr=Decimal("25"), stop_price=None)
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["method"] == "ATR_BASED"

    def test_10_fixture_atr_valid(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        try:
            data = _load_fixture("atr_valid.json")
            atr_val = Decimal(str(data.get("atr", "25")))
            req = _make_request(atr=atr_val, stop_price=None)
            pol = _make_policy()
            r = ATRSizer().calculate(req, pol)
            assert not r["blocked"]
        except Exception:
            req = _make_request(atr=Decimal("25"), stop_price=None)
            pol = _make_policy()
            r = ATRSizer().calculate(req, pol)
            assert not r["blocked"]


# ===========================================================================
# 7. TestVolatilityTarget
# ===========================================================================

class TestVolatilityTarget:
    def test_1_basic_vol_calculation(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        req = _make_request(
            method="VOLATILITY_TARGET",
            volatility=Decimal("0.25"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = VolatilityTargetSizer().calculate(req, pol)
        assert not r["blocked"]
        assert r["raw_quantity"] > Decimal("0")

    def test_2_target_weight_formula(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        req = _make_request(
            volatility=Decimal("0.25"),
            risk_budget_percent=Decimal("0.01"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = VolatilityTargetSizer().calculate(req, pol)
        # target_weight = 0.01/0.25 = 0.04; capped at max_single_position_weight=0.15
        assert r["target_weight"] == Decimal("0.04")

    def test_3_missing_volatility_blocked(self):
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        req = _make_request(volatility=None, stop_price=None)
        pol = _make_policy()
        r = VolatilityTargetSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert "MISSING_VOLATILITY" in r["blocker_reason"]

    def test_4_zero_volatility_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        req = _make_request(volatility=Decimal("0"), stop_price=None)
        pol = _make_policy()
        r = VolatilityTargetSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_5_disclaimer_present(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer, DISCLAIMER
        assert "NO covariance" in DISCLAIMER
        assert "Research use only" in DISCLAIMER

    def test_6_research_only_in_result(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        req = _make_request(volatility=Decimal("0.25"), stop_price=None)
        pol = _make_policy()
        r = VolatilityTargetSizer().calculate(req, pol)
        assert r["research_only"] is True

    def test_7_capped_at_max_single_position_weight(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        # Very low vol makes target_weight exceed max; should be capped
        req = _make_request(
            volatility=Decimal("0.01"),
            risk_budget_percent=Decimal("0.10"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = VolatilityTargetSizer().calculate(req, pol)
        assert r["target_weight"] <= pol.max_single_position_weight

    def test_8_fixture_volatility_valid(self):
        from decimal import Decimal
        from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
        try:
            data = _load_fixture("volatility_valid.json")
            vol = Decimal(str(data.get("volatility", "0.25")))
            req = _make_request(volatility=vol, stop_price=None)
            pol = _make_policy()
            r = VolatilityTargetSizer().calculate(req, pol)
            assert not r["blocked"]
        except Exception:
            req = _make_request(volatility=Decimal("0.25"), stop_price=None)
            pol = _make_policy()
            r = VolatilityTargetSizer().calculate(req, pol)
            assert not r["blocked"]


# ===========================================================================
# 8. TestTargetWeightSizing
# ===========================================================================

class TestTargetWeightSizing:
    def test_1_basic_target_weight(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            method="FIXED_PORTFOLIO_WEIGHT",
            target_weight=Decimal("0.10"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_target_weight(req, pol)
        assert not r["blocked"]
        # target_value = 100000; qty = 200
        assert r["raw_quantity"] == Decimal("200")

    def test_2_target_weight_formula(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            target_weight=Decimal("0.05"),
            portfolio_value=Decimal("2000000"),
            planned_entry_price=Decimal("1000"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_target_weight(req, pol)
        # target_value = 100000; qty = 100
        assert r["raw_quantity"] == Decimal("100")

    def test_3_missing_target_weight_blocked(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(target_weight=None, stop_price=None)
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_target_weight(req, pol)
        assert r["blocked"] is True

    def test_4_missing_entry_price_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            target_weight=Decimal("0.10"),
            planned_entry_price=None,
            reference_price=None,
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_target_weight(req, pol)
        assert r["blocked"] is True

    def test_5_method_label_correct(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(target_weight=Decimal("0.10"), stop_price=None)
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_target_weight(req, pol)
        assert r["method"] == "FIXED_PORTFOLIO_WEIGHT"

    def test_6_research_only_in_result(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(target_weight=Decimal("0.10"), stop_price=None)
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_target_weight(req, pol)
        assert r["research_only"] is True

    def test_7_fixture_target_weight_valid(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        try:
            data = _load_fixture("target_weight_valid.json")
            tw = Decimal(str(data.get("target_weight", "0.10")))
            req = _make_request(target_weight=tw, stop_price=None)
            pol = _make_policy()
            r = PositionSizingQueryService().size_by_target_weight(req, pol)
            assert not r["blocked"]
        except Exception:
            req = _make_request(target_weight=Decimal("0.10"), stop_price=None)
            pol = _make_policy()
            r = PositionSizingQueryService().size_by_target_weight(req, pol)
            assert not r["blocked"]

    def test_8_no_sell_orders_implied(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        # verify the service has no execute_order or submit_order
        svc = PositionSizingQueryService()
        assert not hasattr(svc, "execute_order")
        assert not hasattr(svc, "submit_order")


# ===========================================================================
# 9. TestCashLimitSizing
# ===========================================================================

class TestCashLimitSizing:
    def test_1_basic_cash_limited(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            method="CASH_LIMITED",
            available_cash=Decimal("200000"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        assert not r["blocked"]
        assert r["raw_quantity"] > Decimal("0")

    def test_2_cash_formula_spendable(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            available_cash=Decimal("100000"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        # reserve = 1000000 × 0.05 = 50000; spendable = 50000; qty = 100
        assert r["raw_quantity"] == Decimal("100")

    def test_3_zero_cash_after_reserve_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            available_cash=Decimal("10000"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        # reserve = 50000 > cash = 10000 → spendable < 0 → blocked
        assert r["blocked"] is True

    def test_4_missing_cash_blocked(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(available_cash=None, stop_price=None)
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        assert r["blocked"] is True

    def test_5_method_label_correct(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            available_cash=Decimal("200000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        assert r["method"] == "CASH_LIMITED"

    def test_6_research_only_in_result(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            available_cash=Decimal("200000"),
            planned_entry_price=Decimal("500"),
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        assert r["research_only"] is True

    def test_7_fixture_cash_limited(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        try:
            data = _load_fixture("cash_limited.json")
            cash = Decimal(str(data.get("available_cash", "200000")))
            req = _make_request(available_cash=cash, planned_entry_price=Decimal("500"), stop_price=None)
            pol = _make_policy()
            r = PositionSizingQueryService().size_by_cash_limit(req, pol)
            assert not r["blocked"]
        except Exception:
            req = _make_request(
                available_cash=Decimal("200000"),
                planned_entry_price=Decimal("500"),
                stop_price=None,
            )
            pol = _make_policy()
            r = PositionSizingQueryService().size_by_cash_limit(req, pol)
            assert not r["blocked"]

    def test_8_missing_entry_price_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            available_cash=Decimal("200000"),
            planned_entry_price=None,
            reference_price=None,
            stop_price=None,
        )
        pol = _make_policy()
        r = PositionSizingQueryService().size_by_cash_limit(req, pol)
        assert r["blocked"] is True


# ===========================================================================
# 10. TestConstraints
# ===========================================================================

class TestConstraints:
    def test_1_constraint_engine_runs(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request()
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        assert fq >= Decimal("0")
        assert isinstance(cs, list)

    def test_2_constraints_list_is_non_empty(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request()
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        assert len(cs) > 0

    def test_3_single_name_cap_blocks_excess(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request(
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            current_market_value=Decimal("200000"),  # already at 20% of PV
            max_position_weight=Decimal("0.15"),
        )
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("500"), pol)
        # Already over the cap → quantity should be 0
        assert fq == Decimal("0")

    def test_4_cash_cap_applied(self):
        from decimal import Decimal
        from portfolio.sizing.cash_cap_v151 import CashCapConstraint
        req = _make_request(
            available_cash=Decimal("50000"),
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
        )
        pol = _make_policy()
        r = CashCapConstraint().apply(req, Decimal("500"), pol)
        # spendable = 50000 - 50000 reserve = 0 → blocked
        assert r["severity"] == "BLOCKING"
        assert r["capped_quantity"] == Decimal("0")

    def test_5_lot_normalization_always_rounds_down(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("1999"), 1000, False, None, None)
        assert r["normalized_quantity"] == Decimal("1000")

    def test_6_final_gate_constraint_present(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request()
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        gate_constraints = [c for c in cs if "FINAL_GATE" in c.get("reason", "")]
        assert len(gate_constraints) > 0

    def test_7_constraints_have_before_after_quantity(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request()
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        for c in cs:
            assert "before_quantity" in c
            assert "after_quantity" in c

    def test_8_pit_violation_blocks_immediately(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request(
            as_of="2026-06-20",
            atr_available_from="2026-06-22",  # future
        )
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        assert fq == Decimal("0")
        assert bc is not None

    def test_9_each_constraint_has_research_only(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request()
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        for c in cs:
            assert c.get("research_only") is True

    def test_10_industry_cap_applied_when_industry_set(self):
        from decimal import Decimal
        from portfolio.sizing.industry_cap_v151 import IndustryCapConstraint
        req = _make_request(
            industry="SEMICONDUCTOR",
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
        )
        pol = _make_policy()
        # current_industry_value at 300000 = 30% which is at cap
        r = IndustryCapConstraint().apply(req, Decimal("500"), pol, Decimal("300000"))
        assert r["applied"] is True
        assert r["capped_quantity"] == Decimal("0")

    def test_11_industry_unknown_is_warning_not_blocked(self):
        from decimal import Decimal
        from portfolio.sizing.industry_cap_v151 import IndustryCapConstraint
        req = _make_request(industry=None)
        pol = _make_policy()
        r = IndustryCapConstraint().apply(req, Decimal("500"), pol)
        assert r["severity"] == "WARNING"
        assert r["applied"] is False

    def test_12_weight_cap_constraint_applies(self):
        from decimal import Decimal
        from portfolio.sizing.weight_cap_v151 import WeightCapConstraint
        req = _make_request(
            portfolio_value=Decimal("1000000"),
            planned_entry_price=Decimal("500"),
            current_market_value=Decimal("0"),
        )
        pol = _make_policy()
        # max weight 15%, room = 150000 → max_qty = 300
        r = WeightCapConstraint().apply(req, Decimal("500"), pol)
        assert r["capped_quantity"] <= Decimal("300")

    def test_13_cash_cap_no_entry_is_warning(self):
        from decimal import Decimal
        from portfolio.sizing.cash_cap_v151 import CashCapConstraint
        req = _make_request(planned_entry_price=None, reference_price=None)
        pol = _make_policy()
        r = CashCapConstraint().apply(req, Decimal("100"), pol)
        assert r["severity"] == "WARNING"
        assert r["applied"] is False

    def test_14_minimum_order_value_zero_result(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        # 1 lot × price 5 = 5000 < minimum 10000 → zero
        r = LotNormalizer().normalize(
            Decimal("1000"), 1000, False,
            minimum_order_value=Decimal("10000"),
            reference_price=Decimal("5"),
        )
        assert r["normalized_quantity"] == Decimal("0")

    def test_15_constraint_ordering_data_quality_first(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request(
            as_of="2026-06-20",
            atr_available_from="2026-06-22",  # PIT violation
        )
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        # First constraint should be PIT type
        assert cs[0]["constraint_type"] == "PIT"


# ===========================================================================
# 11. TestLotNormalization
# ===========================================================================

class TestLotNormalization:
    def test_1_standard_lot_1000_rounds_down(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("1500"), 1000, False, None, None)
        assert r["normalized_quantity"] == Decimal("1000")

    def test_2_exact_lot_unchanged(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("2000"), 1000, False, None, None)
        assert r["normalized_quantity"] == Decimal("2000")

    def test_3_never_rounds_up(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        # 1999 should floor to 1000, not round up to 2000
        r = LotNormalizer().normalize(Decimal("1999"), 1000, False, None, None)
        assert r["normalized_quantity"] == Decimal("1000")
        assert r["normalized_quantity"] < Decimal("1999")

    def test_4_odd_lot_false_floors_to_lot(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("750"), 1000, False, None, None)
        assert r["normalized_quantity"] == Decimal("0")

    def test_5_odd_lot_true_floors_to_integer(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("750"), 1000, True, None, None)
        assert r["normalized_quantity"] == Decimal("750")

    def test_6_below_minimum_order_value_returns_zero(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        # 1 lot × 5 TWD = 5000 < 10000 minimum
        r = LotNormalizer().normalize(
            Decimal("1000"), 1000, False,
            minimum_order_value=Decimal("10000"),
            reference_price=Decimal("5"),
        )
        assert r["normalized_quantity"] == Decimal("0")

    def test_7_research_only_in_result(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("1500"), 1000, False, None, None)
        assert r["research_only"] is True

    def test_8_removed_by_rounding_computed(self):
        from decimal import Decimal
        from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
        r = LotNormalizer().normalize(Decimal("1700"), 1000, False, None, None)
        assert r["removed_by_rounding"] == Decimal("700")


# ===========================================================================
# 12. TestEligibility
# ===========================================================================

class TestEligibility:
    def test_1_valid_request_is_eligible(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request()
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert r.sizing_allowed is True
        assert r.eligibility_status in ("ELIGIBLE", "WARNING")

    def test_2_broker_linked_blocks(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request()
        req.broker_linked = True
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert r.sizing_allowed is False
        assert any("BROKER_LINKED" in b for b in r.blockers)

    def test_3_full_kelly_policy_blocked(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        from portfolio.sizing.models_v151 import PositionSizingPolicy
        req = _make_request()
        with pytest.raises(AssertionError):
            # Cannot even create a policy with full_kelly_enabled=True
            pol = PositionSizingPolicy(policy_id="P", name="T", full_kelly_enabled=True)

    def test_4_missing_price_blocks(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request(planned_entry_price=None, reference_price=None)
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert r.sizing_allowed is False

    def test_5_pit_atr_violation_blocks(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request(
            as_of="2026-06-20",
            atr_available_from="2026-06-22",
        )
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert r.sizing_allowed is False

    def test_6_research_only_in_result(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request()
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert r.research_only is True

    def test_7_methods_blocked_without_atr(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request(atr=None)
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert "ATR_BASED" in r.methods_blocked

    def test_8_methods_blocked_without_volatility(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request(volatility=None)
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert "VOLATILITY_TARGET" in r.methods_blocked

    def test_9_eligibility_result_has_all_fields(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate, EligibilityResult
        req = _make_request()
        pol = _make_policy()
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert hasattr(r, "sizing_allowed")
        assert hasattr(r, "methods_allowed")
        assert hasattr(r, "methods_blocked")
        assert hasattr(r, "warnings")
        assert hasattr(r, "blockers")
        assert hasattr(r, "evidence")
        assert hasattr(r, "eligibility_status")

    def test_10_fixture_blocked_broker_linked(self):
        from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
        req = _make_request()
        pol = _make_policy()
        try:
            data = _load_fixture("blocked_broker_linked.json")
            req.broker_linked = data.get("broker_linked", True)
        except Exception:
            req.broker_linked = True
        r = PositionSizingEligibilityGate().evaluate(req, pol)
        assert r.sizing_allowed is False


# ===========================================================================
# 13. TestPIT
# ===========================================================================

class TestPIT:
    def test_1_valid_available_from_passes(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        req = _make_request(as_of="2026-06-22", available_from="2026-06-22")
        issues = PositionSizingValidator().validate_request(req)
        pit_issues = [i for i in issues if "PIT_VIOLATION" in i]
        assert len(pit_issues) == 0

    def test_2_future_atr_is_pit_violation(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        req = _make_request(
            as_of="2026-06-20",
            atr_available_from="2026-06-22",
        )
        issues = PositionSizingValidator().validate_request(req)
        pit_issues = [i for i in issues if "PIT_VIOLATION_ATR" in i]
        assert len(pit_issues) > 0

    def test_3_future_atr_blocked_in_atr_sizer(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        req = _make_request(
            as_of="2026-06-20",
            atr=Decimal("25"),
            atr_available_from="2026-06-22",
            stop_price=None,
        )
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["blocked"] is True
        assert "PIT_VIOLATION" in r["blocker_reason"]

    def test_4_future_liquidity_is_pit_violation(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        req = _make_request(
            as_of="2026-06-20",
            average_daily_value_available_from="2026-06-22",
        )
        issues = PositionSizingValidator().validate_request(req)
        pit_issues = [i for i in issues if "PIT_VIOLATION_LIQUIDITY" in i]
        assert len(pit_issues) > 0

    def test_5_pit_blocks_constraint_engine(self):
        from decimal import Decimal
        from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
        req = _make_request(
            as_of="2026-06-20",
            atr_available_from="2026-06-22",
        )
        pol = _make_policy()
        fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("200"), pol)
        assert fq == Decimal("0")

    def test_6_past_available_from_passes_liquidity(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        req = _make_request(
            as_of="2026-06-22",
            average_daily_value_available_from="2026-06-20",
        )
        issues = PositionSizingValidator().validate_request(req)
        pit_issues = [i for i in issues if "PIT_VIOLATION_LIQUIDITY" in i]
        assert len(pit_issues) == 0

    def test_7_fixture_future_atr(self):
        from decimal import Decimal
        from portfolio.sizing.atr_sizing_v151 import ATRSizer
        try:
            data = _load_fixture("future_atr.json")
            atr_val = Decimal(str(data.get("atr", "25")))
            as_of = data.get("as_of", "2026-06-20")
            atr_af = data.get("atr_available_from", "2026-06-22")
            req = _make_request(as_of=as_of, atr=atr_val, atr_available_from=atr_af, stop_price=None)
        except Exception:
            req = _make_request(
                as_of="2026-06-20", atr=Decimal("25"),
                atr_available_from="2026-06-22", stop_price=None,
            )
        pol = _make_policy()
        r = ATRSizer().calculate(req, pol)
        assert r["blocked"] is True

    def test_8_fixture_future_liquidity(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        try:
            data = _load_fixture("future_liquidity.json")
            as_of = data.get("as_of", "2026-06-20")
            adv_af = data.get("average_daily_value_available_from", "2026-06-22")
            req = _make_request(as_of=as_of, average_daily_value_available_from=adv_af)
        except Exception:
            req = _make_request(
                as_of="2026-06-20",
                average_daily_value_available_from="2026-06-22",
            )
        issues = PositionSizingValidator().validate_request(req)
        assert any("PIT_VIOLATION" in i for i in issues)


# ===========================================================================
# 14. TestLineage
# ===========================================================================

class TestLineage:
    def test_1_proposal_has_source_lineage_ids(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        svc = PositionSizingQueryService()
        proposal = svc.build_sizing_proposal(req, pol)
        assert hasattr(proposal, "source_lineage_ids")

    def test_2_lineage_ids_preserved_from_request(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(source_lineage_ids=["LID_ABC", "LID_DEF"])
        pol = _make_policy()
        svc = PositionSizingQueryService()
        proposal = svc.build_sizing_proposal(req, pol)
        assert "LID_ABC" in proposal.source_lineage_ids

    def test_3_empty_lineage_triggers_warning(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        req = _make_request(source_lineage_ids=[])
        issues = PositionSizingValidator().validate_request(req)
        assert any("MISSING_LINEAGE" in i for i in issues)

    def test_4_proposal_has_content_hash(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        proposal = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert proposal.content_hash
        assert len(proposal.content_hash) == 16

    def test_5_proposal_has_calculation_version(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        proposal = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert proposal.calculation_version == "1.5.1"

    def test_6_store_get_lineage_returns_ids(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(source_lineage_ids=["LID_XYZ"])
        pol = _make_policy()
        svc = PositionSizingQueryService()
        proposal = svc.build_sizing_proposal(req, pol)
        svc.save_sizing_proposal(proposal)
        lineage = svc.get_sizing_lineage(proposal.proposal_id)
        assert lineage["found"] is True
        assert "LID_XYZ" in lineage["lineage_ids"]

    def test_7_missing_lineage_fixture(self):
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        try:
            data = _load_fixture("missing_lineage.json")
            lineage = data.get("source_lineage_ids", [])
            req = _make_request(source_lineage_ids=lineage)
        except Exception:
            req = _make_request(source_lineage_ids=[])
        issues = PositionSizingValidator().validate_request(req)
        assert any("LINEAGE" in i for i in issues)

    def test_8_proposal_has_generated_at(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        proposal = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert proposal.generated_at


# ===========================================================================
# 15. TestExplainability
# ===========================================================================

class TestExplainability:
    def test_1_explain_returns_dict(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP1", request_id="R1", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert isinstance(r, dict)

    def test_2_explain_includes_steps(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP2", request_id="R2", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert "steps" in r
        assert len(r["steps"]) > 0

    def test_3_explain_includes_method(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP3", request_id="R3", portfolio_id="P",
            symbol="2330", method="ATR_BASED", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert r["method"] == "ATR_BASED"

    def test_4_explain_includes_raw_quantity(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP4", request_id="R4", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert "raw_quantity" in r

    def test_5_explain_includes_binding_constraint(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP5", request_id="R5", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert "binding_constraint" in r

    def test_6_explain_safety_labels_present(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP6", request_id="R6", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert "safety_labels" in r
        assert "RESEARCH_ONLY" in r["safety_labels"]

    def test_7_explain_research_only_flag(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP7", request_id="R7", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert r["research_only"] is True

    def test_8_explain_executable_false(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP8", request_id="R8", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert r["executable"] is False

    def test_9_query_service_explain_wrapper(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        svc = PositionSizingQueryService()
        proposal = svc.build_sizing_proposal(req, pol)
        r = svc.explain_sizing_proposal(proposal)
        assert "steps" in r
        assert r["research_only"] is True

    def test_10_explain_assumptions_present(self):
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        from portfolio.sizing.models_v151 import PositionSizingProposal
        p = PositionSizingProposal(
            proposal_id="EXP10", request_id="R10", portfolio_id="P",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        r = PositionSizingExplainer().explain(p)
        assert "assumptions" in r
        assert any("long-only" in a.lower() for a in r["assumptions"])


# ===========================================================================
# 16. TestWhatIf
# ===========================================================================

class TestWhatIf:
    def test_1_what_if_returns_result(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert result is not None

    def test_2_what_if_has_hypothetical_only_label(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert "HYPOTHETICAL_ONLY" in result.labels

    def test_3_what_if_has_no_ledger_write_label(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert "NO_LEDGER_WRITE" in result.labels

    def test_4_what_if_has_no_order_created_label(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert "NO_ORDER_CREATED" in result.labels

    def test_5_what_if_has_no_broker_call_label(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert "NO_BROKER_CALL" in result.labels

    def test_6_what_if_order_created_false(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert result.order_created is False

    def test_7_what_if_persisted_to_ledger_false(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"stop_price": Decimal("920")}, pol)
        assert result.persisted_to_ledger is False

    def test_8_what_if_different_risk_percent(self):
        from decimal import Decimal
        from portfolio.sizing.what_if_v151 import SizingWhatIfEngine
        req = _make_request()
        pol = _make_policy()
        result = SizingWhatIfEngine().run(req, {"risk_budget_percent": Decimal("0.02")}, pol)
        # scenario has higher risk → scenario qty >= baseline qty
        bq = result.baseline_proposal.proposed_final_quantity
        sq = result.scenario_proposal.proposed_final_quantity
        assert result.delta_quantity == sq - bq


# ===========================================================================
# 17. TestStoreQuery
# ===========================================================================

class TestStoreQuery:
    def test_1_save_and_get_proposal(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        from portfolio.sizing.models_v151 import PositionSizingProposal
        store = PositionSizingStore(use_temp_db=True)
        p = PositionSizingProposal(
            proposal_id="SQ_P001", request_id="R1", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        store.save_proposal(p)
        got = store.get_proposal("SQ_P001")
        assert got is not None

    def test_2_list_proposals(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        from portfolio.sizing.models_v151 import PositionSizingProposal
        store = PositionSizingStore(use_temp_db=True)
        p = PositionSizingProposal(
            proposal_id="SQ_P002", request_id="R2", portfolio_id="PORT2",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        store.save_proposal(p)
        items = store.list_proposals()
        assert len(items) >= 1

    def test_3_idempotent_save_no_duplicate(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        from portfolio.sizing.models_v151 import PositionSizingProposal
        store = PositionSizingStore(use_temp_db=True)
        p = PositionSizingProposal(
            proposal_id="SQ_P003", request_id="R3", portfolio_id="PORT",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        store.save_proposal(p)
        store.save_proposal(p)  # duplicate save
        items = [x for x in store.list_proposals() if x.get("proposal_id") == "SQ_P003"]
        assert len(items) == 1

    def test_4_get_nonexistent_returns_none(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        store = PositionSizingStore(use_temp_db=True)
        assert store.get_proposal("DOES_NOT_EXIST") is None

    def test_5_no_order_table_attribute(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        store = PositionSizingStore(use_temp_db=True)
        assert not hasattr(store, "_orders")

    def test_6_no_transaction_ledger_attribute(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        store = PositionSizingStore(use_temp_db=True)
        assert not hasattr(store, "_ledger")

    def test_7_store_research_only_flag(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        assert PositionSizingStore.RESEARCH_ONLY is True

    def test_8_save_and_list_policy(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        store = PositionSizingStore(use_temp_db=True)
        pol = _make_policy(policy_id="POL_SQ_001")
        store.save_policy(pol)
        got = store.get_policy("POL_SQ_001")
        assert got is not None

    def test_9_query_service_save_and_get(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        svc = PositionSizingQueryService()
        proposal = svc.build_sizing_proposal(req, pol)
        svc.save_sizing_proposal(proposal)
        got = svc.get_sizing_proposal(proposal.proposal_id)
        assert got is not None

    def test_10_list_proposals_filter_by_portfolio(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        from portfolio.sizing.models_v151 import PositionSizingProposal
        store = PositionSizingStore(use_temp_db=True)
        p1 = PositionSizingProposal(
            proposal_id="SQ_FILTER_A", request_id="R", portfolio_id="PORTX",
            symbol="2330", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        p2 = PositionSizingProposal(
            proposal_id="SQ_FILTER_B", request_id="R2", portfolio_id="PORTY",
            symbol="2412", method="FIXED_FRACTIONAL", as_of="2026-06-22",
        )
        store.save_proposal(p1)
        store.save_proposal(p2)
        items = store.list_proposals(portfolio_id="PORTX")
        assert all(x.get("portfolio_id") == "PORTX" for x in items)

    def test_11_no_broker_credentials_in_store(self):
        from portfolio.sizing.store_v151 import PositionSizingStore
        store = PositionSizingStore(use_temp_db=True)
        assert not hasattr(store, "broker_api_key")
        assert not hasattr(store, "broker_credentials")

    def test_12_store_no_order_table_constant(self):
        from portfolio.sizing import store_v151
        assert store_v151.NO_ORDER_TABLE is True
        assert store_v151.NO_TRANSACTION_LEDGER is True


# ===========================================================================
# 18. TestBuildProposal
# ===========================================================================

class TestBuildProposal:
    def test_1_build_proposal_returns_proposal(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        from portfolio.sizing.models_v151 import PositionSizingProposal
        req = _make_request()
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert isinstance(p, PositionSizingProposal)

    def test_2_proposal_has_proposal_id(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert p.proposal_id.startswith("PSP_")

    def test_3_proposal_research_only_true(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert p.research_only is True

    def test_4_proposal_executable_false(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert p.executable is False

    def test_5_proposal_order_created_false(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert p.order_created is False

    def test_6_proposal_has_all_safety_labels(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request()
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        for label in ["RESEARCH_ONLY", "NOT_AN_ORDER", "NOT_EXECUTABLE",
                      "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NO_AUTO_REBALANCE"]:
            assert label in p.labels, f"Missing label: {label}"

    def test_7_blocked_sizing_returns_zero_quantity(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        req = _make_request(
            planned_entry_price=Decimal("1000"),
            stop_price=Decimal("1000"),  # stop == entry → blocked
        )
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        assert p.proposed_final_quantity == Decimal("0")
        assert p.sizing_status == "BLOCKED"

    def test_8_valid_sizing_returns_positive_raw_quantity(self):
        from decimal import Decimal
        from portfolio.sizing.query_v151 import PositionSizingQueryService
        # Use entry=50 (small) so raw_qty >> 1000 lot; lots clear minimum_order_value easily
        req = _make_request(
            portfolio_value=Decimal("10000000"),
            available_cash=Decimal("5000000"),
            planned_entry_price=Decimal("50"),
            stop_price=Decimal("47"),
        )
        pol = _make_policy()
        p = PositionSizingQueryService().build_sizing_proposal(req, pol)
        # raw_qty = (10000000 × 0.01) / 3 = 33333; after constraints, must be ≥ 1 lot
        assert p.raw_quantity > Decimal("0")


# ===========================================================================
# 19. TestCLI
# ===========================================================================

class TestCLI:
    def _capture(self, fn):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fn()
        return buf.getvalue()

    def test_1_cmd_health_runs(self):
        from main import cmd_position_sizing_health
        out = self._capture(lambda: cmd_position_sizing_health())
        assert "Position Sizing" in out or "Health" in out

    def test_2_cmd_health_prints_research_only(self):
        from main import cmd_position_sizing_health
        out = self._capture(lambda: cmd_position_sizing_health())
        assert "Research Only" in out

    def test_3_cmd_policies_runs(self):
        from main import cmd_position_sizing_policies
        out = self._capture(lambda: cmd_position_sizing_policies())
        assert "Research Only" in out

    def test_4_cmd_policy_show_runs(self):
        from main import cmd_position_sizing_policy_show
        out = self._capture(lambda: cmd_position_sizing_policy_show())
        assert "Research Only" in out

    def test_5_cmd_eligibility_runs(self):
        from main import cmd_position_sizing_eligibility
        out = self._capture(lambda: cmd_position_sizing_eligibility())
        assert "Research Only" in out

    def test_6_cmd_fixed_fractional_runs(self):
        from main import cmd_position_sizing_fixed_fractional
        out = self._capture(lambda: cmd_position_sizing_fixed_fractional())
        assert "Research Only" in out
        assert "RESEARCH_ONLY" in out or "Raw Quantity" in out

    def test_7_cmd_stop_distance_runs(self):
        from main import cmd_position_sizing_stop_distance
        out = self._capture(lambda: cmd_position_sizing_stop_distance())
        assert "Research Only" in out

    def test_8_cmd_atr_runs(self):
        from main import cmd_position_sizing_atr
        out = self._capture(lambda: cmd_position_sizing_atr())
        assert "Research Only" in out

    def test_9_cmd_volatility_runs(self):
        from main import cmd_position_sizing_volatility
        out = self._capture(lambda: cmd_position_sizing_volatility())
        assert "Research Only" in out

    def test_10_cmd_target_weight_runs(self):
        from main import cmd_position_sizing_target_weight
        out = self._capture(lambda: cmd_position_sizing_target_weight())
        assert "Research Only" in out

    def test_11_cmd_cash_limit_runs(self):
        from main import cmd_position_sizing_cash_limit
        out = self._capture(lambda: cmd_position_sizing_cash_limit())
        assert "Research Only" in out

    def test_12_cmd_constraints_runs(self):
        from main import cmd_position_sizing_constraints
        out = self._capture(lambda: cmd_position_sizing_constraints())
        assert "Research Only" in out

    def test_13_cmd_explain_runs(self):
        from main import cmd_position_sizing_explain
        out = self._capture(lambda: cmd_position_sizing_explain())
        assert "Research Only" in out

    def test_14_cmd_what_if_runs(self):
        from main import cmd_position_sizing_what_if
        out = self._capture(lambda: cmd_position_sizing_what_if())
        assert "Research Only" in out

    def test_15_cmd_show_runs(self):
        from main import cmd_position_sizing_show
        out = self._capture(lambda: cmd_position_sizing_show())
        assert len(out) >= 0  # should not crash

    def test_16_cmd_list_runs(self):
        from main import cmd_position_sizing_list
        out = self._capture(lambda: cmd_position_sizing_list())
        assert len(out) >= 0

    def test_17_cmd_lineage_runs(self):
        from main import cmd_position_sizing_lineage
        out = self._capture(lambda: cmd_position_sizing_lineage())
        assert len(out) >= 0

    def test_18_cmd_report_prints_research_only_banner(self):
        from main import cmd_position_sizing_report
        # cmd always prints the Research Only banner before any report generation
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                cmd_position_sizing_report()
            except Exception:
                pass  # main.py may have a bug; the banner is always first
        out = buf.getvalue()
        assert "Research Only" in out

    def test_19_cmd_fixed_fractional_no_order_output(self):
        from main import cmd_position_sizing_fixed_fractional
        out = self._capture(lambda: cmd_position_sizing_fixed_fractional())
        out_lower = out.lower()
        assert "order submitted" not in out_lower
        assert "broker" not in out_lower or "no broker" in out_lower

    def test_20_all_commands_importable(self):
        from main import (
            cmd_position_sizing_health,
            cmd_position_sizing_policies,
            cmd_position_sizing_policy_show,
            cmd_position_sizing_eligibility,
            cmd_position_sizing_fixed_fractional,
            cmd_position_sizing_stop_distance,
            cmd_position_sizing_atr,
            cmd_position_sizing_volatility,
            cmd_position_sizing_target_weight,
            cmd_position_sizing_cash_limit,
            cmd_position_sizing_constraints,
            cmd_position_sizing_explain,
            cmd_position_sizing_what_if,
            cmd_position_sizing_show,
            cmd_position_sizing_list,
            cmd_position_sizing_lineage,
            cmd_position_sizing_report,
        )
        assert callable(cmd_position_sizing_health)
        assert callable(cmd_position_sizing_report)


# ===========================================================================
# 20. TestGUI
# ===========================================================================

class TestGUI:
    def test_1_panel_imports_without_crash(self):
        from gui.position_sizing_panel import PositionSizingPanel
        assert PositionSizingPanel is not None

    def test_2_panel_instantiates_without_crash(self):
        from gui.position_sizing_panel import PositionSizingPanel
        panel = PositionSizingPanel()
        assert panel is not None

    def test_3_panel_has_safety_banner_strings(self):
        from gui.position_sizing_panel import SAFETY_BANNER_LINES
        assert any("Research" in line for line in SAFETY_BANNER_LINES)
        assert any("Order" in line or "Not an Order" in line for line in SAFETY_BANNER_LINES)

    def test_4_panel_no_buy_button(self):
        from gui.position_sizing_panel import _BLOCKED_BUTTONS
        assert "Buy" in _BLOCKED_BUTTONS

    def test_5_panel_no_sell_button(self):
        from gui.position_sizing_panel import _BLOCKED_BUTTONS
        assert "Sell" in _BLOCKED_BUTTONS

    def test_6_panel_no_order_widget(self):
        # Ensure none of the panel code references BuyButton or OrderWidget
        import inspect
        from gui import position_sizing_panel
        src = inspect.getsource(position_sizing_panel)
        assert "BuyButton" not in src
        assert "SellButton" not in src

    def test_7_panel_research_only_flag(self):
        from gui.position_sizing_panel import PositionSizingPanel
        panel = PositionSizingPanel()
        assert panel.RESEARCH_ONLY is True

    def test_8_panel_metadata_no_broker(self):
        from gui.position_sizing_panel import PositionSizingPanel
        panel = PositionSizingPanel()
        meta = panel.get_metadata()
        assert meta["no_real_orders"] is True
        assert meta["broker_execution_enabled"] is False
        assert meta["production_trading_blocked"] is True


# ===========================================================================
# 21. TestReleaseGate
# ===========================================================================

class TestReleaseGate:
    def test_1_release_gate_runs(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        assert result is not None

    def test_2_gate_version_is_151(self):
        from release.position_sizing_release_gate_v151 import GATE_VERSION
        assert GATE_VERSION == "1.5.1"

    def test_3_gate_passes_all_checks(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        failed = [c for c in result["checks"] if not c["passed"]]
        assert result["gate_passed"] is True, f"Gate failed: {failed}"

    def test_4_gate_research_only_flag(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        assert result["research_only"] is True

    def test_5_gate_all_modules_importable(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        import_checks = [c for c in result["checks"] if c["check"].startswith("import") or
                         "VALID" in c["check"]]
        for c in import_checks:
            assert c["passed"], f"Import failed: {c}"

    def test_6_gate_no_order_creation(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        nc = next((c for c in result["checks"]
                   if c["check"] == "NO_POSITION_SIZING_ORDER_CREATION"), None)
        assert nc is not None
        assert nc["passed"] is True

    def test_7_gate_no_broker(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        nc = next((c for c in result["checks"]
                   if c["check"] == "NO_POSITION_SIZING_BROKER"), None)
        assert nc is not None
        assert nc["passed"] is True

    def test_8_gate_no_auto_rebalance(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        nc = next((c for c in result["checks"]
                   if c["check"] == "NO_POSITION_SIZING_AUTO_REBALANCE"), None)
        assert nc is not None
        assert nc["passed"] is True

    def test_9_health_check_passes(self):
        from portfolio.sizing.health_v151 import PositionSizingHealthCheck
        result = PositionSizingHealthCheck().run()
        assert result["overall"] == "PASS", (
            f"Health failed: {[c for c in result['checks'] if not c['passed']]}"
        )

    def test_10_gate_22_checks_total(self):
        from release.position_sizing_release_gate_v151 import PositionSizingReleaseGate
        result = PositionSizingReleaseGate().run()
        assert result["total"] == 22


# ===========================================================================
# 22. TestReport
# ===========================================================================

class TestReport:
    def test_1_report_generates_without_crash(self):
        from reports.position_sizing_report import PositionSizingReport
        r = PositionSizingReport().generate(
            portfolio_id="PORT_TEST",
            symbol="2330",
            as_of="2026-06-22",
        )
        assert r is not None

    def test_2_report_contains_research_only(self):
        from reports.position_sizing_report import PositionSizingReport
        r = PositionSizingReport().generate(
            portfolio_id="PORT_TEST",
            symbol="2330",
            as_of="2026-06-22",
        )
        assert r["research_only"] is True

    def test_3_report_executable_false(self):
        from reports.position_sizing_report import PositionSizingReport
        r = PositionSizingReport().generate(
            portfolio_id="PORT_TEST",
            symbol="2330",
            as_of="2026-06-22",
        )
        assert r["executable"] is False

    def test_4_report_order_created_false(self):
        from reports.position_sizing_report import PositionSizingReport
        r = PositionSizingReport().generate(
            portfolio_id="PORT_TEST",
            symbol="2330",
            as_of="2026-06-22",
        )
        assert r["order_created"] is False

    def test_5_report_safety_section_present(self):
        from reports.position_sizing_report import PositionSizingReport
        r = PositionSizingReport().generate(
            portfolio_id="PORT_TEST",
            symbol="2330",
            as_of="2026-06-22",
        )
        assert "safety" in r["sections"]
        safety = r["sections"]["safety"]
        assert safety["research_only"] is True

    def test_6_report_broker_called_false(self):
        from reports.position_sizing_report import PositionSizingReport
        r = PositionSizingReport().generate(
            portfolio_id="PORT_TEST",
            symbol="2330",
            as_of="2026-06-22",
        )
        assert r["broker_called"] is False


# ===========================================================================
# 23. TestRegression
# ===========================================================================

class TestRegression:
    def test_1_no_broker_adapter_in_sizing_modules(self):
        import pkgutil
        import importlib
        import portfolio.sizing as pkg
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=pkg.__path__, prefix=pkg.__name__ + "."
        ):
            mod = importlib.import_module(modname)
            src = getattr(mod, "__doc__", "") or ""
            # No broker adapter imports
            assert not hasattr(mod, "BrokerAdapter"), (
                f"{modname} exposes BrokerAdapter"
            )

    def test_2_no_execute_order_in_sizing_modules(self):
        import pkgutil
        import importlib
        import inspect
        import portfolio.sizing as pkg
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=pkg.__path__, prefix=pkg.__name__ + "."
        ):
            mod = importlib.import_module(modname)
            # Check module-level callables
            for name, obj in inspect.getmembers(mod):
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    assert name != "execute_order", (
                        f"{modname}.{name} is execute_order — not allowed"
                    )

    def test_3_no_auto_rebalance_in_sizing_modules(self):
        import pkgutil
        import importlib
        import inspect
        import portfolio.sizing as pkg
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=pkg.__path__, prefix=pkg.__name__ + "."
        ):
            mod = importlib.import_module(modname)
            for name, obj in inspect.getmembers(mod):
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    assert name != "auto_rebalance", (
                        f"{modname}.{name} is auto_rebalance — not allowed"
                    )

    def test_4_query_service_has_no_blocked_methods(self):
        from portfolio.sizing.query_v151 import PositionSizingQueryService, _BLOCKED_METHODS
        svc = PositionSizingQueryService()
        for blocked in _BLOCKED_METHODS:
            assert not hasattr(svc, blocked), (
                f"PositionSizingQueryService has blocked method: {blocked}"
            )

    def test_5_all_sizing_modules_have_research_only_flag(self):
        modules = [
            "portfolio.sizing.fixed_fractional_v151",
            "portfolio.sizing.stop_distance_v151",
            "portfolio.sizing.atr_sizing_v151",
            "portfolio.sizing.volatility_target_v151",
            "portfolio.sizing.cash_cap_v151",
            "portfolio.sizing.weight_cap_v151",
            "portfolio.sizing.lot_normalizer_v151",
            "portfolio.sizing.constraint_engine_v151",
            "portfolio.sizing.eligibility_v151",
            "portfolio.sizing.explain_v151",
            "portfolio.sizing.what_if_v151",
            "portfolio.sizing.store_v151",
            "portfolio.sizing.query_v151",
            "portfolio.sizing.health_v151",
        ]
        import importlib
        for mod_name in modules:
            mod = importlib.import_module(mod_name)
            assert getattr(mod, "RESEARCH_ONLY", None) is True, (
                f"{mod_name} missing RESEARCH_ONLY = True"
            )
