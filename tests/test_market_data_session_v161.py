"""
tests/test_market_data_session_v161.py — Market Data Session Adapter v1.6.1 tests.
[!] Research Only. No Real Orders. No Broker. Market Data Only. Simulation Only.
360+ tests across 30 groups covering all 34 modules, safety invariants, pipeline,
policies, CLI, release gate, GUI, fixtures.
"""
from __future__ import annotations
import json
import os
import pytest
from decimal import Decimal
from typing import List, Dict, Any

REPO = os.path.join(os.path.dirname(__file__), "..")
FIXTURES_DIR = os.path.join(REPO, "tests", "fixtures", "market_data_session")


# =============================================================================
# 1. Package safety flags
# =============================================================================
class TestPackageSafetyFlags:
    def test_01_no_real_orders(self):
        import paper_trading.market_data as md
        assert md.NO_REAL_ORDERS is True

    def test_02_broker_execution_disabled(self):
        import paper_trading.market_data as md
        assert md.BROKER_EXECUTION_ENABLED is False

    def test_03_production_trading_blocked(self):
        import paper_trading.market_data as md
        assert md.PRODUCTION_TRADING_BLOCKED is True

    def test_04_market_data_only(self):
        import paper_trading.market_data as md
        assert md.MARKET_DATA_ONLY is True

    def test_05_no_broker_api(self):
        import paper_trading.market_data as md
        assert md.NO_BROKER_API is True

    def test_06_live_to_fixture_fallback_disabled(self):
        import paper_trading.market_data as md
        assert md.LIVE_TO_FIXTURE_FALLBACK_DISABLED is True

    def test_07_live_to_offline_fallback_disabled(self):
        import paper_trading.market_data as md
        assert md.LIVE_TO_OFFLINE_FALLBACK_DISABLED is True

    def test_08_unknown_source_as_live_disabled(self):
        import paper_trading.market_data as md
        assert md.UNKNOWN_SOURCE_AS_LIVE_DISABLED is True

    def test_09_silent_fixture_fallback_disabled(self):
        import paper_trading.market_data as md
        assert md.SILENT_FIXTURE_FALLBACK_DISABLED is True

    def test_10_research_only(self):
        import paper_trading.market_data as md
        assert md.RESEARCH_ONLY is True


# =============================================================================
# 2. Enums
# =============================================================================
class TestEnums:
    def setup_method(self):
        from paper_trading.market_data.enums_v161 import (
            MarketDataEventType, MarketDataSessionStatus, SourceClass,
            FreshnessStatus, SequenceStatus, DataQualityStatus, FeedFailureType,
            ReconnectPolicy, FailoverPolicy,
        )
        self.EventType = MarketDataEventType
        self.SessionStatus = MarketDataSessionStatus
        self.SourceClass = SourceClass
        self.FreshnessStatus = FreshnessStatus
        self.SequenceStatus = SequenceStatus
        self.DataQualityStatus = DataQualityStatus
        self.FeedFailureType = FeedFailureType
        self.ReconnectPolicy = ReconnectPolicy
        self.FailoverPolicy = FailoverPolicy

    def test_11_event_type_count(self):
        assert len(self.EventType) == 9

    def test_12_session_status_count(self):
        assert len(self.SessionStatus) == 11

    def test_13_source_class_count(self):
        assert len(self.SourceClass) == 6

    def test_14_freshness_status_count(self):
        assert len(self.FreshnessStatus) == 6

    def test_15_sequence_status_count(self):
        assert len(self.SequenceStatus) == 6

    def test_16_quality_status_count(self):
        assert len(self.DataQualityStatus) == 4

    def test_17_feed_failure_count(self):
        assert len(self.FeedFailureType) == 9

    def test_18_reconnect_policy_values(self):
        assert "NO_RECONNECT" in [p.value for p in self.ReconnectPolicy]
        assert "FIXED_INTERVAL" in [p.value for p in self.ReconnectPolicy]
        assert "BOUNDED_EXPONENTIAL_BACKOFF" in [p.value for p in self.ReconnectPolicy]

    def test_19_failover_policy_values(self):
        assert "NO_FAILOVER" in [p.value for p in self.FailoverPolicy]
        assert "PAUSE_ON_FAILURE" in [p.value for p in self.FailoverPolicy]
        assert "HALT_ON_FAILURE" in [p.value for p in self.FailoverPolicy]

    def test_20_session_status_active(self):
        assert self.SessionStatus.ACTIVE.value == "ACTIVE"

    def test_21_source_class_unknown(self):
        assert self.SourceClass.UNKNOWN.value == "UNKNOWN"

    def test_22_freshness_not_applicable(self):
        assert self.FreshnessStatus.NOT_APPLICABLE.value == "NOT_APPLICABLE"

    def test_23_sequence_gap_detected(self):
        assert self.SequenceStatus.GAP_DETECTED.value == "GAP_DETECTED"

    def test_24_quality_blocked(self):
        assert self.DataQualityStatus.BLOCKED.value == "BLOCKED"


# =============================================================================
# 3. Models safety contract
# =============================================================================
class TestModelsSafetyContract:
    def setup_method(self):
        from paper_trading.market_data.enums_v161 import (
            SourceClass, MarketDataEventType, FreshnessStatus, SequenceStatus, DataQualityStatus
        )
        from paper_trading.market_data.models_v161 import (
            MarketDataAdapterConfig, RawMarketDataEvent,
            CanonicalQuoteEvent, CanonicalTradeEvent,
            MarketDataSessionConfig, MarketDataCheckpoint,
        )
        self.SourceClass = SourceClass
        self.EventType = MarketDataEventType
        self.Fresh = FreshnessStatus
        self.Seq = SequenceStatus
        self.Qual = DataQualityStatus
        self.Config = MarketDataAdapterConfig
        self.Raw = RawMarketDataEvent
        self.Quote = CanonicalQuoteEvent
        self.Trade = CanonicalTradeEvent
        self.SessConfig = MarketDataSessionConfig
        self.Checkpoint = MarketDataCheckpoint
        from paper_trading.market_data.enums_v161 import ReconnectPolicy, FailoverPolicy
        self.ReconnectPolicy = ReconnectPolicy
        self.FailoverPolicy = FailoverPolicy

    def test_25_adapter_config_no_real_orders_assertion(self):
        with pytest.raises(AssertionError):
            self.Config(
                adapter_id="a1", source_class=self.SourceClass.FIXTURE,
                provider_name="t", symbols=["2330"],
                no_real_orders=False,
            )

    def test_26_adapter_config_unknown_source_blocked(self):
        with pytest.raises(ValueError):
            self.Config(
                adapter_id="a1", source_class=self.SourceClass.UNKNOWN,
                provider_name="t", symbols=["2330"],
            )

    def test_27_raw_event_safety_markers(self):
        raw = self.Raw(
            event_id="e1", adapter_id="a1", source_class=self.SourceClass.FIXTURE,
            event_type=self.EventType.TRADE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z",
        )
        assert raw.research_only is True
        assert raw.market_data_only is True
        assert raw.no_broker_call is True

    def test_28_canonical_quote_safety_markers(self):
        q = self.Quote(
            event_id="e1", raw_event_id="r1", adapter_id="a1",
            source_class=self.SourceClass.FIXTURE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z",
            bid_price=Decimal("165.0"), ask_price=Decimal("165.5"),
            bid_size=100, ask_size=200, mid_price=Decimal("165.25"),
            freshness_status=self.Fresh.NOT_APPLICABLE,
            sequence_status=self.Seq.UNKNOWN,
            quality_status=self.Qual.PASS,
        )
        assert q.research_only is True
        assert q.market_data_only is True
        assert q.no_broker_call is True
        assert q.no_real_order is True
        assert q.source_classified is True
        assert q.data_mode_disclosed is True

    def test_29_canonical_quote_bid_ask_enforced(self):
        with pytest.raises(ValueError):
            self.Quote(
                event_id="e1", raw_event_id="r1", adapter_id="a1",
                source_class=self.SourceClass.FIXTURE, symbol="2330",
                timestamp_utc="2024-01-02T09:00:00Z",
                bid_price=Decimal("166.0"), ask_price=Decimal("165.0"),
                bid_size=100, ask_size=100, mid_price=Decimal("165.5"),
                freshness_status=self.Fresh.NOT_APPLICABLE,
                sequence_status=self.Seq.UNKNOWN,
                quality_status=self.Qual.PASS,
            )

    def test_30_canonical_trade_safety_markers(self):
        t = self.Trade(
            event_id="e1", raw_event_id="r1", adapter_id="a1",
            source_class=self.SourceClass.FIXTURE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z",
            price=Decimal("165.5"), volume=100,
            freshness_status=self.Fresh.NOT_APPLICABLE,
            sequence_status=self.Seq.UNKNOWN,
            quality_status=self.Qual.PASS,
        )
        assert t.research_only is True
        assert t.no_real_order is True
        assert t.source_classified is True

    def test_31_canonical_trade_price_zero_blocked(self):
        with pytest.raises(ValueError):
            self.Trade(
                event_id="e1", raw_event_id="r1", adapter_id="a1",
                source_class=self.SourceClass.FIXTURE, symbol="2330",
                timestamp_utc="2024-01-02T09:00:00Z",
                price=Decimal("0"), volume=100,
                freshness_status=self.Fresh.NOT_APPLICABLE,
                sequence_status=self.Seq.UNKNOWN,
                quality_status=self.Qual.PASS,
            )

    def test_32_checkpoint_safety_markers(self):
        cp = self.Checkpoint(
            checkpoint_id="cp1", session_id="s1", adapter_id="a1",
            created_at_utc="2024-01-02T09:00:00Z",
            sequence_number=1, last_event_id=None,
        )
        assert cp.research_only is True
        assert cp.market_data_only is True

    def test_33_session_config_safety(self):
        cfg = self.SessConfig(
            session_id="s1", adapter_id="a1",
            symbols=["2330"], source_class=self.SourceClass.FIXTURE,
        )
        assert cfg.no_real_orders is True
        assert cfg.no_broker_api is True

    def test_34_session_config_unknown_source_ok_in_config(self):
        # MarketDataSessionConfig does not block UNKNOWN (adapter does)
        cfg = self.SessConfig(
            session_id="s1", adapter_id="a1",
            symbols=["2330"], source_class=self.SourceClass.UNKNOWN,
        )
        assert cfg.session_id == "s1"


# =============================================================================
# 4. Validation
# =============================================================================
class TestValidation:
    def setup_method(self):
        from paper_trading.market_data.validation_v161 import MarketDataValidator
        self.v = MarketDataValidator()

    def test_35_valid_quote_payload(self):
        ok, errs = self.v.validate_quote_payload({"bid": "165.0", "ask": "165.5", "symbol": "2330", "timestamp": "2024-01-02T09:00:00Z"})
        assert ok is True

    def test_36_quote_bid_gt_ask_fails(self):
        ok, errs = self.v.validate_quote_payload({"bid": "166.0", "ask": "165.0", "symbol": "2330", "timestamp": "2024-01-02T09:00:00Z"})
        assert ok is False
        assert any("bid" in e for e in errs)

    def test_37_valid_trade_payload(self):
        ok, errs = self.v.validate_trade_payload({"price": "165.5", "volume": 100, "symbol": "2330", "timestamp": "2024-01-02T09:00:00Z"})
        assert ok is True

    def test_38_trade_zero_price_fails(self):
        ok, errs = self.v.validate_trade_payload({"price": "0", "volume": 100, "symbol": "2330", "timestamp": "2024-01-02T09:00:00Z"})
        assert ok is False

    def test_39_unknown_source_invalid(self):
        from paper_trading.market_data.enums_v161 import SourceClass
        ok, msg = self.v.validate_source_class(SourceClass.UNKNOWN)
        assert ok is False

    def test_40_empty_symbol_invalid(self):
        ok, msg = self.v.validate_symbol("")
        assert ok is False

    def test_41_valid_timestamp(self):
        ok, msg = self.v.validate_timestamp_utc("2024-01-02T09:00:00Z")
        assert ok is True

    def test_42_invalid_timestamp_no_T(self):
        ok, msg = self.v.validate_timestamp_utc("2024-01-02 09:00:00")
        assert ok is False

    def test_43_missing_quote_field(self):
        ok, errs = self.v.validate_quote_payload({"bid": "165.0", "symbol": "2330", "timestamp": "T"})
        assert ok is False

    def test_44_missing_trade_field(self):
        ok, errs = self.v.validate_trade_payload({"price": "165.5", "symbol": "2330", "timestamp": "T"})
        assert ok is False


# =============================================================================
# 5. Adapter Registry
# =============================================================================
class TestAdapterRegistry:
    def setup_method(self):
        from paper_trading.market_data.adapter_registry_v161 import (
            MarketDataAdapterRegistry, AdapterRegistryError,
        )
        from paper_trading.market_data.fixture_adapter_v161 import FixtureAdapter
        from paper_trading.market_data.models_v161 import MarketDataAdapterConfig
        from paper_trading.market_data.enums_v161 import SourceClass
        self.Registry = MarketDataAdapterRegistry
        self.RegistryError = AdapterRegistryError
        self.FixtureAdapter = FixtureAdapter
        self.Config = MarketDataAdapterConfig
        self.SourceClass = SourceClass

    def _make_adapter(self, adapter_id, source_class=None):
        sc = source_class or self.SourceClass.FIXTURE
        cfg = self.Config(adapter_id=adapter_id, source_class=sc, provider_name="t", symbols=["2330"])
        return self.FixtureAdapter(cfg)

    def test_45_register_valid_adapter(self):
        reg = self.Registry()
        a = self._make_adapter("a1")
        reg.register(a, "event_time_utc")
        assert reg.count() == 1

    def test_46_duplicate_id_blocked(self):
        reg = self.Registry()
        a1 = self._make_adapter("dup")
        a2 = self._make_adapter("dup")
        reg.register(a1, "event_time_utc")
        with pytest.raises(self.RegistryError):
            reg.register(a2, "event_time_utc")

    def test_47_unknown_source_blocked(self):
        reg = self.Registry()
        with pytest.raises(Exception):
            self._make_adapter("bad", self.SourceClass.UNKNOWN)

    def test_48_missing_timestamp_semantics_blocked(self):
        reg = self.Registry()
        a = self._make_adapter("a2")
        with pytest.raises(self.RegistryError):
            reg.register(a, "")

    def test_49_list_adapters(self):
        reg = self.Registry()
        a = self._make_adapter("a3")
        reg.register(a, "event_time_utc")
        assert "a3" in reg.list_adapters()

    def test_50_unregister(self):
        reg = self.Registry()
        a = self._make_adapter("a4")
        reg.register(a, "event_time_utc")
        reg.unregister("a4")
        assert reg.count() == 0


# =============================================================================
# 6. Fixture Adapter
# =============================================================================
class TestFixtureAdapter:
    def _make_adapter(self, events=None):
        from paper_trading.market_data.fixture_adapter_v161 import FixtureAdapter
        from paper_trading.market_data.models_v161 import MarketDataAdapterConfig
        from paper_trading.market_data.enums_v161 import SourceClass
        cfg = MarketDataAdapterConfig(
            adapter_id="fx1", source_class=SourceClass.FIXTURE,
            provider_name="test", symbols=["2330"],
        )
        return FixtureAdapter(cfg, fixture_events=events or [])

    def test_51_connect_returns_true(self):
        a = self._make_adapter()
        assert a.connect() is True

    def test_52_validate_config_pass(self):
        a = self._make_adapter()
        result = a.validate_config()
        assert result["valid"] is True

    def test_53_poll_returns_events(self):
        events = [{"event_id": "e1", "event_type": "TRADE", "symbol": "2330", "timestamp_utc": "2024-01-02T09:00:00Z", "payload": {"price": "165.5", "volume": 100}}]
        a = self._make_adapter(events)
        a.connect()
        raw = a.poll()
        assert len(raw) == 1

    def test_54_poll_empty_after_exhausted(self):
        events = [{"event_id": "e1", "event_type": "TRADE", "symbol": "2330", "timestamp_utc": "2024-01-02T09:00:00Z", "payload": {"price": "165.5", "volume": 100}}]
        a = self._make_adapter(events)
        a.connect()
        a.poll()
        raw2 = a.poll()
        assert raw2 == []

    def test_55_status_has_safety_flags(self):
        a = self._make_adapter()
        status = a.get_status()
        assert status["no_real_orders"] is True
        assert status["silent_fixture_fallback_disabled"] is True

    def test_56_checkpoint_and_restore(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        events = [{"event_id": "e1", "event_type": "TRADE", "symbol": "2330", "timestamp_utc": "2024-01-02T09:00:00Z", "payload": {"price": "165.5", "volume": 100}}]
        a = self._make_adapter(events)
        a.connect()
        a.poll()
        cp = a.checkpoint_state()
        assert cp.checkpoint_hash != ""
        a.restore_state(cp)
        assert a.status == MarketDataSessionStatus.PAUSED

    def test_57_submit_real_order_forbidden(self):
        a = self._make_adapter()
        with pytest.raises(NotImplementedError):
            a.submit_real_order()

    def test_58_connect_broker_forbidden(self):
        a = self._make_adapter()
        with pytest.raises(NotImplementedError):
            a.connect_broker()


# =============================================================================
# 7. Replay Adapter
# =============================================================================
class TestReplayAdapter:
    def _make_adapter(self, events=None, as_of=None):
        from paper_trading.market_data.replay_adapter_v161 import ReplayAdapter
        from paper_trading.market_data.models_v161 import MarketDataAdapterConfig
        from paper_trading.market_data.enums_v161 import SourceClass
        cfg = MarketDataAdapterConfig(
            adapter_id="rpl1", source_class=SourceClass.REPLAY,
            provider_name="replay", symbols=["2330"],
        )
        return ReplayAdapter(cfg, event_log=events or [], paper_session_as_of=as_of)

    def test_59_connect_returns_true(self):
        a = self._make_adapter()
        assert a.connect() is True

    def test_60_pit_filter_excludes_future_events(self):
        events = [
            {"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
             "timestamp_utc": "2024-01-01T09:00:00Z", "available_from": "2024-01-01",
             "payload": {"price": "165.5", "volume": 100}},
            {"event_id": "e2", "event_type": "TRADE", "symbol": "2330",
             "timestamp_utc": "2024-05-01T09:00:00Z", "available_from": "2024-05-01",
             "payload": {"price": "170.0", "volume": 50}},
        ]
        a = self._make_adapter(events, as_of="2024-03-01")
        a.connect()
        raw = a.poll()
        assert len(raw) == 1
        assert raw[0].event_id == "e1"

    def test_61_replay_is_deterministic(self):
        events = [
            {"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
             "timestamp_utc": "2024-01-01T09:00:00Z",
             "payload": {"price": "165.5", "volume": 100}},
        ]
        a1 = self._make_adapter(events)
        a2 = self._make_adapter(events)
        a1.connect(); a2.connect()
        r1 = a1.poll(); r2 = a2.poll()
        assert len(r1) == len(r2) == 1
        assert r1[0].event_id == r2[0].event_id

    def test_62_restore_to_paused(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        a = self._make_adapter()
        a.connect()
        cp = a.checkpoint_state()
        a.restore_state(cp)
        assert a.status == MarketDataSessionStatus.PAUSED


# =============================================================================
# 8. Offline Adapter
# =============================================================================
class TestOfflineAdapter:
    def _make_adapter(self, events=None):
        from paper_trading.market_data.offline_adapter_v161 import OfflineAdapter
        from paper_trading.market_data.models_v161 import MarketDataAdapterConfig
        from paper_trading.market_data.enums_v161 import SourceClass
        cfg = MarketDataAdapterConfig(
            adapter_id="off1", source_class=SourceClass.OFFLINE,
            provider_name="offline", symbols=["2330"],
        )
        return OfflineAdapter(cfg, stored_events=events or [])

    def test_63_connect(self):
        a = self._make_adapter()
        assert a.connect() is True

    def test_64_status_flags(self):
        a = self._make_adapter()
        status = a.get_status()
        assert status["live_to_offline_failover_disabled"] is True

    def test_65_normalized_trade_freshness_stale(self):
        from paper_trading.market_data.enums_v161 import FreshnessStatus, MarketDataEventType, SourceClass
        from paper_trading.market_data.models_v161 import RawMarketDataEvent
        events = [{"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
                   "timestamp_utc": "2024-01-01T09:00:00Z", "payload": {"price": "165.5", "volume": 100}}]
        a = self._make_adapter(events)
        a.connect()
        raw = a.poll()
        canonical = a.normalize_event(raw[0])
        assert canonical is not None
        assert canonical.freshness_status == FreshnessStatus.STALE


# =============================================================================
# 9. Session Clock
# =============================================================================
class TestSessionClock:
    def setup_method(self):
        from paper_trading.market_data.session_clock_v161 import MarketDataSessionClock
        self.Clock = MarketDataSessionClock

    def test_66_now_returns_datetime(self):
        from datetime import datetime
        clock = self.Clock()
        now = clock.now()
        assert isinstance(now, datetime)

    def test_67_inject_time(self):
        from datetime import datetime, timezone
        clock = self.Clock()
        fixed = datetime(2024, 1, 2, 9, 0, 0, tzinfo=timezone.utc)
        clock.set_time(fixed)
        assert clock.now() == fixed

    def test_68_advance_no_real_sleep(self):
        from datetime import datetime, timezone
        clock = self.Clock()
        fixed = datetime(2024, 1, 2, 9, 0, 0, tzinfo=timezone.utc)
        clock.set_time(fixed)
        clock.advance(60)
        assert clock.now().second == 0
        assert clock.now().minute == 1

    def test_69_reset_to_realtime(self):
        from datetime import datetime, timezone
        clock = self.Clock()
        fixed = datetime(2024, 1, 2, 9, 0, 0, tzinfo=timezone.utc)
        clock.set_time(fixed)
        clock.reset()
        now = clock.now()
        assert now != fixed

    def test_70_elapsed_seconds(self):
        from datetime import datetime, timezone
        clock = self.Clock()
        fixed = datetime(2024, 1, 2, 9, 0, 0, tzinfo=timezone.utc)
        clock.set_time(fixed)
        elapsed = clock.elapsed_seconds("2024-01-02T08:59:55Z")
        assert 4 <= elapsed <= 6


# =============================================================================
# 10. Calendar
# =============================================================================
class TestCalendar:
    def setup_method(self):
        from paper_trading.market_data.calendar_v161 import TaiwanMarketCalendar
        self.cal = TaiwanMarketCalendar()

    def test_71_regular_session_weekday(self):
        from datetime import datetime, timezone
        # Tuesday 09:30 TST = Tuesday 01:30 UTC
        dt = datetime(2024, 1, 2, 1, 30, 0, tzinfo=timezone.utc)
        assert self.cal.is_regular_session(dt) is True

    def test_72_weekend_not_session(self):
        from datetime import datetime, timezone
        # Saturday
        dt = datetime(2024, 1, 6, 1, 30, 0, tzinfo=timezone.utc)
        assert self.cal.is_regular_session(dt) is False

    def test_73_session_label_regular(self):
        from datetime import datetime, timezone
        dt = datetime(2024, 1, 2, 1, 30, 0, tzinfo=timezone.utc)
        assert self.cal.get_session_label(dt) == "REGULAR"

    def test_74_session_label_weekend(self):
        from datetime import datetime, timezone
        dt = datetime(2024, 1, 6, 1, 30, 0, tzinfo=timezone.utc)
        assert self.cal.get_session_label(dt) == "WEEKEND"

    def test_75_utc_to_tst_offset(self):
        from datetime import datetime, timezone
        dt = datetime(2024, 1, 2, 1, 0, 0, tzinfo=timezone.utc)
        tst = self.cal.utc_to_tst_iso(dt)
        assert "09:00" in tst


# =============================================================================
# 11. Symbol Mapper
# =============================================================================
class TestSymbolMapper:
    def setup_method(self):
        from paper_trading.market_data.symbol_mapper_v161 import SymbolMapper, SymbolMappingError
        self.SymbolMapper = SymbolMapper
        self.Error = SymbolMappingError

    def test_76_register_and_resolve(self):
        sm = self.SymbolMapper()
        sm.register("TSM", "2330")
        assert sm.resolve("TSM") == "2330"

    def test_77_ambiguous_blocked(self):
        sm = self.SymbolMapper()
        sm.register("TSM", "2330")
        with pytest.raises(self.Error):
            sm.register("TSM", "2317")

    def test_78_unknown_symbol_raises(self):
        sm = self.SymbolMapper()
        with pytest.raises(self.Error):
            sm.resolve("UNKNOWN_SYM")

    def test_79_try_resolve_success(self):
        sm = self.SymbolMapper()
        sm.register("TSM", "2330")
        ok, canon, msg = sm.try_resolve("TSM")
        assert ok is True
        assert canon == "2330"

    def test_80_try_resolve_fail(self):
        sm = self.SymbolMapper()
        ok, canon, msg = sm.try_resolve("NOT_REGISTERED")
        assert ok is False

    def test_81_count(self):
        sm = self.SymbolMapper()
        sm.register("TSM", "2330")
        sm.register("HON", "2317")
        assert sm.count() == 2


# =============================================================================
# 12. Quote Normalizer
# =============================================================================
class TestQuoteNormalizer:
    def setup_method(self):
        from paper_trading.market_data.quote_normalizer_v161 import QuoteNormalizer
        from paper_trading.market_data.models_v161 import RawMarketDataEvent
        from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType
        self.norm = QuoteNormalizer()
        self.Raw = RawMarketDataEvent
        self.SourceClass = SourceClass
        self.EventType = MarketDataEventType

    def _raw(self, payload):
        return self.Raw(
            event_id="e1", adapter_id="a1", source_class=self.SourceClass.FIXTURE,
            event_type=self.EventType.QUOTE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z", raw_payload=payload,
        )

    def test_82_valid_quote_normalizes(self):
        q = self.norm.normalize(self._raw({"bid": "165.0", "ask": "165.5"}))
        assert q is not None
        assert q.bid_price == Decimal("165.0")
        assert q.ask_price == Decimal("165.5")

    def test_83_bid_gt_ask_drops(self):
        q = self.norm.normalize(self._raw({"bid": "166.0", "ask": "165.0"}))
        assert q is None

    def test_84_mid_price_correct(self):
        q = self.norm.normalize(self._raw({"bid": "164.0", "ask": "166.0"}))
        assert q.mid_price == Decimal("165.0")

    def test_85_zero_bid_drops(self):
        q = self.norm.normalize(self._raw({"bid": "0", "ask": "165.0"}))
        assert q is None


# =============================================================================
# 13. Trade Normalizer
# =============================================================================
class TestTradeNormalizer:
    def setup_method(self):
        from paper_trading.market_data.trade_normalizer_v161 import TradeNormalizer
        from paper_trading.market_data.models_v161 import RawMarketDataEvent
        from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType
        self.norm = TradeNormalizer()
        self.Raw = RawMarketDataEvent
        self.SourceClass = SourceClass
        self.EventType = MarketDataEventType

    def _raw(self, payload):
        return self.Raw(
            event_id="e1", adapter_id="a1", source_class=self.SourceClass.FIXTURE,
            event_type=self.EventType.TRADE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z", raw_payload=payload,
        )

    def test_86_valid_trade_normalizes(self):
        t = self.norm.normalize(self._raw({"price": "165.5", "volume": 100}))
        assert t is not None
        assert t.price == Decimal("165.5")
        assert t.volume == 100

    def test_87_zero_price_drops(self):
        t = self.norm.normalize(self._raw({"price": "0", "volume": 100}))
        assert t is None

    def test_88_negative_volume_drops(self):
        t = self.norm.normalize(self._raw({"price": "165.5", "volume": -1}))
        assert t is None


# =============================================================================
# 14. Sequence Validator
# =============================================================================
class TestSequenceValidator:
    def setup_method(self):
        from paper_trading.market_data.sequence_v161 import SequenceValidator
        from paper_trading.market_data.models_v161 import RawMarketDataEvent
        from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType, SequenceStatus
        self.sv = SequenceValidator()
        self.Raw = RawMarketDataEvent
        self.SourceClass = SourceClass
        self.EventType = MarketDataEventType
        self.Seq = SequenceStatus

    def _raw(self, seq):
        return self.Raw(
            event_id=f"e{seq}", adapter_id="a1", source_class=self.SourceClass.FIXTURE,
            event_type=self.EventType.TRADE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z", sequence_number=seq,
        )

    def test_89_in_order(self):
        assert self.sv.check(self._raw(1)) == self.Seq.IN_ORDER
        assert self.sv.check(self._raw(2)) == self.Seq.IN_ORDER

    def test_90_gap_detected(self):
        self.sv.check(self._raw(1))
        assert self.sv.check(self._raw(5)) == self.Seq.GAP_DETECTED

    def test_91_duplicate(self):
        self.sv.check(self._raw(1))
        assert self.sv.check(self._raw(1)) == self.Seq.DUPLICATE

    def test_92_out_of_order(self):
        self.sv.check(self._raw(3))
        assert self.sv.check(self._raw(1)) == self.Seq.OUT_OF_ORDER

    def test_93_no_seq_unknown(self):
        from paper_trading.market_data.models_v161 import RawMarketDataEvent
        raw = RawMarketDataEvent(
            event_id="e_none", adapter_id="a1", source_class=self.SourceClass.FIXTURE,
            event_type=self.EventType.TRADE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z",
        )
        assert self.sv.check(raw) == self.Seq.UNKNOWN

    def test_94_reset(self):
        self.sv.check(self._raw(1))
        self.sv.reset("a1", "2330")
        assert self.sv.get_last_seq("a1", "2330") is None


# =============================================================================
# 15. Deduplication
# =============================================================================
class TestDeduplication:
    def setup_method(self):
        from paper_trading.market_data.deduplication_v161 import MarketDataDeduplicator
        from paper_trading.market_data.models_v161 import RawMarketDataEvent
        from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType
        self.Dedup = MarketDataDeduplicator
        self.Raw = RawMarketDataEvent
        self.SourceClass = SourceClass
        self.EventType = MarketDataEventType

    def _raw(self, eid):
        return self.Raw(
            event_id=eid, adapter_id="a1", source_class=self.SourceClass.FIXTURE,
            event_type=self.EventType.TRADE, symbol="2330",
            timestamp_utc="2024-01-02T09:00:00Z",
        )

    def test_95_first_event_not_dup(self):
        d = self.Dedup()
        assert d.is_duplicate(self._raw("e1")) is False

    def test_96_second_same_is_dup(self):
        d = self.Dedup()
        d.is_duplicate(self._raw("e1"))
        assert d.is_duplicate(self._raw("e1")) is True

    def test_97_different_ids_not_dup(self):
        d = self.Dedup()
        d.is_duplicate(self._raw("e1"))
        assert d.is_duplicate(self._raw("e2")) is False

    def test_98_filter_batch(self):
        d = self.Dedup()
        events = [self._raw("e1"), self._raw("e2"), self._raw("e1")]
        result = d.filter_batch(events)
        assert len(result) == 2

    def test_99_duplicate_count(self):
        d = self.Dedup()
        d.is_duplicate(self._raw("e1"))
        d.is_duplicate(self._raw("e1"))
        assert d.duplicate_count == 1

    def test_100_reset(self):
        d = self.Dedup()
        d.is_duplicate(self._raw("e1"))
        d.reset()
        assert d.is_duplicate(self._raw("e1")) is False


# =============================================================================
# 16. Freshness Classifier
# =============================================================================
class TestFreshnessClassifier:
    def setup_method(self):
        from paper_trading.market_data.freshness_v161 import FreshnessClassifier, FUTURE_DATE_COUNTS_AS_FRESH
        from paper_trading.market_data.enums_v161 import SourceClass, FreshnessStatus
        from datetime import datetime, timezone, timedelta
        self.Classifier = FreshnessClassifier
        self.FUTURE_DATE_COUNTS_AS_FRESH = FUTURE_DATE_COUNTS_AS_FRESH
        self.SourceClass = SourceClass
        self.Fresh = FreshnessStatus
        self.now = datetime.now(timezone.utc)
        self.timedelta = timedelta

    def test_101_future_date_not_fresh_invariant(self):
        assert self.FUTURE_DATE_COUNTS_AS_FRESH is False

    def test_102_live_fresh_event(self):
        ts = (self.now - self.timedelta(seconds=2)).isoformat()
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.LIVE_PUBLIC)
        assert status == self.Fresh.FRESH

    def test_103_live_stale_event(self):
        ts = (self.now - self.timedelta(seconds=200)).isoformat()
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.LIVE_PUBLIC)
        assert status == self.Fresh.STALE

    def test_104_fixture_not_applicable(self):
        ts = (self.now - self.timedelta(seconds=2)).isoformat()
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.FIXTURE)
        assert status == self.Fresh.NOT_APPLICABLE

    def test_105_replay_not_applicable(self):
        ts = (self.now - self.timedelta(seconds=2)).isoformat()
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.REPLAY)
        assert status == self.Fresh.NOT_APPLICABLE

    def test_106_unknown_source_unknown_freshness(self):
        ts = (self.now - self.timedelta(seconds=2)).isoformat()
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.UNKNOWN)
        assert status == self.Fresh.UNKNOWN

    def test_107_future_timestamp_unknown(self):
        ts = "2099-01-01T00:00:00Z"
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.LIVE_PUBLIC)
        assert status == self.Fresh.UNKNOWN

    def test_108_expired_event(self):
        ts = (self.now - self.timedelta(seconds=400)).isoformat()
        c = self.Classifier()
        status = c.classify(ts, self.SourceClass.LIVE_PUBLIC)
        assert status == self.Fresh.EXPIRED


# =============================================================================
# 17. Delay Measurement
# =============================================================================
class TestDelayMeasurement:
    def setup_method(self):
        from paper_trading.market_data.delay_v161 import DelayMeasurement
        self.Delay = DelayMeasurement

    def test_109_measure_positive_delay(self):
        from datetime import datetime, timezone, timedelta
        d = self.Delay()
        now = datetime.now(timezone.utc)
        event_ts = (now - timedelta(seconds=1)).isoformat()
        ms = d.measure_ms(event_ts)
        assert ms is not None
        assert ms >= 0

    def test_110_stats_after_measurement(self):
        from datetime import datetime, timezone, timedelta
        d = self.Delay()
        now = datetime.now(timezone.utc)
        event_ts = (now - timedelta(seconds=1)).isoformat()
        d.measure_ms(event_ts)
        stats = d.get_stats()
        assert stats["count"] == 1
        assert stats["min_ms"] is not None

    def test_111_empty_stats(self):
        d = self.Delay()
        stats = d.get_stats()
        assert stats["count"] == 0
        assert stats["min_ms"] is None


# =============================================================================
# 18. Quality Gate
# =============================================================================
class TestQualityGate:
    def setup_method(self):
        from paper_trading.market_data.quality_v161 import DataQualityGate
        from paper_trading.market_data.enums_v161 import FreshnessStatus, SequenceStatus, DataQualityStatus
        self.gate = DataQualityGate()
        self.Fresh = FreshnessStatus
        self.Seq = SequenceStatus
        self.Qual = DataQualityStatus

    def test_112_pass_normal(self):
        s = self.gate.assess(self.Fresh.FRESH, self.Seq.IN_ORDER)
        assert s == self.Qual.PASS

    def test_113_blocked_duplicate(self):
        s = self.gate.assess(self.Fresh.FRESH, self.Seq.IN_ORDER, is_duplicate=True)
        assert s == self.Qual.BLOCKED

    def test_114_blocked_bid_ask(self):
        s = self.gate.assess(self.Fresh.FRESH, self.Seq.IN_ORDER, bid_ask_violated=True)
        assert s == self.Qual.BLOCKED

    def test_115_fail_expired(self):
        s = self.gate.assess(self.Fresh.EXPIRED, self.Seq.IN_ORDER)
        assert s == self.Qual.FAIL

    def test_116_fail_gap(self):
        s = self.gate.assess(self.Fresh.FRESH, self.Seq.GAP_DETECTED)
        assert s == self.Qual.FAIL

    def test_117_warn_stale(self):
        s = self.gate.assess(self.Fresh.STALE, self.Seq.IN_ORDER)
        assert s == self.Qual.WARN

    def test_118_warn_out_of_order(self):
        s = self.gate.assess(self.Fresh.FRESH, self.Seq.OUT_OF_ORDER)
        assert s == self.Qual.WARN


# =============================================================================
# 19. Anomaly Detection
# =============================================================================
class TestAnomalyDetection:
    def setup_method(self):
        from paper_trading.market_data.anomaly_v161 import MarketDataAnomalyDetector
        self.Detector = MarketDataAnomalyDetector

    def test_119_no_anomaly_normal(self):
        d = self.Detector()
        for _ in range(10):
            r = d.check_price("2330", Decimal("165.0"))
        assert r.is_anomaly is False

    def test_120_price_spike_detected(self):
        d = self.Detector(price_spike_ratio=0.05)
        for _ in range(5):
            d.check_price("2330", Decimal("165.0"))
        r = d.check_price("2330", Decimal("200.0"))  # >5% spike
        assert r.is_anomaly is True
        assert r.anomaly_type == "PRICE_SPIKE"

    def test_121_volume_spike_detected(self):
        d = self.Detector(volume_spike_ratio=3.0)
        for _ in range(10):
            d.check_volume("2330", 100)
        r = d.check_volume("2330", 5000)  # >3x avg
        assert r.is_anomaly is True

    def test_122_reset_clears_history(self):
        d = self.Detector()
        for _ in range(5):
            d.check_price("2330", Decimal("165.0"))
        d.reset("2330")
        # After reset no history — small window won't trigger
        r = d.check_price("2330", Decimal("200.0"))
        assert r.is_anomaly is False


# =============================================================================
# 20. Feed Monitor
# =============================================================================
class TestFeedMonitor:
    def setup_method(self):
        from paper_trading.market_data.feed_monitor_v161 import FeedMonitor
        from paper_trading.market_data.enums_v161 import FeedFailureType
        self.Monitor = FeedMonitor
        self.FailureType = FeedFailureType

    def test_123_alive_after_heartbeat(self):
        m = self.Monitor(heartbeat_timeout_s=30)
        m.record_heartbeat("a1")
        report = m.get_health("a1")
        assert report.is_alive is True

    def test_124_dead_no_heartbeat(self):
        m = self.Monitor(heartbeat_timeout_s=30)
        report = m.get_health("a1")
        assert report.is_alive is False

    def test_125_failure_recorded(self):
        m = self.Monitor()
        m.record_failure("a1", self.FailureType.TIMEOUT)
        report = m.get_health("a1")
        assert report.is_alive is False
        assert report.failure_type == self.FailureType.TIMEOUT

    def test_126_gap_count_tracked(self):
        m = self.Monitor(heartbeat_timeout_s=30)
        m.record_heartbeat("a1")
        m.record_gap("a1")
        report = m.get_health("a1")
        assert report.gap_count == 1

    def test_127_reset(self):
        m = self.Monitor(heartbeat_timeout_s=30)
        m.record_heartbeat("a1")
        m.reset("a1")
        report = m.get_health("a1")
        assert report.is_alive is False


# =============================================================================
# 21. Reconnect Manager
# =============================================================================
class TestReconnectManager:
    def setup_method(self):
        from paper_trading.market_data.reconnect_v161 import ReconnectManager
        from paper_trading.market_data.enums_v161 import ReconnectPolicy
        self.Manager = ReconnectManager
        self.Policy = ReconnectPolicy

    def test_128_no_reconnect_disabled(self):
        m = self.Manager(self.Policy.NO_RECONNECT)
        assert m.should_reconnect() is False

    def test_129_fixed_interval_enabled(self):
        m = self.Manager(self.Policy.FIXED_INTERVAL, max_attempts=3)
        assert m.should_reconnect() is True

    def test_130_exhausted_after_max(self):
        m = self.Manager(self.Policy.FIXED_INTERVAL, max_attempts=2)
        m.record_attempt()
        m.record_attempt()
        assert m.should_reconnect() is False

    def test_131_exponential_backoff_grows(self):
        m = self.Manager(self.Policy.BOUNDED_EXPONENTIAL_BACKOFF,
                          base_interval_s=5, max_interval_s=120, max_attempts=5)
        m.record_attempt()
        i1 = m.get_next_interval_s()
        m.record_attempt()
        i2 = m.get_next_interval_s()
        assert i2 > i1

    def test_132_bounded_at_max_interval(self):
        m = self.Manager(self.Policy.BOUNDED_EXPONENTIAL_BACKOFF,
                          base_interval_s=60, max_interval_s=120, max_attempts=10)
        for _ in range(5):
            m.record_attempt()
        assert m.get_next_interval_s() <= 120

    def test_133_reset_clears_state(self):
        m = self.Manager(self.Policy.FIXED_INTERVAL, max_attempts=2)
        m.record_attempt()
        m.record_attempt()
        m.reset()
        assert m.should_reconnect() is True


# =============================================================================
# 22. Failover Manager
# =============================================================================
class TestFailoverManager:
    def setup_method(self):
        from paper_trading.market_data.failover_v161 import FailoverManager
        from paper_trading.market_data.enums_v161 import FailoverPolicy, SourceClass, MarketDataSessionStatus
        self.Manager = FailoverManager
        self.Policy = FailoverPolicy
        self.SourceClass = SourceClass
        self.Status = MarketDataSessionStatus

    def test_134_live_to_fixture_blocked(self):
        m = self.Manager(self.Policy.PAUSE_ON_FAILURE)
        d = m.decide(self.SourceClass.LIVE_PUBLIC, self.SourceClass.FIXTURE)
        assert d.blocked is True

    def test_135_live_to_offline_blocked(self):
        m = self.Manager(self.Policy.PAUSE_ON_FAILURE)
        d = m.decide(self.SourceClass.LIVE_PUBLIC, self.SourceClass.OFFLINE)
        assert d.blocked is True

    def test_136_pause_on_failure(self):
        m = self.Manager(self.Policy.PAUSE_ON_FAILURE)
        d = m.decide(self.SourceClass.FIXTURE)
        assert d.new_status == self.Status.PAUSED

    def test_137_halt_on_failure(self):
        m = self.Manager(self.Policy.HALT_ON_FAILURE)
        d = m.decide(self.SourceClass.FIXTURE)
        assert d.new_status == self.Status.HALTED

    def test_138_no_failover_halts(self):
        m = self.Manager(self.Policy.NO_FAILOVER)
        d = m.decide(self.SourceClass.FIXTURE)
        assert d.new_status == self.Status.HALTED


# =============================================================================
# 23. Checkpoint Manager
# =============================================================================
class TestCheckpointManager:
    def setup_method(self):
        from paper_trading.market_data.checkpoint_v161 import CheckpointManager
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        self.Manager = CheckpointManager
        self.Status = MarketDataSessionStatus

    def test_139_create_checkpoint(self):
        m = self.Manager()
        cp = m.create("s1", "a1", {"cursor": 10}, sequence_number=10)
        assert cp.checkpoint_id != ""
        assert cp.checkpoint_hash != ""

    def test_140_restore_gives_paused(self):
        m = self.Manager()
        status = m.restore_gives_paused()
        assert status == self.Status.PAUSED

    def test_141_get_latest(self):
        m = self.Manager()
        m.create("s1", "a1", {"cursor": 1})
        m.create("s1", "a1", {"cursor": 2})
        cp = m.get_latest("s1")
        assert cp.adapter_state["cursor"] == 2

    def test_142_deterministic_hash(self):
        m = self.Manager()
        cp1 = m.create("s1", "a1", {"cursor": 10}, sequence_number=10)
        m2 = self.Manager()
        cp2 = m2.create("s1", "a1", {"cursor": 10}, sequence_number=10)
        assert cp1.checkpoint_hash == cp2.checkpoint_hash


# =============================================================================
# 24. Resume Manager
# =============================================================================
class TestResumeManager:
    def setup_method(self):
        from paper_trading.market_data.resume_v161 import SessionResumeManager
        from paper_trading.market_data.models_v161 import MarketDataCheckpoint
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        self.Manager = SessionResumeManager
        self.Checkpoint = MarketDataCheckpoint
        self.Status = MarketDataSessionStatus

    def test_143_resume_from_checkpoint_paused(self):
        m = self.Manager()
        cp = self.Checkpoint(
            checkpoint_id="cp1", session_id="s1", adapter_id="a1",
            created_at_utc="2024-01-02T09:00:00Z",
            sequence_number=1, last_event_id=None,
        )
        result = m.resume_from_checkpoint(cp)
        assert result.success is True
        assert result.new_status == self.Status.PAUSED

    def test_144_resume_from_scratch_paused(self):
        m = self.Manager()
        result = m.resume_from_scratch()
        assert result.new_status == self.Status.PAUSED

    def test_145_cannot_auto_resume_to_running(self):
        m = self.Manager()
        assert m.cannot_auto_resume_to_running() is False


# =============================================================================
# 25. Lineage Tracker
# =============================================================================
class TestLineageTracker:
    def setup_method(self):
        from paper_trading.market_data.lineage_v161 import MarketDataLineageTracker
        self.Tracker = MarketDataLineageTracker

    def test_146_record_and_get(self):
        t = self.Tracker()
        rec = t.record("s1", "r1", "a1", "FIXTURE", "2330", "2024-01-02T09:00:00Z", "STORED")
        assert rec.lineage_id != ""
        assert t.get(rec.lineage_id) is not None

    def test_147_get_for_session(self):
        t = self.Tracker()
        t.record("s1", "r1", "a1", "FIXTURE", "2330", "2024-01-02T09:00:00Z", "STORED")
        t.record("s1", "r2", "a1", "FIXTURE", "2330", "2024-01-02T09:00:01Z", "STORED")
        recs = t.get_for_session("s1")
        assert len(recs) == 2

    def test_148_summarize_session(self):
        t = self.Tracker()
        t.record("s1", "r1", "a1", "FIXTURE", "2330", "2024-01-02T09:00:00Z", "STORED")
        t.record("s1", "r2", "a1", "FIXTURE", "2330", "2024-01-02T09:00:01Z", "NORMALIZATION_FAILED")
        summary = t.summarize_session("s1")
        assert summary["total_records"] == 2
        assert summary["by_stage"]["STORED"] == 1


# =============================================================================
# 26. Reproducibility
# =============================================================================
class TestReproducibility:
    def setup_method(self):
        from paper_trading.market_data.reproducibility_v161 import MarketDataReproducibilityService
        self.Service = MarketDataReproducibilityService

    def test_149_event_hash_deterministic(self):
        svc = self.Service()
        event = {"event_id": "e1", "symbol": "2330", "price": "165.5"}
        h1 = svc.compute_event_hash(event)
        h2 = svc.compute_event_hash(event)
        assert h1 == h2

    def test_150_session_hash_deterministic(self):
        svc = self.Service()
        config = {"adapter_id": "a1"}
        hashes = ["h1", "h2"]
        h1 = svc.compute_session_hash("s1", config, hashes)
        h2 = svc.compute_session_hash("s1", config, hashes)
        assert h1 == h2

    def test_151_different_events_different_hash(self):
        svc = self.Service()
        config = {"adapter_id": "a1"}
        h1 = svc.compute_session_hash("s1", config, ["h1"])
        h2 = svc.compute_session_hash("s1", config, ["h2"])
        assert h1 != h2

    def test_152_build_manifest(self):
        svc = self.Service()
        manifest = svc.build_manifest("m1", "s1", {"a": 1}, ["h1", "h2"])
        assert manifest["reproducible"] is True
        assert manifest["session_hash"] != ""

    def test_153_verify_manifest(self):
        svc = self.Service()
        config = {"a": 1}
        hashes = ["h1", "h2"]
        manifest = svc.build_manifest("m1", "s1", config, hashes)
        assert svc.verify(manifest, "s1", config, hashes) is True

    def test_154_verify_fails_wrong_hashes(self):
        svc = self.Service()
        config = {"a": 1}
        manifest = svc.build_manifest("m1", "s1", config, ["h1"])
        assert svc.verify(manifest, "s1", config, ["h2"]) is False


# =============================================================================
# 27. Explainer
# =============================================================================
class TestExplainer:
    def setup_method(self):
        from paper_trading.market_data.explain_v161 import MarketDataExplainer
        from paper_trading.market_data.enums_v161 import (
            FreshnessStatus, SequenceStatus, DataQualityStatus,
            FailoverPolicy, ReconnectPolicy, SourceClass,
        )
        self.explainer = MarketDataExplainer()
        self.Fresh = FreshnessStatus
        self.Seq = SequenceStatus
        self.Qual = DataQualityStatus
        self.Failover = FailoverPolicy
        self.Reconnect = ReconnectPolicy
        self.Source = SourceClass

    def test_155_explain_freshness_fresh(self):
        s = self.explainer.explain_freshness(self.Fresh.FRESH)
        assert "fresh" in s.lower() or "current" in s.lower()

    def test_156_explain_freshness_not_applicable(self):
        s = self.explainer.explain_freshness(self.Fresh.NOT_APPLICABLE)
        assert "not applicable" in s.lower() or "NOT_APPLICABLE" in s

    def test_157_explain_quality_blocked(self):
        s = self.explainer.explain_quality(self.Qual.BLOCKED)
        assert "blocked" in s.lower() or "duplicate" in s.lower()

    def test_158_explain_failover_blocked(self):
        s = self.explainer.explain_failover(self.Failover.PAUSE_ON_FAILURE, blocked=True)
        assert "BLOCKED" in s or "blocked" in s.lower()

    def test_159_explain_unknown_source(self):
        s = self.explainer.explain_source_class(self.Source.UNKNOWN)
        assert "not trusted" in s.lower() or "UNKNOWN" in s

    def test_160_explain_event_dict(self):
        event = {"symbol": "2330", "source_class": "FIXTURE",
                 "timestamp_utc": "2024-01-02T09:00:00Z",
                 "freshness_status": "NOT_APPLICABLE", "quality_status": "PASS"}
        s = self.explainer.explain_event(event)
        assert "2330" in s
        assert "RESEARCH_ONLY" in s


# =============================================================================
# 28. Store and Query
# =============================================================================
class TestStoreAndQuery:
    def setup_method(self):
        from paper_trading.market_data.store_v161 import MarketDataStore
        from paper_trading.market_data.query_v161 import MarketDataQueryService
        self.Store = MarketDataStore
        self.Query = MarketDataQueryService

    def test_161_store_and_get_trade(self):
        s = self.Store()
        s.store_trade("2330", {"event_id": "e1", "price": "165.5"})
        t = s.get_latest_trade("2330")
        assert t["event_id"] == "e1"

    def test_162_store_and_get_quote(self):
        s = self.Store()
        s.store_quote("2330", {"event_id": "e1", "bid_price": "165.0"})
        q = s.get_latest_quote("2330")
        assert q["event_id"] == "e1"

    def test_163_total_stored(self):
        s = self.Store()
        s.store_trade("2330", {"e": "1"})
        s.store_trade("2330", {"e": "2"})
        assert s.total_stored == 2

    def test_164_list_symbols(self):
        s = self.Store()
        s.store_trade("2330", {"e": "1"})
        s.store_trade("2317", {"e": "2"})
        syms = s.list_symbols_with_trades()
        assert "2330" in syms and "2317" in syms

    def test_165_query_latest_trade(self):
        s = self.Store()
        s.store_trade("2330", {"price": "165.5"})
        q = self.Query(s)
        t = q.latest_trade("2330")
        assert t["price"] == "165.5"

    def test_166_query_submit_real_order_forbidden(self):
        s = self.Store()
        q = self.Query(s)
        with pytest.raises(NotImplementedError):
            q.submit_real_order()

    def test_167_query_connect_broker_forbidden(self):
        s = self.Store()
        q = self.Query(s)
        with pytest.raises(NotImplementedError):
            q.connect_broker()

    def test_168_query_execute_real_trade_forbidden(self):
        s = self.Store()
        q = self.Query(s)
        with pytest.raises(NotImplementedError):
            q.execute_real_trade()


# =============================================================================
# 29. Session end-to-end
# =============================================================================
class TestSessionEndToEnd:
    def _make_session(self, events=None):
        from paper_trading.market_data.session_v161 import MarketDataSession
        from paper_trading.market_data.fixture_adapter_v161 import FixtureAdapter
        from paper_trading.market_data.models_v161 import MarketDataAdapterConfig, MarketDataSessionConfig
        from paper_trading.market_data.enums_v161 import SourceClass
        cfg = MarketDataAdapterConfig(
            adapter_id="test_s1", source_class=SourceClass.FIXTURE,
            provider_name="test", symbols=["2330"],
        )
        adapter = FixtureAdapter(cfg, fixture_events=events or [])
        sess_cfg = MarketDataSessionConfig(
            session_id="sess1", adapter_id="test_s1",
            symbols=["2330"], source_class=SourceClass.FIXTURE,
        )
        return MarketDataSession(sess_cfg, adapter)

    def test_169_start_session(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        s = self._make_session()
        assert s.start() is True
        assert s.status == MarketDataSessionStatus.ACTIVE

    def test_170_pause_and_resume(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        s = self._make_session()
        s.start()
        assert s.pause() is True
        assert s.status == MarketDataSessionStatus.PAUSED
        assert s.resume() is True
        assert s.status == MarketDataSessionStatus.ACTIVE

    def test_171_process_trade_event(self):
        events = [{"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
                   "timestamp_utc": "2024-01-02T09:00:00Z", "payload": {"price": "165.5", "volume": 100}}]
        s = self._make_session(events)
        s.start()
        count = s.poll_and_process()
        assert count == 1
        assert s.store.total_stored == 1

    def test_172_process_quote_event(self):
        events = [{"event_id": "e1", "event_type": "QUOTE", "symbol": "2330",
                   "timestamp_utc": "2024-01-02T09:00:00Z",
                   "payload": {"bid": "165.0", "ask": "165.5"}}]
        s = self._make_session(events)
        s.start()
        count = s.poll_and_process()
        assert count == 1

    def test_173_dedup_prevents_reprocessing(self):
        events = [
            {"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
             "timestamp_utc": "2024-01-02T09:00:00Z", "payload": {"price": "165.5", "volume": 100}},
            {"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
             "timestamp_utc": "2024-01-02T09:00:01Z", "payload": {"price": "165.5", "volume": 100}},
        ]
        s = self._make_session(events)
        s.start()
        count = s.poll_and_process()
        assert count == 1  # second event deduplicated

    def test_174_checkpoint_and_restore_paused(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        s = self._make_session()
        s.start()
        cp = s.create_checkpoint()
        s.restore_from_checkpoint(cp)
        assert s.status == MarketDataSessionStatus.PAUSED

    def test_175_status_dict_safety(self):
        s = self._make_session()
        status = s.get_status_dict()
        assert status["no_real_orders"] is True
        assert status["market_data_only"] is True
        assert status["production_trading_blocked"] is True

    def test_176_lineage_records_pipeline(self):
        events = [{"event_id": "e1", "event_type": "TRADE", "symbol": "2330",
                   "timestamp_utc": "2024-01-02T09:00:00Z", "payload": {"price": "165.5", "volume": 100}}]
        s = self._make_session(events)
        s.start()
        s.poll_and_process()
        summary = s.lineage.summarize_session("sess1")
        assert summary["total_records"] >= 1

    def test_177_halt_session(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        s = self._make_session()
        s.start()
        s.halt()
        assert s.status == MarketDataSessionStatus.HALTED

    def test_178_complete_session(self):
        from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
        s = self._make_session()
        s.start()
        s.complete()
        assert s.status == MarketDataSessionStatus.COMPLETED


# =============================================================================
# 30. Version Info
# =============================================================================
class TestVersionInfo:
    def setup_method(self):
        from release import version_info as vi
        self.vi = vi

    def test_179_version_is_161(self):
        assert self.vi.VERSION == "1.6.1"

    def test_180_release_name(self):
        assert self.vi.RELEASE_NAME == "Market Data Session Adapter"

    def test_181_market_data_session_baseline(self):
        assert self.vi.MARKET_DATA_SESSION_BASELINE == "1.6.1"

    def test_182_live_paper_trading_baseline(self):
        assert self.vi.LIVE_PAPER_TRADING_BASELINE == "1.6.0"

    def test_183_no_real_orders(self):
        assert self.vi.NO_REAL_ORDERS is True

    def test_184_base_release(self):
        assert "1.6.0" in self.vi.BASE_RELEASE

    def test_185_market_data_session_available(self):
        assert self.vi.MARKET_DATA_SESSION_AVAILABLE is True

    def test_186_market_data_session_research_only(self):
        assert self.vi.MARKET_DATA_SESSION_RESEARCH_ONLY is True


# =============================================================================
# 31. CLI Commands
# =============================================================================
class TestCLICommands:
    def setup_method(self):
        from cli.command_registry import get_commands_by_group, get_command, REGISTRY_VERSION
        self.get_group = get_commands_by_group
        self.get_cmd = get_command
        self.REGISTRY_VERSION = REGISTRY_VERSION

    def test_187_market_data_group_count(self):
        cmds = self.get_group("market_data_session")
        assert len(cmds) >= 29

    def test_188_all_research_only(self):
        cmds = self.get_group("market_data_session")
        bad = [c.name for c in cmds if c.safety_classification != "RESEARCH_ONLY"]
        assert not bad, f"Non-RESEARCH_ONLY: {bad}"

    def test_189_market_data_health_registered(self):
        spec = self.get_cmd("market-data-health")
        assert spec is not None
        assert spec.group == "market_data_session"

    def test_190_market_data_session_create_registered(self):
        spec = self.get_cmd("market-data-session-create")
        assert spec is not None

    def test_191_market_data_release_gate_registered(self):
        spec = self.get_cmd("market-data-release-gate")
        assert spec is not None

    def test_192_all_introduced_in_161(self):
        cmds = self.get_group("market_data_session")
        for c in cmds:
            assert c.introduced_in == "1.6.1", f"{c.name} has introduced_in={c.introduced_in}"

    def test_193_registry_version_161(self):
        parts = tuple(int(x) for x in self.REGISTRY_VERSION.split(".")[:3] if x.isdigit())
        assert parts >= (1, 6, 1), f"Expected >= 1.6.1, got {self.REGISTRY_VERSION}"


# =============================================================================
# 32. Release Gate
# =============================================================================
class TestReleaseGate:
    def setup_method(self):
        from release.market_data_session_release_gate_v161 import MarketDataSessionReleaseGate
        self.Gate = MarketDataSessionReleaseGate

    def test_194_gate_runs(self):
        gate = self.Gate()
        result = gate.run()
        assert "overall" in result

    def test_195_gate_passes(self):
        gate = self.Gate()
        result = gate.run()
        assert result["overall"] == "PASS", f"Failed checks: {result['blocked']}"

    def test_196_34_checks(self):
        gate = self.Gate()
        result = gate.run()
        assert result["total"] >= 34

    def test_197_no_blocked_checks(self):
        gate = self.Gate()
        result = gate.run()
        assert result["blocked"] == []

    def test_198_safety_flags_in_result(self):
        gate = self.Gate()
        result = gate.run()
        assert result["no_real_orders"] is True
        assert result["production_trading_blocked"] is True


# =============================================================================
# 33. GUI Panel
# =============================================================================
class TestGUIPanel:
    def setup_method(self):
        import gui.market_data_session_panel as gp
        self.gp = gp
        self.Panel = gp.MarketDataSessionPanel

    def test_199_import_ok(self):
        assert self.gp.NO_REAL_ORDERS is True

    def test_200_broker_disabled(self):
        assert self.gp.BROKER_EXECUTION_ENABLED is False

    def test_201_render_header(self):
        p = self.Panel()
        header = p.render_header()
        assert "Market Data Session" in header

    def test_202_submit_real_order_forbidden(self):
        p = self.Panel()
        with pytest.raises(NotImplementedError):
            p.submit_real_order()

    def test_203_connect_to_broker_forbidden(self):
        p = self.Panel()
        with pytest.raises(NotImplementedError):
            p.connect_to_broker()

    def test_204_execute_live_trade_forbidden(self):
        p = self.Panel()
        with pytest.raises(NotImplementedError):
            p.execute_live_trade()


# =============================================================================
# 34. Health Check
# =============================================================================
class TestHealthCheck:
    def test_205_health_check_passes(self):
        from paper_trading.market_data.health_v161 import MarketDataSessionHealthCheck
        hc = MarketDataSessionHealthCheck()
        result = hc.run()
        assert result["status"] == "PASS"
        assert result["failed"] == 0

    def test_206_health_check_version(self):
        from paper_trading.market_data.health_v161 import MarketDataSessionHealthCheck
        hc = MarketDataSessionHealthCheck()
        result = hc.run()
        assert result["version"] == "1.6.1"


# =============================================================================
# 35. Fixture file existence and validity
# =============================================================================
EXPECTED_FIXTURES = [
    "safety_flags.json",
    "adapter_config_fixture.json",
    "adapter_config_replay.json",
    "adapter_config_offline.json",
    "adapter_unknown_source_blocked.json",
    "raw_event_quote.json",
    "raw_event_trade.json",
    "bid_ask_violated.json",
    "canonical_quote_safety.json",
    "canonical_trade_safety.json",
    "sequence_in_order.json",
    "sequence_gap.json",
    "sequence_duplicate.json",
    "freshness_fresh.json",
    "freshness_stale.json",
    "freshness_not_applicable.json",
    "freshness_future_date.json",
    "failover_live_to_fixture_blocked.json",
    "failover_live_to_offline_blocked.json",
    "failover_pause_on_failure.json",
    "reconnect_no_reconnect.json",
    "reconnect_exponential_backoff.json",
    "checkpoint_valid.json",
    "resume_always_paused.json",
    "symbol_mapper_valid.json",
    "symbol_mapper_ambiguous.json",
    "deduplication_valid.json",
    "quality_gate_blocked.json",
    "quality_gate_warn.json",
    "reproducibility_valid.json",
    "session_e2e_fixture.json",
]


@pytest.mark.parametrize("fname", EXPECTED_FIXTURES)
def test_fixture_exists(fname):
    path = os.path.join(FIXTURES_DIR, fname)
    assert os.path.exists(path), f"Fixture not found: {path}"


@pytest.mark.parametrize("fname", EXPECTED_FIXTURES)
def test_fixture_valid_json(fname):
    path = os.path.join(FIXTURES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)


@pytest.mark.parametrize("fname", EXPECTED_FIXTURES)
def test_fixture_has_market_data_only(fname):
    path = os.path.join(FIXTURES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("market_data_only") is True


@pytest.mark.parametrize("fname", EXPECTED_FIXTURES)
def test_fixture_has_no_real_orders(fname):
    path = os.path.join(FIXTURES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("no_real_orders") is True


@pytest.mark.parametrize("fname", EXPECTED_FIXTURES)
def test_fixture_has_fixture_type(fname):
    path = os.path.join(FIXTURES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("fixture_type") == "TEST_FIXTURE"


# =============================================================================
# 36. Module imports
# =============================================================================
MARKET_DATA_MODULES = [
    "paper_trading.market_data",
    "paper_trading.market_data.enums_v161",
    "paper_trading.market_data.models_v161",
    "paper_trading.market_data.validation_v161",
    "paper_trading.market_data.adapter_base_v161",
    "paper_trading.market_data.adapter_registry_v161",
    "paper_trading.market_data.public_provider_adapter_v161",
    "paper_trading.market_data.replay_adapter_v161",
    "paper_trading.market_data.fixture_adapter_v161",
    "paper_trading.market_data.offline_adapter_v161",
    "paper_trading.market_data.session_v161",
    "paper_trading.market_data.session_clock_v161",
    "paper_trading.market_data.calendar_v161",
    "paper_trading.market_data.symbol_mapper_v161",
    "paper_trading.market_data.normalizer_v161",
    "paper_trading.market_data.quote_normalizer_v161",
    "paper_trading.market_data.trade_normalizer_v161",
    "paper_trading.market_data.sequence_v161",
    "paper_trading.market_data.deduplication_v161",
    "paper_trading.market_data.freshness_v161",
    "paper_trading.market_data.delay_v161",
    "paper_trading.market_data.quality_v161",
    "paper_trading.market_data.anomaly_v161",
    "paper_trading.market_data.feed_monitor_v161",
    "paper_trading.market_data.reconnect_v161",
    "paper_trading.market_data.failover_v161",
    "paper_trading.market_data.checkpoint_v161",
    "paper_trading.market_data.resume_v161",
    "paper_trading.market_data.lineage_v161",
    "paper_trading.market_data.reproducibility_v161",
    "paper_trading.market_data.explain_v161",
    "paper_trading.market_data.store_v161",
    "paper_trading.market_data.query_v161",
    "paper_trading.market_data.health_v161",
]


@pytest.mark.parametrize("module_path", MARKET_DATA_MODULES)
def test_module_imports(module_path):
    import importlib
    mod = importlib.import_module(module_path)
    assert mod is not None


# =============================================================================
# 37. Backward compatibility — v1.6.0 health check still passes
# =============================================================================
class TestBackwardCompatibility:
    def test_207_v160_health_still_passes(self):
        from paper_trading.health_v160 import LivePaperTradingHealthCheck
        hc = LivePaperTradingHealthCheck()
        result = hc.run()
        assert result["status"] == "PASS"

    def test_208_v160_modules_importable(self):
        import paper_trading.enums_v160
        import paper_trading.models_v160
        import paper_trading.session_v160
        assert True
