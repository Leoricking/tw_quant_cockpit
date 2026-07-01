"""
test_multi_session_virtual_clock_v166.py — Virtual Clock tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
from datetime import datetime, timedelta, timezone


def _clock():
    from paper_trading.multi_session.virtual_clock_v166 import VirtualClock
    return VirtualClock()


class TestVirtualClock:
    def test_instantiation(self):
        c = _clock()
        assert c is not None

    def test_now_is_datetime_attribute(self):
        c = _clock()
        assert isinstance(c.now, datetime)

    def test_now_is_not_callable(self):
        c = _clock()
        assert not callable(c.now)

    def test_tick_advances_now(self):
        c = _clock()
        before = c.now
        c.tick(1.0)
        after = c.now
        assert after > before

    def test_tick_advances_by_correct_seconds(self):
        c = _clock()
        before = c.now
        c.tick(10.0)
        elapsed = (c.now - before).total_seconds()
        assert abs(elapsed - 10.0) < 0.001

    def test_tick_default_one_second(self):
        c = _clock()
        before = c.now
        c.tick()
        elapsed = (c.now - before).total_seconds()
        assert abs(elapsed - 1.0) < 0.001

    def test_tick_returns_new_datetime(self):
        c = _clock()
        result = c.tick(5.0)
        assert isinstance(result, datetime)
        assert result == c.now

    def test_advance_to_sets_time(self):
        c = _clock()
        future = c.now + timedelta(hours=1)
        c.advance_to(future)
        assert c.now == future

    def test_advance_to_past_raises(self):
        c = _clock()
        past = c.now - timedelta(seconds=1)
        with pytest.raises(ValueError):
            c.advance_to(past)

    def test_is_expired_false_for_future(self):
        c = _clock()
        future = c.now + timedelta(seconds=60)
        assert c.is_expired(future) is False

    def test_is_expired_true_for_past(self):
        c = _clock()
        past = c.now - timedelta(seconds=1)
        assert c.is_expired(past) is True

    def test_is_expired_at_exact_now(self):
        c = _clock()
        now = c.now
        assert c.is_expired(now) is True

    def test_seconds_until_returns_positive_for_future(self):
        c = _clock()
        future = c.now + timedelta(seconds=30)
        secs = c.seconds_until(future)
        assert secs > 0

    def test_seconds_until_returns_negative_for_past(self):
        c = _clock()
        past = c.now - timedelta(seconds=10)
        secs = c.seconds_until(past)
        assert secs < 0

    def test_elapsed_since_returns_nonnegative(self):
        c = _clock()
        past = c.now - timedelta(seconds=5)
        elapsed = c.elapsed_since(past)
        assert elapsed >= 0

    def test_elapsed_since_correct_value(self):
        c = _clock()
        past = c.now - timedelta(seconds=10)
        elapsed = c.elapsed_since(past)
        assert abs(elapsed - 10.0) < 0.001

    def test_snapshot_returns_string(self):
        c = _clock()
        snap = c.snapshot()
        assert isinstance(snap, str)

    def test_snapshot_is_iso_format(self):
        c = _clock()
        snap = c.snapshot()
        # Should parse as ISO datetime
        parsed = datetime.fromisoformat(snap)
        assert parsed is not None

    def test_no_real_sleep_multiple_ticks_fast(self):
        import time
        c = _clock()
        start = time.monotonic()
        for _ in range(100):
            c.tick(1.0)
        elapsed_real = time.monotonic() - start
        # 100 virtual ticks should complete in well under 1 second
        assert elapsed_real < 1.0

    def test_multiple_ticks_accumulate(self):
        c = _clock()
        start = c.now
        for _ in range(5):
            c.tick(2.0)
        total = (c.now - start).total_seconds()
        assert abs(total - 10.0) < 0.001

    def test_tick_negative_seconds_moves_back(self):
        c = _clock()
        before = c.now
        c.tick(-5.0)
        assert c.now < before

    def test_initial_time_has_timezone(self):
        c = _clock()
        assert c.now.tzinfo is not None

    def test_no_real_sleep_flag(self):
        import paper_trading.multi_session.virtual_clock_v166 as m
        assert m.NO_REAL_SLEEP is True

    def test_custom_start_time(self):
        from paper_trading.multi_session.virtual_clock_v166 import VirtualClock
        custom = datetime(2025, 6, 1, 9, 30, 0, tzinfo=timezone.utc)
        c = VirtualClock(start=custom)
        assert c.now == custom

    def test_advance_to_same_time_ok(self):
        c = _clock()
        now = c.now
        c.advance_to(now)
        assert c.now == now
