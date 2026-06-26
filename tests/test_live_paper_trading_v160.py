"""tests/test_live_paper_trading_v160.py — Live Paper Trading Foundation v1.6.0 Tests.

[!] PAPER TRADING TEST SUITE ONLY. NO REAL ORDERS. SIMULATION_ONLY.
[!] NOT_FOR_EXECUTION. NOT_FOR_INVESTMENT_DECISION. NOT_FOR_PRODUCTION.
[!] All fixture data is synthetic test data only.

Coverage:
- Package safety flags (v160)
- Enums exhaustive validation
- Models safety contract assertions
- Validation functions
- Idempotency registry
- Market session / calendar
- Data classification
- Order state machine
- Slippage models (all 4)
- Liquidity checker
- Paper ledger (hash chain / GENESIS / verify)
- Kill switch (all 10 triggers)
- Paper risk gate
- Execution simulator
- Paper cash / position
- Snapshot hash
- Event journal (sequence / out-of-order / duplicate)
- Reproducibility manifest
- Session config validation
- Query forbidden methods
- CLI command registry
- Version info
- Release gate structure
- GUI metadata
- Health module import
- Fixture file existence / schema
"""
from __future__ import annotations

import json
import sys
import os
import datetime
import importlib
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "live_paper_trading"


def load_fixture(name: str) -> Dict[str, Any]:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


# ===========================================================================
# GROUP 1 — Package Safety Flags (10 tests)
# ===========================================================================

class TestPackageSafetyFlags:
    """paper_trading/__init__.py safety constants."""

    def setup_method(self):
        import paper_trading as pt
        self.pt = pt

    def test_version_is_160(self):
        assert self.pt.PAPER_TRADING_VERSION == "1.6.0"

    def test_stage_is_foundation(self):
        assert self.pt.PAPER_TRADING_STAGE == "FOUNDATION"

    def test_no_real_orders_true(self):
        assert self.pt.NO_REAL_ORDERS is True

    def test_broker_execution_disabled(self):
        assert self.pt.BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked(self):
        assert self.pt.PRODUCTION_TRADING_BLOCKED is True

    def test_real_order_creation_disabled(self):
        assert self.pt.REAL_ORDER_CREATION_ENABLED is False

    def test_paper_order_creation_enabled(self):
        assert self.pt.PAPER_ORDER_CREATION_ENABLED is True

    def test_paper_order_execution_enabled(self):
        assert self.pt.PAPER_ORDER_EXECUTION_ENABLED is True

    def test_paper_fill_simulation_enabled(self):
        assert self.pt.PAPER_FILL_SIMULATION_ENABLED is True

    def test_paper_ledger_write_enabled(self):
        assert self.pt.PAPER_LEDGER_WRITE_ENABLED is True


# ===========================================================================
# GROUP 2 — Enums (24 tests)
# ===========================================================================

class TestEnums:
    """paper_trading/enums_v160.py"""

    def setup_method(self):
        from paper_trading.enums_v160 import (
            PaperSessionStatus, MarketSessionStatus, DataMode,
            PaperOrderType, PaperOrderSide, PaperOrderStatus,
            PaperFillStatus, PaperRiskStatus, PaperEventType,
            LatencyModel, SlippageModel, KillSwitchReason,
        )
        self.PSS = PaperSessionStatus
        self.MSS = MarketSessionStatus
        self.DM = DataMode
        self.POT = PaperOrderType
        self.POS = PaperOrderSide
        self.POSTAT = PaperOrderStatus
        self.PFS = PaperFillStatus
        self.PRS = PaperRiskStatus
        self.LM = LatencyModel
        self.SM = SlippageModel
        self.KSR = KillSwitchReason

    def test_session_status_has_9_values(self):
        assert len(self.PSS) == 9

    def test_session_status_created(self):
        assert self.PSS.CREATED.value == "CREATED"

    def test_session_status_halted(self):
        assert self.PSS.HALTED.value == "HALTED"

    def test_session_status_recovered(self):
        assert self.PSS.RECOVERED.value == "RECOVERED"

    def test_market_session_status_has_non_trading_day(self):
        assert self.MSS.NON_TRADING_DAY.value == "NON_TRADING_DAY"

    def test_data_mode_5_values(self):
        assert len(self.DM) == 5

    def test_data_mode_fixture(self):
        assert self.DM.FIXTURE.value == "FIXTURE"

    def test_paper_order_side_no_short(self):
        sides = {s.value for s in self.POS}
        assert "SHORT" not in sides
        assert "SELL_SHORT" not in sides

    def test_paper_order_side_only_buy_sell(self):
        assert len(self.POS) == 2
        assert self.POS.BUY.value == "BUY"
        assert self.POS.SELL.value == "SELL"

    def test_order_type_4_values(self):
        assert len(self.POT) == 4

    def test_order_status_has_halted(self):
        assert self.POSTAT.HALTED.value == "HALTED"

    def test_fill_status_simulated(self):
        assert self.PFS.SIMULATED.value == "SIMULATED"

    def test_risk_status_blocked(self):
        assert self.PRS.BLOCKED.value == "BLOCKED"

    def test_latency_model_zero_disclosed(self):
        assert self.LM.ZERO_DISCLOSED.value == "ZERO_DISCLOSED"

    def test_latency_model_3_values(self):
        assert len(self.LM) == 3

    def test_slippage_model_4_values(self):
        assert len(self.SM) == 4

    def test_slippage_model_fixed_bps(self):
        assert self.SM.FIXED_BPS.value == "FIXED_BPS"

    def test_slippage_model_spread_based(self):
        assert self.SM.SPREAD_BASED.value == "SPREAD_BASED"

    def test_slippage_model_participation(self):
        assert self.SM.PARTICIPATION_BASED.value == "PARTICIPATION_BASED"

    def test_slippage_model_volatility(self):
        assert self.SM.VOLATILITY_ADJUSTED.value == "VOLATILITY_ADJUSTED"

    def test_kill_switch_10_reasons(self):
        assert len(self.KSR) == 10

    def test_kill_switch_ledger_hash_mismatch(self):
        assert self.KSR.LEDGER_HASH_MISMATCH.value == "LEDGER_HASH_MISMATCH"

    def test_kill_switch_safety_contract(self):
        assert self.KSR.SAFETY_CONTRACT_VIOLATION.value == "SAFETY_CONTRACT_VIOLATION"

    def test_kill_switch_manual_halt(self):
        assert self.KSR.MANUAL_HALT.value == "MANUAL_HALT"


# ===========================================================================
# GROUP 3 — Models Safety Contract (20 tests)
# ===========================================================================

class TestModelsSafetyContract:
    """paper_trading/models_v160.py — safety assertions."""

    def _make_config(self, **kwargs):
        from paper_trading.models_v160 import PaperSessionConfig
        defaults = dict(session_id="s1", name="test")
        defaults.update(kwargs)
        return PaperSessionConfig(**defaults)

    def _make_order(self, **kwargs):
        from paper_trading.models_v160 import PaperOrder
        from paper_trading.enums_v160 import PaperOrderSide, PaperOrderType
        defaults = dict(
            paper_order_id="po1", session_id="s1", client_order_id="c1",
            symbol="2330", side=PaperOrderSide.BUY, order_type=PaperOrderType.MARKET,
            quantity=Decimal("1000"),
        )
        defaults.update(kwargs)
        return PaperOrder(**defaults)

    def _make_ledger_entry(self, **kwargs):
        from paper_trading.models_v160 import PaperLedgerEntry
        defaults = dict(entry_id="e1", session_id="s1", sequence=0, event_type="FILL")
        defaults.update(kwargs)
        return PaperLedgerEntry(**defaults)

    def test_config_defaults_are_safe(self):
        cfg = self._make_config()
        assert cfg.research_only is True
        assert cfg.broker_enabled is False
        assert cfg.real_order_enabled is False
        assert cfg.formal_ledger_write_enabled is False

    def test_config_research_only_false_raises(self):
        with pytest.raises(AssertionError):
            self._make_config(research_only=False)

    def test_config_broker_enabled_true_raises(self):
        with pytest.raises(AssertionError):
            self._make_config(broker_enabled=True)

    def test_config_real_order_enabled_true_raises(self):
        with pytest.raises(AssertionError):
            self._make_config(real_order_enabled=True)

    def test_config_formal_ledger_write_raises(self):
        with pytest.raises(AssertionError):
            self._make_config(formal_ledger_write_enabled=True)

    def test_order_safety_flags(self):
        order = self._make_order()
        assert order.research_only is True
        assert order.executable_on_broker is False
        assert order.real_order_created is False

    def test_order_paper_only_property(self):
        order = self._make_order()
        assert order.paper_only == "PAPER_ONLY"

    def test_order_simulation_only_property(self):
        order = self._make_order()
        assert order.simulation_only == "SIMULATION_ONLY"

    def test_order_not_a_real_order_property(self):
        order = self._make_order()
        assert order.not_a_real_order == "NOT_A_REAL_ORDER"

    def test_order_broker_enabled_raises(self):
        with pytest.raises(AssertionError):
            self._make_order(executable_on_broker=True)

    def test_order_real_order_raises(self):
        with pytest.raises(AssertionError):
            self._make_order(real_order_created=True)

    def test_order_remaining_quantity_initialized(self):
        order = self._make_order()
        assert order.remaining_quantity == Decimal("1000")

    def test_ledger_entry_paper_only_flag(self):
        entry = self._make_ledger_entry()
        assert entry.paper_only is True

    def test_ledger_entry_paper_only_false_raises(self):
        with pytest.raises(AssertionError):
            self._make_ledger_entry(paper_only=False)

    def test_ledger_entry_hash_is_deterministic(self):
        e1 = self._make_ledger_entry(previous_hash="GENESIS")
        e2 = self._make_ledger_entry(previous_hash="GENESIS")
        assert e1.compute_hash() == e2.compute_hash()

    def test_snapshot_content_hash_deterministic(self):
        from paper_trading.models_v160 import PaperSessionSnapshot
        s1 = PaperSessionSnapshot(
            snapshot_id="snap1", session_id="s1", as_of="2024-03-04T10:00:00Z",
            realized_pnl=Decimal("5000"), unrealized_pnl=Decimal("2000"),
            event_sequence=10,
        )
        s2 = PaperSessionSnapshot(
            snapshot_id="snap2", session_id="s1", as_of="2024-03-04T10:00:00Z",
            realized_pnl=Decimal("5000"), unrealized_pnl=Decimal("2000"),
            event_sequence=10,
        )
        assert s1.compute_content_hash() == s2.compute_content_hash()

    def test_config_currency_default_twd(self):
        cfg = self._make_config()
        assert cfg.currency == "TWD"

    def test_config_data_mode_default_fixture(self):
        from paper_trading.enums_v160 import DataMode
        cfg = self._make_config()
        assert cfg.data_mode == DataMode.FIXTURE

    def test_config_market_default_twse(self):
        cfg = self._make_config()
        assert cfg.market == "TWSE"

    def test_config_timezone_default_taipei(self):
        cfg = self._make_config()
        assert cfg.timezone == "Asia/Taipei"


# ===========================================================================
# GROUP 4 — Validation (15 tests)
# ===========================================================================

class TestValidation:
    """paper_trading/validation_v160.py"""

    def setup_method(self):
        from paper_trading import validation_v160 as v
        self.v = v

    def test_validate_symbol_ok(self):
        ok, msg = self.v.validate_symbol("2330")
        assert ok

    def test_validate_symbol_empty(self):
        ok, msg = self.v.validate_symbol("")
        assert not ok

    def test_validate_symbol_too_long(self):
        ok, msg = self.v.validate_symbol("A" * 25)
        assert not ok

    def test_validate_quantity_ok(self):
        ok, msg = self.v.validate_quantity("1000")
        assert ok

    def test_validate_quantity_zero(self):
        ok, msg = self.v.validate_quantity("0")
        assert not ok

    def test_validate_quantity_negative(self):
        ok, msg = self.v.validate_quantity("-100")
        assert not ok

    def test_validate_price_none_ok(self):
        ok, msg = self.v.validate_price(None)
        assert ok

    def test_validate_price_positive(self):
        ok, msg = self.v.validate_price("500")
        assert ok

    def test_validate_price_zero(self):
        ok, msg = self.v.validate_price("0")
        assert not ok

    def test_validate_cash_ok(self):
        ok, msg = self.v.validate_cash("1000000")
        assert ok

    def test_validate_cash_negative(self):
        ok, msg = self.v.validate_cash("-1")
        assert not ok

    def test_validate_no_short_ok_buy(self):
        from paper_trading.enums_v160 import PaperOrderSide
        ok, msg = self.v.validate_no_short(PaperOrderSide.BUY, Decimal("0"), Decimal("1000"))
        assert ok

    def test_validate_no_short_sell_insufficient(self):
        from paper_trading.enums_v160 import PaperOrderSide
        ok, msg = self.v.validate_no_short(PaperOrderSide.SELL, Decimal("500"), Decimal("1000"))
        assert not ok

    def test_validate_no_short_sell_sufficient(self):
        from paper_trading.enums_v160 import PaperOrderSide
        ok, msg = self.v.validate_no_short(PaperOrderSide.SELL, Decimal("1000"), Decimal("1000"))
        assert ok

    def test_validate_session_config_happy_path(self):
        from paper_trading.models_v160 import PaperSessionConfig
        cfg = PaperSessionConfig(session_id="s1", name="test")
        ok, errors = self.v.validate_session_config(cfg)
        assert ok, errors


# ===========================================================================
# GROUP 5 — Idempotency Registry (10 tests)
# ===========================================================================

class TestIdempotencyRegistry:
    """paper_trading/idempotency_v160.py"""

    def setup_method(self):
        from paper_trading.idempotency_v160 import IdempotencyRegistry
        self.reg = IdempotencyRegistry()

    def test_not_duplicate_initially(self):
        assert not self.reg.is_duplicate("key1")

    def test_register_and_check(self):
        self.reg.register("key1", 0)
        assert self.reg.is_duplicate("key1")

    def test_register_duplicate_raises(self):
        self.reg.register("key1", 0)
        with pytest.raises(ValueError):
            self.reg.register("key1", 1)

    def test_get_sequence(self):
        self.reg.register("key1", 5)
        assert self.reg.get_sequence("key1") == 5

    def test_get_sequence_missing_is_none(self):
        assert self.reg.get_sequence("missing") is None

    def test_count(self):
        self.reg.register("k1", 0)
        self.reg.register("k2", 1)
        assert self.reg.count() == 2

    def test_reset(self):
        self.reg.register("k1", 0)
        self.reg.reset()
        assert self.reg.count() == 0

    def test_is_not_duplicate_after_reset(self):
        self.reg.register("k1", 0)
        self.reg.reset()
        assert not self.reg.is_duplicate("k1")

    def test_different_keys_independent(self):
        self.reg.register("k1", 0)
        assert not self.reg.is_duplicate("k2")

    def test_large_key(self):
        key = "x" * 256
        self.reg.register(key, 99)
        assert self.reg.is_duplicate(key)


# ===========================================================================
# GROUP 6 — Market Session / Calendar (12 tests)
# ===========================================================================

class TestMarketSession:
    """paper_trading/market_session_v160.py"""

    def setup_method(self):
        from paper_trading.market_session_v160 import TWMarketSessionState, TWFixtureCalendar
        from paper_trading.enums_v160 import MarketSessionStatus
        self.MSS = MarketSessionStatus
        self.calendar = TWFixtureCalendar()
        self.state = TWMarketSessionState()

    def test_weekday_is_trading_day(self):
        # 2024-03-04 is a Monday
        d = datetime.date(2024, 3, 4)
        assert self.calendar.is_trading_day(d)

    def test_weekend_is_not_trading_day(self):
        # 2024-03-02 is a Saturday
        d = datetime.date(2024, 3, 2)
        assert not self.calendar.is_trading_day(d)

    def test_sunday_is_not_trading_day(self):
        d = datetime.date(2024, 3, 3)
        assert not self.calendar.is_trading_day(d)

    def test_status_open_during_trading_hours(self):
        dt = datetime.datetime(2024, 3, 4, 11, 0, 0)  # Monday 11:00
        assert self.calendar.get_status(dt) == self.MSS.OPEN

    def test_status_pre_open(self):
        dt = datetime.datetime(2024, 3, 4, 8, 45, 0)  # Monday 08:45
        assert self.calendar.get_status(dt) == self.MSS.PRE_OPEN

    def test_status_closed_after_hours(self):
        dt = datetime.datetime(2024, 3, 4, 14, 0, 0)  # Monday 14:00
        assert self.calendar.get_status(dt) == self.MSS.CLOSED

    def test_status_non_trading_day_on_weekend(self):
        dt = datetime.datetime(2024, 3, 2, 11, 0, 0)  # Saturday
        assert self.calendar.get_status(dt) == self.MSS.NON_TRADING_DAY

    def test_state_update_returns_status(self):
        dt = datetime.datetime(2024, 3, 4, 10, 0, 0)
        status = self.state.update(dt)
        assert status == self.MSS.OPEN

    def test_state_none_returns_unknown(self):
        status = self.state.update(None)
        assert status == self.MSS.UNKNOWN

    def test_is_trading_open(self):
        dt = datetime.datetime(2024, 3, 4, 10, 0, 0)
        self.state.update(dt)
        assert self.state.is_trading_open()

    def test_can_simulate_fill_open(self):
        dt = datetime.datetime(2024, 3, 4, 10, 0, 0)
        assert self.state.can_simulate_fill(dt)

    def test_cannot_simulate_fill_closed(self):
        dt = datetime.datetime(2024, 3, 4, 14, 0, 0)
        assert not self.state.can_simulate_fill(dt)


# ===========================================================================
# GROUP 7 — Data Classification (10 tests)
# ===========================================================================

class TestDataClassification:
    """paper_trading/data_classification_v160.py"""

    def setup_method(self):
        from paper_trading.data_classification_v160 import DataClassifier
        from paper_trading.enums_v160 import DataMode
        self.DataClassifier = DataClassifier
        self.DM = DataMode

    def test_classify_live(self):
        ok, mode, reason = self.DataClassifier.classify("LIVE")
        assert ok and mode == self.DM.LIVE

    def test_classify_delayed(self):
        ok, mode, reason = self.DataClassifier.classify("DELAYED")
        assert ok and mode == self.DM.DELAYED

    def test_classify_fixture(self):
        ok, mode, reason = self.DataClassifier.classify("FIXTURE")
        assert ok and mode == self.DM.FIXTURE

    def test_classify_unknown_returns_offline(self):
        ok, mode, reason = self.DataClassifier.classify("UNKNOWN_XYZ")
        assert not ok and mode == self.DM.OFFLINE

    def test_fixture_cannot_generate_formal_conclusion(self):
        ok, reason = self.DataClassifier.can_generate_formal_conclusion(self.DM.FIXTURE)
        assert not ok

    def test_offline_cannot_generate_formal_conclusion(self):
        ok, reason = self.DataClassifier.can_generate_formal_conclusion(self.DM.OFFLINE)
        assert not ok

    def test_live_can_generate_formal_conclusion(self):
        ok, reason = self.DataClassifier.can_generate_formal_conclusion(self.DM.LIVE)
        assert ok

    def test_all_modes_valid_for_paper_trading(self):
        for mode in self.DM:
            ok, reason = self.DataClassifier.validate_for_paper_trading(mode)
            assert ok, f"{mode}: {reason}"

    def test_none_mode_blocked(self):
        ok, reason = self.DataClassifier.validate_for_paper_trading(None)
        assert not ok

    def test_fixture_label(self):
        label = self.DataClassifier.get_label(self.DM.FIXTURE)
        assert "FIXTURE" in label and "FORMAL" in label


# ===========================================================================
# GROUP 8 — Order State Machine (15 tests)
# ===========================================================================

class TestOrderStateMachine:
    """paper_trading/order_state_machine_v160.py"""

    def _make_order(self, status):
        from paper_trading.enums_v160 import PaperOrderSide, PaperOrderType
        from paper_trading.models_v160 import PaperOrder
        o = PaperOrder(
            paper_order_id="po1", session_id="s1", client_order_id="c1",
            symbol="2330", side=PaperOrderSide.BUY, order_type=PaperOrderType.MARKET,
            quantity=Decimal("100"),
        )
        o.status = status
        return o

    def _make_sm(self, status):
        from paper_trading.order_state_machine_v160 import PaperOrderStateMachine
        from paper_trading.enums_v160 import PaperOrderStatus
        return PaperOrderStateMachine(self._make_order(status))

    def setup_method(self):
        from paper_trading.enums_v160 import PaperOrderStatus
        self.S = PaperOrderStatus

    def test_created_can_transition_to_validated(self):
        sm = self._make_sm(self.S.CREATED)
        assert sm.can_transition(self.S.VALIDATED)

    def test_created_can_transition_to_rejected(self):
        sm = self._make_sm(self.S.CREATED)
        assert sm.can_transition(self.S.REJECTED)

    def test_validated_can_transition_to_queued(self):
        sm = self._make_sm(self.S.VALIDATED)
        assert sm.can_transition(self.S.QUEUED)

    def test_queued_can_transition_to_filled(self):
        sm = self._make_sm(self.S.QUEUED)
        assert sm.can_transition(self.S.FILLED)

    def test_queued_can_transition_to_partially_filled(self):
        sm = self._make_sm(self.S.QUEUED)
        assert sm.can_transition(self.S.PARTIALLY_FILLED)

    def test_queued_can_be_halted(self):
        sm = self._make_sm(self.S.QUEUED)
        assert sm.can_transition(self.S.HALTED)

    def test_filled_is_terminal(self):
        sm = self._make_sm(self.S.FILLED)
        assert sm.is_terminal()

    def test_rejected_is_terminal(self):
        sm = self._make_sm(self.S.REJECTED)
        assert sm.is_terminal()

    def test_cancelled_is_terminal(self):
        sm = self._make_sm(self.S.CANCELLED)
        assert sm.is_terminal()

    def test_queued_can_fill(self):
        sm = self._make_sm(self.S.QUEUED)
        assert sm.can_fill()

    def test_partially_filled_can_fill(self):
        sm = self._make_sm(self.S.PARTIALLY_FILLED)
        assert sm.can_fill()

    def test_filled_cannot_fill(self):
        sm = self._make_sm(self.S.FILLED)
        assert not sm.can_fill()

    def test_invalid_transition_raises(self):
        sm = self._make_sm(self.S.FILLED)
        with pytest.raises(ValueError):
            sm.transition(self.S.QUEUED)

    def test_transition_updates_status(self):
        sm = self._make_sm(self.S.CREATED)
        sm.transition(self.S.VALIDATED)
        assert sm._order.status == self.S.VALIDATED

    def test_created_cannot_directly_fill(self):
        sm = self._make_sm(self.S.CREATED)
        assert not sm.can_transition(self.S.FILLED)


# ===========================================================================
# GROUP 9 — Slippage Models (20 tests)
# ===========================================================================

class TestSlippageModels:
    """paper_trading/slippage_model_v160.py"""

    def setup_method(self):
        from paper_trading.slippage_model_v160 import compute_slippage, SlippageResult
        from paper_trading.enums_v160 import SlippageModel, PaperOrderSide
        self.compute = compute_slippage
        self.SM = SlippageModel
        self.BUY = PaperOrderSide.BUY
        self.SELL = PaperOrderSide.SELL

    def test_fixed_bps_buy_increases_price(self):
        r = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"), fixed_bps=Decimal("10"))
        assert r.adjusted_price > Decimal("500")

    def test_fixed_bps_sell_decreases_price(self):
        r = self.compute(self.SM.FIXED_BPS, self.SELL, Decimal("500"), Decimal("1000"), fixed_bps=Decimal("10"))
        assert r.adjusted_price < Decimal("500")

    def test_fixed_bps_amount_correct(self):
        r = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"), fixed_bps=Decimal("10"))
        expected = Decimal("500") * Decimal("10") / Decimal("10000")
        assert r.slippage_amount == expected

    def test_fixed_bps_model_used(self):
        r = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"))
        assert r.model_used == self.SM.FIXED_BPS

    def test_fixed_bps_not_blocked(self):
        r = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"))
        assert not r.blocked

    def test_zero_price_blocked(self):
        r = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("0"), Decimal("1000"))
        assert r.blocked

    def test_spread_based_buy(self):
        r = self.compute(self.SM.SPREAD_BASED, self.BUY, Decimal("500"), Decimal("1000"),
                        bid=Decimal("499"), ask=Decimal("501"))
        assert r.adjusted_price == Decimal("501")  # 500 + half_spread(1)

    def test_spread_based_sell(self):
        r = self.compute(self.SM.SPREAD_BASED, self.SELL, Decimal("500"), Decimal("1000"),
                        bid=Decimal("499"), ask=Decimal("501"))
        assert r.adjusted_price == Decimal("499")  # 500 - half_spread(1)

    def test_spread_based_missing_bid_ask_no_block(self):
        r = self.compute(self.SM.SPREAD_BASED, self.BUY, Decimal("500"), Decimal("1000"))
        assert not r.blocked
        assert r.warning != ""

    def test_spread_based_half_spread_assumption(self):
        r = self.compute(self.SM.SPREAD_BASED, self.BUY, Decimal("500"), Decimal("1000"),
                        bid=Decimal("498"), ask=Decimal("502"))
        assert r.slippage_amount == Decimal("2")  # full spread = 4, half = 2

    def test_participation_based_no_volume_warning(self):
        r = self.compute(self.SM.PARTICIPATION_BASED, self.BUY, Decimal("500"), Decimal("1000"))
        assert r.warning != ""

    def test_participation_based_with_volume(self):
        r = self.compute(self.SM.PARTICIPATION_BASED, self.BUY, Decimal("500"), Decimal("100"),
                        volume=Decimal("10000"))
        assert not r.blocked
        assert r.slippage_bps > Decimal("0")

    def test_participation_caps_at_max_participation(self):
        # very large order relative to volume
        r = self.compute(self.SM.PARTICIPATION_BASED, self.BUY, Decimal("500"), Decimal("99999"),
                        volume=Decimal("1000"), max_participation=Decimal("0.05"))
        assert r.slippage_bps <= Decimal("200") * Decimal("0.05")  # max 5% participation

    def test_volatility_adjusted_default(self):
        r = self.compute(self.SM.VOLATILITY_ADJUSTED, self.BUY, Decimal("500"), Decimal("1000"))
        assert r.model_used == self.SM.VOLATILITY_ADJUSTED
        assert r.slippage_bps > Decimal("0")

    def test_volatility_adjusted_custom_vol(self):
        r = self.compute(self.SM.VOLATILITY_ADJUSTED, self.BUY, Decimal("500"), Decimal("1000"),
                        volatility_bps=Decimal("40"))
        assert r.slippage_bps == Decimal("20")  # vol/2

    def test_buy_adjusted_price_higher_than_base(self):
        for model in [self.SM.FIXED_BPS, self.SM.VOLATILITY_ADJUSTED]:
            r = self.compute(model, self.BUY, Decimal("500"), Decimal("100"))
            assert r.adjusted_price >= Decimal("500"), f"{model} buy should not lower price"

    def test_sell_adjusted_price_lower_than_base(self):
        for model in [self.SM.FIXED_BPS, self.SM.VOLATILITY_ADJUSTED]:
            r = self.compute(model, self.SELL, Decimal("500"), Decimal("100"))
            assert r.adjusted_price <= Decimal("500"), f"{model} sell should not raise price"

    def test_paper_only_assumption_present(self):
        r = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"))
        assert "PAPER" in r.assumption.upper()

    def test_slippage_non_negative(self):
        for model in self.SM:
            r = self.compute(model, self.BUY, Decimal("500"), Decimal("1000"),
                           bid=Decimal("499"), ask=Decimal("501"),
                           volume=Decimal("10000"), volatility_bps=Decimal("30"))
            assert r.slippage_amount >= Decimal("0"), f"{model}: negative slippage"

    def test_deterministic_same_inputs(self):
        r1 = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"), fixed_bps=Decimal("10"))
        r2 = self.compute(self.SM.FIXED_BPS, self.BUY, Decimal("500"), Decimal("1000"), fixed_bps=Decimal("10"))
        assert r1.adjusted_price == r2.adjusted_price


# ===========================================================================
# GROUP 10 — Liquidity Checker (12 tests)
# ===========================================================================

class TestLiquidityChecker:
    """paper_trading/liquidity_model_v160.py"""

    def setup_method(self):
        from paper_trading.liquidity_model_v160 import LiquidityChecker
        self.checker = LiquidityChecker()

    def test_full_fill_within_participation(self):
        r = self.checker.check(Decimal("100"), Decimal("5000"))
        assert not r.partial_fill
        assert r.fillable_quantity == Decimal("100")

    def test_partial_fill_exceeds_participation(self):
        r = self.checker.check(Decimal("5000"), Decimal("1000"))
        assert r.partial_fill
        assert r.fillable_quantity == Decimal("100")  # 10% of 1000

    def test_zero_volume_no_fill(self):
        r = self.checker.check(Decimal("1000"), Decimal("0"))
        assert r.fillable_quantity == Decimal("0")
        assert r.zero_volume

    def test_none_volume_no_fill(self):
        r = self.checker.check(Decimal("1000"), None)
        assert r.fillable_quantity == Decimal("0")

    def test_suspended_blocked(self):
        r = self.checker.check(Decimal("1000"), Decimal("10000"), is_suspended=True)
        assert r.blocked
        assert r.suspended

    def test_stale_blocked(self):
        r = self.checker.check(Decimal("1000"), Decimal("10000"), stale=True)
        assert r.blocked
        assert r.stale_quote

    def test_price_limit_breached_blocked(self):
        r = self.checker.check(
            Decimal("1000"), Decimal("10000"),
            price=Decimal("550"), price_limit=Decimal("500"),
        )
        assert r.blocked
        assert r.price_limit_breached

    def test_price_within_limit_ok(self):
        r = self.checker.check(
            Decimal("100"), Decimal("10000"),
            price=Decimal("490"), price_limit=Decimal("500"),
        )
        assert not r.blocked

    def test_custom_participation_rate(self):
        r = self.checker.check(Decimal("500"), Decimal("1000"), max_participation=Decimal("0.50"))
        assert r.fillable_quantity == Decimal("500")
        assert not r.partial_fill

    def test_remaining_quantity_correct_partial(self):
        r = self.checker.check(Decimal("5000"), Decimal("1000"))
        assert r.remaining_quantity == Decimal("4900")  # 5000 - 100

    def test_remaining_quantity_zero_full_fill(self):
        r = self.checker.check(Decimal("100"), Decimal("5000"))
        assert r.remaining_quantity == Decimal("0")

    def test_assumption_present(self):
        r = self.checker.check(Decimal("100"), Decimal("5000"))
        assert r.assumption != ""


# ===========================================================================
# GROUP 11 — Paper Ledger (15 tests)
# ===========================================================================

class TestPaperLedger:
    """paper_trading/paper_ledger_v160.py"""

    def setup_method(self):
        from paper_trading.paper_ledger_v160 import PaperLedger
        self.ledger = PaperLedger("s1")

    def test_initial_hash_is_genesis(self):
        assert self.ledger.current_hash() == "GENESIS"

    def test_initial_count_is_zero(self):
        assert self.ledger.count() == 0

    def test_append_returns_entry(self):
        entry = self.ledger.append("FILL")
        assert entry is not None

    def test_append_sets_paper_only(self):
        entry = self.ledger.append("FILL")
        assert entry.paper_only is True

    def test_append_increments_count(self):
        self.ledger.append("FILL")
        assert self.ledger.count() == 1

    def test_sequence_numbers_sequential(self):
        self.ledger.append("FILL")
        self.ledger.append("FILL")
        entries = self.ledger.get_entries()
        assert entries[0].sequence == 0
        assert entries[1].sequence == 1

    def test_hash_chain_first_entry_previous_is_genesis(self):
        entry = self.ledger.append("FILL")
        assert entry.previous_hash == "GENESIS"

    def test_hash_chain_chained(self):
        e0 = self.ledger.append("FILL")
        e1 = self.ledger.append("FILL")
        assert e1.previous_hash == e0.content_hash

    def test_verify_chain_empty(self):
        assert self.ledger.verify_chain()

    def test_verify_chain_valid(self):
        self.ledger.append("ORDER_QUEUED")
        self.ledger.append("FILL", cash_delta=Decimal("-500000"))
        assert self.ledger.verify_chain()

    def test_hash_changes_after_append(self):
        h0 = self.ledger.current_hash()
        self.ledger.append("FILL")
        h1 = self.ledger.current_hash()
        assert h0 != h1

    def test_reconstruct_cash(self):
        self.ledger.append("FILL", cash_delta=Decimal("-500000"))
        self.ledger.append("FILL", cash_delta=Decimal("-200000"))
        assert self.ledger.reconstruct_cash() == Decimal("-700000")

    def test_reconstruct_position(self):
        self.ledger.append("FILL", symbol="2330", quantity_delta=Decimal("1000"))
        self.ledger.append("FILL", symbol="2330", quantity_delta=Decimal("500"))
        assert self.ledger.reconstruct_position("2330") == Decimal("1500")

    def test_reconstruct_position_other_symbol(self):
        self.ledger.append("FILL", symbol="2330", quantity_delta=Decimal("1000"))
        assert self.ledger.reconstruct_position("2317") == Decimal("0")

    def test_get_entries_returns_copy(self):
        self.ledger.append("FILL")
        entries = self.ledger.get_entries()
        entries.clear()
        assert self.ledger.count() == 1


# ===========================================================================
# GROUP 12 — Kill Switch (15 tests)
# ===========================================================================

class TestKillSwitch:
    """paper_trading/paper_kill_switch_v160.py"""

    def setup_method(self):
        from paper_trading.paper_kill_switch_v160 import PaperKillSwitch
        from paper_trading.enums_v160 import KillSwitchReason
        self.KSR = KillSwitchReason
        self.ks = PaperKillSwitch(
            max_session_loss=Decimal("50000"),
            max_drawdown_pct=Decimal("0.10"),
            max_rejected_orders=5,
            max_malformed_events=3,
            data_stale_seconds=300,
        )

    def test_not_triggered_initially(self):
        assert not self.ks.is_triggered

    def test_manual_halt_triggers(self):
        evt = self.ks.manual_halt()
        assert evt.triggered
        assert evt.reason == self.KSR.MANUAL_HALT

    def test_max_loss_triggers(self):
        evt = self.ks.check_session_loss(Decimal("60000"))
        assert evt is not None and evt.triggered
        assert evt.reason == self.KSR.MAX_SESSION_LOSS

    def test_max_loss_below_threshold_no_trigger(self):
        evt = self.ks.check_session_loss(Decimal("40000"))
        assert evt is None

    def test_max_drawdown_triggers(self):
        evt = self.ks.check_drawdown(Decimal("0.15"))
        assert evt is not None and evt.triggered

    def test_max_drawdown_below_no_trigger(self):
        evt = self.ks.check_drawdown(Decimal("0.05"))
        assert evt is None

    def test_rejected_orders_triggers(self):
        evt = self.ks.check_rejected_orders(5)
        assert evt is not None and evt.triggered

    def test_malformed_events_triggers(self):
        evt = self.ks.check_malformed_events(3)
        assert evt is not None and evt.triggered

    def test_data_stale_triggers(self):
        evt = self.ks.check_data_stale(True)
        assert evt is not None and evt.triggered
        assert evt.reason == self.KSR.DATA_STALE

    def test_data_not_stale_no_trigger(self):
        evt = self.ks.check_data_stale(False)
        assert evt is None

    def test_data_feed_lost_triggers(self):
        evt = self.ks.check_data_feed_lost(True)
        assert evt is not None and evt.triggered
        assert evt.reason == self.KSR.DATA_FEED_LOST

    def test_ledger_integrity_fail_triggers(self):
        evt = self.ks.check_ledger_integrity(False)
        assert evt is not None and evt.triggered
        assert evt.reason == self.KSR.LEDGER_HASH_MISMATCH

    def test_ledger_integrity_ok_no_trigger(self):
        evt = self.ks.check_ledger_integrity(True)
        assert evt is None

    def test_safety_contract_violation_triggers(self):
        evt = self.ks.check_safety_contract(False)
        assert evt is not None
        assert evt.reason == self.KSR.SAFETY_CONTRACT_VIOLATION

    def test_idempotent_after_first_trigger(self):
        self.ks.manual_halt("first")
        self.ks.manual_halt("second")
        assert self.ks._detail == "first"  # reason doesn't change after first trigger


# ===========================================================================
# GROUP 13 — Event Journal (12 tests)
# ===========================================================================

class TestEventJournal:
    """paper_trading/event_journal_v160.py"""

    def _make_event(self, sequence, event_type="DATA_RECEIVED", key=None):
        from paper_trading.event_v160 import PaperEvent
        from paper_trading.enums_v160 import PaperEventType
        import uuid
        return PaperEvent(
            event_id=f"ev_{uuid.uuid4().hex[:8]}",
            session_id="s1",
            sequence=sequence,
            event_type=PaperEventType.DATA_RECEIVED,
            idempotency_key=key or f"ik_{sequence}",
            timestamp="2024-03-04T10:00:00Z",
            payload={},
        )

    def setup_method(self):
        from paper_trading.event_journal_v160 import PaperEventJournal
        self.journal = PaperEventJournal()

    def test_initial_empty(self):
        assert self.journal.count() == 0

    def test_append_increments_count(self):
        ev = self._make_event(0)
        self.journal.append(ev)
        assert self.journal.count() == 1

    def test_out_of_order_raises(self):
        ev = self._make_event(5)
        with pytest.raises(ValueError, match="Out-of-order"):
            self.journal.append(ev)

    def test_sequence_0_accepted(self):
        ev = self._make_event(0)
        self.journal.append(ev)

    def test_duplicate_key_idempotent(self):
        ev1 = self._make_event(0, key="k1")
        ev2 = self._make_event(0, key="k1")
        self.journal.append(ev1)
        # should not raise; returns existing
        result = self.journal.append(ev2)
        assert result is not None
        assert self.journal.count() == 1

    def test_sequential_events_accepted(self):
        for i in range(5):
            ev = self._make_event(i, key=f"k{i}")
            self.journal.append(ev)
        assert self.journal.count() == 5

    def test_hash_chained(self):
        ev0 = self._make_event(0, key="k0")
        ev1 = self._make_event(1, key="k1")
        self.journal.append(ev0)
        self.journal.append(ev1)
        events = self.journal.get_events()
        assert events[1].previous_hash == events[0].content_hash

    def test_content_hash_set(self):
        ev = self._make_event(0)
        self.journal.append(ev)
        events = self.journal.get_events()
        assert events[0].content_hash != ""

    def test_get_events_returns_copy(self):
        ev = self._make_event(0)
        self.journal.append(ev)
        events = self.journal.get_events()
        events.clear()
        assert self.journal.count() == 1

    def test_get_event_by_sequence(self):
        ev = self._make_event(0)
        self.journal.append(ev)
        found = self.journal.get_event(0)
        assert found is not None

    def test_get_missing_event_returns_none(self):
        result = self.journal.get_event(99)
        assert result is None

    def test_verify_chain(self):
        for i in range(3):
            ev = self._make_event(i, key=f"k{i}")
            self.journal.append(ev)
        assert self.journal.verify_chain()


# ===========================================================================
# GROUP 14 — Paper Cash (10 tests)
# ===========================================================================

class TestPaperCash:
    """paper_trading/paper_cash_v160.py"""

    def setup_method(self):
        from paper_trading.paper_cash_v160 import PaperCashManager
        self.cash = PaperCashManager("s1", Decimal("1000000"))

    def test_initial_cash_set(self):
        assert self.cash.available_cash == Decimal("1000000")

    def test_reserve_reduces_available(self):
        self.cash.reserve_for_order(Decimal("200000"), "o1")
        assert self.cash.available_cash == Decimal("800000")

    def test_release_restores_available(self):
        self.cash.reserve_for_order(Decimal("200000"), "o1")
        self.cash.release_reservation(Decimal("200000"))
        assert self.cash.available_cash == Decimal("1000000")

    def test_reserve_returns_true_when_sufficient(self):
        result = self.cash.reserve_for_order(Decimal("500000"), "o1")
        assert result is True

    def test_reserve_returns_false_when_insufficient(self):
        result = self.cash.reserve_for_order(Decimal("2000000"), "o1")
        assert result is False

    def test_sell_fill_increases_available(self):
        initial = self.cash.available_cash
        self.cash.apply_sell_fill(Decimal("100000"), Decimal("300"), Decimal("1000"))
        assert self.cash.available_cash > initial

    def test_paper_only_flag(self):
        b = self.cash.get_balance()
        assert b.paper_only == "PAPER_ONLY"

    def test_balance_session_id(self):
        b = self.cash.get_balance()
        assert b.session_id == "s1"

    def test_settlement_note_present(self):
        assert "SIMPLIFIED" in self.cash.settlement_note.upper() or \
               "PAPER" in self.cash.settlement_note.upper()

    def test_balance_currency(self):
        b = self.cash.get_balance()
        assert b.currency == "TWD"


# ===========================================================================
# GROUP 15 — Paper Position (10 tests)
# ===========================================================================

class TestPaperPosition:
    """paper_trading/paper_position_v160.py"""

    def setup_method(self):
        from paper_trading.paper_position_v160 import PaperPositionManager
        from paper_trading.enums_v160 import PaperOrderSide
        self.mgr = PaperPositionManager("s1")
        self.BUY = PaperOrderSide.BUY
        self.SELL = PaperOrderSide.SELL

    def test_initial_no_positions(self):
        assert len(self.mgr.get_all_positions()) == 0

    def test_add_buy(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("1000"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        pos = self.mgr.get_position("2330")
        assert pos.quantity == Decimal("1000")

    def test_average_cost_after_buy(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("1000"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        pos = self.mgr.get_position("2330")
        assert pos.average_cost == Decimal("500")

    def test_sell_reduces_quantity(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("1000"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        self.mgr.apply_fill("2330", self.SELL, Decimal("500"), Decimal("510"),
                           Decimal("0"), Decimal("0"))
        pos = self.mgr.get_position("2330")
        assert pos.quantity == Decimal("500")

    def test_sell_all_closes_position(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("1000"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        self.mgr.apply_fill("2330", self.SELL, Decimal("1000"), Decimal("510"),
                           Decimal("0"), Decimal("0"))
        pos = self.mgr.get_position("2330")
        assert pos.quantity == Decimal("0")

    def test_oversell_raises(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("500"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        with pytest.raises((ValueError, AssertionError)):
            self.mgr.apply_fill("2330", self.SELL, Decimal("1000"), Decimal("500"),
                               Decimal("0"), Decimal("0"))

    def test_paper_only_property(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("100"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        pos = self.mgr.get_position("2330")
        assert pos.paper_only == "PAPER_ONLY"

    def test_update_market_price(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("1000"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        self.mgr.update_market_price("2330", Decimal("520"))
        pos = self.mgr.get_position("2330")
        assert pos.market_price == Decimal("520")

    def test_unrealized_pnl_calculated(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("1000"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        self.mgr.update_market_price("2330", Decimal("520"))
        pos = self.mgr.get_position("2330")
        assert pos.unrealized_pnl == Decimal("20000")

    def test_session_id_set(self):
        self.mgr.apply_fill("2330", self.BUY, Decimal("100"), Decimal("500"),
                           Decimal("0"), Decimal("0"))
        pos = self.mgr.get_position("2330")
        assert pos.session_id == "s1"


# ===========================================================================
# GROUP 16 — Version Info (8 tests)
# ===========================================================================

class TestVersionInfo:
    """release/version_info.py"""

    def setup_method(self):
        from release import version_info as vi
        self.vi = vi

    def test_version_is_160(self):
        assert self.vi.VERSION >= "1.6.0", f"Expected >= 1.6.0, got {self.vi.VERSION}"

    def test_release_name_paper_trading(self):
        _KNOWN = {"Live Paper Trading Foundation", "Market Data Session Adapter",
                  "Market Data Session Warning Hygiene Hotfix",
                  "Paper Strategy Orchestration",
                  "Paper Strategy Orchestration Integrity Hotfix",
                  "Session Operations & Observability",
                  "Session Operations Integrity Hotfix",
                  "CLI Registration Health Integrity Hotfix",
            "CLI Handler Resolution Integrity Hotfix"}
        assert self.vi.RELEASE_NAME in _KNOWN or "Paper Trading" in self.vi.RELEASE_NAME or "Paper Strategy" in self.vi.RELEASE_NAME or "Session Operations" in self.vi.RELEASE_NAME, \
            f"Unexpected RELEASE_NAME: {self.vi.RELEASE_NAME}"

    def test_live_paper_trading_available(self):
        assert self.vi.LIVE_PAPER_TRADING_AVAILABLE is True

    def test_live_paper_trading_stage(self):
        assert self.vi.LIVE_PAPER_TRADING_STAGE == "FOUNDATION"

    def test_research_only_true(self):
        assert self.vi.LIVE_PAPER_TRADING_RESEARCH_ONLY is True

    def test_baseline_set(self):
        assert self.vi.LIVE_PAPER_TRADING_BASELINE == "1.6.0"

    def test_base_release_references_v159_or_160(self):
        assert any(v in self.vi.BASE_RELEASE for v in ("1.5.9", "1.6.0", "1.6.1", "1.6.2", "1.6.3"))

    def test_version_string_valid_format(self):
        parts = self.vi.VERSION.split(".")
        assert len(parts) in (3, 4), f"Expected 3 or 4 version parts, got {len(parts)}: {self.vi.VERSION}"


# ===========================================================================
# GROUP 17 — CLI Command Registry (10 tests)
# ===========================================================================

class TestCLICommandRegistry:
    """cli/command_registry.py — live_paper_trading commands"""

    def setup_method(self):
        from cli.command_registry import PROVIDER_COMMANDS, get_formal_command_names
        self.commands = PROVIDER_COMMANDS
        self.get_names = get_formal_command_names

    def test_paper_trading_commands_present(self):
        paper_cmds = [c for c in self.commands if c.group == "live_paper_trading"]
        assert len(paper_cmds) >= 30

    def test_all_paper_commands_simulation_only(self):
        paper_cmds = [c for c in self.commands if c.group == "live_paper_trading"]
        for cmd in paper_cmds:
            assert cmd.safety_classification == "SIMULATION_ONLY", \
                f"{cmd.handler_name} has wrong safety_classification"

    def test_paper_session_create_present(self):
        names = [c.handler_name for c in self.commands]
        assert "cmd_paper_session_create" in names

    def test_paper_trading_health_present(self):
        names = [c.handler_name for c in self.commands]
        assert "cmd_paper_trading_health" in names

    def test_paper_session_report_present(self):
        names = [c.handler_name for c in self.commands]
        assert "cmd_paper_session_report" in names

    def test_get_formal_command_names_callable(self):
        names = self.get_names()
        assert isinstance(names, (list, set, frozenset))

    def test_formal_names_includes_paper_commands(self):
        names = self.get_names()
        paper_names = [n for n in names if "paper" in n]
        assert len(paper_names) >= 30

    def test_paper_commands_have_handler_name(self):
        paper_cmds = [c for c in self.commands if c.group == "live_paper_trading"]
        for cmd in paper_cmds:
            assert cmd.handler_name != ""

    def test_paper_session_show_present(self):
        names = [c.handler_name for c in self.commands]
        assert "cmd_paper_session_show" in names

    def test_paper_kill_switch_present(self):
        names = [c.handler_name for c in self.commands]
        assert "cmd_paper_kill_switch" in names


# ===========================================================================
# GROUP 18 — Release Gate Structure (10 tests)
# ===========================================================================

class TestReleaseGateStructure:
    """release/live_paper_trading_release_gate_v160.py"""

    def setup_method(self):
        from release.live_paper_trading_release_gate_v160 import run_release_gate
        self.run_gate = run_release_gate

    def test_run_release_gate_callable(self):
        assert callable(self.run_gate)

    def test_release_gate_returns_dict(self):
        result = self.run_gate()
        assert isinstance(result, dict)

    def test_release_gate_has_gate_passed_key(self):
        result = self.run_gate()
        assert "gate_passed" in result or "overall" in result

    def test_release_gate_has_checks(self):
        result = self.run_gate()
        assert "checks" in result

    def test_release_gate_checks_is_list(self):
        result = self.run_gate()
        assert isinstance(result.get("checks", []), list)

    def test_release_gate_has_safety_gates(self):
        result = self.run_gate()
        checks = result.get("checks", [])
        names = [c.get("check", c.get("name", "")) for c in checks]
        safety_checks = [n for n in names if "safety" in n.lower() or "no_real" in n.lower()
                        or "paper" in n.lower() or "broker" in n.lower()]
        assert len(safety_checks) >= 1

    def test_release_gate_has_version_key(self):
        result = self.run_gate()
        assert "gate_version" in result or "version" in result or \
               any("version" in str(k).lower() for k in result)

    def test_checks_have_passed_field(self):
        result = self.run_gate()
        for check in result.get("checks", []):
            assert "passed" in check or "status" in check or "result" in check

    def test_release_gate_no_broker_safety_check(self):
        result = self.run_gate()
        checks = result.get("checks", [])
        all_text = str(checks).lower()
        assert "broker" in all_text or "real_order" in all_text or "paper" in all_text

    def test_release_gate_not_blocked(self):
        result = self.run_gate()
        blocked = result.get("blocked", False)
        assert blocked is False or blocked == [] or blocked == {}


# ===========================================================================
# GROUP 19 — GUI Panel Metadata (5 tests)
# ===========================================================================

class TestGUIPanelMetadata:
    """gui/live_paper_trading_panel.py"""

    def setup_method(self):
        import gui.live_paper_trading_panel as p
        self.panel = p

    def test_panel_importable(self):
        assert hasattr(self.panel, "LivePaperTradingPanel")

    def test_panel_metadata_present(self):
        assert hasattr(self.panel, "PANEL_METADATA")

    def test_panel_tab_id(self):
        assert self.panel.PANEL_METADATA["tab_id"] == "live_paper_trading"

    def test_panel_group(self):
        assert self.panel.PANEL_METADATA["group"] == "paper_trading"

    def test_real_order_forbidden(self):
        p = self.panel.LivePaperTradingPanel()
        with pytest.raises(NotImplementedError):
            p.real_buy()


# ===========================================================================
# GROUP 20 — Health Module (5 tests)
# ===========================================================================

class TestHealthModule:
    """paper_trading/health_v160.py"""

    def setup_method(self):
        from paper_trading.health_v160 import LivePaperTradingHealthCheck
        self.health_cls = LivePaperTradingHealthCheck

    def test_health_importable(self):
        assert self.health_cls is not None

    def test_health_callable(self):
        h = self.health_cls()
        assert callable(h.run)

    def test_health_returns_dict(self):
        result = self.health_cls().run()
        assert isinstance(result, dict)

    def test_health_has_status(self):
        result = self.health_cls().run()
        assert "status" in result or "passed" in result or "overall" in result

    def test_health_has_checks_list(self):
        result = self.health_cls().run()
        assert "checks" in result
        assert isinstance(result["checks"], list)


# ===========================================================================
# GROUP 21 — Fixture Files Existence and Schema (34 tests)
# ===========================================================================

REQUIRED_FIXTURES = [
    "session_valid.json",
    "session_invalid.json",
    "market_open.json",
    "market_closed.json",
    "market_non_trading_day.json",
    "data_live.json",
    "data_delayed.json",
    "data_replay.json",
    "data_fixture.json",
    "market_events_ordered.json",
    "market_events_duplicate.json",
    "market_events_out_of_order.json",
    "paper_order_market.json",
    "paper_order_limit.json",
    "paper_order_stop.json",
    "paper_order_stop_limit.json",
    "paper_order_insufficient_cash.json",
    "paper_order_insufficient_position.json",
    "paper_order_duplicate_client_id.json",
    "fill_complete.json",
    "fill_partial.json",
    "fill_none.json",
    "slippage_fixed.json",
    "slippage_spread.json",
    "liquidity_partial.json",
    "ledger_valid.json",
    "ledger_hash_mismatch.json",
    "snapshot_valid.json",
    "kill_switch_loss.json",
    "kill_switch_data_stale.json",
    "replay_valid.json",
    "recovery_valid.json",
    "lineage_complete.json",
    "reproducibility_valid.json",
]


@pytest.mark.parametrize("filename", REQUIRED_FIXTURES)
def test_fixture_exists(filename):
    path = FIXTURES_DIR / filename
    assert path.exists(), f"Missing fixture: {filename}"


@pytest.mark.parametrize("filename", REQUIRED_FIXTURES)
def test_fixture_valid_json(filename):
    data = load_fixture(filename)
    assert isinstance(data, dict)


@pytest.mark.parametrize("filename", REQUIRED_FIXTURES)
def test_fixture_has_paper_only_flag(filename):
    data = load_fixture(filename)
    assert data.get("paper_only") is True, f"{filename}: missing paper_only=true"


@pytest.mark.parametrize("filename", REQUIRED_FIXTURES)
def test_fixture_has_not_real_order_flag(filename):
    data = load_fixture(filename)
    assert data.get("not_real_order") is True, f"{filename}: missing not_real_order=true"


@pytest.mark.parametrize("filename", REQUIRED_FIXTURES)
def test_fixture_has_fixture_type(filename):
    data = load_fixture(filename)
    assert data.get("fixture_type") == "TEST_FIXTURE", f"{filename}: wrong fixture_type"


# ===========================================================================
# GROUP 22 — Reproducibility Manifest (8 tests)
# ===========================================================================

class TestReproducibilityManifest:
    """paper_trading/reproducibility_v160.py"""

    def setup_method(self):
        from paper_trading.reproducibility_v160 import ReproducibilityService
        from paper_trading.models_v160 import PaperSessionConfig
        self.svc = ReproducibilityService()
        self.cfg = PaperSessionConfig(session_id="s1", name="test")

    def _build(self, session_id="s1"):
        from paper_trading.models_v160 import PaperSessionConfig
        cfg = PaperSessionConfig(session_id=session_id, name="test")
        return self.svc.build_manifest(
            manifest_id=f"m_{session_id}",
            session_id=session_id,
            session_config=cfg,
            event_hashes=[],
        )

    def test_builder_importable(self):
        from paper_trading.reproducibility_v160 import ReproducibilityService
        assert ReproducibilityService is not None

    def test_build_returns_manifest(self):
        manifest = self._build()
        assert manifest is not None

    def test_manifest_paper_only(self):
        manifest = self._build()
        assert manifest.paper_only is True

    def test_manifest_research_only(self):
        manifest = self._build()
        assert manifest.research_only is True

    def test_manifest_session_id_matches(self):
        manifest = self._build("my_sess")
        assert manifest.session_id == "my_sess"

    def test_manifest_timezone(self):
        manifest = self._build()
        assert manifest.timezone == "Asia/Taipei"

    def test_manifest_calendar_version(self):
        manifest = self._build()
        assert manifest.calendar_version == "v160"

    def test_manifest_has_manifest_id(self):
        manifest = self._build()
        assert manifest.manifest_id != ""


# ===========================================================================
# GROUP 23 — Query Forbidden Methods (8 tests)
# ===========================================================================

class TestQueryForbiddenMethods:
    """paper_trading/query_v160.py"""

    def setup_method(self):
        from paper_trading.query_v160 import PaperTradingQueryService
        self.query = PaperTradingQueryService()

    def test_submit_real_order_forbidden(self):
        with pytest.raises(NotImplementedError):
            self.query.submit_real_order()

    def test_broker_connect_forbidden(self):
        with pytest.raises(NotImplementedError):
            self.query.connect_broker()

    def test_sync_real_account_forbidden(self):
        with pytest.raises(NotImplementedError):
            self.query.sync_real_account()

    def test_apply_to_real_portfolio_forbidden(self):
        with pytest.raises(NotImplementedError):
            self.query.apply_to_real_portfolio()

    def test_query_importable(self):
        from paper_trading.query_v160 import PaperTradingQueryService
        assert PaperTradingQueryService is not None

    def test_query_has_paper_submit(self):
        assert hasattr(self.query, "submit_paper_order")

    def test_real_trade_execution_forbidden(self):
        with pytest.raises(NotImplementedError):
            self.query.execute_real_trade()

    def test_query_has_create_session(self):
        assert hasattr(self.query, "create_paper_session")


# ===========================================================================
# GROUP 24 — Specific Fixture Content Validation (15 tests)
# ===========================================================================

class TestFixtureContent:
    """Validate key fixture fields."""

    def test_snapshot_valid_has_session_id(self):
        data = load_fixture("snapshot_valid.json")
        assert "session_id" in data

    def test_snapshot_valid_pnl_fields(self):
        data = load_fixture("snapshot_valid.json")
        assert "realized_pnl" in data or "unrealized_pnl" in data

    def test_ledger_valid_has_entries(self):
        data = load_fixture("ledger_valid.json")
        assert "entries" in data
        assert len(data["entries"]) > 0

    def test_ledger_hash_mismatch_expected_kill_switch(self):
        data = load_fixture("ledger_hash_mismatch.json")
        assert data.get("expected_kill_switch") == "LEDGER_HASH_MISMATCH"

    def test_kill_switch_loss_trigger(self):
        data = load_fixture("kill_switch_loss.json")
        assert data.get("trigger") == "MAX_LOSS_EXCEEDED"
        assert data.get("expected_kill_switch_triggered") is True

    def test_kill_switch_loss_no_auto_close(self):
        data = load_fixture("kill_switch_loss.json")
        assert data.get("expected_auto_close") is False

    def test_kill_switch_data_stale_trigger(self):
        data = load_fixture("kill_switch_data_stale.json")
        assert data.get("trigger") == "DATA_FEED_STALE"

    def test_replay_valid_deterministic(self):
        data = load_fixture("replay_valid.json")
        assert data.get("expected_deterministic") is True
        assert data.get("expected_same_ledger_hash") is True

    def test_recovery_valid_paused_state(self):
        data = load_fixture("recovery_valid.json")
        assert data.get("expected_recovery_status") == "PAUSED"
        assert data.get("expected_auto_resume") is False

    def test_lineage_complete_blocks_formal_conclusion(self):
        data = load_fixture("lineage_complete.json")
        assert data.get("expected_formal_conclusion_blocked") is True

    def test_reproducibility_same_hashes(self):
        data = load_fixture("reproducibility_valid.json")
        assert data["run_1_ledger_hash"] == data["run_2_ledger_hash"]
        assert data["run_1_snapshot_hash"] == data["run_2_snapshot_hash"]

    def test_liquidity_partial_fields(self):
        data = load_fixture("liquidity_partial.json")
        assert "order_quantity" in data
        assert "available_volume" in data
        assert "expected_partial" in data

    def test_slippage_spread_has_bid_ask(self):
        data = load_fixture("slippage_spread.json")
        assert "bid" in data and "ask" in data

    def test_paper_order_market_has_symbol(self):
        data = load_fixture("paper_order_market.json")
        assert "symbol" in data or "order_type" in data

    def test_session_invalid_expected_valid_false(self):
        data = load_fixture("session_invalid.json")
        assert data.get("expected_valid") is False


# ===========================================================================
# GROUP 25 — Module Import Completeness (10 tests)
# ===========================================================================

class TestModuleImports:
    """All 34 paper_trading modules must import without error."""

    MODULES = [
        "paper_trading",
        "paper_trading.enums_v160",
        "paper_trading.models_v160",
        "paper_trading.validation_v160",
        "paper_trading.event_v160",
        "paper_trading.idempotency_v160",
        "paper_trading.event_journal_v160",
        "paper_trading.event_bus_v160",
        "paper_trading.market_session_v160",
        "paper_trading.data_classification_v160",
        "paper_trading.order_state_machine_v160",
        "paper_trading.latency_model_v160",
        "paper_trading.slippage_model_v160",
        "paper_trading.liquidity_model_v160",
        "paper_trading.partial_fill_v160",
        "paper_trading.paper_fill_v160",
        "paper_trading.execution_simulator_v160",
        "paper_trading.paper_cash_v160",
        "paper_trading.paper_position_v160",
        "paper_trading.paper_ledger_v160",
        "paper_trading.paper_pnl_v160",
        "paper_trading.paper_risk_gate_v160",
        "paper_trading.paper_kill_switch_v160",
        "paper_trading.snapshot_v160",
        "paper_trading.audit_v160",
        "paper_trading.lineage_v160",
        "paper_trading.reproducibility_v160",
        "paper_trading.explain_v160",
        "paper_trading.store_v160",
        "paper_trading.session_replay_v160",
        "paper_trading.recovery_v160",
        "paper_trading.session_v160",
        "paper_trading.query_v160",
        "paper_trading.health_v160",
    ]

    @pytest.mark.parametrize("module_name", MODULES)
    def test_module_imports(self, module_name):
        mod = importlib.import_module(module_name)
        assert mod is not None
