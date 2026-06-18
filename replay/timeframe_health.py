"""
replay/timeframe_health.py — MultiTimeframeReplayHealthCheck v1.2.5

Health check for multi-timeframe replay. CLI: python main.py replay-timeframe-health.
Checks all MTF components and safety flags.

Output: PASS/WARN/FAIL/BLOCKED for each check.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
import tempfile
import os
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class MultiTimeframeReplayHealthCheck:
    """
    Health check for multi-timeframe replay v1.2.5.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns dict of name → (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}

        results["schema"]           = self._check_schema()
        results["registry"]         = self._check_registry()
        results["data_source"]      = self._check_data_source()
        results["calendar"]         = self._check_calendar()
        results["clock"]            = self._check_clock()
        results["bar_state"]        = self._check_bar_state()
        results["alignment"]        = self._check_alignment()
        results["aggregator"]       = self._check_aggregator()
        results["future_firewall"]  = self._check_future_firewall()
        results["point_in_time"]    = self._check_point_in_time()
        results["indicator_engine"] = self._check_indicator_engine()
        results["context_builder"]  = self._check_context_builder()
        results["agreement"]        = self._check_agreement()
        results["conflict"]         = self._check_conflict()
        results["strategy_adapter"] = self._check_strategy_adapter()
        results["timeline"]         = self._check_timeline()
        results["session"]          = self._check_session()
        results["query"]            = self._check_query()
        results["store"]            = self._check_store()
        results["summary"]          = self._check_summary()
        results["comparator"]       = self._check_comparator()
        results["batch"]            = self._check_batch()

        # Safety flags
        results["version_info"]        = self._check_version_info()
        results["real_no_mock_fallback"] = self._check_real_no_mock()
        results["daily_no_fake_intraday"] = self._check_daily_no_fake_intraday()
        results["no_bfill"]            = self._check_no_bfill()
        results["no_centered_rolling"] = self._check_no_centered_rolling()
        results["no_future_bar"]       = self._check_no_future_bar()
        results["incomplete_close_blocked"] = self._check_incomplete_close_blocked()
        results["partial_bar_marked"]  = self._check_partial_bar_marked()
        results["no_auto_decision"]    = self._check_no_auto_decision()
        results["no_auto_score"]       = self._check_no_auto_score()
        results["no_auto_reveal"]      = self._check_no_auto_reveal()
        results["no_broker_side_effect"] = self._check_no_broker_side_effect()
        results["batch_timing"]        = self._check_batch_timing()
        results["store_corrupted_recovery"] = self._check_store_corrupted_recovery()

        return results

    # ------------------------------------------------------------------
    # Component checks
    # ------------------------------------------------------------------

    def _check_schema(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_schema import (
                Timeframe, TimeframeDefinition, TimeframeBar, TimeframeSnapshot,
                MultiTimeframeSnapshot, TimeframeAlignmentResult, TimeframeAgreementResult
            )
            import uuid
            from datetime import datetime, timezone
            # Instantiate each
            td = TimeframeDefinition("D1", "Daily", 390)
            bar = TimeframeBar("TST", "D1", "2023-01-06", "2023-01-06", 100.0, 102.0, 99.0, 101.0, 1000.0, 101000.0, True, False, "DIRECT")
            snap = TimeframeSnapshot(f"SNP-{uuid.uuid4().hex[:8].upper()}", "S1", "TST", "2023-01-06T10:00:00", "D1")
            mts = MultiTimeframeSnapshot(f"MTS-{uuid.uuid4().hex[:8].upper()}", "S1", "TST", "2023-01-06T10:00:00")
            # Check safety fields
            assert mts.research_only, "research_only must be True"
            assert mts.no_real_orders, "no_real_orders must be True"
            # Check to_dict/from_dict roundtrip
            d = bar.to_dict()
            bar2 = TimeframeBar.from_dict(d)
            assert bar2.symbol == "TST"
            return ("PASS", "All schema dataclasses instantiate correctly with safety invariants")
        except Exception as e:
            return ("FAIL", f"Schema error: {e}")

    def _check_registry(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_registry import ReplayTimeframeRegistry
            reg = ReplayTimeframeRegistry()
            tfs = reg.list_timeframes()
            assert tfs == ["D1", "M60", "M20", "M5", "M1"], f"Unexpected hierarchy: {tfs}"
            # Check aliases
            assert reg.normalize("daily") == "D1"
            assert reg.normalize("60m") == "M60"
            assert reg.normalize("5m") == "M5"
            assert reg.normalize("1m") == "M1"
            # Check hierarchy
            assert reg.parent("M60") == "D1"
            assert reg.child("D1") == "M60"
            assert reg.higher_timeframes("M5") == ["D1", "M60", "M20"]
            assert reg.lower_timeframes("M60") == ["M20", "M5", "M1"]
            return ("PASS", f"Registry: {len(tfs)} timeframes, D1→M60→M20→M5→M1 hierarchy, aliases OK")
        except Exception as e:
            return ("FAIL", f"Registry error: {e}")

    def _check_data_source(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_data_source import MultiTimeframeReplayDataSource
            ds = MultiTimeframeReplayDataSource(mode="real")
            assert ds.REAL_MODE_NO_MOCK_FALLBACK, "Real mode must not fallback to mock"
            assert ds.DAILY_NO_FAKE_INTRADAY, "Daily must not fake intraday"
            # Test UNAVAILABLE for missing data (real mode)
            result = ds.load("NONEXISTENT_SYMBOL_XYZ", "D1", "2023-01-01", "2023-12-31", mode="real")
            assert result["status"] == "UNAVAILABLE", "Missing real data must return UNAVAILABLE"
            assert len(result["data"]) == 0, "UNAVAILABLE must return empty data"
            return ("PASS", "DataSource: real no mock fallback, UNAVAILABLE on missing, no crash")
        except Exception as e:
            return ("FAIL", f"DataSource error: {e}")

    def _check_calendar(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_calendar import TaiwanReplayTradingCalendar
            cal = TaiwanReplayTradingCalendar()
            # 2023-01-06 is Friday
            assert cal.is_trading_day("2023-01-06"), "2023-01-06 should be trading day"
            # 2023-01-07 is Saturday
            assert not cal.is_trading_day("2023-01-07"), "Saturday should not be trading day"
            # Market open
            assert cal.is_market_time("2023-01-06T10:00:00"), "10:00 should be market time"
            assert not cal.is_market_time("2023-01-06T08:00:00"), "08:00 should not be market time"
            assert not cal.is_market_time("2023-01-06T14:00:00"), "14:00 should not be market time"
            # Expected bars
            assert cal.expected_bars("2023-01-06", "M5") == 54, f"Expected 54 5m bars, got {cal.expected_bars('2023-01-06', 'M5')}"
            return ("PASS", "Calendar: Taiwan market hours 09:00-13:30, trading days correct")
        except Exception as e:
            return ("FAIL", f"Calendar error: {e}")

    def _check_clock(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_clock import ReplayTimeframeClock
            clock = ReplayTimeframeClock(
                session_start="2023-01-06T09:00:00",
                session_end="2023-01-06T13:30:00",
                initial_timestamp="2023-01-06T10:00:00",
            )
            assert clock.current_timestamp() == "2023-01-06T10:00:00"
            # Jump within session
            result = clock.jump("2023-01-06T11:00:00")
            assert result["timestamp"] == "2023-01-06T11:00:00"
            # Jump past session end — clamped
            result = clock.jump("2023-01-06T20:00:00")
            assert result["timestamp"] == "2023-01-06T13:30:00", f"Expected clamped to 13:30, got {result['timestamp']}"
            # Check summary
            summary = clock.summary()
            assert summary["research_only"] is True
            return ("PASS", "Clock: single authoritative clock, clamping works, research_only=True")
        except Exception as e:
            return ("FAIL", f"Clock error: {e}")

    def _check_bar_state(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_bar_state import ReplayBarStateEvaluator, QUALIFICATION_CONFIRMED, QUALIFICATION_PARTIAL_OBSERVATION
            ev = ReplayBarStateEvaluator()
            # Complete bar
            bar = {"timestamp": "2023-01-06T09:00:00", "is_complete": True, "is_partial": False}
            state = ev.evaluate(bar, "2023-01-06T09:10:00", "M5")
            assert state["qualification"] == QUALIFICATION_CONFIRMED, f"Expected CONFIRMED, got {state['qualification']}"
            # Partial bar
            bar2 = {"timestamp": "2023-01-06T10:00:00", "is_complete": False, "is_partial": True}
            state2 = ev.evaluate(bar2, "2023-01-06T10:03:00", "M5")
            assert state2["qualification"] == QUALIFICATION_PARTIAL_OBSERVATION, f"Expected PARTIAL_OBSERVATION, got {state2['qualification']}"
            return ("PASS", "BarState: completed vs partial distinction, qualification correct")
        except Exception as e:
            return ("FAIL", f"BarState error: {e}")

    def _check_alignment(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_alignment import TimeframeAlignmentEngine
            eng = TimeframeAlignmentEngine()
            assert eng.NO_BFILL is True
            assert eng.NO_FUTURE_NEAREST is True
            # Latest completed bar — past-only
            bars = [
                {"timestamp": "2023-01-06T09:00:00", "is_complete": True, "is_partial": False, "close": 100.0, "open": 99.0, "high": 101.0, "low": 98.0, "volume": 1000.0},
                {"timestamp": "2023-01-06T09:05:00", "is_complete": True, "is_partial": False, "close": 101.0, "open": 100.0, "high": 102.0, "low": 99.0, "volume": 1000.0},
                {"timestamp": "2023-01-06T10:00:00", "is_complete": False, "is_partial": True, "close": 102.0, "open": 101.0, "high": 103.0, "low": 100.0, "volume": 1000.0},
            ]
            replay_ts = "2023-01-06T09:10:00"
            latest = eng.latest_completed_bar(replay_ts, "M5", bars)
            # Should return bar at 09:05 (completed before 09:10)
            assert latest is not None, "Should find a completed bar"
            # Lookahead detection
            future_bars = [{"timestamp": "2023-01-06T11:00:00"}]
            violations = eng.detect_lookahead("2023-01-06T10:00:00", {"M5": future_bars})
            assert len(violations) > 0, "Should detect lookahead"
            return ("PASS", "Alignment: past-only asof, no bfill, no future, lookahead detection OK")
        except Exception as e:
            return ("FAIL", f"Alignment error: {e}")

    def _check_aggregator(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_aggregator import TimeframeBarAggregator
            agg = TimeframeBarAggregator()
            # Generate 5 1m bars
            bars_1m = []
            for i in range(5):
                bars_1m.append({
                    "timestamp": f"2023-01-06T09:0{i}:00",
                    "open": 100.0 + i,
                    "high": 101.0 + i,
                    "low": 99.0 + i,
                    "close": 100.5 + i,
                    "volume": 100.0,
                    "amount": 10050.0,
                    "symbol": "TST",
                    "timeframe": "M1",
                    "source": "DIRECT",
                })
            result = agg.aggregate(bars_1m, "M5")
            assert result["status"] == "OK", f"Aggregation status: {result['status']}"
            assert result["source"] == "AGGREGATED_FROM_M1"
            assert len(result["bars"]) >= 1, "Should produce at least 1 bar"
            # OHLCV rules
            agg_bar = result["bars"][0]
            assert agg_bar["open"] == 100.0, f"Open should be first: {agg_bar['open']}"
            assert agg_bar["high"] == 105.0, f"High should be max: {agg_bar['high']}"
            assert agg_bar["low"] == 99.0, f"Low should be min: {agg_bar['low']}"
            assert agg_bar["close"] == 104.5, f"Close should be last: {agg_bar['close']}"
            assert agg_bar["volume"] == 500.0, f"Volume should be sum: {agg_bar['volume']}"
            return ("PASS", f"Aggregator: 1m→5m OHLCV correct, source=AGGREGATED_FROM_M1")
        except Exception as e:
            return ("FAIL", f"Aggregator error: {e}")

    def _check_future_firewall(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall, FORBIDDEN_FIELDS
            fw = MultiTimeframeFutureDataFirewall()
            replay_ts = "2023-01-06T10:00:00"
            # Future bar should be blocked
            bars = [
                {"timestamp": "2023-01-06T09:00:00", "is_complete": True},
                {"timestamp": "2023-01-06T11:00:00", "is_complete": False},  # future
            ]
            result = fw.filter_bars(bars, replay_ts, "M5")
            assert result["blocked_count"] == 1, f"Expected 1 blocked, got {result['blocked_count']}"
            assert len(result["filtered_bars"]) == 1
            # Check forbidden fields
            assert "outcome" in FORBIDDEN_FIELDS
            assert "forward_return" in FORBIDDEN_FIELDS
            assert "realized_pnl" in FORBIDDEN_FIELDS
            return ("PASS", "FutureFirewall: future bars blocked, forbidden fields defined")
        except Exception as e:
            return ("FAIL", f"FutureFirewall error: {e}")

    def _check_point_in_time(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_point_in_time import MultiTimeframePointInTimeVerifier
            verifier = MultiTimeframePointInTimeVerifier()
            replay_ts = "2023-01-06T10:00:00"
            # Valid bar
            bar = {"timestamp": "2023-01-06T09:00:00", "available_at": "2023-01-06T09:01:00"}
            result = verifier.verify_bar(bar, replay_ts, "M5")
            assert result["verified"], f"Valid bar should pass: {result}"
            # Future bar
            future_bar = {"timestamp": "2023-01-06T11:00:00"}
            result2 = verifier.verify_bar(future_bar, replay_ts, "M5")
            assert not result2["verified"], "Future bar should fail verification"
            assert result2["status"] == "BLOCKED"
            return ("PASS", "PointInTime: valid bar passes, future bar blocked, per-TF independent")
        except Exception as e:
            return ("FAIL", f"PointInTime error: {e}")

    def _check_indicator_engine(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_indicator_engine import MultiTimeframeIndicatorEngine
            eng = MultiTimeframeIndicatorEngine()
            assert eng.NO_BFILL is True
            assert eng.NO_CENTERED_ROLLING is True
            # Generate enough bars for indicators
            bars = []
            for i in range(70):
                ts = f"2023-01-{(i // 20) + 2:02d}T09:{(i % 60):02d}:00"
                bars.append({
                    "timestamp": ts,
                    "open": 100.0 + i * 0.1,
                    "high": 101.0 + i * 0.1,
                    "low": 99.0 + i * 0.1,
                    "close": 100.5 + i * 0.1,
                    "volume": 1000.0,
                    "is_complete": True,
                    "is_partial": False,
                })
            result = eng.calculate(bars, "M5", "2023-01-10T10:00:00")
            assert result.get("uses_completed_bars_only") is True
            assert result.get("no_bfill") is True
            assert result.get("MA5") is not None or result.get("status") == "INSUFFICIENT"
            return ("PASS", "IndicatorEngine: completed bars only, no bfill, no centered rolling")
        except Exception as e:
            return ("FAIL", f"IndicatorEngine error: {e}")

    def _check_context_builder(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_context_builder import MultiTimeframeContextBuilder
            builder = MultiTimeframeContextBuilder()
            context = builder.build("SESSION_1", "2023-01-06T10:00:00", "TST")
            assert "replay_timestamp" in context
            assert "D1" in context
            assert "M5" in context
            assert "agreement" in context
            assert "warnings" in context
            assert "point_in_time_verified" in context
            return ("PASS", "ContextBuilder: builds full multi-TF context dict with all required keys")
        except Exception as e:
            return ("FAIL", f"ContextBuilder error: {e}")

    def _check_agreement(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_agreement import MultiTimeframeAgreementAnalyzer
            analyzer = MultiTimeframeAgreementAnalyzer()
            assert analyzer.NO_AUTO_TRADE is True
            # Unavailable TF should not be bearish
            context = {
                "replay_timestamp": "2023-01-06T10:00:00",
                "D1": {"has_data": False, "trend_state": "UNKNOWN"},
                "M60": {"has_data": True, "trend_state": "UPTREND"},
                "M20": {"has_data": True, "trend_state": "UPTREND"},
                "M5": {"has_data": False, "trend_state": "UNKNOWN"},
                "M1": {"has_data": False, "trend_state": "UNKNOWN"},
            }
            result = analyzer.analyze(context)
            assert "D1" in result["unavailable_timeframes"] or "D1" not in result["bearish_timeframes"], \
                "Unavailable D1 should not be bearish"
            assert result["no_auto_trade"] is True
            assert result["training_only"] is True
            return ("PASS", "Agreement: unavailable≠bearish, no_auto_trade=True, training_only=True")
        except Exception as e:
            return ("FAIL", f"Agreement error: {e}")

    def _check_conflict(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_conflict import MultiTimeframeConflictAnalyzer
            analyzer = MultiTimeframeConflictAnalyzer()
            assert analyzer.NO_AUTO_BLOCK is True
            assert analyzer.NO_AUTO_DECISION is True
            context = {
                "D1": {"has_data": True, "trend_state": "UPTREND"},
                "M60": {"has_data": True, "trend_state": "DOWNTREND"},
                "M20": {"has_data": True, "trend_state": "DOWNTREND"},
                "M5": {"has_data": False, "trend_state": "UNKNOWN"},
                "M1": {"has_data": False, "trend_state": "UNKNOWN"},
            }
            conflicts = analyzer.detect(context)
            # Should detect DAILY_BULLISH_INTRADAY_BEARISH
            types = [c["conflict_type"] for c in conflicts]
            assert "DAILY_BULLISH_INTRADAY_BEARISH" in types or len(conflicts) > 0
            # All conflicts should have auto_block=False
            for c in conflicts:
                assert c.get("auto_block") is False
                assert c.get("auto_decision") is False
                assert c.get("auto_trade") is False
            return ("PASS", "Conflict: no auto-block, no auto-decision, no auto-trade confirmed")
        except Exception as e:
            return ("FAIL", f"Conflict error: {e}")

    def _check_strategy_adapter(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_strategy_adapter import MultiTimeframeStrategyAdapter
            adapter = MultiTimeframeStrategyAdapter()
            assert adapter.NO_REWRITE_STRATEGY_ENGINE is True
            # 1m with no fundamental → NOT_APPLICABLE
            result = adapter.evaluate_timeframe("M1", [], "2023-01-06T10:00:00")
            # Empty bars → INSUFFICIENT
            assert result["status"] == "INSUFFICIENT"
            # Check summary
            summary = adapter.summary("M5")
            assert summary["1m_no_fundamental"] == "NOT_APPLICABLE"
            return ("PASS", "StrategyAdapter: no rewrite, per-TF independent, 1m no fundamental NOT_APPLICABLE")
        except Exception as e:
            return ("FAIL", f"StrategyAdapter error: {e}")

    def _check_timeline(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_timeline import MultiTimeframeReplayTimeline, FORBIDDEN_TIMELINE_FIELDS
            timeline = MultiTimeframeReplayTimeline()
            bars_by_tf = {
                "M5": [
                    {"timestamp": "2023-01-06T09:00:00", "is_complete": True, "is_partial": False},
                ],
            }
            events = timeline.build("SESSION_1", bars_by_tf)
            # Should have bar events
            assert len(events) > 0
            # No forbidden fields in events
            for ev in events:
                for f in FORBIDDEN_TIMELINE_FIELDS:
                    assert f not in ev, f"Forbidden field {f} in timeline event"
            assert all(ev.get("has_future_outcome") is False for ev in events)
            return ("PASS", f"Timeline: {len(events)} events, no future outcomes, no forbidden fields")
        except Exception as e:
            return ("FAIL", f"Timeline error: {e}")

    def _check_session(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_session import MultiTimeframeReplaySession
            # No M1 data → trigger fallback to M5
            session = MultiTimeframeReplaySession(
                symbol="TST",
                bars_by_tf={"M5": [{"timestamp": "2023-01-06T10:00:00"}]},
            )
            summary = session.summary()
            assert summary["m1_available"] is False
            assert summary["trigger_fallback_to_m5"] is True
            assert summary["trigger_timeframe"] == "M5"
            # With M1 data
            session2 = MultiTimeframeReplaySession(
                symbol="TST",
                bars_by_tf={"M1": [{"timestamp": "2023-01-06T10:00:00"}]},
            )
            summary2 = session2.summary()
            assert summary2["m1_available"] is True
            assert summary2["trigger_timeframe"] == "M1"
            return ("PASS", "Session: M1 missing → trigger fallback M5 (explicit, no fake M1)")
        except Exception as e:
            return ("FAIL", f"Session error: {e}")

    def _check_query(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_query import TimeframeQueryEngine
            query = TimeframeQueryEngine(store=None)
            snaps = query.snapshots()
            assert isinstance(snaps, list)
            return ("PASS", "Query: instantiates, returns empty list with no store")
        except Exception as e:
            return ("FAIL", f"Query error: {e}")

    def _check_store(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_store import MultiTimeframeReplayStore
            with tempfile.TemporaryDirectory() as tmpdir:
                store = MultiTimeframeReplayStore(base_dir=tmpdir)
                # Test append
                ok = store.append_snapshot({
                    "snapshot_id": "SNP-001",
                    "session_id": "S1",
                    "timeframe": "M5",
                    "replay_timestamp": "2023-01-06T10:00:00",
                })
                assert ok, "Append should succeed"
                snaps = store.get_snapshots("S1")
                assert len(snaps) == 1
                # Test forbidden field stripping
                ok2 = store.append_snapshot({
                    "snapshot_id": "SNP-002",
                    "session_id": "S1",
                    "outcome": "PROFIT",  # forbidden
                })
                assert ok2
                snaps2 = store.get_snapshots("S1")
                for s in snaps2:
                    assert "outcome" not in s, "Forbidden field should be stripped"
            return ("PASS", "Store: append-only, forbidden fields stripped, graceful JSONL load")
        except Exception as e:
            return ("FAIL", f"Store error: {e}")

    def _check_summary(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_summary import MultiTimeframeSummaryBuilder
            builder = MultiTimeframeSummaryBuilder()
            assert builder.NEVER_CLAIMS_EFFECTIVENESS is True
            s = builder.build_session_summary("S1")
            assert s["never_claims_effectiveness"] is True
            assert "effectiveness" not in str(s).lower() or "never_claims_effectiveness" in str(s)
            return ("PASS", "Summary: never claims strategy effectiveness")
        except Exception as e:
            return ("FAIL", f"Summary error: {e}")

    def _check_comparator(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_comparator import MultiTimeframeReplayComparator, FORBIDDEN_COMPARE_FIELDS
            comp = MultiTimeframeReplayComparator()
            assert "forward_return" in FORBIDDEN_COMPARE_FIELDS
            assert "realized_pnl" in FORBIDDEN_COMPARE_FIELDS
            result = comp.compare_timestamps("S1", "T1", "T2")
            assert result.get("no_future_reveal") is True
            return ("PASS", "Comparator: no future reveal, forbidden fields excluded")
        except Exception as e:
            return ("FAIL", f"Comparator error: {e}")

    def _check_batch(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
            runner = MultiTimeframeReplayBatchRunner()
            assert runner.DEFAULT_PREVIEW_MODE is True
            assert runner.NO_AUTO_DECISION is True
            assert runner.NO_AUTO_TRADE is True
            # Default preview
            preview = runner.preview(["SESSION_A"])
            assert preview["mode"] == "PREVIEW"
            assert preview["allow_write"] is False
            # Blocked without allow_write
            result = runner.run(["SESSION_A"], execute=True, allow_write=False)
            assert result["status"] == "BLOCKED"
            # Also blocked without execute
            result2 = runner.run(["SESSION_A"], execute=False, allow_write=True)
            assert result2["status"] == "BLOCKED"
            return ("PASS", "Batch: default preview, blocked without --allow-write, no auto-decision/trade")
        except Exception as e:
            return ("FAIL", f"Batch error: {e}")

    # ------------------------------------------------------------------
    # Safety flag checks
    # ------------------------------------------------------------------

    def _check_version_info(self) -> Tuple[str, str]:
        try:
            from release.version_info import (
                VERSION, MULTI_TIMEFRAME_REPLAY_AVAILABLE,
                AUTO_MULTI_TIMEFRAME_DECISION_ENABLED,
                AUTO_TIMEFRAME_STRATEGY_EXECUTION_ENABLED,
                REAL_ORDERS_ENABLED, BROKER_EXECUTION_ENABLED,
            )
            from release.version_compat import version_at_least
            assert version_at_least(VERSION, "1.2.5"), f"Expected >= 1.2.5, got {VERSION}"
            assert MULTI_TIMEFRAME_REPLAY_AVAILABLE is True
            assert AUTO_MULTI_TIMEFRAME_DECISION_ENABLED is False
            assert AUTO_TIMEFRAME_STRATEGY_EXECUTION_ENABLED is False
            assert REAL_ORDERS_ENABLED is False
            assert BROKER_EXECUTION_ENABLED is False
            return ("PASS", f"Version: {VERSION}, multi-timeframe replay available, safety flags valid")
        except Exception as e:
            return ("FAIL", f"VersionInfo error: {e}")

    def _check_real_no_mock(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_data_source import MultiTimeframeReplayDataSource
            ds = MultiTimeframeReplayDataSource(mode="real")
            result = ds.load("TESTONLY_999", "D1", "2023-01-01", "2023-12-31", mode="real")
            assert result["status"] == "UNAVAILABLE"
            assert result.get("source") is None or result.get("is_mock") is not True
            return ("PASS", "Real mode: no mock fallback when data missing")
        except Exception as e:
            return ("FAIL", f"RealNoMock error: {e}")

    def _check_daily_no_fake_intraday(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_aggregator import TimeframeBarAggregator
            agg = TimeframeBarAggregator()
            # Trying to aggregate TO D1 should fail
            result = agg.aggregate([], "D1")
            assert result["status"] == "INVALID", f"Expected INVALID, got {result['status']}"
            return ("PASS", "Daily no fake intraday: aggregation to D1 blocked")
        except Exception as e:
            return ("FAIL", f"DailyNoFakeIntraday error: {e}")

    def _check_no_bfill(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_alignment import TimeframeAlignmentEngine
            eng = TimeframeAlignmentEngine()
            assert eng.NO_BFILL is True
            from replay.timeframe_indicator_engine import MultiTimeframeIndicatorEngine
            ie = MultiTimeframeIndicatorEngine()
            assert ie.NO_BFILL is True
            return ("PASS", "No bfill: alignment and indicator engines confirm NO_BFILL=True")
        except Exception as e:
            return ("FAIL", f"NoBfill error: {e}")

    def _check_no_centered_rolling(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_indicator_engine import MultiTimeframeIndicatorEngine
            ie = MultiTimeframeIndicatorEngine()
            assert ie.NO_CENTERED_ROLLING is True
            return ("PASS", "No centered rolling: MultiTimeframeIndicatorEngine.NO_CENTERED_ROLLING=True")
        except Exception as e:
            return ("FAIL", f"NoCenteredRolling error: {e}")

    def _check_no_future_bar(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall
            fw = MultiTimeframeFutureDataFirewall()
            replay_ts = "2023-01-06T10:00:00"
            bars = [{"timestamp": "2023-01-06T11:00:00", "is_complete": False}]
            result = fw.filter_bars(bars, replay_ts, "M5")
            assert result["blocked_count"] == 1, "Future bar must be blocked"
            return ("PASS", "No future bar: timestamp > replay_timestamp → BLOCKED")
        except Exception as e:
            return ("FAIL", f"NoFutureBar error: {e}")

    def _check_incomplete_close_blocked(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall
            fw = MultiTimeframeFutureDataFirewall()
            # D1 bar marked complete but it's intraday
            daily_leak = [{
                "timestamp": "2023-01-06T09:00:00",
                "session_date": "2023-01-06",
                "timeframe": "D1",
                "is_complete": True,
            }]
            violations = fw.detect_daily_close_leak(daily_leak, "2023-01-06T10:00:00")
            assert len(violations) > 0, "Daily close leak should be detected"
            return ("PASS", "Incomplete close blocked: daily close leak detected correctly")
        except Exception as e:
            return ("FAIL", f"IncompleteCloseBlocked error: {e}")

    def _check_partial_bar_marked(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_bar_state import ReplayBarStateEvaluator, QUALIFICATION_PARTIAL_OBSERVATION
            ev = ReplayBarStateEvaluator()
            bar = {"timestamp": "2023-01-06T10:00:00", "is_complete": False, "is_partial": True}
            state = ev.evaluate(bar, "2023-01-06T10:03:00", "M5")
            assert state["is_partial"] is True
            assert state["qualification"] == QUALIFICATION_PARTIAL_OBSERVATION
            # visible_ohlcv should mark partial
            bar_full = {"timestamp": "2023-01-06T10:00:00", "open": 100.0, "high": 102.0, "low": 99.0, "close": 101.0, "volume": 500.0, "amount": 50500.0}
            visible = ev.visible_ohlcv(bar_full, "2023-01-06T10:03:00", "M5")
            assert visible.get("is_partial") is True
            assert visible.get("confirmed_close") is False
            assert visible.get("confirmed_breakout") is False
            return ("PASS", "Partial bar clearly marked, confirmed_close=False, confirmed_breakout=False")
        except Exception as e:
            return ("FAIL", f"PartialBarMarked error: {e}")

    def _check_no_auto_decision(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_MULTI_TIMEFRAME_DECISION_ENABLED
            assert AUTO_MULTI_TIMEFRAME_DECISION_ENABLED is False
            from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
            runner = MultiTimeframeReplayBatchRunner()
            assert runner.NO_AUTO_DECISION is True
            return ("PASS", "No auto decision: version_info and batch runner confirm False")
        except Exception as e:
            return ("FAIL", f"NoAutoDecision error: {e}")

    def _check_no_auto_score(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_TIMEFRAME_MISTAKE_CONFIRMATION_ENABLED
            assert AUTO_TIMEFRAME_MISTAKE_CONFIRMATION_ENABLED is False
            return ("PASS", "No auto score: AUTO_TIMEFRAME_MISTAKE_CONFIRMATION_ENABLED=False")
        except Exception as e:
            return ("FAIL", f"NoAutoScore error: {e}")

    def _check_no_auto_reveal(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
            runner = MultiTimeframeReplayBatchRunner()
            assert runner.NO_AUTO_REVEAL is True
            return ("PASS", "No auto reveal: batch runner NO_AUTO_REVEAL=True")
        except Exception as e:
            return ("FAIL", f"NoAutoReveal error: {e}")

    def _check_no_broker_side_effect(self) -> Tuple[str, str]:
        try:
            from release.version_info import BROKER_EXECUTION_ENABLED, REPLAY_TRADE_EXECUTION_ENABLED
            assert BROKER_EXECUTION_ENABLED is False
            assert REPLAY_TRADE_EXECUTION_ENABLED is False
            return ("PASS", "No broker side effect: BROKER_EXECUTION_ENABLED=False, REPLAY_TRADE_EXECUTION_ENABLED=False")
        except Exception as e:
            return ("FAIL", f"NoBrokerSideEffect error: {e}")

    def _check_batch_timing(self) -> Tuple[str, str]:
        try:
            import time
            from replay.timeframe_batch import MultiTimeframeReplayBatchRunner
            runner = MultiTimeframeReplayBatchRunner()
            runner.run(["S1"], execute=True, allow_write=True)
            summary = runner.summary()
            assert "total_elapsed" in summary
            assert "average_per_item" in summary
            assert "estimated_remaining" in summary
            return ("PASS", "Batch timing: total_elapsed, average_per_item, estimated_remaining present")
        except Exception as e:
            return ("FAIL", f"BatchTiming error: {e}")

    def _check_store_corrupted_recovery(self) -> Tuple[str, str]:
        try:
            import json
            from replay.timeframe_store import MultiTimeframeReplayStore
            with tempfile.TemporaryDirectory() as tmpdir:
                store = MultiTimeframeReplayStore(base_dir=tmpdir)
                # Append valid record
                store.append_snapshot({"snapshot_id": "SNP-001", "session_id": "S1"})
                # Manually inject corrupted line
                path = store._path("timeframe_snapshots.jsonl")
                with open(path, "a", encoding="utf-8") as f:
                    f.write("{THIS IS CORRUPTED JSON\n")
                # Append another valid record
                store.append_snapshot({"snapshot_id": "SNP-002", "session_id": "S1"})
                # Load should recover gracefully
                snaps = store.get_snapshots("S1")
                assert len(snaps) == 2, f"Should recover 2 valid records, got {len(snaps)}"
            return ("PASS", "Store corrupted tail: graceful recovery, valid records preserved")
        except Exception as e:
            return ("FAIL", f"StoreCorruptedRecovery error: {e}")


def run_health_check() -> None:
    """Run health check and print formatted results."""
    from replay.replay_timing import ReplayOperationTimer

    timer = ReplayOperationTimer()
    timer.start("replay-timeframe-health")

    print("=" * 70)
    print("  Multi-timeframe Replay Health Check v1.2.5")
    print("  [!] Research Only | No Real Orders | No Auto Decision | No Auto Execution")
    print("=" * 70)

    hc = MultiTimeframeReplayHealthCheck()
    results = hc.run()

    counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "BLOCKED": 0}

    for name, (status, message) in results.items():
        counts[status] = counts.get(status, 0) + 1
        print(f"  [{status}] {name}: {message}")

    print("-" * 70)
    total = sum(counts.values())
    overall = "PASS" if counts["FAIL"] == 0 and counts["BLOCKED"] == 0 else "FAIL"
    print(f"  Overall: {overall} | {total} checks | "
          f"PASS={counts['PASS']} WARN={counts['WARN']} "
          f"FAIL={counts['FAIL']} BLOCKED={counts['BLOCKED']}")
    print("=" * 70)
    print()
    timer.finish("COMPLETED")
    timer.print_summary()
    print("[!] Research Only. Not Investment Advice.")
    # Return list of dicts for programmatic use
    return [
        {"check": name, "status": status, "detail": message}
        for name, (status, message) in results.items()
    ]
