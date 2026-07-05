"""
paper_trading/stable_rollup/contract_aggregator_v169.py
Contract aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict

VERSION = "1.6.9"


def run() -> Dict[str, Any]:
    """Run all contract validations and aggregate results."""
    try:
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().run()
        total_checks = result.get("total_validations", 0)
        passed = result.get("passed_validations", 0)
        failed = total_checks - passed
        status = "PASS" if result.get("all_pass", False) else "FAIL"
        return {
            "name": "contract_aggregator_v169",
            "version": VERSION,
            "total_checks": total_checks,
            "passed": passed,
            "failed": failed,
            "status": status,
            "all_pass": result.get("all_pass", False),
            "details": result.get("results", []),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
    except Exception as exc:
        return {
            "name": "contract_aggregator_v169",
            "version": VERSION,
            "total_checks": 0,
            "passed": 0,
            "failed": 0,
            "status": "DEGRADED",
            "all_pass": False,
            "details": [],
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
