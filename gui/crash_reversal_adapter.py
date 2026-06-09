"""
gui/crash_reversal_adapter.py — CrashReversalAdapter v0.9.0.1

GUI bridge between CrashReversalStrategyPack and GUI panels.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

# gui/crash_reversal_adapter.py
# TW Quant Cockpit — Crash Reversal GUI Adapter
# v0.9.0.1 — Research Only / No Real Orders
VERSION = "v0.9.0.1"

import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from strategy_rules.crash_reversal_pack import CrashReversalStrategyPack
    _PACK_AVAILABLE = True
except ImportError:
    _PACK_AVAILABLE = False


class CrashReversalAdapter:
    """Adapter between CrashReversalStrategyPack and GUI panels.

    read_only=True, no_real_orders=True, production_blocked=True
    Never outputs BUY/SELL/ORDER.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    _FORBIDDEN = frozenset([
        "BUY", "SELL", "ORDER", "EXECUTE",
        "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
    ])

    def __init__(self, mode: str = "real") -> None:
        self.mode   = mode
        self._pack  = CrashReversalStrategyPack() if _PACK_AVAILABLE else None

    # ------------------------------------------------------------------
    # Core check methods
    # ------------------------------------------------------------------

    def run_market_check(self, market_context: dict = None) -> dict:
        """Run market-level crash reversal check. Returns dict or error dict."""
        if market_context is None:
            market_context = {}
        try:
            if self._pack is not None:
                return self._pack.evaluate_market(market_context)
        except Exception as exc:
            logger.warning("CrashReversalAdapter.run_market_check: %s", exc)
        return {
            "crash_cause":       None,
            "stabilization":     None,
            "no_real_orders":    True,
            "production_blocked": True,
            "error":             "INSUFFICIENT_DATA",
        }

    def run_symbol_check(
        self,
        symbol: str,
        stock_context: dict = None,
        market_context: dict = None,
    ) -> dict:
        """Run symbol-level crash reversal check. Returns dict or error dict."""
        if stock_context is None:
            stock_context = {}
        if market_context is None:
            market_context = {}
        try:
            if self._pack is not None:
                return self._pack.evaluate_symbol(
                    symbol=symbol,
                    stock_context=stock_context,
                    market_context=market_context,
                )
        except Exception as exc:
            logger.warning("CrashReversalAdapter.run_symbol_check(%s): %s", symbol, exc)
        return {
            "symbol":            symbol,
            "no_real_orders":    True,
            "production_blocked": True,
            "error":             "INSUFFICIENT_DATA",
        }

    def run_full_check(
        self,
        symbols: list = None,
        market_context: dict = None,
    ) -> dict:
        """Run full check for market + list of symbols. Returns combined result dict."""
        if symbols is None:
            symbols = []
        if market_context is None:
            market_context = {}
        try:
            if self._pack is not None:
                return self._pack.evaluate_full(
                    symbols=symbols,
                    market_context=market_context,
                )
        except Exception as exc:
            logger.warning("CrashReversalAdapter.run_full_check: %s", exc)
        # Fallback: attempt market check + individual symbol checks
        result: dict = {
            "no_real_orders":    True,
            "production_blocked": True,
        }
        market_result = self.run_market_check(market_context)
        result["crash_cause"]   = market_result.get("crash_cause")
        result["stabilization"] = market_result.get("stabilization")
        symbol_results = []
        for sym in symbols:
            symbol_results.append(self.run_symbol_check(sym, {}, market_context))
        result["symbols"]  = symbol_results
        result["error"]    = market_result.get("error", "INSUFFICIENT_DATA")
        return result

    # ------------------------------------------------------------------
    # Safe command helper
    # ------------------------------------------------------------------

    def get_safe_command(self, mode: str = None) -> str:
        """Return a safe CLI command string (never contains forbidden keywords)."""
        m   = mode or self.mode
        cmd = f"python main.py crash-reversal --mode {m}"
        for forbidden in self._FORBIDDEN:
            if forbidden.lower() in cmd.lower():
                return "python main.py crash-reversal-summary"
        return cmd

    # ------------------------------------------------------------------
    # Report builder
    # ------------------------------------------------------------------

    def build_report(self, pack_result: dict = None, output_dir: str = "reports") -> str:
        """Build crash reversal report. Returns file path or empty string."""
        try:
            from reports.crash_reversal_strategy_report import CrashReversalStrategyReportBuilder
            if not os.path.isabs(output_dir):
                output_dir = os.path.join(BASE_DIR, output_dir)
            builder = CrashReversalStrategyReportBuilder(output_dir=output_dir)
            result  = pack_result or {}
            return builder.build(result, mode=self.mode) or ""
        except Exception as exc:
            logger.warning("CrashReversalAdapter.build_report: %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Availability
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Return True if the strategy pack is importable and instantiated."""
        return _PACK_AVAILABLE and self._pack is not None
