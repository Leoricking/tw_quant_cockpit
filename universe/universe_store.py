"""
universe/universe_store.py — Universe data persistence for TW Quant Cockpit v1.1.0.

Saves/loads registry and coverage data to/from CSV.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List, Optional

from universe.universe_schema import UniverseSymbol, UniverseCoverageSummary

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UniverseStore:
    """
    Saves and loads universe data.

    Paths:
    - data/backtest_results/universe/universe_registry.csv
    - data/backtest_results/universe/universe_symbol_coverage.csv
    - data/backtest_results/universe/universe_tier_summary.csv
    - data/backtest_results/universe/universe_missing_data.csv
    - data/backtest_results/universe/universe_source_summary.csv

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True

    def __init__(self, output_dir: str = "data/backtest_results/universe") -> None:
        self._output_dir = os.path.join(_BASE_DIR, output_dir) if not os.path.isabs(output_dir) else output_dir

    def _ensure_dir(self) -> None:
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Registry
    # ------------------------------------------------------------------

    def save_registry(self, symbols: List[UniverseSymbol]) -> str:
        self._ensure_dir()
        path = os.path.join(self._output_dir, "universe_registry.csv")
        rows = [s.to_dict() for s in symbols]
        self._write_csv(path, rows)
        return path

    def load_registry(self) -> List[UniverseSymbol]:
        path = os.path.join(self._output_dir, "universe_registry.csv")
        rows = self._read_csv(path)
        return [UniverseSymbol.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Coverage
    # ------------------------------------------------------------------

    def save_coverage(self, symbols: List[UniverseSymbol]) -> str:
        self._ensure_dir()
        path = os.path.join(self._output_dir, "universe_symbol_coverage.csv")
        rows = [s.to_dict() for s in symbols]
        self._write_csv(path, rows)
        return path

    def load_latest_coverage(self) -> List[UniverseSymbol]:
        path = os.path.join(self._output_dir, "universe_symbol_coverage.csv")
        rows = self._read_csv(path)
        return [UniverseSymbol.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def save_summary(self, summary: UniverseCoverageSummary) -> str:
        self._ensure_dir()
        path = os.path.join(self._output_dir, "universe_tier_summary.csv")
        row = {
            "universe_id":           summary.universe_id,
            "symbol_count":          summary.symbol_count,
            "daily_ready":           summary.daily_ready,
            "volume_ready":          summary.volume_ready,
            "chips_ready":           summary.chips_ready,
            "revenue_ready":         summary.revenue_ready,
            "fundamental_ready":     summary.fundamental_ready,
            "average_trading_days":  summary.average_trading_days,
            "average_missing_ratio": summary.average_missing_ratio,
            "ready_count":           len(summary.ready_symbols),
            "partial_count":         len(summary.partial_symbols),
            "insufficient_count":    len(summary.insufficient_symbols),
            "missing_count":         len(summary.missing_symbols),
            "confidence":            summary.confidence,
            "generated_at":          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._write_csv(path, [row])
        return path

    def load_latest_summary(self) -> Optional[UniverseCoverageSummary]:
        path = os.path.join(self._output_dir, "universe_tier_summary.csv")
        rows = self._read_csv(path)
        if not rows:
            return None
        return UniverseCoverageSummary.from_dict(rows[-1])

    # ------------------------------------------------------------------
    # Missing data report
    # ------------------------------------------------------------------

    def save_missing_data(self, symbols: List[UniverseSymbol], tier: str = "") -> str:
        self._ensure_dir()
        from universe.universe_schema import QUALITY_MISSING, QUALITY_INSUFFICIENT
        missing = [s for s in symbols if s.quality_status in (QUALITY_MISSING, QUALITY_INSUFFICIENT)]
        path = os.path.join(self._output_dir, "universe_missing_data.csv")
        rows = [
            {
                "symbol":         s.symbol,
                "name":           s.name,
                "tier":           s.tier or tier,
                "quality_status": s.quality_status,
                "trading_days":   s.trading_days,
                "missing_ratio":  s.missing_ratio,
                "reason":         s.reason,
            }
            for s in missing
        ]
        self._write_csv(path, rows)
        return path

    # ------------------------------------------------------------------
    # Source summary
    # ------------------------------------------------------------------

    def save_source_summary(self, symbols: List[UniverseSymbol]) -> str:
        self._ensure_dir()
        from collections import Counter
        sources = Counter(s.source for s in symbols if s.source)
        path = os.path.join(self._output_dir, "universe_source_summary.csv")
        rows = [{"source": k, "count": v} for k, v in sources.most_common()]
        self._write_csv(path, rows)
        return path

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _write_csv(self, path: str, rows: list) -> None:
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        try:
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.debug("UniverseStore wrote %d rows to %s", len(rows), path)
        except Exception as exc:
            logger.error("UniverseStore._write_csv %s: %s", path, exc)

    def _read_csv(self, path: str) -> list:
        if not os.path.isfile(path):
            return []
        try:
            rows = []
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
            return rows
        except Exception as exc:
            logger.warning("UniverseStore._read_csv %s: %s", path, exc)
            return []
