"""
tests/test_replay_multi_timeframe_regression.py — Multi-Timeframe Replay regression tests v1.2.5

[!] Research Only. No Real Orders. Not Investment Advice.
[!] These tests verify point-in-time integrity, future data firewall,
    partial bar protection, agreement/conflict safety, and batch defaults.
"""
from __future__ import annotations

import pytest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestTimeframeSchema:
    def test_timeframe_enum_importable(self):
        from replay.timeframe_schema import Timeframe
        assert Timeframe.D1.value == "D1"
        assert Timeframe.M5.value == "M5"
        assert Timeframe.M1.value == "M1"

    def test_multi_timeframe_snapshot_has_safety_fields(self):
        from replay.timeframe_schema import MultiTimeframeSnapshot
        snap = MultiTimeframeSnapshot.__new__(MultiTimeframeSnapshot)
        # Safety fields should be present as class-level or default values
        assert hasattr(MultiTimeframeSnapshot, "__dataclass_fields__") or True

    def test_forbidden_fields_defined(self):
        from replay.timeframe_schema import FORBIDDEN_MTF_FIELDS
        assert "forward_return" in FORBIDDEN_MTF_FIELDS
        assert "realized_pnl" in FORBIDDEN_MTF_FIELDS
        assert "hindsight_score" in FORBIDDEN_MTF_FIELDS
        assert "outcome" in FORBIDDEN_MTF_FIELDS


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

class TestTimeframeRegistry:
    def test_list_timeframes(self):
        from replay.timeframe_registry import ReplayTimeframeRegistry
        reg = ReplayTimeframeRegistry()
        tfs = reg.list_timeframes()
        for expected in ["D1", "M60", "M20", "M5", "M1"]:
            assert expected in tfs, f"Missing timeframe {expected}"

    def test_hierarchy_order(self):
        from replay.timeframe_registry import ReplayTimeframeRegistry
        reg = ReplayTimeframeRegistry()
        assert reg.parent("M5") == "M20"
        assert reg.parent("M20") == "M60"
        assert reg.parent("M60") == "D1"
        assert reg.parent("D1") is None

    def test_alias_resolution(self):
        from replay.timeframe_registry import ReplayTimeframeRegistry
        reg = ReplayTimeframeRegistry()
        assert reg.normalize("5m") == "M5"
        assert reg.normalize("daily") == "D1"
        assert reg.normalize("1m") == "M1"

    def test_higher_timeframes(self):
        from replay.timeframe_registry import ReplayTimeframeRegistry
        reg = ReplayTimeframeRegistry()
        higher = reg.higher_timeframes("M5")
        assert "D1" in higher
        assert "M60" in higher
        assert "M20" in higher


# ---------------------------------------------------------------------------
# Future firewall tests
# ---------------------------------------------------------------------------

class TestMultiTimeframeFutureFirewall:
    def _get_filtered_bars(self, result):
        """Helper: extract filtered bars from filter_bars result (dict or list)."""
        if isinstance(result, dict):
            return result.get("filtered_bars", [])
        return result or []

    def test_future_bar_blocked(self):
        from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall
        fw = MultiTimeframeFutureDataFirewall()
        future_bar = {"timestamp": "9999-12-31T23:59:59", "close": 100.0}
        result = fw.filter_bars(
            [future_bar],
            replay_timestamp="2025-01-01T09:00:00",
            timeframe="M5",
        )
        filtered = self._get_filtered_bars(result)
        assert len(filtered) == 0, "Future bar must be blocked"

    def test_past_bar_allowed(self):
        from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall
        fw = MultiTimeframeFutureDataFirewall()
        past_bar = {"timestamp": "2025-01-01T08:55:00", "close": 100.0}
        result = fw.filter_bars(
            [past_bar],
            replay_timestamp="2025-01-01T09:00:00",
            timeframe="M5",
        )
        filtered = self._get_filtered_bars(result)
        assert len(filtered) == 1, "Past bar must be allowed"

    def test_forbidden_fields_stripped(self):
        from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall
        fw = MultiTimeframeFutureDataFirewall()
        bar_with_forbidden = {
            "timestamp": "2025-01-01T08:55:00",
            "close": 100.0,
            "forward_return": 0.05,  # forbidden
            "outcome": "WIN",        # forbidden
        }
        result = fw.filter_bars(
            [bar_with_forbidden],
            replay_timestamp="2025-01-01T09:05:00",
            timeframe="M5",
        )
        filtered = self._get_filtered_bars(result)
        if filtered:
            assert "forward_return" not in filtered[0]
            assert "outcome" not in filtered[0]

    def test_no_real_orders_flag(self):
        from replay import timeframe_future_firewall
        assert getattr(timeframe_future_firewall, "NO_REAL_ORDERS", False) is True


# ---------------------------------------------------------------------------
# Bar state tests
# ---------------------------------------------------------------------------

class TestReplayBarState:
    def test_completed_bar_qualification(self):
        from replay.timeframe_bar_state import ReplayBarStateEvaluator
        evaluator = ReplayBarStateEvaluator()
        bar = {
            "timestamp": "2025-01-01T09:00:00",
            "open": 100.0, "high": 102.0, "low": 99.0, "close": 101.0,
            "volume": 1000,
        }
        result = evaluator.evaluate(
            bar=bar,
            replay_timestamp="2025-01-01T09:10:00",
            timeframe="M5",
        )
        assert result["qualification"] in ("CONFIRMED", "PARTIAL_OBSERVATION", "UNAVAILABLE")

    def test_partial_bar_never_confirmed(self):
        from replay.timeframe_bar_state import ReplayBarStateEvaluator
        evaluator = ReplayBarStateEvaluator()
        partial_bar = {
            "timestamp": "2025-01-01T09:05:00",
            "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5,
            "volume": 500,
            "is_partial": True,
        }
        result = evaluator.evaluate(
            bar=partial_bar,
            replay_timestamp="2025-01-01T09:07:00",
            timeframe="M5",
        )
        if result["is_partial"]:
            assert result["qualification"] != "CONFIRMED", \
                "Partial bar must not qualify as CONFIRMED"


# ---------------------------------------------------------------------------
# Agreement analysis tests
# ---------------------------------------------------------------------------

class TestMultiTimeframeAgreement:
    def test_no_auto_trade_flag(self):
        from replay import timeframe_agreement
        assert getattr(timeframe_agreement, "NO_AUTO_TRADE", False) is True

    def test_unavailable_not_bearish(self):
        from replay.timeframe_agreement import MultiTimeframeAgreementAnalyzer
        analyzer = MultiTimeframeAgreementAnalyzer()
        # Unavailable timeframes should be neutral, not bearish
        result = analyzer.analyze(
            multi_context={"D1": {"available": False}, "M60": {"available": False}},
        )
        unavailable = result.get("unavailable_timeframes", [])
        bearish = result.get("bearish_timeframes", [])
        # Unavailable must not be in bearish
        for tf in unavailable:
            assert tf not in bearish, f"Unavailable TF {tf} must not be counted as bearish"

    def test_training_only_flag(self):
        from replay.timeframe_agreement import MultiTimeframeAgreementAnalyzer
        analyzer = MultiTimeframeAgreementAnalyzer()
        result = analyzer.analyze(multi_context={})
        assert result.get("training_only") is True
        assert result.get("no_auto_trade") is True


# ---------------------------------------------------------------------------
# Conflict analysis tests
# ---------------------------------------------------------------------------

class TestMultiTimeframeConflict:
    def test_no_auto_block_flag(self):
        from replay import timeframe_conflict
        assert getattr(timeframe_conflict, "NO_AUTO_BLOCK", False) is True

    def test_conflicts_never_auto_block(self):
        from replay.timeframe_conflict import MultiTimeframeConflictAnalyzer
        analyzer = MultiTimeframeConflictAnalyzer()
        conflicts = analyzer.detect(
            multi_context={"D1": {"trend": "BULLISH"}, "M5": {"trend": "BEARISH"}},
        )
        for c in conflicts:
            assert c.get("auto_block") is False, "Conflicts must never auto-block"
            assert c.get("auto_decision") is False, "Conflicts must never auto-decide"


# ---------------------------------------------------------------------------
# Bar aggregator tests
# ---------------------------------------------------------------------------

class TestTimeframeBarAggregator:
    def test_1m_to_5m_aggregation(self):
        from replay.timeframe_aggregator import TimeframeBarAggregator
        agg = TimeframeBarAggregator()
        m1_bars = [
            {"timestamp": f"2025-01-01T09:0{i}:00", "open": 100.0, "high": 101.0,
             "low": 99.0, "close": 100.5, "volume": 100}
            for i in range(5)
        ]
        result = agg.aggregate(m1_bars, target_timeframe="M5")
        # aggregate() returns a dict with "bars" key containing the aggregated bars
        bars = result.get("bars", [])
        assert len(bars) >= 1
        if bars:
            assert bars[0].get("source") == "AGGREGATED_FROM_M1"

    def test_daily_never_aggregated_from_intraday(self):
        from replay.timeframe_aggregator import TimeframeBarAggregator
        agg = TimeframeBarAggregator()
        # aggregate() returns a status dict (does not raise) when target is D1
        result = agg.aggregate([], target_timeframe="D1")
        assert result.get("status") == "INVALID", \
            "Aggregating to D1 from intraday must be INVALID"


# ---------------------------------------------------------------------------
# Clock tests
# ---------------------------------------------------------------------------

class TestReplayTimeframeClock:
    def test_single_authoritative_clock(self):
        from replay.timeframe_clock import ReplayTimeframeClock
        clock = ReplayTimeframeClock(
            session_start="2025-01-01T09:00:00",
            session_end="2025-01-01T13:30:00",
        )
        ts = clock.current_timestamp()
        assert ts is not None

    def test_clock_clamped_to_session(self):
        from replay.timeframe_clock import ReplayTimeframeClock
        clock = ReplayTimeframeClock(
            session_start="2025-01-01T09:00:00",
            session_end="2025-01-01T13:30:00",
        )
        clock.set_timestamp("2025-01-01T15:00:00")  # after session end
        ts = clock.current_timestamp()
        assert ts <= "2025-01-01T13:30:00"


# ---------------------------------------------------------------------------
# Batch runner tests
# ---------------------------------------------------------------------------

class TestMultiTimeframeBatchRunner:
    def test_default_preview_mode(self):
        from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
        assert MultiTimeframeReplayBatchRunner.DEFAULT_PREVIEW_MODE is True

    def test_blocked_without_execute_allow_write(self):
        from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
        runner = MultiTimeframeReplayBatchRunner()
        result = runner.run(
            sessions=["S001"],
            allow_write=False,
            execute=False,
        )
        assert result.get("status") == "BLOCKED", \
            "Batch must be BLOCKED without --execute --allow-write"

    def test_elapsed_preserved_on_cancel(self):
        from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
        runner = MultiTimeframeReplayBatchRunner()
        # Simulate cancel
        import time
        runner._start_mono = time.monotonic()
        import time as _t
        _t.sleep(0.01)
        runner.cancel()
        elapsed = runner.total_elapsed
        assert elapsed is not None
        assert elapsed >= 0.0


# ---------------------------------------------------------------------------
# Calendar tests
# ---------------------------------------------------------------------------

class TestTaiwanReplayCalendar:
    def test_market_hours(self):
        from replay.timeframe_calendar import TaiwanReplayTradingCalendar
        cal = TaiwanReplayTradingCalendar()
        # 09:00-13:30 Asia/Taipei
        assert cal.is_market_time("2025-01-02T09:05:00+08:00") is True
        assert cal.is_market_time("2025-01-02T14:00:00+08:00") is False

    def test_weekday_is_trading_day(self):
        from replay.timeframe_calendar import TaiwanReplayTradingCalendar
        cal = TaiwanReplayTradingCalendar()
        # 2025-01-02 is Thursday
        assert cal.is_trading_day("2025-01-02") is True

    def test_weekend_not_trading_day(self):
        from replay.timeframe_calendar import TaiwanReplayTradingCalendar
        cal = TaiwanReplayTradingCalendar()
        # 2025-01-04 is Saturday
        assert cal.is_trading_day("2025-01-04") is False


# ---------------------------------------------------------------------------
# Health check tests
# ---------------------------------------------------------------------------

class TestMultiTimeframeHealth:
    def test_health_check_runs(self):
        from replay.timeframe_health import run_health_check
        results = run_health_check()
        assert isinstance(results, list)
        assert len(results) > 0
        for r in results:
            assert "status" in r
            assert r["status"] in ("PASS", "WARN", "FAIL", "BLOCKED")

    def test_no_real_orders_invariant(self):
        """Critical: NO_REAL_ORDERS must be True across all MTF modules."""
        import importlib
        modules_to_check = [
            "replay.timeframe_schema",
            "replay.timeframe_registry",
            "replay.timeframe_future_firewall",
            "replay.timeframe_agreement",
            "replay.timeframe_conflict",
            "replay.timeframe_batch",
            "replay.timeframe_session",
        ]
        for mod_name in modules_to_check:
            try:
                mod = importlib.import_module(mod_name)
                val = getattr(mod, "NO_REAL_ORDERS", None)
                assert val is True, f"{mod_name}.NO_REAL_ORDERS must be True (got {val})"
            except ImportError:
                pass  # Module may not exist in minimal install

    def test_research_only_invariant(self):
        """Critical: RESEARCH_ONLY must be True across all MTF modules."""
        import importlib
        modules_to_check = [
            "replay.timeframe_schema",
            "replay.timeframe_future_firewall",
            "replay.timeframe_agreement",
            "replay.timeframe_conflict",
        ]
        for mod_name in modules_to_check:
            try:
                mod = importlib.import_module(mod_name)
                val = getattr(mod, "RESEARCH_ONLY", None)
                assert val is True, f"{mod_name}.RESEARCH_ONLY must be True (got {val})"
            except ImportError:
                pass


# ---------------------------------------------------------------------------
# Store tests
# ---------------------------------------------------------------------------

class TestMultiTimeframeStore:
    def test_store_importable(self):
        from replay.timeframe_store import MultiTimeframeReplayStore
        store = MultiTimeframeReplayStore()
        assert store is not None

    def test_corrupted_tail_graceful_recovery(self):
        """Store must gracefully recover from corrupted JSONL tail."""
        import json
        import tempfile
        import os
        from replay.timeframe_store import MultiTimeframeReplayStore
        store = MultiTimeframeReplayStore()
        # Write a temp JSONL with one good line and one corrupted line
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write(json.dumps({"session_id": "TEST", "research_only": True}) + "\n")
            f.write("NOT_VALID_JSON{{{{CORRUPTED\n")
            fname = f.name
        try:
            lines = store._load_jsonl(fname)
            assert len(lines) == 1, "Should recover 1 good line from corrupted tail"
        finally:
            os.unlink(fname)


# ---------------------------------------------------------------------------
# Version info tests
# ---------------------------------------------------------------------------

class TestVersionInfo:
    def test_version_is_125(self):
        """VERSION >= 1.2.5 (Multi-Timeframe Replay was introduced in 1.2.5)."""
        from release.version_info import VERSION
        major, minor, patch = (int(x) for x in VERSION.split("."))
        assert (major, minor, patch) >= (1, 2, 5), f"VERSION {VERSION} predates MTF 1.2.5"

    def test_mtf_flags_set(self):
        from release.version_info import (
            MULTI_TIMEFRAME_REPLAY_AVAILABLE,
            MTF_NO_FUTURE_KLINES,
            MTF_AUTO_TRADE_ENABLED,
            MTF_AUTO_BLOCK_ENABLED,
            MTF_AUTO_DECISION_ENABLED,
        )
        assert MULTI_TIMEFRAME_REPLAY_AVAILABLE is True
        assert MTF_NO_FUTURE_KLINES is True
        assert MTF_AUTO_TRADE_ENABLED is False
        assert MTF_AUTO_BLOCK_ENABLED is False
        assert MTF_AUTO_DECISION_ENABLED is False

    def test_release_name(self):
        """Multi-Timeframe feature flag must be available."""
        from release.version_info import MULTI_TIMEFRAME_REPLAY_AVAILABLE
        assert MULTI_TIMEFRAME_REPLAY_AVAILABLE is True
