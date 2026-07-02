"""
paper_trading/performance_attribution/attribution_query_v167.py
Read-only Query API for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Read-only. Deterministic. Empty state clearly indicated. Invalid query fails explicitly.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, RegimeType
from .models_v167 import AttributionComparison, AttributionSummary
from .attribution_store_v167 import AttributionStore

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class AttributionQueryAPI:
    """
    Read-only query API for attribution runs.
    Never modifies the store. Unsupported queries fail explicitly (not empty PASS).
    """

    def __init__(self, store: AttributionStore) -> None:
        self._store = store

    # ── Individual level queries ──────────────────────────────────────────────

    def get_portfolio_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}", "status": "NOT_FOUND"}
        return run.get("portfolio_attribution", {"status": "EMPTY", "run_id": run_id})

    def get_strategy_attribution(self, run_id: str, strategy_id: Optional[str] = None) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        strategies = run.get("strategy_attribution", {})
        if strategy_id:
            result = strategies.get(strategy_id)
            if result is None:
                return {"error": f"strategy_not_found: {strategy_id}", "status": "NOT_FOUND"}
            return result
        return strategies

    def get_session_attribution(self, run_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        sessions = run.get("session_attribution", {})
        if session_id:
            return sessions.get(session_id, {"error": f"session_not_found: {session_id}"})
        return sessions

    def get_symbol_attribution(self, run_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        symbols = run.get("symbol_attribution", {})
        if symbol:
            return symbols.get(symbol, {"error": f"symbol_not_found: {symbol}"})
        return symbols

    def get_sector_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("sector_attribution", {"status": "EMPTY"})

    def get_industry_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("industry_attribution", {"status": "EMPTY"})

    def get_position_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("position_attribution", {"status": "EMPTY"})

    def get_trade_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("trade_attribution", {"status": "EMPTY"})

    def get_cost_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("cost_attribution", {"status": "EMPTY"})

    def get_execution_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("execution_attribution", {"status": "EMPTY"})

    def get_risk_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("risk_attribution", {"status": "EMPTY"})

    def get_drawdown_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("drawdown_attribution", {"status": "EMPTY"})

    def get_regime_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("regime_attribution", {"status": "EMPTY"})

    def get_factor_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("factor_attribution", {"status": "EMPTY"})

    # ── Aggregation queries ───────────────────────────────────────────────────

    def get_top_contributors(self, run_id: str, level: str = "symbol", n: int = 5) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        key = f"{level}_attribution"
        data = run.get(key, {})
        if isinstance(data, dict):
            sorted_items = sorted(data.items(), key=lambda x: x[1].get("return", 0.0) if isinstance(x[1], dict) else x[1], reverse=True)
            return {"top_contributors": sorted_items[:n], "level": level, "n": n}
        return {"error": f"unsupported_level: {level}"}

    def get_bottom_contributors(self, run_id: str, level: str = "symbol", n: int = 5) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        key = f"{level}_attribution"
        data = run.get(key, {})
        if isinstance(data, dict):
            sorted_items = sorted(data.items(), key=lambda x: x[1].get("return", 0.0) if isinstance(x[1], dict) else x[1])
            return {"bottom_contributors": sorted_items[:n], "level": level, "n": n}
        return {"error": f"unsupported_level: {level}"}

    def get_reconciliation_status(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("reconciliation", {"status": "EMPTY"})

    def get_quality_score(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        return run.get("quality_score", {"status": "EMPTY"})

    # ── Comparison queries ────────────────────────────────────────────────────

    def compare_periods(self, run_ids: List[str], dimension: str = "active_return") -> Dict[str, Any]:
        if not run_ids:
            return {"error": "empty_run_ids"}
        results = {}
        for rid in run_ids:
            run = self._store.load_run(rid)
            if run:
                pa = run.get("portfolio_attribution", {})
                results[rid] = pa.get(dimension, None)
        return {
            "comparison": results,
            "dimension": dimension,
            "run_ids": run_ids,
            "paper_only": True,
            "read_only": True,
        }

    def compare_strategies(self, run_id: str, strategy_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        strategies = run.get("strategy_attribution", {})
        if strategy_ids:
            strategies = {k: v for k, v in strategies.items() if k in strategy_ids}
        return {"strategies": strategies, "run_id": run_id, "paper_only": True}

    def compare_sessions(self, run_id: str, session_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        sessions = run.get("session_attribution", {})
        if session_ids:
            sessions = {k: v for k, v in sessions.items() if k in session_ids}
        return {"sessions": sessions, "run_id": run_id, "paper_only": True}

    def compare_symbols(self, run_id: str, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        sym_data = run.get("symbol_attribution", {})
        if symbols:
            sym_data = {k: v for k, v in sym_data.items() if k in symbols}
        return {"symbols": sym_data, "run_id": run_id, "paper_only": True}

    def summarize_attribution(self, run_id: str) -> Dict[str, Any]:
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run_not_found: {run_id}"}
        pa = run.get("portfolio_attribution", {})
        return {
            "run_id": run_id,
            "portfolio_id": run.get("portfolio_id", ""),
            "period_start": run.get("period_start", ""),
            "period_end": run.get("period_end", ""),
            "status": run.get("status", "UNKNOWN"),
            "active_return": pa.get("active_return", None),
            "reconciled": pa.get("reconciled", None),
            "confidence": pa.get("confidence", "UNKNOWN"),
            "paper_only": True,
            "research_only": True,
            "not_for_real_trading": True,
        }
