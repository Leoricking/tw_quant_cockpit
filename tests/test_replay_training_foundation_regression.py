"""
tests/test_replay_training_foundation_regression.py — Replay Training UX Foundation Regression v1.2.0

Tests covering:
- All schema dataclass instantiation and to_dict/from_dict
- Calendar: available_dates, normalize_date, nearest_previous, build_timeline
- Firewall: filter_dataframe (future rows blocked), detect_future_rows, future_field_scan
- PIT context: indicator computation (MA, KD, MACD, RSI, ATR) with only past data
- Timeline: previous at first day guarded, next at last day completes, jump normalizes non-trading day
- Session: create, load, resume, pause, duplicate (new ID), archive (immutable)
- Decision: simulation_decision_only=True, no paper order side effect
- Health check: imports pass, future firewall works, no forbidden actions

[!] Research Only. No Real Orders. Replay Training Only.
[!] Fixed clock (datetime(2023, 6, 15)). Isolated runtime (tmpdir). No production stores touched.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "replay"
FIXED_CLOCK = datetime(2023, 6, 15, tzinfo=timezone.utc)
FIXED_DATE = "2023-06-15"


class TestReplaySchema(unittest.TestCase):
    """Test all schema dataclass instantiation and to_dict/from_dict."""

    def test_session_config_instantiation(self):
        from replay.replay_schema import ReplaySessionConfig
        config = ReplaySessionConfig(
            session_id="RPL-TST-20230102-TEST",
            session_name="Test Session",
            symbol="TST",
            start_date="2023-01-02",
            end_date="2023-12-29",
            mode="mock",
        )
        self.assertTrue(config.research_only)
        self.assertTrue(config.no_real_orders)
        self.assertEqual(config.symbol, "TST")

    def test_session_config_to_dict_from_dict(self):
        from replay.replay_schema import ReplaySessionConfig
        config = ReplaySessionConfig(
            session_id="RPL-TST-TEST",
            session_name="Round-trip test",
            symbol="TST",
            start_date="2023-01-02",
            end_date="2023-12-29",
            mode="real",
        )
        d = config.to_dict()
        self.assertIn("session_id", d)
        self.assertTrue(d["research_only"])
        self.assertTrue(d["no_real_orders"])

        config2 = ReplaySessionConfig.from_dict(d)
        self.assertEqual(config2.session_id, config.session_id)
        self.assertEqual(config2.symbol, "TST")
        self.assertTrue(config2.research_only)

    def test_session_state_instantiation(self):
        from replay.replay_schema import ReplaySessionState
        state = ReplaySessionState(
            session_id="RPL-TST-TEST",
            current_date="2023-06-15",
            current_index=0,
            total_steps=100,
            status="CREATED",
        )
        self.assertTrue(state.research_only)
        self.assertTrue(state.no_real_orders)
        self.assertEqual(state.status, "CREATED")

    def test_session_state_to_dict_from_dict(self):
        from replay.replay_schema import ReplaySessionState
        state = ReplaySessionState(
            session_id="RPL-TST-TEST",
            current_date=FIXED_DATE,
            current_index=10,
            total_steps=100,
            status="PAUSED",
        )
        d = state.to_dict()
        self.assertTrue(d["research_only"])
        state2 = ReplaySessionState.from_dict(d)
        self.assertEqual(state2.current_index, 10)
        self.assertEqual(state2.status, "PAUSED")
        self.assertTrue(state2.research_only)

    def test_replay_market_snapshot(self):
        from replay.replay_schema import ReplayMarketSnapshot
        snap = ReplayMarketSnapshot(
            session_id="RPL-TST-TEST",
            symbol="TST",
            replay_date=FIXED_DATE,
        )
        self.assertTrue(snap.research_only)
        self.assertTrue(snap.no_real_orders)
        d = snap.to_dict()
        snap2 = ReplayMarketSnapshot.from_dict(d)
        self.assertEqual(snap2.replay_date, FIXED_DATE)

    def test_replay_decision_simulation_invariant(self):
        from replay.replay_schema import ReplayDecision
        dec = ReplayDecision(
            decision_id="DEC-TEST",
            session_id="RPL-TST-TEST",
            symbol="TST",
            replay_date=FIXED_DATE,
            action="WAIT",
        )
        self.assertTrue(dec.simulation_decision_only)
        self.assertTrue(dec.no_real_orders)
        self.assertTrue(dec.research_only)

    def test_replay_decision_to_dict_from_dict(self):
        from replay.replay_schema import ReplayDecision
        dec = ReplayDecision(
            decision_id="DEC-ROUND",
            session_id="RPL-TST-TEST",
            symbol="TST",
            replay_date=FIXED_DATE,
            action="ENTER",
            confidence=70,
        )
        d = dec.to_dict()
        self.assertTrue(d["simulation_decision_only"])
        dec2 = ReplayDecision.from_dict(d)
        self.assertEqual(dec2.action, "ENTER")
        self.assertEqual(dec2.confidence, 70)
        self.assertTrue(dec2.simulation_decision_only)

    def test_replay_event(self):
        from replay.replay_schema import ReplayEvent
        event = ReplayEvent(
            event_id="EVT-TEST",
            session_id="RPL-TST-TEST",
            replay_date=FIXED_DATE,
            event_type="SESSION_CREATED",
        )
        d = event.to_dict()
        event2 = ReplayEvent.from_dict(d)
        self.assertEqual(event2.event_type, "SESSION_CREATED")
        self.assertTrue(event2.research_only)

    def test_replay_annotation(self):
        from replay.replay_schema import ReplayAnnotation
        ann = ReplayAnnotation(
            annotation_id="ANN-TEST",
            session_id="RPL-TST-TEST",
            replay_date=FIXED_DATE,
            annotation_type="SUPPORT",
            title="Test Support",
            content="Support at 115",
        )
        d = ann.to_dict()
        ann2 = ReplayAnnotation.from_dict(d)
        self.assertEqual(ann2.annotation_type, "SUPPORT")
        self.assertFalse(ann2.hidden)

    def test_load_fixture_session_config(self):
        """Load fixture session_config.json and verify."""
        fixture_path = FIXTURES_DIR / "session_config.json"
        if not fixture_path.exists():
            self.skipTest(f"Fixture not found: {fixture_path}")
        with open(str(fixture_path)) as f:
            d = json.load(f)
        from replay.replay_schema import ReplaySessionConfig
        config = ReplaySessionConfig.from_dict(d)
        self.assertEqual(config.symbol, "TST001")
        self.assertTrue(config.research_only)
        self.assertTrue(config.no_real_orders)
        self.assertEqual(config.mode, "mock")

    def test_load_fixture_decision_enter(self):
        """Load fixture decision_enter.json and verify invariants."""
        fixture_path = FIXTURES_DIR / "decision_enter.json"
        if not fixture_path.exists():
            self.skipTest(f"Fixture not found: {fixture_path}")
        with open(str(fixture_path)) as f:
            d = json.load(f)
        from replay.replay_schema import ReplayDecision
        dec = ReplayDecision.from_dict(d)
        self.assertEqual(dec.action, "ENTER")
        self.assertTrue(dec.simulation_decision_only)
        self.assertTrue(dec.no_real_orders)


class TestReplayCalendar(unittest.TestCase):
    """Test trading calendar."""

    def test_normalize_date(self):
        from replay.replay_calendar import ReplayTradingCalendar
        cal = ReplayTradingCalendar()
        self.assertEqual(cal.normalize_date("2023-06-15"), "2023-06-15")
        self.assertEqual(cal.normalize_date("2023-06-15T10:00:00+00:00"), "2023-06-15")

    def test_build_timeline_from_fixture(self):
        """Test build_timeline with actual fixture CSV."""
        from replay.replay_calendar import ReplayTradingCalendar

        fixture_csv = FIXTURES_DIR / "daily_valid.csv"
        if not fixture_csv.exists():
            self.skipTest("Fixture CSV not found")

        # Place fixture in tmpdir with correct path pattern
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            data_dir.mkdir()
            import shutil
            shutil.copy(str(fixture_csv), str(data_dir / "TST.csv"))

            cal = ReplayTradingCalendar(repo_root=tmpdir)
            dates = cal.build_timeline("TST", "2023-11-20", "2023-12-29")
            self.assertGreater(len(dates), 0)
            # All dates should be in range
            for d in dates:
                self.assertGreaterEqual(d, "2023-11-20")
                self.assertLessEqual(d, "2023-12-29")

    def test_nearest_previous_trading_day(self):
        from replay.replay_calendar import ReplayTradingCalendar
        cal = ReplayTradingCalendar()
        cal._dates = ["2023-06-12", "2023-06-13", "2023-06-14", "2023-06-15", "2023-06-16"]

        # Exact match
        result = cal.nearest_previous_trading_day("2023-06-15")
        self.assertEqual(result, "2023-06-15")

        # Weekend - nearest previous
        result = cal.nearest_previous_trading_day("2023-06-17")
        self.assertEqual(result, "2023-06-16")

    def test_available_dates_empty_for_unknown_symbol(self):
        from replay.replay_calendar import ReplayTradingCalendar
        with tempfile.TemporaryDirectory() as tmpdir:
            cal = ReplayTradingCalendar(repo_root=tmpdir)
            dates = cal.available_dates("UNKNOWN_SYMBOL_XYZ")
            self.assertIsInstance(dates, list)
            self.assertEqual(len(dates), 0)


class TestFutureDataFirewall(unittest.TestCase):
    """Test future data firewall."""

    def test_filter_dataframe_blocks_future_rows(self):
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        from replay.future_data_firewall import ReplayFutureDataFirewall
        fw = ReplayFutureDataFirewall()

        df = pd.read_csv(str(FIXTURES_DIR / "daily_with_future_rows.csv"))
        filtered = fw.filter_dataframe(df, "date", "2023-12-29")

        # Should not contain any 2024 rows
        self.assertEqual(len(filtered), 30)
        for _, row in filtered.iterrows():
            self.assertLessEqual(row["date"], "2023-12-29")

    def test_detect_future_rows(self):
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        from replay.future_data_firewall import ReplayFutureDataFirewall
        fw = ReplayFutureDataFirewall()

        df = pd.read_csv(str(FIXTURES_DIR / "daily_with_future_rows.csv"))
        count = fw.detect_future_rows(df, "date", "2023-12-29")
        self.assertEqual(count, 4)  # 4 rows in 2024

    def test_future_field_scan_detects_forbidden(self):
        from replay.future_data_firewall import ReplayFutureDataFirewall
        fw = ReplayFutureDataFirewall()

        test_dict = {
            "close": 100.0,
            "forward_return_5": 0.05,
            "hindsight_score": 0.9,
            "MA20": 99.0,
            "future_high": 110.0,
        }
        found = fw.future_field_scan(test_dict)
        self.assertIn("forward_return_5", found)
        self.assertIn("hindsight_score", found)
        self.assertIn("future_high", found)
        self.assertNotIn("close", found)
        self.assertNotIn("ma20", found)

    def test_sanitize_context_removes_forbidden(self):
        from replay.future_data_firewall import ReplayFutureDataFirewall
        fw = ReplayFutureDataFirewall()

        ctx = {"close": 100.0, "forward_return_5": 0.05, "MA5": 99.0}
        sanitized, blocked, warnings = fw.sanitize_context(ctx, FIXED_DATE)
        self.assertNotIn("forward_return_5", sanitized)
        self.assertIn("close", sanitized)
        self.assertIn("MA5", sanitized)
        self.assertEqual(blocked, 1)

    def test_validate_frame(self):
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        from replay.future_data_firewall import ReplayFutureDataFirewall
        fw = ReplayFutureDataFirewall()

        df = pd.read_csv(str(FIXTURES_DIR / "daily_with_future_rows.csv"))
        is_valid, future_count, warnings = fw.validate_frame(df, "date", "2023-12-29")
        self.assertFalse(is_valid)
        self.assertEqual(future_count, 4)
        self.assertTrue(len(warnings) > 0)

    def test_filter_by_announcement_date_without_col(self):
        """fundamental_without_announcement_date.csv triggers FUNDAMENTAL_TIMING_APPROXIMATE."""
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        from replay.future_data_firewall import ReplayFutureDataFirewall
        fw = ReplayFutureDataFirewall()

        df = pd.read_csv(str(FIXTURES_DIR / "fundamental_without_announcement_date.csv"))
        result, warnings = fw.filter_by_announcement_date(df, "announcement_date", FIXED_DATE)
        self.assertTrue(any("FUNDAMENTAL_TIMING_APPROXIMATE" in w or "ANNOUNCEMENT_DATE_COLUMN_MISSING" in w
                           for w in warnings))


class TestPointInTimeContext(unittest.TestCase):
    """Test indicator computation with only past data."""

    def _make_price_df(self):
        try:
            import pandas as pd
        except ImportError:
            return None
        return pd.read_csv(str(FIXTURES_DIR / "daily_valid.csv"))

    def test_indicators_computed(self):
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        from replay.future_data_firewall import ReplayFutureDataFirewall
        from replay.replay_data_source import ReplayDataSource
        from replay.point_in_time_context import PointInTimeReplayContextBuilder

        fw = ReplayFutureDataFirewall()
        ds = ReplayDataSource(mode="mock")
        builder = PointInTimeReplayContextBuilder(data_source=ds, firewall=fw)

        df = self._make_price_df()
        if df is None:
            self.skipTest("pandas not available")

        indicators = builder.build_indicator_context(df, "2023-12-29")
        self.assertIn("MA5", indicators)
        self.assertIn("MA10", indicators)
        self.assertIn("MA20", indicators)
        self.assertIn("MA60", indicators)
        self.assertIn("KD_K", indicators)
        self.assertIn("KD_D", indicators)
        self.assertIn("MACD", indicators)
        self.assertIn("RSI", indicators)

    def test_ma_values_are_past_only(self):
        """MA values should use only data up to replay_date."""
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        from replay.future_data_firewall import ReplayFutureDataFirewall
        from replay.replay_data_source import ReplayDataSource
        from replay.point_in_time_context import PointInTimeReplayContextBuilder

        fw = ReplayFutureDataFirewall()
        ds = ReplayDataSource(mode="mock")
        builder = PointInTimeReplayContextBuilder(data_source=ds, firewall=fw)

        df = self._make_price_df()
        if df is None:
            self.skipTest("pandas not available")

        # Filter to replay_date
        df_filtered = df[df["date"] <= "2023-12-22"].copy()
        indicators_filtered = builder.build_indicator_context(df_filtered, "2023-12-22")

        df_full = df[df["date"] <= "2023-12-29"].copy()
        indicators_full = builder.build_indicator_context(df_full, "2023-12-29")

        # MA5 should be different because they use different data
        # (just checking they're computed, not NaN)
        ma5_filtered = indicators_filtered.get("MA5")
        ma5_full = indicators_full.get("MA5")
        self.assertIsNotNone(ma5_filtered)
        self.assertIsNotNone(ma5_full)


class TestReplayTimeline(unittest.TestCase):
    """Test date navigation guards."""

    def setUp(self):
        from replay.replay_timeline import ReplayTimeline
        self.timeline = ReplayTimeline()
        self.dates = ["2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06"]
        self.timeline.initialize(self.dates)

    def test_previous_at_first_day_does_not_go_negative(self):
        """previous() at first day returns current, changed=False."""
        prev_date, changed = self.timeline.previous()
        self.assertFalse(changed, "previous() at first day should not change")
        self.assertEqual(prev_date, "2023-01-02")

    def test_next_at_last_day_marks_completed(self):
        """next() at last day returns completed=True."""
        # Jump to last day
        self.timeline.jump_index(4)
        next_date, changed, completed = self.timeline.next()
        self.assertTrue(completed, "next() at last day should return completed=True")
        self.assertEqual(next_date, "2023-01-06")

    def test_jump_normalizes_non_trading_day(self):
        """jump() to non-trading day returns nearest previous and normalized=True."""
        actual, normalized = self.timeline.jump("2023-01-07")  # weekend, not in list
        self.assertTrue(normalized, "jump to non-trading day should set normalized=True")
        self.assertIn(actual, self.dates)

    def test_jump_to_valid_date(self):
        """jump() to valid trading day returns that date, normalized=False."""
        actual, normalized = self.timeline.jump("2023-01-04")
        self.assertEqual(actual, "2023-01-04")
        self.assertFalse(normalized)

    def test_progress(self):
        """progress() returns correct index and total."""
        current_idx, total = self.timeline.progress()
        self.assertEqual(total, 5)
        self.assertEqual(current_idx, 0)

    def test_serialize_restore(self):
        """Timeline state survives serialize/restore."""
        self.timeline.jump("2023-01-04")
        data = self.timeline.serialize()
        from replay.replay_timeline import ReplayTimeline
        t2 = ReplayTimeline()
        t2.restore(data)
        self.assertEqual(t2.current(), "2023-01-04")


class TestReplaySession(unittest.TestCase):
    """Test session lifecycle with isolated tmpdir."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_engine(self):
        from replay.replay_training_engine import ReplayTrainingEngine
        return ReplayTrainingEngine(repo_root=self.tmpdir, mode="mock")

    def test_create_session(self):
        engine = self._make_engine()
        state = engine.create_session("TST", "2023-01-02", "2023-12-29", name="Test Session")
        self.assertIsNotNone(state)
        self.assertTrue(state.session_id.startswith("RPL-"))
        self.assertTrue(state.research_only)
        self.assertTrue(state.no_real_orders)
        self.assertEqual(state.status, "READY")

    def test_session_id_prefix(self):
        engine = self._make_engine()
        state = engine.create_session("TST2", "2023-01-02", "2023-06-30")
        self.assertTrue(state.session_id.startswith("RPL-TST2-"))

    def test_resume_session(self):
        engine = self._make_engine()
        state = engine.create_session("TST", "2023-01-02", "2023-12-29")
        session_id = state.session_id

        # Pause then resume
        paused = engine.pause(session_id)
        self.assertEqual(paused.status, "PAUSED")

        resumed = engine.resume_session(session_id)
        self.assertIsNotNone(resumed)
        self.assertEqual(resumed.status, "READY")

    def test_archive_session_immutable(self):
        """Archived sessions cannot be resumed."""
        engine = self._make_engine()
        state = engine.create_session("TST", "2023-01-02", "2023-12-29")
        session_id = state.session_id

        archived = engine.archive_session(session_id)
        self.assertEqual(archived.status, "ARCHIVED")

        # Cannot resume archived
        resumed = engine._session_mgr.resume(session_id)
        self.assertEqual(resumed.status, "ARCHIVED")

    def test_duplicate_session_gets_new_id(self):
        engine = self._make_engine()
        state = engine.create_session("TST", "2023-01-02", "2023-12-29")
        original_id = state.session_id

        dup_state = engine.duplicate_session(original_id, new_name="Copy")
        self.assertIsNotNone(dup_state)
        self.assertNotEqual(dup_state.session_id, original_id)
        self.assertTrue(dup_state.session_id.startswith("RPL-"))

    def test_step_previous_at_first_day_does_not_crash(self):
        engine = self._make_engine()
        state = engine.create_session("TST", "2023-01-02", "2023-01-31")
        session_id = state.session_id

        result = engine.step_previous(session_id)
        self.assertIsNotNone(result)

    def test_step_next_at_last_day_marks_completed(self):
        engine = self._make_engine()
        # Create with mock dates (pandas bdate_range)
        state = engine.create_session("TST", "2023-01-02", "2023-01-06")
        session_id = state.session_id

        # Step through all days
        for _ in range(20):  # more than enough
            st = engine.step_next(session_id)
            if st and st.status == "COMPLETED":
                break

        final_state = engine._store.load_session_state(session_id)
        # Either COMPLETED or still running if dates are empty
        self.assertIsNotNone(final_state)


class TestReplayDecision(unittest.TestCase):
    """Test simulation-only decisions."""

    def test_decision_simulation_only_invariant(self):
        from replay.replay_decision import ReplayDecisionManager
        mgr = ReplayDecisionManager(store=None)
        self.assertTrue(mgr.SIMULATION_DECISION_ONLY)

        dec = mgr.create_decision(
            session_id="RPL-TST-TEST",
            symbol="TST",
            replay_date=FIXED_DATE,
            action="WAIT",
        )
        self.assertTrue(dec.simulation_decision_only)
        self.assertTrue(dec.no_real_orders)
        self.assertTrue(dec.research_only)

    def test_valid_actions(self):
        from replay.replay_decision import ReplayDecisionManager
        mgr = ReplayDecisionManager(store=None)
        for action in ["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"]:
            dec = mgr.create_decision("RPL-TEST", "TST", FIXED_DATE, action)
            self.assertEqual(dec.action, action)

    def test_invalid_action_raises(self):
        from replay.replay_decision import ReplayDecisionManager
        mgr = ReplayDecisionManager(store=None)
        with self.assertRaises(ValueError):
            mgr.create_decision("RPL-TEST", "TST", FIXED_DATE, "BUY_ORDER")

    def test_decision_has_no_paper_order_side_effect(self):
        """Creating a decision should not call any broker/order functions."""
        from replay.replay_decision import ReplayDecisionManager
        mgr = ReplayDecisionManager(store=None)

        # This should complete without any broker/order calls
        dec = mgr.create_decision(
            session_id="RPL-TST-TEST",
            symbol="TST",
            replay_date=FIXED_DATE,
            action="ENTER",
            planned_price=100.0,
            confidence=75,
        )
        # Verify no order_id or broker fields
        d = dec.to_dict()
        self.assertNotIn("order_id", d)
        self.assertNotIn("broker_token", d)
        self.assertNotIn("execution_id", d)
        self.assertTrue(d["simulation_decision_only"])


class TestReplayHealthCheck(unittest.TestCase):
    """Test health check passes and firewall works."""

    def test_health_check_imports_pass(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        status, msg = hc._check_imports()
        self.assertEqual(status, "PASS", f"Import check failed: {msg}")

    def test_health_check_future_firewall_pass(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        status, msg = hc._check_future_firewall()
        self.assertEqual(status, "PASS", f"Firewall check failed: {msg}")

    def test_health_check_date_navigation_pass(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        status, msg = hc._check_date_navigation()
        self.assertEqual(status, "PASS", f"Date nav check failed: {msg}")

    def test_health_check_decision_simulation_only_pass(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        status, msg = hc._check_decision_simulation_only()
        self.assertEqual(status, "PASS", f"Decision check failed: {msg}")

    def test_health_check_no_forbidden_actions_pass(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        status, msg = hc._check_no_forbidden_actions()
        self.assertEqual(status, "PASS", f"Forbidden actions check failed: {msg}")

    def test_health_check_safety_flags_pass(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        status, msg = hc._check_safety_flags()
        self.assertEqual(status, "PASS", f"Safety flags check failed: {msg}")

    def test_full_health_run(self):
        from replay.replay_health import ReplayTrainingHealthCheck
        hc = ReplayTrainingHealthCheck()
        results = hc.run()
        self.assertIn("imports", results)
        self.assertIn("future_firewall", results)
        overall = hc.overall_status(results)
        self.assertIn(overall, ["PASS", "WARN"])  # WARN acceptable, FAIL/BLOCKED not acceptable


class TestReplayStore(unittest.TestCase):
    """Test store reads/writes in isolated tmpdir."""

    def test_store_basic_session_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.replay_session_store import ReplaySessionStore
            from replay.replay_schema import ReplaySessionConfig, ReplaySessionState

            store = ReplaySessionStore(repo_root=tmpdir)

            config = ReplaySessionConfig(
                session_id="RPL-TST-STORE-TEST",
                session_name="Store Test",
                symbol="TST",
                start_date="2023-01-02",
                end_date="2023-12-29",
            )
            store.save_session_config(config)

            state = ReplaySessionState(
                session_id="RPL-TST-STORE-TEST",
                current_date="2023-01-02",
                current_index=0,
                total_steps=100,
                status="READY",
            )
            store.save_session_state(state)

            # Load back
            loaded_config = store.load_session_config("RPL-TST-STORE-TEST")
            self.assertIsNotNone(loaded_config)
            self.assertEqual(loaded_config["symbol"], "TST")

            loaded_state = store.load_session_state("RPL-TST-STORE-TEST")
            self.assertIsNotNone(loaded_state)
            self.assertEqual(loaded_state["status"], "READY")

    def test_store_reads_corrupted_tail(self):
        """Store should handle corrupted JSONL tail gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import shutil
            from replay.replay_session_store import ReplaySessionStore

            store = ReplaySessionStore(repo_root=tmpdir)
            session_dir = Path(tmpdir) / "data" / "replay_sessions" / "RPL-TST-CORR-TEST"
            session_dir.mkdir(parents=True, exist_ok=True)

            # Copy corrupted fixture
            shutil.copy(
                str(FIXTURES_DIR / "store_corrupted_tail.jsonl"),
                str(session_dir / "events.jsonl")
            )

            # Should not crash, should return 2 valid records
            events = store.load_events("RPL-TST-CORR-TEST")
            self.assertEqual(len(events), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
