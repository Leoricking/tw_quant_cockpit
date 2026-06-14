"""
quality_gates.gate_decision_engine — CoverageQualityGateEngine v1.1.4

Research-only. Orchestrates symbol and universe gate evaluation.
Returns eligibility decisions only. Does NOT execute trades, repair data,
or trigger any automated action.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True
PRODUCTION_TRADING_BLOCKED = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageQualityGateEngine:
    """Orchestrates quality gate evaluation for symbols and universes."""

    NO_REAL_ORDERS = True
    BROKER_DISABLED = True

    def __init__(self, repo_path: Optional[str] = None):
        self._repo_path = repo_path or BASE_DIR
        self._symbol_evaluator = None
        self._universe_evaluator = None

    @property
    def symbol_evaluator(self):
        if self._symbol_evaluator is None:
            from quality_gates.symbol_gate_evaluator import SymbolQualityGateEvaluator
            self._symbol_evaluator = SymbolQualityGateEvaluator(repo_path=self._repo_path)
        return self._symbol_evaluator

    @property
    def universe_evaluator(self):
        if self._universe_evaluator is None:
            from quality_gates.universe_gate_evaluator import UniverseQualityGateEvaluator
            self._universe_evaluator = UniverseQualityGateEvaluator(repo_path=self._repo_path)
        return self._universe_evaluator

    def evaluate_symbol(self, symbol: str, gate_name: str, mode: str = "real"):
        """Evaluate a single symbol against a named gate. Returns QualityGateDecision."""
        try:
            return self.symbol_evaluator.evaluate(symbol, gate_name, mode=mode)
        except Exception as exc:
            logger.warning("evaluate_symbol failed for %s/%s: %s", symbol, gate_name, exc)
            from quality_gates.gate_schema import QualityGateDecision, GATE_LEVEL_BLOCKED, DECISION_BLOCKED_DATA_QUALITY
            return QualityGateDecision(symbol=symbol, gate_name=gate_name,
                                       gate_level=GATE_LEVEL_BLOCKED,
                                       decision=DECISION_BLOCKED_DATA_QUALITY,
                                       reasons=[str(exc)])

    def evaluate_universe(self, tier: str, gate_name: str, mode: str = "real"):
        """Evaluate all symbols in a tier against a named gate. Returns UniverseGateSummary."""
        try:
            return self.universe_evaluator.evaluate_tier(tier, gate_name, mode=mode)
        except Exception as exc:
            logger.warning("evaluate_universe failed for %s/%s: %s", tier, gate_name, exc)
            from quality_gates.gate_schema import UniverseGateSummary
            return UniverseGateSummary(tier=tier, reasons=[str(exc)])

    def evaluate_custom_symbols(self, symbols: List[str], gate_name: str, mode: str = "real"):
        """Evaluate a custom list of symbols against a named gate."""
        try:
            return self.universe_evaluator.evaluate_symbols(symbols, gate_name, mode=mode)
        except Exception as exc:
            logger.warning("evaluate_custom_symbols failed: %s", exc)
            from quality_gates.gate_schema import UniverseGateSummary
            return UniverseGateSummary(reasons=[str(exc)])

    def evaluate_all_gates(self, symbol: str, mode: str = "real") -> Dict[str, Any]:
        """Evaluate all 12 gates for a single symbol. Returns {gate_name: decision}."""
        try:
            return self.symbol_evaluator.evaluate_all_gates(symbol, mode=mode)
        except Exception as exc:
            logger.warning("evaluate_all_gates failed for %s: %s", symbol, exc)
            return {}

    def build_gate_matrix(self, tier: str, mode: str = "real") -> Dict[str, Dict[str, str]]:
        """Build a matrix of {symbol: {gate_name: decision_str}} for all gates in a tier.
        Returns eligibility only — does NOT execute anything."""
        try:
            from quality_gates.gate_policy import ALL_GATES
            symbols = self._resolve_tier_symbols(tier)
            matrix: Dict[str, Dict[str, str]] = {}
            for sym in symbols:
                sym_row: Dict[str, str] = {}
                for gate in ALL_GATES:
                    try:
                        dec = self.symbol_evaluator.evaluate(sym, gate, mode=mode)
                        sym_row[gate] = dec.gate_level
                    except Exception:
                        sym_row[gate] = "UNKNOWN"
                matrix[sym] = sym_row
            return matrix
        except Exception as exc:
            logger.warning("build_gate_matrix failed: %s", exc)
            return {}

    def build_execution_filter(self, decisions: List[Any]) -> Dict[str, Any]:
        """Build an auditable filter dict from a list of QualityGateDecision objects.
        Returns eligibility data only — never executes trades."""
        result: Dict[str, Any] = {}
        for dec in decisions:
            try:
                d = dec if isinstance(dec, dict) else (dec.to_dict() if hasattr(dec, "to_dict") else {})
                sym = d.get("symbol", "")
                if not sym:
                    continue
                result[sym] = {
                    "eligible": d.get("eligible", False),
                    "gate_level": d.get("gate_level", "BLOCKED"),
                    "decision": d.get("decision", "BLOCKED_DATA_QUALITY"),
                    "reason_codes": d.get("reason_codes", []),
                    "confidence": d.get("confidence", "UNKNOWN"),
                }
            except Exception as exc:
                logger.warning("build_execution_filter entry failed: %s", exc)
        return result

    def explain_decision(self, decision_id: str, decisions: Optional[List[Any]] = None) -> str:
        """Return a human-readable explanation of a decision by ID."""
        if decisions:
            for dec in decisions:
                d = dec if isinstance(dec, dict) else (dec.to_dict() if hasattr(dec, "to_dict") else {})
                if d.get("decision_id") == decision_id:
                    lines = [
                        f"Decision ID: {decision_id}",
                        f"Symbol:      {d.get('symbol', '?')}",
                        f"Gate:        {d.get('gate_name', '?')}",
                        f"Level:       {d.get('gate_level', '?')}",
                        f"Decision:    {d.get('decision', '?')}",
                        f"Confidence:  {d.get('confidence', '?')}",
                        f"Reason Codes: {', '.join(d.get('reason_codes', []))}",
                        f"Reasons:     {'; '.join(d.get('reasons', []))}",
                        f"Actions:     {'; '.join(d.get('required_actions', []))}",
                        "[!] Research Only. No Real Orders. Gate does NOT enable trading.",
                    ]
                    return "\n".join(lines)
        return f"Decision {decision_id} not found in provided decisions list."

    def compare_gate_runs(self, run_a: List[Any], run_b: List[Any]) -> Dict[str, Any]:
        """Compare two gate run results. Returns changes dict."""
        map_a = {(d.get("symbol"), d.get("gate_name")): d.get("gate_level")
                 for d in (x.to_dict() if hasattr(x, "to_dict") else x for x in run_a)}
        map_b = {(d.get("symbol"), d.get("gate_name")): d.get("gate_level")
                 for d in (x.to_dict() if hasattr(x, "to_dict") else x for x in run_b)}
        improved, degraded, unchanged = [], [], []
        all_keys = set(map_a) | set(map_b)
        order = ["FORMAL", "OBSERVATIONAL", "DEMO", "BLOCKED", "UNKNOWN"]
        for key in all_keys:
            a_lvl = map_a.get(key, "UNKNOWN")
            b_lvl = map_b.get(key, "UNKNOWN")
            if a_lvl == b_lvl:
                unchanged.append({"symbol": key[0], "gate": key[1], "level": a_lvl})
            elif order.index(a_lvl) > order.index(b_lvl):
                improved.append({"symbol": key[0], "gate": key[1], "from": a_lvl, "to": b_lvl})
            else:
                degraded.append({"symbol": key[0], "gate": key[1], "from": a_lvl, "to": b_lvl})
        return {"improved": improved, "degraded": degraded, "unchanged_count": len(unchanged)}

    def run(self, tier: Optional[str] = None, symbols: Optional[List[str]] = None,
            gate_name: Optional[str] = None, mode: str = "real") -> Dict[str, Any]:
        """Orchestrate a full gate evaluation run. Returns decisions, summaries, matrix, filter."""
        from quality_gates.gate_policy import GATE_PRICE_BACKTEST, ALL_GATES
        effective_gate = gate_name or GATE_PRICE_BACKTEST
        decisions: List[Any] = []
        summaries: Dict[str, Any] = {}
        matrix: Dict[str, Any] = {}

        try:
            if tier:
                summary = self.evaluate_universe(tier, effective_gate, mode=mode)
                summaries[tier] = summary.to_dict() if hasattr(summary, "to_dict") else summary
                sym_list = self._resolve_tier_symbols(tier)
            elif symbols:
                sym_list = symbols
            else:
                sym_list = []

            for sym in sym_list:
                try:
                    dec = self.symbol_evaluator.evaluate(sym, effective_gate, mode=mode)
                    decisions.append(dec)
                except Exception as exc:
                    logger.warning("run: symbol %s gate %s failed: %s", sym, effective_gate, exc)

            execution_filter = self.build_execution_filter(decisions)
        except Exception as exc:
            logger.warning("run() failed: %s", exc)

        return {
            "decisions": [d.to_dict() if hasattr(d, "to_dict") else d for d in decisions],
            "decision_objects": decisions,
            "summaries": summaries,
            "matrix": matrix,
            "execution_filter": execution_filter if "execution_filter" in dir() else {},
            "gate_name": effective_gate,
            "tier": tier,
            "mode": mode,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "no_real_orders": True,
        }

    def allowed_symbols(self, decisions: List[Any]) -> List[str]:
        """Return ELIGIBLE_FORMAL symbol names only."""
        from quality_gates.gate_schema import DECISION_ELIGIBLE_FORMAL
        result = []
        for d in decisions:
            dd = d if isinstance(d, dict) else (d.to_dict() if hasattr(d, "to_dict") else {})
            if dd.get("decision") == DECISION_ELIGIBLE_FORMAL:
                result.append(dd.get("symbol", ""))
        return [s for s in result if s]

    def observational_symbols(self, decisions: List[Any]) -> List[str]:
        """Return ELIGIBLE_FORMAL + ELIGIBLE_OBSERVATIONAL symbol names."""
        from quality_gates.gate_schema import DECISION_ELIGIBLE_FORMAL, DECISION_ELIGIBLE_OBSERVATIONAL
        result = []
        for d in decisions:
            dd = d if isinstance(d, dict) else (d.to_dict() if hasattr(d, "to_dict") else {})
            if dd.get("decision") in (DECISION_ELIGIBLE_FORMAL, DECISION_ELIGIBLE_OBSERVATIONAL):
                result.append(dd.get("symbol", ""))
        return [s for s in result if s]

    def blocked_symbols(self, decisions: List[Any]) -> List[str]:
        """Return all BLOCKED symbol names."""
        from quality_gates.gate_schema import GATE_LEVEL_BLOCKED
        result = []
        for d in decisions:
            dd = d if isinstance(d, dict) else (d.to_dict() if hasattr(d, "to_dict") else {})
            if dd.get("gate_level") == GATE_LEVEL_BLOCKED:
                result.append(dd.get("symbol", ""))
        return [s for s in result if s]

    def demo_symbols(self, decisions: List[Any]) -> List[str]:
        """Return DEMO_ONLY symbol names."""
        from quality_gates.gate_schema import DECISION_DEMO_ONLY
        result = []
        for d in decisions:
            dd = d if isinstance(d, dict) else (d.to_dict() if hasattr(d, "to_dict") else {})
            if dd.get("decision") == DECISION_DEMO_ONLY:
                result.append(dd.get("symbol", ""))
        return [s for s in result if s]

    def _resolve_tier_symbols(self, tier: str) -> List[str]:
        """Try to resolve symbols for a tier via universe package. Graceful degradation."""
        try:
            from universe.universe_tier_registry import UniverseTierRegistry
            reg = UniverseTierRegistry()
            tier_map = {"core10": "CORE_10", "research30": "RESEARCH_30",
                        "expanded50": "EXPANDED_50", "broad100": "BROAD_100"}
            tier_key = tier_map.get(tier.lower(), tier.upper())
            tier_def = reg.get_tier(tier_key)
            if tier_def and hasattr(tier_def, "symbols"):
                return list(tier_def.symbols)
        except Exception as exc:
            logger.warning("Could not resolve symbols for tier=%s: %s", tier, exc)
        return []
