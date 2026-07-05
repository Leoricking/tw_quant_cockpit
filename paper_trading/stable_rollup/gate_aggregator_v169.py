"""
paper_trading/stable_rollup/gate_aggregator_v169.py
Gate aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, List

VERSION = "1.6.9"

_GATE_TARGETS = [
    ("release.operational_integration_hardening_release_gate_v168", "OperationalIntegrationReleaseGate", "operational_integration_gate_v168"),
    ("release.paper_performance_attribution_release_gate_v167", "PaperAttributionReleaseGate", "paper_attribution_gate_v167"),
    ("release.multi_session_coordination_release_gate_v166", "MultiSessionCoordinationReleaseGate", "multi_session_gate_v166"),
    ("release.live_paper_trading_stable_rollup_release_gate_v169", "StableRollupReleaseGate", "stable_rollup_gate_v169"),
]


def _try_run_gate(module_path: str, class_name: str, label: str) -> Dict[str, Any]:
    try:
        import importlib
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        result = cls().run()
        passed = result.get("passed", 0)
        failed = result.get("failed", 0)
        total = result.get("total", passed + failed)
        gate_passed = result.get("gate_passed", failed == 0)
        status = result.get("status", "PASS" if gate_passed else "FAIL")
        return {
            "gate_name": label,
            "version": result.get("target_version", ""),
            "passed": passed,
            "failed": failed,
            "total": total,
            "gate_passed": gate_passed,
            "status": status,
            "source_module": module_path,
            "error": None,
        }
    except ImportError:
        return {
            "gate_name": label,
            "version": "",
            "passed": 0,
            "failed": 0,
            "total": 0,
            "gate_passed": False,
            "status": "DEGRADED",
            "source_module": module_path,
            "error": "ImportError",
        }
    except Exception as exc:
        return {
            "gate_name": label,
            "version": "",
            "passed": 0,
            "failed": 0,
            "total": 0,
            "gate_passed": False,
            "status": "DEGRADED",
            "source_module": module_path,
            "error": str(exc),
        }


def run() -> Dict[str, Any]:
    summaries: List[Dict[str, Any]] = []

    for module_path, class_name, label in _GATE_TARGETS:
        summary = _try_run_gate(module_path, class_name, label)
        summaries.append(summary)

    total_gates = len(summaries)
    passed_gates = sum(1 for s in summaries if s["gate_passed"])
    failed_gates = sum(1 for s in summaries if not s["gate_passed"] and s["status"] == "FAIL")
    degraded_gates = sum(1 for s in summaries if s["status"] == "DEGRADED")
    all_pass = passed_gates == total_gates

    if all_pass:
        status = "PASS"
    elif failed_gates > 0:
        status = "FAIL"
    else:
        status = "DEGRADED"

    return {
        "name": "gate_aggregator_v169",
        "version": VERSION,
        "total_gates": total_gates,
        "passed_gates": passed_gates,
        "failed_gates": failed_gates,
        "degraded_gates": degraded_gates,
        "all_pass": all_pass,
        "status": status,
        "summaries": summaries,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
    }
