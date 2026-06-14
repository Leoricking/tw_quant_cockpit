"""
quality_gates.gate_query — GateQuery v1.1.4

Read-only query interface for quality gate results.
Research Only. No Real Orders.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True


class GateQuery:
    """Read-only query interface over stored gate decisions."""

    def __init__(self, store=None):
        self._store = store

    @property
    def store(self):
        if self._store is None:
            from quality_gates.gate_store import GateStore
            self._store = GateStore()
        return self._store

    def latest_symbol_decisions(self) -> List[Dict]:
        """Return latest stored symbol decisions."""
        try:
            return self.store.load_decisions()
        except Exception as exc:
            logger.warning("GateQuery.latest_symbol_decisions failed: %s", exc)
            return []

    def latest_universe_summary(self) -> Optional[Dict]:
        """Return latest stored universe summary."""
        try:
            return self.store.load_universe_summary()
        except Exception as exc:
            logger.warning("GateQuery.latest_universe_summary failed: %s", exc)
            return None

    def get_decision(self, decision_id: str) -> Optional[Dict]:
        """Find a decision by ID."""
        try:
            for d in self.store.load_decisions():
                if d.get("decision_id") == decision_id:
                    return d
        except Exception as exc:
            logger.warning("GateQuery.get_decision failed: %s", exc)
        return None

    def list_formal_eligible(self) -> List[Dict]:
        """Return decisions where gate_level == FORMAL."""
        from quality_gates.gate_schema import GATE_LEVEL_FORMAL
        return [d for d in self.latest_symbol_decisions()
                if d.get("gate_level") == GATE_LEVEL_FORMAL]

    def list_observational(self) -> List[Dict]:
        """Return OBSERVATIONAL decisions."""
        from quality_gates.gate_schema import GATE_LEVEL_OBSERVATIONAL
        return [d for d in self.latest_symbol_decisions()
                if d.get("gate_level") == GATE_LEVEL_OBSERVATIONAL]

    def list_demo_only(self) -> List[Dict]:
        """Return DEMO decisions."""
        from quality_gates.gate_schema import GATE_LEVEL_DEMO
        return [d for d in self.latest_symbol_decisions()
                if d.get("gate_level") == GATE_LEVEL_DEMO]

    def list_blocked(self) -> List[Dict]:
        """Return BLOCKED decisions."""
        from quality_gates.gate_schema import GATE_LEVEL_BLOCKED
        return [d for d in self.latest_symbol_decisions()
                if d.get("gate_level") == GATE_LEVEL_BLOCKED]

    def list_by_reason(self, reason_code: str) -> List[Dict]:
        """Return decisions containing a specific reason code."""
        import json
        result = []
        for d in self.latest_symbol_decisions():
            codes_raw = d.get("reason_codes", "[]")
            try:
                codes = json.loads(codes_raw) if isinstance(codes_raw, str) else codes_raw
            except Exception:
                codes = []
            if reason_code in codes:
                result.append(d)
        return result

    def list_by_gate(self, gate_name: str) -> List[Dict]:
        """Return decisions for a specific gate."""
        return [d for d in self.latest_symbol_decisions()
                if d.get("gate_name") == gate_name]

    def gate_matrix(self, tier: Optional[str] = None) -> Dict:
        """Return stored gate matrix, optionally filtered by tier."""
        try:
            matrix = self.store.load_gate_matrix()
            if tier:
                # Filter by symbols in tier if possible
                try:
                    from universe.universe_tier_registry import UniverseTierRegistry
                    reg = UniverseTierRegistry()
                    tier_map = {"core10": "CORE_10", "research30": "RESEARCH_30",
                                "expanded50": "EXPANDED_50", "broad100": "BROAD_100"}
                    tier_key = tier_map.get(tier.lower(), tier.upper())
                    tier_def = reg.get_tier(tier_key)
                    if tier_def and hasattr(tier_def, "symbols"):
                        syms = set(tier_def.symbols)
                        matrix = {k: v for k, v in matrix.items() if k in syms}
                except Exception:
                    pass
            return matrix
        except Exception as exc:
            logger.warning("GateQuery.gate_matrix failed: %s", exc)
            return {}

    def compare_runs(self, run_a: List[Dict], run_b: List[Dict]) -> Dict:
        """Compare two decision lists and report changes."""
        map_a = {(d.get("symbol"), d.get("gate_name")): d.get("gate_level") for d in run_a}
        map_b = {(d.get("symbol"), d.get("gate_name")): d.get("gate_level") for d in run_b}
        improved, degraded = [], []
        order = ["FORMAL", "OBSERVATIONAL", "DEMO", "BLOCKED", "UNKNOWN"]
        for key in set(map_a) | set(map_b):
            a = map_a.get(key, "UNKNOWN")
            b = map_b.get(key, "UNKNOWN")
            if a != b:
                a_idx = order.index(a) if a in order else 99
                b_idx = order.index(b) if b in order else 99
                entry = {"symbol": key[0], "gate": key[1], "from": a, "to": b}
                if b_idx < a_idx:
                    improved.append(entry)
                else:
                    degraded.append(entry)
        return {"improved": improved, "degraded": degraded}

    def list_overrides(self) -> List[Dict]:
        """Return override records (read-only)."""
        try:
            import csv
            path = self.store._path("gate_overrides.csv")
            import os
            if not os.path.exists(path):
                return []
            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
            return rows
        except Exception as exc:
            logger.warning("GateQuery.list_overrides failed: %s", exc)
            return []
