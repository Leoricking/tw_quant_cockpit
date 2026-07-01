"""
test_multi_session_data_v166.py — Data Isolation tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
from datetime import datetime, timedelta, timezone


class TestDataIsolation:
    def test_init_session(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        assert "s1" in store._stores

    def test_write_and_read(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        ns = store.ISOLATED_NAMESPACES[0]
        store.write("s1", ns, "key1", {"data": 42})
        val = store.read("s1", ns, "key1")
        assert val == {"data": 42}

    def test_no_contamination_between_sessions(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        store.init_session("s2")
        ns = store.ISOLATED_NAMESPACES[0]
        store.write("s1", ns, "secret_key", {"value": 100})
        val = store.read("s2", ns, "secret_key")
        assert val is None

    def test_read_missing_key_returns_none(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        ns = store.ISOLATED_NAMESPACES[0]
        val = store.read("s1", ns, "nonexistent")
        assert val is None

    def test_write_uninitialized_session_raises(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        ns = store.ISOLATED_NAMESPACES[0]
        with pytest.raises(KeyError):
            store.write("uninit", ns, "k", "v")

    def test_isolated_namespaces_has_at_least_5(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        assert len(store.ISOLATED_NAMESPACES) >= 5

    def test_declare_shared_key(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.declare_shared("shared_key")
        assert "shared_key" in store._shared_declarations

    def test_write_shared_requires_declaration(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        with pytest.raises(ValueError):
            store.write_shared("undeclared_key", "value")

    def test_write_and_read_shared(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.declare_shared("market_ref")
        store.write_shared("market_ref", {"price": 150.0})
        val = store.read_shared("market_ref")
        assert val == {"price": 150.0}

    def test_read_shared_undeclared_returns_none(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        val = store.read_shared("no_such_key")
        assert val is None

    def test_detect_cross_session_contamination_clean(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        store.init_session("s2")
        ns = store.ISOLATED_NAMESPACES[0]
        store.write("s1", ns, "k1", {"a": 1})
        store.write("s2", ns, "k2", {"b": 2})
        contamination = store.detect_cross_session_contamination("s1", "s2")
        assert contamination == []

    def test_detect_cross_session_contamination_returns_list(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        store.init_session("s2")
        result = store.detect_cross_session_contamination("s1", "s2")
        assert isinstance(result, list)

    def test_multiple_namespaces_isolated(self):
        from paper_trading.multi_session.data_isolation_v166 import SessionIsolationStore
        store = SessionIsolationStore()
        store.init_session("s1")
        store.init_session("s2")
        for ns in store.ISOLATED_NAMESPACES[:3]:
            store.write("s1", ns, "key", {"session": "s1"})
            val = store.read("s2", ns, "key")
            assert val is None

    def test_required_contamination_count_zero_flag(self):
        import paper_trading.multi_session.data_isolation_v166 as m
        assert m.REQUIRED_CONTAMINATION_COUNT == 0


class TestMarketDataSharing:
    def _make_snapshot(self, sid="snap1", symbol="2330", session="s1",
                       offset_hours=0, fresh=True, pit=True):
        from paper_trading.multi_session.market_data_sharing_v166 import SharedDataSnapshot
        now = datetime.now(timezone.utc)
        return SharedDataSnapshot(
            snapshot_id=sid,
            symbol=symbol,
            provider="test",
            as_of=now,
            available_from=now - timedelta(hours=offset_hours),
            quality_score=0.95,
            source_lineage="test_lineage",
            permitted_sessions=[session],
            data={"price": 100.0},
            is_fresh=fresh,
            pit_verified=pit,
        )

    def test_register_snapshot(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        snap = self._make_snapshot()
        mds.register_snapshot(snap)
        assert snap.snapshot_id in mds._snapshots

    def test_get_for_session_returns_snapshot(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        snap = self._make_snapshot(sid="s1", symbol="2330", session="s1")
        mds.register_snapshot(snap)
        now = datetime.now(timezone.utc)
        result = mds.get_for_session("s1", "2330", now)
        assert result is not None

    def test_get_for_session_returns_none_wrong_session(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        snap = self._make_snapshot(sid="s2", symbol="0050", session="s1")
        mds.register_snapshot(snap)
        now = datetime.now(timezone.utc)
        result = mds.get_for_session("s2", "0050", now)
        assert result is None

    def test_validate_access_permitted_session(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        snap = self._make_snapshot(sid="s3", session="allowed_sess")
        mds.register_snapshot(snap)
        assert mds.validate_access("allowed_sess", "s3") is True

    def test_validate_access_denied_session(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        snap = self._make_snapshot(sid="s4", session="s1")
        mds.register_snapshot(snap)
        assert mds.validate_access("s_denied", "s4") is False

    def test_validate_access_nonexistent_snapshot(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        assert mds.validate_access("s1", "nonexistent") is False

    def test_check_future_leakage_no_leakage(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing
        mds = MarketDataSharing()
        snap = self._make_snapshot()
        now = datetime.now(timezone.utc)
        result = mds.check_future_leakage(snap, now)
        assert isinstance(result, bool)

    def test_check_future_leakage_detects_future(self):
        from paper_trading.multi_session.market_data_sharing_v166 import MarketDataSharing, SharedDataSnapshot
        mds = MarketDataSharing()
        now = datetime.now(timezone.utc)
        snap = SharedDataSnapshot(
            snapshot_id="future_snap",
            symbol="2330",
            provider="test",
            as_of=now,
            available_from=now + timedelta(hours=1),  # Future!
            quality_score=0.9,
            source_lineage="test",
            permitted_sessions=["s1"],
            data={},
            is_fresh=True,
            pit_verified=True,
        )
        result = mds.check_future_leakage(snap, now)
        assert result is True

    def test_no_live_to_fixture_fallback_flag(self):
        import paper_trading.multi_session.market_data_sharing_v166 as m
        assert m.NO_LIVE_TO_FIXTURE_FALLBACK is True

    def test_no_stale_data_as_healthy_flag(self):
        import paper_trading.multi_session.market_data_sharing_v166 as m
        assert m.NO_STALE_DATA_AS_HEALTHY is True
