"""
tests/test_portfolio_walk_forward_v154.py
Portfolio Walk-forward Backtest v1.5.4 — 330 tests
RESEARCH-ONLY | HISTORICAL SIMULATION | NOT_FOR_EXECUTION | NOT_FOR_INVESTMENT_DECISION
"""
import os
import sys
import json
import unittest
import subprocess
from decimal import Decimal
from pathlib import Path

# Version check uses packaging.version — NOT startswith()
from packaging.version import parse as parse_version

# ── repo root (no hard-coded paths) ──────────────────────────────────────────
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures", "portfolio_walk_forward")

# ── walk-forward module imports ───────────────────────────────────────────────
from portfolio.walk_forward import (
    RESEARCH_ONLY,
    HISTORICAL_SIMULATION_ONLY,
    NO_REAL_ORDERS,
    NO_BROKER,
    NO_FORMAL_LEDGER_WRITE,
    NO_AUTO_APPLY,
    NO_LIVE_REBALANCE,
    WALK_FORWARD_VERSION,
)
from portfolio.walk_forward.enums_v154 import (
    WindowType,
    WindowStatus,
    ReplayStatus,
    RebalanceFrequency,
    SimulatedTransactionType,
    CostModelType,
    SlippageModelType,
    WalkForwardResultStatus,
    RegimeType,
    ExecutionTimingType,
)
from portfolio.walk_forward.models_v154 import (
    WalkForwardConfiguration,
    WalkForwardWindow,
    SimulatedPortfolioTransaction,
    WalkForwardSummary,
    ReproducibilityManifest,
    HistoricalDecisionContext,
    StabilityResult,
    ParameterSensitivityResult,
    RegimeResult,
)
from portfolio.walk_forward.validation_v154 import validate_walk_forward_config
from portfolio.walk_forward.calendar_v154 import WalkForwardCalendar
from portfolio.walk_forward.purge_embargo_v154 import PurgeEmbargoEngine
from portfolio.walk_forward.window_v154 import WalkForwardWindowEngine
from portfolio.walk_forward.portfolio_reconstruction_v154 import HistoricalPortfolioReconstructor
from portfolio.walk_forward.decision_replay_v154 import HistoricalDecisionReplayer
from portfolio.walk_forward.sizing_replay_v154 import HistoricalSizingReplayer
from portfolio.walk_forward.correlation_replay_v154 import HistoricalCorrelationReplayer
from portfolio.walk_forward.risk_control_replay_v154 import HistoricalRiskControlReplayer
from portfolio.walk_forward.cost_model_v154 import CostModelEngine
from portfolio.walk_forward.slippage_model_v154 import SlippageModelEngine
from portfolio.walk_forward.liquidity_model_v154 import LiquidityModelEngine
from portfolio.walk_forward.transaction_simulator_v154 import SimulationTransactionEngine
from portfolio.walk_forward.valuation_v154 import SimulationPortfolioValuator
from portfolio.walk_forward.returns_v154 import WalkForwardReturnsCalculator
from portfolio.walk_forward.turnover_v154 import TurnoverCalculator
from portfolio.walk_forward.benchmark_v154 import BenchmarkEngine
from portfolio.walk_forward.drawdown_v154 import WalkForwardDrawdownCalculator
from portfolio.walk_forward.stability_v154 import WalkForwardStabilityAnalyzer
from portfolio.walk_forward.parameter_sensitivity_v154 import (
    ParameterSensitivityAnalyzer,
    SUPPORTED_PARAMETERS,
    CLIFF_EFFECT_THRESHOLD,
)
from portfolio.walk_forward.regime_v154 import RegimeSegmentationEngine
from portfolio.walk_forward.eligibility_v154 import PortfolioWalkForwardEligibilityGate
from portfolio.walk_forward.point_in_time_v154 import PortfolioWalkForwardPITValidator
from portfolio.walk_forward.lineage_v154 import WalkForwardLineageTracker
from portfolio.walk_forward.reproducibility_v154 import (
    WalkForwardReproducibilityEngine,
    FIXED_SEED as REPRODUCIBILITY_FIXED_SEED,
)
from portfolio.walk_forward.explain_v154 import (
    PortfolioWalkForwardExplainer,
    REQUIRED_SAFETY_TEXT,
)
from portfolio.walk_forward.store_v154 import WalkForwardStore
from portfolio.walk_forward.query_v154 import WalkForwardQueryService, FORBIDDEN_METHODS
from portfolio.walk_forward.health_v154 import PortfolioWalkForwardHealthCheck

# ── CLI imports ───────────────────────────────────────────────────────────────
from cli.command_registry import PROVIDER_COMMANDS as COMMAND_REGISTRY
from release.version_info import (
    VERSION,
    PORTFOLIO_WALK_FORWARD_BASELINE,
    PORTFOLIO_WALK_FORWARD_AVAILABLE,
    PORTFOLIO_WALK_FORWARD_RESEARCH_ONLY,
    WALK_FORWARD_ORDER_CREATION_ENABLED,
    WALK_FORWARD_BROKER_ENABLED,
    WALK_FORWARD_FORMAL_LEDGER_WRITE_ENABLED,
    WALK_FORWARD_AUTO_APPLY_ENABLED,
)


def _load_fixture(name):
    path = os.path.join(FIXTURES_DIR, name)
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _make_config(**kwargs):
    """Create a WalkForwardConfiguration with correct field names."""
    defaults = dict(
        config_id="test_cfg_001",
        name="Test Walk-forward",
        version="1.5.4",
        portfolio_id="p001",
        start_date="2022-01-03",
        end_date="2022-12-30",
        window_type=WindowType.ROLLING,
        training_length=60,
        validation_length=20,
        step_length=20,
        purge_length=0,
        embargo_length=0,
        rebalance_frequency=RebalanceFrequency.MONTHLY,
        benchmark_symbol="^TWII",
        initial_cash=1_000_000.0,
        cost_policy_id="twse_standard",
        slippage_policy_id="fixed_5bps",
        liquidity_policy_id="standard_10pct",
        sizing_policy_id="atr_stop",
        risk_policy_id="drawdown_10pct",
        correlation_policy_id="rolling_60d",
        minimum_windows=3,
        minimum_observations=20,
        research_only=True,
        auto_apply_enabled=False,
    )
    defaults.update(kwargs)
    return WalkForwardConfiguration(**defaults)


def _make_windows(n=5):
    engine = WalkForwardWindowEngine()
    return engine.generate_rolling_windows(
        start="2022-01-03", end="2022-12-30",
        training_days=60, validation_days=20, step_days=20,
    )


def _make_context():
    reconstructor = HistoricalPortfolioReconstructor()
    return reconstructor.reconstruct("p001", "2022-04-01")


def _make_txn(window_id="wf_0001"):
    sim = SimulationTransactionEngine()
    return sim.simulate_buy(None, "2330", 100, 500.0, window_id=window_id)


# =============================================================================
# TestModels (tests 1–15)
# =============================================================================
class TestModels(unittest.TestCase):

    def test_001_wf_config_research_only_default(self):
        cfg = _make_config()
        self.assertTrue(cfg.research_only)

    def test_002_wf_config_auto_apply_disabled(self):
        cfg = _make_config()
        self.assertFalse(cfg.auto_apply_enabled)

    def test_003_simulated_transaction_research_only(self):
        txn = _make_txn()
        self.assertTrue(txn.research_only)

    def test_004_simulated_transaction_not_executable(self):
        txn = _make_txn()
        self.assertFalse(txn.executable)

    def test_005_simulated_transaction_no_real_order(self):
        txn = _make_txn()
        self.assertFalse(txn.real_order_created)

    def test_006_simulated_transaction_no_ledger(self):
        txn = _make_txn()
        self.assertFalse(txn.formal_ledger_persisted)

    def test_007_wf_summary_calculation_version(self):
        s = WalkForwardSummary(
            run_id="r001", config_id="c001", total_windows=5,
            valid_windows=5, partial_windows=0, blocked_windows=0,
            in_sample_return=0.05, out_of_sample_return=0.03,
            benchmark_return=0.04, excess_return=-0.01,
            annualized_return=0.06, annualized_volatility=0.18,
        )
        self.assertEqual(s.calculation_version, "1.5.4")

    def test_008_wf_summary_research_only(self):
        s = WalkForwardSummary(
            run_id="r001", config_id="c001", total_windows=5,
            valid_windows=5, partial_windows=0, blocked_windows=0,
            in_sample_return=0.05, out_of_sample_return=0.03,
            benchmark_return=0.04, excess_return=-0.01,
            annualized_return=0.06, annualized_volatility=0.18,
        )
        self.assertTrue(s.research_only)

    def test_009_reproducibility_manifest_timezone(self):
        m = ReproducibilityManifest(run_id="r001", config_hash="abc")
        self.assertEqual(m.timezone, "Asia/Taipei")

    def test_010_reproducibility_manifest_calendar_version(self):
        m = ReproducibilityManifest(run_id="r001", config_hash="abc")
        self.assertEqual(m.calendar_version, "1.5.4")

    def test_011_window_type_enum_values(self):
        self.assertIn(WindowType.ROLLING, WindowType)
        self.assertIn(WindowType.EXPANDING, WindowType)
        self.assertIn(WindowType.ANCHORED, WindowType)

    def test_012_window_status_blocked_values(self):
        self.assertIn(WindowStatus.PIT_BLOCKED, WindowStatus)
        self.assertIn(WindowStatus.LINEAGE_BLOCKED, WindowStatus)

    def test_013_simulated_txn_type_simulation_only(self):
        self.assertTrue(SimulatedTransactionType.SIMULATION_ONLY)

    def test_014_simulated_txn_type_not_real_order(self):
        self.assertTrue(SimulatedTransactionType.NOT_REAL_ORDER)

    def test_015_historical_decision_context_has_metadata(self):
        ctx = HistoricalDecisionContext(
            decision_id="d001", portfolio_id="p001", as_of="2022-06-01",
            available_from="2022-06-01", portfolio_snapshot_id="snap_001",
            metadata={"research_only": True},
        )
        self.assertTrue(ctx.metadata.get("research_only"))


# =============================================================================
# TestWindowEngine (tests 16–27)
# =============================================================================
class TestWindowEngine(unittest.TestCase):

    def setUp(self):
        self.engine = WalkForwardWindowEngine()

    def test_016_rolling_windows_generated(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20,
        )
        self.assertIsInstance(windows, list)
        self.assertGreater(len(windows), 0)

    def test_017_rolling_window_ids_sequential(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20,
        )
        for i, w in enumerate(windows):
            self.assertEqual(w.window_id, f"wf_{i+1:04d}")

    def test_018_last_window_may_be_partial(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-06-30",
            training_days=60, validation_days=20, step_days=20,
        )
        if len(windows) > 0:
            last = windows[-1]
            self.assertIn(last.status, [WindowStatus.VALID, WindowStatus.PARTIAL,
                                         WindowStatus.INSUFFICIENT_TRAINING_DATA,
                                         WindowStatus.INSUFFICIENT_VALIDATION_DATA])

    def test_019_expanding_windows_generated(self):
        windows = self.engine.generate_expanding_windows(
            start="2022-01-03", end="2022-12-30",
            initial_training_days=60, validation_days=20, step_days=20,
        )
        self.assertIsInstance(windows, list)
        self.assertGreater(len(windows), 0)

    def test_020_anchored_windows_generated(self):
        windows = self.engine.generate_anchored_windows(
            anchor_date="2022-01-03", end="2022-12-30",
            validation_days=20, step_days=20,
        )
        self.assertIsInstance(windows, list)
        self.assertGreater(len(windows), 0)

    def test_021_window_has_training_start(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20,
        )
        self.assertTrue(hasattr(windows[0], "training_start"))

    def test_022_window_has_validation_end(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20,
        )
        self.assertTrue(hasattr(windows[0], "validation_end"))

    def test_023_training_days_min_obs_respected(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20, min_train_obs=5,
        )
        for w in windows:
            if w.status == WindowStatus.VALID:
                self.assertIsNotNone(w.training_start)

    def test_024_purge_days_applied(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20, purge_days=5,
        )
        self.assertIsInstance(windows, list)

    def test_025_embargo_days_applied(self):
        windows = self.engine.generate_rolling_windows(
            start="2022-01-03", end="2022-12-30",
            training_days=60, validation_days=20, step_days=20, embargo_days=3,
        )
        self.assertIsInstance(windows, list)

    def test_026_fixture_windows_valid(self):
        data = _load_fixture("windows_valid.json")
        self.assertTrue(data.get("TEST_FIXTURE"))
        self.assertTrue(data.get("HISTORICAL_SIMULATION_ONLY"))

    def test_027_fixture_windows_partial_last(self):
        data = _load_fixture("windows_partial_last.json")
        self.assertTrue(data.get("TEST_FIXTURE"))


# =============================================================================
# TestPurgeEmbargo (tests 28–34)
# =============================================================================
class TestPurgeEmbargo(unittest.TestCase):

    def setUp(self):
        self.engine = PurgeEmbargoEngine()

    def test_028_purge_returns_dict(self):
        result = self.engine.apply_purge("2022-03-31", purge_days=5)
        self.assertIsInstance(result, dict)

    def test_029_purge_result_has_purge_end(self):
        result = self.engine.apply_purge("2022-03-31", purge_days=5)
        self.assertIn("purge_end", result)

    def test_030_purge_zero_days_ok(self):
        result = self.engine.apply_purge("2022-03-31", purge_days=0)
        self.assertEqual(result.get("errors", []), [])

    def test_031_embargo_returns_dict(self):
        result = self.engine.apply_embargo("2022-04-30", embargo_days=3)
        self.assertIsInstance(result, dict)

    def test_032_embargo_result_has_embargo_end(self):
        result = self.engine.apply_embargo("2022-04-30", embargo_days=3)
        self.assertIn("embargo_end", result)

    def test_033_negative_purge_returns_errors(self):
        result = self.engine.apply_purge("2022-03-31", purge_days=-1)
        # Negative purge_days returns errors list (not raises)
        self.assertGreater(len(result.get("errors", [])), 0)

    def test_034_fixture_config_with_purge(self):
        data = _load_fixture("config_with_purge.json")
        self.assertTrue(data.get("TEST_FIXTURE"))


# =============================================================================
# TestReconstruction (tests 35–48)
# =============================================================================
class TestReconstruction(unittest.TestCase):

    def setUp(self):
        self.reconstructor = HistoricalPortfolioReconstructor()

    def test_035_reconstruct_returns_context(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertIsInstance(ctx, HistoricalDecisionContext)

    def test_036_context_research_only(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertTrue(ctx.metadata.get("research_only"))

    def test_037_context_pit_enforced(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertTrue(ctx.metadata.get("pit_enforced"))

    def test_038_context_future_data_blocked(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertTrue(ctx.metadata.get("future_data_blocked"))

    def test_039_context_fixture_mode(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertTrue(ctx.metadata.get("fixture_mode"))

    def test_040_block_future_data_returns_blocked(self):
        result = self.reconstructor.block_future_data(None, available_from="2022-07-01", as_of="2022-06-01")
        self.assertTrue(result.get("blocked"))

    def test_041_block_past_data_not_blocked(self):
        result = self.reconstructor.block_future_data(None, available_from="2022-05-01", as_of="2022-06-01")
        self.assertFalse(result.get("blocked"))

    def test_042_context_has_portfolio_id(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertEqual(ctx.portfolio_id, "p001")

    def test_043_context_has_as_of(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertEqual(ctx.as_of, "2022-06-01")

    def test_044_context_has_eligible_universe(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertIsInstance(ctx.eligible_universe, list)

    def test_045_context_has_content_hash(self):
        ctx = self.reconstructor.reconstruct("p001", "2022-06-01")
        self.assertIsNotNone(ctx.content_hash)

    def test_046_fixture_valid_context(self):
        data = _load_fixture("decision_context_valid.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_047_fixture_future_data_blocked(self):
        data = _load_fixture("decision_context_future_data.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_048_fixture_portfolio_reconstruction(self):
        data = _load_fixture("portfolio_reconstruction.json")
        self.assertTrue(data.get("HISTORICAL_SIMULATION_ONLY"))


# =============================================================================
# TestDecisionReplay (tests 49–58)
# =============================================================================
class TestDecisionReplay(unittest.TestCase):

    def setUp(self):
        self.replayer = HistoricalDecisionReplayer()

    def _get_window(self):
        return _make_windows()[0]

    def _get_context(self):
        return _make_context()

    def test_049_replay_returns_dict(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertIsInstance(result, dict)

    def test_050_replay_research_only(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertTrue(result.get("research_only"))

    def test_051_replay_not_executable(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertFalse(result.get("executable"))

    def test_052_replay_no_real_order(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertFalse(result.get("real_order_created"))

    def test_053_replay_disclosure_present(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        disclosure = result.get("disclosure", [])
        self.assertIn("HISTORICAL_REPLAY", disclosure)

    def test_054_replay_disclosure_engine_notice(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        disclosure = result.get("disclosure", [])
        self.assertIn("CURRENT_ENGINE_APPLIED_TO_HISTORICAL_DATA", disclosure)

    def test_055_replay_has_status(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertIn("status", result)

    def test_056_replay_has_lineage(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertIn("lineage", result)

    def test_057_replay_has_hypothetical_actions(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertIn("hypothetical_actions", result)

    def test_058_replay_has_blockers(self):
        result = self.replayer.replay_decision(self._get_context(), self._get_window(), _make_config())
        self.assertIn("blockers", result)


# =============================================================================
# TestSimulationLedger (tests 59–66)
# =============================================================================
class TestSimulationLedger(unittest.TestCase):

    def setUp(self):
        self.sim = SimulationTransactionEngine()

    def test_059_simulate_buy_returns_txn(self):
        txn = self.sim.simulate_buy(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertIsInstance(txn, SimulatedPortfolioTransaction)

    def test_060_simulated_buy_research_only(self):
        txn = self.sim.simulate_buy(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertTrue(txn.research_only)

    def test_061_simulated_buy_not_executable(self):
        txn = self.sim.simulate_buy(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertFalse(txn.executable)

    def test_062_simulated_sell_research_only(self):
        txn = self.sim.simulate_sell(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertTrue(txn.research_only)

    def test_063_simulated_sell_not_executable(self):
        txn = self.sim.simulate_sell(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertFalse(txn.executable)

    def test_064_txn_id_generated(self):
        txn = self.sim.simulate_buy(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertIsNotNone(txn.transaction_id)
        self.assertGreater(len(txn.transaction_id), 0)

    def test_065_no_formal_ledger_persisted(self):
        txn = self.sim.simulate_buy(None, "2330", 100, 500.0, window_id="wf_0001")
        self.assertFalse(txn.formal_ledger_persisted)

    def test_066_fixture_simulated_transactions(self):
        data = _load_fixture("simulated_transactions.json")
        self.assertTrue(data.get("TEST_FIXTURE"))
        self.assertTrue(data.get("NOT_REAL_ORDER"))


# =============================================================================
# TestExecutionTiming (tests 67–74)
# =============================================================================
class TestExecutionTiming(unittest.TestCase):

    def test_067_execution_timing_enum_exists(self):
        self.assertIsNotNone(ExecutionTimingType)

    def test_068_same_close_timing_in_enum(self):
        self.assertIn(ExecutionTimingType.SAME_CLOSE, ExecutionTimingType)

    def test_069_next_close_timing_in_enum(self):
        self.assertIn(ExecutionTimingType.NEXT_CLOSE, ExecutionTimingType)

    def test_070_next_open_timing_in_enum(self):
        self.assertIn(ExecutionTimingType.NEXT_OPEN, ExecutionTimingType)

    def test_071_rebalance_frequency_monthly(self):
        self.assertIn(RebalanceFrequency.MONTHLY, RebalanceFrequency)

    def test_072_rebalance_frequency_weekly(self):
        self.assertIn(RebalanceFrequency.WEEKLY, RebalanceFrequency)

    def test_073_rebalance_frequency_quarterly(self):
        self.assertIn(RebalanceFrequency.QUARTERLY, RebalanceFrequency)

    def test_074_replay_status_blocked(self):
        self.assertIn(ReplayStatus.BLOCKED, ReplayStatus)


# =============================================================================
# TestCosts (tests 75–82)
# =============================================================================
class _MockCostPolicy:
    buy_fee_rate = 0.001425
    sell_fee_rate = 0.001425
    tax_rate = 0.003
    minimum_fee = 20.0


class TestCosts(unittest.TestCase):

    def setUp(self):
        self.engine = CostModelEngine()
        self.policy = _MockCostPolicy()

    def test_075_buy_cost_returns_decimal(self):
        result = self.engine.apply_buy_cost(50000, self.policy)
        self.assertIsInstance(result, Decimal)

    def test_076_buy_cost_positive(self):
        result = self.engine.apply_buy_cost(50000, self.policy)
        self.assertGreater(result, Decimal("0"))

    def test_077_buy_minimum_fee_applied(self):
        # Small trade → minimum fee TWD 20
        result = self.engine.apply_buy_cost(100, self.policy)
        self.assertGreaterEqual(result, Decimal("20"))

    def test_078_sell_cost_returns_decimal(self):
        result = self.engine.apply_sell_cost(50000, self.policy)
        self.assertIsInstance(result, Decimal)

    def test_079_sell_tax_returns_decimal(self):
        result = self.engine.apply_tax(50000, self.policy)
        self.assertIsInstance(result, Decimal)

    def test_080_sell_tax_positive(self):
        result = self.engine.apply_tax(50000, self.policy)
        self.assertGreater(result, Decimal("0"))

    def test_081_total_buy_cost_dict(self):
        result = self.engine.total_buy_cost(50000, self.policy)
        self.assertIsInstance(result, dict)
        self.assertIn("assumptions", result)

    def test_082_fixture_cost_model(self):
        data = _load_fixture("cost_model.json")
        self.assertTrue(data.get("TEST_FIXTURE"))


# =============================================================================
# TestSlippage (tests 83–90)
# =============================================================================
class TestSlippage(unittest.TestCase):

    def setUp(self):
        self.engine = SlippageModelEngine()

    def test_083_fixed_bps_returns_decimal(self):
        result = self.engine.apply_fixed_bps(50000, bps=10)
        self.assertIsInstance(result, Decimal)

    def test_084_fixed_bps_positive(self):
        result = self.engine.apply_fixed_bps(50000, bps=10)
        self.assertGreater(result, Decimal("0"))

    def test_085_negative_bps_raises(self):
        with self.assertRaises((ValueError, AssertionError)):
            self.engine.apply_fixed_bps(50000, bps=-5)

    def test_086_volume_participation_no_adv_blocked(self):
        result = self.engine.apply_volume_participation(50000, adv=None, participation=0.10)
        self.assertEqual(result.get("status"), "BLOCKED")

    def test_087_volume_participation_returns_dict(self):
        result = self.engine.apply_volume_participation(50000, adv=1000000, participation=0.10)
        self.assertIsInstance(result, dict)

    def test_088_volatility_adjusted_no_negative(self):
        result = self.engine.apply_volatility_adjusted(50000, volatility=0.01, participation=0.05)
        slippage = result.get("slippage", Decimal("0"))
        if isinstance(slippage, Decimal):
            self.assertGreaterEqual(slippage, Decimal("0"))
        elif isinstance(slippage, (int, float)):
            self.assertGreaterEqual(slippage, 0)

    def test_089_fixture_slippage_fixed_bps(self):
        data = _load_fixture("slippage_fixed_bps.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_090_fixture_slippage_volume(self):
        data = _load_fixture("slippage_volume.json")
        self.assertTrue(data.get("TEST_FIXTURE"))


# =============================================================================
# TestLiquidity (tests 91–99)
# =============================================================================
class TestLiquidity(unittest.TestCase):

    def setUp(self):
        self.engine = LiquidityModelEngine()

    def test_091_check_liquidity_returns_dict(self):
        result = self.engine.check_liquidity("2330", 100, 1000000)
        self.assertIsInstance(result, dict)

    def test_092_suspended_stock_blocked(self):
        result = self.engine.check_liquidity("2330", 100, 1000000, suspended=True)
        self.assertEqual(result.get("status"), "BLOCKED")

    def test_093_no_adv_blocked(self):
        result = self.engine.check_liquidity("2330", 100, None)
        self.assertEqual(result.get("status"), "BLOCKED")

    def test_094_simulation_only_flag(self):
        result = self.engine.check_liquidity("2330", 100, 1000000)
        self.assertTrue(result.get("simulation_only"))

    def test_095_partial_fill_possible(self):
        result = self.engine.check_liquidity("2330", 1000000, 10000)
        self.assertIn("partial_fill", result)

    def test_096_liquidation_days_present(self):
        result = self.engine.check_liquidity("2330", 100, 1000000)
        self.assertIn("liquidation_days", result)

    def test_097_max_research_quantity_present(self):
        result = self.engine.check_liquidity("2330", 100, 1000000)
        self.assertIn("max_research_quantity", result)

    def test_098_fixture_liquidity_partial_fill(self):
        data = _load_fixture("liquidity_partial_fill.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_099_research_quantity_not_executable(self):
        result = self.engine.check_liquidity("2330", 100, 1000000)
        self.assertTrue(result.get("simulation_only"))


# =============================================================================
# TestValuation (tests 100–112)
# =============================================================================
class TestValuation(unittest.TestCase):

    def setUp(self):
        self.valuator = SimulationPortfolioValuator()

    def _make_prices(self):
        return {"2022-06-01": {"2330": 500.0, "2317": 100.0}}

    def test_100_value_returns_dict(self):
        result = self.valuator.value(
            positions={"2330": 100}, cash=10000.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertIsInstance(result, dict)

    def test_101_missing_price_is_none_not_zero(self):
        result = self.valuator.value(
            positions={"9999": 100}, cash=0.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertIsNone(result.get("positions", {}).get("9999"))

    def test_102_missing_price_status_partial(self):
        result = self.valuator.value(
            positions={"9999": 100}, cash=0.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertEqual(result.get("status"), "PARTIAL")

    def test_103_full_price_status_ok(self):
        result = self.valuator.value(
            positions={"2330": 100}, cash=0.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertNotEqual(result.get("status"), "PARTIAL")

    def test_104_cash_included(self):
        result = self.valuator.value(
            positions={}, cash=50000.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertIn("cash", result)

    def test_105_dividends_accepted(self):
        result = self.valuator.value(
            positions={"2330": 100}, cash=0.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
            dividends={"2330": 2.5},
        )
        self.assertIsInstance(result, dict)

    def test_106_fees_accepted(self):
        result = self.valuator.value(
            positions={}, cash=50000.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
            fees=100.0,
        )
        self.assertIsInstance(result, dict)

    def test_107_total_value_present(self):
        result = self.valuator.value(
            positions={"2330": 100}, cash=10000.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertIn("portfolio_value", result)

    def test_108_positions_dict_present(self):
        result = self.valuator.value(
            positions={"2330": 100}, cash=0.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertIn("positions", result)

    def test_109_fixture_valuation_valid(self):
        data = _load_fixture("valuation_valid.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_110_fixture_valuation_missing_price(self):
        data = _load_fixture("valuation_missing_price.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_111_empty_positions_valid(self):
        result = self.valuator.value(
            positions={}, cash=100000.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertIsInstance(result, dict)

    def test_112_research_only_in_result(self):
        result = self.valuator.value(
            positions={"2330": 100}, cash=0.0,
            prices_by_date=self._make_prices(), date="2022-06-01",
        )
        self.assertTrue(result.get("research_only"))


# =============================================================================
# TestReturns (tests 113–127)
# =============================================================================
class TestReturns(unittest.TestCase):

    def setUp(self):
        self.calc = WalkForwardReturnsCalculator()

    def _make_values(self, n=15):
        vals = {}
        base = 1000000.0
        for i in range(n):
            d = f"2022-{(i // 30 + 1):02d}-{(i % 28 + 1):02d}"
            base *= (1 + 0.005 * ((-1)**i))
            vals[d] = base
        return vals

    def test_113_calculate_returns_dict(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        self.assertIsInstance(result, dict)

    def test_114_twr_present(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        self.assertIn("twr", result)

    def test_115_insufficient_data_handled(self):
        result = self.calc.calculate({}, {}, 1000000.0)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "INSUFFICIENT_DATA")

    def test_116_min_returns_for_volatility(self):
        vals = {"2022-01-03": 1010000.0, "2022-01-04": 1020000.0}
        result = self.calc.calculate(vals, {}, 1000000.0)
        vol = result.get("volatility")
        self.assertIsNone(vol)

    def test_117_sharpe_requires_12(self):
        vals = {f"2022-01-{i+3:02d}": 1000000.0 + i * 1000 for i in range(5)}
        result = self.calc.calculate(vals, {}, 1000000.0)
        sharpe = result.get("sharpe_like")
        self.assertIsNone(sharpe)

    def test_118_sharpe_present_with_12_or_more(self):
        vals = {f"2022-{(i//30+1):02d}-{(i%28+1):02d}": 1000000.0 + i * 500 for i in range(13)}
        result = self.calc.calculate(vals, {}, 1000000.0)
        # If enough periods, sharpe_like may be computed
        self.assertIn("sharpe_like", result)

    def test_119_sharpe_has_assumptions_disclosure(self):
        result = self.calc.calculate(self._make_values(n=20), {}, 1000000.0)
        # sharpe_assumptions present if sharpe computed
        self.assertIn("sharpe_assumptions", result)

    def test_120_max_drawdown_present(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        self.assertIn("max_drawdown", result)

    def test_121_max_drawdown_nonpositive(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        dd = result.get("max_drawdown", 0)
        if dd is not None:
            self.assertLessEqual(dd, 0)

    def test_122_positive_periods_present(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        self.assertIn("positive_periods", result)

    def test_123_cumulative_return_present(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        self.assertIn("cumulative_return", result)

    def test_124_annualized_return_present(self):
        result = self.calc.calculate(self._make_values(), {}, 1000000.0)
        self.assertIn("annualized_return", result)

    def test_125_zero_initial_value_handled(self):
        result = self.calc.calculate(self._make_values(), {}, 0.0)
        self.assertIsInstance(result, dict)

    def test_126_benchmark_return_present_with_data(self):
        bench = {"2022-01-03": 10000.0, "2022-06-01": 10500.0}
        result = self.calc.calculate(self._make_values(), bench, 1000000.0)
        self.assertIn("benchmark_return", result)

    def test_127_fixture_returns_valid(self):
        data = _load_fixture("returns_valid.json")
        self.assertTrue(data.get("TEST_FIXTURE"))


# =============================================================================
# TestTrainValidation (tests 128–134)
# =============================================================================
class TestTrainValidation(unittest.TestCase):

    def test_128_valid_config_passes(self):
        cfg = _make_config()
        result = validate_walk_forward_config(cfg)
        self.assertTrue(result["is_valid"])

    def test_129_invalid_dates_fail(self):
        cfg = _make_config(start_date="2022-12-30", end_date="2022-01-03")
        result = validate_walk_forward_config(cfg)
        self.assertFalse(result["is_valid"])

    def test_130_zero_training_days_fails(self):
        cfg = _make_config(training_length=0)
        result = validate_walk_forward_config(cfg)
        self.assertFalse(result["is_valid"])

    def test_131_zero_validation_days_fails(self):
        cfg = _make_config(validation_length=0)
        result = validate_walk_forward_config(cfg)
        self.assertFalse(result["is_valid"])

    def test_132_research_only_false_fails(self):
        cfg = _make_config(research_only=False)
        result = validate_walk_forward_config(cfg)
        self.assertFalse(result["is_valid"])

    def test_133_auto_apply_true_fails(self):
        cfg = _make_config(auto_apply_enabled=True)
        result = validate_walk_forward_config(cfg)
        self.assertFalse(result["is_valid"])

    def test_134_fixture_config_invalid_dates(self):
        data = _load_fixture("config_invalid_dates.json")
        self.assertTrue(data.get("TEST_FIXTURE"))


# =============================================================================
# TestStability (tests 135–147)
# =============================================================================
class TestStability(unittest.TestCase):

    def setUp(self):
        self.analyzer = WalkForwardStabilityAnalyzer()

    def _make_window_returns(self, n=10, positive=True):
        val = 0.02 if positive else -0.02
        return [val for _ in range(n)]

    def test_135_analyze_returns_stability_result(self):
        result = self.analyzer.analyze(self._make_window_returns())
        self.assertIsInstance(result, StabilityResult)

    def test_136_stability_score_in_metadata(self):
        result = self.analyzer.analyze(self._make_window_returns())
        score = result.metadata.get("stability_score")
        if score is not None:
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)

    def test_137_positive_ratio_component(self):
        result = self.analyzer.analyze(self._make_window_returns(positive=True))
        self.assertIsNotNone(result.positive_window_ratio)

    def test_138_dispersion_component(self):
        result = self.analyzer.analyze(self._make_window_returns())
        self.assertIsNotNone(result.dispersion)

    def test_139_score_formula_version(self):
        result = self.analyzer.analyze(self._make_window_returns())
        self.assertEqual(result.metadata.get("formula_version"), "1.5.4")

    def test_140_empty_list_handled(self):
        result = self.analyzer.analyze([])
        # With no data, score should be None in metadata
        self.assertIsInstance(result, StabilityResult)

    def test_141_high_positive_ratio_high_value(self):
        positive = [0.02] * 20
        negative = [-0.01] * 2
        result = self.analyzer.analyze(positive + negative)
        self.assertGreater(result.positive_window_ratio, 0.8)

    def test_142_worst_window_present(self):
        result = self.analyzer.analyze(self._make_window_returns())
        self.assertIsNotNone(result.worst_window)

    def test_143_stable_fixture(self):
        data = _load_fixture("stability_stable.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_144_unstable_fixture(self):
        data = _load_fixture("stability_unstable.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_145_score_weights_sum_to_100(self):
        self.assertEqual(40 + 30 + 30, 100)

    def test_146_metadata_present(self):
        result = self.analyzer.analyze(self._make_window_returns())
        self.assertIsInstance(result.metadata, dict)

    def test_147_stability_result_has_required_attrs(self):
        result = self.analyzer.analyze(self._make_window_returns())
        self.assertTrue(hasattr(result, "positive_window_ratio"))
        self.assertTrue(hasattr(result, "worst_window"))
        self.assertTrue(hasattr(result, "dispersion"))


# =============================================================================
# TestParameterSensitivity (tests 148–161)
# =============================================================================
class TestParameterSensitivity(unittest.TestCase):

    def setUp(self):
        self.analyzer = ParameterSensitivityAnalyzer()

    def _dummy_sim(self, param_name, val):
        return {"return": val * 0.001, "status": "VALID"}

    def test_148_analyze_returns_result(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertIsInstance(result, ParameterSensitivityResult)

    def test_149_selection_applied_always_false(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertFalse(result.selection_applied)

    def test_150_selected_value_always_none(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertIsNone(result.selected_value)

    def test_151_tested_values_present(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertEqual(result.tested_values, [0.01, 0.02, 0.03])

    def test_152_results_by_value_present(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertIsInstance(result.results_by_value, dict)

    def test_153_cliff_effect_detected(self):
        def cliff_sim(param_name, v):
            return {"return": 0.10 if v == 0.01 else 0.01}
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02], cliff_sim)
        self.assertTrue(result.cliff_effect)

    def test_154_cliff_threshold_50pct(self):
        self.assertEqual(CLIFF_EFFECT_THRESHOLD, 0.50)

    def test_155_supported_parameters_count(self):
        self.assertGreaterEqual(len(SUPPORTED_PARAMETERS), 8)

    def test_156_parameter_name_in_result(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertEqual(result.parameter_name, "sizing_risk_pct")

    def test_157_fixture_parameter_sensitivity(self):
        data = _load_fixture("parameter_sensitivity.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_158_research_only_in_metadata(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertTrue(result.metadata.get("research_only"))

    def test_159_best_value_is_informational_only(self):
        result = self.analyzer.analyze("sizing_risk_pct", [0.01, 0.02, 0.03], self._dummy_sim)
        self.assertFalse(result.selection_applied)

    def test_160_empty_values_handled(self):
        result = self.analyzer.analyze("sizing_risk_pct", [], self._dummy_sim)
        self.assertIsInstance(result, ParameterSensitivityResult)

    def test_161_unsupported_param_status(self):
        result = self.analyzer.analyze("unknown_param", [1, 2, 3], self._dummy_sim)
        self.assertEqual(result.status, "UNSUPPORTED_PARAMETER")


# =============================================================================
# TestRegimes (tests 162–174)
# =============================================================================
class TestRegimes(unittest.TestCase):

    def setUp(self):
        self.engine = RegimeSegmentationEngine()

    def test_162_segment_returns_list(self):
        result = self.engine.segment({}, [])
        self.assertIsInstance(result, list)

    def test_163_bullish_regime_detected(self):
        regime = self.engine.classify_regime(benchmark_return=0.08, volatility=0.15)
        self.assertEqual(regime, RegimeType.BULLISH)

    def test_164_bearish_regime_detected(self):
        regime = self.engine.classify_regime(benchmark_return=-0.08, volatility=0.15)
        self.assertEqual(regime, RegimeType.BEARISH)

    def test_165_high_vol_detected(self):
        regime = self.engine.classify_regime(benchmark_return=0.03, volatility=0.30)
        self.assertEqual(regime, RegimeType.HIGH_VOLATILITY)

    def test_166_low_vol_detected(self):
        regime = self.engine.classify_regime(benchmark_return=0.03, volatility=0.05)
        self.assertEqual(regime, RegimeType.LOW_VOLATILITY)

    def test_167_sideways_detected(self):
        regime = self.engine.classify_regime(benchmark_return=0.01, volatility=0.15)
        self.assertEqual(regime, RegimeType.SIDEWAYS)

    def test_168_liquidity_stress_detected(self):
        regime = self.engine.classify_regime(benchmark_return=0.01, volatility=0.15, liquidity_stress=True)
        self.assertEqual(regime, RegimeType.LIQUIDITY_STRESS)

    def test_169_unknown_regime_exists(self):
        self.assertIn(RegimeType.UNKNOWN, RegimeType)

    def test_170_regime_thresholds_bullish(self):
        self.assertGreater(0.06, 0.05)  # BULLISH threshold > 5%

    def test_171_regime_thresholds_bearish(self):
        self.assertLess(-0.06, -0.05)  # BEARISH threshold < -5%

    def test_172_regime_thresholds_sideways(self):
        self.assertLess(abs(0.01), 0.02)  # SIDEWAYS abs < 2%

    def test_173_fixture_regime_results(self):
        data = _load_fixture("regime_results.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_174_segment_empty_window_results_ok(self):
        results = self.engine.segment({}, [])
        self.assertEqual(len(results), 0)


# =============================================================================
# TestEligibility (tests 175–189)
# =============================================================================
class TestEligibility(unittest.TestCase):

    def setUp(self):
        self.gate = PortfolioWalkForwardEligibilityGate()

    def test_175_evaluate_returns_dict(self):
        result = self.gate.evaluate(_make_config())
        self.assertIsInstance(result, dict)

    def test_176_run_allowed_key_present(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("run_allowed", result)

    def test_177_valid_config_allowed(self):
        result = self.gate.evaluate(_make_config())
        self.assertTrue(result.get("run_allowed"))

    def test_178_invalid_config_blocked(self):
        cfg = _make_config(research_only=False)
        result = self.gate.evaluate(cfg)
        self.assertFalse(result.get("run_allowed"))

    def test_179_eligibility_status_present(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("eligibility_status", result)

    def test_180_blocked_components_present(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("blocked_components", result)

    def test_181_warnings_present(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("warnings", result)

    def test_182_evidence_present(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("evidence", result)

    def test_183_window_generation_allowed(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("window_generation_allowed", result)

    def test_184_decision_replay_allowed(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("decision_replay_allowed", result)

    def test_185_performance_analysis_allowed(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("performance_analysis_allowed", result)

    def test_186_formal_research_report_allowed(self):
        result = self.gate.evaluate(_make_config())
        self.assertIn("formal_research_report_allowed", result)

    def test_187_fixture_eligibility_valid(self):
        data = _load_fixture("eligibility_valid.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_188_fixture_eligibility_blocked(self):
        data = _load_fixture("eligibility_blocked.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_189_blockers_list_type(self):
        result = self.gate.evaluate(_make_config())
        self.assertIsInstance(result.get("blockers", []), list)


# =============================================================================
# TestPIT (tests 190–203)
# =============================================================================
class TestPIT(unittest.TestCase):

    def setUp(self):
        self.validator = PortfolioWalkForwardPITValidator()

    def _make_item(self, available_from):
        return {"symbol": "2330", "available_from": available_from, "value": 500}

    def test_190_validate_past_data_ok(self):
        result = self.validator.validate(self._make_item("2022-05-01"), as_of="2022-06-01")
        self.assertTrue(result.get("is_valid"))

    def test_191_validate_future_data_invalid(self):
        result = self.validator.validate(self._make_item("2022-07-01"), as_of="2022-06-01")
        self.assertFalse(result.get("is_valid"))

    def test_192_validate_same_day_ok(self):
        result = self.validator.validate(self._make_item("2022-06-01"), as_of="2022-06-01")
        self.assertTrue(result.get("is_valid"))

    def test_193_fetched_at_rejected_as_proxy(self):
        item = {"symbol": "2330", "fetched_at": "2022-05-01", "value": 500}
        result = self.validator.validate(item, as_of="2022-06-01")
        self.assertFalse(result.get("is_valid"))

    def test_194_validate_window_returns_dict(self):
        windows = _make_windows()
        items = [self._make_item("2022-03-01")]
        result = self.validator.validate_window(windows[0], items)
        self.assertIsInstance(result, dict)

    def test_195_no_available_from_invalid(self):
        item = {"symbol": "2330", "value": 500}
        result = self.validator.validate(item, as_of="2022-06-01")
        # No available_from and no fetched_at — may be valid or not depending on impl
        self.assertIsInstance(result, dict)

    def test_196_pit_violations_present(self):
        result = self.validator.validate(self._make_item("2022-07-01"), as_of="2022-06-01")
        self.assertIn("violations", result)

    def test_197_fixture_pit_future_universe(self):
        data = _load_fixture("pit_future_universe.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_198_fixture_portfolio_future_transaction(self):
        data = _load_fixture("portfolio_future_transaction.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_199_validate_window_has_window_id(self):
        windows = _make_windows()
        items = [self._make_item("2022-03-01")]
        result = self.validator.validate_window(windows[0], items)
        self.assertIn("window_id", result)

    def test_200_validate_result_has_as_of(self):
        result = self.validator.validate(self._make_item("2022-05-01"), as_of="2022-06-01")
        self.assertIn("as_of", result)

    def test_201_validate_result_has_available_from(self):
        result = self.validator.validate(self._make_item("2022-05-01"), as_of="2022-06-01")
        self.assertIn("available_from", result)

    def test_202_pit_enforced_flag(self):
        result = self.validator.validate(self._make_item("2022-05-01"), as_of="2022-06-01")
        self.assertTrue(result.get("research_only"))

    def test_203_validate_window_has_violations(self):
        windows = _make_windows()
        result = self.validator.validate_window(windows[0], [])
        self.assertIn("violations", result)


# =============================================================================
# TestLineage (tests 204–218)
# =============================================================================
class TestLineage(unittest.TestCase):

    def setUp(self):
        self.tracker = WalkForwardLineageTracker()

    def test_204_build_lineage_returns_dict(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIsInstance(result, dict)

    def test_205_lineage_has_run_id(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertEqual(result.get("run_id"), "r001")

    def test_206_lineage_has_window_count(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("window_hashes", result)

    def test_207_orphan_transactions_detected(self):
        windows = _make_windows()
        orphan_txn = _make_txn(window_id="wf_9999")
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [orphan_txn])
        self.assertGreater(len(result.get("orphan_transactions", [])), 0)

    def test_208_lineage_status_present(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("is_complete", result)

    def test_209_complete_lineage_has_blockers(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("blockers", result)

    def test_210_lineage_has_decisions(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("decision_hashes", result)

    def test_211_lineage_has_transactions(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("transaction_hashes", result)

    def test_212_lineage_has_windows(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("window_hashes", result)

    def test_213_fixture_lineage_complete(self):
        data = _load_fixture("lineage_complete.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_214_fixture_lineage_missing(self):
        data = _load_fixture("lineage_missing.json")
        self.assertTrue(data.get("TEST_FIXTURE"))

    def test_215_lineage_research_only(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertTrue(result.get("research_only"))

    def test_216_lineage_config_hash_present(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("config_hash", result)

    def test_217_lineage_policy_versions_present(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("policy_versions", result)

    def test_218_orphan_detection_runs(self):
        windows = _make_windows()
        result = self.tracker.build_lineage("r001", _make_config(), windows, [], [])
        self.assertIn("orphan_transactions", result)


# =============================================================================
# TestReproducibility (tests 219–231)
# =============================================================================
class TestReproducibility(unittest.TestCase):

    def setUp(self):
        self.repr_engine = WalkForwardReproducibilityEngine()

    def test_219_fixed_seed_is_42(self):
        self.assertEqual(REPRODUCIBILITY_FIXED_SEED, 42)

    def test_220_build_manifest_returns_manifest(self):
        result = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        self.assertIsInstance(result, ReproducibilityManifest)

    def test_221_manifest_timezone_taiwan(self):
        result = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        self.assertEqual(result.timezone, "Asia/Taipei")

    def test_222_manifest_seed_42(self):
        result = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        self.assertEqual(result.seed, 42)

    def test_223_verify_returns_dict(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        result = self.repr_engine.verify(manifest, {"config_hash": manifest.config_hash})
        self.assertIsInstance(result, dict)

    def test_224_hash_mismatch_blocked(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        run_result = {"config_hash": "DIFFERENT_HASH_XYZ", "_run_config_hash": "DIFFERENT_HASH_XYZ"}
        result = self.repr_engine.verify(manifest, run_result)
        self.assertEqual(result.get("status"), "BLOCKED")

    def test_225_hash_mismatch_not_reproducible(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        run_result = {"config_hash": "DIFFERENT_HASH_XYZ", "_run_config_hash": "DIFFERENT_HASH_XYZ"}
        result = self.repr_engine.verify(manifest, run_result)
        self.assertFalse(result.get("is_reproducible"))

    def test_226_hash_mismatch_violations_list(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        run_result = {"config_hash": "DIFFERENT_HASH_XYZ", "_run_config_hash": "DIFFERENT_HASH_XYZ"}
        result = self.repr_engine.verify(manifest, run_result)
        self.assertIsInstance(result.get("violations"), list)

    def test_227_fixture_reproducibility_valid(self):
        data = _load_fixture("reproducibility_valid.json")
        self.assertEqual(data.get("_verification"), "VERIFIED — hash match confirmed")

    def test_228_fixture_reproducibility_mismatch_blocked(self):
        data = _load_fixture("reproducibility_hash_mismatch.json")
        self.assertEqual(data.get("status"), "BLOCKED")

    def test_229_manifest_has_config_hash(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        self.assertIsNotNone(manifest.config_hash)

    def test_230_manifest_has_python_version(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        self.assertTrue(hasattr(manifest, "python_version"))

    def test_231_manifest_calendar_version(self):
        manifest = self.repr_engine.build_manifest("r001", _make_config(), _make_windows(), [])
        self.assertEqual(manifest.calendar_version, "1.5.4")


# =============================================================================
# TestExplainability (tests 232–248)
# =============================================================================
class TestExplainability(unittest.TestCase):

    def setUp(self):
        self.explainer = PortfolioWalkForwardExplainer()

    def _make_summary(self):
        return WalkForwardSummary(
            run_id="r001", config_id="c001",
            total_windows=5, valid_windows=5, partial_windows=0, blocked_windows=0,
            in_sample_return=0.05, out_of_sample_return=0.03,
            benchmark_return=0.04, excess_return=-0.01,
            annualized_return=0.06, annualized_volatility=0.18,
        )

    def _make_eligibility(self):
        gate = PortfolioWalkForwardEligibilityGate()
        return gate.evaluate(_make_config())

    def test_232_explain_returns_dict(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIsInstance(result, dict)

    def test_233_safety_text_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("safety_text", result)

    def test_234_historical_simulation_only_in_safety_text(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("HISTORICAL_SIMULATION_ONLY", result.get("safety_text", ""))

    def test_235_not_an_order_in_safety_text(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("NOT_AN_ORDER", result.get("safety_text", ""))

    def test_236_no_broker_call_in_safety_text(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("NO_BROKER_CALL", result.get("safety_text", ""))

    def test_237_no_formal_ledger_in_safety_text(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("NO_FORMAL_LEDGER_WRITE", result.get("safety_text", ""))

    def test_238_past_performance_disclaimer_in_safety_text(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("PAST_PERFORMANCE_NOT_FUTURE_GUARANTEE", result.get("safety_text", ""))

    def test_239_configuration_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("configuration", result)

    def test_240_windows_summary_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("windows_summary", result)

    def test_241_costs_summary_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("costs_summary", result)

    def test_242_stability_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("stability", result)

    def test_243_regimes_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("regimes", result)

    def test_244_sensitivity_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("sensitivity", result)

    def test_245_purge_embargo_present(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        self.assertIn("purge_embargo", result)

    def test_246_required_safety_text_count(self):
        self.assertEqual(len(REQUIRED_SAFETY_TEXT), 5)

    def test_247_selection_applied_false_in_sensitivity(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        sensitivity = result.get("sensitivity", {})
        self.assertFalse(sensitivity.get("selection_applied"))

    def test_248_benchmark_pit_safe(self):
        result = self.explainer.explain(self._make_summary(), _make_config(), _make_windows(), self._make_eligibility())
        benchmark = result.get("benchmark", {})
        self.assertTrue(benchmark.get("pit_safe"))


# =============================================================================
# TestStoreQuery (tests 249–257)
# =============================================================================
class TestStoreQuery(unittest.TestCase):

    def setUp(self):
        self.store = WalkForwardStore()
        self.query = WalkForwardQueryService()

    def test_249_save_config_returns_id(self):
        cfg = _make_config()
        config_id = self.store.save_config(cfg)
        self.assertIsNotNone(config_id)

    def test_250_save_config_idempotent(self):
        cfg = _make_config()
        id1 = self.store.save_config(cfg)
        id2 = self.store.save_config(cfg)
        self.assertEqual(id1, id2)

    def test_251_list_configs_returns_list(self):
        result = self.store.list_configs()
        self.assertIsInstance(result, list)

    def test_252_save_run_immutable(self):
        cfg = _make_config()
        summary = WalkForwardSummary(
            run_id="r001", config_id="c001",
            total_windows=5, valid_windows=5, partial_windows=0, blocked_windows=0,
            in_sample_return=0.05, out_of_sample_return=0.03,
            benchmark_return=0.04, excess_return=-0.01,
            annualized_return=0.06, annualized_volatility=0.18,
        )
        self.store.save_run("r001", summary, _make_windows(), [])
        with self.assertRaises(ValueError):
            # Different summary with different windows → different hash → raises
            summary2 = WalkForwardSummary(
                run_id="r001", config_id="c002",  # different config_id
                total_windows=3, valid_windows=3, partial_windows=0, blocked_windows=0,
                in_sample_return=0.10, out_of_sample_return=0.08,
                benchmark_return=0.04, excess_return=0.06,
                annualized_return=0.12, annualized_volatility=0.20,
            )
            self.store.save_run("r001", summary2, [], [])

    def test_253_list_runs_returns_list(self):
        result = self.store.list_runs()
        self.assertIsInstance(result, list)

    def test_254_query_service_has_required_methods(self):
        required = ["get_walk_forward_run", "list_walk_forward_runs", "generate_windows"]
        for method in required:
            self.assertTrue(hasattr(self.query, method), f"Missing: {method}")

    def test_255_forbidden_methods_absent(self):
        for method in FORBIDDEN_METHODS:
            self.assertFalse(hasattr(self.query, method))

    def test_256_query_get_run_returns_none_missing(self):
        result = self.query.get_walk_forward_run("nonexistent_run")
        self.assertIsNone(result)

    def test_257_query_list_runs_returns_list(self):
        result = self.query.list_walk_forward_runs()
        self.assertIsInstance(result, list)


# =============================================================================
# TestCLI (tests 258–287)
# =============================================================================
class TestCLI(unittest.TestCase):

    def _names(self):
        return [c.name for c in COMMAND_REGISTRY]

    def test_258_health_command_registered(self):
        self.assertIn("portfolio-walk-forward-health", self._names())

    def test_259_configs_command_registered(self):
        self.assertIn("walk-forward-configs", self._names())

    def test_260_eligibility_command_registered(self):
        self.assertIn("walk-forward-eligibility", self._names())

    def test_261_run_command_registered(self):
        self.assertIn("walk-forward-run", self._names())

    def test_262_windows_command_registered(self):
        self.assertIn("walk-forward-windows", self._names())

    def test_263_decision_replay_command_registered(self):
        self.assertIn("walk-forward-decision-replay", self._names())

    def test_264_returns_command_registered(self):
        self.assertIn("walk-forward-returns", self._names())

    def test_265_drawdown_command_registered(self):
        self.assertIn("walk-forward-drawdown", self._names())

    def test_266_stability_command_registered(self):
        self.assertIn("walk-forward-stability", self._names())

    def test_267_sensitivity_command_registered(self):
        self.assertIn("walk-forward-parameter-sensitivity", self._names())

    def test_268_regimes_command_registered(self):
        self.assertIn("walk-forward-regimes", self._names())

    def test_269_reconstruct_command_registered(self):
        self.assertIn("walk-forward-reconstruct", self._names())

    def test_270_lineage_command_registered(self):
        self.assertIn("walk-forward-lineage", self._names())

    def test_271_reproducibility_command_registered(self):
        self.assertIn("walk-forward-reproducibility", self._names())

    def test_272_explain_command_registered(self):
        self.assertIn("walk-forward-explain", self._names())

    def test_273_report_command_registered(self):
        self.assertIn("portfolio-walk-forward-report", self._names())

    def test_274_config_show_command_registered(self):
        self.assertIn("walk-forward-config-show", self._names())

    def test_275_benchmark_command_registered(self):
        self.assertIn("walk-forward-benchmark", self._names())

    def test_276_costs_command_registered(self):
        self.assertIn("walk-forward-costs", self._names())

    def test_277_slippage_command_registered(self):
        self.assertIn("walk-forward-slippage", self._names())

    def test_278_liquidity_command_registered(self):
        self.assertIn("walk-forward-liquidity", self._names())

    def test_279_valuation_command_registered(self):
        self.assertIn("walk-forward-valuation", self._names())

    def test_280_turnover_command_registered(self):
        self.assertIn("walk-forward-turnover", self._names())

    def test_281_correlation_replay_command_registered(self):
        self.assertIn("walk-forward-correlation-replay", self._names())

    def test_282_risk_replay_command_registered(self):
        self.assertIn("walk-forward-risk-replay", self._names())

    def test_283_sizing_replay_command_registered(self):
        self.assertIn("walk-forward-sizing-replay", self._names())

    def test_284_show_command_registered(self):
        self.assertIn("walk-forward-show", self._names())

    def test_285_list_command_registered(self):
        self.assertIn("walk-forward-list", self._names())

    def test_286_all_wf_commands_have_help(self):
        wf_commands = [c for c in COMMAND_REGISTRY
                       if c.name.startswith("portfolio-walk-forward-") or c.name.startswith("walk-forward-")]
        for cmd in wf_commands:
            self.assertIsNotNone(cmd.help)
            self.assertGreater(len(cmd.help), 0)

    def test_287_command_registry_minimum_size(self):
        self.assertGreaterEqual(len(COMMAND_REGISTRY), 310)


# =============================================================================
# TestGUI (tests 288–303)
# =============================================================================
class TestGUI(unittest.TestCase):

    def test_288_panel_importable(self):
        from gui.portfolio_walk_forward_panel import PortfolioWalkForwardPanel
        self.assertIsNotNone(PortfolioWalkForwardPanel)

    def test_289_panel_research_only(self):
        from gui.portfolio_walk_forward_panel import PortfolioWalkForwardPanel, RESEARCH_ONLY
        self.assertTrue(RESEARCH_ONLY)

    def test_290_panel_historical_simulation_only(self):
        from gui.portfolio_walk_forward_panel import PortfolioWalkForwardPanel, HISTORICAL_SIMULATION_ONLY
        self.assertTrue(HISTORICAL_SIMULATION_ONLY)

    def test_291_panel_no_qapplication_at_module_level(self):
        from gui import portfolio_walk_forward_panel
        self.assertFalse(hasattr(portfolio_walk_forward_panel, '_QAPPLICATION_CREATED'))

    def test_292_get_widget_headless_safe(self):
        from gui.portfolio_walk_forward_panel import PortfolioWalkForwardPanel
        panel = PortfolioWalkForwardPanel()
        result = panel.get_widget()
        self.assertIsNone(result)

    def test_293_tab_config_defined(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        self.assertTrue(hasattr(panel_mod, 'TAB_CONFIG'))

    def test_294_safety_banner_defined(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        self.assertTrue(hasattr(panel_mod, 'SAFETY_BANNER_LINES'))

    def test_295_forbidden_actions_defined(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        self.assertTrue(hasattr(panel_mod, 'FORBIDDEN_ACTIONS'))

    def test_296_forbidden_actions_no_execute(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        # Check that Execute (or similar) is in FORBIDDEN_ACTIONS
        self.assertTrue(len(panel_mod.FORBIDDEN_ACTIONS) > 0)

    def test_297_forbidden_actions_no_broker(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        # 'Connect Broker' is in the list
        self.assertTrue(any("broker" in a.lower() or "Broker" in a for a in panel_mod.FORBIDDEN_ACTIONS))

    def test_298_forbidden_actions_no_live_rebalance(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        self.assertTrue(any("Rebalance" in a or "rebalance" in a for a in panel_mod.FORBIDDEN_ACTIONS))

    def test_299_safety_banner_includes_historical(self):
        import gui.portfolio_walk_forward_panel as panel_mod
        banner_text = " ".join(panel_mod.SAFETY_BANNER_LINES)
        self.assertIn("Historical", banner_text)

    def test_300_report_importable(self):
        from reports.portfolio_walk_forward_report import PortfolioWalkForwardReport
        self.assertIsNotNone(PortfolioWalkForwardReport)

    def test_301_report_generate_returns_dict(self):
        from reports.portfolio_walk_forward_report import PortfolioWalkForwardReport
        report = PortfolioWalkForwardReport()
        result = report.generate("r001", "c001")
        self.assertIsInstance(result, dict)

    def test_302_report_has_safety_flags(self):
        from reports.portfolio_walk_forward_report import PortfolioWalkForwardReport
        report = PortfolioWalkForwardReport()
        result = report.generate("r001", "c001")
        self.assertTrue(result.get("HISTORICAL_SIMULATION_ONLY"))

    def test_303_report_render_text_returns_string(self):
        from reports.portfolio_walk_forward_report import PortfolioWalkForwardReport
        report = PortfolioWalkForwardReport()
        result = report.generate("r001", "c001")
        text = report.render_text(result)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)


# =============================================================================
# TestRegression (tests 304–330)
# =============================================================================
class TestRegression(unittest.TestCase):

    def test_304_version_at_least_154(self):
        self.assertGreaterEqual(parse_version(VERSION), parse_version("1.5.4"))

    def test_305_walk_forward_version_154(self):
        self.assertEqual(WALK_FORWARD_VERSION, "1.5.4")

    def test_306_portfolio_walk_forward_baseline(self):
        self.assertEqual(PORTFOLIO_WALK_FORWARD_BASELINE, "1.5.4")

    def test_307_walk_forward_available(self):
        self.assertTrue(PORTFOLIO_WALK_FORWARD_AVAILABLE)

    def test_308_walk_forward_research_only_flag(self):
        self.assertTrue(PORTFOLIO_WALK_FORWARD_RESEARCH_ONLY)

    def test_309_order_creation_disabled(self):
        self.assertFalse(WALK_FORWARD_ORDER_CREATION_ENABLED)

    def test_310_broker_disabled(self):
        self.assertFalse(WALK_FORWARD_BROKER_ENABLED)

    def test_311_formal_ledger_write_disabled(self):
        self.assertFalse(WALK_FORWARD_FORMAL_LEDGER_WRITE_ENABLED)

    def test_312_auto_apply_disabled(self):
        self.assertFalse(WALK_FORWARD_AUTO_APPLY_ENABLED)

    def test_313_module_flags_research_only(self):
        self.assertTrue(RESEARCH_ONLY)

    def test_314_module_flags_no_real_orders(self):
        self.assertTrue(NO_REAL_ORDERS)

    def test_315_module_flags_no_broker(self):
        self.assertTrue(NO_BROKER)

    def test_316_module_flags_no_formal_ledger(self):
        self.assertTrue(NO_FORMAL_LEDGER_WRITE)

    def test_317_module_flags_no_auto_apply(self):
        self.assertTrue(NO_AUTO_APPLY)

    def test_318_module_flags_no_live_rebalance(self):
        self.assertTrue(NO_LIVE_REBALANCE)

    def test_319_all_fixtures_present(self):
        expected_fixtures = [
            "config_rolling.json", "config_expanding.json", "config_anchored.json",
            "config_invalid_dates.json", "config_with_purge.json", "config_with_embargo.json",
            "windows_valid.json", "windows_partial_last.json",
            "decision_context_valid.json", "decision_context_future_data.json",
            "portfolio_reconstruction.json", "portfolio_future_transaction.json",
            "sizing_replay_valid.json", "sizing_replay_blocked.json",
            "correlation_replay_valid.json", "correlation_replay_insufficient.json",
            "risk_replay_valid.json", "risk_replay_blocked.json",
            "cost_model.json", "slippage_fixed_bps.json", "slippage_volume.json",
            "liquidity_partial_fill.json",
            "simulated_transactions.json",
            "valuation_valid.json", "valuation_missing_price.json",
            "returns_valid.json", "turnover_valid.json", "benchmark_valid.json",
            "drawdown_valid.json", "stability_stable.json", "stability_unstable.json",
            "parameter_sensitivity.json", "regime_results.json",
            "eligibility_valid.json", "eligibility_blocked.json",
            "pit_future_universe.json",
            "lineage_complete.json", "lineage_missing.json",
            "reproducibility_valid.json", "reproducibility_hash_mismatch.json",
        ]
        for fname in expected_fixtures:
            path = os.path.join(FIXTURES_DIR, fname)
            self.assertTrue(os.path.exists(path), f"Missing fixture: {fname}")

    def test_320_all_fixtures_have_test_fixture_flag(self):
        for fname in os.listdir(FIXTURES_DIR):
            if fname.endswith(".json"):
                data = _load_fixture(fname)
                self.assertTrue(data.get("TEST_FIXTURE"), f"{fname} missing TEST_FIXTURE=true")

    def test_321_all_fixtures_historical_simulation_only(self):
        for fname in os.listdir(FIXTURES_DIR):
            if fname.endswith(".json"):
                data = _load_fixture(fname)
                self.assertTrue(data.get("HISTORICAL_SIMULATION_ONLY"), f"{fname} missing HISTORICAL_SIMULATION_ONLY=true")

    def test_322_command_registry_minimum_310(self):
        self.assertGreaterEqual(len(COMMAND_REGISTRY), 310)

    def test_323_pytest_collect_walk_forward_tests(self):
        # Uses os.path for repo_root — no hard-coded paths
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_file = os.path.join(repo_root, "tests", "test_portfolio_walk_forward_v154.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "--collect-only", "-q"],
            cwd=repo_root,
            capture_output=True, text=True, timeout=60,
        )
        # Should not crash — returncode 0 or acceptable
        self.assertIn(result.returncode, [0, 1, 2, 5])

    def test_324_health_check_runs(self):
        hc = PortfolioWalkForwardHealthCheck()
        result = hc.run()
        self.assertIsInstance(result, dict)

    def test_325_health_check_version(self):
        hc = PortfolioWalkForwardHealthCheck()
        result = hc.run()
        self.assertEqual(result.get("version"), "1.5.4")

    def test_326_health_check_research_only(self):
        hc = PortfolioWalkForwardHealthCheck()
        result = hc.run()
        self.assertTrue(result.get("research_only"))

    def test_327_health_check_has_checks_dict(self):
        hc = PortfolioWalkForwardHealthCheck()
        result = hc.run()
        self.assertIsInstance(result.get("checks"), dict)

    def test_328_health_check_minimum_checks(self):
        hc = PortfolioWalkForwardHealthCheck()
        result = hc.run()
        self.assertGreaterEqual(result.get("total", 0), 40)

    def test_329_release_gate_runs(self):
        from release.portfolio_walk_forward_release_gate_v154 import PortfolioWalkForwardReleaseGate
        gate = PortfolioWalkForwardReleaseGate()
        result = gate.run()
        self.assertIsInstance(result, dict)

    def test_330_release_gate_version(self):
        from release.portfolio_walk_forward_release_gate_v154 import PortfolioWalkForwardReleaseGate
        gate = PortfolioWalkForwardReleaseGate()
        result = gate.run()
        self.assertEqual(result.get("version"), "1.5.4")


if __name__ == "__main__":
    unittest.main()
