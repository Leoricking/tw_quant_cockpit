"""
universe/scanner.py — Universe Quality Scanner for TW Quant Cockpit v1.3.1.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Single symbol failure must NOT crash entire batch.
[!] No mock fallback on scan failure. No auto-download. No auto-generation of fake OHLCV.
[!] No auto-backtest. No auto-trading suggestions. Not Investment Advice.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from universe.models import (
    CoverageStatus,
    UniverseCoverageRecord,
    UniverseSummary,
    UniverseTier,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True
MOCK_FALLBACK_ENABLED      = False
NO_AUTO_DOWNLOAD           = True
NO_AUTO_FAKE_OHLCV         = True


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class UniverseQualityScanner:
    """
    Batch quality scanner for universe symbols.

    Rules:
    - Uses central DataCompletenessGate (via coverage_analyzer_v131)
    - Single symbol failure does NOT crash entire batch
    - Each symbol has independent result
    - Serial execution (no external worker pool required)
    - Results must be stable and deterministic
    - No mock fallback on scan failure
    - No auto-download of missing data
    - No auto-generation of fake OHLCV
    - No auto-backtest
    - No auto-trading suggestions
    - Must support max scan count limit

    [!] Research Only. No Real Orders.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True
    MOCK_FALLBACK_ENABLED      = False
    MAX_SCAN_DEFAULT           = 500  # Safety limit

    def __init__(
        self,
        registry=None,
        quality_gate=None,
        analyzer=None,
        max_scan: int = 500,
    ) -> None:
        self._registry = registry
        self._quality_gate = quality_gate
        self._max_scan = max_scan
        if analyzer is None:
            from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
            analyzer = UniverseCoverageAnalyzerV131(
                registry=registry,
                quality_gate=quality_gate,
            )
        self._analyzer = analyzer
        self._cancelled = False

    def cancel(self) -> None:
        """Signal cancellation of running scan."""
        self._cancelled = True

    def scan_symbol(self, symbol: str, profile: str = "default") -> UniverseCoverageRecord:
        """
        Scan a single symbol.
        [!] Never auto-downloads. Never generates fake OHLCV. Research Only.
        """
        try:
            return self._analyzer.analyze_symbol(
                symbol,
                profile=profile,
                registry=self._registry,
                quality_gate=self._quality_gate,
            )
        except Exception as exc:
            logger.warning("scan_symbol failed for %s: %s", symbol, exc)
            return UniverseCoverageRecord(
                symbol=symbol,
                quality_status=CoverageStatus.UNAVAILABLE.value,
                blocking_reasons=[f"Scan error: {exc}"],
                checked_at=_now_iso(),
            )

    def scan_universe(self, universe_id: str, profile: str = "default") -> List[UniverseCoverageRecord]:
        """
        Scan all symbols in a universe.
        [!] Single failure does NOT crash batch. Not Investment Advice.
        """
        self._cancelled = False
        if self._registry is None:
            logger.warning("No registry — cannot scan universe %s", universe_id)
            return []
        try:
            symbols = [s.symbol for s in self._registry.list_symbols()]
        except Exception as exc:
            logger.warning("Could not list symbols: %s", exc)
            return []
        return self.scan_symbols(symbols, profile)

    def scan_tier(self, tier: str, profile: str = "default") -> List[UniverseCoverageRecord]:
        """
        Scan all symbols in a tier (across all universes).
        [!] Single failure does NOT crash batch.
        """
        self._cancelled = False
        if self._registry is None:
            return []
        try:
            all_syms = self._registry.list_symbols()
        except Exception:
            return []
        # Filter by tier (use existing tier registry if available, else scan all)
        tier_symbols = [s.symbol for s in all_syms]
        return self.scan_symbols(tier_symbols, profile)

    def scan_symbols(self, symbols: List[str], profile: str = "default") -> List[UniverseCoverageRecord]:
        """
        Scan a list of symbols.
        Applies max_scan limit.
        [!] Single failure does NOT crash batch.
        [!] Results are stable and deterministic (sorted by symbol).
        """
        self._cancelled = False
        if not symbols:
            return []
        # Sort for deterministic order
        sorted_symbols = sorted(set(symbols))
        if len(sorted_symbols) > self._max_scan:
            logger.warning(
                "scan_symbols: %d symbols exceed max_scan=%d; scanning first %d only",
                len(sorted_symbols), self._max_scan, self._max_scan,
            )
            sorted_symbols = sorted_symbols[: self._max_scan]

        results = []
        for sym in sorted_symbols:
            if self._cancelled:
                logger.info("scan_symbols: cancelled after %d symbols", len(results))
                break
            results.append(self.scan_symbol(sym, profile))
        return results

    # ------------------------------------------------------------------
    # Aggregation helpers
    # ------------------------------------------------------------------

    def summarize(self, results: List[UniverseCoverageRecord], profile: str = "") -> UniverseSummary:
        """
        Build UniverseSummary from scan results.
        [!] Summary does NOT indicate tradeable status. Research Only.
        """
        summary = UniverseSummary(
            total_symbols=len(results),
            profile=profile,
            latest_scan_at=_now_iso(),
        )
        for r in results:
            status = r.quality_status
            if status == CoverageStatus.READY.value:
                summary.ready_count += 1
            elif status == CoverageStatus.PARTIAL.value:
                summary.partial_count += 1
            elif status == CoverageStatus.MISSING.value:
                summary.missing_count += 1
            elif status == CoverageStatus.STALE.value:
                summary.stale_count += 1
            elif status == CoverageStatus.BLOCKED.value:
                summary.blocked_count += 1
            elif status == CoverageStatus.DEMO_ONLY.value:
                summary.demo_only_count += 1
            else:  # UNAVAILABLE, EXCLUDED, unknown
                summary.unavailable_count += 1
        return summary

    def list_ready(self, results: List[UniverseCoverageRecord]) -> List[str]:
        return [r.symbol for r in results if r.quality_status == CoverageStatus.READY.value]

    def list_partial(self, results: List[UniverseCoverageRecord]) -> List[str]:
        return [r.symbol for r in results if r.quality_status == CoverageStatus.PARTIAL.value]

    def list_blocked(self, results: List[UniverseCoverageRecord]) -> List[str]:
        return [r.symbol for r in results if r.quality_status == CoverageStatus.BLOCKED.value]

    def list_unavailable(self, results: List[UniverseCoverageRecord]) -> List[str]:
        return [r.symbol for r in results if r.quality_status == CoverageStatus.UNAVAILABLE.value]

    def list_demo_only(self, results: List[UniverseCoverageRecord]) -> List[str]:
        return [r.symbol for r in results if r.quality_status == CoverageStatus.DEMO_ONLY.value]
