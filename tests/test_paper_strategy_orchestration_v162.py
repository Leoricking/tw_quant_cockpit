"""
tests/test_paper_strategy_orchestration_v162.py — Test suite for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import json
import os
import unittest
from datetime import datetime, timezone
from typing import List, Optional

# ---------------------------------------------------------------------------
# Fixture strategies (TEST_FIXTURE / DEMO_ONLY / PAPER_ONLY / NOT_FOR_PRODUCTION)
# ---------------------------------------------------------------------------

class ThresholdFixtureStrategy:
    """TEST_FIXTURE. DEMO_ONLY. NOT_FOR_PRODUCTION."""
    PAPER_ONLY = True
    RESEARCH_ONLY = True
    SIMULATION_ONLY = True
    NOT_A_REAL_ORDER = True
    NO_BROKER_CALL = True
    NO_REAL_ACCOUNT = True

    def __init__(self, config):
        self._config = config
        self._status_val = "REGISTERED"
        self._meta = type("M", (), {
            "signal_count": 0, "decision_count": 0, "proposal_count": 0,
            "approved_count": 0, "rejected_count": 0, "error_count": 0,
            "last_signal_at": None, "strategy_id": config.strategy_id,
            "status": None
        })()

    @property
    def config(self): return self._config
    @property
    def strategy_id(self): return self._config.strategy_id
    @property
    def strategy_name(self): return self._config.strategy_name
    @property
    def status(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        return StrategyStatus(self._status_val)
    @property
    def metadata(self): return self._meta

    def start(self):
        self._status_val = "RUNNING"
        self._meta.status = self.status
        self.on_start()
    def pause(self):
        self._status_val = "PAUSED"
        self.on_pause()
    def halt(self):
        self._status_val = "HALTED"
        self.on_halt()
    def complete(self):
        self._status_val = "COMPLETED"

    def on_start(self): pass
    def on_pause(self): pass
    def on_halt(self): pass
    def describe(self): return "ThresholdFixtureStrategy (TEST_FIXTURE)"

    def generate_signals(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.enums_v162 import SignalStrength
        return [make_entry_long(self.strategy_id, "2330.TW",
                                confidence=0.8, strength=SignalStrength.MODERATE)]

    def safe_generate_signals(self):
        return self.generate_signals()


class RiskBlockedFixtureStrategy(ThresholdFixtureStrategy):
    """TEST_FIXTURE for risk-blocked scenarios."""
    def describe(self): return "RiskBlockedFixtureStrategy (TEST_FIXTURE)"
    def generate_signals(self):
        from paper_trading.strategy.signal_v162 import make_block
        return [make_block(self.strategy_id, "2330.TW", reason="risk_block_test")]


class ConflictFixtureStrategy(ThresholdFixtureStrategy):
    """TEST_FIXTURE for conflict resolution scenarios."""
    def describe(self): return "ConflictFixtureStrategy (TEST_FIXTURE)"
    def generate_signals(self):
        from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
        return [
            make_entry_long(self.strategy_id, "2330.TW"),
            make_exit_long(self.strategy_id, "2330.TW"),
        ]


# ---------------------------------------------------------------------------
# Test classes
# ---------------------------------------------------------------------------

class TestModuleInit(unittest.TestCase):
    """Tests for paper_trading/strategy/__init__.py"""

    def test_001_module_importable(self):
        import paper_trading.strategy as ps
        self.assertIsNotNone(ps)

    def test_002_version(self):
        from paper_trading.strategy import PAPER_STRATEGY_ORCHESTRATION_VERSION
        self.assertEqual(PAPER_STRATEGY_ORCHESTRATION_VERSION, "1.6.2")

    def test_003_stage(self):
        from paper_trading.strategy import PAPER_STRATEGY_ORCHESTRATION_STAGE
        self.assertEqual(PAPER_STRATEGY_ORCHESTRATION_STAGE, "FOUNDATION")

    def test_004_research_only(self):
        from paper_trading.strategy import PAPER_STRATEGY_RESEARCH_ONLY
        self.assertIs(PAPER_STRATEGY_RESEARCH_ONLY, True)

    def test_005_no_real_orders(self):
        from paper_trading.strategy import NO_REAL_ORDERS
        self.assertIs(NO_REAL_ORDERS, True)

    def test_006_broker_disabled(self):
        from paper_trading.strategy import BROKER_EXECUTION_ENABLED
        self.assertIs(BROKER_EXECUTION_ENABLED, False)

    def test_007_production_blocked(self):
        from paper_trading.strategy import PRODUCTION_TRADING_BLOCKED
        self.assertIs(PRODUCTION_TRADING_BLOCKED, True)

    def test_008_no_short_selling(self):
        from paper_trading.strategy import SHORT_SELLING_ENABLED
        self.assertIs(SHORT_SELLING_ENABLED, False)

    def test_009_no_margin(self):
        from paper_trading.strategy import MARGIN_ENABLED
        self.assertIs(MARGIN_ENABLED, False)

    def test_010_real_order_creation_disabled(self):
        from paper_trading.strategy import REAL_ORDER_CREATION_ENABLED
        self.assertIs(REAL_ORDER_CREATION_ENABLED, False)

    def test_011_real_order_execution_disabled(self):
        from paper_trading.strategy import REAL_ORDER_EXECUTION_ENABLED
        self.assertIs(REAL_ORDER_EXECUTION_ENABLED, False)

    def test_012_autonomous_production_disabled(self):
        from paper_trading.strategy import AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED
        self.assertIs(AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED, False)

    def test_013_auto_paper_only_disabled_by_default(self):
        from paper_trading.strategy import AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT
        self.assertIs(AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT, False)

    def test_014_signal_evaluation_enabled(self):
        from paper_trading.strategy import PAPER_SIGNAL_EVALUATION_ENABLED
        self.assertIs(PAPER_SIGNAL_EVALUATION_ENABLED, True)

    def test_015_decision_pipeline_enabled(self):
        from paper_trading.strategy import PAPER_DECISION_PIPELINE_ENABLED
        self.assertIs(PAPER_DECISION_PIPELINE_ENABLED, True)


class TestEnums(unittest.TestCase):
    """Tests for enums_v162.py"""

    def test_020_strategy_status_values(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        self.assertIn("REGISTERED", [s.value for s in StrategyStatus])
        self.assertIn("RUNNING", [s.value for s in StrategyStatus])
        self.assertIn("HALTED", [s.value for s in StrategyStatus])

    def test_021_signal_type_no_short(self):
        from paper_trading.strategy.enums_v162 import SignalType
        types = [st.value for st in SignalType]
        self.assertNotIn("ENTRY_SHORT", types)
        self.assertNotIn("SELL_SHORT", types)

    def test_022_signal_type_allowed(self):
        from paper_trading.strategy.enums_v162 import SignalType
        types = [st.value for st in SignalType]
        self.assertIn("ENTRY_LONG", types)
        self.assertIn("EXIT_LONG", types)
        self.assertIn("HOLD", types)
        self.assertIn("BLOCK", types)
        self.assertIn("ALERT", types)
        self.assertIn("REDUCE_RESEARCH", types)

    def test_023_decision_outcome(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        self.assertEqual(DecisionOutcome.APPROVED.value, "APPROVED")
        self.assertEqual(DecisionOutcome.DEFERRED.value, "DEFERRED")
        self.assertEqual(DecisionOutcome.RISK_BLOCKED.value, "RISK_BLOCKED")

    def test_024_approval_mode_default(self):
        from paper_trading.strategy.enums_v162 import ApprovalMode
        self.assertEqual(ApprovalMode.MANUAL_REQUIRED.value, "MANUAL_REQUIRED")

    def test_025_conflict_policy_default(self):
        from paper_trading.strategy.enums_v162 import ConflictPolicy
        self.assertEqual(ConflictPolicy.MOST_CONSERVATIVE.value, "MOST_CONSERVATIVE")

    def test_026_proposal_status(self):
        from paper_trading.strategy.enums_v162 import ProposalStatus
        self.assertIn("PENDING", [ps.value for ps in ProposalStatus])
        self.assertIn("SUBMITTED", [ps.value for ps in ProposalStatus])

    def test_027_journal_event_types(self):
        from paper_trading.strategy.enums_v162 import JournalEventType
        self.assertIn("STRATEGY_REGISTERED", [e.value for e in JournalEventType])
        self.assertIn("SIGNAL_RECEIVED", [e.value for e in JournalEventType])

    def test_028_trigger_types(self):
        from paper_trading.strategy.enums_v162 import TriggerType
        types = [t.value for t in TriggerType]
        self.assertIn("MANUAL", types)
        self.assertIn("REPLAY", types)

    def test_029_eligibility_result(self):
        from paper_trading.strategy.enums_v162 import EligibilityResult
        self.assertEqual(EligibilityResult.ELIGIBLE.value, "ELIGIBLE")
        self.assertEqual(EligibilityResult.INELIGIBLE.value, "INELIGIBLE")
        self.assertEqual(EligibilityResult.UNCERTAIN.value, "UNCERTAIN")

    def test_030_recovery_mode(self):
        from paper_trading.strategy.enums_v162 import RecoveryMode
        modes = [m.value for m in RecoveryMode]
        self.assertIn("FULL_REPLAY", modes)
        self.assertIn("STATE_RESTORE", modes)
        self.assertIn("COLD_START", modes)


class TestModels(unittest.TestCase):
    """Tests for models_v162.py"""

    def test_040_strategy_config_defaults(self):
        from paper_trading.strategy.models_v162 import StrategyConfig
        cfg = StrategyConfig(strategy_name="test")
        self.assertIs(cfg.paper_only, True)
        self.assertIs(cfg.research_only, True)
        self.assertIs(cfg.simulation_only, True)
        self.assertIs(cfg.not_a_real_order, True)
        self.assertIs(cfg.no_broker_call, True)
        self.assertIs(cfg.no_real_account, True)
        self.assertIs(cfg.no_formal_portfolio_ledger_write, True)

    def test_041_strategy_config_assertion_paper_only(self):
        from paper_trading.strategy.models_v162 import StrategyConfig
        with self.assertRaises(AssertionError):
            StrategyConfig(strategy_name="bad", paper_only=False)

    def test_042_strategy_config_assertion_research_only(self):
        from paper_trading.strategy.models_v162 import StrategyConfig
        with self.assertRaises(AssertionError):
            StrategyConfig(strategy_name="bad", research_only=False)

    def test_043_paper_signal_defaults(self):
        from paper_trading.strategy.models_v162 import PaperSignal
        sig = PaperSignal(ticker="2330.TW")
        self.assertIs(sig.paper_only, True)
        self.assertIs(sig.research_only, True)
        self.assertIs(sig.not_a_real_order, True)

    def test_044_paper_signal_confidence_range(self):
        from paper_trading.strategy.models_v162 import PaperSignal
        with self.assertRaises(AssertionError):
            PaperSignal(ticker="2330.TW", confidence=1.5)
        with self.assertRaises(AssertionError):
            PaperSignal(ticker="2330.TW", confidence=-0.1)

    def test_045_paper_signal_forbidden_type(self):
        from paper_trading.strategy.models_v162 import PaperSignal
        with self.assertRaises(AssertionError):
            PaperSignal(ticker="2330.TW", signal_type="ENTRY_SHORT")

    def test_046_paper_order_proposal_safety(self):
        from paper_trading.strategy.models_v162 import PaperOrderProposal
        p = PaperOrderProposal(ticker="2330.TW", proposed_size=100.0)
        self.assertIs(p.paper_only, True)
        self.assertIs(p.no_formal_portfolio_ledger_write, True)

    def test_047_paper_order_proposal_assertion(self):
        from paper_trading.strategy.models_v162 import PaperOrderProposal
        with self.assertRaises(AssertionError):
            PaperOrderProposal(ticker="2330.TW", proposed_size=100.0, paper_only=False)

    def test_048_decision_result_safety(self):
        from paper_trading.strategy.models_v162 import DecisionResult
        r = DecisionResult()
        self.assertIs(r.paper_only, True)
        self.assertIs(r.not_a_real_order, True)
        self.assertIs(r.no_broker_call, True)

    def test_049_strategy_metadata_defaults(self):
        from paper_trading.strategy.models_v162 import StrategyMetadata
        from paper_trading.strategy.enums_v162 import StrategyStatus
        m = StrategyMetadata(strategy_id="test")
        self.assertEqual(m.status, StrategyStatus.REGISTERED)
        self.assertEqual(m.signal_count, 0)

    def test_050_lineage_record_defaults(self):
        from paper_trading.strategy.models_v162 import LineageRecord
        r = LineageRecord()
        self.assertIsInstance(r.lineage_id, str)
        self.assertEqual(r.outcome, "REJECTED")


class TestValidation(unittest.TestCase):
    """Tests for validation_v162.py"""

    def test_060_validate_signal_type_allowed(self):
        from paper_trading.strategy.validation_v162 import validate_signal_type
        for t in ("ENTRY_LONG", "EXIT_LONG", "HOLD", "REDUCE_RESEARCH", "BLOCK", "ALERT"):
            ok, msg = validate_signal_type(t)
            self.assertTrue(ok, f"Should be valid: {t}")

    def test_061_validate_signal_type_forbidden(self):
        from paper_trading.strategy.validation_v162 import validate_signal_type
        for t in ("ENTRY_SHORT", "SELL_SHORT"):
            ok, msg = validate_signal_type(t)
            self.assertFalse(ok, f"Should be forbidden: {t}")
            self.assertIn("forbidden", msg.lower())

    def test_062_validate_confidence_valid(self):
        from paper_trading.strategy.validation_v162 import validate_confidence
        ok, _ = validate_confidence(0.0)
        self.assertTrue(ok)
        ok, _ = validate_confidence(1.0)
        self.assertTrue(ok)
        ok, _ = validate_confidence(0.5)
        self.assertTrue(ok)

    def test_063_validate_confidence_invalid(self):
        from paper_trading.strategy.validation_v162 import validate_confidence
        ok, msg = validate_confidence(1.5)
        self.assertFalse(ok)
        ok, msg = validate_confidence(-0.1)
        self.assertFalse(ok)

    def test_064_validate_ticker_valid(self):
        from paper_trading.strategy.validation_v162 import validate_ticker
        ok, _ = validate_ticker("2330.TW")
        self.assertTrue(ok)

    def test_065_validate_ticker_empty(self):
        from paper_trading.strategy.validation_v162 import validate_ticker
        ok, _ = validate_ticker("")
        self.assertFalse(ok)
        ok, _ = validate_ticker("   ")
        self.assertFalse(ok)

    def test_066_validate_paper_signal_dict_valid(self):
        from paper_trading.strategy.validation_v162 import validate_paper_signal_dict
        d = {
            "ticker": "2330.TW", "signal_type": "ENTRY_LONG",
            "confidence": 0.8,
            "paper_only": True, "research_only": True, "not_a_real_order": True,
        }
        ok, errors = validate_paper_signal_dict(d)
        self.assertTrue(ok)

    def test_067_validate_paper_signal_dict_forbidden(self):
        from paper_trading.strategy.validation_v162 import validate_paper_signal_dict
        d = {
            "ticker": "2330.TW", "signal_type": "ENTRY_SHORT",
            "confidence": 0.8,
            "paper_only": True, "research_only": True, "not_a_real_order": True,
        }
        ok, errors = validate_paper_signal_dict(d)
        self.assertFalse(ok)

    def test_068_validate_strategy_config_dict_valid(self):
        from paper_trading.strategy.validation_v162 import validate_strategy_config_dict
        d = {
            "strategy_name": "test",
            "approval_mode": "MANUAL_REQUIRED",
            "conflict_policy": "MOST_CONSERVATIVE",
            "max_signals_per_minute": 10,
            "cooldown_seconds": 30,
            "paper_only": True, "research_only": True, "simulation_only": True,
            "not_a_real_order": True, "no_broker_call": True,
            "no_real_account": True, "no_formal_portfolio_ledger_write": True,
        }
        ok, errors = validate_strategy_config_dict(d)
        self.assertTrue(ok)

    def test_069_assert_safety_invariants_pass(self):
        from paper_trading.strategy.validation_v162 import assert_safety_invariants
        from paper_trading.strategy.models_v162 import StrategyConfig
        cfg = StrategyConfig(strategy_name="test")
        assert_safety_invariants(cfg)  # should not raise

    def test_070_assert_safety_invariants_fail(self):
        from paper_trading.strategy.validation_v162 import assert_safety_invariants
        obj = type("Fake", (), {"paper_only": False, "research_only": True,
                                 "not_a_real_order": True})()
        with self.assertRaises(AssertionError):
            assert_safety_invariants(obj)


class TestStrategyBase(unittest.TestCase):
    """Tests for strategy_base_v162.py"""

    def _make_strategy(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config("fixture_threshold")
        return ThresholdFixtureStrategy(cfg)

    def test_080_class_safety_flags(self):
        from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
        self.assertIs(PaperStrategyBase.PAPER_ONLY, True)
        self.assertIs(PaperStrategyBase.RESEARCH_ONLY, True)
        self.assertIs(PaperStrategyBase.NO_BROKER_CALL, True)

    def test_081_strategy_initial_status(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        s = self._make_strategy()
        self.assertEqual(s.status, StrategyStatus.REGISTERED)

    def test_082_strategy_start(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        s = self._make_strategy()
        s.start()
        self.assertEqual(s.status, StrategyStatus.RUNNING)

    def test_083_strategy_pause(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        s = self._make_strategy()
        s.start()
        s.pause()
        self.assertEqual(s.status, StrategyStatus.PAUSED)

    def test_084_strategy_halt(self):
        from paper_trading.strategy.enums_v162 import StrategyStatus
        s = self._make_strategy()
        s.halt()
        self.assertEqual(s.status, StrategyStatus.HALTED)

    def test_085_generate_signals_returns_list(self):
        s = self._make_strategy()
        signals = s.generate_signals()
        self.assertIsInstance(signals, list)
        self.assertGreater(len(signals), 0)

    def test_086_signals_paper_only(self):
        s = self._make_strategy()
        for sig in s.generate_signals():
            self.assertIs(sig.paper_only, True)
            self.assertIs(sig.not_a_real_order, True)

    def test_087_signals_no_short(self):
        s = self._make_strategy()
        forbidden = {"ENTRY_SHORT", "SELL_SHORT"}
        for sig in s.generate_signals():
            self.assertNotIn(sig.signal_type, forbidden)


class TestStrategyRegistry(unittest.TestCase):
    """Tests for strategy_registry_v162.py"""

    def setUp(self):
        from paper_trading.strategy.strategy_registry_v162 import reset_global_registry
        reset_global_registry()

    def _make_strategy(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config("test_strategy")
        return ThresholdFixtureStrategy(cfg)

    def test_100_registry_empty_initial(self):
        from paper_trading.strategy.strategy_registry_v162 import get_global_registry
        reg = get_global_registry()
        self.assertEqual(reg.count(), 0)

    def test_101_register_strategy(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s = self._make_strategy()
        sid = reg.register(s)
        self.assertEqual(sid, s.strategy_id)
        self.assertEqual(reg.count(), 1)

    def test_102_register_duplicate(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s = self._make_strategy()
        reg.register(s)
        reg.register(s)  # second registration should be no-op
        self.assertEqual(reg.count(), 1)

    def test_103_get_strategy(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s = self._make_strategy()
        reg.register(s)
        found = reg.get(s.strategy_id)
        self.assertIs(found, s)

    def test_104_get_unknown(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        self.assertIsNone(reg.get("nonexistent"))

    def test_105_is_registered(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s = self._make_strategy()
        self.assertFalse(reg.is_registered(s.strategy_id))
        reg.register(s)
        self.assertTrue(reg.is_registered(s.strategy_id))

    def test_106_unregister(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s = self._make_strategy()
        reg.register(s)
        ok = reg.unregister(s.strategy_id)
        self.assertTrue(ok)
        self.assertEqual(reg.count(), 0)

    def test_107_list_all(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s1 = self._make_strategy()
        s2 = self._make_strategy()
        reg.register(s1)
        reg.register(s2)
        listing = reg.list_all()
        self.assertEqual(len(listing), 2)
        self.assertTrue(all(item["paper_only"] is True for item in listing))

    def test_108_count_by_status(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        reg = StrategyRegistry()
        s = self._make_strategy()
        reg.register(s)
        counts = reg.count_by_status()
        self.assertEqual(counts.get("REGISTERED", 0), 1)

    def test_109_start_strategy(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        from paper_trading.strategy.enums_v162 import StrategyStatus
        reg = StrategyRegistry()
        s = self._make_strategy()
        reg.register(s)
        ok = reg.start_strategy(s.strategy_id)
        self.assertTrue(ok)
        self.assertEqual(s.status, StrategyStatus.RUNNING)

    def test_110_halt_all(self):
        from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
        from paper_trading.strategy.enums_v162 import StrategyStatus
        reg = StrategyRegistry()
        s = self._make_strategy()
        reg.register(s)
        s.start()
        count = reg.halt_all()
        self.assertEqual(count, 1)
        self.assertEqual(s.status, StrategyStatus.HALTED)


class TestStrategyConfig(unittest.TestCase):
    """Tests for strategy_config_v162.py"""

    def test_120_build_default_config(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        from paper_trading.strategy.enums_v162 import ApprovalMode, ConflictPolicy
        cfg = build_default_config("test")
        self.assertIs(cfg.paper_only, True)
        self.assertEqual(cfg.approval_mode, ApprovalMode.MANUAL_REQUIRED)
        self.assertEqual(cfg.conflict_policy, ConflictPolicy.MOST_CONSERVATIVE)

    def test_121_config_from_dict_safety_override(self):
        from paper_trading.strategy.strategy_config_v162 import config_from_dict
        d = {
            "strategy_name": "test",
            "paper_only": False,   # caller tries to disable — must be overridden
            "research_only": False,
        }
        cfg = config_from_dict(d)
        self.assertIs(cfg.paper_only, True)
        self.assertIs(cfg.research_only, True)

    def test_122_config_to_dict(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config, config_to_dict
        cfg = build_default_config("test")
        d = config_to_dict(cfg)
        self.assertIs(d["paper_only"], True)
        self.assertIs(d["not_a_real_order"], True)
        self.assertIn("strategy_name", d)
        self.assertIn("approval_mode", d)

    def test_123_no_short_in_allowed_types(self):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        cfg = build_default_config("test")
        self.assertNotIn("ENTRY_SHORT", cfg.allowed_signal_types)
        self.assertNotIn("SELL_SHORT", cfg.allowed_signal_types)


class TestStrategyState(unittest.TestCase):
    """Tests for strategy_state_v162.py"""

    def test_130_initial_state(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id")
        self.assertFalse(s.is_on_cooldown("2330.TW"))
        self.assertFalse(s.is_rate_limited())
        self.assertEqual(s.open_proposal_count(), 0)
        self.assertEqual(s.signal_count, 0)

    def test_131_cooldown_record_and_check(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id", cooldown_seconds=3600)
        self.assertFalse(s.is_on_cooldown("2330.TW"))
        s.record_decision("2330.TW")
        self.assertTrue(s.is_on_cooldown("2330.TW"))

    def test_132_cooldown_zero_seconds(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        import time
        s = StrategyState("test-id", cooldown_seconds=0)
        s.record_decision("2330.TW")
        self.assertFalse(s.is_on_cooldown("2330.TW"))

    def test_133_rate_limit_trigger(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id", max_signals_per_minute=3)
        for _ in range(3):
            s.record_signal()
        self.assertTrue(s.is_rate_limited())

    def test_134_rate_limit_below_threshold(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id", max_signals_per_minute=10)
        for _ in range(5):
            s.record_signal()
        self.assertFalse(s.is_rate_limited())

    def test_135_open_proposal_capacity(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id", max_open_proposals=2)
        self.assertTrue(s.add_open_proposal("p1"))
        self.assertTrue(s.add_open_proposal("p2"))
        self.assertFalse(s.add_open_proposal("p3"))  # at capacity
        self.assertTrue(s.at_proposal_capacity())

    def test_136_close_proposal(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id", max_open_proposals=2)
        s.add_open_proposal("p1")
        ok = s.close_proposal("p1")
        self.assertTrue(ok)
        self.assertFalse(s.at_proposal_capacity())

    def test_137_cooldown_snapshot_and_restore(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id", cooldown_seconds=3600)
        s.record_decision("2330.TW")
        snap = s.cooldown_snapshot()
        self.assertIn("2330.TW", snap)
        s2 = StrategyState("test-id-2", cooldown_seconds=3600)
        s2.restore_cooldown(snap)
        self.assertTrue(s2.is_on_cooldown("2330.TW"))

    def test_138_summary(self):
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        s = StrategyState("test-id")
        summary = s.summary()
        self.assertIn("strategy_id", summary)
        self.assertIn("signal_count", summary)


class TestSignalHelpers(unittest.TestCase):
    """Tests for signal_v162.py"""

    def test_150_make_entry_long(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        sig = make_entry_long("s1", "2330.TW", confidence=0.8)
        self.assertEqual(sig.signal_type, "ENTRY_LONG")
        self.assertIs(sig.paper_only, True)
        self.assertIs(sig.not_a_real_order, True)
        self.assertEqual(sig.confidence, 0.8)

    def test_151_make_exit_long(self):
        from paper_trading.strategy.signal_v162 import make_exit_long
        sig = make_exit_long("s1", "2330.TW")
        self.assertEqual(sig.signal_type, "EXIT_LONG")

    def test_152_make_hold(self):
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("s1", "2330.TW")
        self.assertEqual(sig.signal_type, "HOLD")

    def test_153_make_block(self):
        from paper_trading.strategy.signal_v162 import make_block
        sig = make_block("s1", "2330.TW", reason="test_block")
        self.assertEqual(sig.signal_type, "BLOCK")
        self.assertEqual(sig.metadata.get("reason"), "test_block")

    def test_154_make_alert(self):
        from paper_trading.strategy.signal_v162 import make_alert
        sig = make_alert("s1", "2330.TW", message="test_alert")
        self.assertEqual(sig.signal_type, "ALERT")

    def test_155_forbidden_signal_type_raises(self):
        # validate_signal_type returns (False, msg) for forbidden types — not ValueError.
        # make_signal raises ValueError when a SignalType with forbidden .value is passed,
        # but SignalType enum has no SHORT members so we test via validation directly.
        from paper_trading.strategy.validation_v162 import validate_signal_type
        ok, msg = validate_signal_type("ENTRY_SHORT")
        self.assertFalse(ok)
        self.assertIn("forbidden", msg.lower())

    def test_156_dedup_key_computed(self):
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("s1", "2330.TW")
        self.assertIsInstance(sig.dedup_key, str)
        self.assertGreater(len(sig.dedup_key), 0)

    def test_157_same_strategy_ticker_type_same_key(self):
        from paper_trading.strategy.signal_v162 import make_hold
        sig1 = make_hold("s1", "2330.TW")
        sig2 = make_hold("s1", "2330.TW")
        self.assertEqual(sig1.dedup_key, sig2.dedup_key)

    def test_158_different_ticker_different_key(self):
        from paper_trading.strategy.signal_v162 import make_hold
        sig1 = make_hold("s1", "2330.TW")
        sig2 = make_hold("s1", "2454.TW")
        self.assertNotEqual(sig1.dedup_key, sig2.dedup_key)

    def test_159_signal_to_dict(self):
        from paper_trading.strategy.signal_v162 import make_hold, signal_to_dict
        sig = make_hold("s1", "2330.TW")
        d = signal_to_dict(sig)
        self.assertIs(d["paper_only"], True)
        self.assertEqual(d["signal_type"], "HOLD")


class TestSignalNormalizer(unittest.TestCase):
    """Tests for signal_normalizer_v162.py"""

    def test_170_entry_long_strong_high_confidence(self):
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.enums_v162 import SignalStrength
        n = SignalNormalizer()
        sig = make_entry_long("s1", "2330.TW", confidence=1.0,
                              strength=SignalStrength.STRONG)
        n.normalize(sig)
        self.assertAlmostEqual(sig.normalized_value, 1.0, places=4)

    def test_171_exit_long_strong_high_confidence(self):
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        from paper_trading.strategy.signal_v162 import make_exit_long
        from paper_trading.strategy.enums_v162 import SignalStrength
        n = SignalNormalizer()
        sig = make_exit_long("s1", "2330.TW", confidence=1.0,
                             strength=SignalStrength.STRONG)
        n.normalize(sig)
        self.assertLess(sig.normalized_value, 0)

    def test_172_hold_normalized_zero(self):
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        from paper_trading.strategy.signal_v162 import make_hold
        n = SignalNormalizer()
        sig = make_hold("s1", "2330.TW")
        n.normalize(sig)
        self.assertAlmostEqual(sig.normalized_value, 0.0, places=6)

    def test_173_normalize_batch(self):
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        from paper_trading.strategy.signal_v162 import make_entry_long, make_hold
        n = SignalNormalizer()
        sigs = [make_entry_long("s1", "2330.TW"), make_hold("s1", "2454.TW")]
        n.normalize_batch(sigs)
        for sig in sigs:
            self.assertIsNotNone(sig.normalized_value)

    def test_174_normalized_in_range(self):
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        from paper_trading.strategy.signal_v162 import make_entry_long
        n = SignalNormalizer()
        for conf in (0.0, 0.25, 0.5, 0.75, 1.0):
            sig = make_entry_long("s1", "2330.TW", confidence=conf)
            n.normalize(sig)
            self.assertGreaterEqual(sig.normalized_value, -1.0)
            self.assertLessEqual(sig.normalized_value, 1.0)


class TestSignalDedup(unittest.TestCase):
    """Tests for signal_dedup_v162.py"""

    def test_180_first_signal_not_duplicate(self):
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        from paper_trading.strategy.signal_v162 import make_hold
        d = SignalDeduplicator()
        sig = make_hold("s1", "2330.TW")
        self.assertFalse(d.record(sig))
        self.assertFalse(sig.is_duplicate)

    def test_181_second_signal_is_duplicate(self):
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        from paper_trading.strategy.signal_v162 import make_hold
        d = SignalDeduplicator()
        sig = make_hold("s1", "2330.TW")
        d.record(sig)
        sig2 = make_hold("s1", "2330.TW")
        self.assertTrue(d.record(sig2))
        self.assertTrue(sig2.is_duplicate)

    def test_182_different_ticker_not_duplicate(self):
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        from paper_trading.strategy.signal_v162 import make_hold
        d = SignalDeduplicator()
        sig1 = make_hold("s1", "2330.TW")
        sig2 = make_hold("s1", "2454.TW")
        d.record(sig1)
        self.assertFalse(d.record(sig2))

    def test_183_filter_duplicates(self):
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        from paper_trading.strategy.signal_v162 import make_hold
        d = SignalDeduplicator()
        sigs = [make_hold("s1", "2330.TW"), make_hold("s1", "2330.TW"),
                make_hold("s1", "2454.TW")]
        result = d.filter_duplicates(sigs)
        self.assertEqual(len(result), 2)

    def test_184_reset_clears_cache(self):
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        from paper_trading.strategy.signal_v162 import make_hold
        d = SignalDeduplicator()
        sig = make_hold("s1", "2330.TW")
        d.record(sig)
        d.reset()
        self.assertEqual(d.cache_size(), 0)


class TestDecisionPipeline(unittest.TestCase):
    """Tests for decision_pipeline_v162.py"""

    def _make_context(self, approval_mode=None, ticker="2330.TW"):
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.decision_context_v162 import build_decision_context
        from paper_trading.strategy.enums_v162 import EligibilityResult, ApprovalMode
        am = approval_mode or ApprovalMode.AUTO_PAPER_ONLY
        cfg = build_default_config("pipeline_test", approval_mode=am)
        sig = make_entry_long(cfg.strategy_id, ticker, confidence=0.8)
        return build_decision_context(sig, cfg, eligibility=EligibilityResult.ELIGIBLE), sig

    def _run_pipeline(self, ctx, **kwargs):
        from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
        pl = DecisionPipeline()
        defaults = dict(is_registered=True, is_running=True,
                        data_quality_ok=True, pit_valid=True,
                        eligibility="ELIGIBLE", suggested_size=100.0,
                        is_market_open=True)
        defaults.update(kwargs)
        return pl.run(ctx, **defaults)

    def test_200_approved_all_pass(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx)
        self.assertEqual(result.outcome, DecisionOutcome.APPROVED.value)

    def test_201_rejected_not_registered(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, is_registered=False)
        self.assertEqual(result.outcome, DecisionOutcome.PIPELINE_ERROR.value)
        self.assertEqual(result.pipeline_steps_completed, 1)

    def test_202_rejected_not_running(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, is_running=False)
        self.assertEqual(result.outcome, DecisionOutcome.BLOCKED.value)

    def test_203_rejected_duplicate(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, is_duplicate=True)
        self.assertEqual(result.outcome, DecisionOutcome.DUPLICATE.value)
        self.assertEqual(result.pipeline_steps_completed, 3)

    def test_204_rejected_cooldown(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, is_on_cooldown=True)
        self.assertEqual(result.outcome, DecisionOutcome.COOLDOWN.value)

    def test_205_rejected_rate_limited(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, is_rate_limited=True)
        self.assertEqual(result.outcome, DecisionOutcome.RATE_LIMITED.value)

    def test_206_rejected_data_stale(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, data_quality_ok=False)
        self.assertEqual(result.outcome, DecisionOutcome.DATA_STALE.value)

    def test_207_rejected_pit_invalid(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, pit_valid=False)
        self.assertEqual(result.outcome, DecisionOutcome.DATA_STALE.value)

    def test_208_rejected_ineligible(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, eligibility="INELIGIBLE")
        self.assertEqual(result.outcome, DecisionOutcome.INELIGIBLE.value)

    def test_209_rejected_sizing_zero(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, suggested_size=0.0)
        self.assertEqual(result.outcome, DecisionOutcome.SIZING_ZERO.value)

    def test_210_rejected_correlation_breach(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, correlation_breach=True)
        self.assertEqual(result.outcome, DecisionOutcome.RISK_BLOCKED.value)

    def test_211_rejected_risk_blocked(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, risk_blocked=True)
        self.assertEqual(result.outcome, DecisionOutcome.RISK_BLOCKED.value)

    def test_212_rejected_conflict(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, conflict_detected=True)
        self.assertEqual(result.outcome, DecisionOutcome.CONFLICT.value)

    def test_213_deferred_manual_required(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome, ApprovalMode
        ctx, _ = self._make_context(approval_mode=ApprovalMode.MANUAL_REQUIRED)
        result = self._run_pipeline(ctx)
        self.assertEqual(result.outcome, DecisionOutcome.DEFERRED.value)

    def test_214_result_safety_flags(self):
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx)
        self.assertIs(result.paper_only, True)
        self.assertIs(result.not_a_real_order, True)
        self.assertIs(result.no_broker_call, True)

    def test_215_pipeline_log_populated(self):
        ctx, _ = self._make_context()
        self._run_pipeline(ctx)
        self.assertGreater(len(ctx.pipeline_log), 0)

    def test_216_at_proposal_capacity_blocked(self):
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ctx, _ = self._make_context()
        result = self._run_pipeline(ctx, at_proposal_capacity=True)
        self.assertEqual(result.outcome, DecisionOutcome.BLOCKED.value)


class TestEligibilityAdapter(unittest.TestCase):
    """Tests for eligibility_adapter_v162.py"""

    def test_230_default_eligible(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
        from paper_trading.strategy.enums_v162 import EligibilityResult
        ea = EligibilityAdapter()
        self.assertEqual(ea.check("2330.TW"), EligibilityResult.ELIGIBLE)

    def test_231_blocked_ticker_ineligible(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
        from paper_trading.strategy.enums_v162 import EligibilityResult
        ea = EligibilityAdapter(blocked_tickers={"BLOCKED.TW"})
        self.assertEqual(ea.check("BLOCKED.TW"), EligibilityResult.INELIGIBLE)

    def test_232_block_unblock(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
        from paper_trading.strategy.enums_v162 import EligibilityResult
        ea = EligibilityAdapter()
        ea.block_ticker("2330.TW")
        self.assertEqual(ea.check("2330.TW"), EligibilityResult.INELIGIBLE)
        ea.unblock_ticker("2330.TW")
        self.assertEqual(ea.check("2330.TW"), EligibilityResult.ELIGIBLE)

    def test_233_allow_list_restricts(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
        from paper_trading.strategy.enums_v162 import EligibilityResult
        ea = EligibilityAdapter(allowed_tickers={"2330.TW"})
        self.assertEqual(ea.check("2330.TW"), EligibilityResult.ELIGIBLE)
        self.assertEqual(ea.check("2454.TW"), EligibilityResult.INELIGIBLE)

    def test_234_min_confidence_gate(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
        from paper_trading.strategy.enums_v162 import EligibilityResult
        ea = EligibilityAdapter(min_confidence=0.7)
        self.assertEqual(ea.check("2330.TW", confidence=0.5), EligibilityResult.INELIGIBLE)
        self.assertEqual(ea.check("2330.TW", confidence=0.9), EligibilityResult.ELIGIBLE)

    def test_235_stats(self):
        from paper_trading.strategy.eligibility_adapter_v162 import EligibilityAdapter
        ea = EligibilityAdapter()
        ea.check("2330.TW")
        stats = ea.stats()
        self.assertEqual(stats["check_count"], 1)
        self.assertIs(stats["paper_only"], True)


class TestSizingAdapter(unittest.TestCase):
    """Tests for sizing_adapter_v162.py"""

    def test_240_compute_fallback(self):
        from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
        from paper_trading.strategy.signal_v162 import make_entry_long
        sa = SizingAdapter(fixed_size=100.0, use_portfolio_sizing=False)
        sig = make_entry_long("s1", "2330.TW", confidence=1.0)
        size = sa.compute(sig)
        self.assertIsNotNone(size)
        self.assertGreater(size, 0)

    def test_241_max_size_clamp(self):
        from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
        from paper_trading.strategy.signal_v162 import make_entry_long
        sa = SizingAdapter(fixed_size=50000.0, max_size=1000.0, use_portfolio_sizing=False)
        sig = make_entry_long("s1", "2330.TW", confidence=1.0)
        size = sa.compute(sig)
        self.assertLessEqual(size, 1000.0)

    def test_242_confidence_scales_size(self):
        from paper_trading.strategy.sizing_adapter_v162 import SizingAdapter
        from paper_trading.strategy.signal_v162 import make_entry_long
        sa = SizingAdapter(fixed_size=100.0, use_portfolio_sizing=False)
        sig_low = make_entry_long("s1", "2330.TW", confidence=0.2)
        sig_high = make_entry_long("s1", "2330.TW", confidence=0.8)
        self.assertLess(sa.compute(sig_low), sa.compute(sig_high))


class TestCorrelationAdapter(unittest.TestCase):
    """Tests for correlation_adapter_v162.py"""

    def test_250_no_breach_by_default(self):
        from paper_trading.strategy.correlation_adapter_v162 import CorrelationAdapter
        ca = CorrelationAdapter(use_portfolio_correlation=False)
        self.assertFalse(ca.check_breach("2330.TW"))

    def test_251_stats_research_only(self):
        from paper_trading.strategy.correlation_adapter_v162 import CorrelationAdapter
        ca = CorrelationAdapter(use_portfolio_correlation=False)
        ca.check_breach("2330.TW")
        stats = ca.stats()
        self.assertIs(stats["paper_only"], True)
        self.assertIs(stats["research_only"], True)


class TestRiskAdapter(unittest.TestCase):
    """Tests for risk_adapter_v162.py"""

    def test_260_no_block_by_default(self):
        from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
        ra = RiskAdapter(use_portfolio_risk=False)
        self.assertFalse(ra.is_blocked("2330.TW"))

    def test_261_drawdown_gate(self):
        from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
        ra = RiskAdapter(max_drawdown_pct=0.10, use_portfolio_risk=False)
        self.assertTrue(ra.is_blocked("2330.TW", current_drawdown_pct=0.15))

    def test_262_position_count_gate(self):
        from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
        ra = RiskAdapter(max_positions=5, use_portfolio_risk=False)
        self.assertTrue(ra.is_blocked("2330.TW", open_position_count=5))

    def test_263_stats_paper_only(self):
        from paper_trading.strategy.risk_adapter_v162 import RiskAdapter
        ra = RiskAdapter(use_portfolio_risk=False)
        self.assertIs(ra.stats()["paper_only"], True)


class TestApprovalPolicy(unittest.TestCase):
    """Tests for approval_v162.py"""

    def _deferred_result(self):
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        return DecisionResult(
            outcome=DecisionOutcome.DEFERRED.value,
            paper_only=True, research_only=True, simulation_only=True,
            not_a_real_order=True, no_broker_call=True,
        )

    def test_270_submit_for_approval(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        ap = ApprovalPolicy()
        r = self._deferred_result()
        ap.submit_for_approval(r)
        self.assertEqual(ap.pending_count(), 1)

    def test_271_manual_approve(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ap = ApprovalPolicy()
        r = self._deferred_result()
        ap.submit_for_approval(r)
        ok, reason = ap.approve(r.decision_id)
        self.assertTrue(ok)
        self.assertEqual(r.outcome, DecisionOutcome.APPROVED.value)
        self.assertEqual(ap.pending_count(), 0)

    def test_272_deny(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        ap = ApprovalPolicy()
        r = self._deferred_result()
        ap.submit_for_approval(r)
        ok, _ = ap.deny(r.decision_id, reason="test_deny")
        self.assertTrue(ok)
        self.assertEqual(r.outcome, DecisionOutcome.REJECTED.value)

    def test_273_approve_unknown_id(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        ap = ApprovalPolicy()
        ok, reason = ap.approve("nonexistent")
        self.assertFalse(ok)

    def test_274_auto_approve_safety_check(self):
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        from paper_trading.strategy.enums_v162 import DecisionOutcome, ApprovalMode
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        ap = ApprovalPolicy()
        r = self._deferred_result()
        cfg = build_default_config("test", approval_mode=ApprovalMode.AUTO_PAPER_ONLY)
        approved = ap.auto_approve(r, cfg)
        self.assertTrue(approved)
        self.assertEqual(r.outcome, DecisionOutcome.APPROVED.value)


class TestConflictResolver(unittest.TestCase):
    """Tests for conflict_resolution_v162.py"""

    def test_280_no_conflict(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long, make_hold
        cr = ConflictResolver()
        sigs = [make_entry_long("s1", "2330.TW"), make_hold("s1", "2454.TW")]
        resolved, log = cr.resolve(sigs)
        self.assertEqual(len(resolved), 2)
        self.assertEqual(len(log), 0)

    def test_281_conflict_most_conservative(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
        from paper_trading.strategy.enums_v162 import ConflictPolicy
        cr = ConflictResolver(ConflictPolicy.MOST_CONSERVATIVE)
        sigs = [make_entry_long("s1", "2330.TW"), make_exit_long("s1", "2330.TW")]
        resolved, log = cr.resolve(sigs)
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0].signal_type, "EXIT_LONG")

    def test_282_conflict_block_all(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
        from paper_trading.strategy.enums_v162 import ConflictPolicy
        cr = ConflictResolver(ConflictPolicy.BLOCK_ALL)
        sigs = [make_entry_long("s1", "2330.TW"), make_exit_long("s1", "2330.TW")]
        resolved, log = cr.resolve(sigs)
        self.assertEqual(len(resolved), 0)

    def test_283_conflict_first_wins(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
        from paper_trading.strategy.enums_v162 import ConflictPolicy
        cr = ConflictResolver(ConflictPolicy.FIRST_WINS)
        sigs = [make_entry_long("s1", "2330.TW"), make_exit_long("s1", "2330.TW")]
        resolved, log = cr.resolve(sigs)
        self.assertEqual(resolved[0].signal_type, "ENTRY_LONG")

    def test_284_has_conflict(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
        cr = ConflictResolver()
        sigs = [make_entry_long("s1", "2330.TW"), make_exit_long("s1", "2330.TW")]
        self.assertTrue(cr.has_conflict(sigs))

    def test_285_conflicting_tickers(self):
        from paper_trading.strategy.conflict_resolution_v162 import ConflictResolver
        from paper_trading.strategy.signal_v162 import make_entry_long, make_exit_long
        cr = ConflictResolver()
        sigs = [make_entry_long("s1", "2330.TW"), make_exit_long("s1", "2330.TW")]
        tickers = cr.conflicting_tickers(sigs)
        self.assertIn("2330.TW", tickers)


class TestCooldownManager(unittest.TestCase):
    """Tests for cooldown_v162.py"""

    def test_290_not_on_cooldown_initially(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager()
        self.assertFalse(cm.is_on_cooldown("2330.TW"))

    def test_291_on_cooldown_after_record(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=3600)
        cm.record("2330.TW")
        self.assertTrue(cm.is_on_cooldown("2330.TW"))

    def test_292_check_and_record_allows_first(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=3600)
        blocked = cm.check_and_record("2330.TW")
        self.assertFalse(blocked)

    def test_293_check_and_record_blocks_second(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=3600)
        cm.check_and_record("2330.TW")
        blocked = cm.check_and_record("2330.TW")
        self.assertTrue(blocked)

    def test_294_clear(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=3600)
        cm.record("2330.TW")
        cm.clear("2330.TW")
        self.assertFalse(cm.is_on_cooldown("2330.TW"))

    def test_295_snapshot_restore(self):
        from paper_trading.strategy.cooldown_v162 import CooldownManager
        cm = CooldownManager(cooldown_seconds=3600)
        cm.record("2330.TW")
        snap = cm.snapshot()
        cm2 = CooldownManager(cooldown_seconds=3600)
        cm2.restore(snap)
        self.assertTrue(cm2.is_on_cooldown("2330.TW"))


class TestRateLimiter(unittest.TestCase):
    """Tests for rate_limit_v162.py"""

    def test_300_not_limited_initially(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=10)
        self.assertFalse(rl.is_limited())

    def test_301_acquire_succeeds_within_limit(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=5)
        for _ in range(5):
            self.assertTrue(rl.try_acquire())

    def test_302_acquire_fails_at_limit(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=3)
        for _ in range(3):
            rl.try_acquire()
        self.assertFalse(rl.try_acquire())

    def test_303_current_rate(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=10)
        for _ in range(4):
            rl.try_acquire()
        self.assertEqual(rl.current_rate(), 4)

    def test_304_headroom(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=10)
        for _ in range(3):
            rl.try_acquire()
        self.assertEqual(rl.headroom(), 7)

    def test_305_stats(self):
        from paper_trading.strategy.rate_limit_v162 import RateLimiter
        rl = RateLimiter(max_per_minute=5)
        rl.try_acquire()
        stats = rl.stats()
        self.assertIs(stats["paper_only"], True)
        self.assertEqual(stats["total_allowed"], 1)


class TestProposalBuilder(unittest.TestCase):
    """Tests for proposal_v162.py"""

    def _make_approved_decision(self):
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        return DecisionResult(
            strategy_id="s1", ticker="2330.TW", signal_id="sig1",
            outcome=DecisionOutcome.APPROVED.value,
            pipeline_steps_completed=16,
            paper_only=True, research_only=True, simulation_only=True,
            not_a_real_order=True, no_broker_call=True,
        )

    def test_310_build_proposal(self):
        from paper_trading.strategy.proposal_v162 import build_proposal
        from paper_trading.strategy.signal_v162 import make_entry_long
        sig = make_entry_long("s1", "2330.TW", confidence=0.8)
        decision = self._make_approved_decision()
        proposal = build_proposal(decision, sig, suggested_size=100.0)
        self.assertIs(proposal.paper_only, True)
        self.assertIs(proposal.not_a_real_order, True)
        self.assertEqual(proposal.proposed_size, 100.0)

    def test_311_proposal_safety_flags(self):
        from paper_trading.strategy.proposal_v162 import build_proposal
        from paper_trading.strategy.signal_v162 import make_entry_long
        sig = make_entry_long("s1", "2330.TW")
        decision = self._make_approved_decision()
        p = build_proposal(decision, sig, suggested_size=50.0)
        self.assertIs(p.no_formal_portfolio_ledger_write, True)
        self.assertIs(p.no_real_account, True)
        self.assertIs(p.no_broker_call, True)

    def test_312_proposal_to_dict(self):
        from paper_trading.strategy.proposal_v162 import build_proposal, proposal_to_dict
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("s1", "2330.TW")
        decision = self._make_approved_decision()
        p = build_proposal(decision, sig, suggested_size=100.0)
        d = proposal_to_dict(p)
        self.assertIs(d["paper_only"], True)
        self.assertIs(d["not_a_real_order"], True)


class TestOrderBridge(unittest.TestCase):
    """Tests for order_bridge_v162.py"""

    def test_320_safety_constants(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        self.assertIs(PaperOrderBridge.BROKER_CONNECTED, False)
        self.assertIs(PaperOrderBridge.REAL_ORDERS_ENABLED, False)
        self.assertIs(PaperOrderBridge.PRODUCTION_ENABLED, False)

    def test_321_stats_paper_only(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        bridge = PaperOrderBridge()
        stats = bridge.stats()
        self.assertIs(stats["paper_only"], True)
        self.assertIs(stats["broker_connected"], False)

    def test_322_submit_validates_safety(self):
        from paper_trading.strategy.order_bridge_v162 import PaperOrderBridge
        from paper_trading.strategy.models_v162 import PaperOrderProposal
        bridge = PaperOrderBridge()
        # Build a proposal with paper_only=False (should be rejected)
        # Note: PaperOrderProposal.__post_init__ will raise, so we patch
        p = PaperOrderProposal.__new__(PaperOrderProposal)
        object.__setattr__(p, "paper_only", False)
        object.__setattr__(p, "research_only", True)
        object.__setattr__(p, "simulation_only", True)
        object.__setattr__(p, "not_a_real_order", True)
        object.__setattr__(p, "no_broker_call", True)
        object.__setattr__(p, "no_real_account", True)
        object.__setattr__(p, "no_formal_portfolio_ledger_write", True)
        object.__setattr__(p, "proposal_id", "test-bad")
        object.__setattr__(p, "status", "PENDING")
        ok, reason = bridge.submit(p)
        self.assertFalse(ok)


class TestJournal(unittest.TestCase):
    """Tests for journal_v162.py"""

    def test_330_record_and_count(self):
        from paper_trading.strategy.journal_v162 import StrategyJournal
        from paper_trading.strategy.enums_v162 import JournalEventType
        j = StrategyJournal("test-strategy")
        j.record(JournalEventType.STRATEGY_REGISTERED, "registered")
        j.record(JournalEventType.SIGNAL_RECEIVED, "signal")
        self.assertEqual(j.count(), 2)

    def test_331_filter_by_event_type(self):
        from paper_trading.strategy.journal_v162 import StrategyJournal
        from paper_trading.strategy.enums_v162 import JournalEventType
        j = StrategyJournal("test-strategy")
        j.record(JournalEventType.STRATEGY_REGISTERED, "registered")
        j.record(JournalEventType.SIGNAL_RECEIVED, "signal")
        entries = j.entries(event_type=JournalEventType.SIGNAL_RECEIVED)
        self.assertEqual(len(entries), 1)

    def test_332_tail(self):
        from paper_trading.strategy.journal_v162 import StrategyJournal
        from paper_trading.strategy.enums_v162 import JournalEventType
        j = StrategyJournal("test-strategy")
        for i in range(5):
            j.record(JournalEventType.SIGNAL_RECEIVED, f"signal {i}")
        tail = j.tail(3)
        self.assertEqual(len(tail), 3)

    def test_333_summary_paper_only(self):
        from paper_trading.strategy.journal_v162 import StrategyJournal
        j = StrategyJournal("test-strategy")
        summary = j.summary()
        self.assertIs(summary["paper_only"], True)
        self.assertIs(summary["research_only"], True)


class TestCheckpointManager(unittest.TestCase):
    """Tests for checkpoint_v162.py"""

    def test_340_save_and_latest(self):
        from paper_trading.strategy.checkpoint_v162 import CheckpointManager
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            cm = CheckpointManager("test-strategy", checkpoint_dir=tmpdir)
            state = StrategyState("test-strategy")
            state.signal_count = 5
            cp = cm.save(state)
            self.assertEqual(cp.signal_count, 5)
            latest = cm.latest()
            self.assertIsNotNone(latest)
            self.assertEqual(latest.signal_count, 5)

    def test_341_restore_to_state(self):
        from paper_trading.strategy.checkpoint_v162 import CheckpointManager
        from paper_trading.strategy.strategy_state_v162 import StrategyState
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            cm = CheckpointManager("test-strategy", checkpoint_dir=tmpdir)
            state = StrategyState("test-strategy")
            state.signal_count = 42
            cp = cm.save(state)
            state2 = StrategyState("test-strategy")
            cm.restore_to_state(state2, cp)
            self.assertEqual(state2.signal_count, 42)


class TestReplaySession(unittest.TestCase):
    """Tests for replay_v162.py"""

    def test_350_empty_replay(self):
        from paper_trading.strategy.replay_v162 import ReplaySession
        rs = ReplaySession("test-strategy", [])
        summary = rs.run_all()
        self.assertTrue(summary["complete"])
        self.assertEqual(summary["replayed"], 0)
        self.assertIs(summary["paper_only"], True)

    def test_351_replay_signals(self):
        from paper_trading.strategy.replay_v162 import ReplaySession
        from paper_trading.strategy.signal_v162 import make_hold, make_entry_long
        results = []
        sigs = [make_hold("s1", "2330.TW"), make_entry_long("s1", "2454.TW")]
        rs = ReplaySession("s1", sigs, replay_handler=lambda s: results.append(s))
        summary = rs.run_all()
        self.assertEqual(summary["replayed"], 2)
        self.assertEqual(len(results), 2)

    def test_352_replay_marks_trigger_as_replay(self):
        from paper_trading.strategy.replay_v162 import ReplaySession
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("s1", "2330.TW")
        rs = ReplaySession("s1", [sig])
        rs.run_all()
        self.assertEqual(sig.trigger_type, "REPLAY")

    def test_353_build_replay_from_dicts(self):
        from paper_trading.strategy.replay_v162 import build_replay_session
        dicts = [
            {"ticker": "2330.TW", "signal_type": "ENTRY_LONG", "confidence": 0.8},
            {"ticker": "2454.TW", "signal_type": "HOLD", "confidence": 0.5},
        ]
        rs = build_replay_session("s1", dicts)
        summary = rs.run_all()
        self.assertEqual(summary["replayed"], 2)


class TestLineageTracker(unittest.TestCase):
    """Tests for lineage_v162.py"""

    def _make_signal_decision(self):
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        sig = make_entry_long("s1", "2330.TW", confidence=0.8)
        dec = DecisionResult(
            strategy_id="s1", ticker="2330.TW", signal_id=sig.signal_id,
            outcome=DecisionOutcome.APPROVED.value, pipeline_steps_completed=16,
            paper_only=True, research_only=True, simulation_only=True,
            not_a_real_order=True, no_broker_call=True,
        )
        return sig, dec

    def test_360_record_lineage(self):
        from paper_trading.strategy.lineage_v162 import LineageTracker
        lt = LineageTracker()
        sig, dec = self._make_signal_decision()
        rec = lt.record(sig, dec)
        self.assertEqual(lt.count(), 1)
        self.assertEqual(rec.outcome, "APPROVED")

    def test_361_reproducibility_hash(self):
        from paper_trading.strategy.lineage_v162 import LineageTracker
        lt = LineageTracker()
        sig, dec = self._make_signal_decision()
        rec = lt.record(sig, dec)
        self.assertIsInstance(rec.reproducibility_hash, str)
        self.assertGreater(len(rec.reproducibility_hash), 0)

    def test_362_find_by_signal(self):
        from paper_trading.strategy.lineage_v162 import LineageTracker
        lt = LineageTracker()
        sig, dec = self._make_signal_decision()
        lt.record(sig, dec)
        found = lt.find_by_signal(sig.signal_id)
        self.assertEqual(len(found), 1)

    def test_363_find_by_ticker(self):
        from paper_trading.strategy.lineage_v162 import LineageTracker
        lt = LineageTracker()
        sig, dec = self._make_signal_decision()
        lt.record(sig, dec)
        found = lt.find_by_ticker("2330.TW")
        self.assertEqual(len(found), 1)

    def test_364_summary(self):
        from paper_trading.strategy.lineage_v162 import LineageTracker
        lt = LineageTracker()
        sig, dec = self._make_signal_decision()
        lt.record(sig, dec)
        s = lt.summary()
        self.assertEqual(s["total_records"], 1)
        self.assertIs(s["paper_only"], True)


class TestReproducibilityVerifier(unittest.TestCase):
    """Tests for reproducibility_v162.py"""

    def test_370_same_decision_passes(self):
        from paper_trading.strategy.reproducibility_v162 import ReproducibilityVerifier
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        rv = ReproducibilityVerifier()
        sig = make_entry_long("s1", "2330.TW", confidence=0.8)
        dec = DecisionResult(
            strategy_id="s1", ticker="2330.TW", signal_id=sig.signal_id,
            outcome=DecisionOutcome.APPROVED.value, pipeline_steps_completed=16,
            paper_only=True, research_only=True, simulation_only=True,
            not_a_real_order=True, no_broker_call=True,
        )
        ok, detail = rv.verify(sig, dec, dec)
        self.assertTrue(ok)

    def test_371_safety_invariant_check(self):
        from paper_trading.strategy.reproducibility_v162 import ReproducibilityVerifier
        from paper_trading.strategy.models_v162 import DecisionResult
        rv = ReproducibilityVerifier()
        dec = DecisionResult(
            paper_only=True, research_only=True, simulation_only=True,
            not_a_real_order=True, no_broker_call=True,
        )
        ok, violations = rv.verify_safety_invariants(dec)
        self.assertTrue(ok)
        self.assertEqual(len(violations), 0)

    def test_372_compute_signal_hash_deterministic(self):
        from paper_trading.strategy.reproducibility_v162 import compute_signal_hash
        from paper_trading.strategy.signal_v162 import make_hold
        sig = make_hold("s1", "2330.TW")
        h1 = compute_signal_hash(sig)
        h2 = compute_signal_hash(sig)
        self.assertEqual(h1, h2)


class TestDecisionExplainer(unittest.TestCase):
    """Tests for explain_v162.py"""

    def test_380_explain_approved(self):
        from paper_trading.strategy.explain_v162 import DecisionExplainer
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        de = DecisionExplainer()
        dec = DecisionResult(
            ticker="2330.TW", outcome=DecisionOutcome.APPROVED.value,
            paper_only=True, not_a_real_order=True, no_broker_call=True,
            research_only=True, simulation_only=True,
        )
        exp = de.explain_decision(dec)
        self.assertEqual(exp["outcome"], "APPROVED")
        self.assertIs(exp["paper_only"], True)
        self.assertIs(exp["not_investment_advice"], True)

    def test_381_conditions_for_deferred(self):
        from paper_trading.strategy.explain_v162 import DecisionExplainer
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        de = DecisionExplainer()
        dec = DecisionResult(
            outcome=DecisionOutcome.DEFERRED.value,
            paper_only=True, not_a_real_order=True, no_broker_call=True,
            research_only=True, simulation_only=True,
        )
        exp = de.explain_decision(dec)
        self.assertGreater(len(exp["conditions_for_approval"]), 0)

    def test_382_narrative_contains_disclaimer(self):
        from paper_trading.strategy.explain_v162 import DecisionExplainer
        from paper_trading.strategy.models_v162 import DecisionResult
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        de = DecisionExplainer()
        dec = DecisionResult(
            outcome=DecisionOutcome.REJECTED.value,
            paper_only=True, not_a_real_order=True, no_broker_call=True,
            research_only=True, simulation_only=True,
        )
        exp = de.explain_decision(dec)
        self.assertIn("NOT INVESTMENT ADVICE", exp["narrative"])


class TestStoreAndQuery(unittest.TestCase):
    """Tests for store_v162.py and query_v162.py"""

    def test_390_store_and_retrieve_signal(self):
        from paper_trading.strategy.store_v162 import PaperStrategyStore
        from paper_trading.strategy.signal_v162 import make_hold
        store = PaperStrategyStore()
        sig = make_hold("s1", "2330.TW")
        store.save_signal(sig)
        found = store.get_signal(sig.signal_id)
        self.assertIs(found, sig)

    def test_391_store_and_list_proposals(self):
        from paper_trading.strategy.store_v162 import PaperStrategyStore
        from paper_trading.strategy.models_v162 import PaperOrderProposal
        store = PaperStrategyStore()
        p = PaperOrderProposal(ticker="2330.TW", proposed_size=100.0)
        store.save_proposal(p)
        props = store.list_proposals()
        self.assertEqual(len(props), 1)

    def test_392_query_full_summary(self):
        from paper_trading.strategy.store_v162 import PaperStrategyStore
        from paper_trading.strategy.query_v162 import PaperStrategyQueryService
        store = PaperStrategyStore()
        qs = PaperStrategyQueryService(store)
        summary = qs.full_summary()
        self.assertIs(summary["paper_only"], True)
        self.assertIs(summary["not_investment_advice"], True)

    def test_393_query_outcome_distribution_empty(self):
        from paper_trading.strategy.store_v162 import PaperStrategyStore
        from paper_trading.strategy.query_v162 import PaperStrategyQueryService
        store = PaperStrategyStore()
        qs = PaperStrategyQueryService(store)
        dist = qs.outcome_distribution()
        self.assertIsInstance(dist, dict)

    def test_394_store_summary(self):
        from paper_trading.strategy.store_v162 import PaperStrategyStore
        store = PaperStrategyStore()
        summary = store.summary()
        self.assertIs(summary["paper_only"], True)
        self.assertIs(summary["research_only"], True)


class TestHealthCheck(unittest.TestCase):
    """Tests for health_v162.py"""

    def test_400_health_runs(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        result = PaperStrategyOrchestrationHealthCheck().run()
        self.assertIn("status", result)
        self.assertIn("passed", result)
        self.assertIn("failed", result)
        self.assertIn("total", result)
        self.assertIn("checks", result)

    def test_401_health_paper_only(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        result = PaperStrategyOrchestrationHealthCheck().run()
        self.assertIs(result["paper_only"], True)
        self.assertIs(result["no_real_orders"], True)
        self.assertIs(result["broker_enabled"], False)

    def test_402_health_all_pass(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        result = PaperStrategyOrchestrationHealthCheck().run()
        failed_checks = [c for c in result["checks"] if not c["ok"]]
        self.assertEqual(len(failed_checks), 0,
                         f"Failed health checks: {[c['name'] for c in failed_checks]}")

    def test_403_health_status_healthy(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        result = PaperStrategyOrchestrationHealthCheck().run()
        self.assertEqual(result["status"], "HEALTHY")

    def test_404_health_check_count(self):
        from paper_trading.strategy.health_v162 import PaperStrategyOrchestrationHealthCheck
        result = PaperStrategyOrchestrationHealthCheck().run()
        self.assertGreaterEqual(result["total"], 34)


class TestReleaseGate(unittest.TestCase):
    """Tests for paper_strategy_orchestration_release_gate_v162.py"""

    def test_410_gate_runs(self):
        from release.paper_strategy_orchestration_release_gate_v162 import run_gate
        result = run_gate()
        self.assertIn("all_pass", result)
        self.assertIn("checks", result)
        self.assertIs(result["paper_only"], True)
        self.assertIs(result["no_real_orders"], True)

    def test_411_gate_all_pass(self):
        from release.paper_strategy_orchestration_release_gate_v162 import run_gate
        result = run_gate()
        if not result["all_pass"]:
            self.fail(f"Release gate failed: {result['blocked']}")

    def test_412_gate_version(self):
        result = {}
        from release.paper_strategy_orchestration_release_gate_v162 import _GATE_VERSION, _GATE_NAME
        self.assertEqual(_GATE_VERSION, "1.6.2")
        self.assertEqual(_GATE_NAME, "Paper Strategy Orchestration")


class TestGUIPanel(unittest.TestCase):
    """Tests for gui/paper_strategy_orchestration_panel.py"""

    def test_420_panel_importable(self):
        import gui.paper_strategy_orchestration_panel as p
        self.assertTrue(hasattr(p, "PaperStrategyOrchestrationPanel"))

    def test_421_panel_render(self):
        from gui.paper_strategy_orchestration_panel import PaperStrategyOrchestrationPanel
        panel = PaperStrategyOrchestrationPanel()
        data = panel.render()
        self.assertIn("title", data)
        self.assertIs(data["paper_only"], True)
        self.assertIs(data["not_investment_advice"], True)

    def test_422_panel_text_summary(self):
        from gui.paper_strategy_orchestration_panel import PaperStrategyOrchestrationPanel
        panel = PaperStrategyOrchestrationPanel()
        text = panel.format_text_summary()
        self.assertIn("Paper Strategy Orchestration", text)
        self.assertIn("PAPER STRATEGY ONLY", text)


class TestReport(unittest.TestCase):
    """Tests for reports/paper_strategy_orchestration_report.py"""

    def test_430_report_generates(self):
        from reports.paper_strategy_orchestration_report import PaperStrategyOrchestrationReport
        r = PaperStrategyOrchestrationReport()
        report = r.generate()
        self.assertEqual(report["version"], "1.6.2")
        self.assertIs(report["safety_verification"]["paper_only"], True)
        self.assertIs(report["safety_verification"]["broker_execution_enabled"], False)

    def test_431_report_disclaimer(self):
        from reports.paper_strategy_orchestration_report import PaperStrategyOrchestrationReport
        r = PaperStrategyOrchestrationReport()
        report = r.generate()
        self.assertIn("NOT INVESTMENT ADVICE", report["disclaimer"])

    def test_432_report_format_text(self):
        from reports.paper_strategy_orchestration_report import PaperStrategyOrchestrationReport
        r = PaperStrategyOrchestrationReport()
        report = r.generate()
        text = r.format_text(report)
        self.assertIn("PAPER STRATEGY ORCHESTRATION REPORT", text)
        self.assertIn("SAFETY VERIFICATION", text)


class TestVersionInfo(unittest.TestCase):
    """Tests for version_info.py v1.6.2 constants"""

    def test_440_version_is_162(self):
        from release.version_info import VERSION
        self.assertEqual(VERSION, "1.6.2")

    def test_441_release_name(self):
        from release.version_info import RELEASE_NAME
        self.assertEqual(RELEASE_NAME, "Paper Strategy Orchestration")

    def test_442_baseline(self):
        from release.version_info import PAPER_STRATEGY_ORCHESTRATION_BASELINE
        self.assertEqual(PAPER_STRATEGY_ORCHESTRATION_BASELINE, "1.6.2")

    def test_443_base_release(self):
        from release.version_info import BASE_RELEASE
        self.assertIn("1.6.1", BASE_RELEASE)

    def test_444_safety_flags(self):
        from release.version_info import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            PAPER_STRATEGY_RESEARCH_ONLY, REAL_STRATEGY_EXECUTION_ENABLED,
            AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED,
        )
        self.assertIs(NO_REAL_ORDERS, True)
        self.assertIs(BROKER_EXECUTION_ENABLED, False)
        self.assertIs(PRODUCTION_TRADING_BLOCKED, True)
        self.assertIs(PAPER_STRATEGY_RESEARCH_ONLY, True)
        self.assertIs(REAL_STRATEGY_EXECUTION_ENABLED, False)
        self.assertIs(AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED, False)

    def test_445_no_short_selling(self):
        from release.version_info import SHORT_SELLING_ENABLED, MARGIN_ENABLED
        self.assertIs(SHORT_SELLING_ENABLED, False)
        self.assertIs(MARGIN_ENABLED, False)

    def test_446_paper_strategy_available(self):
        from release.version_info import PAPER_STRATEGY_ORCHESTRATION_AVAILABLE
        self.assertIs(PAPER_STRATEGY_ORCHESTRATION_AVAILABLE, True)

    def test_447_auto_paper_only_disabled_by_default(self):
        from release.version_info import AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT
        self.assertIs(AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT, False)


class TestFixtureFiles(unittest.TestCase):
    """Tests that fixture JSON files are valid and safe"""

    def _fixture_path(self, name):
        return os.path.join(
            os.path.dirname(__file__), "fixtures", "paper_strategy", name
        )

    def _load(self, name):
        with open(self._fixture_path(name), encoding="utf-8") as fh:
            return json.load(fh)

    def test_450_threshold_config_fixture(self):
        d = self._load("fixture_strategy_config_threshold.json")
        self.assertIs(d["paper_only"], True)
        self.assertIs(d["not_a_real_order"], True)
        self.assertEqual(d["strategy_name"], "ThresholdFixtureStrategy")

    def test_451_moving_average_config_fixture(self):
        d = self._load("fixture_strategy_config_moving_average.json")
        self.assertIs(d["paper_only"], True)
        self.assertEqual(d["approval_mode"], "AUTO_PAPER_ONLY")

    def test_452_signal_entry_long_fixture(self):
        d = self._load("fixture_signal_entry_long.json")
        self.assertEqual(d["signal_type"], "ENTRY_LONG")
        self.assertIs(d["paper_only"], True)
        self.assertNotEqual(d["signal_type"], "ENTRY_SHORT")

    def test_453_signal_exit_long_fixture(self):
        d = self._load("fixture_signal_exit_long.json")
        self.assertEqual(d["signal_type"], "EXIT_LONG")
        self.assertIs(d["not_a_real_order"], True)

    def test_454_signal_hold_fixture(self):
        d = self._load("fixture_signal_hold.json")
        self.assertEqual(d["signal_type"], "HOLD")
        self.assertEqual(d["normalized_value"], 0.0)

    def test_455_signal_block_fixture(self):
        d = self._load("fixture_signal_block.json")
        self.assertEqual(d["signal_type"], "BLOCK")
        self.assertEqual(d["confidence"], 1.0)

    def test_456_no_short_in_fixtures(self):
        for fname in (
            "fixture_signal_entry_long.json",
            "fixture_signal_exit_long.json",
            "fixture_signal_hold.json",
            "fixture_signal_block.json",
        ):
            d = self._load(fname)
            self.assertNotIn(d["signal_type"], ("ENTRY_SHORT", "SELL_SHORT"),
                             f"Forbidden signal type in {fname}")


class TestIntegrationEndToEnd(unittest.TestCase):
    """End-to-end integration tests: signal → pipeline → proposal"""

    def test_460_full_pipeline_auto_paper_only(self):
        """Full flow: config → signal → normalize → dedup → pipeline → proposal → lineage"""
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.signal_normalizer_v162 import SignalNormalizer
        from paper_trading.strategy.signal_dedup_v162 import SignalDeduplicator
        from paper_trading.strategy.decision_context_v162 import build_decision_context
        from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
        from paper_trading.strategy.proposal_v162 import build_proposal
        from paper_trading.strategy.lineage_v162 import LineageTracker
        from paper_trading.strategy.enums_v162 import (
            ApprovalMode, DecisionOutcome, EligibilityResult, SignalStrength
        )

        cfg = build_default_config("e2e_test", approval_mode=ApprovalMode.AUTO_PAPER_ONLY)
        sig = make_entry_long(cfg.strategy_id, "2330.TW", confidence=0.9,
                              strength=SignalStrength.STRONG)
        SignalNormalizer().normalize(sig)
        dedup = SignalDeduplicator()
        is_dup = dedup.record(sig)
        self.assertFalse(is_dup)

        ctx = build_decision_context(sig, cfg, eligibility=EligibilityResult.ELIGIBLE)
        pipeline = DecisionPipeline()
        result = pipeline.run(ctx, is_registered=True, is_running=True,
                              data_quality_ok=True, pit_valid=True,
                              eligibility=EligibilityResult.ELIGIBLE.value,
                              suggested_size=100.0, is_market_open=True)
        self.assertEqual(result.outcome, DecisionOutcome.APPROVED.value)
        self.assertIs(result.paper_only, True)
        self.assertIs(result.not_a_real_order, True)

        proposal = build_proposal(result, sig, suggested_size=100.0)
        self.assertIs(proposal.paper_only, True)
        self.assertEqual(proposal.proposed_size, 100.0)

        tracker = LineageTracker()
        rec = tracker.record(sig, result, proposal)
        self.assertIsNotNone(rec.reproducibility_hash)
        self.assertEqual(tracker.count(), 1)

    def test_461_manual_required_deferred_then_approved(self):
        """Manual approval flow: DEFERRED → approve() → APPROVED"""
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.decision_context_v162 import build_decision_context
        from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
        from paper_trading.strategy.approval_v162 import ApprovalPolicy
        from paper_trading.strategy.enums_v162 import (
            ApprovalMode, DecisionOutcome, EligibilityResult
        )

        cfg = build_default_config("e2e_manual", approval_mode=ApprovalMode.MANUAL_REQUIRED)
        sig = make_entry_long(cfg.strategy_id, "2454.TW", confidence=0.8)
        ctx = build_decision_context(sig, cfg, eligibility=EligibilityResult.ELIGIBLE)
        pipeline = DecisionPipeline()
        result = pipeline.run(ctx, is_registered=True, is_running=True,
                              data_quality_ok=True, pit_valid=True,
                              eligibility=EligibilityResult.ELIGIBLE.value,
                              suggested_size=50.0)
        self.assertEqual(result.outcome, DecisionOutcome.DEFERRED.value)

        policy = ApprovalPolicy()
        policy.submit_for_approval(result)
        self.assertEqual(policy.pending_count(), 1)
        ok, reason = policy.approve(result.decision_id, approver="test_operator")
        self.assertTrue(ok)
        self.assertEqual(result.outcome, DecisionOutcome.APPROVED.value)

    def test_462_risk_blocked_flow(self):
        """Risk-blocked flow: pipeline returns RISK_BLOCKED"""
        from paper_trading.strategy.strategy_config_v162 import build_default_config
        from paper_trading.strategy.signal_v162 import make_entry_long
        from paper_trading.strategy.decision_context_v162 import build_decision_context
        from paper_trading.strategy.decision_pipeline_v162 import DecisionPipeline
        from paper_trading.strategy.enums_v162 import (
            ApprovalMode, DecisionOutcome, EligibilityResult
        )

        cfg = build_default_config("e2e_risk", approval_mode=ApprovalMode.AUTO_PAPER_ONLY)
        sig = make_entry_long(cfg.strategy_id, "2330.TW", confidence=0.7)
        ctx = build_decision_context(sig, cfg, eligibility=EligibilityResult.ELIGIBLE)
        pipeline = DecisionPipeline()
        result = pipeline.run(ctx, is_registered=True, is_running=True,
                              data_quality_ok=True, pit_valid=True,
                              eligibility=EligibilityResult.ELIGIBLE.value,
                              suggested_size=100.0, risk_blocked=True)
        self.assertEqual(result.outcome, DecisionOutcome.RISK_BLOCKED.value)
        self.assertIs(result.not_a_real_order, True)


if __name__ == "__main__":
    unittest.main()
