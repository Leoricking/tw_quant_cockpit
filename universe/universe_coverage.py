"""
universe/universe_coverage.py — Per-symbol data coverage analyzer for TW Quant Cockpit v1.1.0.

Analyzes real data coverage per symbol: daily rows, OHLC completeness,
volume, chips, revenue, fundamental coverage.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Real mode: mock rows do NOT count toward READY status.
[!] Missing data: not a crash — returns MISSING/INSUFFICIENT.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from universe.universe_schema import (
    UniverseSymbol,
    UniverseCoverageSummary,
    TIER_CORE_10,
    QUALITY_READY,
    QUALITY_PARTIAL,
    QUALITY_INSUFFICIENT,
    QUALITY_MISSING,
    QUALITY_INVALID,
)

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Quality thresholds
# ---------------------------------------------------------------------------
_READY_MIN_ROWS         = 240
_READY_OHLC_MIN         = 0.98
_PARTIAL_MIN_ROWS       = 120
_PARTIAL_OHLC_MIN       = 0.90


class UniverseCoverageAnalyzer:
    """
    Analyzes per-symbol data coverage.

    For each symbol, computes:
    - daily row count, first/last date, trading_days
    - OHLC completeness, volume completeness
    - duplicate date count, invalid price count
    - chips coverage, revenue coverage, fundamental coverage
    - quality_status: READY / PARTIAL / INSUFFICIENT / MISSING / INVALID

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Mock rows do NOT count toward READY.
    """

    NO_REAL_ORDERS                    = True
    BROKER_DISABLED                   = True
    PRODUCTION_TRADING_BLOCKED        = True
    REAL_DATA_COVERAGE_REQUIRED       = True
    MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False

    def __init__(
        self,
        import_root: str = "data/import",
        results_dir: str = "data/backtest_results",
        mode: str = "real",
    ) -> None:
        self._import_root = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self._results_dir = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self.mode = mode
        self._daily_df = None
        self._chips_syms: Optional[set] = None
        self._revenue_syms: Optional[set] = None
        self._fundamental_syms: Optional[set] = None

    # ------------------------------------------------------------------
    # Main analysis
    # ------------------------------------------------------------------

    def analyze_symbol(self, symbol: str) -> UniverseSymbol:
        """
        Analyze coverage for a single symbol.
        Returns a UniverseSymbol with quality fields populated.
        """
        sym = str(symbol).strip()
        df = self._get_daily_df()

        if df is None or df.empty:
            return UniverseSymbol(
                symbol=sym, quality_status=QUALITY_MISSING,
                reason="no daily data file available",
                daily_available=False,
            )

        try:
            sym_df = df[df["symbol"].astype(str) == sym].copy()
        except Exception as exc:
            logger.warning("analyze_symbol filter error for %s: %s", sym, exc)
            return UniverseSymbol(
                symbol=sym, quality_status=QUALITY_INVALID,
                reason=f"data filter error: {exc}",
            )

        if sym_df.empty:
            return UniverseSymbol(
                symbol=sym, quality_status=QUALITY_MISSING,
                reason="symbol not found in daily data",
                daily_available=False,
            )

        row_count = len(sym_df)
        first_date, last_date = self._date_range(sym_df)
        trading_days = row_count
        ohlc_completeness = self._ohlc_completeness(sym_df)
        volume_completeness = self._volume_completeness(sym_df)
        dup_count = self._duplicate_dates(sym_df)
        invalid_price_count = self._invalid_prices(sym_df)
        missing_ratio = round(1.0 - ohlc_completeness, 4)
        latest_age = self._latest_data_age(last_date)

        chips_ok = sym in self._get_chips_symbols()
        revenue_ok = sym in self._get_revenue_symbols()
        fundamental_ok = sym in self._get_fundamental_symbols()

        quality_status, reason = self._classify(
            row_count=row_count,
            ohlc_completeness=ohlc_completeness,
            invalid_price_count=invalid_price_count,
            dup_count=dup_count,
        )

        return UniverseSymbol(
            symbol=sym,
            tier=TIER_CORE_10,
            daily_available=True,
            volume_available=volume_completeness > 0.8,
            chips_available=chips_ok,
            revenue_available=revenue_ok,
            fundamental_available=fundamental_ok,
            first_date=first_date,
            last_date=last_date,
            trading_days=trading_days,
            missing_ratio=missing_ratio,
            quality_status=quality_status,
            reason=reason,
        )

    def analyze_symbols(self, symbols: List[str]) -> List[UniverseSymbol]:
        """Analyze coverage for a list of symbols."""
        return [self.analyze_symbol(s) for s in symbols]

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_coverage_summary(
        self,
        symbols: List[UniverseSymbol],
        universe_id: str = "",
    ) -> UniverseCoverageSummary:
        """Build a UniverseCoverageSummary from a list of analyzed symbols."""
        total = len(symbols)
        ready = [s for s in symbols if s.quality_status == QUALITY_READY]
        partial = [s for s in symbols if s.quality_status == QUALITY_PARTIAL]
        insufficient = [s for s in symbols if s.quality_status == QUALITY_INSUFFICIENT]
        missing = [s for s in symbols if s.quality_status in (QUALITY_MISSING, QUALITY_INVALID)]

        avg_days = (
            round(sum(s.trading_days for s in symbols if s.trading_days > 0) / total, 1)
            if total > 0 else 0.0
        )
        avg_missing = (
            round(sum(s.missing_ratio for s in symbols) / total, 4)
            if total > 0 else 0.0
        )

        daily_ready = sum(1 for s in symbols if s.daily_available)
        volume_ready = sum(1 for s in symbols if s.volume_available)
        chips_ready = sum(1 for s in symbols if s.chips_available)
        revenue_ready = sum(1 for s in symbols if s.revenue_available)
        fundamental_ready = sum(1 for s in symbols if s.fundamental_available)

        # Statistical confidence
        from backtest.stat_confidence import StatConfidence
        conf = StatConfidence.for_universe_coverage(
            registered_symbols=total,
            ready_symbols=len(ready),
            evaluated_symbols=len(ready) + len(partial),
        )
        confidence = conf["overall"]

        return UniverseCoverageSummary(
            universe_id=universe_id,
            symbol_count=total,
            daily_ready=daily_ready,
            volume_ready=volume_ready,
            chips_ready=chips_ready,
            revenue_ready=revenue_ready,
            fundamental_ready=fundamental_ready,
            average_trading_days=avg_days,
            average_missing_ratio=avg_missing,
            ready_symbols=[s.symbol for s in ready],
            partial_symbols=[s.symbol for s in partial],
            insufficient_symbols=[s.symbol for s in insufficient],
            missing_symbols=[s.symbol for s in missing],
            confidence=confidence,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_daily_df(self):
        if self._daily_df is not None:
            return self._daily_df
        daily_path = os.path.join(_BASE_DIR, "data", "import", "daily", "daily_k.csv")
        if not os.path.isfile(daily_path):
            logger.debug("_get_daily_df: daily_k.csv not found")
            return None
        try:
            import pandas as pd
            self._daily_df = pd.read_csv(daily_path, low_memory=False)
            return self._daily_df
        except Exception as exc:
            logger.warning("_get_daily_df: %s", exc)
            return None

    def _date_range(self, df) -> tuple:
        try:
            date_col = None
            for c in ("date", "Date", "trade_date", "trading_date"):
                if c in df.columns:
                    date_col = c
                    break
            if date_col is None:
                return "", ""
            dates = df[date_col].dropna().astype(str)
            return str(dates.min()), str(dates.max())
        except Exception:
            return "", ""

    def _ohlc_completeness(self, df) -> float:
        ohlc_cols = [c for c in ("open", "high", "low", "close") if c in df.columns]
        if not ohlc_cols or df.empty:
            return 0.0
        try:
            total_cells = len(df) * len(ohlc_cols)
            null_cells = df[ohlc_cols].isnull().sum().sum()
            return round((total_cells - int(null_cells)) / total_cells, 4)
        except Exception:
            return 0.0

    def _volume_completeness(self, df) -> float:
        if "volume" not in df.columns or df.empty:
            return 0.0
        try:
            total = len(df)
            nulls = int(df["volume"].isnull().sum())
            return round((total - nulls) / total, 4)
        except Exception:
            return 0.0

    def _duplicate_dates(self, df) -> int:
        try:
            date_col = None
            for c in ("date", "Date", "trade_date", "trading_date"):
                if c in df.columns:
                    date_col = c
                    break
            if date_col is None:
                return 0
            return int(df[date_col].duplicated().sum())
        except Exception:
            return 0

    def _invalid_prices(self, df) -> int:
        count = 0
        try:
            for col in ("open", "high", "low", "close"):
                if col in df.columns:
                    count += int((df[col].dropna() <= 0).sum())
        except Exception:
            pass
        return count

    def _latest_data_age(self, last_date_str: str) -> int:
        """Returns days since last date. Returns 9999 if unknown."""
        try:
            from datetime import datetime
            ld = datetime.strptime(last_date_str[:10], "%Y-%m-%d")
            return (datetime.now() - ld).days
        except Exception:
            return 9999

    def _classify(
        self,
        row_count: int,
        ohlc_completeness: float,
        invalid_price_count: int,
        dup_count: int,
    ) -> tuple:
        if dup_count > row_count * 0.1 or invalid_price_count > row_count * 0.05:
            return QUALITY_INVALID, f"invalid prices={invalid_price_count} dup_dates={dup_count}"
        if row_count == 0:
            return QUALITY_MISSING, "no rows"
        if row_count >= _READY_MIN_ROWS and ohlc_completeness >= _READY_OHLC_MIN and invalid_price_count == 0:
            return QUALITY_READY, f"rows={row_count} ohlc={ohlc_completeness:.1%}"
        if row_count >= _PARTIAL_MIN_ROWS and ohlc_completeness >= _PARTIAL_OHLC_MIN:
            return QUALITY_PARTIAL, f"rows={row_count} ohlc={ohlc_completeness:.1%}"
        if row_count > 0:
            return QUALITY_INSUFFICIENT, f"rows={row_count} < {_PARTIAL_MIN_ROWS} or ohlc={ohlc_completeness:.1%}"
        return QUALITY_MISSING, "insufficient data"

    def _get_chips_symbols(self) -> set:
        if self._chips_syms is not None:
            return self._chips_syms
        self._chips_syms = self._symbols_from_csv("data/import/institutional/institutional.csv")
        return self._chips_syms

    def _get_revenue_symbols(self) -> set:
        if self._revenue_syms is not None:
            return self._revenue_syms
        self._revenue_syms = self._symbols_from_csv("data/import/monthly_revenue/monthly_revenue.csv")
        return self._revenue_syms

    def _get_fundamental_symbols(self) -> set:
        if self._fundamental_syms is not None:
            return self._fundamental_syms
        for rel_path in (
            "data/import/fundamental/fundamental.csv",
            "data/import/financials/financials.csv",
        ):
            syms = self._symbols_from_csv(rel_path)
            if syms:
                self._fundamental_syms = syms
                return self._fundamental_syms
        self._fundamental_syms = set()
        return self._fundamental_syms

    def _symbols_from_csv(self, rel_path: str) -> set:
        abs_path = os.path.join(_BASE_DIR, rel_path)
        if not os.path.isfile(abs_path):
            return set()
        try:
            import pandas as pd
            df = pd.read_csv(abs_path, low_memory=False, usecols=["symbol"])
            return set(df["symbol"].dropna().astype(str).unique())
        except Exception:
            return set()
