"""
intraday/microstructure_quality.py — Microstructure quality checker (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MicrostructureQualityChecker:
    """
    Checks the availability of intraday microstructure data for one or all symbols.

    In v0.3.27 tick and bid/ask data are NOT yet available — this checker reports
    INTRADAY_BAR_ONLY for any symbol that has 1min/5min data and TICK_PLANNED
    for symbols with no bar data.

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, standard_root: str = "data/import/intraday_standard"):
        self.standard_root = (
            standard_root if os.path.isabs(standard_root)
            else os.path.join(BASE_DIR, standard_root)
        )

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def run(self, symbol: Optional[str] = None) -> dict:
        """
        Check microstructure data availability for one symbol or all symbols.

        Parameters
        ----------
        symbol : str or None
            If None, scan all symbols found in standard_root.

        Returns
        -------
        dict with status, symbols, results, overall_status
        """
        if symbol is not None:
            result = self.check_symbol(symbol)
            return {
                "status": "OK",
                "symbols": [symbol],
                "results": [result],
                "overall_status": result["status"],
            }

        # Scan all symbols
        symbols = self._discover_symbols()
        if not symbols:
            return {
                "status": "NO_DATA",
                "symbols": [],
                "results": [],
                "overall_status": "TICK_PLANNED",
            }

        results = []
        for sym in symbols:
            results.append(self.check_symbol(sym))

        overall = self.get_overall_status(results)
        return {
            "status": "OK",
            "symbols": symbols,
            "results": results,
            "overall_status": overall,
        }

    def check_symbol(self, symbol: str) -> dict:
        """
        Check data availability for a single symbol.

        Returns
        -------
        dict with keys:
            symbol, has_1min, has_5min, has_tick, has_bidask,
            tick_provider_ready, bidask_provider_ready, status, readiness_note
        """
        path_1min = os.path.join(self.standard_root, "1min", f"{symbol}_1min.csv")
        path_5min = os.path.join(self.standard_root, "5min", f"{symbol}_5min.csv")

        has_1min = os.path.isfile(path_1min)
        has_5min = os.path.isfile(path_5min)

        # Tick and BidAsk not available in v0.3.27
        has_tick = False
        has_bidask = False
        tick_provider_ready = False
        bidask_provider_ready = False

        if has_1min or has_5min:
            status = "INTRADAY_BAR_ONLY"
            bar_types = []
            if has_1min:
                bar_types.append("1min")
            if has_5min:
                bar_types.append("5min")
            readiness_note = (
                f"Bar data available: {', '.join(bar_types)}. "
                "Tick and BidAsk data are planned for a future version. "
                "No tick/bidask provider ready in v0.3.27."
            )
        else:
            status = "TICK_PLANNED"
            readiness_note = (
                f"No standardized bar data found for {symbol}. "
                "Tick and BidAsk data are planned for a future version. "
                "Import 1min or 5min CSV data to enable intraday analysis."
            )

        return {
            "symbol": symbol,
            "has_1min": has_1min,
            "has_5min": has_5min,
            "has_tick": has_tick,
            "has_bidask": has_bidask,
            "tick_provider_ready": tick_provider_ready,
            "bidask_provider_ready": bidask_provider_ready,
            "status": status,
            "readiness_note": readiness_note,
        }

    def get_overall_status(self, results: List[dict]) -> str:
        """
        Derive overall microstructure status from a list of per-symbol results.

        If any symbol has INTRADAY_BAR_ONLY, return INTRADAY_BAR_ONLY.
        Otherwise return TICK_PLANNED.
        """
        if not results:
            return "TICK_PLANNED"
        for r in results:
            if r.get("status") == "INTRADAY_BAR_ONLY":
                return "INTRADAY_BAR_ONLY"
        return "TICK_PLANNED"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _discover_symbols(self) -> List[str]:
        """Scan standard_root for all {symbol}_{freq}.csv files and return unique symbols."""
        symbols = []
        if not os.path.isdir(self.standard_root):
            return symbols

        for freq in ["1min", "5min"]:
            freq_dir = os.path.join(self.standard_root, freq)
            if not os.path.isdir(freq_dir):
                continue
            try:
                for fname in os.listdir(freq_dir):
                    if not fname.endswith(".csv"):
                        continue
                    parts = fname.replace(".csv", "").split("_")
                    if parts:
                        sym = parts[0]
                        if sym and sym not in symbols:
                            symbols.append(sym)
            except Exception as exc:
                logger.warning("_discover_symbols: error scanning %s: %s", freq_dir, exc)

        return symbols
