"""data_freshness/scanner_v134.py — v1.3.4 Data Freshness Scanner.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No auto-refresh, no auto-repair, no mock fallback on scan failure.
[!] Single failure isolated — scan continues on individual symbol errors.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data_freshness.models_v134 import (
    FreshnessRecord, FreshnessSeverity, FreshnessStatus, DatasetType, DailyFreshnessSummary,
)
from data_freshness.evaluator_v134 import DataFreshnessEvaluator

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FRESHNESS_AUTO_REFRESH_ENABLED = False
FRESHNESS_AUTO_REPAIR_ENABLED = False
FRESHNESS_MOCK_FALLBACK_ENABLED = False

_MAX_SYMBOLS = 500  # safety limit

# Default dataset types to scan per symbol
_DEFAULT_DATASETS = [
    DatasetType.DAILY_OHLCV,
    DatasetType.INSTITUTIONAL,
    DatasetType.MARGIN,
    DatasetType.MONTHLY_REVENUE,
]


class DataFreshnessScanner:
    """Scan freshness status for symbols and datasets.

    [!] Research Only. No auto-refresh, no auto-repair, no mock fallback.
    [!] Single failure per symbol/dataset is isolated — scan continues.
    """

    def __init__(
        self,
        evaluator: Optional[DataFreshnessEvaluator] = None,
        policy_registry=None,
        calendar=None,
        max_symbols: int = _MAX_SYMBOLS,
    ) -> None:
        self._evaluator = evaluator or DataFreshnessEvaluator(
            policy_registry=policy_registry,
            calendar=calendar,
        )
        self._policy_registry = policy_registry
        self._calendar = calendar
        self._max_symbols = max_symbols

    def scan_symbol(
        self,
        symbol: str,
        market: str = "TWSE",
        datasets: Optional[List[str]] = None,
        policy_registry=None,
        calendar=None,
        data_store: Optional[Dict[str, Any]] = None,
    ) -> List[FreshnessRecord]:
        """Scan freshness for a single symbol across dataset types."""
        target_datasets = datasets or _DEFAULT_DATASETS
        records: List[FreshnessRecord] = []

        for dt in target_datasets:
            try:
                # Get last known timestamp from data_store or None
                ts_info = self._lookup_timestamp(symbol, dt, data_store)
                rec = self._evaluator.evaluate(
                    symbol=symbol,
                    dataset_type=dt,
                    observed_ts=ts_info.get("observed_timestamp"),
                    source_ts=ts_info.get("source_timestamp"),
                    fetched_at=ts_info.get("fetched_at"),
                    provider_id=ts_info.get("provider_id"),
                    data_mode=ts_info.get("data_mode", "REAL"),
                    market=market,
                )
                records.append(rec)
            except Exception as exc:
                logger.warning("scan_symbol: error scanning %s/%s: %s", symbol, dt, exc)
                # Create an UNKNOWN record for this dataset — don't abort entire scan
                records.append(FreshnessRecord(
                    symbol=symbol,
                    market=market,
                    dataset_type=dt,
                    freshness_status=FreshnessStatus.UNKNOWN,
                    severity=FreshnessSeverity.WARNING,
                    reasons=[f"Scan error: {exc}"],
                ))

        return records

    def _lookup_timestamp(
        self,
        symbol: str,
        dataset_type: str,
        data_store: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Look up last known timestamp from data_store. Returns empty dict if not found."""
        if data_store is None:
            return {}
        key = f"{symbol}::{dataset_type}"
        return data_store.get(key, data_store.get(symbol, {}))

    def scan_symbols(
        self,
        symbols: List[str],
        market: str = "TWSE",
        datasets: Optional[List[str]] = None,
        policy_registry=None,
        calendar=None,
        data_store: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[FreshnessRecord]]:
        """Scan freshness for multiple symbols."""
        if len(symbols) > self._max_symbols:
            logger.warning(
                "scan_symbols: truncating symbol list from %d to %d",
                len(symbols), self._max_symbols,
            )
            symbols = symbols[:self._max_symbols]

        result: Dict[str, List[FreshnessRecord]] = {}
        for sym in symbols:
            result[sym] = self.scan_symbol(
                sym, market=market, datasets=datasets,
                policy_registry=policy_registry, calendar=calendar,
                data_store=data_store,
            )
        return result

    def scan_universe(
        self,
        universe_id: str = "core",
        registry=None,
        market: str = "TWSE",
        datasets: Optional[List[str]] = None,
        data_store: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[FreshnessRecord]]:
        """Scan freshness for all symbols in a universe."""
        symbols = self._get_universe_symbols(universe_id, registry)
        return self.scan_symbols(symbols, market=market, datasets=datasets, data_store=data_store)

    def _get_universe_symbols(self, universe_id: str, registry) -> List[str]:
        """Get symbol list from registry or return core defaults."""
        if registry is not None:
            try:
                return list(registry.get_symbols(universe_id))
            except Exception as exc:
                logger.warning("scan_universe: registry error: %s", exc)
        # Fallback core symbols
        return ["2330", "2317", "2454", "2303", "2412"]

    def scan_tier(
        self,
        tier: str = "core",
        registry=None,
        market: str = "TWSE",
        datasets: Optional[List[str]] = None,
        data_store: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[FreshnessRecord]]:
        """Scan freshness for all symbols in a tier."""
        return self.scan_universe(
            universe_id=tier, registry=registry, market=market,
            datasets=datasets, data_store=data_store,
        )

    def scan_provider(
        self,
        provider_id: str,
        symbols: Optional[List[str]] = None,
        datasets: Optional[List[str]] = None,
        data_store: Optional[Dict[str, Any]] = None,
    ) -> List[FreshnessRecord]:
        """Scan freshness for all records from a provider."""
        target_symbols = symbols or ["2330"]
        all_records: List[FreshnessRecord] = []
        for sym in target_symbols:
            recs = self.scan_symbol(sym, datasets=datasets, data_store=data_store)
            for rec in recs:
                rec.provider_id = rec.provider_id or provider_id
            all_records.extend(recs)
        return all_records

    def scan_dataset_type(
        self,
        dataset_type: str,
        symbols: Optional[List[str]] = None,
        data_store: Optional[Dict[str, Any]] = None,
    ) -> List[FreshnessRecord]:
        """Scan freshness for a single dataset_type across all symbols."""
        target_symbols = symbols or ["2330", "2317", "2454"]
        all_records: List[FreshnessRecord] = []
        for sym in target_symbols:
            recs = self.scan_symbol(sym, datasets=[dataset_type], data_store=data_store)
            all_records.extend(recs)
        return all_records

    def scan_cache(
        self,
        cache: Dict[str, Any],
        dataset_type: str = DatasetType.CACHE_ENTRY,
    ) -> List[FreshnessRecord]:
        """Scan freshness for cache entries."""
        records: List[FreshnessRecord] = []
        for key, entry in cache.items():
            try:
                rec = self._evaluator.evaluate_cache_entry(
                    entry if isinstance(entry, dict) else {"cached_at": str(entry)},
                    dataset_type,
                )
                rec.symbol = rec.symbol or key
                records.append(rec)
            except Exception as exc:
                logger.warning("scan_cache: error scanning key=%s: %s", key, exc)
        return records

    # ------------------------------------------------------------------ #
    # Summary / filter helpers
    # ------------------------------------------------------------------ #

    def summarize(self, records: List[FreshnessRecord]) -> DailyFreshnessSummary:
        """Build a DailyFreshnessSummary from a list of FreshnessRecords."""
        summary = DailyFreshnessSummary(
            symbols_scanned=len({r.symbol for r in records}),
            datasets_scanned=len(records),
            fresh_count=len(self.list_fresh(records)),
            near_stale_count=sum(1 for r in records if r.freshness_status == FreshnessStatus.NEAR_STALE),
            stale_count=len(self.list_stale(records)),
            critically_stale_count=len(self.list_critical(records)),
            never_received_count=len(self.list_never_received(records)),
            provider_delayed_count=len(self.list_provider_delayed(records)),
            blocked_count=len(self.list_blocked(records)),
            precise_price_blocked_count=sum(1 for r in records if not r.precise_price_allowed),
            backtest_blocked_count=sum(1 for r in records if not r.backtest_allowed),
            abc_blocked_count=sum(1 for r in records if not r.abc_buy_point_allowed),
        )
        return summary

    def list_fresh(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.freshness_status == FreshnessStatus.FRESH]

    def list_near_stale(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.freshness_status == FreshnessStatus.NEAR_STALE]

    def list_stale(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.freshness_status == FreshnessStatus.STALE]

    def list_critical(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.freshness_status == FreshnessStatus.CRITICALLY_STALE]

    def list_never_received(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.freshness_status == FreshnessStatus.NEVER_RECEIVED]

    def list_provider_delayed(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.freshness_status == FreshnessStatus.PROVIDER_DELAYED]

    def list_blocked(self, records: List[FreshnessRecord]) -> List[FreshnessRecord]:
        return [r for r in records if r.blocks_analysis]
