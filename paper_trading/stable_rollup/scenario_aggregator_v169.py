"""
paper_trading/stable_rollup/scenario_aggregator_v169.py
Scenario aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict

VERSION = "1.6.9"


def run() -> Dict[str, Any]:
    """Aggregate scenario registry stats."""
    try:
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry, validate_registry
        registry = get_registry()
        total = len(registry)
        passed = sum(1 for s in registry if s.get("expected_status") == "PASS")
        failed = sum(1 for s in registry if s.get("expected_status") == "FAIL")

        categories: Dict[str, int] = {}
        for s in registry:
            cat = s.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        val_result = validate_registry()
        status = "PASS" if (total >= 80 and val_result["status"] == "PASS") else "DEGRADED"

        return {
            "name": "scenario_aggregator_v169",
            "version": VERSION,
            "total": total,
            "passed": passed,
            "failed": failed,
            "categories": categories,
            "status": status,
            "validation_status": val_result["status"],
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
    except Exception as exc:
        return {
            "name": "scenario_aggregator_v169",
            "version": VERSION,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "categories": {},
            "status": "DEGRADED",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
