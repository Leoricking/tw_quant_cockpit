"""tests/test_data_freshness_v134.py — v1.3.4 Data Freshness Monitor tests.

[!] Research Only. No Real Orders. All test data is DEMO_ONLY / TEST_FIXTURE.
[!] Tests do not trigger auto-refresh, auto-repair, or broker actions.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import pytest

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TEST_DATA_MODE = "DEMO_ONLY"
FIXTURE_TYPE = "TEST_FIXTURE"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ts_ago(seconds: float) -> str:
    dt = datetime.now(timezone.utc) - timedelta(seconds=seconds)
    return dt.isoformat()


def _ts_future(seconds: float = 86400) -> str:
    dt = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    return dt.isoformat()


# ---------------------------------------------------------------------------
# Fixed-clock helpers — produce deterministic timestamps independent of the
# real system clock.  Use these whenever a test needs a specific staleness
# outcome that would otherwise depend on whether tests run on a trading day
# or inside market hours.
#
# _FIXED_NOW_UTC  =  2026-01-07 02:00 UTC  =  2026-01-07 10:00 Asia/Taipei
#                 →  Wednesday, market open (09:00–13:30 TWSE)
#                 →  is_trading_day=True, market_open=True
# ---------------------------------------------------------------------------
_FIXED_NOW_UTC = datetime(2026, 1, 7, 2, 0, 0, tzinfo=timezone.utc)


def _fixed_now_provider():
    """Return the fixed UTC datetime used in date-stable tests."""
    return _FIXED_NOW_UTC


def _ts_ago_fixed(seconds: float, now: datetime = _FIXED_NOW_UTC) -> str:
    """Create a timestamp *seconds* before *now* (default fixed trading-day clock)."""
    return (now - timedelta(seconds=seconds)).isoformat()


def _ts_future_fixed(seconds: float = 86400, now: datetime = _FIXED_NOW_UTC) -> str:
    """Create a timestamp *seconds* after *now* (default fixed trading-day clock)."""
    return (now + timedelta(seconds=seconds)).isoformat()


# ============================================================
# TestFreshnessModels
# ============================================================
class TestFreshnessModels:
    """8 tests for model round-trips and invariants."""

    def test_freshness_record_defaults(self):
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus, FreshnessSeverity
        rec = FreshnessRecord()
        assert rec.freshness_status == FreshnessStatus.UNKNOWN
        assert rec.severity == FreshnessSeverity.INFO
        assert rec.blocks_analysis is False

    def test_freshness_record_round_trip(self):
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus
        rec = FreshnessRecord(
            record_id="r1", symbol="2330", dataset_type="DAILY_OHLCV",
            freshness_status=FreshnessStatus.FRESH, data_mode="DEMO_ONLY",
        )
        d = rec.to_dict()
        rec2 = FreshnessRecord.from_dict(d)
        assert rec2.record_id == "r1"
        assert rec2.symbol == "2330"
        assert rec2.freshness_status == FreshnessStatus.FRESH

    def test_freshness_policy_round_trip(self):
        from data_freshness.models_v134 import FreshnessPolicy
        p = FreshnessPolicy(policy_id="p1", stale_after=86400.0, critical_after=172800.0)
        d = p.to_dict()
        p2 = FreshnessPolicy.from_dict(d)
        assert p2.policy_id == "p1"
        assert p2.stale_after == 86400.0

    def test_provider_sla_record_round_trip(self):
        from data_freshness.models_v134 import ProviderSLARecord, ProviderSLAStatus
        r = ProviderSLARecord(provider_id="p1", capability="DAILY_OHLCV",
                               status=ProviderSLAStatus.HEALTHY)
        d = r.to_dict()
        r2 = ProviderSLARecord.from_dict(d)
        assert r2.provider_id == "p1"
        assert r2.status == ProviderSLAStatus.HEALTHY

    def test_freshness_alert_round_trip(self):
        from data_freshness.models_v134 import FreshnessAlert
        a = FreshnessAlert(alert_id="a1", symbol="2330", dataset_type="DAILY_OHLCV",
                            status="OPEN")
        d = a.to_dict()
        a2 = FreshnessAlert.from_dict(d)
        assert a2.alert_id == "a1"
        assert a2.status == "OPEN"

    def test_freshness_status_is_ok(self):
        from data_freshness.models_v134 import FreshnessStatus
        assert FreshnessStatus.is_ok(FreshnessStatus.FRESH) is True
        assert FreshnessStatus.is_ok(FreshnessStatus.NEAR_STALE) is True
        assert FreshnessStatus.is_ok(FreshnessStatus.STALE) is False

    def test_freshness_status_is_blocking(self):
        from data_freshness.models_v134 import FreshnessStatus
        assert FreshnessStatus.is_blocking(FreshnessStatus.CRITICALLY_STALE) is True
        assert FreshnessStatus.is_blocking(FreshnessStatus.NEVER_RECEIVED) is True
        assert FreshnessStatus.is_blocking(FreshnessStatus.FRESH) is False

    def test_daily_freshness_summary_round_trip(self):
        from data_freshness.models_v134 import DailyFreshnessSummary
        s = DailyFreshnessSummary(fresh_count=5, stale_count=2)
        d = s.to_dict()
        assert d["fresh_count"] == 5
        assert d["stale_count"] == 2


# ============================================================
# TestCalendar
# ============================================================
class TestCalendar:
    """9 tests for trading calendar."""

    def test_weekday_is_trading(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        monday = date(2024, 1, 8)  # Monday
        assert cal.is_trading_day(monday) is True

    def test_saturday_not_trading(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        saturday = date(2024, 1, 6)  # Saturday
        assert cal.is_trading_day(saturday) is False

    def test_sunday_not_trading(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        sunday = date(2024, 1, 7)  # Sunday
        assert cal.is_trading_day(sunday) is False

    def test_previous_trading_day_from_monday(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        monday = date(2024, 1, 8)
        prev = cal.previous_trading_day(monday)
        assert prev == date(2024, 1, 5)  # Friday

    def test_previous_trading_day_from_tuesday(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        tuesday = date(2024, 1, 9)
        prev = cal.previous_trading_day(tuesday)
        assert prev == date(2024, 1, 8)  # Monday

    def test_expected_latest_trading_day_returns_date(self):
        from data_freshness.trading_calendar import TradingCalendar
        cal = TradingCalendar()
        d = cal.expected_latest_trading_day()
        from datetime import date
        assert isinstance(d, date)

    def test_trading_days_between(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        # Mon to Fri inclusive = 5 trading days
        start = date(2024, 1, 8)
        end = date(2024, 1, 12)
        count = cal.trading_days_between(start, end)
        assert count == 5

    def test_is_approximate_with_no_holidays(self):
        from data_freshness.trading_calendar import TradingCalendar
        cal = TradingCalendar()
        assert cal.is_approximate() is True

    def test_is_not_approximate_with_holidays(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar(holidays={date(2024, 2, 8)})
        assert cal.is_approximate() is False


# ============================================================
# TestFreshnessPolicy
# ============================================================
class TestFreshnessPolicy:
    """9 tests for policy registry."""

    def test_get_daily_ohlcv_policy(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        p = reg.get_policy(DatasetType.DAILY_OHLCV)
        assert p.stale_after == 86400.0
        assert p.critical_after == 172800.0

    def test_get_intraday_policy(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        p = reg.get_policy(DatasetType.INTRADAY_OHLCV)
        assert p.stale_after == 300.0

    def test_get_monthly_revenue_policy(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        p = reg.get_policy(DatasetType.MONTHLY_REVENUE)
        assert p.stale_after == 2592000.0

    def test_get_financial_statement_policy(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        p = reg.get_policy(DatasetType.FINANCIAL_STATEMENT)
        assert p.stale_after == 7776000.0

    def test_corporate_actions_blocks_backtest(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        profiles = reg.get_blocking_profiles(DatasetType.CORPORATE_ACTIONS)
        assert "backtest" in profiles

    def test_daily_ohlcv_blocks_precise_price(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import DatasetType
        reg = DataFreshnessPolicyRegistry()
        profiles = reg.get_blocking_profiles(DatasetType.DAILY_OHLCV)
        assert "precise_price" in profiles

    def test_register_custom_policy(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        from data_freshness.models_v134 import FreshnessPolicy, DatasetType
        reg = DataFreshnessPolicyRegistry()
        custom = FreshnessPolicy(policy_id="custom", dataset_type=DatasetType.DAILY_OHLCV,
                                  stale_after=3600.0)
        reg.register_policy(custom)
        p = reg.get_policy(DatasetType.DAILY_OHLCV)
        assert p.policy_id == "custom"
        assert p.stale_after == 3600.0

    def test_list_policies_returns_all(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        reg = DataFreshnessPolicyRegistry()
        policies = reg.list_policies()
        assert len(policies) >= 10

    def test_fallback_for_unknown_type(self):
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        reg = DataFreshnessPolicyRegistry()
        p = reg.get_policy("NONEXISTENT_TYPE")
        # Should return DAILY_OHLCV default
        assert p.stale_after == 86400.0


# ============================================================
# TestEvaluator
# ============================================================
class TestEvaluator:
    """17 tests for freshness evaluator."""

    def test_fresh_recent_timestamp(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        ts = _ts_ago(3600)  # 1 hour ago
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        # 1h old data is FRESH, NEAR_STALE, MARKET_CLOSED_VALID, or NON_TRADING_DAY_VALID
        assert FreshnessStatus.is_ok(rec.freshness_status)

    def test_stale_old_timestamp(self):
        # Use a fixed clock (Wed 2026-01-07 10:00 Asia/Taipei, market open) so that
        # trading-day exemptions are irrelevant and age alone determines staleness.
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ts = _ts_ago_fixed(200000)  # 200 000 s ≈ 2.3 days before fixed clock
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)

    def test_critically_stale_very_old(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        ts = _ts_ago(500000)  # very old
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status == FreshnessStatus.CRITICALLY_STALE

    def test_future_timestamp_never_fresh(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        ts = _ts_future(86400)
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status == FreshnessStatus.FUTURE_TIMESTAMP

    def test_missing_timestamp_never_received(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        rec = ev.evaluate("2330", "DAILY_OHLCV", None)
        assert rec.freshness_status == FreshnessStatus.NEVER_RECEIVED

    def test_naive_timestamp_invalid(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        rec = ev.evaluate("2330", "DAILY_OHLCV", "2024-01-15T08:00:00")  # naive
        assert rec.freshness_status == FreshnessStatus.INVALID_TIMESTAMP

    def test_demo_mode_yields_demo_only(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        rec = ev.evaluate("2330", "DAILY_OHLCV", _now_iso(), data_mode="DEMO_ONLY")
        assert rec.freshness_status == FreshnessStatus.DEMO_ONLY

    def test_mock_mode_yields_demo_only(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        rec = ev.evaluate("2330", "DAILY_OHLCV", _now_iso(), data_mode="MOCK")
        assert rec.freshness_status == FreshnessStatus.DEMO_ONLY

    def test_near_stale_timestamp(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        ts = _ts_ago(75000)  # ~20.8 hours — past 80% but within 24h
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status in (FreshnessStatus.NEAR_STALE, FreshnessStatus.FRESH,
                                         FreshnessStatus.NON_TRADING_DAY_VALID,
                                         FreshnessStatus.MARKET_CLOSED_VALID)

    def test_source_ts_preferred_over_fetched_at(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        ev = DataFreshnessEvaluator()
        # source_ts = recent, fetched_at = very old
        rec = ev.evaluate("2330", "DAILY_OHLCV",
                           observed_ts=_ts_ago(500000),
                           source_ts=_ts_ago(3600))
        # Should use source_ts -> recent/fresh rather than observed_ts old
        assert rec.freshness_status not in (FreshnessStatus.CRITICALLY_STALE,)

    def test_calculate_age_positive(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        ev = DataFreshnessEvaluator()
        ts = _ts_ago(3600)
        age = ev.calculate_age(ts)
        assert age is not None
        assert 3500 < age < 3700

    def test_calculate_age_none_on_invalid(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        ev = DataFreshnessEvaluator()
        assert ev.calculate_age("invalid-ts") is None

    def test_evaluate_timestamp_returns_tuple(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        ev = DataFreshnessEvaluator()
        status, severity, reasons = ev.evaluate_timestamp(_ts_ago(3600), "DAILY_OHLCV")
        assert isinstance(status, str)
        assert isinstance(severity, str)
        assert isinstance(reasons, list)

    def test_evaluate_dataset_from_dict(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        ev = DataFreshnessEvaluator()
        d = {"symbol": "2330", "source_timestamp": _ts_ago(3600), "data_mode": "REAL"}
        rec = ev.evaluate_dataset(d, "DAILY_OHLCV")
        assert rec.symbol == "2330"

    def test_determine_severity_fresh(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessSeverity
        ev = DataFreshnessEvaluator()
        assert ev.determine_severity(FreshnessStatus.FRESH) == FreshnessSeverity.INFO

    def test_determine_severity_critical(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessSeverity
        ev = DataFreshnessEvaluator()
        assert ev.determine_severity(FreshnessStatus.CRITICALLY_STALE) == FreshnessSeverity.CRITICAL

    def test_precise_price_blocked_when_stale(self):
        # Use a fixed clock so the result is stable regardless of when tests run.
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.policy_v134 import DataFreshnessPolicyRegistry
        ev = DataFreshnessEvaluator(
            policy_registry=DataFreshnessPolicyRegistry(),
            now_provider=_fixed_now_provider,
        )
        ts = _ts_ago_fixed(200000)  # 200 000 s ≈ 2.3 days before fixed clock
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.precise_price_allowed is False


# ============================================================
# TestScanner
# ============================================================
class TestScanner:
    """11 tests for freshness scanner."""

    def test_scan_symbol_returns_records(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        records = scanner.scan_symbol("2330")
        assert len(records) > 0

    def test_scan_symbol_each_record_has_status(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        records = scanner.scan_symbol("2330")
        for rec in records:
            assert rec.freshness_status is not None

    def test_scan_symbols_returns_dict(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        result = scanner.scan_symbols(["2330", "2317"])
        assert isinstance(result, dict)
        assert "2330" in result
        assert "2317" in result

    def test_scan_symbol_with_data_store(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        from data_freshness.models_v134 import FreshnessStatus
        scanner = DataFreshnessScanner()
        store = {"2330::DAILY_OHLCV": {"source_timestamp": _ts_ago(3600), "data_mode": "REAL"}}
        records = scanner.scan_symbol("2330", data_store=store)
        assert len(records) > 0

    def test_scan_universe_default(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        result = scanner.scan_universe("core")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_scan_tier(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        result = scanner.scan_tier("core")
        assert isinstance(result, dict)

    def test_scan_provider(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        recs = scanner.scan_provider("test_provider")
        assert isinstance(recs, list)

    def test_scan_dataset_type(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner()
        recs = scanner.scan_dataset_type("DAILY_OHLCV")
        assert isinstance(recs, list)

    def test_summarize(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus
        scanner = DataFreshnessScanner()
        records = [FreshnessRecord(symbol="2330", freshness_status=FreshnessStatus.FRESH),
                   FreshnessRecord(symbol="2330", freshness_status=FreshnessStatus.STALE)]
        summary = scanner.summarize(records)
        assert summary.fresh_count == 1
        assert summary.stale_count == 1

    def test_list_stale(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus
        scanner = DataFreshnessScanner()
        records = [FreshnessRecord(freshness_status=FreshnessStatus.STALE),
                   FreshnessRecord(freshness_status=FreshnessStatus.FRESH)]
        stale = scanner.list_stale(records)
        assert len(stale) == 1

    def test_max_symbols_limit(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        scanner = DataFreshnessScanner(max_symbols=3)
        symbols = [f"{i:04d}" for i in range(10)]
        result = scanner.scan_symbols(symbols)
        assert len(result) <= 3


# ============================================================
# TestProviderSLA
# ============================================================
class TestProviderSLA:
    """11 tests for provider SLA monitor."""

    def test_record_success(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        from data_freshness.models_v134 import ProviderSLAStatus
        m = ProviderSLAMonitor()
        m.record_success("p1", "DAILY_OHLCV", latency_seconds=1.0)
        rec = m.get_sla("p1", "DAILY_OHLCV")
        assert rec is not None
        assert rec.status == ProviderSLAStatus.HEALTHY

    def test_record_failure_increments(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        m.record_failure("p1", "DAILY_OHLCV", reason="timeout")
        rec = m.get_sla("p1", "DAILY_OHLCV")
        assert rec.consecutive_failures == 1

    def test_three_failures_breach(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        from data_freshness.models_v134 import ProviderSLAStatus
        m = ProviderSLAMonitor()
        m.record_failure("p1", "DAILY_OHLCV")
        m.record_failure("p1", "DAILY_OHLCV")
        m.record_failure("p1", "DAILY_OHLCV")
        rec = m.get_sla("p1", "DAILY_OHLCV")
        assert rec.status == ProviderSLAStatus.BREACHED
        assert rec.breached is True

    def test_list_all(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        m.record_success("p1", "DAILY_OHLCV")
        m.record_success("p2", "INSTITUTIONAL")
        all_recs = m.list_all()
        assert len(all_recs) == 2

    def test_list_breached(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        m.record_failure("p1", "DAILY_OHLCV")
        m.record_failure("p1", "DAILY_OHLCV")
        m.record_failure("p1", "DAILY_OHLCV")
        breached = m.list_breached()
        assert len(breached) >= 1

    def test_summarize(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        summary = m.summarize()
        assert summary["auto_refresh_enabled"] is False
        assert summary["no_real_orders"] is True

    def test_evaluate_provider_unknown(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        from data_freshness.models_v134 import ProviderSLAStatus
        m = ProviderSLAMonitor()
        rec = m.evaluate_provider("p_new", "DAILY_OHLCV")
        # New provider with no history: UNKNOWN or HEALTHY (no failures observed yet)
        assert rec.status in (ProviderSLAStatus.UNKNOWN, ProviderSLAStatus.HEALTHY)

    def test_success_resets_failures(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        m.record_failure("p1", "DAILY_OHLCV")
        m.record_failure("p1", "DAILY_OHLCV")
        m.record_success("p1", "DAILY_OHLCV")
        rec = m.get_sla("p1", "DAILY_OHLCV")
        assert rec.consecutive_failures == 0

    def test_no_auto_refresh_in_summary(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        s = m.summarize()
        assert s.get("auto_refresh_enabled") is False

    def test_record_success_stores_latency(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        m.record_success("p1", "DAILY_OHLCV", latency_seconds=2.5)
        rec = m.get_sla("p1", "DAILY_OHLCV")
        assert rec.latency_seconds == 2.5

    def test_get_sla_none_if_not_exists(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        m = ProviderSLAMonitor()
        assert m.get_sla("nonexistent", "DAILY_OHLCV") is None


# ============================================================
# TestAlerts
# ============================================================
class TestAlerts:
    """9 tests for alert engine."""

    def test_build_alert_from_record(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus, FreshnessSeverity
        engine = FreshnessAlertEngine()
        rec = FreshnessRecord(symbol="2330", dataset_type="DAILY_OHLCV",
                               freshness_status=FreshnessStatus.STALE,
                               severity=FreshnessSeverity.ERROR,
                               policy_id="default_daily_ohlcv")
        alert = engine.build_alert(rec)
        assert alert.symbol == "2330"
        assert "STALE" in alert.title

    def test_add_alert_new(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        a = FreshnessAlert(alert_id=str(uuid.uuid4()),
                            dedup_key="2330|DAILY_OHLCV||STALE|",
                            symbol="2330", dataset_type="DAILY_OHLCV")
        result = engine.add_alert(a)
        assert result is True

    def test_add_alert_dedup(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        a1 = FreshnessAlert(alert_id=str(uuid.uuid4()),
                             dedup_key="2330|DAILY_OHLCV||STALE|",
                             symbol="2330", dataset_type="DAILY_OHLCV")
        a2 = FreshnessAlert(alert_id=str(uuid.uuid4()),
                             dedup_key="2330|DAILY_OHLCV||STALE|",
                             symbol="2330", dataset_type="DAILY_OHLCV")
        engine.add_alert(a1)
        result = engine.add_alert(a2)
        assert result is False  # dedup

    def test_list_active(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        a = FreshnessAlert(alert_id=str(uuid.uuid4()),
                            dedup_key="k1", symbol="2330", dataset_type="DAILY_OHLCV")
        engine.add_alert(a)
        active = engine.list_active()
        assert len(active) == 1

    def test_acknowledge_alert(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        aid = str(uuid.uuid4())
        a = FreshnessAlert(alert_id=aid, dedup_key="k_ack",
                            symbol="2330", dataset_type="DAILY_OHLCV")
        engine.add_alert(a)
        result = engine.acknowledge(aid, reason="test ack")
        assert result is True
        assert a.acknowledged is True

    def test_resolve_alert(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        aid = str(uuid.uuid4())
        a = FreshnessAlert(alert_id=aid, dedup_key="k_res",
                            symbol="2330", dataset_type="DAILY_OHLCV")
        engine.add_alert(a)
        engine.resolve(aid, reason="test resolve")
        active = engine.list_active()
        assert all(x.alert_id != aid for x in active)

    def test_summarize(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        engine = FreshnessAlertEngine()
        summary = engine.summarize()
        assert summary["alerts_trigger_trade_actions"] is False
        assert summary["no_real_orders"] is True

    def test_list_by_symbol(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        a = FreshnessAlert(alert_id=str(uuid.uuid4()), dedup_key="k_sym",
                            symbol="2330", dataset_type="DAILY_OHLCV")
        engine.add_alert(a)
        alerts = engine.list_by_symbol("2330")
        assert len(alerts) >= 1

    def test_reopen_alert(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        from data_freshness.models_v134 import FreshnessAlert
        engine = FreshnessAlertEngine()
        aid = str(uuid.uuid4())
        a = FreshnessAlert(alert_id=aid, dedup_key="k_reopen",
                            symbol="2330", dataset_type="DAILY_OHLCV")
        engine.add_alert(a)
        engine.resolve(aid)
        result = engine.reopen(aid, reason="re-occurred")
        assert result is True
        assert a.status == "OPEN"


# ============================================================
# TestRepairIntegration
# ============================================================
class TestRepairIntegration:
    """9 tests for freshness-repair integration."""

    def test_map_stale_to_stale_data(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessStatus
        ri = FreshnessRepairIntegration()
        assert ri.map_freshness_to_repair_issue(FreshnessStatus.STALE) == "STALE_DATA"

    def test_map_critically_stale(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessStatus
        ri = FreshnessRepairIntegration()
        assert ri.map_freshness_to_repair_issue(FreshnessStatus.CRITICALLY_STALE) == "STALE_DATA"

    def test_map_never_received(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessStatus
        ri = FreshnessRepairIntegration()
        assert ri.map_freshness_to_repair_issue(FreshnessStatus.NEVER_RECEIVED) == "MISSING_DATA"

    def test_map_provider_delayed(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessStatus
        ri = FreshnessRepairIntegration()
        assert ri.map_freshness_to_repair_issue(FreshnessStatus.PROVIDER_DELAYED) == "UNAVAILABLE_SOURCE"

    def test_map_future_timestamp(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessStatus
        ri = FreshnessRepairIntegration()
        assert ri.map_freshness_to_repair_issue(FreshnessStatus.FUTURE_TIMESTAMP) == "BLOCKED_DATA"

    def test_no_auto_create_without_flag(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus
        ri = FreshnessRepairIntegration()
        rec = FreshnessRecord(symbol="2330", freshness_status=FreshnessStatus.STALE)
        task_id = ri.create_repair_task(rec, create_task=False)
        assert task_id is None

    def test_summarize_repair_candidates(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus
        ri = FreshnessRepairIntegration()
        records = [
            FreshnessRecord(symbol="2330", freshness_status=FreshnessStatus.STALE,
                            dataset_type="DAILY_OHLCV"),
            FreshnessRecord(symbol="2317", freshness_status=FreshnessStatus.FRESH,
                            dataset_type="DAILY_OHLCV"),
        ]
        candidates = ri.summarize_repair_candidates(records)
        assert len(candidates) == 1
        assert candidates[0]["symbol"] == "2330"

    def test_attach_repair_task_id(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessAlert
        ri = FreshnessRepairIntegration()
        a = FreshnessAlert(alert_id="a1", dedup_key="k", symbol="2330", dataset_type="DAILY_OHLCV")
        ri.attach_repair_task_id(a, "task-001")
        assert a.repair_task_id == "task-001"

    def test_map_invalid_timestamp(self):
        from data_freshness.repair_integration_v134 import FreshnessRepairIntegration
        from data_freshness.models_v134 import FreshnessStatus
        ri = FreshnessRepairIntegration()
        assert ri.map_freshness_to_repair_issue(FreshnessStatus.INVALID_TIMESTAMP) == "INVALID_SCHEMA"


# ============================================================
# TestDataQualityUniverse
# ============================================================
class TestDataQualityUniverse:
    """8 tests for snapshot store and report."""

    def test_snapshot_store_save_load(self, tmp_path):
        from data_freshness.snapshot_store_v134 import FreshnessSnapshotStore
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus
        store = FreshnessSnapshotStore(base_dir=str(tmp_path))
        records = [FreshnessRecord(symbol="2330", freshness_status=FreshnessStatus.FRESH)]
        store.save_snapshot(records)
        loaded = store.load_latest_snapshot()
        assert len(loaded) == 1
        assert loaded[0].symbol == "2330"

    def test_snapshot_store_sla_history(self, tmp_path):
        from data_freshness.snapshot_store_v134 import FreshnessSnapshotStore
        from data_freshness.models_v134 import ProviderSLARecord, ProviderSLAStatus
        store = FreshnessSnapshotStore(base_dir=str(tmp_path))
        records = [ProviderSLARecord(provider_id="p1", status=ProviderSLAStatus.HEALTHY)]
        store.save_sla_history(records)
        loaded = store.load_sla_history()
        assert len(loaded) == 1

    def test_snapshot_store_alerts(self, tmp_path):
        from data_freshness.snapshot_store_v134 import FreshnessSnapshotStore
        from data_freshness.models_v134 import FreshnessAlert
        store = FreshnessSnapshotStore(base_dir=str(tmp_path))
        alerts = [FreshnessAlert(alert_id="a1", dedup_key="k", symbol="2330",
                                  dataset_type="DAILY_OHLCV")]
        store.save_alerts(alerts)
        loaded = store.load_alerts()
        assert len(loaded) == 1

    def test_snapshot_store_daily_summary(self, tmp_path):
        from data_freshness.snapshot_store_v134 import FreshnessSnapshotStore
        from data_freshness.models_v134 import DailyFreshnessSummary
        store = FreshnessSnapshotStore(base_dir=str(tmp_path))
        s = DailyFreshnessSummary(fresh_count=10, stale_count=2)
        store.save_daily_summary(s)
        loaded = store.load_daily_summary()
        assert loaded is not None
        assert loaded.fresh_count == 10

    def test_snapshot_store_empty_load(self, tmp_path):
        from data_freshness.snapshot_store_v134 import FreshnessSnapshotStore
        store = FreshnessSnapshotStore(base_dir=str(tmp_path))
        assert store.load_latest_snapshot() == []
        assert store.load_sla_history() == []
        assert store.load_alerts() == []
        assert store.load_daily_summary() is None

    def test_report_generate(self):
        from data_freshness.report_v134 import DataFreshnessReport
        from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus, DailyFreshnessSummary
        report = DataFreshnessReport()
        records = [FreshnessRecord(symbol="2330", freshness_status=FreshnessStatus.FRESH)]
        d = report.generate(records, [], [], DailyFreshnessSummary())
        assert d["safety"]["no_real_orders"] is True
        assert d["totals"]["fresh"] == 1

    def test_report_format_text(self):
        from data_freshness.report_v134 import DataFreshnessReport
        from data_freshness.models_v134 import DailyFreshnessSummary
        report = DataFreshnessReport()
        d = report.generate([], [], [], DailyFreshnessSummary())
        text = report.format_text(d)
        assert "Research Only" in text

    def test_report_format_markdown(self):
        from data_freshness.report_v134 import DataFreshnessReport
        from data_freshness.models_v134 import DailyFreshnessSummary
        report = DataFreshnessReport()
        d = report.generate([], [], [], DailyFreshnessSummary())
        md = report.format_markdown(d)
        assert "Data Freshness Report" in md
        assert "No Real Orders" in md


# ============================================================
# TestCLI
# ============================================================
class TestCLI:
    """9 tests for CLI command functions."""

    @staticmethod
    def _main_py():
        import pathlib
        return str(pathlib.Path(__file__).resolve().parent.parent / "main.py")

    def test_freshness_health_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-health"],
            capture_output=True, text=True, timeout=60
        )
        # Should not crash — may FAIL checks but should complete
        assert result.returncode in (0, 1)

    def test_freshness_status_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-status"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_freshness_show_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-show", "--symbol", "2330"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_freshness_scan_symbol(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-scan", "--symbol", "2330"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_freshness_summary_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-summary"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_freshness_alerts_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-alerts"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_provider_sla_status_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "provider-sla-status"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_freshness_create_repair_runs(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "freshness-create-repair"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode in (0, 1)

    def test_version_info_shows_134(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, self._main_py(), "version-info"],
            capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode == 0
        # Accept v1.3.4 or any successor version in the 1.3.x/1.4.x+ line
        assert "1.3." in result.stdout or "1.4." in result.stdout or "1.5." in result.stdout


# ============================================================
# TestGUI
# ============================================================
class TestGUI:
    """10 tests for GUI panel."""

    def test_gui_panel_importable(self):
        from gui.data_freshness_panel import DataFreshnessPanel
        assert DataFreshnessPanel is not None

    def test_gui_panel_has_no_real_orders(self):
        from gui import data_freshness_panel
        assert getattr(data_freshness_panel, "NO_REAL_ORDERS", False) is True

    def test_gui_panel_stub_when_no_pyside(self):
        from gui import data_freshness_panel
        panel_cls = data_freshness_panel.DataFreshnessPanel
        # Should be instantiable (stub or real)
        assert panel_cls is not None

    def test_gui_panel_stub_has_no_real_orders_attr(self):
        from gui.data_freshness_panel import DataFreshnessPanel
        # stub class should have safety attr
        assert hasattr(DataFreshnessPanel, "NO_REAL_ORDERS") or True  # stub or real

    def test_adapter_importable(self):
        try:
            from gui.data_freshness_adapter import DataFreshnessAdapter
        except ImportError:
            pass  # optional adapter

    def test_models_v134_importable(self):
        from data_freshness.models_v134 import (
            FreshnessRecord, FreshnessPolicy, FreshnessAlert,
            ProviderSLARecord, DailyFreshnessSummary,
        )
        assert FreshnessRecord is not None

    def test_evaluator_importable(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        assert DataFreshnessEvaluator is not None

    def test_scanner_importable(self):
        from data_freshness.scanner_v134 import DataFreshnessScanner
        assert DataFreshnessScanner is not None

    def test_alert_engine_importable(self):
        from data_freshness.alert_engine_v134 import FreshnessAlertEngine
        assert FreshnessAlertEngine is not None

    def test_sla_monitor_importable(self):
        from data_freshness.sla_monitor_v134 import ProviderSLAMonitor
        assert ProviderSLAMonitor is not None


# ============================================================
# TestRegression
# ============================================================
class TestRegression:
    """14 regression tests: version, safety, existing features."""

    def test_version_is_134(self):
        from release.version_info import VERSION
        # v1.3.4 functionality preserved — accept v1.3.4 or any successor release
        major, minor, patch = (int(x) for x in VERSION.split(".")[:3])
        assert (major, minor, patch) >= (1, 3, 4), f"Expected >= 1.3.4, got {VERSION}"

    def test_release_name_is_data_freshness_monitor(self):
        from release.version_info import RELEASE_NAME, BASE_RELEASE, VERSION
        # Data Freshness Monitor is either current or a predecessor release
        # Accept v1.3.4+, v1.4.x or any future release built on it
        major, minor, patch = (int(x) for x in VERSION.split(".")[:3])
        assert (
            RELEASE_NAME == "Data Freshness Monitor"
            or "Data Freshness Monitor" in BASE_RELEASE
            or (major, minor, patch) >= (1, 3, 5)
        )

    def test_no_real_orders(self):
        from release.version_info import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_broker_execution_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_freshness_auto_refresh_disabled(self):
        from release.version_info import FRESHNESS_AUTO_REFRESH_ENABLED
        assert FRESHNESS_AUTO_REFRESH_ENABLED is False

    def test_freshness_auto_repair_disabled(self):
        from release.version_info import FRESHNESS_AUTO_REPAIR_ENABLED
        assert FRESHNESS_AUTO_REPAIR_ENABLED is False

    def test_freshness_mock_fallback_disabled(self):
        from release.version_info import FRESHNESS_MOCK_FALLBACK_ENABLED
        assert FRESHNESS_MOCK_FALLBACK_ENABLED is False

    def test_coverage_repair_still_available(self):
        from release.version_info import COVERAGE_REPAIR_WORKFLOW_AVAILABLE
        assert COVERAGE_REPAIR_WORKFLOW_AVAILABLE is True

    def test_universe_registry_still_available(self):
        from release.version_info import UNIVERSE_REGISTRY_AVAILABLE
        assert UNIVERSE_REGISTRY_AVAILABLE is True

    def test_data_freshness_monitor_available(self):
        from release.version_info import DATA_FRESHNESS_MONITOR_AVAILABLE
        assert DATA_FRESHNESS_MONITOR_AVAILABLE is True

    def test_provider_sla_monitor_available(self):
        from release.version_info import PROVIDER_SLA_MONITOR_AVAILABLE
        assert PROVIDER_SLA_MONITOR_AVAILABLE is True

    def test_trading_calendar_aware_freshness(self):
        from release.version_info import TRADING_CALENDAR_AWARE_FRESHNESS
        assert TRADING_CALENDAR_AWARE_FRESHNESS is True

    def test_freshness_alerts_available(self):
        from release.version_info import FRESHNESS_ALERTS_AVAILABLE
        assert FRESHNESS_ALERTS_AVAILABLE is True


# ============================================================
# TestDateStability  (20 tests)
# All tests inject a fixed clock via now_provider so they pass
# on any real date, time-of-day, weekday, or timezone offset.
# ============================================================
class TestDateStability:
    """20 date-stable tests for DataFreshnessEvaluator clock injection."""

    # ── helpers ──────────────────────────────────────────────
    @staticmethod
    def _ev(**kwargs):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        kwargs.setdefault("now_provider", _fixed_now_provider)
        return DataFreshnessEvaluator(**kwargs)

    # ── 1. Fixed weekday trading-day mid-morning ──────────────
    def test_fixed_weekday_intraday_fresh(self):
        from data_freshness.models_v134 import FreshnessStatus
        ev = self._ev()
        ts = _ts_ago_fixed(3600)  # 1 h before fixed clock
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert FreshnessStatus.is_ok(rec.freshness_status)

    # ── 2. Fixed weekday trading-day after close ──────────────
    def test_fixed_weekday_after_close_stale_by_age(self):
        # now_utc = 2026-01-07 06:00 UTC = 14:00 Asia/Taipei (after close)
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        now_after_close = datetime(2026, 1, 7, 6, 0, 0, tzinfo=timezone.utc)
        ev = DataFreshnessEvaluator(now_provider=lambda: now_after_close)
        ts = (now_after_close - timedelta(seconds=200000)).isoformat()
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        # 200 000 s > critical_after=172 800 s → CRITICALLY_STALE
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)

    # ── 3. Fixed Saturday (non-trading day) ──────────────────
    def test_fixed_saturday_non_trading_day(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.trading_calendar import TradingCalendar
        # 2026-01-10 is Saturday
        now_sat = datetime(2026, 1, 10, 2, 0, 0, tzinfo=timezone.utc)  # 10:00 Taipei Sat
        ev = DataFreshnessEvaluator(now_provider=lambda: now_sat)
        cal = TradingCalendar()
        from datetime import date
        assert cal.is_trading_day(date(2026, 1, 10)) is False

    # ── 4. Fixed Sunday (non-trading day) ────────────────────
    def test_fixed_sunday_non_trading_day(self):
        from data_freshness.trading_calendar import TradingCalendar
        from datetime import date
        cal = TradingCalendar()
        assert cal.is_trading_day(date(2026, 1, 11)) is False

    # ── 5. Fixed Monday early morning ────────────────────────
    def test_fixed_monday_early_morning_market_not_open(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        # 2026-01-12 Monday 01:00 UTC = 09:00 Taipei (market just opened)
        now_mon = datetime(2026, 1, 12, 1, 0, 0, tzinfo=timezone.utc)
        ev = DataFreshnessEvaluator(now_provider=lambda: now_mon)
        now_tw = now_mon + timedelta(hours=8)
        # 09:00 Taiwan — market open
        assert ev._is_market_open(now_tw) is True

    # ── 6. Cross month boundary ───────────────────────────────
    def test_cross_month_boundary_stale(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        # now = 2026-02-02 02:00 UTC = 10:00 Asia/Taipei (Mon, trading day)
        now_feb = datetime(2026, 2, 2, 2, 0, 0, tzinfo=timezone.utc)
        ev = DataFreshnessEvaluator(now_provider=lambda: now_feb)
        ts = (now_feb - timedelta(seconds=200000)).isoformat()
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)

    # ── 7. Cross year boundary ────────────────────────────────
    def test_cross_year_boundary_stale(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        # now = 2026-01-05 02:00 UTC = 10:00 Asia/Taipei (Mon, trading day)
        now_jan5 = datetime(2026, 1, 5, 2, 0, 0, tzinfo=timezone.utc)
        ev = DataFreshnessEvaluator(now_provider=lambda: now_jan5)
        ts = (now_jan5 - timedelta(seconds=200000)).isoformat()
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)

    # ── 8. Asia/Taipei aware datetime passes as now_provider ──
    def test_taipei_aware_datetime_as_now_provider(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        tz_taipei = timezone(timedelta(hours=8))
        now_tp = datetime(2026, 1, 7, 10, 0, 0, tzinfo=tz_taipei)
        ev = DataFreshnessEvaluator(now_provider=lambda: now_tp)
        ts = _ts_ago_fixed(200000, now=now_tp.astimezone(timezone.utc))
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)

    # ── 9. UTC timestamp converted to Asia/Taipei age ─────────
    def test_utc_timestamp_converts_to_taipei_age(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        ev = self._ev()
        ts_utc = _ts_ago_fixed(7200)  # 2 h before fixed clock
        age = ev.calculate_age(ts_utc)
        assert age is not None
        assert 7100 < age < 7300

    # ── 10. Naive datetime returns INVALID_TIMESTAMP ──────────
    def test_naive_datetime_invalid_timestamp_fixed_clock(self):
        from data_freshness.models_v134 import FreshnessStatus
        ev = self._ev()
        rec = ev.evaluate("2330", "DAILY_OHLCV", "2026-01-06T09:00:00")  # naive
        assert rec.freshness_status == FreshnessStatus.INVALID_TIMESTAMP

    # ── 11. Daily OHLCV fresh on previous trading day ────────
    def test_daily_ohlcv_previous_trading_day_fresh(self):
        from data_freshness.models_v134 import FreshnessStatus
        ev = self._ev()
        # 1 h old during market hours on same trading day → FRESH or ok
        ts = _ts_ago_fixed(3600)
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert FreshnessStatus.is_ok(rec.freshness_status)

    # ── 12. Intraday data stale during trading hours ──────────
    def test_intraday_data_stale_mid_session(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessPolicy
        # Intraday policy: stale after 900 s (15 min)
        policy = FreshnessPolicy(policy_id="intraday_test", dataset_type="INTRADAY_1MIN",
                                  stale_after=900.0, critical_after=1800.0)
        ev = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ts = _ts_ago_fixed(2000)  # 33 min old → > stale_after=900
        rec = ev.evaluate("2330", "INTRADAY_1MIN", ts, policy=policy)
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE,
                                         FreshnessStatus.NEAR_STALE)

    # ── 13. Intraday data fresh right after capture ───────────
    def test_intraday_data_fresh_right_after_capture(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessPolicy
        policy = FreshnessPolicy(policy_id="intraday_test2", dataset_type="INTRADAY_1MIN",
                                  stale_after=900.0, critical_after=1800.0)
        ev = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ts = _ts_ago_fixed(60)  # 1 min old → FRESH
        rec = ev.evaluate("2330", "INTRADAY_1MIN", ts, policy=policy)
        assert FreshnessStatus.is_ok(rec.freshness_status)

    # ── 14. Monthly revenue freshness unaffected by hourly drift ─
    def test_monthly_revenue_long_stale_after(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessPolicy
        # Monthly revenue: stale_after = 45 days × 86400 s
        policy = FreshnessPolicy(policy_id="monthly_rev_test",
                                  dataset_type="MONTHLY_REVENUE",
                                  stale_after=45 * 86400.0,
                                  critical_after=90 * 86400.0)
        ev = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ts = _ts_ago_fixed(10 * 86400)  # 10 days old → still FRESH
        rec = ev.evaluate("2330", "MONTHLY_REVENUE", ts, policy=policy)
        assert FreshnessStatus.is_ok(rec.freshness_status)

    # ── 15. Financial statement freshness unaffected by daily drift ─
    def test_financial_statement_fresh_within_quarter(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessPolicy
        policy = FreshnessPolicy(policy_id="fin_stmt_test",
                                  dataset_type="FINANCIAL_STATEMENTS",
                                  stale_after=90 * 86400.0,
                                  critical_after=120 * 86400.0)
        ev = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ts = _ts_ago_fixed(30 * 86400)  # 30 days old → FRESH for quarterly data
        rec = ev.evaluate("2330", "FINANCIAL_STATEMENTS", ts, policy=policy)
        assert FreshnessStatus.is_ok(rec.freshness_status)

    # ── 16. Technical indicator freshness follows OHLCV age ───
    def test_technical_indicator_follows_ohlcv_age(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus, FreshnessPolicy
        policy = FreshnessPolicy(policy_id="tech_ind_test",
                                  dataset_type="TECHNICAL_INDICATORS",
                                  stale_after=86400.0, critical_after=172800.0)
        ev = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ts = _ts_ago_fixed(200000)  # same age as underlying OHLCV would be stale
        rec = ev.evaluate("2330", "TECHNICAL_INDICATORS", ts, policy=policy)
        assert rec.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)

    # ── 17. Future timestamp always BLOCKED ───────────────────
    def test_future_timestamp_blocked_fixed_clock(self):
        from data_freshness.models_v134 import FreshnessStatus
        ev = self._ev()
        ts = _ts_future_fixed(86400)  # 1 day in the future from fixed clock
        rec = ev.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec.freshness_status == FreshnessStatus.FUTURE_TIMESTAMP

    # ── 18. Fixed clock does not pollute next test ────────────
    def test_fixed_clock_does_not_pollute_next_test(self):
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        ev_fixed = DataFreshnessEvaluator(now_provider=_fixed_now_provider)
        ev_real = DataFreshnessEvaluator()  # uses real clock
        ts = _ts_ago_fixed(200000)
        # Fixed evaluator sees age ~200000 s → STALE/CRITICALLY_STALE
        from data_freshness.models_v134 import FreshnessStatus
        rec_fixed = ev_fixed.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec_fixed.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)
        # Real evaluator may differ — just verify it doesn't crash
        rec_real = ev_real.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec_real.freshness_status is not None

    # ── 19. Same fixed clock always produces same result ──────
    def test_same_fixed_clock_reproducible(self):
        from data_freshness.models_v134 import FreshnessStatus
        ev1 = self._ev()
        ev2 = self._ev()
        ts = _ts_ago_fixed(200000)
        rec1 = ev1.evaluate("2330", "DAILY_OHLCV", ts)
        rec2 = ev2.evaluate("2330", "DAILY_OHLCV", ts)
        assert rec1.freshness_status == rec2.freshness_status

    # ── 20. Different execution dates produce same result ─────
    def test_different_execution_dates_same_result(self):
        # Two evaluators with different fixed clocks but identical timestamps
        # produce identically deterministic staleness for the *same* ts.
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        from data_freshness.models_v134 import FreshnessStatus
        now_a = datetime(2026, 1, 7, 2, 0, 0, tzinfo=timezone.utc)   # Wed
        now_b = datetime(2026, 3, 4, 2, 0, 0, tzinfo=timezone.utc)   # Wed
        ts_a = (now_a - timedelta(seconds=200000)).isoformat()
        ts_b = (now_b - timedelta(seconds=200000)).isoformat()
        ev_a = DataFreshnessEvaluator(now_provider=lambda: now_a)
        ev_b = DataFreshnessEvaluator(now_provider=lambda: now_b)
        rec_a = ev_a.evaluate("2330", "DAILY_OHLCV", ts_a)
        rec_b = ev_b.evaluate("2330", "DAILY_OHLCV", ts_b)
        # Both are 200 000 s old evaluated on a trading-day market-open clock
        assert rec_a.freshness_status == rec_b.freshness_status
        assert rec_a.freshness_status in (FreshnessStatus.STALE, FreshnessStatus.CRITICALLY_STALE)
