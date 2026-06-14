"""
gui/coverage_quality_gate_adapter.py — CoverageQualityGateAdapter v1.1.4

Adapter between GUI/CLI and the quality_gates package.

[!] Research Only. No Real Orders. Quality Gate does NOT enable trading.
[!] All methods return safe empty defaults on exception — no crash.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageQualityGateAdapter:
    """Adapter between GUI and the quality_gates package.

    [!] Research Only. No Real Orders. Quality Gate does NOT enable trading.
    """

    NO_REAL_ORDERS  = True
    BROKER_DISABLED = True
    RESEARCH_ONLY   = True
    GATE_DOES_NOT_ENABLE_TRADING = True

    def __init__(self, repo_path: Optional[str] = None) -> None:
        self._repo_path = repo_path or BASE_DIR
        self._engine    = None
        self._store     = None
        self._query     = None

    # ----------------------------------------------------------------
    # Lazy-init helpers
    # ----------------------------------------------------------------

    def _get_engine(self):
        if self._engine is None:
            try:
                from quality_gates.gate_engine import CoverageQualityGateEngine
                self._engine = CoverageQualityGateEngine()
            except Exception as exc:
                logger.warning("CoverageQualityGateAdapter: engine unavailable: %s", exc)
        return self._engine

    def _get_store(self):
        if self._store is None:
            try:
                from quality_gates.gate_store import GateResultStore
                self._store = GateResultStore()
            except Exception as exc:
                logger.warning("CoverageQualityGateAdapter: store unavailable: %s", exc)
        return self._store

    def _get_query(self):
        if self._query is None:
            try:
                from quality_gates.gate_query import GateResultQuery
                self._query = GateResultQuery()
            except Exception as exc:
                logger.warning("CoverageQualityGateAdapter: query unavailable: %s", exc)
        return self._query

    # ----------------------------------------------------------------
    # Core evaluation
    # ----------------------------------------------------------------

    def run_evaluation(
        self,
        tier: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        gate_name: Optional[str] = None,
        mode: str = "real",
    ) -> Dict[str, Any]:
        """Run the gate engine and persist results via store.

        Returns a result dict with keys: decisions, universe_summary, errors.
        Returns empty defaults on any exception.
        """
        try:
            engine = self._get_engine()
            if engine is None:
                return {
                    "decisions": [],
                    "universe_summary": {},
                    "errors": ["engine_unavailable"],
                    "research_only": True,
                }
            result = engine.run(
                tier=tier,
                symbols=symbols,
                gate_name=gate_name,
                mode=mode,
            )
            if not isinstance(result, dict):
                result = {"decisions": [], "universe_summary": {}}

            # Persist via store
            store = self._get_store()
            if store is not None:
                try:
                    store.save(result)
                except Exception as exc:
                    logger.warning("CoverageQualityGateAdapter: store.save failed: %s", exc)

            result["research_only"] = True
            return result
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.run_evaluation: %s", exc)
            return {
                "decisions": [],
                "universe_summary": {},
                "errors": [str(exc)],
                "research_only": True,
            }

    # ----------------------------------------------------------------
    # Read-only accessors
    # ----------------------------------------------------------------

    def get_latest_decisions(self) -> List[Dict[str, Any]]:
        """Return latest stored decisions list."""
        try:
            store = self._get_store()
            if store is None:
                return []
            result = store.load_latest()
            if isinstance(result, dict):
                return result.get("decisions", [])
            return []
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.get_latest_decisions: %s", exc)
            return []

    def get_universe_summary(self) -> Dict[str, Any]:
        """Return latest universe summary dict."""
        try:
            store = self._get_store()
            if store is None:
                return {}
            result = store.load_latest()
            if isinstance(result, dict):
                return result.get("universe_summary", {})
            return {}
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.get_universe_summary: %s", exc)
            return {}

    def get_formal_eligible(self) -> List[str]:
        """Return list of formal eligible symbols."""
        try:
            decisions = self.get_latest_decisions()
            return [
                d.get("symbol", "?")
                for d in decisions
                if d.get("decision") == "FORMAL"
            ]
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.get_formal_eligible: %s", exc)
            return []

    def get_blocked_list(self) -> List[Dict[str, Any]]:
        """Return list of blocked symbols with reason codes."""
        try:
            decisions = self.get_latest_decisions()
            result = []
            for d in decisions:
                if d.get("decision") == "BLOCKED":
                    codes = d.get("reason_codes", [])
                    result.append({
                        "symbol": d.get("symbol", "?"),
                        "reason": str(codes[0]) if codes else "UNKNOWN",
                        "reason_codes": codes,
                    })
            return result
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.get_blocked_list: %s", exc)
            return []

    def get_gate_matrix(self, tier: Optional[str] = None) -> Dict[str, Any]:
        """Return gate matrix dict keyed by symbol.

        Each value is a dict of {gate_name: decision_status}.
        """
        try:
            query = self._get_query()
            if query is not None:
                return query.get_gate_matrix(tier=tier)
            # Fallback: build from latest decisions
            decisions = self.get_latest_decisions()
            matrix: Dict[str, Any] = {}
            for d in decisions:
                sym = d.get("symbol", "?")
                if tier and d.get("tier") != tier:
                    continue
                matrix[sym] = d.get("module_gates", {})
            return matrix
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.get_gate_matrix: %s", exc)
            return {}

    # ----------------------------------------------------------------
    # Reporting
    # ----------------------------------------------------------------

    def build_report(
        self,
        tier: Optional[str] = None,
        gate_name: Optional[str] = None,
        mode: str = "real",
    ) -> str:
        """Build and save a coverage quality gate report. Returns file path."""
        try:
            from reports.coverage_quality_gate_report import (
                CoverageQualityGateReportBuilder,
            )
            decisions = self.get_latest_decisions()
            universe  = self.get_universe_summary()
            builder   = CoverageQualityGateReportBuilder()
            return builder.build(
                decisions=decisions,
                universe_summary=universe,
                mode=mode,
                tier=tier,
                gate_name=gate_name,
            )
        except Exception as exc:
            logger.warning("CoverageQualityGateAdapter.build_report: %s", exc)
            return ""

    # ----------------------------------------------------------------
    # CLI helpers
    # ----------------------------------------------------------------

    def get_safe_cli_commands(self) -> List[str]:
        """Return a list of safe CLI commands for this workflow."""
        return [
            "python main.py quality-gate-health",
            "python main.py quality-gate-summary",
            "python main.py quality-gate-universe --tier research30 --gate price_backtest",
            "python main.py quality-gate-blocked",
            "python main.py quality-gate-formal",
            "python main.py quality-gate-run --tier core10 --gate all",
            "python main.py quality-gate-run --tier research30 --gate price_backtest",
            "python main.py quality-gate-report --tier research30",
            "python main.py quality-gate-matrix --tier core10",
            "python main.py quality-gate-override-list",
        ]
