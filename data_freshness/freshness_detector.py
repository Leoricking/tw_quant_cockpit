"""
data_freshness/freshness_detector.py — Data Freshness Detector for v1.1.3.
[!] Research Only. No Real Orders.
[!] Future date does NOT count as fresh.
[!] Mock data not used for formal freshness conclusions.
[!] No automatic data download. No broker connection. No trading.
[!] File mtime is NOT used as a proxy for data freshness.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from data_freshness.freshness_schema import (
    DATASET_DAILY_PRICE, DATASET_VOLUME, DATASET_CHIPS,
    DATASET_REVENUE, DATASET_FUNDAMENTALS, DATASET_MARGIN,
    DATASET_SHORT_INTEREST, DATASET_CORPORATE_ACTION, DATASET_UNKNOWN,
    SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_INFO, SEVERITY_LOW, SEVERITY_MEDIUM,
    STATUS_FRESH, STATUS_ACCEPTABLE, STATUS_DELAYED, STATUS_STALE,
    STATUS_INTERRUPTED, STATUS_MISSING, STATUS_FUTURE_DATE,
    STATUS_DATE_REGRESSION, STATUS_UNKNOWN,
    DatasetFreshnessRecord,
)
from data_freshness.trading_calendar import TradingCalendar
from data_freshness.freshness_policy import FreshnessPolicy

logger = logging.getLogger(__name__)

# Safety invariants
NO_REAL_ORDERS                     = True
RESEARCH_ONLY                      = True
BROKER_DISABLED                    = True
AUTO_EXTERNAL_REFRESH_ENABLED      = False
STALE_DATA_AUTO_REPAIR_ENABLED     = False
FUTURE_DATE_COUNTS_AS_FRESH        = False
MOCK_DATA_FORMAL_FRESHNESS_ALLOWED = False

# Dataset → typical CSV filename patterns (relative to repo_path/data/)
_DATASET_CSV_PATHS: Dict[str, List[str]] = {
    DATASET_DAILY_PRICE: [
        "daily_k/daily_k.csv",
        "daily_k/{symbol}.csv",
        "raw/{symbol}_daily.csv",
        "price/{symbol}.csv",
    ],
    DATASET_VOLUME: [
        "daily_k/daily_k.csv",
        "daily_k/{symbol}.csv",
        "raw/{symbol}_daily.csv",
    ],
    DATASET_CHIPS: [
        "chips/{symbol}.csv",
        "chips/chips.csv",
        "raw/{symbol}_chips.csv",
    ],
    DATASET_MARGIN: [
        "margin/{symbol}.csv",
        "margin/margin.csv",
        "raw/{symbol}_margin.csv",
    ],
    DATASET_SHORT_INTEREST: [
        "short_interest/{symbol}.csv",
        "raw/{symbol}_short.csv",
    ],
    DATASET_REVENUE: [
        "revenue/{symbol}.csv",
        "fundamentals/{symbol}_revenue.csv",
    ],
    DATASET_FUNDAMENTALS: [
        "fundamentals/{symbol}.csv",
        "fundamentals/{symbol}_fundamentals.csv",
    ],
    DATASET_CORPORATE_ACTION: [
        "corporate_actions/{symbol}.csv",
        "dividends/{symbol}.csv",
    ],
}

# Date column names to try, in priority order
_DATE_COLUMNS = ["date", "Date", "DATE", "trade_date", "TradeDate", "trading_date"]


def _auto_repo_path() -> str:
    """Infer repo root from this file's location (data_freshness/ is one level deep)."""
    here = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(here))


def _parse_date_safe(val: Any) -> Optional[date]:
    """Try to parse a date value; return None on failure."""
    if val is None or val == "" or val != val:  # NaN check
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    s = str(val).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s[:10], fmt).date()
        except (ValueError, TypeError):
            continue
    return None


class DataFreshnessDetector:
    """
    Detects data freshness for symbols/datasets by reading CSV files.

    [!] Does NOT download data, connect to brokers, or trigger repairs.
    [!] File mtime is NOT used — only actual date values in data.
    [!] Future dates are flagged and NOT treated as fresh.
    [!] Mock sources are labelled source='mock' and excluded from confidence.
    """

    def __init__(
        self,
        calendar: Optional[TradingCalendar] = None,
        policy: Optional[FreshnessPolicy] = None,
        repo_path: Optional[str] = None,
        as_of: Optional[datetime] = None,
    ):
        self.calendar: TradingCalendar = calendar or TradingCalendar()
        self.policy: FreshnessPolicy = policy or FreshnessPolicy()
        self.repo_path: str = repo_path or _auto_repo_path()
        self._as_of: Optional[datetime] = as_of
        self._history_cache: Dict[str, Dict[str, Optional[date]]] = {}

    def _now(self) -> datetime:
        return self._as_of if self._as_of is not None else datetime.now(timezone.utc)

    def _data_dir(self) -> str:
        return os.path.join(self.repo_path, "data")

    # ------------------------------------------------------------------
    # Tier / symbol resolution
    # ------------------------------------------------------------------

    def _get_tier_for_symbol(self, symbol: str) -> str:
        """Try to resolve tier from universe package; fall back to UNKNOWN."""
        try:
            from universe import get_symbol_tier  # type: ignore
            return get_symbol_tier(symbol) or "unknown"
        except Exception:
            pass
        try:
            from universe.universe_manager import get_symbol_tier  # type: ignore
            return get_symbol_tier(symbol) or "unknown"
        except Exception:
            return "unknown"

    def _get_symbols_for_tier(self, tier: str) -> List[str]:
        """Try to resolve symbols for a tier from universe package."""
        try:
            from universe import get_tier_symbols  # type: ignore
            result = get_tier_symbols(tier)
            if result:
                return list(result)
        except Exception:
            pass
        try:
            from universe.universe_manager import get_tier_symbols  # type: ignore
            result = get_tier_symbols(tier)
            if result:
                return list(result)
        except Exception:
            pass
        logger.warning(
            "Could not resolve symbols for tier=%s via universe package", tier
        )
        return []

    # ------------------------------------------------------------------
    # CSV reading
    # ------------------------------------------------------------------

    def _find_csv_for_dataset(self, symbol: str, dataset: str) -> Optional[str]:
        """Return path to first existing CSV file for (symbol, dataset)."""
        patterns = _DATASET_CSV_PATHS.get(dataset, [])
        data_dir = self._data_dir()
        for pattern in patterns:
            path = os.path.join(data_dir, pattern.format(symbol=symbol))
            if os.path.isfile(path):
                return path
        return None

    def _read_latest_date_from_csv(
        self, csv_path: str, symbol: Optional[str] = None
    ) -> tuple[Optional[date], int]:
        """
        Read a CSV and return (latest_date, row_count).
        [!] Does NOT use file mtime.
        [!] Filters out future dates.
        Returns (None, 0) on error or if no valid dates found.
        """
        now_date = self._now().date()
        try:
            # Try pandas first
            try:
                import pandas as pd  # type: ignore

                df = pd.read_csv(csv_path, low_memory=False)
                if symbol and "symbol" in df.columns:
                    mask = df["symbol"].astype(str).str.strip().str.upper() == symbol.upper()
                    df = df[mask]

                date_col = None
                for col in _DATE_COLUMNS:
                    if col in df.columns:
                        date_col = col
                        break

                if date_col is None:
                    logger.warning(
                        "No date column found in %s (tried %s)", csv_path, _DATE_COLUMNS
                    )
                    return None, len(df)

                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                df = df.dropna(subset=[date_col])
                valid_dates = df[date_col].dt.date
                # Exclude future dates from freshness consideration
                valid_dates = valid_dates[valid_dates <= now_date]
                if valid_dates.empty:
                    return None, len(df)
                return valid_dates.max(), len(df)

            except ImportError:
                pass

            # Fallback: csv module
            with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    return None, 0

                date_col = None
                for col in _DATE_COLUMNS:
                    if col in (reader.fieldnames or []):
                        date_col = col
                        break

                if date_col is None:
                    logger.warning(
                        "No date column found in %s (tried %s)", csv_path, _DATE_COLUMNS
                    )
                    return None, 0

                rows = list(reader)
                row_count = len(rows)
                if symbol:
                    symbol_col = None
                    for c in ("symbol", "Symbol", "SYMBOL", "code", "Code"):
                        if c in (reader.fieldnames or []):
                            symbol_col = c
                            break
                    if symbol_col:
                        rows = [r for r in rows if r.get(symbol_col, "").strip().upper() == symbol.upper()]

                valid_dates: List[date] = []
                for row in rows:
                    d = _parse_date_safe(row.get(date_col, ""))
                    if d is not None and d <= now_date:
                        valid_dates.append(d)

                if not valid_dates:
                    return None, row_count
                return max(valid_dates), row_count

        except Exception as exc:
            logger.warning("Error reading CSV %s: %s", csv_path, exc)
            return None, 0

    # ------------------------------------------------------------------
    # Core detection helpers
    # ------------------------------------------------------------------

    def get_actual_latest_date(self, symbol: str, dataset: str) -> Optional[date]:
        """
        Read CSV data files and return the latest valid non-future date.
        Returns None if no data found.
        [!] Does NOT use file mtime.
        """
        csv_path = self._find_csv_for_dataset(symbol, dataset)
        if csv_path is None:
            return None
        latest, _ = self._read_latest_date_from_csv(csv_path, symbol)
        return latest

    def get_previous_latest_date(self, symbol: str, dataset: str) -> Optional[date]:
        """
        Read previous run's latest date from freshness history store, if available.
        Returns None if no history.
        """
        key = f"{symbol}::{dataset}"
        if key in self._history_cache:
            return self._history_cache[key]

        try:
            history_path = os.path.join(
                self.repo_path, "data", "freshness_reports", "freshness_history.csv"
            )
            if not os.path.isfile(history_path):
                return None

            best: Optional[date] = None
            best_ts: Optional[str] = None
            with open(history_path, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (
                        row.get("symbol", "") == symbol
                        and row.get("dataset", "") == dataset
                        and row.get("actual_latest_date", "")
                    ):
                        ts = row.get("detected_at", "")
                        if best_ts is None or ts > best_ts:
                            d = _parse_date_safe(row["actual_latest_date"])
                            if d is not None:
                                best = d
                                best_ts = ts
            self._history_cache[key] = best
            return best
        except Exception as exc:
            logger.warning(
                "Could not load previous date for %s/%s: %s", symbol, dataset, exc
            )
            return None

    def calculate_calendar_age(
        self, actual_date: Optional[date], as_of: Optional[datetime] = None
    ) -> Optional[int]:
        """Return calendar days between actual_date and as_of (or now)."""
        if actual_date is None:
            return None
        ref = (as_of or self._now()).date()
        return (ref - actual_date).days

    def calculate_trading_day_lag(
        self, actual_date: Optional[date], expected_date: date
    ) -> Optional[int]:
        """Use calendar.trading_day_lag to compute lag."""
        return self.calendar.trading_day_lag(actual_date, expected_date)

    def detect_future_date(
        self, actual_date: Optional[date], as_of: Optional[datetime] = None
    ) -> bool:
        """
        Return True if actual_date is strictly after today (as_of).
        [!] Future date must NOT be counted as fresh.
        """
        if actual_date is None:
            return False
        ref = (as_of or self._now()).date()
        return actual_date > ref

    def detect_date_regression(
        self, symbol: str, dataset: str, actual_date: Optional[date]
    ) -> bool:
        """Return True if actual_date < previous_latest_date (date went backwards)."""
        if actual_date is None:
            return False
        prev = self.get_previous_latest_date(symbol, dataset)
        if prev is None:
            return False
        return actual_date < prev

    def detect_partial_update(
        self, symbol: str, records: List[DatasetFreshnessRecord]
    ) -> bool:
        """
        Return True if daily price was updated but volume was not.
        Indicates a partial update scenario.
        """
        price_rec = next(
            (r for r in records if r.dataset == DATASET_DAILY_PRICE), None
        )
        vol_rec = next(
            (r for r in records if r.dataset == DATASET_VOLUME), None
        )
        if price_rec is None or vol_rec is None:
            return False
        price_fresh = price_rec.status in (STATUS_FRESH, STATUS_ACCEPTABLE)
        vol_stale = vol_rec.status in (STATUS_STALE, STATUS_DELAYED, STATUS_MISSING, STATUS_INTERRUPTED)
        return price_fresh and vol_stale

    def detect_coverage_not_refreshed(self, symbol: str) -> bool:
        """
        Check if last import succeeded but universe coverage was not refreshed.
        Returns False if coverage data is unavailable.
        """
        try:
            from data_coverage import CoverageStore  # type: ignore
            store = CoverageStore(repo_path=self.repo_path)
            record = store.get_latest_for_symbol(symbol)
            if record is None:
                return False
            imported = getattr(record, "imported", False)
            coverage_refreshed = getattr(record, "coverage_refreshed", True)
            return bool(imported and not coverage_refreshed)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Record building
    # ------------------------------------------------------------------

    def build_record(
        self,
        symbol: str,
        tier: str,
        dataset: str,
        source: str,
        actual_date: Optional[date] = None,
        previous_date: Optional[date] = None,
        expected_date: Optional[date] = None,
        row_count: int = 0,
        latest_row_valid: bool = True,
        status: Optional[str] = None,
        reason: str = "",
    ) -> DatasetFreshnessRecord:
        """Construct a DatasetFreshnessRecord, computing derived fields."""
        now = self._now()
        as_of_date = now.date()

        # Expected date
        if expected_date is None:
            expected_date = self.calendar.expected_latest_trading_day(now)

        # Future date detection
        future_detected = self.detect_future_date(actual_date, now)

        # Date regression detection
        regression_detected = self.detect_date_regression(symbol, dataset, actual_date)

        # Calendar age
        calendar_age = self.calculate_calendar_age(actual_date, now)

        # Trading day lag
        if actual_date is not None and not future_detected:
            td_lag = self.calculate_trading_day_lag(actual_date, expected_date)
        elif future_detected:
            td_lag = self.calculate_trading_day_lag(actual_date, expected_date)
        else:
            td_lag = None

        # Status classification
        if status is None:
            if actual_date is None:
                status = STATUS_MISSING
                if not reason:
                    reason = f"{dataset} data not found for {symbol}"
            elif future_detected:
                status = STATUS_FUTURE_DATE
                if not reason:
                    reason = f"{dataset} has future date {actual_date} — not counted as fresh"
            elif regression_detected:
                status = STATUS_DATE_REGRESSION
                if not reason:
                    reason = (
                        f"{dataset} date regressed: {actual_date} < previous {previous_date}"
                    )
            else:
                pol_policy = self.policy.get_policy(dataset)
                freq = pol_policy.get("freq", "unknown")
                if freq == "daily":
                    status = self.policy.classify(dataset, td_lag)
                elif freq in ("monthly", "quarterly", "event", "unknown"):
                    status = STATUS_UNKNOWN
                    if not reason:
                        reason = f"{dataset} freq={freq}: classification requires specialized method"
                else:
                    status = STATUS_UNKNOWN

        if not reason:
            reason = self.policy.explain_status(dataset, status, td_lag)

        severity = self.policy.severity_for(status)
        sla_policy = self.policy.get_policy(dataset)
        sla_limit = sla_policy.get("stale") or sla_policy.get("fresh_days")

        return DatasetFreshnessRecord(
            record_id=str(uuid4()),
            symbol=symbol,
            tier=tier,
            dataset=dataset,
            source=source,
            expected_latest_date=expected_date.isoformat() if expected_date else None,
            actual_latest_date=actual_date.isoformat() if actual_date else None,
            previous_latest_date=previous_date.isoformat() if previous_date else None,
            calendar_age_days=calendar_age,
            trading_day_lag=td_lag,
            row_count=row_count,
            latest_row_valid=latest_row_valid,
            future_date_detected=future_detected,
            date_regression_detected=regression_detected,
            status=status,
            severity=severity,
            sla_name=f"{dataset}_SLA",
            sla_limit=sla_limit,
            detected_at=now.isoformat(),
            reason=reason,
            research_only=True,
            no_real_orders=True,
        )

    # ------------------------------------------------------------------
    # Public detection API
    # ------------------------------------------------------------------

    def detect_dataset(self, symbol: str, dataset: str) -> DatasetFreshnessRecord:
        """Detect freshness for a single (symbol, dataset) pair."""
        try:
            tier = self._get_tier_for_symbol(symbol)
            source = "csv"

            csv_path = self._find_csv_for_dataset(symbol, dataset)
            if csv_path is None:
                return self.build_record(
                    symbol=symbol,
                    tier=tier,
                    dataset=dataset,
                    source=source,
                    actual_date=None,
                    row_count=0,
                    status=STATUS_MISSING,
                    reason=f"No CSV file found for {symbol}/{dataset}",
                )

            actual_date, row_count = self._read_latest_date_from_csv(csv_path, symbol)
            previous_date = self.get_previous_latest_date(symbol, dataset)

            return self.build_record(
                symbol=symbol,
                tier=tier,
                dataset=dataset,
                source=source,
                actual_date=actual_date,
                previous_date=previous_date,
                row_count=row_count,
            )
        except Exception as exc:
            logger.warning(
                "detect_dataset(%s, %s) failed: %s", symbol, dataset, exc
            )
            tier = "unknown"
            try:
                tier = self._get_tier_for_symbol(symbol)
            except Exception:
                pass
            return self.build_record(
                symbol=symbol,
                tier=tier,
                dataset=dataset,
                source="error",
                actual_date=None,
                row_count=0,
                status=STATUS_MISSING,
                reason=f"Exception during detection: {exc}",
            )

    def detect_symbol(self, symbol: str) -> List[DatasetFreshnessRecord]:
        """Detect freshness for DAILY_PRICE and VOLUME datasets for a symbol."""
        records: List[DatasetFreshnessRecord] = []
        for dataset in (DATASET_DAILY_PRICE, DATASET_VOLUME):
            records.append(self.detect_dataset(symbol, dataset))
        # Detect partial update
        _ = self.detect_partial_update(symbol, records)
        return records

    def detect_tier(self, tier: str) -> List[DatasetFreshnessRecord]:
        """Detect freshness for all symbols in a tier."""
        symbols = self._get_symbols_for_tier(tier)
        if not symbols:
            logger.warning("No symbols found for tier=%s", tier)
            return []
        all_records: List[DatasetFreshnessRecord] = []
        for symbol in symbols:
            try:
                records = self.detect_symbol(symbol)
                all_records.extend(records)
            except Exception as exc:
                logger.warning(
                    "detect_symbol(%s) in tier=%s failed: %s", symbol, tier, exc
                )
        return all_records
