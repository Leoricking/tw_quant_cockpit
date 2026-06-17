"""
replay/strategy_knowledge_adapter.py — Adapter for Strategy Knowledge Engine in replay context.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Does NOT re-implement strategy rules.
[!] Does NOT modify the engine's real/mock behavior.
[!] If engine unavailable, returns UNAVAILABLE for all modules (no crash).
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_STRATEGY_EXECUTION_ENABLED = False


class ReplayStrategyKnowledgeAdapter:
    """
    Adapter that calls the existing Strategy Knowledge Engine and normalizes
    output for the Replay schema.

    Does NOT re-implement strategy rules.
    Does NOT modify the engine's real/mock behavior.
    If engine unavailable, returns UNAVAILABLE for all modules (no crash).
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    REQUIRED_KEYS = [
        "signal", "score", "warning", "reason", "available",
        "evidence", "confidence", "qualification", "timing_warning",
    ]

    MODULE_NAMES = [
        "KD_ADVANCED", "SHORT_INTEREST", "BOTTOM_REVERSAL",
        "SECTOR_ROTATION", "FUNDAMENTAL_QUALITY", "NO_CHASE",
        "NO_PANIC_SELL", "DO_NOT_REBUY_YET", "ABC_BUY_POINT",
    ]

    # Map module names to engine output keys
    ENGINE_KEY_MAP = {
        "KD_ADVANCED": "kd_advanced_signals",
        "SHORT_INTEREST": "short_interest_signals",
        "BOTTOM_REVERSAL": "bottom_reversal_signals",
        "SECTOR_ROTATION": "sector_rotation_signals",
        "FUNDAMENTAL_QUALITY": "fundamental_quality_signals",
        "NO_CHASE": "no_chase_reasons",
        "NO_PANIC_SELL": "no_sell_low_reasons",
        "DO_NOT_REBUY_YET": "do_not_rebuy_yet_reasons",
        "ABC_BUY_POINT": "kd_advanced_signals",  # ABC derived from kd
    }

    def evaluate(
        self,
        symbol: str,
        replay_date: str,
        context: Dict[str, Any],
        mode: str = "real",
    ) -> Dict[str, Any]:
        """
        Call existing strategy engine and normalize all module outputs.
        Returns dict keyed by module_name -> normalized module dict.
        On any error: returns all modules as UNAVAILABLE (no crash).
        """
        results = {}
        try:
            raw_output = self._call_engine(symbol, replay_date, context, mode)
        except Exception as exc:
            logger.warning("Strategy engine unavailable for %s on %s: %s", symbol, replay_date, exc)
            raw_output = {}

        for module_name in self.MODULE_NAMES:
            try:
                engine_key = self.ENGINE_KEY_MAP.get(module_name, "")
                raw_module = raw_output.get(engine_key, {}) if raw_output else {}
                results[module_name] = self.normalize_module_output(module_name, raw_module)
            except Exception as exc:
                logger.warning("Module %s normalize error: %s", module_name, exc)
                results[module_name] = self.safe_fallback(module_name, str(exc))

        return results

    def evaluate_module(
        self,
        module_name: str,
        symbol: str,
        replay_date: str,
        context: Dict[str, Any],
        mode: str = "real",
    ) -> Dict[str, Any]:
        """Evaluate a single module. Returns normalized dict."""
        try:
            raw_output = self._call_engine(symbol, replay_date, context, mode)
            engine_key = self.ENGINE_KEY_MAP.get(module_name, "")
            raw_module = raw_output.get(engine_key, {}) if raw_output else {}
            return self.normalize_module_output(module_name, raw_module)
        except Exception as exc:
            logger.warning("evaluate_module %s error: %s", module_name, exc)
            return self.safe_fallback(module_name, str(exc))

    def _call_engine(
        self,
        symbol: str,
        replay_date: str,
        context: Dict[str, Any],
        mode: str = "real",
    ) -> Dict[str, Any]:
        """
        Call the existing build_strategy_signals engine.
        Returns raw engine output dict. Raises if engine unavailable.
        """
        try:
            from analysis.strategy_knowledge_engine import build_strategy_signals
        except ImportError as exc:
            raise RuntimeError(f"Strategy Knowledge Engine unavailable: {exc}") from exc

        import pandas as pd
        df = context.get("df")
        if df is None or not isinstance(df, pd.DataFrame) or len(df) == 0:
            raise RuntimeError("No valid DataFrame provided in context")

        kwargs = {
            "df": df,
            "symbol": symbol,
            "entry_price": context.get("entry_price"),
            "portfolio_value": context.get("portfolio_value", 1_000_000),
            "strategy_capital_ratio": context.get("strategy_capital_ratio", 0.30),
            "n_positions": context.get("n_positions", 4),
            "atr": context.get("atr"),
            "estimated_eps": context.get("estimated_eps"),
            "trailing_eps": context.get("trailing_eps"),
            "pe_low": context.get("pe_low"),
            "pe_mid": context.get("pe_mid"),
            "pe_high": context.get("pe_high"),
            "pe_extreme_low": context.get("pe_extreme_low"),
            "pe_extreme_high": context.get("pe_extreme_high"),
            "revenue_growth": context.get("revenue_growth"),
            "gross_margin": context.get("gross_margin"),
            "eps_declining": context.get("eps_declining", False),
            "institution_type": context.get("institution_type", "none"),
            "institution_net": context.get("institution_net", 0.0),
            "institution_buying": context.get("institution_buying", False),
            "half_profit_taken": context.get("half_profit_taken", False),
            "trend_stage": context.get("trend_stage"),
            "previous_high": context.get("previous_high"),
            "take_profit_price": context.get("take_profit_price"),
            "margin_df": context.get("margin_df"),
            "sector_peers": context.get("sector_peers"),
            "theme_tags": context.get("theme_tags"),
            "leader_symbol": context.get("leader_symbol"),
            "leader_df": context.get("leader_df"),
            "monthly_revenue_rows": context.get("monthly_revenue_rows"),
            "eps_ttm": context.get("eps_ttm"),
            "eps_qoq_change": context.get("eps_qoq_change"),
            "gross_margin_prev": context.get("gross_margin_prev"),
            "operating_margin": context.get("operating_margin"),
            "operating_margin_prev": context.get("operating_margin_prev"),
            "price_vs_ma20": context.get("price_vs_ma20"),
            "price_vs_ma60": context.get("price_vs_ma60"),
        }

        return build_strategy_signals(**kwargs)

    def normalize_engine_output(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize the engine's full output to standard dict keyed by module name."""
        normalized = {}
        for module_name in self.MODULE_NAMES:
            engine_key = self.ENGINE_KEY_MAP.get(module_name, "")
            raw_module = raw_output.get(engine_key, {}) if raw_output else {}
            normalized[module_name] = self.normalize_module_output(module_name, raw_module)
        return normalized

    def normalize_module_output(
        self, module_name: str, raw_module_output: Any
    ) -> Dict[str, Any]:
        """
        Normalize a single module output.
        Fill missing keys with safe defaults.
        """
        if not isinstance(raw_module_output, dict):
            return self.safe_fallback(module_name, "output not a dict")

        result = {k: raw_module_output.get(k, None) for k in self.REQUIRED_KEYS}

        if result["available"] is None:
            result["available"] = bool(raw_module_output)
        if not result["available"]:
            result["signal"] = "UNAVAILABLE"
        if result["signal"] is None:
            result["signal"] = "UNKNOWN"
        if result["score"] is not None:
            try:
                result["score"] = float(result["score"])
            except (TypeError, ValueError):
                result["score"] = None
        if result["warning"] is None:
            result["warning"] = ""
        if result["reason"] is None:
            result["reason"] = ""
        if result["evidence"] is None:
            result["evidence"] = []
        elif not isinstance(result["evidence"], list):
            result["evidence"] = [str(result["evidence"])]
        if result["confidence"] is None:
            result["confidence"] = "INSUFFICIENT"
        if result["qualification"] is None:
            result["qualification"] = "OBSERVATIONAL_ONLY"
        if result["timing_warning"] is None:
            result["timing_warning"] = ""

        result["source_fields"] = list(raw_module_output.keys())
        result["source_dates"] = raw_module_output.get("source_dates", [])
        result["limitations"] = raw_module_output.get("limitations", [])

        return result

    def availability(
        self,
        symbol: str,
        replay_date: str,
        context: Dict[str, Any],
    ) -> Dict[str, bool]:
        """Check which modules are available."""
        results = self.evaluate(symbol, replay_date, context)
        return {
            module: bool(results.get(module, {}).get("available", False))
            for module in self.MODULE_NAMES
        }

    def source_metadata(
        self, module_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get source field metadata for a module."""
        engine_key = self.ENGINE_KEY_MAP.get(module_name, "")
        return {
            "module_name": module_name,
            "engine_key": engine_key,
            "context_keys": list(context.keys()) if context else [],
        }

    def timing_warnings(
        self, module_name: str, result: Dict[str, Any], replay_date: str
    ) -> str:
        """Generate point-in-time timing warnings."""
        warnings = []
        if not result.get("available", False):
            return ""
        if result.get("timing_warning"):
            warnings.append(result["timing_warning"])
        source_dates = result.get("source_dates", [])
        for sd in source_dates:
            if sd and sd > replay_date:
                warnings.append(f"Source date {sd} is after replay_date {replay_date}")
        return "; ".join(warnings) if warnings else ""

    def verify_consistent_keys(
        self, module_name: str, result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify all required keys present."""
        missing = [k for k in self.REQUIRED_KEYS if k not in result]
        return {
            "consistent": len(missing) == 0,
            "missing_keys": missing,
            "module_name": module_name,
        }

    def safe_fallback(
        self, module_name: str, error_msg: str = ""
    ) -> Dict[str, Any]:
        """Return safe UNAVAILABLE result on error."""
        return {
            "signal": "UNAVAILABLE",
            "score": None,
            "warning": f"Module unavailable: {error_msg}",
            "reason": "Engine not accessible or data missing",
            "available": False,
            "evidence": [],
            "confidence": "INSUFFICIENT",
            "qualification": "UNAVAILABLE",
            "timing_warning": "",
            "source_fields": [],
            "source_dates": [],
            "limitations": [f"Engine error: {error_msg}" if error_msg else "Engine unavailable"],
        }
