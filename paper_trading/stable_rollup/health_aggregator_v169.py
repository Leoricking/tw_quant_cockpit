"""
paper_trading/stable_rollup/health_aggregator_v169.py
Health aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, List

VERSION = "1.6.9"

_HEALTH_TARGETS = [
    ("paper_trading.health_v160", "LivePaperTradingHealthCheck", "live_paper_trading_v160"),
    ("paper_trading.operations.health_v163", "SessionOperationsObservabilityHealthCheck", "session_operations_v163"),
    ("paper_trading.analytics.health_v164", "OperationalAnalyticsReviewHealthCheck", "operational_analytics_v164"),
    ("paper_trading.performance_attribution.health_v167", "PaperAttributionHealthCheck", "paper_attribution_v167"),
    ("paper_trading.operational_integration.health_v168", "OperationalIntegrationHealthCheck", "integration_v168"),
    ("paper_trading.stable_rollup.health_v169", "StableRollupHealthCheck", "stable_rollup_v169"),
]


def _try_run_health(module_path: str, class_name: str, label: str) -> Dict[str, Any]:
    try:
        import importlib
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        result = cls().run()
        passed = result.get("passed", 0)
        failed = result.get("failed", 0)
        total = result.get("total", passed + failed)
        status = result.get("status", "PASS" if failed == 0 else "FAIL")
        return {
            "health_name": label,
            "version": result.get("version", ""),
            "passed": passed,
            "failed": failed,
            "total": total,
            "status": status,
            "blocking": failed > 0,
            "source_module": module_path,
            "error": None,
        }
    except ImportError:
        return {
            "health_name": label,
            "version": "",
            "passed": 0,
            "failed": 0,
            "total": 0,
            "status": "DEGRADED",
            "blocking": False,
            "source_module": module_path,
            "error": "ImportError",
        }
    except Exception as exc:
        return {
            "health_name": label,
            "version": "",
            "passed": 0,
            "failed": 0,
            "total": 0,
            "status": "DEGRADED",
            "blocking": False,
            "source_module": module_path,
            "error": str(exc),
        }


def run() -> Dict[str, Any]:
    summaries: List[Dict[str, Any]] = []

    for module_path, class_name, label in _HEALTH_TARGETS:
        summary = _try_run_health(module_path, class_name, label)
        summaries.append(summary)

    total_healths = len(summaries)
    passed_healths = sum(1 for s in summaries if s["status"] == "PASS")
    failed_healths = sum(1 for s in summaries if s["status"] in ("FAIL",))
    degraded_healths = sum(1 for s in summaries if s["status"] == "DEGRADED")
    blocking_count = sum(1 for s in summaries if s.get("blocking", False))
    all_pass = (failed_healths == 0 and degraded_healths == 0)

    if all_pass:
        status = "PASS"
    elif blocking_count > 0:
        status = "FAIL"
    else:
        status = "DEGRADED"

    return {
        "name": "health_aggregator_v169",
        "version": VERSION,
        "total_healths": total_healths,
        "passed_healths": passed_healths,
        "failed_healths": failed_healths,
        "degraded_healths": degraded_healths,
        "blocking_count": blocking_count,
        "all_pass": all_pass,
        "status": status,
        "summaries": summaries,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
    }
