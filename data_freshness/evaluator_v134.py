"""data_freshness/evaluator_v134.py — v1.3.4 Data Freshness Evaluator.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Future timestamp never counts as FRESH.
[!] Naive datetimes flagged as INVALID_TIMESTAMP.
[!] Mock/demo data flagged as DEMO_ONLY.
[!] No auto-refresh, no auto-repair, no mock fallback.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple

from data_freshness.models_v134 import (
    FreshnessRecord, FreshnessPolicy, FreshnessSeverity, FreshnessStatus,
    DatasetType, DailyFreshnessSummary,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FRESHNESS_AUTO_REFRESH_ENABLED = False
FRESHNESS_AUTO_REPAIR_ENABLED = False
FRESHNESS_MOCK_FALLBACK_ENABLED = False

_FUTURE_GRACE_SECONDS = 300.0  # 5 min grace for clock skew


def _parse_iso(ts_str: str) -> Optional[datetime]:
    """Parse ISO 8601 string to UTC-aware datetime. Returns None on failure."""
    if not ts_str:
        return None
    try:
        # Python 3.7+ fromisoformat handles Z suffix only in 3.11+
        ts_str_clean = ts_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts_str_clean)
        if dt.tzinfo is None:
            return None  # naive datetime — caller must handle
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class DataFreshnessEvaluator:
    """Evaluate data freshness for a symbol/dataset combination.

    [!] Research Only. Does not trigger refresh, repair, or download.
    [!] Future timestamps are never FRESH.
    [!] Naive timestamps produce INVALID_TIMESTAMP.
    [!] Mock/fixture data produces DEMO_ONLY.
    """

    def __init__(
        self,
        policy_registry=None,
        calendar=None,
        now_provider: Optional[Callable[[], datetime]] = None,
    ) -> None:
        self._policy_registry = policy_registry
        self._calendar = calendar
        self._now_provider = now_provider

    def _now_utc(self) -> datetime:
        """Return current UTC time. Uses injected now_provider in tests; real clock in production."""
        if self._now_provider is not None:
            dt = self._now_provider()
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        return _now_utc()

    def _get_policy(self, dataset_type: str, policy: Optional[FreshnessPolicy]) -> FreshnessPolicy:
        if policy is not None:
            return policy
        if self._policy_registry is not None:
            return self._policy_registry.get_policy(dataset_type)
        # Fallback: create default policy
        return FreshnessPolicy(
            policy_id=f"fallback_{dataset_type}",
            dataset_type=dataset_type,
        )

    def _get_calendar(self, calendar=None):
        if calendar is not None:
            return calendar
        if self._calendar is not None:
            return self._calendar
        from data_freshness.trading_calendar import TradingCalendar
        return TradingCalendar()

    def calculate_age(self, ts_str: str) -> Optional[float]:
        """Calculate age in seconds from ts_str to now (UTC). None on error."""
        dt = _parse_iso(ts_str)
        if dt is None:
            return None
        now = self._now_utc()
        delta = now - dt
        return delta.total_seconds()

    def calculate_trading_day_age(self, ts_str: str, calendar) -> Optional[float]:
        """Calculate age in trading days. None on error."""
        dt = _parse_iso(ts_str)
        if dt is None:
            return None
        ts_date = dt.astimezone(timezone(timedelta(hours=8))).date()
        today = self._now_utc().astimezone(timezone(timedelta(hours=8))).date()
        return float(calendar.trading_days_between(ts_date, today))

    def expected_latest_timestamp(
        self, dataset_type: str, calendar, as_of: Optional[datetime] = None
    ) -> Optional[str]:
        """Return expected latest timestamp string for the dataset_type."""
        try:
            now = as_of or self._now_utc()
            ltd = calendar.expected_latest_trading_day(now)
            # Return end-of-day UTC for trading-sensitive types
            from datetime import date
            dt_eod = datetime(ltd.year, ltd.month, ltd.day, 6, 0, 0, tzinfo=timezone.utc)  # ~14:00 Taiwan
            return dt_eod.isoformat()
        except Exception as exc:
            logger.debug("expected_latest_timestamp failed: %s", exc)
            return None

    def determine_status(
        self,
        age_seconds: Optional[float],
        policy: FreshnessPolicy,
        calendar,
        data_mode: str = "REAL",
        ts_str: Optional[str] = None,
    ) -> str:
        """Determine FreshnessStatus string from age and policy."""
        # DEMO_ONLY
        if data_mode in ("MOCK", "FIXTURE", "DEMO", "DEMO_ONLY", "TEST_FIXTURE"):
            return FreshnessStatus.DEMO_ONLY

        # Missing
        if age_seconds is None:
            return FreshnessStatus.NEVER_RECEIVED

        # Future timestamp (age < -grace)
        if age_seconds < -_FUTURE_GRACE_SECONDS:
            return FreshnessStatus.FUTURE_TIMESTAMP

        # Non-trading day valid: if policy allows and day is non-trading
        try:
            now_tw = self._now_utc() + timedelta(hours=8)
            today = now_tw.date()
            is_trading = calendar.is_trading_day(today)
            if not is_trading:
                # Allow non-trading-day delay
                if age_seconds <= policy.allowed_non_trading_day_delay:
                    return FreshnessStatus.NON_TRADING_DAY_VALID

            # Market closed valid: trading day but market not yet open
            if is_trading and not self._is_market_open(now_tw):
                # If we have yesterday's data (age < 86400 + close grace)
                if age_seconds <= (policy.allowed_market_close_delay + 86400):
                    return FreshnessStatus.MARKET_CLOSED_VALID
        except Exception:
            pass

        # Freshness by age thresholds
        near_stale_after = policy.stale_after * policy.near_stale_ratio
        if age_seconds <= near_stale_after:
            return FreshnessStatus.FRESH
        if age_seconds <= policy.stale_after:
            return FreshnessStatus.NEAR_STALE
        if age_seconds <= policy.critical_after:
            return FreshnessStatus.STALE
        return FreshnessStatus.CRITICALLY_STALE

    def _is_market_open(self, taiwan_now) -> bool:
        """Approximate: market open 9:00-13:30 Taiwan time."""
        hour = taiwan_now.hour
        minute = taiwan_now.minute
        if hour < 9:
            return False
        if hour > 13:
            return False
        if hour == 13 and minute > 30:
            return False
        return True

    def determine_severity(self, status: str) -> str:
        """Map FreshnessStatus to FreshnessSeverity."""
        if status in (FreshnessStatus.FRESH, FreshnessStatus.MARKET_CLOSED_VALID,
                      FreshnessStatus.NON_TRADING_DAY_VALID):
            return FreshnessSeverity.INFO
        if status in (FreshnessStatus.NEAR_STALE, FreshnessStatus.PROVIDER_DELAYED,
                      FreshnessStatus.DEMO_ONLY, FreshnessStatus.UNKNOWN):
            return FreshnessSeverity.WARNING
        if status in (FreshnessStatus.STALE, FreshnessStatus.PROVIDER_UNAVAILABLE):
            return FreshnessSeverity.ERROR
        if status in (FreshnessStatus.CRITICALLY_STALE, FreshnessStatus.NEVER_RECEIVED,
                      FreshnessStatus.FUTURE_TIMESTAMP, FreshnessStatus.INVALID_TIMESTAMP,
                      FreshnessStatus.BLOCKED):
            return FreshnessSeverity.CRITICAL
        return FreshnessSeverity.WARNING

    def determine_blocking_profiles(
        self,
        status: str,
        dataset_type: str,
        policy: FreshnessPolicy,
    ) -> List[str]:
        """Return list of profiles blocked by this freshness status."""
        blocked: List[str] = []
        profiles = policy.blocking_profiles

        if "precise_price" in profiles:
            # Precise price blocked if NEAR_STALE or worse
            if status not in (FreshnessStatus.FRESH, FreshnessStatus.MARKET_CLOSED_VALID,
                               FreshnessStatus.NON_TRADING_DAY_VALID):
                blocked.append("precise_price")

        if "backtest" in profiles:
            if FreshnessStatus.is_stale(status) or FreshnessStatus.is_blocking(status):
                blocked.append("backtest")
            # CORPORATE_ACTIONS unknown -> blocks backtest
            if dataset_type == DatasetType.CORPORATE_ACTIONS and status == FreshnessStatus.UNKNOWN:
                if "backtest" not in blocked:
                    blocked.append("backtest")

        if "abc" in profiles:
            if FreshnessStatus.is_stale(status) or FreshnessStatus.is_blocking(status):
                blocked.append("abc")

        return blocked

    def evaluate(
        self,
        symbol: str,
        dataset_type: str,
        observed_ts: Optional[str],
        source_ts: Optional[str] = None,
        fetched_at: Optional[str] = None,
        provider_id: Optional[str] = None,
        data_mode: str = "REAL",
        policy: Optional[FreshnessPolicy] = None,
        calendar=None,
        market: str = "TWSE",
    ) -> FreshnessRecord:
        """Evaluate freshness for a symbol/dataset and return FreshnessRecord."""
        resolved_policy = self._get_policy(dataset_type, policy)
        cal = self._get_calendar(calendar)

        # Use source_timestamp preferentially; fetched_at only if that's all we have
        eval_ts = source_ts or observed_ts

        # Check for invalid (naive) timestamp
        invalid_ts = False
        if eval_ts:
            ts_clean = eval_ts.replace("Z", "+00:00")
            try:
                dt = datetime.fromisoformat(ts_clean)
                if dt.tzinfo is None:
                    invalid_ts = True
            except (ValueError, TypeError):
                invalid_ts = True

        if invalid_ts:
            status = FreshnessStatus.INVALID_TIMESTAMP
            severity = FreshnessSeverity.CRITICAL
            age_seconds = None
            reasons = [f"Naive or unparseable timestamp: {eval_ts!r}"]
        elif not eval_ts:
            status = FreshnessStatus.NEVER_RECEIVED
            severity = FreshnessSeverity.CRITICAL
            age_seconds = None
            reasons = ["No timestamp available"]
        else:
            age_seconds = self.calculate_age(eval_ts)
            status = self.determine_status(age_seconds, resolved_policy, cal, data_mode, eval_ts)
            severity = self.determine_severity(status)
            reasons = self._build_reasons(status, age_seconds, resolved_policy, dataset_type)

        blocked_profiles = self.determine_blocking_profiles(status, dataset_type, resolved_policy)

        # Compute market/trading context
        now_tw = self._now_utc() + timedelta(hours=8)
        today = now_tw.date()
        try:
            is_trading = cal.is_trading_day(today)
            market_open = is_trading and self._is_market_open(now_tw)
        except Exception:
            is_trading = False
            market_open = False

        try:
            prev_td = str(cal.previous_trading_day(today))
        except Exception:
            prev_td = None

        try:
            age_td = self.calculate_trading_day_age(eval_ts, cal) if eval_ts and not invalid_ts else None
        except Exception:
            age_td = None

        expected_ts = self.expected_latest_timestamp(dataset_type, cal)
        near_stale_after = resolved_policy.stale_after * resolved_policy.near_stale_ratio

        record = FreshnessRecord(
            record_id=str(uuid.uuid4()),
            symbol=symbol,
            market=market,
            dataset_type=dataset_type,
            provider_id=provider_id,
            data_mode=data_mode,
            observed_timestamp=observed_ts,
            source_timestamp=source_ts,
            fetched_at=fetched_at,
            expected_latest_timestamp=expected_ts,
            age_seconds=age_seconds,
            age_trading_days=age_td,
            freshness_status=status,
            severity=severity,
            policy_id=resolved_policy.policy_id,
            stale_after_seconds=resolved_policy.stale_after,
            critical_after_seconds=resolved_policy.critical_after,
            near_stale_threshold_seconds=near_stale_after,
            market_open=market_open,
            trading_day=is_trading,
            previous_trading_day=prev_td,
            blocks_analysis=bool(blocked_profiles),
            precise_price_allowed="precise_price" not in blocked_profiles,
            backtest_allowed="backtest" not in blocked_profiles,
            abc_buy_point_allowed="abc" not in blocked_profiles,
            reasons=reasons,
        )
        return record

    def _build_reasons(
        self,
        status: str,
        age_seconds: Optional[float],
        policy: FreshnessPolicy,
        dataset_type: str,
    ) -> List[str]:
        reasons: List[str] = []
        if age_seconds is not None:
            age_h = age_seconds / 3600
            reasons.append(f"age={age_h:.1f}h stale_after={policy.stale_after/3600:.1f}h")
        if status == FreshnessStatus.DEMO_ONLY:
            reasons.append("Data mode is MOCK/DEMO — not real data")
        if status == FreshnessStatus.FUTURE_TIMESTAMP:
            reasons.append("Timestamp is in the future — never counts as FRESH")
        if status == FreshnessStatus.CRITICALLY_STALE:
            reasons.append(f"Age exceeds critical_after={policy.critical_after/3600:.0f}h")
        if status == FreshnessStatus.STALE:
            reasons.append(f"Age exceeds stale_after={policy.stale_after/3600:.0f}h")
        return reasons

    def evaluate_timestamp(
        self,
        ts_str: str,
        dataset_type: str,
        policy: Optional[FreshnessPolicy] = None,
        calendar=None,
    ) -> Tuple[str, str, List[str]]:
        """Quick evaluation returning (status, severity, reasons)."""
        rec = self.evaluate(
            symbol="",
            dataset_type=dataset_type,
            observed_ts=ts_str,
            policy=policy,
            calendar=calendar,
        )
        return rec.freshness_status, rec.severity, rec.reasons

    def evaluate_dataset(
        self,
        record_dict: Dict[str, Any],
        dataset_type: str,
        policy: Optional[FreshnessPolicy] = None,
    ) -> FreshnessRecord:
        """Evaluate freshness from a raw record dict."""
        return self.evaluate(
            symbol=record_dict.get("symbol", ""),
            dataset_type=dataset_type,
            observed_ts=record_dict.get("observed_timestamp") or record_dict.get("source_timestamp"),
            source_ts=record_dict.get("source_timestamp"),
            fetched_at=record_dict.get("fetched_at"),
            provider_id=record_dict.get("provider_id"),
            data_mode=record_dict.get("data_mode", "REAL"),
            policy=policy,
        )

    def evaluate_provider_response(
        self,
        response: Dict[str, Any],
        symbol: str,
        dataset_type: str,
    ) -> FreshnessRecord:
        """Evaluate freshness from a provider response dict."""
        return self.evaluate(
            symbol=symbol,
            dataset_type=dataset_type,
            observed_ts=response.get("source_timestamp") or response.get("timestamp"),
            source_ts=response.get("source_timestamp"),
            fetched_at=response.get("fetched_at"),
            provider_id=response.get("provider_id"),
            data_mode=response.get("data_mode", "REAL"),
        )

    def evaluate_cache_entry(
        self,
        entry: Dict[str, Any],
        dataset_type: str,
    ) -> FreshnessRecord:
        """Evaluate freshness of a cache entry."""
        return self.evaluate(
            symbol=entry.get("symbol", ""),
            dataset_type=dataset_type,
            observed_ts=entry.get("source_timestamp") or entry.get("cached_at"),
            source_ts=entry.get("source_timestamp"),
            fetched_at=entry.get("cached_at"),
            provider_id=entry.get("provider_id"),
            data_mode=entry.get("data_mode", "REAL"),
        )

    def build_record(
        self,
        symbol: str,
        dataset_type: str,
        observed_ts: Optional[str],
        **kwargs: Any,
    ) -> FreshnessRecord:
        """Build a FreshnessRecord with explicit parameters."""
        return self.evaluate(
            symbol=symbol,
            dataset_type=dataset_type,
            observed_ts=observed_ts,
            **kwargs,
        )
